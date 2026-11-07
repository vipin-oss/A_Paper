# Paper A — Round 11: final technical readiness

Date: 2026-11-07 · Branch `arena/ea7ca4dd-a-paper` · base commit `1ff9166a5bdf27d5d3ed0adeb21472719654bfeb`

---

## Verdict

The implementation, the datasets and the ten figures of Paper A are **internally
consistent, reproducible from an empty data directory, and guarded against every
defect found in this round and in the nine before it**. The manuscript's quantitative
statements now agree with the data of the figures they cite: three sentences were
corrected because their own data contradicted them.

The paper is **not submission-ready**, and this round does not move it closer by
editing prose. The three reasons remain what they were: the novelty against the
primary 2025 source is **UNRESOLVED** (closed access), the corner line-force
behaviour is unresolved, and the strain-gradient length, frequency and coupling are
synthetic rather than experimentally calibrated.

The typeset manuscript is **BUILD UNVERIFIED**: no TeX engine exists in this
environment. No PDF is included and none is claimed.

---

## What is proven

| claim | evidence |
|---|---|
| The delivered data regenerate from an empty directory | `PAPER_A_ROUND11_NUMERICAL_REPRODUCIBILITY.md` §1–2: every plotted column reproduces to ≤ 4 × 10⁻⁶ relative, the dispersion frequency bit for bit |
| The battery passes on that regenerated data, nothing restored | 18 PASS / 0 FAIL / 1 SKIP, `OVERALL: PASS`, `validation/round11_battery_run_clean_reproduction.log` |
| The headline is stable across runs | 0.9467953685099261 → 0.9467952305821763 ($1.5\times10^{-7}$), same classification, same $k_xd=0.52752$ |
| The refinement bounds are real bounds | degree spreads 5.61e−9 and 6.22e−9 against a registered bound of 1e−8; quadrature 4.32e−10; mutant M13 fails when a spread exceeds its bound |
| The manuscript and the records agree | 23 claims, 46 tokens, 11 of 11 source-agreement rows, 5 deprecated values still guarded |
| The figures say what they plot | 8 label/graphic defects repaired, panel map generated from the code, 8 provenance tests, 15 mutants caught |
| The package is intact | 223 entries, ≈3.0 MB, `unzip -t` clean, 80/80 manifest re-hash performed on the extracted archive, exactly one `main.tex`, `static_check` exit 0 (104 labels, 75 references, 13 citations) |

---

## What changed, in one paragraph per file

* **`sections/results.tex`** — five sentences: the coupling-induced frequency shift
  (60 kHz → 184 kHz / 1.1 × 10⁻⁵), the $v_g$–$v_E$ agreement (3.5 % over the whole
  branch → 3.5 % except the lowest sample at 6.4 %), the gradient-length
  percentages at the actual abscissae, and the two refinement spreads restated as
  bounds. Nothing else.
* **`sections/discussion.tex`** — one sentence, the same frequency shift.
* **`sections/conclusions.tex`** — one clause, the same bound.
* **`generate_final_figures.py`** — eleven lines of labelling, one inset limit, one
  margin, one floor band, and the panel-source table; no plotted value changed.
* **`claims.json`** — two claims reclassified as bounds, one claim added.
* **`claim_audit.py`** — inequality semantics for bounds, the degree spread tested at
  both recorded wavenumbers, the new source row.
* **`test_model.py`** — eight figure-provenance tests (47 in all).
* **`mutation_tests.py`** — two mutants (15 in all).
* **`run_all_checks.py`** — the test gate moved after the producers; docstring order
  corrected.
* **`regenerate_revised_data.py`** — marked superseded, refuses to run without an
  explicit opt-in.

The model, the governing equations, the boundary conditions, the Galerkin scheme,
the quadrature order and every solver parameter are untouched.

---

## The eight reports of this round

1. `PAPER_A_ROUND11_STAGE1_PROGRAMMING_AND_FIGURE_AUDIT.md` — 28 items audited before any edit
2. `PAPER_A_ROUND11_NUMERICAL_REPRODUCIBILITY.md` — the clean reproduction and the data comparison
3. `PAPER_A_ROUND11_FIGURE_BY_FIGURE_AUDIT.md` — ten figures, forty panels, status per panel
4. `PAPER_A_ROUND11_PANEL_SOURCE_MATRIX.md` — which column every panel plots
5. `PAPER_A_ROUND11_CLAIM_REGISTRY_CORRECTION.md` — categories A–E, bounds, tolerances
6. `PAPER_A_ROUND11_MUTATION_AND_REGRESSION_RESULTS.md` — 15 mutants, 47 tests, anti-regression list
7. `PAPER_A_ROUND11_CORRECTION_HISTORY.md` — every change with its evidence
8. `PAPER_A_ROUND11_FINAL_TECHNICAL_READINESS.md` — this file

The cumulative `PAPER_A_CORRECTION_HISTORY.md` carries the round-11 addendum at its
end (append-only, nothing overwritten).

---

## Package

```
downloads/Paper_A_Complete_Project_round11.zip
223 entries · 3,027,211 bytes · 3.03 MB
SHA-256: printed in downloads/README.md and in the delivery message
```

The archive cannot carry its own checksum, so the SHA-256 is recorded beside it in
`downloads/README.md` and in the delivery message; every other check is performed on
the archive itself.

Verification performed on the archive itself: `unzip -t` (no errors), extraction to a
scratch directory, 80/80 `MANIFEST.json` hashes recomputed from the extracted tree,
exactly one `main.tex`, `scripts/static_check.py` exit 0 (104 labels, 75 references,
13 citations, 13 bib entries).

One-click link (direct, no checkout, no Git client needed):

`https://github.com/vipin-oss/A_Paper/raw/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round11.zip`

Supersedes the round-10 archive (`81d2452a…48c2`), which superseded round 9.

---

## Open items, carried forward unchanged

| item | status |
|---|---|
| novelty against the primary 2025 source (closed access) | **UNRESOLVED** — no priority claim is made anywhere |
| corner line-force / free-edge idealisation | unresolved; the corner band (1.22–1.30 %) is reported as a band, not a value |
| $\ell$, $f$ and $H/H^*$ are synthetic | no experimental sensitivity is inferred from them |
| the maximum is **local** | "local maximum of the declared window" throughout; never global |
| 94.68 % is a backward **modal-power share** | not a reflectance; the incident flux at the maximum is 128× smaller than at the operating point |
| typeset PDF | **BUILD UNVERIFIED** — no engine; build with `pdflatex main && bibtex main && pdflatex main && pdflatex main` |
| submission readiness | **not claimed** |

---

## Stop

Round 11 stops here, at a clean tree, a passing battery on freshly generated data, a
verified archive and a pushed commit. Round 12 has not begun and must not begin
without the supervisor's instruction.
