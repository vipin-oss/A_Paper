"""Final independent matched-point and artifact audit after run_checks.py.

Also writes expanded CSV columns and QA PNGs; never changes the computed
roots, physical input grid, H range, thresholds, or recommendation.
"""
from __future__ import annotations
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import numpy as np

import run_checks as r
from dispersion_screen import (conditioned_fields,conditioned_root,spatial_diagnostics,
                               strong_root,strong_energy,tracked_mode,ROOT)

HERE=Path(__file__).resolve().parent;OUT=HERE/'results';CACHE=HERE/'cache'
CACHE.mkdir(exist_ok=True)


def hook(d):
    return complex(d['real'],d['imag']) if set(d)=={'real','imag'} else d


def load(name):return json.loads((OUT/name).read_text(),object_hook=hook)


def main():
    data=load('screening.json');validation=load('validation.json')
    checks=[]
    def check(name,passed,detail=None):
        checks.append(dict(name=name,passed=bool(passed),detail=detail))
        if not passed:print('AUDIT FAILED',name,detail,flush=True)
    check('Main numerical checks all passed',validation['passed']==validation['total'])
    groups=[('operating_summary.csv','base'),('H_summary.csv','H_synthetic'),
            ('ordinary_parameter_controls.csv','ordinary_parameter_controls')]
    allcases=[]
    for name,key in groups:
        allcases+=data[key]
        r.csvwrite(name,[r.flat_summary(s) for s in data[key]])
    cases={s['case']['id']:s for s in allcases}
    check('12 base,72 nonzero H,16 ordinary probes',
          [len(data[k]) for _,k in groups]==[12,72,16])
    check('No extra carrier concentrations',set(s['case']['n0'] for s in allcases)=={2e18,1e19})
    check('No empirical H range or Maxwell proof claimed',data['H_physical_range'] is None and not data['full_Maxwell_validated'])
    check('No negative reflection claim',not data['negative_reflection_demonstrated'])
    for path,digest in load('retained_sha256.json').items():
        check('Retained '+path,hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest)
    for checkpoint in ['a0','a0r']:
        dd=json.loads((ROOT/checkpoint/'results/validation.json').read_text())
        check(checkpoint+' retained acceptance checks',dd['all_executed_checks_passed'],len(dd['checks']))
    selected_ids=list(data['selected'].values())
    check('Exactly primary and fallback',set(data['selected'])=={'primary','fallback'})
    forward_validation=[]
    for label,ident in data['selected'].items():
        s=cases[ident]
        check(label+' actual transport gate',s['midpoint']['transport_screen_pass'])
        check(label+' independent and convergence validation exists','validation' in s)
        check(label+' backward and forward exterior sheets',s['midpoint']['K'].real>0 and s['forward_midpoint']['K'].real>0)
        p=r.make_plate(s['case']);fm=s['forward_midpoint'];K=fm['K'];Om=fm['Omega_drive'];e=fm['transport']
        ir=strong_root(p,'spatial',Om,K);ie=strong_energy(p,K,Om)
        dk=abs(ir['value']-K)
        check(label+' independent forward spatial',ir['converged'] and dk<2e-7,dk)
        check(label+' passive positive-energy forward port',K.real>0 and K.imag>0 and e['power']>0 and e['mean_energy']>0)
        row=dict(case=ident,label=label,independent_K_delta=dk)
        for key in ['power','mean_energy','dissipation']:
            relative=abs(ie[key]-e[key])/max(abs(e[key]),1e-30)
            check(label+' independent forward '+key,relative<1e-6,relative)
            row['relative_'+key+'_delta']=relative
        check(label+' independent forward energy balance',ie['spatial_balance_relative']<1e-5,ie['spatial_balance_relative'])
        kk=[];converged=True
        for degree in [24,28,32]:
            pr=r.make_plate(s['case'],degree);rr=conditioned_root(pr,Om,K)
            kk.append(rr['K']);converged=converged and rr['converged']
        spread=max(abs(z-kk[-1]) for z in kk)
        check(label+' forward degree convergence',converged and spread<2e-7,spread)
        row['degree_K_max_delta']=spread;forward_validation.append(row)
    r.csvwrite('selected_forward_validation.csv',forward_validation)
    # Direct independent check at the SAME reference K and SAME driving frequency
    # as the H=0 comparison, not merely at each case's shifted interval midpoint.
    matched=[]
    for s in data['H_synthetic']+data['ordinary_parameter_controls']:
        if s['case']['base_id'] not in selected_ids:continue
        m=s['matched_H0'];p=r.make_plate(s['case'])
        it=strong_root(p,'temporal',m['reference_K'],m['omega'])
        delta=abs(it['value']-m['omega'])*r.scale_hz(p)
        check(s['case']['id']+': independent matched-K pole',it['converged'] and delta<1,delta)
        row=dict(case=s['case']['id'],matched_complex_frequency_delta_Hz=delta)
        if m['fixed_drive_root_resolved']:
            K=m['fixed_drive']['K'];ir=strong_root(p,'spatial',m['fixed_drive']['Omega_drive'],K)
            dk=abs(K-ir['value'])
            check(s['case']['id']+': independent matched-drive root',ir['converged'] and dk<2e-7,dk)
            row['matched_complex_K_delta']=dk
        matched.append(row)
    r.csvwrite('matched_point_validation.csv',matched)
    # Reconstruct positive-sheet energies to audit classification and retain
    # positive stored-energy and dissipation columns. Existing roots are reused.
    plates={}
    with (OUT/'spatial_port_screen.csv').open() as file:ports=list(csv.DictReader(file))
    changed=0;minimum_energy=float('inf');maximum_residual=0.;maximum_balance=0.
    for row in ports:
        ident=row['case'];s=cases[ident]
        if ident not in plates:plates[ident]=r.make_plate(s['case'])
        p=plates[ident];K=complex(float(row['K_real']),float(row['K_imag']))
        if K.real<=0:
            row['stored_energy_dimensionless']='';row['dissipation_dimensionless']=''
            continue
        Om=float(row['frequency_Hz'])/r.scale_hz(p)
        diag=spatial_diagnostics(p,K,Om);e=diag['transport']
        row['stored_energy_dimensionless']=e['mean_energy'];row['dissipation_dimensionless']=e['dissipation']
        if (row['admissible_backward']=='True')!=diag['admissible_backward']:changed+=1
        if (row['transport_screen_pass']=='True')!=diag['transport_screen_pass']:changed+=1
        minimum_energy=min(minimum_energy,e['mean_energy'])
        maximum_residual=max(maximum_residual,max(diag['residuals'].values()))
        maximum_balance=max(maximum_balance,e['spatial_balance_relative'])
    check('Explicit positive-energy guard changes no classification',changed==0,changed)
    check('All reconstructed positive-sheet stored energies positive',minimum_energy>0,minimum_energy)
    r.csvwrite('spatial_port_screen.csv',ports)
    check('Expected temporal/spatial grid sizes',validation['temporal_rows']==15100 and len(ports)==10100)
    # Ordinary printed-scale probes are not measured confidence intervals.
    for key in ['ha','hb','hc']:
        for eta in [-.1,.1,-.5,.5]:
            hs=[s['H_SI'] for s in data['H_synthetic'] if s['case']['H_direction']==key and s['case']['eta_reference']==eta]
            check(f'Fixed physical H {key} {eta:+g}',all(np.array_equal(x,hs[0]) for x in hs))
    # Re-render with the zero-H point included and without hiding very lossy H
    # points below a preselected log-axis floor. QA PNGs stay ignored.
    with (OUT/'temporal_dispersion.csv').open() as file:
        r.TRACE_ROWS=[dict(case=z['case'],K=float(z['K']),frequency_Hz=float(z['frequency_Hz'])) for z in csv.DictReader(file)]
    r.PORT_ROWS=[dict(case=z['case'],grid_index=int(z['grid_index']),survival_100um=float(z['survival_100um']) if z['survival_100um'] else None) for z in ports]
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    original=Figure.savefig
    def save(self,path,*args,**kwargs):
        result=original(self,path,*args,**kwargs)
        original(self,CACHE/(Path(path).stem+'.png'),dpi=150)
        return result
    Figure.savefig=save
    try:r.figures(data['base'],data['H_synthetic'],{k:cases[v] for k,v in data['selected'].items()})
    finally:Figure.savefig=original;plt.close('all')
    tests={}
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1')
    for folder,expected in [('a0s',22),('a0r',16),('a0',12)]:
        cmd=[sys.executable,'-m','unittest','discover','-s',folder,'-p','test_*.py','-v']
        ans=subprocess.run(cmd,cwd=ROOT,env=env,text=True,capture_output=True)
        log=ans.stdout+ans.stderr;(CACHE/(folder+'_final_tests.log')).write_text(log)
        count=re.search(r'Ran (\d+) tests?',log);n=int(count[1]) if count else 0
        check(folder+' final tests',ans.returncode==0 and n==expected,n)
        tests[folder]=dict(count=n,exit_code=ans.returncode)
    filehashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in [HERE/'protocol.json',HERE/'dispersion_screen.py',HERE/'run_checks.py',HERE/'test_a0s.py',HERE/'audit_outputs.py']}
    r.dump('final_audit.json',dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
        matched_points=len(matched),selected_forward_validation=forward_validation,
        tests=tests,retained_checks=dict(a0=52,a0r=65),
        minimum_reconstructed_stored_energy=minimum_energy,
        all_positive_sheet_maximum_strong_residual=maximum_residual,
        all_positive_sheet_maximum_energy_balance=maximum_balance,source_sha256=filehashes,
        main_checks=dict(passed=validation['passed'],total=validation['total']),
        recommendation='REVISE',stop_after='A0-S'))
    print('Final A0-S audit',sum(c['passed'] for c in checks),'/',len(checks),flush=True)
    return 0 if all(c['passed'] for c in checks) else 1

if __name__=='__main__':raise SystemExit(main())
