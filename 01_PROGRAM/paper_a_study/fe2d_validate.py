"""Convergence of the direct 2D solution (fe2d.py) against the modal edge matching.

Writes figure_data/fe2d_validation.csv.  Usage: python3 fe2d_validate.py [which]
  which = op | fold | all   (default all)
"""
import sys, csv, time
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_figure_data import KY0, K0, KB0, OMEGA0, plate
from model import MeshPlate
from fe2d import Strip

OUT = HERE / 'figure_data' / 'fe2d_validation.csv'
FIELDS = ['case', 'zbasis', 'Lt', 'Ls', 'gamma', 'n_uniform', 'n_graded', 'first_len', 'spline_deg',
          'omega', 'RB_modal', 'RB_FE', 'rel_diff', 'amp_rel_diff', 'fit_residual', 'seconds']


def run(case, p, omega, Kinc, Ktar, **kw):
    r, d = p.edge(KY0, float(omega), Kinc, Ktar, L=10.)
    Y = d['Y']; K = d['K']; aa = d['amplitudes']; ib = d['index_backward']
    t = time.time()
    S = Strip(p, KY0, omega, **kw)
    S.solve(d['incident']['y'])
    a, res = S.fit(Y, K, -20., -4., nx=50)
    inc = np.exp(2 * d['incident']['K'].imag * 10.)
    Rb = float(-p.power(Y[:, ib], omega) * abs(a[ib]) ** 2 * np.exp(2 * K[ib].imag * 10.) / inc)
    Rm = r['backward_reflection_self_power']
    row = dict(case=case, zbasis=type(p).__name__ + f'({p.degree})', Lt=kw.get('Lt'), Ls=kw.get('Ls'),
               gamma=kw.get('gamma'), n_uniform=kw.get('n_uniform'), n_graded=kw.get('n_graded', 8),
               first_len=kw.get('first_len', 0.02), spline_deg=kw.get('degree', 4), omega=omega,
               RB_modal=Rm, RB_FE=Rb, rel_diff=(Rb - Rm) / Rm,
               amp_rel_diff=abs(a[ib] - aa[ib]) / abs(aa[ib]), fit_residual=res, seconds=time.time() - t)
    print({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items()}, flush=True)
    new = not OUT.exists()
    with open(OUT, 'a', newline='') as f:
        w = csv.DictWriter(f, FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    return row


BASE = dict(Lt=200., Ls=170., gamma=0.1, n_uniform=500, n_graded=8, first_len=0.02, degree=4)


def op():
    p = plate(0.0)
    run('op/base', p, OMEGA0, K0, KB0, **BASE)
    # absorbing layer
    run('op/longer', p, OMEGA0, K0, KB0, **{**BASE, 'Lt': 300., 'Ls': 260., 'n_uniform': 750})
    run('op/weaker', p, OMEGA0, K0, KB0, **{**BASE, 'gamma': 0.05})
    # x resolution and corner grading
    run('op/finer_x', p, OMEGA0, K0, KB0, **{**BASE, 'n_uniform': 800})
    run('op/quintic', p, OMEGA0, K0, KB0, **{**BASE, 'degree': 5})
    run('op/corner_x4', p, OMEGA0, K0, KB0, **{**BASE, 'first_len': 0.005, 'n_graded': 11})
    run('op/corner_x16', p, OMEGA0, K0, KB0, **{**BASE, 'first_len': 0.00125, 'n_graded': 14})
    # through-thickness space
    for deg in (14, 18):
        run('op/z_degree', plate(0.0, degree=deg), OMEGA0, K0, KB0, **BASE)
    for el in (12, 24):
        pm = MeshPlate(elements=el, H=0.0, edge_electric='insulating')
        run('op/z_hermite', pm, OMEGA0, K0, KB0, **BASE)
        run('op/z_hermite_corner_x4', pm, OMEGA0, K0, KB0, **{**BASE, 'first_len': 0.005, 'n_graded': 11})
        run('op/z_hermite_corner_x16', pm, OMEGA0, K0, KB0, **{**BASE, 'first_len': 0.00125, 'n_graded': 14})


def fold():
    from robustness_sweeps import fold_scan, edge_RB
    p = plate(0.0)
    ref = p.temporal(K0, None, ky=KY0)
    from build_figure_data import operating_mode
    ref = operating_mode(p)
    Kf, Kb, Rb, m, _ = fold_scan(p, ref)
    om = float(m['omega'].real)
    print('fold: Kf', Kf, 'K at max', Kb, 'R_B', Rb, 'omega', om, flush=True)
    run('fold/base', p, om, Kb, Kb, **BASE)
    run('fold/longer', p, om, Kb, Kb, **{**BASE, 'Lt': 300., 'Ls': 260., 'n_uniform': 750})
    run('fold/corner_x4', p, om, Kb, Kb, **{**BASE, 'first_len': 0.005, 'n_graded': 11})


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if which in ('op', 'all'):
        op()
    if which in ('fold', 'all'):
        fold()
