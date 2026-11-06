# Paper A — Round 8: delivery and status

**Date:** 2026-11-06 · **Branch:** `arena/ea7ca4dd-a-paper` · **Baseline:** `f56fd8c` (round 7)
**Authoritative manuscript:** `Paper_A_Final_Submission/main.tex` (one tree, no second copy)
**Build status: BUILD UNVERIFIED** — no TeX engine exists in this environment. Nothing in this delivery
claims a PDF.

---

## 1. The full battery, re-executed

`python paper_a_study/run_all_checks.py` → `validation/verification_log.txt`, run
**2026-11-06T18:33:12Z**, total ≈ 11 min, **18 gates PASS, 1 SKIP (no TeX engine), OVERALL PASS**.

| gate | time | result |
|---|---|---|
| unit and scientific tests (26) | 14.7 s | PASS |
| dimensional and constitutive audit | 0.5 s | PASS |
| quasistatic justification | 0.4 s | PASS |
| flexoelectric control | 5.4 s | PASS |
| admissibility re-derivation (139 / 130 / 95 rows) | 0.0 s | PASS |
| figure data and figure files | — | PASS |
| phase-speed and e.m. reconciliation | 0.4 s | PASS |
| modal-flux rescaling proof | 10.6 s | PASS |
| mechanism matched controls | 217.6 s | PASS |
| corner assessment and regression | 13.1 s | PASS |
| **certified peak (four fixed wavenumbers)** | 15.6 s | PASS |
| **peak search and classification** | 330.6 s | PASS |
| **peak identity and artefact audit** | 22.3 s | PASS |
| spectral convergence | 9.1 s | PASS |
| quadrature sufficiency | 9.7 s | PASS |
| claim registry and stale guard (19 claims, 42 tokens) | 0.0 s | PASS |
| gate mutation tests (8 mutants, all caught) | 0.7 s | PASS |
| LaTeX static validation | 0.0 s | PASS |
| LaTeX build | — | **SKIP: no pdflatex / latexmk / tectonic / xelatex / lualatex** |

The three bold rows are new this round. The first battery attempt in this round *failed* at
`certified peak` with `ModuleNotFoundError: build_figure_data` — the script could not be run as a module —
and that failure is recorded rather than hidden: the script now bootstraps its own `sys.path` and the
re-run passes.

## 2. The deliverable

* **Manuscript:** `Paper_A_Final_Submission/` — `main.tex`, 8 section files, 10 vector PDF figures,
  `references.bib`, `MANIFEST.json`, `static_validation.txt`.
* **Fig. 4 regenerated only:** `figures/fig04_frequency.pdf`, 42 143 B, identical to
  `paper_a_study/figures_final/fig04_frequency.pdf` (md5 `39fcfb20adc66607dd6b8540126d7f68`), built from
  139 rows.
* **Data:** `paper_a_study/figure_data/` — including the two new records `peak_search.json` and
  `peak_identity_audit.json`.
* **Reports:** the seven `PAPER_A_ROUND8_*.md` files listed in `START_HERE.txt`, plus the round-8 addendum
  appended to `PAPER_A_CORRECTION_HISTORY.md`.
* **Archive:** `downloads/Paper_A_Complete_Project_round8.zip`, with `downloads/PACKAGE_SHA256.txt`
  beside it. The checksum is deliberately **not** inside the archive it describes; the authoritative
  size and digest are in `downloads/README.md` and `downloads/PACKAGE_SHA256.txt`.

## 3. What a reader can verify without re-running anything

| question | where the answer is stored |
|---|---|
| Is the maximum a maximum? | `peak_search.json → classification` (`certified_local_maximum`, flat top, scanned domain) |
| Could it be an artefact? | `peak_identity_audit.json → verdict` (plane invariance 2.4e-16, reconstruction 0.0, cond×ε 3.6e-14) |
| Is the number converged? | `peak_search.json → degree`, `quadrature`, `tracking_path`, `restarts` |
| Does the manuscript agree with the data? | `claim_audit.json → rows, source_rows, problems` |
| Do the gates actually fire? | `mutation_tests.json` (8 mutants, all CAUGHT) |
| Did anything fail? | `validation/verification_log.txt` (one line per gate, with times) |

## 4. Open items — stated, not smoothed

| item | status | why it is open |
|---|---|---|
| **Novelty / priority** | **UNRESOLVED** | the primary 2025 source is closed access; search absence is not evidence of novelty, and no claim is inferred from an abstract |
| **Corner-line boundary condition** | **not certified** | the corner band carries 0.9–1.3 % of the strain-gradient energy and its share drifts 6.6–6.8 % between degrees 18 and 30; no number in the paper depends on it beyond the third digit, and the abstract says so |
| **Material parameters** | **synthetic** | ℓ = 50 nm, f = 1 nC/m, H = 0.05 H* are labelled synthetic everywhere; no calibration is invented |
| **Experimental validation** | **absent** | this is a theory/numerics paper; no measurement is claimed, and numerical residuals 10⁻¹³–10⁻¹⁶ are never described as accuracy |
| **LaTeX build** | **UNVERIFIED** | no engine available; the static validator checks labels, refs, environments and citation keys only |
| **Non-authoritative material** | **AUTHOR INPUT REQUIRED** | funding, competing interests, CRediT, acknowledgements and any generative-tool disclosure are not in this delivery; they must be supplied by the authors and are kept out of the declarations until then |

## 5. What changed in the headline, in one paragraph

Round 7 said 93.19 % at k_xd = 0.525. That was the largest sample of a 0.01 raster. The response has a
flat top 10⁻³ wide, and a three-stage search places the maximum at **k_xd = 0.52752** with
**R_B = 0.9467954**, i.e. **94.68 %**, flat to 0.01 percentage point over [0.5266, 0.5277]. It is a
**certified local maximum** in the declared window and is not claimed to be global. At that point the
incident modal flux is **128 times smaller** than at the operating point, so the share is maximal where
the transported power is minimal; the paper now says this in the abstract, the results, the discussion and
the conclusions. The coupling's effect at the peak is −34.2 % at the reference plane and −11.1 % at the
edge plane, and the re-searched ceiling falls to 0.6244 / 0.7013 at the extremes of H.
