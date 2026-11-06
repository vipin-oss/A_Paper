"""Validate revised Paper A data and manuscript-figure consistency."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "paper_a_study" / "figure_data"
RESULTS = ROOT / "paper_a_study" / "results"


def rows(name: str) -> list[dict]:
    with (DATA / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def finite(value: str) -> bool:
    return value != "" and math.isfinite(float(value))


def main():
    checks: list[tuple[str, bool, str]] = []
    data = {name: rows(name) for name in [
        "fig01_dispersion_velocity_attenuation.csv",
        "fig02_material_parameter_sweep.csv",
        "fig03_geometry_sweep.csv",
        "fig04_frequency_reflection.csv",
        "fig05_channel_power.csv",
        "fig06_attenuation_distance.csv",
        "fig07_coupling_sensitivity.csv",
        "fig08_boundary_sensitivity.csv",
        "fig09_validation_convergence.csv",
    ]}
    for name, rows_value in data.items():
        if not rows_value:
            checks.append((f"{name} nonempty", False, "empty data"))
            continue
        checks.append((f"{name} nonempty", True, f"{len(rows_value)} rows"))

    # No NaN/Inf and no out-of-range fraction.
    for row in data["fig05_channel_power.csv"]:
        fraction = float(row["total_outgoing_fraction"])
        checks.append((f"fig05 fraction {row['eta']}", math.isfinite(fraction) and -1e-9 <= fraction <= 1.0 + 1e-9, str(fraction)))
    for row in data["fig06_attenuation_distance.csv"]:
        survival = float(row["incident_self_flux"])
        checks.append((f"fig06 survival finite {row['eta']}", math.isfinite(survival), str(survival)))

    # Primary edge and field metrics.
    primary = json.loads((RESULTS / "primary_edge_revised.json").read_text())
    checks.append(("primary edge present", len(primary) == 3, f"{len(primary)} rows"))
    checks.append(("primary edge residual", all(math.isfinite(float(r["edge_scaled_residual"])) and float(r["edge_scaled_residual"]) < 1e-10 for r in primary), str(min(float(r["edge_scaled_residual"]) for r in primary))))
    checks.append(("primary power balance", all(math.isfinite(float(r["power_balance_relative"])) and float(r["power_balance_relative"]) < 1e-8 for r in primary), str(max(float(r["power_balance_relative"]) for r in primary))))
    checks.append(("primary backward fraction bounded", all(0.0 <= float(r["backward_reflection_self_power"]) <= 1.0 for r in primary), str([float(r["backward_reflection_self_power"]) for r in primary])))

    metrics = json.loads((DATA / "fig10_field_metrics.json").read_text())
    checks.append(("fig10 metrics", len(metrics) == 2, f"{len(metrics)} planes"))
    checks.append(("fig10 centroid finite", all(math.isfinite(float(m["backward_centroid_y_um"])) for m in metrics), str([float(m["backward_centroid_y_um"]) for m in metrics])))

    # Convergence monotonicity for power error is not guaranteed at every single
    # resolution, but the primary-level value must be small.
    convergence = data["fig09_validation_convergence.csv"]
    baseline = float([r for r in convergence if r["method"] == "Legendre" and float(r["resolution"]) == 22][0]["R_B"])
    deviation = max(abs(float(r["R_B"]) - baseline) for r in convergence if r["method"] == "Legendre")
    checks.append(("convergence primary deviation", deviation < 1e-7, str(deviation)))

    print("Validation summary")
    print(f"checks: {len(checks)}, passed: {sum(passed for _, passed, _ in checks)}")
    failures = [(name, value) for name, passed, value in checks if not passed]
    if failures:
        print("FAILURES")
        for name, value in failures:
            print(f"{name}: {value}")
        raise SystemExit(1)
    print("All revised data checks passed.")


if __name__ == "__main__":
    main()
