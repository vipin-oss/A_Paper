# HANDOFF NOTES -- Paper A (read this first when resuming)

Paper: *Backward-branch negative reflection of guided waves from the free edge of a
flexoelectric piezoelectric semiconductor plate.*  Author: Dr Vipin Gupta
(vipin@gurugramuniversity.ac.in; writes Hinglish, reply in Hinglish).  Repo:
https://github.com/vipin-oss/A_Paper.  Status: **submission-ready except the user-owned fields below.**

## 1. Layout
- `02_MANUSCRIPT/` master LaTeX (`main.tex`, `sections/`, `references.bib`, `figures/`), `PAPER_A.pdf` (48 pages, 12 pt).
  Build: `pdflatex main && bibtex main && pdflatex main && pdflatex main`.  Must give Overfull 0, undefined 0.
- `01_PROGRAM/paper_a_study/` solver (`model.py`), figure data builder, all audits, tests, `fe2d*.py`.
- `01_PROGRAM/Paper_A_Final_Submission/` synced copy of `main.tex` + `sections/` (read by static checks).
- `03_EXPECTED_OUTPUTS/` reference outputs.  `README_START_HERE.md` how to run.

## 2. Headline numbers (all reproduced by the code)
- Operating point: k_x d = 0.7362, f = 16.68412 GHz, R_B = 0.0192916 (d = 200 nm, l = 50 nm, n0 = 2e18 m^-3,
  mu = 0.0175 m^2/Vs, insulating edge, Galerkin degree 22).
- ZGV fold: k_x d = 0.52719, f = 16.6547 GHz, R_B = 0.94287 -- a **modal share, not a reflectance**.
- Edge convention: plate in x<0, fields ~ e^{iKx}, outgoing modes Im K < 0.

## 2b. v15 restructuring (author request, 12 pt, 62 -> 54 pages)
- No separate Discussion section: mechanism/observable text moved into the results (end of "branch maximum" subsection),
  literature + Qu-2025 comparison moved to the end of the Introduction, parameter provenance is now a prose paragraph
  (`sec:params`, after Table `tab:groups`), limitations are 5 bullets at the end of Conclusions.
- Tables removed (their numbers are in the text/figures): refinement, lambda_path, n0wide, eta_loss, provenance.
- Equations not referenced anywhere are unnumbered (starred); appendix "worked matrix elements" and "end-to-end evaluation" removed.
- `claims.json` was re-pointed to the new locations; claim_audit PASS.  `static_check.py` whitelist gained nonumber, sloppy.
- Overleaf copy of the manuscript lives in repo `vipin-oss/PAPER_12_OVERLEAF_SUBMISSION` (same files as `SUBMISSION_PACKAGES`).

## 3. 2D finite-element validation (added in v13)
- `fe2d.py` / `fe2d_validate.py`.  Operating point: FE R_B agrees with modal value within -0.14 % .. +0.42 %
  over sponge length/strength, x-resolution, spline degree, thickness basis (spectral and C1), edge cell
  0.02 d -> 0.00125 d (Table tab:fe2d, `figure_data/fe2d_validation.csv`).
- **Pitfall found:** when refining `first_len`, scale `n_graded` so the last graded cell is about the uniform
  cell (0.4 d): `ng = ceil(1 + ln(0.4/fl)/ln 1.6)`.  Unscaled grading gave false +7 %/+112 % "errors".
- Standard PML fails for backward waves; a long (170 d) mass-proportional sponge is used.
- **Not validated:** the fold (incident and backward modes coincide; the modal fit is ill-posed there; FE gave
  0.64-0.72 vs 0.943 and that is NOT evidence against the modal result).  The paper states the check is
  operating-point only.  Do not claim more.

## 4. Standing rules from the author
- Diplomatic tone.  Do not follow GPT/other-LLM review blindly.  No proactive reviewer-anticipating text.
- Never invent numbers, references or DOIs.  Every bib entry must have a DOI (currently 61/61 do).
- At most 4 self-citations of Vipin Gupta, each in a different place (currently 4: gupta2027ellipsoidal, gupta2025psvoid,
  gupta2026heatmap, aldandani2026kg).
- Wang 2025 (Rayleigh) removed, approved.  Do only mandatory changes; skip optional ones.
- Declined: adding a "big name" author to avoid desk rejection (guest authorship is misconduct).
- The AI declaration in `main.tex` is written; the author reviews it.

## 5. The author fills in himself (left as template in `main.tex`)
Author name / affiliation / corresponding author, acknowledgement, funding, CRediT statement, competing
interests, licence/DOI.  The manuscript does NOT refer to the program or data: the author submits the paper only, so the data-availability line says data are included in the article and further detail is available on reasonable request (the author may edit it to the journal's wording). Nothing in the text may cite a script, file, repository or dataset.
Journal: not fixed (AMM was the first target; alternatives suggested: JASA, JSV, IJES, IJSS, JMPS, Wave Motion,
PRB/JAP).  Q1 / ranking status was **not verified**.  Reformat to the chosen journal's template and check
its guidelines (word/page limits, highlights, graphical abstract) -- `HIGHLIGHTS.txt` exists.

## 6. Known open items (honest list)
- Biswas DOI (10.1177/10812865251315937) browser check by the author.
- n0 >= 2e21 fold maximum is only a lower bound.  Observable flux / beat-length analysis not done.
- Corner line force decays only algebraically (about n^-0.62) and is bounded, not proven zero; stated in
  the Conclusions limitations.  Free edge is satisfied weakly.
- Physical parameters (l, flexoelectric constant, coupling H) are assumed values, as the paper says.
- T = 301.72 K recompute not redone.  Overleaf compile not tested by the author.

## 7. Checks to run after ANY edit
1. 02_MANUSCRIPT: 4-step build; Overfull 0; no `undefined`.
2. `cd 01_PROGRAM && python3 verify_paper_a.py` -> 46/46.
3. `cd paper_a_study && python3 -m pytest test_model.py -q`; `python3 claim_audit.py` PASS; `python3 test_review_regressions.py` OK.
4. `python3 paper_a_study/run_all_checks.py` -> OVERALL: PASS (about 10 min).
5. Copy `main.tex` + `sections/` to `Paper_A_Final_Submission/`; copy `main.pdf` to `PAPER_A.pdf`.

## 8. Final state (this session)
- Manuscript is 12 pt, 48 pages, no Discussion section, no appendix on data/code.  Introduction and Sections 2-5 were
  revised section by section by the author with outside language review; only genuine issues were adopted:
  generalized traction for arbitrary normal n, J_x notation, reduced single-component (f_3zz, H_zzz) statement,
  assembled-operator degree count, orthonormal basis b_j = sqrt(2j+1) P_j with degree n and N = n+1, gradient index l,
  density/mobility equivalence qualified, angle convention, Conclusions claim strength (local maximum; 0.943 is the
  lossless-elastic baseline and an optimistic estimate; flux balance independent, interference term is a remainder).
- Extra checks added (scripts `extra_checks.py`, `extra_loss_refine.py`, data in `figure_data/extra_*.json`): the
  mode-classification tolerance tau from 1e-9 to 1e-6 changes nothing; the share is smooth through the fold; the
  structural-loss scan refined to 0.6003 and 0.1967.  `model.py` reads the tolerance from `Plate.modal_tol` (default 2e-8).
- Not done (would need new computation, optional): through-thickness flux decomposition by contribution; separate
  density-only and mobility-only fold sweeps; fold validation by 2D FE (only the operating point is validated).
- Workflow rule: edit in `paper_12_overleaf_submission` (GitHub, Overleaf-synced), `git pull --rebase` before pushing,
  then copy `main.tex`, `sections/`, `references.bib`, `main.pdf` into `02_MANUSCRIPT/` and `Paper_A_Final_Submission/`.
- Conclusions were shortened at the author's request: six one-to-two-line findings plus a short usefulness paragraph; no
  limitations list (the corner-force and FE-at-operating-point details stay in the results/appendix).  The three corner
  claims were removed from `claims.json` because their only tokens were in the old Conclusions.
- Added the author's own paper gupta2027ellipsoidal (Finite Elem. Anal. Des. 263, 104681, DOI 10.1016/j.finel.2026.104681) in Section 3 (FE plate check); self-citations are now 4 = the maximum, do not add more.
- Abstract rewritten (starts 'This paper presents'; only 1.93% and 94.29% quoted); claims 1.21/36.1/131 no longer in_abstract.
