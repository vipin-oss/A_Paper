# Paper A — Round 18, Part A: pre-edit audit of the mathematical content

**Branch** `arena/ea7ca4dd-a-paper` · base commit `c33cec6` (round 17) ·
**BUILD UNVERIFIED** — no TeX engine in this environment, none installable.

This is the record of what was wrong **before** anything was edited, written
against the round-17 tree, with the line numbers of that tree.  Nothing in this
report was reconstructed after the repair: each entry was located, reproduced
numerically, classified, and only then corrected.  The two independent scripts
that produced the evidence are

* `paper_a_study/round18_mathematical_audit.py` — 43 checks against the
  production solver, log `PAPER_A_ROUND18_AUDIT_LOG.txt`, exit status 0,
  `RESULT: all independent checks agree`;
* `paper_a_study/round18_reference_checks.py` — 59 checks that import **nothing**
  from the solver and reproduce every number the repaired text prints, exit
  status 0, `RESULT: every printed number reproduced independently`.

Classification vocabulary is the one demanded by the round-18 brief: CONFIRMED
ERROR · NOTATION OR NORMALISATION ERROR · ARITHMETIC ERROR · UNSUPPORTED
INTERPRETATION · CORRECT UNDER EXPLICIT CONVENTION · UNVERIFIED.

---

## 0. Summary

| # | Location (round-17 tree) | Subject | Class |
|---|---|---|---|
| A1 | `appendix_derivations.tex` 13–49 | basis normalisation quoted in the wrong measure | NOTATION OR NORMALISATION ERROR |
| A2 | `appendix_derivations.tex` 25–49 | diagonal stiffness derivation missing the Jacobian chain | NOTATION OR NORMALISATION ERROR |
| A3 | `appendix_derivations.tex` 25–49 | weighted orthogonality attributed to the unweighted integral | UNSUPPORTED INTERPRETATION |
| A4 | `appendix_derivations.tex` 71–93 | charge matrix orientation (C vs Cᵀ, `r_i` vs `r_j`) | CONFIRMED ERROR |
| A5 | `appendix_derivations.tex` 97–142 | transport entry printed as `k_x²+k_y²` inside `A00` | ARITHMETIC ERROR |
| A6 | `appendix_derivations.tex` 97–142 | "largest single entry" of the gradient block | CONFIRMED ERROR |
| A7 | `appendix_derivations.tex` 97–142 | inertia ratio read as a mode frequency | UNSUPPORTED INTERPRETATION |
| A8 | `appendix_derivations.tex` 214–241 | edge operator quoted as `4n × M` and "four statements per field" | CONFIRMED ERROR |
| A9 | `appendix_derivations.tex` 243–255 | modal-power normalisation and the `R_B` chain | CORRECT (no edit) |
| A10 | `governing_equations.tex` 880–881 | "fourteen Debye lengths thin in the ratio d/L_D = 1/Q" | CONFIRMED ERROR (reversed ratio) |
| A11 | `numerical_methods.tex` 186–192 | `n_w = 5n+3` with `n` basis functions; `n_w = 93` at the reported degree; degree `372` | CONFIRMED ERROR (accounting) |
| A12 | `numerical_methods.tex` ~170 | "`A22 = A12 = 0`" at zero strain-gradient length | CONFIRMED ERROR |
| A13 | `numerical_methods.tex` 131 | block inner product written in the ζ measure | NOTATION OR NORMALISATION ERROR |
| A14 | `results.tex` 706–716 | coupling matrix "upper-triangular", rows 187.8/315.9, "largest entry 3.35" | CONFIRMED ERROR |
| A15 | `appendix_derivations.tex` 233ff | same measure slip inside the block construction | NOTATION OR NORMALISATION ERROR |
| A16 | `governing_equations.tex` 310–340, 420–470 | σ, D, τ, momentum, Gauss, carrier equations | CORRECT UNDER EXPLICIT CONVENTION |

Seven of these (A1, A4, A5, A8, A10, A11, A14) were the items flagged for this
round.  The rest were found by auditing every calculation newly introduced in
round 17, as instructed.

---

## A1 — The orthonormality statement was made in the wrong measure

**Where.** `appendix_derivations.tex` lines 13–23, opening of
§"Element matrices of the Legendre basis".

**What was written.** The basis `b_j(ζ) = √(2j+1) P_j(ζ)` with
`ζ ∈ [−1,1]`, followed by `∫_{-1}^{1} b_i b_j dζ = δ_ij`.

**What is true.** `∫_{-1}^{1} b_i b_j dζ = 2δ_ij`.  The production basis is
generated on `s = z/d ∈ [−1/2, 1/2]` (`model.py`, `basis()` and `self.z /= 2;
self.weights /= 2`), i.e. `s = ζ/2`, and **in that measure** the Gram matrix is
the identity.  Verified: the independent 301-node rule gives `max|M − I| =
8.2e-14`, `1.1e-13`, `1.3e-13` at `N = 5, 6, 7`, and in the ζ measure the same
integral is `2I` to `1.1e-13`.  The solver's mass matrix `W = b₀ᵀ diag(w) b₀`
agrees with the identity to `1.4e-13`.

**Why it matters.** The whole of §A.2 is quotable against this identity: with
`δ` in the ζ measure the compressibility entry would have been `−2`, the
carrier mass `−2`, and every scalar premultiplied by two.

**Class.** NOTATION OR NORMALISATION ERROR — a measure, not a formula.

**Repair.** Three coordinates are now named and separated (`z`, `ζ = 2z/d`,
`s = z/d`), each element matrix is declared to be an `s`-integral, and the ζ
form is given *as well, with its factor 2*, so the two can never be confused
again: `eq:app_measures`, `eq:app_mass`.

## A2 — Diagonal stiffness: the chain-rule factor was absent

**Where.** Same block, lines 25–40.

**What was written.** `S_jj = ∫(db_j/dζ)² dζ` with no statement of which
variable the prime referred to, and the result quoted as `2j(j+1)(2j+1)`
without the two powers of the chain factor that the derivative brings.

**What is true.** `b_j'(s) = 2√(2j+1) P_j'(2s)`, so
`S_jj = 4(2j+1)·½∫(P_j')²dζ = 2(2j+1)j(j+1)`; the `4` is the chain rule
squared and the `½` is the Jacobian.  Verified at `N = 5, 6, 7`:
`max|S_jj − 2j(j+1)(2j+1)| = 3.8e-12, 1.0e-11, 2.2e-11`, and the model's
assembled stiffness agrees with the independent rule to `2.4e-10`.

**Class.** NOTATION OR NORMALISATION ERROR.

**Repair.** `eq:app_S` now carries the derivation, the Jacobian is named, and
the off-diagonal companion `eq:app_S_off` plus the `N = 6` matrix
`eq:app_S_matrix` are printed with entries verified to `5e-5` absolute
(18.330, 22.978, 80.498, 210.599).

## A3 — The weighted orthogonality was attributed to the unweighted integral

**What was written.** The Legendre identity in the form that follows from
`[(1−ζ²)P_j']' = −j(j+1)P_j`, i.e. under the weight `(1−ζ²)`, presented as if it
were the identity `∫P_i'P_j' = j(j+1)δ_ij` used in `S_jj`.

**Status.** The weighted identity is correct — verified against the closed form
`2j(j+1)/(2j+1)δ_jk` — but it is *not* the integral that appears in `S_jj`, and
the text did not distinguish them.

**Class.** UNSUPPORTED INTERPRETATION (a correct formula attached to the wrong
object).

**Repair.** The weighted form is now labelled as such (`eq:app_S_weighted`), the
unweighted companion is what drives `eq:app_S`, and the sentence states which is
which and why the boundary term in the weighted identity vanishes.

## A4 — The two charge matrices were transposed against each other

**Where.** `appendix_derivations.tex` 71–93, the grounded potential space.

**What was written.** A single matrix `(φ_i, b_j) = δ_ij − r_j δ_{i,j+2}` with the
comment that the other orientation was "the transpose"; and the coefficient
attached to `r_j` in a shape where the test index is `i`.

**What is true.** With `ψ_j = b_j − r_j b_{j+2}`,

* `(ψ_i, b_j) = δ_ij − r_i δ_{j,i+2}` — shape `n_φ × N`, band **above** the
  diagonal, coefficient on the **row** index;
* `(b_i, ψ_j) = δ_ij − r_j δ_{i,j+2}` — shape `N × n_φ`, band **below** the
  diagonal, coefficient on the **column** index.

Verified: `1.1e-14` and `5.8e-15` respectively; the model's own matrix agrees
with the first orientation to `1.2e-14`.  Using `r_j` where `r_i` belongs
changes the largest entry by **0.2981** (`r_0 = 0.4472` against `r_2 = 0.7454`),
which is large enough to change every coupling entry in the assembled block.

**Class.** CONFIRMED ERROR.

**Repair.** Both matrices are now written out with their shapes, their bands and
their indices, `eq:app_charge` and `eq:app_charge_T`, and the block construction
says which one sits in the potential row and which in the carrier row.  The
assembled block reproduces `eq:app_w3` to `8.7e-16`.

## A5 — The transport diagonal was printed with the axial wavenumber in the wrong block

**Where.** `appendix_derivations.tex` 97–142, worked element 2.

**What was written.** `(A00)_{μ_iμ_j} = −(iα_d/ω)(k_x² + k_y² + S_jj)` with values
`−i1.80e-3, −i1.304, −i6.512, −i18.23`.

**What is true.** The `k_x²` power sits in the `A11` block, not in `A00`:
`A00 = −(iα_d/ω)(k_y²δ_ij + S_ij)` and `A11 = −(iα_d/ω)δ_ij`.  Verified: the
assembled `A00` diagonal is `−i1.828e-3, −i1.3039, −i6.5124, −i18.2314,
−i39.0651` for `j = 0…4`, the assembled `A11` value is `−i0.108509`, and the
polynomial combination reproduces `(α_d/ω)(k_x² + k_y² + S_jj)` to `3.6e-15`.
Had the printed bracket been evaluated as written with `k_x² = 0.541990`, the
first entry would have been `−i0.0607` — a factor 33 from the assembled
`−i0.001828`.  The four printed numbers therefore belonged to a *different*
matrix than the one they were attributed to; the numbers themselves were the
`A00` values.

**Class.** ARITHMETIC ERROR (the arithmetic of the printed bracket does not
produce the printed numbers).

**Repair.** `eq:app_w2` splits the two blocks explicitly, `eq:app_w2_values`
lists the assembled values with their scale, and the text states the identity
that the polynomial reproduces.

## A6 — "Largest single entry" of the gradient block

**What was written.** The gradient-stiffness entries listed at 3.85 with the
remark that this was the largest single entry of the block.

**What is true.** At degree four the entries are `0, 3.85, 19.27, 54.00, 115.64`
for `j = 0…4`; 3.85 is the `j = 1` entry and the largest is 115.64
(`λ²c33/c44 = 0.3212`, `S_jj = 2j(j+1)(2j+1)`).

**Class.** CONFIRMED ERROR (a superlative that the numbers contradict).

**Repair.** `eq:app_w4` prints the four entries and states that 115.64 is the
largest at that degree.  Verified independently: `max|err| = 8.8e-4` against
`[3.8547, 19.273, 53.966, 115.64]`.

## A7 — An entry ratio was read as a mode frequency

**What was written.** The inertia entry `−ω²` compared with the `j = 1` gradient
entry and the ratio described as "the thickness-mode frequency scale".

**What is true.** `−ω² = −58.27` and `58.27/3.85 = 15.1`; the frequency of a
thickness mode is an eigenvalue of the coupled quartic `eq:quartic`, not the
ratio of two matrix elements, and no such frequency is computed anywhere in the
manuscript.

**Class.** UNSUPPORTED INTERPRETATION.

**Repair.** `eq:app_w5` keeps the entry and states the ratio, then says in one
sentence what it is not.  This is the round-18 prohibition "do not infer a
physical modal frequency from an isolated matrix-element ratio", applied.

## A8 — The edge operator was given the wrong shape

**Where.** `appendix_derivations.tex` 214–241.

**What was written.** `R ∈ ℂ^{4n×M}` for the stacked traction / double-traction /
blocking / charge blocks, described as "four scalar statements per field on the
two faces", and an equation in which `R` was written twice as if the identity
`y(0) = y_inc + Σ a_j y^{(j)}` needed restating.

**What is true.** The rows are one block per condition on the test functions of
the field it multiplies: `n_u` for the traction, `n_u` for the double traction
(present only when `ℓ ≠ 0`), `n_φ` for the normal displacement and `n_μ` for the
normal flux, so `m = 2n_u + n_φ + n_μ`.  At degree four that is `m = 38` against
`M = n_w = 23` columns: the system is overdetermined by the fifteen
double-traction rows and is solved least-squares by SVD.  It is square only when
`ℓ = 0`, where `m = 23 = n_w` (verified by building `R` at degrees 4, 18 and
with `ℓ = 0`).

**Class.** CONFIRMED ERROR.

**Repair.** `eq:app_edge_R` gives the block structure and the row count; the
text states the overdetermination, the least-squares/SVD solve and the
`ℓ = 0` square case, and the redundant `R y(0) = …` display was replaced by the
linear system it was trying to state.

## A9 — The modal-power normalisation and the `R_B` chain (checked, not changed)

`appendix_derivations.tex` 243–255 were re-derived from the stored amplitudes
and reproduced to `4.2e-15`:

```
|a|^2 = 1.1374909^2        = 1.2938855
|a|^2 P_B                  = -0.023150588
x exp(2 Im k_Bx L) 0.9998954 = -0.023148167
÷ exp(2 Im k_ix L) 1.0001081 = -0.023145598   → R_B = 0.9467952
```

**Class.** CORRECT (no edit).  This is the chain that carries the headline
number, and it was re-verified after every other repair.

## A10 — The Debye ratio was inverted

**Where.** `governing_equations.tex` 880–881.

**What was written.** "The plate is therefore fourteen Debye lengths thin in the
ratio `d/L_D = 1/Q`".

**What is true.** `Q = d/L_D = 0.074635`, so `L_D/d = 1/Q = 13.3986`: the Debye
length is 13.4 times the thickness, and the plate is 7.5 % of a Debye length
thick — it is *thinner* than a screening length, not "fourteen Debye lengths
thin".  Verified twice (`round18_mathematical_audit.py` §1:
`max|err| = 0.0`; `round18_reference_checks.py` §1: `13.39856` against
`13.3986`, relative `3.0e-6`).

**Class.** CONFIRMED ERROR (reversed ratio; the round-18 brief names this
prohibition explicitly).

**Repair.** The sentence now reads `L_D/d = 1/Q = 13.40`, "thinner than one
screening length by more than an order of magnitude", and keeps the separate,
correct statement that the screening coefficient in the blocks is
`Q² = 5.57e-3`.  The other four places where the manuscript quotes the ratio
(`governing_equations.tex` 553–555, `discussion.tex` 121, `results.tex` 134,
`numerical_methods.tex` 76) already said `d/L_D = 0.075: thinner than the Debye
length` and were left alone — they are right.

## A11 — Degree-of-freedom accounting

**Where.** `numerical_methods.tex` 186–192 (equation `eq:nw`).

**What was written.** "With `n` basis functions per mechanical component, `n` for
the potential and `n` for the carrier, `n_w = 5n+3`", then "`n_w = 93` at the
degree used for the reported results and 153 at the highest degree examined",
and "the polynomial has degree `4n_w = 372`".

**What is true.** `n` is the polynomial *degree*, and there are `N = n+1` basis
functions per field, so `n_u = 3N`, `n_φ = N−2` (grounded) or `N−1` (open),
`n_μ = N`, giving `n_w = 5n+3` grounded and `5n+4` open.  The reported results
use `n = 22`, hence `n_w = 113`; `93` is the value at `n = 18` and `153` at
`n = 30`; the quartic degree at the reported degree is `4×113 = 452`, not 372.
Verified by construction and against the solver at `n = 4, 5, 18, 22, 30`
(23/24, 28/29, 93/94, 113/114, 153/154), and the reported degree is confirmed by
the stored datasets (`figure_data/peak_search.json`, rows with `degree = 22`).

**Class.** CONFIRMED ERROR (a basis-function count used where a degree belongs,
and a size belonging to a different degree).

**Repair.** `eq:nw` now defines `N = n+1`, gives both circuit cases, and quotes
113 at `n = 22`, 93 at `n = 18`, 153 at `n = 30` and quartic degree 452.

## A12 — "`A22 = A12 = 0`"

**Where.** `numerical_methods.tex`, the paragraph after `eq:polynomial`.

**What was written.** That the classical limit "returns the familiar quadratic
problem, and it does so identically, with `A22 = A12 = 0`".

**What is true.** The blocks that vanish identically for every `ℓ` are `A02` and
`A20` (verified: Frobenius norm exactly `0.0`).  `A12`, `A21` and `A22` are
proportional to `ℓ²` and vanish only at `ℓ = 0` (verified by rebuilding the
operator with `λ = 0`: `‖A12‖ = ‖A21‖ = ‖A22‖ = 0.0` exactly, against
`4.04, 4.04, 0.7115` with `λ = 0.25`).

**Class.** CONFIRMED ERROR.

**Repair.** The sentence now names the three `ℓ²` blocks, says they vanish at
`ℓ = 0` leaving `A00 + k_x A01 + k_x² A11`, and keeps the separate, correct
statement that `A02 = A20 = 0` for every `ℓ`.

## A13 / A15 — Measure slips in the block construction

**Where.** `numerical_methods.tex` 131 (`eq:block`) and
`appendix_derivations.tex` 233ff (`eq:app_block`).

**What was written.** `⟨a,b⟩ = ∫_{-1}^{1} a*ᵀ b dζ`.

**Why it is wrong.** With that measure the compressibility term
`⟨W,W⟩ = −2δ`, not `−δ`, contradicting `eq:app_w1` and the assembled `−1`.
Verified: the same integral is `δ` in `ds` and `2δ` in `dζ` (`1.1e-13`).

**Class.** NOTATION OR NORMALISATION ERROR.

**Repair.** Both occurrences now use `∫_{-1/2}^{1/2} … ds` and point at
`eq:app_measures`.

## A14 — The coupling matrix in the results section

**Where.** `results.tex` 706–716, the paragraph explaining `fig:fig08`.

**What was written.** Rows `0, 0, 26.83, 91.65, 187.8, 315.9`, "and is
upper-triangular", "with `h = ±1.06×10⁻²` the largest entry is 3.35".

**What is true.** The coupling block is `h∫ b_i'' b_j ds` against the **carrier**
basis (not `ψ_j`).  It vanishes unless `j ≤ i−2`, so it is **lower** triangular
with two bands; at degree six its row norms are
`0, 0, 26.83, 91.65, 222.89, 450.87, 809.44`, its largest entry is 580.5, and
`h × 580.5 = 6.13`, i.e. 10.5 % of `ω² = 58.27`.  The printed 187.8 and 315.9
were two *entries* of the matrix (`(4,0)` of an `ψ`-based matrix and `(5,3)`
here), not row norms; 3.35 was `h × 315.9`.

**Class.** CONFIRMED ERROR (structure, statistic and size all wrong).

**Repair.** `eq:H_entry` now states the measure and the carrier basis; the text
gives the lower-triangular structure, the seven row norms, the largest entry
580.5 and the assembled `h·580.5 = 6.13`, and compares it to `ω²` and to the
largest diagonal entry of the same rows (`2.16×10⁵`) without drawing a frequency
from it.  Verified independently in `round18_reference_checks.py` §7.

## A16 — The constitutive, momentum, Gauss and carrier equations (checked, kept)

`governing_equations.tex` 310–340 and 420–470 were checked component by
component against the assembled fields at `p = 5` with random coefficients
(`round18_mathematical_audit.py` §9).  Every relation holds to machine
precision:

| relation | max abs error |
|---|---|
| `σ_xz = 2c44 ε_xz − e15 E_x` | `7.1e-15` |
| `σ_yz = 2c44 ε_yz − e15 E_y` | `4.0e-15` |
| `σ_xy = 2c66 ε_xy` | `1.0e-15` |
| `σ_zz = c13(ε_xx+ε_yy) + c33 ε_zz − e33 E_z` | `2.3e-13` |
| `σ_xx = c11 ε_xx + c12 ε_yy + c13 ε_zz − e31 E_z` | `5.7e-14` |
| `D_x = κ11 E_x + 2e15 ε_xz` | `2.7e-15` |
| `D_y = κ11 E_y + 2e15 ε_yz` | `8.9e-16` |
| `D_z = κ33 E_z + e31(ε_xx+ε_yy) + e33 ε_zz + f u3''` | `2.8e-14` |

The conventions that make them true are stated in the manuscript: `E = −∇φ`,
Voigt shear strains carry the factor 2, and the solver's fields are scaled by
`c44` and `κ33` (stresses) and by `√(c44κ33)` (couplings).  `τ_zzz` is the one
object the solver does not return (`fields()` has no `tauzz` key); its `f` and
`H` terms were verified by source inspection and are exercised by the
edge/dissipation checks, and the manuscript's `eq:tauZnO` is consistent with the
code including the sign (`−f E_z = +f φ'`).

**Class.** CORRECT UNDER EXPLICIT CONVENTION.

---

## What the audit also checked and did **not** need to change

* the mass matrix is the identity in the implemented measure at `p = 4, 5, 6`
  (`≤ 1.4e-13`);
* parity: entries of `S` with `i+j` odd are `≤ 4.6e-15`;
* `ψ_j(±½) = 0` to `8.9e-16` and `Q r₀ = Q/√5 = 0.033378`;
* sized accounting of the state operator (`4n_w × 4n_w = 76 × 76` at `p = 4`)
  and of the boundary vector (`38`);
* the block Frobenius norms printed in `eq:block_norms`
  (`1.888e4, 567.0, 235.0, 4.04, 0.7115`) — recomputed from the solver, all five
  reproduce, and `A02 = A20 = 0` exactly;
* the `R_B` chain of A9, which is the only place a reported number is assembled
  by hand.

## Consequences for the rest of the round

Because A1–A15 are all *presentational* — a measure, an index, a count, a
statistic, a word — no material constant, no solver, no dataset, no figure and
no reported peak moved.  The four correctness verdicts in
`PAPER_A_ROUND18_CORRECTNESS_VERDICTS.md` are stated against exactly this split.
