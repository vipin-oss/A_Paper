# Paper A — Final Focused Scientific Check

**Scope.** This check preserves `PAPER_A_RESEARCH_REPORT.md`, `paper_a_study/`, its four figures and all numerical artifacts. No model, coupling, material, geometry or research phase was added. The checks below use the retained `primary_edge.json`, `H_sensitivity.csv`, `validation.json`, figure inputs and executed test/regression logs.

## Verdicts

| # | Required check | Verdict | Conclusion |
|---:|---|---|---|
| 1 | Backward-channel classification | **PASS** | The reported channel is a solved backward-mode conversion, not ordinary reflection, retroreflection, negative refraction or a slope inference. |
| 2 | Geometry and angle terminology | **CORRECT** | The calculation is a 2D plane-strain plate-edge calculation with a specified propagation-plane tangential component. It is not a true 3D oblique plate-edge solution. The primary report and Figure 2 caption were corrected to state this explicitly. |
| 3 | Matched H comparison | **PASS** | The report now gives a compact H = 0 / H ≠ 0 table at one frequency, one geometry, one reference distance and one normalization, and separates edge conversion from propagation attenuation. |
| 4 | Coupling novelty | **UNRESOLVED** | Qu et al.'s relevant equations remain inaccessible. No identity with or novelty over their published constitutive equations can be established. The provisional-novelty statement is retained. |
| 5 | Figures and validation scope | **PASS** | All four figures are generated from the focused numerical artifacts. The 143 numerical checks, 18 new tests and 50 retained regression tests apply to this focused model/result. |

## 1. Backward reflection evidence

For every primary case, the edge solve classifies 182 modes as outgoing and enforces rank-182 edge matching. The incident port is normalized to unit self-power. The following H = 0 quantities are retained in `primary_edge.json`:

\[
k_{xi}=(3680.995098+0.0270136i)\ \mathrm{m^{-1}},
\qquad
k_{xB}=(1225.873461-0.0261530i)\ \mathrm{m^{-1}}.
\]

The edge-tangential wavenumber is fixed at

\[
k_y=K_y/d=649.058752\ \mathrm{m^{-1}},
\]

so it is identically conserved in every primary case.

At H = 0, the incident and backward thickness-integrated mechanical/electrical/carrier power components are

\[
(P_{xi},P_{yi})=(1.000000,0.176327),
\qquad
(P_{xB},P_{yB})=(-0.0154248,-0.00816692).
\]

Both backward components are negative. The solved backward energy velocities are

\[
(v_{E x}^i,v_{E y}^i)=(378.912,66.812)\ \mathrm{m/s},
\qquad
(v_{E x}^B,v_{E y}^B)=(-186.020,-98.491)\ \mathrm{m/s}.
\]

The backward channel coefficient is nonzero, with self-power

\[
R_{B,\mathrm{edge}}=0.0231505420,\qquad
R_{B,\,2\mu\mathrm m}=0.0231456192,
\]

using the same incident-self-power normalization. Thus the calculation satisfies all four required conditions: solved outgoing coefficient, positive incoming physical power, negative backward physical power, and negative physical power along the phase direction. It is not retroreflection because the backward phase wavenumber does not retrace the incident wavevector.

For the H ≠ 0 rows, the incident and backward physical power directions and the negative energy-velocity condition remain satisfied. The 2.3% value remains an isolated-channel self-power, not total reflectance.

## 2. Plane-strain terminology correction

The model has an invariant y direction, a propagation plane in x–z and a fixed nonzero y-component of the phase vector. It is therefore a **2D plane-strain plate-edge problem**, not a full 3D oblique-incidence plate problem.

At H = 0,

\[
\frac{\operatorname{Re} k_{xB}}{\sqrt{\operatorname{Re}^2 k_{xB}+k_y^2}}
=0.5303.
\]

A true oblique reflected ray retracing the opposite x-normal would have cosine 1. The signed physical energy angle is −27.90°, but this is not a claim that the complex phase wavenumber obeys a classical same-magnitude reflection law. The nonzero kᵧ is the tangential propagation-plane component required by the fixed drive, not a validated third oblique dimension.

The primary report now labels the geometry as 2D plane strain, identifies −27.90° as a signed thickness-integrated energy angle, states the reflected mode cosine, and explicitly declines to call the result a 3D oblique reflection. Figure 2's caption now makes the energy-angle/phase-ray distinction explicit. No numerical value was changed.

## 3. Matched H comparison

The following table uses one real frequency (16.684123136 GHz), one real kᵧ (0.1298117503), the same degree-22 edge solve, the same 182 outgoing modes, the same geometry and edge conditions, and incident-self-power normalization. `L = 10d = 2 μm` is the reference plane.

| Fixed-drive quantity | H = −0.05 H* | H = 0 | H = +0.05 H* |
|---|---:|---:|---:|
| Re kᵢₓ | 3682.191697 m⁻¹ | 3680.995098 m⁻¹ | 3683.293078 m⁻¹ |
| Im kᵢₓ (propagating/attenuation coefficient) | 0.929927 m⁻¹ | 0.0270136 m⁻¹ | 1.667167 m⁻¹ |
| Re kᴮₓ | 1224.057422 m⁻¹ | 1225.873461 m⁻¹ | 1222.771642 m⁻¹ |
| Im kᴮₓ (propagating/attenuation coefficient) | −1.326168 m⁻¹ | −0.0261530 m⁻¹ | −2.173365 m⁻¹ |
| Conserved kᵧ = Kᵧ/d | 649.058752 m⁻¹ | same | same |
| Pᵢₓ/Pᵢᵧ | 1.0000 / 0.1763 | 1.0000 / 0.1763 | 1.0000 / 0.1762 |
| Pᴮₓ/Pᴮᵧ | −0.01544 / −0.00819 | −0.01542 / −0.00817 | −0.01545 / −0.00820 |
| Backward energy angle from outward −x normal | −27.93° | −27.90° | −27.96° |
| Reflected mode cosine Re kᴮₓ / √(Re² kᴮₓ + kᵧ²) | 0.5296 | 0.5303 | 0.5308 |
| Backward channel self-flux at edge / incident self-flux | 2.307% | 2.315% | 2.301% |
| Same-plane return, 2 μm from edge | 2.286% | 2.315% | 2.266% |
| Attained-range separation, attenuation-only prediction | 2.272% | — | 2.265% |
| Same-plane return, 100 μm from edge | 1.469% | 2.291% | 1.067% |
| Carrier-only x attenuation length, incident/backward | 537.7 / 377.0 μm | 18,509 / 19,118 μm | 299.9 / 230.1 μm |
| Temporal power FWHM at common real K = 0.27741975 | 78.52 kHz | 1.549 kHz | 128.71 kHz |
| Frequency shift at that same real K | −53.76 kHz | 0 | −91.83 kHz |

The **edge conversion** is the self-power ratio at the edge. The **same-plane return** includes propagation from the source plane to the reference plane. At 2 μm, the H = −0.05 H* result is 0.013 percentage points below its attenuation-only attained-range prediction. The larger endpoint discrepancies show that conversion and attenuation are not algebraically separable at finite distance in this calculation. Thus the table does not attribute the entire H-dependent return change solely to propagation attenuation.

The 21-point `H_sensitivity.csv` sweep supplies the same matched comparison for intermediate H values, with all power-balance errors below 2.25 × 10⁻¹².

## 4. Coupling novelty

The only additional energy is

\[
\Delta \mathcal H=\nu H:g.
\]

It is not mathematically identical to the retained static flexoelectric term \(-E\cdot f:g\), because the product is with \(\nu\), not with \(E\), and it is not identical to the retained strain-gradient energy \(g:A:g\). No previously published constitutive term has been recovered from a complete equation set in this study.

**UNRESOLVED.** Qu et al., *International Journal of Engineering Science* 208, 104165 (2025), DOI [10.1016/j.ijengsci.2024.104165](https://doi.org/10.1016/j.ijengsci.2024.104165), could not be accessed beyond metadata/preview. The relevant appendix was not available, so no statement is made that this H coupling is absent from Qu et al.'s model. Novelty over that work remains **provisional**, not established.

## 5. Figures and validation scope

| Figure | Source data | Verified content |
|---|---|---|
| `dispersion_and_H.svg` | `dispersion.csv`, `H_sensitivity.csv` | Matched guided-family frequency, frequency shift and temporal power FWHM for H = 0, ±0.05 H*. |
| `edge_conversion.svg` | `frequency_scan.csv` | Backward self-flux at 2 μm and 100 μm, plus the signed energy angle at identical real ω and kᵧ. |
| `H_parameter_effect.svg` | `H_sensitivity.csv` | Edge, 2 μm and 100 μm self-flux; carrier-only spatial attenuation lengths; temporal power FWHM. |
| `computed_channel_beam.svg` | `beam_validation.json` and the 17/25-node Hermite angular-spectrum solve | Independently solved incident and backward channel intensity fields. |

The four PNG cache previews correspond to these computed data products. No figure is an assumed ray diagram.

The focused runner reports **143/143** numerical checks and exit status 0. The standalone focused package reports **18/18** tests. Fresh retained regressions report **12/16/22 = 50** tests. These counts cover the focused model, edge calculation, figures and validation artifacts reported here. They do not validate a missing Fang/Wei transcription, Qu novelty, material calibration or pointwise corner stresses.

## Overall

**PASS with one terminology correction and one retained UNRESOLVED novelty limitation.** The 2.315% channel is a genuine solved backward-mode edge-conversion result in the explicitly specified 2D plane-strain model. The angle has been reclassified and is no longer described as a 3D oblique-reflection angle. Coupling novelty remains provisional.
