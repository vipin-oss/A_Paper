#!/usr/bin/env python3
"""Machine-checkable reconciliation of every speed, wavenumber and frequency.

Issue A of the final audit reported a factor-of-ten discrepancy between the
phase speed quoted in the text and the value implied by the frequency,
thickness and dimensionless wavenumbers.  This script recomputes every
conversion from first principles in SI units and compares the result with

  * the figure data (figure_data/fig01_*.csv),
  * the numbers quoted in the manuscript.

Nothing is scaled to make anything agree: each quantity is reconstructed from
its definition and the residual is printed.

Writes figure_data/phase_speed_audit.json and prints a table.
"""
from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_figure_data import K0, KY0, OMEGA0, plate  # noqa: E402

DATA = HERE / "figure_data"

# Numbers as they appear in the *corrected* manuscript.  The values this script
# was written to audit are kept below as HISTORICAL_PRE_FIX so that the audit
# trail survives; the checker itself must verify the text that is shipped.
MANUSCRIPT = {
    "v_p_governing_eq": 28.0e3,         # governing_equations.tex, eq:governing_electric
    "v_p_results_min": 20.0e3,          # results.tex, fig01 panel (b)
    "v_p_results_max": 105.8e3,
    "frequency_GHz": 16.68,
    "lambda_em_mm": 5.68,               # = 2 pi / k_EM, governing_equations.tex
    "inverse_k_em_mm": 0.905,           # 1/k_EM, quoted separately in the text
    "k_em_times_d": 2.2e-4,             # retardation parameter
    "d_over_lambda_em": 3.52e-5,
}

# Round-4 findings, recorded as evidence and never used as a target.
HISTORICAL_PRE_FIX = {
    "v_p_governing_eq": 2.8e3,          # factor 10.016 low
    "lambda_em_mm": 0.905,              # this is 1/k_EM, not a wavelength
    "d_over_lambda_em": 2.2e-4,         # this is k_EM d
}


def main() -> int:
    p = plate(0.0)
    d = p.d
    cs = p.cs
    kap33 = p.kap[2, 2] * __import__("model").SI["kappa33"]
    eps0 = 8.8541878188e-12
    kappa_r = kap33 / eps0
    c0 = 2.99792458e8

    kx = K0 / d                       # rad/m
    ky = KY0 / d
    k = math.hypot(kx, ky)
    omega = OMEGA0 * cs / d           # rad/s
    freq = omega / (2 * math.pi)      # Hz
    lam_mech = 2 * math.pi / k
    v_p = omega / k

    # e.m. quantities at the same frequency
    k_em = omega * math.sqrt(kappa_r) / c0
    lam_em = 2 * math.pi / k_em
    v_em = c0 / math.sqrt(kappa_r)

    # figure data at the operating point
    rows = list(csv.DictReader(open(DATA / "fig01_dispersion_velocity_attenuation.csv")))
    row = min(rows, key=lambda r: abs(float(r["K"]) - K0))
    csv_vp = float(row["phase_speed_m_s"])
    csv_f = float(row["frequency_GHz"])
    maxK = max(rows, key=lambda r: float(r["K"]))
    minK = min(rows, key=lambda r: float(r["K"]))

    out = {
        "inputs": {"K0": K0, "KY0": KY0, "OMEGA0": OMEGA0, "d_m": d,
                   "c_s_m_per_s": cs, "kappa33_F_per_m": kap33,
                   "kappa_r": kappa_r},
        "derived": {
            "k_x_rad_per_m": kx, "k_y_rad_per_m": ky, "k_rad_per_m": k,
            "omega_rad_per_s": omega, "frequency_Hz": freq,
            "mechanical_wavelength_m": lam_mech,
            "phase_speed_m_per_s": v_p,
            "v_p_over_c": v_p / c0,
            "k_em_rad_per_m": k_em, "lambda_em_m": lam_em,
            "v_em_m_per_s": v_em,
            "k_em_d": k_em * d, "d_over_lambda_em": d / lam_em,
            "k_em_d_squared": (k_em * d) ** 2,
            "v_p_over_c_squared": (v_p / c0) ** 2,
            "frequency_from_omega_GHz": freq / 1e9,
            "wavelength_from_v_over_f_m": v_em / freq,
        },
        "figure_data_at_operating_point": {
            "K": float(row["K"]), "phase_speed_m_s": csv_vp,
            "frequency_GHz": csv_f,
            # independent reconstruction: v_p = 2 pi f / |k|, with |k| from the
            # row's own K and the conserved k_y d.  This tests the figure data
            # against itself using a different route than the code that wrote it.
            "v_p_from_own_frequency": float(
                2 * math.pi * csv_f * 1e9
                / (math.hypot(float(row["K"]), KY0) / d)),
            "v_p_at_K0_exact": float(v_p),
            "v_p_at_K0_interpolated": float(
                csv_vp + (v_p - csv_vp) * 0),
        },
        "figure_extremes": {
            "min_K": float(minK["K"]), "v_p_at_min_K": float(minK["phase_speed_m_s"]),
            "max_K": float(maxK["K"]), "v_p_at_max_K": float(maxK["phase_speed_m_s"]),
        },
        "manuscript_values": MANUSCRIPT,
    }

    print("ISSUE A - phase speed and wavenumber reconciliation")
    print("=" * 66)
    print("inputs")
    print(f"  d                      = {d:.3e} m      (full plate thickness)")
    print(f"  c_s = sqrt(c44/rho)    = {cs:.4f} m/s")
    print(f"  k_x d                  = {K0:.10f}       (dimensionless)")
    print(f"  k_y d                  = {KY0:.10f}")
    print(f"  omega d / c_s          = {OMEGA0:.10f}   (dimensionless)")
    print("\nreconstruction (SI)")
    print(f"  k_x                    = {kx:.6e} rad/m   = k_x d / d")
    print(f"  k_y                    = {ky:.6e} rad/m")
    print(f"  |k|                    = {k:.6e} rad/m")
    print(f"  lambda_mech = 2pi/|k|  = {lam_mech:.6e} m")
    print(f"  omega                  = {omega:.6e} rad/s")
    print(f"  f = omega/(2 pi)       = {freq/1e9:.6f} GHz")
    print(f"  v_p = omega/|k|        = {v_p:.2f} m/s  = {v_p/1e3:.3f} km/s")
    print(f"  v_p / c                = {v_p/c0:.4e}")
    print(f"  f * lambda_mech        = {freq*lam_mech:.2f} m/s   (must equal v_p)")

    print("\n  manuscript values")
    for name, val in MANUSCRIPT.items():
        print(f"    {name:22s} {val:.6g}")
    print("\n  residuals against the reconstruction")
    rec = out["figure_data_at_operating_point"]["v_p_from_own_frequency"]
    checks = [
        ("v_p in governing_equations.tex", MANUSCRIPT["v_p_governing_eq"], v_p),
        ("frequency", MANUSCRIPT["frequency_GHz"] * 1e9, freq),
        ("figure-data v_p vs its own freq", csv_vp, rec),
        ("figure-data frequency", csv_f * 1e9, freq),
    ]
    ok = True
    for name, got, want in checks:
        rel = abs(got - want) / abs(want)
        flag = "ok" if rel < 5e-3 else "MISMATCH"
        ok &= rel < 5e-3
        print(f"    {name:32s} {got: .6e} vs {want: .6e}   rel={rel:.2e}  {flag}")

    print("\nISSUE B - electromagnetic scaling")
    print(f"  k_EM = omega sqrt(kappa_r)/c = {k_em:.6e} rad/m")
    print(f"  lambda_EM = 2 pi / k_EM      = {lam_em*1e3:.6f} mm   (= v_EM/f = {v_em/freq*1e3:.6f} mm)")
    print(f"  1/k_EM  (NOT a wavelength)   = {1/k_em*1e3:.6f} mm")
    print(f"  k_EM d                       = {k_em*d:.6e}")
    print(f"  d / lambda_EM                = {d/lam_em:.6e}")
    print(f"  (k_EM d)^2                   = {(k_em*d)**2:.6e}")
    print(f"\n  manuscript (corrected): lambda_EM = {MANUSCRIPT['lambda_em_mm']} mm,"
          f" 1/k_EM = {MANUSCRIPT['inverse_k_em_mm']} mm,"
          f" k_EM d = {MANUSCRIPT['k_em_times_d']:.2g},"
          f" d/lambda_EM = {MANUSCRIPT['d_over_lambda_em']:.2g}")
    b_checks = [
        ("lambda_EM", MANUSCRIPT["lambda_em_mm"] * 1e-3, lam_em),
        ("1/k_EM", MANUSCRIPT["inverse_k_em_mm"] * 1e-3, 1 / k_em),
        ("k_EM d", MANUSCRIPT["k_em_times_d"], k_em * d),
        ("d/lambda_EM", MANUSCRIPT["d_over_lambda_em"], d / lam_em),
    ]
    for name, got, want in b_checks:
        rel = abs(got - want) / abs(want)
        flag = "ok" if rel < 5e-3 else "MISMATCH"
        ok &= rel < 5e-3
        print(f"    {name:16s} {got: .6e} vs {want: .6e}   rel={rel:.2e}  {flag}")
    print("  round-4 pre-fix values (evidence only): "
          f"v_p = {HISTORICAL_PRE_FIX['v_p_governing_eq']:.4g} m/s, "
          f"lambda_EM = {HISTORICAL_PRE_FIX['lambda_em_mm']} mm (= 1/k_EM), "
          f"d/lambda = {HISTORICAL_PRE_FIX['d_over_lambda_em']:.2g} (= k_EM d)")
    out["historical_pre_fix"] = dict(HISTORICAL_PRE_FIX)

    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "phase_speed_audit.json").write_text(json.dumps(out, indent=2))
    print("\nwrote", DATA / "phase_speed_audit.json")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
