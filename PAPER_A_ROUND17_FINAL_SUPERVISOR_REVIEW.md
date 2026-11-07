# Paper A — Round 17 final supervisor review

**Branch** `arena/ea7ca4dd-a-paper` · base `a68bb76` (round 16) · **date** 2026-11-07
**Outcome class: B — the round's manuscript work is complete and self-consistent,
but the document has not been compiled, and two known questions remain open
(priority against the 2025 source, and the corner line force).**

---

## 1. The one-line answer to "is it a calculation-rich mathematical paper now?"

Yes, within the limits below. The formulation section now differentiates the
enthalpy term by term, reduces the tensors to the `6mm` constants the code
actually has, writes the field equations out in components, names the sector
blocks and derives the quartic's coefficient structure and its degree from a
derivative count. The solution section derives the Legendre elements, quotes the
five element values and the `n_w = 5n+3` sizing, and states the edge system and
its scaling. A new mathematical Appendix A carries the element matrices, five
worked matrix elements, the block construction, the edge system, the modal-power
normalisation and one end-to-end evaluation. Six worked numerical chains are in
the body, each input → expression → number → interpretation.

What has *not* been added is any new physics, any new claim, or any new number
that is not recomputed from the stored model.

## 2. Against the ten parts

| Part | Requirement | State |
|---|---|---|
| A | delete dimensions table, define symbols in prose, keep Nomenclature, audit other tables | **done** — `tab:units` and `tab:conjugates` removed, one prose paragraph derives every unit; 8 tables → 5, all numerical or provenance; Nomenclature untouched |
| B | Intro single section; formulation 4–6; solution ~3; results 5–7 | **done** — 1 / 5 / 3 / 7; also repaired the Discussion, which had been rendering as a sub-section of Results |
| C | constitutive derivation, 6mm specialisation, explicit wave reduction, quartic with traceable coefficients, ≥2–3 Galerkin elements, edge system + modal power, 3–6 worked examples | **done** — see the derivations and worked-calculations reports; 39 equations added, all derivational |
| D | new mathematical Appendix A, maths only | **done** — Appendix A (six sub-sections, 16 equations), no commands, no paths, no test vocabulary |
| E | figure overlap repair, real-data insets, quantified separations, coincidence labelled with a bound, per-figure review at width | **done for 01, 02, 04, 07, 08**; 03, 05, 09, 10 unchanged (byte-identical re-render); `fig10(c)` preserved |
| F | no `UNRESOLVED`/`PASS`/audit vocabulary in manuscript tables | **done** — `tab:novelty` deleted, the comparison survives as prose with the uncertainty stated in scientific language; zero occurrences of the banned tokens in the sections |
| G | four/five short numbered limitations | **done** — five numbered points; the corner evidence and the corner caveat now sit in one point, and the line force is nowhere called harmless |
| H | no audit content or dev-history | **done** — no test counts, script names, round numbers, archive hashes; "Verification" retitled and reworded |
| I | no science change without evidence | **held** — figure *data* files unchanged (only the recorded hashes move); the two places where my first draft contradicted the code (the `D`-component signs and the double-counted exponentials in `R_B`) were corrected against the model, not the other way round |
| J | attempt compile, else BUILD UNVERIFIED; siunitx decimals | **BUILD UNVERIFIED** (no engine, none installable); `siunitx` now `group-digits=integer`, `group-minimum-digits=5`, `output-decimal-marker={.}` |

## 3. Evidence that can be checked without compiling

* `static_check.py` → **PASS**: 160 labels, 98 references, 13/13 citations, no
  duplicate label, no undefined reference, no macro outside the whitelist,
  20 036 prose words (was 17 021).
* Figures re-rendered from unchanged CSVs; `figure_panel_sources.json` records
  new hashes and the same data sources.
* Every number in the new derivations is either a manuscript constant or a value
  recomputed this round from `paper_a_study/model.py`; the recomputed set
  (`c_s`, `T`, `a`, `L_D`, `Q`, `α_d`, `λ`, `f_group`, `H_ref`, `H_bound`, `H*`,
  the `n=6` element matrices, the coupling rows) is listed in the
  worked-calculations report.

## 4. What I could not do, and what a supervisor should look at first

1. **Compile.** There is no TeX engine in this environment and none is
   installable from the hosts available. Every layout claim (page count, float
   placement, `cleveref` output for stacked labels on one heading, `siunitx`
   key acceptance in the installed version) is unverified. This is the largest
   single risk of the round, and it is environmental, not editorial.
2. **Judge the paper as a reader will.** I reviewed ten figures at manuscript
   width and read every edited passage, but I cannot see the typeset pages.
3. **Re-run the 18-gate battery.** No solver or producer logic changed; the last
   clean run is `validation/round11_battery_run_clean_reproduction.log`
   (18 PASS, 0 FAIL, 1 SKIP, the skip being the LaTeX build). I did not re-run it
   and I do not claim it for this round.
4. **Priority against the 2025 source.** Still open; closed access. The paper now
   says so in plain scientific language and makes no priority claim. The full
   argument stays in the internal round-16 material.
5. **The corner line force.** Still open pointwise. The paper states the energy
   evidence *and* the reason it is not a proof, in the same numbered limitation.

## 5. Honest assessment of quality

The manuscript is materially better than round 16 as a *mathematical* document:
a referee can now follow the enthalpy to the discrete blocks to the edge system
to the reported number without opening a file. Three weaknesses remain, in the
order I would fix them if I had another round:

* the `6mm` specialisation and the expanded field equations are in the
  formulation section, and the carrier strong form `eq:carrier_strong` is now
  written beside them (added after this list was first drafted);
* the appendix's worked matrix elements are at degree five and six, while the
  reported results are at degree 18–30, so the numbers are illustrative rather
  than the ones the results use (stated in the text, but a reader may expect
  otherwise);
* the figures are repaired where they were broken, but `fig01`(a) now carries a
  leader line that is tight at narrow column widths.

None of these is a scientific defect. The paper is **not** submission-ready, and
this report does not claim it is; it is ready for the supervisor's inspection.
