# PAPER_A_COMPLETE_REPRODUCIBILITY_ARCHIVE

One self-contained archive for a single-manuscript project: the program, the manuscript
source, the data, the derivations, the validation evidence, the final outputs and a
reproduction test.  Five years from now, this folder should be all you need.

**Project:** Paper A — backward-branch negative reflection of guided waves from the free
edge of a flexoelectric piezoelectric-semiconductor plate (ZnO, class 6mm), with the
carrier–strain-gradient coupling `Δn H_jkl ε_jk,l`.
**Archive version:** 1.0 · **built:** 2026-11-07 · **source state:** repository commit
`f0a61e4` (round 21) plus this round's verification run.
**Nothing here has been re-derived for the archive; the archive ships the state of record.**

---

## Read this first

| If you want to… | Go to |
|---|---|
| know what is and is not finished | `FINAL_PACKAGE_STATUS.md` |
| understand the physics | `07_DOCUMENTATION/MODEL_DESCRIPTION.md` |
| understand the numerics | `07_DOCUMENTATION/NUMERICAL_METHOD.md` |
| run it yourself | `04_REPRODUCTION/REPRODUCE_FROM_SCRATCH.md` |
| know the exact order and commands | `04_REPRODUCTION/RUN_ORDER.md` |
| see the reproduction test result | `04_REPRODUCTION/REPRODUCTION_TEST_RESULT.md` |
| compile the paper | `02_OVERLEAF/README_OVERLEAF.md` |
| find where a number comes from | `08_FINAL_OUTPUTS/FINAL_RESULTS_TABLE.csv`, `07_DOCUMENTATION/FIGURE_PROVENANCE.md` |
| check a file's integrity | `SHA256SUMS.txt`, `09_ARCHIVE_METADATA/file_manifest_sha256.csv` |
| know what was validated against what | `06_VALIDATION/VALIDATION_MATRIX.md` |
| see every parameter and its provenance | `09_ARCHIVE_METADATA/parameter_manifest.json` |

## Structure

```
PAPER_A_COMPLETE_REPRODUCIBILITY_ARCHIVE/
├── ARCHIVE_README.md               ← you are here
├── FINAL_PACKAGE_STATUS.md         measured status, limitations, recommended action
├── SHA256SUMS.txt                  sha256 of every file in the archive
├── 01_PROGRAM/                     solver, audits, tests, plotting, feasibility studies
│   ├── README_PROGRAM.md
│   ├── requirements.txt
│   ├── prepare_archive_layout.py   symlink shim so the battery runs inside the archive
│   ├── paper_a_study/              model.py + 38 scripts + claims/reference JSONs
│   ├── a0/                         material model, materials.json, A0 audit
│   ├── feasibility/a0r, a0s/       novelty and model-selection studies
│   └── tools/                      static_check, submission/archive builders
├── 02_OVERLEAF/                    main.tex, 8 sections, 10 figure PDFs, references.bib
│   ├── README_OVERLEAF.md
│   └── static_check.py             runs without TeX
├── 03_DATA/                        the data of record
│   ├── README_DATA.md
│   ├── DATA_DICTIONARY.md          every column, unit, meaning, provenance
│   ├── figure_data/                16 CSVs + 20 audit JSONs + baseline records
│   └── results_legacy/             rounds 4–12 outputs (historical, not quoted)
├── 04_REPRODUCTION/                install → data → figures → tests → compare
│   ├── REPRODUCE_FROM_SCRATCH.md
│   ├── RUN_ORDER.md
│   ├── repro_test.sh               one-command orchestration
│   ├── compare_outputs.py          numeric comparison against the shipped data
│   ├── make_run_manifest.py, make_parameter_manifest.py
│   └── logs/                       battery log of record + older logs
├── 05_DERIVATIONS/                 weak form, boundary variation, Gate 1 identity
│   └── README_DERIVATIONS.md
├── 06_VALIDATION/                  validation matrix + audit reports + logs
│   ├── README_VALIDATION.md
│   └── VALIDATION_MATRIX.md
├── 07_DOCUMENTATION/               model, numerics, figures, changelog, limitations
│   ├── PROJECT_OVERVIEW.md, MODEL_DESCRIPTION.md, NUMERICAL_METHOD.md
│   ├── FIGURE_PROVENANCE.md, CHANGELOG.md, KNOWN_LIMITATIONS.md
│   └── audit_history/              the dated round reports, unedited
├── 08_FINAL_OUTPUTS/               figures (pdf/png/svg), results table, package manifest
│   ├── README_FINAL_OUTPUTS.md
│   ├── FINAL_RESULTS_TABLE.csv
│   └── figures_final/
└── 09_ARCHIVE_METADATA/            run manifest, parameter manifest, integrity manifests
    ├── run_manifest.json
    ├── parameter_manifest.json
    ├── file_manifest_sha256.csv
    ├── BUILD_RECORD.md
    └── LICENSE_AND_AUTHORSHIP_NOTE.md
```

## Three sentences of substance

The calculation solves a 2.5D spectral Galerkin problem for the coupled
elastic–electric–carrier system at a free, charge-free edge and reports the backward
modal share at the reference plane `L = 10d = 2 µm`: `R_B = 0.9428718` at the certified
local maximum (`k_x d = 0.52719`, flat top `[0.5267, 0.5276]`) and `R_B = 0.0192916` at the
operating point.  It is **not** a reflectance: `R_B` is one member of the outgoing power
partition, and Fig. 5 reports the partition, whose closure residual is `1.3e-17`.  The
supporting claims are the reductions to closed-form limits (`1e-9`…`1e-10`), reciprocity at
`±k_y` (`1e-13`), an independent `H¹` mesh, degree/quadrature/restart spreads of
`1.1e-6 / 1.7e-9 / 3.2e-6`, and a corner result reported honestly as a **bounded closure**
(exponent ≈ −0.63), not as a resolved singularity.

## Two things that are not here, deliberately

1. **No `main.pdf`.**  No TeX engine existed in the build environment (`pdflatex`,
   `latexmk`, `xelatex`, `lualatex`, `tectonic` all absent and not installable).  The
   manuscript is statically validated only; the typeset layout is unverified.  No compiled
   PDF is claimed anywhere in this archive.
2. **No 29 MB `fig10_field.svg`.**  It regenerates in ~10 s and the manuscript does not
   use it.

## Quick start

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r 01_PROGRAM/requirements.txt
cd 01_PROGRAM && python prepare_archive_layout.py
python paper_a_study/run_all_checks.py        # ≈ 15 min → 22 PASS, 1 SKIP, OVERALL: PASS
```

Or, for the deliverables rather than the audits:

```bash
cd 02_OVERLEAF && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Integrity

```bash
sha256sum -c SHA256SUMS.txt                   # every file
python 04_REPRODUCTION/compare_outputs.py     # regenerated data vs shipped data
```

The archive's own build is described in `09_ARCHIVE_METADATA/BUILD_RECORD.md`; it is
reproducible with `01_PROGRAM/tools/build_repro_archive.py`.

**License / authorship:** not documented in the source repository; see
`09_ARCHIVE_METADATA/LICENSE_AND_AUTHORSHIP_NOTE.md`.  No third-party files are
redistributed; the material constants are quoted values with a DOI.
