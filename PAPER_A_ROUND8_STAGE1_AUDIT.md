# Paper A — Round 8, Stage 1: independent audit before any edit

**Date:** 2026-11-06
**Scope:** the manuscript in `Paper_A_Final_Submission/`, its figures, and every script in
`paper_a_study/` that produces a quoted number.
**Method:** re-execution. No prior Arena "PASS" verdict, no stored JSON and no log file was treated as
evidence; every number below was recomputed in this round, on this tree, with
`numpy 2.4.6 / scipy 1.17.1 / matplotlib 3.11.2 / Python 3.11.2`.
**Edits in Stage 1:** none. Stage 1 produced this list only; the corrections are Stage 2 and are
recorded in `PAPER_A_ROUND8_MANUSCRIPT_CHANGES.md`.

---

## 1. What the audited object claims

The round-7 manuscript stated, in the abstract, the results section and the conclusions:

> along the acoustic branch the backward-propagating mode carries **93.19 %** of the incident power at
> **k_x d = 0.525**, where the group velocity passes through zero; at the operating point the share is
> **2.31 %**; switching the carrier–strain-gradient coupling on lowers the peak share by **33.1 %**.

The audit asked one question of each of those sentences: *is the quoted number the value of the quantity
the sentence names, computed the way the sentence says it is computed?* Five defects survived the question
and are listed below as D1–D5, with four supporting defects D6–D9 in the tooling that allowed them to
persist.

## 2. Defects proven in Stage 1

### D1 — the "maximum" was a coarse-grid sample

`build_figure_data.py::fig04` evaluated the branch on a raster of Δk_x d = 0.01 and the manuscript read
its largest sample as the maximum. The response is not resolved on that raster: at Δk_x d = 0.01 the two
samples nearest the top are 0.5200 (R_B = 0.8314), 0.5250 (0.9319) and 0.5300 (0.9200), and the true top
lies between them. Re-solving on a raster ten times finer and then a hundred times finer places the
extremum at **k_x d = 0.52752, R_B = 0.9467954**, i.e. **94.68 %**, with the top flat to 0.01 percentage
point over 0.5266 ≤ k_x d ≤ 0.5277.

The statement "93.19 % is the maximum" is therefore false in both directions: the value is low by 1.49
percentage points, and the abscissa 0.5250 is not the location of the extremum.

### D2 — the modal share depended on the plane at which it was read

`peak_identity_audit.py` rescaled the partition between reference planes with the backward attenuation
alone, `exp(α_B p.d)`. Both partner modes attenuate, in opposite directions, so the correct factor is the
**net** exponent `2(|Im k_ix| + |Im k_Bx|)`. With the backward-only factor the audit reported a 2.0 %
discrepancy between the planes and wrote a note calling it acceptable; with the net exponent the
rescaled values agree to **2.35 × 10⁻¹⁶**. The 2 % was not physics; it was a wrong exponent, and the note
that rationalised it was a false statement in a validation script.

### D3 — a canned note and a renormalised flux

Two fields of the same audit were not measurements at all:

* the correlation between the partition and the incident flux was written into the note as a fixed
  favourable value while the computed columns said otherwise. Recomputed on the hump window it is
  **r = −0.959** (anti-correlated, which is the honest zero-group-velocity signature, not the artefact-free
  claim the note made);
* `modal_power_incident_raw` reported **1.0** for every configuration, because the incident mode had been
  renormalised to unit power before the field was filled. The true incident modal power is 5.08 × 10⁻³ at
  the operating point and **3.97 × 10⁻⁵** at the maximum — a factor **128**. The abstract's silence about
  that factor, while quoting a 95 % share, was a direct consequence.

### D4 — `certify_peak.py` certified a value that was not the maximum

The script's case list contained `peak_candidate = 0.5250`, inherited from the coarse stage, and its
docstring described it as "the peak". A refinement study run at the wrong abscissa converges beautifully
and certifies nothing. The four fixed wavenumbers are now named for what they are, and the docstring
states explicitly that the script **certifies values and never searches**.

### D5 — a case-labelling guard was set so tight that it excluded the certified peak

`corner_assessment.py` rejected any case whose incident root differed from the requested wavenumber by
more than 1 × 10⁻⁶ relative. That guard exists to catch a case labelled with the *backward* target
(K_B = 0.2452, which sits 54–67 % away) instead of the incident wavenumber — the blunder that once
produced a plausible 0.5444. But at a zero-group-velocity fold the flat branch pushes the incident root
**7.36 × 10⁻⁴ (0.14 %)** away from the branch parameter, so the guard silently excluded the very
configuration under study. A guard that excludes the physics it is meant to protect is a defect.

### D6 — Fig. 4 did not show what its caption said

The figure was drawn from 110 rows on the coarse raster, with no panel that resolves the top, and its
caption described the largest plotted sample as the branch maximum. It also hardcoded a row count, which
made the caption wrong the moment the data changed.

### D7 — the discussion and conclusions carried the superseded numbers

93.19 %, 0.525, −33.1 % and the derived "11.5 points are propagation loss" appeared in
`discussion.tex` and `conclusions.tex`. The last of these is the most damaging: it compared a
reference-plane figure with an edge-plane figure, which is exactly the mixed-baseline comparison the
round-8 rules forbid.

### D8 — the verification tooling could not have caught D1–D4

* `run_all_checks.py` asserted **110 rows** for the Fig. 4 CSV and had no step that ran a peak search or a
  peak-identity audit at all;
* `claims.json` registered the superseded headline, so the registry agreed with the error;
* no test could detect a *nearby higher admissible value* — that is, the suite would pass on a tree whose
  "maximum" was beaten by a neighbouring sample.

### D9 — reproducible artefacts were undocumented

`peak_search.py` and `peak_identity_audit.py` were absent from the package table and from the command
list of `appendix_reproducibility.tex`, and the stated battery time (≈25 s) was an order of magnitude
below the truth.

## 3. What was *not* found defective (and was therefore left alone)

The audit explicitly re-tested and re-confirmed the following, and Stage 2 changed none of them:

| Item | Round-8 re-execution |
|---|---|
| Constitutive law ΔH = H_jkl Δn ε_jk,l, kept exactly as derived | unchanged in `model.py` |
| 2.5D Fourier-reduced formulation, spectral Galerkin edge matching | unchanged |
| Operating-point value R_B = 0.0231456 at k_x d = 0.7362 | reproduced, 4.1 × 10⁻¹¹ offset |
| 0.55 sample R_B = 0.5791801 | reproduced, 4.5 × 10⁻⁸ offset |
| Classical and strain-gradient exact limits, strong-form propagators | 26 tests, all pass |
| Power balance and admissibility flags | unchanged, every plotted row admissible |
| Figures 1–3, 5–10 | untouched |
| Material constants and their provenance | unchanged |

## 4. Consequence for Stage 2

Nine defects, all traceable to one root cause: **a number was named before it was computed**. The
correction is not a new number in the same sentence; it is a different construction — a search that is
classified rather than named, an audit that measures rather than asserts, and a test suite that fails if a
sample is promoted to a maximum. That construction is described in
`PAPER_A_ROUND8_PEAK_CERTIFICATION.md` and `PAPER_A_ROUND8_ARTEFACT_AUDIT.md`.

**Stage 1 verdict: 9 defects proven; 0 edits made.**
