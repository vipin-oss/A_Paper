# Paper A — Round 9: claims and manuscript audit

**Gates:** `paper_a_study/claim_audit.py` — **PASS**, 22 claims, 45 tokens, 5 deprecated values
guarded, 9 source-agreement rows (9 passing), figure first-citation order 1…10.
Record: `paper_a_study/figure_data/claim_audit.json` (`verdict: PASS`, 45 rows).

Every number in the manuscript that the correction could have moved was treated as a claim to be
re-derived from the regenerated record, not adjusted by eye. Each occurrence was classified as
**CORRECT**, **STALE** (the regenerated data behind it changed), **ROUNDING** (same value, different
printed precision) or **UNVERIFIED** (no stored source — not kept).

---

## 1. The registry

| group | claims |
|---|---|
| headline and its neighbours | `R_B_certified_maximum` 0.9467952, `R_B_at_located_argmax` 0.9467954, `R_B_operating_point` 0.0231456, `R_B_earlier_sample` 0.9318915, `R_B_k055_sample` 0.5791801 |
| **edge plane (new this round)** | `R_B_edge_certified_maximum` 0.9856, `R_B_edge_operating_point` 0.0232, `R_B_edge_k055` 0.5802 |
| coupling | `coupling_change_operating` 1.21 %, `coupling_change_peak` 34.2 %, `coupling_change_peak_edge_plane` 11.1 %, `coupling_change_k055_edge_plane` 2.007 %, `coupling_change_k055_reference_plane` −9.85 % |
| stability | `degree_stability_peak` 5.0e-9, `quadrature_stability_peak` 5.6e-9, `reference_plane_closure` 2e-16 |
| physical context | `attenuation_peak_backward` 87.1 dB/mm, `wavenumber_ratio_peak` 0.996, `incident_wavenumber_peak` 0.5282, `incident_power_ratio_fold` 128, `total_outgoing_peak` 0.99769, `total_outgoing_operating` 0.9998 |

The three edge-plane claims did not exist in round 8. That gap is why the defect survived: nothing
compared the edge-plane number any script produced with the number the text quoted.

---

## 2. Manuscript edits, each with its classification

| # | site | round-8 text | round-9 text | class | source |
|---|---|---|---|---|---|
| 1 | `results.tex` Table 5 (edge-plane row) | 0.0231 | **0.0232** | ROUNDING | `mechanism_controls.json → operating_point/no_coupling/R_B_edge = 0.023150542` |
| 2 | `results.tex` §4.2 (degree spread) | 5.6e-9 | **5.0e-9** | STALE | `peak_search.json → degree_spread["0.52752"] = 4.973e-9` |
| 3 | `results.tex` §4.2 (spread at the reported wavenumber) | 6.2e-9 | **7.3e-9** | STALE | `degree_spread["0.52750"] = 7.281e-9` |
| 4 | `results.tex` §4.2 (quadrature spread) | 9.4e-10 | **5.6e-9** | STALE | `quadrature_spread = 5.591e-9` |
| 5 | `results.tex` Table 3, certified-maximum cell | 1.7e-9 | **3.8e-9** | STALE | `peak_certification.json`, degrees 18–30 |
| 6 | `results.tex` Table 3, earlier-sample cell | 2.1e-8 | **2.3e-8** | STALE | same record |
| 7 | `results.tex` §4.6 (reproduction across degrees/quadrature) | 5.6e-9 / 9.4e-10 | **5.0e-9 / 5.6e-9** | STALE | as #2, #4 |
| 8 | `results.tex` §4.6 (what the stability does not mean) | 6e-9 | **1e-8** | CONSERVATIVE | both spreads quoted above |
| 9 | `conclusions.tex` (degree spread) | 5.6e-9 | **5.0e-9** | STALE | as #2 |
| 10 | `results.tex` §4.5 (plane of the edge value) | “reference plane moved from 5 to 20” | **“from 0 to 20 thicknesses”**, plus one sentence that the transform is implemented once and the stored shares are reproduced to 1e-10 | CORRECTED | `peak_identity_audit.json → reference_plane.rows`, which now includes `L = 0` |
| 11 | `results.tex` §5.1 (round-off digits) | 3.4e-16, 7.3e-13, 3.2e-13 | **1.9e-17, 6.6e-13, 3.0e-13** | STALE | `fig05_channel_power.csv` (H = 0); `mechanism_controls.json → refined_peak/full` |
| 12 | `results.tex` §5.3 (0.55 comparison) | 2.0 % / −9.9 % | **2.01 % / −9.85 %** | ROUNDING | registry values 2.007 / −9.85 |
| 13 | `results.tex` §5.5 (Fig. 9 panels) | “both fall from 3e-6 and 4e-12 at n = 14 … both remain at 1e-12–1e-13, four to five orders below 1e-8 and 1e-10” | rewritten: channel error 3e-6 → 1e-7, wavenumber at the 1e-12 floor, residual 3e-15, balance 2e-13…1e-12, **six to seven** and **two to three** orders below the two tolerances | STALE + CORRECTED (the round-8 sentence was also wrong about the residual, which is 3e-15, not 1e-12) | `fig09_validation_convergence.csv` |
| 14 | `numerical_methods.tex` §3.4 | 26 tests | **39 tests**, plus a paragraph on the shared transform and the three new tests | STALE (count) + NEW | `test_model.py` |
| 15 | `appendix_reproducibility.tex` | 26 checks, `# 26 tests, ~14 s` | **39 checks**, `# 39 tests, ~9 s` | STALE | measured |

Nothing else in the text was touched. In particular the abstract, the 94.68 % headline, the
`certified_local_maximum` wording, the novelty paragraph, the synthetic-parameter statements and the
corner-line caveat are unchanged from round 8.

---

## 3. The six numbers that needed a decision, not an edit

**3.1 The degree and quadrature spreads are larger than they were.** The old values (5.6e-9, 9.4e-10)
were produced by a search whose edge-plane column was wrong; the new ones (5.0e-9, 5.6e-9) come from
the corrected transform. The values were re-read, not tuned, and the registry tolerance is 20 % because
the spread itself is a difference of two nearly equal numbers. Between degrees 14 and 34 the maximum
still moves by less than 1e-8 relative, so the conclusion — the number is converged — is unchanged.

**3.2 0.0231 or 0.0232?** The stored value is 0.023150542. Rounded to four decimals that is 0.0232.
The table had been filled from a truncated intermediate, which is why it read 0.0231. The cell now reads
0.0232 and the registry tolerance for all three four-decimal edge shares is 5e-3 — a four-decimal share
cannot be checked more tightly than its own rounding, and pretending otherwise would produce a gate
that fails for arithmetic reasons.

**3.3 The Fig. 9 paragraph was wrong about more than the digits.** The round-8 sentence said both panel
(c) curves stay at 1e-12–1e-13 and sit “four to five orders” below the tolerances. The record says the
scaled residual is 3e-15 (six to seven orders below 1e-8) and the energy balance is 2e-13…1e-12 (two to
three orders below 1e-10). The sentence was rewritten from the CSV. This is the one place where the
audit found the *prose* wrong rather than only the digits.

**3.4 Round-off digits are not claims.** 3.4e-16, 7.3e-13 and 3.2e-13 were printed from a single run of
a quantity whose value is hardware- and order-dependent. They are updated to the current run and are
described in the text as the solver's own balance at the round-off level, not as accuracy.

**3.5 The 2.0 % and −9.9 % pair at `k_x d = 0.55`.** Measured 2.007 % (edge plane) and −9.85 %
(reference plane). They are printed as 2.01 % and −9.85 % so that the same quantity is not printed with
two different precisions in two places. The three-way distinction the manuscript makes — absolute pp
difference, relative change, difference of relative changes at different planes — is untouched.

**3.6 The `4.4e-6` reactive share at the edge plane.** Not stored in any record, so it was
**re-computed** this round rather than carried forward: a direct solve of the reference configuration at
`L = 0` gives an evanescent reactive fraction of **4.445813e-6**, which is the quoted 4.4e-6. The value
is correct; it is now reproducible on demand rather than asserted.

---

## 4. What the registry does not cover

Stated so that the gate is not mistaken for a proof:

* numbers quoted at one or two significant figures in the discussion (e.g. “a factor of sixty-two”,
  “1.0e-3 to 8.5e-3 per unit thickness”) are checked for stale values but not re-derived by the gate;
* the Fig. 10 field metrics and the corner-line band numbers are covered by their own scripts
  (`corner_assessment.py`, `fig10_field_metrics.json`), not by this registry;
* the LaTeX build is not covered by anything: no engine is available. `static_check.py` validates
  labels, references, environments, citation keys, fragile moving arguments and figure order, and
  nothing else.

---

## 5. Verdict

* registry and text agree: **PASS**;
* every edge-plane number in the manuscript traces to a stored record: **yes** (three new claims, three
  source-agreement rows);
* any stale or superseded number remaining in the text: **none found**;
* any number quoted without a source: **none** (the one candidate, 4.4e-6, was re-derived);
* figure order, citation keys and moving arguments: **clean**.
