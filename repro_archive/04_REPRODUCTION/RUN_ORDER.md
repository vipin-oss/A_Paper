# RUN_ORDER

The exact order, with the reason each step depends on the one before it.

All commands below are run **from `01_PROGRAM/`** (the archive's copy of the source
repository root).  Steps marked `-m` must be run as modules from that directory --
`python -m paper_a_study.<script>` -- because they import siblings by package path,
which is exactly how `run_all_checks.py` invokes them.

```
 0. install            pip install -r 01_PROGRAM/requirements.txt
 0b. layout shim       python prepare_archive_layout.py            (symlinks only)
 1. import check       python -c "import model"                     (01_PROGRAM/paper_a_study)
 2. figure data        python build_figure_data.py                  ≈ 8 min
 3. figures            python generate_final_figures.py             ≈ 10 s
 4. certification      python -m paper_a_study.certify_peak                       ≈ 20 s
 5. peak search        python -m paper_a_study.peak_search                        ≈ 6.5 min (64 min on a loaded machine)
 6. peak identity      python -m paper_a_study.peak_identity_audit                ≈ 30 s
 7. convergence        python convergence_audit.py                  ≈ 12 s
 8. quadrature         python quadrature_audit.py                   ≈ 10 s
 9. modal flux         python -m paper_a_study.modal_flux_audit                   ≈ 11 s
10. mechanism controls python -m paper_a_study.mechanism_controls                 ≈ 5.5 min
11. corner assessment  python -m paper_a_study.corner_assessment                  ≈ 17 s
12. dimensional audit  python verify_dimensions.py                  ≈ 1 s
13. quasistatic       python quasistatic_check.py                   ≈ 1 s
14. flexo control     python flexo_control.py                       ≈ 6 s
15. admissibility     python reclassify_csv.py                      ≈ 0.1 s
16. phase speed       python -m paper_a_study.phase_speed_audit                   ≈ 1 s
17. gate 1 traction   python round21_gate1_traction.py              ≈ 5 s
18. gate 2 corner     python round21_gate_corner.py                 ≈ 27 s
19. gate 3 edge       python round21_edge_default_audit.py          ≈ 0.4 s
20. round-21 tests    python -m paper_a_study.round21_tests                       ≈ 2 s
21. unit tests        python -m unittest paper_a_study.test_model   ≈ 27 s
22. claim audit       python claim_audit.py                         ≈ 0.1 s
23. mutation tests    python mutation_tests.py                      ≈ 10 s
24. LaTeX static      python Paper_A_Final_Submission/scripts/static_check.py   (after the layout shim, §9)   ≈ 0.1 s
25. LaTeX build       pdflatex main && bibtex main && pdflatex main ×2   (needs TeX)
```

Steps 0–3 produce the deliverables.  Steps 4–24 are the evidence.  Step 25 needs a TeX
engine that the build environment did not have.

`01_PROGRAM/paper_a_study/run_all_checks.py` performs steps 4–24 in this order, each in
its own subprocess, and writes one log; use it unless you are debugging a single step.

---

## Why this order (the real dependencies)

1. **`build_figure_data.py` before everything.**  Steps 4–24 read `figure_data/*.csv` and
   `figure_data/*.json`; `reclassify_csv.py` reads the CSVs and writes nothing new;
   `test_model.py` reads `peak_certification.json`, `peak_search.json`,
   `mechanism_controls.json` and `figure_panel_sources.json`.
2. **`certify_peak.py` before `test_model.py`.**  `test_stored_operating_point_matches_
   certification` asserts that the stored operating point equals the paper's value and
   that the certification record exists.  If you run the tests first, they fail with a
   *missing record*, not with a physics mismatch — the message says so.
3. **`peak_search.py` before `peak_identity_audit.py`.**  The identity audit checks that
   the peak found by the search is the backward branch, not an artefact of the reference
   plane; it reads the search record.
4. **`mechanism_controls.py` before `test_model.py`.**  `test_mechanism_controls_record_
   matches_the_shared_transform` compares the controls against the shared
   plane-transform function; without the record it has nothing to compare.
5. **`generate_final_figures.py` after `build_figure_data.py`** (it reads
   `figure_panel_sources.json` and the CSVs), and **before** `static_check.py` if you
   want the static check to see fresh figure PDFs.
6. **`claim_audit.py` last** among the audits: it re-reads the manuscript, the registry
   and the stored data, so it is only meaningful once the data exist.
7. **`mutation_tests.py` after the test suite exists**: it mutates the *tests'* targets
   and requires each mutation to be caught; running it before the tests would prove
   nothing.

## Idempotence

Every script overwrites its own outputs and touches nothing else.  Re-running any subset
is safe; re-running all of them in a different order changes only timestamps.  No script
deletes a file it did not write, and none writes outside
`paper_a_study/figure_data/`, `paper_a_study/figures_final/`, `paper_a_study/results/`
and `validation/`.

## The two expensive steps

`mechanism_controls.py` and `peak_search.py` dominate the wall time (≈ 4–6.5 min on an
idle machine; `peak_search.py` took 64 min on a loaded sandbox — same result, machine-bound).  If you are only re-deriving the paper's headline
number, `certify_peak.py` (20 s) is enough — it recomputes `R_B` at the four fixed
wavenumbers including the certified maximum.  The full search is needed only to
re-establish that the maximum is a local maximum with a flat top.
