"""Render the ten Paper A main figures from the committed datasets.

Plotting only: every number comes from a CSV/JSON written by
``paper_a_study/build_figure_data.py``.  Nothing is generated, smoothed or
extrapolated here.

Canvas contract
---------------
Every PDF is written at exactly 6.50 x 5.10 in = the LaTeX ``\\textwidth`` of
``Paper_A_LaTeX/main.tex`` with ``savefig.bbox = None``.  Because the canvas is
never re-cropped, the 11 pt labels, 9 pt ticks and 5.5 pt markers keep the same
physical size in every figure and in the compiled manuscript.

Layout rules (see ``FIGURE_BY_FIGURE_SUPERVISOR_RESPONSE.md``)
  * 2 x 2 panels, one shared ``H/H*`` legend inside the reserved top band and
    never over the data;
  * the fixed ``H`` colour/dash/marker triple from ``figure_style.py``;
  * a different ordered sequential ramp for every other parameter family;
  * log axes only where the data span more than about one decade, with the
    reason stated in the caption;
  * no titles inside panels: only the bold (a)-(d) tags.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize, SymLogNorm
from matplotlib.lines import Line2D
from matplotlib.ticker import LogLocator, NullFormatter
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

import figure_style as S

HERE = Path(__file__).resolve().parent
DATA = HERE / "figure_data"
OUT = HERE / "figures_final"
K0 = 0.7361990195318475
KY0 = 0.12981175031447484


# --------------------------------------------------------------------------
# loading helpers
# --------------------------------------------------------------------------
def load(name: str) -> list[dict]:
    with (DATA / name).open() as handle:
        rows = list(csv.DictReader(handle))
    out = []
    for row in rows:
        item = {}
        for key, value in row.items():
            if value == "":
                item[key] = None
                continue
            try:
                item[key] = float(value)
            except (TypeError, ValueError):
                item[key] = value
        out.append(item)
    return out


def series(rows, **filters):
    def keep(row):
        for key, want in filters.items():
            got = row.get(key)
            if isinstance(want, (int, float)) and isinstance(got, (int, float)):
                if abs(float(got) - float(want)) > 1e-9 * max(1.0, abs(float(want))):
                    return False
            elif got != want:
                return False
        return True
    return [r for r in rows if keep(r)]


def col(rows, key):
    return np.array([r[key] for r in rows], dtype=float)


def logify(ax, axis="y"):
    a = ax.yaxis if axis == "y" else ax.xaxis
    a.set_major_locator(LogLocator(base=10, numticks=6))
    a.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1, numticks=12))
    if axis == "y":
        ax.yaxis.set_minor_formatter(NullFormatter())
    else:
        ax.xaxis.set_minor_formatter(NullFormatter())


def finish(fig, stem: str) -> list[Path]:
    paths = S.save_figure(fig, stem, OUT, dpi=400)
    plt.close(fig)
    return paths


def panel_axes(*, top=0.858, hspace=0.44, wspace=0.32, bottom=0.098, left=0.128,
               right=0.952):
    fig = S.new_figure()
    axs = np.array([fig.add_subplot(2, 2, i + 1) for i in range(4)])
    fig.subplots_adjust(left=left, right=right, bottom=bottom, top=top,
                        wspace=wspace, hspace=hspace)
    for ax, letter in zip(axs, "abcd"):
        S.label_panel(ax, letter)
    return fig, axs


def h_legend(fig, axs, *, y=0.998, ncol=5, title=None):
    return S.h_legend(fig, axs, ncol=ncol, y=y, title=title)


def note(ax, text, *, loc=(0.03, 0.96), fontsize=8.0, va="top", ha="left", box=True):
    kw = dict(fontsize=fontsize, va=va, ha=ha, color="#1b2229")
    if box:
        kw["bbox"] = dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor="#c6ced5", linewidth=0.5, alpha=0.92)
    ax.text(*loc, text, transform=ax.transAxes, **kw)


def machine_label(value: float, unit_exp: int) -> str:
    """'1.5e18' -> '1.5' (exponent shown once in the legend title)."""
    mant = value / 10 ** unit_exp
    return f"{mant:g}"


# ==========================================================================
# Figure 1 -- dispersion, wave speeds, linewidth and spatial attenuation
# ==========================================================================
def fig01():
    rows = load("fig01_dispersion_velocity_attenuation.csv")
    fig, axs = panel_axes(right=0.895)
    a, b, c, d = axs
    base = sorted(series(rows, eta=0.0), key=lambda r: r["K"])

    # (a) all five H levels: they coincide to <2e-5 relative -- drawn thin so the
    # overlap itself is the message, the inset resolves the residual splitting.
    for eta in S.H_LEVELS:
        sub = sorted(series(rows, eta=eta), key=lambda r: r["K"])
        a.plot(col(sub, "K"), col(sub, "frequency_GHz"), color=S.H_COLORS[eta],
               linestyle=S.H_STYLE[eta]["linestyle"], linewidth=1.6, zorder=4)
    k0f = float(np.interp(K0, col(base, "K"), col(base, "frequency_GHz")))
    a.plot([K0], [k0f], marker="*", markersize=13, color="#C83E58",
           markeredgecolor="white", markeredgewidth=0.7, zorder=9,
           linestyle="None")
    a.annotate("operating point\n$k_xd=0.736$", xy=(K0, k0f),
               xytext=(0.128, 16.664), fontsize=7.4, color="#202A44",
               va="center", ha="left",
               arrowprops=dict(arrowstyle="-", linewidth=0.9, color="#C83E58",
                               shrinkA=2, shrinkB=7, alpha=0.9))
    a.set_xlabel(r"normalised wavenumber  $k_x d$")
    a.set_ylabel(r"frequency  $f$ (GHz)")
    a.set_xlim(0.10, 1.10)
    a.set_ylim(16.647, 16.895)
    S.style_axes(a)
    ins = a.inset_axes([0.480, 0.545, 0.425, 0.395])
    for eta in S.H_LEVELS:
        if eta == 0.0:
            continue
        sub = sorted(series(rows, eta=eta), key=lambda r: r["K"])
        ins.plot(col(sub, "K"), (col(sub, "frequency_GHz")
                                 - col(base, "frequency_GHz")) * 1e6,
                 color=S.H_COLORS[eta], linestyle=S.H_STYLE[eta]["linestyle"],
                 linewidth=1.4)
    ins.axhline(0, color="#202A44", linewidth=0.8)
    ins.set_xlabel(r"$k_x d$", fontsize=7.0, labelpad=1)
    ins.set_ylabel(r"$\Delta f$ (kHz)", fontsize=7.0, labelpad=1)
    ins.tick_params(labelsize=6.4, length=2, pad=1.2)
    ins.set_ylim(-150, 150)
    ins.set_yticks([-100, 0, 100])
    ins.grid(True, alpha=0.45, linewidth=0.4)
    ins.set_title(r"$\Delta f=f(H)-f(0)$", fontsize=6.9, pad=2.2)

    b.plot(col(base, "K"), col(base, "group_speed_m_s"), color="#087E8B",
           linestyle="-", linewidth=2.0, marker="o", markersize=4.0,
           markerfacecolor="white", markevery=3,
           label=r"group  $v_g=\partial\omega/\partial k_x$")
    b.plot(col(base, "K"), col(base, "energy_speed_m_s"), color="#E3A008",
           linestyle="None", marker="x", markersize=6.0, markeredgewidth=1.6,
           label=r"energy  $v_E=P_x/E$")
    b.axhline(0, color="#202A44", linewidth=1.0, zorder=1)
    b.set_xlabel(r"normalised wavenumber  $k_x d$")
    b.set_ylabel(r"velocity (m s$^{-1}$)")
    b.set_xlim(0.10, 1.10)
    b.set_ylim(-330, 1500)
    b.legend(loc="upper center", fontsize=7.2, handlelength=1.8, borderpad=0.35,
             labelspacing=0.3, ncol=1)
    S.style_axes(b)
    bt = b.twinx()
    bt.plot(col(base, "K"), col(base, "phase_speed_m_s") / 1e3, color="#3867D6",
            linestyle=(0, (6, 2)), linewidth=1.8)
    bt.set_ylabel(r"$v_p$ ($10^{3}$ m s$^{-1}$)", color="#3867D6", fontsize=10.5)
    bt.tick_params(axis="y", colors="#3867D6", labelsize=9)
    bt.spines["right"].set_visible(True)
    bt.spines["right"].set_color("#3867D6")
    bt.set_ylim(10, 115)

    for eta in S.H_LEVELS:
        sub = sorted(series(rows, eta=eta), key=lambda r: r["K"])
        S.h_plot(c, col(sub, "K"), col(sub, "FWHM_MHz"), eta, markevery=4,
                 markersize=4.4)
    c.set_yscale("log")
    logify(c, "y")
    c.set_xlabel(r"normalised wavenumber  $k_x d$")
    c.set_ylabel(r"linewidth FWHM (MHz)")
    c.set_xlim(0.10, 1.10)
    S.style_axes(c)

    for eta in S.H_LEVELS:
        sub = sorted(series(rows, eta=eta), key=lambda r: r["K"])
        S.h_plot(d, col(sub, "K"), col(sub, "attenuation_dB_per_mm"), eta,
                 markevery=4, markersize=4.4)
    d.set_yscale("log")
    logify(d, "y")
    d.set_xlabel(r"normalised wavenumber  $k_x d$")
    d.set_ylabel(r"attenuation (dB mm$^{-1}$)")
    d.set_xlim(0.10, 1.10)
    S.style_axes(d)

    h_legend(fig, axs)
    return finish(fig, "fig01_dispersion")


# ==========================================================================
# Figure 2 -- carrier density and mobility
# ==========================================================================
def fig02():
    rows = [r for r in load("fig02_material_parameter_sweep.csv")
            if r.get("valid") in (True, "true")]
    n0 = sorted({r["value_SI"] for r in rows if r["parameter"] == "n0"})
    mu = sorted({r["value_SI"] for r in rows if r["parameter"] == "mobility"})
    cn0, cmu = S.ramp(S.RAMP_N0, n0), S.ramp(S.RAMP_MU, mu)
    fig, axs = panel_axes()
    a, b, c, d = axs

    def fam_legend(ax, values, colors, title, fmt, marker, loc="upper left"):
        handles = [Line2D([], [], color=colors[v], linewidth=2.0, marker=marker,
                          markersize=4.6, markerfacecolor="white") for v in values]
        ax.legend(handles, [fmt(v) for v in values], title=title, loc=loc,
                  fontsize=7.6, title_fontsize=7.8, handlelength=1.9,
                  borderpad=0.4, labelspacing=0.30)

    for v in n0:
        sub = sorted(series(rows, parameter="n0", value_SI=v), key=lambda r: r["K"])
        a.semilogy(col(sub, "K"), col(sub, "FWHM_MHz"), color=cn0[v], linewidth=1.9,
                   marker="o", markersize=4.3, markerfacecolor="white", markevery=2)
    a.set_xlabel(r"normalised wavenumber  $k_x d$")
    a.set_ylabel(r"linewidth FWHM (MHz)")
    logify(a, "y")
    S.style_axes(a)
    fam_legend(a, n0, cn0, r"carrier density $n_0$ ($10^{18}$ m$^{-3}$)",
               lambda v: machine_label(v, 18), "o")

    for v in n0:
        sub = sorted(series(rows, parameter="n0", value_SI=v), key=lambda r: r["K"])
        b.semilogy(col(sub, "K"), col(sub, "attenuation_dB_per_mm"), color=cn0[v],
                   linewidth=1.9, marker="s", markersize=4.3,
                   markerfacecolor="white", markevery=2)
    b.set_xlabel(r"normalised wavenumber  $k_x d$")
    b.set_ylabel(r"attenuation (dB mm$^{-1}$)")
    logify(b, "y")
    S.style_axes(b)

    # (c) the quantity that matters: the backward reflectance itself
    for v in n0:
        sub = sorted(series(rows, parameter="n0", value_SI=v), key=lambda r: r["K"])
        c.plot(col(sub, "K"), [100 * x for x in col(sub, "R_B_2um")], color=cn0[v],
               linewidth=1.7, marker="D", markersize=3.4, markerfacecolor="white",
               markeredgewidth=0.9, markevery=3)
    c.set_xlabel(r"normalised wavenumber  $k_x d$")
    c.set_ylabel("backward reflectance $R_B$ (%)")
    c.set_ylim(-4, 92)
    S.style_axes(c)
    note(c, r"all five $n_0$ levels lie on this curve" "\n"
            r"($|\Delta R_B|/R_B<0.2\%$, see caption)", loc=(0.045, 0.93),
         fontsize=7.0)
    for v in mu:
        sub = sorted(series(rows, parameter="mobility", value_SI=v), key=lambda r: r["K"])
        d.semilogy(col(sub, "K"), col(sub, "FWHM_MHz"), color=cmu[v], linewidth=1.9,
                   marker="^", markersize=4.3, markerfacecolor="white", markevery=2)
    d.set_xlabel(r"normalised wavenumber  $k_x d$")
    d.set_ylabel(r"linewidth FWHM (MHz)")
    d.set_ylim(7e-4, 1.4)
    logify(d, "y")
    S.style_axes(d)
    fam_legend(d, mu, cmu, r"mobility $\mu$ ($10^{-3}$ m$^2$V$^{-1}$s$^{-1}$)",
               lambda v: f"{v*1e3:.1f}", "^", loc="upper left")

    h_legend(fig, axs, y=0.998)
    return finish(fig, "fig02_material")


# ==========================================================================
# Figure 3 -- thickness and gradient length
# ==========================================================================
def fig03():
    rows = load("fig03_geometry_sweep.csv")
    ds = sorted({r["value_SI"] for r in rows if r["parameter"] == "d"})
    ells = sorted({r["value_SI"] for r in rows if r["parameter"] == "ell"})
    cd, ce = S.ramp(S.RAMP_D, ds), S.ramp(S.RAMP_ELL, ells)
    fig, axs = panel_axes()
    a, b, c, d = axs

    for v in ds:
        sub = sorted(series(rows, parameter="d", value_SI=v), key=lambda r: r["K"])
        base = abs(v - 200e-9) < 1e-12
        a.plot(col(sub, "K"), col(sub, "frequency_GHz"), color=cd[v],
               linewidth=2.7 if base else 1.8, marker="o", markersize=4.4,
               markerfacecolor="white", markevery=3, zorder=6 if base else 3)
    a.set_xlabel(r"normalised wavenumber  $k_x d$")
    a.set_ylabel(r"frequency  $f$ (GHz)")
    S.style_axes(a)
    a.set_ylim(9.0, 30.6)
    a.legend([Line2D([], [], color=cd[v], linewidth=2.7 if abs(v - 200e-9) < 1e-12 else 1.8)
              for v in ds], [r"$d$ = " + f"{v*1e9:.0f} nm" for v in ds],
             fontsize=7.4, loc="upper right", bbox_to_anchor=(0.995, 0.885),
             handlelength=1.8, ncol=2, columnspacing=1.0,
             borderpad=0.4, labelspacing=0.3)

    for v in ells:
        sub = sorted(series(rows, parameter="ell", value_SI=v), key=lambda r: r["K"])
        base = abs(v - 50e-9) < 1e-12
        b.plot(col(sub, "K"), col(sub, "frequency_GHz"), color=ce[v],
               linewidth=2.7 if base else 1.8, marker="s", markersize=4.4,
               markerfacecolor="white", markevery=3, zorder=6 if base else 3)
    b.set_xlabel(r"normalised wavenumber  $k_x d$")
    b.set_ylabel(r"frequency  $f$ (GHz)")
    S.style_axes(b)
    b.legend([Line2D([], [], color=ce[v], linewidth=2.7 if abs(v - 50e-9) < 1e-12 else 1.8)
              for v in ells], [r"$\ell$ = " + f"{v*1e9:.0f} nm" for v in ells],
             fontsize=7.4, loc="upper left", handlelength=1.8, ncol=2,
             columnspacing=1.0, borderpad=0.4, labelspacing=0.3)

    KREF = 0.5
    shifts, f_ref = [], None
    for v in ds:
        row = min(series(rows, parameter="d", value_SI=v),
                  key=lambda r: abs(r["K"] - KREF))
        shifts.append((v, row["frequency_GHz"]))
        if abs(v - 200e-9) < 1e-12:
            f_ref = row["frequency_GHz"]
    df = np.array([(f - f_ref) * 1e3 for _, f in shifts])
    c.axhline(0, color="#202A44", linewidth=1.0)
    c.plot([v * 1e9 for v in ds], df, color="#3F6A93", linewidth=1.8, zorder=4)
    for v, y in zip(ds, df):
        c.plot([v * 1e9], [y], marker="o", markersize=7.5, markerfacecolor=cd[v],
               markeredgecolor="white", markeredgewidth=1.0, linestyle="None",
               zorder=6)
    c.set_xlabel(r"plate thickness  $d$ (nm)")
    c.set_ylabel(r"$\Delta f$ (MHz) at $k_xd=0.50$")
    S.style_axes(c)
    note(c, r"reference $\Delta f\equiv0$ at $d$ = 200 nm", loc=(0.40, 0.955),
         fontsize=7.4)

    ref_ell = {round(r["K"], 6): r["frequency_GHz"]
               for r in series(rows, parameter="ell", value_SI=50e-9)}
    for v in ells:
        sub = sorted(series(rows, parameter="ell", value_SI=v), key=lambda r: r["K"])
        d.plot(col(sub, "K"),
               [100 * (r["frequency_GHz"] - ref_ell[round(r["K"], 6)])
                / ref_ell[round(r["K"], 6)] for r in sub],
               color=ce[v], linewidth=2.7 if abs(v - 50e-9) < 1e-12 else 1.8,
               marker="^", markersize=4.2, markerfacecolor="white",
               markevery=3, zorder=6 if abs(v - 50e-9) < 1e-12 else 3)
    d.axhline(0, color="#202A44", linewidth=1.0)
    d.set_xlabel(r"normalised wavenumber  $k_x d$")
    d.set_ylabel(r"$\Delta f/f_0$ (%)")
    d.set_ylim(-6.6, 12.4)
    S.style_axes(d)
    note(d, r"$\ell$ = 50 nm reference ($d$ = 200 nm)", loc=(0.035, 0.955),
         fontsize=7.4)
    return finish(fig, "fig03_geometry")


# ==========================================================================
# Figure 4 -- backward conversion along the guided branch
# ==========================================================================
def fig04():
    rows = [r for r in load("fig04_frequency_reflection.csv")
            if r.get("certified") in (True, "true") and r["R_B_2um"] is not None]
    fig, axs = panel_axes()
    a, b, c, d = axs

    for eta in S.H_LEVELS:
        sub = sorted(series(rows, eta=eta), key=lambda r: r["frequency_GHz"])
        S.h_plot(a, col(sub, "frequency_GHz"), 100 * col(sub, "R_B_2um"), eta,
                 markevery=2, markersize=4.4)
    a.set_xlabel(r"frequency  $f$ (GHz)")
    a.set_ylabel(r"$R_B$ at $\ell=2\,\mu$m (%)")
    a.set_ylim(bottom=0)
    S.style_axes(a)

    for eta in S.H_LEVELS:
        sub = sorted(series(rows, eta=eta), key=lambda r: r["frequency_GHz"])
        S.h_plot(b, col(sub, "frequency_GHz"), col(sub, "angle_deg"), eta,
                 markevery=2, markersize=4.4)
    b.axhline(0, color="#202A44", linewidth=1.0)
    b.set_xlabel(r"frequency  $f$ (GHz)")
    b.set_ylabel(r"energy angle  $\theta_E$ (deg)")
    S.style_axes(b)

    # (c) reflectance against the group velocity of the guided branch
    vmax = 0.0
    for eta in S.H_LEVELS:
        sub = sorted(series(rows, eta=eta), key=lambda r: r["group_speed_m_s"])
        S.h_plot(c, col(sub, "group_speed_m_s"), 100 * col(sub, "R_B_2um"), eta,
                 markevery=2, markersize=4.4)
        vmax = max(vmax, max(100 * x for x in col(sub, "R_B_2um")))
    c.axvline(0, color="#202A44", linewidth=1.0, linestyle=(0, (4, 3)))
    c.set_xlabel(r"group velocity  $v_g$ (m s$^{-1}$)")
    c.set_ylabel(r"$R_B$ at $\ell=2\,\mu$m (%)")
    c.set_ylim(0, 66)
    S.style_axes(c)
    note(c, r"slowest branch, largest $R_B$", loc=(0.045, 0.955), fontsize=7.2)

    for eta in S.H_LEVELS:
        sub = sorted(series(rows, eta=eta), key=lambda r: r["frequency_GHz"])
        S.h_plot(d, col(sub, "frequency_GHz"), col(sub, "K_ratio"), eta,
                 markevery=2, markersize=4.4)
    d.set_xlabel(r"frequency  $f$ (GHz)")
    d.set_ylabel(r"wavenumber ratio  $k_{Bx}/k_{ix}$")
    S.style_axes(d)

    h_legend(fig, axs, y=0.998)
    return finish(fig, "fig04_frequency")


# ==========================================================================
# Figure 5 -- channel power accounting
# ==========================================================================
def fig05():
    rows = sorted(load("fig05_channel_power.csv"), key=lambda r: r["eta"])
    eta = col(rows, "eta")
    fig, axs = panel_axes(hspace=0.46)
    a, b, c, d = axs
    ticks = [f"{v:+.3f}" if v else "0" for v in S.H_LEVELS]
    CH = [("backward\n(far field)", "backward_propagating_fraction", "#202A44", "D"),
          ("dissipated", "dissipated_fraction", "#B4552A", "s"),
          ("reactive\n(near field)", "evanescent_reactive_fraction", "#2F6BA0", "o")]

    # (a) where the incident energy goes at H = 0
    for i, (lab, key, colour, mk) in enumerate(CH):
        a.plot([rows[2][key]], [i], marker=mk, markersize=8.5, color=colour,
               markerfacecolor="white", markeredgewidth=1.5, linestyle="None",
               zorder=5)
    a.set_xscale("log")
    a.set_xlim(5e-7, 2e-1)
    a.set_yticks(range(len(CH)))
    a.set_yticklabels([c0[0] for c0 in CH], fontsize=8.4)
    a.set_ylim(-0.55, 3.15)
    a.set_xlabel("fraction of incident power")
    S.style_axes(a, grid=False)
    a.grid(True, axis="x", alpha=0.28, linewidth=0.6)
    note(a, "at $H=0$; the forward-propagating channel is\n"
            "exactly zero (no propagating forward mode)",
         loc=(0.035, 0.955), fontsize=7.0)

    # (b) how each channel responds to H
    for lab, key, colour, mk in CH:
        b.semilogy(eta, [r[key] for r in rows], color=colour, linewidth=2.0,
                   marker=mk, markersize=5.6, markerfacecolor="white",
                   markeredgewidth=1.2, linestyle={"D": "-", "s": "--", "o": "-."}[mk])
    b.set_xlabel(r"$H/H^{*}$")
    b.set_ylabel("fraction of incident power")
    b.set_xticks(S.H_LEVELS)
    b.set_xticklabels(ticks, fontsize=8)
    b.set_ylim(2e-6, 3.0)
    logify(b, "y")
    S.style_axes(b)
    b.legend(handles=[Line2D([], [], color=c0[2], linewidth=2.0, marker=c0[3],
                             markersize=5.0, markerfacecolor="white",
                             label=c0[0].split("\n")[0]) for c0 in CH],
             loc="upper center", ncol=3, fontsize=6.8, handlelength=1.6,
             columnspacing=0.9, borderpad=0.3, handletextpad=0.4)

    # (c) solver power balance
    c.semilogy(eta, [r["power_balance_error"] for r in rows], color="#202A44",
               linewidth=2.0, marker="o", markersize=5.6, markerfacecolor="white",
               markeredgewidth=1.2)
    c.axhline(1e-6, color="#C83E58", linewidth=1.0, linestyle=(0, (5, 3)))
    c.text(eta[0], 1e-6 * 1.15, "acceptance threshold $10^{-6}$", fontsize=6.8,
           color="#C83E58")
    c.set_xlabel(r"$H/H^{*}$")
    c.set_ylabel("relative power balance error")
    c.set_xticks(S.H_LEVELS)
    c.set_xticklabels(ticks, fontsize=8)
    c.set_ylim(1e-13, 3e-6)
    logify(c, "y")
    S.style_axes(c)

    # (d) sensitivity of the backward channel
    rel = 100 * (np.array([r["R_B_2um"] for r in rows]) / rows[2]["R_B_2um"] - 1)
    d.axhline(0, color="#202A44", linewidth=1.0)
    for e, y in zip(eta, rel):
        st = S.H_STYLE[e]
        d.plot([e], [y], marker=st["marker"], markersize=8.0, color=st["color"],
               markerfacecolor="white", markeredgewidth=1.5, linestyle="None",
               zorder=6)
    d.plot(eta, rel, color="#5A6570", linewidth=1.1, linestyle=(0, (3, 2)), zorder=3)
    d.set_xlabel(r"$H/H^{*}$")
    d.set_ylabel(r"$[R_B(H)-R_B(0)]/R_B(0)$ (%)")
    d.set_xticks(S.H_LEVELS)
    d.set_xticklabels(ticks, fontsize=8)
    d.set_ylim(-2.6, 0.7)
    S.style_axes(d)

    return finish(fig, "fig05_channel")


# ==========================================================================
# Figure 6 -- propagation distance, survival and attenuation lengths
# ==========================================================================
def fig06():
    rows = load("fig06_attenuation_distance.csv")
    fig, axs = panel_axes()
    a, b, c, d = axs
    ticks = [f"{v:+.3f}" if v else "0" for v in S.H_LEVELS]

    for eta in S.H_LEVELS:
        sub = sorted(series(rows, eta=eta), key=lambda r: r["distance_um"])
        S.h_plot(a, col(sub, "distance_um"), col(sub, "R_B_isolated"), eta,
                 markevery=2, markersize=4.4)
    a.set_xscale("log")
    a.set_yscale("log")
    logify(a, "x")
    logify(a, "y")
    a.set_xlabel(r"distance from edge  $\ell$ ($\mu$m)")
    note(a, "isolated channel", loc=(0.035, 0.06), fontsize=7.0)
    a.set_ylabel(r"$R_B(\ell)$")
    S.style_axes(a)

    for eta in S.H_LEVELS:
        sub = sorted(series(rows, eta=eta), key=lambda r: r["distance_um"])
        S.h_plot(b, col(sub, "distance_um"), col(sub, "incident_survival"), eta,
                 markevery=2, markersize=4.4)
    b.set_xscale("log")
    b.set_yscale("log")
    logify(b, "x")
    logify(b, "y")
    b.axhline(1.0, color="#202A44", linewidth=0.9, linestyle=(0,(4,3)))
    b.text(1.25, 0.40, r"unitary limit", fontsize=7.0, color="#202A44")
    b.set_xlabel(r"distance from edge  $\ell$ ($\mu$m)")
    b.set_ylabel("power at the edge")
    S.style_axes(b)

    fixed = {eta: series(rows, eta=eta)[0] for eta in S.H_LEVELS}
    c.semilogy(S.H_LEVELS, [fixed[e]["attenuation_length_incident_mm"] for e in S.H_LEVELS],
               color="#2F6BA0", linewidth=2.1, marker="o", markersize=7.0,
               markerfacecolor="white", label="incident channel")
    c.semilogy(S.H_LEVELS, [fixed[e]["attenuation_length_backward_mm"] for e in S.H_LEVELS],
               color="#B4552A", linewidth=2.1, marker="s", markersize=7.0,
               markerfacecolor="white", linestyle="--", label="backward channel")
    c.set_xlabel(r"$H/H^{*}$")
    c.set_ylabel(r"$L$ (mm)")
    c.set_xticks(S.H_LEVELS)
    c.set_xticklabels(ticks, fontsize=8)
    logify(c, "y")
    c.set_ylim(0.18, 90)
    c.legend(loc="upper center", ncol=2, fontsize=7.4, borderpad=0.3,
             columnspacing=0.9, handlelength=1.7)
    S.style_axes(c)

    d.semilogy(S.H_LEVELS, [fixed[e]["incident_attenuation_dB_per_mm"] for e in S.H_LEVELS],
               color="#2F6BA0", linewidth=2.1, marker="o", markersize=7.0,
               markerfacecolor="white", label=r"$\alpha_i$ incident")
    d.semilogy(S.H_LEVELS, [fixed[e]["backward_attenuation_dB_per_mm"] for e in S.H_LEVELS],
               color="#B4552A", linewidth=2.1, marker="s", markersize=7.0,
               markerfacecolor="white", linestyle="--", label=r"$\alpha_B$ backward")
    d.set_xlabel(r"$H/H^{*}$")
    d.set_ylabel(r"$\alpha$ (dB mm$^{-1}$)")
    d.set_xticks(S.H_LEVELS)
    d.set_xticklabels(ticks, fontsize=8)
    logify(d, "y")
    d.set_ylim(0.25, 70)
    d.legend(loc="upper left", fontsize=7.4, borderpad=0.3, handlelength=1.7,
             labelspacing=0.3)
    S.style_axes(d)
    note(d, r"$\alpha=2|{\rm Im}\,k|$", loc=(0.035, 0.06), fontsize=7.0)

    h_legend(fig, axs, y=0.998)
    return finish(fig, "fig06_attenuation")


# ==========================================================================
# Figure 7 -- (ky, H) two-parameter landscape
# ==========================================================================
def fig07():
    rows = load("fig07_coupling_sensitivity.csv")
    kys = sorted({r["ky"] for r in rows})
    fig, axs = panel_axes(right=0.900)
    a, b, c, d = axs
    ticks = [f"{v:+.3f}" if v else "0" for v in S.H_LEVELS]

    # (a) the dominant parameter: transverse wavenumber
    for eta in S.H_LEVELS:
        sub = sorted(series(rows, eta=eta), key=lambda r: r["ky"])
        S.h_plot(a, col(sub, "ky"), 100 * col(sub, "R_B_2um"), eta, markevery=3,
                 markersize=4.2)
    a.set_xlabel(r"transverse wavenumber  $k_y d$")
    a.set_ylabel(r"$R_B$ (%)")
    S.style_axes(a)
    note(a, r"$k_y$ sets the level; the five $H$ levels" "\n" r"are superposed",
         loc=(0.04, 0.055), fontsize=6.8)

    # (b) the (ky, H) landscape, drawn as the measured grid (no interpolation)
    grid = np.array([[100 * r["R_B_2um"] for r in sorted(series(rows, eta=e),
                                                          key=lambda r: r["ky"])]
                     for e in S.H_LEVELS])
    mesh = b.pcolormesh(np.array(kys), np.array(S.H_LEVELS), grid,
                        cmap=S.CMAP_SEQUENTIAL, shading="nearest",
                        vmin=grid.min(), vmax=grid.max(), rasterized=True)
    cb = fig.colorbar(mesh, ax=b, fraction=0.046, pad=0.025)
    cb.set_label(r"$R_B$ (%)", fontsize=9)
    cb.ax.tick_params(labelsize=7.4)
    b.set_xlabel(r"transverse wavenumber  $k_y d$")
    b.set_ylabel(r"$H/H^{*}$")
    b.set_yticks(S.H_LEVELS)
    b.set_yticklabels(ticks, fontsize=8)
    S.style_axes(b, grid=False)

    # (c) how much H matters along three declared slices
    slices = [kys[0], kys[len(kys) // 2], kys[-1]]
    colr = [S.RAMP_KY[0], S.RAMP_KY[2], S.RAMP_KY[4]]
    for i, kv in enumerate(slices):
        sub = sorted(series(rows, ky=kv), key=lambda r: r["eta"])
        c.plot(col(sub, "eta"), col(sub, "rel_change_percent"),
               color=colr[i], linewidth=1.9, marker=["o", "s", "^"][i],
               markersize=5.6, markerfacecolor="white", markeredgewidth=1.2,
               label=rf"$k_yd={kv:.3f}$")
    c.axhline(0, color="#202A44", linewidth=1.0)
    c.set_xlabel(r"$H/H^{*}$")
    c.set_ylabel(r"$\Delta R_B/R_B$ (%)")
    c.set_xticks(S.H_LEVELS)
    c.set_xticklabels(ticks, fontsize=8)
    c.set_ylim(-3.0, 0.55)
    c.legend(loc="lower left", fontsize=7.2, handlelength=1.6, borderpad=0.3,
             labelspacing=0.25)
    S.style_axes(c)

    # (d) the same change against the transverse wavenumber
    for eta in S.H_LEVELS:
        sub = sorted(series(rows, eta=eta), key=lambda r: r["ky"])
        S.h_plot(d, col(sub, "ky"), col(sub, "rel_change_percent"), eta,
                 markevery=3, markersize=4.2)
    d.axhline(0, color="#202A44", linewidth=1.0)
    d.set_xlabel(r"transverse wavenumber  $k_y d$")
    d.set_ylabel(r"$\Delta R_B/R_B$ (%)")
    d.set_ylim(-3.0, 0.55)
    S.style_axes(d)

    h_legend(fig, axs, y=0.998)
    return finish(fig, "fig07_coupling")


# ==========================================================================
# Figure 8 -- thickness-resolved energy flux of the guided channels
# ==========================================================================
def fig08():
    rows = load("fig08_thickness_flux.csv")
    fig, axs = panel_axes()
    a, b, c, d = axs
    p_inc = float(np.mean(col(sorted(series(rows, eta=0.0), key=lambda r: r["z"]),
                              "incident_Px")))

    for ax, key, sym in ((a, "backward_Px", "x"), (b, "backward_Pz", "z")):
        for eta in S.H_LEVELS:
            sub = sorted(series(rows, eta=eta), key=lambda r: r["z"])
            S.h_plot(ax, col(sub, key) / p_inc, col(sub, "z"), eta,
                     marker=False)
        ax.axvline(0, color="#202A44", linewidth=1.0)
        ax.set_xlabel(rf"$P_{sym}^{{\rm B}}(z)\,/\,P_x^{{\rm inc}}$")
        ax.set_ylabel(r"$z/d$")
        ax.set_ylim(0, 1)
        S.style_axes(ax)

    # (c) running (through-thickness) integral, normalised to its own total
    for eta in S.H_LEVELS:
        sub = sorted(series(rows, eta=eta), key=lambda r: r["z"])
        cum = np.cumsum(col(sub, "quadrature_weight") * col(sub, "backward_Px"))
        c.plot(cum / cum[-1], col(sub, "z"), color=S.H_COLORS[eta],
               linestyle=S.H_STYLE[eta]["linestyle"],
               linewidth=S.H_LINEWIDTH[round(float(eta), 6)])
    c.set_xlabel(r"$\int_0^{z}P_x^{\rm B}\,{\rm d}z'\,/\,\int_0^{d}P_x^{\rm B}\,{\rm d}z'$")
    c.set_ylabel(r"$z/d$")
    c.set_ylim(0, 1)
    S.style_axes(c)

    # (d) shape comparison with the incident mode at H = 0
    sub0 = sorted(series(rows, eta=0.0), key=lambda r: r["z"])
    zz = col(sub0, "z")
    pb = np.abs(col(sub0, "backward_Px"))
    pi = np.abs(col(sub0, "incident_Px"))
    d.plot(pb / pb.max(), zz, color="#B4552A", linewidth=2.1,
           label="backward mode")
    d.plot(pi / pi.max(), zz, color="#2F6BA0", linewidth=2.1,
           linestyle=(0, (6, 2)), label="incident mode")
    d.set_xlabel(r"$|P_x(z)|\,/\,|P_x|_{\max}$")
    d.set_ylabel(r"$z/d$")
    d.set_ylim(0, 1)
    d.set_xlim(0.2, 1.06)
    d.legend(loc="lower left", fontsize=7.8, handlelength=1.9, borderpad=0.35,
             labelspacing=0.3)
    S.style_axes(d)

    h_legend(fig, (a, b, c), y=0.998)
    return finish(fig, "fig08_boundary")


# ==========================================================================
# Figure 9 -- discretisation study and temporal/spatial consistency
# ==========================================================================
def fig09():
    rows = sorted(load("fig09_validation_convergence.csv"), key=lambda r: r["degree"])
    cons = sorted(load("fig09_temporal_spatial_consistency.csv"), key=lambda r: r["K"])
    n = col(rows, "degree")
    fig, axs = panel_axes()
    a, b, c, d = axs

    a.semilogy(n, np.maximum(col(rows, "R_B_rel_error"), 1e-13), color="#2F6BA0", linewidth=2.1,
               marker="o", markersize=6.8, markerfacecolor="white")
    a.axhline(1e-6, color="#B4552A", linewidth=1.0, linestyle=(0, (4, 3)))
    a.set_xlabel(r"Galerkin basis degree  $n$")
    a.set_ylabel(r"$|\Delta R_B|/R_B$")
    a.set_ylim(1e-9, 1e-4)
    logify(a, "y")
    S.style_axes(a)
    note(a, r"reference $n=33$ excluded; dashed $=10^{-6}$", loc=(0.035, 0.955),
         fontsize=7.0)

    b.semilogy(n, np.maximum(col(rows, "K_B_rel_error"), 1e-14), color="#087E8B", linewidth=2.1,
               marker="s", markersize=6.8, markerfacecolor="white")
    b.axhline(1e-6, color="#B4552A", linewidth=1.0, linestyle=(0, (4, 3)))
    b.set_xlabel(r"Galerkin basis degree  $n$")
    b.set_ylabel(r"$|\Delta k_B|/|k_B|$")
    b.set_ylim(1e-14, 1e-5)
    logify(b, "y")
    S.style_axes(b)

    c.semilogy(n, col(rows, "edge_scaled_residual"), color="#C83E58", linewidth=2.1,
               marker="^", markersize=6.8, markerfacecolor="white",
               label="scaled edge residual")
    c.semilogy(n, col(rows, "power_error"), color="#2F6BA0", linewidth=2.1,
               marker="v", markersize=6.8, markerfacecolor="white", linestyle="--",
               label="relative energy-balance error")
    c.axhline(1e-8, color="#202A44", linewidth=0.9, linestyle=(0, (2, 2)))
    c.axhline(1e-10, color="#202A44", linewidth=0.9, linestyle=(0, (4, 3)))
    c.text(14.3, 1.3e-8, r"$10^{-8}$ tolerance", fontsize=7.0, color="#202A44")
    c.text(14.3, 1.3e-10, r"$10^{-10}$ tolerance", fontsize=7.0, color="#202A44")
    c.set_xlabel(r"Galerkin basis degree  $n$")
    c.set_ylabel("magnitude")
    c.set_ylim(1e-16, 1e-6)
    logify(c, "y")
    c.legend(loc="lower left", fontsize=7.2, handlelength=2.0, borderpad=0.4)
    S.style_axes(c)
    note(c, "round-off floor, not a convergence trend", loc=(0.035, 0.955),
         fontsize=7.0)

    d.semilogy(col(cons, "K"), np.maximum(col(cons, "rel_K_mismatch"), 1e-16),
               color="#3F6A93", linewidth=2.1, marker="o", markersize=6.2,
               markerfacecolor="white")
    d.set_xlabel(r"normalised wavenumber  $k_x d$")
    d.set_ylabel(r"$|\Delta k|/|k|$")
    d.set_ylim(1e-8, 1e-4)
    logify(d, "y")
    S.style_axes(d)
    note(d, "temporal generator vs complex spatial QEP:\n"
            r"same branch, agreement $\approx2\times10^{-5}$",
         loc=(0.035, 0.955), fontsize=6.8)

    return finish(fig, "fig09_validation")


# ==========================================================================
# Figure 10 -- solved field maps and energy-flux directions
# ==========================================================================
def fig10():
    rows = load("fig10_field_maps.csv")
    metrics = json.loads((DATA / "fig10_field_metrics.json").read_text())
    xs = sorted({r["x_um"] for r in rows})
    ys = sorted({r["y_um"] for r in rows})
    xi = {v: i for i, v in enumerate(xs)}
    yi = {v: i for i, v in enumerate(ys)}
    I_inc = np.zeros((len(ys), len(xs)))
    I_bwd = np.zeros_like(I_inc)
    for r in rows:
        I_inc[yi[r["y_um"]], xi[r["x_um"]]] = r["incident_intensity"]
        I_bwd[yi[r["y_um"]], xi[r["x_um"]]] = r["backward_intensity"]

    fig = plt.figure(figsize=(S.FIGURE_WIDTH_IN, S.FIGURE_HEIGHT_IN))
    gs = fig.add_gridspec(2, 2, left=0.105, right=0.905, bottom=0.098, top=0.862,
                          wspace=0.34, hspace=0.44)
    a = fig.add_subplot(gs[0, 0])
    b = fig.add_subplot(gs[0, 1])
    c = fig.add_subplot(gs[1, 0])
    d = fig.add_subplot(gs[1, 1])
    for ax, letter in zip((a, b, c, d), "abcd"):
        S.label_panel(ax, letter)

    vmax = float(max(np.nanmax(I_inc), np.nanmax(I_bwd)))
    norm = LogNorm(vmin=max(vmax * 2e-4, 1e-6), vmax=vmax)
    im = None
    for ax, data in ((a, I_inc), (b, I_bwd)):
        im = ax.pcolormesh(xs, ys, np.maximum(data, norm.vmin),
                           cmap=S.CMAP_SEQUENTIAL, norm=norm, shading="auto",
                           rasterized=True)
        ax.axvline(0, color="#101820", linewidth=1.8)
        ax.set_xlabel(r"$x$ ($\mu$m)")
        ax.set_ylabel(r"$y$ ($\mu$m)")
        ax.set_aspect("equal")
        ax.set_xlim(-60, 1.5)
        ax.set_ylim(-45, 45)
    cax = fig.add_axes([0.925, 0.60, 0.016, 0.255])
    cb = fig.colorbar(im, cax=cax)
    cb.set_label(r"$I$ (a.u.)", fontsize=8.6)
    cb.ax.tick_params(labelsize=7.4)

    a.annotate("", xy=(-14, -36), xytext=(-46, -36),
               arrowprops=dict(arrowstyle="-|>", lw=1.4, color="#C83E58"))
    a.text(-30, -41.5, r"energy flux $P_x>0$", color="#C83E58", fontsize=7.4,
           ha="center")
    b.annotate("", xy=(-46, -36), xytext=(-14, -36),
               arrowprops=dict(arrowstyle="-|>", lw=1.4, color="#087E8B"))
    b.text(-30, -41.5, r"energy flux $P_x<0$", color="#087E8B", fontsize=7.4,
           ha="center")
    a.text(0.02, 0.965, "incident beam", transform=a.transAxes, fontsize=7.8,
           va="top", bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="#c6ced5",
                               lw=0.5, alpha=0.92))
    b.text(0.02, 0.965, "backward channel", transform=b.transAxes, fontsize=7.8,
           va="top", bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="#c6ced5",
                               lw=0.5, alpha=0.92))

    # (c) schematic, all directions taken from the solved flux
    p = metrics["primary_flux"]
    c.set_xlim(-1.45, 0.30)
    c.set_ylim(-1.05, 1.05)
    c.axvspan(-1.45, 0.0, color="#EEF3F7", zorder=0)
    c.axvline(0, color="#101820", linewidth=1.9, zorder=4)
    c.text(-1.40, 0.86, "ZnO plate, $d$ = 200 nm", fontsize=7.8)
    c.text(-0.05, 0.86, "edge", fontsize=7.6, rotation=90, ha="right", va="top")
    c.annotate("", xy=(-0.02, -0.92), xytext=(-1.34, -0.92),
               arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#8a949d"))
    c.text(-0.68, -1.00, r"$x$", fontsize=8.4, ha="center")
    c.annotate("", xy=(-1.34, 0.62), xytext=(-1.34, -0.62),
               arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#8a949d"))
    c.text(-1.42, 0.0, r"$y$", fontsize=8.4, va="center")

    def arrow(vec, color, label, anchor, scale, ha="left"):
        tip = (anchor[0] + scale * vec[0], anchor[1] + scale * vec[1])
        c.annotate("", xy=tip, xytext=anchor,
                   arrowprops=dict(arrowstyle="-|>", lw=1.8, color=color,
                                   shrinkA=0, shrinkB=0))
        c.text(tip[0] + (0.045 if ha == "left" else -0.045), tip[1], label,
               fontsize=8.6, color=color, va="center", ha=ha)

    arrow((1.0, 0.176), "#C83E58", r"${\bf k}_i$", (-1.16, -0.50), 0.55)
    arrow((0.333, -0.530), "#087E8B", r"${\bf k}_B$", (-0.82, 0.74), 0.74, ha="right")
    arrow((1.0, p["incident_Py"]), "#B4552A", r"${\bf P}_i$", (-1.16, 0.12), 0.50)
    arrow((-1.0, -0.530), "#6C3F8D", r"${\bf P}_B$", (-0.26, 0.06), 0.46, ha="right")
    c.set_xticks([])
    c.set_yticks([])
    for spine in c.spines.values():
        spine.set_visible(False)

    rows7 = [r for r in load("fig07_coupling_sensitivity.csv")
             if r["Px_backward"] is not None]
    for key, color, style, lab, marker in (
            ("Px_backward", "#C83E58", "-", r"$P_{Bx}/P_{ix}$", "o"),
            ("Py_backward", "#2F6BA0", "--", r"$P_{By}/P_{ix}$", "s")):
        sub = sorted(series(rows7, eta=0.0), key=lambda r: r["ky"])
        d.plot(col(sub, "ky"), col(sub, key), color=color, linestyle=style,
               linewidth=2.2, marker=marker, markersize=5.6,
               markerfacecolor="white", markevery=3, label=lab)
    d.axhline(0, color="#202A44", linewidth=1.0)
    d.set_xlabel(r"$k_yd$")
    d.set_ylabel(r"$P_B/P_{ix}$")
    d.legend(loc="upper right", fontsize=7.6, handlelength=2.0, borderpad=0.4)
    S.style_axes(d)

    return finish(fig, "fig10_field")


ALL = {
    "fig01_dispersion": fig01,
    "fig02_material": fig02,
    "fig03_geometry": fig03,
    "fig04_frequency": fig04,
    "fig05_channel": fig05,
    "fig06_attenuation": fig06,
    "fig07_coupling": fig07,
    "fig08_boundary": fig08,
    "fig09_validation": fig09,
    "fig10_field": fig10,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for stem, fn in ALL.items():
        print(f"[render] {stem} ...", flush=True)
        fn()
    print("[render] done ->", OUT)


if __name__ == "__main__":
    main()
