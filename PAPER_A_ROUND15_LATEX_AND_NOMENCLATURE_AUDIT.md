# Round 15 — LaTeX and nomenclature audit

## 1. The nomenclature table

### Defect (round 14)

```latex
\begin{tabular}{@{}ll p{7mm} ll@{}}
```

The specification declares **five** columns for rows that contain **four** cells.
The `p{7mm}` was intended as a gap; LaTeX treats it as a column, so the third cell
of every row — a *symbol* — was typeset into a 7 mm column and overran it. The
table would have looked broken in the supervisor's build, and it is exactly the
kind of defect that a static source check cannot see.

### Repair

```latex
\begin{tabular}{@{}ll@{\qquad}ll@{}}
```

Four columns, with the gap expressed as inter-column spacing (`@{\qquad}`), which
is not a column. `\qquad` is inside the static validator's whitelist, so the
validator and the typesetting agree.

### Notation de-collision

| Symbol | Was | Now |
| --- | --- | --- |
| `D` vs `D_i` | both listed as "diffusivity" and "electric displacement" with no gloss | explicitly *electron diffusivity* and *electric displacement*, on separate rows |
| `α` vs `α_d` | `α` appeared with two meanings (attenuation, and the transport group used in the weak form) | `α_d = D/(dc_s)` is the transport-over-elastic rate; `α = 2|\Imag k_x|` is the spatial attenuation; only `α_d` appears in the weak form |
| `f` vs `f_ijkl` | frequency and flexoelectric constant shared a letter | `ω, f` = angular frequency and frequency; `f_ijkl` = flexoelectric constant |
| `μ̃` vs `μ_e` | similar glyphs | `μ̃` = electrochemical potential; `μ_e` = electron mobility |
| `k_x`, `k_y`, `k_{Bx}`, `k_{ix}` | incident/backward roots not in the table | added explicitly |
| `v_i`, `ψ`, `Φ` | test functions never listed | added, because the weak forms use them |

Additions to the table: `Σ_ij`, `n_i`, `v_i`, `ψ`, `Φ`, `Ñ = μ̃ + Qφ`, `Q`, `k_{Bx}`,
`k_{ix}`, `α_d`, `H` (`≡ H_zzz`), `a`, `τ_ijk = τ_jik`.

## 2. Static validation (executed this round)

`Paper_A_Final_Submission/scripts/static_check.py`, exit status **0**:

- 112 labels, 85 references, 13/13 citation keys resolved, 13 bib entries;
- environments balanced, brackets balanced, every included figure present, no
  macro outside the whitelist (the previous `\hspace` failure does not recur);
- approximate word count 16 854 (including math tokens);
- residual *notes* (not findings): a number of section and equation labels are
  never referenced. That is expected for equations cited only by their
  surrounding prose; it is not an error and it is not hidden.

## 3. Build status — separated from the source quality

| Item | Status |
| --- | --- |
| TeX engines present in this environment | **none**: `pdflatex`, `latexmk`, `xelatex`, `lualatex`, `tectonic` all absent (checked again this round) |
| `bibtex` | absent |
| Package installation | not possible (no distribution mirror reachable) |
| Consequence | the manuscript was **not** compiled here; no PDF is included in the archive and none is claimed |
| What *is* verified | source-level: environment balance, cross-reference resolution, citation resolution, figure-file presence, macro whitelist, table column/cell arity (by inspection of every tabular) |
| What the supervisor's environment provides | round 13 was compiled on the supervisor side, so the manuscript is buildable; round 15 changed no preamble command, no package, and no environment name, only content and one tabular specification |

**A source that passes these checks can still typeset badly** (overfull boxes,
bad page breaks, a table that runs into the margin). Since no engine exists here,
none of that is claimed as verified. The three risk areas for the supervisor's
build are named honestly:

1. the new `eq:block` (`aligned` inside `equation`) is long; it may need
   `\small` or a line-break adjustment at 22 mm margins;
2. the nomenclature table is now four columns wide with long entries
   (`τ_ijk = τ_jik`, `Ñ = μ̃ + Qφ`); it is the widest object added this round;
3. `eq:weak_mech`–`eq:weak_carrier` are ordinary displays and carry no unusual
   constructs.

No journal template has been specified for this work, so no journal-specific
compliance is claimed; the layout is the consistent A4, 22 mm-margin manuscript
layout used throughout.

## 4. Structure preserved from round 14

One continuous Introduction · Mathematical formulation with written derivations ·
Solution of the problem · Numerical results and discussion · Conclusions ·
Declarations · Appendix on resolution and data availability · separate
computational supplement. No section was reordered, renamed or removed this
round, and no software narrative was reintroduced.
