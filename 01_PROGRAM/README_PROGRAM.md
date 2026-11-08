# README_PROGRAM

The program of record for Paper A: one model module, a figure-data builder, a plotting
script, an audit battery, and the tests that guard all of it.

**Language:** Python 3.11 (tested on 3.11.2; no 3.10-only or 3.12-only syntax is used).
**Third-party dependencies:** `numpy`, `scipy`, `matplotlib` — nothing else is needed to
reproduce every number and figure.  `sympy` is used only by the `a0/` feasibility audit
and is optional for the paper's results.
**Exact versions used:** `09_ARCHIVE_METADATA/environment_pip_freeze.txt`.
**Declared ranges:** `requirements.txt` in this folder.

---

## 1. Layout

```
01_PROGRAM/
  paper_a_study/
    model.py                     THE solver: Plate (assembly, temporal, spatial, edge),
                                 MeshPlate (independent FE check), strong-form roots
    build_figure_data.py         every plotted number → figure_data/*.csv|*.json
    generate_final_figures.py    the ten figures → figures_final/*.{pdf,png,svg}
    figure_style.py              matplotlib rcParams, fonts, colours, panel labels
    run_all_checks.py            the full battery, one log, subprocess-isolated
    test_model.py                52 unit/scientific tests (the main guard)
    run_study.py                 older end-to-end driver (superseded by build_figure_data.py)
    regenerate_revised_data.py   round-19 regeneration driver (kept for the baseline)
    validate_revised_data.py     round-19 validator for that regeneration
    certify_peak.py              four fixed wavenumbers, refinement ladder
    peak_search.py               grid + plateau + refine + classification
    peak_identity_audit.py       peak identity / artefact audit
    convergence_audit.py         spectral degree 14…34
    quadrature_audit.py          Gauss nodes 64…256
    modal_flux_audit.py          rescaling-invariance of the modal power
    phase_speed_audit.py         phase/energy-speed and EM reconciliation
    mechanism_controls.py        matched controls for the H mechanism (dominant cost)
    fe2d.py                      direct 2D (x,z) finite-element solve of the edge problem (B-spline in x
                                 graded to the edge, absorbing layer, scattered-field load, modal fit)
    fe2d_validate.py             runs fe2d.py at the operating point -> figure_data/fe2d_validation.csv
                                 (Table tab:fe2d).  `python3 fe2d_validate.py op`; `fold` is NOT a valid test
                                 (incident and backward modes coincide there)
    corner_assessment.py         corner line-force assessment + regression
    quasistatic_check.py         quasistatic justification
    flexo_control.py             flexoelectric magnitude control
    reclassify_csv.py            admissibility re-derivation, no re-solving
    mutation_tests.py            15 deliberate defects; each must be caught
    claim_audit.py               claims.json ↔ manuscript ↔ stored data
    round16_*.py … round21_*.py  the round-by-round gate scripts (see RUN_ORDER.md)
    claims.json                  40 live claims (+6 deprecated), each with its source
    reference_constants.json     frozen K0/KB0/KY0/OMEGA0/HCRIT + material + bands
    figure_validation_report.json
  a0/                            material model, materials.json, requirements.txt,
                                 run_checks.py, test_a0.py (feasibility audit only)
  tools/
    static_check.py              LaTeX static validation (labels, refs, citations)
    build_submission_package.py  builds Paper_A_Final_Submission from these sources
    make_download_archive.py     builds the round-21 delivery zip
    build_repro_archive.py       builds THIS archive (documented, re-runnable)
    sync_paper_a_figures.py      copies figures_final → manuscript figures/
```

## 2. Install (no build step, no compilation)

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt          # numpy, scipy, matplotlib
```

Nothing is compiled; there is no setup.py/pyproject because the code is run as scripts
from the `paper_a_study/` directory.  `model.py` reads `../a0/materials.json`
**relative to its own location**, so the folder structure must keep `paper_a_study/`
and `a0/` as siblings:

```
01_PROGRAM/paper_a_study/model.py
01_PROGRAM/a0/materials.json          ← required by model.py at import time
```

If you move `paper_a_study/` alone, the import fails immediately with a `FileNotFoundError`
(it does not fall back to defaults — deliberately).

## 3. Entry point

There is exactly one entry point that matters:

```bash
cd 01_PROGRAM
python paper_a_study/run_all_checks.py
```

It runs each check in its own subprocess, prints one line per check, and writes
`validation/verification_log.txt` at the root of the tree it is run from.  Expected on a
clean environment: **22 PASS, 1 SKIP (no TeX engine), `OVERALL: PASS`**, ~15 min.

For the deliverables rather than the audits:

```bash
cd 01_PROGRAM/paper_a_study
python build_figure_data.py          # ≈ 8 min  → figure_data/
python generate_final_figures.py     # ≈ 10 s   → figures_final/
```

## 4. Exact order, commands, outputs

The canonical order is `04_REPRODUCTION/RUN_ORDER.md`; it is not repeated here except
for the dependency note that matters: **`test_model.py` needs the records produced by
`certify_peak.py`, `peak_search.py` and `mechanism_controls.py`** — it asserts that the
stored operating point matches its own independent recomputation, so running the tests
before those records exist fails for the right reason (missing record), not because the
physics changed.

## 5. Runtime and resources

Single core, no GPU, no network.  Peak memory is dominated by the 29 MB SVG writing of
Fig. 10 (< 1 GB).  Measured times are tabulated in
`07_DOCUMENTATION/NUMERICAL_METHOD.md` §7; the two expensive checks are
`mechanism_controls.py` (323 s) and `peak_search.py` (390 s).

## 6. Tolerances and solver settings (summary)

| Setting | Value | Where |
|---|---|---|
| polynomial degree | 22 | `build_figure_data.DEGREE` |
| Gauss–Legendre nodes | `max(64, 2·degree+10)` = 64 | `Plate.__init__` |
| electrical case (faces) | `ground` | `Plate(electric='ground')` default |
| electrical case (edge) | `insulating` | `Plate(edge_electric='insulating')` default |
| frequency | `Ω0 = 7.633372404423294` | `reference_constants.json` |
| outgoing/incoming cut-off | `τ = 2e-8 max(1,|k_x|)` | `Plate.edge` |
| SVD rank cut-off | `1e-12` relative | `Plate.edge` (raises on deficiency) |
| reference plane | `L = 10 d` | `REF_NORM = 10.0` |
| seeds | **none used** (fully deterministic) | — |
| energy-balance tolerance (tests) | `5e-6` relative | `test_model.py` |
| degree-convergence assertion | `2e-7` (measured 1.06e-7) | `test_degree_convergence` |

## 7. Scripts that are history, not method

`run_study.py`, `regenerate_revised_data.py`, `validate_revised_data.py` and the
`round16_*`–`round21_*` scripts are the audit trail of the corrections.  They are shipped
because the reports in `06_VALIDATION/` cite them, and because they let a reader
re-execute a specific gate.  **They are not on the path to the paper's figures**; that
path is `model.py` → `build_figure_data.py` → `generate_final_figures.py`.

## 8. Failure behaviour

Deliberately loud, no silent fallbacks:

* `Plate.__init__` raises if the Schur condition is violated, if `ℓ = 0` with `f ≠ 0`, or
  if an unknown electrical case is requested.
* `Plate.edge` raises `RuntimeError('rank deficiency')` instead of regularising.
* `run_all_checks.py` records SKIP only for a missing TeX engine; everything else is
  PASS/FAIL, and one failure cannot mask another (separate subprocesses).
* `claim_audit.py` fails on a number in the manuscript that does not match stored data,
  and on any `deprecated` value quoted without its guard.
* `mutation_tests.py` fails if a deliberate defect is **not** caught.

    test_review_regressions.py   3 regression tests for the independent-review fixes (energy-balance sign, flux balance, open-circuit full basis vs C1 mesh)
