"""Reproduce the bounded A0-S screen. Never runs an edge/scattering solver.

Run with OPENBLAS_NUM_THREADS=1 using the retained pinned environment.
Numerical controls and H are synthetic unless explicitly sourced in protocol.
"""
from __future__ import annotations
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
import time
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

from dispersion_screen import (ROOT,ComplexPlate,SI,CONST,derived, mass_mac,
    longitudinal_cutoff,tracked_mode,conditioned_root,conditioned_fields,
    spatial_diagnostics,strong_root,strong_energy,conditioned_scalar,radiation_screen)

HERE=Path(__file__).resolve().parent
OUT=HERE/'results';OUT.mkdir(exist_ok=True)
PROTOCOL=json.loads((HERE/'protocol.json').read_text())
DEGREE=PROTOCOL['numerics']['base_degree']
HSTEP=PROTOCOL['branch_domain']['finite_difference_h']
CHECKS=[]
TRACE_ROWS=[];PORT_ROWS=[];CONVERGENCE=[];INDEPENDENT=[];MATCHED=[]


def clean(value):
    if isinstance(value,complex):return {'real':float(value.real),'imag':float(value.imag)}
    if isinstance(value,np.generic):return clean(value.item())
    if isinstance(value,np.ndarray):return [clean(x) for x in value]
    if isinstance(value,dict):return {str(k):clean(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(x) for x in value]
    return value


def dump(name,value):
    (OUT/name).write_text(json.dumps(clean(value),indent=2,allow_nan=False)+'\n')


def csvwrite(name,rows):
    if not rows:return
    keys=list(dict.fromkeys(key for row in rows for key in row))
    with (OUT/name).open('w',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=keys);writer.writeheader();writer.writerows(rows)


def check(name,condition,detail=None):
    CHECKS.append(dict(name=name,passed=bool(condition),detail=clean(detail)))
    if not condition:print('CHECK FAILED:',name,detail,flush=True)


def make_plate(case,degree=DEGREE):
    return ComplexPlate(degree=degree,d=case['d'],n0=case['n0'],ell=case['ell'],
                        H=case.get('H',[0,0,0]),overrides=case['overrides'])


def scale_hz(plate):return plate.sc['cs']/(2*np.pi*plate.sc['d'])


def fd(plate,K,ref,h=HSTEP):
    def f(k):return tracked_mode(plate,k,ref)['omega']
    if K>=2*h:
        vals=[f(K+j*h) for j in [-2,-1,0,1,2]]
        d1=(vals[0]-8*vals[1]+8*vals[3]-vals[4])/(12*h)
        d2=(-vals[0]+16*vals[1]-30*vals[2]+16*vals[3]-vals[4])/(12*h*h)
    else:
        vals=[f(K+j*h) for j in range(5)]
        d1=(-25*vals[0]+48*vals[1]-36*vals[2]+16*vals[3]-3*vals[4])/(12*h)
        d2=(35*vals[0]-104*vals[1]+114*vals[2]-56*vals[3]+11*vals[4])/(12*h*h)
    return d1,d2


def trace_branch(plate):
    ks=np.linspace(0,PROTOCOL['branch_domain']['K_max'],151)
    modes=[longitudinal_cutoff(plate)];modes[0]['MAC']=1.
    for K in ks[1:]:modes.append(tracked_mode(plate,K,modes[-1]))
    omega=np.array([m['omega'] for m in modes])
    if min(m['MAC'] for m in modes)<PROTOCOL['branch_domain']['minimum_allowed_MAC']:
        raise RuntimeError('MAC continuation below preregistered threshold; no automatic branch substitution.')
    candidates=np.where((omega[1:-1].real<omega[:-2].real)&(omega[1:-1].real<omega[2:].real))[0]+1
    if not len(candidates):raise RuntimeError('No closed first minimum in fixed domain; unresolved, not nonexistence.')
    j=int(candidates[0]);ref=modes[j]
    def derivative(K):return fd(plate,float(K),ref)[0].real
    left,right=ks[j-1],ks[j+1]
    Kz=brentq(derivative,left,right,xtol=2e-9)
    mz=tracked_mode(plate,Kz,ref)
    slope,curvature=fd(plate,Kz,mz)
    curvhalf=fd(plate,Kz,mz,h=HSTEP/2)[1]
    Omid=(omega[0].real+mz['omega'].real)/2
    # Solve the real-frequency projection; it is only a seed for complex k.
    Kb=brentq(lambda k:tracked_mode(plate,k,mz)['omega'].real-Omid,0,Kz,xtol=2e-10)
    mb=tracked_mode(plate,Kb,mz)
    jf=np.where((ks>Kz)&(omega.real>Omid))[0]
    if not len(jf):raise RuntimeError('No forward projection partner in fixed K domain.')
    hi=ks[int(jf[0])]
    Kf=brentq(lambda k:tracked_mode(plate,k,mz)['omega'].real-Omid,Kz,hi,xtol=2e-10)
    mf=tracked_mode(plate,Kf,mz)
    return dict(K=ks,modes=modes,omega=omega,Kz=Kz,mz=mz,curvature=curvature,
                curvature_step_discrepancy=abs(curvature-curvhalf),Omid=Omid,
                Kb=Kb,mb=mb,Kf=Kf,mf=mf,min_MAC=min(m['MAC'] for m in modes))


def initial_spatial(plate,trace,direction):
    K=trace['Kb'] if direction=='backward' else trace['Kf']
    mode=trace['mb'] if direction=='backward' else trace['mf']
    slope=fd(plate,K,mode)[0]
    seed=complex(K,-mode['omega'].imag/slope.real)
    first=conditioned_root(plate,trace['Omid'],seed)
    if first['converged']:return first
    # A different local seed is a numerical fallback, not a new material case.
    dz=np.sqrt(2*(trace['Omid']-trace['mz']['omega'])/trace['curvature'])
    second=conditioned_root(plate,trace['Omid'],trace['Kz']+(-dz if direction=='backward' else dz))
    return second if second['scalar_residual']<first['scalar_residual'] else first


def segments(rows,flag):
    good=[j for j,r in enumerate(rows) if r.get(flag,False)]
    groups=[]
    for j in good:
        if not groups or j>groups[-1][-1]+1:groups.append([j])
        else:groups[-1].append(j)
    answer=[]
    for group in groups:
        a,b=group[0],group[-1]
        answer.append(dict(first_grid_index=a,last_grid_index=b,
            first_frequency_Hz=rows[a]['frequency_Hz'],last_frequency_Hz=rows[b]['frequency_Hz'],
            lower_boundary_bracket_Hz=[rows[max(a-1,0)]['frequency_Hz'],rows[a]['frequency_Hz']],
            upper_boundary_bracket_Hz=[rows[b]['frequency_Hz'],rows[min(b+1,len(rows)-1)]['frequency_Hz']],
            lower_domain_edge=a==0,upper_domain_edge=b==len(rows)-1))
    return answer


def evaluate(case,save_rows=True):
    plate=make_plate(case);trace=trace_branch(plate);sc=scale_hz(plate)
    ident=case['id']
    if save_rows:
        for K,mode in zip(trace['K'],trace['modes']):
            TRACE_ROWS.append(dict(case=ident,K=float(K),omega_real=mode['omega'].real,
                omega_imag=mode['omega'].imag,frequency_Hz=mode['omega'].real*sc,
                power_FWHM_Hz=-2*mode['omega'].imag*sc,MAC=mode['MAC']))
    rootb=initial_spatial(plate,trace,'backward');rootf=initial_spatial(plate,trace,'forward')
    nfreq=PROTOCOL['real_frequency_port_screen']['fractions']
    oms=np.linspace(trace['mz']['omega'].real,trace['omega'][0].real,nfreq)
    imid=nfreq//2;roots={imid:rootb}
    for sequence in [range(imid-1,-1,-1),range(imid+1,nfreq)]:
        previous=rootb['K']
        for j in sequence:
            rr=conditioned_root(plate,float(oms[j]),previous)
            roots[j]=rr
            if rr['converged']:previous=rr['K']
    ports=[]
    for j,Om in enumerate(oms):
        rr=roots[j]
        if rr['converged']:
            diag=spatial_diagnostics(plate,rr['K'],float(Om))
        else:
            diag=dict(K=rr['K'],Omega_drive=float(Om),admissible_backward=False,
                      transport_screen_pass=False,numerically_unresolved=True)
        diag.update(grid_index=j,frequency_Hz=float(Om*sc),case=ident)
        ports.append(diag)
        if save_rows:
            e=diag.get('transport',{});r=diag.get('residuals',{});rad=diag.get('radiation',{})
            PORT_ROWS.append(dict(case=ident,grid_index=j,frequency_Hz=float(Om*sc),
                K_real=rr['K'].real,K_imag=rr['K'].imag,root_converged=rr['converged'],
                root_scalar_residual=rr['scalar_residual'],
                admissible_backward=diag['admissible_backward'],transport_screen_pass=diag['transport_screen_pass'],
                energy_velocity_m_s=e.get('energy_velocity_m_s'),power_dimensionless=e.get('power'),
                energy_length_m=e.get('energy_1e_length_m'),amplitude_length_m=e.get('amplitude_1e_length_m'),
                wavelength_m=e.get('phase_wavelength_m'),survival_100um=e.get('power_fraction_100um'),
                survival_one_wavelength=e.get('power_fraction_one_phase_wavelength'),
                spatial_balance_relative=e.get('spatial_balance_relative'),
                momentum_residual=r.get('momentum'),gauss_residual=r.get('gauss'),carrier_residual=r.get('carrier'),
                traction_residual=r.get('traction'),double_traction_residual=r.get('double_traction'),
                vacuum_residual=r.get('vacuum'),blocking_residual=r.get('blocking'),
                above_light_line=rad.get('above_vacuum_phase_light_line'),
                relative_EM_exponent_change=rad.get('relative_EM_exponent_change')))
    midpoint=ports[imid]
    forward=spatial_diagnostics(plate,rootf['K'],trace['Omid']) if rootf['converged'] else dict(K=rootf['K'],numerically_unresolved=True)
    summary=dict(case=case,minimum_MAC=trace['min_MAC'],
        cutoff_Omega=trace['omega'][0],Kz=trace['Kz'],minimum_Omega=trace['mz']['omega'],
        projected_frequency_low_Hz=trace['mz']['omega'].real*sc,
        projected_frequency_high_Hz=trace['omega'][0].real*sc,
        projected_bandwidth_Hz=(trace['omega'][0].real-trace['mz']['omega'].real)*sc,
        projected_midpoint_frequency_Hz=trace['Omid']*sc,
        curvature_minimum=trace['curvature'],curvature_step_discrepancy=trace['curvature_step_discrepancy'],
        temporal_reference_K=trace['Kb'],temporal_reference_Omega=trace['mb']['omega'],
        temporal_power_FWHM_Hz=-2*trace['mb']['omega'].imag*sc,
        temporal_energy=plate.temporal_energy(trace['Kb'],trace['mb']['omega'],trace['mb']),
        midpoint=midpoint,forward_midpoint=forward,
        admitted_port_count=sum(r['admissible_backward'] for r in ports),
        transport_qualified_count=sum(r['transport_screen_pass'] for r in ports),
        unresolved_spatial_count=sum(not r['converged'] for r in roots.values()),
        backward_port_segments=segments(ports,'admissible_backward'),
        transport_segments=segments(ports,'transport_screen_pass'),
        frequency_grid_step_Hz=float((oms[1]-oms[0])*sc),
        maximum_temporal_growth=max(m['maximum_temporal_growth'] for m in trace['modes']),
        H_SI=list(plate.H_SI),Schur_fraction=float(plate.schur_fraction))
    check(ident+': MAC',trace['min_MAC']>=.98,trace['min_MAC'])
    check(ident+': finite interval',summary['projected_bandwidth_Hz']>1)
    check(ident+': passive temporal',summary['maximum_temporal_growth']<2e-7,summary['maximum_temporal_growth'])
    check(ident+': strict full3D Schur',plate.schur_fraction<1,plate.schur_fraction)
    check(ident+': resolved midpoint backward-family root',rootb['converged'],rootb)
    check(ident+': resolved midpoint forward root',rootf['converged'],rootf)
    print(ident,'width Hz',round(summary['projected_bandwidth_Hz'],3),
          'B ports',summary['admitted_port_count'],'transport',summary['transport_qualified_count'],
          'E100',midpoint.get('power_survival_100um'),flush=True)
    return summary,plate,trace


def compare_matched(summary,plate,trace,base,baseplate,basetrace):
    K=basetrace['Kb'];omega=tracked_mode(plate,K,basetrace['mb'])['omega']
    ref=base['midpoint']['K'];Om=basetrace['Omid']
    # Homotopy of the existing reciprocal H, at fixed drive, to preserve root identity.
    current=ref;ok=True
    H=np.array(summary['case'].get('H',[0,0,0]),float)
    if np.any(H):
        for t in np.linspace(0,1,9)[1:]:
            sub=dict(summary['case']);sub['H']=list(t*H)
            answer=conditioned_root(make_plate(sub),Om,current)
            if not answer['converged']:ok=False;break
            current=answer['K']
    else:
        answer=conditioned_root(plate,Om,current);ok=answer['converged'];current=answer['K']
    row=dict(case=summary['case']['id'],base_case=base['case']['id'],
             reference_K=K,omega=omega,frequency_shift_Hz=(omega.real-basetrace['mb']['omega'].real)*scale_hz(plate),
             FWHM_Hz=-2*omega.imag*scale_hz(plate),
             FWHM_change_Hz=-2*(omega.imag-basetrace['mb']['omega'].imag)*scale_hz(plate),
             own_projected_bandwidth_change_Hz=summary['projected_bandwidth_Hz']-base['projected_bandwidth_Hz'],
             own_curvature_change=summary['curvature_minimum']-base['curvature_minimum'],
             fixed_drive_Hz=Om*scale_hz(plate),fixed_drive_root_resolved=ok)
    if ok:row['fixed_drive']=spatial_diagnostics(plate,current,Om)
    summary['matched_H0']=row
    e=row.get('fixed_drive',{}).get('transport',{})
    MATCHED.append(dict(case=row['case'],base_case=row['base_case'],reference_K=K,
        frequency_shift_Hz=row['frequency_shift_Hz'],FWHM_change_Hz=row['FWHM_change_Hz'],
        own_bandwidth_change_Hz=row['own_projected_bandwidth_change_Hz'],
        own_curvature_real_change=row['own_curvature_change'].real,
        fixed_drive_root_resolved=ok,K_real=current.real,K_imag=current.imag,
        fixed_drive_energy_velocity_m_s=e.get('energy_velocity_m_s'),
        fixed_drive_energy_length_m=e.get('energy_1e_length_m'),
        fixed_drive_survival_100um=e.get('power_fraction_100um'),
        fixed_drive_survival_wavelength=e.get('power_fraction_one_phase_wavelength')))


def validate_selected(summary,plate,trace,label):
    case=summary['case'];ident=case['id'];Om=trace['Omid'];K=summary['midpoint']['K']
    # Same frequency, same physical constants and same H in all checks.
    strongt=strong_root(plate,'temporal',trace['Kb'],trace['mb']['omega'])
    strongs=strong_root(plate,'spatial',Om,K)
    dt=abs(strongt['value']-trace['mb']['omega'])*scale_hz(plate)
    dk=abs(strongs['value']-K)
    INDEPENDENT.append(dict(label=label,case=ident,kind='temporal',difference_Hz=dt,
        reference_real=trace['mb']['omega'].real,reference_imag=trace['mb']['omega'].imag,
        independent_real=strongt['value'].real,independent_imag=strongt['value'].imag,
        independent_boundary_singular=strongt['singular_relative']))
    INDEPENDENT.append(dict(label=label,case=ident,kind='spatial',difference_K=dk,
        reference_real=K.real,reference_imag=K.imag,
        independent_real=strongs['value'].real,independent_imag=strongs['value'].imag,
        independent_boundary_singular=strongs['singular_relative']))
    check(label+': independent temporal <1 Hz',strongt['converged'] and dt<1,dt)
    check(label+': independent spatial <2e-7',strongs['converged'] and dk<2e-7,dk)
    if K.real>0 and plate.ell_SI>0:
        ie=strong_energy(plate,K,Om)
        ge=summary['midpoint']['transport']
        for key in ['power','mean_energy','dissipation']:
            relative=abs(ie[key]-ge[key])/max(abs(ge[key]),1e-30)
            check(label+': independent '+key,relative<1e-6,relative)
            INDEPENDENT.append(dict(label=label,case=ident,kind='energy_'+key,
                relative_difference=relative,reference_real=ge[key],independent_real=ie[key]))
        check(label+': independent energy conservation',ie['spatial_balance_relative']<1e-5,ie)
    endpoint_deltas=[]
    for ek,em,ename in [(0,trace['modes'][0],'cutoff'),(trace['Kz'],trace['mz'],'minimum')]:
        ir=strong_root(plate,'temporal',ek,em['omega'])
        ed=abs(ir['value']-em['omega'])*scale_hz(plate);endpoint_deltas.append(ed)
        check(label+': independent '+ename,ir['converged'] and ed<1,ed)
        INDEPENDENT.append(dict(label=label,case=ident,kind=ename,difference_Hz=ed,
            reference_real=em['omega'].real,reference_imag=em['omega'].imag,
            independent_real=ir['value'].real,independent_imag=ir['value'].imag,
            independent_boundary_singular=ir['singular_relative']))
    ivals=[]
    for delta in [-2,-1,0,1,2]:
        kk=trace['Kz']+delta*HSTEP
        mm=tracked_mode(plate,kk,trace['mz'])
        ivals.append(strong_root(plate,'temporal',kk,mm['omega'])['value'])
    icurv=(-ivals[0]+16*ivals[1]-30*ivals[2]+16*ivals[3]-ivals[4])/(12*HSTEP**2)
    independent_curvature_delta=abs(icurv-trace['curvature'])
    check(label+': independent curvature',independent_curvature_delta<.005,independent_curvature_delta)
    frequencies=[];ks=[];curvatures=[];endpoint_frequencies=[]
    for p in PROTOCOL['numerics']['independent_degrees']:
        pp=make_plate(case,p)
        mm=pp.temporal_mode(trace['Kb'],near=trace['mb']['omega'])
        rr=conditioned_root(pp,Om,K)
        cc=fd(pp,trace['Kz'],pp.temporal_mode(trace['Kz'],near=trace['mz']['omega']))[1]
        diag=spatial_diagnostics(pp,rr['K'],Om)
        frequencies.append(mm['omega']);ks.append(rr['K']);curvatures.append(cc)
        oc=pp.temporal_mode(0,near=trace['omega'][0])['omega']
        oz=pp.temporal_mode(trace['Kz'],near=trace['mz']['omega'])['omega']
        endpoint_frequencies.append((oc,oz))
        CONVERGENCE.append(dict(label=label,case=ident,degree=p,
            omega_real=mm['omega'].real,omega_imag=mm['omega'].imag,
            K_real=rr['K'].real,K_imag=rr['K'].imag,
            curvature_real=cc.real,curvature_imag=cc.imag,
            cutoff_real=oc.real,cutoff_imag=oc.imag,minimum_real=oz.real,minimum_imag=oz.imag,
            bandwidth_Hz=(oc.real-oz.real)*scale_hz(pp),
            energy_length_m=diag.get('transport',{}).get('energy_1e_length_m'),
            energy_balance=diag.get('transport',{}).get('spatial_balance_relative')))
        check(f'{label}: p{p} spatial converged',rr['converged'],rr['scalar_residual'])
        check(f'{label}: p{p} strong BC residual',max(diag['residuals'].values())<1e-5,diag['residuals'])
        if 'transport' in diag:
            check(f'{label}: p{p} energy',diag['transport']['spatial_balance_relative']<1e-5,
                  diag['transport']['spatial_balance_relative'])
    uncertainty=dict(complex_frequency_max_degree_delta_Hz=max(abs(x-frequencies[-1])*scale_hz(plate) for x in frequencies),
        power_FWHM_max_degree_delta_Hz=max(2*abs(x.imag-frequencies[-1].imag)*scale_hz(plate) for x in frequencies),
        complex_K_max_degree_delta=max(abs(x-ks[-1]) for x in ks),
        curvature_max_degree_delta=max(abs(x-curvatures[-1]) for x in curvatures),
        curvature_step_discrepancy=summary['curvature_step_discrepancy'],
        independent_complex_frequency_delta_Hz=dt,independent_complex_K_delta=dk,
        independent_endpoints_max_delta_Hz=max(endpoint_deltas),
        independent_curvature_delta=independent_curvature_delta,
        bandwidth_max_degree_delta_Hz=max(abs((oc.real-oz.real)-(endpoint_frequencies[-1][0].real-endpoint_frequencies[-1][1].real))*scale_hz(plate) for oc,oz in endpoint_frequencies),
        frequency_reporting_floor_Hz=1,power_FWHM_reporting_floor_Hz=2)
    check(label+': degree convergence <1Hz',uncertainty['complex_frequency_max_degree_delta_Hz']<1,uncertainty)
    check(label+': spatial degree convergence',uncertainty['complex_K_max_degree_delta']<2e-7,uncertainty)
    summary['validation']=uncertainty


def flat_summary(s):
    case=s['case'];mid=s['midpoint'];e=mid.get('transport',{})
    forward=s['forward_midpoint'];fe=forward.get('transport',{})
    return dict(case=case['id'],kind=case['kind'],transport_source=case['carrier_id'],
        thickness_m=case['d'],n0_m_minus3=case['n0'],ell_m=case['ell'],
        H_direction=case.get('H_direction','zero'),eta_reference=case.get('eta_reference',0),
        H_a_J_m=s['H_SI'][0],H_b_J_m=s['H_SI'][1],H_c_J_m=s['H_SI'][2],
        Schur_fraction=s['Schur_fraction'],
        cutoff_Omega_real=s['cutoff_Omega'].real,cutoff_Omega_imag=s['cutoff_Omega'].imag,
        minimum_Omega_real=s['minimum_Omega'].real,minimum_Omega_imag=s['minimum_Omega'].imag,
        temporal_reference_Omega_real=s['temporal_reference_Omega'].real,
        temporal_reference_Omega_imag=s['temporal_reference_Omega'].imag,
        frequency_low_Hz=s['projected_frequency_low_Hz'],
        frequency_high_Hz=s['projected_frequency_high_Hz'],bandwidth_Hz=s['projected_bandwidth_Hz'],
        K_zgv=s['Kz'],curvature_real=s['curvature_minimum'].real,
        power_FWHM_Hz=s['temporal_power_FWHM_Hz'],
        K_back_real=mid['K'].real,K_back_imag=mid['K'].imag,
        energy_velocity_m_s=e.get('energy_velocity_m_s'),energy_length_m=e.get('energy_1e_length_m'),
        wavelength_m=e.get('phase_wavelength_m'),survival_100um=e.get('power_fraction_100um'),
        survival_one_wavelength=e.get('power_fraction_one_phase_wavelength'),
        admitted_port_count=s['admitted_port_count'],transport_qualified_count=s['transport_qualified_count'],
        unresolved_spatial_count=s['unresolved_spatial_count'],minimum_MAC=s['minimum_MAC'],
        K_forward_real=forward['K'].real,K_forward_imag=forward['K'].imag,
        forward_energy_velocity_m_s=fe.get('energy_velocity_m_s'),
        forward_energy_length_m=fe.get('energy_1e_length_m'),
        forward_survival_100um=fe.get('power_fraction_100um'),
        forward_survival_one_wavelength=fe.get('power_fraction_one_phase_wavelength'))


def figures(base_summaries,H_summaries,selected):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'svg.fonttype':'none'})
    fig,axes=plt.subplots(1,2,figsize=(12,4),constrained_layout=True)
    for s in base_summaries:
        if s['case']['kind']!='synthetic_gradient':continue
        rr=[r for r in TRACE_ROWS if r['case']==s['case']['id']]
        label=f"d={s['case']['d']*1e6:g} µm, {s['case']['carrier_id']}"
        axes[0].plot([r['K'] for r in rr],[(r['frequency_Hz']-s['projected_frequency_high_Hz'])/1e6 for r in rr],label=label)
        pp=[r for r in PORT_ROWS if r['case']==s['case']['id'] and r['survival_100um'] is not None]
        axes[1].plot([r['grid_index']/100 for r in pp],[r['survival_100um'] for r in pp],label=label)
    axes[0].set(xlabel='K = k d (real temporal sweep)',ylabel='f − own cutoff (MHz)',title='Synthetic A=ℓ²C, ℓ=50 nm; f=H=0')
    axes[1].set(xlabel='Fraction of own projected frequency bracket',ylabel='Energy survival at 100 µm',yscale='log',ylim=(1e-8,1.1),title='Actual complex-k backward-family roots')
    axes[1].axhline(.1,color='black',ls=':',label='Predeclared transport threshold')
    axes[0].legend(fontsize=7);axes[1].legend(fontsize=7)
    fig.savefig(OUT/'operating_regimes.svg');plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(13,4),constrained_layout=True)
    colors={'ha':'#1459a0','hb':'#be5420','hc':'#18805b'}
    for key,summary in selected.items():
        ident=summary['case']['id']
        for direction in ['ha','hb','hc']:
            rows=[s for s in H_summaries if s['case'].get('base_id')==ident and s['case'].get('H_direction')==direction]
            zero=dict(case=dict(eta_reference=0),matched_H0=dict(frequency_shift_Hz=0,FWHM_change_Hz=0,
                      fixed_drive=summary['midpoint']))
            rows=sorted(rows+[zero],key=lambda s:s['case']['eta_reference'])
            x=[s['case']['eta_reference'] for s in rows]
            axes[0].plot(x,[s['matched_H0']['frequency_shift_Hz']/1e6 for s in rows],marker='o',color=colors[direction],ls='-' if key=='primary' else '--',label=key+' '+direction)
            axes[1].plot(x,[s['matched_H0']['FWHM_change_Hz']/1e6 for s in rows],marker='o',color=colors[direction],ls='-' if key=='primary' else '--')
            axes[2].plot(x,[s['matched_H0'].get('fixed_drive',{}).get('power_survival_100um',float('nan')) for s in rows],marker='o',color=colors[direction],ls='-' if key=='primary' else '--')
    axes[0].set(xlabel='η relative to common reference Hcrit',ylabel='Matched-K Δf (MHz)',title='Synthetic H: no physical range')
    axes[1].set(xlabel='η relative to common reference Hcrit',ylabel='Matched-K Δ power FWHM (MHz)')
    positive=[s['matched_H0'].get('fixed_drive',{}).get('power_survival_100um',0)
              for s in H_summaries if s['case'].get('base_id') in [v['case']['id'] for v in selected.values()]]
    lower=10**(math.floor(math.log10(max(min([v for v in positive if v>0],default=1e-8),1e-290)))-1)
    axes[2].set(xlabel='η relative to common reference Hcrit',ylabel='Fixed-drive E(100 µm)',yscale='log',ylim=(lower,1.1))
    axes[0].legend(fontsize=7);axes[2].axhline(.1,color='black',ls=':')
    fig.savefig(OUT/'H_sensitivity.svg');plt.close(fig)


def main():
    started=time.time()
    retained=json.loads((OUT/'retained_sha256.json').read_text())
    for path,digest in retained.items():
        check('retained '+path,hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest)
    base=[];states={};H_results=[];controls=[]
    for carrier in PROTOCOL['carrier_cases']:
        for d in PROTOCOL['thickness_m']:
            for model in PROTOCOL['model_controls']:
                ident=f"{carrier['id']}_d{d*1e6:g}_{model['id']}"
                case=dict(id=ident,kind=model['id'],carrier_id=carrier['id'],d=d,n0=carrier['n0_m_minus3'],ell=model['ell_m'],
                    overrides=dict(electron_mobility=carrier['electron_mobility_m2_Vs'],electron_diffusivity=carrier['electron_diffusivity_m2_s']),H=[0,0,0])
                s,p,t=evaluate(case);base.append(s);states[ident]=(s,p,t)
    # Stable selection applies only to own-midpoint transport qualification.
    qualified=[s for s in base if s['case']['kind']=='synthetic_gradient' and s['midpoint']['transport_screen_pass']]
    qualified.sort(key=lambda s:s['midpoint']['power_survival_100um'],reverse=True)
    if len(qualified)>=2:
        if (qualified[0]['midpoint']['power_survival_100um']-qualified[1]['midpoint']['power_survival_100um']<.05
            and qualified[1]['case']['carrier_id']=='bulk_Hall_transfer'):
            qualified[:2]=qualified[1],qualified[0]
        selected=dict(primary=qualified[0],fallback=qualified[1])
    else:
        selected={}
        check('Two conditional transport-qualified cases available',False,len(qualified))
    for label,s in selected.items():validate_selected(*states[s['case']['id']],label)
    # Independently validate all 12 H=0 base cases (not just favorable ones).
    for s,p,t in states.values():
        rr=strong_root(p,'temporal',t['Kb'],t['mb']['omega'])
        delta=abs(rr['value']-t['mb']['omega'])*scale_hz(p)
        check(s['case']['id']+': independent temporal',rr['converged'] and delta<1,delta)
        INDEPENDENT.append(dict(label='all_base',case=s['case']['id'],kind='temporal',difference_Hz=delta,
            reference_real=t['mb']['omega'].real,reference_imag=t['mb']['omega'].imag,
            independent_real=rr['value'].real,independent_imag=rr['value'].imag,
            independent_boundary_singular=rr['singular_relative']))
        ss=strong_root(p,'spatial',t['Omid'],s['midpoint']['K'])
        deltaK=abs(ss['value']-s['midpoint']['K'])
        check(s['case']['id']+': independent spatial',ss['converged'] and deltaK<2e-7,deltaK)
        INDEPENDENT.append(dict(label='all_base',case=s['case']['id'],kind='spatial',difference_K=deltaK,
            reference_real=s['midpoint']['K'].real,reference_imag=s['midpoint']['K'].imag,
            independent_real=ss['value'].real,independent_imag=ss['value'].imag,
            independent_boundary_singular=ss['singular_relative']))
    for direction,vec in PROTOCOL['H_screen']['directions'].items():
        ref=ComplexPlate(degree=DEGREE,d=1e-6,n0=1e19,ell=50e-9,eta=1-1e-10,direction=vec)
        Hcrit=ref.H_SI/(1-1e-10)
        for baseline in [s for s in base if s['case']['kind']=='synthetic_gradient']:
            bs,bp,bt=states[baseline['case']['id']]
            for eta in PROTOCOL['H_screen']['eta_reference']:
                if eta==0:continue
                case=dict(baseline['case']);case.update(id=baseline['case']['id']+f'_{direction}_{eta:+g}',kind='H_synthetic',
                    base_id=baseline['case']['id'],H_direction=direction,eta_reference=eta,H=list(eta*Hcrit))
                s,p,t=evaluate(case);compare_matched(s,p,t,bs,bp,bt);H_results.append(s)
                if case['base_id'] in [v['case']['id'] for v in selected.values()]:
                    validate_selected(s,p,t,'H_'+case['id'])
    for label,baseline in selected.items():
        bs,bp,bt=states[baseline['case']['id']]
        variants=[]
        for name,delta in [('c33',.5e9),('c44',.05e9),('e33',.005)]:
            for sign in [-1,1]:variants.append((name+f'{sign:+}',{name:SI[name]+sign*delta}))
        for fraction in [.95,1.05]:variants.append(('MD_'+str(fraction),
            {key:baseline['case']['overrides'][key]*fraction for key in ['electron_mobility','electron_diffusivity']}))
        for name,overrides in variants:
            case=dict(baseline['case']);case['overrides']=dict(case['overrides'],**overrides)
            case.update(id=baseline['case']['id']+'_probe_'+name,kind='ordinary_parameter_probe',base_id=baseline['case']['id'])
            s,p,t=evaluate(case);compare_matched(s,p,t,bs,bp,bt);controls.append(s)
    allresults=base+H_results+controls
    for s in allresults:
        check(s['case']['id']+': no unresolved port roots',s['unresolved_spatial_count']==0,s['unresolved_spatial_count'])
    csvwrite('operating_summary.csv',[flat_summary(s) for s in base])
    csvwrite('H_summary.csv',[flat_summary(s) for s in H_results])
    csvwrite('ordinary_parameter_controls.csv',[flat_summary(s) for s in controls])
    csvwrite('temporal_dispersion.csv',TRACE_ROWS);csvwrite('spatial_port_screen.csv',PORT_ROWS)
    csvwrite('matched_controls.csv',MATCHED);csvwrite('complex_convergence.csv',CONVERGENCE)
    csvwrite('independent_propagator.csv',INDEPENDENT)
    figures(base,H_results,selected)
    dump('screening.json',dict(base=base,H_synthetic=H_results,ordinary_parameter_controls=controls,
        selected={k:v['case']['id'] for k,v in selected.items()},
        H_physical_range=None,full_Maxwell_validated=False,negative_reflection_demonstrated=False,
        recommendation='REVISE',novelty='NOVELTY UNRESOLVED'))
    dump('validation.json',dict(checks=CHECKS,passed=sum(c['passed'] for c in CHECKS),total=len(CHECKS),
        elapsed_seconds=time.time()-started,base_cases=len(base),H_synthetic_cases=len(H_results),
        parameter_probe_cases=len(controls),temporal_rows=len(TRACE_ROWS),spatial_rows=len(PORT_ROWS),
        recommendation='REVISE',stop_after='A0-S',
        research_gates=dict(physical_A_f_H_calibrated=False,thin_plate_transport_verified=False,
            closest_equations_available=False,full_Maxwell_radiation_validated=False,edge_scattering_done=False)))
    print(f"A0-S checks {sum(c['passed'] for c in CHECKS)}/{len(CHECKS)}; {time.time()-started:.1f}s; selection",{k:v['case']['id'] for k,v in selected.items()},flush=True)
    return 0 if all(c['passed'] for c in CHECKS) else 1

if __name__=='__main__':raise SystemExit(main())
