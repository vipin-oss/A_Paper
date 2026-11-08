"""Classical free-edge benchmark: the production solver with the ZnO constants replaced by
Duralumin (rho=2790, cL=6398, cT=3122 m/s), no piezoelectricity, no strain gradient, no
carrier coupling, normal incidence (ky=1e-7).  Compared by eye with Gerardin et al. 2016,
Fig. 2(b).  Output: figure_data/benchmark_duralumin.csv.  Run: python3 benchmark_duralumin.py"""
import sys, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import model
S = model.SI
rho, cL, cT = 2790., 6398., 3122.
S['rho'] = rho; S['c11'] = S['c33'] = rho*cL**2; S['c12'] = S['c13'] = rho*(cL**2-2*cT**2)
S['c44'] = S['c66'] = rho*cT**2; S['e15'] = S['e31'] = S['e33'] = 0.
KY = 1e-7

def pair(p, om):
    w, _, _ = p.waves(KY, om)
    real = [(x['K'].real, x['power']) for x in w if abs(x['K'].imag) < 1e-6 and x['K'].real > 1e-6]
    return [k for k, q in real if q > 0], [k for k, q in real if q < 0]

rows = []
for deg in (18, 26):
    p = model.Plate(degree=deg, d=1e-3, ell=0., flexo=0., H=0., n0=2e18)
    lo, hi = 2.870, 2.875
    for _ in range(40):
        mid = (lo+hi)/2
        if pair(p, mid*1e6/p.fscale)[1]: hi = mid
        else: lo = mid
    for f2h in (hi+2e-6, hi+1e-4, 2.875, 2.88, 2.90, 2.95, 3.00, 3.10):
        om = f2h*1e6/p.fscale
        pos, neg = pair(p, om)
        kb = max(neg); ki = min(pos, key=lambda k: abs(k-kb))
        r, _ = p.edge(KY, om, ki, kb, L=10.)
        rows.append(dict(degree=deg, zgv_f2h=hi, f2h_MHz_mm=f2h, kb_over_ki=kb/ki,
                         R_B=r['backward_reflection_self_power'], abs_r=r['backward_reflection_self_power']**.5,
                         total_outgoing=r['total_outgoing_self_power'], balance=r['power_balance_relative'],
                         edge_residual=r['edge_scaled_residual']))
out = Path(__file__).parent/'figure_data'/'benchmark_duralumin.csv'
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('wrote', out, len(rows))
