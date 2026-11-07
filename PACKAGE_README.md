# Paper A — review package (round 12)

**Topic.** Negative reflection of guided waves at the free edge of a flexoelectric
piezoelectric–semiconductor plate: the strain-gradient backward branch, its modal-power partition and
the size of the carrier-coupling contribution.

**Authoritative manuscript.** `Paper_A_Final_Submission/main.tex` — one tree, seven section files,
ten vector figures, `references.bib`, `MANIFEST.json` (SHA-256 of every file in the package),
`static_validation.txt`. It is **statically validated and not compiled**: no TeX engine exists in the
authoring environment. Build with
`cd Paper_A_Final_Submission && pdflatex main && bibtex main && pdflatex main && pdflatex main`.
An earlier compiled PDF is not included and would not certify this source.

**Read first.** `START_HERE.txt` gives the reading order of this round's reports. Round 12 is a
section-by-section review of the manuscript — mathematics, physics, language and what a journal
requires — with two round-11 reporting defects corrected before any manuscript text was touched
(`PAPER_A_ROUND12_PRELIMINARY_EVIDENCE_CORRECTIONS.md`, which is where a reader should start). The
scientific content is unchanged: no equation, no constant, no boundary condition, no solver, no
dataset, no figure PDF and no reported number. Nineteen prose defects were repaired, twenty printed
numbers that disagreed with the delivered records among them; one frozen figure annotation defect is
reported and not repaired (`PAPER_A_ROUND12_BLOCKING_ISSUES.md`, B1).

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

# 1. the datasets (7 min on two cores).  Run this FIRST: the tests and the
#    figures read what it writes.
OMP_NUM_THREADS=1 .venv/bin/python paper_a_study/build_figure_data.py

# 2. the ten vector figures (10 s), then copy them into the manuscript
OMP_NUM_THREADS=1 .venv/bin/python paper_a_study/generate_final_figures.py
cp paper_a_study/figures_final/fig*.pdf Paper_A_Final_Submission/figures/

# 3. the 18 verification gates (13 min on two cores)
OMP_NUM_THREADS=1 .venv/bin/python paper_a_study/run_all_checks.py

# individually
.venv/bin/python -m unittest paper_a_study.test_model -v      # 47 tests, ~21 s
.venv/bin/python paper_a_study/claim_audit.py                 # 23 claims, 46 tokens
.venv/bin/python paper_a_study/mutation_tests.py              # 15 mutants, all caught
```

Run one solver script at a time. On two cores, two concurrent solver runs make each about ten times
slower and the peak search then exceeds its own timeout.

The round-11 battery was run **on freshly generated data, with nothing restored**, starting from an
empty `paper_a_study/figure_data/`. It returned **18 PASS, 0 FAIL, 1 SKIP** — the skip is the LaTeX
build, for which this environment has no engine. The run is recorded verbatim in
`validation/round11_battery_run_clean_reproduction.log`; the mutant record is in
`paper_a_study/figure_data/mutation_tests.json` (15 mutants, all caught) and the registry audit in
`paper_a_study/figure_data/claim_audit.json` (23 claims, 46 tokens, 11 of 11 source rows).

That PASS replaces the round-10 failure honestly rather than by restoring records. Round 10 failed
because the two refinement *spreads* — differences of nearly equal numbers lying on the round-off
floor — were registered as values and tested by a 1 % equality test; the headline meanwhile moved by
1e-13. Round 11 recomputed the quadrature spread at a fixed degree (it had pooled two degrees),
registered both spreads as **bounds** (<1e-8), taught the gate inequality semantics, and restated the
manuscript sentences as bounds. In the delivered run the degree spreads are 5.61e-9 and 6.22e-9 and
the quadrature spread is 4.32e-10, all below the registered bound, and mutation M13 shows the gate
still fails when a spread exceeds it.

---

## 3. What is in the package

| path | contents |
|---|---|
| `Paper_A_Final_Submission/` | the manuscript, its sections, figures, bibliography, `MANIFEST.json`, static validation output, and a copy of the solver and data it reads |
| `paper_a_study/` | the solver (`model.py`), the figure-data builder, the audit and verification scripts, the unit suite, the claim registry and the mutation harness |
| `paper_a_study/figure_data/` | every CSV and JSON the manuscript and figures are built from, including the search, certification, identity and matched-control records |
| `validation/` | the verification log of this delivery |
| `a0/`, `a0r/`, `a0s/` | completed historical studies, retained as review evidence; they are not part of the current result |
| `PAPER_A_ROUND12_*.md` | the seven reports of this round: preliminary evidence corrections (Part A), section-by-section review, edit ledger, numerical traceability audit, readiness assessment, blocking issues, correction history |
| `PAPER_A_ROUND11_*.md` | the eight reports of round 11: pre-edit programming audit, numerical reproducibility, figure-by-figure audit, panel-source matrix, claim registry, mutation and regression results, correction ledger, final readiness. Two of these carry "Corrected in round 12" annotations where round 11 mislabelled a reproducibility number |
| `PAPER_A_ROUND10_*.md` | the five reports of round 10: pre-edit audit, author style, structure comparison, edit log, closing audit |
| `PAPER_A_ROUND9_*.md`, `PAPER_A_ROUND8_*.md` | the earlier rounds, retained as review evidence |
| `PAPER_A_CORRECTION_HISTORY.md` | cumulative correction history, with the round-8 … round-11 addenda at the end |

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
  condition remain open, the LaTeX build is unverified, and five declarations await the author.
  Numerical readiness and scientific readiness are assessed separately in
  `PAPER_A_ROUND12_READINESS_ASSESSMENT.md`.
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
