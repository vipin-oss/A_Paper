# REPRODUCE_FROM_SCRATCH

From an empty machine to the figures and the manuscript source, with the exact commands,
the expected output of each, and the signs of a wrong environment.

**Time budget:** ~25 min on an idle machine (≈ 8 min data + 10 s figures + ≈ 15 min full battery).
On a loaded shared machine the battery can take an hour or more — measured 71 min during the
archive verification run, dominated by `peak_search.py` (64 min).
**Resources:** one CPU core, < 1 GB RAM, no GPU, **no network** after installation.

---

## 0. What you need

* Python **3.11** (3.11.2 was used; 3.10 or 3.12 are expected to work but were not
  tested here).
* A C-free install: `numpy`, `scipy`, `matplotlib` wheels only — nothing compiles.
* Optional: a TeX distribution, if you want a PDF (see §5).

## 1. Unpack and place the tree

```bash
unzip PAPER_A_COMPLETE_REPRODUCIBILITY_ARCHIVE.zip
cd PAPER_A_COMPLETE_REPRODUCIBILITY_ARCHIVE
```

Nothing needs to be moved: `01_PROGRAM/paper_a_study/` and `01_PROGRAM/a0/` are siblings,
which is what `model.py` requires (it reads `../a0/materials.json` at import time).

## 2. Create the environment

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r 01_PROGRAM/requirements.txt
python -c "import numpy, scipy, matplotlib; print(numpy.__version__, scipy.__version__, matplotlib.__version__)"
```

Expected (the recorded build environment): `2.4.6 1.17.1 3.11.2`.
Any recent version works numerically, but **byte-level reproduction of the shipped CSVs
is only guaranteed for these versions** (different BLAS/LAPACK may change the last
digits).

Sanity check that must fail loudly if the layout is wrong:

```bash
cd 01_PROGRAM
python -c "import sys; sys.path.insert(0,'paper_a_study'); import model; p=model.Plate(degree=22); print(p.Q, p.alpha, p.lam, p.f, p.h)"
```

Expected: `0.0746… 0.828… 0.25 0.002563… 0.0` (the five dimensionless groups; `h = 0`
because production uses `H = 0`).  Wrong values ⇒ wrong `a0/materials.json` or a stale
`PYTHONPATH`.

## 3. Regenerate the data

```bash
cd 01_PROGRAM/paper_a_study
python build_figure_data.py          # ≈ 8 min (measured 469.6 s of per-figure time)
```

Expected: 16 CSVs and the accompanying JSON records rewritten in `figure_data/`, with a
final summary of row counts.  Failure modes and their meaning:

| Symptom | Meaning |
|---|---|
| `FileNotFoundError: ../a0/materials.json` | the folder layout was changed (§1) |
| `ValueError: H violates full 3D strict Schur bound` | a swept `H` was set outside `H_b` (should not happen with the shipped values) |
| `RuntimeError: rank deficiency` | a degenerate edge system: report it, do not regularise |

## 4. Regenerate the figures

```bash
python generate_final_figures.py     # ≈ 10 s
```

Expected: `fig01…fig10` in `pdf`, `png` and `svg` inside `figures_final/`.
**Size warning:** `fig10_field.svg` is ~29 MB (dense vector map).  It is intentionally
not shipped; the PDF (48 kB) and PNG are.

The delivered manuscript figures in `02_OVERLEAF/figures/` are byte-identical to
`08_FINAL_OUTPUTS/figures_final/*.pdf`, so nothing needs copying to compile the paper.
If you regenerate and want the new figures in the manuscript, copy them over:

```bash
cd ../..                       # archive root
cp 01_PROGRAM/paper_a_study/figures_final/fig*.pdf 02_OVERLEAF/figures/
```

(In the original source repository the same step was automated by
`01_PROGRAM/tools/build_submission_package.py`, which is shipped for the record; it
expects that repository's layout, not this archive's.)

## 5. Compile the manuscript (needs TeX)

```bash
cd 02_OVERLEAF
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Expected: a PDF, no undefined references, no undefined citations.
**In the environment where this archive was built there was no TeX engine at all**
(`pdflatex`, `latexmk`, `xelatex`, `lualatex`, `tectonic` all absent; not installable
from the available package sources).  The manuscript was therefore validated
**statically** and never compiled — see `02_OVERLEAF/README_OVERLEAF.md` §4.  To repeat
that static validation without TeX:

```bash
cd 02_OVERLEAF
python scripts/static_check.py          # exit 0, prints labels/refs/citations
```

## 6. Run the full verification battery

```bash
cd 01_PROGRAM
python paper_a_study/run_all_checks.py      # ≈ 15 min
```

Expected last lines:

```
PASS  22 checks
SKIP  1 check   (LaTeX build: no TeX engine found)
OVERALL: PASS
```

The log is written to `validation/verification_log.txt` relative to where you run it.
A SKIP for the TeX build is **not** a failure of the science; a FAIL anywhere else is a
real failure and the check prints its own diagnosis.

## 7. One-command orchestration

```bash
bash 04_REPRODUCTION/repro_test.sh
```

Runs §2–§6 in the correct order, keeps every log in `04_REPRODUCTION/logs/`, and prints a
final PASS/PARTIAL/FAIL summary.  It is what produced
`04_REPRODUCTION/REPRODUCTION_TEST_RESULT.md`.

## 8. Compare against the shipped numbers

Do not eyeball.  The shipped values are machine-readable:

```bash
python 04_REPRODUCTION/compare_outputs.py            # prints per-file agreement
```

It compares a fresh `figure_data/` against the shipped copies (SHA-256 and, where bytes
differ, field-by-field numeric agreement) and reports the maximum relative deviation.

## 9. What can legitimately differ

| Thing | Why it may differ | Does it matter? |
|---|---|---|
| last digits of a float | different BLAS/LAPACK/`libm` | no, if within `1e-12` relative |
| `build_log.json` timestamps, elapsed seconds in audit JSONs | wall clock | no |
| figure PDF/PNG/SVG bytes | embedded creation date and font subsetting | no; compare the data, not the bytes |
| `fig10_field.svg` size | matplotlib version | no |
| battery runtimes | machine | no |
| anything in the *physics* (`R_B`, `K_B`, `α`, partition, corner forces) | should not differ beyond the stated tolerance | **yes** — report it |

Tolerances to hold yourself to when comparing (they are the paper's own):
`R_B` degree spread `1.1e-6` relative; quadrature spread `1.7e-9`; restart spread
`3.2e-6`; edge residual `< 1e-12`; power balance `< 1e-12`.
