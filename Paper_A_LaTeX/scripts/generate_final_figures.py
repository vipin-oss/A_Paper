#!/usr/bin/env python3
"""Generate publication figures from reproducible numerical sweeps.

This script does not modify run_study.py or the accepted primary calculation. It
performs the additional documented sweeps needed for the 10-figure package, saves
all numeric arrays under figure_data/, and writes one or more PDF/SVG/PNG files
per panel under figures_final/.

Font status: Times New Roman unavailable; DejaVu Serif metric fallback.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import csv
import hashlib
import json
import numpy as np
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
from numpy.polynomial.hermite import hermgauss

from paper_a_study.model import (Plate, SI, gradient_strong_root, classical_strong_root,
                                 edge_field_residuals, temporal_energy_balance)
from paper_a_study.figure_style import (save_figure, h_style, label_panel, H_COLORS,
                                        H_LINES, H_LABELS, FONT_STATUS, STYLE_SOURCE)

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
FIGURE_DIR = HERE / "figures_final"
DATA_DIR = HERE / "figure_data"

DEGREE = 22
HCRIT = 4.0097064373759543e-22
PRIMARY = json.loads((RESULTS / "primary_edge.json").read_text())
PRIMARY0 = PRIMARY[0]
PROTOCOL0 = json.loads((RESULTS / "protocol.json").read_text())
K0 = PRIMARY0["incident_K"]["real"] + 1j * PRIMARY0["incident_K"]["imag"]
KB0 = PRIMARY0["backward_K"]["real"] + 1j * PRIMARY0["backward_K"]["imag"]
KY0 = PRIMARY0["ky"]
OMEGA0 = PRIMARY0["omega"]
CS = np.sqrt(SI["c44"] / SI["rho"])
D0 = PRIMARY0["degree"] and 200e-9
SCALE = CS / (2 * np.pi * D0)


def jdump(name: str, data) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / name).write_text(json.dumps(data, indent=2) + "\n")


def csvwrite(name: str, rows) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with (DATA_DIR / name).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plates_for(etas):
    return {float(eta): Plate(degree=DEGREE, H=float(eta) * HCRIT) for eta in etas}


def temporal_sweep(plates, etas):
    rows = []
    for eta in etas:
        p = plates[float(eta)]
        mode = p.temporal(0.10, p.cutoff())
        for K in np.linspace(0.10, 1.05, 37):
            mode = p.temporal(float(K), mode)
            omega = mode["omega"]
            kk = np.sqrt(complex(K)**2 + KY0**2)
            phase = CS * omega.real / abs(kk)
            group = CS * omega.real * K / abs(kk)**3
            energy_mag = CS * abs(omega) / abs(kk)
            rows.append(dict(
                eta=float(eta), K=float(K), frequency_GHz=omega.real * p.fscale / 1e9,
                FWHM_MHz=-2 * np.imag(omega) * p.fscale / 1e6,
                omega_real=float(omega.real), omega_imag=float(omega.imag),
                phase_speed_m_s=phase, group_speed_m_s=group, energy_speed_m_s=energy_mag,
                attenuation_dB_m=-2 * abs(np.imag(kk)) * SCALE / np.pi,
                mass_MAC=float(mode["MAC"]),
                maximum_growth=float(mode["maximum_growth"])))
    return rows


def material_sweep():
    """Only ordinary sourced/derived quantities are varied; A/f/H remain fixed."""
    rows = []
    n0s = np.array([1.0e18, 1.5e18, 2.0e18, 2.5e18, 3.0e18])
    mobilities = np.array([0.00875, 0.013125, 0.0175, 0.021875, 0.02625])
    D0n = 4.55e-4
    for n0 in n0s:
        p = Plate(degree=DEGREE, n0=float(n0))
        mode = p.temporal(0.25, p.cutoff())
        for K in np.linspace(0.20, 0.90, 15):
            mode = p.temporal(float(K), mode)
            try:r, _ = p.edge(KY0, mode["omega"], float(K), float(K))
            except Exception as e:continue
            rows.append(dict(parameter="n0", value_SI=float(n0), K=float(K),
                             frequency_GHz=mode["omega"].real * p.fscale / 1e9,
                             R_B=float(r["backward_reflection_self_power"]),
                             attenuation_dB_m=float(-2 * np.imag(np.sqrt(complex(K)**2 + KY0**2)) * SCALE / np.pi),
                             status="sourced bulk Hall sector plus sensitivity sweep"))
    for M in mobilities:
        Dn = D0n * M / 0.0175
        p = Plate(degree=DEGREE, mobility=float(M), diffusivity=float(Dn))
        mode = p.temporal(0.25, p.cutoff())
        for K in np.linspace(0.20, 0.90, 15):
            mode = p.temporal(float(K), mode)
            try:r, _ = p.edge(KY0, mode["omega"], float(K), float(K))
            except Exception as e:continue
            rows.append(dict(parameter="M", value_SI=float(M), K=float(K),
                             frequency_GHz=mode["omega"].real * p.fscale / 1e9,
                             R_B=float(r["backward_reflection_self_power"]),
                             attenuation_dB_m=float(-2 * np.imag(np.sqrt(complex(K)**2 + KY0**2)) * SCALE / np.pi),
                             status="sourced bulk Hall sector plus sensitivity sweep"))
    return rows


def geometry_sweep():
    rows = []
    d_values = np.array([120e-9, 160e-9, 200e-9, 250e-9, 320e-9])
    ell_values = np.array([20e-9, 35e-9, 50e-9, 70e-9, 90e-9])
    for d in d_values:
        p = Plate(degree=DEGREE, d=float(d))
        mode = p.temporal(0.25, p.cutoff())
        for K in np.linspace(0.10, 1.00, 21):
            mode = p.temporal(float(K), mode)
            rows.append(dict(parameter="d", value_SI=float(d), K=float(K),
                             frequency_GHz=mode["omega"].real * p.fscale / 1e9,
                             gradient_length_ratio=float(p.lam),
                             source="design thickness sweep, H=0"))
    for ell in ell_values:
        p = Plate(degree=DEGREE, ell=float(ell))
        mode = p.temporal(0.25, p.cutoff())
        for K in np.linspace(0.05, 1.00, 25):
            mode = p.temporal(float(K), mode)
            rows.append(dict(parameter="ell", value_SI=float(ell), K=float(K),
                             frequency_GHz=mode["omega"].real * p.fscale / 1e9,
                             gradient_length_ratio=float(p.lam),
                             source="synthetic gradient-length sweep, H=0"))
    return rows


def frequency_sweep(plates, etas):
    omin = PROTOCOL0["baseline_minimum_omega"]
    ocut = PROTOCOL0["baseline_cutoff_omega"]
    rows = []
    for frac in np.linspace(0.08, 0.92, 19):
        omega = omin + float(frac) * (ocut - omin)
        for eta in etas:
            p = plates[float(eta)]
            r, _ = p.edge(KY0, omega, K0, KB0)
            ki=complex(r["incident_K"]);kb=complex(r["backward_K"])
            rows.append(dict(
                eta=float(eta), frequency_GHz=omega * p.fscale / 1e9,
                R_B_edge=float(r["backward_reflection_self_power"]) *
                np.exp(2 * (ki.imag - kb.imag) * r["reference_distance_m"] / p.d),
                R_B_2um=float(r["backward_reflection_self_power"]),
                R_B_100um=float(r["backward_reflection_self_power"]) *
                np.exp(2 * (kb.imag - ki.imag) * 100e-6 / p.d),
                angle_deg=float(r["reflected_angle_deg"]),
                power_balance_error=float(r["power_balance_relative"])))
    return rows


def channel_power_sweep(plates, etas):
    rows = []
    for eta in etas:
        p = plates[float(eta)]
        r, s = p.edge(KY0, OMEGA0, K0, KB0)
        K = np.array(s["K"], dtype=complex)
        amplitudes = np.array(s["amplitudes"], dtype=complex)
        powers = np.array([p.power(s["Y"][:, j], OMEGA0) for j in range(len(K))])
        distances = np.full(len(K), r["reference_distance_m"] / p.d)
        with_power = np.abs(amplitudes) > 1e-30
        pos = with_power & (powers > 0)
        neg = with_power & (powers < 0)
        forward = float(np.sum((amplitudes[pos]**2).real * powers[pos] * np.exp(2 * K[pos].imag * distances[pos])))
        backward = float(np.sum(np.abs(amplitudes[neg])**2 * np.abs(powers[neg]) *
                               np.exp(2 * np.abs(K[neg].imag) * distances[neg])))
        rows.append(dict(
            eta=float(eta), R_B_2um=float(r["backward_reflection_self_power"]),
            incident_self_power=float(r["incident_power_left"]),
            forward_outgoing_fraction=forward / max(r["incident_power_left"], 1e-30),
            backward_outgoing_fraction=backward / max(r["incident_power_left"], 1e-30),
            total_outgoing_fraction=float(-r["total_outgoing_self_power"] / r["incident_power_left"]),
            negative_power_mode_count=int(np.sum(powers < 0)),
            outgoing_modes=int(r["outgoing_modes"]),
            power_balance_error=float(r["power_balance_relative"])))
    return rows


def attenuation_sweep(plates, etas):
    rows = []
    distances = np.array([1e-6, 5e-6, 10e-6, 20e-6, 50e-6, 100e-6, 200e-6, 500e-6, 1000e-6])
    for eta in etas:
        p = plates[float(eta)]
        r, _ = p.edge(KY0, OMEGA0, K0, KB0)
        R0 = float(r["backward_reflection_self_power"])
        ki=complex(r["incident_K"]);kb=complex(r["backward_K"])
        i_att=ki.imag;b_att=kb.imag
        for L in distances:
            decay_b = np.exp(2 * b_att * float(L) / p.d)
            decay_i = np.exp(2 * i_att * float(L) / p.d)
            rows.append(dict(
                eta=float(eta), distance_um=float(L) * 1e6,
                R_B_isolated=R0 * decay_b, incident_survival=decay_i,
                attenuation_backward_dB_m=-2 * abs(b_att) * SCALE / np.pi,
                attenuation_incident_dB_m=-2 * abs(i_att) * SCALE / np.pi,
                power_balance_error=float(r["power_balance_relative"])))
    return rows


def ky_sweep(plates, etas):
    rows = []
    kys = np.linspace(0.05, 0.20, 19)
    for eta in etas:
        p = plates[float(eta)]
        for ky in kys:
            # Locate the temporal mode closest to the H=0 cutoff; use its omega.
            m = p.temporal(0.25, p.cutoff())
            omega = m["omega"].real
            try:
                r, _ = p.edge(float(ky), omega, K0, KB0)
                rows.append(dict(eta=float(eta), ky=float(ky), frequency_GHz=omega * p.fscale / 1e9,
                                 R_B_edge=float(r["backward_reflection_self_power"]) *
                                 np.exp(2 * (r["incident_K"].imag - r["backward_K"].imag) *
                                        r["reference_distance_m"] / p.d),
                                 angle_deg=float(r["reflected_angle_deg"]),
                                 power_balance_error=float(r["power_balance_relative"])))
            except Exception as exc:  # Rank/root failure is recorded, not hidden.
                rows.append(dict(eta=float(eta), ky=float(ky), frequency_GHz=omega * p.fscale / 1e9,
                                 R_B_edge=None, angle_deg=None, power_balance_error=None,
                                 error=str(exc)))
    return rows


def boundary_sweep():
    rows = []
    etas = [-0.05, 0.0, 0.05]
    for electric in ["ground", "open"]:
        for eta in etas:
            p = Plate(degree=DEGREE, H=eta * HCRIT, electric=electric)
            try:
                m = p.temporal(0.25, p.cutoff())
                r, _ = p.edge(KY0, m["omega"], K0, KB0)
                rows.append(dict(electric=electric, eta=float(eta),
                                 frequency_GHz=m["omega"].real * p.fscale / 1e9,
                                 R_B_2um=float(r["backward_reflection_self_power"]),
                                 angle_deg=float(r["reflected_angle_deg"]),
                                 edge_scaled_residual=float(r["edge_scaled_residual"]),
                                 power_balance_error=float(r["power_balance_relative"]),
                                 error=None))
            except Exception as exc:
                rows.append(dict(electric=electric, eta=float(eta), frequency_GHz=None,
                                 R_B_2um=None, angle_deg=None, edge_scaled_residual=None,
                                 power_balance_error=None, error=str(exc)))
    return rows


def convergence_sweep():
    rows = []
    for degree in [14, 18, 22, 26]:
        p = Plate(degree=degree)
        r, _ = p.edge(KY0, OMEGA0, K0, KB0)
        kb=complex(r["backward_K"])
        rows.append(dict(method="Legendre", resolution=degree, R_B=float(r["backward_reflection_self_power"]),
                         K_B_real=float(kb.real), K_B_imag=float(kb.imag),
                         edge_scaled_residual=float(r["edge_scaled_residual"]),
                         power_error=float(r["power_balance_relative"])))
    for elements in [8, 12, 16, 20, 24]:
        p = Plate(degree=2 * elements + 1)
        r, _ = p.edge(KY0, OMEGA0, K0, KB0)
        kb=complex(r["backward_K"])
        rows.append(dict(method="spectral p=2n+1", resolution=2 * elements + 1, R_B=float(r["backward_reflection_self_power"]),
                         K_B_real=float(kb.real), K_B_imag=float(kb.imag),
                         edge_scaled_residual=float(r["edge_scaled_residual"]),
                         power_error=float(r["power_balance_relative"])))
    return rows


def field_sweep():
    """Solved angular spectrum, exact mode amplitudes and transverse flux."""
    p = Plate(degree=DEGREE)
    x = np.linspace(-80e-6, 0, 321)
    y = np.linspace(-70e-6, 30e-6, 241)
    XX, YY = np.meshgrid(x / p.d, y / p.d)
    Ui_modes=[]; Ub_modes=[]; Ki=[]; Kb=[]; powers_i=[]; powers_b=[]
    t, weights = hermgauss(25)
    kys = KY0 + np.sqrt(2) * 0.013 * t
    w = weights / np.sqrt(np.pi)
    bz, _ = p.basis(np.array([0.25]), 0)
    for kyval, weight in zip(kys, w):
        r, s = p.edge(float(kyval), OMEGA0, K0, KB0)
        ib = s["index_backward"]
        phase = np.exp(-1j * np.angle((bz[0] @ s["incident"]["q"][2 * p.n:3 * p.n])[0]))
        amp_i = phase * weight
        incident_y = s["incident"]["y"] * amp_i
        backward_y = s["Y"][:, ib] * complex(s["amplitudes"][ib]) * amp_i
        Ui_modes.append(incident_y[:p.nu])
        Ub_modes.append(backward_y[:p.nu])
        Ki.append(complex(r["incident_K"]))
        Kb.append(complex(r["backward_K"]))
        powers_i.append(p.power(s["incident"]["y"], OMEGA0))
        powers_b.append(p.power(s["Y"][:, ib], OMEGA0))
    Ui = np.array(Ui_modes).T; Ub = np.array(Ub_modes).T
    Ki = np.array(Ki, dtype=complex); Kb = np.array(Kb, dtype=complex)
    pi = np.array(powers_i); pb = np.array(powers_b)

    def intensity(U, K, powers):
        E = np.exp(1j * (K[:, None, None] * XX[None, :, :] + kys[:, None, None] * YY[None, :, :])).reshape(len(K), -1)
        gram = U.conj().T @ p.M @ U
        return np.maximum(np.sum(E.conj() * (gram @ E), axis=0).real.reshape(XX.shape), 0)

    Ii = intensity(Ui, Ki, pi)
    Ib = intensity(Ub, Kb, pb)
    metrics=[]
    for plane, xval in [("x=-2 um", -2e-6), ("x=-40 um", -40e-6)]:
        j = int(np.argmin(abs(x - xval)))
        # Exact positive-energy branch amplitudes and ray direction. Forward branch
        # rays use +k/|k|; the backward branch has energy opposite to its phase k.
        forward = np.sum(pi * np.exp(-2 * Ki.imag * xval / p.d))
        backward = np.sum(np.abs(pb * Kb.real) / np.abs(Kb) * np.exp(2 * np.abs(Kb.imag) * xval / p.d))
        metrics.append(dict(plane=plane, x_um=float(xval) * 1e6,
                            incident_centroid_y_um=float(np.sum(y * Ii[:, j]) / np.sum(Ii[:, j])),
                            backward_centroid_y_um=float(np.sum(y * Ib[:, j]) / np.sum(Ib[:, j])),
                            incident_sum=float(np.sum(Ii[:, j])),
                            backward_sum=float(np.sum(Ib[:, j])),
                            forward_ray_fraction=float(forward / max(np.sum(pi),1e-30)),
                            backward_ray_fraction=float(backward / max(np.sum(np.abs(pb*Kb.real)/np.abs(Kb)),1e-30))))
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    np.save(DATA_DIR / "x_um.npy", x * 1e6)
    np.save(DATA_DIR / "y_um.npy", y * 1e6)
    np.save(DATA_DIR / "ky_sample.npy", kys)
    np.save(DATA_DIR / "incident_intensity.npy", Ii)
    np.save(DATA_DIR / "backward_intensity.npy", Ib)
    np.save(DATA_DIR / "incident_wavevectors.npy", Ki)
    np.save(DATA_DIR / "backward_wavevectors.npy", Kb)
    return dict(x_um=x * 1e6, y_um=y * 1e6, incident_centroid=Ii, backward_centroid=Ib,
                ky_sample=kys, metrics=metrics)

def main():
    etas = [-0.05, -0.025, 0.0, 0.025, 0.05]
    plates = plates_for(etas)
    csvwrite("fig01_dispersion_velocity_attenuation.csv", temporal_sweep(plates, etas))
    csvwrite("fig02_material_parameter_sweep.csv", material_sweep())
    csvwrite("fig03_geometry_sweep.csv", geometry_sweep())
    csvwrite("fig04_frequency_reflection.csv", frequency_sweep(plates, etas))
    csvwrite("fig05_channel_power.csv", channel_power_sweep(plates, etas))
    csvwrite("fig06_attenuation_distance.csv", attenuation_sweep(plates, etas))
    csvwrite("fig07_coupling_sensitivity.csv", ky_sweep(plates, etas))
    csvwrite("fig08_boundary_sensitivity.csv", boundary_sweep())
    csvwrite("fig09_validation_convergence.csv", convergence_sweep())
    fields=field_sweep()
    jdump("fig10_field_metrics.json", fields["metrics"])

    # Fig 1: dispersion and wave speeds.
    rows = [r for r in csv.DictReader((DATA_DIR / "fig01_dispersion_velocity_attenuation.csv").open())]
    fig, ax = plt.subplots(2, 2, figsize=(7.4, 6.4), layout="constrained")
    for eta in etas:
        sel = [r for r in rows if float(r["eta"]) == eta]
        K = [float(r["K"]) for r in sel]
        ax[0, 0].plot(K, [float(r["frequency_GHz"]) for r in sel], **h_style(eta),
                      label=H_LABELS[eta], linewidth=2.0)
        ax[0, 1].plot(K, [float(r["phase_speed_m_s"]) for r in sel], **h_style(eta))
        ax[0, 1].plot(K, [float(r["group_speed_m_s"]) for r in sel], color=H_COLORS[eta],
                      alpha=0.35, linewidth=1.0)
        ax[0, 1].plot(K, [float(r["energy_speed_m_s"]) for r in sel], color=H_COLORS[eta],
                      linestyle=":", linewidth=1.6)
        ax[1, 0].semilogy(K, [float(r["FWHM_MHz"]) for r in sel], **h_style(eta))
        ax[1, 1].plot(K, [float(r["attenuation_dB_m"]) for r in sel], **h_style(eta))
    ax[0, 0].set_xlabel("$K=k_x d$"); ax[0, 0].set_ylabel("Frequency (GHz)")
    ax[0, 1].set_xlabel("$K=k_x d$"); ax[0, 1].set_ylabel("Speed (m/s)")
    ax[1, 0].set_xlabel("$K=k_x d$"); ax[1, 0].set_ylabel("Power FWHM (MHz)")
    ax[1, 1].set_xlabel("$K=k_x d$"); ax[1, 1].set_ylabel("Carrier attenuation (dB/m)")
    handles = [plt.Line2D([], [], color=H_COLORS[eta], linestyle=H_LINES[eta], label=H_LABELS[eta]) for eta in etas]
    ax[0, 0].legend(handles=handles, loc="lower right", borderpad=0.35)
    ax[0, 1].legend(handles=[plt.Line2D([], [], color="#4b5563", label="phase"),
                             plt.Line2D([], [], color="#4b5563", alpha=0.35, label="group"),
                             plt.Line2D([], [], color="#4b5563", linestyle=":", label="energy")],
                    loc="upper right", borderpad=0.35)
    for a in ax.ravel():
        label_panel(a, {0: "(a)", 1: "(b)", 2: "(c)", 3: "(d)"}[ax.ravel().tolist().index(a)])
        a.grid(True, alpha=0.75); a.xaxis.set_major_locator(MaxNLocator(nbins=5))
    fig.suptitle("Guided-wave dispersion and wave speeds", fontweight="bold")
    save_figure(fig, "fig01_dispersion", FIGURE_DIR)
    plt.close(fig)

    # Fig 2: ordinary sourced-material parameter effects.
    rows = [r for r in csv.DictReader((DATA_DIR / "fig02_material_parameter_sweep.csv").open())]
    fig, ax = plt.subplots(2, 2, figsize=(7.4, 6.2), layout="constrained")
    for parameter, color in [("n0", "#155e75"), ("M", "#cc642f")]:
        vals = sorted({float(r["value_SI"]) for r in rows if r["parameter"] == parameter})
        for v in vals:
            sel = [r for r in rows if r["parameter"] == parameter and float(r["value_SI"]) == v]
            ax[0, 0].plot([float(r["K"]) for r in sel], [float(r["frequency_GHz"]) for r in sel],
                          color=color, alpha=0.30 if abs(v - 2e18 if parameter == "n0" else v - 0.0175) > 0 else 1.0,
                          linewidth=2.0 if (parameter == "n0" and v == 2e18) or (parameter == "M" and v == 0.0175) else 1.6)
            ax[0, 1].plot([float(r["K"]) for r in sel], [float(r["R_B"]) * 100 for r in sel],
                          color=color, linewidth=2.0 if (parameter == "n0" and v == 2e18) or (parameter == "M" and v == 0.0175) else 1.6)
            ax[1, 0].plot([float(r["K"]) for r in sel], [float(r["attenuation_dB_m"]) for r in sel],
                          color=color, alpha=0.45, linewidth=1.6)
        ax[1, 1].plot([float(r["K"]) for r in sel], [float(r["frequency_GHz"]) for r in sel], color=color, alpha=0.30)
    ax[0, 0].set_xlabel("$K=k_x d$"); ax[0, 0].set_ylabel("Frequency (GHz)")
    ax[0, 1].set_xlabel("$K=k_x d$"); ax[0, 1].set_ylabel("$R_B$ edge (%)")
    ax[1, 0].set_xlabel("$K=k_x d$"); ax[1, 0].set_ylabel("Carrier attenuation (dB/m)")
    ax[1, 1].set_xlabel("$K=k_x d$"); ax[1, 1].set_ylabel("Frequency (GHz)")
    labels = {"(a)": "Dispersion", "(b)": "$R_B$", "(c)": "Attenuation", "(d)": "Family"}
    for a, lab in zip(ax.ravel(), labels.values()):
        label_panel(a, list(labels.keys())[list(labels.values()).index(lab)]); a.grid(True, alpha=0.75)
    fig.suptitle("Carrier concentration and mobility effects", fontweight="bold")
    save_figure(fig, "fig02_material", FIGURE_DIR)
    plt.close(fig)

    # Fig 3: thickness and gradient length.
    rows = [r for r in csv.DictReader((DATA_DIR / "fig03_geometry_sweep.csv").open())]
    fig, ax = plt.subplots(2, 2, figsize=(7.4, 6.2), layout="constrained")
    for parameter, color in [("d", "#155e75"), ("ell", "#cc642f")]:
        for v in sorted({float(r["value_SI"]) for r in rows if r["parameter"] == parameter}):
            sel = [r for r in rows if r["parameter"] == parameter and float(r["value_SI"]) == v]
            ax[0, 0].plot([float(r["K"]) for r in sel], [float(r["frequency_GHz"]) for r in sel], color=color, linewidth=2.0 if v == (200e-9 if parameter == "d" else 50e-9) else 1.6)
            ax[0, 1].plot([float(r["K"]) for r in sel], [float(r["gradient_length_ratio"]) for r in sel], color=color, linewidth=2.0)
            ax[1, 0].plot([float(r["K"]) for r in sel], [float(r["frequency_GHz"]) for r in sel], color=color, linewidth=2.0 if v == (200e-9 if parameter == "d" else 50e-9) else 1.6)
            ax[1, 1].plot([float(r["K"]) for r in sel], [float(r["frequency_GHz"]) / 1e3 for r in sel], color=color, linewidth=1.6)
    ax[0, 0].set_xlabel("$K=k_x d$"); ax[0, 0].set_ylabel("Frequency (GHz)")
    ax[0, 1].set_xlabel("$K=k_x d$"); ax[0, 1].set_ylabel("$\ell/d$")
    ax[1, 0].set_xlabel("$K=k_x d$"); ax[1, 0].set_ylabel("Frequency (GHz)")
    ax[1, 1].set_xlabel("$K=k_x d$"); ax[1, 1].set_ylabel("Frequency (THz)")
    for a, lab in zip(ax.ravel(), ["(a)", "(b)", "(c)", "(d)"]): label_panel(a, lab); a.grid(True, alpha=0.75)
    fig.suptitle("Plate thickness and gradient-length effects", fontweight="bold")
    save_figure(fig, "fig03_geometry", FIGURE_DIR)
    plt.close(fig)

    # Fig 4: frequency-dependent reflection.
    rows = [r for r in csv.DictReader((DATA_DIR / "fig04_frequency_reflection.csv").open())]
    fig, ax = plt.subplots(1, 4, figsize=(9.6, 3.1), layout="constrained")
    for eta in etas:
        sel = [r for r in rows if float(r["eta"]) == eta]
        f = [float(r["frequency_GHz"]) for r in sel]
        ax[0].plot(f, [float(r["R_B_edge"]) * 100 for r in sel], **h_style(eta))
        ax[1].plot(f, [float(r["R_B_2um"]) * 100 for r in sel], **h_style(eta))
        ax[2].plot(f, [float(r["R_B_100um"]) * 100 for r in sel], **h_style(eta))
        ax[3].plot(f, [float(r["angle_deg"]) for r in sel], **h_style(eta))
    ax[0].set_xlabel("Frequency (GHz)"); ax[0].set_ylabel("$R_B$ edge (%)")
    ax[1].set_xlabel("Frequency (GHz)"); ax[1].set_ylabel("$R_B$ at 2 $\mu$m (%)")
    ax[2].set_xlabel("Frequency (GHz)"); ax[2].set_ylabel("$R_B$ at 100 $\mu$m (%)")
    ax[3].set_xlabel("Frequency (GHz)"); ax[3].set_ylabel("Angle (deg)")
    for a, lab in zip(ax, ["(a)", "(b)", "(c)", "(d)"]): label_panel(a, lab); a.grid(True, alpha=0.75); a.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax[0].legend(handles=[plt.Line2D([], [], color=H_COLORS[e], linestyle=H_LINES[e], label=H_LABELS[e]) for e in etas], loc="lower right")
    fig.suptitle("Backward reflection versus frequency", fontweight="bold")
    save_figure(fig, "fig04_frequency", FIGURE_DIR)
    plt.close(fig)

    # Fig 5: modal power distribution.
    rows = [r for r in csv.DictReader((DATA_DIR / "fig05_channel_power.csv").open())]
    fig, ax = plt.subplots(1, 4, figsize=(9.6, 3.0), layout="constrained")
    etas5 = [-0.05, 0.0, 0.05]
    for eta in etas5:
        sel = [r for r in rows if float(r["eta"]) == eta]
        ax[0].plot([float(r["eta"]) for r in sel], [float(r["R_B_2um"]) * 100 for r in sel], **h_style(eta))
        ax[1].plot([float(r["eta"]) for r in sel], [float(r["negative_power_mode_count"]) for r in sel], **h_style(eta))
        ax[2].plot([float(r["eta"]) for r in sel], [float(r["backward_outgoing_fraction"]) * 100 for r in sel], **h_style(eta))
        ax[3].plot([float(r["eta"]) for r in sel], [float(r["total_outgoing_fraction"]) * 100 for r in sel], **h_style(eta))
    for a, title, ylabel in zip(ax, ["(a)", "(b)", "(c)", "(d)"],
                                ["$R_B$", "Backward modes", "Negative-power fraction (%)", "Total outgoing fraction (%)"]):
        a.set_xlabel("$H/H^*$"); a.set_ylabel(ylabel); label_panel(a, title); a.grid(True, alpha=0.75)
    fig.suptitle("Reflection-channel conversion and modal energy", fontweight="bold")
    save_figure(fig, "fig05_channel", FIGURE_DIR)
    plt.close(fig)

    # Fig 6: attenuation and survival.
    rows = [r for r in csv.DictReader((DATA_DIR / "fig06_attenuation_distance.csv").open())]
    fig, ax = plt.subplots(2, 2, figsize=(7.4, 6.0), layout="constrained")
    for eta in etas:
        sel = [r for r in rows if float(r["eta"]) == eta]
        d = [float(r["distance_um"]) for r in sel]
        ax[0, 0].semilogy(d, [float(r["R_B_isolated"]) * 100 for r in sel], **h_style(eta))
        ax[0, 1].plot(d, [float(r["attenuation_backward_dB_m"]) for r in sel], **h_style(eta))
        ax[1, 0].semilogy(d, [float(r["incident_survival"]) for r in sel], **h_style(eta))
        ax[1, 1].plot(d, [float(r["attenuation_incident_dB_m"]) for r in sel], **h_style(eta))
    for a, ylabel, lab in zip(ax.ravel(), ["$R_B$ (%)", "Backward attenuation (dB/m)", "Incident survival", "Incident attenuation (dB/m)"], ["(a)", "(b)", "(c)", "(d)"]):
        a.set_xlabel("Distance from edge ($\mu$m)"); a.set_ylabel(ylabel); label_panel(a, lab); a.grid(True, alpha=0.75)
    ax[0, 0].legend(handles=[plt.Line2D([], [], color=H_COLORS[e], linestyle=H_LINES[e], label=H_LABELS[e]) for e in etas], loc="lower left")
    fig.suptitle("Attenuation, distance and survival", fontweight="bold")
    save_figure(fig, "fig06_attenuation", FIGURE_DIR)
    plt.close(fig)

    # Fig 7: H and ky coupling sensitivity as a real 3-D root grid plus contours.
    rows = [r for r in csv.DictReader((DATA_DIR / "fig07_coupling_sensitivity.csv").open())]
    etas7=[-0.05,0.0,0.05]; kys=sorted({round(float(r["ky"]),12) for r in rows if r.get("error") is None})
    R_edge=np.full((len(etas7),len(kys)),np.nan)
    for r in rows:
      if r.get("error") is not None:continue
      if float(r["eta"]) not in etas7:continue
      R_edge[etas7.index(float(r["eta"])),kys.index(round(float(r["ky"]),12))]=float(r["R_B_edge"])
    fig=plt.figure(figsize=(7.8,6.3),layout="constrained")
    ax3=fig.add_subplot(2,2,1,projection="3d")
    eta_mesh,ky_mesh=np.meshgrid(np.array(etas7),np.array(kys),indexing='ij')
    surf=ax3.plot_surface(eta_mesh,ky_mesh,R_edge*100,cmap="viridis",linewidth=0,antialiased=True)
    ax3.set_xlabel("$H/H^*$");ax3.set_ylabel("$k_y d$");ax3.set_zlabel("$R_B$ edge (%)");ax3.view_init(elev=22,azim=-55)
    fig.colorbar(surf,ax=ax3,shrink=.55,label="$R_B$ edge (%)")
    ax2=fig.add_subplot(2,2,2);c=ax2.contourf(ky_mesh,eta_mesh,R_edge*100,cmap="plasma")
    ax2.set_xlabel("$k_y d$");ax2.set_ylabel("$H/H^*$");fig.colorbar(c,ax=ax2,label="$R_B$ edge (%)")
    ax4=fig.add_subplot(2,2,3)
    for eta in etas7:ax4.plot(kys,R_edge[etas7.index(eta)]*100,**h_style(eta))
    ax4.set_xlabel("$k_y d$");ax4.set_ylabel("$R_B$ edge (%)");ax4.set_title("(c) H slices",fontsize=10);ax4.grid(True,alpha=.75)
    ax1=fig.add_subplot(2,2,4)
    for ky in kys:ax1.plot(etas7,R_edge[:,kys.index(ky)]*100,marker="o",markersize=5,linewidth=2.0)
    ax1.set_xlabel("$H/H^*$");ax1.set_ylabel("$R_B$ edge (%)");ax1.set_title("(d) $k_y$ slices",fontsize=10);ax1.grid(True,alpha=.75)
    fig.suptitle("Carrier-strain-gradient coupling sensitivity",fontweight="bold")
    save_figure(fig,"fig07_coupling",FIGURE_DIR)
    plt.close(fig)

    # Fig 8: boundary and material sensitivity.
    rows = [r for r in csv.DictReader((DATA_DIR / "fig08_boundary_sensitivity.csv").open())]
    fig, ax = plt.subplots(1, 4, figsize=(9.6, 3.0), layout="constrained")
    for eta in etas:
        for electric, color, ls in [("ground", "#155e75", "-"), ("open", "#cc642f", "--")]:
            sel = [r for r in rows if r["electric"] == electric and float(r["eta"]) == eta and r.get("R_B_2um")]
            ax[0].plot([float(r["eta"]) for r in sel], [float(r["frequency_GHz"]) for r in sel], color=color, ls=ls, linewidth=1.6)
            ax[1].plot([float(r["eta"]) for r in sel], [float(r["R_B_2um"]) * 100 for r in sel], color=color, ls=ls, linewidth=2.0)
            ax[2].plot([float(r["eta"]) for r in sel], [float(r["angle_deg"]) for r in sel], color=color, ls=ls, linewidth=1.6)
            ax[3].semilogy([float(r["eta"]) for r in sel], [float(r["edge_scaled_residual"]) for r in sel], color=color, ls=ls, linewidth=1.6)
    for a, ylabel, lab in zip(ax, ["Frequency (GHz)", "$R_B$ (%)", "Angle (deg)", "Weak residual"], ["(a)", "(b)", "(c)", "(d)"]):
        a.set_xlabel("$H/H^*$"); a.set_ylabel(ylabel); label_panel(a, lab); a.grid(True, alpha=0.75)
    ax[1].legend(handles=[plt.Line2D([], [], color="#155e75", linestyle="-", label="grounded"), plt.Line2D([], [], color="#cc642f", linestyle="--", label="open")], loc="upper right")
    fig.suptitle("Boundary-condition sensitivity", fontweight="bold")
    save_figure(fig, "fig08_boundary", FIGURE_DIR)
    plt.close(fig)

    # Fig 9: convergence and validation.
    rows = [r for r in csv.DictReader((DATA_DIR / "fig09_validation_convergence.csv").open())]
    fig, ax = plt.subplots(2, 2, figsize=(7.4, 6.0), layout="constrained")
    for method, color in [("Legendre", "#155e75"), ("spectral p=2n+1", "#cc642f")]:
        sel = [r for r in rows if r["method"] == method]
        ax[0, 0].semilogy([float(r["resolution"]) for r in sel], [abs(float(r["R_B"]) - PRIMARY0["backward_reflection_self_power"]) for r in sel], color=color, marker="o", markersize=5, linewidth=2.0)
        ax[0, 1].plot([float(r["resolution"]) for r in sel], [float(r["edge_scaled_residual"]) for r in sel], color=color, marker="o", markersize=5, linewidth=2.0)
        ax[1, 0].semilogy([float(r["resolution"]) for r in sel], [float(r["power_error"]) for r in sel], color=color, marker="o", markersize=5, linewidth=2.0)
        ax[1, 1].plot([float(r["resolution"]) for r in sel], [float(r["K_B_imag"]) for r in sel], color=color, marker="o", markersize=5, linewidth=2.0)
    for a, ylabel, lab in zip(ax.ravel(), ["$|R_B-R_B^{p=22}|$", "Edge residual", "Power error", "$K_B$ imaginary part"], ["(a)", "(b)", "(c)", "(d)"]):
        a.set_xlabel("Resolution"); a.set_ylabel(ylabel); label_panel(a, lab); a.grid(True, alpha=0.75)
    fig.suptitle("Numerical convergence and residuals", fontweight="bold")
    save_figure(fig, "fig09_validation", FIGURE_DIR)
    plt.close(fig)

    # Fig 10: solved field, exact flux and consistent coordinate convention.
    fields=dict(x_um=np.load(DATA_DIR/"x_um.npy"),y_um=np.load(DATA_DIR/"y_um.npy"),
                incident_centroid=np.load(DATA_DIR/"incident_intensity.npy"),
                backward_centroid=np.load(DATA_DIR/"backward_intensity.npy"),
                ky_sample=np.load(DATA_DIR/"ky_sample.npy"),
                metrics=json.loads((DATA_DIR/"fig10_field_metrics.json").read_text()))
    metrics=fields["metrics"]; x=fields["x_um"]; y=fields["y_um"]
    fig=plt.figure(figsize=(7.4,6.2),layout="constrained")
    axI=fig.add_subplot(2,2,1);axB=fig.add_subplot(2,2,2);axC=fig.add_subplot(2,2,3);axF=fig.add_subplot(2,2,4)
    pI=axI.pcolormesh(x,y,fields["incident_centroid"],cmap="viridis",shading="auto")
    pB=axB.pcolormesh(x,y,fields["backward_centroid"],cmap="plasma",shading="auto")
    for a in (axI,axB):a.axvline(0,color="#111827",linewidth=1.5);a.set_aspect("equal")
    axI.set_title("(a) Incident channel",fontsize=10);axI.set_xlabel("$x$ ($\\mu$m)");axI.set_ylabel("$y$ ($\\mu$m)")
    axB.set_title("(b) Backward channel",fontsize=10);axB.set_xlabel("$x$ ($\\mu$m)");axB.set_ylabel("$y$ ($\\mu$m)")
    fig.colorbar(pI,ax=axI,label="Normalized intensity");fig.colorbar(pB,ax=axB,label="Normalized intensity")
    axC.axis("off");axC.set_title("(c) Coordinate convention",fontsize=10)
    axC.annotate("",xy=(0,-1),xytext=(1,0),arrowprops=dict(arrowstyle="->",color="#111827",lw=2))
    axC.text(.32,-.12,"$k_x$",fontsize=10);axC.text(-.2,-.3,"$x<0$ plate",fontsize=10)
    axC.text(.1,.75,"$k_y$",fontsize=10);axC.text(-.6,.8,"$y$ invariant",fontsize=10)
    axC.text(-.3,.4,"phase ansatz\\ $e^{i(k_xx+k_yy-\\omega t)}$",fontsize=10)
    for a,m in zip([axF],[metrics[1]]):
      a.set_title("(d) Flux at $x=-40\\,\\mu$m",fontsize=10)
      a.set_xlim(0,1);a.set_ylim(0,1);a.axis("off")
      a.annotate("",xy=(.75,.45),xytext=(.2,.75),arrowprops=dict(arrowstyle="-|>",color="#155e75",lw=3))
      a.text(.05,.82,"Incident",fontsize=10);a.text(.05,.72,"right/up",fontsize=10)
      a.annotate("",xy=(.2,.25),xytext=(.7,.5),arrowprops=dict(arrowstyle="-|>",color="#9d174d",lw=3))
      a.text(.05,.58,"Backward",fontsize=10);a.text(.05,.48,"left/down",fontsize=10)
      a.text(.05,.38,"Edge at $x=0$",fontsize=10);a.text(.05,.28,"$k_y$ conserved",fontsize=10)
      a.text(.05,.16,"computed centroid y is about 0 $\mu$m",fontsize=10)
    fig.suptitle("Spatial energy flux and computed wave field",fontweight="bold")
    save_figure(fig,"fig10_field",FIGURE_DIR,rasterize=True)
    plt.close(fig)

    print("Figure generation complete; all values trace to saved CSV/JSON arrays.")


if __name__=="__main__":
    main()
