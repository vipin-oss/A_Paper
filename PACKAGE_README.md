# Paper A — review package (round 9)

**Topic.** Negative reflection of guided waves at the free edge of a flexoelectric
piezoelectric–semiconductor plate: the strain-gradient backward branch, its modal-power partition and
the size of the carrier-coupling contribution.

**Authoritative manuscript.** `Paper_A_Final_Submission/main.tex` — one tree, seven section files,
ten vector figures, `references.bib`, `MANIFEST.json` (SHA-256 of every file in the package),
`static_validation.txt`. It is **statically validated and not compiled**: no TeX engine exists in the
authoring environment. Build with
`cd Paper_A_Final_Submission && pdflatex main && bibtex main && pdflatex main && pdflatex main`.
An earlier compiled PDF is not included and would not certify this source.

**Read first.** `START_HERE.txt` gives the reading order of the seven round-9 reports. The Stage-1
audit (`PAPER_A_ROUND9_STAGE1_NORMALIZATION_AUDIT.md`) is the one to read before anything else: it
documents, before any edit, the normalisation defect that round 9 repaired and why the headline is not
affected by it.

---

## 1. Headline result

`R_B = 0.9467952` (94.68 %) at `k_x d = 0.5275`, a **numerically certified local maximum** of the
backward-modal power share inside the declared search interval `0.465 < k_x d < 0.625`. The top is flat:
every sampled `k_x d` in `[0.5266, 0.5277]` lies within 0.01 percentage point of the maximum. This is
**not** a global maximum and **not** a statement that energy is turned around — the incident flux at the
maximum is 128 times smaller than at the operating point.

`R_B` is defined at a reference plane ten plate thicknesses from the edge. At the edge plane itself the
same solve gives 0.9855722; the two numbers are the same quantity at different planes and the manuscript
labels them by plane wherever they appear.

---

## 2. Reproduce everything

Python 3.11 with numpy, scipy and matplotlib (the authoring environment used numpy 2.4.6, scipy 1.17.1,
matplotlib 3.11.2).

```bash
python -m venv .venv && .venv/bin/pip install numpy scipy matplotlib

# 18 verification gates, one line each, ~5 min on two cores
OMP_NUM_THREADS=1 .venv/bin/python paper_a_study/run_all_checks.py

# the datasets and the ten vector figures
OMP_NUM_THREADS=1 .venv/bin/python paper_a_study/build_figure_data.py
OMP_NUM_THREADS=1 .venv/bin/python paper_a_study/generate_final_figures.py

# tests, registry, mutants, individually
.venv/bin/python -m unittest paper_a_study.test_model -v      # 39 tests, ~9 s
.venv/bin/python paper_a_study/claim_audit.py                 # 22 claims, 45 tokens
.venv/bin/python paper_a_study/mutation_tests.py              # 13 mutants, all caught
```

Run one solver script at a time. On two cores, two concurrent solver runs make each about ten times
slower and the peak search then exceeds its own timeout.

The gate results of this delivery are recorded in `validation/verification_log.txt`, the mutant record
in `paper_a_study/figure_data/mutation_tests.json`, and the registry audit in
`paper_a_study/figure_data/claim_audit.json`.

---

## 3. What is in the package

| path | contents |
|---|---|
| `Paper_A_Final_Submission/` | the manuscript, its sections, figures, bibliography, `MANIFEST.json`, static validation output, and a copy of the solver and data it reads |
| `paper_a_study/` | the solver (`model.py`), the figure-data builder, the audit and verification scripts, the unit suite, the claim registry and the mutation harness |
| `paper_a_study/figure_data/` | every CSV and JSON the manuscript and figures are built from, including the search, certification, identity and matched-control records |
| `validation/` | the verification log of this delivery |
| `a0/`, `a0r/`, `a0s/` | completed historical studies, retained as review evidence; they are not part of the current result |
| `PAPER_A_ROUND9_*.md` | the seven reports of this round |
| `PAPER_A_CORRECTION_HISTORY.md` | cumulative correction history, with the round-8 and round-9 addenda at the end |

---

## 4. Material parameters and provenance

Classical ZnO constants are the sourced elastic, piezoelectric and dielectric values used throughout;
the carrier model uses a density-dependent conductivity with `n_ref = 1e19 m^-3` at the operating
point. The following are **explicitly synthetic** and labelled as such in the manuscript: the
strain-gradient length `ℓ = 50 nm`, the strain-gradient tensor `A = ℓ² C ⊗ I`, the static flexoelectric
coefficient `f₃₃₃₃ = 1 nC/m`, and every value of the flexoelectric coupling `H`.
`H* = 4.0097064373759543e-22 J m` is defined at the fixed reference density. None of these is a
measured ZnO constant and no calibration is claimed.

The plate thickness is `d = 200 nm`; the reference plane is `L = 10` thicknesses.

---

## 5. Scope, and what this package does not claim

* **Not an experiment.** No measurement is claimed; numerical residuals of 1e-13–1e-17 are described as
  round-off, never as accuracy.
* **Not a global maximum.** The certified maximum is local, inside a declared interval, with a flat top.
* **Not a novelty claim.** The comparison with the primary 2025 source is **UNRESOLVED** (closed
  access). Absence from a search is not evidence of novelty, and no priority claim is made.
* **Not a submission-ready SCI Q1 manuscript.** The physics, the numbers and the internal consistency
  are verified as far as this environment allows; the novelty question and the corner-line boundary
  condition remain open, and the LaTeX build is unverified.
* **Corner line not certified.** The corner band carries 0.9–1.3 % of the strain-gradient energy and its
  share drifts 6.6–6.8 % between degrees 18 and 30; no quoted number depends on it beyond the third
  digit.
* **Author input required.** Funding, competing interests, CRediT and acknowledgements are not invented
  here and must be supplied by the authors.

---

## 6. Integrity

`MANIFEST.json` (inside the manuscript directory) lists the SHA-256 of every file in the package.
`PACKAGE_SHA256.txt`, delivered beside the archive rather than inside it, gives the digest and size of
the archive itself; a checksum cannot be embedded in the file it describes.
