"""SUPERSEDED (round 11, finding D25) --- do not run in the delivered tree.

This script writes the *same file names* as ``build_figure_data.py`` but with an
older, 14-column schema (no ``ky``, no ``attenuation_dB_per_mm``, no
``K_spatial_*``).  Running it replaces the delivered datasets with data the
figures cannot read and the manuscript does not describe.  The delivered
datasets are produced by::

    python paper_a_study/build_figure_data.py

Setting ``PAPER_A_ALLOW_LEGACY_REGENERATION=1`` re-enables this script for the
legacy figures of ``generate_revised_figures.py`` only.

Regenerate revised publication datasets for Paper A.

The earlier numerical pipeline contained four bookkeeping errors that are fixed
here:

- energy velocity was replaced by ``|omega|/|k|`` instead of the physical ratio
  of thickness-integrated power to thickness-integrated energy;
- finite-distance transfer was reported as an incident survival factor that could
  exceed unity, instead of an isolated self-flux transfer;
- channel power accounting mixed positive and negative self-powers and could
  produce an infinite fraction;
- open-boundary failures were represented by empty cells instead of an explicit
  error status.

The script writes intermediate CSV/JSON data before any rendering is performed.
Rendering is intentionally separated into
``paper_a_study/generate_revised_figures.py``.
"""
from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import numpy as np
from numpy.polynomial.hermite import hermgauss

from paper_a_study.model import Plate

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "paper_a_study" / "figure_data"
RESULTS = ROOT / "paper_a_study" / "results"
DEGREE = 22
HCRIT = 4.0097064373759543e-22
KY0 = 0.12981175031447484
OMEGA0 = 7.633372404423294
K0 = 0.7361990195318475
KB0 = 0.2451746921716515
ETAS = [-0.05, -0.025, 0.0, 0.025, 0.05]
ETAS7 = [-0.05, 0.0, 0.05]


def dump_json(name: str, data) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / name).write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


def dump_csv(name: str, rows) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    with (DATA / name).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def scalar(value):
    if isinstance(value, dict):
        return {key: scalar(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [scalar(item) for item in value]
    if np.iscomplexobj(value):
        return {"real": float(np.real(value)), "imag": float(np.imag(value))}
    return float(value)


def incident_reference(plate: Plate, K0: float):
    """Select the positive-frequency guided temporal branch at source K0."""
    modes = plate.temporal(K0)
    if not modes:
        raise RuntimeError("no temporal modes at reference K")
    if OMEGA0 <= 0:
        raise RuntimeError("nonpositive primary omega")
    options = [
        mode
        for mode in modes
        if mode["omega"].real > 0
        and np.vdot(mode["U"], plate.M @ mode["U"]).real > 0
    ]
    if not options:
        raise RuntimeError("no positive-energy temporal modes")
    return min(options, key=lambda mode: abs(mode["omega"].real - OMEGA0))


def cutoff_reference(plate: Plate, Kguess=0.25):
    """Lowest positive-frequency guided temporal mode used as a sweep seed."""
    modes = plate.temporal(float(Kguess))
    options = [
        mode
        for mode in modes
        if mode["omega"].real > 7.0
        and np.vdot(
            mode["U"][2 * plate.n :], plate.W @ mode["U"][2 * plate.n :]
        ).real > 0.85
    ]
    if not options:
        raise RuntimeError("no guided cutoff mode found")
    return min(options, key=lambda mode: mode["omega"].real)


def track_mode(plate: Plate, K: float, reference):
    mode = plate.temporal(float(K), reference)
    if mode["omega"].real <= 0:
        raise RuntimeError(f"nonpositive frequency at K={K:.6g}")
    return mode


def primary_dispersion(plate: Plate, eta: float) -> dict:
    reference = incident_reference(plate, K0)
    rows = []
    Ks = np.linspace(0.10, 1.05, 25)
    mode = reference
    for K in Ks:
        mode = track_mode(plate, float(K), mode)
        wavenumber = np.sqrt(complex(K) ** 2 + KY0**2)
        phase = mode["omega"].real * wavenumber.real
        group = plate.cs * mode["omega"].real * K / abs(wavenumber) ** 3
        diag = plate.mode_diagnostics(float(K), KY0, mode["omega"], mode["q"])
        power = 2.0 * diag["Px"]
        energy = diag["energy"]
        if energy <= 0:
            raise RuntimeError(f"nonpositive modal energy at K={K:.6g}")
        energy_velocity = plate.cs * power / energy
        rows.append(
            {
                "eta": float(eta),
                "K": float(K),
                "frequency_GHz": float(mode["omega"].real * plate.fscale / 1e9),
                "omega_real": float(mode["omega"].real),
                "omega_imag": float(mode["omega"].imag),
                "FWHM_MHz": float(-2 * mode["omega"].imag * plate.fscale / 1e6),
                "phase_speed_m_s": float(phase),
                "group_speed_m_s": float(group),
                "energy_speed_m_s": float(energy_velocity),
                "attenuation_dB_m": float(-8.686 * float(np.imag(wavenumber))),
                "modal_power": power,
                "modal_energy": energy,
                "mass_MAC": float(mode["MAC"]),
                "maximum_growth": float(mode["maximum_growth"]),
            }
        )
    return {"eta": float(eta), "rows": rows}


def material_dispersion(plate: Plate, parameter: str, value: float) -> dict:
    reference = cutoff_reference(plate)
    rows = []
    Ks = np.linspace(0.20, 0.90, 13)
    mode = reference
    for K in Ks:
        mode = track_mode(plate, float(K), mode)
        diag = plate.mode_diagnostics(float(K), KY0, mode["omega"], mode["q"])
        rows.append(
            {
                "parameter": parameter,
                "value_SI": float(value),
                "K": float(K),
                "cutoff_frequency_GHz": float(reference["omega"].real * plate.fscale / 1e9),
                "frequency_GHz": float(mode["omega"].real * plate.fscale / 1e9),
                "attenuation_dB_m": float(
                    -8.686 * np.imag(np.sqrt(complex(K) ** 2 + KY0**2))
                ),
                "modal_power": 2.0 * diag["Px"],
                "modal_energy": diag["energy"],
            }
        )
        try:
            edge, _ = plate.edge(KY0, mode["omega"], float(K), float(K))
            rows[-1]["R_B_2um"] = float(edge["backward_reflection_self_power"])
            rows[-1]["edge_scaled_residual"] = float(edge["edge_scaled_residual"])
            rows[-1]["error"] = ""
        except Exception as exc:  # noqa: BLE001 - failures are data, not crashes.
            rows[-1]["R_B_2um"] = None
            rows[-1]["edge_scaled_residual"] = None
            rows[-1]["error"] = type(exc).__name__
    return {"rows": rows}


def geometry_dispersion(plate: Plate, parameter: str, value: float) -> dict:
    reference = cutoff_reference(plate)
    rows = []
    Ks = np.linspace(0.10, 1.00, 17) if parameter == "d" else np.linspace(0.05, 1.00, 19)
    mode = reference
    for K in Ks:
        mode = track_mode(plate, float(K), mode)
        rows.append(
            {
                "parameter": parameter,
                "value_SI": float(value),
                "K": float(K),
                "cutoff_frequency_GHz": float(reference["omega"].real * plate.fscale / 1e9),
                "frequency_GHz": float(mode["omega"].real * plate.fscale / 1e9),
                "gradient_length_ratio": float(plate.lam),
            }
        )
    return {"rows": rows}


def edge_reference(plate: Plate):
    reference = incident_reference(plate, K0)
    return plate.edge(KY0, OMEGA0, K0, KB0)[0], reference


def channel_accounting(plate: Plate, eta: float) -> dict:
    result, _ = edge_reference(plate)
    solution = plate.edge(KY0, OMEGA0, K0, KB0)[1]
    K = np.array([complex(value) for value in solution["K"]])
    amplitudes = np.array([complex(value) for value in solution["amplitudes"]])
    powers = np.array([plate.power(solution["Y"][:, j], OMEGA0) for j in range(len(K))])
    distance = result["reference_distance_m"] / plate.d
    flux = powers * np.abs(amplitudes) ** 2 * np.exp(2 * K.imag * distance)
    incident = float(result["incident_power_left"])
    positive = flux[flux > 0]
    negative = flux[flux < 0]
    primary_kb = complex(result["backward_K"])
    backward_idx = int(np.argmin(np.abs(K - primary_kb)))
    return {
        "eta": float(eta),
        "R_B_2um": float(result["backward_reflection_self_power"]),
        "R_B_isolated_transfer": float(
            result["backward_reflection_self_power"]
            * np.exp(
                2
                * (K[backward_idx].imag - complex(result["incident_K"]).imag)
                * distance
            )
        ),
        "incident_self_power": incident,
        "forward_self_flux": float(positive.sum()),
        "backward_self_flux": float(-negative.sum()),
        "total_outgoing_self_flux": float(positive.sum() - negative.sum()),
        "forward_fraction": float(positive.sum() / max(incident, 1e-30)),
        "backward_fraction": float(-negative.sum() / max(incident, 1e-30)),
        "total_outgoing_fraction": float(
            (positive.sum() - negative.sum()) / max(incident, 1e-30)
        ),
        "negative_power_mode_count": int(np.sum(powers < 0)),
        "positive_power_mode_count": int(np.sum(powers > 0)),
        "outgoing_modes": int(result["outgoing_modes"]),
        "power_balance_error": float(result["power_balance_relative"]),
    }


def attenuation_transfer(plate: Plate, eta: float) -> dict:
    result, _ = edge_reference(plate)
    ki = complex(result["incident_K"])
    kb = complex(result["backward_K"])
    R0 = float(result["backward_reflection_self_power"])
    rows = []
    distances_um = np.array([1, 5, 10, 20, 50, 100, 200, 500, 1000])
    for distance_um in distances_um:
        distance_m = distance_um * 1e-6
        rows.append(
            {
                "eta": float(eta),
                "distance_um": float(distance_um),
                "R_B_2um": R0,
                "R_B_isolated_transfer": float(
                    R0
                    * np.exp(2 * (kb.imag - ki.imag) * distance_m / plate.d)
                ),
                "incident_self_flux": float(np.exp(2 * ki.imag * distance_m / plate.d)),
                "backward_self_flux": float(
                    -float(result["backward"]["Px"])
                    * np.exp(2 * abs(kb.imag) * distance_m / plate.d)
                ),
                "attenuation_backward_dB_m": float(-8.686 * kb.imag),
                "attenuation_incident_dB_m": float(-8.686 * ki.imag),
                "power_balance_error": float(result["power_balance_relative"]),
            }
        )
    return {"rows": rows}


def ky_sweep(plate: Plate, eta: float) -> dict:
    rows = []
    for ky in np.linspace(0.05, 0.20, 13):
        try:
            result, _ = plate.edge(float(ky), OMEGA0, K0, KB0)
            ki = complex(result["incident_K"])
            kb = complex(result["backward_K"])
            rows.append(
                {
                    "eta": float(eta),
                    "ky": float(ky),
                    "frequency_GHz": float(OMEGA0 * plate.fscale / 1e9),
                    "R_B_edge": float(
                        result["backward_reflection_self_power"]
                        * np.exp(
                            2
                            * (ki.imag - kb.imag)
                            * result["reference_distance_m"]
                            / plate.d
                        )
                    ),
                    "R_B_2um": float(result["backward_reflection_self_power"]),
                    "angle_deg": float(result["reflected_angle_deg"]),
                    "edge_scaled_residual": float(result["edge_scaled_residual"]),
                    "power_balance_error": float(result["power_balance_relative"]),
                    "error": "",
                }
            )
        except Exception as exc:  # noqa: BLE001
            rows.append(
                {
                    "eta": float(eta),
                    "ky": float(ky),
                    "frequency_GHz": float(OMEGA0 * plate.fscale / 1e9),
                    "R_B_edge": None,
                    "R_B_2um": None,
                    "angle_deg": None,
                    "edge_scaled_residual": None,
                    "power_balance_error": None,
                    "error": type(exc).__name__,
                }
            )
    return {"rows": rows}


def boundary_sweep() -> dict:
    rows = []
    for electric in ("ground", "open"):
        for eta in (-0.05, 0.0, 0.05):
            plate = Plate(degree=DEGREE, H=float(eta) * HCRIT, electric=electric)
            try:
                result, _ = plate.edge(KY0, OMEGA0, K0, KB0)
                rows.append(
                    {
                        "electric": electric,
                        "eta": float(eta),
                        "frequency_GHz": float(OMEGA0 * plate.fscale / 1e9),
                        "R_B_2um": float(result["backward_reflection_self_power"]),
                        "angle_deg": float(result["reflected_angle_deg"]),
                        "edge_scaled_residual": float(result["edge_scaled_residual"]),
                        "power_balance_error": float(result["power_balance_relative"]),
                        "error": "",
                    }
                )
            except Exception as exc:  # noqa: BLE001
                rows.append(
                    {
                        "electric": electric,
                        "eta": float(eta),
                        "frequency_GHz": None,
                        "R_B_2um": None,
                        "angle_deg": None,
                        "edge_scaled_residual": None,
                        "power_balance_error": None,
                        "error": type(exc).__name__,
                    }
                )
    return {"rows": rows}


def convergence_sweep() -> dict:
    rows = []
    for degree in (14, 18, 22, 26):
        plate = Plate(degree=degree)
        result, _ = plate.edge(KY0, OMEGA0, K0, KB0)
        kb = complex(result["backward_K"])
        rows.append(
            {
                "method": "Legendre",
                "resolution": int(degree),
                "R_B": float(result["backward_reflection_self_power"]),
                "K_B_real": float(kb.real),
                "K_B_imag": float(kb.imag),
                "edge_scaled_residual": float(result["edge_scaled_residual"]),
                "power_error": float(result["power_balance_relative"]),
            }
        )
    for elements in (8, 12, 16, 20, 24):
        degree = 2 * elements + 1
        plate = Plate(degree=degree)
        result, _ = plate.edge(KY0, OMEGA0, K0, KB0)
        kb = complex(result["backward_K"])
        rows.append(
            {
                "method": "spectral p=2n+1",
                "resolution": int(degree),
                "R_B": float(result["backward_reflection_self_power"]),
                "K_B_real": float(kb.real),
                "K_B_imag": float(kb.imag),
                "edge_scaled_residual": float(result["edge_scaled_residual"]),
                "power_error": float(result["power_balance_relative"]),
            }
        )
    return {"rows": rows}


def field_metrics() -> dict:
    plate = Plate(degree=DEGREE)
    result, solution = plate.edge(KY0, OMEGA0, K0, KB0)
    x_um = np.linspace(-80, 0, 241)
    y_um = np.linspace(-70, 30, 181)
    x = x_um * 1e-6
    y = y_um * 1e-6
    xd = x / plate.d
    yd = y / plate.d
    XX, YY = np.meshgrid(xd, yd)
    t, weights = hermgauss(25)
    kys = KY0 + np.sqrt(2) * 0.013 * t
    ky_weights = weights / np.sqrt(np.pi)
    bz, _ = plate.basis(np.array([0.25]), 0)
    incident_amplitude = np.zeros(len(kys), complex)
    backward_amplitude = np.zeros(len(kys), complex)
    for index, (ky, weight) in enumerate(zip(kys, ky_weights)):
        result, solution = plate.edge(float(ky), OMEGA0, K0, KB0)
        ib = solution["index_backward"]
        phase = np.exp(
            -1j
            * np.angle(
                (bz[0] @ solution["incident"]["q"][2 * plate.n : 3 * plate.n])[0]
            )
        )
        amp = phase * weight
        incident_amplitude[index] = amp
        backward_amplitude[index] = complex(solution["amplitudes"][ib]) * amp
    Ui = np.stack([solution["incident"]["y"][: plate.nu]] * len(kys), axis=1)
    Ub = np.stack(
        [solution["Y"][: plate.nu, ib] * complex(solution["amplitudes"][ib])]
        * len(kys),
        axis=1,
    )
    Ki = np.full(len(kys), complex(result["incident_K"]))
    Kb = np.full(len(kys), complex(result["backward_K"]))
    powers_i = np.full(len(kys), plate.power(solution["incident"]["y"], OMEGA0))
    powers_b = np.full(len(kys), plate.power(solution["Y"][:, ib], OMEGA0))

    def intensity(U, K, powers):
        exponential = np.exp(
            1j * (K[:, None, None] * XX[None, :, :] + kys[:, None, None] * YY[None, :, :])
        ).reshape(len(K), -1)
        gram = U.conj().T @ plate.M @ U
        return np.maximum(
            np.sum(exponential.conj() * (gram @ exponential), axis=0).real.reshape(XX.shape),
            0,
        )

    incident_intensity = intensity(Ui, Ki, powers_i)
    backward_intensity = intensity(Ub, Kb, powers_b)
    metrics = []
    for plane, x_plane in (("x=-2 um", -2e-6), ("x=-40 um", -40e-6)):
        j = int(np.argmin(np.abs(x - x_plane)))
        incident_sum = float(np.sum(incident_intensity[:, j]))
        backward_sum = float(np.sum(backward_intensity[:, j]))
        incident_centroid = (
            float(np.sum(y * incident_intensity[:, j]) / incident_sum) if incident_sum else 0.0
        )
        backward_centroid = (
            float(np.sum(y * backward_intensity[:, j]) / backward_sum) if backward_sum else 0.0
        )
        forward_ray = float(np.sum(powers_i * np.exp(-2 * Ki.imag * xd[j])))
        backward_ray = float(
            np.sum(
                np.abs(powers_b * Kb.real)
                / np.abs(Kb)
                * np.exp(2 * np.abs(Kb.imag) * xd[j])
            )
        )
        metrics.append(
            {
                "plane": plane,
                "x_um": float(x_plane * 1e6),
                "incident_centroid_y_um": incident_centroid,
                "backward_centroid_y_um": backward_centroid,
                "incident_sum": incident_sum,
                "backward_sum": backward_sum,
                "forward_ray_fraction": float(
                    forward_ray / max(float(np.sum(powers_i)), 1e-30)
                ),
                "backward_ray_fraction": float(
                    backward_ray
                    / max(float(np.sum(np.abs(powers_b * Kb.real) / np.abs(Kb))), 1e-30)
                ),
            }
        )
    np.save(DATA / "x_um.npy", x_um)
    np.save(DATA / "y_um.npy", y_um)
    np.save(DATA / "ky_sample.npy", kys)
    np.save(DATA / "incident_intensity.npy", incident_intensity)
    np.save(DATA / "backward_intensity.npy", backward_intensity)
    return {"metrics": metrics, "ky_sample": [float(value) for value in kys]}


def main():
    if os.environ.get("PAPER_A_ALLOW_LEGACY_REGENERATION") != "1":
        raise SystemExit(
            "regenerate_revised_data.py is superseded by build_figure_data.py.\n"
            "It writes the same file names with an older 14-column schema and would\n"
            "silently replace the delivered datasets (round-11 finding D25).\n"
            "Use:  python paper_a_study/build_figure_data.py\n"
            "Set PAPER_A_ALLOW_LEGACY_REGENERATION=1 only for the legacy figures.")
    protocol = json.loads((RESULTS / "protocol.json").read_text())
    omin = float(protocol["baseline_minimum_omega"])
    ocut = float(protocol["baseline_cutoff_omega"])
    distance_m = float(protocol["reference_distance_m"])

    dispersion = []
    for eta in ETAS:
        plate = Plate(degree=DEGREE, H=float(eta) * HCRIT)
        dispersion.append(primary_dispersion(plate, eta))
    dump_csv(
        "fig01_dispersion_velocity_attenuation.csv",
        [row for group in dispersion for row in group["rows"]],
    )

    material_rows = []
    for n0 in np.array([1.0e18, 1.5e18, 2.0e18, 2.5e18, 3.0e18]):
        material_rows.extend(
            material_dispersion(Plate(degree=DEGREE, n0=float(n0)), "n0", float(n0))["rows"]
        )
    for mobility in np.array([0.00875, 0.013125, 0.0175, 0.021875, 0.02625]):
        diffusivity = 0.000455 * mobility / 0.0175
        material_rows.extend(
            material_dispersion(
                Plate(
                    degree=DEGREE,
                    mobility=float(mobility),
                    diffusivity=float(diffusivity),
                ),
                "M",
                float(mobility),
            )["rows"]
        )
    dump_csv("fig02_material_parameter_sweep.csv", material_rows)

    geometry_rows = []
    for d in np.array([120e-9, 160e-9, 200e-9, 250e-9, 320e-9]):
        geometry_rows.extend(
            geometry_dispersion(Plate(degree=DEGREE, d=float(d)), "d", float(d))["rows"]
        )
    for ell in np.array([20e-9, 35e-9, 50e-9, 70e-9, 90e-9]):
        geometry_rows.extend(
            geometry_dispersion(Plate(degree=DEGREE, ell=float(ell)), "ell", float(ell))["rows"]
        )
    dump_csv("fig03_geometry_sweep.csv", geometry_rows)

    frequency_rows = []
    for eta in ETAS:
        plate = Plate(degree=DEGREE, H=float(eta) * HCRIT)
        for frac in np.linspace(0.08, 0.92, 19):
            omega = omin + float(frac) * (ocut - omin)
            try:
                result, _ = plate.edge(KY0, omega, K0, KB0)
                ki = complex(result["incident_K"])
                kb = complex(result["backward_K"])
                frequency_rows.append(
                    {
                        "eta": float(eta),
                        "frequency_GHz": float(omega * plate.fscale / 1e9),
                        "R_B_edge": float(
                            result["backward_reflection_self_power"]
                            * np.exp(2 * (ki.imag - kb.imag) * distance_m / plate.d)
                        ),
                        "R_B_2um": float(result["backward_reflection_self_power"]),
                        "R_B_100um": float(
                            result["backward_reflection_self_power"]
                            * np.exp(2 * (kb.imag - ki.imag) * 100e-6 / plate.d)
                        ),
                        "angle_deg": float(result["reflected_angle_deg"]),
                        "power_balance_error": float(result["power_balance_relative"]),
                        "error": "",
                    }
                )
            except Exception as exc:  # noqa: BLE001
                frequency_rows.append(
                    {
                        "eta": float(eta),
                        "frequency_GHz": float(omega * plate.fscale / 1e9),
                        "R_B_edge": None,
                        "R_B_2um": None,
                        "R_B_100um": None,
                        "angle_deg": None,
                        "power_balance_error": None,
                        "error": type(exc).__name__,
                    }
                )
    dump_csv("fig04_frequency_reflection.csv", frequency_rows)

    dump_csv(
        "fig05_channel_power.csv",
        [channel_accounting(Plate(degree=DEGREE, H=float(eta) * HCRIT), eta) for eta in ETAS],
    )
    dump_csv(
        "fig06_attenuation_distance.csv",
        [
            row
            for eta in ETAS
            for row in attenuation_transfer(
                Plate(degree=DEGREE, H=float(eta) * HCRIT), eta
            )["rows"]
        ],
    )
    coupling_rows = []
    for eta in ETAS7:
        coupling_rows.extend(
            ky_sweep(Plate(degree=DEGREE, H=float(eta) * HCRIT), eta)["rows"]
        )
    dump_csv("fig07_coupling_sensitivity.csv", coupling_rows)
    dump_csv("fig08_boundary_sensitivity.csv", boundary_sweep()["rows"])
    dump_csv("fig09_validation_convergence.csv", convergence_sweep()["rows"])
    dump_json("fig10_field_metrics.json", field_metrics()["metrics"])

    primary_rows = []
    for eta in (-0.05, 0.0, 0.05):
        plate = Plate(degree=DEGREE, H=float(eta) * HCRIT)
        result, _ = plate.edge(KY0, OMEGA0, K0, KB0)
        primary_rows.append({key: scalar(value) for key, value in result.items()})
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "primary_edge_revised.json").write_text(
        json.dumps(primary_rows, indent=2, allow_nan=False) + "\n"
    )
    print("Revised numerical datasets complete.")


if __name__ == "__main__":
    main()
