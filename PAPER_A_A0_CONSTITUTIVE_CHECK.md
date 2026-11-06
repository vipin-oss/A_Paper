# PAPER A — A0 constitutive, symmetry and mathematical checks

**Date:** 2026-11-05 UTC  
**Scope:** one additional energy coupling, `ν H_jkl ε_jk,l`, with ν = Δn. No thermal field, carrier inertia, nonlocal elasticity, dynamic flexoelectricity, optimization, or extra coupling is added.  
**A0 decision:** **REVISE**. The algebra below is verified for the stated potential; this does not establish literature novelty or determine ZnO's missing higher-order constants.

## 1. Variables and a complete, explicit potential

Use small strain `ε_jk = (u_j,k + u_k,j)/2`, strain gradient `g_jkl = ε_jk,l`, and quasistatic electric field `E_i = −φ_,i`. Repeated spatial indices run from 1 to 3. Strain indices j,k are symmetric; the gradient index l is **not** interchangeable with them in general.

ν is excess electron **number per reference volume**, relative to the co-moving, neutral donor/lattice background. It is not the absolute Eulerian electron density. This choice makes the usual small-signal charge law `ρ_free = −qν` and carrier conservation consistent with the retrieved classical base, without accidentally adding a spurious `n0 div u_,t` term to one equation but not the donor charge. An absolute Eulerian-density formulation would require transforming both species' continuity and charge laws consistently.

The isothermal electric enthalpy density, before imposing free-charge electrostatics, is

```math
\mathcal H(\varepsilon,g,E,\nu)
=\tfrac12 C_{jkmn}\varepsilon_{jk}\varepsilon_{mn}
 +\tfrac12 A_{jklmnp}g_{jkl}g_{mnp}
 -e_{ijk}E_i\varepsilon_{jk}
 -f_{ijkl}E_i g_{jkl}
 -\tfrac12\kappa_{ij}E_iE_j
 +\tfrac12 a\nu^2
 +\nu H_{jkl}g_{jkl} .
```

Here `a = kBT/n0 > 0` for the ideal nondegenerate carrier linearization; the equilibrium chemical constant is subtracted. A is the baseline gradient coefficient in this **fixed-E electric-enthalpy convention**. f is defined by `−E_i f_ijkl g_jkl`; a coefficient from an independent-polarization formulation cannot be inserted without its Legendre transformation and unit conversion.

Free charge is included by the augmented functional

`Π = ∫[𝓗(ε,g,−∇φ,ν) − qνφ] dV`,

plus the vacuum electric enthalpy outside, mechanical loads, and any explicitly prescribed electrical work. The `−qνφ` term enforces the known electrostatic coupling; it is not a second proposed material coupling. For a closed body impose the conserved total electron excess, normally `∫ν dV = 0`. Under a potential gauge shift the electrochemical constant shifts consistently; this does not change its gradient or physical flux.

Required material symmetries are the usual elastic minor/major symmetries, `A_jklmnp = A_kjlmnp = A_jklnmp = A_mnpjkl`, `e_ijk = e_ikj`, `f_ijkl = f_ikjl`, `H_jkl = H_kjl`, and symmetric positive κ. All tensors are homogeneous in A0.

## 2. Constitutive derivatives — all reciprocal terms must be retained

Differentiation at independent ε, g, E, ν gives

```math
\sigma_{jk}=\frac{\partial\mathcal H}{\partial\varepsilon_{jk}}
=C_{jkmn}\varepsilon_{mn}-e_{ijk}E_i,
```

```math
\tau_{jkl}=\frac{\partial\mathcal H}{\partial g_{jkl}}
=A_{jklmnp}g_{mnp}-f_{ijkl}E_i+H_{jkl}\nu,
```

```math
D_i=-\frac{\partial\mathcal H}{\partial E_i}
=e_{ijk}\varepsilon_{jk}+f_{ijkl}g_{jkl}+\kappa_{ij}E_j,
```

```math
\mu^{\rm chem}=\frac{\partial\mathcal H}{\partial\nu}
=a\nu+H_{jkl}g_{jkl},\qquad
\widetilde\mu=\mu^{\rm chem}-q\phi .
```

Thus:

- H adds **no direct local Cauchy stress** when ε and g are independent constitutive variables.
- It adds `ν H_jkl` to hyperstress and `H:g` to chemical potential.
- It adds **no direct term to D** for this potential. Its electrical influence is mediated through coupled fields/charge.
- It **does** change the effective force stress

  `S_jk = σ_jk − τ_jkl,l`,

  including the term `−H_jkl ν_,l` for constant H. Confusing S with σ would incorrectly report that H has no mechanical effect.

The reciprocal Maxwell relation is

`∂τ_jkl/∂ν = H_jkl = ∂μ^chem/∂g_jkl`.

Electric reciprocity uses the enthalpy sign: `∂τ/∂E = −f`, whereas `∂D/∂g = +f`. The complete potential Hessian is symmetric, not a matrix in which every electric-response block has the same sign.

### 2.1 Thermodynamically consistent drift–diffusion

Let `L_ij = n0 M_ij/q` be positive definite and use electron particle flux Γ, not conventional electrical current, in the dissipation law:

```math
\Gamma_i=-L_{ij}\widetilde\mu_{,j},\qquad
J_i=-q\Gamma_i,
```

```math
\nu_{,t}+\Gamma_{i,i}=0,
\qquad D_{i,i}=-q\nu,
\qquad \rho u_{j,tt}=S_{jk,k}.
```

For constant coefficients this gives

```math
J_i=q n_0M_{ij}E_j+q d_{ij}\nu_{,j}
       +n_0M_{ij}\partial_j(H_{klm}g_{klm}),
\qquad d_{ij}=aL_{ij}=\frac{k_BT}{q}M_{ij}.
```

The H-induced transport force and reciprocal hyperstress are inseparable. Adding H only to stress, or only to the current, would not be the proposed potential-based model. The last term has a plus sign in **conventional electron current** and the opposite sign in particle flux.

The continuity equation equivalently reads `div J = q ν_,t`, matching Zhang Eq. (4). The time convention in this report and code is `exp(i kx − iωt)`; passive temporal modes have `Im ω ≤ 0`.

## 3. Reduction under 6mm symmetry

Let `a_j = δ_j3` denote the polar axis and `P_jk = δ_jk − a_j a_k` the basal projector. A polar third-rank tensor symmetric in its first two indices has exactly **three** independent coefficients under 6mm:

```math
H_{jkl}=h_a a_j a_k a_l+h_b P_{jk}a_l
        +h_c(P_{jl}a_k+P_{kl}a_j).
```

Equivalently, the only nonzero components are

```text
H333 = h_a,
H113 = H223 = h_b,
H131 = H311 = H232 = H322 = h_c.
```

Their contraction is

```math
H:g=h_a\varepsilon_{33,3}
    +h_b(\varepsilon_{11,3}+\varepsilon_{22,3})
    +2h_c(\varepsilon_{13,1}+\varepsilon_{23,2}).
```

The factor 2 is required by the two symmetric shear-index entries. If using engineering shear, the same term is `h_c γ13,1`, not `2 h_c γ13,1`. Imposing full symmetry over all three indices without physical justification would incorrectly identify h_b and h_c.

For sagittal plane strain `(u1,u3)(x1,x3,t)`, `u2 = 0`, `∂2 = 0`, `ε22 = 0`,

```math
H:g=h_a u_{3,33}+(h_b+h_c)u_{1,13}+h_c u_{3,11}.
```

The full 6mm reduction is symbolic, not a numerical fit. The sensitivity calculation deliberately uses the admissible **one-component subfamily** `h_a = H333`, `h_b = h_c = 0`; all three remain available in the formulation. An odd-rank polar tensor would vanish in a centrosymmetric material, but **6mm ZnO is not centrosymmetric**. Symmetry permission alone is not evidence of a nonzero measured coefficient or of novelty.

**Independent verification:** `a0/constitutive_check.py` applies a 60° rotation and a vertical mirror to all 18 first-pair-symmetric components. The exact SymPy invariant nullspace has dimension 3 and equals the tensor family above.

## 4. Dimensional audit

ν is a number concentration; “per electron” is a counting convention, not an extra SI dimension.

| Variable/coefficient | SI units | Check |
|---|---|---|
| ε | 1 | Small strain |
| g = ∇ε | m^-1 | Strain gradient |
| C | Pa = J m^-3 | `C ε²` is energy density |
| A | Pa m² = J m^-1 | `A g²` is energy density |
| e | C m^-2 | `e E ε` is energy density |
| f in this enthalpy | C m^-1 | `f E g` is energy density |
| κ | F m^-1 | Absolute dielectric coefficient |
| ν | m^-3 | Excess electron number per volume |
| a | J m³ | `a ν²` is energy density |
| **H** | **J m** | `ν H g` has units J m^-3 |
| τ | Pa m = N m^-1 | `Hν` has these units |
| μ^chem, μ̃ | J per electron count | `H:g`, `aν`, `qφ` all have units J |
| Γ | m^-2 s^-1 | Particle flux |
| J | A m^-2 | Conventional electrical current |
| L | (J m s)^-1 | `L ∇μ̃` is particle flux |

For the normalized carrier `r = ν/n0`, the coefficient multiplying `r g` in energy is **n0 H**, not H. For a charge-density variable `ρc = −qν`, the coefficient is **−H/q**. Comparing these coefficients without conversion can create both false novelty and catastrophic magnitude errors.

## 5. Quadratic stability — test the energy, not the electric-enthalpy saddle

The electric enthalpy is concave in E; requiring its entire Hessian to be positive would be incorrect. Use the Legendre-transformed stored energy, with `P_e = e:ε + f:g`:

```math
\mathcal U(\varepsilon,g,D,\nu)
=\tfrac12\varepsilon:C:\varepsilon+\tfrac12 g:A:g
 +\tfrac12(D-P_e)\cdot\kappa^{-1}(D-P_e)
 +\tfrac12 a\nu^2+\nu H:g .
```

Electrostatic charge is then enforced by Gauss's law; the multiplier `−qνφ` is not included as a stored-energy positivity term. For this explicitly chosen baseline, local strict convexity follows from

```math
C\succ0,\quad\kappa\succ0,\quad A\succ0,\quad
 a-H:A^{-1}:H>0 .
```

Equivalently `A − H⊗H/a ≻ 0`. Compute the contraction using a consistent independent strain-gradient basis (Kelvin or correctly weighted engineering coordinates). A diagonal norm of raw tensor entries with duplicated shear indices is not this Schur test.

The electric square is nonnegative and can be zero when `D = P_e`; the C, A, carrier block therefore supplies the relevant bound in this convention. If the baseline is instead specified in polarization variables, first transform its coefficients: it need not have the same numerical A. No numerical f calibration is supplied by this check.

For the synthetic law `A_jklmnp = ell² C_jkmn δ_lp` and H333 alone, the full 3D bound is

```math
|H_{333}|<H_{crit}
=\ell\sqrt{a\left(c_{33}-\frac{2c_{13}^2}{c_{11}+c_{12}}\right)}.
```

Define η = H333/Hcrit. The tested `|η| ≤ 0.8` has margin `1−η² ≥ 0.36`; η = 1 is only semidefinite and is excluded. If **A = 0 and H ≠ 0**, the local quadratic potential as written is indefinite: one cannot stabilize it merely by ignoring the missing gradient modulus.

The exact Schur identity and independent dimensionless SPD-block tests pass. A deliberately inadmissible η = 1.01 produces a negative eigenvalue, as it should. SI Hessian eigenvalues with wildly disparate units are not compared directly as if their raw magnitudes were meaningful.

## 6. Elimination of carriers — non-equivalence, and the exceptions

### 6.1 Instantaneous local electrochemical equilibration

For a reservoir with a prescribed electrochemical constant, or a nonzero Fourier mode of a closed equilibrated body,

`μ̃ = μ0`, hence `ν = (qφ − H:g + μ0)/a`.

Eliminating ν from `𝓗 − qνφ − μ0ν` contributes

```math
-\frac{1}{2a}(q\phi-H:g+\mu_0)^2.
```

For μ0 = 0 this includes **all** of

```text
−(H:g)²/(2a),        +(q/a) φ(H:g),        −q² φ²/(2a).
```

Only the first is an ordinary gradient-modulus renormalization. The other terms retain charge screening and direct potential/gradient mixing. Eliminating φ next involves a Poisson/Debye operator, exterior conditions and charge constraints, and is generally spatially nonlocal. The closed-body μ0 is determined by conserved electron number; it is not an arbitrary zero mode that may be dropped.

### 6.2 Finite drift–diffusion

For scalar constant L and a bulk Fourier vector Q,

```math
(La|Q|^2-i\omega)\nu
=L|Q|^2(q\phi-H:g).
```

The mechanical feedback `Hν` contains a relaxation factor

`L |Q|² / (La |Q|² − iω)`.

It is generally complex and depends on frequency and wavevector. A constant redefinition of C, A, e or f in the original local model cannot reproduce this dependence for all frequencies, wavenumbers and boundary conditions. Changing potential variables to absorb `H:g/q` instead introduces higher spatial derivatives into the electric terms; it does not preserve the same baseline problem.

### 6.3 Explicit exceptions that limit the proposed contribution

- In a **neutral, local, instantaneous** relaxation model with q suppressed and no charge constraint, elimination gives exactly `A_eff = A − H⊗H/a`. In that restricted model H is not independently identifiable from a gradient modulus.
- With **initially zero frozen carriers**, ν remains zero and H has **no effect at all** on linear dispersion. A plot showing an H effect in that same frozen model would be an implementation error.
- If an existing baseline already includes the same carrier–strain-gradient chemical-potential law, adding its reciprocal term is not a new coupling, regardless of the general nonlocal elimination argument.

The A0 numerical operator test finds a relative difference `6.528 × 10^-3` between charge-retaining H feedback and the simple local renormalization, for the stated synthetic matrices. When q is algebraically suppressed, the difference falls to `2.30 × 10^-17`. The neutral test is a mathematical diagnostic, **not another proposed ZnO model**.

**Finding:** generic mathematical non-equivalence is verified for the charge-retaining/dynamic formulation, with the above explicit exceptions. This is **not a literature-novelty certificate**; Qu Appendix C remains unread.

## 7. Correct carrier-free and classical limits

### 7.1 Carrier-free means removing the mobile excess, not just conductivity

Write `ν = n0 r` with `|r| ≪ 1` bounded, and take n0 → 0 at fixed physical C, A, e, f, H and T. Then

```text
½ aν² = ½ n0 kBT r² -> 0,
ν H:g = n0 r H:g -> 0,
−qν -> 0,
Hν -> 0.
```

The drift–diffusion currents also vanish when r and the fields remain regular. The result is a **carrier-free piezo-flexoelectric gradient plate**, not automatically a purely elastic plate. It retains e, f and A. Leaving ν finite while n0 → 0 violates the small-perturbation assumption and makes the ideal-gas quadratic coefficient singular.

Setting mobility to zero at fixed n0 is instead a **frozen-carrier** limit. With Einstein consistency, scale both M and diffusivity down together while holding a fixed. It is not carrier-free, and nonzero initial trapped charge would remain. Setting one transport coefficient to zero independently while holding the other fixed changes the thermodynamics.

The executed fixed-H carrier-free test decreases n0 from 10^19 to 10^17 to 10^15 m^-3, with physical H333 unchanged. The relative frequency gaps to the frozen piezo-gradient reference fall from `5.868 × 10^-4` to `5.706 × 10^-6` to `5.704 × 10^-8`. These are **synthetic limit checks**, not a doping calibration.

### 7.2 Further classical recovery

- H → 0: recover the chosen flexoelectric piezoelectric-semiconductor baseline, including its original drift–diffusion loss.
- Carrier-free and f → 0: recover piezoelectric **gradient** elasticity if A remains nonzero.
- Then A → 0: recover the classical piezoelectric plate and reduce the mechanical boundary-condition count.
- e → 0 as well: recover a classical elastic plate (with electrostatic/carrier fields zero in an unforced neutral case).

The A → 0 limit can be singular through thin boundary layers. Do not retain double-traction conditions in a now second-order displacement theory.

## 8. Higher-order boundary conditions and corner forces

These formulas are for the **flat faces/edge of the specified plate**, with no independent surface energy. Set `S_jk = σ_jk − τ_jkl,l`. For outward normal n and tangent projector P, the virtual work on a smooth face is

```math
T_j\,\delta u_j+R_j\,\delta u_{j,n},\qquad
R_j=n_k n_l\tau_{jkl},\qquad
T_j=n_k S_{jk}-\operatorname{div}_s(P_{ka}n_l\tau_{jkl}).
```

The surface divergence here differentiates along the face's tangential coordinate. On `x3 = ±d/2`, with Fourier `∂1 = ik`, the zero mechanical data become

```text
R_j = τ_j33 = 0,
T_j = n3 [ S_j3 − i k τ_j13 ] = 0,    j = 1,3.
```

Therefore setting only `σ_j3 = 0`, or imposing all components `n_l τ_jkl = 0`, is generally wrong. The latter would overconstrain the plate.

For an unelectroded face in vacuum require `φ_inside = φ_vacuum` and normal D continuity, with no added free surface charge. The exterior solves Laplace's equation and decays away. For a single Fourier mode k > 0 this reduces to

```text
D3(top)    = +ε0 |k| φ(top),
D3(bottom) = −ε0 |k| φ(bottom).
```

The external potential amplitudes have already been eliminated here: these are one electrical condition **per face**, not two extra interior conditions. A local `D·n = 0` approximation is a different electrical model, not exact vacuum continuity.

For blocking carrier boundaries use **one** condition per face, `Γ·n = 0`, equivalently `n_i L_ij μ̃_,j = 0`. Do not additionally impose ν = 0. There is no added `|∇ν|²` energy in the one-coupling model and no second independent carrier boundary datum.

| Interior formulation, plane strain | Mechanical conditions per face | Electric per face | Carrier per face | Total across two faces |
|---|---:|---:|---:|---:|
| Full A ≠ 0, finite drift–diffusion | 4 (two T, two R) | 1 | 1 | **12** |
| A ≠ 0, frozen ν = 0 | 4 | 1 | 0 | **10** |
| A ≠ 0, instantaneous carrier equilibration | 4 | 1 | Algebraic μ̃ constraint replaces transport | **10** |
| Classical A = f = H = 0, finite carriers | 2 | 1 | 1 | **8** |
| Classical, initially uncharged frozen carriers | 2 | 1 | 0 | **6** |

H changes coefficients and boundary terms, not the count of unknown fields. An electric-field-gradient theory would have a different electrical count; it is **not silently imported** from Fang into this fixed base.

At intersections of faces there is also a natural corner/line force

`r_j = Σ_adjacent_faces m_k n_l τ_jkl`,

where m is the outward in-face conormal. Balance it against prescribed corner forces (zero if none). It follows from the surface integration by parts; it is not another arbitrary boundary condition on every point of a smooth face. A future free-edge formulation must retain this term or satisfy it weakly.

## 9. Energy accounting and a necessary guided-power correction

Let v = u_,t. With the stored energy 𝓤 above and kinetic energy, the local balance is

```math
\partial_t(\tfrac12\rho |v|^2+\mathcal U)+\partial_s\mathcal P_s
=-\widetilde\mu_{,i}L_{ij}\widetilde\mu_{,j}\le0,
```

```math
\mathcal P_s=-S_{js}v_j-\tau_{jks}v_{j,k}
                 +\phi D_{s,t}+\widetilde\mu\Gamma_s.
```

Products in time-harmonic mean power are `½ Re(a b*)`. Carrier loss must be counted; finite passive drift–diffusion cannot simply be relabeled “lossless” by discarding Im ω.

For a free **gradient-elastic** plate, the local normal bulk power on the upper/lower face is a tangential divergence, even when T = R = 0. Consequently the guided axial power is

```math
P_1^{guided}=\int_{-d/2}^{d/2}\langle\mathcal P_1\rangle\,dx_3
 +P_1^{vacuum}
 -\left[\langle\tau_{j13}v_j\rangle\right]_{-d/2}^{+d/2}.
```

The last, **face-hyperstress correction** is essential. It is derived from the existing bulk potential and free-face conditions, not a new surface field or extra physical mechanism. In the executed synthetic check, omitting it disagrees with group velocity; including it restores agreement to approximately machine precision. In the classical reference τ = 0, so it vanishes. The exterior electric contribution is also retained, rather than treating vacuum only as a frequency correction.

For a conservative positive-energy mode, compare this direct power with `v_energy = P_guided / E_mean` and independently with `dω/dk`. For lossy modes compute actual flux and the dissipation integral; the derivative of Re ω alone is not a universal energy-velocity classifier.

## 10. Executed validation and remaining limits

Run `OPENBLAS_NUM_THREADS=1 python a0/run_checks.py` after installing `a0/requirements.txt`. See `a0/results/validation.json` for values, thresholds and failures, not just a prose assertion.

Executed:

- exact symbolic constitutive derivatives, Hessian reciprocity and carrier elimination;
- exact 6mm invariant-tensor reduction and unit exponents;
- positive classical ZnO stiffness and strict synthetic H Schur margins, including an intentionally inadmissible control;
- independent six-state thickness-propagator roots versus Legendre–Galerkin classical roots;
- strong governing-equation and natural-boundary residuals, polynomial-order convergence, mass-overlap branch continuation;
- direct guided power including vacuum and face hyperstress versus analytic/finite-difference group velocity;
- finite-carrier passivity, blocking-boundary residuals, and energy-decay/diffusive-dissipation identity;
- carrier-free recovery at **fixed physical H**, and the neutral renormalization exception.

The **52 numerical acceptance checks pass for the explicitly executed limiting/synthetic cases**; the symbolic assertions also pass. Lower-order runs are retained in the convergence table and are not all accepted: for example, a synthetic p = 12 mode has a mechanical residual about 0.043 despite an apparently converged frequency. Frequency agreement alone is insufficient.

Not executed/certified: a sourced nonzero-f ZnO baseline, a calibrated A/H model, three inaccessible primary constitutive-law comparisons, or an edge-scattering/negative-reflection calculation. Those unresolved items prevent an overall A0 PASS.
