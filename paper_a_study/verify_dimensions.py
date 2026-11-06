#!/usr/bin/env python3
"""Dimensional and constitutive-consistency audit of the Paper A model.

Three independent checks, none of which needs a symbolic algebra package:

1.  Dimensional homogeneity of every relation quoted in the manuscript, using
    explicit exponents in SI base units (L, M, T, I) with kg, m, s, A.
2.  That the solver's dimensionless groups equal their analytic expressions
    evaluated from the material file, and that the coupling constant
    h = H/(d sqrt(a c44)) is dimensionless.
3.  That the strain-gradient tensor implemented by the solver has the index
    contraction A_(ijk)(lmn) = ell^2 c_(ij)(lm) delta_(kn).  The two candidate
    contractions predict different exact shear-horizontal branches, so the
    solver's own branch identifies the implemented one.

Writes figure_data/dimension_audit.json and prints a table.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from model import CONST, SI, Plate  # noqa: E402

DATA = HERE / "figure_data"

# Exponents in (L, M, T, I); SI base units kg, m, s, A.
DIM = {
    "length": (1, 0, 0, 0),
    "displacement": (1, 0, 0, 0),
    "strain": (0, 0, 0, 0),
    "strain_gradient": (-1, 0, 0, 0),
    "stress": (-1, 1, -2, 0),              # Pa
    "elastic_modulus": (-1, 1, -2, 0),     # Pa
    "gradient_modulus": (1, 1, -2, 0),     # N  == J/m
    "hyperstress": (0, 1, -2, 0),          # N/m
    "energy_density": (-1, 1, -2, 0),      # J/m^3
    "electric_field": (1, 1, -3, -1),      # V/m
    "potential": (2, 1, -3, -1),           # V
    "charge": (0, 0, 1, 1),                # C
    "charge_density": (-3, 0, 1, 1),       # C/m^3
    "displacement_field": (-2, 0, 1, 1),   # C/m^2
    "permittivity": (-3, -1, 4, 2),        # F/m
    "piezoelectric": (-2, 0, 1, 1),        # C/m^2
    "flexoelectric": (-1, 0, 1, 1),        # C/m
    "carrier_density": (-3, 0, 0, 0),      # 1/m^3
    "compressibility": (5, 1, -2, 0),      # J m^3
    "H_coupling": (3, 1, -2, 0),           # J m
    "energy_per_carrier": (2, 1, -2, 0),   # J
    "mobility": (0, -1, 2, 1),             # m^2/(V s)
    "diffusivity": (2, 0, -1, 0),          # m^2/s
    "current_density": (-2, 0, 0, 1),      # A/m^2
    "number_flux": (-2, 0, -1, 0),         # 1/(m^2 s)
    "mass_density": (-3, 1, 0, 0),         # kg/m^3
    "power_flux": (0, 1, -3, 0),           # W/m^2
    "force_density": (-2, 1, -2, 0),       # N/m^3
    "time": (0, 0, 1, 0),
}


def add(*keys):
    out = [0, 0, 0, 0]
    for k in keys:
        for i in range(4):
            out[i] += DIM[k][i]
    return tuple(out)


def sub(a, *keys):
    out = list(DIM[a])
    for k in keys:
        for i in range(4):
            out[i] -= DIM[k][i]
    return tuple(out)


def report(rows):
    good = True
    for name, got, want in rows:
        flag = "ok" if got == want else "MISMATCH"
        good &= got == want
        print(f"  {name:44s} {str(got):20s} {str(want):20s} {flag}")
    return good


def dimensional_audit() -> bool:
    print("1. dimensional homogeneity of the formulation")
    # [rho u_tt]
    rho_utt = tuple(add("mass_density", "displacement")[i] - [0, 0, 2, 0][i]
                    for i in range(4))
    # [phi dD/dt]
    phi_dD = tuple(add("potential", "displacement_field")[i] - [0, 0, 1, 0][i]
                   for i in range(4))
    # [mu J_n] : energy per carrier times number flux gives J/(m^2 s) = W/m^2
    mu_J = add("energy_per_carrier", "number_flux")
    # [D n0 / mu * grad mu]
    jn = tuple(DIM["diffusivity"][i] + DIM["carrier_density"][i] - DIM["length"][i]
               for i in range(4))
    rows = [
        ("[strain] = 1", DIM["strain"], (0, 0, 0, 0)),
        ("[strain gradient] = 1/L", sub("strain", "length"),
         DIM["strain_gradient"]),
        ("[stress] = [c][strain]", DIM["elastic_modulus"], DIM["stress"]),
        ("[w_g] = [A][eta]^2", add("gradient_modulus", "strain_gradient",
                                   "strain_gradient"), DIM["energy_density"]),
        ("[A] = L^2[c] = N (not Pa)",
         add("elastic_modulus", "length", "length"), DIM["gradient_modulus"]),
        ("[A] in SI base units (kg m/s^2)", DIM["gradient_modulus"], (1, 1, -2, 0)),
        ("[tau] = [w_g]/[eta]", sub("energy_density", "strain_gradient"),
         DIM["hyperstress"]),
        ("[tau] = [A][eta]", add("gradient_modulus", "strain_gradient"),
         DIM["hyperstress"]),
        ("[H dn] = [tau] = N/m", add("H_coupling", "carrier_density"),
         DIM["hyperstress"]),
        ("[H eta] = [mu] = J", add("H_coupling", "strain_gradient"),
         DIM["energy_per_carrier"]),
        ("[H] = J m", DIM["H_coupling"], (3, 1, -2, 0)),
        ("[D] = [kappa][E]", add("permittivity", "electric_field"),
         DIM["displacement_field"]),
        ("[D] = [e][strain]", DIM["piezoelectric"], DIM["displacement_field"]),
        ("[D] = [f][eta]", add("flexoelectric", "strain_gradient"),
         DIM["displacement_field"]),
        ("[f] = C/m", DIM["flexoelectric"], (-1, 0, 1, 1)),
        ("[a dn] = [mu] = J", add("compressibility", "carrier_density"),
         DIM["energy_per_carrier"]),
        ("[a] = J m^3", DIM["compressibility"], (5, 1, -2, 0)),
        ("[q phi] = [mu] = J", add("charge", "potential"),
         DIM["energy_per_carrier"]),
        ("[J_n] = [D n0/mu][grad mu]", jn, DIM["number_flux"]),
        ("[j] = q[J_n]", add("charge", "number_flux"), DIM["current_density"]),
        ("[d sigma/dx] = N/m^3", sub("stress", "length"), DIM["force_density"]),
        ("[d2 tau/dx2] = N/m^3", sub("hyperstress", "length", "length"),
         DIM["force_density"]),
        ("[rho u_tt] = N/m^3", rho_utt, DIM["force_density"]),
        ("[phi dD/dt] = W/m^2", phi_dD, DIM["power_flux"]),
        ("[mu J_n] = W/m^2", mu_J, DIM["power_flux"]),
    ]
    return report(rows)


def numeric_groups() -> dict:
    """Analytic expressions for the solver's dimensionless groups.

    The solver works in units where c44 = 1 and kappa33 = 1, so the SI values
    are taken from the material file itself rather than from the solver's
    normalised arrays.
    """
    p = Plate(degree=10)              # defaults carry the operating material
    q = CONST["q"]
    kB = CONST["kB"]
    c44 = SI["c44"]
    kap33 = SI["kappa33"]
    T = q * p.diffusivity / (p.mobility * kB)      # implied by the Einstein relation
    a = kB * T / p.n0
    LD = np.sqrt(kap33 * kB * T / (q ** 2 * p.n0))
    # The Schur complement of the in-plane block of the 6mm stiffness is the
    # reduced modulus c* = c33 - 2 c13^2/(c11 + c12), not c33 itself.
    c_red = SI["c33"] - 2.0 * SI["c13"] ** 2 / (SI["c11"] + SI["c12"])
    H_test = 2.00485322e-23
    p2 = Plate(degree=10, H=H_test)
    return {
        "d_m": float(p.d),
        "n0_per_m3": float(p.n0),
        "T_implied_K": float(T),
        "a_analytic_J_m3": float(a),
        "a_code": float(p.a),
        "debye_length_m": float(LD),
        "Q_code": float(p.Q),
        "Q_analytic": float(p.d / LD),
        "alpha_code": float(p.alpha),
        "alpha_analytic": float(p.diffusivity / (p.d * p.cs)),
        "lambda": float(p.lam),
        "f_code": float(p.f),
        "f_analytic": float(p.flexo_SI / (p.d * np.sqrt(c44 * kap33))),
        "c_reduced_Pa": float(c_red),
        "H_bound_J_m": float(p.ell_SI * np.sqrt(a * c_red)),
        "schur_code_at_Htest": float(p2.schur),
        "schur_analytic_at_Htest": float(H_test ** 2 / (c_red * p.ell_SI ** 2 * a)),
        "h_per_eta": float(p2.h / 0.05),
        "sigma_e_S_per_m": float(q * p.mobility * p.n0),
        "epsilon33_F_per_m": float(kap33),
        "cs_m_per_s": float(p.cs),
    }


def tensor_contraction_check() -> dict:
    """Identify the implemented contraction from the exact SH branch."""
    p = Plate(degree=22, ell=50e-9, flexo=0.0)
    K = 0.8
    sh = [m["omega"] for m in p.temporal(K)
          if np.vdot(m["U"][p.n:2 * p.n], p.W @ m["U"][p.n:2 * p.n]).real > 0.999]
    cand1 = np.sqrt(p.C[5, 5] * K * K * (1 + p.lam ** 2 * K * K))
    cand2 = np.sqrt(p.C[5, 5] * K * K + p.lam ** 2 * K ** 2 * (np.pi / p.d) ** 2)
    e1 = min(abs(a - cand1) for a in sh)
    e2 = min(abs(a - cand2) for a in sh)
    print("\n3. strain-gradient index contraction (exact SH branch, K = 0.8)")
    print(f"  A = ell^2 c_(ij)(lm) delta_(kn)   |dw| = {e1:.3e}")
    print(f"  A = ell^2 c_(ij)(kl) delta_(mn)   |dw| = {e2:.3e}")
    return {"candidate1_residual": float(e1), "candidate2_residual": float(e2),
            "implemented": "A_(ijk)(lmn) = ell^2 c_(ij)(lm) delta_(kn)",
            "verdict": "candidate 1" if e1 < e2 else "candidate 2"}


def main() -> int:
    ok = dimensional_audit()

    print("\n2. dimensionless groups against their analytic forms")
    g = numeric_groups()
    for name, got, want in [
        ("Q = d / L_D", g["Q_code"], g["Q_analytic"]),
        ("alpha = D / (d c_s)", g["alpha_code"], g["alpha_analytic"]),
        ("f = f33 / (d sqrt(c44 kappa33))", g["f_code"], g["f_analytic"]),
        ("a = k_B T / n0  [J m^3]", g["a_code"], g["a_analytic_J_m3"]),
    ]:
        rel = abs(got - want) / max(abs(want), 1e-300)
        ok &= rel < 1e-12
        print(f"  {name:34s} {got: .10e} {want: .10e} rel={rel:.1e} "
              f"{'ok' if rel < 1e-12 else 'MISMATCH'}")
    print(f"  {'c* = c33 - 2c13^2/(c11+c12) [GPa]':34s} {g['c_reduced_Pa']/1e9: .6e}")
    print(f"  {'H_bound = ell sqrt(a c*) [J m]':34s} {g['H_bound_J_m']: .6e}")
    print(f"  {'schur at H_test (code)':34s} {g['schur_code_at_Htest']: .6e}")
    print(f"  {'schur at H_test (analytic)':34s} {g['schur_analytic_at_Htest']: .6e}")
    print(f"  {'h per unit eta (dimensionless)':34s} {g['h_per_eta']: .6e}")
    rel = abs(g["schur_code_at_Htest"] - g["schur_analytic_at_Htest"]) \
        / g["schur_analytic_at_Htest"]
    ok &= rel < 1e-10
    print(f"  {'  agreement of the two Schur forms':34s} rel = {rel:.1e}")

    t = tensor_contraction_check()
    ok &= t["candidate1_residual"] < 1e-9

    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "dimension_audit.json").write_text(
        json.dumps({"dimensional_homogeneity": bool(ok), "groups": g,
                    "tensor_contraction": t}, indent=2))
    print("\nwrote", DATA / "dimension_audit.json")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
