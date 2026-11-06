# PAPER A — Blueprint V2.1: A0-controlled, provisional model finalization

**Date:** 2026-11-05 UTC  
**Fixed title/objective:** **Negative Reflection of Guided Waves in a Flexoelectric Piezoelectric-Semiconductor Plate with Carrier–Strain-Gradient Coupling.**

> **Decision: REVISE — H is symmetry-allowed and admits a consistent reciprocal/stable formulation, but its novelty, higher-order ZnO calibration, and robust full-model backward-wave feasibility remain unverified.**

**STOP at A0.** This is a blueprint and an evidence-based feasibility audit, not a manuscript, permission to begin edge scattering, or a change to the accepted production solver. No Papers B/C are investigated.

## A0 deliverables and status

| Requested report | Actual status |
|---|---|
| [PAPER_A_A0_MATERIALS.md](PAPER_A_A0_MATERIALS.md) | Complete transcription of Zhang Table 1; Fang numerical cross-check and f/A/H closure **open** |
| [PAPER_A_A0_PRIOR_ART.md](PAPER_A_A0_PRIOR_ART.md) | Zhang equations inspected; the three other primary constitutive/chemical-potential comparisons **blocked by unavailable full texts** |
| [PAPER_A_A0_CONSTITUTIVE_CHECK.md](PAPER_A_A0_CONSTITUTIVE_CHECK.md) | Explicit potential, derivatives, exact 6mm reduction, units, stability, elimination exceptions, corrected limits/BCs and energy accounting verified for the stated model |
| [PAPER_A_A0_DISPERSION_FEASIBILITY.md](PAPER_A_A0_DISPERSION_FEASIBILITY.md) | Independent classical-reference and labeled synthetic tests completed; **no finalized nonzero-f baseline or negative reflection demonstrated** |
| This V2.1 blueprint | Direction preserved; later work is conditional on finite evidence/geometry gates below |

**Verification record:** [a0/results/validation.json](a0/results/validation.json), [reproduction instructions](README.md). Passing the executed checks is **not** an overall A0 PASS.

## 1. Change control — necessary corrections explained before the formulation

No earlier blueprint, previous research paper, or production solver was supplied in the checkout; initially it contained only a README. “V2.1” is the requested filename/version label, **not a claim that an unseen V2.0 was reviewed or approved**. The fixed subject, n-type 6mm ZnO, reflecting-edge target, base mechanisms and **one** additional H coupling are retained.

Only these scientifically necessary clarifications/corrections are made:

1. **Reciprocity and signs:** derive both `τ^(H) = Hν` and `μ̃^(H) = H:g`, with the corresponding drift–diffusion force. Distinguish particle flux from conventional electron current and local stress from effective force stress.
2. **Correct carrier-free limit:** take ν = n0 r with bounded small r at fixed physical H as n0 → 0. Zero conductivity at finite n0 is a frozen-carrier limit, not carrier removal.
3. **Boundary order:** use two generalized tractions and two double tractions per flat face for plane-strain gradient mechanics, one electrical condition and one carrier-flux condition. Do not carry higher-order conditions into a classical second-order limit.
4. **Lossless means a defined limit:** finite passive drift–diffusion is dissipative. Initially uncharged frozen carriers give a conservative reference but no H response; instantaneous equilibration is another ideal limit. Retain complex roots at finite mobility.
5. **Power accounting:** include vacuum-field power and the free-face hyperstress correction when comparing group and energy velocity. These follow from the same bulk energy, not a new surface theory.
6. **Geometry issue requiring approval before later scattering:** strict global sagittal plane strain permits normal-incidence backward-mode conversion, but cannot resolve a nonzero negative reflection angle. Oblique edge matching would require an edge-parallel wavenumber and, generally, all necessary elastic polarizations. This is a geometric clarification, **not silently implemented here**. The negative-reflection objective is not replaced by ordinary reflection or by normal conversion alone.
7. **Evidence control:** nonzero f/A/H values and the three unavailable chemical-potential equations are not guessed. The implemented classical/synthetic diagnostics are explicitly labeled as such.

No additional physical coupling, new material pairing, thermal/magnetic field, carrier inertia, dynamic flexoelectricity, nonlocal model, optimization program, or unrelated theory is introduced. These corrections do not independently authorize a project redesign.

## 2. Proposed contribution and finite base-literature check

The proposed contribution is a **modest constitutive-model extension**: retain a direct, symmetry-allowed carrier–strain-gradient energy term and its reciprocal mechanical/transport consequences, then determine whether it changes a genuinely demonstrated negative-reflection regime through backward guided-mode conversion.

It is **not yet established that the coupling itself is unpublished**. The finite primary list is:

1. Fang et al. (2025), *Applied Mathematical Modelling* **141**, 115928, [10.1016/j.apm.2025.115928](https://doi.org/10.1016/j.apm.2025.115928): closest requested SH flexoelectric-semiconductor/size-effects model. Its full equations/table are unavailable here.
2. Wei et al. (2026), *Applied Mathematical Modelling* **150**, Part A, 116353, [10.1016/j.apm.2025.116353](https://doi.org/10.1016/j.apm.2025.116353): requested dynamic-flexoelectric wave comparison; full constitutive equations unavailable. Its additional mechanisms are **not** adopted.
3. Qu et al. (2025), *International Journal of Engineering Science* **208**, 104165, [10.1016/j.ijengsci.2024.104165](https://doi.org/10.1016/j.ijengsci.2024.104165): specifically inspect the energy, carrier chemical potentials, linearized Eq. (4.19), and **Appendix C on chemo-mechanical couplings**. Exact H-related equation numbers are unavailable, not invented.
4. Zhang et al. (2025), *Applied Mathematics and Mechanics* **46**(7), 1331–1346, [10.1007/s10483-025-3272-7](https://doi.org/10.1007/s10483-025-3272-7): **Eqs. (2)–(4), (5), (30)–(31), Appendix A, Table 1** inspected. Its displayed classical constitutive system has no direct H term.

If an existing `μ_n^chem = aν + B:g + ...` integrates to `ν B:g` with the same reciprocal/boundary structure, the proposed H term cannot be described as new. Stop and ask the user to adjudicate the contribution; do not independently replace the paper with an application-only or multi-field project. No unlimited search is proposed.

## 3. Assumptions, material and geometry

- Homogeneous n-type ZnO, 6mm; +x3 is its c/polar axis, x1/x2 basal axes.
- Small strain, small carrier perturbation `|ν|/n0 ≪ 1`, uniform neutral equilibrium, isothermal nondegenerate carrier thermodynamics, positive constant mobility/diffusivity, no applied bias/gain.
- Co-moving/reference excess carrier density relative to neutral donors; no separate carrier inertia or recombination field.
- Full strain-gradient elasticity and quasistatic flexoelectric/piezoelectric coupling; no added electric-field-gradient or micro-inertia energy.
- Plate total thickness d, faces x3 = ±d/2. Plane-strain bulk modes use u2 = ∂2 = 0. A reflecting edge is at x1 = 0 with the interior x1 < 0; distant incidence is defined in a long uniform region. A finite numerical truncation would have to be independently converged.
- Free mechanical faces/edge, no independent surface energy or prescribed corner forces; unelectroded vacuum exterior, no additional surface free charge; blocking carrier boundaries. Actual sample boundary conditions must later be confirmed, not inferred from a bulk table.

**Sourced classical set:** C11 = C22 = 210, C12 = 121, C13 = C23 = 105, C33 = 221, C44 = C55 = 43, C66 = 44.5 GPa; e15 = e24 = −0.48, e31 = e32 = −0.57, e33 = 1.32 C/m²; κ11 = κ22 = 7.61×10^-11, κ33 = 8.85×10^-11 F/m; ρ = 5700 kg/m³; M = 0.01 m²/(V s), Dn = 2.6×10^-4 m²/s. All are from Zhang Table 1, with the detailed convention/conversion audit in the materials report.

**Unresolved:** f_ijkl and A_jklmnp are not numerically finalized. H has no retrieved physical estimate. A0 synthetic `A = ell² C⊗I`, ell/d = 0.05 and strict H fractions are **not material data**. The diagnostic thickness d = 1 μm and n0 = 10^19 m^-3 are stated scenarios. T_effective = 301.717 K is inferred only to make the rounded sourced M/Dn ratio exactly Einstein-consistent.

## 4. Complete symbolic governing formulation

Use `ε_jk = (u_j,k+u_k,j)/2`, `g_jkl = ε_jk,l`, `E = −∇φ`, `a = kBT/n0`, `L = n0 M/q`. The electric enthalpy is

```math
\mathcal H=\tfrac12\varepsilon:C:\varepsilon+\tfrac12 g:A:g
-E\cdot(e:\varepsilon+f:g)-\tfrac12E\cdot\kappa E
+\tfrac12a\nu^2+\nu H:g.
```

Use the augmented potential `∫(𝓗−qνφ)dV`, the vacuum exterior, and the closed-body electron-number constraint where appropriate. The constitutive laws and field equations are

```text
σ_jk = C_jkmn ε_mn − e_ijk E_i,
τ_jkl = A_jklmnp g_mnp − f_ijkl E_i + H_jkl ν,
D_i = e_ijk ε_jk + f_ijkl g_jkl + κ_ij E_j,
μ̃ = aν + H_jkl g_jkl − qφ,
S_jk = σ_jk − ∂l τ_jkl,
ρ u_j,tt = ∂k S_jk,
div D = −qν,
Γ = −L∇μ̃,       J = −qΓ,       ν_,t + div Γ = 0.
```

The 6mm H tensor has exactly three independent coefficients:

```text
H333 = h_a,
H113 = H223 = h_b,
H131 = H311 = H232 = H322 = h_c,
H:g = h_a ε33,3 + h_b(ε11,3+ε22,3) + 2 h_c(ε13,1+ε23,2).
```

H has units **J m** in the ν number-density convention. Require `C ≻ 0`, `κ ≻ 0`, `A ≻ 0` and **`a − H:A^-1:H > 0`**, with consistent shear weights. Test positivity on the stored energy

`𝓤 = ½ε:C:ε + ½g:A:g + ½(D−e:ε−f:g)·κ^-1(D−e:ε−f:g) + ½aν² + νH:g`,

not on the concave-in-E electric enthalpy. The potential and reciprocity are verified in the constitutive report; the baseline's numerical coefficients remain an evidence gate.

**Identifiability limitation:** retaining charge/finite transport generally makes eliminated H feedback screened/nonlocal or frequency-dependent; neutral instantaneous elimination gives exactly `A_eff = A−H⊗H/a`, and initially zero frozen carriers give no H feedback. Do not claim a new independent mechanism in those equivalent/inactive limits.

## 5. Boundary, initial and corner data

On a flat face with normal n and tangent projector P, prescribe either displacement/normal derivative or their corresponding generalized tractions:

```text
R_j = n_k n_l τ_jkl,
T_j = n_k S_jk − div_s(P_ka n_l τ_jkl).
```

For the free surfaces use `T1=T3=R1=R3=0`. In a single sagittal Fourier mode this is `τ_j33=0` and `n3(S_j3−ik τ_j13)=0`, j=1,3. Apply the analogous normal/tangential formulas at the reflecting edge; do not replace T by Cauchy traction.

Electrical data: continuity of φ and normal D to a vacuum Laplace solution, decaying outside, with no imposed surface charge. For an infinite uniform guided mode these reduce to `D3(top)=+ε0|k|φ(top)`, `D3(bottom)=−ε0|k|φ(bottom)`. The finite edge exterior must later be solved consistently rather than reusing only the far-field face formula at a corner.

Carrier data: `Γ·n=0` on every blocking face/edge, conserved initial total excess (normally zero), no extra simultaneous ν = 0 condition. Frozen references specify ν(t=0)=0. Equilibrated closed-body calculations use a constant μ̃ fixed by electron number; at nonzero Fourier k its amplitude is zero.

Corner/line force balance: `r_j = Σ_faces m_k n_l τ_jkl = 0` when no corner force is imposed. Retain it in the later weak or strong edge formulation.

**Full plane-strain finite-rate count:** 4 mechanical + 1 electrical + 1 carrier condition **per face**, 12 over the two uniform faces. Frozen or equilibrated gradient models have 10; the classical frozen piezoelectric model has 6. Counts must be reduced in the corresponding limits, not copied indiscriminately.

## 6. Guided-wave and proposed scattering problems

### 6.1 Bulk mode problem

Insert `(U1,U3,Φ,N)(x3) exp(ikx1−iωt)` into the governing equations and face conditions. Solve the mixed higher-order eigenproblem by a converged through-thickness weak method, and cross-check a suitable limit with an independently assembled strong-equation propagator.

Use mass-overlap continuation, field parity/profiles where meaningful, and **direct total guided power** to distinguish forward/backward, propagating, evanescent and diffusive states. A negative phase velocity or a plotted negative slope alone is insufficient. ZGV points with zero flux are not regular flux-normalized scattering ports.

At finite transport, do not discard loss. For real-frequency excitation determine complex longitudinal roots and select radiating/decaying channels with actual energy accounting; temporal roots at real k are an initial diagnostic only.

### 6.2 Scattering specification — planned, not implemented

At x1 = 0, the later field would be an incident guided mode plus outgoing propagating, evanescent and necessary charge/electrostatic modes satisfying all edge, face, exterior and corner conditions. In x1 < 0:

- incident power has P1 > 0;
- outgoing propagating channels have P1 < 0, independent of the sign of phase k1;
- with `exp(ik1 x1)`, decaying evanescent channels have **Im k1 < 0** as x1 → −∞;
- evanescent near-edge fields cannot be omitted simply because they carry no isolated far-field power.

For genuine **angle-resolved negative reflection**, introduce a common edge-parallel κ only after the geometry clarification is approved. For the transversely isotropic classical/synthetic case, roots satisfy `k1²+κ² = q_mode²`; in a general 6mm gradient material use the full anisotropic dispersion and group/flux vectors instead. SH components may be essential at an oblique edge even if bulk sagittal modes were obtained by plane-strain reductions.

Required demonstration at nonzero incidence:

```text
P1_inc > 0,   P1_ref < 0,
P2_inc × P2_ref < 0,
P_ref · k_ref < 0 for the claimed backward reflected channel,
nonzero, converged reflected-channel power from the solved edge problem.
```

These identify negative **reflection in the same plate**, not refraction into another medium or reflection suppression. At κ = 0 the angular sign test degenerates; normal-incidence backward conversion alone is not silently substituted for that claim.

## 7. Numerical experiments and validation gates

### A0 completed, within stated limits

- Zhang table transcription; exact symbolic derivatives/reciprocity, 6mm tensor nullspace and units.
- Classical frozen reference: first ten branches on 0.02 ≤ K ≤ 12, with a bounded local branch-5 scan on 0.005 ≤ K ≤ 0.08.
- Independent classical propagator, strong PDE/BC residuals, p convergence, mass-MAC continuation, direct power and centered group derivative.
- A reference-only same-frequency forward/backward pair near **3.249035 GHz at d = 1 μm**; checked band only **34.6 kHz** wide. Finite-carrier decay-frequency scale at the backward root is **1.157 MHz**, so no robust semiconductor window is inferred.
- Strictly **synthetic**, f = 0 H sensitivity at K = 2, η = −0.8, −0.5, 0, 0.5, 0.8 with `1−η²≥0.36`; frozen invariance, equilibrated/finite-rate response, passivity and fixed-H carrier-free recovery.

### Conditional future experiments — no execution authorization now

1. After the finite source gate, compute the **actual sourced flexoelectric baseline** H = 0 under the same documented geometry/boundaries. Use only justified tensor reductions and parameter values.
2. Continue any backward candidates under finite transport; check overlap, complex roots, energy direction, loss and robustness to thickness, n0 and physically justified f/A uncertainty. Do not replace a missing candidate with a complex new theory.
3. Compare H = 0 with a few signed, strictly admissible H values. Keep physical constants fixed across thickness/doping sweeps. Distinguish physical estimates, literature-assumed values and synthetic sensitivities in every graph.
4. Only if an accessible same-frequency forward/backward pair survives and geometry is clarified, solve the reflecting-edge problem, converge its outgoing/evanescent basis and edge/exterior resolution, and measure conversion power/angle.
5. Check small perturbation amplitudes, classical/H→0/carrier-free recovery, positive energy, governing residuals and flux/loss balance independently before results are accepted.

### Required energy and residual checks

The local flux follows from the same stored energy:

`𝓟_s = −S_js v_j − τ_jks v_j,k + φ D_s,t + μ̃ Γ_s`,

with dissipation `∇μ̃·L∇μ̃ ≥ 0`. Guided power must also include the vacuum exterior and the face term **`−[〈τ_j13 v_j〉]_bottom^top`**. In conservative calculations compare total `P/E_mean` with dω/dk. In lossy calculations integrate dissipation and account for boundary/exterior work rather than imposing unitary reflection by assumption.

A future scattering balance must close **incident = outgoing propagating power + integrated dissipation + any specified external boundary power**, using a finite control volume and power evaluated at the same reference planes. Reconstruct the full field when cross terms matter. For a conservative, complete isolated-edge problem it reduces to unit flux balance, not before.

Retain separate tolerances for eigenpair, strong momentum, Gauss, carrier continuity, generalized traction, double traction, electrical matching, blocking flux, corner balance, mode truncation and mesh/order convergence. A small determinant or a stable-looking curve is not adequate validation.

## 8. Graph plan and honest result labels

Already supplied:

- [Classical reference dispersion](a0/results/classical_reference.svg), clearly marked f = A = H = 0 and frozen.
- [Narrow reference backward interval](a0/results/classical_backward_window.svg), with signed energy velocity and the finite-carrier warning.
- [Synthetic H sensitivity](a0/results/synthetic_H_sensitivity.svg), not a material prediction.
- CSV/JSON convergence and residual tables, including unresolved lower-order fields despite apparently converged frequencies.

Only after the gates pass, propose:

1. Full-model dispersion with energy/phase direction, loss, ZGV markers and validated mode profiles.
2. H = 0 versus signed H maps of candidate bandwidth and attenuation, separately labeled physical/synthetic.
3. Conversion-power coefficients versus frequency and nonzero incidence angle, with all channels and a flux-balance residual.
4. Tangential-energy sign/angle and a reconstructed displacement or energy-flow field demonstrating reflection on the negative side.
5. Convergence/residual graphs and classical-limit overlays. No successful shape or trend is preassigned.

## 9. Phase-wise execution and stop rules

| Phase | Work / exit evidence | Current state |
|---|---|---|
| **A0 — this delivery** | Sourced classical table, bounded primary audit, reciprocal formulation, limiting/synthetic diagnostics, honest decision | **Stopped here; evidence gaps explicit** |
| A1 — finite model-finalization gate | Obtain F25/W26/Q25 full texts; exact H-law references and Fang cross-check; establish f/A conventions and justified values; user adjudicates any prior-art equivalence and geometry clarification | **Not started** |
| A2 — full guided-wave feasibility | Sourced H=0 baseline, admissible H response, independent residual/convergence/energy checks, robust accessible backward pair | **Not started** |
| A3 — edge conversion / negative reflection | Only after A2 and geometry approval; complete boundary/exterior/corner matching, converged negative reflected power and angle | **Not started** |
| A4 — independently validated results | Error budgets, reproducible data, classical recovery and physically justified claims | **Not started** |
| A5 — manuscript | Only if the model contribution is identifiable and negative reflection is demonstrated wherever claimed | **Not started; no manuscript written** |

A mathematical model is not paper-complete because it is solvable. If H already exists in the selected base, if only a renormalized/inactive limit is studied, if admissible parameters do not support the target, or if negative reflection fails the edge/energy checks, report that outcome and obtain the user's decision. Do not manufacture a successful result or independently add physical fields to rescue it.

## 10. Limitations and finite evidence needed to revisit the decision

- Three primary full texts and Fang's numerical cross-check are missing. **In particular, Qu Appendix C must be read.**
- No sourced nonzero f, calibrated A, or measured H closes the full ZnO model. A strict Schur range is not a physical estimate.
- The verified backward feature belongs to a narrow, electrical-boundary-sensitive **classical limit**; finite-carrier effects exceed its band at the chosen diagnostic n0.
- Strict global plane strain and a nonzero signed reflection angle are not equivalent geometries; the necessary clarification awaits user approval.
- No edge solver, scattering coefficient, negative-reflection demonstration, experimental validation, or previous-paper style match is claimed.
- Claude/Arena's role remains derivation, implementation, review and error identification under the fixed research objective, not independent project selection.

**Fixed sequence preserved:** model extension → governing equations → wave analysis → negative reflection → essential validation → results/manuscript. The A0 stopping point is enforced; later phases above are a plan only.
