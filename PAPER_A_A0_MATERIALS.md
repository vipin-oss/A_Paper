# PAPER A — A0 material-parameter audit

**Date:** 2026-11-05 UTC  
**Fixed subject:** Negative Reflection of Guided Waves in a Flexoelectric Piezoelectric-Semiconductor Plate with Carrier–Strain-Gradient Coupling.  
**A0 decision:** **REVISE** — the coupling is mathematically admissible under a strict stability bound, but novelty, higher-order material closure, and full-model negative-reflection feasibility are not established.

## 1. Evidence status — do not mistake this for a completed material calibration

The complete **classical ZnO parameter table** was retrieved from Zhang et al., *Applied Mathematics and Mechanics* **46**(7), 1331–1346 (2025), DOI [10.1007/s10483-025-3272-7](https://doi.org/10.1007/s10483-025-3272-7). The journal's [full HTML article, Table 1](https://www.amm.shu.edu.cn/article/2025/0253-4827/0253-4827-2025-07-1331.shtml#T1) is accessible even though the Springer landing page presents subscription access. Table 1 attributes its data to Zhang's reference **[11]**, J. S. Yang, *Analysis of Piezoelectric Semiconductor Structures*, Springer Nature (2020). The book's underlying measurements were **not** independently audited here.

Fang et al.'s [publisher preview](https://www.sciencedirect.com/science/article/abs/pii/S0307904X25000034) identifies an n-type ZnO film/diamond substrate example, but does **not** expose its full material table. Its article and PDF routes returned the preview rather than the equations/table. A narrowly targeted search of the connected Drive for the four identifiers/titles found no matching source files. **No numerical agreement with Fang is claimed.** See `PAPER_A_A0_PRIOR_ART.md` for the bounded access audit.

Zhang's article is a **classical piezoelectric-semiconductor** model, not a source of a complete ZnO flexoelectric or strain-gradient tensor. Missing higher-order constants must remain missing; the classical reference calculations do not finalize the prescribed flexoelectric model.

## 2. Retrieved ZnO values

All entries in this table are transcribed from **Zhang Table 1**, with only the displayed unit conversions. Use the material axes with **+x3 along the reported polar/c-axis**, x1 and x2 in the basal plane. Reversing the polar axis requires consistent tensor transformation; do not change individual piezoelectric signs by hand.

| Quantity | Value as reported | SI value used | Provenance / convention |
|---|---:|---:|---|
| c11 = c22 | 2.10 × 10^11 N m^-2 | 210 GPa | Zhang Table 1 |
| c12 | 1.21 × 10^11 N m^-2 | 121 GPa | Zhang Table 1 |
| c13 = c23 | 1.05 × 10^11 N m^-2 | 105 GPa | Zhang Table 1 |
| c33 | 2.21 × 10^11 N m^-2 | 221 GPa | Zhang Table 1 |
| c44 = c55 | 4.30 × 10^10 N m^-2 | 43.0 GPa | Zhang Table 1 |
| c66 | 4.45 × 10^10 N m^-2 | 44.5 GPa | Zhang Table 1; exactly (c11−c12)/2 at tabulated precision |
| e15 = e24 | −0.48 C m^-2 | −0.48 C m^-2 | Stress-charge form, engineering shear convention |
| e31 = e32 | −0.57 C m^-2 | −0.57 C m^-2 | Same source/convention |
| e33 | 1.32 C m^-2 | 1.32 C m^-2 | Same source/convention |
| κ11 = κ22 | 7.61 × 10^-11 C V^-1 m^-1 | 7.61 × 10^-11 F m^-1 | **Absolute**, not relative, permittivity |
| κ33 | 8.85 × 10^-11 C V^-1 m^-1 | 8.85 × 10^-11 F m^-1 | Absolute permittivity |
| Electron mobility M11 = M22 = M33 | 100 cm² V^-1 s^-1 | 0.0100 m² V^-1 s^-1 | 1 cm² = 10^-4 m² |
| Electron diffusivity d11 = d22 = d33 | 2.6 cm² s^-1 | 2.60 × 10^-4 m² s^-1 | Same area conversion |
| Mass density ρ | 5700 kg m^-3 | 5700 kg m^-3 | Do not silently substitute another common ZnO density |

The same constitutive sign convention is visible in Zhang **Eqs. (2)–(3)**: electric displacement is `D = e ε + κ E`, stress is `σ = C ε − eᵀ E`, and conventional electron current is `J = q n0 M E + q d ∇ν`, with `ν = Δn`. The additional H force is **not** part of that retrieved current law.

### 2.1 Matrices used in the diagnostics

With engineering strain `s = (ε11, ε22, ε33, 2ε23, 2ε13, 2ε12)ᵀ`,

```text
C = [c11 c12 c13  0   0   0 ]       e = [0   0   0   0  e15  0]
    [c12 c11 c13  0   0   0 ]           [0   0   0  e15  0   0]
    [c13 c13 c33  0   0   0 ]           [e31 e31 e33 0   0   0]
    [ 0   0   0  c44  0   0 ]
    [ 0   0   0   0  c44  0 ]       κ = diag(κ11, κ11, κ33).
    [ 0   0   0   0   0  c66]
```

For sagittal plane strain, retain `s_PS = (ε11, ε33, 2ε13)ᵀ` and use the corresponding **submatrix**, not the plane-stress Schur reduction. In particular, ε22 = 0 while σ22 need not vanish.

## 3. Universal constants and carrier thermodynamics

These are separate from ZnO fitted properties:

| Constant | Value used | Source |
|---|---:|---|
| Positive elementary charge q | 1.602176634 × 10^-19 C, exact | [NIST/SI](https://physics.nist.gov/cgi-bin/cuu/Value?e) |
| Boltzmann constant kB | 1.380649 × 10^-23 J K^-1, exact | [NIST/SI](https://physics.nist.gov/cgi-bin/cuu/Value?k) |
| Vacuum permittivity ε0 | 8.8541878188 × 10^-12 F m^-1 | [NIST, 2022 CODATA central value](https://physics.nist.gov/cgi-bin/cuu/Value?ep0); uncertainty 1.4 × 10^-21 F m^-1 |

Zhang's text after Eq. (3) rounds q to `1.6 × 10^-19 C`. The diagnostics deliberately use the exact SI value; this is documented, not a different material calibration.

For an isothermal, nondegenerate, ideal electron gas, the quadratic perturbation energy follows by expanding

`kBT [(n0+ν) ln((n0+ν)/n0) − ν] = (kBT/2n0) ν² + O(ν³/n0²)`.

Define `a = kBT/n0 > 0` and `Lij = n0 Mij/q`. Thermodynamic drift–diffusion requires `dij = (kBT/q) Mij`. The **rounded tabulated ratio** gives

```text
d/M = 0.026000 V,
θ := kBT = q d/M = 4.1656592484 × 10^-21 J,
T_effective = 301.7174712 K.
```

This effective temperature makes both reported transport constants exactly consistent in the calculation. It is **not** a claim that Zhang measured the sample at 301.717 K. If instead fixing T = 300 K, recompute d = M kBT/q and explicitly report the approximately 0.57% change. Do not mix the two conventions in a dissipation check.

Nondegeneracy, carrier linearization, constant mobility, and full donor ionization remain assumptions, not experimental validations. A sample-specific study must check them against doping, temperature, and band statistics. No unsourced effective mass, band gap, relaxation time, or recombination coefficient is introduced.

## 4. What remains unavailable

| Required quantity | Present status | Consequence |
|---|---|---|
| Full Fang ZnO table and its conventions | Full text/table not retrieved | Cross-check **open**; no agreement inferred from the abstract or similar papers |
| Flexoelectric tensor f_ijkl, in the `−E_i f_ijkl ε_jk,l` convention | No verified numerical value obtained from the requested sources | No nonzero f is assigned; a polarization-based coefficient in volts cannot simply be copied as C/m |
| Strain-gradient elastic tensor A_jklmnp, or a justified reduced length law | Not in Zhang Table 1; no verified Fang values available | Fixed-model size effects are not material-calibrated |
| H_jkl, units J m per electron-number convention | No measured or independently derived value supplied/retrieved | Only a mathematical sensitivity range is allowed, not a physical estimate |
| n0 and actual plate thickness d | Sample/device choices, not intrinsic constants | State each scenario; do not present it as a material property |
| Actual surface electrical/contact/carrier conditions | Not specified by a sample description | Vacuum + blocking faces below are an explicit diagnostic choice, not a measured boundary law |

**Task 1 is therefore partially completed, not certified complete.** Obtaining Fang's table and the other two primary full texts is the finite next evidence request; a broader novelty hunt is unnecessary.

## 5. Explicitly labeled reference and synthetic scenarios

### 5.1 Sourced-constant classical reference — not the finalized base

Use total thickness `d = 1 μm`, c-axis normal, mechanically free faces, a quasistatic **vacuum exterior**, and initially zero **frozen** carrier perturbation. Set `f = A = H = 0` only as an exact classical-limit diagnostic. This is a model limit, **not** an assertion that ZnO has zero flexoelectricity or no strain-gradient stiffness.

`n0 = 10^19 m^-3` is a modeling scenario also used by Zhang in **Figs. 2 and 7**, not a reported measurement of the proposed plate. This n0 matters in finite-carrier comparisons, but not in a frozen, initially uncharged classical dispersion.

### 5.2 Synthetic gradient/H sensitivity — not a ZnO estimate

For a separate, clearly artificial test of the coupling, use

```text
A_jklmnp = ell² C_jkmn δ_lp,
ell/d = 0.05,
f = 0 (still only a limiting diagnostic),
H333 = h; all other independent H components = 0.
```

There is still **one additional coupling**, ν H:g. Choosing the H333 subfamily does not introduce another mechanism. The gradient-length law and ell are **not sourced ZnO constants**. Their purpose is to supply a positive higher-order stiffness for a stability-constrained sensitivity test, not to finalize the material.

Use the full **3D**, not merely plane-strain, Schur bound:

```text
C_eff = 1/(C^-1)33 = c33 − 2 c13²/(c11+c12)
      = 1.5438368580 × 10^11 Pa,
Hcrit = ell sqrt(a C_eff),
h = eta Hcrit,      |eta| < 1.
```

At d = 1 μm, ell = 50 nm, n0 = 10^19 m^-3 and the consistent θ above,

```text
a = 4.1656592484 × 10^-40 J m³,
Hcrit = 4.0097064374 × 10^-22 J m,
eta tested = −0.8, −0.5, 0, +0.5, +0.8.
```

The resulting largest tested `|H333| = 3.2077651499 × 10^-22 J m` is **only a mathematical admissibility example**. A Schur bound is not an experimental estimate and does not establish physical realizability. Stability is checked in `PAPER_A_A0_CONSTITUTIVE_CHECK.md`.

When varying n0 for a carrier-free limit, hold physical H fixed: for this parametrization `eta(n0) = eta_ref sqrt(n0/n0_ref)`. Holding eta fixed would change the physical coupling and would not test one fixed material law.

## 6. Derived scales and elementary checks

At d = 1 μm and n0 = 10^19 m^-3:

| Derived quantity | Value | Meaning |
|---|---:|---|
| cs = sqrt(c44/ρ) | 2746.608754 m/s | Frequency/wavenumber normalization only |
| cs/(2πd) | 4.371363600 × 10^8 Hz | Ω-to-frequency scale |
| λD,3 = sqrt(κ33 θ/(q² n0)) | 1.198403621 μm | Debye length in x3 |
| τdielectric,3 = κ33/(q n0 M) | 5.523735531 ns | Dielectric relaxation time |
| τdiffusion = d²/Dn | 3.846153846 ns | Dn is electron diffusivity; d is total plate thickness |
| d/λD,3 | 0.834443407 | Dimensionless charge parameter |

The code calls diffusivity `electron_diffusivity` and thickness `d`; these must never be confused despite the source's use of d_ij for diffusion coefficients.

All principal dielectric entries, mobility, diffusivity, and density are positive. The engineering-Voigt elastic eigenvalues in GPa are approximately `43, 43, 44.5, 89, 117.6491, 434.3509`; the actual Kelvin eigenvalues differ by shear normalization, but positivity is unchanged. The hexagonal identity for c66 is recovered exactly at table precision.

These checks establish admissibility of the **retrieved classical parameter set**, not calibration of f, A, or H.

## 7. Reproducibility and source boundary

- Machine-readable transcription: [`a0/materials.json`](a0/materials.json).
- Derived values and executed checks: [`a0/results/validation.json`](a0/results/validation.json).
- No publisher PDFs, large datasets, or production-solver files are included or modified.
- Independent formulas and original numerical calculations in this audit are explicitly distinguished from source values.
- No claim of matching the user's previous paper style can be certified: the checkout initially contained only a README, with no earlier paper or accepted blueprint supplied.
