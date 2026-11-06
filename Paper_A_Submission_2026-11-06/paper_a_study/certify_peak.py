"""Certification of the two backward-reflection values quoted in the manuscript.

The manuscript quotes (i) the operating-point return R_B = 2.3 % at
k_x d = 0.736 and (ii) a much larger peak of about 58 % at k_x d = 0.55.
Both numbers are re-solved here with an explicit convergence test: the same
physical problem is discretised at four Galerkin degrees and the reported
quantities must be stable under refinement.  The test also records the modal
decomposition (self-powers, cross-interference, dissipation) so that the
energy identity can be checked independently of the plotting code.

Run:  python certify_peak.py     (writes figure_data/peak_certification.json)
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from build_figure_data import (KB0, KY0, dump_json, operating_mode, plate,
                               track)

HERE = Path(__file__).resolve().parent
CASES = [("operating_point", 0.7361990195318475), ("peak_candidate", 0.55),
         ("peak_lower", 0.525), ("peak_upper", 0.575)]
DEGREES = [18, 22, 26, 30]


def one(degree: int, K: float) -> dict:
    p = plate(0.0, degree=degree)
    mode = track(p, [K], operating_mode(p))[0]
    out = dict(degree=degree, K=K, omega=float(mode["omega"].real))
    try:
        res, _ = p.edge(KY0, mode["omega"].real, K, KB0)
    except Exception as exc:                      # noqa: BLE001
        out.update(status="edge solve failed", error=type(exc).__name__)
        return out
    inc = res["incident"]
    back = res["backward"]
    inc_left = float(res["incident_power_left"])
    out.update(
        status="solved",
        R_B=float(res["backward_reflection_self_power"]),
        angle_deg=float(res["reflected_angle_deg"]),
        incident_angle_deg=float(res["incident_angle_deg"]),
        residual=float(res["edge_scaled_residual"]),
        balance=float(res["power_balance_relative"]),
        svd_condition=float(res["edge_condition"]),
        forward_self_power=float(-res["total_outgoing_self_power"] / inc_left),
        cross_power=float(res["cross_power_left"] / inc_left),
        dissipation=float(res["dissipation_control_volume"] / inc_left),
        incident_Px=float(inc["Px"]), incident_Py=float(inc["Py"]),
        backward_Px=float(back["Px"]), backward_Py=float(back["Py"]),
        backward_K_real=float(np.real(res["backward_K"])),
        backward_K_imag=float(np.imag(res["backward_K"])),
        incident_K_real=float(np.real(res["incident_K"])),
        incident_K_imag=float(np.imag(res["incident_K"])),
        x_flux_fraction=float(abs(back["Px"]) /
                              max(np.hypot(back["Px"], back["Py"]), 1e-30)),
    )
    return out


def main() -> None:
    rows = []
    for name, K in CASES:
        for degree in DEGREES:
            row = one(degree, K)
            row["case"] = name
            rows.append(row)
            print(f"{name:16s} d={degree:2d} R_B={row.get('R_B', float('nan')):.6f} "
                  f"angle={row.get('angle_deg', float('nan')):8.3f} "
                  f"res={row.get('residual', float('nan')):.2e}", flush=True)
    # refinement verdict per case
    verdict = {}
    for name, _ in CASES:
        sel = [r for r in rows if r["case"] == name and r["status"] == "solved"]
        sel.sort(key=lambda r: r["degree"])
        if len(sel) < 2:
            verdict[name] = dict(certified=False, reason="not enough solved degrees")
            continue
        vals = np.array([r["R_B"] for r in sel])
        rel = float(np.max(np.abs(vals - vals[-1])) / max(abs(vals[-1]), 1e-30))
        ang = np.array([r["angle_deg"] for r in sel])
        ang_spread = float(np.max(np.abs(ang - ang[-1])))
        verdict[name] = dict(
            certified=bool(rel < 1e-3 and ang_spread < 0.5),
            max_relative_change=rel, max_angle_change_deg=ang_spread,
            R_B_finest=float(vals[-1]), angle_finest=float(ang[-1]),
        )
    dump_json("peak_certification.json", dict(rows=rows, verdict=verdict))
    print(json.dumps(verdict, indent=2))


if __name__ == "__main__":
    main()
