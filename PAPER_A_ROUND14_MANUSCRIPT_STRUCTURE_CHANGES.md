# Round 14 — manuscript structure changes

Single authoritative manuscript: `Paper_A_Final_Submission/main.tex` (174 lines)
with eight section files. No second or competing manuscript exists in the
repository; `build_submission_package.py` refuses to build if one appears.

## 1. Before → after

| Round 13 | Round 14 | Reason |
| --- | --- | --- |
| §1 Introduction **with 1.1 The added coupling and its reciprocals** and **1.2 Scope and organisation** | §1 Introduction, one continuous section, seven paragraphs, no subsections | the brief and the author's own articles use no such subdivision; the subsections were a table of contents inside the introduction |
| three equations in the introduction | moved to §2.3, with a forward cross-reference from the introduction | an equation belongs where the potential it comes from is differentiated |
| §2 Mathematical formulation, 10 subsections, balance laws asserted | §2 as before, **11 subsections**: new §2.4 derivation of the balance laws, new §2.8 reduction to a single propagation direction | the algebra was the missing content, not the prose |
| §3 Solution method | §3 **Solution of the problem**, opening with the weak form | the author's own title, and the weak form is the bridge from §2 to the matrices |
| §4 Results (14 subsections) | §4 **Numerical results and discussion** (14 subsections) | results and their reading belong in one section |
| §5 Discussion (5 subsections) | §4.15 **Discussion** (5 sub-subsections) | as above; the discussion is now the closing part of §4, not a second paper |
| §6 Conclusions | §6 Conclusions | unchanged |
| Declarations | Declarations, data-availability paragraph rewritten to point at the supplementary record | the previous wording advertised the software package inside the article |
| Appendix: reproduction package, 205 lines, scripts/commands/versions/test counts | Appendix: **Numerical resolution and data availability**, 37 lines | software prose out of the article; the record moved to `SUPPLEMENTARY_COMPUTATIONAL_REPRODUCIBILITY.md` |
| no nomenclature | **Nomenclature** table after the abstract (36 symbols) | present in both author papers read (A1, A2) |

Line counts: `main.tex` 174 · `introduction.tex` 137 (was 154) ·
`governing_equations.tex` 675 (was 522) · `numerical_methods.tex` 246 (was 204) ·
`results.tex` 777 (unchanged) · `discussion.tex` 365 (was 360) ·
`conclusions.tex` 44 · `appendix_reproducibility.tex` 37 (was 205).
Approximate prose word count (including math tokens): 16 375.

## 2. Material relocated, not deleted

1. `eq:added_coupling`, `eq:added_hyperstress`, `eq:added_mu` — introduction →
   §2.3, now derived rather than displayed.
2. The software record — appendix → `SUPPLEMENTARY_COMPUTATIONAL_REPRODUCIBILITY.md`
   (file inventory, 16 commands with run-times, exit-status contract,
   environment versions, check inventory, mutation record, provenance,
   integrity and the "what is not reproducible" statement).
3. Nothing was deleted from the scientific content.

## 3. Cross-reference integrity

- Labels: **108** (was 104). New: `eq:var_kinematics`, `eq:virtual_work`,
  `eq:ibp_stress`, `eq:ibp_hyper`, `eq:ansatz`, `eq:substitution`,
  `eq:strain_amplitudes`, `eq:eta_amplitudes`, `eq:quartic`, `eq:weak_form`,
  `sec:governing_reduction`; retired with the appendix: `tab:package`,
  `app:repro_contents`, `app:repro_commands`, `app:repro_env`,
  `app:repro_provenance`, `app:repro_limits`, `sec:numerics_repro`.
- References: **82** (was 75). Every retired label had its references updated;
  `app:checks` and `app:repro` survive because §3.6 and §4 cite them.
- Citations: 13 of 13 bib entries cited; no new citation keys were added.
- Static validator (`scripts/static_check.py`): **PASS**, exit 0 — balanced
  environments, every `\ref` resolved, every `\cite` resolved, every included
  figure present, no macro outside the whitelist (the nomenclature table was
  rewritten to avoid `\hspace` after the first run failed on it).

## 4. Section titles as they now read

1. Introduction
2. Mathematical formulation (geometry and fields; kinematics and the strain
   gradient; enthalpy and constitutive relations; balance laws; electric model;
   boundary conditions; power flux and the energy identity; reduction to a single
   propagation direction; non-dimensionalisation; limits; thermodynamic
   admissibility)
3. Solution of the problem (thickness discretisation and weak form; temporal and
   spatial routes; edge matching; conditions on a reported share; verification)
4. Numerical results and discussion (…; discussion: the meaning of the
   partition, the mechanism, the literature and the limits)
5. Conclusions
6. Declarations · Appendix A: Numerical resolution and data availability

## 5. What this restructuring did not touch

Material constants, governing model, boundary conditions, solver, root
classification, the numerical peak (0.9467952 at $k_xd=0.5275$, local to the
declared window), the coupling results (−34.2 % at the maximum, +1.21 % at the
operating point), the modal-power normalisation, the energy balance
(4×10⁻¹²), the datasets, and the synthetic status of $\ell$, $f$ and $H$.
