# Paper A — Round 10: final manuscript style audit

**Branch:** `arena/ea7ca4dd-a-paper` · **Baseline:** `aabcb77` (round 9) · **Round:** 10, presentation only
**Manuscript:** `Paper_A_Final_Submission/main.tex` + the seven files in `sections/`
**Build status:** **BUILD UNVERIFIED** — no TeX engine in this environment; no PDF is claimed, and no
old PDF is offered in place of one.

This is the closing report of the round. The pre-edit audit is
`PAPER_A_ROUND10_STYLE_AND_STRUCTURE_AUDIT.md`, the style evidence is
`PAPER_A_ROUND10_AUTHOR_WRITING_STYLE.md`, the architecture comparison is
`PAPER_A_ROUND10_STRUCTURE_COMPARISON.md` and the edit log is
`PAPER_A_ROUND10_LANGUAGE_AND_STRUCTURE_CHANGES.md`.

---

## 1. What the round did

The manuscript was rewritten so that it reads as a mathematical research article in the author's own
manner rather than as a verification report.  The governing equations, the constitutive tensors, the
material constants, the boundary conditions, the code, the datasets, the figures, the parameter values
and the claim registry are all untouched.  No numerical cell moved.

| dimension | at `aabcb77` | now |
|---|---|---|
| title | three stacked modifiers, method-flavoured | "Backward-branch negative reflection of guided waves from the free edge of a flexoelectric piezoelectric semiconductor plate" |
| abstract | 236 words, one third certification bookkeeping | 222 words: system → solution → two findings → coupling → caveats |
| body words | 15 839 | 15 572 |
| appendix words | 1 159 | 1 681 |
| audit/software register in the body | *certif\\** 39, *audit* 19, *admissib\\** 20, *solver* 21, *script* 18, *CSV* 12 (whole manuscript) | 2 / 0 / 9 / 1 / 2 / 0 in the body, the rest confined to the reproduction appendix |
| section architecture | §2 without limits, §3 carrying tests, §5 with defensive titles | §2 + limits, §3 method only, tests in Appendix A, §5 restructured |
| captions | two carried procedure or a wrong symbol | physics first, no row counts, `fig02` symbol corrected |
| equations / tables / figures / citations | 29 / 8 / 10 / 13 | 29 / 8 / 10 / 13 |

## 2. Style audit against the twelve adopted rules

| rule (`AUTHOR_WRITING_STYLE` §4) | verdict | evidence |
|---|---|---|
| 1. abstract = findings, 180–220 words | **met** (222) | all six `in_abstract` literals retained; ends on the synthetic-parameter and corner caveats |
| 2. six keywords, material first | **met** | flexoelectric semiconductor; strain-gradient elasticity; guided plate waves; backward branch; negative reflection; spectral Galerkin method |
| 3. introduction in five groups + organisation | **met** | phenomenon; continuum formulation; wave theory (named authorities); the gap, stated once; this article, then the organisation paragraph naming every section |
| 4. equation lead-ins and `\eqref` continuity | **met** | §2 opens with a map of its own subsections; every block has a lead-in; 75 references, 104 labels, all resolved |
| 5. limits of the formulation, flagged | **met** | new §2.10: classical piezoelectric, strain-gradient dielectric, semiconductor without the gradient sector, uncoupled carriers, plus the two reductions used in the text |
| 6. method described derivationally, software elsewhere | **met** | §3 = basis, polynomial form, two routes, edge matching, conditions, five checks; the 39-test suite, the regression guards, the plane tests and the reproducibility statement are in Appendix A |
| 7. results: physics first, panel and number second | **met** | every §4 subsection opens with the physical statement; panels are named in-sentence |
| 8. captions descriptive, no code vocabulary | **met** | `fig02`, `fig04`, `fig07`, `fig08` rewritten; no file name, row count or tolerance in any caption |
| 9. discussion affirmative, limitations grouped | **met** | §5.1 retitled, §5.5 grouped into five headed limitations, the two negations that *are* the claim retained |
| 10. conclusions = findings | **met** | five items, each a physical result with its number; the two precision statements folded into the findings they qualify |
| 11. connective budget, no template per figure | **met** | zero occurrences of furthermore / moreover / notably / remarkably / importantly / significantly; the ten figure discussions differ in length and shape (two short, four long, four split) |
| 12. no development history in the article | **met** | zero references to a previous version, a prior script, a defect or a correction; those live in `PAPER_A_CORRECTION_HISTORY.md` |

## 3. Claim and reference audit

| check | result |
|---|---|
| `python paper_a_study/claim_audit.py` | **PASS** — 22 claims, 45 tokens, 5 deprecated strings guarded, figure order 1…10, **9 of 9** source-agreement rows |
| `python Paper_A_Final_Submission/scripts/static_check.py` | **PASS (exit 0)** — 8 files, 104 labels, 75 references, 13 citation keys against 13 bib entries, balanced environments |
| figure census | 10 `\includegraphics`, 10 `fig:` labels, first citation ascending 1…10 |
| deprecated strings (`0.99985`, `28.06`, `93.19`, `33.1`, `110 rows`) | absent |
| LaTeX build | **not attempted** |

## 4. The battery, run on the round-10 tree

`python paper_a_study/run_all_checks.py`, 2026-11-07T05:25Z, ≈ 10 min:
**17 PASS · 1 FAIL · 1 SKIP**.

| gate | result |
|---|---|
| unit and scientific tests (39) | PASS, 18.9 s |
| dimensional and constitutive audit | PASS — contraction residuals 2.171e-13 against 3.120e+06 |
| quasistatic justification | PASS — (k_EM d)² = 4.889e-8, ωτ_d = 1654.4, d/L_D = 0.0746 |
| flexoelectric control | PASS — R_B = 0.579180033 at k_xd = 0.55 with f = 2.563e-03 |
| admissibility re-derivation | PASS |
| figure data and figure files | PASS |
| phase-speed and e.m. reconciliation | PASS |
| modal-flux rescaling proof | PASS, 9.4 s |
| mechanism matched controls | PASS, 198.4 s |
| corner assessment and regression | PASS, 12.2 s |
| peak certification at four fixed wavenumbers | PASS, 13.9 s |
| peak search and classification | PASS, 292.4 s — `certified_local_maximum`, `K_at_max = 0.52752`, `R_B_at_max = 0.9467953677961777` (committed record `0.9467953685099261`, relative difference 8e-13) |
| peak identity and artefact audit | PASS, 20.0 s |
| spectral convergence / quadrature sufficiency | PASS / PASS |
| **claim registry and stale guard** | **FAIL** — two floor-level spreads moved between the committed and the regenerated search record |
| gate mutation tests | PASS — every injected defect caught |
| LaTeX static validation | PASS |
| LaTeX build | SKIP, no engine |

**The one failure, stated plainly.**  The battery regenerates `peak_search.json` as it runs.  In the
regenerated record two *differences of nearly equal numbers* differ from the committed ones while the
headline does not: the degree spread is 5.613e-09 (committed 4.973e-09) and the quadrature spread is
9.382e-10 (committed 5.591e-09).  A 1e-12 absolute change in `R_B` moves a 5e-09 difference by tens of
per cent, so the registry's 1 % tolerance is tighter than the quantity can support on a different run.
Round 10 is a manuscript-only round, so the regenerated data records were restored to their committed
state and the registry gate re-run on the restored tree: **PASS, 9 of 9 source rows**.  Both the failing
comparison and the restored-state pass are recorded in `validation/verification_log.txt`,
`validation/round10_battery_run_2026-11-07.log` and `validation/round10_registry_gate_note.txt`.

No claim in this report is that the package passes all gates on an arbitrary machine.  It passes 17 of
18 on this one, and the eighteenth fails only on a floor-level spread.

## 5. Items opened for round 11 (nothing in the manuscript was changed to hide them)

| id | item |
|---|---|
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-1 | `fig02` panel (c) axis label: the caption now uses $L$ for the reference plane and $\ell$ for the gradient length; the panel label must follow |
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-2 | `fig05(c)` and `fig09(c)` plot 1e-12…1e-16 quantities on logarithmic axes; floor and tolerance are not distinguishable |
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-3 | three captions remain decodable only with the panel-source map (colour limits, panel-to-column mapping) |
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-4 | whether the schematic panel `fig10(c)` belongs in a results figure set |
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-5 | the two spread-type claims (`5.0e-09`, `5.6e-09`) are quoted at a precision the re-run does not support: report them as bounds, re-derive the records on the delivery machine, and widen the registry tolerance for difference-of-two-nearly-equal-values claims |

## 6. Standing statements, unchanged

* The novelty relation to the primary 2025 formulation is **UNRESOLVED** (closed access); nothing in
  this round claims priority, and the literature comparison refers only to the equations that could be
  inspected.
* The gradient length, the flexoelectric coefficient and the coupling constant are **synthetic**; the
  carriers are linearised; the plate has a single edge; corner line forces are **not resolved**.
* \SI{94.68}{\percent} is a **modal share**, not a reflectance; the maximum is **local**, not global;
  the fold carries a factor 128 less incident flux than the operating point.
* The typeset output is **unverified**.  Content and cross-references are validated; the PDF is not.
* No statement of Q1 readiness, and no claim that the article is submission-ready, is made in this
  round or implied by it.

## 7. Delivery

| element | value |
|---|---|
| round-10 commit | recorded in `downloads/README.md` and in the delivery message |
| archive | `downloads/Paper_A_Complete_Project_round10.zip` |
| size and SHA-256 | in `downloads/PACKAGE_SHA256.txt` and `downloads/README.md`, which sit **beside** the archive; a checksum cannot be embedded in the file it describes, and this report is inside the archive, so it does not carry the digest |
| manifest | rebuilt by `build_submission_package.py` after the static validator, then checked against the extracted archive |
