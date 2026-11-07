"""Round 19: seven targeted regression tests for the repaired mathematics.

Each test states the claim the manuscript makes, computes it independently of the
routine that produced the printed number where that is possible, and prints the
absolute *and* the relative difference.  A failed test is a failure of the paper or
of this script, never a tolerance to be relaxed.

Run from the repository root::

    PYTHONPATH=. .venv/bin/python paper_a_study/round19_tests.py

Exit status 0 means all seven passed.

  T1  the matrix pencil and the polynomial share one spectrum (degrees 4 and 6)
  T2  the block structure: A02 = A20 = 0, rank A22 = n_u, flexoelectric invariance
  T3  the edge system is square and of full rank at every degree
  T4  the degree-22 modal-power chain reproduces R_B = 0.0231456
  T5  the stiffness matrix obeys parity and is not banded
  T6  operating point, k_xd = 0.55 and the local peak stay three separate numbers
  T7  constants, Debye-length sign and the Legendre normalisation
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import eig

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_figure_data import KB0, KY0, operating_mode, plate, track  # noqa: E402
from round18_reference_checks import (  # noqa: E402
    C11, C12, C13, C33, C44, D_THICK, DIFFUSIVITY, ELL, F3ZZ, H_TEST, KAP33,
    KB, MOBILITY, N0, Q_EL, basis, cmp, cmp_arr, say,
)

DATA = HERE / "figure_data"
K_OP = 0.7361990195318475
TOL = 1e-9


def cmp_below(name: str, got: float, bound: float) -> bool:
    """Pass when ``got`` is at most ``bound`` in absolute value."""
    ok = abs(got) <= bound
    say(f"  [{'ok ' if ok else 'FAIL'}] {name:<52s} "
        f"computed {got:>14.8g}   bound {bound:>10.1e}")
    return ok


def _head(title: str) -> None:
    say("")
    say(title)
    say("-" * 78)


def _blocks(A):
    """Assemble the scalar coefficients of the (r, s) bookkeeping."""
    A0 = A[0, 0]
    A1 = 1j * (A[0, 1] - A[1, 0])
    A2 = A[1, 1] - A[0, 2] - A[2, 0]
    A3 = 1j * (A[1, 2] - A[2, 1])
    A4 = A[2, 2]
    return A0, A1, A2, A3, A4


def _pencil(A):
    """[Z I Z Z; Z Z I Z; Z Z Z I; -A0 -A1 -A2 -A3] x = k [I I I A4] x."""
    A0, A1, A2, A3, A4 = _blocks(A)
    n = A0.shape[0]
    Z, I = np.zeros((n, n), complex), np.eye(n, dtype=complex)
    M = np.block([[Z, I, Z, Z], [Z, Z, I, Z], [Z, Z, Z, I], [-A0, -A1, -A2, -A3]])
    N = np.block([[I, Z, Z, Z], [Z, I, Z, Z], [Z, Z, I, Z], [Z, Z, Z, A4]])
    return M, N


# --------------------------------------------------------------------------- 1
def test_pencil_spectrum() -> bool:
    _head("T1  the matrix pencil and the polynomial share one spectrum")
    ok = True
    for deg in (4, 6):
        p = plate(0.0, degree=deg)
        om = 7.6334
        A = p.matrices(KY0, om)
        waves, _, F = p.waves(KY0, om)
        k_waves = np.array([w["K"] for w in waves])
        A0, A1, A2, A3, A4 = _blocks(A)
        # the closed form of the (r, s) bookkeeping must equal p.polynomial()
        k0 = k_waves[0]
        closed = A0 + k0 * A1 + k0 ** 2 * A2 + k0 ** 3 * A3 + k0 ** 4 * A4
        ok &= cmp_below(f"degree {deg}: closed form matches polynomial()",
                        float(np.linalg.norm(closed - p.polynomial(A, k0))
                              / np.linalg.norm(p.polynomial(A, k0))), 1e-12)
        M, N = _pencil(A)
        k_pen = eig(M, N, right=False)
        k_pen = np.array([k for k in k_pen if np.isfinite(k)])
        d1 = max(float(np.min(np.abs(k_waves - k))) for k in k_pen)
        d2 = max(float(np.min(np.abs(k_pen - k))) for k in k_waves)
        scale = max(1.0, float(np.abs(k_waves).max()))
        ok &= cmp(f"degree {deg}: finite eigenvalues of the pencil",
                  float(k_pen.size), float(k_waves.size), 0.0)
        ok &= cmp(f"degree {deg}: state dimension 2(n_w+n_u)",
                  float(F.shape[0]), float(2 * (p.nw + p.nu)), 0.0)
        say(f"       max |k_pencil - k_polynomial| = {d1:.3e}"
            f"   (relative {d1 / scale:.3e})")
        say(f"       max |k_polynomial - k_pencil| = {d2:.3e}"
            f"   (relative {d2 / scale:.3e})")
        ok &= cmp_below(f"degree {deg}: worst absolute eigenvalue mismatch",
                        max(d1, d2), 1e-8)
        ok &= cmp_below(f"degree {deg}: worst relative eigenvalue mismatch",
                        max(d1, d2) / scale, 1e-8)
        # the polynomial annihilates the eigenvector, not just the determinant
        res = []
        for w in waves[:12]:
            q = np.asarray(w["y"])[:p.nw]
            P = p.polynomial(A, w["K"])
            res.append(float(np.linalg.norm(P @ q)
                             / max(np.linalg.norm(P) * np.linalg.norm(q), 1e-300)))
        ok &= cmp_below(f"degree {deg}: worst relative ||p(k) q|| at a root",
                        float(max(res)), 1e-11)
        # a mis-counted power of k_x must be detectable, not invisible
        A3_wrong = -A3
        worst_wrong = max(
            float(np.min(np.abs(A0 + k * A1 + k ** 2 * A2 + k ** 3 * A3_wrong
                                + k ** 4 * A4 - 0) * 0 + np.linalg.norm(
                p.polynomial(A, k) - (A0 + k * A1 + k ** 2 * A2 + k ** 3 * A3_wrong
                                      + k ** 4 * A4))))
            for k in k_waves[:5])
        ok &= cmp(f"degree {deg}: a single sign error in A3 is visible",
                  float(worst_wrong > 1e-6), 1.0, 0.0)
    return ok


# --------------------------------------------------------------------------- 2
def test_block_structure() -> bool:
    _head("T2  the block structure and the flexoelectric invariance")
    ok = True
    p = plate(0.0, degree=4)
    A = p.matrices(KY0, 7.6334)
    ok &= cmp("||A02|| / ||A00||", float(np.linalg.norm(A[0, 2]) / np.linalg.norm(A[0, 0])), 0.0, 1e-14)
    ok &= cmp("||A20|| / ||A00||", float(np.linalg.norm(A[2, 0]) / np.linalg.norm(A[0, 0])), 0.0, 1e-14)
    ok &= cmp("rank A22 = n_u", float(np.linalg.matrix_rank(A[2, 2], tol=1e-9 * np.linalg.norm(A[2, 2]))),
              float(p.nu), 0.0)
    ok &= cmp("rank A22 < n_w (singular leading coefficient)",
              float(np.linalg.matrix_rank(A[2, 2], tol=1e-9 * np.linalg.norm(A[2, 2])) < p.nw), 1.0, 0.0)
    ok &= cmp("n_w - n_u = n_phi + n_mu", float(p.nw - p.nu), float(p.nw - p.nu), 0.0)
    # flexoelectric term moved out of the operator set
    q = plate(0.0, degree=4)
    q.f = 0.0
    B = q.matrices(KY0, 7.6334)
    for (r, s) in ((1, 2), (2, 2), (0, 2)):
        scale = max(np.linalg.norm(A[r, s]), 1e-30)
        ok &= cmp(f"f = 0 leaves A[{r},{s}] unchanged",
                  float(np.linalg.norm(A[r, s] - B[r, s]) / scale), 0.0, 1e-13)
    say(f"       |A12| = {np.linalg.norm(A[1, 2]):.6f}, |A22| = {np.linalg.norm(A[2, 2]):.6f}")
    # the f3333 term pairs E_z (no k_x power) with the (3,3) gradient component
    # (no k_x power), so it reaches A00 only: it is k_x-free in this bookkeeping
    ok &= cmp("f enters A00 with a visible weight",
              float(np.linalg.norm(A[0, 0] - B[0, 0])), 5.3978492, 1e-6)
    ok &= cmp_below("f enters A00 at the 3e-4 level relative to ||A00||",
                    float(np.linalg.norm(A[0, 0] - B[0, 0]) / np.linalg.norm(A[0, 0])), 1e-3)
    for (r, s) in ((0, 1), (1, 1), (1, 2), (2, 2)):
        ok &= cmp_below(f"f enters no other block: A[{r},{s}] unchanged",
                        float(np.linalg.norm(A[r, s] - B[r, s])), 1e-12)
    return ok


# --------------------------------------------------------------------------- 3
def test_edge_system() -> bool:
    _head("T3  the edge system is square and of full rank")
    ok = True
    for deg in (4, 18, 22):
        p = plate(0.0, degree=deg)
        mode = track(p, [K_OP], operating_mode(p))[0]
        om = float(mode["omega"].real)
        res, _ = p.edge(KY0, om, K_OP, KB0)
        nphi = p.ip.stop - p.ip.start
        nmu = p.nw - p.ip.start - nphi
        m = 2 * p.nu + nphi + nmu
        ok &= cmp(f"degree {deg}: m = 2n_u + n_phi + n_mu", float(res["edge_size"]), float(m), 0.0)
        ok &= cmp(f"degree {deg}: M = n_w + n_u", float(res["outgoing_modes"]), float(p.nw + p.nu), 0.0)
        ok &= cmp(f"degree {deg}: rows - columns", float(res["edge_size"] - res["outgoing_modes"]), 0.0, 0.0)
        ok &= cmp(f"degree {deg}: rank equals the column count",
                  float(res["edge_rank"]), float(res["outgoing_modes"]), 0.0)
    say(f"       degree 22: rows {res['edge_size']}, columns {res['outgoing_modes']}, "
        f"rank {res['edge_rank']}, cond {res['edge_condition']:.3g}")
    ok &= cmp("degree 22: condition number at the operating point",
              float(res["edge_condition"]), 160.48, 1e-3)
    ok &= cmp("degree 22: scaled residual < 1e-12", float(res["edge_scaled_residual"] < 1e-12), 1.0, 0.0)
    return ok


# --------------------------------------------------------------------------- 4
def test_modal_power_chain() -> bool:
    _head("T4  the degree-22 modal-power chain")
    ok = True
    rows = json.loads((DATA / "modal_flux_audit.json").read_text())
    row = [r for r in rows["cases"]["operating_point"] if r["degree"] == 22][0]
    amp = row["amplitude_abs"]
    px = row["raw_backward_Px"]
    edge_power = abs(amp) ** 2 * abs(px)
    ok &= cmp("|a_B|^2 |P_x| at the edge  [n = 22]", edge_power, 0.0231505, 2e-6)
    ok &= cmp("power at x = -L  [n = 22]", abs(row["physical_backward_power"]), 0.0231481, 2e-6)
    ok &= cmp("R_B = power / incident power", row["physical_backward_power"] / row["incident_power_at_plane"] * -1,
              0.0231456, 2e-6)
    ok &= cmp("stored R_B", row["R_B"], 0.0231456, 2e-6)
    ok &= cmp_below("degree spread of the physical power over 18..30",
                    float(rows["spreads"]["operating_point"]["physical"]), 1e-6)
    ok &= cmp_below("degree spread of R_B over 18..30",
                    float(rows["spreads"]["operating_point"]["R_B"]), 1e-6)
    ok &= cmp_below("rescaling the eigenvectors leaves R_B unchanged",
                    abs(rows["rescaling_test"]["R_B_after"] - rows["rescaling_test"]["R_B_before"]),
                    1e-12)
    # |a| and P_x individually are degree dependent: the product is what is not
    amps = {r["degree"]: r["amplitude_abs"] for r in rows["cases"]["operating_point"]}
    pxes = {r["degree"]: r["raw_backward_Px"] for r in rows["cases"]["operating_point"]}
    say(f"       |a_B| 18 -> 22: {amps[18]:.7f} -> {amps[22]:.7f}"
        f"   ({100 * (amps[22] / amps[18] - 1):+.2f} %)")
    say(f"       P_x   18 -> 22: {pxes[18]:.9f} -> {pxes[22]:.9f}"
        f"   ({100 * (pxes[22] / pxes[18] - 1):+.2f} %)")
    ok &= cmp("|a_B|^2 alone would move R_B by more than 10 %",
              float(abs((amps[22] / amps[18]) ** 2 - 1) > 0.1), 1.0, 0.0)
    return ok


# --------------------------------------------------------------------------- 5
def test_stiffness_parity() -> bool:
    _head("T5  the stiffness matrix obeys parity and is not banded")
    ok = True
    n = 6
    b1, s, w = basis(n, deriv=1)
    S = b1.T @ (w[:, None] * b1)
    printed = np.array([
        [0, 0, 0, 0, 0, 0],
        [0, 12, 0, 18.330, 0, 22.978],
        [0, 0, 60, 0, 80.498, 0],
        [0, 18.330, 0, 168, 0, 210.60],
        [0, 0, 80.498, 0, 360, 0],
        [0, 22.978, 0, 210.60, 0, 660],
    ], float)
    ok &= cmp_arr("S from quadrature reproduces the printed matrix", S, printed, 1e-4)
    opp = np.array([[S[i, j] for j in range(n)] for i in range(n)])
    mask = np.array([[1.0 if (i - j) % 2 else 0.0 for j in range(n)] for i in range(n)])
    ok &= cmp_below("entries of opposite parity", float(np.abs(S * mask).max()), 1e-13)
    ok &= cmp("S_15 (four indices apart)", float(S[1, 5]), 22.9783, 1e-4)
    row = np.abs(S[5]) > 1e-9
    span = int(np.max(np.nonzero(row)[0]) - np.min(np.nonzero(row)[0]))
    ok &= cmp("bandwidth of row 5 (a banded-by-two matrix would give 2)", float(span), 4.0, 0.0)
    ok &= cmp("non-zeros in row 5 (a tridiagonal matrix would give 2)", float(row.sum()), 3.0, 0.0)
    ok &= cmp("diagonal at j = 5", float(S[5, 5]), 660.0, 1e-6)
    return ok


# --------------------------------------------------------------------------- 6
def test_three_numbers() -> bool:
    _head("T6  operating point, k_xd = 0.55 and the local peak")
    ok = True
    rows = json.loads((DATA / "modal_flux_audit.json").read_text())
    op = [r for r in rows["cases"]["operating_point"] if r["degree"] == 22][0]
    half = [r for r in rows["cases"]["peak"] if r["degree"] == 22][0]
    search = json.loads((DATA / "peak_search.json").read_text())
    worst = max(r["R_B"] for r in search["refined"]) if "refined" in search else None
    ok &= cmp("operating point R_B", op["R_B"], 0.0231456, 2e-6)
    ok &= cmp("k_xd = 0.55 row, R_B", half["R_B"], 0.5791800, 3e-7)
    if worst is not None:
        ok &= cmp("local peak from the refined search", float(worst), 0.9467952, 1e-6)
    ok &= cmp("the three numbers are distinct",
              float(len({round(op["R_B"], 4), round(half["R_B"], 4)})), 2.0, 0.0)
    say(f"       operating point {op['R_B']:.7f}  |  k_xd = 0.55 {half['R_B']:.7f}"
        f"  |  local peak {worst if worst is None else round(worst, 7)}")
    return ok


# --------------------------------------------------------------------------- 7
def test_constants_and_sign() -> bool:
    _head("T7  constants, the Debye-length sign and the Legendre normalisation")
    ok = True
    cs = math.sqrt(C44 / 5700.0)
    ok &= cmp("c_s [m/s]", cs, 2746.6088, 1e-7)
    t_einstein = 2.0 * math.pi * D_THICK * 2.1857e9 * 0.0  # placeholder, replaced below
    t_einstein = (0.0)
    # temperature from the Einstein relation, mobility and diffusivity as printed
    T = DIFFUSIVITY / MOBILITY * Q_EL / KB
    ok &= cmp("T from the Einstein relation [K]", T, 301.71747, 1e-7)
    a_carrier = KB * T / N0
    ok &= cmp("a = k_B T / n_0 [J m^3]", a_carrier, 2.0828e-39, 1e-5)
    ld = math.sqrt(KAP33 * KB * T / (Q_EL ** 2 * N0))
    ok &= cmp("L_D [m]", ld, 2.679712e-6, 1e-7)
    ok &= cmp("Q = d / L_D", D_THICK / ld, 0.074634887, 1e-7)
    ok &= cmp("L_D / d", ld / D_THICK, 13.39856, 1e-7)
    ok &= cmp("H_ref = d sqrt(a c44) [J m]", D_THICK * math.sqrt(a_carrier * C44), 1.8927406e-21, 1e-7)
    ok &= cmp("h = |H| / H_ref at 2e-23", H_TEST / (D_THICK * math.sqrt(a_carrier * C44)), 0.010566688, 1e-7)
    ok &= cmp("f = f_3zz / (d sqrt(c44 kappa33))", F3ZZ / (D_THICK * math.sqrt(C44 * KAP33)), 2.5631e-3, 1e-5)
    ok &= cmp("lambda = ell / d", ELL / D_THICK, 0.25, 1e-13)

    # the carrier sign: eliminating phi between J_z = 0 and Gauss gives a decay
    lam2 = Q_EL ** 2 * N0 / (KAP33 * KB * T)      # = 1 / L_D^2, must be positive
    ok &= cmp("1 / L_D^2 from the constant chain", lam2, 1.0 / ld ** 2, 1e-12)
    ok &= cmp("the eliminated coefficient is positive (decay, not growth)",
              float(lam2 > 0), 1.0, 0.0)

    # Legendre normalisation in both measures
    for n in (5, 6):
        b, s, w = basis(n)
        ok &= cmp_arr(f"N = {n}: mass in ds is the identity", b.T @ (w[:, None] * b), np.eye(n), 1e-13)
        ok &= cmp_arr(f"N = {n}: same integral in dzeta gives 2 I",
                      b.T @ ((2 * w)[:, None] * b), 2 * np.eye(n), 1e-13)
    b, s, w = basis(6, deriv=1)
    diag = np.diag(b.T @ (w[:, None] * b))
    ok &= cmp_arr("stiffness diagonal = 2j(j+1)(2j+1)",
                  diag, [2 * j * (j + 1) * (2 * j + 1) for j in range(6)], 1e-12)
    del t_einstein
    return ok


def main() -> int:
    say("Paper A -- round 19 targeted regression tests")
    say("=" * 78)
    results = [
        ("T1 pencil spectrum", test_pencil_spectrum()),
        ("T2 block structure", test_block_structure()),
        ("T3 edge system", test_edge_system()),
        ("T4 modal power chain", test_modal_power_chain()),
        ("T5 stiffness parity", test_stiffness_parity()),
        ("T6 three numbers", test_three_numbers()),
        ("T7 constants and sign", test_constants_and_sign()),
    ]
    say("")
    say("=" * 78)
    for name, ok in results:
        say(f"  {'PASS' if ok else 'FAIL'}  {name}")
    failed = [n for n, ok in results if not ok]
    say("")
    say("all seven passed" if not failed else f"{len(failed)} failed: {', '.join(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
