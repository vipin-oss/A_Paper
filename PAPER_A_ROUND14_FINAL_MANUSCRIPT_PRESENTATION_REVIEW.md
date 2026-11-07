# Round 14 — final manuscript presentation review

One judgement per criterion. No blanket pass. Where a criterion is met only in
part, the part that is missing is named.

## A. Style against the author's own published articles

| Criterion | Judgement |
| --- | --- |
| Author's articles studied | **PARTIAL** — two full texts read (IJNMF 2025, DOI 10.1108/HFF-04-2025-0254; Phys. Scr. 99 (2024) 025515). Composite Structures 2025, IJNMF 2026 and Scientific Reports 2026 were **not obtained**; no claim rests on them. |
| Style matrix produced | **MET** — `PAPER_A_ROUND14_AUTHOR_STYLE_AND_PRESENTATION_FAILURE_AUDIT.md` §3 |
| Section-by-section "how it differs and improves" | **MET** for six sections; the improvement claim for *rendered* readability is **UNPROVEN** (no PDF) |
| No copying | **MET** — no sentence, symbol or figure adopted from A1/A2; only structural habits |

## B. Structure

| Criterion | Judgement |
| --- | --- |
| Introduction one continuous section, no 1.1/1.2 | **MET** |
| Order: Introduction → Mathematical formulation → Solution of the problem → Numerical results and discussion → Conclusions | **MET** |
| Equations that belong in the formulation relocated rather than deleted | **MET** (three equations, §2.3) |
| Limitations preserved | **MET** (§4.15.5, corner flag, synthetic-parameter flag) |
| Results and discussion merged | **MET** |
| One authoritative `main.tex` | **MET** (guarded by the build script) |

## C. Mathematical derivation

| Criterion | Judgement |
| --- | --- |
| Dependency matrix before editing | **MET** — `PAPER_A_ROUND14_MATHEMATICAL_DERIVATION_MATRIX.md`, 23 rows |
| Real intermediate algebra for enthalpy → constitutives | **MET** (§2.3, with the Maxwell identity) |
| Balance laws derived rather than asserted | **MET** (§2.4, two integrations by parts, sign explained) |
| Harmonic substitution written out | **MET** (§2.8: operator table, six strain amplitudes, two strain-gradient amplitudes) |
| Spectral Galerkin → quartic matrix polynomial | **MET** as structure and degree (§2.8 and §3.1); closed-form entries **NOT CLAIMED** (flag F-1) |
| Edge system `B a = −b_inc` faithful to the solver | **MET** (statement matches `Plate.edge`; SVD cut-off and rank condition stated) |
| Exact `R_B` denominator | **MET** — both exponentials retained, denominator the incident power at the same plane |
| Limiting cases from tested controls | **MET** |
| No invented derivation | **MET** — anything not derivable is flagged, not written |

## D. Worked calculations and independent verification

| Criterion | Judgement |
| --- | --- |
| Formula → source values → result → interpretation | **MET** for the electric-model ratios, the non-dimensional groups, the quartic collapse and the parameter-equivalence table |
| Independent verification of each new derivation | **MET** — finite differences (7 identities, ≤7.4e-11), expansion identity (≤9.1e-13), exact collapse (0), parameter identity (bit-identical) |

## E. Figures

| Criterion | Judgement |
| --- | --- |
| All ten re-evaluated | **PARTIAL** — all ten re-rendered; F1, F2, F3, F10 inspected at full size, F4/F6/F7/F9 at contact-sheet scale, F5/F8 at contact-sheet scale only |
| Distinguishable palette, dash, marker | **MET** — family ramps are hue-separated; each member carries its own dash and marker; measured luminance steps reported (smallest 3.8 L*, covered by dash/marker, not claimed as luminance-safe) |
| No low-contrast pastel | **MET** |
| Overlap resolved by insets / difference panels / explicit statements | **MET** for F1 (inset relocated, −183.7 kHz readable), F2 (equivalence stated), F3 (headroom), F4 (zoom retained), F7 (relative-change panels); **NOT MET** for F5(c) and F8(c,d), whose annotation density is still high at column width |
| No zoom of floating-point noise | **MET** |
| F10 vectors and magnitudes preserved | **MET** — $k_B$ up-right at $+27.9^\circ$, $|k_B|/|k_i|=0.371$, $P_B$ down-left; test class passes |

## F. Results narration and captions

| Criterion | Judgement |
| --- | --- |
| Author-style narration (parameter varied, fixed quantities, panel, trend, real values, extrema, reason) | **MET** in the fourteen results subsections (unchanged from round 13, where the template repetition had already been removed) |
| Captions short, no file names, no test counts | **MET** — the validator finds no script, CSV, JSON or test-count string in the body or captions |

## G. Software content removed from the article

| Criterion | Judgement |
| --- | --- |
| Commands, filenames, versions, test counts, hashes out of the article | **MET** — appendix reduced 205 → 37 lines; the record is in `SUPPLEMENTARY_COMPUTATIONAL_REPRODUCIBILITY.md` |
| Method statements retained (degree, quadrature, convergence, conservation, data availability) | **MET** |

## H–I. Scientific integrity

| Criterion | Judgement |
| --- | --- |
| Constants, model, BCs, solver, root classification, peak, coupling results, normalisation, energy balance unchanged | **MET** — no producer or solver file changed; 52/52 tests pass on the shipped tree |
| Peak still reported as a **local** maximum of the declared window at 0.9467952 | **MET** |
| 94.68 % still the backward outgoing modal **self-power fraction** | **MET** |
| Novelty status | **UNRESOLVED** — closest work closed access |
| $\ell$, $f$, $H$ still declared synthetic | **MET** |
| Five `AUTHOR INPUT REQUIRED` declarations still visible | **MET** |
| Corner line force | **UNRESOLVED**, unchanged |
| Affected gates run, full battery not re-run | **MET** — and the round-11 battery is not re-claimed |
| LaTeX compiled and pages inspected | **NOT MET** — no TeX engine; **BUILD UNVERIFIED** |

## Overall

The manuscript now has the shape and the derivational content of a mathematical
research article in the author's idiom, a single continuous introduction, a
discussion that belongs to its results, and no software log inside it. It is
**not** a typeset paper: no page was ever rendered in this environment, several
figure annotations remain dense at column width, and three of the five author
papers could not be obtained. Those three sentences are the honest summary; any
of them being false would make the delivery dishonest.
