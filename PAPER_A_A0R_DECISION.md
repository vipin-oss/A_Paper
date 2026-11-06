# PAPER A — A0-R supervisor decision

**Date:** 2026-11-05

**Decision: REVISE — do not advance on the basis of the earlier lossless window.**

**Retained objective:** *Negative Reflection of Guided Waves in a Flexoelectric Piezoelectric-Semiconductor Plate with Carrier–Strain-Gradient Coupling.*

The objective, n-type ZnO/6mm material family, finite-plate/reflecting-edge geometry, [Blueprint V2.1](PAPER_A_BLUEPRINT_V2_1.md), and **one added interaction** \(\Delta\mathcal H=\Delta n\,H_{jkl}\varepsilon_{jk,l}\) are unchanged. No alternative topic, extra coupling, edge solver, manuscript or later phase has been introduced.

**Evidence boundary:** sourced-constant propagation figures use the **finite-carrier classical limit f=A=H=0**. All nonzero A/H tests are **synthetic at f=0**. The full nonzero-flexoelectric material model is not calibrated or claimed validated, and no negative reflection is demonstrated.

## 1. Requested reports

1. [PAPER_A_A0R_NOVELTY_COMPARISON.md](PAPER_A_A0R_NOVELTY_COMPARISON.md)
2. [PAPER_A_A0R_BACKWARD_WAVE_FEASIBILITY.md](PAPER_A_A0R_BACKWARD_WAVE_FEASIBILITY.md)
3. This decision.

These reports supersede the **interpretation** of the historical A0 34.62 kHz segment and 1.1567 MHz damping number; the earlier reports are retained as historical evidence, not silently rewritten.

## 2. Disposition of the focused corrections

| Supervisor requirement | Work performed | Finding / remaining gate |
|---|---|---|
| Inspect actual Qu Appendix C if accessible | Bounded publisher, public XML, exact-title/identifier and connected-Drive access check | Actual constitutive equations still inaccessible: **NOVELTY UNRESOLVED**. No absence/equivalence/special-case claim. |
| Independently verify the reported narrow window | Analytic K→0 thickness cutoff, parity Galerkin K=0 solve, independent six-state finite-K roots | **34.62 kHz was the checked K≥0.005 segment; the full one-sided frozen quasistatic-model interval is 58.46 kHz**, near 3.249 GHz for d=1 μm. |
| Calculate complex loss/transport, not infer feasibility from slope | Complex ω at real k **and** complex k at real ω; independent eight-state propagator; power/energy/dissipation accounting | At original n0=10¹⁹ m⁻³, pole power FWHM is **2.313 MHz**. Original backward continuation is not on a decaying-vacuum sheet. |
| Minimal justified ZnO thickness/carrier study | Exactly nine design scenarios: d=0.5,1,3 μm; n0=10¹⁷,10¹⁸,10¹⁹ m⁻³, fixed source constants | Some lower-carrier **classical-limit** roots carry backward energy over short distances; achievable samples and full-model feasibility are unverified. |
| H symmetry, stability, numerical and ordinary-parameter sensitivity | All three 6mm directions, strict full-3D bound, signed η, convergence, rounding-scale C/e probes and explicit transport controls | Some **synthetic** linewidth effects exceed numerical/control variations; frequency shifts remain confounded. A physically plausible ZnO H range is **not known**. |
| Maintain validation and stop | 65 A0-R numerical checks + symbolic assertions; 16 A0-R tests; rerun original 52 checks + 12 tests | All pass for the calculations actually executed. **Research decision remains REVISE. STOP.** |

## 3. The decisive propagation correction

At d=1 μm and n0=10¹⁹ m⁻³, the reproduced temporal pole has:

- **1.1567 MHz:** \(-\operatorname{Im}\omega/(2\pi)\), amplitude-decay frequency scale / isolated-pole **power HWHM**;
- **2.3135 MHz:** isolated-pole **power FWHM**, approximately **39.6 times the full** frozen 58.46 kHz interval;
- **137.6 ns / 68.8 ns:** amplitude / energy 1/e lifetimes.

None is a spatial attenuation coefficient or propagation length. At the original real drive frequency, the backward continuation gives \(K\simeq-0.05201-0.06366i\) on the q_vac=K sheet: **the exterior grows rather than decays**, so this is not an admissible backward guided port. Both numerical methods find that formal zero; algebraic agreement alone does not make it physical. No admissible backward continuation of this family was found at the **41 sampled frequencies** across the frozen window. This is not a proof about every frequency or every other mode.

The admissible **forward** root instead has an energy 1/e length of **8.02 μm**, with only \(3.83\times10^{-6}\) of its pre-launched power remaining after 100 μm. That length must not be reported as a backward reflected-wave result.

The lower-carrier n0=10¹⁷ scenarios conditionally retain backward-energy roots. At the retained target, the classical carrier-only model predicts about **48–54% survival over 100 μm**, but less than 0.22% over 1 mm. Their phase wavelengths are roughly 0.34–2.98 mm; even the least attenuated target case preserves only **8.8% over one phase wavelength**. These are conditional short-distance/subwavelength transport results, **not demonstrated negative-reflection beams**. Mechanical/surface/contact losses and an actual excitation/conversion efficiency are not supplied.

## 4. H correction: mathematical sensitivity is not physical plausibility

The three allowed tensor directions belong to the same single coupling; no additional mechanism is introduced. Synthetic tests use fixed \(\ell=50\) nm and \(A=\ell^2C\otimes I\), with \(H:A^{-1}:H/a\le0.64<1\). The length and coefficients are **not calibrated ZnO properties**.

- At K=2, η=+0.1 ha changes the pole FWHM by about **129.7 kHz**, well above the conservative numerical floor and the roughly 2 kHz range of the specified parameter controls.
- At the small original K, hb/hc frequency shifts at η=+0.1 are only about **1.09 / 0.66 Hz**—near/below the 1 Hz numerical reporting floor—whereas ha couples much more strongly.
- Across the signed tested η range, K=2 frequency shifts for all three directions lie within the roughly **±2.614 MHz** envelope of the declared C/e rounding-scale probes. This prevents a frequency-only attribution to H under that control set.
- The controls are **not measured uncertainty distributions**, and unknown A, f, actual carrier/transport variation and surfaces are not bounded by them.

Therefore **numerical distinguishability is demonstrated for some artificial coefficients; physically plausible, experimentally identifiable H effects are not established**. No fraction of the stability bound is presented as an empirical range.

## 5. Why REVISE, not PASS or a material-wide NO-GO

**PASS is unsupported** because the primary Qu equation comparison, physical higher-order parameter closure, and physically justified H range remain unresolved. The original claimed operating point also fails the finite-carrier backward-port test in the explicitly studied classical limit. The completed numerical checks do not close those research gates.

A **universal NO-GO is also unsupported**: conditional lower-carrier backward-energy roots survive in this bounded limiting-model study. They do not justify replacing the retained objective, claiming a viable sample, or hunting unlimited alternative parameters. The uncalibrated full flexoelectric model and unexamined parts of the spectrum cannot be declared impossible from this focused calculation.

No edge calculation was required or authorized in A0-R, and none was built. Its absence is **not a failure to execute this correction**; it is why no negative-reflection coefficient, reflected angle or complete-paper success is claimed. The existing plane-strain/angle-selection geometry gate remains unchanged.

If this work is explicitly resumed later, the finite missing evidence is: the actual Qu Appendix C definitions/equations; a justified nonzero f/A material closure and defensible H magnitude/bound beyond abstract stability; and sample/boundary/loss data sufficient to select a usable backward port. These are unresolved evidence requirements, **not an authorization for a new programme or the next phase**.

## 6. Audit trail and stop

- Isolated new code/protocol/results: [`a0r/`](a0r/).
- Machine-readable result: [`a0r/results/validation.json`](a0r/results/validation.json); **65/65** numerical checks passed, plus exact symbolic assertions.
- **16/16** A0-R regression tests and retained **12/12** A0 tests passed; the retained **52/52** A0 numerical checks also passed on rerun.
- Blueprint and five retained A0 source hashes match [`retained_a0_sha256.json`](a0r/results/retained_a0_sha256.json). No production solver was changed.
- Reproduction commands and dependency versions are in [README](README.md) and the feasibility report.

**STOP after A0-R. No A1, edge solver, manuscript, Papers B/C, or further parameter/literature search has been started.**
