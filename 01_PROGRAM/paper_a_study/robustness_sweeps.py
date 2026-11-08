"""Robustness sweeps requested by the review: (A) carrier density over many decades,
(B) added structural (hysteretic) loss.  Same solver and same branch-following definition
of R_B as the main text (frequency follows the guided branch, L = 10 d, k_y d = 0.1298).
Usage: python3 robustness_sweeps.py A | B   -> figure_data/robustness_{A,B}.csv"""
import sys, csv, time
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_figure_data import KY0, K0, plate, operating_mode, spatial_root

def edge_RB(p, omega, Kg):
    try:
        r, _ = p.edge(KY0, float(omega), Kg, Kg, L=10.)
        return r
    except Exception:
        return None

def branch(p, ref, Ks):
    out = []
    for K in Ks:
        ref = p.temporal(float(K), ref, ky=KY0); out.append(ref)
    return out

def fold_scan(p, ref):
    """follow branch from K0 down; fold = minimum of Re omega; then fine raster of R_B around it."""
    Ks = np.linspace(K0, 0.44, 32)
    ms = branch(p, ref, Ks)
    om = np.array([m['omega'].real for m in ms]); i = int(np.argmin(om))
    Kf = float(Ks[i])
    Kr = np.linspace(Kf-0.012, Kf+0.012, 25)
    mr = branch(p, ms[i], Kr)
    rb = []
    for K, m in zip(Kr, mr):
        r = edge_RB(p, m['omega'].real, float(K))
        rb.append(np.nan if r is None else r['backward_reflection_self_power'])
    rb = np.array(rb); j = int(np.nanargmax(rb)) if np.isfinite(rb).any() else 0
    return Kf, Kr[j], rb[j], mr[j], ms[0]

def run_A():
    rows = []; ref = None
    n0s = [2e18*10**(0.25*i) for i in range(0, 23)]   # 2e18 ... ~ 6e23
    p0 = plate(0.0, n0=n0s[0]); ref = operating_mode(p0)
    for n0 in n0s:
        t = time.time(); p = plate(0.0, n0=n0)
        try:
            ref = p.temporal(K0, ref, ky=KY0)
            r0 = edge_RB(p, ref['omega'].real, K0)
            Kf, Kmax, Rmax, mm, back = fold_scan(p, ref)
            ref = ref  # keep operating-point reference for next n0
            ksp = spatial_root(p, mm['omega'].real, Kmax)
            rows.append(dict(n0=n0, Q=p.Q, wtau=None, f_op_GHz=ref['omega'].real*p.fscale/1e9,
                FWHM_op_MHz=-2*ref['omega'].imag*p.fscale/1e6,
                R_B_operating=None if r0 is None else r0['backward_reflection_self_power'],
                K_fold=Kf, K_max=Kmax, R_B_max=Rmax, f_max_GHz=mm['omega'].real*p.fscale/1e9,
                atten_dB_mm_at_max=4.343*2*abs(ksp.imag)/p.d/1000, seconds=time.time()-t))
        except Exception as e:
            rows.append(dict(n0=n0, Q=p.Q, error=repr(e)[:80]))
        print(rows[-1], flush=True)
    return rows

if __name__ == '__main__':
    which = sys.argv[1]
    rows = run_A() if which == 'A' else []
    keys = sorted({k for r in rows for k in r}, key=lambda k: list(rows[0]).index(k) if k in rows[0] else 99)
    with open(HERE/'figure_data'/f'robustness_{which}.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)


def run_A_refined(select=(0, 4, 8, 12, 16, 20)):
    """Same as run_A but with a finer fold search and a wider R_B raster at selected n0;
    the argmax is flagged if it falls on the edge of the raster (then R_B_max is a lower bound)."""
    rows = []; n0s = [2e18*10**(0.25*i) for i in range(0, 23)]
    p0 = plate(0.0, n0=n0s[0]); ref = operating_mode(p0)
    for idx, n0 in enumerate(n0s):
        p = plate(0.0, n0=n0); ref = p.temporal(K0, ref, ky=KY0)
        if idx not in select: continue
        Ks = np.linspace(K0, 0.44, 60); ms = branch(p, ref, Ks)
        om = np.array([m['omega'].real for m in ms]); i = int(np.argmin(om)); Kf = float(Ks[i])
        Kr = np.linspace(Kf-0.03, Kf+0.03, 41); mr = branch(p, ms[i], Kr)
        rb = np.array([np.nan if (r := edge_RB(p, m['omega'].real, float(K))) is None
                       else r['backward_reflection_self_power'] for K, m in zip(Kr, mr)])
        j = int(np.nanargmax(rb))
        rows.append(dict(n0=n0, Q=float(p.Q), K_fold=Kf, K_max=float(Kr[j]), R_B_max=float(rb[j]),
                         argmax_on_edge=bool(j in (0, len(Kr)-1)),
                         FWHM_at_max_MHz=float(-2*mr[j]['omega'].imag*p.fscale/1e6),
                         f_max_GHz=float(mr[j]['omega'].real*p.fscale/1e9)))
        print(rows[-1], flush=True)
    out = HERE/'figure_data'/'robustness_A_refined.csv'
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def edge_pick(p, omega):
    """edge solve with incident/backward ports picked from the roots at this real frequency."""
    waves, _, _ = p.waves(KY0, float(omega))
    inc = out = None
    for w in waves:
        K = w['K']; tol = 2e-8*max(1, abs(K))
        isout = (K.imag < -tol) or (abs(K.imag) <= tol and w['power'] < 0)
        if not (0.3 < K.real < 0.8): continue
        if (not isout) and w['power'] > 0 and (inc is None or abs(K.real-0.527) < abs(inc.real-0.527)): inc = K
        if isout and w['power'] < 0 and (out is None or abs(K.real-0.527) < abs(out.real-0.527)): out = K
    if inc is None or out is None: return None
    try:
        r, _ = p.edge(KY0, float(omega), inc, out, L=10.); return r
    except Exception:
        return None

def run_B(etas=(0.0, 1e-5, 1e-4, 1e-3, 1e-2)):
    """Hysteretic structural loss: C -> C(1 - i*eta) (time dependence exp(-i omega t)) (loss tangent eta, Q_mech = 1/eta) in the
    stiffness and the gradient stiffness; carriers as in the main text; real-frequency scan
    around the lossless fold frequency; R_B(f) maximised over the scan."""
    rows = []
    base = plate(0.0); ref = base.temporal(0.5269, operating_mode(base), ky=KY0)
    om0 = ref['omega'].real
    grid = np.r_[-np.logspace(-9, -2.5, 20)[::-1], 0., np.logspace(-9, -2.5, 20)]
    for eta in etas:
        p = plate(0.0); p.C = p.C*(1-1j*eta)
        best = (-1, None, None)
        for d in grid:
            r = edge_pick(p, om0*(1+d))
            if r is None: continue
            R = r['backward_reflection_self_power']
            if R > best[0]: best = (R, d, r)
        R, d, r = best
        rows.append(dict(eta=eta, R_B_max=R, rel_detuning=d, f_GHz=om0*(1+d)*p.fscale/1e9,
                         incident_ImK_d=r['incident_K'].imag, backward_ImK_d=r['backward_K'].imag,
                         total_outgoing=r['total_outgoing_self_power'], edge_residual=r['edge_scaled_residual']))
        print(rows[-1], flush=True)
    out = HERE/'figure_data'/'robustness_B.csv'
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
