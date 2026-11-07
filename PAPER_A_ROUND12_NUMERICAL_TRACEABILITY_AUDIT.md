# Paper A — round 12: numerical traceability audit

**Scope.** Every number in the manuscript was traced to a stored record, or marked
as untraceable. No dataset was regenerated, no solver file was touched, and no
figure was re-rendered: this round audits the delivered records against the prose
and nothing else.

Baseline `75d86dc9710d69e2100a85fa5c8b56e9681f7744`. Records are under
`paper_a_study/figure_data/`.

## Summary

| class | count | meaning |
|---|---|---|
| MATCH | 61 | the printed number equals the stored value at the printed precision |
| CORRECTED | 20 printed numbers in 19 ledger rows | the printed number disagreed with the stored value; corrected in this round (L12-01…L12-18) |
| UNSUPPORTED, REMOVED | 2 | the claim had no stored source and is contradicted by a direct evaluation (L12-07, L12-08) |
| UNVERIFIED | 3 | outside the delivered records: the typeset build, the prior-art comparison, the pointwise corner field |
| BLOCKED | 1 | a frozen figure draws a vector the prose can no longer support (B1) |

Nothing in the MATCH class changed. The 19 corrections and the 2 removals are all in
the prose; the records and the figures are untouched.

---

## 1. Headline numbers (all MATCH)

| manuscript | stored | where |
|---|---|---|
| $R_B=0.0231456$ at the operating point | 0.0231456192 | `peak_certification.json` `verdict.operating_point.R_B_finest` |
| $R_B=0.9467952$ at $k_xd=0.5275$ | 0.9467952306 | `peak_search.json` `classification.R_B_reported` |
| $R_B=0.9467954$ at $k_xd=0.52752$ | 0.9467953678 | `peak_search.json` `classification.R_B_at_max` |
| $R_B=0.931891$ at $k_xd=0.5250$ | 0.9318914859 | `peak_certification.json` `verdict.round7_sample.R_B_finest` |
| $R_B=0.579180$ at $k_xd=0.5500$ | 0.5791800586 | `peak_certification.json` `verdict.k055_sample.R_B_finest` |
| 16.684 GHz operating point | 16.684123 | `peak_certification.json` `rows[case=operating_point]` |
| 16.6547 GHz at the maximum | 16.65467 | `peak_search.json` `degree[K=0.5275]` |
| 0.99980 / 0.99769 total outgoing | 0.9997973117 / 0.9976849787 | `fig05_channel_power.csv`, `peak_certification.json` |
| $94.68\%$ modal share | 0.9467952 | as above; also 5 of 5 `tokens` in `claims.json` |
| $0.9856$ edge-plane share at the maximum | 0.9855722004 | `peak_identity_audit.json` `reference_plane.rows[L=0]` |
| $0.0232$ and $0.5802$ edge-plane shares | 0.0231505 / 0.5802414 | `mechanism_controls.json` `no_coupling.R_B_edge` |
| $1.4\times10^{-7}$ argmax offset | 1.372140e−07 | `classification.offset_reported_vs_argmax` |
| $8.4\times10^{-6}$ below the refined maximum | 8.361658e−06 | `classification.gain_over_coarse`, `verdict.restart_spread` |
| plateau intervals $[0.5266,0.5277]$, $[0.5265,0.5281]$, half-width $\pm0.0009$ | 0.5266–0.5277, 0.5265–0.5281, 0.00092 | `classification.plateau_*` |
| $5.61\times10^{-9}$ / $6.22\times10^{-9}$ degree spreads | 5.613409e−09 / 6.220088e−09 | `verdict.degree_spread` |
| $4.32\times10^{-10}$ quadrature spread | 4.317446e−10 | `verdict.quadrature_spread` |
| three tracking paths identical | 0.0 | `verdict.tracking_path_relative_spread` |
| factor 128 incident-flux drop | 127.94 (0.005075081 / 3.966976e−05) | `peak_identity_audit.json` `cases.*.modal_power_incident_raw` |
| overlap 0.999995, separation $1.45$ decay rates, second candidate $2.0|k_x|$ away | 0.9999949939, 1.448063, 2.003996 | `peak_identity_audit.json` `cases.peak.*` |
| condition number $1.6\times10^{2}$ (production degree) and $\le1.9\times10^{2}$ (refinement set) | 160.47 (degree 22), 185.86 (degree 30) | `peak_identity_audit.json`, `peak_certification.json` |
| scaled edge residual $\le3\times10^{-15}$ | max 2.92e−15 | `peak_certification.json` |
| projection error bound $4\times10^{-14}$ | 3.563374e−14 | `peak_identity_audit.json` `verdict.relative_error_bound` |
| reference-plane spread $2\times10^{-16}$ | 0.0 (row-to-row) | `reference_plane.rows`, `verdict.reference_plane_spread` |
| 99.77 % leaves as propagating modes | 0.99769 | `peak_certification.json` |

## 2. Coupling and control numbers (all MATCH)

| manuscript | stored | where |
|---|---|---|
| $+1.21\%$ at the operating point, $+34.2\%$ at the maximum, $+9.85\%$ at $k_xd=0.55$ | 1.21, 34.2, −9.85 | `mechanism_controls.json`, `branch_consistent_H_sweep` |
| $11.1\%$ at the edge plane, $23.1$ points of propagation loss | 11.1 (0.876125/0.985572), 23.1 | same |
| $+2.01\%$ at the edge plane at $k_xd=0.55$ | 2.007 | same, `k055_sample` edge shares |
| $R_B=0.9468, 0.7711, 0.6230$ and $0.8636, 0.7006$ | 0.9467952, 0.7710907, 0.6229733, 0.8636…, 0.7006… | same |
| re-searched argmax $0.5218, 0.5248, 0.5275, 0.5261, 0.5309$; ceilings $0.6244$, $0.7013$ | 0.5218 / 0.6243892; 0.5309 / 0.7013 | `reoptimised_peak` |
| flexoelectric contribution $-0.012\%$, $-0.009\%$, $0.0004\%$ | −0.0120, −0.0088, 0.0004 | `full` vs `no_flexo`, three cases |
| $183.7$ kHz and $1.1\times10^{-5}$ dispersion shift; $92$ kHz for the negative coupling | 183.71 kHz; 1.09e−5 | `claims.json` `coupling_frequency_shift_max`, `fig01…csv` |
| attenuation at the maximum rises $1.0\to8.5\times10^{-3}$ per thickness | 1.004e−03 → 8.531e−03 | `mechanism_controls.json` `refined_peak.full.backward_K`, `tab:configurations` |

## 3. Sweeps (MATCH except where a ledger row says otherwise)

| panel | claim | stored | verdict |
|---|---|---|---|
| fig01(a) | five curves within the linewidth; max shift 184 kHz at $k_xd=1.05$; 92 kHz negative | 183.71 / 91.7 kHz | MATCH |
| fig01(b) | $v_p$ 105.8 → 20.0 km/s; $v_g/v_E$ −188/−189 → +1097/+1136 m/s; sign change just below 0.53 | 105.771 → 20.038; −187.8/−188.7 → +1097/+1136; sign change between 0.510 and 0.540 | MATCH of values, **abscissae corrected** (L12-01) |
| fig01(b) | $v_g$–$v_E$ agreement 3.5 % except the lowest sample 6.4 % | 3.55 % excluding $k_xd=0.15$; 6.45 % there | MATCH |
| fig01(c) | linewidth 1.4 kHz – 0.27 MHz, monotone in $k_xd$ | 0.00139 – 0.2662 MHz, monotone | MATCH; the "ordering in $H$" claim corrected (L12-02) |
| fig01(d) | attenuation 0.23 – 456 dB/mm, positive everywhere | 0.226 – 455.7 dB/mm | MATCH; the peak abscissa corrected (L12-02) |
| fig02 | density 1→3 ×10¹⁸ raises linewidth and attenuation | ×3.0 and ×3.0 | **corrected** from ×9 and ×10 (L12-05) |
| fig02 | mobility factor-of-three change moves the linewidth | ×3.0, identical to the density sweep | **corrected** from ×5 (L12-05) |
| fig02 | $R_B$ independent of density to 0.2 %; maximum 0.5796 at 0.55 | 0.14 % spread; 0.57959 | MATCH |
| fig02 | panel (c) tail "falls to $10^{-7}$ at 0.9" | 3.04e−07 at 0.80, 1.55e−11 at 0.90 | **corrected** (L12-06) |
| fig03 | thickness family 30.4 → 10.5 GHz | 28.34–30.43 (120 nm), 10.46–10.74 (320 nm) | MATCH of the numbers; wording corrected (L12-03) |
| fig03 | $\ell=90$: +2.0 % and +10.2 %; $\ell=35$: −1.9 % and −4.9 % | +2.05/+10.21, −1.93/−4.93 at 0.145 and 1.000 | MATCH; **abscissae corrected** from 0.15/1.05 (L12-04) |
| fig04 | 0.0399 at 0.30 (16.676 GHz), 0.9468 at 0.5275, 0.0173 at 0.75 (16.688 GHz) | 0.039924 (16.6759), 0.946795 (16.6547), 0.017290 (16.6884) | MATCH |
| fig04 | ratio 0.9960; angle span 16°; $v_g$ −180/+355; $\lvert v_g\rvert<1$ m/s at the fold | 0.996017; 16.23°; −180.4/+355.4; 0.26 | MATCH |
| fig06 | survival minimum 0.0356 at 1000 µm; 18.5 → 0.30 mm; 62× | 0.03564; 18.5 → 0.30; 61.7 | MATCH; the "factor of three" clause corrected (L12-11) |
| fig06 | 0.469/0.454 at $H=0$; 16.2/23.0 at −0.05; 0.47 and 29 dB/mm extremes | 0.469/0.454; 16.15/23.04; 0.469/28.96 | MATCH |
| fig07 | $R_B$ 0.01896–0.02560; $k_y$ factor 1.35; $H$ effect ≤2.44 % | 0.01896/0.02560; 1.3502; 2.442 % | MATCH |
| fig08 | $\pm0.0367$ and $\pm0.0317$ across the thickness | −0.0367 / +0.0317 | MATCH |
| fig09(a),(b) | channel error 3×10⁻⁶ at $n=14$ → 10⁻⁷; wavenumber error at the 10⁻¹² floor | as printed in `fig09_validation_convergence.csv` | MATCH |
| fig09(c) | residual 3×10⁻¹⁵; balance "between 2×10⁻¹³ and 10⁻¹²" | `edge_scaled_residual` 2.66e−15…3.28e−15; `power_error` 2.41e−15, 2.40e−13, 6.40e−13, 7.31e−13, 9.90e−13, 3.98e−12, 4.14e−12 | residual MATCH; the balance range **corrected** (L12-13) |
| fig09(d) | temporal and spatial routes agree to 2×10⁻⁵ | 1.99e−05 | MATCH |
| fig10 | incident 10.0°, backward 27.9°; $P_B\propto(-1,-0.530)$ | 10.0000°, −27.8997°, (−0.015425, −0.008167) | MATCH |
| fig10 | $\vect{k}_B\propto(0.333,-0.530)$ | (0.24517, +0.12981) → $(1,0.5295)$ | **corrected** (L12-14); the drawn arrow remains wrong (**B1**) |

## 4. Structural and apparatus numbers

| manuscript | stored / measured | verdict |
|---|---|---|
| "the 39 automated checks", "39 tests, ~9 s" | `Ran 47 tests in 22.911s … OK` (this round) | **corrected** to 47 and ~25 s (L12-18) |
| "the twelve data files behind the figures" | 11 CSVs in `figure_data/` (plus 17 JSON records) | **corrected** (L12-18) |
| "Five limitations" | six paragraphs | **corrected** (L12-17) |
| "three-term polynomial" | degree 4, five coefficients | **corrected** (L12-15) |
| the five dimensionless groups: $Q=0.0746$, $\alpha_{\mathrm{d}}=0.828$, $\lambda=0.250$, $f=2.56\times10^{-3}$, $h=\eta\times0.212$ | recomputed from `a0/materials.json`: $d/L_D=7.46\times10^{-2}$, $D/(dc_s)=8.28\times10^{-1}$, $\ell/d=0.250$, $f_{3zz}/(d\sqrt{c_{44}\kappa_{33}})=2.56\times10^{-3}$, $H^{*}/(d\sqrt{ac_{44}})=0.212$ | MATCH |
| $H^{*}=H_{\text{bound}}/\sqrt5=4.01\times10^{-22}$ J m, $H_{\text{bound}}=8.97\times10^{-22}$, $H_{\text{ref}}=1.89\times10^{-21}$, $c^{*}=154.4$ GPa, $s\le5\times10^{-4}$ | recomputed from the material file and eqs. (schur) | MATCH |
| 13 citations / 13 bib entries / 104 labels / 75 references | `static_check.py` | MATCH |

## 5. The one claim that could not be traced — and what replaced it

The manuscript said, in §3.5:

> "a relative change of $1.8\times10^{-12}$ in the frequency moves $R_B$ by
> $5.6\times10^{-6}$. The maximum is therefore reproducible to about
> $\pm6\times10^{-6}$."

Neither $1.8\times10^{-12}$ nor $5.6\times10^{-6}$ occurs in any delivered record.
`peak_search.json` stores no frequency perturbation, `claims.json` registers none,
and no report of rounds 7–11 records the pair. The claim was therefore tested
directly, by evaluating the same configuration at perturbed frequencies, at
$H=0$, $k_yd=0.1298118$, $k_xd=0.5275$, degree 22, $\omega=7.619899227279142$:

| $\delta\omega/\omega$ | $\delta R_B/R_B$ | amplification $\lvert\delta R_B/R_B\rvert/\lvert\delta\omega/\omega\rvert$ |
|---|---|---|
| $-10^{-12}$ | $-8.57\times10^{-10}$ | $8.6\times10^{2}$ |
| $-10^{-11}$ | $-9.82\times10^{-9}$ | $9.8\times10^{2}$ |
| $-10^{-10}$ | $-1.04\times10^{-7}$ | $1.0\times10^{3}$ |
| $-10^{-9}$ | $-2.23\times10^{-6}$ | $2.2\times10^{3}$ |
| $+10^{-12}$ | $+7.45\times10^{-10}$ | $7.5\times10^{2}$ |
| $+10^{-11}$ | $+9.48\times10^{-9}$ | $9.5\times10^{2}$ |
| $+10^{-10}$ | $+7.80\times10^{-8}$ | $7.8\times10^{2}$ |
| $+10^{-9}$ | $-4.08\times10^{-7}$ | sign reverses; no longer linear |
| $+10^{-8}$ | $-1.21\times10^{-4}$ | sign reverses; no longer linear |

The measured amplification is of order $10^{3}$ near $10^{-12}$, not
$3.1\times10^{6}$: a $1.8\times10^{-12}$ relative frequency change moves $R_B$ by
about $1.5\times10^{-9}$, i.e. three orders of magnitude less than the printed
$5.6\times10^{-6}$. The printed pair is therefore wrong by roughly three orders of
magnitude, and the sentence that depended on it — "reproducible to
$\pm6\times10^{-6}$" — was three orders too pessimistic in its bound while being
wrong in its mechanism.

Both the pair and the bound were removed (L12-07, L12-08) rather than re-estimated:
a number whose only source would be a review-time run does not belong in a
manuscript whose datasets are shipped. What replaces them is a statement built
entirely from registered spreads (degree, quadrature, tracking path) plus the
offset between the two abscissae, which is what a reader can verify from the
archive. The measurement above is recorded here so that the decision is auditable.

Nothing downstream moved: the printed digits of $R_B$ are unchanged, the headline
is unchanged, and the two other stability statements of the paper (degree and
quadrature) were already independent of this pair.

## 6. What this audit did not do

* No dataset was regenerated; the audit compares prose with the committed records.
  The round-11 battery (`18 PASS / 0 FAIL / 1 SKIP`, `OVERALL: PASS`) remains the
  last full-execution evidence, and this round did not repeat it because it touches
  no producer (`PAPER_A_ROUND12_READINESS_ASSESSMENT.md` §1).
* The prior-art comparison was not re-attempted; the source is closed access and
  the status remains **UNRESOLVED**.
* No figure was re-rendered, so the frozen panels are audited as they are; the one
  panel whose drawing disagrees with the corrected prose is **B1**.
