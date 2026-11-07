"""Round-21 Gate 1: exact identification and verification of the natural
boundary data of the implemented second-gradient edge problem.

Physical expressions (derivation: PAPER_A_ROUND21_GATE1_DERIVATION.md), for the
free edge x = 0, normal n = e_x, tangential derivatives d_y -> i k_y and d_z
handled exactly on the Legendre basis:

    traction         t_i = n_j (sigma_ij - d_k tau_ijk) - d_j^s tau_ijn
                        = S_i1 - i k_y tau_{i21} - d_z tau_{i31}
    double traction  m_i = n_j n_k tau_ijk = tau_{i11}
    corner force     f_i = tau_{i31} + tau_{i13}
      (the two mixed normal/tangential hyperstress components carried by the two
       free faces that meet at z = +-1/2; exact identity for a prismatic plate)

Discrete state-space flux rows (model.py::state_from_q):

    T[:nu]  mechanical flux conjugate to the displacement state
    R       x-normal double traction

The identities checked here use no fitting and no adjustable coefficient:

    proj(T[:nu]) = proj(t) + f_+ b0(z_+) - f_- b0(z_-)
    proj(R)      = proj(m)

with proj(v) = int_{-1/2}^{1/2} b0(z) v(z) dz.  Everything is reported per mode
and on the complete incident+reflected field, and the pointwise residuals of the
superposed field are quantified: they are not zero, because the variational
statement imposes the natural data weakly, which is the substantive Gate-1
statement.

Run: PYTHONPATH=paper_a_study .venv/bin/python paper_a_study/round21_gate1_traction.py
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_figure_data import KB0, K0, KY0, operating_mode, plate  # noqa: E402
from model import tensor_matrix  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figure_data", "round21")
CORNER = 0.5


def _proj(v, basis, weights):
    return np.array([basis.T @ (weights * v[:, i]) for i in range(3)]).ravel()


def _node(basis, z, zz):
    return basis[int(np.argmin(abs(z - zz)))]


def _corner_functional_exact(p, ftop, fbot):
    """f_+ b(z_+) - f_- b(z_-) with the basis evaluated exactly at the corners.

    p.eb[0] has rows ordered (-1/2, +1/2), so top = row 1, bottom = row 0.
    """
    top, bot = p.eb[0][1], p.eb[0][0]
    return np.concatenate([fwt * top - fwb * bot for fwt, fwb in zip(ftop, fbot)])


def boundary_fields(p, K, q, ky=None, corner=False):
    """Pointwise natural data of one mode at the x=0 edge.

    With corner=True the fields are evaluated with the endpoint basis
    (p.eb, p.epb), i.e. exactly at z = -1/2 (index 0) and z = +1/2 (index 1),
    which is where the corner line forces live; the Gauss nodes never hit the
    endpoints and using the nearest node leaves an O(nquad^-2) error.
    """
    ky = KY0 if ky is None else ky
    f = p.fields(K, ky, q, p.eb, p.epb) if corner else p.fields(K, ky, q)
    tau = [tensor_matrix(f["tau"][l]) for l in range(3)]
    dtau = [tensor_matrix(f["dtau"][l]) for l in range(3)]
    traction = f["S"][:, :, 0] - 1j * ky * tau[0][:, :, 1] - dtau[0][:, :, 2]
    double = tau[0][:, :, 0]
    corner = tau[0][:, :, 2] + tau[2][:, :, 0]
    return dict(traction=traction, double=double, corner=corner)


def mode_identity(p, K, y, ky=None):
    q = y[: p.nw]
    fl = boundary_fields(p, K, q, ky)
    _, _, T, R = p.state_parts(y)
    b0, w = p.b[0], p.weights
    Tc, Rc = T[: p.nu], R[: p.nw]
    ec = boundary_fields(p, K, q, corner=True)["corner"]
    ftop, fbot = ec[1], ec[0]          # p.eb is ordered (-1/2, +1/2)
    corner_fun = _corner_functional_exact(p, ftop, fbot)
    base = _proj(fl["traction"], b0, w)
    return dict(
        traction_incl_corner=float(np.linalg.norm(base + corner_fun - Tc) / np.linalg.norm(Tc)),
        traction_plain=float(np.linalg.norm(base - Tc) / np.linalg.norm(Tc)),
        double=Float(np.linalg.norm(_proj(fl["double"], b0, w) - Rc) / np.linalg.norm(Rc)),
    )


def Float(x):
    return float(x)


def _enc(o):
    """JSON encoder for the complex values stored alongside the scalars."""
    if isinstance(o, complex):
        return [float(o.real), float(o.imag)]
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.integer):
        return int(o)
    raise TypeError(type(o))


def run_case(degree, nquad=0, label=""):
    p = plate(0.0, degree=degree, nquad=nquad)
    mode = operating_mode(p)
    om = float(mode["omega"].real)
    res, scr = p.edge(KY0, om, K0, KB0)

    modes = [(1.0, scr["incident"]["K"], scr["incident"]["q"], scr["incident"]["y"])]
    for j, (Kj, aj) in enumerate(zip(scr["K"], scr["amplitudes"])):
        modes.append((aj, Kj, scr["Y"][: p.nw, j], scr["Y"][:, j]))
    ident = [mode_identity(p, K, y) for _, K, _, y in modes]

    b0, w, z = p.b[0], p.weights, p.z
    it, ib = int(np.argmin(abs(z - CORNER))), int(np.argmin(abs(z + CORNER)))
    acc = None
    inc = None
    ctop = cbot = 0.0
    for c, K, q, _ in modes:
        fl = boundary_fields(p, K, q)
        if acc is None:
            acc = {k: c * v for k, v in fl.items()}
            inc = {k: v.copy() for k, v in fl.items()}
        else:
            for k in acc:
                acc[k] = acc[k] + c * fl[k]
        ctop = ctop + c * fl["corner"][it]
        cbot = cbot + c * fl["corner"][ib]

    def l2(v):
        return float(np.sqrt(np.sum(w[:, None] * abs(v) ** 2)))

    total = scr["incident"]["y"] + scr["Y"] @ scr["amplitudes"]
    weak_row = float(np.linalg.norm(p.boundary_vector(total)))
    return dict(
        label=label or f"degree={degree}",
        degree=degree,
        nquad=p.nquad,
        omega=om,
        incident_K=[float(scr["incident"]["K"].real), float(scr["incident"]["K"].imag)],
        backward_K=[float(res["backward_K"].real), float(res["backward_K"].imag)],
        R_B=float(res["backward_reflection_self_power"]),
        edge_scaled_residual=float(res["edge_scaled_residual"]),
        weak_boundary_row=weak_row,
        mode_traction_incl_corner=max(x["traction_incl_corner"] for x in ident),
        mode_traction_plain=max(x["traction_plain"] for x in ident),
        mode_double=max(x["double"] for x in ident),
        per_mode=ident,
        superposed_traction_l2_rel=float(l2(acc["traction"]) / l2(inc["traction"])),
        superposed_traction_max_rel=float(np.max(abs(acc["traction"])) / np.max(abs(inc["traction"]))),
        superposed_double_l2_rel=float(l2(acc["double"]) / l2(inc["double"])),
        superposed_double_max_rel=float(np.max(abs(acc["double"])) / np.max(abs(inc["double"]))),
        corner_top=ctop.tolist(),
        corner_bottom=cbot.tolist(),
        corner_rel=float(max(np.max(abs(ctop)), np.max(abs(cbot)))
                         / max(np.max(abs(inc["corner"])), 1e-30)),
        corner_incident_top=inc["corner"][it].tolist(),
        corner_incident_bottom=inc["corner"][ib].tolist(),
        corner_top_abs=float(np.max(abs(ctop))),
        corner_bottom_abs=float(np.max(abs(cbot))),
    )


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for degree in (8, 10, 12, 14, 16):
        rows.append(run_case(degree))
        r = rows[-1]
        print(f"{r['label']:12s} nquad={r['nquad']:3d} R_B={r['R_B']:.10f}")
        print("   identity  traction(incl corner)=%.2e  plain=%.2e  double=%.2e"
              % (r["mode_traction_incl_corner"], r["mode_traction_plain"], r["mode_double"]))
        print("   superposed traction l2=%.3e max=%.3e | double l2=%.3e max=%.3e | corner rel=%.3e"
              % (r["superposed_traction_l2_rel"], r["superposed_traction_max_rel"],
                 r["superposed_double_l2_rel"], r["superposed_double_max_rel"],
                 r["corner_rel"]))
        print("   corner top=%s bottom=%s" % (np.round(r["corner_top"], 5),
                                              np.round(r["corner_bottom"], 5)))
    for nq in (96, 192):
        rows.append(run_case(12, nquad=nq, label=f"degree=12,nquad={nq}"))
        r = rows[-1]
        print(f"{r['label']:22s} R_B={r['R_B']:.12f} traction=%.2e corner_rel=%.3e"
              % (r["mode_traction_incl_corner"], r["corner_rel"]))

    path = os.path.join(OUT, "gate1_traction_identity.json")
    with open(path, "w") as handle:
        json.dump(rows, handle, indent=1, default=_enc)
    print("wrote", path)

    # The incident mode is the physical statement and must close at round-off.
    # Reflected evanescent modes are ill-conditioned (|Im k_x| up to 2.5e2 makes
    # the individual hyperstress terms ~1e2 larger than the flux they cancel), so
    # their bound is looser by construction and is reported, not hidden.
    ok_inc = all(r["per_mode"][0]["traction_incl_corner"] < 1e-10
                 and r["per_mode"][0]["double"] < 1e-10 for r in rows)
    ok_worst = all(r["mode_traction_incl_corner"] < 1e-4 for r in rows)
    print("GATE1 identity, incident mode (<1e-10):", "PASS" if ok_inc else "FAIL")
    print("GATE1 identity, worst reflected mode (<1e-4):", "PASS" if ok_worst else "FAIL")
    ok = ok_inc and ok_worst
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
