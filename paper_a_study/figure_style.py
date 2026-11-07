"""Single authoritative publication style for every Paper A figure.

Semantic colour rules (enforced for the whole ten-figure set)
------------------------------------------------------------
1. The dimensionless carrier-strain-gradient coupling ``H/H*`` has exactly one
   colour / dash / marker triple, used wherever ``H`` is a plotted variable.
   The mapping is fixed by the supervisor's repair order and is not reused for
   any other physical quantity.
2. Material and geometry families (carrier density, mobility, plate thickness,
   gradient length, tangential wavenumber) use *different* ordered sequential
   ramps, one colour per value, so that five values of one parameter can never
   collapse into a single colour.
3. Signed relative changes use a balanced diverging map with white at zero.

Fonts
-----
Times New Roman is not installed in the build container.  DejaVu Serif is the
documented, licence-clean serif fallback; no font binary is redistributed.  The
choice is recorded in ``FONT_STATUS`` and repeated in the figure manifest.

Grayscale safety
----------------
Every semantic mapping also differs in dash pattern and marker shape, so the
five ``H`` levels remain separable when the figure is printed in greyscale.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.colors import LinearSegmentedColormap

# --------------------------------------------------------------------------
# Global matplotlib state
# --------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "STIXGeneral"],
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.labelweight": "bold",
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "axes.titlesize": 10,
    "axes.titleweight": "normal",
    "figure.titlesize": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "axes.prop_cycle": cycler(color=["#202A44"]),
    "lines.linewidth": 2.0,
    "lines.linestyle": "-",
    "lines.markersize": 5.5,
    "lines.markeredgewidth": 0.9,
    "grid.color": "#dde3e8",
    "grid.linewidth": 0.55,
    "grid.alpha": 0.9,
    "grid.linestyle": "-",
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.size": 3.2,
    "ytick.major.size": 3.2,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.minor.size": 1.8,
    "ytick.minor.size": 1.8,
    "legend.frameon": True,
    "legend.framealpha": 0.95,
    "legend.edgecolor": "#b6c0c8",
    "legend.fancybox": False,
    "legend.borderpad": 0.4,
    "legend.handlelength": 2.4,
    "legend.handletextpad": 0.6,
    "legend.labelspacing": 0.35,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.bbox": None,          # exact figsize: identical scale in LaTeX
    "savefig.pad_inches": 0.0,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "mathtext.fontset": "dejavuserif",
    "axes.unicode_minus": True,
    "figure.autolayout": False,
})

FONT_STATUS = ("Times New Roman unavailable in the build container; "
               "DejaVu Serif (licence-clean serif fallback) used throughout.")

# Journal text width for the 22 mm-margin A4 article class used by main.tex.
TEXT_WIDTH_IN = 6.50
FIGURE_WIDTH_IN = TEXT_WIDTH_IN
FIGURE_HEIGHT_IN = 5.10          # 2x2 panels, ~1.27 aspect per panel

# --------------------------------------------------------------------------
# 1. H/H* -- fixed semantic triple (colour, dash, marker)
# --------------------------------------------------------------------------
H_LEVELS = [-0.05, -0.025, 0.0, 0.025, 0.05]
H_STYLE = {
    -0.05:  dict(color="#087E8B", linestyle="-",        marker="o",  label="-0.050"),
    -0.025: dict(color="#3867D6", linestyle="--",       marker="s",  label="-0.025"),
     0.0:   dict(color="#202A44", linestyle="-",        marker="D",  label="0 (baseline)"),
     0.025: dict(color="#E3A008", linestyle="-.",       marker="^",  label="+0.025"),
     0.05:  dict(color="#C83E58", linestyle=(0, (1, 1.3)), marker="v", label="+0.050"),
}
H_COLORS = {k: v["color"] for k, v in H_STYLE.items()}
#: Zorder so the near-black baseline is never hidden under a neighbour.
H_ZORDER = {-0.05: 4, -0.025: 5, 0.0: 7, 0.025: 6, 0.05: 3}
H_LINEWIDTH = {k: (2.6 if k == 0.0 else 1.9) for k in H_LEVELS}

H_LEGEND_TITLE = r"$H/H^{*}$"


def h_style(eta: float) -> dict:
    """Return the fixed plotting keywords for one ``H/H*`` level."""
    return dict(H_STYLE[round(float(eta), 6)])


def h_plot(ax, x, y, eta: float, *, marker: bool = True, label: bool = True,
           markevery=None, zorder=None, **kw):
    """Plot a curve with the fixed ``H`` semantics."""
    st = h_style(eta)
    plot_kw = dict(color=st["color"], linestyle=st["linestyle"],
                   linewidth=H_LINEWIDTH[round(float(eta), 6)],
                   marker=st["marker"] if marker else "None",
                   markersize=5.0, markeredgewidth=0.8,
                   markeredgecolor=st["color"], markerfacecolor="white" if
                   round(float(eta), 6) != 0.0 else st["color"],
                   zorder=H_ZORDER[round(float(eta), 6)] if zorder is None else zorder,
                   label=(H_LEGEND_TITLE + " = " + st["label"]) if label else None)
    if markevery is not None:
        plot_kw["markevery"] = markevery
    plot_kw.update(kw)
    return ax.plot(x, y, **plot_kw)


def h_legend(fig, axes, *, ncol: int = 5, y: float = 0.998, title: str | None = None,
             loc: str = "upper center", fontsize: float = 8.8, **kw):
    """One shared ``H`` legend for the whole figure, placed outside the data."""
    handles, labels, seen = [], [], set()
    for ax in axes:
        for h, lab in zip(*ax.get_legend_handles_labels()):
            if lab and "H/H" in lab:
                lab = lab.replace(" = ", "=").replace(" (baseline)", "")
                if lab not in seen:
                    seen.add(lab)
                    handles.append(h)
                    labels.append(lab)
    if not handles:
        return None
    leg = fig.legend(handles, labels, ncol=ncol, loc=loc,
                     bbox_to_anchor=(0.5, y), frameon=True, title=title,
                     borderaxespad=0.0, columnspacing=1.0, handlelength=1.9,
                     handletextpad=0.5, borderpad=0.35, prop={"size": fontsize},
                     **kw)
    return leg


# --------------------------------------------------------------------------
# 2. Ordered sequential ramps for the other parameter families
# --------------------------------------------------------------------------
# Round 14: each family is a *different hue*, not five shades of one hue, so a
# reader can name the curve without consulting the legend, and every family is
# separated from the H/H* triple (teal, blue, ink, gold, crimson) used for the
# coupling.  Within a family the lightness step is large enough to survive
# greyscale printing together with the dash and marker cycles below.
# No step is a pastel: the lightest member of each family is a mid tone, so no
# curve washes out against the white page at journal column width.
RAMP_N0 = ["#8FB3DA", "#5E92C8", "#3773AE", "#1F5590", "#10325E"]        # carrier density  blue
RAMP_MU = ["#8CC26A", "#5FA344", "#3F7F33", "#2A5C24", "#16381A"]        # mobility         green
RAMP_D = ["#F0B366", "#DE9440", "#C0731F", "#94540F", "#5E3407"]         # thickness        orange
RAMP_ELL = ["#CDB6E6", "#A87FD0", "#7F53B3", "#5A318C", "#371C60"]       # gradient length  purple
RAMP_KY = ["#A8B4BE", "#828E99", "#5F6B75", "#3F4A53", "#242C33"]        # ky slices        neutral

# One dash pattern and one marker per position in a five-value family, applied
# by ramp_styles() so that two curves can never differ in colour alone.
RAMP_DASH = ["-", (0, (6.0, 1.8)), (0, (1.4, 1.3)), (0, (7.0, 1.8, 1.4, 1.8)),
             (0, (3.0, 1.3))]
RAMP_MARK = ["o", "s", "^", "D", "v"]

CMAP_SEQUENTIAL = LinearSegmentedColormap.from_list(
    "paper_a_seq", ["#F4F7FA", "#BBD2E4", "#6E9DC4", "#2F6BA0", "#12385E"])
CMAP_DIVERGING = LinearSegmentedColormap.from_list(
    "paper_a_div", ["#2B6CA3", "#9CC3DF", "#FFFFFF", "#E8B48A", "#B4552A"])


def ramp(colors, values) -> dict:
    """Return an ordered ``value -> colour`` mapping for a parameter family."""
    values = sorted(float(v) for v in values)
    if len(values) != len(colors):
        raise ValueError(f"ramp needs {len(values)} colours, got {len(colors)}")
    return dict(zip(values, colors))


def ramp_styles(colors, values) -> dict:
    """Ordered ``value -> plot kwargs`` for a parameter family.

    Colour alone is not a distinction: every family member also carries its own
    dash pattern and marker, so five curves of one family stay separable in
    greyscale and for colour-blind readers (round-14 figure redesign).
    """
    values = sorted(float(v) for v in values)
    if len(values) != len(colors):
        raise ValueError(f"ramp_styles needs {len(values)} colours, got {len(colors)}")
    if len(values) > len(RAMP_DASH):
        raise ValueError("ramp_styles covers at most five family members")
    return {v: dict(color=c, linestyle=RAMP_DASH[i], marker=RAMP_MARK[i])
            for i, (v, c) in enumerate(zip(values, colors))}


# Fixed label formatting so every panel in the set uses the same precision.
def fmt_sci(value: float, digits: int = 3) -> str:
    if value == 0:
        return "0"
    exp = int(f"{value:e}".split("e")[1])
    mant = value / 10 ** exp
    return rf"${mant:.{digits}g}\times10^{{{exp}}}$"


def label_panel(ax, letter: str, *, dx: float = -0.13, dy: float = 1.045) -> None:
    """Uniform bold (a)-(d) panel tag, inside the axes bounding box."""
    ax.text(dx, dy, f"({letter})", transform=ax.transAxes, fontsize=11,
            fontweight="bold", va="bottom", ha="left", color="#101820")


def style_axes(ax, *, grid: bool = True, minor: bool = False) -> None:
    if grid:
        ax.grid(True, which="major", axis="both")
        ax.set_axisbelow(True)
    if minor:
        from matplotlib.ticker import AutoMinorLocator
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())


def tight_panel(fig, *, wspace: float = 0.30, hspace: float = 0.34,
                left: float = 0.085, right: float = 0.985,
                bottom: float = 0.10, top: float = 0.90) -> None:
    fig.subplots_adjust(left=left, right=right, bottom=bottom, top=top,
                        wspace=wspace, hspace=hspace)


def new_figure(width_in: float = FIGURE_WIDTH_IN,
               height_in: float = FIGURE_HEIGHT_IN):
    fig = plt.figure(figsize=(width_in, height_in))
    return fig


def save_figure(figure, stem: str, directory, *, dpi: int = 400,
                formats=("pdf", "png"), rasterize_panels=None) -> list[Path]:
    """Write a vector PDF plus a high-resolution PNG proof.

    ``rasterize_panels`` optionally takes a list of artists (collections /
    images) whose rasterisation is acceptable because they are dense field
    maps; axes, ticks, text and colourbars stay vector.
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    written = []
    for ext in formats:
        path = directory / f"{stem}.{ext}"
        figure.savefig(path, dpi=dpi, format=ext)
        written.append(path)
    return written


STYLE_SOURCE = "paper_a_study/figure_style.py"
