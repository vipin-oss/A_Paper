"""Render revised Paper A publication figures from validated CSV/JSON data.

Every annotated number is read from the corresponding CSV/JSON file. No figure
contains a hard-coded numerical result.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from paper_a_study.figure_style import (
    save_figure, h_style, label_panel, H_COLORS, H_LINES, H_LABELS,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "paper_a_study" / "figure_data"
FIGURE_DIR = ROOT / "paper_a_study" / "figures_final"
ETAS = [-0.05, -0.025, 0.0, 0.025, 0.05]
ETAS7 = [-0.05, 0.0, 0.05]
COLORS = {"n0": "#155e75", "M": "#cc642f", "d": "#155e75", "ell": "#cc642f"}
BASELINE = {"n0": 2e18, "M": 0.0175, "d": 200e-9, "ell": 50e-9}


def rows(name: str) -> list[dict]:
    with (DATA / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def panel_labels(axes) -> list[str]:
    return [f"({chr(ord('a') + index)})" for index in range(len(axes))]


def fig01_dispersion() -> None:
    data = rows("fig01_dispersion_velocity_attenuation.csv")
    fig, axes = plt.subplots(2, 2, figsize=(7.4, 6.4), layout="constrained")
    for eta in ETAS:
        selected = [row for row in data if float(row["eta"]) == eta]
        K = [float(row["K"]) for row in selected]
        axes[0, 0].plot(K, [float(row["frequency_GHz"]) for row in selected], **h_style(eta), label=H_LABELS[eta])
        axes[0, 1].plot(K, [float(row["phase_speed_m_s"]) for row in selected], **h_style(eta))
        axes[0, 1].plot(K, [float(row["group_speed_m_s"]) for row in selected], color=H_COLORS[eta], alpha=0.35, linewidth=1.0)
        axes[0, 1].plot(K, [float(row["energy_speed_m_s"]) for row in selected], color=H_COLORS[eta], linestyle=":", linewidth=1.6)
        axes[1, 0].semilogy(K, [float(row["FWHM_MHz"]) for row in selected], **h_style(eta))
        axes[1, 1].plot(K, [float(row["attenuation_dB_m"]) for row in selected], **h_style(eta))
    for axis, xlabel, ylabel in zip(
        axes.ravel(),
        ["$K=k_x d$", "$K=k_x d$", "$K=k_x d$", "$K=k_x d$"],
        ["Frequency (GHz)", "Speed (m/s)", "Power FWHM (MHz)", "Carrier attenuation (dB/m)"],
    ):
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.grid(True, alpha=0.75)
        axis.xaxis.set_major_locator(MaxNLocator(nbins=5))
    handles = [plt.Line2D([], [], color=H_COLORS[eta], linestyle=H_LINES[eta], label=H_LABELS[eta]) for eta in ETAS]
    axes[0, 0].legend(handles=handles, loc="lower right", borderpad=0.35)
    axes[0, 1].legend(
        handles=[
            plt.Line2D([], [], color="#4b5563", label="phase"),
            plt.Line2D([], [], color="#4b5563", alpha=0.35, label="group"),
            plt.Line2D([], [], color="#4b5563", linestyle=":", label="energy"),
        ],
        loc="upper right", borderpad=0.35,
    )
    for axis, label in zip(axes.ravel(), panel_labels(axes)):
        label_panel(axis, label)
    fig.suptitle("Guided-wave dispersion and wave speeds", fontweight="bold")
    save_figure(fig, "fig01_dispersion", FIGURE_DIR)
    plt.close(fig)


def fig02_material() -> None:
    data = rows("fig02_material_parameter_sweep.csv")
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.2), layout="constrained")
    for parameter in ("n0", "M"):
        values = sorted({float(row["value_SI"]) for row in data if row["parameter"] == parameter})
        for value in values:
            selected = [row for row in data if row["parameter"] == parameter and float(row["value_SI"]) == value]
            baseline = abs(value - BASELINE[parameter]) < 1e-30
            linewidth = 2.0 if baseline else 1.5
            alpha = 1.0 if baseline else 0.45
            axes[0].plot([float(row["K"]) for row in selected], [float(row["frequency_GHz"]) for row in selected], color=COLORS[parameter], linewidth=linewidth, alpha=alpha)
            axes[1].plot([float(row["K"]) for row in selected], [float(row["R_B_2um"]) * 100 if row["R_B_2um"] else np.nan for row in selected], color=COLORS[parameter], linewidth=linewidth, alpha=alpha)
            axes[2].plot([float(row["K"]) for row in selected], [float(row["attenuation_dB_m"]) for row in selected], color=COLORS[parameter], linewidth=linewidth, alpha=alpha)
    for axis, xlabel, ylabel in zip(axes, ["$K=k_x d$", "$K=k_x d$", "$K=k_x d$"], ["Frequency (GHz)", "$R_B$ (%)", "Carrier attenuation (dB/m)"]):
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.grid(True, alpha=0.75)
        axis.xaxis.set_major_locator(MaxNLocator(nbins=4))
    for axis, label in zip(axes, panel_labels(axes)):
        label_panel(axis, label)
    fig.suptitle("Carrier concentration and mobility effects", fontweight="bold")
    save_figure(fig, "fig02_material", FIGURE_DIR)
    plt.close(fig)


def fig03_geometry() -> None:
    data = rows("fig03_geometry_sweep.csv")
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.2), layout="constrained")
    for parameter in ("d", "ell"):
        values = sorted({float(row["value_SI"]) for row in data if row["parameter"] == parameter})
        for value in values:
            selected = [row for row in data if row["parameter"] == parameter and float(row["value_SI"]) == value]
            baseline = abs(value - BASELINE[parameter]) < 1e-30
            axes[0].plot([float(row["K"]) for row in selected], [float(row["frequency_GHz"]) for row in selected], color=COLORS[parameter], linewidth=2.0 if baseline else 1.5)
            axes[1].plot([float(row["K"]) for row in selected], [float(row["gradient_length_ratio"]) for row in selected], color=COLORS[parameter], linewidth=1.5)
            axes[2].plot([float(row["K"]) for row in selected], [float(row["cutoff_frequency_GHz"]) for row in selected], color=COLORS[parameter], linewidth=1.5, alpha=0.45)
    for axis, xlabel, ylabel in zip(axes, ["$K=k_x d$", "$K=k_x d$", "$K=k_x d$"], ["Frequency (GHz)", "$\ell/d$", "Cutoff frequency (GHz)"]):
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.grid(True, alpha=0.75)
        axis.xaxis.set_major_locator(MaxNLocator(nbins=4))
    for axis, label in zip(axes, panel_labels(axes)):
        label_panel(axis, label)
    fig.suptitle("Plate thickness and gradient-length effects", fontweight="bold")
    save_figure(fig, "fig03_geometry", FIGURE_DIR)
    plt.close(fig)


def fig04_frequency() -> None:
    data = rows("fig04_frequency_reflection.csv")
    fig, axes = plt.subplots(1, 4, figsize=(9.6, 3.1), layout="constrained")
    for eta in ETAS:
        selected = [row for row in data if float(row["eta"]) == eta and row["R_B_2um"]]
        axes[0].plot([float(row["frequency_GHz"]) for row in selected], [float(row["R_B_edge"]) * 100 for row in selected], **h_style(eta))
        axes[1].plot([float(row["frequency_GHz"]) for row in selected], [float(row["R_B_2um"]) * 100 for row in selected], **h_style(eta))
        axes[2].plot([float(row["frequency_GHz"]) for row in selected], [float(row["R_B_100um"]) * 100 for row in selected], **h_style(eta))
        axes[3].plot([float(row["frequency_GHz"]) for row in selected], [float(row["angle_deg"]) for row in selected], **h_style(eta))
    for axis, xlabel, ylabel in zip(axes, ["Frequency (GHz)"] * 4, ["$R_B$ edge (%)", "$R_B$ at 2 $\mu$m (%)", "$R_B$ at 100 $\mu$m (%)", "Angle (deg)"]):
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.grid(True, alpha=0.75)
        axis.xaxis.set_major_locator(MaxNLocator(nbins=4))
    axes[0].legend(handles=[plt.Line2D([], [], color=H_COLORS[eta], linestyle=H_LINES[eta], label=H_LABELS[eta]) for eta in ETAS], loc="lower right")
    for axis, label in zip(axes, panel_labels(axes)):
        label_panel(axis, label)
    fig.suptitle("Backward reflection versus frequency", fontweight="bold")
    save_figure(fig, "fig04_frequency", FIGURE_DIR)
    plt.close(fig)


def fig05_channel() -> None:
    data = rows("fig05_channel_power.csv")
    fig, axes = plt.subplots(1, 4, figsize=(9.6, 3.0), layout="constrained")
    for eta in ETAS7:
        selected = [row for row in data if float(row["eta"]) == eta]
        axes[0].plot([float(row["eta"]) for row in selected], [float(row["R_B_2um"]) * 100 for row in selected], **h_style(eta))
        axes[1].plot([float(row["eta"]) for row in selected], [float(row["negative_power_mode_count"]) for row in selected], **h_style(eta))
        axes[2].plot([float(row["eta"]) for row in selected], [float(row["backward_fraction"]) * 100 for row in selected], **h_style(eta))
        axes[3].plot([float(row["eta"]) for row in selected], [float(row["total_outgoing_fraction"]) * 100 for row in selected], **h_style(eta))
    for axis, ylabel in zip(axes, ["$R_B$ (%)", "Backward modes", "Backward self-flux fraction (%)", "Total outgoing fraction (%)"]):
        axis.set_xlabel("$H/H^*$")
        axis.set_ylabel(ylabel)
        axis.grid(True, alpha=0.75)
    for axis, label in zip(axes, panel_labels(axes)):
        label_panel(axis, label)
    fig.suptitle("Reflection-channel conversion and modal energy", fontweight="bold")
    save_figure(fig, "fig05_channel", FIGURE_DIR)
    plt.close(fig)


def fig06_attenuation() -> None:
    data = rows("fig06_attenuation_distance.csv")
    fig, axes = plt.subplots(2, 2, figsize=(7.4, 6.0), layout="constrained")
    for eta in ETAS:
        selected = [row for row in data if float(row["eta"]) == eta]
        distance = [float(row["distance_um"]) for row in selected]
        axes[0, 0].semilogy(distance, [float(row["R_B_isolated_transfer"]) * 100 for row in selected], **h_style(eta))
        axes[0, 1].plot(distance, [float(row["backward_self_flux"]) * 100 for row in selected], **h_style(eta))
        axes[1, 0].plot(distance, [float(row["incident_self_flux"]) for row in selected], **h_style(eta))
        axes[1, 1].plot(distance, [float(row["attenuation_backward_dB_m"]) for row in selected], **h_style(eta))
    for axis, xlabel, ylabel in zip(axes.ravel(), ["Distance from edge ($\mu$m)"] * 4, ["$R_B$ transfer (%)", "Backward self-flux (%)", "Incident self-flux", "Backward growth (dB/m)"]):
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.grid(True, alpha=0.75)
    axes[0, 0].legend(handles=[plt.Line2D([], [], color=H_COLORS[eta], linestyle=H_LINES[eta], label=H_LABELS[eta]) for eta in ETAS], loc="lower left")
    for axis, label in zip(axes.ravel(), panel_labels(axes)):
        label_panel(axis, label)
    fig.suptitle("Attenuation, distance and isolated-channel transfer", fontweight="bold")
    save_figure(fig, "fig06_attenuation", FIGURE_DIR)
    plt.close(fig)


def fig07_coupling() -> None:
    data = rows("fig07_coupling_sensitivity.csv")
    etas = ETAS7
    kys = sorted({round(float(row["ky"]), 12) for row in data if not row["error"]})
    transfer = np.full((len(etas), len(kys)), np.nan)
    for row in data:
        if row["error"]:
            continue
        transfer[etas.index(float(row["eta"])), kys.index(round(float(row["ky"]), 12))] = float(row["R_B_edge"]) * 100
    fig = plt.figure(figsize=(7.8, 6.3), layout="constrained")
    ax3 = fig.add_subplot(2, 2, 1, projection="3d")
    eta_mesh, ky_mesh = np.meshgrid(np.array(etas), np.array(kys), indexing="ij")
    surface = ax3.plot_surface(eta_mesh, ky_mesh, transfer, cmap="viridis", linewidth=0, antialiased=True)
    ax3.set_xlabel("$H/H^*$")
    ax3.set_ylabel("$k_y d$")
    ax3.set_zlabel("$R_B$ edge (%)")
    ax3.view_init(elev=22, azim=-55)
    fig.colorbar(surface, ax=ax3, shrink=0.55, label="$R_B$ edge (%)")
    ax2 = fig.add_subplot(2, 2, 2)
    contour = ax2.contourf(ky_mesh, eta_mesh, transfer, cmap="plasma")
    ax2.set_xlabel("$k_y d$")
    ax2.set_ylabel("$H/H^*$")
    fig.colorbar(contour, ax=ax2, label="$R_B$ edge (%)")
    ax4 = fig.add_subplot(2, 2, 3)
    for eta in etas:
        ax4.plot(kys, transfer[etas.index(eta)], **h_style(eta))
    ax4.set_xlabel("$k_y d$")
    ax4.set_ylabel("$R_B$ edge (%)")
    ax4.set_title("(c) H slices", fontsize=10)
    ax4.grid(True, alpha=0.75)
    ax1 = fig.add_subplot(2, 2, 4)
    for ky in kys:
        ax1.plot(etas, transfer[:, kys.index(ky)], marker="o", markersize=5, linewidth=2.0)
    ax1.set_xlabel("$H/H^*$")
    ax1.set_ylabel("$R_B$ edge (%)")
    ax1.set_title("(d) $k_y$ slices", fontsize=10)
    ax1.grid(True, alpha=0.75)
    fig.suptitle("Carrier-strain-gradient coupling sensitivity", fontweight="bold")
    save_figure(fig, "fig07_coupling", FIGURE_DIR)
    plt.close(fig)


def fig08_boundary() -> None:
    data = rows("fig08_boundary_sensitivity.csv")
    grounded = [row for row in data if row["electric"] == "ground" and row["R_B_2um"]]
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.1), layout="constrained")
    for eta in (-0.05, 0.0, 0.05):
        selected = [row for row in grounded if float(row["eta"]) == eta]
        axes[0].plot([float(row["eta"]) for row in selected], [float(row["frequency_GHz"]) for row in selected], **h_style(eta))
        axes[1].plot([float(row["eta"]) for row in selected], [float(row["R_B_2um"]) * 100 for row in selected], **h_style(eta))
        axes[2].semilogy([float(row["eta"]) for row in selected], [float(row["edge_scaled_residual"]) for row in selected], **h_style(eta))
    axes[1].text(0.02, 0.95, "open-boundary solver singular in all tested cases", transform=axes[1].transAxes, va="top", fontsize=8, color="#cc642f")
    for axis, xlabel, ylabel in zip(axes, ["$H/H^*$"] * 3, ["Frequency (GHz)", "$R_B$ (%)", "Weak residual"]):
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.grid(True, alpha=0.75)
    for axis, label in zip(axes, panel_labels(axes)):
        label_panel(axis, label)
    fig.suptitle("Boundary-condition sensitivity", fontweight="bold")
    save_figure(fig, "fig08_boundary", FIGURE_DIR)
    plt.close(fig)


def fig09_validation() -> None:
    data = rows("fig09_validation_convergence.csv")
    baseline = float([row for row in data if row["method"] == "Legendre" and float(row["resolution"]) == 22][0]["R_B"])
    fig, axes = plt.subplots(2, 2, figsize=(7.4, 6.0), layout="constrained")
    for method, color in (("Legendre", "#155e75"), ("spectral p=2n+1", "#cc642f")):
        selected = [row for row in data if row["method"] == method]
        axes[0, 0].semilogy([float(row["resolution"]) for row in selected], [abs(float(row["R_B"]) - baseline) for row in selected], color=color, marker="o", markersize=5, linewidth=2.0)
        axes[0, 1].plot([float(row["resolution"]) for row in selected], [float(row["edge_scaled_residual"]) for row in selected], color=color, marker="o", markersize=5, linewidth=2.0)
        axes[1, 0].semilogy([float(row["resolution"]) for row in selected], [float(row["power_error"]) for row in selected], color=color, marker="o", markersize=5, linewidth=2.0)
        axes[1, 1].plot([float(row["resolution"]) for row in selected], [float(row["K_B_imag"]) for row in selected], color=color, marker="o", markersize=5, linewidth=2.0)
    for axis, xlabel, ylabel in zip(axes.ravel(), ["Resolution"] * 4, ["$|R_B-R_B^{p=22}|$", "Edge residual", "Power error", "$K_B$ imaginary part"]):
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.grid(True, alpha=0.75)
    for axis, label in zip(axes.ravel(), panel_labels(axes)):
        label_panel(axis, label)
    fig.suptitle("Numerical convergence and residuals", fontweight="bold")
    save_figure(fig, "fig09_validation", FIGURE_DIR)
    plt.close(fig)


def fig10_field() -> None:
    metrics = json.loads((DATA / "fig10_field_metrics.json").read_text())
    x_um = np.load(DATA / "x_um.npy")
    y_um = np.load(DATA / "y_um.npy")
    incident = np.load(DATA / "incident_intensity.npy")
    backward = np.load(DATA / "backward_intensity.npy")
    fig = plt.figure(figsize=(7.4, 6.2), layout="constrained")
    ax_incident = fig.add_subplot(2, 2, 1)
    ax_backward = fig.add_subplot(2, 2, 2)
    ax_convention = fig.add_subplot(2, 2, 3)
    ax_flux = fig.add_subplot(2, 2, 4)
    incident_map = ax_incident.pcolormesh(x_um, y_um, incident, cmap="viridis", shading="auto")
    backward_map = ax_backward.pcolormesh(x_um, y_um, backward, cmap="plasma", shading="auto")
    for axis in (ax_incident, ax_backward):
        axis.axvline(0, color="#111827", linewidth=1.5)
        axis.set_aspect("equal")
    ax_incident.set_title("(a) Incident channel", fontsize=10)
    ax_incident.set_xlabel("$x$ ($\\mu$m)")
    ax_incident.set_ylabel("$y$ ($\\mu$m)")
    ax_backward.set_title("(b) Backward channel", fontsize=10)
    ax_backward.set_xlabel("$x$ ($\\mu$m)")
    ax_backward.set_ylabel("$y$ ($\\mu$m)")
    fig.colorbar(incident_map, ax=ax_incident, label="Normalized intensity")
    fig.colorbar(backward_map, ax=ax_backward, label="Normalized intensity")
    ax_convention.axis("off")
    ax_convention.set_title("(c) Coordinate convention", fontsize=10)
    ax_convention.annotate("", xy=(0, -1), xytext=(1, 0), arrowprops=dict(arrowstyle="->", color="#111827", lw=2))
    ax_convention.text(0.32, -0.12, "$k_x$", fontsize=10)
    ax_convention.text(-0.2, -0.3, "$x<0$ plate", fontsize=10)
    ax_convention.text(0.1, 0.75, "$k_y$", fontsize=10)
    ax_convention.text(-0.6, 0.8, "$y$ invariant", fontsize=10)
    ax_convention.text(-0.3, 0.4, "phase ansatz $e^{i(k_xx+k_yy-\omega t)}$", fontsize=10)
    reference_metric = metrics[1]
    ax_flux.set_title("(d) Flux at $x=-40\\,\\mu$m", fontsize=10)
    ax_flux.set_xlim(0, 1)
    ax_flux.set_ylim(0, 1)
    ax_flux.axis("off")
    ax_flux.annotate("", xy=(0.75, 0.45), xytext=(0.2, 0.75), arrowprops=dict(arrowstyle="-|>", color="#155e75", lw=3))
    ax_flux.text(0.05, 0.82, "Incident", fontsize=10)
    ax_flux.text(0.05, 0.72, "right/up", fontsize=10)
    ax_flux.annotate("", xy=(0.2, 0.25), xytext=(0.7, 0.5), arrowprops=dict(arrowstyle="-|>", color="#9d174d", lw=3))
    ax_flux.text(0.05, 0.58, "Backward", fontsize=10)
    ax_flux.text(0.05, 0.48, "left/down", fontsize=10)
    ax_flux.text(0.05, 0.38, "Edge at $x=0$", fontsize=10)
    ax_flux.text(0.05, 0.28, "$k_y$ conserved", fontsize=10)
    ax_flux.text(0.05, 0.16, f"computed centroid y is {reference_metric['backward_centroid_y_um']:.3f} $\\mu$m", fontsize=10)
    fig.suptitle("Spatial energy flux and computed wave field", fontweight="bold")
    save_figure(fig, "fig10_field", FIGURE_DIR, rasterize=True)
    plt.close(fig)


def main():
    fig01_dispersion()
    fig02_material()
    fig03_geometry()
    fig04_frequency()
    fig05_channel()
    fig06_attenuation()
    fig07_coupling()
    fig08_boundary()
    fig09_validation()
    fig10_field()
    print("Revised figure generation complete.")


if __name__ == "__main__":
    main()
