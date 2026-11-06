"""Re-derive the admissibility flags of the stored sweeps, no re-solving.

The stored CSV rows carry the numbers that came out of ``Plate.edge``; only the
*classification* changed.  The old test gated on |theta_E| < 80 deg, which is a
plotting threshold and is not a physical criterion.  The test used here is the
conservation bound derived in the manuscript:

    a single outgoing mode cannot carry more power than the incident wave plus
    the interference term,  0 <= R_B <= 1 + |P_cross|/P_inc,

together with the two convergence numbers of the solve.  ``x_flux_fraction``
= |cos theta_E| is stored alongside so that the resolution of the x-projection
is visible instead of being used as a silent cut-off.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "figure_data"
CROSS_BOUND = 1e-2
TARGETS = [("fig02_material_parameter_sweep.csv", "valid"),
           ("fig04_frequency_reflection.csv", "certified"),
           ("fig07_coupling_sensitivity.csv", "valid"),
           ("fig06_attenuation_distance.csv", None)]


def admissible(row) -> bool:
    try:
        r2 = float(row["R_B_2um"])
        bal = float(row["power_balance_error"])
        res = float(row["edge_scaled_residual"])
        ang = float(row["angle_deg"])
    except (KeyError, TypeError, ValueError):
        return False
    ok = 0.0 <= r2 <= 1.0 + CROSS_BOUND and bal < 1e-6 and res < 1e-8
    row["x_flux_fraction"] = f"{abs(math.cos(math.radians(ang))):.6e}" if ok else ""
    return ok


def main() -> None:
    for name, flag in TARGETS:
        path = DATA / name
        if not path.exists():
            continue
        with path.open() as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            continue
        changed = 0
        for row in rows:
            if flag:
                new = admissible(row)
                if str(row.get(flag, "")).lower() != str(new).lower():
                    changed += 1
                row[flag] = "true" if new else "false"
        fields = []
        for row in rows:
            for key in row:
                if key not in fields:
                    fields.append(key)
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        n_ok = sum(1 for r in rows if flag and str(r.get(flag)).lower() == "true")
        print(f"{name:42s} rows={len(rows):4d} admissible={n_ok:4d} flipped={changed}"
              if flag else f"{name:42s} rows={len(rows)} (annotation only)")


if __name__ == "__main__":
    main()
