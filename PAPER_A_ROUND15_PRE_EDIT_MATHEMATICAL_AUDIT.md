# Round 15 — pre-edit independent mathematical audit

Baseline: `18e3cb627e2af9c630d60477955c3f65ef5033ca`, branch
`arena/ea7ca4dd-a-paper`. Every equation introduced or modified in round 14 was
re-derived from the enthalpy, the balance laws and the implemented operator
before anything was edited. Nothing in the round-14 self-assessment was taken as
evidence.

Classification: **CE** confirmed mathematical error · **ID** incomplete
derivation · **NE** notation error · **ME** misleading explanation · **AC**
already correct · **UV** unverified.

| ID | Equation (round 14) | Mathematical defect | Evidence | Solver impact | Severity | Required correction |
| --- | --- | --- | --- | --- | --- | --- |
| M15-1 | `eq:var_kinematics`: `δη_ijk = ½(δu_i,jk + δu_j,ik) = δu_i,jk` | **CE.** The final equality is asserted between tensor components. It is false: the antis symmetric part in (i,j) is not zero in general. Only the contraction with a hyperstress symmetric in (i,j) annihilates it. | Random τ (τ_ijk = τ_jik) and random δu: `max|δη − δu| = 0.962` component-wise, while `τ:δη = −0.450615573385995` and `τ:δu = −0.450615573385994`, difference `3.3e-16`. | None — the implementation contracts through `C`/`λ²` blocks that act on symmetric (engineering) strain components. | **High**: a referee reads it as a tensor identity and rejects the derivation. | Replace by the component relation plus the contracted identity `τ_ijk δη_ijk = τ_ijk δu_i,jk`, with the reason (η symmetric ⇒ τ symmetric). Done. |
| M15-2 | `eq:weak_form` (single integral, `+μ̃N*`, RHS `ω²ρûv`) | **CE + ME.** One integral is presented as "the weak form" while it mixes the mechanical balance, Gauss's law and carrier continuity, and the carrier term shown is the electrochemical part of the enthalpy, not the transport equation. The carrier equation has its own time-harmonic accumulation and its own natural condition. | Strong residual implemented in `model.py` (`carrier = −iω N − α_d ∂_i∂_i μ̃`) is not obtainable from the displayed integral; the assembled carrier block is `−(iα_d/ω)⟨∇μ̃,∇Φ⟩ − ⟨N,Φ⟩`, which is the weak form of that continuity equation. | None on numbers: the code discretises the correct three equations. The manuscript misdescribed them. | **High**: the manuscript does not state what it discretises. | Split into (A) mechanical, (B) Gauss, (C) carrier continuity, (D) assembled block system; state that `μ̃` is the carrier unknown and `N = μ̃ + Qφ`. Done. |
| M15-3 | `eq:quartic` and `eq:polynomial` | **ID/ME.** The nine-block sum is displayed as if all nine blocks exist. Two of them are identically zero, `A₀₂ = A₂₀ = 0`, and this is never said; a reader will look for a missing term. | `‖A₀₂‖ = ‖A₂₀‖ = 0.000e+00` in the assembled operator (no field of the enthalpy carries two derivatives in `x`). | None. | Medium. | State the two vanishing blocks; state the Hermiticity structure. Done. |
| M15-4 | `eq:quartic` coefficients | **AC.** The regrouped polynomial is exact. | Expansion identity against `Σ(−ik_x)^r(ik_x)^s A_rs` at k = 0.17, −0.53, 0.99, 2.40: max deviation `3.6e-12` absolute against entries of `1.4e6`. | — | — | None. |
| M15-5 | `α` used for both spatial attenuation and the transport group | **NE.** `§2.9` already defines `α_d = D/(dc_s)` and reserves `α` for `2|Im k_x|`; round 14 used bare `α` for the transport group in the weak form and in the block construction. | `governing_equations.tex` l. 472 defines `α_d`; `numerical_methods.tex` used `α` in three places. | None. | Medium: an unambiguous symbol was made ambiguous. | Use `α_d` in the weak form and the block; keep `α` for the attenuation. Done. |
| M15-6 | Nomenclature table `@{}ll p{7mm} ll@{}` | **CE (format).** The column specification declares five columns for a four-cell row, so the third cell — a symbol — is typeset into a 7 mm column and overflows; it is not a spacer. | Column count vs cell count in `main.tex`. | None. | Medium (visible in the PDF the supervisor builds). | Four-column specification with an inter-pair gap that is not a column: `@{}ll@{\qquad}ll@{}`, plus notation de-collisions (`D` vs `D_i`, `α` vs `α_d`, `μ̃` vs `μ_e`). Done. |
| M15-7 | Piezoelectric signs `σ = cε − e E`, `D = κE + e ε` | **AC, with a convention note.** The pair is thermodynamically consistent (both are derivatives of one `w` with `−eEε`), and the implemented pair `(+⟨G,e,B⟩, +⟨B,eᵀ,G⟩)` is consistent with it once the sign of the electric-field operator is carried with the unknown. Row-wise the two conventions agree; no sign error is demonstrated. | Block-by-block check of `Plate.matrices` against the four constitutive relations; the independent strong-form propagator uses the same convention and agrees to `1e-10`. | None. | — | None; recorded as a convention, not as a defect. |
| M15-8 | Corner line force | **UV, unchanged.** The variational surface terms include a corner (boundary-of-boundary) contribution which the model does not resolve pointwise. | `§2.6` states it; `corner_assessment.py` measures a non-zero line-force density `>1e-4`. | Known, unchanged. | **Blocking for any claim of a complete strong boundary formulation.** | Not repaired; reported as a limitation (see the boundary audit). |

## What the audit did **not** find

- No error in the constitutive relations `eq:sigma`–`eq:mu`.
- No error in the strain/curvature amplitude relations `eq:strain_amplitudes`,
  `eq:eta_amplitudes` (finite-difference check, `≤7.4e-11`, round 14, re-run
  round 15 with a different seed set).
- No error in the sign of the double divergence in `eq:momentum`.
- No error in `eq:RB`, including the two retained exponentials.
- No error in the energy identity `eq:energy_identity`.
