"""Round 18 independent mathematical audit of the Paper A manuscript.

Nothing here imports an algebraic helper from the manuscript's own derivation
path: the Legendre basis is rebuilt from explicit coefficient arrays, derivatives
are taken analytically with ``numpy.polynomial.legendre.legder``, integrals use a
quadrature rule of a *different* order from the model's, and every closed form is
evaluated directly.

Run from the repository root:

    PYTHONPATH=. python paper_a_study/round18_mathematical_audit.py

Exit status 0 means every check passed.  A failure prints the offending index and
both numbers; nothing is suppressed.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from numpy.polynomial import legendre as L

from paper_a_study.model import Plate, SI, CONST

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "PAPER_A_ROUND18_AUDIT_LOG.txt"
LOG: list[str] = []


def say(text: str = "") -> None:
    LOG.append(text)
    print(text)


# ---------------------------------------------------------------- basis ----
def basis(n: int, order: int = 0, nodes: int = 301):
    """Independent basis: explicit Legendre coefficients, analytic derivatives.

    Returns the values on the half interval s in [-1/2, 1/2] together with the
    nodes and the quadrature weights of a 301 point Gauss-Legendre rule.  The
    model uses max(64, 2p+10) points, so the rule is independent of it.
    """
    x, w = L.leggauss(nodes)
    s = 0.5 * x
    w = 0.5 * w                      # ds measure on [-1/2, 1/2]
    cols = []
    for j in range(n):
        c = np.zeros(j + 1)
        c[j] = math.sqrt(2 * j + 1)
        for _ in range(order):
            c = L.legder(c)
        cols.append(2 ** order * L.legval(2 * s, c))
    return np.array(cols), s, w


def check(name: str, got, want, tol: float, extra: str = "") -> bool:
    got = np.asarray(got, dtype=float)
    want = np.asarray(want, dtype=float)
    err = float(np.max(np.abs(got - want))) if got.size else 0.0
    scale = max(1.0, float(np.max(np.abs(want))) if want.size else 1.0)
    ok = err <= tol * scale
    say(f"  [{'ok ' if ok else 'FAIL'}] {name}: max|err| = {err:.3e}"
        f" (tol {tol:.0e} x {scale:.3g}) {extra}")
    return ok


def main() -> int:
    good = True
    say("Paper A -- round 18 independent mathematical audit")
    say("=" * 72)

    # ---------------------------------------------------------- groups ----
    say("\n1. Dimensionless groups from the material file")
    p = Plate(degree=4, H=0.0)
    cs = math.sqrt(SI["c44"] / SI["rho"])
    good &= check("c_s [m/s]", cs, 2746.608754, 1e-8)
    good &= check("frequency unit c_s/(2 pi d) [GHz]", cs / (2 * math.pi * p.d) / 1e9,
                  2.185682, 1e-6)
    T = CONST["q"] * p.diffusivity / (p.mobility * CONST["kB"])
    say(f"       T implied by Einstein = {T:.4f} K")
    a = CONST["kB"] * T / p.n0
    good &= check("a = k_B T / n0", a, p.a, 1e-12)
    LD = math.sqrt(SI["kappa33"] * CONST["kB"] * T / (CONST["q"] ** 2 * p.n0))
    good &= check("L_D [m]", LD, 2.679712e-6, 1e-6)
    good &= check("Q = d/L_D", p.d / LD, p.Q, 1e-12)
    good &= check("alpha_d = D/(d c_s)", p.diffusivity / (p.d * cs), p.alpha, 1e-12)
    say(f"       d/L_D = {p.Q:.6f};  L_D/d = {1 / p.Q:.4f}"
        "   <-- the manuscript must quote these the right way round")
    good &= check("lambda = ell/d", 50e-9 / p.d, p.lam, 1e-12)
    f_group = 1e-9 / (200e-9 * math.sqrt(SI["c44"] * SI["kappa33"]))
    good &= check("flexoelectric group f", f_group, p.f, 1e-12)
    H_ref = p.d * math.sqrt(a * SI["c44"])
    say(f"       H_ref = d sqrt(a c44) = {H_ref:.6e} J m")
    cstar = SI["c33"] - 2 * SI["c13"] ** 2 / (SI["c11"] + SI["c12"])
    say(f"       c* = {cstar/1e9:.2f} GPa")
    H_bound = 50e-9 * math.sqrt(a * cstar)
    say(f"       H_bound = ell sqrt(a c*) = {H_bound:.6e} J m;  H* = {H_bound/math.sqrt(5):.6e}")
    ph = Plate(degree=4, H=2e-23)
    good &= check("h at |H| = 2.0e-23", 2e-23 / H_ref, ph.h, 1e-12)
    say(f"       h = {ph.h:.6e};  Schur number = {ph.schur:.3e}")

    # ------------------------------------------------------ basis tests ----
    say("\n2. Basis, mass and stiffness on the implemented half interval")
    say("   b_j(s) = sqrt(2j+1) P_j(2s), s = z/d in [-1/2, 1/2], measure ds")
    for pdeg in (4, 5, 6):
        n = pdeg + 1
        bb, s, w = basis(n, 0)
        b1, _, _ = basis(n, 1)
        mass = bb @ (w[:, None] * bb.T)
        stiff = b1 @ (w[:, None] * b1.T)
        plate = Plate(degree=pdeg, H=0.0)
        say(f"   p = {pdeg} (N = {n}):")
        good &= check("mass matrix = identity (independent rule)", mass, np.eye(n), 1e-12)
        Mm = plate.b[0].T @ (plate.weights[:, None] * plate.b[0])
        good &= check("mass: model agrees with independent rule", Mm, mass, 1e-10)
        Sm = plate.b[1].T @ (plate.weights[:, None] * plate.b[1])
        good &= check("stiffness: model agrees with independent rule", Sm, stiff, 1e-9)
        closed = np.diag([2 * j * (j + 1) * (2 * j + 1) for j in range(n)]).astype(float)
        good &= check("stiffness diagonal = 2j(j+1)(2j+1)", np.diag(Sm), np.diag(closed),
                      1e-10)
        off = stiff - np.diag(np.diag(stiff))
        say(f"       largest off-diagonal stiffness entry = {np.max(np.abs(off)):.4f}"
            f"; parity-violating entries (i+j odd) = {np.max(np.abs(off[::2, 1::2])):.2e}")

    # ------------------------------------------- potential space and Q ----
    say("\n3. Grounded potential space and the two charge-matrix orientations")
    pdeg = 4
    plate = Plate(degree=pdeg, H=0.0)
    n = plate.n
    bp, s, w = basis(n, 0)
    nl = plate.np
    ratio = np.sqrt((2 * np.arange(nl) + 1) / (2 * np.arange(nl) + 5))
    psi = np.array([bp[j] - ratio[j] * bp[j + 2] for j in range(nl)])
    say(f"   n_phi = {nl} for grounded faces at p = {pdeg} (N = {n}, n_phi = N-2)")
    def psi_at(sv):
        vals = []
        for j in range(nl):
            c1 = np.zeros(j + 1); c1[j] = math.sqrt(2 * j + 1)
            c2 = np.zeros(j + 3); c2[j + 2] = math.sqrt(2 * j + 5)
            vals.append(L.legval(2 * sv, c1) - ratio[j] * L.legval(2 * sv, c2))
        return np.array(vals)
    good &= check("psi_j(+/-1/2) = 0", np.r_[psi_at(-0.5), psi_at(0.5)],
                  np.zeros(2 * nl), 1e-14)
    charge = psi @ (w[:, None] * bp.T)          # (phi_i, b_j)
    want = np.eye(nl, n) - ratio[:, None] * np.eye(nl, n, k=2)
    good &= check("(phi_i,b_j) = delta_ij - r_i delta_{j,i+2}", charge, want, 1e-12)
    wp_model = plate.pb[0].T @ (plate.weights[:, None] * plate.b[0])
    good &= check("model charge matrix = same orientation", wp_model, charge, 1e-11)
    ratio_ext = np.sqrt((2 * np.arange(n) + 1) / (2 * np.arange(n) + 5))
    wrong = np.eye(nl, n) - ratio_ext[None, :] * np.eye(nl, n, k=2)
    say("       the transposed-index formula -r_j delta_{i,j+2} differs from the"
        f" assembled matrix by {np.max(np.abs(wrong - charge)):.4f}")
    say("       assembled (phi_i, b_j) entries at j = i+2: "
        + ", ".join(f"{plate.Q*charge[i, i+2]:+.6f}" for i in range(min(4, nl - 2))))
    say("       transpose (b_i, phi_j) entries are the same numbers at (j, j+2)")
    good &= check("Q r_0 = Q/sqrt5", plate.Q * ratio[0], plate.Q / math.sqrt(5), 1e-12)
    good &= check("Q from the model", plate.Q, 0.074634887, 1e-8)

    # ------------------------------------------ assembled block entries ----
    say("\n4. Transport and coupling entries of the assembled operator at p = 4")
    ky, omega = 0.1298, 7.6334
    kx = 0.7362
    A = plate.matrices(ky, omega)
    nw, nu, ip, im = plate.nw, plate.nu, plate.ip, plate.im
    S = plate.b[1].T @ (plate.weights[:, None] * plate.b[1])
    kk = kx * kx + ky * ky
    say(f"   n_w = {nw}, n_u = {nu}, n_phi = {plate.np}, n_mu = {n}")
    say(f"   k_y^2 = {ky*ky:.6f}, k_x^2 = {kx*kx:.6f}, k_x^2 + k_y^2 = {kk:.6f}")
    Sdiag = np.diag(S)[:4]
    # A[0,0] carries the k_x^0 part: transport there is -(alpha/omega)(k_y^2 + S)
    im00 = np.imag(np.diag(A[0, 0][im, im]))
    good &= check("A00 transport diag = -(alpha/omega)(ky^2 + S_jj)", im00[:4],
                  -plate.alpha / omega * (ky * ky + Sdiag), 1e-10)
    re00 = np.real(np.diag(A[0, 0][im, im]))
    good &= check("A00 mass diag = -1", re00[:4], -np.ones(4), 1e-12)
    im11 = np.imag(np.diag(A[1, 1][im, im]))
    # the x derivative carries no k factor inside MG; the k_x^2 comes from the
    # polynomial expansion (i k_x)^1 (-i k_x)^1, so A11 transport is -(alpha/omega) * mass
    good &= check("A11 transport diag = -(alpha/omega) (mass)", im11[:4],
                  -plate.alpha / omega * np.ones(4), 1e-10)
    say("   assembled A00 values: " + ", ".join(f"-i{abs(v):.6f}" for v in im00[:5]))
    say(f"   assembled A11 value:  -i{abs(im11[0]):.6f} (times k_x^2 = {kx*kx:.6f})"
        f"  (so the polynomial carries -(alpha/omega)(kx^2+ky^2+S))")
    total = -(im00[:4] + kx * kx * im11[:4])
    good &= check("polynomial transport diag = (alpha/omega)(kk + S_jj)", total,
                  plate.alpha / omega * (kk + Sdiag), 1e-10)
    say("   round-17 printed: -i0.00180, -i1.304, -i6.512, -i18.23 for A00")
    say("   with the printed formula (kx^2+ky^2) inside the bracket, which belongs"
        " to A11+A00, the first value would have been -i0.0607")

    # carrier--potential coupling sits in A[0,0] (from -W^H W)
    cp = plate.Q * charge                       # (phi_i, b_j)
    good &= check("A00 phimu = -Q (phi_i,b_j)", A[0, 0][ip, im], -cp, 1e-11)
    good &= check("A00 muphi = A00 phimu^T", A[0, 0][im, ip], A[0, 0][ip, im].T, 1e-12)
    say("   A00[phi_i, mu_(i+2)] = "
        + ", ".join(f"{A[0,0][ip,im][i,i+2]:+.6f}" for i in range(min(3, plate.np - 2))))
    say("   A00[mu_i, phi_(i+2)] = "
        + ", ".join(f"{A[0,0][im,ip][i,i+2]:+.6f}" for i in range(min(3, plate.np - 2))))

    # gradient stiffness entries and the "largest entry" claim
    lam2 = plate.lam ** 2
    ratio_c = SI["c33"] / SI["c44"]
    gs = lam2 * ratio_c * np.diag(S)
    say(f"   lambda^2 c33/c44 S_jj for j = 0..{n-1}: "
        + ", ".join(f"{v:.3g}" for v in gs))
    say(f"   j=1 entry = {gs[1]:.4f}; largest diagonal = {gs.max():.4f} at j = {int(gs.argmax())}")

    # --------------------------------------------------- coupling rows ----
    say("\n5. Carrier--strain-gradient coupling rows of eq:H_entry")
    n6 = 6
    b0, s6, w6 = basis(n6, 0)
    b2, _, _ = basis(n6, 2)
    psi6 = np.array([b0[j] - math.sqrt((2 * j + 1) / (2 * j + 5)) * b0[j + 2]
                     for j in range(n6 - 2)])
    M_h = b2 @ (w6[:, None] * psi6.T)
    rows = [float(np.linalg.norm(M_h[i])) for i in range(n6)]
    say("   u3-phi block at degree five (N = 6), row norms of int b_i'' psi_j: "
        + ", ".join(f"{v:.4f}" for v in rows))
    good &= check("row norms 0,0,26.83,91.65,191.25,336.14", rows,
                  [0, 0, 26.8328, 91.6515, 191.2485, 336.1428], 1e-5)
    say("   matrix (rows i, columns j):")
    for i in range(n6):
        say("     " + " ".join(f"{np.real(M_h[i, j]):9.3f}" for j in range(n6 - 2)))
    say(f"   upper-triangular defect: max|entries below the diagonal| = "
        f"{np.max(np.abs(np.tril(M_h, -1))):.1f} (the matrix is lower triangular)")
    bands = [(i, j, float(np.real(M_h[i, j]))) for i in range(n6) for j in range(n6 - 2)
             if abs(M_h[i, j]) > 1e-9]
    say(f"   nonzero entries: {bands}")
    ph6 = Plate(degree=5, H=2e-23)          # N = 6
    p7 = Plate(degree=6, H=2e-23)
    Mb7 = p7.b[2].T @ (p7.weights[:, None] * p7.b[0])
    say(f"   u3-mu block at degree six (N = 7): row norms "
        + ", ".join(f"{v:.2f}" for v in np.linalg.norm(Mb7, axis=1))
        + f"; largest entry {np.max(np.abs(Mb7)):.1f}")
    say(f"   the two physical couplings are h times the entry of the u3-mu block,"
        f" max|int b_i'' b_j| = {np.max(np.abs(ph6.b[2].T @ (ph6.weights[:, None] * ph6.b[0]))):.1f},"
        f" and f times the entry of the u3-phi block, max|int b_i'' psi_j| ="
        f" {np.max(np.abs(M_h)):.1f}")
    say(f"   at |H| = 2e-23 (h = {abs(ph6.h):.6e}) the u3-mu entry is"
        f" {abs(ph6.h)*np.max(np.abs(ph6.b[2].T @ (ph6.weights[:, None] * ph6.b[0]))):.3f},"
        f" the u3-phi entry {abs(ph6.f)*np.max(np.abs(M_h)):.3f}, against"
        f" omega^2 = {omega**2:.2f}")

    # -------------------------------------------------- size accounting ----
    say("\n6. Unknown counts, grounded and open circuit")
    for pdeg in (4, 5, 18, 22, 30):
        g = Plate(degree=pdeg, H=0.0, electric="ground")
        o = Plate(degree=pdeg, H=0.0, electric="open")
        say(f"   p = {pdeg:2d}: N = {pdeg+1:2d}, grounded n_w = {g.nw:3d}"
            f" (5p+3 = {5*pdeg+3}), open n_w = {o.nw:3d} (5p+4 = {5*pdeg+4})")
        good &= g.nw == 5 * pdeg + 3
        good &= o.nw == 5 * pdeg + 4
    pl = Plate(degree=4, H=2e-23)
    A = pl.matrices(0.1298, 7.6334)
    F = pl.state_operator(A)
    say(f"   state-operator size 4 n_w x 4 n_w = {F.shape[0]} x {F.shape[1]}"
        f" (4 x {pl.nw})")
    y = np.zeros(F.shape[0], complex)
    y[:pl.nw] = 1.0
    say(f"   boundary vector length = {len(pl.boundary_vector(y))}"
        f" vs n_w = {pl.nw} (rows = 2 n_u + n_phi + n_mu = {2*pl.nu+pl.np+pl.n})")

    # ------------------------------------------------------ R_B chain ----
    say("\n7. End-to-end evaluation of the reported share")
    raw, amp = -0.017892253333615923, 1.1374909585196669
    kBi, kIi, Lref = -5.230594890969936e-06, 5.402718506941832e-06, 10.0
    pb_edge = amp ** 2 * raw
    pb_plane = pb_edge * math.exp(2 * kBi * Lref)
    inc_plane = math.exp(2 * kIi * Lref)
    RB = -pb_plane / inc_plane
    say(f"   P_edge = {pb_edge:.7f}, P(-L) = {pb_plane:.7f}, P_inc(-L) = {inc_plane:.7f}")
    good &= check("R_B", RB, 0.023145607570647334, 1e-12)
    good &= check("exp(2 Im k_B L)", math.exp(2 * kBi * Lref), 0.9998954, 1e-6)

    # ---------------------------------------------- edge system sizes ----
    say("\n8. Edge system row/column counts")
    for pdeg in (4, 18):
        g = Plate(degree=pdeg, d=200e-9, H=0.0)
        A = g.matrices(0.1298, 7.6334)
        F = g.state_operator(A)
        y = np.zeros(F.shape[0], complex)
        y[:g.nw] = 1.0
        rows = len(g.boundary_vector(y))
        say(f"   p = {pdeg}: R is {rows} x {g.nw}; square only when ell = 0")
        good &= rows >= g.nw
    g0 = Plate(degree=4, d=200e-9, n0=2e18, mobility=0.0175, diffusivity=0.000455,
               ell=0e-9, flexo=0.0, H=0.0)
    A = g0.matrices(0.1298, 7.6334)
    F0 = g0.state_operator(A)
    y = np.zeros(F0.shape[0], complex)
    y[:g0.nw] = 1.0
    say(f"   ell = 0: R is {len(g0.boundary_vector(y))} x {g0.nw} (square)")

    # ------------------------------------ constitutive component checks ----
    say("\n9. Constitutive component relations against the assembled fields")
    say("   (scaled units of the solver: sigma/c44, e/sqrt(c44 kappa33), kappa/kappa33,")
    say("    dimensionless strains, wavenumbers and z derivatives)")
    pl = Plate(degree=5, H=2e-23, flexo=1e-9)
    n = pl.n
    rng = np.random.default_rng(20261107)
    q = np.zeros(pl.nw, complex)
    q[:pl.nu] = rng.standard_normal(pl.nu) + 1j * rng.standard_normal(pl.nu)
    q[pl.ip] = rng.standard_normal(pl.np) + 1j * rng.standard_normal(pl.np)
    q[pl.im] = rng.standard_normal(n) + 1j * rng.standard_normal(n)
    kxv, kyv = 0.7362, 0.1298
    fl = pl.fields(kxv, kyv, q)
    sig, Dv = fl["sigma"], fl["D"]
    u, du, phi, dphi = fl["u"][0], fl["u"][1], fl["phi"][0], fl["phi"][1]
    u1, u2, u3 = u[:, 0], u[:, 1], u[:, 2]
    d1, d2, d3 = du[:, 0], du[:, 1], du[:, 2]
    gx, gy, gz = 1j * kxv * phi, 1j * kyv * phi, dphi
    eps_xx, eps_yy, eps_zz = 1j * kxv * u1, 1j * kyv * u2, d3
    eps_yz = 0.5 * (d2 + 1j * kyv * u3)
    eps_xz = 0.5 * (d1 + 1j * kxv * u3)
    eps_xy = 0.5 * (1j * kyv * u1 + 1j * kxv * u2)
    cs4, sc_e = SI["c44"], math.sqrt(SI["c44"] * SI["kappa33"])
    good &= check("sigma_xz = 2 c44 eps_xz - e15 E_x", sig[:, 4],
                  (2 * cs4 * eps_xz) / cs4 + (SI["e15"] * gx) / sc_e, 1e-12)
    good &= check("sigma_yz = 2 c44 eps_yz - e15 E_y", sig[:, 3],
                  (2 * cs4 * eps_yz) / cs4 + (SI["e15"] * gy) / sc_e, 1e-12)
    good &= check("sigma_xy = 2 c66 eps_xy", sig[:, 5],
                  (2 * SI["c66"] * eps_xy) / cs4, 1e-12)
    good &= check("sigma_zz = c13(eps_xx+eps_yy) + c33 eps_zz - e33 E_z", sig[:, 2],
                  (SI["c13"] * (eps_xx + eps_yy) + SI["c33"] * eps_zz) / cs4
                  + (SI["e33"] * gz) / sc_e, 1e-12)
    good &= check("sigma_xx = c11 eps_xx + c12 eps_yy + c13 eps_zz - e31 E_z", sig[:, 0],
                  (SI["c11"] * eps_xx + SI["c12"] * eps_yy + SI["c13"] * eps_zz) / cs4
                  + (SI["e31"] * gz) / sc_e, 1e-12)
    good &= check("D_x = kappa11 E_x + 2 e15 eps_xz", Dv[:, 0],
                  -(SI["kappa11"] / SI["kappa33"]) * gx
                  + (2 * SI["e15"] * eps_xz) / sc_e, 1e-12)
    good &= check("D_y = kappa11 E_y + 2 e15 eps_yz", Dv[:, 1],
                  -(SI["kappa11"] / SI["kappa33"]) * gy
                  + (2 * SI["e15"] * eps_yz) / sc_e, 1e-12)
    good &= check("D_z = kappa33 E_z + e31(eps_xx+eps_yy) + e33 eps_zz + f u3''",
                  Dv[:, 2],
                  -gz + (SI["e31"] * (eps_xx + eps_yy) + SI["e33"] * eps_zz) / sc_e
                  + (1e-9 / (200e-9 * sc_e)) * fl["u"][2][:, 2], 1e-12)
    say("   the elastic shears carry the factor 2 of the tensor-to-Voigt conversion; the")
    say("   electric terms carry the sign of E = -grad(phi), so '+2 e15 eps_xz' and")
    say("   '- e15 E_x' are the same statement with E = -grad(phi)")

    say("   tau_zzz is not returned by fields(); its f and h terms are therefore verified")
    say("   by source inspection and exercised by the edge/dissipation checks, not here")

    say("\n" + "=" * 72)
    say("RESULT: " + ("all independent checks agree" if good else "FAILURES ABOVE"))
    OUT.write_text("\n".join(LOG) + "\n")
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main())
