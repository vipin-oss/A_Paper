"""Single publication style for all Paper A figures.

Times New Roman was not installed in the build environment. DejaVu Serif is the
metrically compatible serif fallback used by Matplotlib; no font binary is
packaged. Every export uses the same fonts, geometry, color cycle and units.
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from cycler import cycler

# Serif fallback is explicit and globally recorded.
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Liberation Serif", "Nimbus Roman"],
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.labelweight": "bold",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "figure.titlesize": 12,
    "figure.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "axes.prop_cycle": cycler(color=[
        "#155e75", "#cc642f", "#16806a", "#8b5cf6", "#b45309", "#0369a1", "#9d174d"
    ]),
    "lines.linewidth": 2.0,
    "lines.linestyle": "-",
    "lines.markersize": 5,
    "lines.marker": "",
    "grid.color": "#dbe4ea",
    "grid.linewidth": 0.6,
    "grid.alpha": 0.75,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.size": 3.0,
    "ytick.major.size": 3.0,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "legend.frameon": True,
    "legend.framealpha": 0.92,
    "legend.edgecolor": "#9aa7b0",
    "legend.fancybox": False,
    "legend.borderpad": 0.35,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.12,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "mathtext.fontset": "custom",
    "mathtext.rm": "DejaVu Serif",
    "mathtext.it": "DejaVu Serif:italic",
    "mathtext.bf": "DejaVu Serif:bold",
})

# Fixed H colors so the same physical parameter has the same color everywhere.
H_COLORS = {
    -0.05: "#155e75",
    -0.025: "#0369a1",
    0.0: "#cc642f",
    0.025: "#b45309",
    0.05: "#9d174d",
}
H_LINES = {-0.05: "--", -0.025: "--", 0.0: "-", 0.025: "--", 0.05: "--"}
H_LABELS = {
    -0.05: "H/H$^*$ = -0.05",
    -0.025: "H/H$^*$ = -0.025",
    0.0: "H/H$^*$ = 0",
    0.025: "H/H$^*$ = +0.025",
    0.05: "H/H$^*$ = +0.05",
}

STYLE_SOURCE = "paper_a_study/figure_style.py"
FONT_STATUS = "Times New Roman unavailable; DejaVu Serif metric-compatible fallback"
COLORMAPS = {"sequential": "viridis", "alternate": "plasma", "diverging": "coolwarm"}


def h_style(eta: float) -> dict:
    """Return fixed line style for an H value."""
    return {"color": H_COLORS[float(eta)], "linestyle": H_LINES[float(eta)]}


def label_panel(axis, label: str) -> None:
    """Place a uniform, non-overlapping subfigure label."""
    if hasattr(axis, "get_zlim"):
        axis.text(0.0, 1.02, 0.0, label, transform=axis.transAxes,
                  fontsize=11, fontweight="bold", va="bottom", ha="left")
    else:
        axis.text(-0.035, 1.035, label, transform=axis.transAxes,
                  fontsize=11, fontweight="bold", va="bottom", ha="right")


def save_figure(figure, stem: str, directory, *, dpi: int = 600, rasterize: bool = False) -> None:
    """Save vector PDF/SVG plus a 600-dpi PNG; rasterize only requested surfaces."""
    directory.mkdir(parents=True, exist_ok=True)
    figure.savefig(directory / f"{stem}.pdf")
    figure.savefig(directory / f"{stem}.svg")
    figure.savefig(directory / f"{stem}.png", dpi=dpi)
