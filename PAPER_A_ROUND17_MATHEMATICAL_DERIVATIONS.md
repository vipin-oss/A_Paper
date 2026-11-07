# Paper A — Round 17 mathematical derivations (Parts C and D)

**Branch** `arena/ea7ca4dd-a-paper` · base `a68bb76` · BUILD UNVERIFIED (no TeX
engine in this environment).

This report lists every mathematical block added in round 17, where it sits, and
what in the implementation fixes its signs and factors. The rule applied
throughout: a derivation was written only if it can be checked against
`paper_a_study/model.py`, and where the code and a textbook form differ, the code
is described as it is and the difference is named.

---

## 1. Constitutive derivatives from the enthalpy (Part C, item 1)

**Where:** `sec:governing_constitutive`, new equations `eq:diff_el`,
`eq:diff_coup`, `eq:diff_elec`, `eq:diff_carr`, `eq:euler`.

Eight derivatives of the single enthalpy are written out, each as a pair of
halves that merge because of the tensor symmetries, then collected:

```
∂w_el/∂ε_ij  = ½c_klij ε_kl + ½c_ijkl ε_kl = c_ijkl ε_kl
∂w_grad/∂η   = A_ijklmn η_lmn
∂w_piezo/∂ε  = −e_kij E_k          ∂w_flexo/∂η = −f_lijk E_l
∂w_diel/∂E_i = −κ_ij E_j           ∂w_piezo/∂E_i = −e_ijk ε_jk
∂w_flexo/∂E_i = −f_ijkl η_jkl
∂w_carr/∂Δn  = a Δn                ∂w_H/∂Δn = H_jkl η_jkl
∂w_es/∂Δn    = −q φ
```

Two remarks are attached that were not in the paper before and that a referee
can use as a check:

* the symmetries `c_ijkl = c_jikl = c_klij` and `A_ijklmn = A_lmnijk` are what
  merge each quadratic pair; without them the same energy would give a different
  stress;
* `w` is homogeneous of degree two except for `−qΔnφ`, so Euler's theorem gives
  the identity `eq:euler`. That identity is used twice later (internal energy of
  a mode; energy budget of the edge solve) and it is the reason the factor ½ and
  the electrostatic term appear where they do.

**Consistency with the implementation.** `D_i = −∂w/∂E_i` with the code's
`e[k,j]` (field index first) is what makes `sigma = strain@C.T + grad_phi@e`
equal `σ = Cε − e^T E`; this is why `D` in the paper carries `+2e₁₅ε_xz` rather
than `−2e₁₅ε_xz`. The first draft of this block had the sign and the shear index
wrong; both were corrected against `model.py` before the file was saved, and the
correction is recorded in the round-17 audit log line `D components corrected`.

## 2. The 6mm ZnO reduction, explicitly (Part C, item 2)

**Where:** end of `sec:governing_constitutive`, equations `eq:CZnO` (6×6 elastic
matrix with the five constants and `c₆₆ = ½(c₁₁−c₁₂)`), `eq:ZnOe` (3×6
piezoelectric matrix with `e₃₃, e₃₁, e₁₅`), `eq:sigmaZnO` (six component
relations), `eq:tauZnO` (the one hyperstress component the two non-classical
constants touch), `eq:DZnO` (three electric components).

Only components the implementation has are written:

* `A_ijklmn = ℓ²c_ijlm δ_kn` — the gradient modulus is *not* an independent
  tensor in this model, and `eq:tauZnO` shows that only `τ_zzz` receives the
  `−fE_z` and `+HΔn` terms, because `f ≡ f₃zz` and `H ≡ H_zzz` are single
  components;
* `D_z` carries `+f η_zzz` and `D_x, D_y` carry no flexoelectric term at all,
  which is exactly what `model.py` assembles (`D[:,2] += f·∂_z u3`);
* the factors of two in `σ_xz = 2c₄₄ε_xz`, `σ_xy = 2c₆₆ε_xy` are the
  tensor-to-Voigt conversion, and the manuscript says so, because the program
  stores `γ = 2ε` in the shear slots while the paper writes `ε`.

## 3. From constitutive laws to field equations (Part C, item 3)

**Where:** `sec:governing_constitutive`, `eq:momentum_expanded`, `eq:Hterm`;
`sec:governing_electric`, `eq:gauss_expanded`.

The out-of-plane balance is written out in full with the 6mm constants, because
it is the only component that carries all four sectors. The hyperstress term is
treated honestly: of its derivatives only the `(j,k)=(z,z)` one meets `f` and
`H`, so `eq:Hterm` shows the non-classical contribution to the balance is
`f ∂_z²∂_zφ + H ∂_z²Δn` — a second thickness derivative of the potential and of
the carrier density driving a fourth-order mechanical operator. The elastic
`ℓ²c₃jlm η_lmk` remainder is described by its two leading combinations,
`ℓ²c₄₄` (shear) and `ℓ²c₃₃` (thickness stretch).

Gauss's law is expanded the same way (`eq:gauss_expanded`): dielectric operator,
then piezoelectric and flexoelectric charge, with `−qΔn` on the right.

## 4. The characteristic polynomial, power by power (Part C, item 4)

**Where:** `sec:governing_reduction`, `eq:sector_blocks`, `eq:coeffs`.

* `eq:sector_blocks` gives the `3×3` block structure by sectors
  `(û, φ̂, μ̃)`, with each block named as the bilinear form it is
  (`⟨B,CB⟩`, `⟨B,e^T G⟩`, `⟨G,κG⟩`, `−Q⟨G⁽⁰⁾,B⟩`,
  `−⟨W,W⟩ − (iα_d/ω)⟨MG,MG⟩`), and states that the symmetric part is the
  Hessian of the discretised enthalpy while the only antisymmetric contribution
  is the carrier transport form — i.e. the entire source of loss.
* `eq:coeffs` gives `A(k_x) = A₀ + k_xA₁ + k_x²A₂ + k_x³A₃ + k_x⁴A₄` with
  `A₀=A₀₀`, `A₁=i(A₀₁−A₁₀)`, `A₂=A₁₁−A₀₂−A₂₀=A₁₁`, `A₃=i(A₁₂−A₂₁)`, `A₄=A₂₂`,
  and states which are Hermitian.
* The **degree count is derived, not asserted**: a term of the enthalpy
  contributes at most one power of `k_x` per derivative falling on an `x`-dependent
  factor (`ε` one, `η` two, `E` one, `Δn` and `μ̃` none), so the mechanical form
  reaches `k_x²` from `σ:ε*` and `k_x⁴` from `τ⋮η*`, and odd powers appear only as
  the antisymmetric differences carrying the explicit `i`. With `ℓ=0`,
  `A₄=A₃=0` and the polynomial is quadratic — the classical piezoelectric–
  semiconductor plate, which is the reduction used as a check in
  `sec:results_mechanism`.

## 5. Legendre elements derived (Part C, item 5; Part D)

**Where:** Appendix A.1, `eq:app_basis`, `eq:app_S`, `eq:app_S_weighted`,
`eq:app_S_scaled`, `eq:app_S_matrix`, `eq:app_pot`, `eq:app_charge`,
`eq:app_diel`; body version in `sec:numerics_basis` (`eq:nw`, `eq:block_norms`).

What is *derived*:

* mass matrix = identity, from the normalisation `b_j = √(2j+1)P_j`;
* the weighted orthogonality `∫(1−ζ²)P_j'P_k' = 2j(j+1)/(2j+1) δ_jk` is derived
  from the Legendre equation by multiplying by `P_k` and integrating by parts,
  with the boundary term vanishing because of the `(1−ζ²)` factor — this is the
  step usually skipped;
* the unweighted companion `∫(P_j')² = j(j+1)` is quoted as classical and then
  **checked numerically** by the assembled matrix, rather than taken on trust;
* the scaled stiffness `S_jj = 2j(j+1)(2j+1)` from the chain factor 2 and the
  half-interval measure, giving `12, 60, 168, 360, 660` for `j=1..5` and the full
  `n=6` matrix `eq:app_S_matrix` (values 12, 18.330, 22.978, 60, 80.498, 168,
  210.60, 360, 660) — every entry of which was reproduced by an independent
  quadrature this round;
* the grounded potential space `ψ_j = b_j − r_j b_{j+2}` with
  `r_j = √((2j+1)/(2j+5))`, and the resulting charge matrix
  `∫ψ_i b_j = δ_ij − r_j δ_{i,j+2}` and dielectric matrix `eq:app_diel`.

The **five worked matrix elements** of Appendix A.2 are: mass/compressibility
entry (−1), transport entry (−i·1.80×10⁻³ at `j=0`, and −i(1.304, 6.512, 18.23)
for `j=1,2,3`), carrier–potential entry (−0.074635 diagonal, −0.033378 first
subdiagonal from `Qr₀ = 0.074635×0.4472`), gradient-stiffness entry
(`0.0625×5.14×12 = 3.86`), and the inertia entry (−58.27), with the ratio
`58.27/3.86 = 15.1` interpreted as the frequency at which the first thickness
mode of the gradient operator appears.

## 6. Boundary conditions → edge system (Part C, item 6; Part D)

**Where:** Appendix A.4, `eq:app_edge`; `sec:numerics_edge`, `eq:classification`,
`eq:edge_ansatz`, `eq:RB`.

The four edge conditions (traction, double traction, blocking, charge) are
written as four row blocks `R_Σ`, `R_τ`, `R_J`, `R_D` acting on the total field,
giving `B a = −b_inc` with `B_ij = (R y⁽ʲ⁾)_i`; the solved system is the
column- and row-scaled form solved by SVD, with the rank requirement at `10⁻¹²`
of the largest singular value. The condition number at the operating point
(1.6×10²) and the scaled residual (<10⁻¹²) are quoted; both are stored per row.

## 7. Backward modal power and its normalisation (Part C, item 6)

**Where:** Appendix A.5, `eq:app_power`, `eq:app_power_numbers`.

`P_j = |a_j|² 𝒫_x(y⁽ʲ⁾)` is derived from the bilinearity of the flux, and the
degree-invariance is then *demonstrated on stored data*: the raw modal power
changes by 57 % between degree 18 and degree 30 (−0.0178923 → −0.0113777) while
`|a|²𝒫_x` stays at −0.0231481 in all four degrees. That is the test that the
normalisation is right, and it is why `tab:refinement` shows a degree spread of
7.2×10⁻⁷.

## 8. What is *not* claimed

* Nothing here changes a physical input; every number quoted in the derivations
  is either a material constant already in the paper or a value recomputed this
  round from the model (`c_s = 2746.6 m/s`, `T = 301.72 K`, `a = 2.0828×10⁻³⁹
  J m³`, `L_D = 2.6797 µm`, `Q = 0.074635`, `α_d = 0.8283`, `λ = 0.25`,
  `f_group = 2.563×10⁻³`, `H_ref = 1.8927×10⁻²¹ J m`, `H_bound = 8.966×10⁻²²
  J m`, `H* = 4.0097×10⁻²² J m`).
* The `∫(P_j')² = j(j+1)` identity is *not* derived in the paper; it is quoted as
  classical and checked numerically. The derivation of its weighted form is
  given in full.
* `A_ijklmn = ℓ²c_ijlmδ_kn` is given as the model's assumption, not as a result;
  it is the assumption that makes `ℓ` a single length.
* The corner line force is not analysed anywhere in these derivations, and no
  derivation is offered that would bound it.
