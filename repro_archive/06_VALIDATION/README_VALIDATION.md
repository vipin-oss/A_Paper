# README_VALIDATION

The evidence folder: what was checked, against what, with which tolerance, and what was
not checked at all.  The one-page answer is `VALIDATION_MATRIX.md`; this file says how to
read the rest.

```
06_VALIDATION/
  VALIDATION_MATRIX.md        22 verification rows + 5 explicit "not validated" rows
  reports/                    the dated audit reports this archive depends on
  logs/                       the battery log of record (and older battery logs)
```

---

## 1. The four kinds of claim, and where each is defended

| Kind of claim | Example | Defence |
|---|---|---|
| **The code solves the stated equations** | discretisation, quadrature, mode classification | exact reductions (§1 rows 1–7), spectral/quadrature convergence (8–9), strong-form roots (3–4), reciprocity (5), FE cross-check (7), Gate 1 data identity (14) |
| **The number is converged** | `R_B = 0.9428718` at the peak | `peak_certification.json` (refinement ladder, four wavenumbers), `peak_search.json` (degree `1.1e-6`, quadrature `1.7e-9`, restart `3.2e-6`), flat-top plateau `[0.5267, 0.5276]` |
| **The number means what it says** | it is a modal share, not a reflectance | `fig05_channel_power.csv` (full partition with closure residual `1.3e-17`), `peak_identity_audit.json`, and the naming tests (`test_backward_share_is_never_called_a_reflectance`) |
| **The paper's text matches the data** | every quoted number | `claims.json` + `claim_audit.py` (10/10 source-agreement), `static_check.py` (labels, refs, citations) |

## 2. The reports in `reports/`, and their status

These are dated audit records, not current statements.  Where a report's number differs
from a value in `03_DATA/figure_data/`, the **stored record wins**; the report's round
tells you what the state of knowledge was at that date.

| Report | What it establishes | Status |
|---|---|---|
| `PAPER_A_ROUND21_FINAL_SUBMISSION_DECISION.md` | final classification **B**; the deliverable set; the 22 PASS / 1 SKIP battery | **current** (latest) |
| `PAPER_A_ROUND21_GATE1_DERIVATION.md` (in `05_DERIVATIONS/`) | the natural-boundary identity, derived | current |
| `PAPER_A_ROUND20_FINAL_SUPERVISOR_DECISION.md` | what round 20 changed and why | historical (superseded by round 21) |
| `PAPER_A_ROUND20_ELECTRICAL_EDGE_CONDITION_AUDIT.md` | the edge condition changed from `ground` to `insulating`; the numerical impact | current (the model of record) |
| `PAPER_A_ROUND20_NUMERICAL_IMPACT_AND_RECOMPUTATION.md` | what had to be recomputed after that change | current |
| `PAPER_A_ROUND20_PRE_EDIT_BOUNDARY_AUDIT.md`, `…_SPATIAL_SPECTRAL_COUNT_AUDIT.md` | pre-edit state; the 182-root count | historical record of the defect and its repair |
| `PAPER_A_ROUND20_HYPERSTRESS_AND_CORNER_AUDIT.md`, `…_FACE_VS_EDGE_NORMAL_AUDIT.md` (in `05_DERIVATIONS/`) | hyperstress and corner normal | current |
| `PAPER_A_EXTENDED_NUMERICAL_VALIDATION.md` | the extended check set | current |
| `PAPER_A_ROUND9_PLANE_INVARIANCE_VALIDATION.md` | plane-invariance of the partition | current (identity re-tested in the suite) |
| `PAPER_A_CLAIM_PROVENANCE_MATRIX.md` | claim → data → manuscript mapping | current |
| `FIGURE_5_VALIDATION_REPORT.md`, `figure_validation_report.json` | figure 5 (the partition) audited against its own closure | current |
| `static_validation.txt` | the last `static_check.py` output | current |

## 3. The logs

`logs/verification_log.txt` is the battery output of record.  It prints one line per
check, the measured numbers of the important ones, and ends with `OVERALL: PASS`.
Older logs (`verification_run_*.txt`) are kept to show that the present state is not a
one-off.  A SKIP line for `LaTeX build` means **no TeX engine was present**; it is not a
pass and it is not a failure of the science.

## 4. What a reader should distrust first

Stated plainly, because it is the point of this folder:

1. **The typeset paper.**  Never compiled here. Layout unverified.
2. **The `H`-coupling magnitudes.**  No measured `H` or `f` for ZnO; all values are
   modelling choices, and the sweeps exist because of that.
3. **The corner.**  Bounded closure, exponent ≈ −0.63 — not a proof of regularity and not
   a converged singular field.
4. **Anything in `03_DATA/results_legacy/`.**  Superseded; kept for the audit trail only.
5. **The word "reflectance".**  `R_B` is a modal share. If a sentence anywhere in the
   archive calls it a reflectance, that sentence is wrong and the tests say so.
