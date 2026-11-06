# Paper A — Round 8: what changed in the manuscript, and why

Rule applied: **only defects proven in Stage 1 were corrected** (`PAPER_A_ROUND8_STAGE1_AUDIT.md`,
D1–D9). Everything else was left exactly as it was, including text that could be improved but was not
proven wrong.

---

## 1. Abstract (`main.tex`)

| round 7 | round 8 | defect |
|---|---|---|
| "the share reaches 93.19 % at k_xd = 0.525" | "rises to a maximum of 94.68 % at k_xd = 0.5275 (16.6547 GHz), where the incident and backward wavenumbers differ by 0.4 % and the group velocity is below 1 m/s" | D1 |
| — (no statement about the maximum's status) | "The maximum is a certified local extremum, flat to 0.01 percentage point over 0.5266 ≤ k_xd ≤ 0.5277, and a modal share" | D1 |
| "99.0 % of the incident power leaves" | "99.77 % of the incident power leaves as propagating modes, although the incident flux at the fold is a factor 128 smaller than at the operating point" | D2, D3 |
| "lowers the share by 33.1 % at the maximum" | "by 34.2 % at the maximum" | D7 |

Length: ≈229 words (was 213). The added words are the two honesty clauses: *certified local extremum*
and *the incident flux is 128 times smaller there*.

## 2. Results (`sections/results.tex`)

1. **Sweep paragraph** rewritten: the maximum is at 0.5275, where v_g → 0, the backward wavenumber
   approaches the incident one to within 0.4 %, and the near-parallel geometry is why the edge condition
   needs only a small admixture of other modes. Panel (c) is cited for the collapse in k_Bx/k_ix. (D1)
2. **Second half of the mechanism added:** at the fold the incident mode is nearly cut off and its flux
   falls by a factor 128, so "a maximal share coexists with a minimal transported power". (D2, D3)
3. **Fig. 4 caption** rewritten for the new figure: no hardcoded row count, both rasters named, the inset
   and the collapse described. (D6)
4. **`tab:refinement`** now has four rows — operating point, certified maximum, the earlier 0.5250 sample
   (kept deliberately), 0.55 — with the max relative change over degrees 18–30. (D4)
5. **New §"Certification of the maximum"** (`sec:results_certification`): the objective defined before the
   search, the three-stage raster, the flat top, the classification, the restarts, and the explicit
   statement that the maximum is local and that the classification lives with the data. (D1, D4)
6. **New §"Why the high fraction is not an artefact"** (`sec:results_artefact`): vanishing denominator,
   branch ambiguity, near-degenerate decomposition, and the "what it is not" paragraph. (D2, D3)
7. **Energy budget at the peak** added to the results text: total outgoing 0.99769, cross −2.29 × 10⁻³,
   dissipation 2.32 × 10⁻⁵, edge-plane share 0.98557 quoted beside — never instead of — the
   reference-plane 0.94680.
8. **`tab:configurations`** rebuilt with the certified maximum as its second column (k_x 0.5275,
   Re k_ix 0.5282, v_g 0.45 m/s, attenuation 87.2 / 87.1 dB mm⁻¹, R_B 0.9467952, edge share 0.9856,
   θ_E −13.85°, total outgoing 0.99769, cross −2.29 × 10⁻³, diss 2.32 × 10⁻⁵).
9. **`tab:controls`** peak column updated to the certified maximum (0.622973 / 0.622971 / 0.946795 /
   0.946801 / 0.134050).
10. **Coupling paragraph:** 33.1 % → 34.2 % (D7).
11. Two arithmetic corrections found while writing 5 and 6: the argmax–reported difference is
    1.4 × 10⁻⁷ (not 10⁻⁶), and the location is determined to the half-width of the flat top (±0.0009),
    not ±0.0003.
12. The restart sentence now says what the restarts actually test (bracketing; 8.4 × 10⁻⁶ below the
    refined maximum) instead of claiming that they return the same top.

## 3. Discussion (`sections/discussion.tex`)

* 93.19 % → 94.68 %, 5.81 % → 5.09 %, 0.99000 → 0.99769. (D7)
* The slow-mode paragraph was rebuilt around the **near-parallel wavenumbers** rather than a vague
  "more time to interact", and now names the 128-fold flux reduction as a limit on the reading. (D1, D3)
* 33.1 % → 34.2 % in three places; the edge-plane comparison now reads 11.1 % vs 34.2 %, so **23.1 points**
  (not 11.5) are propagation loss — the previous pair mixed a reference-plane figure with an edge-plane
  figure, which the round-8 rules forbid. (D7)
* One sentence added on the re-optimised peaks: the ceiling falls to 0.6244 / 0.7013 and the displacement
  is not monotone in sign(H).
* Corner-band paragraph extended to three configurations (operating, certified maximum, 0.55) with the
  measured shares, peak/mean ratios and degree drift.

## 4. Conclusions (`sections/conclusions.tex`)

* "93.19 % at 0.525" → "a certified maximum of 94.68 % at 0.5275 (16.6547 GHz), where the group velocity
  vanishes and the backward wavenumber approaches the incident one to within 0.4 %; stable to
  5.6 × 10⁻⁹ between degrees 14 and 34 and not claimed as a global maximum". (D1)
* "99.0 %" → "99.77 % at the maximum, where the incident flux itself has fallen by a factor 128, so a
  maximal share coexists with a minimal transported power". (D3)
* "33.1 % … of which 11.5 points are added propagation loss" → "34.2 % … of which 23.1 points … when the
  two configurations are compared at the edge plane; re-searched at each coupling level, the extremum
  shifts and its ceiling falls". (D7)

## 5. Introduction (`sections/introduction.tex`)

One phrase only: "by a third at the branch maximum" → "by a third at the certified maximum". The
introduction's numbers (one per cent / a third) remain correct.

## 6. Numerical methods (`sections/numerical_methods.tex`)

* 22 → **26** tests.
* One paragraph added describing the four new peak tests: the coarse-raster test, the incident-root test,
  the reference-plane exponent test, and the stored-classification test — all written as solver
  evaluations rather than stored expectations. (D8)

## 7. Appendix (`sections/appendix_reproducibility.tex`)

* Package table: added `peak_search.py` and `peak_identity_audit.py`; `certify_peak.py` re-described as
  certifying four fixed wavenumbers and **never searching**; test count 22 → 26. (D4, D9)
* Command list: added the two new scripts with their run times; battery time ≈25 s → ≈15 min; test time
  9 s → 14 s; `certify_peak.py` 4 min → 30 s. (D9)
* One sentence on the ordering dependencies (the identity audit and the claim audit read the records
  written by the search and the certification).

## 8. Figure 4

Regenerated only. 2 × 2 panels, 139 rows, inset over the top, star at the maximum, dashed line at the
group-velocity zero. No other figure was touched, and no other figure's data was recomputed.

## 9. What was deliberately *not* changed

| not changed | reason |
|---|---|
| constitutive law, 2.5D Fourier reduction, spectral Galerkin matching | re-verified, not defective |
| operating-point value 0.0231456 | re-verified to 4 × 10⁻¹¹ |
| the 0.55 sample 0.5791801 | re-verified to 5 × 10⁻⁸ |
| the 0.5250 sample itself (still tabulated) | converged; kept so the correction is auditable |
| Figs. 1–3, 5–10 and their CSVs | unaffected by D1–D5 |
| the limitation statements (synthetic material, corner line) | still true |
| reference list | no new primary source was accessed this round; no citation was inferred |

**Build status: BUILD UNVERIFIED.** No TeX engine exists in this environment. The static validator passes
(`Paper_A_Final_Submission/static_validation.txt`), which checks labels, references, environments and
citation keys, but it is not a compile.
