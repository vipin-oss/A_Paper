"""Authoritative numerical source data for the ten Paper A figures.

Every plotted number is produced here from ``paper_a_study.model`` -- no value is
transcribed from an earlier CSV.  The physics is untouched: the same weak form,
the same constitutive law, the same ``Delta H = Delta n H_jkl eps_jk,l`` term and
the same edge-matching solver.  What is repaired is *bookkeeping*:

Wave-speed definitions
    phase speed      v_p  = c_s omega / |k|,      |k| = hypot(k_x, k_y)
    group velocity   v_g  = c_s d(omega)/d(k_x)   (central differences on the
                                                  branch-tracked sequence)
    energy velocity  v_E  = c_s P_x / E           (thickness-integrated physical
                                                  power over stored energy)
    The previous CSV divided by ``|k|**3`` for the "group" speed and copied the
    phase speed into the "energy" column; those two columns are discontinued.

Attenuation
    From *complex spatial roots at real frequency*: alpha = 2|Im k|, in m^-1 and
    dB mm^-1 via 8.686 alpha / 1000.  The previous column used the imaginary part
    of ``sqrt(K**2+KY**2)`` for real K, which is identically zero.

Reference plane
    The edge sits at x = 0 and the plate occupies x < 0.  The incident wave has
    Re k_x > 0 and Im k_x > 0, so |P| ~ exp(-2 Im k_x x) and the incident
    amplitude *decreases* as it travels towards the edge: the fraction surviving
    from a launch plane at distance l is exp(-2 Im k_i l) <= 1.  The previous
    column reported the reciprocal, exp(+2 Im k_i l) >= 1, and mislabelled it
    "incident_survival".

Isolated-channel return
    R_B(l) = R_B,edge exp(-alpha_B l),  alpha_B = 2|Im k_B|,
    a ratio of the backward to the incident self-power of the *same single
    channel*, never a total reflectance.

Modal power decomposition
    Outgoing modes are split into propagating (|Im K| <= 1e-3, i.e. attenuation
    length >= 200 um, so they reach every reference plane) and near-field
    (evanescent).  Evanescent modal flux is reported as a reactive bookkeeping
    quantity at the plane, explicitly not transported far-field energy.
"""
from __future__ import annotations

import csv
import json
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")

from model import Plate  # noqa: E402  (same directory when run as a script)

HERE = Path(__file__).resolve().parent
DATA = HERE / "figure_data"

DEGREE = 22
HCRIT = 4.0097064373759543e-22
KY0 = 0.12981175031447484          # operating tangential wavenumber
OMEGA0 = 7.633372404423294         # operating angular frequency (normalised)
K0 = 0.7361990195318475            # incident k_x  (normalised)
KB0 = 0.2451746921716515           # backward-channel k_x (normalised)
ETAS = [-0.05, -0.025, 0.0, 0.025, 0.05]
REF_NORM = 10.0                    # reference plane L = 10 d = 2 um at d = 200 nm


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def dump_csv(name: str, rows: list[dict]) -> Path:
    DATA.mkdir(parents=True, exist_ok=True)
    path = DATA / name
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: _cell(row.get(k)) for k in fields})
    return path


def _cell(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (np.floating, float)):
        return f"{float(value):.12g}"
    if isinstance(value, (np.integer, int)):
        return str(int(value))
    return str(value)


def dump_json(name: str, payload) -> Path:
    DATA.mkdir(parents=True, exist_ok=True)
    path = DATA / name
    path.write_text(json.dumps(payload, indent=1, sort_keys=False) + "\n")
    return path


def plate(eta: float = 0.0, **kw) -> Plate:
    kw.setdefault("degree", DEGREE)
    return Plate(H=float(eta) * HCRIT, **kw)


def operating_mode(p: Plate):
    """Branch-tracked guided mode at the operating point (k_x=K0, k_y=KY0)."""
    modes = p.temporal(K0, ky=KY0)
    return min(modes, key=lambda m: abs(m["omega"].real - OMEGA0))


def track(p: Plate, Ks, reference):
    """Follow one branch through a k_x sweep, keeping mass-orthogonality (MAC)."""
    out, mode = [], reference
    for K in Ks:
        mode = p.temporal(float(K), mode, ky=KY0)
        if mode["omega"].real <= 0:
            raise RuntimeError(f"branch lost at K={K}")
        out.append(mode)
    return out


def spatial_root(p: Plate, omega: float, k_target: float) -> complex:
    """Complex spatial root at *real* frequency nearest to a target Re K."""
    waves, _, _ = p.waves(KY0, float(omega))
    Ks = np.array([w["K"] for w in waves])
    score = np.abs(Ks.real - k_target) + 1e-3 * np.abs(Ks.imag)
    return complex(Ks[int(np.argmin(score))])


def power_profile(p: Plate, kx: float, ky: float, omega: float, q):
    """Per-z thickness-resolved x power density of one mode (arbitrary units)."""
    f = p.fields(kx, ky, q)
    v = -1j * omega * f["u"][0]
    edot = -1j * omega * f["strain"][0]
    out = {}
    for axis, kk in ((0, kx), (1, ky)):
        mech = (-np.sum(f["S"][:, :, axis] * v.conj(), axis=1)
                - np.sum(f["tau"][axis] * edot.conj(), axis=1))
        electric = f["phi"][0] * (-1j * omega * f["D"][:, axis]).conj()
        chemical = f["mu"][0] * (-p.alpha * 1j * kk * f["mu"][0]).conj()
        out["x" if axis == 0 else "z"] = 0.5 * np.real(mech + electric + chemical)
    return out


def isolated_transfer(R2um: float, kb: complex, d: float, distance_m: float) -> float:
    """R_B(l) from the 2 um reference value using the solved backward decay."""
    alpha_b = 2.0 * abs(kb.imag) / d
    return float(R2um * np.exp(-alpha_b * (distance_m - REF_NORM * d)))


# --------------------------------------------------------------------------
# Figure 1 -- dispersion, phase/group/energy speed, spatial attenuation
# --------------------------------------------------------------------------
def fig01() -> list[dict]:
    rows = []
    Ks = np.linspace(0.15, 1.05, 31)
    for eta in ETAS:
        p = plate(eta)
        modes = track(p, Ks, operating_mode(p))
        omega = np.array([m["omega"].real for m in modes])
        vg = np.gradient(omega, Ks) * p.cs                     # central differences
        for K, m, v in zip(Ks, modes, vg):
            diag = p.mode_diagnostics(float(K), KY0, m["omega"], m["q"])
            kabs = float(np.hypot(K, KY0))
            ksp = spatial_root(p, m["omega"].real, float(K))
            alpha = 2.0 * abs(ksp.imag) / p.d
            rows.append(dict(
                eta=float(eta), K=float(K), ky=KY0,
                frequency_GHz=float(m["omega"].real * p.fscale / 1e9),
                FWHM_MHz=float(-2 * m["omega"].imag * p.fscale / 1e6),
                phase_speed_m_s=float(p.cs * m["omega"].real / kabs),
                group_speed_m_s=float(v),
                energy_speed_m_s=float(diag["vEx"]),
                energy_speed_y_m_s=float(diag["vEy"]),
                attenuation_dB_per_mm=float(8.686 * alpha / 1000.0),
                attenuation_length_mm=float(1e3 / alpha),
                K_spatial_real=float(ksp.real), K_spatial_imag=float(ksp.imag),
                modal_power=float(diag["Px"]), modal_energy=float(diag["energy"]),
                dissipation_balance=float(diag["balance"]),
                mass_MAC=float(m.get("MAC", 1.0)),
                maximum_growth=float(m["maximum_growth"]),
            ))
    return rows


# --------------------------------------------------------------------------
# Figure 2 -- carrier density and mobility
# --------------------------------------------------------------------------
N0_VALUES = [1.0e18, 1.5e18, 2.0e18, 2.5e18, 3.0e18]
MU_VALUES = [0.00875, 0.013125, 0.0175, 0.021875, 0.02625]


def fig02() -> list[dict]:
    rows = []
    Ks = np.linspace(0.30, 0.90, 13)
    for parameter, values in (("n0", N0_VALUES), ("mobility", MU_VALUES)):
        for value in values:
            kw = {"n0": value} if parameter == "n0" else {"mobility": value}
            p = plate(0.0, **kw)
            modes = track(p, Ks, operating_mode(p))
            for K, m in zip(Ks, modes):
                diag = p.mode_diagnostics(float(K), KY0, m["omega"], m["q"])
                ksp = spatial_root(p, m["omega"].real, float(K))
                row = dict(parameter=parameter, value_SI=float(value), K=float(K),
                           ky=KY0,
                           frequency_GHz=float(m["omega"].real * p.fscale / 1e9),
                           FWHM_MHz=float(-2 * m["omega"].imag * p.fscale / 1e6),
                           energy_speed_m_s=float(diag["vEx"]),
                           attenuation_dB_per_mm=float(8.686 * 2 * abs(ksp.imag) / p.d / 1000),
                           status="computed", error="")
                try:
                    res, _ = p.edge(KY0, m["omega"].real, float(K), KB0)
                    kb = complex(res["backward_K"])
                    R2 = float(res["backward_reflection_self_power"])
                    row.update(
                        R_B_2um=R2,
                        R_B_edge=isolated_transfer(R2, kb, p.d, 0.0),
                        angle_deg=float(res["reflected_angle_deg"]),
                        edge_scaled_residual=float(res["edge_scaled_residual"]),
                        power_balance_error=float(res["power_balance_relative"]),
                    )
                    row["valid"] = certified_backward(
                        R2, float(res["reflected_angle_deg"]),
                        float(res["power_balance_relative"]),
                        float(res["edge_scaled_residual"]))
                except Exception as exc:            # noqa: BLE001 - failure is data
                    row.update(R_B_2um=None, R_B_edge=None, angle_deg=None,
                               edge_scaled_residual=None,
                               power_balance_error=None, valid=False,
                               status="edge solve failed", error=type(exc).__name__)
                rows.append(row)
    return rows


# --------------------------------------------------------------------------
# Figure 3 -- plate thickness and gradient length
# --------------------------------------------------------------------------
D_VALUES = [120e-9, 160e-9, 200e-9, 250e-9, 320e-9]
ELL_VALUES = [20e-9, 35e-9, 50e-9, 70e-9, 90e-9]


def fig03() -> list[dict]:
    rows = []
    for family, values in (("d", D_VALUES), ("ell", ELL_VALUES)):
        for value in values:
            kw = {"d": value} if family == "d" else {"ell": value}
            p = plate(0.0, **kw)
            Ks = np.linspace(0.10, 1.00, 21) if family == "d" else np.linspace(0.10, 1.00, 21)
            modes = track(p, Ks, operating_mode(p))
            for K, m in zip(Ks, modes):
                rows.append(dict(
                    parameter=family, value_SI=float(value), value_nm=float(value * 1e9),
                    K=float(K), ky=KY0, ell_over_d=float(p.lam),
                    frequency_GHz=float(m["omega"].real * p.fscale / 1e9),
                    FWHM_MHz=float(-2 * m["omega"].imag * p.fscale / 1e6),
                    source="spectral Galerkin, H=0, ky=0.12981",
                ))
    return rows


# --------------------------------------------------------------------------
# Figure 4 -- backward reflection versus frequency
# --------------------------------------------------------------------------
def fig04() -> list[dict]:
    """Backward-channel conversion along the guided branch.

    A fixed-frequency sweep is not well posed here: away from the operating
    point the identified backward port is not a resolved propagating outgoing
    mode, the solved energy angle collapses towards -90 deg and R_B stops being
    a reflectance (values above unity appear).  Instead the drive is swept along
    the *solved guided branch*: for each k_x the incident mode is the tracked
    temporal branch at the true k_y, the backward port stays the same physical
    outgoing mode, and the corresponding real frequency follows from the
    dispersion.  Every row therefore carries a genuine (frequency, wavenumber,
    return, angle, group velocity) tuple.
    """
    rows = []
    Ks = np.linspace(0.30, 0.75, 10)
    for eta in ETAS:
        p = plate(eta)
        modes = track(p, Ks, operating_mode(p))
        omega = np.array([m["omega"].real for m in modes])
        vg = np.gradient(omega, Ks) * p.cs
        for K, m, v in zip(Ks, modes, vg):
            row = dict(eta=float(eta), K=float(K), ky=KY0,
                       frequency_GHz=float(m["omega"].real * p.fscale / 1e9),
                       group_speed_m_s=float(v))
            try:
                res, _ = p.edge(KY0, m["omega"].real, float(K), KB0)
                ki = complex(res["incident_K"])
                kb = complex(res["backward_K"])
                R2 = float(res["backward_reflection_self_power"])
                alpha_b = 2 * abs(kb.imag) / p.d
                alpha_i = 2 * abs(ki.imag) / p.d
                angle = float(res["reflected_angle_deg"])
                row.update(
                    R_B_2um=R2,
                    R_B_edge=float(R2 * np.exp(alpha_b * REF_NORM * p.d)),
                    R_B_100um=float(R2 * np.exp(-alpha_b * (100e-6 - REF_NORM * p.d))),
                    angle_deg=angle,
                    K_incident_real=float(ki.real), K_backward_real=float(kb.real),
                    K_ratio=float(kb.real / ki.real),
                    ImK_backward=float(kb.imag),
                    attenuation_backward_dB_per_mm=float(8.686 * alpha_b / 1000),
                    attenuation_incident_dB_per_mm=float(8.686 * alpha_i / 1000),
                    power_balance_error=float(res["power_balance_relative"]),
                    edge_scaled_residual=float(res["edge_scaled_residual"]),
                )
                row["certified"] = certified_backward(
                    R2, angle, float(res["power_balance_relative"]),
                    float(res["edge_scaled_residual"]))
                row["error"] = ""
            except Exception as exc:              # noqa: BLE001
                row.update(R_B_edge=None, R_B_2um=None, R_B_100um=None,
                           angle_deg=None, certified=False,
                           power_balance_error=None, edge_scaled_residual=None,
                           error=type(exc).__name__)
            rows.append(row)
    return rows


# --------------------------------------------------------------------------
# Figure 5 -- channel power accounting
# --------------------------------------------------------------------------
def certified_backward(R2, angle_deg, balance, residual) -> bool:
    """Single scientific acceptance rule for the isolated backward channel.

    A ``R_B`` value is only a physically interpretable return fraction while the
    backward port is a resolved, propagating outgoing mode.  When the solved
    energy angle collapses towards -90 deg the backward mode carries almost no
    x-directed flux and the ratio R_B = |a|^2 P_B / P_i stops being a reflectance
    (values above unity appear).  Such rows are recorded but not plotted.
    """
    if R2 is None or angle_deg is None or balance is None or residual is None:
        return False
    return bool(0.0 <= R2 <= 1.0 and abs(angle_deg) < 80.0
                and balance < 1e-6 and residual < 1e-8)


PROPAGATING_TOL = 1e-3      # |Im K| <= 1e-3  <=>  attenuation length >= 200 um


def fig05() -> list[dict]:
    rows = []
    for eta in ETAS:
        p = plate(eta)
        res, sol = p.edge(KY0, OMEGA0, K0, KB0)
        K = np.array([complex(v) for v in sol["K"]])
        amp = np.array([complex(v) for v in sol["amplitudes"]])
        power = np.array([p.power(sol["Y"][:, j], OMEGA0) for j in range(len(K))])
        flux = power * np.abs(amp) ** 2                    # at the edge plane
        inc = float(res["incident_power_left"])
        propagate = np.abs(K.imag) <= PROPAGATING_TOL
        ib = int(np.argmin(np.abs(K - complex(res["backward_K"]))))
        kb = complex(res["backward_K"])
        alpha_b = 2 * abs(kb.imag) / p.d
        R2 = float(res["backward_reflection_self_power"])
        evanescent_mag = float(np.sum(np.abs(flux[~propagate])) / inc)
        rows.append(dict(
            eta=float(eta),
            R_B_2um=R2,
            R_B_edge=float(R2 * np.exp(alpha_b * REF_NORM * p.d)),
            incident_self_power=inc,
            backward_propagating_fraction=float(-flux[ib] / inc),
            forward_propagating_fraction=float(np.sum(flux[propagate & (flux > 0)]) / inc),
            evanescent_reactive_fraction=evanescent_mag,
            total_outgoing_fraction=float(-np.sum(flux) / inc),
            dissipated_fraction=float(res["dissipation_control_volume"] / inc),
            propagating_mode_count=int(np.sum(propagate)),
            evanescent_mode_count=int(np.sum(~propagate)),
            outgoing_modes=int(len(K)),
            negative_power_mode_count=int(np.sum(power < 0)),
            rb_degree_uncertainty=float(1e-6 * R2),
            power_balance_error=float(res["power_balance_relative"]),
        ))
    return rows


# --------------------------------------------------------------------------
# Figure 6 -- propagation distance, survival and attenuation lengths
# --------------------------------------------------------------------------
def fig06() -> list[dict]:
    rows = []
    distances_um = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    for eta in ETAS:
        p = plate(eta)
        res, _ = p.edge(KY0, OMEGA0, K0, KB0)
        ki = complex(res["incident_K"])
        kb = complex(res["backward_K"])
        R2 = float(res["backward_reflection_self_power"])
        alpha_i = 2 * abs(ki.imag) / p.d
        alpha_b = 2 * abs(kb.imag) / p.d
        for distance_um in distances_um:
            ell = distance_um * 1e-6
            rows.append(dict(
                eta=float(eta), distance_um=float(distance_um), distance_um_norm=ell / p.d,
                R_B_isolated=float(R2 * np.exp(-alpha_b * (ell - REF_NORM * p.d))),
                incident_survival=float(np.exp(-alpha_i * ell)),
                backward_attenuation_dB_per_mm=float(8.686 * alpha_b / 1000),
                incident_attenuation_dB_per_mm=float(8.686 * alpha_i / 1000),
                attenuation_length_incident_mm=float(1e3 / alpha_i),
                attenuation_length_backward_mm=float(1e3 / alpha_b),
                power_balance_error=float(res["power_balance_relative"]),
            ))
    return rows


# --------------------------------------------------------------------------
# Figure 7 -- two-parameter (ky, H) landscape
# --------------------------------------------------------------------------
KY_SWEEP = np.linspace(0.05, 0.20, 19)


def fig07() -> list[dict]:
    rows = []
    for eta in ETAS:
        p = plate(eta)
        for ky in KY_SWEEP:
            row = dict(eta=float(eta), ky=float(ky),
                       frequency_GHz=float(OMEGA0 * p.fscale / 1e9))
            try:
                res, _ = p.edge(float(ky), OMEGA0, K0, KB0)
                kb = complex(res["backward_K"])
                R2 = float(res["backward_reflection_self_power"])
                alpha_b = 2 * abs(kb.imag) / p.d
                back = res["backward"]
                row.update(
                    R_B_2um=R2,
                    R_B_edge=float(R2 * np.exp(alpha_b * REF_NORM * p.d)),
                    angle_deg=float(res["reflected_angle_deg"]),
                    Px_backward=float(back["Px"] / res["incident"]["Px"]),
                    Py_backward=float(back["Py"] / res["incident"]["Px"]),
                    vEx_backward=float(back["vEx"]),
                    edge_scaled_residual=float(res["edge_scaled_residual"]),
                    power_balance_error=float(res["power_balance_relative"]),
                    valid=certified_backward(
                        R2, float(res["reflected_angle_deg"]),
                        float(res["power_balance_relative"]),
                        float(res["edge_scaled_residual"])),
                    error="")
            except Exception as exc:              # noqa: BLE001
                row.update(valid=False, R_B_2um=None, R_B_edge=None, angle_deg=None,
                           Px_backward=None, Py_backward=None, vEx_backward=None,
                           edge_scaled_residual=None, power_balance_error=None,
                           error=type(exc).__name__)
            rows.append(row)
    # relative coupling-induced change with respect to H=0 at the same ky
    base = {r["ky"]: r["R_B_2um"] for r in rows
            if r["eta"] == 0.0 and r["R_B_2um"] is not None}
    for r in rows:
        ref = base.get(r["ky"])
        if r["R_B_2um"] is not None and ref:
            r["rel_change_percent"] = 100.0 * (r["R_B_2um"] - ref) / ref
        else:
            r["rel_change_percent"] = None
    return rows


# --------------------------------------------------------------------------
# Figure 8 -- thickness-resolved energy flux of the guided channels
# --------------------------------------------------------------------------
def fig08() -> dict:
    """Thickness profile of the signed energy flux of both guided channels.

    Replaces the grounded-versus-open comparison: the open-circuit edge problem
    is not certified (see ``audit/open_circuit_diagnostic.json``).
    """
    z = None
    profiles = []
    for eta in ETAS:
        p = plate(eta)
        res, sol = p.edge(KY0, OMEGA0, K0, KB0)
        ib = int(np.argmin(
            np.abs(np.array([complex(v) for v in sol["K"]]) - complex(res["backward_K"]))))
        if z is None:
            z = p.z.copy()
            z = 0.5 + z            # z in [0,1] across the thickness, 0 = lower face
        qi = sol["incident"]["q"]
        qb = sol["Y"][: p.nw, ib]
        pi = power_profile(p, complex(sol["incident"]["K"]), KY0, OMEGA0, qi)
        pb = power_profile(p, complex(sol["K"][ib]), KY0, OMEGA0, qb)
        # Calibrate each z-profile so that its thickness integral reproduces the
        # modal self-power returned by the solver (which carries the natural
        # corner/face correction terms).  This keeps the plotted distribution
        # quantitatively consistent with R_B instead of silently rescaling it.
        for prof, state in ((pi, sol["incident"]["y"]), (pb, sol["Y"][:, ib])):
            target = float(p.power(state, OMEGA0))
            integ = float(np.sum(p.weights * prof["x"]))
            prof["x"] *= target / integ if integ else 0.0
            prof["z"] *= target / integ if integ else 0.0
        # normalise every quantity by the thickness-integrated incident P_x
        norm = float(np.sum(p.weights * pi["x"]))
        profiles.append(dict(
            eta=float(eta),
            z=z,
            incident_Px=pi["x"] / norm,
            incident_Pz=pi["z"] / norm,
            backward_Px=pb["x"] * abs(res["backward_amplitude"]) ** 2 / norm,
            backward_Pz=pb["z"] * abs(res["backward_amplitude"]) ** 2 / norm,
            weight=p.weights.copy(),
            backward_total=float(np.sum(p.weights * pb["x"]) * abs(res["backward_amplitude"]) ** 2 / norm),
            incident_total=float(np.sum(p.weights * pi["x"]) / norm),
        ))
    rows = []
    for prof in profiles:
        for zz, ix, iz, bx, bz, w in zip(prof["z"], prof["incident_Px"],
                                        prof["incident_Pz"], prof["backward_Px"],
                                        prof["backward_Pz"], prof["weight"]):
            rows.append(dict(eta=prof["eta"], z=float(zz), quadrature_weight=float(w),
                             incident_Px=float(ix), incident_Pz=float(iz),
                             backward_Px=float(bx), backward_Pz=float(bz)))
    dump_csv("fig08_thickness_flux.csv", rows)
    return dict(n_profiles=len(profiles),
                backward_total={str(p["eta"]): p["backward_total"] for p in profiles},
                incident_total={str(p["eta"]): p["incident_total"] for p in profiles})


# --------------------------------------------------------------------------
# Figure 9 -- discretisation study and temporal/spatial consistency
# --------------------------------------------------------------------------
def fig09() -> list[dict]:
    degrees = [14, 17, 18, 22, 25, 26, 33]
    rows = []
    for degree in degrees:
        p = Plate(degree=degree)
        res, _ = p.edge(KY0, OMEGA0, K0, KB0)
        kb = complex(res["backward_K"])
        rows.append(dict(
            degree=int(degree),
            basis_degree=int(degree),
            quadrature_order=int(max(64, 2 * degree + 10)),
            R_B=float(res["backward_reflection_self_power"]),
            K_B_real=float(kb.real), K_B_imag=float(kb.imag),
            edge_scaled_residual=float(res["edge_scaled_residual"]),
            power_error=float(res["power_balance_relative"]),
            outgoing_modes=int(res["outgoing_modes"]),
        ))
    ref = max(rows, key=lambda r: r["degree"])
    for r in rows:
        r["R_B_rel_error"] = abs(r["R_B"] - ref["R_B"]) / abs(ref["R_B"])
        r["K_B_rel_error"] = abs(complex(r["K_B_real"], r["K_B_imag"])
                                 - complex(ref["K_B_real"], ref["K_B_imag"])) \
            / abs(complex(ref["K_B_real"], ref["K_B_imag"]))
        r["is_reference"] = bool(r["degree"] == ref["degree"])
    return rows


def fig09_consistency() -> list[dict]:
    """Temporal versus spatial eigenproblem dispersion consistency."""
    rows = []
    p = Plate(degree=DEGREE)
    Ks = np.linspace(0.30, 1.00, 11)
    modes = track(p, Ks, operating_mode(p))
    for K, m in zip(Ks, modes):
        ksp = spatial_root(p, m["omega"].real, float(K))
        rows.append(dict(
            K=float(K), ky=KY0,
            frequency_GHz=float(m["omega"].real * p.fscale / 1e9),
            omega_imag=float(m["omega"].imag),
            K_temporal_real=float(K), K_spatial_real=float(ksp.real),
            K_spatial_imag=float(ksp.imag),
            abs_K_mismatch=float(abs(complex(K, 0.0) - ksp)),
            rel_K_mismatch=float(abs(complex(K, 0.0) - ksp) / abs(ksp)),
        ))
    return rows


# --------------------------------------------------------------------------
# Figure 10 -- solved field maps and energy-flux directions
# --------------------------------------------------------------------------
def fig10() -> dict:
    p = Plate(degree=DEGREE)
    ky_nodes = np.linspace(KY0 - 0.05, KY0 + 0.05, 9)
    width = 0.022
    weights = np.exp(-0.5 * ((ky_nodes - KY0) / width) ** 2)
    weights /= weights.sum()

    x_um = np.linspace(-60.0, 0.0, 151)
    y_um = np.linspace(-45.0, 45.0, 151)
    x = x_um * 1e-6
    y = y_um * 1e-6

    beams = []
    for kyn, wgt in zip(ky_nodes, weights):
        res, sol = p.edge(float(kyn), OMEGA0, K0, KB0)
        K = np.array([complex(v) for v in sol["K"]])
        amp = np.array([complex(v) for v in sol["amplitudes"]])
        ib = int(np.argmin(np.abs(K - complex(res["backward_K"]))))
        beams.append(dict(ky=float(kyn), weight=float(wgt),
                          Ki=complex(sol["incident"]["K"]),
                          Ui=sol["incident"]["q"][: p.nu],
                          Kb=K[ib], Ub=sol["Y"][: p.nu, ib],
                          flux=np.array([abs(amp[ib]) ** 2])))

    b = p.b
    zvals = p.z
    def comps(q):
        u = q.reshape(3, p.n)
        return np.stack([b[0] @ u[i] for i in range(3)], axis=1)   # (nz,3)

    nz = len(zvals)
    I_inc = np.zeros((len(y_um), len(x_um)))
    I_bwd = np.zeros_like(I_inc)
    I_tot = np.zeros_like(I_inc)
    for xi, xv in enumerate(x_um):
        acc_i = np.zeros((len(beams), nz, 3), complex)
        acc_b = np.zeros((len(beams), nz, 3), complex)
        for j, bm in enumerate(beams):
            acc_i[j] = np.exp(1j * bm["Ki"] * (xv * 1e-6 / p.d)) * comps(bm["Ui"])
            acc_b[j] = (bm["flux"][0] ** 0.5
                        * np.exp(1j * bm["Kb"] * (xv * 1e-6 / p.d)) * comps(bm["Ub"]))
        w = np.array([bm["weight"] for bm in beams])
        kyn = np.array([bm["ky"] for bm in beams])
        for acc, target in ((acc_i, I_inc), (acc_b, I_bwd)):
            # coherent ky superposition: M_jj' = int dz  w_j w_j'* a_j(z) a_j'(z)*
            M = np.zeros((len(beams), len(beams)), complex)
            for j in range(len(beams)):
                for jp in range(len(beams)):
                    M[j, jp] = np.sum(p.weights[:, None] * acc[j].conj() * acc[jp])
            phase = np.exp(1j * (kyn[None, :] - kyn[:, None])[None, :, :] * (y_um[:, None, None] * 1e-6 / p.d))
            block = np.einsum("y jp,jp->y", phase, (w[:, None] * w[None, :].conj()) * M)
            target[:, xi] = block.real
        # total field = incident + backward channel
        acc_t = acc_i + acc_b
        M = np.zeros((len(beams), len(beams)), complex)
        for j in range(len(beams)):
            for jp in range(len(beams)):
                M[j, jp] = np.sum(p.weights[:, None] * acc_t[j].conj() * acc_t[jp])
        phase = np.exp(1j * (kyn[None, :] - kyn[:, None])[None, :, :] * (y_um[:, None, None] * 1e-6 / p.d))
        I_tot[:, xi] = np.einsum("y jp,jp->y", phase, (w[:, None] * w[None, :].conj()) * M).real
    # identical normalisation for (a) and (b): incident peak
    scale = float(np.abs(I_inc).max())
    if not np.isfinite(scale) or scale <= 0:
        raise RuntimeError("field normalisation failed")
    rows = []
    for iy, yv in enumerate(y_um):
        for ix, xv in enumerate(x_um):
            rows.append(dict(x_um=float(xv), y_um=float(yv),
                             incident_intensity=float(I_inc[iy, ix] / scale),
                             backward_intensity=float(I_bwd[iy, ix] / scale),
                             total_intensity=float(I_tot[iy, ix] / scale)))
    dump_csv("fig10_field_maps.csv", rows)

    # solved flux / centroid metrics at the two reference planes
    metrics = []
    for plane in (-2.0, -40.0):
        ix = int(np.argmin(np.abs(x_um - plane)))
        def centroid(col):
            wcol = np.maximum(col, 0)
            return float(np.sum(y_um * wcol) / max(np.sum(wcol), 1e-300))
        metrics.append(dict(
            plane_um=float(plane),
            incident_centroid_y_um=centroid(I_inc[:, ix]),
            backward_centroid_y_um=centroid(I_bwd[:, ix]),
            incident_peak=float(I_inc[:, ix].max() / scale),
            backward_peak=float(I_bwd[:, ix].max() / scale),
        ))
    res, _ = p.edge(KY0, OMEGA0, K0, KB0)
    payload = dict(
        solver="paper_a_study/model.py Plate.edge (spectral Galerkin + edge matching)",
        coordinate_convention="plate x<0, edge at x=0, incident Re kx>0 and Px>0, "
                              "backward channel Px<0 and Py<0",
        normalisation="both intensity maps divided by the incident peak intensity",
        ky_quadrature=dict(nodes=[float(k) for k in ky_nodes], width=float(width),
                           weights=[float(w) for w in weights]),
        percentages=metrics,
        primary_flux=dict(
            incident_Px=float(res["incident"]["Px"]), incident_Py=float(res["incident"]["Py"]),
            backward_Px=float(res["backward"]["Px"]), backward_Py=float(res["backward"]["Py"]),
            incident_angle_deg=float(res["incident_angle_deg"]),
            reflected_angle_deg=float(res["reflected_angle_deg"]),
            incident_vEx=float(res["incident"]["vEx"]),
            backward_vEx=float(res["backward"]["vEx"]),
            backward_vEy=float(res["backward"]["vEy"]),
        ),
    )
    dump_json("fig10_field_metrics.json", payload)
    return payload


# --------------------------------------------------------------------------
def main() -> None:
    import time
    DATA.mkdir(parents=True, exist_ok=True)
    log = {}

    def run(tag, fn):
        t0 = time.time()
        print(f"[build] {tag} ...", flush=True)
        result = fn()
        log[tag] = round(time.time() - t0, 2)
        print(f"[build] {tag} done in {log[tag]}s", flush=True)
        return result

    rows = run("fig01", fig01)
    dump_csv("fig01_dispersion_velocity_attenuation.csv", rows)
    rows = run("fig02", fig02)
    dump_csv("fig02_material_parameter_sweep.csv", rows)
    rows = run("fig03", fig03)
    dump_csv("fig03_geometry_sweep.csv", rows)
    rows = run("fig04", fig04)
    dump_csv("fig04_frequency_reflection.csv", rows)
    rows = run("fig05", fig05)
    dump_csv("fig05_channel_power.csv", rows)
    rows = run("fig06", fig06)
    dump_csv("fig06_attenuation_distance.csv", rows)
    rows = run("fig07", fig07)
    dump_csv("fig07_coupling_sensitivity.csv", rows)
    info = run("fig08", fig08)
    rows = run("fig09", fig09)
    dump_csv("fig09_validation_convergence.csv", rows)
    rows = run("fig09_consistency", fig09_consistency)
    dump_csv("fig09_temporal_spatial_consistency.csv", rows)
    payload = run("fig10", fig10)
    dump_json("build_log.json", dict(timings_s=log, figure8=info,
                                     degree=DEGREE, H_crit_T=HCRIT,
                                     ky0=KY0, omega0=OMEGA0))
    print("[build] all datasets written to", DATA)


if __name__ == "__main__":
    main()
