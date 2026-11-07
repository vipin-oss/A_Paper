# Paper A — Round 19: final report

**Status:** targeted mathematical repair complete; **BUILD UNVERIFIED**.
**Branch:** `arena/ea7ca4dd-a-paper` only. `main` untouched.
**Manuscript:** `Paper_A_Final_Submission/main.tex`, 41 pages in the round-18 build.

Round 19 asked for six named repairs, one re-check of the dependent-equation set, seven
targeted regression tests and a layout repair, with no new physics, no solver change, no
dataset regeneration and no figure change. All six repairs were made. Three of them turned out
to be corrections of *statements*, not of code: the code was already doing the right thing and
the prose described something else. That distinction is the main result of the round and is
set out case by case below.

## 1. What was wrong, and what it was replaced by

| # | Round-18 statement | Round-19 replacement | Nature |
|---|---|---|---|
| R19-1 | constitutive-derivative display overflowed the text block by 67.6 pt | six per-family `align` rows, no shrink, no `\resizebox`, every term kept | presentation |
| R19-2 | "the double-traction block exists only when the strain-gradient length is non-zero" | the block exists whenever τ ≠ 0, i.e. in four of five cases; ℓ = 0 with f ≠ 0 is *inadmissible* in this formulation and is now stated as a restriction | **mathematical** |
| R19-3 | "38 rows against 23 columns … overdetermined by the fifteen double-traction rows … least squares" | N_s = 76, m = M = 38, **square**, full rank, SVD solve of a square system | **mathematical** |
| R19-4 | the worked R_B chain mixed n = 18 and n = 22 rows | all five numbers from the n = 22 row; product shown to be degree-independent | traceability |
| R19-5 | "banded by two" | same-parity coupling, explicitly *not* banded (row 5 spans four columns) | **mathematical** |
| R19-6 | "the strain operator carries the k_x power in its first slot" | powers counted by (r, s) alone; ε split once into ε⁽⁰⁾ + ik_x ε⁽¹⁾; A₂₂ = λ²⟨ε⁽¹⁾, Cε⁽¹⁾⟩ | **mathematical** |

Nothing in the numerical pipeline was changed. `model.py`, `build_figure_data.py` and every
figure-data file are byte-identical to round 18.

## 2. The correction that was not on the list

While verifying R19-3 the root count in `numerical_methods.tex` failed its own check. The text
said the polynomial is of degree 4n_w = 452 in k_x and that "the 2n_w roots with negative
imaginary part" decay into the plate. Both halves are wrong:

* the leading coefficient A₂₂ has rank n_u, not n_w, so 2(n_w − n_u) = 2(n_φ + n_μ) roots are
  **infinite** and the finite spectrum contains 4n_w − 2(n_w − n_u) = **2(n_w + n_u)** roots:
  76, 300 and 364 at degrees 4, 18 and 22 — the state dimension, not twice it;
* the outgoing/incoming split is not the sign of Im k_x. It is `eq:classification`
  (Im k_x < −τ, or |Im k_x| ≤ τ with backward axial power), which is how the solver has always
  classified them.

Both statements are now in the manuscript with the numbers attached, and both are tested.

## 3. Verification record

| check | command | result |
|---|---|---|
| LaTeX static validation | `python scripts/static_check.py` | **PASS** — 0 undefined references, 0 duplicate labels |
| unit suite | `python paper_a_study/test_model.py` | **52 tests, OK** |
| independent reference | `python paper_a_study/round18_reference_checks.py` | **every printed number reproduced** |
| independent audit | `python paper_a_study/round18_mathematical_audit.py` | **43 checks agree** |
| round-19 targeted tests | `python paper_a_study/round19_tests.py` | **7 of 7 PASS** |
| display-width screen | `python paper_a_study/round19_layout_check.py` | 83 rows measured, **0 overfull**, widest 36.9 em of 47.05 em |

The seven round-19 tests are new; they are listed with their independent references and results
in `PAPER_A_ROUND19_EDGE_SYSTEM_VERIFICATION.md` §5.

## 4. What the round did not do

* No new physics, no new section, no new table beyond the five-case table that R19-2 requires.
* No material constant, no solver algorithm, no modal-power definition, no figure, no dataset
  was touched.
* The Introduction was not rewritten.
* No audit or software-test vocabulary was added to the article.

## 5. Verdict

The manuscript is **mathematically consistent** on every point this round examined: the
boundary operator, the edge system, the polynomial bookkeeping, the stiffness structure and the
degree-22 chain all agree with the code and with independent recomputation. It is **not
submission-ready**, for reasons that this round did not create and could not remove:

1. **BUILD UNVERIFIED.** No TeX engine exists in this environment. Nothing about page breaks,
   float placement or overfull boxes in the *actual* build is claimed; see
   `PAPER_A_ROUND19_LATEX_AND_LAYOUT_REPAIR.md` §5 for the exact commands the supervisor should run.
2. **ℓ, f and H are synthetic choices**, not measured material data. Stated in the manuscript.
3. **The corner line force is unresolved** pointwise (> 10⁻⁴ in the reported runs).
4. **Novelty against the 2025 closed-access source** cannot be settled from here.
5. **Five author declarations** are outstanding.
6. **Case C is a restriction, not a repair.** The formulation cannot represent ℓ = 0 with
   f ≠ 0, and says so. No reported number depends on it, but a referee who wants that limit will
   find the model closed against it.

Items 1–6 are unchanged from round 18 except that item 1 now carries a longer list of displays
known to be safe in the font model and one that is not measurable by it.
