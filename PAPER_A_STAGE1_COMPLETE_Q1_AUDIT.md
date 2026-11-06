# Paper A — Stage 1 complete Q1 audit (round 7)

**Repository** `vipin-oss/A_Paper` · **branch** `arena/ea7ca4dd-a-paper`
**Baseline audited** `405ed2acbf453a1f9df08cf88001d725077762e8` (round 6)
**Authoritative manuscript** `Paper_A_Final_Submission/main.tex`
**Date** 2026-11-06

Written **before** any repository edit. Every row states what was found, where,
on what evidence, and what it implies. Checks that could not be executed are
marked UNVERIFIED; nothing is recorded as PASS because an earlier report said so.

**Evidence key.** `EXEC` = executed in this environment during this round.
`READ` = read out of a stored dataset or source file. `LIT` = verified against
an external bibliographic record (OpenAlex) during this round. `PRIOR` = reported
by an earlier round and not re-executed here.

Environment: Python 3.11.2, NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.11.2, no TeX
engine.

---

## A. Correction-level findings

| Item | Exact location | Existing claim | Evidence | Classification | Severity | Scientific consequence | Correction | Recalculation | Verification | Expected evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| **S1-01** | `figure_data/fig04_frequency_reflection.csv`; `sections/results.tex` §"Backward conversion along the branch"; abstract; conclusions | "the maximum along the branch is 57.92 % at k_xd = 0.55, where v_g → 0" | The production sweep sampled k_xd on a 0.05 grid (0.50, 0.55, 0.60). A fine sweep executed here (0.005 and 0.01 steps, all rows admissible, condition 160.5, balance ≤1e-12) gives R_B = 0.9319 at k_xd = 0.5250 with v_g = −3 m/s, 0.5792 at 0.5500 with v_g = +34 m/s. `EXEC` | CONFIRMED | CRITICAL | The paper's headline number is a sampling artefact, and its own `tab:refinement` already printed 0.9319 at 0.5250 — a referee would see the contradiction on the same page | Re-solve on a refined grid, relabel the configurations, report 0.9319 as the branch maximum and 0.5792 as the value at k_xd = 0.55 | YES | `build_figure_data.fig04` (110 rows), `convergence_audit.py`, `mechanism_controls.py` | `convergence_audit.json`: R_B(0.525) = 0.93189149 at degree 30, stable to 2.1e-8 |
| **S1-02** | `sections/results.tex` §"What creates the backward channel"; abstract; conclusions; discussion | "the added coupling is a perturbation; it reduces the partition by 1.21 % (operating point) and 9.85 % (peak)" | With the branch maximum identified (S1-01), the matched controls at k_xd = 0.525 give R_B = 0.9319 (H = 0) → 0.6234 (H = 0.05H\*), i.e. **−33.1 %**; edge-plane values 0.9407 → 0.7372 (−21.6 %). `EXEC` | CONFIRMED | CRITICAL | The central interpretation ("bounded perturbation") is true only at the operating point; at the branch maximum the coupling removes a third of the partition | Report the coupling effect at all three configurations and re-derive the interpretation (loss-mediated, largest where the branch is slow) | YES | `mechanism_controls.py` with the added case | `mechanism_controls.json`: `branch_maximum` block, `branch_consistent_H_sweep` |
| **S1-03** | abstract (round-6 text) | "total outgoing propagating power is 0.99985 at the operating point" | Stored value is 0.999797 (`mechanism_controls.json`, `cases.operating_point.no_coupling.total_outgoing_propagating`), and `tab:configurations` prints 0.99980. `READ` | CONFIRMED | MAJOR | A number in the abstract contradicts a table in the same paper | Abstract rewritten; registry entry `total_outgoing_operating_point` now pins 0.99980 | NO | `claim_audit.py` | PASS with 14 registered claims |
| **S1-04** | `main.tex` abstract | three paragraphs, ≈600 words, contains round-off residuals (7e-13), stability figures (1.5e-7) and defensive statements | Counted; journal norm is 180–220 words in one paragraph | CONFIRMED | MAJOR | Desk-rejection risk; abstract unreadable | Rewritten to a single 220-word paragraph with four audit-checked numbers | NO | `claim_audit.py` (in_abstract coverage) | 220 words; every abstract number registered |
| **S1-05** | `sections/conclusions.tex` | 8 paragraphs, ≈700 words, narrating which earlier statements were "reversed" and "corrected here" | Counted; the text also contains development history | CONFIRMED | MAJOR | Violates journal style, exposes internal revision history | Rewritten to 5 numbered results in ≈250 words, no history | NO | static check + word count | Conclusions ≈250 words |
| **S1-06** | 11 figure captions and 1 table caption | "Data: `fig01_….csv`", "Produced by `certify_peak.py`; full table in `peak_certification.json`" | Captions are typeset article text; internal paths belong in reproducibility documentation | CONFIRMED | MINOR | Unprofessional typesetting; the round-6 `\protect` fix was needed only because of this | All file references removed from captions; the appendix table already lists every file | NO | `grep` for `\path` in captions = 0; `static_check` PASS | No path survives outside the appendix |
| **S1-07** | `sections/results.tex` (3 places), `sections/numerical_methods.tex` (3), `sections/governing_equations.tex` (2), `sections/conclusions.tex` (2) | "the earlier version of this paper", "were previously described", "the honest reading", "genuinely independent", "which is exactly what happened" | Full-text search | CONFIRMED | MAJOR | Revision history and self-commentary in a scientific article | All rewritten to state the physics; the history lives in `PAPER_A_CORRECTION_HISTORY.md` | NO | `grep` for the banned phrases | 0 occurrences |
| **S1-08** | `main.tex` | no back matter of any kind | No `Data availability`, `Competing interests`, `Funding`, `CRediT`, `Ethics` sections | CONFIRMED | MAJOR | Not submittable to any journal with a declaration requirement | Declarations section added after Conclusions; author-controlled items marked AUTHOR INPUT REQUIRED rather than invented | NO | read-through | Present; flagged items listed in §31 of the readiness report |
| **S1-09** | `sections/results.tex` §"Energy budget" | "the sum reproduces the flux at the plane to 3.4e-16" next to four-digit printed values that close to 1.4e-6 | Arithmetic on the printed numbers. `READ` | CONFIRMED | MINOR | A reader checking the printed partition finds a residual four orders larger than claimed | Text now distinguishes the rounded closure (1.4e-6) from the exact closure (3.4e-16) and prints 0.976651 | NO | recomputation | Statement matches the arithmetic |
| **S1-10** | `sections/results.tex` §"Dispersion"; `fig01` caption | "$v_g$ and $v_E$ change sign at $k_xd\approx0.55$" | Refined group velocity: −10.0 m/s at 0.52, +4.1 m/s at 0.53 | CONFIRMED | MINOR | Numerical mis-statement of the zero-group-velocity location | Corrected to "just below k_xd = 0.53" | NO | `fig04` CSV | Consistent |
| **S1-11** | `main.tex` title | 18 words, subtitle carries the mechanism | Counted | CONFIRMED | MINOR | Above the 10–16-word preference | "Backward-branch negative reflection of guided waves at a free edge in a flexoelectric piezoelectric–semiconductor plate" (15 words) | NO | count | 15 words, system + phenomenon + mechanism |
| **S1-12** | `main.tex` keywords | 8 keywords | Counted | CONFIRMED | MINOR | Outside the 5–6 preferred | Reduced to 6 | NO | count | 6 |
| **S1-13** | `sections/governing_equations.tex`, `sections/discussion.tex` | "Fourier-reduced three-dimensional formulation" | Ansatz is f(x,z)e^{ik_yy−iωt} with three displacement components; no y-discretisation | MANUSCRIPT-ONLY | MINOR | The phrase invites the reading that this is a full 3D simulation | Both places now say 2.5D explicitly and state what is and is not discretised | NO | read-through | Consistent wording |

## B. Findings that required an investigation, with the outcome

| Item | Location | Question | Investigation | Classification | Severity | Outcome |
|---|---|---|---|---|---|---|
| **S1-20** | `tab:refinement` row "Peak, lower flank" | Is 0.9319 at k_xd = 0.525 admissible, or an artefact of the near-degeneracy with the specular mode? | Fine sweep plus modal diagnostics. At 0.525: K_B = 0.524949, K_inc = 0.529414 (ratio 0.992), specular at −0.529414, so the backward mode is distinct in sign and 0.8 % away in magnitude; edge condition number 160–186, scaled residual ≤3e-15, power balance 1e-14, degree stability 2.1e-8, quadrature stability 7e-9. `EXEC` | CONFIRMED (admissible) | — | The high value is real, not a projection artefact; the report recommends reporting it (S1-01) while stating the near-degeneracy openly. |
| **S1-21** | `sections/results.tex` §"Scope" | Does the flexoelectric sector contribute what the text says? | `mechanism_controls.json`: full vs no-flexo at all three configurations. Operating point −0.011 %, branch maximum <1e-4 %, k_xd = 0.55 −0.009 %. `READ` | CONFIRMED | MINOR | Text updated: "−0.011 % at the operating point and less than 1e-4 % at the branch maximum". |
| **S1-22** | Novelty vs Qu et al. (2025) | Is the added enthalpy term already in the primary theory? | OpenAlex record for DOI 10.1016/j.ijengsci.2024.104165: `oa_status = closed`, no repository copy, `has_fulltext = false`. Equation-level comparison therefore still runs against the open-access transcription in Hu et al. (2025), DOI 10.1016/j.ijmecsci.2025.110740 (`oa_status = hybrid`). `LIT` | UNRESOLVED | MAJOR | Cannot be closed from this environment; see `PAPER_A_ROUND7_NOVELTY_AND_MECHANISM_REPORT.md`. |
| **S1-23** | Literature coverage of the Introduction | Are the closest scattering/surface-wave papers cited? | Two directly relevant papers were located and verified by DOI: Biswas & Sahu, *Math. Mech. Solids* **30**(12) 2822–2842 (2025), DOI 10.1177/10812865251315937; Mondal, Sahu & Nirwal, *Math. Methods Appl. Sci.* **45**(12) 7700–7714 (2022), DOI 10.1002/mma.8272. `LIT` | CONFIRMED (missing) | MAJOR | Both added to `references.bib` and cited where they bear on the gap statement; the gap is now stated precisely rather than as "no work exists". |
| **S1-24** | Bibliography records | Do the 11 existing entries match their records? | All 11 checked against OpenAlex by DOI or title (authors, title, journal, year, volume, pages). Four entries lacked DOIs and now have verified ones. `LIT` | CONFIRMED (correct) | — | No bibliographic error found; two DOIs added for completeness. |
| **S1-25** | `paper_a_study/model.py` | Is the quadrature justified or merely high order? | The rule is fixed at `max(64, 2·degree+10)` with no way to test it. A `nquad` override was added (default unchanged) and the two reported configurations re-solved with 64/128/192/256 nodes. `EXEC` | CODE-LEVEL gap | MINOR | Worst relative change of R_B is 6.9e-9 — far below the quoted precision. Now an executable test. |
| **S1-26** | `paper_a_study/test_model.py` | Could a material constant entered in the wrong unit pass the suite? | Every existing test compares code against code, so yes. `EXEC` (mutation M5 initially *passed* the suite) | CODE-LEVEL gap | MAJOR | Two tests added: frozen derived constants (K0, KB0, KY0, OMEGA0, HCRIT to 1e-10) and literature bands on the elastic, piezoelectric and dielectric constants. Mutation M5 now fails as it should. |
| **S1-27** | Manuscript ↔ dataset consistency | Can a number drift between manuscript and dataset? | There was no machine check. A 14-claim registry with 36 literal tokens was built, plus a stale-value guard. `EXEC` | CODE-LEVEL gap | MAJOR | `claim_audit.py` PASS; mutations M2/M3 caught. |

## C. Items examined and found sound (no action)

| Item | Location | Claim | Evidence | Classification |
|---|---|---|---|---|
| S1-30 | `sections/governing_equations.tex` | Sign conventions: E_i = −∂_iφ, electron charge −q, electrochemical potential in joules | Re-derived by differentiation of the stated enthalpy; constants of the solver agree | CONFIRMED (correct) |
| S1-31 | `governing_equations.tex`, `numerical_methods.tex` | Energy identity P_inc + ΣP_j + P_cross = P_edge − P_diss | Closes to 3.4e-16 at the operating point; 7.3e-13 solver balance; the interference term is quoted separately | CONFIRMED (correct) |
| S1-32 | `results.tex` | R_B is a modal share, not a reflectance | Stated in the text, in both table captions and in the abstract | CONFIRMED (correct) |
| S1-33 | `discussion.tex` | Corner band carries 0.93–1.00 % and 1.18–1.26 %, decreasing under refinement | `corner_assessment.json`, cross-check PASS; the text explicitly refuses to call this a proof about line forces | CONFIRMED (correct) |
| S1-34 | `discussion.tex` §Limitations | ℓ, f, H synthetic; Q1-readiness not claimed | Present in the material table, the provenance table and the limitations | CONFIRMED (correct) |
| S1-35 | `governing_equations.tex` §Thermodynamic admissibility | Schur bound on H | `Plate` raises when violated; test `test_material_units_and_schur` passes | CONFIRMED (correct) |
| S1-36 | ten figures | Vector PDF, 10.5 cm width, no font below 7 pt, consistent colours | Inspected at source level; only `fig04` needed regeneration (S1-01) | CONFIRMED |
| S1-37 | `sections/results.tex` | Figure citation order | 1…10 in first-citation order (`claim_audit.py` gate) | CONFIRMED (correct) |
| S1-38 | `numerical_methods.tex` | Time integrators, α-schemes, patch tests | The method is frequency-domain spectral Galerkin; no time integrator exists, and the classical limit is checked analytically instead of by a patch test | NOT APPLICABLE (documented) |

## D. Checks that could not be executed

| Item | Why | Classification |
|---|---|---|
| S1-40 | LaTeX/BibTeX compilation, page count, overfull boxes, float placement in a rendered PDF | No TeX engine in this environment | **UNVERIFIED** |
| S1-41 | Visual inspection of the regenerated Fig. 4 in a rendered page | Depends on S1-40 | **UNVERIFIED** (the PDF's own content stream was regenerated and its size is stable) |
| S1-42 | Full text of Qu et al. (2025) | Closed access, no repository copy (`LIT`) | **UNRESOLVED** |
| S1-43 | Experimental calibration of ℓ, f, H | No measurements exist for this stack | **NOT AVAILABLE** by construction |

---

## Stage 1 verdict

Two **CRITICAL** defects were confirmed (S1-01, S1-02), both in the reporting of
the headline numbers rather than in the governing equations; six **MAJOR**
editorial/validation defects (S1-03 … S1-08, S1-26, S1-27); the rest MINOR.
The mathematics, the energy identity, the corner argument and the material
provenance survived the audit unchanged.

Stage 2 was therefore authorised for: the branch-maximum correction (with its
dependent figures, tables, abstract, discussion and conclusions), the coupling
interpretation, the abstract/conclusions/title/keywords rewrite, caption and
history-language cleanup, back matter, two verified references, and the four new
verification gates. No change to the governing equations was required and none
was made.
