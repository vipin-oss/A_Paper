# CHANGELOG

Version history of the science, the code, the parameters, the figures and the
manuscript — in that order of importance, with the reason for each change.

**A historical changelog IS available** for the whole project: this file is the index,
and `PAPER_A_CORRECTION_HISTORY.md` (shipped alongside, in this folder) is the
item-by-item record for rounds 7–13 with an explicit "not corrected, deliberately"
section.  Rounds 14–21 have one decision report each, listed below and included under
`06_VALIDATION/reports/` and `05_DERIVATIONS/`.

Versioning scheme: the project has no semantic version numbers; it is organised in
**rounds**, each ending in a supervisor/decision report.  The archive is a snapshot of
the state after round 21.

---

## Archive v1.0 — 2026-11-07 (this package)

**Two consistency defects were found while assembling the archive, and fixed:**

1. **The manuscript's figure copies were stale.**  Three of the ten PDFs in
   `Paper_A_Final_Submission/figures/` (fig02, fig07, fig08) were older renders whose
   annotation text differed from the program's canonical figures — e.g. fig08 carried
   "all five H/H* levels: profiles agree to <0.9% of the peak" while the canonical render
   says "the five H/H* levels coincide in (a)–(c): agreement to <0.9% of the peak value".
   The ten PDFs were refreshed from `paper_a_study/figures_final/` and the submission
   `MANIFEST.json` rebuilt (88 entries); all ten pairs are now byte-identical.
2. **Two copies of the styling module existed.**  `Paper_A_Final_Submission/scripts/
   figure_style.py` was a 102-line earlier version of the 275-line canonical
   `paper_a_study/figure_style.py`.  The canonical file was copied into the package
   (identical SHA-256), the submission manifest rebuilt, and the archive ships one copy
   only.

Neither defect changed any reported number: the figure *data* were already consistent, and
`claim_audit` (10/10 source-agreement) and `static_check` (PASS) were re-run after both
fixes.


**New.** Single self-contained reproducibility archive: nine folders, all required
READMEs and manifests, SHA-256 for every file, an isolated reproduction test, and this
changelog index.  Nothing scientific was changed in this build; the only new code is
`01_PROGRAM/tools/build_repro_archive.py` (produces this archive),
`01_PROGRAM/prepare_archive_layout.py` (symlink shim so the battery runs inside the
archive) and `04_REPRODUCTION/compare_outputs.py` (numeric comparison of a regenerated
`figure_data/` against the shipped copy).

## Round 21 — final submission decision (classification **B**)

* Gate 1 (natural boundary data identity) derived and executed:
  incident `5.7e-14…1.3e-12`, worst reflected `8.9e-9…3.5e-6`, plain pointwise traction
  `1.7e+1` — i.e. the pointwise check was the wrong test, and the identity is the right
  one.
* Gate 2 (corner line force) executed at `n = 10, 28` for three configurations:
  `8.42e-2/3.27e-3/3.79e-2 → 4.46e-2/1.71e-3/1.98e-2`, exponent ≈ −0.63, partition
  moves `3.9e-6`.  Verdict: **bounded closure** — not "resolved".
* Gate 3: insulating edge confirmed as the default the manuscript describes.
* Manuscript: limitation rewrites, novelty paragraph restricted to the
  reflection/edge-mode calculation, `B` defined as the negative-real-part component
  amplitude, norms placed before equations, `φ` introduced as the quasi-Fermi potential
  with the external `V`, ±1/4-percent/pp bracketing, and all "exact / rigorous / to
  machine precision" phrasing removed from abstract, introduction and conclusions.
* Registry: 40 live claims, 6 deprecated; `claim_audit` 10/10 source-agreement.
* Battery: 22 PASS, 1 SKIP (no TeX engine), `OVERALL: PASS`.
* Report: `06_VALIDATION/reports/PAPER_A_ROUND21_FINAL_SUBMISSION_DECISION.md`.

## Round 20 — boundary audit and repair

* **Found a real defect**: the edge boundary data had been checked pointwise against
  tractions, which is not what the weak solution satisfies; and the face normal and the
  edge normal had been used interchangeably in one derivation.
* The electrical condition on the reflecting edge was changed from `ground` to
  `insulating` as the **model of record**; `ground` is retained only to reproduce the
  round-19 baseline.  Consequences recomputed (`…_NUMERICAL_IMPACT_AND_RECOMPUTATION`).
* Variational boundary derivation rewritten; hyperstress and corner audit re-derived.
* The charge-free edge converges more slowly than the grounded one (`1.06e-7` vs
  `3e-8`), so the degree-convergence bound in the test suite was re-stated at the
  measured level (`2e-7`).  The tolerance was re-stated, **not** the result.
* Reports: `PAPER_A_ROUND20_FINAL_SUPERVISOR_DECISION.md`,
  `…_ELECTRICAL_EDGE_CONDITION_AUDIT.md`, `…_NUMERICAL_IMPACT_AND_RECOMPUTATION.md`,
  `…_PRE_EDIT_BOUNDARY_AUDIT.md`, `…_SPATIAL_SPECTRAL_COUNT_AUDIT.md`,
  `…_HYPERSTRESS_AND_CORNER_AUDIT.md`, `…_FACE_VS_EDGE_NORMAL_AUDIT.md`,
  `…_VARIATIONAL_BOUNDARY_DERIVATION.md`.

## Round 19 — targeted mathematical repair

* Hyperstress/boundary audit raised the boundary-data question that round 20 answered;
  modal power recalculated; polynomial operator audited; edge system verified; LaTeX
  layout repaired without changing content.
* **Still unverified**: no build (no TeX engine).
* Reports: `PAPER_A_ROUND19_FINAL.md`, `…_HYPERSTRESS_AND_BOUNDARY_AUDIT.md`,
  `…_MODAL_POWER_RECALCULATION.md`, `…_POLYNOMIAL_OPERATOR_AUDIT.md`,
  `…_EDGE_SYSTEM_VERIFICATION.md`, `…_PRE_EDIT_VERIFICATION.md`,
  `…_LATEX_AND_LAYOUT_REPAIR.md`.

## Round 18 — mathematical repair and independent recheck

* Carrier sign, weak-form block entries and reference checks re-derived independently
  (`round18_reference_checks.py`), including the Schur bound and the Legendre measures.
* Correctness verdicts recorded per claim type; **bounded closure** introduced as the
  only admissible wording for the corner.
* Reports: `PAPER_A_ROUND18_FINAL_SUPERVISOR_REVIEW.md`, `…_MATHEMATICAL_REPAIR.md`,
  `…_INDEPENDENT_RECHECK.md`, `…_CORRECTNESS_VERDICTS.md`, `…_PRE_EDIT_AUDIT.md`,
  `…_REGRESSION_AND_PACKAGE.md`.

## Round 17 — derivations, tables, limitations

* Derivations completed and worked calculations written out; table and limitation
  corrections; figure zoom/overlap audit; manuscript restructured.
* Reports: `PAPER_A_ROUND17_FINAL_SUPERVISOR_REVIEW.md`,
  `…_MATHEMATICAL_DERIVATIONS.md`, `…_WORKED_CALCULATIONS.md`,
  `…_TABLE_AND_LIMITATION_CORRECTIONS.md`, `…_MANUSCRIPT_RESTRUCTURING.md`,
  `…_FIGURE_ZOOM_AND_OVERLAP_AUDIT.md`.

## Round 16 — conventions, dimensions, carrier equation

* Conventions and dimensions fixed; carrier strong→weak derivation written; carrier
  operator compared with an independent form; mechanical/Gauss audit.
* Reports: `PAPER_A_ROUND16_SUPERVISOR_DECISION.md`, `…_CONVENTIONS_AND_DIMENSIONS.md`,
  `…_CARRIER_STRONG_TO_WEAK_DERIVATION.md`, `…_CARRIER_OPERATOR_COMPARISON.md`,
  `…_MECHANICAL_AND_GAUSS_AUDIT.md`, `…_CORRECTION_HISTORY.md`.

## Round 15 — complete coupled weak form

* All three weak equations and every surface term written out; boundary variation and
  corner audit begun; independent mathematical audit; nomenclature and LaTeX audit.
* Reports: `PAPER_A_ROUND15_SUPERVISOR_DECISION.md`,
  `…_COMPLETE_COUPLED_WEAK_FORM.md`, `…_BOUNDARY_VARIATION_AND_CORNER_AUDIT.md`,
  `…_INDEPENDENT_MATHEMATICAL_AUDIT.md`, `…_PRE_EDIT_MATHEMATICAL_AUDIT.md`,
  `…_LATEX_AND_NOMENCLATURE_AUDIT.md`, `…_FIGURE_5_8_VISUAL_REVIEW.md`.

## Round 14 — derivation verification, figure redesign

* `…_DERIVATION_VERIFICATION.md`, `…_MATHEMATICAL_DERIVATION_MATRIX.md`,
  `…_FIGURE_REDESIGN_AUDIT.md`, `…_FINAL_MANUSCRIPT_PRESENTATION_REVIEW.md`,
  `…_MANUSCRIPT_STRUCTURE_CHANGES.md`, `…_AUTHOR_STYLE_AND_PRESENTATION_FAILURE_AUDIT.md`.

## Rounds 7–13 — corrections, reproducibility, figures

Item-by-item record in `PAPER_A_CORRECTION_HISTORY.md`; the corrections that changed a
reported number were:

| ID | Correction | Effect |
|---|---|---|
| C-1 (round 7) | the backward-channel maximum was mislocated | superseded by the round-8 addendum |
| C-2 (round 7) | size and mechanism of the coupling effect | the `H`-sweep replaced a single-point claim |
| C-3 (round 7) | total outgoing power in the abstract | corrected |
| C-4, C-5, C-6 | zero-group-velocity location, flexoelectric contribution at the peak, rounded partition | corrected |
| round 8 | **headline replaced**: the certified maximum supersedes C-1 | `R_B = 0.9428718` at `k_x d = 0.52719`, flat top `[0.5267, 0.5276]` |
| round 9 | the plane transform of a modal-power **ratio** derived | the `exp(2Im k L)` factors and the `incident_survival` direction corrected; the wrong `α` from `Im√(K²+ky²)` discontinued |
| round 11 | programming audit: figure panels regenerated from the solver, panel-source map created | `figure_panel_sources.json` |
| round 12 | section-by-section review; numerical traceability | `claims.json` registry begun |
| round 13 | Fig. 10(c), docstrings, packaging | vector verification, package build |

Deliberately *not* changed (recorded in `PAPER_A_CORRECTION_HISTORY.md` §E): the
linearised carrier equation, the single-component flexoelectric specialisation, and the
absence of a measured `H`.

## Parameter changes worth knowing

| Parameter | Old | New | When / why |
|---|---|---|---|
| edge electrical condition | `ground` | `insulating` | round 20; the free edge of an unmetalised plate is charge-free |
| reference plane | not fixed in early versions | `L = 10 d = 2 µm` | round 9; both channels evaluated at the same plane |
| attenuation | `Im√(K² + ky²)` (identically zero for real `K`) | `α = 2|Im k_x|` from the complex spatial root | round 9 |
| `incident_survival` | reciprocal (≥ 1) | `exp(−2 Im k_i ℓ) ≤ 1` | round 9 |
| group speed | `c_s dω/dk / |k|³` | `c_s dω/dK` central differences | round 11 |
| energy speed column | duplicated phase speed | `c_s P_x/E` | round 11 |
| `H` normalisation | ad hoc | `H* = H_bound/√5`, swept `|H/H*| ≤ 0.05` | round 8 |

## Figure changes

* Round 11: all ten figures regenerated from `build_figure_data.py` (no transcribed
  numbers), four panels each, explicit panel map.
* Round 14: redesign pass (fonts, panel labels, colour cycle, no ink at the canvas edge).
* Round 17: zoom/overlap audit.
* Round 21: fig. 5 partition annotated with the closure residual; fig. 9 residual panels
  declare their round-off floor.

## Manuscript changes

Round 10 (presentation only), 12 (section review), 14 (structure), 17 (restructuring,
tables, limitations), 19 (layout repair), 20 (boundary statements re-derived),
21 (novelty paragraph, limitations, "exact/rigorous" removal, bracketing).  The
preamble repairs that fix hard build errors (`\sisetup` instead of `\siunitxsetup`;
`\vect` as an alias instead of redefining `\boldsymbol`) are recorded in
`02_OVERLEAF/README_OVERLEAF.md` §4.
