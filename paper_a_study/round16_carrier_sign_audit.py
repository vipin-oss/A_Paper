"""Round-16 audit: carrier strong->weak sign, operator comparison, Gauss factor.

Independent of ``Plate.matrices`` for the carrier block: the reference
operator is rebuilt from ``numpy.polynomial.legendre`` and a 200-node
Gauss-Legendre rule.  Run from the repository root:

    python paper_a_study/round16_carrier_sign_audit.py

Every number printed here is quoted in the round-16 reports.
"""
import numpy as np
from numpy.polynomial.legendre import Legendre, leggauss

from paper_a_study.model import Plate, SI, CONST

LINE = "-" * 72


def quad_rule(nodes=200):
    x, w = leggauss(nodes)
    return x / 2.0, w / 2.0          # z in [-1/2, 1/2], dz = d(xi)/2


def basis(z, order, m):
    """Same normalisation as Plate.basis: sqrt(2j+1) 2^r P_j^{(r)}(2z)."""
    return np.stack([np.sqrt(2 * j + 1) * 2.0 ** order
                     * Legendre.basis(j).deriv(order)(2 * z) for j in range(m)], axis=1)


def bil(A, C, w):
    """Bilinear form  int A^T (w C).  Never sum axis 0 here."""
    return A.T @ (w[:, None] * C)


def carrier_row(pb, kx, ky, om, z, w):
    """The carrier (mu) test row of the reduced operator, rebuilt from scratch.

    Row layout of the trial columns: u1 | u2 | u3 | phi(np) | mu(n).
    """
    n, npot, nu = pb.n, pb.np, pb.nu
    Bb, Bz, Bz2 = basis(z, 0, n), basis(z, 1, n), basis(z, 2, n)
    # grounded potential space exactly as model.Plate.basis builds it
    ratio = np.sqrt((2 * np.arange(npot) + 1.0) / (2 * np.arange(npot) + 5.0))
    Pg = np.stack([Bb[:, j] - ratio[j] * Bb[:, j + 2] for j in range(npot)], axis=1)

    R = np.zeros((n, pb.nw), complex)
    F = kx * kx * bil(Bb, Bb, w) + ky * ky * bil(Bb, Bb, w) + bil(Bz, Bz, w)
    R[:, 2 * n:3 * n] = pb.h * bil(Bb, Bz2, w)              # + h u3''  (from N)
    R[:, nu:nu + npot] = -pb.Q * bil(Bb, Pg, w)             # - Q phi
    R[:, nu + npot:] = -1j * pb.alpha / om * F - bil(Bb, Bb, w)   # -i a/w F - M
    return R, F


def implemented_row(pb, kx, ky, om):
    """Same row lifted out of the assembled blocks via (-i kx)^r (i kx)^s."""
    A = pb.matrices(ky, om)
    n, npot, nu = pb.n, pb.np, pb.nu
    G = np.zeros((n, pb.nw), complex)
    for i in range(n):
        row = nu + npot + i
        for jc in range(pb.nw):
            G[i, jc] = sum((-1j * kx) ** r * (1j * kx) ** s * A[r, s][row, jc]
                           for r in range(3) for s in range(3))
    return G


def main():
    print("ROUND 16 CARRIER / GAUSS / MECHANICAL AUDIT LOG")
    print(LINE)
    z, w = quad_rule()

    # ---------------------------------------------------------------- 1. row
    print("1. CARRIER ROW: independent reference vs implemented assembly")
    for degree in (4, 6):
        pb = Plate(degree=degree, H=1.073e-24)
        worst = 0.0
        for kx, ky, om in ((0.7362, 0.1298, 7.6334), (0.5275, 0.0, 6.9),
                           (-0.30, 0.20, 4.0)):
            ref, _ = carrier_row(pb, kx, ky, om, z, w)
            got = implemented_row(pb, kx, ky, om)
            rel = np.max(np.abs(got - ref)) / np.max(np.abs(got))
            worst = max(worst, rel)
            print("   degree=%d kx=%+.4f ky=%.4f om=%.4f  |row|=%.3e  "
                  "max|diff|=%.2e  rel=%.2e"
                  % (degree, kx, ky, om, np.max(np.abs(got)),
                     np.max(np.abs(got - ref)), rel))
        print("   -> worst relative deviation, degree %d: %.2e" % (degree, worst))

    pb = Plate(degree=4, H=1.073e-24)
    print("   n=%d nw=%d nu=%d npot=%d  Q=%.12f  alpha_d=%.12f  h=%.6e"
          % (pb.n, pb.nw, pb.nu, pb.np, pb.Q, pb.alpha, pb.h))

    # ------------------------------------------------- 2. sign / dissipation
    print(LINE)
    print("2. SIGN OF THE TRANSPORT BLOCK AND DISSIPATIVITY (e^{-i omega t})")
    Bb, Bz = basis(z, 0, pb.n), basis(z, 1, pb.n)
    kx, ky, om = 0.7362, 0.1298, 7.6334
    F0 = kx * kx * bil(Bb, Bb, w) + ky * ky * bil(Bb, Bb, w) + bil(Bz, Bz, w)
    T = -1j * pb.alpha / om * F0
    print("   implemented transport block  -i a/w F : max|Re| = %.1e" % np.max(np.abs(T.real)))
    print("   min eig(F) = %.6e  (>0: F positive definite)" % np.min(np.linalg.eigvalsh(F0)))
    print("   the two candidate blocks differ by 2*max|T| = %.6e (operator norm)"
          % (2 * np.max(np.abs(T))))
    # pure carrier mode: -i w N - a lap(mu) = 0 -> w = -i a |grad|^2/|N|^2, Im w < 0
    for kappa in (1.0, 3.0):
        Fk = kappa ** 2 + 0.25
        omega_from_plus = -1j * pb.alpha * Fk
        omega_from_minus = +1j * pb.alpha * Fk
        print("   kappa=%4.1f  correct sign -> Im omega = %+8.4f (decay, e^{-i omega t} "
              "gives e^{+Im omega t});  printed minus -> Im omega = %+8.4f (growth)"
              % (kappa, omega_from_plus.imag, omega_from_minus.imag))
    print("   model.py dissipation functional: 0.5*alpha*int[(kx^2+ky^2)|mu|^2+|d_z mu|^2]"
          " >= 0 (line 297) -> consistent with -i a/w F, not with +i a/w F")

    # ------------------------------------------------------- 3. Gauss factor
    print(LINE)
    print("3. GAUSS ROW: IS THE MOBILE-CHARGE COEFFICIENT 1 OR Q?")
    # The phi-test row of the discrete system comes from  -<G,kap G>  (dielectric)
    # and from the completed square  <W,W>  with W = mu + Q phi - h u3''.  Rebuild
    # both entries from scratch on the model's own quadrature rule.
    zw, ww = pb.z, pb.weights
    Bb = basis(zw, 0, pb.n)
    ratio = np.sqrt((2 * np.arange(pb.np) + 1.0) / (2 * np.arange(pb.np) + 5.0))
    Pg = np.stack([Bb[:, j] - ratio[j] * Bb[:, j + 2] for j in range(pb.np)], axis=1)
    dzP = basis(zw, 1, pb.n)
    dPg = np.stack([dzP[:, j] - ratio[j] * dzP[:, j + 2] for j in range(pb.np)], axis=1)
    grad_phi = [np.stack([1j * pb.Q * 0 + 0 * Pg, 0 * Pg, dPg], axis=2)]
    for ky, om in ((0.0, 6.9), (0.1298, 7.6334)):
        A = pb.matrices(ky, om)
        ip, im, nu = pb.ip, pb.im, pb.nu
        # dielectric part: -int (grad phi_i) . (kap grad phi_j) for (kx=ky=0: d_z only)
        kap33 = pb.kap[2, 2]
        ref_pp = -kap33 * bil(dPg, dPg, ww) - pb.kap[0, 0] * ky * ky * bil(Pg, Pg, ww)
        got_pp = A[0, 0][ip, ip]
        # charge-coupling part: Q^2 int pb_i pb_j  (from the square) and Q int pb_i b_j
        ref_pp_charge = -pb.Q ** 2 * bil(Pg, Pg, ww)   # from  A -= W^H W
        ref_pm = -pb.Q * bil(Pg, Bb, ww)               # from  A -= W^H W
        got_pm = A[0, 0][ip, im]
        print("   ky=%.4f: phi-phi block: max|A - (-kappa d_z + Q^2)| = %.2e (scale %.2e)"
              % (ky, np.max(np.abs(got_pp - (ref_pp + ref_pp_charge))),
                 np.max(np.abs(got_pp))))
        print("            phi-mu  block: max|A - Q int(pb,b)| = %.2e (scale %.2e)"
              % (np.max(np.abs(got_pm - ref_pm)), np.max(np.abs(got_pm))))
        rel = np.max(np.abs(got_pm - ref_pm)) / np.max(np.abs(got_pm))
        print("            charge coupling vs  -Q int(pb,b): rel = %.2e  (elementwise)" % rel)
    print("   -> the discrete Gauss row carries the mobile charge with coefficient Q,")
    print("      not 1: the printed -int N psi* of eq:weak_gauss is off by 1/Q = %.4f"
          % (1.0 / pb.Q))
    L_D = np.sqrt(SI["kappa33"] * CONST["kB"] * 301.7 / (CONST["q"] ** 2 * 2e18))
    print("   check Q = d/L_D: Q=%.12f  d/L_D=%.12f  rel=%.2e"
          % (pb.Q, 200e-9 / L_D, abs(pb.Q - 200e-9 / L_D) / pb.Q))
    cs = np.sqrt(SI["c44"] / SI["rho"])
    print("   check alpha_d = D/(d c_s): %.12f vs %.12f"
          % (pb.alpha, pb.diffusivity / (200e-9 * cs)))

    # ------------------------------------------- 4. reciprocity / hermiticity
    print(LINE)
    print("4. BLOCK STRUCTURE: RECIPROCITY AND THE NON-HERMITIAN PART")
    for ky, om in ((0.0, 6.9), (0.1298, 7.6334)):
        A = pb.matrices(ky, om)
        h = lambda M: M.conj().T
        print("   ky=%.4f om=%.4f  nw=%d" % (ky, om, pb.nw))
        for (r, s) in ((0, 1), (1, 2), (2, 2), (0, 2), (0, 0), (1, 1)):
            ref = A[s, r].conj().T if (r, s) != (2, 2) else A[2, 2]
            d = np.max(np.abs(A[r, s] - ref)) / max(np.max(np.abs(A[r, s])), 1e-300)
            print("      A%d%d vs %s : rel.asym = %.2e" % (r, s, "A%d%d^H" % (s, r), d))
        # remove the transport block from A00 and A11: what is left must be Hermitian
        MG = pb.operators(ky)[3]
        for r in (0, 1):
            T = -1j * pb.alpha / om * pb.form(MG[r].conj(), np.eye(3), MG[r], pb.weights)
            rest = A[r, r] - T
            print("      A%d%d - transport : max|asym| = %.2e  (A%d%d alone: %.2e)"
                  % (r, r, np.max(np.abs(rest - rest.conj().T)), r, r,
                     np.max(np.abs(A[r, r] - A[r, r].conj().T))))

    # ------------------------------------------ 5. contraction identity check
    print(LINE)
    print("5. CONTRACTION IDENTITY tau_jik = tau_jik (i<->j symmetry)")
    for ky in (0.0, 0.1298):
        q = np.random.default_rng(3).normal(size=pb.nw) + 0j
        f = pb.fields(1.7, ky, q)
        for l, name in ((0, "x"), (1, "y"), (2, "z")):
            from paper_a_study.model import tensor_matrix
            T = tensor_matrix(f["tau"][l])
            asym = np.max(np.abs(T - np.transpose(T, (0, 2, 1))))
            print("      direction %s: max|tau_ij - tau_ji| = %.2e (scale %.2e)"
                  % (name, asym, np.max(np.abs(T))))
    print(LINE)
    print("END OF LOG")


if __name__ == "__main__":
    main()
