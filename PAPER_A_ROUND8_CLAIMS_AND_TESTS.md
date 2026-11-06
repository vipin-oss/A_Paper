# Paper A — Round 8: claim registry, tests and mutation gates

The point of this round is not that the numbers changed. It is that the previous construction *could not
have detected* that they were wrong (defect D8). This report documents the construction that now can.

---

## 1. The claim registry (`paper_a_study/claims.json`)

**19 claims, 42 checked literal strings, 5 guarded deprecated values.**

Each claim has eight fields and is machine-checked:

| field | meaning |
|---|---|
| `id` | stable identifier, used in failure messages |
| `value` | the number the paper asserts |
| `tolerance_rel` | how far a denoting string may sit from `value` (rounding, not physics) |
| `in_abstract` | whether the abstract must carry it |
| `source` | where the number comes from, down to the field of the stored record |
| `tokens[].file` | the `.tex` file that must contain the string |
| `tokens[].text` | the literal LaTeX string, e.g. `\SI{94.68}{\percent}` |
| `tokens[].value` | the number that string denotes |

Coverage: the operating-point share, the certified maximum, the located argmax, the earlier 0.5250
sample (kept deliberately), the 0.55 sample, both total-outgoing powers, the coupling changes at all three
configurations (reference *and* edge plane), the peak attenuations, the wavenumber ratio, the incident
wavenumber, the degree and quadrature spreads, the 128-fold incident-flux ratio and the reference-plane
closure.

## 2. What `claim_audit.py` now checks

| gate | what fails it |
|---|---|
| 1. Registry agreement | a registered string is missing from its file, or denotes a different number than the registry says |
| 2. Stale-value guard | any of `0.99985`, `28.06`, `93.19`, `33.1`, `110 rows` reappears anywhere in the manuscript |
| 3. Ordering and coverage | figures are first cited out of numerical order, or an `in_abstract` claim is absent from the abstract |
| **4. Source agreement (new)** | the registry agrees with the text but not with the data |

Gate 4 is the one that would have caught D1 at the registry level. It requires, from
`peak_search.json` and `peak_identity_audit.json`:

* the stored classification is `certified_local_maximum`;
* the registered headline equals the stored headline to 10⁻⁴ relative;
* **no sample of the coarse raster reaches the stored maximum** — a maximum read off a grid fails here;
* the located maximum lies strictly inside the scanned domain;
* the registered incident wavenumber equals the audited incident root, is **more than 0.2 from K_B**
  (so the case cannot have been labelled with the backward target) and is **more than 10⁻⁴ from the
  branch parameter** (the two are distinct quantities and are reported apart);
* the registered degree and quadrature spreads equal the stored ones.

`--registry` was added so the mutation suite can point the audit at an edited copy without touching the
real registry.

## 3. The test suite: 22 → 26 tests, all passing in 14.4 s

Four tests were added, and they are written as **solver evaluations, not stored expectations**, so they
fail if the physics moves:

| test | what it requires | defect it guards |
|---|---|---|
| `test_a_coarse_raster_cannot_be_certified` | the refined value at 0.5275 exceeds every sample at 0.52 / 0.525 / 0.53 by more than 5 × 10⁻⁴, and lies in (0.94, 1.0) | D1 |
| `test_incident_mode_is_not_the_backward_target` | the incident root is within 2 × 10⁻³ of the requested wavenumber, more than 0.2 from K_B; Re K_B > 0; the backward x-power is negative | D5 |
| `test_partition_is_independent_of_the_reference_plane` | solving at L = 10 and L = 15 and rescaling by the *measured* net exponent reproduces the partition to 10⁻⁹ | D2 |
| `test_reported_peak_matches_the_search_record` | the stored classification is `certified_local_maximum`, a fresh solve equals the stored headline to 10⁻⁹, and the argmax exceeds it by less than 10⁻⁵ | D1, D4 |

The remaining 22 tests are unchanged: exact classical and strain-gradient limits, the two independent
strong-form propagators, the C¹ finite-element plate, the residual suite, reciprocity, the singular-system
rejection, the two corner-labelling regressions, and the two frozen-constant regressions.

## 4. The mutation suite: 5 → 8 defects, each must be caught

Run on temporary copies of the manuscript (the working tree is never modified), plus two in-process
mutations that are restored in a `finally` block. **Nothing from the mutation run is committed** — only
the script that performs it.

| id | deliberate defect | gate that must catch it | caught |
|---|---|---|---|
| M1 | `\path` in a caption without `\protect` | static_check | yes |
| M2 | registered headline 94.68 → 94.86 in the conclusions | claim_audit registry | yes |
| M3 | deprecated total-outgoing power 0.99985 re-inserted | claim_audit stale guard | yes |
| M4 | undefined citation key | static_check | yes |
| M5 | c44 entered in Pa instead of GPa | TestFrozenReferenceConstants | yes |
| **M6** | **the superseded coarse-grid maximum (93.19 at 0.525) reinstated in the abstract** | **claim_audit stale guard** | **yes** |
| **M7** | **the peak case relabelled with the backward root K_B = 0.2452** | **TestCornerAssessmentCaseSelection** | **yes** |
| **M8** | **the registered incident wavenumber replaced by K_B** | **claim_audit source agreement** | **yes** |

M6–M8 are new and each exercises one of the three new defences: a coarse-grid maximum cannot re-enter the
text, a case cannot be relabelled with the backward root, and a registry that drifts away from the data is
caught even when it still matches the text.

## 5. Checks `run_all_checks.py` now performs

Added this round: `certify_peak.py` (four fixed wavenumbers), `peak_search.py` (the staged search and its
classification) and `peak_identity_audit.py` (the five artefact probes). The Fig. 4 row count assertion was
corrected from 110 to 139 — as data, never as prose: the manuscript does not state a row count.

The battery is a single log, `validation/verification_log.txt`, with one line per gate and its wall time.

## 6. What the suite still cannot check

* **No compile.** There is no TeX engine in this environment, so the manuscript is **BUILD UNVERIFIED**;
  `static_validation.txt` checks labels, references, environments and citation keys and nothing else.
* **No novelty verdict.** The claim registry checks internal consistency. Whether the result is new is a
  literature question, and it remains **UNRESOLVED** (see the delivery report).
* **No physical validation.** Every test is against the solver's own formulation or an independent
  discretisation of the same equations. Nothing here is an experiment.
