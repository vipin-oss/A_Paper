#!/usr/bin/env python3
"""Quadrature sufficiency for the production solves.

The thickness quadrature is Gauss-Legendre with ``max(64, 2*degree + 10)`` nodes.
This script holds the physical problem and the basis degree fixed, raises the
node count alone, and re-solves the two reported edge configurations.  A rule
that is merely "high order" is not evidence; what matters is the change in the
reported return when the rule is refined at fixed basis.

Writes ``figure_data/quadrature_audit.json``.
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
CASES = {"operating_point": 0.7361990195318475, "branch_maximum": 0.525}
NODES = (0, 128, 192, 256)          # 0 = the production default


def solve(K: float, degree: int, nquad: int) -> dict:
    p = Plate(degree=degree, flexo=1e-9, H=0.0, ell=50e-9, nquad=nquad)
    mode = track(p, [K], operating_mode(p))[0]
    omega = float(mode["omega"].real)
    res, _ = p.edge(KY0, omega, K, KB0)
    return dict(nodes=p.nquad, degree=degree,
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
        out[case] = [solve(K, 22, nq) for nq in NODES]
    print(f"{'case':16s} {'degree':>6s} {'nodes':>6s} {'f/GHz':>10s} {'R_B':>12s} "
          f"{'delta R_B':>10s} {'K_B':>10s}")
    worst = 0.0
    for case, rows in out.items():
        ref = max(rows, key=lambda r: r["nodes"])
        for r in rows:
            d = (r["R_B"] - ref["R_B"]) / ref["R_B"]
            worst = max(worst, abs(d))
            print(f"{case:16s} {r['degree']:6d} {r['nodes']:6d} "
                  f"{r['frequency_GHz']:10.6f} {r['R_B']:12.9f} {d:+10.2e} "
                  f"{r['backward_K_real']:10.6f}")
    # Tolerance: R_B is quoted to 4-6 significant digits (1e-4 relative), so a
    # quadrature-induced change of 1e-7 cannot move a quoted digit.  The
    # near-degenerate branch maximum (K_B/K_inc = 0.992) sets a noise floor of
    # order 5e-9 in any case.
    out["verdict"] = {"worst_relative_change_vs_256_nodes": worst,
                      "tolerance": 1e-7, "pass": bool(worst < 1e-7)}
    print(f"\nworst relative change of R_B against the 256-node rule: {worst:.2e}")
    print("verdict:", "PASS" if worst < 1e-7 else "FAIL")
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "quadrature_audit.json").write_text(json.dumps(out, indent=2))
    return 0 if worst < 1e-7 else 1


if __name__ == "__main__":
    sys.exit(main())
