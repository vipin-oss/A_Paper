import sys, json
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
from build_figure_data import KY0, operating_mode, plate
from robustness_sweeps import edge_pick
base = plate(0.0); ref = base.temporal(0.5269, operating_mode(base), ky=KY0); om0 = ref['omega'].real
def R(p, d):
    r = edge_pick(p, om0*(1+d)); return None if r is None else r['backward_reflection_self_power']
out = []
for eta in (0.0, 1e-5, 1e-4):
    p = plate(0.0); p.C = p.C*(1-1j*eta)
    lo, hi = -3e-3, 3e-3; hist = []
    for lvl in range(4):
        g = np.linspace(lo, hi, 81); v = [R(p, d) for d in g]
        v = np.array([np.nan if x is None else x for x in v]); j = int(np.nanargmax(v))
        hist.append((float(g[j]), float(v[j]), hi-lo))
        step = g[1]-g[0]; lo, hi = g[j]-2*step, g[j]+2*step
    out.append(dict(eta=eta, levels=hist)); print(eta, hist, flush=True)
(HERE/'figure_data'/'extra_loss_refine.json').write_text(json.dumps(out, indent=1))
