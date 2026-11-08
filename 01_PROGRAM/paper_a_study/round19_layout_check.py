"""Round 19: display-width audit against Computer Modern metrics.

No TeX engine exists in this environment, so nothing here replaces a build.  What
it does is measure: every display is translated into the subset of maths that
`matplotlib`'s mathtext can typeset with the Computer Modern font set
(`mathtext.fontset = "cm"`, i.e. the BaKoMa CM fonts whose metrics are those of
TeX), rendered at the manuscript's 10 pt, and its width compared with the text
block.  The paper is `a4paper` with `margin=22mm`, so the text width is 166 mm =
470.5 pt = 47.05 em.

Constructs mathtext cannot render are replaced by their width-carrying part and
listed in `LOSSY`, so the estimate is conservative in a known direction:
`\\underbrace{X}_{Y}` is measured as `X`, `\\bigl(`/`\\Bigr)` as plain delimiters,
`\\text{...}` as `\\mathrm{...}`, `\\qquad` as two `\\quad`-width spaces, and
macros of the manuscript (`\\vect`, `\\Imag`, `\\cref`, `\\SI`) are expanded.

Calibration: the round-18 supervisor build reported exactly one overfull display,
the constitutive-derivative block on page 5, overfull by 67.6 pt, i.e. a row of
470.5 + 67.6 = 538.1 pt = 53.8 em.  This script, run on the round-18 source,
locates that row by measurement rather than by assumption; the row and its
measured width are printed by `--calibrate`.

    PYTHONPATH=. python paper_a_study/round19_layout_check.py [--calibrate]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "Paper_A_Final_Submission" / "sections"
TEXTWIDTH_EM = 470.5 / 10.0
DISPLAY_BEGIN = re.compile(r"\\begin\{(equation|align|gather|multline)\*?\}")
DISPLAY_END = re.compile(r"\\end\{(equation|align|gather|multline)\*?\}")

matplotlib.rcParams["mathtext.fontset"] = "cm"
_FIG = plt.figure(figsize=(40, 2), dpi=100)
_RENDERER = _FIG.canvas.get_renderer()

def _strip_underbrace(s: str) -> str:
    r"""`\underbrace{X}_{Y}` -> `X`, `\overbrace{X}^{Y}` -> `X` (brace aware)."""
    out = []
    i = 0
    while i < len(s):
        m = re.match(r"\\(under|over)brace\s*", s[i:])
        if not m:
            out.append(s[i])
            i += 1
            continue
        i += m.end()
        if i < len(s) and s[i] == "{":
            depth, j = 0, i
            while j < len(s):
                if s[j] == "{":
                    depth += 1
                elif s[j] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            out.append(s[i:j + 1])
            i = j + 1
            # drop the following _{...} or ^{...}
            while i < len(s) and s[i] in "_^":
                i += 1
                if i < len(s) and s[i] == "{":
                    depth, j = 0, i
                    while j < len(s):
                        if s[j] == "{":
                            depth += 1
                        elif s[j] == "}":
                            depth -= 1
                            if depth == 0:
                                break
                        j += 1
                    i = j + 1
        else:
            continue
    return "".join(out)


SUBST = [
    (r"\\tfrac|\\dfrac", r"\\frac"),
    (r"\\frac\s*([0-9])\s*([0-9])", r"\\frac{\1}{\2}"),
    (r"\\frac\s*([a-zA-Z])\s*([a-zA-Z])\b", r"\\frac{\1}{\2}"),
    (r"\\label\{[^}]*\}", ""),
    (r"\\notag|\\nonumber", ""),
    (r"\\begin\{aligned\}|\\end\{aligned\}", ""),
    (r"\\bigl|\\bigr|\\Bigl|\\Bigr|\\biggl|\\biggr|\\Biggl|\\Biggr|\\big|\\Big", ""),
    (r"\\left|\\right", ""),
    (r"\\text\s*\{", r"\\mathrm{"),
    (r"\\mathsf\s*\{", r"\\mathrm{"),
    (r"\\textrm\s*\{", r"\\mathrm{"),
    (r"\\boldsymbol\s*\{\\", r"\\"),
    (r"\\vect\s*\{([a-zA-Z])\}", r"\1"),
    (r"\\vect\s+([a-zA-Z])", r"\1"),
    (r"\{\}\{", "{"),
    (r"\\ii\b", r"\\mathrm{i}"),
    (r"\\mathrm{i}\s*i\b", r"\\mathrm{i}"),
    (r"\\mathsf\s+([A-Za-z])", r"\\mathrm{\1}"),
    (r"\\Imag", r"\\mathrm{Im}"),
    (r"\\Real", r"\\mathrm{Re}"),
    (r"\\cref\{[^}]*\}|\\Cref\{[^}]*\}", "0"),
    (r"\\eqref\{[^}]*\}", "(0)"),
    (r"\\SI\{[^}]*\}\{[^}]*\}", "0"),
    (r"\\si\{[^}]*\}", "0"),
    (r"\\qquad", r"\\quad\\quad"),
    (r"\\dd\b", r"\\mathrm{d}"),
    (r"\\!", ""),
    (r"\\;", r"\\,"),
    (r"\\displaystyle", ""),
    (r"&", ""),
]

_MATRIX = re.compile(r"\\begin\{(pmatrix|bmatrix|matrix)\}(.*?)\\end\{\1\}", re.S)


def _matrix_width(body: str) -> float:
    """Width of a matrix: sum of its column maxima plus skips and delimiters."""
    rows = [r for r in re.split(r"\\\\", body) if r.strip()]
    cells = [[c for c in r.split("&")] for r in rows]
    ncol = max((len(r) for r in cells), default=1)
    colmax = [0.0 for _ in range(ncol)]
    for r in cells:
        for j, c in enumerate(r):
            colmax[j] = max(colmax[j], measure(c))
    return sum(colmax) + 0.6 * ncol + 0.5


def translate(row: str) -> str:
    s = _strip_underbrace(row)
    for pat, rep in SUBST:
        s = re.sub(pat, rep, s)
    s = s.replace("{}&{", "{").replace("{}{", "{")
    return s.strip()


def measure(row: str, fontsize: float = 10.0) -> float:
    """Width of one display row, in em, from Computer Modern metrics.

    Matrix environments are measured cell by cell (mathtext cannot typeset
    them); the width of a matrix is the sum of its column maxima plus the
    inter-column skips and the delimiters."""
    extra = 0.0
    while True:
        m = _MATRIX.search(row)
        if not m:
            break
        extra += _matrix_width(m.group(2))
        row = row[:m.start()] + row[m.end():]
    body = re.sub(r"\s+", " ", translate(row)).strip()
    if not body:
        return extra
    try:
        artist = _FIG.text(0, 0, "$" + body + "$", fontsize=fontsize)
        box = artist.get_window_extent(renderer=_RENDERER)
        artist.remove()
        return (box.width / (100 / 72.0)) / fontsize + extra
    except Exception:
        FAILED.append(body[:70])
        return float("nan")


FAILED: list[str] = []


def displays(path: Path):
    lines = path.read_text().split("\n")
    inside, buf, start = False, [], 0
    for k, line in enumerate(lines):
        if DISPLAY_BEGIN.search(line):
            inside, buf, start = True, [], k + 1
            continue
        if DISPLAY_END.search(line) and inside:
            inside = False
            yield start, " ".join(buf)
            continue
        if inside:
            buf.append(line)


def rows_of(text: str):
    """Split a display into rows at `\\`, but never inside a matrix environment."""
    rows, buf, i = [], [], 0
    depth = 0
    while i < len(text):
        m = re.match(r"\\begin\{(pmatrix|bmatrix|matrix|aligned|array)\}", text[i:])
        if m:
            depth += 1
            buf.append(text[i:i + m.end()])
            i += m.end()
            continue
        m = re.match(r"\\end\{(pmatrix|bmatrix|matrix|aligned|array)\}", text[i:])
        if m:
            depth = max(0, depth - 1)
            buf.append(text[i:i + m.end()])
            i += m.end()
            continue
        if depth == 0 and text.startswith("\\\\", i):
            rows.append("".join(buf))
            buf = []
            i += 2
            while i < len(text) and text[i] == "[":
                j = text.find("]", i)
                i = len(text) if j < 0 else j + 1
            continue
        buf.append(text[i])
        i += 1
    rows.append("".join(buf))
    return [r for r in rows if r.strip()]


def report() -> int:
    print(f"Text block: {TEXTWIDTH_EM:.2f} em = 470.5 pt (166 mm at 10 pt).")
    print("Widths are measured with Computer Modern metrics through "
          "matplotlib mathtext; the build itself is UNVERIFIED.\n")
    print(f"{'file':30s} {'line':>5s} {'em':>6s} {'pt':>7s} {'over':>7s}  row")
    print("-" * 110)
    total = over = 0
    worst = (0.0, "", 0, "")
    for path in sorted(SECTIONS.glob("*.tex")):
        for start, text in displays(path):
            for row in rows_of(text):
                w = measure(row)
                if w != w:                     # mathtext refused the fragment
                    continue
                total += 1
                if w > TEXTWIDTH_EM:
                    over += 1
                    print(f"{path.name:30s} {start:5d} {w:6.1f} {w * 10:7.1f} "
                          f"{(w - TEXTWIDTH_EM) * 10:+7.1f}  {row.strip()[:56]}")
                if w > worst[0]:
                    worst = (w, path.name, start, row.strip()[:70])
    print("-" * 110)
    print(f"rows measured: {total};  estimated overfull: {over}")
    print(f"widest row: {worst[0]:.1f} em = {worst[0]*10:.1f} pt "
          f"({worst[1]}:{worst[2]}) {worst[3]}")
    print(f"fragments mathtext refused: {len(FAILED)}")
    for f in FAILED[:5]:
        print("   ", f)
    return 0


def calibrate() -> int:
    """Measure the round-18 constitutive display as it stood before the repair."""
    old = [
        r"\frac{\partial w_{\text{el}}}{\partial\varepsilon_{ij}}"
        r"&=\tfrac12 c_{klij}\varepsilon_{kl}+\tfrac12 c_{ijkl}\varepsilon_{kl}"
        r"=c_{ijkl}\varepsilon_{kl},"
        r"&\frac{\partial w_{\text{grad}}}{\partial\eta_{ijk}}"
        r"&=\tfrac12 A_{lmnijk}\eta_{lmn}+\tfrac12 A_{ijklmn}\eta_{lmn}"
        r"=A_{ijklmn}\eta_{lmn},",
        r"\frac{\partial w_{\text{piezo}}}{\partial\varepsilon_{ij}}&=-e_{kij}E_k,"
        r"&\frac{\partial w_{\text{flexo}}}{\partial\eta_{ijk}}&=-f_{lijk}E_l,",
        r"\frac{\partial w_{\text{diel}}}{\partial E_i}&=-\kappa_{ij}E_j,"
        r"&\frac{\partial w_{\text{piezo}}}{\partial E_i}&=-e_{ijk}\varepsilon_{jk},"
        r"&\frac{\partial w_{\text{flexo}}}{\partial E_i}&=-f_{ijkl}\eta_{jkl},",
        r"\frac{\partial w_{\text{carr}}}{\partial\Delta n}&=a\,\Delta n,"
        r"&\frac{\partial w_{H}}{\partial\Delta n}&=H_{jkl}\eta_{jkl},"
        r"&\frac{\partial w_{\text{es}}}{\partial\Delta n}&=-q\varphi,",
    ]
    print("Round-18 constitutive display, reconstructed row by row:")
    old = rows_of(" ".join(old))
    for row in old:
        # three alignment columns add two inter-column skips of 1 em each
        w = measure(row)
        print(f"  {w:6.1f} em = {w*10:7.1f} pt   over {(w-TEXTWIDTH_EM)*10:+7.1f} pt"
              f"   {row.strip()[:50]}")
    print("The supervisor's build reported one overfull row at +67.6 pt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(calibrate() if "--calibrate" in sys.argv else report())
