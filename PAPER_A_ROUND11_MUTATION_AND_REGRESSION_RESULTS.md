# Paper A — Round 11: mutation and regression results

A gate that has never failed is not a gate. This file records what each gate was
made to swallow, and what the anti-regression list still rejects after the round-11
changes.

Machine-readable record: `paper_a_study/figure_data/mutation_tests.json`
(15 mutations, verdict **PASS** — every one caught).

---

## 1. The fifteen mutations

Two are new in this round: **M13** (a bound that must bite) and **M14** (a figure
label that must not come back).

| id | deliberate defect | gate that must catch it | result | first line of evidence |
|---|---|---|---|---|
| **M1** | \path inserted in a caption without \protect | `static_check` | CAUGHT | - sections/results.tex: line 467: fragile \path in a moving argument (\caption) - use \protect\path |
| **M2** | registered headline 0.9468 edited to 0.9486 | `claim_audit registry` | CAUGHT |  |
| **M3** | deprecated total outgoing power 0.99985 re-inserted | `claim_audit stale guard` | CAUGHT | - deprecated value '0.99985' reappeared in sections/results.tex: mislabelled total outgoing power |
| **M4** | undefined citation key \cite{nosuchkey2024} | `static_check` | CAUGHT | - citation key not in references.bib: nosuchkey2024 |
| **M6** | superseded coarse-grid maximum (93.19 at 0.525) reinstated | `claim_audit stale guard` | CAUGHT | - deprecated value '93.19' reappeared in main.tex: superseded headline: the 0.525 sample is not the maximum |
| **M8** | incident wavenumber replaced by the backward target KB0 | `claim_audit source agreement` | CAUGHT | - incident_wavenumber_peak: registry says 0.2451746921716515 but the stored identity-audit incident root is 0. |
| **M13** | registered refinement bound tighter than the executed spread | `claim_audit bound` | CAUGHT | - degree_stability_peak: the registered bound is 1e-10 but the stored search-record degree spread at K = 0.527 |
| **M14** | R_B labelled a reflectance again | `TestFigureProvenance` | CAUGHT | AssertionError: 'backward reflectance' unexpectedly found in '"""Render the ten Paper A main figures from the  |
| **M5** | c44 entered in Pa instead of GPa | `TestFrozenReferenceConstants` | CAUGHT | AssertionError: False is not true : c44 = 4.3e+19 is outside the literature band [30000000000.0, 60000000000.0 |
| **M7** | peak case labelled with KB0 instead of its incident root | `TestCornerAssessmentCaseSelection` | CAUGHT | AssertionError: 0.2451746921716515 != 0.5275 within 12 places (0.28232530782834847 difference) |
| **M9** | edge-plane transform reduced to the backward decay only (omits the incident attenuation) | `TestCrossScriptEdgeFraction` | CAUGHT | AssertionError: 0.0001080610577728347 not less than 1e-06 : fig05 CSV vs shared transform: 1.08e-04 |
| **M10** | sign of the plane-transform exponent flipped (wrong direction of propagation) | `TestCrossScriptEdgeFraction` | CAUGHT | AssertionError: 0.0004254238646290709 not less than 1e-06 : fig05 CSV vs shared transform: 4.25e-04 |
| **M11** | reference plane moved from 10 to 8 thicknesses (wrong reference distance) | `TestCrossScriptEdgeFraction` | CAUGHT | AssertionError: 4.2535005448263163e-05 not less than 1e-06 : fig05 CSV vs shared transform: 4.25e-05 |
| **M12** | thickness d replaced by the gradient length l (L and l confused) | `TestCrossScriptEdgeFraction` | CAUGHT | AssertionError: 1.0 not less than 1e-06 : fig05 CSV vs shared transform: 1.00e+00 |
| **M10b** | flipped exponent, checked by an invariance test that uses no stored values | `TestPlaneInvariance` | CAUGHT | AssertionError: 0.07714125271109584 not less than 1e-09 : reconstructed edge value depends on the plane (L=10. |

Notes on the two new mutants:

* **M13** writes a registry in which `degree_stability_peak` is bound at
  $10^{-10}$, tighter than the $5.6\times10^{-9}$ the solver produces — which is
  what a genuinely unconverged (or wrongly computed) spread would look like. The
  gate fails with
  `the registered bound is 1e-10 but the stored search-record degree spread ... is 7.28e-09`.
  A bound that cannot fail would be decoration; this one fails on demand.
* **M14** puts the round-10 fig02 label back (`backward reflectance $R_B$ (%)`) in a
  copy of the plotting code and runs the provenance test against that copy through
  the `PAPER_A_FIGURE_SRC` hook. The test fails with
  `'backward reflectance' unexpectedly found`. This is the only way a label defect
  can be kept out; prose review of ten figures per round is not a gate.

---

## 2. Anti-regression list, re-checked in this round

Each item is a defect that has appeared at least once and must never reappear.

| stale statement | where the guard lives | status after round 11 |
|---|---|---|
| headline 57.92 % (a mid-window sample read as a maximum) | `claim_audit` deprecated list + `R_B_certified_maximum` | still rejected |
| headline 93.19 % (coarse raster, $k_xd=0.525$) | `claim_audit` deprecated list; mutant **M6** | still rejected |
| coupling change 33.1 % (superseded by 34.2 %) | `claim_audit` deprecated list | still rejected |
| total outgoing 0.99985 (pre-corner bookkeeping) | `claim_audit` deprecated list; mutant **M3** | still rejected |
| attenuation 28.06 dB/mm (superseded plane) | `claim_audit` deprecated list | still rejected |
| "110 rows" (a data property quoted as physics) | `claim_audit` deprecated list | still rejected |
| wrong edge normalisation (single-mode decay used as a ratio transform) | `TestCrossScriptEdgeFraction`; mutants **M9**, **M10**, **M10b**, **M11**, **M12** | still caught |
| wrong incident wavenumber (the backward root used as the incident one) | `claim_audit` source row + identity audit; mutants **M7**, **M8** | still caught |
| wrong units (c44 in Pa instead of GPa) | `TestFrozenReferenceConstants`; mutant **M5** | still caught |
| unreferenced `\path` in a caption, undefined citation key | `static_check`; mutants **M1**, **M4** | still caught |
| unsupported accuracy claim ($\pm60$ kHz, $<4\times10^{-6}$) | **new**: `coupling_frequency_shift_max` claim + source row | now rejected automatically (D11) |
| a refinement spread quoted as a value, tested by equality | **new**: `kind = "bound"` + mutant **M13** | now caught (D9) |
| a modal share labelled a reflectance | **new**: `TestFigureProvenance` + mutant **M14** | now caught (D1) |

## 3. Unit and scientific tests

`python -m unittest paper_a_study.test_model` — **47 tests, OK** (21 s).
Eight are new (`TestFigureProvenance`):

1. the panel map agrees with the plotting code;
2. every figure is mapped with four panels and has PDF, PNG and SVG;
3. $R_B$ is never called a reflectance;
4. the reference plane is $L$ and the gradient length is $\ell$;
5. residual panels declare their round-off floor;
6. the schematic panel is labelled;
7. the figure CSVs carry the columns the plotters read (catches a stale generator, D25);
8. no panel ink touches the canvas edge (catches a clipped label, D24).

The seven provenance tests were **not** satisfiable by the round-10 tree: applied to
it, tests 3, 4, 5, 6 and 8 fail, which is the point — they encode the defects this
round found.

## 4. Repeatability

The full battery was run twice on freshly generated data in this round (once
ending FAIL on the mis-united claim, once after the unit fix ending PASS). The
second run re-solved the whole chain, rewrote every record, and reproduced the
classification, the reported maximum and every gate result. No record was restored
between runs.
