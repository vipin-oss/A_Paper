# REPRODUCTION_TEST_RESULT

**Verdict: PASS WITH NUMERICAL DIFFERENCE, and PARTIAL on one step that could not be
executed at all (the LaTeX build).**  Nothing below is asserted: every line states what was
run, on what, and what came back.

* **Test date:** 2026-11-07
* **Environment:** fresh `python3 -m venv`, Python 3.11.2, numpy 2.4.6, scipy 1.17.1,
  matplotlib 3.11.2, Linux x86-64, single core, no network.
* **Source state:** repository commit `f0a61e4` (round 21) plus the archive scripts.
* **What "isolated" means here:** the environment was created from scratch for this test
  (`python3 -m venv .venv` + `pip install numpy scipy matplotlib`); no pre-existing site
  packages, no cached build artifacts, no environment variables beyond `PYTHONPATH=.`.
  It is *not* a different machine — the same sandbox, a clean interpreter environment.

---

## 1. Step-by-step result

| # | Step | Command | Result | Evidence |
|---|---|---|---|---|
| 1 | environment install | `python3 -m venv .venv && pip install -r requirements` | **PASS** | numpy 2.4.6, scipy 1.17.1, matplotlib 3.11.2 |
| 2 | import + model construction | `python -c "import model; model.Plate(degree=22)"` | **PASS** | `Q = 0.0746`, `α = 0.828`, `λ = 0.25`, `f = 2.563e-3`, `h = 0`, `nquad = 64` |
| 3 | full verification battery | `python paper_a_study/run_all_checks.py` | **PASS** (22 PASS, 1 SKIP) | `logs/battery_2026-11-07.log`, `EXIT=0` |
| 4 | data regeneration determinism | compare `figure_data/` before vs after the battery | **PASS WITH NUMERICAL DIFFERENCE** | 33 of 34 files byte-identical; `peak_search.json` differs in one wall-clock field (`verdict.elapsed_s`, 389.3 → 3831.8 s) and in nothing else |
| 5 | test suite in the unpacked archive | `python -m unittest paper_a_study.test_model` | **PASS** | 52 tests, `OK`, 21.5 s |
| 6 | figure regeneration in the archive | `python generate_final_figures.py` | **PASS** | 10 figures × 3 formats in 9.5 s |
| 7 | figure content vs shipped | text-run extraction + byte comparison | **PASS WITH RENDERING DIFFERENCE** | all 10: identical text runs (`303…369` runs, same sequence); 2 of 10 byte-identical up to the 5-byte creation-date stamp, 8 of 10 differ in font-subset bytes only, sizes within 12–313 B |
| 8 | LaTeX static validation | `python scripts/static_check.py` (in `02_OVERLEAF`) | **PASS** | 9 files, 173 labels, 111 refs, 13/13 citations |
| 9 | **LaTeX compile** | `pdflatex …` | **NOT EXECUTED** | no TeX engine exists in this environment and none could be installed; see §4 |
| 10 | archive audit | `python 04_REPRODUCTION/audit_archive.py` | **PASS** | required documents, no absolute paths, no junk, all manuscript paths, SHA-256 manifest |

## 2. The battery, as measured this run

```
PASS  dimensional and constitutive audit      0.6 s
PASS  quasistatic justification               0.5 s
PASS  flexoelectric control                   5.7 s
PASS  admissibility re-derivation             0.0 s
PASS  figure data and figure files            (inline)
PASS  phase-speed and e.m. reconciliation     0.5 s
PASS  modal-flux rescaling proof             10.6 s
PASS  mechanism matched controls            239.0 s
PASS  corner assessment and regression       14.0 s
PASS  certified peak (four fixed wavenumbers) 16.0 s
PASS  peak search and classification       3832.3 s   ← see §5
PASS  peak identity and artefact audit       22.6 s
PASS  spectral convergence                    8.7 s
PASS  quadrature sufficiency                  9.3 s
PASS  unit and scientific tests              24.0 s
PASS  natural boundary data identity          4.7 s
PASS  corner line force gate                 26.6 s
PASS  insulating edge default audit           0.4 s
PASS  round-21 regression tests               2.3 s
PASS  claim registry and stale guard          0.0 s
PASS  gate mutation tests                     9.5 s
PASS  LaTeX static validation                 0.1 s
SKIP  LaTeX build                    no TeX engine found
OVERALL: PASS          EXIT=0
```

## 2b. Archive-level checks, run on the unpacked archive

```
52 tests, OK                                        (python -m unittest paper_a_study.test_model)
compare_outputs.py  -> 34/34 files identical        (RESULT: PASS)
static_check.py     -> PASS (173 labels, 111 refs, 13/13 citations)
audit_archive.py    -> AUDIT: PASS (2 documented WARNs)
```

Nothing in the archive needed repairing to make these pass; the two items the audit lists
as WARN are structural (unedited historical reports; generic file names reused by
independent sub-studies) and are explained in `09_ARCHIVE_METADATA/BUILD_RECORD.md` §6.

## 3. Data determinism — the measurement behind step 4

`sha256sum` over all 34 files in `paper_a_study/figure_data/` before and after a complete
re-run of every producer:

```
identical      : 33 / 34
different      : 1  (peak_search.json)
```

`peak_search.json` field-by-field:

```
only difference: /verdict/elapsed_s   389.3 -> 3831.8
```

Every physical quantity (`R_B`, `K_B`, `ω`, angles, spreads, plateau, classification) is
bit-identical.  `compare_outputs.py` classifies this file as `VOLATILE-ONLY` and returns
`RESULT: PASS`; the two keys it treats as volatile are wall-clock fields only
(`elapsed_s`, timestamps) and it prints each one it ignores.

## 4. The step that could not be executed: the manuscript build

* `pdflatex`, `latexmk`, `xelatex`, `lualatex`, `tectonic`: **none present**.
* `apt-get install texlive-latex-base`: the package is not available in this image
  ("Unable to locate package").
* `pip install tectonic`: no such distribution on PyPI (`pip index versions tectonic`
  returns nothing).

Consequences, stated rather than hidden: **no `main.pdf` exists**, the typeset layout is
unverified, and the manuscript verdict in `FINAL_PACKAGE_STATUS.md` is **PARTIAL**.  The
source is validated statically (structure, references, citations, figure paths, macros);
that is all that could be done here.

## 5. Runtime variance (an honest observation, not a claim)

`peak_search.py` took **389.9 s** during round 21 and **3832.3 s** during this run — same
code, same data, same result (its `R_B` and classification are bit-identical).  The
difference is machine load on a shared sandbox: the check itself is deterministic, its
wall time is not.  Do not use the recorded times as a performance criterion; see
`07_DOCUMENTATION/NUMERICAL_METHOD.md` §7 for the range.

## 6. What this verdict does and does not license

**Licensed:** the program runs from a clean environment; the stored data are reproducible
from the code to the last digit (apart from one wall-clock field); the figures re-render
with identical drawn text; the manuscript source passes static validation; the archive is
internally consistent and complete.

**Not licensed:** any statement that the manuscript compiles, that the typeset pages were
seen, or that the numbers were checked against an independent implementation or an
experiment.  Those are open, and they are open in the same words in
`FINAL_PACKAGE_STATUS.md` and `07_DOCUMENTATION/KNOWN_LIMITATIONS.md`.

## 7. How to repeat this test

```bash
cd <unpacked archive>
python3 -m venv .venv && . .venv/bin/activate
pip install -r 01_PROGRAM/requirements.txt
cd 01_PROGRAM && python prepare_archive_layout.py
python -m unittest paper_a_study.test_model                    # 52 tests
python paper_a_study/run_all_checks.py                         # ≈ 15 min nominal
cd paper_a_study && python generate_final_figures.py           # ≈ 10 s
cd ../.. && python 04_REPRODUCTION/compare_outputs.py          # data vs shipped
python 04_REPRODUCTION/audit_archive.py                        # final audit
```
