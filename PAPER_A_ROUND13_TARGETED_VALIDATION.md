# Paper A — round 13: targeted validation

Everything below was executed in this round, on the edited tree, and is reported as
it came out. Nothing is claimed that was not run, and the one gate that was **not**
run is named with its reason.

Baseline `3827543016ece4a9d0612e861bf75425457291bf`; environment Python 3.11,
numpy 2.4.6, scipy 1.17.1, matplotlib 3.11.2; no TeX engine.

---

## 1. Summary

| # | gate | command | result | verdict |
|---|---|---|---|---|
| 1 | fig10 dataset regeneration | `python -c "import build_figure_data as b; b.fig10()"` | ran in 4.6 s; CSV byte-identical; JSON +2 keys | PASS |
| 2 | fig10 render | `python -c "import generate_final_figures as g; g.fig10()"` | wrote PDF + PNG | PASS |
| 3 | full unit and scientific suite | `python -m unittest paper_a_study.test_model` | `Ran 52 tests in 24.461s — OK` | PASS |
| 4 | new fig10 vector tests | `python -m unittest ...TestFigure10BackwardWavenumber -v` | `Ran 5 tests in 0.287s — OK` | PASS |
| 5 | deliberate reversal of the arrow | mutant copy in `/tmp/m16`, same test class | `FAILED (failures=2, errors=1)` | CAUGHT ✔ |
| 6 | claim registry | `python paper_a_study/claim_audit.py` | 23 claims / 46 tokens / 5 deprecated / 11-11 rows | PASS |
| 7 | gate mutation tests | `python paper_a_study/mutation_tests.py` | 15 mutants, 15 caught | PASS |
| 8 | phase-speed audit | `python paper_a_study/phase_speed_audit.py` | exit 0 | PASS |
| 9 | static manuscript check | `python scripts/static_check.py` | 104 labels / 75 refs / 13-13 citations | PASS |
| 10 | full 18-gate battery | `python paper_a_study/run_all_checks.py` | **not run** — see §6 | — |
| 11 | LaTeX build | `pdflatex` … | **not possible** — no engine, see report 4 | UNVERIFIED |

---

## 2. The fig10 dataset regeneration

```
$ cp figure_data/fig10_field_maps.csv /tmp/fig10_maps_before.csv
$ time python -c "import build_figure_data as b; b.fig10()"
wrote {'ky_d': 0.12981175031447484, 'incident_kx_d': 0.7361990195318475,
       'incident_im_kx_d': 5.402718679033664e-06, 'backward_kx_d': 0.2451746921716515,
       'backward_im_kx_d': -5.230595074070594e-06, 'incident_phase_angle_deg': 9.999999999991843,
       'backward_phase_angle_deg': 27.899713983543208,
       'magnitude_ratio_backward_over_incident': 0.3711022669787309, ...}
real 0m4.635s
$ cmp /tmp/fig10_maps_before.csv figure_data/fig10_field_maps.csv
(no output)
```

The 22 801-row field map is **byte-identical** to the shipped one, so panels (a) and
(b) are the same data. Only `fig10_field_metrics.json` changed, by eleven added lines
(`git diff --stat`: `1 file changed, 11 insertions(+)`).

### A threading observation worth recording

The first regeneration was run with `OMP_NUM_THREADS=1` (the setting the README
recommends for the heavy producers). That version differed from the shipped CSV by
at most $3.8\times10^{-11}$ absolute and $1.5\times10^{-7}$ relative — round-off from
BLAS reduction order, not physics. Re-running the unchanged producer at the
environment's default threading reproduced the shipped file **exactly**, and the
default-threaded output was then confirmed deterministic:

```
$ python -c "import build_figure_data as b; b.fig10()"     # run 1 → /tmp/run1.csv
$ python -c "import build_figure_data as b; b.fig10()"     # run 2
run2 CSV identical to run1
run2 JSON identical to run1
```

So the delivered dataset is reproducible bit-for-bit *given the threading*, and
thread count moves the intensities by $10^{-7}$ relative — five orders below any
number the manuscript quotes. Both facts are now on record; nothing was restored or
hand-edited.

---

## 3. Test suite

```
$ python -m unittest paper_a_study.test_model
Ran 52 tests in 24.461s
OK
```

47 tests carried over from round 12, all still passing, plus five new ones:

```
$ python -m unittest paper_a_study.test_model.TestFigure10BackwardWavenumber -v
test_drawn_backward_wavenumber_is_the_solved_one ... ok
test_flux_opposes_the_wavenumber ... ok
test_reversed_arrow_is_rejected ... ok
test_the_drawn_length_keeps_the_solved_magnitude_ratio ... ok
test_the_renderer_calls_the_guard ... ok
Ran 5 tests in 0.287s
OK
```

The suite includes the figure-provenance tests that were invisible to the 39-test
suite of round 10 — among them `test_no_panel_ink_touches_the_canvas_edge`, which
re-ran against the regenerated `fig10_field.png` and passed (no label clipped by the
new arrow placement).

---

## 4. The reversal is caught

A copy of the renderer with the backward wavevector negated was placed in `/tmp/m16`
and the new class was pointed at it through the same environment variable the
mutation harness uses:

```
$ PAPER_A_FIGURE_SRC=/tmp/m16 python -m unittest paper_a_study.test_model.TestFigure10BackwardWavenumber
FAIL: test_flux_opposes_the_wavenumber
AssertionError: 1.2803346198043053 not less than 0.0 : for a backward mode the flux
points opposite to the phase vector
Ran 5 tests in 0.289s
FAILED (failures=2, errors=1)
```

Two failures and one error from one reversed sign: the direction comparison, the
flux-opposition test, and the guard expectation. The defect that shipped in rounds
11–12 cannot return silently, and the guard also aborts the render itself.

---

## 5. Registry, mutants, phase speed, static check

```
$ python paper_a_study/claim_audit.py
claims registered: 23   tokens checked: 46
deprecated values guarded: 5
figure first-citation order: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
source-agreement rows: 11 (11 passing)
PASS
```

```
$ python paper_a_study/mutation_tests.py
verdict: PASS            # 15 mutants defined, 15 caught
```

Note that the suite grew from 47 to 52 while the mutant count stayed at 15: the
mutants probe gates (bounds, labels, units, registries), and no gate changed in this
round — only a new test was added. M14, the mutant that reintroduces the round-11
"backward reflectance" axis label, still fails the suite as designed.

```
$ python paper_a_study/phase_speed_audit.py
wrote .../figure_data/phase_speed_audit.json
RESULT: PASS

$ python Paper_A_Final_Submission/scripts/static_check.py ; echo $?
files checked: 8
labels: 104   references: 75
citation keys used: 13   bib entries: 13
PASS
0
```

---

## 6. What was deliberately not run

| gate | why not |
|---|---|
| `run_all_checks.py` (the 18-gate battery, ~13 min, regenerates every dataset from an empty directory) | no producer's *logic* changed. `build_figure_data.fig10()` gained one metadata block, and that one function was re-run and verified byte-for-byte against the shipped CSV. Re-running the whole battery would rebuild nine unrelated datasets, re-timestamp the log, and re-measure round 11 rather than round 13 |
| `peak_search.py` (~5 min) | its inputs did not change; only its docstring did. `peak_search.json` is untouched and still the record the docstring now describes |
| `generate_final_figures.py` in full | re-rendering all ten figures would change nine PDFs only in their embedded `CreationDate`, which is churn, not verification. fig10 — the only figure whose content changed — was rendered and inspected |
| LaTeX build | no engine (report 4) |

The last full battery remains the round-11 run: **18 PASS / 0 FAIL / 1 SKIP**
(`validation/round11_battery_run_clean_reproduction.log`), and that is reported as a
historical result, not as a round-13 one.

---

## 7. Files whose bytes changed in this round

| file | nature of the change |
|---|---|
| `paper_a_study/build_figure_data.py` | one metadata block added to the fig10 payload |
| `paper_a_study/generate_final_figures.py` | two helpers added; four direction literals replaced by derived values; guard call; label offset |
| `paper_a_study/test_model.py` | one new test class, 5 tests (47 → 52) |
| `paper_a_study/peak_search.py` | docstring only |
| `paper_a_study/figure_data/fig10_field_metrics.json` | +11 lines, no existing value moved |
| `paper_a_study/figure_data/fig10_field_maps.csv` | **unchanged** (byte-identical after regeneration) |
| `paper_a_study/figures_final/fig10_field.pdf`, `.png` | re-rendered; the arrow moved |
| `Paper_A_Final_Submission/figures/fig10_field.pdf` | the new render |
| `Paper_A_Final_Submission/sections/results.tex` | caption, two words |
| `Paper_A_Final_Submission/sections/appendix_reproducibility.tex` | 47 → 52 in three places |
| `PAPER_A_ROUND12_CORRECTION_HISTORY.md`, `downloads/README.md` | the 0.622973 abscissa, with a dated note |
| `PAPER_A_ROUND12_BLOCKING_ISSUES.md`, `PAPER_A_ROUND12_READINESS_ASSESSMENT.md` | dated status notes, body unchanged |
| `PACKAGE_README.md` | round-13 header, 52 tests, report list |
| `Paper_A_Final_Submission/MANIFEST.json`, `static_validation.txt` | regenerated by their own tools |

Unchanged in bytes: the other nine figure PDFs, all ten figure CSVs other than the
fig10 metrics, every solver file, every table, every reported number.
