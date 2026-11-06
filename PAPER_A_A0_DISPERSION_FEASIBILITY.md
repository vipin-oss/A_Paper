# PAPER A — A0 guided-wave feasibility and validation

**Date:** 2026-11-05 UTC  
**A0 decision:** **REVISE** — a narrow backward-wave feature is verified in a classical reference, not in the finalized flexoelectric semiconductor model. Negative reflection has not been demonstrated.

## 1. What was actually computed

| Calculation | Coefficients / closure | Evidence level |
|---|---|---|
| **Classical lossless reference** | Zhang Table 1 C, e, κ, ρ; `f = A = H = 0`; initially zero frozen carrier perturbation; exact quasistatic vacuum exterior | Computed and independently checked; a legitimate classical limit, **not** the complete prescribed baseline |
| Classical finite-carrier comparison | Same C, e, κ, ρ and sourced mobility/diffusivity; n0 = 10^19 m^-3; full linear drift–diffusion | Computed to assess loss near the reference feature |
| **Synthetic H diagnostic** | `f = 0`, `A = ell² C ⊗ I`, ell/d = 0.05, H333 only with strict Schur fractions η; frozen, instantaneously equilibrated, and finite-mobility closures | Computed sensitivity test; **not physical ZnO f/A/H calibration** |
| Fixed-model flexoelectric baseline | Nonzero sourced f and a sourced/justified A, with carriers | **Not computed/certified:** the necessary numerical higher-order constants were not retrieved |
| Complete edge scattering | Incident/reflected/evanescent modes, edge boundary matching and conversion coefficients | **Not started**, as instructed |

The repository initially contained only a README. No accepted Negative Reflection production solver was present, imported, or modified. All executable work is isolated under `a0/`.

**Sources:** [Zhang full article, Table 1 and Eqs. (2)–(4)](https://www.amm.shu.edu.cn/article/2025/0253-4827/0253-4827-2025-07-1331.shtml). The material and access limitations are documented in `PAPER_A_A0_MATERIALS.md` and `PAPER_A_A0_PRIOR_ART.md`. No flexoelectric value is invented to fill the missing baseline.

## 2. Geometry, boundaries and the meaning of lossless

Let `−d/2 < x3 < d/2`, with **d the total thickness** and +x3 the ZnO polar axis. For the bulk guided-wave calculation use `(u1,u3,φ,ν)(x3) exp(ikx1−iωt)`, `u2 = 0`, `∂2 = 0`. Faces are mechanically free and carrier-blocking. No electrode, bias, recombination, gain, micro-inertia or independent electric-field-gradient energy is introduced.

For A ≠ 0 impose generalized free traction **and** double traction, not only Cauchy traction; see the constitutive report. The exterior potential solves Laplace's equation and decays, giving

```text
D3(+d/2) = +ε0 |k| φ(+d/2),
D3(−d/2) = −ε0 |k| φ(−d/2).
```

The full model uses `n·L∇μ̃ = 0` for carriers. A local `D·n = 0` approximation is a different boundary model and is tested only as a sensitivity control.

Finite drift–diffusion with positive mobility/diffusivity dissipates energy. There are two well-defined conservative comparisons, neither obtained by discarding imaginary roots:

1. **Frozen:** scale mobility and diffusivity to zero together at fixed carrier compressibility a, and set initial ν = 0. Then ν remains zero. **H cannot affect this dispersion.**
2. **Instantaneously equilibrated:** send transport rates to infinity at fixed a, so the nonzero spatial Fourier component has μ̃ = 0. Eliminate ν and φ consistently. This is an ideal screened-equilibrium limit, not a finite-mobility calculation at GHz frequencies.

At finite rates the code solves complex temporal eigenfrequencies at real k. Stable modes have Im ω ≤ 0. Future steady-frequency edge scattering would instead need a real driving frequency and the corresponding complex longitudinal wavenumbers; the two problems must not be conflated.

## 3. Dispersion formulation and reproducible discretization

### 3.1 Normalization

```text
cs = sqrt(c44/ρ) = 2746.608754 m/s,
ξ = x3/d ∈ [−1/2,1/2],       K = kd,
Ω = ωd/cs,                   f_Hz = Ω cs/(2πd),
U = u/d,
Φ = φ / [d sqrt(c44/κ33)],
N = ν / sqrt(c44/a),
Q = qd/sqrt(aκ33) = d/λD,3,
α = Dn/(d cs).
```

At d = 1 μm, n0 = 10^19 m^-3 and the transport-consistent θ = kBT inferred from the source ratio, `Q = 0.834443407`, `α = 0.0946621901`, and `cs/(2πd) = 437.136360 MHz`. Amplitudes U = O(1) are only numerical normalization. Physical excitation must be rescaled so **both** small strain and `max|ν|/n0 ≪ 1` hold; normalized eigenvectors are not literal large-strain experiments.

### 3.2 Weak form (including where a sourced f would enter)

Use orthonormal Legendre functions `ψ_j(ξ) = sqrt(2j+1) P_j(2ξ)` for displacement components, potential and carrier fields. Their derivatives are analytic; Gauss–Legendre quadrature integrates the polynomial bulk forms. Denote the mechanical strain operator B, its gradient G, and potential gradient operator V:

```text
s_PS = (iK U1, U3', U1' + iK U3)ᵀ = B U,
∇s_PS = (iK B U, B' U) = G U,
∇Φ = (iK Φ, Φ') = V Φ.
```

A prime denotes d/dξ. The potential-based weak matrices have the structure

```text
Kuu = ∫(B† C B + G† A G),
Kup = ∫(B† eᵀ V + G† fᵀ V),
F   = ∫G† H Ψn,
P   = ∫V† κ V + Pvacuum,
W   = ∫Ψn† Ψn,
L0  = ∫(∇Ψn)† ∇Ψn.
```

Coefficients in these expressions are consistently nondimensionalized; the executed f = 0 code implements their explicit plane-strain forms. For the synthetic H333 subfamily, `F_U3,N = hbar ∫(ψ'')ᵀψ`, with

`hbar = H333/[d sqrt(a c44)] = η (ell/d) sqrt(C_eff/c44)`.

For matching potential/carrier bases, the coupled equations are

```text
(Kuu − Ω² M) U + Kup Φ + F N = 0,
Kup† U − P Φ − Q W N = 0,
W μ = F† U + W N − Q W Φ,
−iΩ W N + α L0 μ = 0.
```

The last two equations enforce the **same** H coupling in chemical potential and mechanics. Boundary terms give the higher-order natural conditions and blocking μ flux. Vacuum contributes `ε0/κ33 × |K|` times each face-potential outer product to P.

Eliminating Φ gives

```text
Kf = Kuu + Kup P^-1 Kup†,
R  = F − Q Kup P^-1 W,
An = W + Q² W P^-1 W.
```

Frozen carriers solve `Kf U = Ω² M U`. Instantaneous equilibrium solves

`[Kf − R An^-1 R†] U = Ω² M U`.

Finite rates are solved as a first-order system in `(U,V=U_,t,N)`, retaining all relaxation modes rather than taking only a real stiffness. The chemical field μ is a derived mixed variable, not an additional physical mechanism.

### 3.3 Branch classification and independent check

- Broad bounded scan: **first 10 modes**, K = 0.02 to 12, 301 points, polynomial degree 22.
- Adjacent eigenvectors are matched by **mass-weighted modal overlap**, using one-to-one assignment, not independently sorted curve segments. Minimum consecutive MAC in this scan: **0.999620**.
- Conservative group velocity is evaluated by the analytic Hellmann–Feynman/envelope derivative and checked with a centered frequency derivative.
- Backward classification requires **positive frequency and negative total axial power for k > 0**. Power includes exterior electric transport and, for gradient elasticity, the face-hyperstress correction derived in the constitutive report.
- An independent **six-state constant-coefficient thickness propagator** in `(u1,u3,φ,σ13,σ33,D3)` is assembled directly from the classical strong equations. Its matrix-exponential boundary determinant is root-refined separately. It does not reuse the Galerkin derivative matrices or stiffness assembly.

Near K = 0 very small acoustic eigenvalues can be roundoff-sensitive at high p. Such points are not used to infer a new backward branch. The candidate below is a finite, thickness-resonant eigenvalue, independently root-checked and residual-checked. No numerical ZGV root at exactly zero power is treated as a propagating flux-normalized port.

## 4. Actual classical-reference backward feature

The broad scan locates a very short negative-power segment near the cutoff of the **lowest longitudinal-thickness-like branch**, labeled **branch 5 by ascending frequency near K = 0**. This is a numerical family label, not an unverified S/A mode assignment.

A bounded finer calculation on that branch, **K = 0.005 to 0.08**, yields:

| Quantity | Computed classical-reference value |
|---|---:|
| ZGV wavenumber Kzgv | 0.02169259415 |
| Ωzgv | 7.43250434799 |
| Ω at K = 0.005 | 7.43258355041 |
| Checked backward interval | `0.005 ≤ K < 0.02169259415` |
| fzgv at d = 1 μm | 3.249017896 GHz |
| f at K = 0.005, d = 1 μm | 3.249052519 GHz |
| Width of this **bounded** frequency band | **34.6223 kHz** |

The interval starts at the finite checked K = 0.005. It is **not** extrapolated through k = 0, where electrical gauge/charge constraints and ultimately quasistatic validity require separate treatment.

A same-frequency pair on opposite sides of that minimum is independently checked:

| Propagation state | K > 0 | Ω | `v_energy/cs = dΩ/dK` |
|---|---:|---:|---:|
| Backward | 0.00989001558 | 7.43254394920 | −0.00670940467 |
| Forward | 0.03349083877 | 7.43254394920 | +0.00671433406 |

At d = 1 μm the pair frequency is **3.249035207 GHz**; the energy velocities are about **−18.43 m/s** and **+18.44 m/s**. The positive-k backward state truly has energy opposite its axial phase propagation in this reference calculation. These are two propagating roots of the same resonant dispersion family, not proof of a nonzero conversion amplitude at an edge.

The classical frequency-thickness product is approximately `f d = 3.2490 GHz·μm`; inverse-thickness scaling follows **only for this classical scale-free reference**. Once a physical gradient length, carriers or f enter, that scaling is not generally valid. **No validated full fixed-model frequency/thickness operating range is yet identified.**

Extra numerical digits identify reproducible roots, not experimental accuracy. The sourced constants are rounded and have no sample-specific uncertainty budget here; the 34.6 kHz computational feature must not be presented as a physically calibrated GHz operating tolerance.

### 4.1 Why this is not a robust feasibility result

1. **Boundary sensitivity.** Replacing exact vacuum by local `D·n = 0` removes negative group velocity on this same branch in the bounded fine interval. This explicitly tested control is recorded in `validation.json`; it is not a statement about all branches or all k. The vacuum-related near-cutoff feature cannot be presented as a boundary-independent Lamb-wave result.
2. **Finite carriers matter more than the band.** At the backward K, the matched finite-mobility **classical** mode at n0 = 10^19 m^-3 is

   `Ω ≈ 7.43218926981 − 0.00264614666 i`, with MAC **0.99999999967** relative to the frozen shape.

   Its decay-frequency scale `−Im ω/(2π)` is **1.15673 MHz**, about **33.4 times** the 34.6 kHz reference band, and its real-frequency shift is approximately **−155.0 kHz**. This is a calculated temporal decay scale, **not a measured linewidth, a scattering coefficient, or a spatial attenuation length**. It invalidates treating carriers as an innocuous perturbation of this very narrow frozen feature. It does not prove that no backward state exists anywhere in the full damped problem.
3. **f and A are unresolved.** Even small higher-order or boundary corrections can move a feature this narrow. A classical-limit window is not a substitute for the requested sourced flexoelectric baseline.
4. **No scattering amplitude was solved.** Accessible same-frequency roots are necessary kinematics, not sufficient proof of negative reflection.

## 5. H sensitivity — separate synthetic evidence

Set `f = 0`, `A = ell² C ⊗ I`, ell/d = 0.05, d = 1 μm, n0 = 10^19 m^-3, K = 2. Only H333 varies, with `H333 = η Hcrit` and `Hcrit = 4.0097064374 × 10^-22 J m`. This is an **admissible synthetic range**, not a physical estimate of ZnO's H or gradient length.

For the fifth low-order mode at this K, p = 28 gives:

| η | H333 [10^-22 J m] | Frozen Ω | Equilibrated Ω | Finite-mobility Re Ω | Finite-mobility Im Ω |
|---:|---:|---:|---:|---:|---:|
| −0.8 | −3.207765 | 8.831350811 | 8.827955452 | 8.829928985 | −0.000758425 |
| −0.5 | −2.004853 | 8.831350811 | 8.830548202 | 8.830927156 | −0.000164313 |
| 0 | 0 | 8.831350811 | 8.830745296 | 8.831190547 | −0.000193563 |
| +0.5 | +2.004853 | 8.831350811 | 8.826168951 | 8.830168810 | −0.001454247 |
| +0.8 | +3.207765 | 8.831350811 | 8.820126905 | 8.828866919 | −0.002914059 |

Interpretation is deliberately limited:

- Frozen spectra are **identical** for all H: a compulsory limiting check, not a null experimental discovery.
- H changes charge-retaining equilibrium/relaxation feedback and can affect **both frequency and loss**. Changes are not necessarily monotonic in signed H because of interference with the existing electromechanical/charge coupling.
- Relative to η = 0, η = +0.8 changes this equilibrated frequency by about **−0.120%**, but the finite-mobility real part by only about **−0.0263%**. This is a numerical sensitivity, not a predicted device effect.
- This mode at K = 2 has positive energy velocity; this sensitivity table is **not a demonstration that H creates, enlarges or improves a backward-wave interval**. That fixed-model question remains open.
- A fixed physical H must be held fixed in a doping/thickness study. Sweeping a dimensionless stability fraction at every new n0/ell would otherwise change the material being compared.

## 6. Validation actually performed

The machine-readable record is [`a0/results/validation.json`](a0/results/validation.json). It includes numerical thresholds and individual outcomes. **52 numerical acceptance checks pass**, plus exact symbolic assertions; **12 regression tests also pass**. Detailed independent/strong-residual checks target the candidate pair and representative synthetic modes, not a uniform certification of every high-order point in the broad plotted scan. These results apply only to the executed reference/synthetic cases, not to the missing full-model tasks.

### 6.1 Classical same-frequency pair

At the backward root:

| Check | Recorded result |
|---|---:|
| Strong mechanical residual, relative L² | 3.76 × 10^-13 |
| Strong Gauss residual, relative L² | 2.23 × 10^-10 |
| Free traction residual, stress-normalized | 3.79 × 10^-14 |
| Exact-vacuum boundary residual, D-normalized | 1.74 × 10^-14 |
| Independent propagator frequency discrepancy | 7.11 × 10^-14 relative |
| Independent propagator boundary σmin/σmax | 2.54 × 10^-13 |
| Direct energy velocity − analytic group velocity | about 3.5 × 10^-18 in cs units |

The forward-root checks are comparably small. Same-frequency relative mismatch is about `1.95 × 10^-13`. A centered derivative at K = 0.01 differs from analytic dΩ/dK by about `3.53 × 10^-9`, using half-step 0.0005.

Mechanical residuals are normalized by the larger L² norm of inertia and force-divergence terms; Gauss residuals by the largest of its separate derivative/charge terms. Boundary residuals use the corresponding bulk stress or displacement-field norm. Raw definitions are implemented in `Plate.diagnostics`; they are not residuals normalized by an arbitrarily huge whole stiffness norm.

### 6.2 Polynomial convergence — frequency alone can be misleading

At K = 0.01 the classical branch-5 Ω is 7.4325432147 to the shown precision from p = 10 onward, **but** its Gauss residual falls from about `1.58 × 10^-3` at p = 10 to `4.70 × 10^-10` at p = 18. Early frequency agreement alone would have hidden an inadequately resolved field.

For the synthetic equilibrated η = 0.8 mode at K = 2:

| Polynomial degree p | Ω | Strong mechanical residual | Generalized traction residual |
|---:|---:|---:|---:|
| 12 | 8.8201285041 | 4.28 × 10^-2 | 1.88 × 10^-2 |
| 16 | 8.8201269062 | 3.77 × 10^-3 | 1.24 × 10^-3 |
| 20 | 8.8201269044 | 1.24 × 10^-4 | 3.24 × 10^-5 |
| 24 | 8.8201269046 | 1.83 × 10^-6 | 3.96 × 10^-7 |
| 28 | 8.8201269055 | 1.18 × 10^-8 | 2.15 × 10^-9 |

At p = 28 the synthetic double-traction residual is `2.75 × 10^-12` in stress×thickness units; strong Gauss residual is `6.90 × 10^-12`. The face-hyperstress power correction is nonzero and is included. Blindly adding degrees indefinitely is not assumed to improve floating-point conditioning; compare residuals as well as eigenvalues.

### 6.3 Carrier loss, stability and classical recovery

For the synthetic finite-mobility η = 0.8 mode:

- strong momentum and Gauss residuals: `1.85 × 10^-8` and `1.44 × 10^-11`;
- generalized traction, double traction and vacuum-boundary residuals: `3.42 × 10^-9`, `4.51 × 10^-12` and `6.04 × 10^-13`;
- carrier strong residual: `3.21 × 10^-10`;
- blocking-boundary residual: `1.57 × 10^-10`;
- first-order eigenpair residual: `2.33 × 10^-11`;
- energy-decay identity discrepancy: `6.85 × 10^-11` relative;
- all retained state eigenvalues obey the tested passive sign.

Finite-rate convergence is recorded separately in `a0/results/dynamic_convergence.csv`: increasing p = 16, 20, 24, 28 reduces the carrier strong residual approximately as `2.80 × 10^-4`, `4.54 × 10^-6`, `3.75 × 10^-8`, `3.21 × 10^-10`, while the full complex frequency also converges. The associated mechanical residual falls from `5.34 × 10^-3` to `1.85 × 10^-8`. Lower-order runs are not passed merely because their frequencies look stable.

The energy identity uses the positive reduced energy and diffusion dissipation: `2 Re(s) E = −D_diss`, with `s = −iΩ`. The classical finite-carrier comparison satisfies the same identity to about `4.98 × 10^-13` relative; its strong momentum, Gauss, carrier and blocking-boundary residuals are also explicitly checked. See the constitutive report for fixed-physical-H carrier-free recovery and the neutral-renormalization control.

No edge energy partition, conversion coefficient, or scattering convergence test exists yet. None is marked passed.

## 7. Geometry gate: backward conversion is not already negative reflection

In **strict global sagittal plane strain**, ∂2 = 0 and a straight edge normal to x1 has zero conserved in-plane tangential wavenumber. One can study **normal-incidence conversion between forward/backward guided states**, but there is no nonzero tangential ray angle with which to establish the negative side of angular reflection.

If an angle-resolved negative-reflection claim is intended, the minimal later geometry clarification is an edge-parallel coordinate x2 and common κ = k2, with modes evaluated at `(k1,κ)`. This adds no new physical coupling, but it is **not the same global plane-strain field**. An oblique free edge may require SH as well as sagittal polarizations to satisfy its traction conditions. For a general 6mm sixth-order A, in-plane isotropy must not be presumed from classical C alone.

For the transversely isotropic classical reference, a necessary kinematic condition would be `|κ| < min(k_forward,k_backward)`. Genuine negative reflection would then require outgoing energy toward the plate interior and a tangential energy component opposite the incident one. These are **future checks**, not an A0 demonstration. The blueprint records this clarification for the user's approval before any scattering implementation; no geometry or scope change is silently adopted.

## 8. Files, graphs and reproducibility

From a clean Python environment:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r a0/requirements.txt
OPENBLAS_NUM_THREADS=1 .venv/bin/python a0/run_checks.py
.venv/bin/python -m unittest discover -s a0 -p 'test_*.py' -v
```

The reference run used Python 3.11.2 and the package versions pinned in `a0/requirements.txt`. Matrices, source transcription and the independent propagator are in `a0/dispersion.py`; symbolic checks are separate in `a0/constitutive_check.py`.

Small audit outputs are retained because they are part of A0 validation:

- [`classical_reference.svg`](a0/results/classical_reference.svg): first six displayed branches of the classical limiting scan;
- [`classical_backward_window.svg`](a0/results/classical_backward_window.svg): the narrow **reference-only** backward feature;
- [`synthetic_H_sensitivity.svg`](a0/results/synthetic_H_sensitivity.svg): explicitly synthetic equilibrium/finite-rate frequency sensitivity;
- CSV tables for the full bounded reference scan, local feature, sensitivity and convergence;
- `validation.json`: all recorded checks, qualifiers, actual results and unresolved gates.

No complete edge solver, production-solver patch, manuscript, or broader project is produced.

## 9. Feasibility conclusion

A necessary backward-wave kinematic ingredient exists in a **very narrow, boundary-sensitive classical reference**. Its finite-carrier comparison warns against claiming a usable lossless band at the chosen n0. The one-coupling constitutive law can be implemented consistently and has nontrivial charge-retaining feedback, but the available evidence does **not** establish a robust full-model backward-wave window or negative reflection. Complete the finite primary-equation/material checks before promoting this reference into Paper A's operating regime.
