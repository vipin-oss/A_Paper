# Paper A — Round 10: structural comparison with the author's papers

**Purpose.** Put the architecture of this manuscript next to the architecture of the author's
published papers, section by section, and record what is adopted, what is adapted and what is
deliberately not copied.
**Sources.** The five papers of `PAPER_A_ROUND10_AUTHOR_WRITING_STYLE.md`. Section lists are given
here only where the extracted text actually showed them; a heading that was not seen is written
"not observed" rather than guessed. Papers 3 and 4 were read only as far as the nomenclature, so
their later headings are not observed.

---

## 1. Section skeletons

| level | paper 1 (Phys. Scr. 2024) | paper 2 (Compos. Struct. 2025) | papers 3, 4 (HFF) | paper 5 (Sci. Rep. 2026) | **Paper A at `aabcb77`** |
|---|---|---|---|---|---|
| front | title, authors, keywords, abstract (single paragraph) | title, authors, keywords, abstract (single paragraph) | title, authors, structured abstract, keywords, nomenclature | title, authors, keywords, abstract (single paragraph) | title, authors, abstract with six keywords inside it |
| 1 | Introduction | 1. Introduction | 1. Introduction | (unnumbered) introduction | 1. Introduction + 1.1 the added coupling + 1.2 scope and organisation |
| 2 | Fundamental equations + **2.1 Limiting case** | 2. Formulation of the geometrical model + 2.1… per medium | 2. (formulation, not observed beyond heading) | (formulation, not observed) | 2. Mathematical formulation + eight subsections (geometry, kinematics, constitutive, balance, electric model, boundary conditions, power flux, non-dimensionalisation, thermodynamic admissibility) |
| 3 | Formulation of the problem (the reduction to the $xz$ plane) | boundary/solution sections (not observed) | — | — | 3. Solution method and verification + six subsections including a 39-test list |
| 4 … | limiting cases of the model (section 9), 10. Numerical results and discussion + 10.1 per parameter | results and conclusions | — | results and discussion | 4. Results + ten subsections; 5. Discussion + eight subsections; 6. Conclusions; declarations; appendix |

Three structural facts follow immediately.

* **The author's papers separate *fundamental equations* from *formulation of the problem*** — the
  general theory first, then the reduction to the configuration at hand. Paper A does this inside one
  section; the boundary is still legible, so no section is invented to imitate the split.
* **Limiting cases are a flagged subsection, not a remark.** Paper 1 devotes 2.1 to them and the
  model-comparison section later. Paper A has the material for this (classical $\ell=0$; strain
  gradient without carriers; no-flexoelectric; $H=0$) scattered across three sections.
* **The author's results sections are shorter than their formulation sections, and their discussion
  is not a separate numbered section** in the papers where it was observed. Paper A has a 361-line
  Discussion after a 763-line Results. That asymmetry is legitimate for a numerical paper, but the
  Discussion must earn it: it is restructured to mechanism → literature → provenance → limitations.

---

## 2. Mapping: what plays the role of what

| author's element | Paper A equivalent at `aabcb77` | verdict |
|---|---|---|
| "Fundamental equations" with numbered equations and a nomenclature | §2.1–2.4, with `tab:units`, `tab:conjugates`, `tab:groups` in place of a nomenclature list | **keep the tables, no nomenclature list added** — three tables already carry the symbols and units, and a fourth list would be inventory without information |
| "2.1 Limiting case" | §2.9 (thermodynamic admissibility) plus the $\ell=0$ control in §4 | **add a compact limits subsection** in §2 that collects them with their citations already in `references.bib`; the control table stays where it is |
| "Formulation of the problem" | §2.1 (geometry) and §3 (method) | **keep as is**; the split already exists, only the prose changes |
| "Numerical results and discussion", subsection per parameter | §4.1–4.11, subsection per sweep | **keep the granularity, reorder by physics** (audit §5, F4) |
| parameter justification at the point of use (H8) | scattered: $\ell$, $f$, $H$ provenance in §4.2 and §5.4 | **keep both, cross-referenced once from §2**, so the reader meets the caveat before the first number rather than after it |
| software named in the numerical section | software and test suite described *inside* §3 | **moved to the appendix**; §3 keeps the mathematics of the method |
| short itemised conclusions | §6, a five-item list with bookkeeping items | **keep the itemised form, change the items to findings** |

---

## 3. What is deliberately **not** copied

| not copied | why |
|---|---|
| the structured "Purpose / Design / Findings / Limitations / Practical / Originality" abstract | that is an Emerald house style, not an authorial one; the two journals that use it in the corpus are not this manuscript's target |
| a nomenclature block | three tables already fix every symbol, sign convention and unit; a list would duplicate them |
| "novel" as an adjective on the model | the brief forbids it, and the novelty relation to the primary literature is **unresolved** in this study |
| the bulleted "implications for industry" paragraph | nothing in this study supports an application claim beyond the observable identified in §6 |
| the citation-dense literature walk of paper 2 (one bracketed citation per clause) | this manuscript has 20 references, all load-bearing; padding the introduction with citation-per-clause prose would add citations, which the brief forbids |
| the phrase-level borrowings of the corpus | no sentence, clause or figure caption is reused; only the habits of `AUTHOR_WRITING_STYLE` §2 |

---

## 4. Target architecture of the round-10 manuscript

| section | role | change of shape |
|---|---|---|
| Title | system + mechanism + process | shortened modifier chain |
| Abstract | model → solved → found → depends on → synthetic | rebuilt, 180–220 words |
| 1 Introduction | phenomenon / formulation / wave theory / gap / this paper + organisation | same five groups; register rewritten; organisation paragraph made explicit and final |
| 2 Mathematical formulation | fields, kinematics, constitutive, balance, electric model, boundary conditions, power flux, non-dimensionalisation, limits, admissibility | + one new subsection (limits), every equation given a lead-in, unit and dimension statements phrased as conditions on the model |
| 3 Method | basis, polynomial form, two routes, edge matching | testing prose moved out; admissibility stated as mathematics |
| 4 Results | dispersion → material scope → geometry → branch sweep → resolution of the maximum → energy budget → mechanism → attenuation → transverse dependence → flux profile → field picture | *reordered*; every number, table and figure retained; captions rewritten |
| 5 Discussion | mechanism / literature / provenance / limitations / outlook | *merged and retitled*; affirmative voice; one limitations subsection |
| 6 Conclusions | findings, itemised | rewritten as physics, literals retained |
| Declarations, Appendix A | data availability, roles, package, commands | received the displaced testing material; no new content |

Word budget: the manuscript is 16 998 words at `aabcb77`. Round 10 is not a shortening round and not
a lengthening round: the target is a small net reduction (register removal and appendix absorption
outweigh the lead-in sentences), with no section losing content. The per-file before/after counts are
tabulated in `PAPER_A_ROUND10_LANGUAGE_AND_STRUCTURE_CHANGES.md`.
