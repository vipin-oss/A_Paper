# Paper A — Round 19: pre-edit verification

Everything below was measured **before** any file was edited in this round, in the order it was
measured. No engine is available, so page-level observations are quoted from the supervisor's
round-18 PDF, not re-derived here.

## 1. What the round-18 PDF showed

The supervisor's review of the 41-page build reported six items and one layout defect. The
layout defect is quantified: the constitutive-derivative display on page 5 exceeded the text
width by approximately **67.6 pt**. The text width is fixed by `main.tex`
(`\usepackage[margin=22mm]{geometry}` on A4): 210 − 44 = 166 mm = **470.5 pt = 47.05 em** at
10 pt.

## 2. The environment

* No `pdflatex`, `latex`, `lualatex` or `tectonic`, and no way to install one (no deb mirror,
  no PyPI engine, release host blocked). Every statement about the build in this round is
  therefore **BUILD UNVERIFIED**.
* Python 3.11 with numpy 2.4.6 / scipy 1.17.1. `scipy.linalg.polyeig` does not exist in that
  version, so every polynomial-eigenvalue statement below was obtained from a hand-built pencil.
* `Plate.edge()` returns `(result, scratch)`; `Plate.waves()` returns `(waves, A, F)`.

## 3. Dimensions, measured not assumed

Probe on `model.py` at the operating point (k_y d = 0.1298, ω d/c_s = 7.6334):

| degree n | n_w | n_u | n_φ | n_μ | state | roots | outgoing | m = 2n_u+n_φ+n_μ | rank B |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 23 | 15 | 3 | 5 | 76 | 76 | 38 | 38 | 38 |
| 6 | 33 | 21 | 5 | 7 | 108 | 108 | 54 | 54 | 54 |
| 18 | 93 | 57 | 17 | 19 | 300 | 300 | 150 | 150 | 150 |
| 22 | 113 | 69 | 21 | 23 | 364 | 364 | 182 | 182 | 182 |
| 30 | 153 | 93 | 29 | 31 | 492 | 492 | 246 | 246 | 246 |

The square-ness is exact at every degree, which is what made R19-3 a statement correction
rather than a solver change (§`PAPER_A_ROUND19_EDGE_SYSTEM_VERIFICATION.md`).

Two ranks were measured directly rather than inferred: rank A₂₂ = **15 = n_u** at degree 4
(not n_w = 23) and rank A₁₂ = 10. The singular leading coefficient is the reason the finite
spectrum is 2(n_w + n_u) and not 4n_w.

## 4. The stiff matrix, measured

`S = b₁ᵀ W b₁` at N = 6 from an independent 60-point quadrature reproduces the printed 6×6
matrix to 8.5e-4 absolute (tolerance 1e-4 × 660). Row 5 is `(0, 22.978, 0, 210.60, 0, 660)`:
three non-zeros, spanning four columns. Row 1 is `(0, 12, 0, 18.330, 0, 22.978)`. Between them
these settle R19-5 before the edit: the matrix is parity-structured and **not** banded by two.

## 5. The flexoelectric placement, measured

With f = 0 in place of the manuscript value, only A₀₀ changes, by 5.3978492 in Frobenius norm
(2.9e-4 relative to ‖A₀₀‖ = 1.89e4). A₁₂ = A₂₁ = 4.040018 and A₂₂ = 0.711536 are unchanged to
1e-13, and A₀₂ = A₂₀ = 0 exactly. This is the measurement behind the new paragraph in
Appendix A.3: f₃₃₃₃ pairs E_z with ∂_z ε_zz, neither of which carries a k_x power, so f enters
A₀₀ and no other block.

## 6. The polynomial, measured

Evaluating the two candidate linearisations by hand:

* `C₁ = [−A₀, −A₁, −A₂, −A₃ ; I …]` with `C₂ = [A₄ ; I …]` — roots do not agree with the
  polynomial: nearest-neighbour distance up to **41.6** (degree 4) and **75.4** (degree 6).
  Discarded, and not used anywhere.
* pencil `[Z,I,Z,Z ; Z,Z,I,Z ; Z,Z,Z,I ; −A₀,−A₁,−A₂,−A₃] x = k [I,I,I,A₄] x` — agreement to
  **6.4e-12** (degree 4, 76 roots) and **8.2e-10** (degree 6, 108 roots), median 5e-14 / 2e-13.
  Used for test T1.

The first form fails because it puts A₄ on the wrong side; the second is the correct companion
form for a monic-on-the-right pencil, and it stays correct here even though A₄ is singular.

## 7. What this report changed

Nothing by itself. It fixed the numbers that the five repair reports quote, and it is the reason
two of them are labelled "correction of a statement, not of code".
