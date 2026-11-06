#!/usr/bin/env python3
"""Quantify what the flexoelectric term actually does in the reported solves.

The manuscript states the flexoelectric coefficient as a synthetic value.  This
script measures its contribution rather than asserting it: the same edge solve
is repeated with f33 = 0, with the default 1 nC/m, and with 10 nC/m, at the
operating point and at the peak of the backward channel.

Writes figure_data/flexo_control.json.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_figure_data import (KB0, K0, KY0, OMEGA0, operating_mode,  # noqa: E402
                               plate, track)

DATA = HERE / "figure_data"
CASES = {"operating_point": (K0, KY0), "peak": (0.55, KY0)}
FLEXO = {"zero": 0.0, "synthetic_1nC_m": 1e-9, "ten_x": 1e-8}


def solve(kx: float, ky: float, flexo: float) -> dict:
    """Same sequence as certify_peak.one(): track the branch, then solve."""
    p = plate(0.0, flexo=flexo)
    mode = track(p, [kx], operating_mode(p))[0]
    omega = float(mode["omega"].real)
    r, _ = p.edge(ky, omega, kx, KB0)
    return {
        "R_B_2um": float(r["backward_reflection_self_power"]),
        "angle_deg": float(r["reflected_angle_deg"]),
        "power_balance_relative": float(r["power_balance_relative"]),
        "edge_scaled_residual": float(r["edge_scaled_residual"]),
        "frequency_GHz": float(r["frequency_Hz"] / 1e9),
        "f_dimensionless": float(p.f),
    }


def main() -> int:
    out: dict[str, dict] = {}
    for case, (kx, ky) in CASES.items():
        out[case] = {name: solve(kx, ky, f) for name, f in FLEXO.items()}
        base = out[case]["synthetic_1nC_m"]["R_B_2um"]
        zero = out[case]["zero"]["R_B_2um"]
        ten = out[case]["ten_x"]["R_B_2um"]
        out[case]["effect_of_synthetic_f_percent"] = 100.0 * (base - zero) / zero
        out[case]["effect_of_ten_times_f_percent"] = 100.0 * (ten - zero) / zero

    print("flexoelectric control")
    for case, rows in out.items():
        print(f"\n{case}")
        for name in FLEXO:
            r = rows[name]
            print(f"  {name:16s} f = {r['f_dimensionless']:.3e}  "
                  f"R_B = {r['R_B_2um']:.9f}  theta = {r['angle_deg']:+.4f}  "
                  f"balance = {r['power_balance_relative']:.1e}")
        print(f"  effect of f = 1 nC/m : {rows['effect_of_synthetic_f_percent']:+.3f} %")
        print(f"  effect of f = 10 nC/m: {rows['effect_of_ten_times_f_percent']:+.3f} %")

    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "flexo_control.json").write_text(json.dumps(out, indent=2))
    print("\nwrote", DATA / "flexo_control.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
