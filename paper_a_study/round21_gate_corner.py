"""Round-21 Gates 1-2: natural boundary data and the corner line force.

Gate 1 (derivation + two independent evaluations) is in
PAPER_A_ROUND21_GATE1_DERIVATION.md; this script produces the numbers.

For every configuration it reports

  * the per-mode identity between the physical natural data
        t_i = S_i1 - i k_y tau_i21 - d_z tau_i31        (traction)
        m_i = tau_i11                                    (double traction)
        f_i = tau_i31 + tau_i13                          (corner line force)
    and the discrete state-space flux rows (T[:nu], R), evaluated on the
    complete incident + reflected field and per mode;
  * the pointwise residuals of the superposed field, split into an interior
    window and the two corner layers, because the variational statement imposes
    the natural data only weakly and the deficit is localised at the corners;
  * the corner line force itself, at three corner-localisation scales, and its
    dependence on the Galerkin degree, which is the Gate-2 question.

Run: PYTHONPATH=paper_a_study .venv/bin/python paper_a_study/round21_gate_corner.py
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_figure_data import KB0, K0, KY0, operating_mode, plate, track  # noqa: E402
from model import tensor_matrix  # noqa: E402
import round21_gate1_traction as G  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figure_data", "round21")
CASES = [("operating point", K0), ("corrected maximum", 0.52719), ("k_x d = 0.55", 0.55)]


def _enc(o):
    if isinstance(o, complex):
        return [float(o.real), float(o.imag)]
    if isinstance(o, np.floating):
        return float(o)
    raise TypeError(type(o))


def band(z, zz, h):
    return np.abs(z - zz) <= h


def superposed(p, scr):
    """Complete incident + reflected field of the boundary data."""
    modes = [(1.0, scr["incident"]["K"], scr["incident"]["q"])]
    for j, (Kj, aj) in enumerate(zip(scr["K"], scr["amplitudes"])):
        modes.append((aj, Kj, scr["Y"][: p.nw, j]))
    out = inc = cout = cinc = None
    for c, K, q in modes:
        node = G.boundary_fields(p, K, q)
        cor = G.boundary_fields(p, K, q, corner=True)
        if out is None:
            out, inc = {k: c * v for k, v in node.items()}, dict(node)
            cout, cinc = {k: c * v for k, v in cor.items()}, dict(cor)
        else:
            for k in out:
                out[k] = out[k] + c * node[k]
                cout[k] = cout[k] + c * cor[k]
    return (out, inc), (cout, cinc)


def metrics(p, out, inc, cout, cinc):
    z, w = p.z, p.weights
    it, ib = int(np.argmin(abs(z - 0.5))), int(np.argmin(abs(z + 0.5)))

    def rms(v, mask):
        if not np.any(mask):
            return 0.0
        return float(np.sqrt(np.sum(w[mask, None] * abs(v[mask]) ** 2) / np.sum(w[mask])))

    t, ti = out["traction"], inc["traction"]
    d, di = out["double"], inc["double"]
    inner = np.abs(z) < 0.4
    layer = ~inner
    scale = max(rms(ti, np.ones_like(z, bool)), 1e-30)
    scale_d = max(rms(di, np.ones_like(z, bool)), 1e-30)
    res = dict(
        traction_inner_rel=float(rms(t, inner) / scale),
        traction_layer_rel=float(rms(t, layer) / scale),
        traction_max_rel=float(np.max(abs(t)) / np.max(abs(ti))),
        double_inner_rel=float(rms(d, inner) / scale_d),
        double_max_rel=float(np.max(abs(d)) / np.max(abs(di))),
    )
    f, fi = cout["corner"], cinc["corner"]
    ftop, fbot = f[1], f[0]          # p.eb ordered (-1/2, +1/2)
    fitop, fibot = fi[1], fi[0]
    cscale = max(np.max(abs(fitop)), np.max(abs(fibot)), 1e-30)
    res.update(
        corner_top=ftop.tolist(), corner_bottom=fbot.tolist(),
        corner_top_rel=float(np.max(abs(ftop)) / cscale),
        corner_bottom_rel=float(np.max(abs(fbot)) / cscale),
        corner_max_rel=float(max(np.max(abs(ftop)), np.max(abs(fbot))) / cscale),
        corner_incident_scale=float(cscale),
    )
    for h in (2.0 / p.degree, 4.0 / p.degree, 0.05):
        vals = []
        fn = out["corner"]   # nodal values, length nquad
        for zz in (0.5, -0.5):
            m = band(z, zz, h)
            vals.append(float(np.max(abs(fn[m])) if np.any(m) else np.nan))
        res[f"corner_band_h{h:.4f}_max"] = max(vals)
        res[f"corner_band_h{h:.4f}_rel"] = max(vals) / cscale
    return res


def run(degree, K, nquad=0, label=""):
    p = plate(0.0, degree=degree, nquad=nquad)
    m = track(p, [K], operating_mode(p))[0]
    om = float(m["omega"].real)
    res, scr = p.edge(KY0, om, K, KB0)
    modes = [(scr["incident"]["K"], scr["incident"]["y"])]
    modes += [(Kj, scr["Y"][:, j]) for j, Kj in enumerate(scr["K"])]
    ident = [G.mode_identity(p, Kx, y) for Kx, y in modes]
    (out, inc), (cout, cinc) = superposed(p, scr)
    row = dict(label=label or f"deg{degree}", degree=degree, K=float(K), nquad=p.nquad,
               omega=om, R_B=float(res["backward_reflection_self_power"]),
               edge_residual=float(res["edge_scaled_residual"]),
               id_incident=float(ident[0]["traction_incl_corner"]),
               id_worst=float(max(i["traction_incl_corner"] for i in ident)),
               id_plain_worst=float(max(i["traction_plain"] for i in ident)),
               id_double_worst=float(max(i["double"] for i in ident)))
    row.update(metrics(p, out, inc, cout, cinc))
    return row


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for name, K in CASES:
        for degree in (10, 12, 14, 16, 20, 24, 28):
            r = run(degree, K, label=f"{name} deg{degree}")
            rows.append(r)
            print(f"{name:18s} n={degree:2d} K={K:.5f} R_B={r['R_B']:.10f} "
                  f"id(inc)={r['id_incident']:.1e} id(plain,worst)={r['id_plain_worst']:.1e} "
                  f"t_inner={r['traction_inner_rel']:.3e} t_layer={r['traction_layer_rel']:.3e} "
                  f"m={r['double_max_rel']:.1e} f={r['corner_max_rel']:.4e}")
    for nq in (96, 128, 192):
        r = run(12, 0.52719, nquad=nq, label=f"corrected maximum deg12 nquad{nq}")
        rows.append(r)
        print(f"nquad={nq:3d} id(inc)={r['id_incident']:.2e} id(plain,worst)={r['id_plain_worst']:.2e} "
              f"f={r['corner_max_rel']:.5e} t_inner={r['traction_inner_rel']:.3e}")
    path = os.path.join(OUT, "gate12_corner.json")
    with open(path, "w") as h:
        json.dump(rows, h, indent=1, default=_enc)
    print("wrote", path)

    # Gate-2 corner force trend: fit |f| = a n^-p per case
    for name, _ in CASES:
        sub = [(r["degree"], r["corner_max_rel"]) for r in rows
               if r["label"].startswith(name + " deg")]
        ns = np.array([s[0] for s in sub], float)
        fs = np.array([s[1] for s in sub])
        A = np.column_stack([np.ones_like(ns), np.log(ns)])
        coef = np.linalg.lstsq(A, np.log(fs), rcond=None)[0]
        print(f"{name:18s} |f|/scale = {np.exp(coef[0]):.3e} n^({coef[1]:+.3f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
