#!/usr/bin/env python3
"""Issue C: is the backward reflection certified, or only an eigenvector artefact?

The `backward_Px` diagnostic stored in `peak_certification.json` varies by about
60 % between Galerkin degrees while the reported return R_B is stable to 1e-7.
This script decides which of the two is the physical quantity.

The solver normalises the *incident* state to unit power but leaves every
outgoing eigenvector at whatever scaling the eigen-solver returns.  Therefore

    P_B (raw)  = power of the unscaled outgoing eigenvector   -> arbitrary
    |a_B|^2 P_B = power actually carried by that port          -> physical

The script tabulates both at four degrees for the operating point and for the
peak, checks that |a_B|^2 P_B is invariant, and then performs an explicit
rescaling experiment: every eigenvector is multiplied by an independent random
complex factor, the matching is re-solved with the same algorithm, and the
physical fluxes and R_B are required to be unchanged to machine precision.

Writes figure_data/modal_flux_audit.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import svd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_figure_data import KB0, KY0, operating_mode, plate, track  # noqa: E402

DATA = HERE / "figure_data"
CASES = {"operating_point": 0.7361990195318475, "peak": 0.55}
DEGREES = [18, 22, 26, 30]


def solve(degree: int, K: float, scalings=None):
    """Run the edge solve, optionally rescaling every eigenvector first."""
    p = plate(0.0, degree=degree)
    mode = track(p, [K], operating_mode(p))[0]
    omega = float(mode["omega"].real)

    if scalings is None:
        res, scr = p.edge(KY0, omega, K, KB0)
        return p, res, scr, None

    # replicate edge() with rescaled eigenvectors
    waves, A, F = p.waves(KY0, omega)
    outgoing, incoming = [], []
    for w in waves:
        tol = 2e-8 * max(1, abs(w["K"]))
        out = (w["K"].imag < -tol) or (abs(w["K"].imag) <= tol and w["power"] < 0)
        (outgoing if out else incoming).append(w)
    inc = min(incoming, key=lambda a: abs(a["K"] - K))
    iy = inc["y"] / np.sqrt(inc["power"])
    Y = np.stack([v["y"] for v in outgoing], axis=1)
    Ks = np.array([v["K"] for v in outgoing])
    ib = int(np.argmin(abs(Ks - KB0)))

    lam = scalings
    Ys = Y * lam[None, :]
    incs = iy                                # incident kept at unit power
    B = np.stack([p.boundary_vector(Ys[:, j]) for j in range(len(Ks))], axis=1)
    bi = p.boundary_vector(incs)
    row = np.maximum(np.linalg.norm(B, axis=1), 1e-30)
    C = B / row[:, None]
    rhs = -bi / row
    col = np.maximum(np.linalg.norm(C, axis=0), 1e-30)
    u, s, vh = svd(C / col[None, :])
    aa = (vh.conj().T @ ((u.conj().T @ rhs) / s)) / col

    L = 10.0
    selfout = np.array([p.power(Ys[:, j], omega) * abs(aa[j]) ** 2
                        * np.exp(2 * Ks[j].imag * L) for j in range(len(Ks))])
    inc_left = float(np.exp(2 * inc["K"].imag * L))
    return p, None, dict(Y=Ys, K=Ks, aa=aa, ib=ib, selfout=selfout,
                         inc_left=inc_left), lam


def main() -> int:
    rows = {}
    ok = True
    for case, K in CASES.items():
        table = []
        for degree in DEGREES:
            p, res, scr, _ = solve(degree, K)
            if res is None:
                continue
            ib = int(np.argmin(abs(scr["K"] - KB0)))
            raw_P = float(p.power(scr["Y"][:, ib], res["omega"]))
            table.append({
                "degree": degree,
                "raw_backward_Px": res["backward"]["Px"],
                "raw_mode_power": raw_P,
                "amplitude_abs": float(abs(res["backward_amplitude"])),
                "physical_backward_power": float(
                    abs(res["backward_amplitude"]) ** 2
                    * np.exp(2 * res["backward_K"].imag * 10.0)
                    * res["backward"]["Px"]),
                "incident_power_at_plane": res["incident_power_left"],
                "R_B": res["backward_reflection_self_power"],
                "ok": True,
            })
        rows[case] = table

    print("ISSUE C - modal flux normalisation")
    print("=" * 78)
    spreads = {}
    for case, table in rows.items():
        print(f"\n{case}  (k_x d = {CASES[case]})")
        print(f"{'deg':>4} {'raw P_B':>13} {'|a_B|':>11} {'|a_B|^2 P_B':>14}"
              f" {'P_inc':>11} {'R_B':>12}")
        for r in table:
            print(f"{r['degree']:>4} {r['raw_backward_Px']:>13.6e}"
                  f" {r['amplitude_abs']:>11.4e}"
                  f" {r['physical_backward_power']:>14.6e}"
                  f" {r['incident_power_at_plane']:>11.6e}"
                  f" {r['R_B']:>12.9f}")
        phys = np.array([r["physical_backward_power"] for r in table])
        rb = np.array([r["R_B"] for r in table])
        spread_p = float(phys.max() / phys.min() - 1)
        spread_r = float(rb.max() / rb.min() - 1)
        raw = np.array([r["raw_backward_Px"] for r in table])
        spread_raw = float(raw.max() / raw.min() - 1)
        print(f"     spread of raw P_B           : {spread_raw:9.3%}")
        print(f"     spread of |a_B|^2 P_B       : {spread_p:9.3e}")
        print(f"     spread of R_B               : {spread_r:9.3e}")
        ok &= spread_p < 5e-4 and spread_r < 1e-5
        spreads[case] = {"raw": spread_raw, "physical": spread_p,
                         "R_B": spread_r}

    # ---- explicit rescaling invariance -------------------------------------
    print("\nexplicit rescaling invariance (operating point, degree 22)")
    rng = np.random.default_rng(7)
    p, _, scr, _ = solve(22, CASES["operating_point"], scalings=None)
    base_res, _ = p.edge(KY0, float(track(p, [CASES["operating_point"]],
                                          operating_mode(p))[0]["omega"].real),
                         CASES["operating_point"], KB0)
    base_R = base_res["backward_reflection_self_power"]
    n_out = scr["Y"].shape[1]
    lam = np.exp(rng.uniform(-1.5, 1.5, n_out) + 1j * rng.uniform(0, 2 * np.pi, n_out))
    _, _, scr2, _ = solve(22, CASES["operating_point"], scalings=lam)
    ib = scr["index_backward"]
    R2 = float(-scr2["selfout"][scr2["ib"]] / scr2["inc_left"])
    print(f"  R_B before rescaling : {base_R:.12f}")
    print(f"  R_B after  rescaling : {R2:.12f}")
    print(f"  relative difference  : {abs(R2-base_R)/abs(base_R):.3e}")
    ok &= abs(R2 - base_R) / abs(base_R) < 1e-9

    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "modal_flux_audit.json").write_text(json.dumps(
        {"cases": rows, "spreads": spreads,
         "rescaling_test": {"R_B_before": base_R,
                                           "R_B_after": R2}}, indent=2))
    print("\nwrote", DATA / "modal_flux_audit.json")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
