#!/usr/bin/env python3
"""Static validation of the Paper A LaTeX source.

No TeX engine is assumed.  The script checks what can be checked without one:
brace and environment balance, math-mode balance, \\cite -> bibliography key
resolution, \\ref/\\cref/\\eqref -> \\label resolution, the existence of every
included figure file, duplicate labels, and the presence of every macro in a
whitelist of kernel, package and locally defined commands.

Exit status 0 means every check passed.  The report is written next to this
script as static_validation.txt.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "main.tex"
BIB = ROOT / "references.bib"
REPORT = ROOT / "static_validation.txt"

# ---------------------------------------------------------------- whitelist
KERNEL = """
begin end documentclass usepackage newcommand renewcommand providecommand
DeclareMathOperator DeclareRobustCommand makeatletter makeatother
title author date maketitle begin end appendix section subsection
paragraph subsubsection label ref eqref pageref cite citep citet nocite
caption centering includegraphics textwidth linewidth columnwidth
textbf textit textrm textsf textsc texttt emph footnote thanks
item itemize enumerate description quote small medskip bigskip noindent
hfill vfill newline par newpage clearpage tableofcontents listoffigures
bibliographystyle bibliography input include clearpaper
toprule midrule bottomrule cmidrule addlinespace
arraystretch tabcolsep
Real Imag vect dd ii ee op
frac tfrac dfrac sqrt sum int oint prod lim liminf limsup max min sup inf
partial nabla delta Delta varepsilon epsilon sigma tau mu varphi phi Phi psi
Psi omega Omega rho kappa lambda Lambda Gamma alpha beta gamma theta Theta
zeta eta xi pi Pi nu chi zero
mathrm mathcal mathbf mathit mathsf mathtt mathbb mathfrak boldsymbol
operatorname text textnormal hbox mbox
left right big Big bigl bigr Bigl Bigr biggl biggr Biggl Biggr
langle rangle langle rangle vert Vert mid
cdot cdots ldots dots vdots ddots times div pm mp ast star circ bullet
le leq ge geq neq approx sim simeq equiv propto ll gg
to rightarrow leftarrow leftrightarrow Rightarrow Leftarrow iff implies
in notin subset subseteq cup cap setminus emptyset forall exists
infty infty partial
exp log ln sin cos tan sinh cosh tanh
quad qquad enspace thinspace negthinspace , ; : ! space
hat tilde bar vec dot ddot overline underline widetilde widehat
mathcal mathrm
iff
SI si num qty ang unit
cref Cref crefrange Crefrange namecref nameCref
aligned align gather split cases matrix pmatrix bmatrix vmatrix
small footnotesize scriptsize tiny normalsize large Large LARGE huge
bfseries itshape rmfamily sffamily ttfamily mdseries upshape
setlength addtolength setcounter value the
cline hline multicolumn multirow
renewcommand
bra ket
parallel perp
square blacksquare checkmark
color textcolor
subfloat
subcaption
ContinuedFloat
nameref autoref
hypersetup
geometry
sisetup
numlist
ang ell hbar
bel coulomb pascal farad volt joule kelvin hertz metre second gram
giga mega kilo micro milli nano pico deci centi
per percent cubic square
textsuperscript subscript
today
underbrace overbrace underbrace
gtrsim lesssim Sigma iint siemens oiiint
path url urlstyle arraybackslash raggedright normalfont tabularx X protect
emergencystretch hsize textwidth linewidth
ldots dots
""".split()


def strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        cut = len(line)
        i = 0
        while i < len(line):
            if line[i] == "\\":
                i += 2
                continue
            if line[i] == "%":
                cut = i
                break
            i += 1
        out.append(line[:cut])
    return "\n".join(out)


FRAGILE = ("path", "url", "href", "nolinkurl")


def _brace_argument(text: str, open_index: int) -> str:
    """Return the balanced {...} argument that starts at ``open_index``."""
    depth = 0
    i = open_index
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[open_index + 1 : i]
        i += 1
    return text[open_index + 1 :]


def check_moving_arguments(text: str, label: str = "text") -> list[str]:
    import re as _re

    found: list[str] = []
    pattern = _re.compile(
        r"\\(caption|section|subsection|subsubsection|paragraph)\s*(\[[^\]]*\])?\s*\{")
    for m in pattern.finditer(text):
        arg = _brace_argument(text, m.end() - 1)
        base = text.count("\n", 0, m.end() - 1) + 1
        for cmd in FRAGILE:
            for hit in _re.finditer(r"(?<!\\protect)\\" + cmd + r"\{", arg):
                line = base + arg[: hit.start()].count("\n")
                found.append(
                    f"{label}: line {line}: fragile \\{cmd} in a moving "
                    f"argument (\\{m.group(1)}) - use \\protect\\{cmd}")
    return found


def main() -> int:
    files = [MAIN] + sorted((ROOT / "sections").glob("*.tex"))
    problems: list[str] = []
    notes: list[str] = []
    text_all = ""

    for f in files:
        raw = f.read_text(encoding="utf-8")
        text = strip_comments(raw)
        text_all += "\n" + text
        rel = f.relative_to(ROOT)

        # braces
        depth = 0
        for ch in text:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth < 0:
                    problems.append(f"{rel}: closing brace without opener")
                    depth = 0
        if depth != 0:
            problems.append(f"{rel}: brace balance {depth:+d}")

        # math delimiters: $ must be even, \[ \] and \( \) balanced
        n_dollar = len(re.findall(r"(?<!\\)\$", text))
        if n_dollar % 2:
            problems.append(f"{rel}: odd number of $ delimiters ({n_dollar})")
        n_disp = len(re.findall(r"(?<!\\)\\\[", text))
        if n_disp != text.count("\\]"):
            problems.append(f"{rel}: display-math \\[ and \\] counts differ")

        # environments
        stack = []
        for m in re.finditer(r"\\(begin|end)\{([^}]*)\}", text):
            kind, name = m.group(1), m.group(2).strip()
            if kind == "begin":
                stack.append(name)
            else:
                if not stack:
                    problems.append(f"{rel}: \\end{{{name}}} without \\begin")
                elif stack[-1] != name:
                    problems.append(
                        f"{rel}: \\end{{{name}}} closes \\begin{{{stack[-1]}}}")
                    stack.pop()
                else:
                    stack.pop()
        for name in stack:
            problems.append(f"{rel}: unclosed environment {name}")

        # fragile commands inside moving arguments (per file, so the line
        # number reported is the line of the offending source file)
        problems.extend(check_moving_arguments(text, str(rel)))

    # ---- fragile commands inside moving arguments
    # \caption and \section arguments are written to the .lof/.toc files with
    # \protected@write, which expands everything that is not \protect-ed.  A
    # \path or \url there aborts the build with
    #   "\Url Error -> \url used in a moving argument".
    # Round 5 shipped exactly that in fourteen captions; the per-file check
    # above is the regression guard for it.

    # ---- bibliography
    bib = BIB.read_text(encoding="utf-8")
    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    cite_keys: set[str] = set()
    for m in re.finditer(r"\\cite[a-z]*\{([^}]*)\}", text_all):
        for k in m.group(1).split(","):
            if k.strip():
                cite_keys.add(k.strip())
    for k in sorted(cite_keys - bib_keys):
        problems.append(f"citation key not in references.bib: {k}")
    for k in sorted(bib_keys - cite_keys):
        notes.append(f"bibliography entry never cited: {k}")

    # ---- labels and references
    labels = re.findall(r"\\label\{([^}]*)\}", text_all)
    dups = {l for l in labels if labels.count(l) > 1}
    for d in sorted(dups):
        problems.append(f"duplicate label: {d}")
    refs: set[str] = set()
    for m in re.finditer(r"\\(?:ref|cref|Cref|eqref|autoref|nameref|pageref)\{([^}]*)\}",
                         text_all):
        refs.update(x.strip() for x in m.group(1).split(",") if x.strip())
    for r in sorted(refs - set(labels)):
        problems.append(f"reference to undefined label: {r}")
    for l in sorted(set(labels) - refs):
        notes.append(f"label never referenced: {l}")

    # ---- figures
    for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", text_all):
        target = (ROOT / m.group(1)).with_suffix(".pdf")
        cand = ROOT / m.group(1)
        if not (cand.exists() or target.exists()):
            problems.append(f"missing figure file: {m.group(1)}")

    # ---- macros
    used = set(re.findall(r"\\([A-Za-z@]+)", text_all))
    known = set(KERNEL) | {w.lower() for w in KERNEL}
    unknown = sorted(u for u in used if u not in known)
    if unknown:
        problems.append("macros outside the whitelist: " + ", ".join(unknown))

    # ---- document structure
    if "\\begin{document}" not in text_all or "\\end{document}" not in text_all:
        problems.append("missing \\begin{document} or \\end{document}")
    if text_all.count("\\begin{document}") != 1:
        problems.append("more than one \\begin{document}")
    if "\\maketitle" not in text_all:
        problems.append("no \\maketitle")
    if "\\begin{abstract}" not in text_all:
        problems.append("no abstract")
    for need in ["\\section{Introduction}", "\\section{Conclusions}"]:
        if need not in text_all:
            problems.append(f"missing {need}")

    words = len(re.findall(r"[A-Za-z]{2,}", re.sub(r"\\[A-Za-z@]+", " ", text_all)))
    notes.append(f"approximate prose word count (including math tokens): {words}")

    lines = ["Paper A static validation", "=" * 40, ""]
    lines.append(f"files checked: {len(files)}")
    lines.append(f"labels: {len(labels)}   references: {len(refs)}")
    lines.append(f"citation keys used: {len(cite_keys)}   bib entries: {len(bib_keys)}")
    lines.append("")
    lines.append("FAIL" if problems else "PASS")
    lines.append("")
    if problems:
        lines.append("Problems:")
        lines += [f"  - {p}" for p in problems]
        lines.append("")
    if notes:
        lines.append("Notes:")
        lines += [f"  - {n}" for n in notes]
    lines.append("")
    lines.append("No TeX engine was invoked by this script.")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
