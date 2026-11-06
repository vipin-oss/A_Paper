# Paper A — progress and resume state

Updated: 2026-11-06.  Branch `arena/ea7ca4dd-a-paper`.

## Where the work stands

The manuscript is **complete in content** and **statically validated**, but it
has **never been compiled** (no TeX engine in the sandbox).  The submission
package reproduces from a clean extraction: 18/18 tests, static check PASS, and
a full rebuild of the figure data that is bit-identical to the shipped CSVs.

Do not restart the figure work.  The ten figures are final.

## Closed this phase

* **A** grounded/open labels in the manuscript corrected to match `model.py`
  (`ground` = `φ = 0` both faces, `np = n-2`; `open` = `D_z = 0`, constant mode
  dropped, `np = n-1`).
* **B** `sections/governing_equations.tex` rewritten: enthalpy, conjugates,
  hyperstress, `D`, `μ̃`, flux, balances, three surfaces of BCs, power flux,
  dimensionless groups, Schur stability.  Terminology: Fourier-reduced 3-D, not
  plane strain.
* **C** `build_figure_data.py::fig05` — three real bugs fixed (`L = REF_NORM`
  not `REF_NORM*p.d`; evanescent sum; closure from `total_power_left`).  Closure
  `~1` → `3.8e-16`.
* **D** peak certification: all four cases certified, degrees 18→30, max rel.
  change `7.2e-7` (`figure_data/peak_certification.json`).  `|angle| < 80°` gate
  replaced by the conservation bound in `certified_backward` and
  `reclassify_csv.admissible`.
* **E** three velocities separated; `v_p` is a magnitude, `v_g`/`v_E` are signed.
* **F** two solution routes demoted to consistency checks; independent checks
  (strong-form, C¹ FE plate) separated out.
* **G** provenance table added; synthetic `ℓ`, `f_33`, `H` declared.
* **I** package rebuilt with `a0/materials.json` and verified by re-running.
* **J** preamble fixed, `references.bib` rebuilt (9 real entries), appendix
  written, `scripts/static_check.py` PASS.

## Open

* **H** novelty vs Qu et al. / Fang & Wei — **UNRESOLVED**, declared in
  `discussion.tex`.  Primary equations not accessible.  No priority claim.
* **Compilation** — UNVERIFIED.  One attempt made and failed (no root, no repo
  access, no wheel-based engine).  Next environment with TeX:
  `pdflatex main && bibtex main && pdflatex main && pdflatex main`.
* Optional strengthening: justify `ℓ`, `f_33`, `H` against literature, or state
  the headline result in dimensionless form.

## Files that matter

| Path | Why |
|---|---|
| `Paper_A_LaTeX/main.tex` + `sections/` | the manuscript |
| `Paper_A_LaTeX/static_validation.txt` | PASS record |
| `Paper_A_Submission_2026-11-06/` | the submission directory |
| `Paper_A_Submission_2026-11-06.zip` | the distributable archive |
| `PAPER_A_FINAL_SCIENTIFIC_CORRECTION_AND_Q1_AUDIT.md` | itemised audit A–J |
| `paper_a_study/build_figure_data.py` | all physics that feeds the figures |
| `paper_a_study/certify_peak.py` | degree-refinement certification |
| `paper_a_study/reclassify_csv.py` | admissibility flags, no re-solving |
| `a0/materials.json` | material source of truth |

## Do not repeat

* Do not re-run `build_figure_data.py` unless the physics changes.
* Do not reintroduce an angle gate; the energy angle is a diagnostic only.
* Do not build the energy closure from `edge_power`.
* Do not add `.npy`/`.npz` dependencies to the reproduction path.
