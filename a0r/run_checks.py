"""Reproduce the bounded A0-R correction; not an edge solver or paper pipeline."""
from __future__ import annotations
import csv
import hashlib
import itertools
import json
import platform
from pathlib import Path
import sys
import numpy as np
import scipy
from scipy.optimize import brentq

from complex_dispersion import (ComplexPlate, Plate, SI, derived,
                                independent_spatial_root, independent_temporal_root)
from dispersion import independent_classical_root
from constitutive_check import run as symbolic_run

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'a0r/results'
OUT.mkdir(parents=True,exist_ok=True)
PROTOCOL=json.loads((ROOT/'a0r/protocol.json').read_text())
OLD=json.loads((ROOT/'a0/results/validation.json').read_text())['candidate_classical_only']
KB=OLD['K_backward']; KF=OLD['K_forward']; TARGET=OLD['Omega_target']
DIRECTIONS={'ha':(1.,0.,0.),'hb':(0.,1.,0.),'hc':(0.,0.,1.)}


def plain(x):
    if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [plain(v) for v in x]
    if isinstance(x,np.ndarray):return plain(x.tolist())
    if isinstance(x,complex):return dict(real=float(x.real),imag=float(x.imag))
    if isinstance(x,np.generic):return x.item()
    return x


def csvwrite(name,rows):
    if not rows:raise ValueError(f'No rows for {name}')
    keys=list(dict.fromkeys(k for row in rows for k in row))
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)


def mac(p,u,v):
    return float(abs(np.vdot(u,p.M@v))**2/(np.vdot(u,p.M@u).real*np.vdot(v,p.M@v).real))


def temporal_numbers(p,om):
    fs=p.sc['frequency_scale_Hz']; gamma=-complex(om).imag*p.sc['cs']/p.sc['d']
    return dict(Omega_real=om.real,Omega_imag=om.imag,frequency_Hz=om.real*fs,
                gamma_s_minus1=gamma,temporal_amplitude_1e_s=1/gamma,
                temporal_energy_1e_s=1/(2*gamma),pole_HWHM_Hz=gamma/(2*np.pi),
                pole_power_FWHM_Hz=gamma/np.pi,
                pole_quality_factor=om.real*p.sc['cs']/p.sc['d']/(2*gamma))


def main():
    checks=[]
    def check(name,value,bound,sense='le'):
        value=float(value);bound=float(bound)
        passed=bool(np.isfinite(value) and (value<=bound if sense=='le' else value>=bound))
        checks.append(dict(name=name,value=value,bound=bound,sense=sense,passed=passed))
    retained=json.loads((OUT/'retained_a0_sha256.json').read_text())
    hashes={k:hashlib.sha256((ROOT/k).read_bytes()).hexdigest() for k in retained}
    check('Retained blueprint and five A0 source hashes unchanged',sum(hashes[k]!=v for k,v in retained.items()),0)
    symbolic=symbolic_run()

    # Complete the one-sided K->0 limit, independently of the old K=.005 floor.
    classical=Plate(20)
    group=lambda k:classical.modes(k,count=6)['group'][4]
    kz=brentq(group,.005,.08,xtol=1e-12)
    oz=float(classical.modes(kz,count=6)['omega'][4])
    o0=float(np.pi*np.sqrt((SI['c33']+SI['e33']**2/SI['kappa33'])/SI['c44']))
    fs=derived()['frequency_scale_Hz']
    ref=dict(K_zgv=kz,Omega_zgv=oz,Omega_cutoff_K_to_0=o0,
             frequency_zgv_Hz=oz*fs,frequency_cutoff_Hz=o0*fs,
             full_frozen_bandwidth_Hz=(o0-oz)*fs,
             checked_K_ge_0p005_bandwidth_Hz=(classical.modes(.005,count=6)['omega'][4]-oz)*fs,
             original_target_Omega=TARGET,original_target_Hz=TARGET*fs,
             original_target_fraction_of_full_window=(TARGET-oz)/(o0-oz),
             classical_model='f=A=H=0, frozen carriers; exact quasistatic vacuum')
    cutoff_galerkin=ComplexPlate().frozen_mode(0)['omega']
    check('K=0 parity Galerkin matches independent analytic thickness cutoff',abs(cutoff_galerkin-o0),2e-11)
    check('Original checked classical bandwidth independently recovered [Hz]',abs(ref['checked_K_ge_0p005_bandwidth_Hz']-OLD['bounded_backward_bandwidth_Hz']),.02)
    check('Full K->0 bandwidth strictly exceeds old checked bandwidth [Hz]',ref['full_frozen_bandwidth_Hz']-ref['checked_K_ge_0p005_bandwidth_Hz'],20000,'ge')
    independent_classical=[]
    for kval in [1e-4,KB,kz,KF,.08]:
        mode=ComplexPlate().frozen_mode(kval)
        ind=independent_classical_root(kval,mode['omega'])
        independent_classical.append(dict(K=kval,galerkin=mode['omega'],independent=ind))
    check('Independent classical six-state frequency agreement, max relative',max(x['independent']['relative_difference'] for x in independent_classical),1e-10)
    check('Classical six-state roots all converged',sum(not x['independent']['converged'] for x in independent_classical),0)
    frozen_rows=[]
    for k in np.linspace(0,.08,81):
        m=ComplexPlate(degree=20).frozen_mode(k)
        frozen_rows.append(dict(K=k,Omega=m['omega'],frequency_Hz=m['omega']*fs))
    csvwrite('full_classical_window.csv',frozen_rows)
    curv=(group(kz+1e-4)-group(kz-1e-4))/2e-4

    # Ensure formal Fourier continuation really agrees at real K and is analytic.
    a0=Plate(22,ell_rel=.05,eta=.5)
    cp=ComplexPlate(degree=22,ell=50e-9,eta=.5)
    old=a0.matrices(2.);new=cp.analytic_matrices(2.)
    u,p=cp.udofs,cp.pdofs
    errors=[np.linalg.norm(new[key]-old[key][np.ix_(u if key in ('Kuu','Kup','F') else p,
                                                                       u if key=='Kuu' else p)])/max(np.linalg.norm(new[key]),1e-30)
            for key in ['Kuu','Kup','P','F','L']]
    check('Analytic assembly matches old real-K matrices in selected parity',max(errors),1e-12)
    olddyn=a0.dynamic_modes(2.)
    got=cp.temporal_mode(2.,near=8.83)['omega']
    check('Finite-rate analytic parity recovers old A0 H333 temporal root',min(abs(olddyn['omega']-got)),2e-9)
    mix=ComplexPlate(degree=22,ell=50e-9,eta=.5,direction=(1.,.4,.3))
    a=mix.analytic_matrices(.08)
    check('All three H components satisfy real-K reciprocal Fnu=F^H',np.linalg.norm(a['Fnu']-a['F'].conj().T)/np.linalg.norm(a['F']),1e-12)
    z=.02-.004j;step=1e-5
    f=lambda w:mix.spatial_stiffness(w,7.5)[0]
    dx=(f(z+step)-f(z-step))/(2*step)
    dy=(f(z+1j*step)-f(z-1j*step))/(2j*step)
    check('Complex-K Cauchy-Riemann continuation check',np.linalg.norm(dx-dy)/np.linalg.norm(dx),2e-6)

    scenarios=[];temporal_rows=[];spatial_rows=[];nominal_roots=[]
    temporal_res=[];spatial_res=[];temporal_bal=[];spatial_bal=[]
    temporal_ind_errors=[];spatial_ind_errors=[];min_mac=1.;max_growth=-np.inf
    all_root_success=[];distinct=[]
    ns=PROTOCOL['scenarios_NOT_measured_samples']['carrier_concentration_m_minus3']
    ds=PROTOCOL['scenarios_NOT_measured_samples']['total_thickness_m']
    omega_grid=np.linspace(oz,o0,41)
    for n0 in ns:
        for d in ds:
            plate=ComplexPlate(degree=22,d=d,n0=n0)
            tm=plate.temporal_mode(KB)
            delta=tm['omega']-TARGET
            tr=plate.residuals(KB,tm['omega'],tm)
            te=plate.temporal_energy(KB,tm['omega'],tm)
            temporal_res.append(tr);temporal_bal.append(te['temporal_balance_relative'])
            ind=independent_temporal_root(KB,tm['omega'],d,n0)
            temporal_ind_errors.append(abs(ind['omega']-tm['omega']))
            row=dict(d_m=d,n0_m_minus3=n0,drive_frequency_Hz=TARGET*plate.sc['frequency_scale_Hz'],
                     full_frozen_bandwidth_Hz=(o0-oz)*plate.sc['frequency_scale_Hz'],
                     temporal=temporal_numbers(plate,tm['omega']),temporal_residuals=tr,
                     temporal_energy=te,temporal_independent=ind,derived=plate.sc)
            previous=None
            for k in np.linspace(0,.08,41):
                m=plate.temporal_mode(float(k))
                res=plate.residuals(k,m['omega'],m)
                bal=plate.temporal_energy(k,m['omega'],m)
                temporal_res.append(res);temporal_bal.append(bal['temporal_balance_relative'])
                max_growth=max(max_growth,m['maximum_temporal_growth'])
                if previous is not None:min_mac=min(min_mac,mac(plate,previous,m['U']))
                previous=m['U']
                temporal_rows.append(dict(d_m=d,n0_m_minus3=n0,K=k,**temporal_numbers(plate,m['omega']),
                                          **{f'residual_{key}':value for key,value in res.items()},
                                          energy_balance=bal['temporal_balance_relative']))

            def get_pair(om,seeds=None):
                sq=np.sqrt(complex(2*(om-oz-delta)/curv))
                seedlist=[kz-sq,kz+sq] if seeds is None else seeds
                found=[]
                for seed in seedlist:
                    r=plate.spatial_root(om,seed)
                    if not r['converged']:
                        # One bounded independent-method refinement, not a parameter hunt.
                        fallback=independent_spatial_root(om,seed,d,n0)
                        r=plate.spatial_root(om,fallback['K'])
                        r['used_independent_seed_refinement']=True
                    all_root_success.append(r['converged'])
                    found.append(r)
                distinct.append(abs(found[0]['K']-found[1]['K']))
                return found

            pair=get_pair(TARGET)
            row['spatial']=[]
            for label,r in zip(['continued_backward','continued_forward'],pair):
                kval=r['K'];m=plate.spatial_fields(kval,TARGET)
                sr=plate.residuals(kval,TARGET,m);spatial_res.append(sr)
                ii=independent_spatial_root(TARGET,kval,d,n0)
                spatial_ind_errors.append(abs(ii['K']-kval))
                info=dict(label=label,**r,residuals=sr,independent=ii)
                if r['exterior_decays']:
                    energy=plate.spatial_energy(kval,TARGET,m)
                    info['transport']=energy;spatial_bal.append(energy['spatial_balance_relative'])
                row['spatial'].append(info)
                nominal_roots.append(dict(d_m=d,n0_m_minus3=n0,label=label,K=kval,Omega=TARGET))
            prev=None;admissible_back=0
            for om in omega_grid:
                roots=get_pair(float(om),prev)
                prev=[r['K'] for r in roots]
                valid_back=False
                for label,r in zip(['continued_backward','continued_forward'],roots):
                    kval=r['K'];m=plate.spatial_fields(kval,float(om))
                    res=plate.residuals(kval,float(om),m);spatial_res.append(res)
                    record=dict(d_m=d,n0_m_minus3=n0,root_label=label,
                                Omega_drive=om,drive_frequency_Hz=om*plate.sc['frequency_scale_Hz'],
                                full_window_fraction=(om-oz)/(o0-oz),K_real=kval.real,K_imag=kval.imag,
                                root_converged=r['converged'],exterior_decays=r['exterior_decays'],
                                scalar_residual=r['scalar_residual'],
                                **{f'residual_{key}':value for key,value in res.items()})
                    if r['converged'] and r['exterior_decays']:
                        energy=plate.spatial_energy(kval,float(om),m)
                        spatial_bal.append(energy['spatial_balance_relative'])
                        record.update(energy)
                        valid_back |= energy['backward'] and energy['passive_direction']
                    spatial_rows.append(record)
                admissible_back+=int(valid_back)
            row['sampled_admissible_backward_frequencies']=admissible_back
            row['sampled_frequency_count']=len(omega_grid)
            scenarios.append(row)
            print(f"scenario d={d*1e6:g} um, n0={n0:.0e}: backward sheet-admissible at {admissible_back}/41 sampled frequencies",flush=True)

    csvwrite('temporal_dispersion.csv',temporal_rows)
    csvwrite('spatial_dispersion.csv',spatial_rows)
    compact=[]
    for s in scenarios:
        b,f=s['spatial'];t=s['temporal'];be=b.get('transport',{})
        compact.append(dict(d_m=s['d_m'],n0_m_minus3=s['n0_m_minus3'],
                            drive_frequency_Hz=s['drive_frequency_Hz'],full_frozen_bandwidth_Hz=s['full_frozen_bandwidth_Hz'],
                            **t,backward_K_real=b['K'].real,backward_K_imag=b['K'].imag,
                            backward_exterior_decays=b['exterior_decays'],
                            backward_flux_negative=be.get('backward',False),
                            backward_energy_length_m=be.get('energy_1e_length_m'),
                            backward_energy_velocity_m_s=be.get('energy_velocity_m_s'),
                            backward_power_fraction_10um=be.get('power_fraction_10um'),
                            backward_power_fraction_100um=be.get('power_fraction_100um'),
                            backward_power_fraction_1mm=be.get('power_fraction_1mm'),
                            backward_phase_wavelength_m=be.get('phase_wavelength_m'),
                            backward_power_fraction_one_wavelength=be.get('power_fraction_one_phase_wavelength'),
                            forward_K_real=f['K'].real,forward_K_imag=f['K'].imag,
                            forward_energy_length_m=f.get('transport',{}).get('energy_1e_length_m'),
                            sampled_admissible_backward_frequencies=s['sampled_admissible_backward_frequencies'],
                            sampled_frequency_count=s['sampled_frequency_count']))
    csvwrite('scenario_summary.csv',compact)
    check('All bounded spatial solves have verified small scalar residual',sum(not x for x in all_root_success),0)
    check('Two continued roots remain distinct (minimum |delta K|)',min(distinct),1e-4,'ge')
    check('Independent eight-state temporal frequency agreement, max |delta Omega|',max(temporal_ind_errors),2e-10)
    check('Independent eight-state spatial agreement, max |delta K|',max(spatial_ind_errors),2e-8)
    check('Temporal branch tracking minimum mass MAC',min_mac,.999,'ge')
    check('No resolved positive temporal growth in evaluated parity operators',max_growth,2e-6)
    for name,lim in dict(momentum=1e-8,gauss=1e-7,carrier=2e-6,traction=1e-8,
                         double_traction=1e-12,vacuum=1e-7,blocking=2e-6).items():
        check(f'All classical finite-carrier temporal strong/face residuals: {name}',max(x[name] for x in temporal_res),lim)
        check(f'All classical finite-carrier complex-K strong/face residuals: {name}',max(x[name] for x in spatial_res),lim)
    check('All temporal mean-energy dissipation identities',max(temporal_bal),1e-6)
    check('All admissible spatial roots: 2 Im(K) P = D',max(spatial_bal),2e-5)

    check('Independent eight-state temporal determinants are singular at every nominal root',
          max(x['temporal_independent']['singular_relative'] for x in scenarios),1e-9)
    check('Independent eight-state spatial determinants are singular at every nominal root',
          max(r['independent']['singular_relative'] for x in scenarios for r in x['spatial']),1e-9)
    energies=[r['transport'] for x in scenarios for r in x['spatial'] if 'transport' in r]
    check('Admissible classical spatial roots all have positive mean energy',min(e['mean_energy'] for e in energies),1.,'ge')
    check('Admissible classical spatial roots all dissipate in their energy direction',sum(not e['passive_direction'] for e in energies),0)
    check('All evaluated temporal thickness poles have decay, not growth',min(r['gamma_s_minus1'] for r in temporal_rows),0.,'ge')

    # Ordinary-parameter probes. The eight elastic/piezo corners are a declared
    # sensitivity box, not a measured confidence interval. A and f remain unknown.
    Hrows=[];probes=[];corners=[];Hres=[];Hbal=[];Hschur=[];Hmac=[];Hgrowth=[]
    probe_specs=[('c33',-.5e9),('c33',.5e9),('c44',-.05e9),('c44',.05e9),
                 ('e33',-.005),('e33',.005),('transport_joint_factor',.95),('transport_joint_factor',1.05)]
    limits=[]
    for K in [KB,2.]:
        baseline_plate=ComplexPlate(degree=30,ell=50e-9)
        baseline=baseline_plate.temporal_mode(K,near=7.5 if K<1 else 8.83)
        omega_base=baseline['omega']
        for component,direction in DIRECTIONS.items():
            for eta in PROTOCOL['synthetic_H_NOT_physical_calibration']['eta_values']:
                p=ComplexPlate(degree=30,ell=50e-9,eta=eta,direction=direction)
                m=p.temporal_mode(K,near=omega_base.real)
                rr=p.residuals(K,m['omega'],m);bb=p.temporal_energy(K,m['omega'],m)
                Hres.append(rr);Hbal.append(bb['temporal_balance_relative'])
                Hschur.append(p.schur_fraction);Hmac.append(mac(p,baseline['U'],m['U']))
                Hgrowth.append(m['maximum_temporal_growth'])
                Hrows.append(dict(K=K,component=component,eta=eta,
                                  H_a_J_m=p.H_SI[0],H_b_J_m=p.H_SI[1],H_c_J_m=p.H_SI[2],
                                  schur_fraction=p.schur_fraction,**temporal_numbers(p,m['omega']),
                                  delta_frequency_Hz=(m['omega'].real-omega_base.real)*fs,
                                  delta_FWHM_Hz=-2*(m['omega'].imag-omega_base.imag)*fs,
                                  mode_MAC=mac(p,baseline['U'],m['U']),
                                  **{f'residual_{k}':v for k,v in rr.items()},
                                  energy_balance=bb['temporal_balance_relative']))
                if eta:
                    f0=p.frozen_mode(K,near=omega_base.real)['omega']
                    f1=baseline_plate.frozen_mode(K,near=omega_base.real)['omega']
                    limits.append(abs(f0-f1))
        for param,change in probe_specs:
            over=({param:SI[param]+change} if param!='transport_joint_factor'
                  else {key:SI[key]*change for key in ['electron_mobility','electron_diffusivity']})
            p=ComplexPlate(degree=30,ell=50e-9,overrides=over)
            m=p.temporal_mode(K,near=omega_base.real)
            probes.append(dict(K=K,parameter=param,increment_or_factor=change,
                               **temporal_numbers(p,m['omega']),
                               delta_frequency_Hz=(m['omega'].real-omega_base.real)*fs,
                               delta_FWHM_Hz=-2*(m['omega'].imag-omega_base.imag)*fs))
        for signs in itertools.product([-1,1],repeat=3):
            over={name:SI[name]+sign*diff for name,diff,sign in zip(['c33','c44','e33'],[.5e9,.05e9,.005],signs)}
            p=ComplexPlate(degree=30,ell=50e-9,overrides=over)
            m=p.temporal_mode(K,near=omega_base.real)
            corners.append(dict(K=K,sign_c33=signs[0],sign_c44=signs[1],sign_e33=signs[2],
                                delta_frequency_Hz=(m['omega'].real-omega_base.real)*fs,
                                delta_FWHM_Hz=-2*(m['omega'].imag-omega_base.imag)*fs))
    csvwrite('synthetic_H_sensitivity.csv',Hrows)
    csvwrite('material_parameter_probes.csv',probes)
    csvwrite('material_rounding_box_corners.csv',corners)
    check('Full-3D Schur fraction of all synthetic H cases below one',max(Hschur),.6400000001)
    check('Frozen-carrier frequencies independent of all allowed H components',max(limits),1e-12)
    check('Synthetic H branch mass MAC relative to H=0',min(Hmac),.999,'ge')
    check('No resolved growth in synthetic H operators',max(Hgrowth),2e-6)
    for key,lim in dict(momentum=1e-7,gauss=1e-7,carrier=1e-6,traction=1e-7,
                        double_traction=1e-8,vacuum=1e-7,blocking=1e-6).items():
        check(f'All synthetic H strong/face residuals: {key}',max(x[key] for x in Hres),lim)
    check('All synthetic H mean-energy dissipation identities',max(Hbal),1e-6)

    # Check full synthetic A/H complex-K energy accounting, including tangential
    # hyperstress face power, without mistaking these forward roots for NR.
    Hspatial=[];Hspatial_convergence=[]
    for component,direction,eta in [('zero',(1.,0.,0.),0.),('ha',(1.,0.,0.),.8),
                                     ('hb',(0.,1.,0.),-.8),('hc',(0.,0.,1.),.8),
                                     ('mixed',(1.,.4,.3),.5)]:
        p=ComplexPlate(degree=30,ell=50e-9,eta=eta,direction=direction)
        tm=p.temporal_mode(2.,near=8.83);om=tm['omega'].real
        vg=(p.temporal_mode(2.001,near=8.83)['omega'].real-p.temporal_mode(1.999,near=8.83)['omega'].real)/.002
        r=p.spatial_root(om,2.-1j*tm['omega'].imag/vg)
        mode=p.spatial_fields(r['K'],om)
        rr=p.residuals(r['K'],om,mode);ee=p.spatial_energy(r['K'],om,mode)
        Hspatial.append(dict(component=component,eta=eta,Omega_drive=om,**r,residuals=rr,transport=ee))
        lower=ComplexPlate(degree=28,ell=50e-9,eta=eta,direction=direction)
        kr=lower.spatial_root(om,r['K'])['K']
        Hspatial_convergence.append(abs(kr-r['K']))
    check('Synthetic A/H complex-K roots all converged',sum(not r['converged'] for r in Hspatial),0)
    check('Synthetic A/H complex-K convergence p28->p30, max delta K',max(Hspatial_convergence),2e-8)
    for key,lim in dict(momentum=1e-7,gauss=1e-7,carrier=1e-6,traction=1e-7,
                        double_traction=1e-8,vacuum=1e-7,blocking=1e-6).items():
        check(f'Synthetic A/H complex-K strong/face residuals: {key}',max(r['residuals'][key] for r in Hspatial),lim)
    check('Synthetic A/H complex-K power identity including chemical/vacuum/face flux',max(r['transport']['spatial_balance_relative'] for r in Hspatial),1e-6)
    check('Synthetic A/H complex-K roots all have positive stored energy',min(r['transport']['mean_energy'] for r in Hspatial),1.,'ge')

    # Explicit convergence of complex roots and sensitive higher-order fields.
    convergence=[]
    for degree in [16,20,24,28,30]:
        p=ComplexPlate(degree=degree,d=3e-6,n0=1e19)
        t=p.temporal_mode(KB)
        refroot=next(x for x in nominal_roots if x['d_m']==3e-6 and x['n0_m_minus3']==1e19 and x['label']=='continued_forward')
        r=p.spatial_root(TARGET,refroot['K'])
        res=p.residuals(r['K'],TARGET,p.spatial_fields(r['K'],TARGET))
        convergence.append(dict(case='classical_finite_carrier',degree=degree,
                                temporal_Omega_real=t['omega'].real,temporal_Omega_imag=t['omega'].imag,
                                spatial_K_real=r['K'].real,spatial_K_imag=r['K'].imag,
                                **{f'spatial_{k}':v for k,v in res.items()}))
        for component,direction in DIRECTIONS.items():
            p=ComplexPlate(degree=degree,ell=50e-9,eta=.8,direction=direction)
            t=p.temporal_mode(2.,near=8.83)
            rr=p.residuals(2.,t['omega'],t)
            convergence.append(dict(case=f'synthetic_H_{component}',degree=degree,
                                    temporal_Omega_real=t['omega'].real,temporal_Omega_imag=t['omega'].imag,
                                    **{f'temporal_{k}':v for k,v in rr.items()}))
    csvwrite('complex_convergence.csv',convergence)
    freq_last_differences=[]
    for name in ['classical_finite_carrier','synthetic_H_ha','synthetic_H_hb','synthetic_H_hc']:
        items=[x for x in convergence if x['case']==name]
        delta=complex(items[-1]['temporal_Omega_real']-items[-2]['temporal_Omega_real'],
                      items[-1]['temporal_Omega_imag']-items[-2]['temporal_Omega_imag'])
        freq_last_differences.append(abs(delta)*fs)
    check('Last-degree temporal complex frequency convergence, max equivalent Hz',max(freq_last_differences),.1)
    crows=[x for x in convergence if x['case']=='classical_finite_carrier']
    deltaK=abs(complex(crows[-1]['spatial_K_real']-crows[-2]['spatial_K_real'],crows[-1]['spatial_K_imag']-crows[-2]['spatial_K_imag']))
    check('Last-degree classical spatial root convergence',deltaK,2e-8)

    # Limit checks keep physical H fixed as n0->0, rather than rescaling eta.
    fixedH=ComplexPlate(degree=30,ell=50e-9,eta=.8).H_SI
    dilute=[]
    for n0 in [1e19,1e17,1e15]:
        p=ComplexPlate(degree=30,ell=50e-9,n0=n0,H=fixedH)
        zero=ComplexPlate(degree=30,ell=50e-9,n0=n0)
        om=p.temporal_mode(2.,near=8.83)['omega'];om0=zero.temporal_mode(2.,near=8.83)['omega']
        dilute.append(dict(n0=n0,physical_H333_J_m=fixedH[0],schur_fraction=p.schur_fraction,
                           coupling_delta_Omega=abs(om-om0)))
    check('Carrier-free fixed-physical-H limit: contrast decreases at least 1000 fold',dilute[-1]['coupling_delta_Omega']/dilute[0]['coupling_delta_Omega'],.001)
    mobility=ComplexPlate(degree=30,ell=50e-9,H=fixedH,
                          overrides={'electron_mobility':SI['electron_mobility']*1e-6,
                                     'electron_diffusivity':SI['electron_diffusivity']*1e-6})
    om=mobility.temporal_mode(2.,near=8.83)['omega']
    frozen=mobility.frozen_mode(2.,near=8.83)['omega']
    check('Frozen-mobility recovery with H fixed: |Omega_dynamic-Omega_frozen|',abs(om-frozen),1e-6)
    numerical_floor=max(1.,10*max(freq_last_differences),10*max(temporal_ind_errors)*fs)
    # A small, declared eta=0.1 test is enough to ask whether the response is
    # numerically distinguishable; it is NOT claimed to be physically plausible.
    check('Synthetic ha eta=.1 frequency effect exceeds conservative numerical floor by 1000',
          min(abs(x['delta_frequency_Hz']) for x in Hrows if x['component']=='ha' and x['eta']==.1)/numerical_floor,1000,'ge')

    validation=dict(checkpoint='A0-R',date_local='2026-11-05',decision='REVISE',
                    novelty_status='NOVELTY UNRESOLVED',
                    research_gates=dict(actual_Qu_Appendix_C=False,physical_H_calibrated=False,
                                        nonzero_f_and_A_calibrated=False,negative_reflection_demonstrated=False),
                    environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
                    scope=PROTOCOL,retained_hashes_match=hashes==retained,symbolic=symbolic,
                    classical_window=ref,classical_independent=independent_classical,
                    scenarios=scenarios,convergence=convergence,carrier_free_fixed_physical_H=dilute,
                    synthetic_numerical_frequency_floor_Hz=numerical_floor,
                    independent_max_delta_Omega=max(temporal_ind_errors),
                    independent_max_delta_K=max(spatial_ind_errors),
                    minimum_temporal_tracking_MAC=min_mac,
                    all_temporal_residual_maxima={k:max(x[k] for x in temporal_res) for k in temporal_res[0]},
                    all_spatial_residual_maxima={k:max(x[k] for x in spatial_res) for k in spatial_res[0]},
                    all_synthetic_H_residual_maxima={k:max(x[k] for x in Hres) for k in Hres[0]},
                    temporal_balance_max=max(temporal_bal),spatial_balance_max=max(spatial_bal),
                    synthetic_H_balance_max=max(Hbal),synthetic_H_spatial=Hspatial,
                    synthetic_H_spatial_max_degree_delta_K=max(Hspatial_convergence),checks=checks,
                    check_count=len(checks),all_executed_checks_passed=all(x['passed'] for x in checks),
                    no_edge_solver=True,no_negative_reflection_claim=True,
                    stop_after_checkpoint=True)
    (OUT/'validation.json').write_text(json.dumps(plain(validation),indent=2,allow_nan=False)+'\n')
    make_plots(frozen_rows,temporal_rows,spatial_rows,Hrows,probes,corners,ref)
    failures=[x for x in checks if not x['passed']]
    print(json.dumps(dict(checks=len(checks),failed=failures,decision='REVISE'),indent=2),flush=True)
    if failures:raise SystemExit(1)


def make_plots(frozen_rows,temporal,spatial,H,probes,corners,ref):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
    colors={1e17:'#147d92',1e18:'#aa6900',1e19:'#a2385a'}
    fig,ax=plt.subplots(1,2,figsize=(11,4.3),constrained_layout=True)
    ax[0].plot([r['K'] for r in frozen_rows],[(r['frequency_Hz']-ref['frequency_zgv_Hz'])/1e3 for r in frozen_rows],color='#263c52',label='frozen classical')
    for n,c in colors.items():
        rows=[r for r in temporal if r['d_m']==1e-6 and r['n0_m_minus3']==n]
        ax[0].plot([r['K'] for r in rows],[(r['frequency_Hz']-ref['frequency_zgv_Hz'])/1e3 for r in rows],color=c,label=f'n0={n:.0e} m−3')
        ax[1].plot([r['K'] for r in rows],[r['pole_power_FWHM_Hz']/1e3 for r in rows],color=c)
    ax[0].axhspan(0,ref['full_frozen_bandwidth_Hz']/1e3,color='#d8dfe6',alpha=.5)
    ax[0].set(xlabel='K = k d (real)',ylabel='Re(f) − frozen f_ZGV (kHz)')
    ax[0].legend(fontsize=8)
    ax[1].axhline(ref['full_frozen_bandwidth_Hz']/1e3,color='#263c52',ls='--',label='full frozen bandwidth')
    ax[1].set(xlabel='K = k d (real)',ylabel='Isolated-pole power FWHM (kHz)',yscale='log')
    ax[1].legend(fontsize=8)
    fig.suptitle('FINITE-CARRIER CLASSICAL LIMIT: d = 1 μm, f_tensor = A = H = 0\nComplex temporal poles; not a negative-reflection result',fontsize=11)
    fig.savefig(OUT/'complex_temporal_dispersion.svg');plt.close(fig)

    fig,ax=plt.subplots(1,2,figsize=(11,4.3),constrained_layout=True)
    for n,c in colors.items():
        for label,ls in [('continued_backward','-'),('continued_forward',':')]:
            rows=[r for r in spatial if r['d_m']==1e-6 and r['n0_m_minus3']==n and r['root_label']==label]
            x=[r['full_window_fraction'] for r in rows]
            ax[0].plot(x,[r['K_real'] for r in rows],color=c,ls=ls,label=f'{n:.0e} '+('B continuation' if ls=='-' else 'F continuation'))
            ax[1].plot(x,[r['K_imag'] for r in rows],color=c,ls=ls)
    for a in ax:a.axhline(0,color='#263c52',lw=.8);a.set_xlabel('(f − frozen f_ZGV) / full frozen bandwidth')
    ax[0].axhspan(-.1,0,color='#d5d5d5',alpha=.45)
    ax[0].set(ylabel='Re(K)',ylim=(-.075,.12))
    ax[0].text(.03,-.069,'Re(K) ≤ 0: q_vac = K sheet is NOT decaying',fontsize=8)
    ax[0].legend(fontsize=7,ncol=2)
    ax[1].set_ylabel('Im(K)')
    fig.suptitle('COMPLEX SPATIAL ROOTS: real drive frequency, d = 1 μm, classical limit\nFormal continuation ≠ an admissible outgoing backward port',fontsize=11)
    fig.savefig(OUT/'complex_spatial_dispersion.svg');plt.close(fig)

    fig,ax=plt.subplots(1,2,figsize=(11,4.3),constrained_layout=True)
    for comp,c in zip(['ha','hb','hc'],['#147d92','#aa6900','#a2385a']):
        rows=[r for r in H if r['K']==2. and r['component']==comp]
        ax[0].plot([r['eta'] for r in rows],[r['delta_frequency_Hz']/1e6 for r in rows],'o-',color=c,label=comp)
        ax[1].plot([r['eta'] for r in rows],[r['delta_FWHM_Hz']/1e6 for r in rows],'o-',color=c,label=comp)
    pr=[r for r in probes if r['K']==2.];cr=[r for r in corners if r['K']==2.]
    for a,key in zip(ax,['delta_frequency_Hz','delta_FWHM_Hz']):
        values=[r[key]/1e6 for r in pr+cr]
        a.axhspan(min(values),max(values),color='#cbd3dc',alpha=.5,label='declared parameter probes')
        a.axhline(0,color='#263c52',lw=.7);a.set_xlabel('η: fraction of directional strict Schur bound')
        a.legend(fontsize=8)
    ax[0].set_ylabel('Δ Re(f) from H=0 (MHz)');ax[1].set_ylabel('Δ pole power FWHM from H=0 (MHz)')
    fig.suptitle('SYNTHETIC ONLY: ell = 50 nm, d = 1 μm, n0 = 10¹⁹ m⁻³, K = 2, f_tensor = 0\nStability-admissible H is NOT a measured or physically plausible range',fontsize=11)
    fig.savefig(OUT/'synthetic_H_vs_parameter_probes.svg');plt.close(fig)


if __name__=='__main__':main()
