# Paper A — Round 19: edge-system verification (R19-3)

## 1. The claim that was in the manuscript

> At degree four (n_u = 15, n_φ = 3, n_μ = 5) this is m = 38 rows against M = n_w = 23 columns:
> the edge system is overdetermined by the fifteen double-traction rows and is solved in the
> least-squares sense by a singular-value decomposition.

Measured shape of the matrix the solver actually builds and solves, at that degree: **38 × 38**.
The claim is off by fifteen columns and the word "overdetermined" is wrong.

## 2. The three objects, separated

The round-18 text used `y`, `R` and `B` loosely. They are three different things with three
different second dimensions, and only two of them agree:

| object | definition | type at degree 4 | at degree 22 |
|---|---|---|---|
| modal state y⁽ʲ⁾ | the eigenvector of the pencil, ordered as coefficients then conjugates | C⁷⁶ | C³⁶⁴ |
| boundary operator R | applies the four edge conditions to *one state* | C^{38×76} | C^{182×364} |
| boundary matrix B | `B = [R y⁽¹⁾ … R y⁽ᴹ⁾]`, one column per outgoing mode | C^{38×38} | C^{182×182} |
| right-hand side b_inc | `b_inc = R y_inc` | C³⁸ | C¹⁸² |

The system solved is `B a = −b_inc` in the scaled unknowns a. The state dimension N_s never
enters B: it is the column dimension of R and the row dimension of nothing.

## 3. Why it is square, not overdetermined

Two counts, both structural:

1. The number of decaying states is half the state dimension: M = N_s/2 = n_w + n_u (cases A, B,
   D of the hyperstress audit) and M = n_w in the classical limit.
2. The number of independent edge conditions is m = 2n_u + n_φ + n_μ, and
   n_w = 3N + n_φ + n_μ with n_u = 3N gives m = 2n_u + n_φ + n_μ = n_w + n_u = M.

Equality of these two counts is the content of eq:app_edge_square. It is not a coincidence of
degree four: the table in `PAPER_A_ROUND19_PRE_EDIT_VERIFICATION.md` §3 verifies it at degrees
4, 6, 18, 22 and 30, in each case with rows − columns = 0 and rank = columns.

## 4. What the rank criterion does and does not prove

The solver row- and column-scales B and solves through an SVD, requiring rank(B) = number of
columns at a cut-off of 1e-12 of the largest singular value. That criterion is a statement about
the **conditioning of the edge operator**, not about the **physical admissibility of the edge
conditions** — a square system can be full rank and still impose a boundary condition that the
physics does not justify, and a small residual in `B a = −b_inc` proves only that the matching
was solved. The manuscript now says this explicitly (numerical_methods.tex, immediately after
the SVD sentence): admissibility is argued from eq:bc_edge independently, and the hyperstress
audit is where that argument is made.

Numbers at the operating point, degree 22: 182 rows, 182 columns, rank 182, condition number
**160.48**, scaled residual 3.1e-15. Degree 4: 38 / 38 / 38.

## 5. The seven regression tests

`paper_a_study/round19_tests.py`, seven tests, all passing (`all seven passed`, exit 0):

| test | claim | independent reference | result |
|---|---|---|---|
| T1 | pencil and polynomial share one spectrum | eigenvalues of a hand-built pencil vs roots of the scalar polynomial; plus closed-form (r,s) identity and annihilation of the eigenvector | max abs 6.6e-12 (deg 4), 3.9e-10 (deg 6); rel 1.6e-13 / 4.9e-12; ‖p(k)q‖ ≤ 1.8e-15 |
| T2 | block structure | rank A₂₂ = n_u; A₀₂ = A₂₀ = 0; f enters A₀₀ only | all exact / 4.6e-9 |
| T3 | edge system square and full rank | counted from n_w, n_u, n_φ, n_μ and compared with the assembled B | rows − columns = 0 at 4, 18, 22; rank = columns |
| T4 | degree-22 modal-power chain | recomputed from the stored row in `modal_flux_audit.json` | 0.0231505 → 0.0231481 → 0.0231456 |
| T5 | stiffness parity, not banded | independent 60-point quadrature vs the printed 6×6 matrix | max abs 8.5e-4 (tol 1e-4 × 660); opposite parity ≤ 2.4e-15; row-5 span 4, not 2 |
| T6 | three separate numbers | operating point, k_xd = 0.55 row, refined-search peak | 0.0231456 / 0.5791800 / 0.9467952, all distinct |
| T7 | constants and sign | constants retyped from the manuscript table | c_s, T, L_D, Q, L_D/d, H_ref, h, f, λ to ≤ 3.4e-8 |

T1 is the test that would have caught R19-6 had it existed in round 18: a single sign error in
A₃ changes the closed form by O(10⁵) and the eigenvalue matching fails loudly.

## 6. Confidence statement

The edge system is square and well conditioned at every degree the paper reports, its rank
criterion is met with five orders of magnitude to spare, and the counts that make it square are
derived from the constitutive model rather than fitted. What is *not* claimed is that the
boundary conditions are physically complete: case C of the hyperstress audit is the one place
where they are not, and it is excluded from the model rather than solved.
