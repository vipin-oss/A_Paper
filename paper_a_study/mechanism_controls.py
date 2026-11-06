#!/usr/bin/env python3
"""Issue D: which ingredient actually produces the negative reflection?

Matched controls at the two reported operating points.  Everything except the
named ingredient is held fixed: same wavenumbers, same carrier parameters, same
reference plane, same incident normalisation.  The frequency is allowed to
follow the branch, because switching off the strain gradient changes the
dispersion and comparing solutions at different frequencies of a *different*
branch would not be a control.

Configurations
    1 full          f = 1 nC/m, H = +0.05 H_ref      (the paper's model)
    2 no_flexo      f = 0,      H = +0.05 H_ref
    3 no_coupling   f = 1 nC/m, H = 0
    4 no_flexo_H    f = 0,      H = 0
    5 classical     ell = 0,    f = 0, H = 0         (no strain gradient at all)

Writes figure_data/mechanism_controls.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_figure_data import (HCRIT, KB0, KY0, edge_plane_fraction,  # noqa: E402
                               operating_mode, plate, track)
from model import Plate  # noqa: E402

DATA = HERE / "figure_data"
CASES = {"operating_point": 0.7361990195318475, "refined_peak": 0.5275,
         "round7_sample": 0.525, "k055_sample": 0.55}
ETA_COUPLING = 0.05

CONFIGS = {
    "full": dict(flexo=1e-9, eta=ETA_COUPLING),
    "no_flexo": dict(flexo=0.0, eta=ETA_COUPLING),
    "no_coupling": dict(flexo=1e-9, eta=0.0),
    "no_flexo_H": dict(flexo=0.0, eta=0.0),
    "classical": dict(flexo=0.0, eta=0.0, ell=0.0),
}


def run(case_K: float, cfg: dict, degree: int = 22) -> dict:
    kw = {}
    if cfg.get("ell") == 0.0:
        p0 = Plate(degree=degree, ell=0.0, flexo=0.0, H=0.0)
    else:
        p0 = plate(0.0, degree=degree, flexo=cfg["flexo"])
    H = cfg["eta"] * HCRIT
    p = Plate(degree=degree, flexo=kw.get("flexo", cfg["flexo"]), H=H,
              ell=50e-9 if cfg.get("ell") != 0.0 else 0.0)
    try:
        mode = track(p, [case_K], operating_mode(p))[0]
    except Exception as exc:                       # noqa: BLE001
        return {"status": f"branch tracking failed: {type(exc).__name__}"}
    omega = float(mode["omega"].real)
    try:
        res, _ = p.edge(KY0, omega, case_K, KB0)
    except Exception as exc:                       # noqa: BLE001
        return {"status": f"edge solve failed: {type(exc).__name__}",
                "frequency_GHz": omega * p.fscale / 1e9}
    return {
        "status": "solved",
        "frequency_GHz": float(omega * p.fscale / 1e9),
        "R_B": float(res["backward_reflection_self_power"]),
        "angle_deg": float(res["reflected_angle_deg"]),
        "backward_K": complex(res["backward_K"]),
        "incident_K": complex(res["incident_K"]),
        "total_outgoing_propagating": float(-res["total_outgoing_self_power"]
                                            / res["incident_power_left"]),
        "cross": float(res["cross_power_left"] / res["incident_power_left"]),
        # edge-plane share on the same convention as the tabulated
        # configurations: both modes rescaled from the reference plane to x=0.
        "R_B_edge": edge_plane_fraction(float(res["backward_reflection_self_power"]),
                                        complex(res["incident_K"]),
                                        complex(res["backward_K"]), 1.0),
        "dissipation": float(res["dissipation_control_volume"]
                             / res["incident_power_left"]),
        "backward_energy": float(res["backward"]["energy"]),
        "backward_vEx": float(res["backward"]["vEx"]),
        "incident_vEx": float(res["incident"]["vEx"]),
        "power_balance_relative": float(res["power_balance_relative"]),
        "outgoing_modes": int(res["outgoing_modes"]),
        "negative_direction": bool(res["negative_direction"]),
        # A genuine backward port has Re K_B > 0 with negative x-power.  If the
        # strain-gradient sector is removed no such branch exists, and the
        # target heuristic falls back on the specular reflection, whose
        # wavenumber is exactly -k_incident.  Classify instead of pretending.
        "backward_is_specular": bool(abs(complex(res["backward_K"]) + complex(res["incident_K"]))
                                     < 1e-6 * abs(complex(res["incident_K"]))),
        "port": ("backward" if (res["negative_direction"]
                                and complex(res["backward_K"]).real > 0) else "no_backward_port"),
    }


def tracked_sweep(case_K: float, etas=(0.05, 0.025, 0.0, -0.025, -0.05)) -> list[dict]:
    """R_B along the branch: k_x fixed, frequency tracked, H varied.

    This is the branch-consistent sensitivity.  The fixed-frequency sweeps of
    Figures 5 and 7 answer a different question (the incident wavenumber drifts
    with H there), and the two are reported separately on purpose.
    """
    rows = []
    for eta in etas:
        p = Plate(degree=22, flexo=1e-9, H=eta * HCRIT, ell=50e-9)
        m = track(p, [case_K], operating_mode(p))[0]
        omega = float(m["omega"].real)
        res, _ = p.edge(KY0, omega, case_K, KB0)
        rows.append(dict(eta=float(eta), frequency_GHz=float(omega * p.fscale / 1e9),
                         R_B=float(res["backward_reflection_self_power"]),
                         angle_deg=float(res["reflected_angle_deg"]),
                         backward_K_real=float(complex(res["backward_K"]).real),
                         backward_K_imag=float(complex(res["backward_K"]).imag),
                         R_B_edge=edge_plane_fraction(
                             float(res["backward_reflection_self_power"]),
                             complex(res["incident_K"]), complex(res["backward_K"]), 1.0),
                         dissipation=float(res["dissipation_control_volume"]
                                           / res["incident_power_left"]),
                         power_balance_relative=float(res["power_balance_relative"])))
    return rows


def reoptimised(eta: float, lo: float = 0.518, hi: float = 0.538,
                step: float = 1e-3, degree: int = 22) -> dict:
    """Largest admissible backward fraction at this H, searched afresh.

    Comparison (C) of the coupling analysis: the extremum is allowed to move
    with H, so this answers "how much backward power can this coupling level
    deliver at best" rather than "what happens to the H = 0 extremum".
    """
    grid = list(np.round(np.arange(lo, hi + 0.5 * step, step), 6))
    p = Plate(degree=degree, flexo=1e-9, H=eta * HCRIT, ell=50e-9)
    modes = track(p, grid, operating_mode(p))
    best = None
    for K, m in zip(grid, modes):
        try:
            res, _ = p.edge(KY0, float(m["omega"].real), float(K), KB0)
        except Exception:                              # noqa: BLE001
            continue
        r = dict(K=float(K), R_B=float(res["backward_reflection_self_power"]),
                 frequency_GHz=float(res["frequency_Hz"]) / 1e9,
                 R_B_edge=edge_plane_fraction(
                     float(res["backward_reflection_self_power"]),
                     complex(res["incident_K"]), complex(res["backward_K"]), 1.0),
                 power_balance_relative=float(res["power_balance_relative"]))
        if best is None or r["R_B"] > best["R_B"]:
            best = dict(r, neighbour_points=len(grid))
    fine = list(np.round(np.arange(best["K"] - 1.5e-3, best["K"] + 1.5e-3 + 5e-5, 1e-4), 6))
    p = Plate(degree=degree, flexo=1e-9, H=eta * HCRIT, ell=50e-9)
    modes = track(p, fine, operating_mode(p))
    rb = []
    for K, m in zip(fine, modes):
        res, _ = p.edge(KY0, float(m["omega"].real), float(K), KB0)
        rb.append(dict(K=float(K), R_B=float(res["backward_reflection_self_power"]),
                       frequency_GHz=float(res["frequency_Hz"]) / 1e9))
    ref = max(rb, key=lambda r: r["R_B"])
    return dict(eta=float(eta), coarse_best=best, refined_best=ref,
                coarse_step=step, refine_step=1e-4, domain=[lo, hi],
                refined_rows=rb)


def main() -> int:
    out: dict[str, dict] = {}
    for case, K in CASES.items():
        out[case] = {}
        for name, cfg in CONFIGS.items():
            r = run(K, cfg)
            out[case][name] = r
            if r["status"] != "solved":
                print(f"{case:15s} {name:12s} {r['status']}")
                continue
            print(f"{case:15s} {name:12s} f={r['frequency_GHz']:8.4f} GHz  "
                  f"R_B={r['R_B']:.9f}  angle={r['angle_deg']:+8.3f}  "
                  f"v_gB={r['backward_vEx']:+10.2f}  bal={r['power_balance_relative']:.1e}")

    # incremental effects
    print("\nincremental effects (same branch, same k)")
    for case in CASES:
        c = out[case]
        if c["no_flexo_H"]["status"] != "solved":
            continue
        base = c["no_flexo_H"]["R_B"]
        print(f"\n{case}")
        for name in ("full", "no_flexo", "no_coupling"):
            if c[name]["status"] == "solved":
                d = 100 * (c[name]["R_B"] - base) / base
                print(f"  {name:12s} R_B={c[name]['R_B']:.9f}  "
                      f"change vs f=H=0: {d:+.4f} %")
        if c["classical"]["status"] == "solved":
            print(f"  classical    R_B={c['classical']['R_B']:.9f}  "
                  f"(strain gradient removed)")
        else:
            print(f"  classical    {c['classical']['status']}")

    print("\nbranch-consistent H sweep (k_x fixed, frequency tracked)")
    sweeps = {case: tracked_sweep(K) for case, K in CASES.items()}
    for case, rows in sweeps.items():
        base = [r["R_B"] for r in rows if r["eta"] == 0.0][0]
        for r in rows:
            print(f"  {case:15s} H/H*={r['eta']:+.3f}  f={r['frequency_GHz']:8.4f}  "
                  f"R_B={r['R_B']:.9f}  {100 * (r['R_B'] - base) / base:+7.3f} %  "
                  f"R_B_edge={r['R_B_edge']:.6f}  "
                  f"ImK_B={r['backward_K_imag']:+.3e}")
    out["branch_consistent_H_sweep"] = sweeps

    print("\nre-optimised peak per coupling level (search restarted for each H)")
    reopt = {}
    for eta in (0.05, 0.025, 0.0, -0.025, -0.05):
        r = reoptimised(eta)
        reopt[f"{eta:+.3f}"] = r
        print(f"  H/H*={eta:+.3f}  coarse K={r['coarse_best']['K']:.4f}  "
              f"refined K={r['refined_best']['K']:.4f}  "
              f"R_B={r['refined_best']['R_B']:.9f}  "
              f"f={r['refined_best']['frequency_GHz']:.4f} GHz")
    out["reoptimised_peak"] = reopt

    DATA.mkdir(parents=True, exist_ok=True)

    def enc(o):
        if isinstance(o, complex):
            return [o.real, o.imag]
        raise TypeError

    (DATA / "mechanism_controls.json").write_text(
        json.dumps(out, indent=2, default=enc))
    print("\nwrote", DATA / "mechanism_controls.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
