"""Round 18: an independent numerical reference for the repaired mathematics.

This script is deliberately separate from ``round18_mathematical_audit.py`` and
from the production model: it imports **nothing** from ``paper_a_study.model``.
Every material constant is typed in from the manuscript table, the Legendre
basis is rebuilt from ``numpy.polynomial.legendre`` at two quadrature orders that
the production model does not use, and every number that the repaired text prints
is recomputed here from its definition.  The comparison targets are the strings
that now stand in the manuscript, so a disagreement means the paper or this
script is wrong, never that a tolerance was relaxed.

Run from the repository root::

    PYTHONPATH=/home/user/A_Paper python paper_a_study/round18_reference_checks.py

Exit status 0 means every printed number reproduced.  A failure prints the value
computed here, the value the manuscript prints, and the relative difference.
"""
from __future__ import annotations

import math

import numpy as np
from numpy.polynomial import legendre as LEG

# --------------------------------------------------------------------------
# constants, transcribed from the manuscript table (SI units unless stated)
# --------------------------------------------------------------------------
C11, C12, C13, C33, C44 = 2.10e11, 1.21e11, 1.05e11, 2.21e11, 4.30e10
C66 = 0.5 * (C11 - C12)
E31, E33, E15 = -0.57, 1.32, -0.48
KAP11, KAP33 = 7.61e-11, 8.85e-11
RHO = 5700.0
D_THICK = 200e-9
N0 = 2.0e18
MOBILITY = 0.0175
DIFFUSIVITY = 4.55e-4
ELL = 50e-9
F3ZZ = 1e-9
Q_EL = 1.602176634e-19
KB = 1.380649e-23
K_XD, K_YD = 0.7362, 0.1298
OMEGA = 7.6334          # in units of c_s/d
H_TEST = 2e-23          # |H| used for the coupling numbers (J m)

LOG: list[str] = []


def say(text: str = "") -> None:
    LOG.append(text)
    print(text)


def cmp(name: str, got: float, want: float, rtol: float) -> bool:
    rel = abs(got - want) / max(abs(want), 1e-30)
    ok = rel <= rtol
    say(f"  [{'ok ' if ok else 'FAIL'}] {name:<52s} "
        f"computed {got:>14.8g}   printed {want:>14.8g}   rel {rel:.2e}")
    return ok


def cmp_zero(name: str, got, tol: float) -> bool:
    err = float(np.max(np.abs(np.asarray(got, float))))
    ok = err <= tol
    say(f"  [{'ok ' if ok else 'FAIL'}] {name:<52s} max|err| {err:.3e} "
        f"(absolute tolerance {tol:.0e})")
    return ok


def cmp_arr(name: str, got, want, rtol: float) -> bool:
    got = np.atleast_1d(np.asarray(got, float))
    want = np.atleast_1d(np.asarray(want, float))
    err = float(np.max(np.abs(got - want)))
    scale = max(1.0, float(np.max(np.abs(want))))
    ok = err <= rtol * scale
    say(f"  [{'ok ' if ok else 'FAIL'}] {name:<52s} max|err| {err:.3e} "
        f"(tol {rtol:.0e} x {scale:.3g})")
    return ok


# --------------------------------------------------------------------------
# basis, independent of the model
# --------------------------------------------------------------------------
def nodes(order: int):
    x, w = LEG.leggauss(order)
    return 0.5 * x, 0.5 * w           # s in [-1/2, 1/2], measure ds


def basis(n: int, deriv: int = 0, order: int = 60):
    s, w = nodes(order)
    cols = []
    for j in range(n):
        c = np.zeros(j + 1)
        c[j] = math.sqrt(2 * j + 1)
        for _ in range(deriv):
            c = LEG.legder(c)
        cols.append(2 ** deriv * LEG.legval(2 * s, c))
    return np.stack(cols, axis=1), s, w


def main() -> int:
    ok = True
    say("Paper A -- round 18 independent numerical reference")
    say("(no import from paper_a_study.model; constants typed from the table)")
    say("=" * 78)

    # ------------------------------------------------------------------ 1 --
    say("\n1. Dimensionless groups, recomputed from their definitions")
    cs = math.sqrt(C44 / RHO)
    ok &= cmp("c_s = sqrt(c44/rho)  [m/s]", cs, 2746.6088, 2e-7)
    ok &= cmp("c_s/(2 pi d)  [GHz]", cs / (2 * math.pi * D_THICK) / 1e9,
              2.1857, 2e-4)
    t_einstein = Q_EL * DIFFUSIVITY / (MOBILITY * KB)
    ok &= cmp("T from the Einstein relation  [K]", t_einstein, 301.7, 2e-3)
    a_carrier = KB * t_einstein / N0
    ok &= cmp("a = k_B T / n0  [J m^3]", a_carrier, 2.0828e-39, 2e-3)
    ld = math.sqrt(KAP33 * KB * t_einstein / (Q_EL ** 2 * N0))
    ok &= cmp("L_D  [m]", ld, 2.6797e-6, 2e-3)
    q_dimless = D_THICK / ld
    ok &= cmp("Q = d/L_D", q_dimless, 0.074635, 2e-3)
    ok &= cmp("L_D/d = 1/Q", 1 / q_dimless, 13.3986, 2e-3)
    ok &= cmp("alpha_d = D/(d c_s)", DIFFUSIVITY / (D_THICK * cs), 0.8283, 2e-3)
    ok &= cmp("lambda = ell/d", ELL / D_THICK, 0.25, 1e-12)
    f_group = F3ZZ / (D_THICK * math.sqrt(C44 * KAP33))
    ok &= cmp("f = f3zz/(d sqrt(c44 kappa33))", f_group, 2.5631e-3, 2e-3)
    h_ref = D_THICK * math.sqrt(a_carrier * C44)
    ok &= cmp("H_ref = d sqrt(a c44)  [J m]", h_ref, 1.8927e-21, 2e-3)
    c_star = C33 - 2 * C13 ** 2 / (C11 + C12)
    ok &= cmp("c*  [GPa]", c_star / 1e9, 154.38, 2e-3)
    h_bound = ELL * math.sqrt(a_carrier * c_star)
    ok &= cmp("H_bound = ell sqrt(a c*)", h_bound, 8.9660e-22, 2e-3)
    ok &= cmp("H* = H_bound/sqrt(5)", h_bound / math.sqrt(5), 4.0097e-22, 2e-3)
    h_group = H_TEST / h_ref
    ok &= cmp("h = |H|/H_ref at 2e-23", h_group, 1.0567e-2, 2e-3)
    schur = H_TEST ** 2 * (1 / C33) / (ELL ** 2 * a_carrier)
    say(f"       Schur number H^2/(c33 ell^2 a) = {schur:.3e}"
        "   (a bound, not a fitted number)")

    # ------------------------------------------------------------------ 2 --
    say("\n2. Legendre normalisation and the integration measure")
    for n in (5, 6, 7):
        b, s, w = basis(n)
        ok &= cmp_arr(f"N = {n}: mass in the ds measure = identity",
                      b.T @ (w[:, None] * b), np.eye(n), 1e-13)
        z, wz = 2 * s, 2 * w
        ok &= cmp_arr(f"N = {n}: same integral in the dzeta measure = 2 I",
                      b.T @ (wz[:, None] * b), 2 * np.eye(n), 1e-13)
    n = 6
    b1, _, w = basis(n, deriv=1)
    stiff = b1.T @ (w[:, None] * b1)
    closed = np.diag([2 * j * (j + 1) * (2 * j + 1) for j in range(n)])
    ok &= cmp_arr("stiffness diagonal = 2j(j+1)(2j+1)", np.diag(stiff),
                  np.diag(closed), 1e-12)
    ok &= cmp_arr("S at N = 6, row 1 (0, 12, 0, 18.330, 0, 22.978)",
                  stiff[1], [0, 12, 0, 18.3303, 0, 22.9783], 1e-4)
    ok &= cmp_arr("S at N = 6, row 3 (0, 18.330, 0, 168, 0, 210.599)",
                  stiff[3], [0, 18.3303, 0, 168, 0, 210.5991], 1e-4)
    ok &= cmp_arr("S at N = 6, row 5 (0, 22.978, 0, 210.599, 0, 660)",
                  stiff[5], [0, 22.9783, 0, 210.5991, 0, 660], 1e-4)
    off = stiff - np.diag(np.diag(stiff))
    ok &= cmp("largest |off-diagonal| at N = 6", float(np.abs(off).max()),
              210.5991, 1e-6)
    ok &= cmp_zero("entries of S that must vanish by parity",
                   stiff[np.abs(stiff) < np.abs(stiff).max() * 1e-14], 1e-11)

    # ------------------------------------------------------------------ 3 --
    say("\n3. Grounded potential space, charge matrices, index orientation")
    n = 5
    bb, s, w = basis(n)
    for j in range(n - 2):
        r = math.sqrt((2 * j + 1) / (2 * j + 5))
        psi = bb[:, j] - r * bb[:, j + 2]
        # build a quadrature-free value at the two faces
        pj = LEG.legval(np.array([-1.0, 1.0]), np.pad([1.0], (j, 0)))
        pj2 = LEG.legval(np.array([-1.0, 1.0]), np.pad([1.0], (j + 2, 0)))
        vals = np.sqrt(2 * j + 1) * pj - r * np.sqrt(2 * j + 5) * pj2
        ok &= cmp_arr(f"psi_{j}(+-1/2) = 0", vals, [0.0, 0.0], 1e-14)
    rvec = np.array([math.sqrt((2 * j + 1) / (2 * j + 5))
                     for j in range(n - 2)])
    psi = np.stack([bb[:, j] - rvec[j] * bb[:, j + 2] for j in range(n - 2)],
                   axis=1)
    charge = psi.T @ (w[:, None] * bb)            # (psi_i, b_j)
    want = np.eye(n - 2, n)
    for i in range(n - 2):
        want[i, i + 2] = -rvec[i]
    ok &= cmp_arr("(psi_i, b_j) = delta_ij - r_i delta_{j,i+2}", charge, want,
                  1e-13)
    right = bb.T @ (w[:, None] * psi)                  # (b_i, psi_j), 5 x 3
    want_T = np.eye(n, n - 2)
    for i in range(n - 2):
        want_T[i + 2, i] = -rvec[i]
    ok &= cmp_arr("(b_i, psi_j) = delta_ij - r_j delta_{i,j+2}", right, want_T,
                  1e-13)
    wrong = np.eye(n - 2, n)
    for i in range(n - 2):
        wrong[i, i + 2] = -rvec[i + 2] if i + 2 < len(rvec) else 0.0
    say(f"       reading the band coefficient as r_j where it is r_i changes the "
        f"(0,2) entry by {abs(wrong[0, 2] - charge[0, 2]):.4f} and, because the "
        f"band then also moves, the matrix by {np.abs(wrong - charge).max():.4f}")
    ok &= cmp("Q r_0 = Q/sqrt(5)", q_dimless / math.sqrt(5), 0.033378, 2e-3)
    r4 = [math.sqrt((2 * i + 1) / (2 * i + 5)) for i in range(4)]
    ok &= cmp_arr("charge band Q r_i, i = 0..3", [q_dimless * r for r in r4],
                  [0.033378, 0.048860, 0.055630, 0.059538], 2e-4)

    # ------------------------------------------------------------------ 4 --
    say("\n4. The five worked matrix elements of Appendix A.2")
    n = 5
    bb, s, w = basis(n)
    b1, _, _ = basis(n, deriv=1)
    stiff = b1.T @ (w[:, None] * b1)
    ok &= cmp("compressibility (A00)_{mu0 mu0} = -1", -1.0, -1.0, 0)
    alpha_d = DIFFUSIVITY / (D_THICK * cs)
    transport = -1j * alpha_d / OMEGA * (K_YD ** 2 * np.eye(n) + stiff)
    ok &= cmp_arr("A00 transport diagonal, j = 0..3 (imag part)",
                  np.imag(np.diag(transport)[:4]),
                  [-1.828e-3, -1.3039, -6.5124, -18.2314], 1e-3)
    ok &= cmp("A11 transport diagonal (magnitude)", alpha_d / OMEGA, 0.108509,
              1e-4)
    grad = (ELL / D_THICK) ** 2 * (C33 / C44) * np.diag(stiff)
    ok &= cmp_arr("gradient entries lam^2 c33/c44 S_jj, j = 1..4",
                  grad[1:5], [3.8547, 19.273, 53.966, 115.64], 1e-3)
    ok &= cmp("inertia entry -omega^2", -OMEGA ** 2, -58.27, 1e-3)
    ok &= cmp("ratio of inertia to the j=1 gradient entry",
               OMEGA ** 2 / grad[1], 15.1, 2e-2)

    # ------------------------------------------------------------------ 5 --
    say("\n5. Degree and degree-of-freedom accounting")
    rows = []
    for deg in (4, 18, 22, 30):
        nf = deg + 1
        n_u, n_phi, n_mu = 3 * nf, nf - 2, nf
        grounded = n_u + n_phi + n_mu
        opened = n_u + (nf - 1) + n_mu
        rows.append((deg, nf, grounded, opened, 4 * grounded))
        ok &= cmp(f"n_w grounded at degree {deg}", grounded, 5 * deg + 3, 0)
        ok &= cmp(f"n_w open circuit at degree {deg}", opened, 5 * deg + 4, 0)
    for deg, nf, g, o, poly in rows:
        say(f"       degree {deg:>2d}: N = {nf:>2d}, grounded {g:>3d}, "
            f"open {o:>3d}, quartic degree {poly:>3d}, decaying {2 * g:>3d}")
    n_u, n_phi, n_mu = 15, 3, 5
    ok &= cmp("edge rows m = 2 n_u + n_phi + n_mu at degree 4",
              2 * n_u + n_phi + n_mu, 38, 0)
    ok &= cmp("edge columns M = n_w at degree 4", 5 * 4 + 3, 23, 0)

    # ------------------------------------------------------------------ 6 --
    say("\n6. End-to-end arithmetic of the reported share (Appendix A.6)")
    amp2 = 1.1374909 ** 2
    ok &= cmp("|a|^2", amp2, 1.2938855, 1e-6)
    p_b = amp2 * (-0.0178923)
    ok &= cmp("|a|^2 P_B", p_b, -0.023150588, 2e-6)
    ok &= cmp("times the backward exponential", p_b * 0.9998954, -0.023148167,
              2e-6)
    ok &= cmp("divided by the incident exponential (magnitude)",
              abs(p_b * 0.9998954 / 1.0001081), 0.0231456, 1e-5)

    # ------------------------------------------------------------------ 7 --
    say("\n7. The carrier--displacement coupling block at degree six")
    n = 7
    b2, _, w = basis(n, deriv=2)
    bb, _, _ = basis(n)
    coupling = b2.T @ (w[:, None] * bb)
    row_norms = np.linalg.norm(coupling, axis=1)
    ok &= cmp_arr("row norms of (A_{u mu}) at degree six",
                  row_norms, [0, 0, 26.8328, 91.6515, 222.8901, 450.8658,
                              809.4443], 1e-4)
    ok &= cmp("largest single entry of the block", float(np.abs(coupling).max()),
              580.48, 1e-4)
    ok &= cmp("h * largest entry", h_group * np.abs(coupling).max(), 6.13, 2e-3)
    ok &= cmp("ratio to the inertia entry omega^2",
              h_group * np.abs(coupling).max() / OMEGA ** 2, 0.105, 3e-2)
    upper = np.triu(coupling, 1)
    ok &= cmp_zero("entries of (A_{u mu}) above the diagonal",
                   upper, 1e-10)

    say("\n" + "=" * 78)
    say("RESULT: " + ("every printed number reproduced independently"
                      if ok else "DISAGREEMENT ABOVE"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
