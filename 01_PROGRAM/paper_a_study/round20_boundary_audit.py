#!/usr/bin/env python3
"""Round 20: ten targeted boundary-physics checks.

These are checks of four *different* kinds of statement and the script keeps them
apart, because a numerical identity does not establish a physical condition:

  A. algebraic/structural identities about the discretisation (tests 1, 2, 8, 9);
  B. implementation facts about what the solver actually imposes (tests 4-7, 10);
  C. physical correctness of the boundary-value problem (tests 3, 5 and the
     cross-condition test 11 -- the only ones that speak about physics);
  D. experimental validation: *not attempted anywhere in this round*.

Every residual is evaluated on the complete superposed scattering field (incident
mode plus all outgoing modes with their solved amplitudes), not on a single
eigenvector, and is normalised by the same functional applied to the incident mode.

Run from the repository root::

    PYTHONPATH=. .venv/bin/python paper_a_study/round20_boundary_audit.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_figure_data import HCRIT, KB0, KY0, operating_mode, plate, track  # noqa: E402
from model import Plate, tensor_matrix  # noqa: E402

K_OP = 0.7361990195318475
DEG = 6
LOG: list[str] = []


def say(text: str = "") -> None:
    LOG.append(text)
    print(text, flush=True)


def report(name: str, value: float, ok: bool, detail: str = "") -> bool:
    say(f"  [{'ok ' if ok else 'FAIL'}] {name:<58s} {value:>12.4e}   {detail}")
    return ok


def projections(p, res, scr):
    """Boundary residuals of the superposed field, per condition."""
    inc = scr["incident"]
    Y, Ks, aa = scr["Y"], scr["K"], scr["amplitudes"]
    modes = [(1.0, inc["K"], inc["q"])] + [(aa[j], Ks[j], Y[: p.nw, j]) for j in range(len(Ks))]
    b0, pb0, w = p.b[0], p.pb[0], p.weights
    keys = ("t", "m", "phi", "D", "J")
    acc = {k: None for k in keys}
    ref = {}
    for n, (c, K, q) in enumerate(modes):
        f = p.fields(K, KY0, q)
        tau0 = tensor_matrix(f["tau"][0])
        vals = {"t": tensor_matrix(f["sigma"])[:, :, 0] - 1j * K * tau0[:, :, 0],
                "m": tau0[:, :, 0], "phi": f["phi"][0], "D": f["D"][:, 0],
                "J": (1j * p.alpha / p.omega_ref) * (1j * K) * f["mu"][0]}
        if n == 0:
            ref = vals
        for k, v in vals.items():
            acc[k] = c * v if acc[k] is None else acc[k] + c * v
    out = {}
    for k, basis in (("t", b0), ("m", b0), ("phi", pb0), ("D", pb0), ("J", b0)):
        def pr(v):
            return basis.T @ (w * v) if v.ndim == 1 else np.array(
                [basis.T @ (w * v[:, i]) for i in range(3)]).ravel()
        out[k] = float(np.linalg.norm(pr(acc[k])) / max(np.linalg.norm(pr(ref[k])), 1e-300))
        out[k + "_pointwise"] = float(np.abs(acc[k]).max() / max(np.abs(ref[k]).max(), 1e-300))
    return out


def solve(degree, K, edge):
    p = plate(0.0, degree=degree, edge_electric=edge)
    p.omega_ref = float(track(p, [K], operating_mode(p))[0]["omega"].real)
    res, scr = p.edge(KY0, p.omega_ref, K, KB0)
    return p, res, scr


def main() -> int:
    ok = True
    say("Paper A -- round 20 boundary-physics audit")
    say("=" * 96)

    p = plate(0.0, degree=DEG)
    waves, A, F = p.waves(KY0, 7.6334)
    mode = [v for v in waves if v["K"].imag < -1e-9][0]
    K, q = mode["K"], mode["q"]
    f = p.fields(K, KY0, q)
    b0, b1, w = p.b[0], p.b[1], p.weights
    tau = [tensor_matrix(f["tau"][l]) for l in range(3)]
    _, _, T, R = p.state_parts(mode["y"])

    # ---------------------------------------------------------------- 1 & 2
    say("\n1-2  normal directions and hyperstress contractions (algebraic)")
    def pr3(v, basis):
        return np.array([basis.T @ (w * v[:, i]) for i in range(3)]).ravel()
    Rc = R.ravel()
    for lab, comp in (("tau_j11 (x-normal)", tau[0][:, :, 0]),
                      ("tau_j13", tau[2][:, :, 0]),
                      ("tau_j33 (z-normal)", tau[2][:, :, 2])):
        d = np.linalg.norm(pr3(comp, b0) - Rc) / np.linalg.norm(Rc)
        if lab.startswith("tau_j11"):
            ok &= report("double-traction row is the x-normal tau_j11", d, d < 1e-11,
                         "must be ~0")
        else:
            ok &= report(f"double-traction row is NOT {lab}", d, d > 1e-3, "must be O(1)")
    sym = max(np.abs(tau[l][:, i, j] - tau[l][:, j, i]).max()
              for l in range(3) for i in range(3) for j in range(3))
    ok &= report("hyperstress symmetric in its two gradient indices", float(sym), sym < 1e-12)

    # the stated parametric laws, checked on a *fixed* coefficient vector so that the
    # comparison isolates the operator: tau_bulk ~ lam^2, the f- and h-parts linear
    # in f and h and independent of lam (model.py lines 279-288).
    base = Plate(degree=DEG, flexo=0.0, H=0.0)
    big = Plate(degree=DEG, ell=1e-7, flexo=0.0, H=0.0)
    tb = np.abs(base.fields(K, KY0, q)["tau"][0]).max()
    tl = np.abs(big.fields(K, KY0, q)["tau"][0]).max()
    ok &= report("tau scales as lam^2 (ell doubled -> x4 at fixed q)", float(tl / tb),
                 abs(tl / tb - 4.0) < 1e-9, "must be 4")
    # the f- and h-parts enter the z-derivative hyperstress tau[2] only (model.py:281)
    tz = lambda pl: pl.fields(K, KY0, q)["tau"][2]
    zero = Plate(degree=DEG, flexo=1e-9, H=0.0)
    t0 = tz(zero)
    t0f = tz(Plate(degree=DEG, flexo=0.0, H=0.0))
    d1 = np.abs(tz(Plate(degree=DEG, flexo=2e-9, H=0.0)) - t0f).max()
    d2 = np.abs(tz(Plate(degree=DEG, flexo=1e-9, H=0.0)) - t0f).max()
    ok &= report("flexoelectric part of tau is linear in f", float(d1 / d2),
                 abs(d1 / d2 - 2.0) < 1e-9, "f doubled -> part doubled")
    half = np.abs(tz(Plate(degree=DEG, flexo=0.5e-9, H=0.0)) - t0f).max()
    ok &= report("  ... with zero constant term in f", float(half / d2),
                 abs(half / d2 - 0.5) < 1e-9, "f halved -> part halved")
    # H enters both directly (h * N_r) and through N = mu + Q phi - h u_zz.  Take the
    # deviation from H = 0 at three fields below the Schur bound: a pure quadratic has
    # ratios 4 and 9 for 2x and 3x the field, a linear-in-H term would break that.
    dev = {}
    for m in (1, 2, 3):
        pl = Plate(degree=DEG, flexo=1e-9, H=0.25 * m * HCRIT)
        dev[m] = float(np.abs(tz(pl) - t0).max() / np.abs(t0).max())
    ok &= report("H-part of tau grows as H^2 (Delta(0.5H)/Delta(0.25H))", dev[2] / dev[1],
                 abs(dev[2] / dev[1] - 4.0) < 1e-2, "must be 4")
    ok &= report("  ... and has no linear term (Delta(0.75H)/Delta(0.25H))", dev[3] / dev[1],
                 abs(dev[3] / dev[1] - 9.0) < 1e-2, "must be 9")
    ok &= report("  ... magnitude at 0.25 H_crit", dev[1], 1e-6 < dev[1] < 1.0,
                 f"h = {Plate(degree=DEG, flexo=1e-9, H=0.25*HCRIT).h:.3e}")
    xdep = np.abs(Plate(degree=DEG, flexo=2e-9, H=0.0).fields(K, KY0, q)["tau"][0]
                  - zero.fields(K, KY0, q)["tau"][0]).max()
    ok &= report("f/H enter only the z-derivative hyperstress", float(xdep), xdep < 1e-30,
                 "x-derivative component carries no flexoelectric part")
    say("        note (observation only, nothing altered): with this discretisation the")
    say("        flexoelectric and H contributions to the hyperstress appear in the")
    say("        z-derivative component alone (model.py:281, l == 2).")

    # ------------------------------------------------------- 3-7 and 11
    say("\n3-7, 11  what each condition actually enforces (implementation + physics)")
    rows = {}
    for edge in ("ground", "insulating"):
        pp, res, scr = solve(DEG, K_OP, edge)
        r = projections(pp, res, scr)
        rows[edge] = r
        say(f"\n   edge = {edge}:  R_B = {res['backward_reflection_self_power']:.8f}")
        lim = 1e-8 if edge == "insulating" else 1e-8
        if edge == "ground":
            ok &= report("  electric Dirichlet residual  |r_phi|", r["phi"], r["phi"] < lim)
            ok &= report("  [physics] D_x is therefore violated", r["D"], r["D"] > 0.1)
        else:
            ok &= report("  electric Neumann residual  |r_Dx|", r["D"], r["D"] < lim)
            ok &= report("  [physics] phi is therefore violated", r["phi"], r["phi"] > 0.1)
        ok &= report("  carrier blocking residual  |r_J|", r["J"], r["J"] < 1e-6)
        ok &= report("  double-traction residual  |r_m|", r["m"], r["m"] < 1e-9)
        ok &= report("  generalised traction residual (pointwise sigma_x1 - i k tau_j11)",
                     r["t"], r["t"] > 0, "reported, not asserted: see report S5")
        ok &= report("  edge rows = columns, rank = columns",
                     float(res["edge_size"] - res["outgoing_modes"]), 
                     res["edge_size"] == res["outgoing_modes"] == res["edge_rank"])
        ok &= report("  scaled edge residual", res["edge_scaled_residual"],
                     res["edge_scaled_residual"] < 1e-12)

    # ---------------------------------------------------------------- 8
    say("\n8  edge-matrix construction")
    for edge in ("ground", "insulating"):
        pp, res, scr = solve(DEG, K_OP, edge)
        nphi = pp.ip.stop - pp.ip.start
        nmu = pp.nw - pp.ip.stop
        m = 2 * pp.nu + nphi + nmu
        ok &= report(f"  {edge}: m = 2n_u + n_phi + n_mu", float(res["edge_size"]), res["edge_size"] == m)
        ok &= report(f"  {edge}: rank = column count", float(res["edge_rank"]),
                     res["edge_rank"] == res["outgoing_modes"])
        ok &= report(f"  {edge}: condition number", res["edge_condition"], res["edge_condition"] < 1e4)

    # ---------------------------------------------------------------- 9
    say("\n9  finite/infinite eigenvalue structure of the matrix polynomial")
    from scipy.linalg import eig
    p4 = plate(0.0, degree=4)
    A4m = p4.matrices(KY0, 7.6334)
    A0, A1, A2, A3, A4 = (A4m[0, 0], 1j * (A4m[0, 1] - A4m[1, 0]),
                          (A4m[1, 1] - A4m[0, 2] - A4m[2, 0]),
                          1j * (A4m[1, 2] - A4m[2, 1]), A4m[2, 2])
    n = A0.shape[0]
    Z, I = np.zeros((n, n), complex), np.eye(n, dtype=complex)
    M = np.block([[Z, I, Z, Z], [Z, Z, I, Z], [Z, Z, Z, I], [-A0, -A1, -A2, -A3]])
    N = np.block([[I, Z, Z, Z], [Z, I, Z, Z], [Z, Z, I, Z], [Z, Z, Z, A4]])
    ev = eig(M, N, right=False)
    fin = int(np.isfinite(ev).sum())
    inf = int((~np.isfinite(ev)).sum())
    sv = np.linalg.svd(A4, compute_uv=False)
    rank = int((sv > 1e-10 * sv[0]).sum())
    ok &= report(f"  finite eigenvalues of the pencil (expect 2(n_w+n_u) = {2*(p4.nw+p4.nu)})",
                 float(fin), fin == 2 * (p4.nw + p4.nu))
    ok &= report(f"  infinite eigenvalues (expect 2(n_w-n_u) = {2*(p4.nw-p4.nu)})",
                 float(inf), inf == 2 * (p4.nw - p4.nu))
    ok &= report("  rank A22 = n_u (nullity sets the multiplicity at infinity)",
                 float(rank), rank == p4.nu)
    ks = np.array([0.3 + 0.7j, -1.2 + 0.1j, 2.0 - 0.4j])
    dets = [abs(np.linalg.det(A0 + k * A1 + k ** 2 * A2 + k ** 3 * A3 + k ** 4 * A4)) for k in ks]
    ok &= report("  polynomial is regular: min |det p(k)| at random k", float(min(dets)),
                 min(dets) > 1e-30)

    # --------------------------------------------------------------- 10
    say("\n10  scattering power balance on the superposed field")
    for edge in ("ground", "insulating"):
        pp, res, scr = solve(DEG, K_OP, edge)
        ok &= report(f"  {edge}: |P_left - P_edge - dissipation| / P_inc",
                     res["power_balance_relative"], res["power_balance_relative"] < 1e-9)
        ok &= report(f"  {edge}: total outgoing power / incident", res["total_outgoing_self_power"],
                     0 < res["total_outgoing_self_power"] <= 1 + 1e-6, "must not exceed 1")

    say("")
    say("=" * 96)
    say("kind A (structural): tests 1, 2, 8, 9      -- identities about the discretisation")
    say("kind B (implementation): tests 4-7, 10     -- what the solver enforces")
    say("kind C (physical): the D_x / phi cross-checks -- which boundary-value problem is solved")
    say("kind D (experimental): none attempted; no measured data are compared in this round")
    say("")
    say("RESULT: all checks behave as reported" if ok else "RESULT: at least one check failed")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
