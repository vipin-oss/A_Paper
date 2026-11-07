#!/usr/bin/env python3
"""Round 20: the two electrical edge conditions, measured and recomputed.

The round-19 solver imposes ``phi(0,z) = 0`` on the reflecting edge (Dirichlet, a
metallised edge).  The manuscript describes the edge as charge-free,
``D_x(0,z) = 0`` (natural).  This script

 1. recomputes, for the *complete superposed scattering field* (incident mode plus
    every outgoing mode with its solved amplitude), the physical boundary
    residuals at x = 0 -- generalised traction, double traction tau_j11, electric
    potential phi, normal electric displacement D_x and carrier flux J_x -- for
    both electrical conditions, so that "satisfied" and "violated" are measured
    numbers and not assertions;
 2. reruns the backward-channel search for R_B (coarse raster, bracket, plateau
    and refinement) under the charge-free condition, which is the problem the
    manuscript describes but has never been solved;
 3. writes ``figure_data/round20_edge_condition_audit.json``.

Nothing here modifies the delivered datasets: the grounded rows are recomputed
with the default solver and must reproduce the stored values, and the insulating
rows are written to a new file.

Run from the repository root::

    PYTHONPATH=. .venv/bin/python paper_a_study/round20_recompute.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_figure_data import KB0, KY0, operating_mode, plate, track  # noqa: E402
from model import tensor_matrix  # noqa: E402

DATA = HERE / "figure_data"
K_OP = 0.7361990195318475
K055 = 0.55
DOMAIN = (0.465, 0.625)
COARSE, PLATEAU, REFINE = 0.002, 5e-4, 2.5e-5


def _proj3(v, b, w):
    """Project the three components of a (q,3) field onto one z-basis."""
    return np.array([b.T @ (w * v[:, i]) for i in range(3)])


def residuals(p, res, scr):
    """Physical edge residuals of the superposed field at x = 0.

    Every quantity is formed from the *physical* fields of every mode, weighted
    by its scattering amplitude, so the residual belongs to the field the paper
    reports and not to an individual eigenvector.  Each is normalised by the same
    functional applied to the incident mode alone.
    """
    inc = scr["incident"]
    Y, Ks, aa = scr["Y"], scr["K"], scr["amplitudes"]
    modes = [(1.0, inc["K"], inc["q"])]
    modes += [(aa[j], Ks[j], Y[: p.nw, j]) for j in range(len(Ks))]
    b0, pb0, w = p.b[0], p.pb[0], p.weights
    acc = {k: None for k in ("t", "m", "phi", "D", "J")}
    ref = {}
    for n, (c, K, q) in enumerate(modes):
        f = p.fields(K, KY0, q)
        tau0 = tensor_matrix(f["tau"][0])
        vals = {
            "t": tensor_matrix(f["sigma"])[:, :, 0] - 1j * K * tau0[:, :, 0],
            "m": tau0[:, :, 0],
            "phi": f["phi"][0],
            "D": f["D"][:, 0],
            "J": (1j * p.alpha / p.omega_ref) * (1j * K) * f["mu"][0],
        }
        if n == 0:
            ref = vals
        for k, v in vals.items():
            acc[k] = c * v if acc[k] is None else acc[k] + c * v
    out = {}
    for k, basis in (("t", b0), ("m", b0), ("phi", pb0), ("D", pb0), ("J", b0)):
        num = np.linalg.norm(_proj(k, acc[k], basis, w, p))
        den = np.linalg.norm(_proj(k, ref[k], basis, w, p))
        out[f"residual_{k}"] = float(num / max(den, 1e-300))
        out[f"pointwise_{k}"] = float(np.abs(acc[k]).max() / max(np.abs(ref[k]).max(), 1e-300))
    return out


def _proj(k, v, basis, w, p):
    if v.ndim == 1:
        return basis.T @ (w * v)
    return _proj3(v, basis, w)


def solve_one(degree, K, edge_electric, target=KB0):
    p = plate(0.0, degree=degree, edge_electric=edge_electric)
    p.omega_ref = float(track(p, [K], operating_mode(p))[0]["omega"].real)
    res, scr = p.edge(KY0, p.omega_ref, K, target)
    res["R_B"] = float(res["backward_reflection_self_power"])
    res.update(residuals(p, res, scr))
    return res


def raster(a, b, step):
    n = int(round((b - a) / step)) + 1
    return [round(a + i * step, 10) for i in range(n)]


def main() -> int:
    t0 = time.time()
    out = {"note": "round 20: grounded (as delivered) vs charge-free (as described) edge",
           "K_operating": K_OP, "K_055": K055, "ky": KY0}

    rows = {}
    for name, K in (("operating_point", K_OP), ("k_xd_0.55", K055)):
        rows[name] = {}
        for edge in ("ground", "insulating"):
            r = solve_one(22, K, edge)
            rows[name][edge] = {k: r[k] for k in
                                ("R_B", "backward_reflection_self_power", "edge_size",
                                 "edge_rank", "edge_condition", "edge_scaled_residual",
                                 "power_balance_relative", "frequency_Hz") if k in r}
            rows[name][edge].update({k: v for k, v in r.items() if k.startswith(("residual_", "pointwise_"))})
            print(f"{name:16s} {edge:11s} R_B={r['R_B']:.7f} "
                  f"res phi={r['residual_phi']:.2e} D_x={r['residual_D']:.2e} "
                  f"t={r['residual_t']:.2e} m={r['residual_m']:.2e} J={r['residual_J']:.2e}",
                  flush=True)
    out["rows"] = rows

    # ---------------------------------------------------------------- search
    def sweep(Ks):
        p = plate(0.0, degree=22, edge_electric="insulating")
        vals = []
        for K in Ks:
            om = float(track(p, [K], operating_mode(p))[0]["omega"].real)
            res, _ = p.edge(KY0, om, K, KB0)
            vals.append({"K": K, "omega": om,
                         "R_B": float(res["backward_reflection_self_power"])})
        return vals

    coarse = sweep(raster(*DOMAIN, COARSE))
    best = max(coarse, key=lambda r: r["R_B"])
    print(f"coarse best K={best['K']:.4f} R_B={best['R_B']:.7f}  ({time.time()-t0:.0f}s)", flush=True)
    bracket = raster(max(DOMAIN[0], best["K"] - 0.01), min(DOMAIN[1], best["K"] + 0.01), PLATEAU)
    plateau = sweep(bracket)
    pb = max(plateau, key=lambda r: r["R_B"])
    print(f"plateau best K={pb['K']:.5f} R_B={pb['R_B']:.7f}  ({time.time()-t0:.0f}s)", flush=True)
    fine = raster(pb["K"] - 5e-4, pb["K"] + 5e-4, REFINE)
    refined = sweep([k for k in fine if DOMAIN[0] <= k <= DOMAIN[1]])
    rb = max(refined, key=lambda r: r["R_B"])
    print(f"refined best K={rb['K']:.6f} R_B={rb['R_B']:.7f}  ({time.time()-t0:.0f}s)", flush=True)

    flat = [r["R_B"] for r in plateau if abs(r["K"] - pb["K"]) <= 5e-4]
    out["search"] = {"domain": list(DOMAIN), "steps": {"coarse": COARSE, "plateau": PLATEAU,
                                                       "refine": REFINE},
                     "coarse": coarse, "plateau": plateau, "refined": refined,
                     "argmax": rb, "plateau_flatness": float(max(flat) - min(flat)) if flat else None}

    peak = {}
    for degree in (22, 26):
        r = solve_one(degree, rb["K"], "insulating")
        peak[str(degree)] = {k: r[k] for k in ("R_B", "edge_size", "edge_rank", "edge_condition",
                                               "edge_scaled_residual", "power_balance_relative")}
        peak[str(degree)].update({k: v for k, v in r.items() if k.startswith("residual_")})
        print(f"degree {degree}: R_B={r['R_B']:.7f} phi={r['residual_phi']:.2e} D_x={r['residual_D']:.2e}",
              flush=True)
    out["peak"] = peak

    (DATA / "round20_edge_condition_audit.json").write_text(json.dumps(out, indent=1))
    print(f"written {DATA/'round20_edge_condition_audit.json'}  ({time.time()-t0:.0f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
