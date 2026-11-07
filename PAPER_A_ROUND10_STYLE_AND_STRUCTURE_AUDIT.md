# Paper A — Round 10: style and structure audit (written before any edit)

**Date:** 2026-11-07 · **Branch:** `arena/ea7ca4dd-a-paper` · **Baseline:** `aabcb77` (round 9)
**Object of the round:** `Paper_A_Final_Submission/main.tex` and the seven files in
`Paper_A_Final_Submission/sections/` — and nothing else in the manuscript.
**Status of the build:** no TeX engine in this environment, so the typeset output remains
**BUILD UNVERIFIED**. Nothing in this round claims a compiled PDF.

This document exists **before** the first edit. It records what the manuscript looks like at
`aabcb77`, what the author's published papers look like, and what will therefore be changed, left
alone, or refused. Every later edit is tagged with the classification vocabulary of section 4 and
logged in `PAPER_A_ROUND10_LANGUAGE_AND_STRUCTURE_CHANGES.md`.

---

## 1. Scope of the round

Round 10 is a **manuscript-only** round. It changes structure, language, scientific presentation and
narrative register. It does not recompute, regenerate, re-fit or re-label a single result.

| frozen this round | how it is protected |
|---|---|
| governing equations, constitutive tensors, boundary-condition mathematics | no equation deleted, no tensor index changed, no $\ell$, $f$, $H$ definition touched; `\label`/`\eqref` graph preserved |
| all Python and solver code, tolerances, datasets | `paper_a_study/` not opened for writing in this round |
| peak search, energy balance, coupling and control results | every registered literal string of `claims.json` must survive verbatim (section 6) |
| figure generation code and the ten figure PDFs | no `figures/*.pdf` rewritten; captions are text only |
| parameter values and the claim registry | `claims.json` not edited; `MANIFEST.json` not hand-edited |
| correction history | new material goes to the private `PAPER_A_CORRECTION_HISTORY.md`, never into the article |

No numerical cell may move. The check is mechanical: `claim_audit.py` must still return PASS with
22 claims / 45 tokens / 9 source rows after the last edit, and `static_check.py` must still return 0.

---

## 2. What was read, and how

Style evidence comes from papers carrying **Vipin Gupta** as an author, taken from the author's own
Google Drive copy. Filenames are author-era and duplicates exist; one file per paper was used. Text
was extracted from the PDF by the Drive reader and read in the extracted form. Extraction of
mathematical typesetting is lossy, so the evidence used below is **prose, structure, section
headings, figure-reference habits and abstract construction** — not equations.

| # | paper (as filed) | venue | what was read | depth |
|---|---|---|---|---|
| 1 | `2023_Gupta_Reflection_Quasi_Plasma_Wave_Photo-piezo_Semiconductor.pdf` | Phys. Scr. 99 (2024) 025515 | title, keywords, abstract, full introduction, fundamental equations, formulation, limiting-case subsection, nomenclature, numerical-results opening and per-parameter subsections | **read, ~26 k characters** |
| 2 | `2025_Gupta_Effects_Layer_Imperfections_Material_Gradation_Circumferential.pdf` | Compos. Struct. 359 (2025) 118997 | title, six keywords, single-paragraph abstract, introduction with numbered literature, closing contribution paragraphs and bullet implications, geometry/formulation section | **read, ~14 k characters** |
| 3 | `B01-034__P34_2025_HFF_Piezo-semiconductor-void-…-Rayleigh-Waves-Within.pdf` | Int. J. Numer. Methods Heat Fluid Flow (2025) | structured Emerald abstract (purpose/design/findings/limitations/practical/originality), keywords, nomenclature, introduction opening | **read, ~6.5 k characters** |
| 4 | `B02-006__P40_2026_HFF_Dispersion-Damping-Characteristics-Rayleigh-type-Waves-KG-Nonlocal.pdf` | Int. J. Numer. Methods Heat Fluid Flow (2026) | structured abstract, keywords, nomenclature, introduction opening | **read, ~5 k characters** |
| 5 | `2026_Aldandani_On_Rayleigh_Surface_Wave_Dynamics_Porous.pdf` | Sci. Rep. 16 (2026) 28908 | title, keywords, single-paragraph abstract, introduction with author-named literature | **read, ~5 k characters** |

Five papers were opened and read in the form above. Two further items that the round-10 brief listed
were located but **not opened**: the monoclinic interface energy-transfer paper
(`2023_Barak_Energy_Transfer_Interface_Monoclinic_Piezothermoelastic.pdf`) and the
higher-order-MDD energy-ratio paper. No statement in the four round-10 reports is derived from them,
and nothing about interface energy ratios is claimed here. **Direct comparison with those two papers:
UNVERIFIED.**

One file consulted by name was *not* the paper it was filed under
(`NA_NA_B06-016_MDD_Energy_Ratio.pdf` is a 2020 ASME *J. Heat Transfer* article by Sarkar, De, Das
and Sarkar, not an MDD energy-ratio paper by this author); it was therefore discarded as evidence
rather than used. This is recorded because a filename is not provenance.

---

## 3. What the reference corpus does, stated as six habits

1. **A title that names the physics and the model, not the method.** "Reflection of quasi plasma wave
   in photo-piezo semiconductor medium with distinct higher order fractional derivative two
   temperature models" — system, process, and the modelling ingredient.
2. **An abstract that is one paragraph of results-in-language**: what is modelled, what is solved,
   what is found, what it depends on. No claim that the work is validated, audited, certified or
   delivered. ~150–210 words.
3. **Five to six keywords**, always including the material class, the wave type and the modelling
   ingredient.
4. **An introduction organised by physics, not by chronology of the project**: a paragraph on the
   phenomenon and why it matters, then one thread of literature per paragraph ("Biot was the first
   proponent…", "Chen and his coworkers [9–11] have put forward…"), closing with what is missing and
   what this paper does. Named authors with numbered citations are used freely.
5. **A formulation section that is a narrative of derivation**: "Following [x], the fundamental
   equations are…", "Equation (3.1), when combined with equation (2.3), leads to…". Limiting cases
   are listed as a short, itemised subsection, and a nomenclature list is provided.
6. **Results discussed figure by figure and effect by effect**, in moderate-length paragraphs, each
   opening with the physical statement and then the number ("as the angle of incidence increases,
   there is a corresponding increase in the magnitude of reflected plasma wave… this increment slows
   down as the incidence angle approaches grazing incidence"). Conclusions are a short list of
   findings plus a horizon sentence.

What the corpus does **not** do, and what therefore has to leave this manuscript: the vocabulary of
audit and software delivery ("certified", "admissible", "gate", "registry", "the solver refuses",
"the panel is allowed to claim"), the essayistic-defensive construction ("what the numbers are, and
what they are not"), and the reproducibility material inside the results narrative.

---

## 4. Audit table: element, current state, author pattern, action, classification

Classification vocabulary used in this table and in the change log:
**STRUCTURE** (order, grouping, sectioning) · **LANGUAGE** (wording and register, no claim changed) ·
**EXPLANATION** (a physical or mathematical point made explicit in prose) · **CAPTION** ·
**MATHEMATICAL REFERENCE** (`\eqref`/`\cref` continuity) · **SCIENTIFIC CONTENT UNCHANGED** (an
explicit statement that nothing was re-derived).

| # | element | current state at `aabcb77` | author pattern | round-10 action | classification |
|---|---|---|---|---|---|
| 1 | title | "Backward-branch negative reflection of guided waves at a free edge in a flexoelectric piezoelectric–semiconductor plate" — accurate, but two adjectives away from naming the mechanism | names system + process + modelling ingredient | keep the object, shorten the modifier chain, put the strain-gradient mechanism in the title | LANGUAGE |
| 2 | abstract | 236 words; ~30 % of it is certification and bookkeeping ("certified local extremum, flat to 0.01 pp", "a modal share: 99.77 % …", "corner line forces are not certified"); opens on a literature wager | one paragraph: model → solved → found → depends on → caveat | rebuild to 180–220 words in that order; keep 94.68 %, 2.31 %, 16.68 GHz, 16.6547 GHz, 0.736/0.5275, backward branch, carrier coupling, 1.21 %/34.2 %, factor 128, 99.77 %, synthetic-parameter caveat, modal-share caveat | LANGUAGE + STRUCTURE |
| 3 | keywords | six, correct | 5–6, material + wave + ingredient | keep six; re-order so the material and the mechanism lead | LANGUAGE |
| 4 | introduction | five substantial paragraphs + two subsections (added coupling; scope and organisation). Literature is grouped by *formulation* vs *wave theory* — an audit grouping. The final paragraph announces "answers turn out to be different in kind" and closes on "Reporting the two separately … is what the rest of the paper does" | phenomenon → three literature threads → gap → this paper → organisation | keep the five-paragraph group, rewrite the gap and contribution paragraphs as the author writes them (named authors, numbered citations, no self-adjudication), and end with a clean organisation paragraph that names sections by number | STRUCTURE + LANGUAGE |
| 5 | formulation | `governing_equations.tex`: correct and complete, but written as a specification with audit glosses ("it is not a full three-dimensional simulation, and nothing below is reported as one"; "Writing $A$ in pascals … is dimensionally wrong") | derivation narrative with lead-ins, limiting cases | add equation lead-ins, convert audit glosses into physics statements, group the electric-model ratios as a short justification subsection, keep every equation and every unit table | EXPLANATION + MATHEMATICAL REFERENCE |
| 6 | solution methodology | `numerical_methods.tex` mixes three things: the numerical method, the admissibility *policy*, and the software test suite (39 tests, mutation descriptions, "the solver refuses to run", regression guards against "mislabelled" cases) | method described once, in the author's derivational voice; software in a package appendix | keep basis, polynomial form, two routes, edge matching; move testing/regression/mutation prose to the reproducibility appendix; state admissibility as a mathematical condition, not a gate | STRUCTURE + LANGUAGE |
| 7 | results narrative | ten figures, ten subsections; several subsections lead with a *policy* ("Before any number is read…", "The search is staged and its result is classified rather than named") and one is titled "Why the high fraction is not an artefact" | figure-wise, effect-wise, physical statement first | re-order the prose inside subsections to state the physics first and the number second; retitle the artefact subsection as a discussion of resolution; keep every table, every number, every figure in citation order | STRUCTURE + LANGUAGE |
| 8 | figure captions | complete, but several carry code and file vocabulary ("at $\ell=\SI{2}{\micro\metre}$" mis-scaled label, "95/95 rows admissible", "the coarse raster has $\Delta k_xd=0.01$") | short, descriptive, physical | rewrite as physics-first descriptions, drop row counts, admissibility tallies and raster spacing from captions (they belong in the text or the data), keep panel-by-panel enumeration | CAPTION |
| 9 | discussion | 361 lines; three of eight subsections are defensive in title and construction ("What the reported numbers are, and what they are not"; "Limitations" spread over two subsections with an embedded rebuttal) | the author discusses mechanisms and comparisons, then states limitations in one compact place | restructure into mechanism → comparison with the literature → material provenance → a single grouped Limitations subsection → closing outlook; keep every caveat sentence, in affirmative form | STRUCTURE + LANGUAGE |
| 10 | conclusions | numbered list of five results, three of which are numerical-bookkeeping statements (energy identity closes to 3.4e-16; stable to 5.0e-9) | short list of physical findings + horizon | rewrite as physical findings, folding precision statements into the finding they qualify; keep 2.31 %, 94.68 %, 99.77 %, 1.21 %, 34.2 %, factor 128, the $5.0\times10^{-9}$ stability literal, novelty unresolved, synthetic parameters | LANGUAGE + STRUCTURE |
| 11 | declarations / appendix | present and complete; reproducibility appendix 148 lines | package appendix is normal practice | leave in place; absorb the displaced software prose; remove references to "round-eight version of the search script" (development history) | STRUCTURE |
| 12 | register | 39 occurrences of "certif*", 27 of "certified", 20 of "admissib*", 19 of "audit", 21 of "solver", 18 of "script", 12 of "CSV"; 25 "rather than", 41 "not a" | plain formal prose; technical words used for things, not for epistemic status | remove the audit/software register from the article; keep "numerical solution", "computed", "the present calculation"; no new "Furthermore/Moreover/Notably/Remarkably/Importantly/Significantly" padding; no five-paragraph template applied to any figure | LANGUAGE |

---

## 5. Findings that drive the rewrite

**F1 — the article argues with an auditor, not with a reader.** Sentences such as "Before any number
is read, it is necessary to be precise about…", "That is what the panel is allowed to claim", "The
result is classified rather than named" are addressed to a reviewer of a verification round. They
are replaced by the same content stated as physics or as a scope condition.

**F2 — reproducibility has leaked into the science sections.** Test counts, mutation descriptions,
"the solver verifies that the number of outgoing roots equals $M$ and aborts otherwise", regression
guards against a mislabelled configuration: these are engineering facts about the package, not
results. They move to `appendix_reproducibility.tex` in compressed form. Nothing is deleted, because
the brief forbids deleting content to shorten the paper.

**F3 — defensive negation is the default rhetorical shape.** 41 occurrences of "not a", 25 of
"rather than". The caveats are required and stay; the *shape* changes from "X is not Y" to "X is Z,
which is the weaker/stronger statement" wherever the affirmative form is available. Where a negation
is the claim itself (the share is not a reflectance), it stays a negation.

**F4 — the results narrative is ordered by procedure rather than by physics.** Subsection order
follows the order in which the records were produced: dispersion → material scope → geometry →
sweep → refinement → certification → artefact tests → energy budget → mechanism → attenuation →
coupling → flux profile → convergence → field. An author's order is: what the branch looks like →
what the edge does to it → where the maximum is and how well it is resolved → what creates it →
what modifies it → the field picture. The reordering keeps the figure citation order (fig01 … fig10)
strictly ascending, which `claim_audit.py` checks.

**F5 — one caption contains a unit error and one a tally.** `fig02`'s caption says "the backward
channel $R_B$ at $\ell=\SI{2}{\micro\metre}$", where $\ell$ is the gradient length and the
reference plane is $L=2\,\si{\micro\metre}$; and `fig07`'s caption carries "95/95 rows admissible".
The first is corrected as a **CAPTION** matter (it is a label, not a datum). The second is removed
from the caption and its content kept in the text. Neither touches a number in a table.

**F6 — the abstract's opening is a hypothesis nobody asked for.** "…has not been settled" reads as a
literature wager. The author's abstracts open on the material system and the process.

---

## 6. Load-bearing strings (the constraint that bounds every edit)

`claims.json` is frozen, so the 45 registered literal strings must survive **verbatim** in the file
they are registered against. They are not decoration: each is the string that carries a number.
The table lists the shapes an edit must not break.

| file | literals that must remain |
|---|---|
| `main.tex` | `2.31`, `94.68`, `99.77`, `1.21`, `34.2`, `128` |
| `sections/results.tex` | `2.3146\times10^{-2}`, `0.023\,146`, `0.946\,795`, `0.9467952`, `0.9467954`, `0.931\,891`, `0.579\,180`, `0.99769`, `0.99980`, `1.21`, `34.2`, `11.1`, `87.1`, `0.9960`, `0.996`, `0.5282`, `5.0\times10^{-9}`, `5.6\times10^{-9}`, `128`, `2\times10^{-16}`, `\SI{2.01}{\percent}`, `\SI{-9.85}{\percent}`, `0.9856`, `0.0232`, `0.5802` |
| `sections/conclusions.tex` | `2.31`, `94.68`, `99.77`, `1.21`, `34.2`, `128`, `5.0\times10^{-9}` |
| `sections/discussion.tex` | `94.68`, `0.99769`, `1.21`, `34.2`, `11.1`, `128`, `\SI{-9.85}{\percent}` |

Also binding, and checked by the same script:

* **deprecated strings must not appear**: `0.99985`, `28.06`, `93.19`, `33.1`, `110 rows`;
* **figures must be first cited in ascending order** `fig01 … fig10`;
* **every claim flagged `in_abstract` must be in the abstract** — that is `2.31`, `94.68`, `99.77`,
  `1.21`, `34.2`, `128`, which is why the abstract keeps all six.

Consequence: the abstract and the conclusions keep their percentage literals in `\SI{..}{\percent}`
form, the results tables keep their `\,`-grouped six-figure entries, and no number is re-rounded
while a sentence is rewritten.

---

## 7. Round-11 items opened by this audit (not fixed here)

| id | item | why it is not fixed in round 10 |
|---|---|---|
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-1 | `fig02` panel (c) axis label and the caption previously used $\ell$ for a distance from the edge; the panel labels themselves were not inspected or changed here | figure text is frozen this round; the caption is corrected, the panel label needs the figure pipeline |
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-2 | `fig05` and `fig09` plot round-off-level quantities ($10^{-12}$–$10^{-16}$) on logarithmic axes; the reader cannot see whether the plotted floor is numerical noise or a tolerance | a plotting decision, not a caption decision |
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-3 | three of the ten captions describe panels whose content is only decodable with the accompanying data file (colour-map limits, panel-to-column mapping) | needs the figure audit |
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-4 | panel (c) of `fig10` is a schematic; whether a schematic belongs in a results figure set is a scientific-presentation question for the figure round | figure set composition is frozen |

None of these was corrected by editing a number or a box in the text.

## 8. What this round will refuse to do

* It will not import an equation, a result, a boundary condition or a physical explanation from any
  published paper. The reference papers supply **habits**, not content.
* It will not add a citation, or a physical interpretation, that is not already supported by
  `references.bib` and by a stored record.
* It will not describe a PDF as read when it was not opened (section 2), and it will not claim
  priority, novelty, experimental validation or Q1 readiness.
* It will not delete an equation, a table, a figure or a limitation to reach a page count.
* It will not report a figure defect as fixed: section 7 exists for that.
* It will not compile the manuscript; the build stays **UNVERIFIED**, and no old PDF is substituted.

## 9. Verification plan for the round

1. `python paper_a_study/claim_audit.py` → PASS, 22 claims / 45 tokens / 9 source rows.
2. `python Paper_A_Final_Submission/scripts/static_check.py` → exit 0 (labels, refs, cites, figure
   files, balanced environments).
3. `grep` census of the removed register (`certified`, `admissib`, `audit`, `gate`, `registry`,
   `script`, `CSV`) with the before/after counts recorded in the change log.
4. Figure census: exactly ten `\includegraphics`, exactly ten `\label{fig:...}`, first citations
   ascending.
5. Word-count comparison per file, so that "no content deleted" is a number, not a promise.
6. The full battery (`run_all_checks.py`) is re-run at the end of the round; the manuscript is the
   only thing that may have changed, so any movement in a data gate would be a defect.
