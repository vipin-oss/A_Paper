"""Reproduce bounded A0 diagnostics and small audit artifacts.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 python a0/run_checks.py
No scattering or production-solver code is imported or modified.
"""
from __future__ import annotations

import csv
import importlib.metadata
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve
from scipy.optimize import brentq

from constitutive_check import run as symbolic_run
from dispersion import (Plate, SI, CONST, derived, elastic_matrix,
                        independent_classical_root, track_grid)

OUT = Path(__file__).resolve().parent / 'results'
OUT.mkdir(exist_ok=True)


def native(x):
    if isinstance(x, dict): return {str(k): native(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [native(v) for v in x]
    if isinstance(x, np.ndarray): return native(x.tolist())
    if isinstance(x, np.generic): return x.item()
    return x


def write_csv(name, rows):
    with (OUT/name).open('w', newline='') as f:
        w = csv.DictWriter(f, list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def dynamic_match(plate, K, reference, j):
    dy = plate.dynamic_modes(K)
    shapes = dy['V'][:2*plate.n]
    norm = np.real(np.sum(shapes.conj()*(plate.M@shapes), axis=0))
    mac = np.abs(reference['U'][:, j].conj()@plate.M@shapes)**2/norm
    index = int(np.argmax(mac))
    return dy, index, float(mac[index])


def main():
    checks = []
    def check(name, value, bound, sense='less'):
        passed = bool(value < bound) if sense == 'less' else bool(value > bound)
        checks.append(dict(name=name, value=float(value), criterion=f'{sense} than {bound}', passed=passed))

    symbolic = symbolic_run()
    c6 = elastic_matrix()
    check('positive ZnO elastic stiffness, smallest engineering-Voigt eigenvalue [Pa]',
          np.linalg.eigvalsh(c6)[0], 0., 'greater')
    check('6mm c66 relation relative discrepancy',
          abs(SI['c66']-(SI['c11']-SI['c12'])/2)/SI['c66'], 1e-14)
    sc = derived()
    reference = Plate(22)
    ks = np.linspace(.02, 12., 301)
    modes, minimum_mac = track_grid(reference, ks, count=10)
    check('minimum consecutive mass-MAC, bounded first-ten-branch scan', minimum_mac, .98, 'greater')
    grid_rows = [dict(K=float(k), branch=j+1, Omega=float(m['omega'][j]),
                      group_over_cs=float(m['group'][j]))
                 for k,m in zip(ks,modes) for j in range(10)]
    write_csv('classical_reference_dispersion.csv', grid_rows)

    # A bounded finer search on the lowest longitudinal-thickness-like branch.
    # Branch label 5 means ascending-frequency position near K=0, not an assumed S/A label.
    local = Plate(20)
    branch = 4
    gfun = lambda k: local.modes(k,count=6)['group'][branch]
    kzgv = brentq(gfun, .005, .08, xtol=1e-11)
    omega_zgv = float(local.modes(kzgv,count=6)['omega'][branch])
    omega_lo_k = float(local.modes(.005,count=6)['omega'][branch])
    target = (omega_lo_k+omega_zgv)/2
    ofun = lambda k: float(local.modes(k,count=6)['omega'][branch]-target)
    kb = brentq(ofun,.005,kzgv,xtol=2e-9)
    kf = brentq(ofun,kzgv,.08,xtol=2e-9)
    candidate = dict(K_backward=kb, K_forward=kf, K_zgv=kzgv,
                     Omega_target=target, Omega_zgv=omega_zgv,
                     Omega_at_K_0p005=omega_lo_k,
                     frequency_target_Hz=target*sc['frequency_scale_Hz'],
                     frequency_zgv_Hz=omega_zgv*sc['frequency_scale_Hz'],
                     bounded_backward_bandwidth_Hz=(omega_lo_k-omega_zgv)*sc['frequency_scale_Hz'],
                     qualification='ONLY f=A=H=0 frozen-carrier reference with exact quasistatic vacuum; NOT fixed-model feasibility or negative reflection')
    local_ks = np.linspace(.005,.08,201)
    fine_rows=[]
    for k in local_ks:
        m=local.modes(float(k),count=6)
        fine_rows.append(dict(K=k,Omega=m['omega'][branch],group_over_cs=m['group'][branch]))
    write_csv('classical_backward_window.csv',fine_rows)
    no_exterior = Plate(20, vacuum=False)
    no_exterior_groups = [no_exterior.modes(float(k), count=6)['group'][branch]
                          for k in local_ks]
    boundary_sensitivity = dict(
        control='local D.n=0 approximation instead of exact vacuum exterior',
        K_min=float(local_ks[0]), K_max=float(local_ks[-1]), points=len(local_ks),
        branch=5, minimum_group_over_cs=float(min(no_exterior_groups)),
        negative_group_points=int(np.sum(np.array(no_exterior_groups)<0)),
        note='A different electrical boundary model; no claim about all branches or wavenumbers.')

    candidate_diagnostics=[]
    for k in [kb,kf]:
        m=local.modes(k,count=6)
        dg=local.diagnostics(k,m['omega'][branch],m['U'][:,branch],m['Phi'][:,branch],m['N'][:,branch])
        independent=independent_classical_root(k,m['omega'][branch])
        candidate_diagnostics.append(dict(K=k,Omega=m['omega'][branch],
                                          group_over_cs=m['group'][branch],
                                          diagnostics=dg,independent_stroh=independent))
        check(f'classical strong mechanics at K={k:.6g}',dg['strong_mechanical_relative'],1e-8)
        check(f'classical strong Gauss at K={k:.6g}',dg['strong_gauss_relative'],1e-7)
        check(f'classical free traction at K={k:.6g}',dg['traction_relative'],1e-8)
        check(f'classical vacuum boundary at K={k:.6g}',dg['vacuum_bc_relative'],1e-8)
        check(f'independent Stroh frequency at K={k:.6g}',independent['relative_difference'],1e-9)
        check(f'group vs direct total power/energy at K={k:.6g}',
              abs(dg['energy_velocity']-m['group'][branch]),1e-9)
    check('backward reference energy flux sign',-candidate_diagnostics[0]['diagnostics']['direct_power'],0.,'greater')
    check('forward reference energy flux sign',candidate_diagnostics[1]['diagnostics']['direct_power'],0.,'greater')
    check('same-frequency pair relative mismatch',
          abs(candidate_diagnostics[0]['Omega']-candidate_diagnostics[1]['Omega'])/target,1e-9)

    # Finite drift-diffusion on the same classical limiting model: do NOT
    # discard the imaginary part and call this a lossless semiconductor.
    rm=local.modes(kb,count=6)
    dy, idx, mac=dynamic_match(local,kb,rm,branch)
    om=dy['omega'][idx]
    loss=dict(K=kb,Omega_real=om.real,Omega_imag=om.imag,mass_MAC=mac,
              temporal_decay_Hz=-om.imag*sc['frequency_scale_Hz'],
              frequency_shift_from_frozen_Hz=(om.real-target)*sc['frequency_scale_Hz'],
              decay_to_reference_bandwidth_ratio=-om.imag*sc['frequency_scale_Hz']/candidate['bounded_backward_bandwidth_Hz'],
              diagnostics=local.dynamic_diagnostics(kb,dy,idx))
    check('classical finite-carrier temporal passivity',float(np.max(dy['all_s'].real)),1e-7)
    check('classical dynamic energy-decay balance',loss['diagnostics']['energy_decay_identity_relative'],1e-7)
    for metric, limit in [('strong_mechanical_relative',1e-8),('strong_gauss_relative',1e-7),
                          ('traction_relative',1e-8),('vacuum_bc_relative',1e-8),
                          ('carrier_strong_relative',1e-7),('no_flux_boundary_relative',1e-7)]:
        check('classical finite-carrier '+metric,loss['diagnostics'][metric],limit)

    # Convergence of the very narrow classical backward feature.
    convergence=[]
    for degree in [10,14,18,22,26]:
        p=Plate(degree)
        m=p.modes(.01,count=6)
        dg=p.diagnostics(.01,m['omega'][branch],m['U'][:,branch],m['Phi'][:,branch],m['N'][:,branch])
        convergence.append(dict(case='classical',degree=degree,K=.01,branch=5,
                                Omega=m['omega'][branch],group_over_cs=m['group'][branch],
                                mechanical_residual=dg['strong_mechanical_relative'],
                                gauss_residual=dg['strong_gauss_relative'],traction_residual=dg['traction_relative']))
    check('classical p=18 to 22 frequency convergence',
          abs(convergence[2]['Omega']-convergence[3]['Omega'])/convergence[3]['Omega'],1e-9)
    check('classical p=18 to 22 group convergence',
          abs(convergence[2]['group_over_cs']-convergence[3]['group_over_cs']),1e-8)
    # Independent finite-difference derivative, deliberately larger than rounding noise.
    h=.0005
    finite_difference=(local.modes(.01+h,count=6)['omega'][branch]-local.modes(.01-h,count=6)['omega'][branch])/(2*h)
    analytic=local.modes(.01,count=6)['group'][branch]
    check('classical analytic group vs centered frequency derivative',abs(finite_difference-analytic),1e-7)

    sensitivity=[]
    syn_diag=[]
    K=2.
    frozen_omegas=[]
    for eta in [-.8,-.5,0.,.5,.8]:
        p=Plate(28,.05,eta)
        fm=p.modes(K,'frozen',count=6)
        eq=p.modes(K,'equilibrated',count=6)
        dm,dj,dmac=dynamic_match(p,K,fm,branch)
        frozen_omegas.append(fm['omega'][branch])
        sensitivity.append(dict(eta=eta,H333_J_m=p.h_SI,K=K,ell_over_d=.05,n0_m_minus3=p.sc['n0'],
                                branch=5,frozen_Omega=fm['omega'][branch],
                                equilibrated_Omega=eq['omega'][branch],
                                finite_mobility_Omega_real=dm['omega'][dj].real,
                                finite_mobility_Omega_imag=dm['omega'][dj].imag,
                                dynamic_mass_MAC=dmac,strict_Schur_margin=1-eta**2))
        if eta==.8:
            dd=p.diagnostics(K,eq['omega'][branch],eq['U'][:,branch],eq['Phi'][:,branch],eq['N'][:,branch],'equilibrated')
            dyn_dd=p.dynamic_diagnostics(K,dm,dj)
            syn_diag=[dict(case='equilibrated_synthetic',diagnostics=dd),
                      dict(case='finite_mobility_synthetic',diagnostics=dyn_dd)]
            check('synthetic equilibrated strong mechanics',dd['strong_mechanical_relative'],1e-6)
            check('synthetic equilibrated strong Gauss',dd['strong_gauss_relative'],1e-7)
            check('synthetic equilibrated generalized traction',dd['traction_relative'],1e-7)
            check('synthetic equilibrated double traction',dd['double_traction_over_stress_d'],1e-8)
            check('synthetic equilibrated total guided power including face hyperstress',
                  abs(dd['energy_velocity']-eq['group'][branch]),1e-9)
            check('synthetic finite-mobility carrier strong residual',dyn_dd['carrier_strong_relative'],1e-7)
            check('synthetic finite-mobility blocking boundary residual',dyn_dd['no_flux_boundary_relative'],1e-7)
            check('synthetic finite-mobility energy-decay balance',dyn_dd['energy_decay_identity_relative'],1e-7)
            check('synthetic finite-mobility temporal passivity',np.max(dm['all_s'].real),1e-7)
            for metric, limit in [('strong_mechanical_relative',1e-6),('strong_gauss_relative',1e-7),
                                  ('traction_relative',1e-7),('double_traction_over_stress_d',1e-8),
                                  ('vacuum_bc_relative',1e-8)]:
                check('synthetic finite-mobility '+metric,dyn_dd[metric],limit)
    check('H has exactly no effect with initially zero frozen carriers',np.ptp(frozen_omegas),1e-12)
    write_csv('synthetic_H_sensitivity.csv',sensitivity)

    for degree in [12,16,20,24,28]:
        p=Plate(degree,.05,.8)
        m=p.modes(K,'equilibrated',count=6)
        dg=p.diagnostics(K,m['omega'][branch],m['U'][:,branch],m['Phi'][:,branch],m['N'][:,branch],'equilibrated')
        convergence.append(dict(case='synthetic_equilibrated',degree=degree,K=K,branch=5,
                                Omega=m['omega'][branch],group_over_cs=m['group'][branch],
                                mechanical_residual=dg['strong_mechanical_relative'],
                                gauss_residual=dg['strong_gauss_relative'],traction_residual=dg['traction_relative']))
    check('synthetic p=24 to 28 frequency convergence',
          abs(convergence[-1]['Omega']-convergence[-2]['Omega'])/convergence[-1]['Omega'],1e-8)
    check('synthetic p=12 to 28 strong residual reduction',
          convergence[-1]['mechanical_residual']/convergence[-5]['mechanical_residual'],1e-4)
    write_csv('convergence.csv',convergence)
    dynamic_convergence=[]
    for degree in [16,20,24,28]:
        p=Plate(degree,.05,.8)
        fm=p.modes(2.,'frozen',count=6)
        dm,dj,_=dynamic_match(p,2.,fm,branch)
        dg=p.dynamic_diagnostics(2.,dm,dj)
        dynamic_convergence.append(dict(degree=degree,K=2.,eta=.8,branch=5,
            Omega_real=dm['omega'][dj].real,Omega_imag=dm['omega'][dj].imag,
            mechanical_residual=dg['strong_mechanical_relative'],gauss_residual=dg['strong_gauss_relative'],
            carrier_residual=dg['carrier_strong_relative'],blocking_residual=dg['no_flux_boundary_relative']))
    r0,r1=dynamic_convergence[1:3]
    delta_omega=abs(complex(r0['Omega_real']-r1['Omega_real'],r0['Omega_imag']-r1['Omega_imag']))
    check('synthetic finite-mobility p=20 to 24 complex-frequency convergence',
          delta_omega/abs(complex(r1['Omega_real'],r1['Omega_imag'])),1e-8)
    check('synthetic finite-mobility p=16 to 28 carrier-residual reduction',
          dynamic_convergence[-1]['carrier_residual']/dynamic_convergence[0]['carrier_residual'],1e-4)
    write_csv('dynamic_convergence.csv',dynamic_convergence)

    # Carrier-free limit, holding PHYSICAL H fixed as n0 -> 0. Holding eta fixed
    # instead would change H and is not a valid test of a fixed material law.
    carrier_free=[]
    frozen_reference=Plate(22,.05,.5).modes(2.,'frozen',count=6)['omega'][branch]
    for n0 in [1e19,1e17,1e15]:
        eta=.5*np.sqrt(n0/1e19)
        p=Plate(22,.05,eta,n0=n0)
        m=p.modes(2.,'equilibrated',count=6)
        carrier_free.append(dict(n0=n0,eta=eta,H333_J_m=p.h_SI,
                                  Omega=m['omega'][branch],
                                  relative_gap_to_frozen=abs(m['omega'][branch]-frozen_reference)/frozen_reference))
    check('fixed-physical-H carrier-free convergence',
          carrier_free[-1]['relative_gap_to_frozen']/carrier_free[0]['relative_gap_to_frozen'],1e-3)
    check('physical H unchanged during carrier-free limit',
          np.ptp([r['H333_J_m'] for r in carrier_free])/abs(carrier_free[0]['H333_J_m']),1e-14)

    # Explicit exception vs general non-equivalence after algebraic elimination.
    def relaxed(p):
        a=p.matrices(2.)
        return a['K']-a['R']@solve(a['A'],a['R'].conj().T,assume_a='pos'),a
    ph,p0=Plate(14,.05,.8),Plate(14,.05,0.)
    kh,ah=relaxed(ph);k0,_=relaxed(p0)
    naive=-ah['F']@solve(ph.W,ah['F'].conj().T,assume_a='pos')
    charged_gap=np.linalg.norm((kh-k0)-naive)/np.linalg.norm(naive)
    ph.sc['Q']=p0.sc['Q']=0.  # algebraic neutral limit, not another ZnO model
    knh,anh=relaxed(ph);kn0,_=relaxed(p0)
    neutral_gap=np.linalg.norm((knh-kn0)-naive)/np.linalg.norm(naive)
    check('charged elimination differs from constant local A renormalization',charged_gap,1e-6,'greater')
    check('neutral algebraic special case DOES reduce to A renormalization',neutral_gap,1e-10)

    summary=dict(
        scope='A0 only; no manuscript, edge scattering, production-solver changes, or full f != 0 ZnO feasibility claim',
        decision='REVISE',date_utc='2026-11-05',
        unresolved=['Fang full table and governing equations',
                    'Wei constitutive/carrier equations',
                    'Qu constitutive/chemical-potential equations and Appendix C',
                    'sourced ZnO flexoelectric tensor and gradient modulus',
                    'measured or independently justified H; novelty not established',
                    'strict global plane strain versus angle-resolved negative-reflection geometry'],
        environment=dict(python=platform.python_version(),
                         packages={k:importlib.metadata.version(k) for k in ['numpy','scipy','sympy','matplotlib']}),
        derived_SI=sc,elastic_eigenvalues_Pa=np.linalg.eigvalsh(c6),
        symbolic=symbolic,reference_scan=dict(K_min=.02,K_max=12.,points=301,
                                             branches=10,degree=22,minimum_mass_MAC=minimum_mac),
        candidate_classical_only=candidate,candidate_checks=candidate_diagnostics,
        electrical_boundary_sensitivity=boundary_sensitivity,
        classical_finite_carrier_warning=loss,
        classical_centered_group_derivative=finite_difference,
        sensitivity_is_SYNTHETIC_f_zero=sensitivity,synthetic_diagnostics=syn_diag,
        convergence=convergence,dynamic_convergence=dynamic_convergence,carrier_free_fixed_H=carrier_free,
        renormalization_test=dict(charged_relative_gap=charged_gap,neutral_relative_gap=neutral_gap),
        checks=checks,all_executed_checks_passed=all(r['passed'] for r in checks))
    (OUT/'validation.json').write_text(json.dumps(native(summary),indent=2,allow_nan=False)+'\n')

    # Clear scientific labels: plots are NOT evidence of the complete model.
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(7.8,4.8),layout='constrained')
    for j in range(6):
        ax.plot(ks,[m['omega'][j] for m in modes],lw=1.3,label=f'branch {j+1}')
    ax.set(xlabel=r'$K=kd$ (total thickness $d$)',ylabel=r'$\Omega=\omega d/c_s$',
           title='Classical lossless reference ONLY: f = A = H = 0; frozen carriers')
    ax.legend(ncols=3,frameon=False)
    ax.text(.98,.03,'ZnO: Zhang Table 1; quasistatic vacuum exterior',transform=ax.transAxes,ha='right',fontsize=9)
    fig.savefig(OUT/'classical_reference.svg');plt.close(fig)
    fig,ax=plt.subplots(figsize=(7.8,4.8),layout='constrained')
    omfine=np.array([r['Omega'] for r in fine_rows])
    delta=(omfine-omega_zgv)*sc['frequency_scale_Hz']/1e3
    ax.plot(local_ks,delta,color='#243f60')
    neg=np.array([r['group_over_cs'] for r in fine_rows])<0
    ax.plot(local_ks[neg],delta[neg],color='#c4423c',lw=3,label='negative total energy velocity')
    ax.scatter([kb,kf],[(target-omega_zgv)*sc['frequency_scale_Hz']/1e3]*2,color='#243f60',zorder=3)
    ax.set(xlabel=r'$K=kd$',ylabel=r'$(f-f_{ZGV})$ [kHz], $d=1\,\mu$m',
           title='Very narrow backward feature: CLASSICAL vacuum reference only')
    ax.legend(frameon=False)
    ax.text(.98,.05,'Not negative-reflection evidence.\nAt n0 = 1e19 m^-3, carrier decay exceeds the checked band.',
            transform=ax.transAxes,ha='right',fontsize=8)
    fig.savefig(OUT/'classical_backward_window.svg');plt.close(fig)
    fig,ax=plt.subplots(figsize=(7.8,4.8),layout='constrained')
    baseline=sensitivity[2]['equilibrated_Omega']
    etas=[r['eta'] for r in sensitivity]
    ax.plot(etas,[100*(r['equilibrated_Omega']/baseline-1) for r in sensitivity],'o-',label='instantaneously equilibrated (ideal limit)')
    dynamicbase=sensitivity[2]['finite_mobility_Omega_real']
    ax.plot(etas,[100*(r['finite_mobility_Omega_real']/dynamicbase-1) for r in sensitivity],'s-',label='finite sourced mobility (Re frequency)')
    ax.axhline(0,color='gray',lw=.7)
    ax.set(xlabel=r'Synthetic stability fraction $\eta=H_{333}/H_{crit}$',ylabel='Frequency shift from H = 0 [%]',
           title='SYNTHETIC sensitivity ONLY: f = 0; A = ell^2 C; ell/d = 0.05; K = 2')
    ax.legend(frameon=False)
    ax.text(.98,.03,'No measured ZnO H or gradient length is claimed.',transform=ax.transAxes,ha='right',fontsize=9)
    fig.savefig(OUT/'synthetic_H_sensitivity.svg');plt.close(fig)
    failures=[r['name'] for r in checks if not r['passed']]
    print(json.dumps(native(dict(decision='REVISE',checks=len(checks),failures=failures,
                                 candidate_classical_only=candidate,finite_carrier_warning=loss,
                                 sensitivity=sensitivity)),indent=2))
    if failures:
        raise SystemExit(1)


if __name__=='__main__':
    main()
