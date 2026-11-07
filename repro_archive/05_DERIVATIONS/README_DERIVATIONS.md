# README_DERIVATIONS

The written derivations behind the formulation and the gates: governing and constitutive
statements, the weak form and its natural boundary data, the nondimensionalisation, the
edge system, and the two derivations that decide how the results may be worded
(Gate 1: natural boundary data; Gate 2: corner line force).

These files are the **derivation record of the project**, not a textbook. Where a
derivation was later found wrong, the file that found it wrong is here too, and the
`sections/` in `02_OVERLEAF` carry the corrected version.

---

## 1. Reading order

| # | File | What it derives | Status |
|---|---|---|---|
| 1 | `PAPER_A_ROUND15_COMPLETE_COUPLED_WEAK_FORM.md` | the complete coupled weak form: three weak equations (mechanical, Gauss, carrier continuity), every surface term, all natural boundary data | foundational |
| 2 | `PAPER_A_ROUND16_CONVENTIONS_AND_DIMENSIONS.md` | signs, index conventions, units of `A`, `τ`, `H`, and where each unit comes from | foundational |
| 3 | `PAPER_A_ROUND16_CARRIER_STRONG_TO_WEAK_DERIVATION.md` | the carrier equation from strong form to weak form, including the electrochemical-potential substitution | foundational |
| 4 | `PAPER_A_ROUND14_MATHEMATICAL_DERIVATION_MATRIX.md` | equation-by-equation matrix of what is derived where, with the check that catches each error | map |
| 5 | `PAPER_A_ROUND17_MATHEMATICAL_DERIVATIONS.md` | the 2.5D reduction, the quartic polynomial, the block structure, the finite-root count | method |
| 6 | `PAPER_A_ROUND17_WORKED_CALCULATIONS.md` | the numbers worked by hand: `c_s`, frequency unit, `a`, `L_D`, the five groups, `R_B` from four stored numbers | method (arithmetic) |
| 7 | `PAPER_A_ROUND19_HYPERSTRESS_AND_BOUNDARY_AUDIT.md` | hyperstress on the faces and the edge; why a plain traction check fails | audit → **found a defect** |
| 8 | `PAPER_A_ROUND20_VARIATIONAL_BOUNDARY_DERIVATION.md` | the variational boundary derivation that repaired it: corner term, edge traction, which data the spectral solution really satisfies | **current** |
| 9 | `PAPER_A_ROUND20_HYPERSTRESS_AND_CORNER_AUDIT.md` | the repair, re-derived and re-checked | **current** |
| 10 | `PAPER_A_ROUND20_FACE_VS_EDGE_NORMAL_AUDIT.md` | face normal vs. edge normal: the two are not interchangeable, and the earlier text conflated them | **current** |
| 11 | `PAPER_A_ROUND21_GATE1_DERIVATION.md` | Gate 1: the identity that must hold between the reconstructed natural data and the spectral solution (incident `~1e-13`, reflected `≲1e-6`, plain traction `1.7e+1`) | **current, decisive** |

Machine-readable counterparts: `03_DATA/figure_data/gate1_*.json`, `corner_assessment.json`,
`round21/*.json`; the executable gates are
`01_PROGRAM/paper_a_study/round21_gate1_traction.py` and `round21_gate_corner.py`.

## 2. The equations in one place

For convenience, the statements that the derivation files establish (the manuscript's
`sections/governing_equations.tex` is the authoritative rendering):

```
ε_ij = ½(u_i,j + u_j,i),        η_ijk = ε_ij,k
w_g  = ½ ℓ² c_ijlm η_ijk η_lmk ,   A_ijklmn = ℓ² c_ijlm δ_kn   (third and sixth slots = gradients)

σ_ij = c_ijkl ε_kl − e_kij E_k + H_ijk Δn
τ_ijk = A_ijklmn η_lmn + H_ijk Δn − f_lijk E_l
D_i  = κ_ij E_j + e_ijk ε_jk + f_ijkl η_jkl
μ̃   = a Δn − q φ + H_jkl η_jkl ,        a = k_B T / n_0

σ_ij,j − τ_ijk,jk = ρ ü_i ,    D_i,i = −q Δn ,    Δṅ = ∇·(D ∇Δn − μ_e n ∇μ̃/q)
```

Nondimensionalisation: lengths `÷ d`, stresses `÷ c_44`, time `÷ d/c_s`, densities `÷ n_0`,
energies per carrier `÷ k_B T`; groups `Q = d/L_D`, `α_d = D/(d c_s)`, `λ = ℓ/d`,
`f = f_3zz/(d√(c_44κ_33))`, `h = H/(d√(a c_44))`.

Sensitivity / Fisher-information content: the archive contains **no** Fisher-information
or Cramér–Rao derivation, and the paper makes no such claim — the sensitivity information
that exists is the explicit finite-difference sweep `fig07_coupling_sensitivity.csv`
(relative change of `R_B` under `k_y` detuning: 1.21 % at the operating point, 36.1 % at
the peak) and the parameter sweeps `fig02`, `fig03`.  Stated here so nobody assumes a FIM
analysis was performed.

## 3. Known-wrong statements, kept on purpose

These are preserved because the correction is part of the scientific record, and the
manuscript's history section refers to them:

| Statement (old) | Why it is wrong | Where corrected |
|---|---|---|
| "the traction is zero on the edge, checked pointwise" | the spectral solution satisfies the natural data in the weak sense; pointwise sampling at the nearest Gauss node is not the boundary data | `round20_variational_boundary_derivation`, Gate 1 |
| "`τ31` alone vanishes at the corner" | the corner line force involves the full hyperstress combination plus the corner term | `round21_gate_corner`, `PAPER_A_ROUND20_HYPERSTRESS_AND_CORNER_AUDIT.md` |
| "`R_B` is the reflectance" | it is one modal share of the partition | `fig05`, `test_backward_share_is_never_called_a_reflectance` |
| "the alternative contraction of `A` is equivalent" | it misses the SH branch by a residual of `3e6` | `governing_equations.tex`, `test_gradient_exact_fundamental_SH` |
| "the corner is fully resolved" | only a **bounded closure** was achieved (exponent ≈ −0.63, partition shift `3.9e-6`) | `PAPER_A_ROUND21_FINAL_SUBMISSION_DECISION.md` |

## 4. Notation

`d` thickness; `ℓ` gradient length; `λ = ℓ/d`; `c_s = √(c_44/ρ)`; `a = k_BT/n_0`
(compressibility, J·m³); `L_D` Debye length; `Q = d/L_D`; `K = k_x d`, `KY = k_y d`,
`Ω = ω d/c_s`; `R_B` backward **modal share**; `P_x` thickness-integrated axial power
(negative away from the edge); `H*` plotting normalisation `= H_bound/√5`;
`H_bound = ℓ√(a c*)`; `s` Schur number.
