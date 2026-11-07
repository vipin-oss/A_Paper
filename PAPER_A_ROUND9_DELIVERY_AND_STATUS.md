# Paper A — Round 9: delivery and status

**Branch:** `arena/ea7ca4dd-a-paper`. **Round-8 baseline:** `081cc8e5c2f887c084de4992a856c9aedf335c45`.
**Verification:** 39 tests OK · 18/18 gates PASS · 22 claims / 45 tokens PASS · 13/13 mutants CAUGHT ·
LaTeX build **UNVERIFIED** (no engine).

---

## 1. What round 9 was, and what it did

Round 9 was a correction round, not a research round. The Stage-1 audit
(`PAPER_A_ROUND9_STAGE1_NORMALIZATION_AUDIT.md`) found that three call sites moved a modal-power
**ratio** between planes with the **single-mode absolute decay**, omitting the incident attenuation.
The two-mode ratio requires `2(|Im K_i| + |Im K_B|)`, not `2|Im K_B|`.

Repaired; every affected record regenerated; three gates added so the defect cannot return; the
manuscript re-read against the regenerated data. The reference-plane headline `0.9467952` was never
produced by the defective code and is unchanged.

| what | where |
|---|---|
| the defect, derived and reproduced before any edit | `PAPER_A_ROUND9_STAGE1_NORMALIZATION_AUDIT.md` |
| every edit, old → new, and what was deliberately left alone | `PAPER_A_ROUND9_CORRECTION_HISTORY.md` |
| five planes, one reconstructed value (2.345e-16 spread) | `PAPER_A_ROUND9_PLANE_INVARIANCE_VALIDATION.md` |
| 13 injected defects, 13 caught, by which gate | `PAPER_A_ROUND9_MUTATION_REPORT.md` |
| 22 claims, 45 tokens, every re-read number classified | `PAPER_A_ROUND9_CLAIMS_AND_MANUSCRIPT_AUDIT.md` |
| 39 tests, 18 gates, and what they do not establish | `PAPER_A_ROUND9_TEST_RESULTS.md` |

---

## 2. The deliverable

* **Manuscript:** `Paper_A_Final_Submission/` — `main.tex`, seven section files, ten vector PDF
  figures, `references.bib`, `MANIFEST.json` (79 files, 2.76 MB), `static_validation.txt`.
* **Data:** `paper_a_study/figure_data/` — all 13 figure datasets regenerated from the corrected
  sources, plus the search, certification, identity, matched-control, convergence, quadrature,
  dimension and claim records.
* **Code:** `paper_a_study/` — solver, figure builder, audit scripts, 39-test suite, claim registry
  and mutation harness.
* **Reports:** the seven `PAPER_A_ROUND9_*.md` files, plus `PAPER_A_CORRECTION_HISTORY.md`
  (cumulative correction history, round-9 addendum at the end).
* **Archive:** `downloads/Paper_A_Complete_Project_round9.zip`. Its size and SHA-256 are in
  `downloads/PACKAGE_SHA256.txt` and `downloads/README.md`, which sit **beside** the archive: a
  checksum cannot be embedded in the file it describes, and this report is inside the archive, so it
  does not carry the digest either.

**Figures.** All ten were re-rendered from the regenerated data, because the CSVs ship with the
package and would otherwise contain a column that contradicts the corrected transform. No panel plots
`R_B_edge`; a pixel comparison against the committed exports shows no visible change, except in
Fig. 5(c,d) and Fig. 9(c,d), which plot round-off-level quantities on logarithmic axes and therefore
move within the 1e-12–1e-15 band they are there to document.

**Reproducibility of the delivery itself.** The whole dataset was generated twice from the same
sources during this round, the second time from a clean checkout. Both runs agree to the last stored
digit: `K_at_max = 0.52752`, `R_B_at_max = 0.9467953685099261`, degree-22 edge share
0.9855721942926737, `degree_spread = 4.973e-9 / 7.281e-9`, `quadrature_spread = 5.591e-9`. Nothing in
this delivery is a single unrepeatable run.

---

## 3. What a reader can verify without re-running anything

| question | where the answer is stored |
|---|---|
| Is the maximum a maximum? | `peak_search.json → classification` (`certified_local_maximum`, flat top, scanned domain) |
| Could it be an artefact? | `peak_identity_audit.json → verdict` (`artefact: false`; plane spread 2.3e-16; bound cond×ε 3.6e-14) |
| Is the edge-plane number consistent everywhere? | `claim_audit.json → source_rows` (9 rows, including the cross-script edge fraction) |
| Does the manuscript agree with the data? | `claim_audit.json → rows` (45 rows) and `PAPER_A_ROUND9_CLAIMS_AND_MANUSCRIPT_AUDIT.md` |
| Do the gates fire? | `mutation_tests.json` (13 mutants, all caught) |
| Did anything fail? | `validation/verification_log.txt` (one line per gate, with times) |
| Is the document compiled? | no — and no claim that it is |

---

## 4. Open items — stated, not smoothed

| item | status | why it is open |
|---|---|---|
| **Novelty / priority** | **UNRESOLVED** | the primary 2025 source is closed access; search absence is not evidence of novelty, and no claim is inferred from an abstract |
| **Corner-line boundary condition** | **not certified** | the corner band carries 0.9–1.3 % of the strain-gradient energy and its share drifts 6.6–6.8 % between degrees 18 and 30; no number depends on it beyond the third digit |
| **Material parameters** | **synthetic** | `ℓ = 50 nm`, `f = 1 nC/m`, `H = 0.05 H*` are labelled synthetic everywhere; no calibration is invented |
| **Experimental validation** | **absent** | theory/numerics paper; residuals of 1e-13–1e-17 are round-off, never accuracy |
| **LaTeX build** | **UNVERIFIED** | no engine in this environment; `static_check.py` validates references, labels, environments, citation keys, moving arguments and figure order only |
| **Non-authoritative material** | **AUTHOR INPUT REQUIRED** | funding, competing interests, CRediT, acknowledgements and any generative-tool disclosure are not invented here |
| **The maximum itself** | **local, not global** | certified inside `0.465 < k_x d < 0.625` only; outside that interval nothing is claimed |

`R_B ≈ 0.9467952` is therefore reported as a numerically certified local maximum within a declared
search interval — never as a universal maximum, never as a conversion efficiency, and never as a
percentage of energy turned around.

---

## 5. What changed in the headline, in one paragraph

Nothing. The headline is the reference-plane value, it was read directly from the solve, and the
defective transform only ever produced edge-plane numbers. What changed is the edge-plane record: the
search record moved from 0.965978 to 0.985572 (1.96 pp), the coupling dataset from a 0.019173–0.025598
range to 0.019304–0.025601, the density sweep's edge column by up to 0.14 % relative, and the printed
spreads of the maximum over degrees and quadrature from 5.6e-9 / 9.4e-10 to 5.0e-9 / 5.6e-9. Four
manuscript numbers were re-read from the regenerated records, three table cells moved (0.0231 → 0.0232
on rounding; 1.7e-9 → 3.8e-9 and 2.1e-8 → 2.3e-8 on regeneration), one paragraph about Fig. 9 was rewritten
because it had been wrong about the round-off levels, and the edge-plane share is now a registered
claim with a cross-script gate behind it.

**Submission readiness: not claimed.** The internal consistency of the paper is as far as this
environment can verify; the novelty question, the corner line and the LaTeX build are open, and they
are listed above rather than buried.
