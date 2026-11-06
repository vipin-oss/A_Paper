# PAPER A — A0-S model and operating-regime selection

**Date:** 2026-11-05
**Single recommendation: REVISE.**
**Novelty: NOVELTY UNRESOLVED.**
**Scope: STOP after A0-S; no edge scattering or manuscript.**

## 1. Decision in one paragraph

Keep the agreed objective: **Negative Reflection in a Flexoelectric Piezoelectric-Semiconductor Plate with Carrier–Strain-Gradient Coupling**. Retain ZnO, [Blueprint V2.1](PAPER_A_BLUEPRINT_V2_1.md), geometry, governing structure and the sole added reciprocal energy term Δn H_jkl ε_jk,l. The bounded calculation identifies **one primary and one fallback numerical validation target**, both 200 nm plates under the **existing synthetic A = ℓ² C ⊗ I, ℓ = 50 nm, f = 0 control**. Their H = 0 backward-energy transport is real within that specified mathematical model and independently checked. **Neither is an experimentally qualified full-model ZnO regime.** The broad bandwidth depends on unmeasured A; actual f/H, thin-plate transport and exact radiation admissibility remain unverified, and the closest prior-art equations remain unavailable. Numerical success therefore does **not** justify proceeding to a negative-reflection claim.

The focused A0-S work is complete; the scientific gates below are not.

## 2. Exactly one primary and one fallback

These are **conditional numerical targets**, not certified device specifications. H = 0 is the comparison baseline, not a measured absence of the proposed coupling.

| Item | **Primary: B0.2-G** | **Fallback: L0.2-G** |
|---|---|---|
| Stored case identifier | `bulk_Hall_transfer_d0.2_synthetic_gradient` | `literature_model_d0.2_synthetic_gradient` |
| Material family / total thickness | n-type 6mm ZnO / **200 nm** | n-type 6mm ZnO / **200 nm** |
| Free-electron concentration | **2 × 10¹⁸ m⁻³** | **10¹⁹ m⁻³** |
| Mobility / diffusion | 0.0175 m²/(V s) / 0.000455 m²/s | 0.01 m²/(V s) / 0.00026 m²/s |
| Transport provenance | Paired bulk Hall n and mobility, Suscavage et al. (1999); **D derived** and Hall-to-drift/thinning transfer assumed | Retained **literature-model** inputs, not same-sample measured plate transport |
| Higher-order / flexoelectric status | **Synthetic ℓ = 50 nm, A = ℓ²C; f = 0 incomplete control** | Same explicit limitations |
| Baseline drive | **17.326041078 GHz** | **17.325774742 GHz** |
| Finite-carrier projected backward interval | 17.251515472–17.400566684 GHz | 17.251258601–17.400290882 GHz |
| Projected width / pole power FWHM | **149.051211 / 0.327462 MHz** | **149.032282 / 1.440760 MHz** |
| Actual backward K = k d | **0.320992366 − 0.000490737 i** | **0.320996617 − 0.002159312 i** |
| Backward energy velocity | **−419.25 m/s** | **−419.17 m/s** |
| Energy attenuation length | **203.775 μm** | **46.311 μm** |
| Backward E(100 μm) / E(one phase wavelength) | **0.61217 / 0.98097** | **0.11540 / 0.91894** |
| Sample-supported transport span | 17.253005985–17.399076172 GHz, **99/101** points | 17.300439254–17.351110229 GHz, **35/101** points |
| Forward control E(100 μm) | **0.77229** | **0.30547** |
| 100 μm each-leg transport product, unit-conversion ceiling | **0.47278** | **0.03525** |
| Exterior / radiation status | Decaying Laplace exterior; passes conservative phase-light-line/exponent guards; **full Maxwell radiation not solved** | Same |
| Expected H sensitivity from this screen | Strong attenuation sensitivity; tested ha = −0.1 reference improves same-drive E100 to 0.95262, +0.1 reduces it to 0.094175 | More marginal: the same signed reference tests give 0.70812 versus 2.9339e−5 |

The primary's carrier data come from **bulk hydrothermal ZnO**, not a demonstrated released 200 nm plate. Classical C/e/κ/ρ are retained from another literature-model source; this is a **hybrid-provenance scenario**, not a jointly measured specimen. The fallback's density and transport constants are model inputs. Both thicknesses are design choices, not fabricated observations. Neither has empirical f, A or H calibration.

### Why this ranking is defensible within its limited role

1. **Admissibility:** both actual backward roots have Re K > 0, Im K < 0, Px < 0, positive stored energy and passive spatial decay in the energy-flow direction. Both have forward controls at the same real drive. Roots were not selected by dispersion slope alone.
2. **Manageable carrier loss at the stated distance:** both pass the predeclared **10% energy at 100 μm AND 10% per phase wavelength** criterion. The primary has substantial margin; the fallback is only marginal at 100 μm. These are calculated carrier-loss properties, not measured total loss.
3. **Ranking before H tuning:** selection uses each H = 0 case's interval midpoint and E100. No favorable H cancellation was used to make a case qualify. The primary's 0.61217 outranks 0.11540; the source-provenance tie-break is not needed.
4. **Genuine backward energy:** normalized powers are −4.795915 and −4.794807, with full chemical/electrical/exterior/face power accounting. This is stronger evidence than a lossless negative slope, but still not edge reflection.
5. **Finite propagation scale:** both phase wavelengths are about 3.915 μm. The one-wavelength condition excludes spurious-looking short-distance survival of very long-wave, strongly attenuated roots.
6. **H sensitivity is exposed, not hidden:** neither target is robust across the tested synthetic H set. Stable H can greatly improve or destroy transport. No physical H range is known, so these favorable H = 0 operating points are not certified for actual ZnO.

The fallback should be used only as the best remaining **evaluated comparison target**, not as an equally low-loss replacement. Its two-leg transport product is only 3.53% even with hypothetical unit edge conversion. No actual edge conversion coefficient is known.

## 3. Why other evaluated cases are not selected

The main grid contains **two sourced/model-backed carrier sets × three design thicknesses × two control models = twelve H = 0 cases**. No unsourced lower concentration was introduced to make loss disappear.

- **All six sourced-constant classical limits fail the combined transport screen.** B0.2-C has an admissible backward branch at many sampled frequencies but only E100 = 1.925e−4 and Eλ ≈ 5.0e−12 at the midpoint. It is explicitly **not feasible**.
- The other classical cases and the four thicker H = 0 gradient cases have no admitted positive-phase backward port in their sampled, carrier-shifted frequency brackets. Formal exterior-growing roots remain recorded rather than being relabelled physical. This is a bounded result, **not global nonexistence** over all modes or exterior sheets.
- Every tested H perturbation at 0.5/1 μm fails the combined transport screen. A B1-G/negative-ha example has E100 ≈ 0.10011 but only **2.38e−131 per wavelength**; it is not promoted to feasibility.
- The thin-plate **149 MHz** bandwidth is induced primarily by the **synthetic A-dependent thickness-mode ordering**, already at H = 0. It is not proof of a calibrated material effect or an H-created backward branch.
- Ordinary-parameter probes do not overturn the H = 0 ranking: primary own-midpoint E100 = 0.60882–0.61551; fallback = 0.10997–0.12178. Those probes are not measured uncertainty intervals and do not overcome unknown f/A/H or surface effects.

The complete per-case tables and actual complex roots are in the [operating report](PAPER_A_A0S_OPERATING_REGIME.md), [H report](PAPER_A_A0S_H_SENSITIVITY.md) and [screening JSON](a0s/results/screening.json).

## 4. Mandatory validation retained and extended

| Validation layer | Outcome |
|---|---|
| Formal A0-S numerical criteria | **1,254 / 1,254 passed** |
| Independent final artifact / matched-point audit | **136 / 136 passed** |
| A0-S regression tests | **22 / 22 passed** |
| Retained A0-R | **65 checks / 16 tests passed again** |
| Retained A0 | **52 checks / 12 tests passed again**, including symbolic assertions |
| Blueprint plus ten-file retained ledger | Blueprint and all ten listed retained files hash-identical; the blueprint is one of the ten, not an eleventh file |
| Independent full-gradient subset check | Newly derived **12-state strong-equation propagator**, same f = 0, A = ℓ²C, reciprocal-H subset; no Galerkin matrices/basis reused |
| Independent classical recovery | Retained **8-state** finite-carrier strong system |
| Selected configurations and their H variants | Complex poles/roots, cutoff/minimum, curvature, p = 24/28/32 convergence, governing/face residuals, positive energy, carrier dissipation and complete power balance |
| Same-K / same-drive comparisons | **40 matched comparisons** for selected-H and ordinary probes, with independent temporal and spatial checks for each |
| Full electromagnetic radiation / genuine negative reflection | **Not demonstrated**; not silently inferred from numerical agreement |

Across the main independent comparisons, maximum equivalent complex-frequency discrepancy is **0.00820 Hz** and |ΔK| **3.27e−12**. Same-point independent comparisons give **0.00884 Hz** and **2.81e−12**. Maximum selected/H degree spread is **0.01341 Hz** in the pole, **0.01543 Hz** in power FWHM and **3.14e−12** in K. A **1 Hz pole / 2 Hz FWHM reporting floor** is used. Curvature contrasts have a much larger empirical numerical-resolution envelope, **2.4e−4 in Ω/K²**; small changes are not all declared resolved.

For all positive-sheet sampled spatial roots, maximum governing/face residual is **2.96e−10** and maximum energy-balance error **1.90e−8**. Independent strong/Galerkin power/energy/dissipation agree within **1.52e−11 relative** in the selected checks. The primary/fallback minimum adjacent-step modal MAC is about **0.99993**. Exact high-DOF condensation improves conditioning without changing the governing operator or truncating those DOFs.

Derivation and reproduction are documented in [a0s/STRONG_VALIDATION.md](a0s/STRONG_VALIDATION.md), [protocol](a0s/protocol.json), [formal validation](a0s/results/validation.json), [final audit](a0s/results/final_audit.json) and [README](README.md).

## 5. Research gates that remain open

| Gate | Current evidence | Consequence |
|---|---|---|
| Achievable plate transport | Low-density n/Hall mobility measured in bulk; no matching released-plate measurement or surface/depletion calibration; Hall/drift and GHz applicability assumed | Cannot certify uniform n/M/D for the 200 nm geometry |
| Full flexoelectric/gradient material | No empirical f/A; ℓ = 50 nm synthetic and f = 0 an incomplete control | Broad branch is conditional; not a calibrated result for the full objective |
| Physical carrier–gradient coupling | No defensible electron H range; strong synthetic sensitivity, including catastrophic loss | Cannot certify the chosen operating point or experimentally isolate H |
| Total attenuation | Carrier loss computed; other intrinsic mechanical/electrical loss and defect kinetics uncalibrated | Calculated survival is not measured device performance |
| Radiation | Laplace exterior decay and conservative light-line/exponent diagnostics pass for selected ports; no Maxwell outgoing solution or radiated-power accounting | Exact radiation admissibility remains unclosed |
| Closest prior art | One new bounded repository-targeted Qu query did not expose Appendix C; earlier inaccessible routes not repeated | **NOVELTY UNRESOLVED**; no absence/equivalence/newness claim |
| Negative reflection | Uniform sagittal forward/backward mode pair only; no off-normal edge matching, scattering coefficients or angular energy-flux classification | No genuine negative-reflection claim is permissible |

A meaningful next scientific authorization would first need to address the consequential evidence gaps, not merely add more favorable plots. Actual Qu equations must be compared in consistent carrier-variable/energy/boundary conventions; post-release transport and nonzero higher-order coefficients must be defensibly supplied or bounded; radiation and the agreed off-normal edge problem must eventually receive the mandatory validation. **These are conditions for later consideration, not work started or automatically authorized here.** No new field, different material family or substitute reflection objective is proposed.

## 6. Why REVISE

There is a mathematically coherent, independently checked **conditional** transport-capable regime, so the bounded screen does not establish fundamental impossibility. But none of the evaluated cases closes the empirical full-model, radiation or novelty gates. Calling either selected target a physically viable negative-reflection experiment would manufacture success.

**Recommendation: REVISE. Keep the original objective and model structure. Retain the primary/fallback only as conditional numerical validation targets. STOP after A0-S. No edge scattering, manuscript, blueprint edit, commit or push was performed for this checkpoint.**

### Delivered reports

1. [PAPER_A_A0S_OPERATING_REGIME.md](PAPER_A_A0S_OPERATING_REGIME.md)
2. [PAPER_A_A0S_H_SENSITIVITY.md](PAPER_A_A0S_H_SENSITIVITY.md)
3. **[PAPER_A_A0S_MODEL_SELECTION.md](PAPER_A_A0S_MODEL_SELECTION.md)** — this decision.
