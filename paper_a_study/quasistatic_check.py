#!/usr/bin/env python3
"""Numerical justification of the quasistatic (retardation-free) electric model.

The manuscript does not use a generic "small device" argument.  At the actual
operating point it evaluates the dimensionless ratios that decide whether
electromagnetic retardation can be neglected, and separately reports the
carrier-relaxation ratio, which is *not* small and is therefore not
approximated away by the model.

Writes figure_data/quasistatic_audit.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_figure_data import K0, KY0, OMEGA0, plate  # noqa: E402
from model import CONST, SI  # noqa: E402

DATA = HERE / "figure_data"


def main() -> int:
    p = plate(0.0)
    q = CONST["q"]
    kB = CONST["kB"]
    c0 = 2.99792458e8
    eps0 = CONST["epsilon0"]

    d = p.d
    n0 = p.n0
    mu = p.mobility
    D = p.diffusivity
    kap33 = SI["kappa33"]
    kap_r = kap33 / eps0
    T = q * D / (mu * kB)

    omega = OMEGA0 * p.cs / d          # rad/s
    freq = omega / (2 * np.pi)
    period = 2 * np.pi / omega
    k = np.sqrt(K0 ** 2 + KY0 ** 2) / d

    sigma_e = q * mu * n0              # conductivity, S/m
    tau_dielectric = kap33 / sigma_e   # charge relaxation time, s
    lambda_em = c0 / (omega * np.sqrt(kap_r))
    v_p = omega / k

    out = {
        "operating_point": {"K0": K0, "KY0": KY0, "omega_over_cs_over_d": OMEGA0},
        "d_m": d,
        "frequency_Hz": float(freq),
        "period_s": float(period),
        "conductivity_S_per_m": float(sigma_e),
        "permittivity_F_per_m": float(kap33),
        "relative_permittivity": float(kap_r),
        "implied_temperature_K": float(T),
        # retardation
        "em_wavelength_m": float(lambda_em),
        "d_over_lambda_em": float(d / lambda_em),
        "kd_over_c_omega": float(k / (omega / c0) if False else k * c0 / omega),
        "phase_speed_m_per_s": float(v_p),
        "phase_speed_over_c": float(v_p / c0),
        "retardation_error_order": float((d / lambda_em) ** 2),
        # carrier relaxation (NOT assumed instantaneous)
        "dielectric_relaxation_time_s": float(tau_dielectric),
        "omega_tau_dielectric": float(omega * tau_dielectric),
        "tau_over_period": float(tau_dielectric / period),
        # screening
        "debye_length_m": float(np.sqrt(kap33 * kB * T / (q ** 2 * n0))),
        "d_over_debye": float(d / np.sqrt(kap33 * kB * T / (q ** 2 * n0))),
        "diffusion_length_over_d": float(np.sqrt(D / omega) / d),
    }

    print("quasistatic audit at the operating point")
    print(f"  frequency                          {freq/1e9:.3f} GHz")
    print(f"  conductivity                       {sigma_e:.3f} S/m")
    print(f"  relative permittivity              {kap_r:.2f}")
    print(f"  EM wavelength in the medium        {lambda_em*1e3:.3f} mm")
    print(f"  d / lambda_EM                      {d/lambda_em:.3e}")
    print(f"  phase speed / c                    {v_p/c0:.3e}")
    print(f"  (d/lambda_EM)^2                    {(d/lambda_em)**2:.3e}")
    print(f"  omega * tau_dielectric             {omega*tau_dielectric:.3f}"
          "   (carrier response is NOT instantaneous)")
    print(f"  tau_dielectric / period            {tau_dielectric/period:.3f}")
    print(f"  d / Debye length                   {d/out['debye_length_m']:.4f}")

    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "quasistatic_audit.json").write_text(json.dumps(out, indent=2))
    print("wrote", DATA / "quasistatic_audit.json")

    ok = (d / lambda_em) < 1e-3 and (v_p / c0) ** 2 < 1e-6
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
