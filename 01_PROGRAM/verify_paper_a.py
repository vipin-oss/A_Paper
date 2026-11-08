#!/usr/bin/env python3
"""One-command independent verification of the headline numbers of Paper A.

    cd 01_PROGRAM && python verify_paper_a.py

The script uses NO stored result.  Part 1 recomputes the dimensionless groups,
the positivity bound and the electromagnetic ratios from the material inputs
with plain arithmetic (it does not import the solver).  Part 2 solves the
guided-mode and free-edge problems from scratch with ``paper_a_study/model.py``
and compares each result with the value printed in the manuscript.  Every
comparison prints EXPECTED, COMPUTED and the tolerance; the exit code is 0 only
if all of them pass.

Typical run time: a few minutes on one CPU core.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
STUDY = HERE / "paper_a_study"
sys.path.insert(0, str(STUDY))

ROWS: list[tuple[str, float, float, float, bool]] = []


def check(name: str, expected: float, computed: float, rel: float = 0.0,
          abs_: float = 0.0) -> None:
    tol = max(rel * abs(expected), abs_)
    ok = abs(computed - expected) <= tol
    ROWS.append((name, expected, computed, tol, ok))
    print(f"{'PASS' if ok else 'FAIL'}  {name:58s} expected {expected:<14.8g} "
          f"computed {computed:<14.8g} tol {tol:.2g}")


# ---------------------------------------------------------------- part 1
def part1() -> None:
    print("\n=== Part 1: plain-arithmetic checks (no solver) ===")
    kB, q, eps0, c_light = 1.380649e-23, 1.602176634e-19, 8.8541878128e-12, 2.99792458e8
    c11, c12, c13, c33, c44 = 210e9, 121e9, 105e9, 221e9, 43e9
    rho, kap33 = 5700.0, 8.85e-11
    d, ell, n0, mu, D = 200e-9, 50e-9, 2e18, 0.0175, 4.55e-4
    T = q * D / (mu * kB)                      # Einstein relation
    a = kB * T / n0
    cs = math.sqrt(c44 / rho)
    LD = math.sqrt(kap33 * kB * T / (q * q * n0))
    Q = d / LD
    alpha_d = D / (d * cs)
    Href = d * math.sqrt(a * c44)
    cstar = c33 - 2 * c13 ** 2 / (c11 + c12)
    Hbound = ell * math.sqrt(a * cstar)
    Hstar = Hbound / math.sqrt(5)
    check("T from Einstein relation (K)", 301.7, T, abs_=0.05)
    check("c_s (m/s)", 2746.6, cs, rel=1e-4)
    check("Debye length L_D (um)", 2.6797, LD * 1e6, rel=2e-4)
    check("Q = d/L_D", 0.074635, Q, rel=2e-4)
    check("alpha_d = D/(d c_s)", 0.8283, alpha_d, rel=2e-4)
    check("reduced modulus c* (GPa)", 154.4, cstar / 1e9, rel=1e-3)
    check("H_ref = d sqrt(a c44) (J m)", 1.8927e-21, Href, rel=2e-4)
    check("H_bound (J m)", 8.97e-22, Hbound, rel=2e-3)
    check("H* = H_bound/sqrt5 (J m)", 4.01e-22, Hstar, rel=2e-3)
    check("tabulated extreme 0.05 H* (J m)", 2.0e-23, 0.05 * Hstar, rel=3e-3)
    check("s = Schur ratio at extreme", 5.0e-4, (0.05 * Hstar / Hbound) ** 2,
          rel=0.02)
    check("h = 0.05 H*/H_ref", 1.06e-2, 0.05 * Hstar / Href, rel=0.01)
    fscale = cs / (2 * math.pi * d)
    check("frequency unit c_s/(2 pi d) (GHz)", 2.1857, fscale / 1e9, rel=1e-4)
    check("operating frequency 7.6334*unit (GHz)", 16.684, 7.6334 * fscale / 1e9,
          rel=1e-4)
    omega = 2 * math.pi * 16.684e9
    kEM = omega * math.sqrt(kap33 / eps0) / c_light
    check("k_EM d  (retardation)", 2.2e-4, kEM * d, rel=0.03)
    sigma_e = q * mu * n0
    check("omega * tau_d (carrier relaxation)", 1.65e3, omega * kap33 / sigma_e,
          rel=0.01)
    check("lambda^2 c33/c44", 0.32122, (ell / d) ** 2 * c33 / c44, rel=1e-4)


# ---------------------------------------------------------------- part 2
def part2() -> None:
    print("\n=== Part 2: solver from scratch ===")
    from build_figure_data import (KB0, KY0, K0, OMEGA0, operating_mode, plate,
                                   track)

    def edge(p, mode, K):
        res, _ = p.edge(KY0, mode["omega"].real, K, KB0)
        return res

    p0 = plate(0.0)                                   # H = 0, degree 22
    ref = operating_mode(p0)
    check("operating omega (units c_s/d)", 7.6334, ref["omega"].real, rel=2e-5)
    check("operating frequency (GHz)", 16.684, ref["omega"].real * p0.fscale / 1e9,
          rel=2e-5)
    r = edge(p0, ref, K0)
    RB = float(r["backward_reflection_self_power"])
    check("R_B at operating point (H=0)", 0.0192916, RB, rel=2e-4)
    check("backward energy angle (deg)", -27.8997, float(r["reflected_angle_deg"]),
          abs_=2e-3)
    check("scaled edge residual below 1e-12", 0.0, float(r["edge_scaled_residual"]),
          abs_=1e-12)
    check("power balance below 1e-10", 0.0, float(r["power_balance_relative"]),
          abs_=1e-10)
    inc = float(r["incident_power_left"])
    tot = float(r["total_outgoing_self_power"] / inc)
    check("total outgoing propagating power (op. point)", 0.99980, tot, abs_=2e-5)

    # certified fold
    Kf = 0.52719
    mode_f = track(p0, [Kf], ref)[0]
    rf = edge(p0, mode_f, Kf)
    RBf = float(rf["backward_reflection_self_power"])
    check("R_B at certified fold k_x d=0.52719", 0.9428718, RBf, rel=3e-6)
    check("fold frequency (GHz)", 16.6547, mode_f["omega"].real * p0.fscale / 1e9,
          rel=1e-5)
    incf = float(rf["incident_power_left"])
    def raw_incident_power(p, omega, K):
        waves, _, _ = p.waves(KY0, omega)
        tol = lambda w: 2e-8 * max(1, abs(w["K"]))
        inc_w = [w for w in waves
                 if not (w["K"].imag < -tol(w) or
                         (abs(w["K"].imag) <= tol(w) and w["power"] < 0))]
        return float(min(inc_w, key=lambda w: abs(w["K"] - K))["power"])
    ratio = (raw_incident_power(p0, ref["omega"].real, K0) /
             raw_incident_power(p0, mode_f["omega"].real, Kf))
    check("incident modal power ratio operating/fold (raw)", 131.0, ratio, rel=0.01)
    check("total outgoing power at fold", 1.00050,
          float(rf["total_outgoing_self_power"] / incf), abs_=2e-5)
    check("k_Bx/k_ix at fold", 0.9960,
          float(np.real(rf["backward_K"]) / np.real(rf["incident_K"])), abs_=2e-4)

    # k_x d = 0.55 sample
    m55 = track(p0, [0.55], ref)[0]
    r55 = edge(p0, m55, 0.55)
    check("R_B at k_x d=0.55 (H=0)", 0.551910,
          float(r55["backward_reflection_self_power"]), rel=3e-5)

    # coupling effect, branch-consistent (frequency follows the branch)
    pH = plate(0.05)
    refH = operating_mode(pH)
    for K, label, expected in ((K0, "operating point", -1.21),
                               (0.55, "k_x d=0.55", -10.17),
                               (Kf, "fold", -36.1)):
        mH = refH if K == K0 else track(pH, [K], refH)[0]
        rH = edge(pH, mH, K)
        base = {K0: RB, 0.55: float(r55["backward_reflection_self_power"]),
                Kf: RBf}[K]
        change = 100 * (float(rH["backward_reflection_self_power"]) / base - 1)
        check(f"coupling effect at {label} (%)", expected, change, abs_=0.06)


    # ---- appendix worked example and controls (all recomputed)
    check("|a_B| at n=22 (appendix worked example)", 1.1184598,
          float(abs(r["backward_amplitude"])), rel=2e-6)
    check("|a_B|^2 |P_x| = R_B * P_inc(-L)  (edge power)", 0.0192957,
          RB * inc / math.exp(2 * float(np.imag(r["backward_K"])) * 10.0), rel=2e-6)
    check("P_inc(-L) = exp(2 Im k_ix L)", 1.0001081, inc, abs_=2e-7)
    check("Im k_Bx (per d)", -5.2306e-6, float(np.imag(r["backward_K"])), abs_=2e-9)
    p_nof = plate(0.0, flexo=0.0)
    ref_nof = operating_mode(p_nof)
    r_nof = edge(p_nof, ref_nof, K0)
    check("R_B, f=0, H=0 (tab:controls)", 0.019294,
          float(r_nof["backward_reflection_self_power"]), rel=3e-4)
    p_nofH = plate(0.05, flexo=0.0)
    r_nofH = edge(p_nofH, operating_mode(p_nofH), K0)
    check("R_B, f=0, H=+0.05 H* (tab:controls)", 0.019060,
          float(r_nofH["backward_reflection_self_power"]), rel=3e-4)
    # classical limit: follow the branch from lambda = 0.25 to 0 (degree 18)
    import lambda_continuation as LC
    rows = {round(x["lam"], 2): x for x in LC.run(lams=(0.25, 0.0), deg=18)}
    cs = p0.cs
    to_ghz = lambda Om: Om * cs / (2 * math.pi * 200e-9) / 1e9
    check("fold k_x d at lambda=0.25", 0.527, float(rows[0.25]["K_zgv"]), abs_=1.5e-3)
    check("fold k_x d at lambda=0 (classical)", 0.824, float(rows[0.0]["K_zgv"]),
          abs_=1.5e-3)
    check("classical fold frequency (GHz)", 13.686, to_ghz(rows[0.0]["Omega_zgv"]),
          abs_=2e-3)
    # element matrix of the Legendre basis, N = 6 (appendix eq. app_S_matrix)
    from numpy.polynomial.legendre import Legendre, leggauss
    xs, ws = leggauss(80)
    s_pts, ws = xs / 2, ws / 2
    db = [np.sqrt(2 * j + 1) * 2 * Legendre.basis(j).deriv(1)(2 * s_pts)
          for j in range(6)]
    S = np.array([[np.sum(ws * db[i] * db[j]) for j in range(6)] for i in range(6)])
    check("S_15 entry (N=6)", 22.978, float(S[1, 5]), abs_=5e-4)
    check("S_24 entry (N=6)", 80.498, float(S[2, 4]), abs_=5e-4)
    check("S_35 entry (N=6)", 210.60, float(S[3, 5]), abs_=5e-3)
    check("S_jj = 2 j (j+1)(2j+1), j=5", 660.0, float(S[5, 5]), abs_=1e-6)


def main() -> int:
    part1()
    part2()
    bad = [r for r in ROWS if not r[4]]
    print(f"\n{len(ROWS) - len(bad)} / {len(ROWS)} checks passed")
    for name, e, c, t, _ in bad:
        print(f"  FAILED: {name}: expected {e}, computed {c}, tol {t}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
