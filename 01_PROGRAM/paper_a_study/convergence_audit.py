#!/usr/bin/env python3
"""Spectral convergence of the two reported configurations.

Holds the physics fixed and varies the Galerkin degree of the thickness
expansion.  For each degree it records the tracked frequency, the backward modal
share, the scaled edge residual, the power balance and the condition number of
the edge system, then reports successive differences.  No convergence rate is
fitted: the sequence reaches the round-off floor before an asymptotic slope
could be identified, and the script reports the raw differences instead.

Writes ``figure_data/convergence_audit.json``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_figure_data import KB0, KY0, operating_mode, track  # noqa: E402
from model import Plate  # noqa: E402

DATA = HERE / "figure_data"
CASES = {"operating_point": 0.7361990195318475, "near_peak_k0p525": 0.525, "peak_k0p52719": 0.52719}
DEGREES = (14, 18, 22, 26, 30)


def solve(K: float, degree: int) -> dict:
    p = Plate(degree=degree, flexo=1e-9, H=0.0, ell=50e-9)
    mode = track(p, [K], operating_mode(p))[0]
    omega = float(mode["omega"].real)
    res, _ = p.edge(KY0, omega, K, KB0)
    return dict(degree=degree, dof=p.nw,
                frequency_GHz=omega * p.fscale / 1e9,
                R_B=float(res["backward_reflection_self_power"]),
                backward_K_real=float(complex(res["backward_K"]).real),
                angle_deg=float(res["reflected_angle_deg"]),
                edge_residual=float(res["edge_scaled_residual"]),
                power_balance=float(res["power_balance_relative"]),
                condition=float(res["edge_condition"]))


def main() -> int:
    out: dict[str, list] = {}
    for case, K in CASES.items():
        out[case] = [solve(K, n) for n in DEGREES]
    summary: dict[str, dict] = {}
    for case, rows in out.items():
        ref = rows[-1]
        print(f"\n{case}: k_xd = {CASES[case]:.6f}")
        print(f"{'n':>4} {'dof':>5} {'f/GHz':>12} {'R_B':>13} {'|dR_B|/R_B':>11} "
              f"{'K_B':>10} {'residual':>9} {'balance':>9} {'cond':>8}")
        for r in rows:
            d = abs(r["R_B"] - ref["R_B"]) / ref["R_B"]
            print(f"{r['degree']:4d} {r['dof']:5d} {r['frequency_GHz']:12.9f} "
                  f"{r['R_B']:13.10f} {d:11.2e} {r['backward_K_real']:10.6f} "
                  f"{r['edge_residual']:9.1e} {r['power_balance']:9.1e} "
                  f"{r['condition']:8.1f}")
        succ = [abs(rows[i + 1]["R_B"] - rows[i]["R_B"]) / rows[i]["R_B"]
                for i in range(len(rows) - 1)]
        print("  successive relative changes:", " ".join(f"{x:.1e}" for x in succ))
        summary[case] = {
            "successive_relative_changes": succ,
            "monotone_decrease": bool(all(succ[i + 1] < succ[i]
                                          for i in range(len(succ) - 1))),
            "max_change_18_to_30": float(abs(rows[-1]["R_B"] - rows[1]["R_B"])
                                         / rows[-1]["R_B"]),
        }
    out["summary"] = summary
    worst = max(v["max_change_18_to_30"] for v in summary.values())
    out["verdict"] = {"max_relative_change_degree18_to_30": worst,
                      "tolerance": 1e-5, "pass": bool(worst < 1e-5)}
    print(f"\nlargest relative change between degree 18 and degree 30: {worst:.2e}")
    print("verdict:", "PASS" if worst < 1e-5 else "FAIL")
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "convergence_audit.json").write_text(json.dumps(out, indent=2))
    return 0 if worst < 1e-5 else 1


if __name__ == "__main__":
    sys.exit(main())
