"""Recompute only the group_speed_m_s column of fig01 / fig04 data with
build_figure_data.group_speed (symmetric difference, half-width 0.0025).
All other columns are untouched."""
import csv, sys
import numpy as np
sys.path.insert(0, ".")
import build_figure_data as B

def patch(name):
    path = f"figure_data/{name}"
    rows = list(csv.DictReader(open(path)))
    fields = list(rows[0].keys())
    for eta in sorted({float(r["eta"]) for r in rows}):
        idx = sorted([i for i, r in enumerate(rows) if float(r["eta"]) == eta],
                     key=lambda i: float(rows[i]["K"]))
        Ks = np.array([float(rows[i]["K"]) for i in idx])
        p = B.plate(eta)
        modes = B.track(p, Ks, B.operating_mode(p))
        vg = B.group_speed(p, Ks, modes)
        for i, v in zip(idx, vg):
            rows[i]["group_speed_m_s"] = repr(float(v))
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

for n in ("fig01_dispersion_velocity_attenuation.csv", "fig04_frequency_reflection.csv"):
    patch(n); print("patched", n)
