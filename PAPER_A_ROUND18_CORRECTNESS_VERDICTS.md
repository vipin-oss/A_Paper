# Paper A — Round 18: four correctness verdicts

**Branch** `arena/ea7ca4dd-a-paper` · **BUILD UNVERIFIED**.
Scope: the mathematics newly introduced in round 17, as repaired in round 18.
The four verdicts are deliberately separated, because a derivation can be right
while the arithmetic printed from it is wrong, and both can be right while the
implementation disagrees.

---

## Verdict 1 — Analytical correctness of the derivations: **PASS (conditional on the declared conventions)**

*Every closed-form statement in Appendix A and in the round-17 additions of the
four main sections has been re-derived from its own definition and compared with
an independent evaluation.*

What is now correct and why:

| statement | how it was established |
|---|---|
| `b_j = √(2j+1)P_j(2s)`, `∫b_ib_j ds = δ_ij` | Legendre orthogonality + Jacobian, and three quadrature orders |
| `S_jj = 2j(j+1)(2j+1)` | chain rule `(2)²` and Jacobian `½`, from `∫(P_j')² = j(j+1)` |
| weighted orthogonality `2j(j+1)/(2j+1)` | integration by parts of the Legendre equation; now labelled as the weighted form and not used where it does not belong |
| `ψ_j(±½) = 0`, `r_j = √((2j+1)/(2j+5))` | direct substitution of `P_j(±1)` |
| `(ψ_i,b_j)` vs `(b_i,ψ_j)` | both shapes and both bands derived and computed; the two differ, and the text no longer treats them as the same object |
| `S = σ − ik_xτ⁰ − ik_yτ¹ − ∂_zτ²` | matches `fields()` line for line |
| `τ_zzz = ℓ²c33η_zzz + … − fE_z + HΔn` | matches `fields()` including the sign `−fE_z = +fφ'` |
| `D_i` components | eight component identities verified to `1e-15 … 2.3e-13` |
| `A02 = A20 = 0` | exactly zero at every degree and every `ℓ` |
| `A12, A21, A22 ∝ ℓ²` | exact zero when `λ = 0`, non-zero otherwise |
| `m = 2n_u + n_φ + n_μ` | counted from the test functions each condition multiplies; `38` at `p = 4`, `150` at `p = 18` |

The condition is the one the manuscript now states explicitly: `E = −∇φ`, Voigt
shears carry the factor 2, and the solver's fields are scaled by `c44`/`κ33`
(stresses, permittivities) and `√(c44κ33)` (couplings).  Under those conventions
no statement in the repaired appendix is unproven; under a different one several
would change sign or factor 2, which is why they are printed.

**Residual uncertainty.** `τ_zzz` is not returned by `fields()`, so its `f` and
`H` terms are verified by source inspection plus the edge and dissipation tests,
not by a component-level check.  This is a gap in the *tooling*, not in the text,
and it is stated in the audit log.

## Verdict 2 — Arithmetic correctness: **PASS**

Every number printed in the repaired passages was recomputed from its definition
and the definition was evaluated twice (once by the solver-side audit, once by the
solver-free reference).  Maximum errors, absolute and relative:

| quantity | max abs error | max relative error |
|---|---|---|
| `S_jj` vs `2j(j+1)(2j+1)` | `2.2e-11` | `2e-14` |
| `S` matrix at `N = 6` vs print | `4.9e-5` | `2e-7` |
| mass identity | `1.3e-13` | `1.3e-13` |
| `ψ_j(±½)` | `8.9e-16` | — |
| charge matrices | `1.2e-14` | `1.2e-14` |
| transport diagonal `A00` | `4.3e-19` | `4.3e-19` |
| transport identity `(A00 + k_x²A11)` | `3.6e-15` | `2e-16` |
| charge block `A_{φμ}` | `8.7e-16` | `8.7e-16` |
| gradient entries | `8.8e-4` | `7.6e-6` |
| coupling row norms | `4.6e-5` | `6e-8` |
| coupling largest entry | `2.6e-3` (print `580.5`) | `4.4e-6` |
| DOF counts | `0` | `0` |
| `R_B` chain | `4.2e-15` | `3.7e-18` |
| dimensionless groups | `2.9e-7` (on `c_s`) | `5.8e-5` (print rounding of `T`) |

**The seven flagged items are all in this table**, each with a number: the
measure (row 3), the stiffness chain (row 1), the index orientation (row 5), the
transport bracket (row 6–7), the edge shape (row 12, `0` error after repair),
the Debye ratio (group table, `3.0e-6`), the DOF count (row 12).

**One thing that was *not* accepted on plausibility:** the transport diagonal.  The
round-17 values were numerically right and dimensionally attached to the wrong
matrix.  Only recomputing the bracket revealed it — with `A00` and `A11`
separated, the first entry is `−i1.828e-3`; with the printed bracket it would be
`−i0.0607`.

## Verdict 3 — Agreement between text and implementation: **PASS**

| statement in the text | implemented | check |
|---|---|---|
| measure and basis | `self.z /= 2; self.weights /= 2`, `√(2j+1)P_j(2z)` | `1.4e-13` |
| mass = identity | `W = b₀ᵀ diag(w) b₀` | `1.4e-13` |
| stiffness diagonal | assembled `S` | `2.4e-10` vs independent rule |
| grounded space | `self.np = n−2`, `pb` | charge matrix `1.2e-14` |
| block assembly | `matrices()` vs `eq:block` terms | `A02 = A20 = 0`; five norms reproduce |
| constitutive relations | `fields()` | `1e-15 … 2.3e-13` |
| edge system shape | `boundary_vector` length `2n_u + n_φ + n_μ` | `38` at `p = 4` |
| degree/DOF counts | `plate.nw` | `23/24, 28/29, 93/94, 113/114, 153/154` |
| headline share | `edge()` solve | asserted `0.9467952307`, suite `OK` |

No line of `model.py` was edited: `git diff` on the repository contains only
`.tex` files, the static-validation record, and the two new audit scripts.

## Verdict 4 — Physical interpretation: **PASS WITH STATED LIMITS**

Repaired or re-worded:

* **Debye length.** `L_D/d = 13.4`, not "fourteen Debye lengths thick".  The
  physical claim that survives is the one the numbers support: the plate is
  7.5 % of a Debye length thick, so the carrier perturbation is not a surface
  layer, and screening enters with the small coefficient `Q² = 5.6e-3`.
* **Entry ratios.** `58.27/3.85 = 15.1` is a ratio of two matrix entries at one
  frequency; the frequency of a thickness mode is an eigenvalue of the coupled
  quartic.  The text now says so, and no mode frequency is inferred anywhere.
* **Coupling size.** `h·580.5 = 6.13` is 10.5 % of `ω² = 58.27` and `4.5` orders
  below the largest diagonal entry of the same rows (`2.16e5`); the operator is
  row-equilibrated before solution, so the entry is a scale statement about the
  coupling.  What it predicts — flux profiles within 0.9 % of the peak across the
  five coupling levels while the partition still differs measurably — is what
  `fig:fig08` and `fig:fig07` show.

Limits that remain, unchanged from round 17 and not repairable by arithmetic:

1. `ℓ`, `f` and `H` are synthetic; `H*` is an order-of-magnitude bound, `h = 1.06e-2`
   is a chosen operating value.
2. The corner line force is enforced weakly, not pointwise.
3. Novelty against the primary 2025 source is open (closed access); only the prose
   comparison exists.
4. The build is unverified: no PDF was produced and no page was inspected.

## Overall

**PASS on all four axes, with the four limits above accepted and stated.**  The
manuscript's mathematics is now internally consistent, its printed numbers are
reproducible from their definitions by a script that shares no code with the
solver, and the text agrees with the implementation wherever the two can be
compared.  The item that remains genuinely open is not mathematical: it is the
build, which cannot be verified in this environment.
