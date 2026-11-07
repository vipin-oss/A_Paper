# Paper A — Round 9: test and gate results

All numbers below were produced in this session, in this sandbox, with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1` on two cores. No result is quoted from an
earlier round, and nothing here is claimed that was not executed.

---

## 1. Unit and scientific suite

```
python -m unittest paper_a_study.test_model -v
Ran 39 tests in 8.3s
OK
```

39 tests in 7 classes (round 8 had 26 in 4):

| class | tests | what it holds |
|---|---|---|
| `TestStudy` | 18 | the physics: exact `SH` limits, the strong-form residual, the energy identity, reciprocity, the independent `C¹` plate, temporal↔spatial consistency, singular-system rejection |
| `TestEdgePlaneTransform` | 6 | **new** — the four identities of the two-plane ratio transform, plus a test that the single-mode transfer is a *different* quantity |
| `TestPlaneInvariance` | 3 | **new** — the reconstructed edge value from solves at `L = 0, 10, 15, 20`; the transform against a direct solve at the edge; and the check that the raw values really do move with the plane (so the invariance is not vacuous) |
| `TestCrossScriptEdgeFraction` | 4 | **new** — stored edge shares of `peak_search`, `mechanism_controls`, `fig05` and `fig07` against a fresh evaluation, and against each other |
| `TestCertifiedPeak` | 4 | the search record: classification, reported vs located maximum, coarse raster insufficient, incident root ≠ backward target |
| `TestCornerAssessmentCaseSelection` | 2 | case labelling in the corner assessment |
| `TestFrozenReferenceConstants` | 2 | units and values of the frozen material constants |

### 1.1 Two tests that failed and were repaired (not deleted)

* `test_round_trip_between_planes` asserted that the ratio *rises* as the plane moves away from the
  edge. It falls: the ratio is `P_B/P_i`, and moving away multiplies it by
  `exp(−2(|Im K_i| + |Im K_B|)ΔL) < 1`. The assertion was inverted to match the derivation, with the
  direction stated in the failure message.
* `test_figure_csvs_match_the_shared_transform` rebuilt the reference solve by branch-tracking, which is
  not how `fig07` is produced: `fig07` sweeps `k_y` at the fixed operating frequency and wavenumber. The
  test now poses the reference solve the same way (`p.edge(ky, OMEGA0, K0, KB0)` per row) and checks
  three rows of the 19-row `H = 0` block.

Neither repair relaxes what is being tested; both make the test ask the same question as the production
code.

### 1.2 Tolerance policy

The new assertions compare plane-transformed quantities at `1e-6` relative (records: `1e-12`), not at
`places=9`. Rationale, stated in the code: the defect being guarded against is 2e-2 relative, agreement
between two arithmetic routes through the same solve is good to about 1e-6, and a 1e-9 bound on a
quantity that moves by 5e-9 under degree refinement would fail for reasons that have nothing to do with
the defect. Measured agreement is in fact 1.5e-12 (`fig05`) and 1.0e-11 (`fig07` worst of 19 rows), i.e.
five orders inside the bound.

---

## 2. The eighteen-gate battery

```
python paper_a_study/run_all_checks.py
OVERALL: PASS
TeX compilation: NOT EXECUTED - no engine available; source is statically validated only
```

| gate | result | time |
|---|---|---|
| unit and scientific tests | PASS | 9.3 s |
| dimensional and constitutive audit | PASS | < 1 s |
| quasistatic justification | PASS | 0.4 s |
| flexoelectric control | PASS | 2.4 s |
| admissibility re-derivation | PASS | < 1 s |
| figure data and figure files | PASS | — |
| phase-speed and e.m. reconciliation | PASS | 0.4 s |
| modal-flux rescaling proof | PASS | 4.7 s |
| mechanism matched controls | PASS | 86.9 s |
| corner assessment and regression | PASS | 6.5 s |
| certified peak (four fixed wavenumbers) | PASS | 7.0 s |
| peak search and classification | PASS | 147.2 s |
| peak identity and artefact audit | PASS | 10.4 s |
| spectral convergence | PASS | 4.1 s |
| quadrature sufficiency | PASS | 4.6 s |
| claim registry and stale guard | PASS | < 1 s |
| gate mutation tests | PASS (13/13 caught) | 3.3 s |
| LaTeX static validation | PASS | < 1 s |
| LaTeX build | **SKIPPED — no engine** | — |

The authoritative per-gate log of this delivery is `validation/verification_log.txt`, written by the
battery itself; the mutant record is `paper_a_study/figure_data/mutation_tests.json`.

---

## 3. What the battery does and does not establish

**Establishes:** every stored number the manuscript quotes is reproducible from the scripts; the edge
transform is implemented once and every producer uses it; the maximum is a certified local maximum in
the declared interval; convergence and quadrature are measured, not asserted; the gates fire when
defects are injected; the LaTeX source is statically consistent.

**Does not establish:** that the document compiles. There is no TeX engine in this environment, so
**LATEX BUILD — UNVERIFIED**; the static validator checks labels, references, environments, citation
keys, fragile moving arguments, figure order and deprecated values, and nothing beyond that.

**A note on reading the mutation output.** `gate mutation tests` prints a unittest summary containing one
deliberate `FAILED (failures=1)` per in-process mutant. That is the intended output: the gate is
*supposed* to fail there. The gate's own verdict line (`verdict: PASS`) means every mutant was caught.

---

## 4. Reproduction

```
python -m unittest paper_a_study.test_model -v      # 39 tests, ~9 s
python paper_a_study/claim_audit.py                 # registry vs records, ~0.1 s
python paper_a_study/mutation_tests.py              # 13 mutants, ~5 s
python paper_a_study/run_all_checks.py              # 18 gates, ~5 min on two cores
```

The battery is serial on purpose: running two solver scripts at once on two cores makes each roughly
ten times slower, and the peak search would exceed its own timeout.
