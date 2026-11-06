"""Issue F: are the reported modal partitions sensitive to the plate corner?

The edge problem is solved in a spectral Galerkin basis through the thickness,
so the free edge meets the free faces at two corners (x=0, z=+-d/2).  A corner
singularity of the higher-order (strain-gradient) edge problem would show up as
(i) a strain-gradient energy density that concentrates without bound in the
outer band |z|>0.4d as the degree is raised, or (ii) a pointwise field that
grows with degree.  Both are measured here at the operating point and at the
zero-group-velocity peak, for degrees 18/22/26/30.

The density is the x=0 plane value of the strain-gradient energy density
lam^2 * sum_l (d eps/dx_l) : C : (d eps/dx_l), built from the *coherent sum* of
all outgoing modes plus the incident mode (interference retained).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from build_figure_data import KB0, KY0, plate, track, operating_mode

OUT = Path(__file__).resolve().parent / 'figure_data' / 'corner_assessment.json'
BAND = 0.40          # |z| > 0.40 d/2 ... faces are at +-0.5
DEGREES = (18, 22, 26, 30)
CASES = {'operating_point': KB0, 'peak': 0.55}


def gradient_energy(plate_, ky, res, scr):
    """Coherent strain-gradient energy density on the x=0 plane."""
    p = plate_
    Y, K, aa, inc = scr['Y'], scr['K'], scr['amplitudes'], scr['incident']
    G = [np.zeros((len(p.z), 6), complex) for _ in range(3)]
    modes = [(1.0, inc['y'], inc['K'])] + [(aa[j], Y[:, j], K[j]) for j in range(len(K))]
    for amp, prof, Kj in modes:
        f = p.fields(Kj, ky, prof[:p.nw])
        G[0] += amp * 1j * Kj * f['strain'][0]
        G[1] += amp * 1j * ky * f['strain'][0]
        G[2] += amp * f['strain'][1]
    dens = np.zeros(len(p.z))
    for g in G:
        dens += np.einsum('qi,ij,qj->q', g.conj(), p.C, g).real
    dens *= p.lam ** 2
    w = p.weights
    total = float(np.sum(w * dens))
    band = np.abs(p.z) > BAND
    corner = float(np.sum(w[band] * dens[band]))
    share = corner / total if total > 0 else float('nan')
    peak_ratio = float(np.max(dens[band]) / (total / np.sum(w))) if band.any() else float('nan')
    # algebraic growth probe: peak density relative to the same measure at band mean
    return dict(total=total, corner_band=corner, corner_share=share,
                corner_peak_over_mean=peak_ratio,
                inner_share=1.0 - share)


def main():
    report = {'band': BAND, 'note': 'x=0 plane, coherent modal sum, lam^2|grad eps|_C^2', 'cases': {}}
    for name, K in CASES.items():
        rows = []
        for deg in DEGREES:
            p = plate(degree=deg)
            m = track(p, [K], operating_mode(p))[0]
            res, scr = p.edge(KY0, float(m['omega'].real), K, KB0)
            g = gradient_energy(p, KY0, res, scr)
            rows.append(dict(degree=deg, R_B=res['backward_reflection_self_power'],
                             frequency_Hz=res['frequency_Hz'],
                             **g))
        rb = [r['R_B'] for r in rows]
        sh = [r['corner_share'] for r in rows]
        pk = [r['corner_peak_over_mean'] for r in rows]
        report['cases'][name] = dict(
            rows=rows,
            R_B_spread_rel=float((max(rb) - min(rb)) / max(abs(np.mean(rb)), 1e-30)),
            corner_share_range=[float(min(sh)), float(max(sh))],
            corner_share_drift_rel=float((sh[-1] - sh[0]) / max(sh[0], 1e-30)),
            corner_peak_over_mean_range=[float(min(pk)), float(max(pk))],
            corner_peak_drift_rel=float((pk[-1] - pk[0]) / max(pk[0], 1e-30)))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
