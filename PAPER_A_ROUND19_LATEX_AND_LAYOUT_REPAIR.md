# Paper A — Round 19: LaTeX and layout repair (R19-1)

## 1. The defect

The supervisor's round-18 build reported one overfull display: the constitutive-derivative set on
page 5, exceeding the text width by approximately **67.6 pt**. The text block is fixed:
`\usepackage[margin=22mm]{geometry}` on A4 gives 166 mm = 470.5 pt = 47.05 em at 10 pt.

## 2. What the display was

Six derivative statements packed into a multi-column `align`: the elastic and the gradient
derivation sharing one row, the piezoelectric-in-strain and flexoelectric-in-gradient pair on
the next, the three field-derivative statements on a third, the carrier and electrostriction
statements on a fourth. The two long rows carried two multi-line derivations each.

## 3. What it is now

One display, six rows, at most two statements per row and each long derivation alone on its row:

```
∂w_el/∂ε_ij   = ½ c_klij ε_kl + ½ c_ijkl ε_kl = c_ijkl ε_kl        (eq:diff_el)
∂w_grad/∂η_ijk = ½ A_lmnijk η_lmn + ½ A_ijklmn η_lmn = A_ijklmn η_lmn (eq:diff_grad)
∂w_piezo/∂ε_ij = −e_kij E_k          ∂w_flexo/∂η_ijk = −f_lijk E_l   (eq:diff_coup)
∂w_diel/∂E_i   = −κ_ij E_j           ∂w_piezo/∂E_i   = −e_ijk ε_jk   (eq:diff_elec)
∂w_flexo/∂E_i  = −f_ijkl η_jkl       ∂w_carr/∂Δn     = a Δn           (eq:diff_carr)
∂w_H/∂Δn       = H_jkl η_jkl         ∂w_es/∂Δn       = −q φ            (eq:diff_es)
```

Every term of the round-18 display is present. Nothing was deleted, no font was shrunk, no
`\resizebox`, no `\scalebox`, no `\small`. The new labels are `eq:diff_el`, `eq:diff_grad`,
`eq:diff_coup`, `eq:diff_elec`, `eq:diff_carr`, `eq:diff_es`; the old single label was
repointed and `static_check.py` passes with no undefined reference.

## 4. Measurement, and its limits

No TeX engine exists in this environment (`pdflatex`, `latex`, `lualatex`, `tectonic`: all
absent; installation impossible). The layout evidence in this round therefore comes from a new
font-metric screen, `paper_a_study/round19_layout_check.py`, which:

* parses every `equation`, `align`, `gather` and `multline` in `sections/*.tex`;
* splits rows at `\\` **outside** matrix and `aligned` environments;
* measures each row by typesetting it in matplotlib mathtext with `mathtext.fontset = "cm"`
  (the BaKoMa Computer Modern metrics), converting pixels to points to em at 10 pt;
* measures matrices cell by cell (mathtext cannot typeset environments) as the sum of column
  maxima plus inter-column skips and delimiters;
* compares each row with 47.05 em and prints the margin in points.

Calibration: the checked rows that could be measured against known widths agree — an isolated
`∂w_diel/∂E_i = −κ_ij E_j` measures 6.48 em, the ∂/∂E_i pair row 15.55 em, and the round-18
`\tfrac12` elastic row 14.4 em when brace-broken correctly.

**Result of the final run:** 83 rows measured, **0 estimated overfull**, widest measured row
**36.9 em = 368.6 pt** (78 % of the block, 101.9 pt of margin). 26 fragments were **refused** by
mathtext (nested `\left…\right`, `\langle` inside braces, `\mathcal` with subscripts, some
matrices) and are therefore *not* measured; they are reported as refused and are not claimed to
be safe.

**This is a screen, not a build.** Mathtext renders fractions in text style, so a display-style
fraction is under-measured by roughly 15–20 %; a row at 40 em in this model can be overfull in
the real build. Every row this round touched is at 37 em or below, which leaves margin against
that bias, but the honest status is: **BUILD UNVERIFIED**, and the model itself could not
reproduce the reported 67.6 pt overflow from the reconstructed round-18 row (it is recorded, not
explained).

## 5. What the supervisor should run

```
cd Paper_A_Final_Submission
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
grep -n "Overfull \\\\hbox" main.log
```

Expected: no `Overfull \hbox` on or near page 5. If one survives, it will be in a row the screen
refused, and the log line identifies it by file and line.

## 6. Other displays reformatted in this round

Four further displays were split for the same reason, none of them reported by the supervisor:

| display | file | before | after |
|---|---|---|---|
| eq:block_norms | numerical_methods.tex | 45.0 em, one line, five norms | two `aligned` rows |
| eq:RB_planes | numerical_methods.tex | 43.9 em, chained equalities | two `aligned` rows |
| eq:momentum_expanded | governing_equations.tex | 43.6 em | two `aligned` rows |
| eq:gauss_expanded | governing_equations.tex | 41.7 em | two `aligned` rows |

## 7. Static validation

`python scripts/static_check.py` → **PASS**: no undefined reference, no duplicate label, all 13
citations present, every macro in the whitelist. The only advisory note is that `eq:diff_es`
(the electrostriction derivative) is not referenced from the text; it is kept because the row
belongs to the set.

## 8. Structure and style

No section was added, removed or reordered. The five-case table of the hyperstress audit is the
only new float and is required by R19-2. No colour, no box, no change of notation. The
Introduction is untouched.
