# VALIDATION_MATRIX

Every validation and verification performed, with its source, its expected value, its
reproduced value, its tolerance, and the script that produces it.  Where something was
**not** reproduced, it says so and gives the reason.  No row is aspirational: each is a
check that runs.

Legend: **V** = verification (the code solves the stated equations correctly);
**v** = validation (the equations reproduce an independent physical result).

---

## 1. Reductions to closed-form limits (**v**)

| # | Source / benchmark | Equation or limit checked | Parameters | Expected | Reproduced | Tolerance | Script |
|---|---|---|---|---|---|---|---|
| 1 | Classical shear-horizontal plate modes, `ω² = c₅₅(k_x² + k_z²)` with `k_z = jπ/d`, `j = 1,2,3` (textbook Rayleigh–Lamb SH family) | `Plate.temporal` with `ℓ = 0`, `f = 0`, `H = 0` | `K = 0.8`, `degree = 18`, ZnO `c₄₄` | `ω_j = √(c₅₅K² + (jπ)²)` | every one of the three branches matched | `1e-9` (absolute in `ω`) | `test_model.py::test_classical_exact_SH_modes` |
| 2 | Strain-gradient SH branch with the single-length gradient energy, `ω² = c₅₅K²(1 + λ²K²)` | same, `ℓ = 50 nm ≠ 0` | `K = 0.8`, default `Plate` | `ω = √(c₅₅K²(1+λ²K²))` | matched | `1e-10` | `test_gradient_exact_fundamental_SH` |
| 3 | Classical plate, both electrical face conditions | strong-form root of the reduced system vs. the spectral eigenvalue, `ground` and `open` | `K = 0.3, 0.7`, `degree = 18`, `ℓ = f = 0` | same `ω` from two routes | agreed | `1e-10` | `test_independent_classical_grounded_and_open` |
| 4 | Non-zero carrier–gradient coupling, strong form | `H ∈ {0, ±H_TEST}`: spectral vs. strong-form root; and the sign of the decay | `K = 0.3` | same `ω`, `Im ω < 0` | agreed | `1e-10` | `test_independent_nonzero_f_H_temporal` |
| 5 | Reciprocity (Maxwell identity of `H` and `f`) | polynomial operator at `+k_y` vs `−k_y`: `Dᵀ = E`, `FᵀJ + JG = 0` | `k_y = ±0.13` | symmetry exact | `1.0e-13` / `1.0e-12` relative | as stated | `test_reciprocity_at_oblique_wavenumber` |
| 6 | Energy/dissipation balance of a mode | stored energy > 0, dissipation > 0, relative balance | `K = 0.3`, three `H` | balance closes | `5e-6` relative bound (measured `~1e-12`) | `5e-6` | `test_temporal_energy_dissipation_balance` |
| 7 | Independent finite-element plate in the thickness direction | `MeshPlate` (H¹-conforming) at 8, 12, 18 elements vs. the spectral edge value | operating point | monotone convergence to the spectral value | errors fall monotonically; finest `< 3e-5` | `3e-5` at 18 elements | `test_independent_C1_mesh_approaches_spectral_edge` |
| 8 | Spectral convergence | `R_B(degree)` for degrees 14…33 | operating point | error decreases | reference at 33; `R_B` relative error `2.6e-5 … 1.6e-6`; `K_B` error `< 4e-12` | recorded, no rejection | `convergence_audit.py` → `fig09_validation_convergence.csv` |
| 9 | Quadrature sufficiency | 64 … 256 Gauss nodes at fixed degree | operating point | no change | spread `1.70e-9` relative | recorded | `quadrature_audit.py` |
| 10 | Temporal vs. spatial route | same mode, both routes, 11 wavenumbers | operating point | `k` agrees | `abs_K_mismatch = 5.6e-6…7.3e-6`; `rel = 1.9e-5` | recorded | `convergence_audit.py` → `fig09_temporal_spatial_consistency.csv` |
| 11 | Elastic-wave-speed / EM-wavelength arithmetic | `c_s = √(c₄₄/ρ)`; `k_EM d` from `ω√(μ₀ε₀)d` | material file | `c_s = 2746.6 m/s`; `k_EM d = 2.2e-4` | `2746.6 m/s`; `2.211005e-4` (`rel 4.98e-3`) | `5e-3` relative | `phase_speed_audit.py` |
| 12 | Dimension and constitutive audit | every group re-derived from `materials.json`; Legendre measures; block entries | all | 5 groups to 4 digits; `Q = 0.074635`, `α_d = 0.8283`, `λ = 0.25`, `f = 2.5631e-3`, `H_ref = 1.8927e-21` | all reproduced | `2e-3` relative | `verify_dimensions.py`, `round18_reference_checks.py` |
| 13 | Schur (positive-definiteness) bound | `H_bound = ℓ√(a c*)`, `c* = c₃₃ − 2c₁₃²/(c₁₁+c₁₂)` | material file | `8.9660e-22 J·m` | reproduced; all runs at `s ≤ 5e-4` | `2e-3` relative | `round18_reference_checks.py` |
| 14 | Natural-boundary data identity (Gate 1) | traction + corner data reconstructed from the spectral solution vs. an independent double-precision evaluation | operating point, peak, `k055` | incident `~1e-13`, reflected `≲1e-6`, plain traction `≫1` | incident `5.7e-14…1.3e-12`; worst reflected `8.9e-9…3.5e-6`; plain traction `1.7e+1` | as recorded | `round21_gate1_traction.py` |
| 15 | Corner line-force gate (Gate 2) | three configurations, `n = 10` vs `n = 28` | operating, peak, `k055` | force decreases with `n`; exponent ≈ `−0.63`; partition insensitive | `8.42e-2/3.27e-3/3.79e-2 → 4.46e-2/1.71e-3/1.98e-2`; partition moves `3.9e-6` | recorded | `round21_gate_corner.py` |
| 16 | Insulating-edge default (Gate 3) | default `edge_electric` is `insulating`; manuscript says so | — | default matches text | PASS | exact | `round21_edge_default_audit.py` |
| 17 | Phase-speed / plane-transform identities | composition additive in distance; coincident planes return the input; zero attenuation leaves the ratio alone; both attenuations used at the edge | algebra | identities hold | PASS | `1e-13` | `test_composition_is_additive_in_distance`, `test_coincident_planes_return_the_input`, `test_zero_attenuation_leaves_the_ratio_alone`, `test_edge_value_uses_both_attenuations` |
| 18 | Mutation testing | 15 deliberate defects (sign, slot of `A`, reference plane, `R_B`-as-reflectance, …) | — | every mutant caught | 15/15 caught | exact | `mutation_tests.py` |
| 19 | Claim registry ↔ data ↔ manuscript | 40 live claims, 6 deprecated, 10 source-agreement entries | — | all agree | 10/10 source-agreement, PASS | exact string/number match | `claim_audit.py` |
| 20 | Quasistatic justification | `ω d/c_s ≪ 1` regime argument, evaluated at the operating point | — | PASS | PASS | recorded | `quasistatic_check.py` |
| 21 | Flexoelectric magnitude control | `f = 1 nC/m` and `10 nC/m` vs. `1 nC/m` baseline | operating point | small effect | `−0.012 %`, `−1.176 %` | recorded | `flexo_control.py` |
| 22 | Admissibility re-derivation | every sweep row re-tested against conservation + convergence, no re-solving | fig02/04/07 | no row flips | 130/130, 139/139, 95/95 admissible, 0 flipped | exact | `reclassify_csv.py` |

## 2. What was **not** validated, and why

| Not done | Reason | Consequence stated in the paper |
|---|---|---|
| Comparison with an **experiment** | No measurement of `R_B` for this structure exists; `f` and `H` have no measured value for ZnO (`a0/materials.json` marks them `NOT_SOURCED`) | The paper reports a theoretical share and explicitly declines to claim experimental agreement |
| Comparison with another group's **numerical** solution of the same coupled edge problem | No published solution of the flexoelectric + strain-gradient + semiconductor edge-reflection problem was found to compare against | Novelty is claimed for the calculation, so there is nothing to benchmark it against; the defence is the reduction set above, not a head-to-head |
| Convergence against a **full 3D finite-element** solution | Not available in this environment; the H¹ mesh check is 1D in the thickness and does not resolve the edge singularity | The corner result is reported as a **bounded closure** with exponent ≈ −0.63, not as a converged singular field |
| Exact reproduction of the cited thermodynamic theory's own examples | The 2025 paper's plane-strain examples are a different boundary-value problem | The paper cites it for the framework, not for a numerical benchmark |
| **Compiled** manuscript / typeset page proof | No TeX engine existed in the build environment | Static validation only; no PDF is shipped or claimed |

## 3. How to re-run everything in this document

```bash
cd 01_PROGRAM
python prepare_archive_layout.py          # layout shim (symlinks only)
python paper_a_study/run_all_checks.py    # 22 PASS, 1 SKIP (no TeX), OVERALL: PASS
```

Individual rows: the script column above names the file; all are runnable standalone
(see `04_REPRODUCTION/RUN_ORDER.md` for the `-m` invocations that the battery uses).
