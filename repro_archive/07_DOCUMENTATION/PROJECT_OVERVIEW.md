# PROJECT_OVERVIEW

**Project name:** Paper A
**Archive name:** `PAPER_A_COMPLETE_REPRODUCIBILITY_ARCHIVE`
**Archive version:** 1.0 (built 2026-11-07, from repository state `f0a61e4` + this round's verification run)
**Subject:** reflection of a shear-horizontal guided mode by the free edge of a
flexoelectric, strain-gradient, piezoelectric semiconductor plate (ZnO, class 6mm),
with the carrier–strain-gradient coupling `Δn H_jkl ε_jk,l`.

---

## 1. What the paper claims, and what it does not

The manuscript computes **one number and its provenance**: the share of the incident
shear-horizontal (SH) power that returns in the phase-conjugated backward channel when
a guided mode is reflected from a traction-free, charge-free edge of a ZnO plate.

| Quantity | Value | Where it is stored |
|---|---|---|
| `R_B` at the **operating point** (`K0 = 0.7362`, `Ω0 = 7.6334`) | **0.0192916** | `03_DATA/figure_data/peak_certification.json` → `verdict.operating_point.R_B_finest` |
| `R_B` at the **certified local maximum** of the frequency sweep (`k_x d = 0.52719`) | **0.9428718** | `03_DATA/figure_data/peak_search.json` → `verdict.R_B_at_max` |
| `R_B` at the edge plane, certified maximum | 0.9824311 | `03_DATA/figure_data/peak_identity_audit.json`, `claims.json: R_B_edge_certified_maximum` |
| `k_x d` of the backward channel | 0.2451746921716515 (`K_B0`) | `03_DATA/figure_data/peak_certification.json` |
| incident `k_x d` at the operating point | 0.7361990195318475 (`K0`) | `01_PROGRAM/paper_a_study/reference_constants.json` |
| incident `k_x d` at the certified maximum | 0.52719, flat top `[0.5267, 0.5276]` at the `1e-4` level | `03_DATA/figure_data/peak_search.json` → `plateau` |
| operating `k_y d` | 0.12981175031447484 (`K_Y0`) | `03_DATA/...` |
| operating `ω d/c_s` | 7.633372404423294 (`OMEGA0`) | `03_DATA/...` |
| operating frequency | 16.684 GHz at `d = 200 nm` | manuscript Table (dimensionless groups) |
| `R_B` at `k_x d = 0.55` (off peak) | 0.5519095 | `03_DATA/figure_data/peak_certification.json` → `verdict.k055_sample.R_B_finest` |

Novelty is claimed **only** for the reflection / edge-mode calculation of this
coupled system — not for the constitutive framework, not for the variational
statement, and not for the thermodynamic derivation, all of which follow published
work (see `06_VALIDATION/reports/` and the citation of the 2025 thermodynamic-
consistency paper in the manuscript).  The manuscript states this restriction
explicitly.

**Three limitations are stated in the manuscript and repeated here**
(`07_DOCUMENTATION/KNOWN_LIMITATIONS.md`): (i) `R_B` is a *modal share*, not a
reflectance — it is one member of the power partition, and the total propagating
share is reported separately (Fig. 5); (ii) the `H`-coupling is a single-component
phenomenological term, not a derived material model, and no value of `H` is sourced
from measurement (`a0/materials.json` marks it `NOT_SOURCED`); (iii) the "corner"
question is closed only as a **bounded closure** — the residual plateau is bounded
and the exponent is ≈ −0.63, not a proof of regularity
(`06_VALIDATION/reports/PAPER_A_ROUND21_FINAL_SUBMISSION_DECISION.md`).

## 2. Where everything is

| Folder | Contents | Start with |
|---|---|---|
| `01_PROGRAM` | full solver, audits, tests, plotting, submission builder, configs | `README_PROGRAM.md` |
| `02_OVERLEAF` | `main.tex`, `sections/`, `figures/`, `references.bib`, static checker | `README_OVERLEAF.md` |
| `03_DATA` | every CSV/JSON the figures and claims come from, legacy results | `README_DATA.md`, `DATA_DICTIONARY.md` |
| `04_REPRODUCTION` | install → run → regenerate → compare instructions, logs, test result | `REPRODUCE_FROM_SCRATCH.md` |
| `05_DERIVATIONS` | weak form, boundary variation, Gate 1 identity, hyperstress audits | `README_DERIVATIONS.md` |
| `06_VALIDATION` | validation matrix, audit reports, battery logs | `README_VALIDATION.md`, `VALIDATION_MATRIX.md` |
| `07_DOCUMENTATION` | model, numerics, figure provenance, changelog, limitations | this file, then `MODEL_DESCRIPTION.md` |
| `08_FINAL_OUTPUTS` | final figure PDFs/PNGs/SVGs, results table, package manifest | `README_FINAL_OUTPUTS.md` |
| `09_ARCHIVE_METADATA` | run manifest, parameter manifest, SHA-256 manifests, build record | `parameter_manifest.json` |

Root files: `ARCHIVE_README.md` (orientation), `FINAL_PACKAGE_STATUS.md`
(measured status and blockers), `SHA256SUMS.txt` (integrity of every file).

## 3. Status in one paragraph

The program runs end-to-end from a clean environment (22 checks PASS, 1 SKIP because
no TeX engine exists in the build environment), the figure data regenerate from the
solver, and the manuscript source passes static LaTeX validation (173 labels, 111
references, 13/13 citations resolved).  The manuscript has **never been compiled in
this environment**: no TeX engine was available, so no `main.pdf` is shipped and none
is claimed.  Full detail, including the exact reproduction verdict, is in
`FINAL_PACKAGE_STATUS.md` and `04_REPRODUCTION/REPRODUCTION_TEST_RESULT.md`.

## 4. Reading order for a reader five years from now

1. `ARCHIVE_README.md` → `FINAL_PACKAGE_STATUS.md` (what is and is not proved here)
2. `07_DOCUMENTATION/MODEL_DESCRIPTION.md` (the physics, all symbols, all units)
3. `07_DOCUMENTATION/NUMERICAL_METHOD.md` (the discretisation and tolerances)
4. `04_REPRODUCTION/REPRODUCE_FROM_SCRATCH.md` (run it yourself)
5. `06_VALIDATION/VALIDATION_MATRIX.md` (what was checked against what, and what was not)
6. `02_OVERLEAF/README_OVERLEAF.md` (compile the paper)
