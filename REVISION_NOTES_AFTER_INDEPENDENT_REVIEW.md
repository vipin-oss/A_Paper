# Paper A — response to the GPT audit report (Claude, independent re-derivation)
Original ZIP (unchanged, SHA-256 65090f16...9508) was audited; every item was re-derived or re-run, none accepted on the report's word.
Legend: YES = defect confirmed and fixed; PARTIAL = real but already bounded/disclosed or fix differs from the proposal; NO = not a defect / already handled; AUTHOR = only the author can settle.

| # | Verdict | What I found / did |
|---|---|---|
| A01 | YES | Solver: P_left = P_edge + P_diss (residual 2.5e-13); printed RHS P_edge - P_diss would leave 4.0e-4. Manuscript eq:energy_identity corrected to "edge flux plus loss". Solver unchanged. |
| A02 | YES (different fix) | Code flux = -sigma_xi v_i* - tau_jkx eps_dot_jk* + phi D_dot_x* + mu Gamma_x* PLUS a face line term -[tau_ixz v_i*]. Printed display had eta_dot_jk (undefined; correct is eps_dot_jk), an extra dot on Gamma_x, and omitted the face term. Test: removing the face term breaks the single-mode balance (0.71 and 0.13); with it 2e-9 and 2e-10. Display fixed accordingly. GPT's guessed mu J_x was not needed. |
| A03 | YES (notation) | Code already uses |k_x|^2 and the cross-term x-integral over [-L,0]; printed formula used k_x^2 and one section. Rewritten as total-field integral of |d_x mu|^2 + k_y^2|mu|^2 + |d_z mu|^2. Numerics unchanged. |
| A04 | YES (wording) | Full enthalpy has -1/2 E kappa E, a saddle, not positive definite. Schur bound s<1 concerns the (eps, eta, Delta n) block at fixed E. All "positive definite / strictly convex" statements restricted to that block (5 places). |
| A05 | YES (wording) | dw/d(Delta n) defines mu; continuity follows from number conservation + flux law. PDE and sign unchanged. |
| A06 | YES | eq:mu gives a Delta n = mu + Q phi - H eta_zzz; code N = mu + Q phi - h u3''. Printed N lacked the term (zero only at H=0). Definition in numerical_methods and nomenclature corrected; completed-square W = N + h u3'' = mu + Q phi. |
| A07 | PARTIAL | Concern valid; manuscript already called the corner closure "bounded". Added explicit statement that the weak form closes but pointwise traction does not (interior norm 4.3e-2 -> 3.6e-2; edge max 0.77 -> 2.4, degree 10 -> 28) and that a 2-D x-z corner-resolving check is NOT supplied. No 2-D corner computation was done (out of scope here). |
| A08 | YES | Discussion said l=0 removes the backward branch; results show the classical plate has its own fold at k_x d = 0.824 (13.686 GHz). Sentence rewritten. |
| B01 | YES | A z-constant potential gives E_x = -i k_x phi: not a gauge for k != 0. Dropping it over-constrained the open-circuit space. Full-basis Plate and C1 MeshPlate agree (omega 7.90391 vs 7.90393 at 16 elements; R_B 2.94e-18 both) while the old basis gave R_B = 0.287. Code, DOF count (5n+5), text fixed. Headline results use grounded faces and are unchanged; open-circuit numbers appear nowhere in the manuscript text. |
| B02 | YES | Reproduced ValueError (64,18)->(64,17). Fixed by B01 (np = n). New regression test. |
| B03 | YES | Case "branch_maximum"=0.525 renamed near_peak_k0p525; actual peak case K=0.52719 added (R_B 0.9428717 at degree 30, change 8.8e-6 from degree 18). convergence/quadrature JSON regenerated. |
| B04 | YES (label) | certified_local_maximum -> numerically_resolved_sampled_local_maximum in code, stored JSON, tests and the manuscript. Values unchanged. |
| B05 | NO (already reported) | +-2e-23 J m gives 0.6832 / 0.6034 at the fold; the manuscript already states 0.6034/0.6832 and -36.1%. |
| B06 | NO (already handled) | Manuscript calls R_B a modal power share at L=10d, not reflectance, and gives the 13.8% propagation loss. |
| B07 | PARTIAL | Agreed; sentence added that the C1 check keeps the modal x-dependence and tests the thickness discretization only. |
| C01 | YES | Final_Submission/main.pdf (42 p, no bibliography) removed; single canonical PAPER_A.pdf rebuilt by clean pdflatex/bibtex/pdflatex x2: 46 pages, 61 bibliography entries, 0 undefined. |
| C02 | YES | run_all_checks LaTeX stage replaced by clean-directory lifecycle gate (halt-on-error, bibtex, 2 passes, fails on undefined refs or empty bibliography). Negative test with a missing citation correctly FAILS. |
| C03 | AUTHOR | Author block, funding, ethics, repository: not touched. |
| C04 | YES | All four DOIs verified against Crossref (title, authors, journal, year match) and added. |
| C05 | PARTIAL | Environment pins and tolerances already in README_VERIFICATION; no "any machine" guarantee is made. No change. |
| C06 | PARTIAL | Synthetic parameters (l, mu, H) already disclosed in Discussion; no new claims added. |

## Re-run after the changes
verify_paper_a.py 46/46; unit tests 52/52; new test_review_regressions 3/3; claim_audit PASS; full run_all_checks battery: all stages PASS (see log), clean LaTeX build PASS. Headline numbers unchanged (R_B 0.0192916 at the operating point; 0.9428718 at k_xd=0.52719).

## Not done / still open
- 2-D x-z corner-resolving verification (A07).
- Open-circuit physics beyond cross-checking two discretizations of the same model.
- Author-only items (C03, funding, CRediT, AI declaration).

## Addendum — Qu, Pan, Zhu, Deng (2025) read in full text
- Main text (Eqs. 3.16–3.17): carrier energy has no strain gradient, as the manuscript assumed.
- Appendix C.1–C.2 (Eqs. C.1–C.2): chemo-mechanical energy  n~ M^n_IJ G_IJ + n~ M^n_IJK eta_IJK  (and holes), giving psi^n_c = M^n_IJ G_IJ + M^n_IJK eta_IJK. Same structure as Delta n H_jkl eps_jk,l. Qu et al. neglect it in Sec. 3.4. => the "left open" sentence is now resolved; novelty wording softened in Introduction, Governing equations, Discussion, Conclusions. No priority claimed.
- Notation error fixed: in Qu et al. H_IJKLM is the fifth-order strain–strain-gradient coupling and the sixth-order tensor is G_IJKLMN (manuscript had said H_ijklmn). The same claim about Hu et al. was dropped because Hu et al. was not re-read.
- Abstract shortened to ~237 words (limit 250).
- Rebuilt: 47 pages, 61 references, 0 undefined; claim audit, mutation tests and LaTeX gate PASS.

## Addendum 2 — Hu et al. (2025) and Qu–Jin–Yang (2020) read
- Hu et al. 2025 (IJMS 305, 110740) Eqs. (4a)–(4e): additive Gibbs energy, Psi_Mech = 1/2 C eps eps + 1/2 H_ijklmn g g (H = sixth-order tensor), Psi_Diele = -eta e eps - mu e g, carrier energy a function of (n,p) only. The manuscript's reproduction is correct; notation sentence now states H_ijklmn (Hu), G_IJKLMN (Qu 2025).
- Qu, Jin, Yang 2020 (JAP 127, 194502): balance laws + drift–diffusion, flexoelectricity only in the dielectric layer of a composite beam; it is NOT a free-energy/variational derivation. Introduction corrected accordingly, and "same construction" for qu2022bending/qu2022thermal (not read) softened to "related models".
- T. Hu et al. 2017 (JAP 122, 055106) gives a measured BaTiO3 longitudinal flexoelectric coefficient 17.33e-6 C/m: relevant to the NEW_FEM paper's assumed mu, not to Paper A.
