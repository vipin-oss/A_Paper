# Paper A — Round 10: language and structure changes

**Baseline:** `aabcb77` · **Branch:** `arena/ea7ca4dd-a-paper` · **Scope:** manuscript files only.
**No number was changed, no figure was re-rendered, no code was touched.**

Every edit below is classified with the vocabulary of
`PAPER_A_ROUND10_STYLE_AND_STRUCTURE_AUDIT.md`: **STRUCTURE**, **LANGUAGE**, **EXPLANATION**,
**CAPTION**, **MATHEMATICAL REFERENCE**, **SCIENTIFIC CONTENT UNCHANGED**. An edit that carries more
than one label is listed once with all its labels.

---

## 1. Size of the change

| file | words at `aabcb77` | words now | Δ | subsections |
|---|---|---|---|---|
| `main.tex` (title, abstract, keywords, declarations) | 653 | 648 | −5 | — |
| `sections/introduction.tex` | 1 333 | 1 308 | −25 | 2 → 2 |
| `sections/governing_equations.tex` | 2 709 | 3 080 | +371 | 9 → **10** |
| `sections/numerical_methods.tex` | 1 819 | 1 360 | **−459** | 6 → **5** |
| `sections/results.tex` | 6 118 | 5 957 | −161 | 15 → 15 (three retitled, two merged in substance) |
| `sections/discussion.tex` | 2 844 | 2 841 | −3 | 5 → 5 (all retitled or re-headed) |
| `sections/conclusions.tex` | 363 | 378 | +15 | — |
| **body total** | **15 839** | **15 572** | **−267** | |
| `sections/appendix_reproducibility.tex` | 1 159 | 1 681 | +522 | 5 → **7** |
| **whole manuscript** | **16 998** | **17 253** | **+255** | |

The appendix grew by 522 words because 459 words of software prose were **moved out of §3 into it**.
The body therefore shrinks by 267 words while losing nothing: the only genuinely new body text is the
limits subsection of §2 (+371 words, of which about 300 are the four limits and 70 the lead-in), and
it is paid for by the 459 words that left §3 and by the register removed elsewhere. This was not a
shortening round and no equation, table, figure, citation or limitation was deleted.

---

## 2. Edits by classification

### 2.1 STRUCTURE

| where | change |
|---|---|
| title block | title rewritten: "Backward-branch negative reflection of guided waves from the free edge of a flexoelectric piezoelectric semiconductor plate" |
| abstract | rebuilt in the order system → solved → found → depends on → caveat; 222 words |
| keywords | re-ordered to material class first, mechanism, then method |
| §1 | the five paragraph groups kept; the gap paragraph and the closing contribution paragraph rewritten; the conventions paragraph moved **before** the organisation paragraph, which now ends the introduction and names every section |
| §2 | new subsection **2.10 "Limits of the formulation"** (classical piezoelectric, strain-gradient dielectric, piezoelectric semiconductor without the gradient sector, uncoupled carriers, plus the two reductions used in the text); the section now opens with a one-paragraph map of its own subsections |
| §3 | **the verification material split**: the five mathematical checks stay in §3.5, the 39-test suite, the two regression guards, the four tests around the maximum and the three tests around the reference plane move to the appendix; the "reproducibility" subsection of §3 moves to the appendix as well |
| §4 | subsections retitled and re-ordered rhetorically (physics first): "Refinement study" → "Convergence of the reported values"; "Certification of the maximum" → "Location of the maximum"; "Why the high fraction is not an artefact" → "The maximum read as a modal share"; "Scope of the executed material specialization" → "The material specialisation and the role of the flexoelectric sector". Figure citation order unchanged: 1…10 ascending |
| §5 | "What the reported numbers are, and what they are not" → "The observable: a modal partition of the scattered power"; the limitations of §5.5 broken into five headed paragraphs (geometry / the corner / the carrier model / the parameters / the electrical condition / the constitutive relation) under one subsection |
| appendix | two new subsections: "Automated checks" (the relocated software prose) and "Reproducibility of the plotted numbers" |

### 2.2 LANGUAGE

| where | before → after (representative) |
|---|---|
| abstract | "A … plate is modelled with … and the free-edge problem is solved as a Fourier-reduced spectral Galerkin matching of outgoing modes" → "The edge problem is solved at fixed frequency by a spectral Galerkin expansion through the thickness, matched to the traction-free edge conditions" |
| abstract | "The maximum is a certified local extremum, flat to 0.01 percentage point …" → removed (the flat top is stated in §4.7) |
| §1 | "This closed loop … is the subject of the rapidly developing theory of" → "… is the content of the … theory of" |
| §1 | "The answers turn out to be different in kind: … Reporting the two separately, rather than attributing the effect to the new term, is what the rest of the paper does." → "The answers separate the two mechanisms. … The article reports the two effects with their own numbers and their own controls, at fixed transverse wavenumber, so that the contribution of each can be read without the other." |
| §2 | "It is not a full three-dimensional simulation, and nothing below is reported as one." → deleted (the 2.5D sentence already carries the content) |
| §2 | "Writing $A$ in pascals … is dimensionally wrong" → "A strain-gradient energy of the form (2) therefore assigns a force, and not a stiffness, to $A$ …" |
| §2 | "The solver enforces (45) and refuses to run outside it." → "Every calculation reported below is confined to (45)." |
| §3 | "a rank deficiency raises an error instead of returning a regularised answer" → "a deficient system is reported as such rather than regularised" |
| §4 | "Before any number is read, it is necessary to be precise about…" → "The title names the full flexoelectric framework, and it is worth fixing which part of (5) the calculations exercise before the numbers are read." |
| §4 | "Three independent tests answer the three ways in which such a number could be spurious" → "Three properties of the solution decide whether such a number can be read at face value"; the three italic headings become "A small denominator", "Which branch", "Nearly parallel modes" |
| §4 | "Conflating the two would turn a partition into a reflection coefficient." → "The two are different readings of the same solution." |
| §5 | "the most important thing to say about it is what it does not mean" → "It is a partition of the scattered field rather than a reflectance." |
| §5 | "No claim of priority, equivalence or superiority is made, and the title does not suggest that…" → "The comparison in this section is made against the equations that could be inspected, and no priority claim follows from it: the status of the added term in the full theory remains unresolved." |
| §6 | five items rewritten as physical findings; the two bookkeeping items recast (energy budget; modal share vs reflectance) |

### 2.3 EXPLANATION

| where | what was made explicit |
|---|---|
| §2.1 | the relationship between the 2.5D reduction and the fields it retains, stated once, positively |
| §2.2 | why the contraction $A=\ell^2 c\otimes\delta$ is the one used: major symmetry **and** the exact shear-horizontal spectrum, with the two residuals (2·10⁻¹³ against 3·10⁶) |
| §2.9–2.10 | the four limits of the enthalpy, each with the consequence that matters downstream (the backward branch exists only in the gradient sector; the carriers act through Gauss's law even at $H=0$) |
| §3.2 | the statement that attenuation is taken from the complex root at real frequency |
| §4.1 | the sign change of $v_g,v_E$ explained as a property of the infinite plate, and the edge as what converts into it |
| §5.5 | the corner evidence and its limit ("evidence that the outer band does not accumulate gradient energy", not "a proof that a corner line force is negligible") grouped with the other four limitations |

### 2.4 CAPTION

| figure | change |
|---|---|
| `fig02` | "the backward channel $R_B$ at $\ell=\SI{2}{\micro\metre}$" (wrong symbol, and the wrong quantity) → "the backward share at the reference plane $L=\SI{2}{\micro\metre}$" |
| `fig04` | panel description kept; the raster-spacing sentence replaced by "The top of the response is resolved in the inset, which uses the same data."; "admissibility test" → "conservation bound" |
| `fig07` | "95/95 rows admissible" removed from the caption; the grid description retained |
| `fig08` | "These are normalised profiles, not an independent local-flux validation." → "These are normalised profiles; the local flux is reported as computed and is not independently validated." (caveat kept, negation removed) |
| `tab:controls`, `tab:configurations`, `tab:refinement` | table labels "Certified maximum" → "Maximum"; no cell value touched |

### 2.5 MATHEMATICAL REFERENCE

* Every equation retained, in the same order and with the same labels: 3 in §1, 18 in §2, 6 in §3,
  1 in §4, 1 in §5 (static check: 104 labels, 75 references, all resolved).
* The new limits subsection refers to \eqref{eq:enthalpy}, \eqref{eq:gradient_energy},
  \eqref{eq:added_coupling}, \eqref{eq:continuity} and to the sections that use each limit.
* The appendix now carries the moved checks and still refers to \cref{sec:numerics_verification},
  \cref{sec:results_certification}, \cref{tab:refinement} and \eqref{eq:RB}, all of which resolve.
* `sec:numerics_repro` moved from §3 to the appendix and is still resolvable; no dangling `\cref`.

### 2.6 SCIENTIFIC CONTENT UNCHANGED — the explicit list

| element | status |
|---|---|
| all 45 registered literals of `claims.json` | present, unchanged, in the registered files (`claim_audit.py`: PASS) |
| every numerical cell of `tab:units`, `tab:conjugates`, `tab:groups`, `tab:refinement`, `tab:configurations`, `tab:controls`, `tab:novelty`, `tab:provenance` | unchanged |
| the ten figures, their files and the figure citation order | unchanged |
| the 13 citations and the `references.bib` keys | unchanged (13 bib entries, 13 keys used) |
| headline values 0.0231456 / 0.9467952 / 0.9467954 / 0.995… / 94.68 % / 99.77 % / 1.21 % / 34.2 % / 11.1 % / 2.01 % / −9.85 % / factor 128 | unchanged |
| novelty status **UNRESOLVED**, synthetic $\ell$, $f$, $H$, single edge, corner line force unresolved, linearised carriers, gauge, LaTeX build unverified | all retained, one negation converted to a positive limitation statement in each case |

---

## 3. Register census (the point of the round)

Counted over `main.tex` + `sections/*.tex`, case-insensitive, appendix shown separately because the
reproduction package legitimately names scripts and data files.

| token | at `aabcb77` | now, body | now, appendix | now, total |
|---|---|---|---|---|
| `certif*` (certified / certification) | 39 | 2 (label names only) | 8 | 10 |
| `admissib*` | 20 | 9 (the term "thermodynamic admissibility" and `\eqref{eq:admissible}`) | 1 | 10 |
| `audit` | 19 | **0** | 17 | 17 |
| `gate` | 2 | **0** | 1 | 1 |
| `registry` | 3 | **0** | 3 | 3 |
| `solver` | 21 | 1 (data-availability paragraph) | 5 | 6 |
| `script` | 18 | 2 | 15 | 17 |
| `CSV` | 12 | **0** | 12 | 12 |
| `rather than` | 25 | 27 | — | — |
| `not a` | 41 | 37 | — | — |
| `Furthermore / Moreover / Notably / Remarkably / Importantly / Significantly` | 0 | **0** | **0** | **0** |

The two surviving body uses of "certified" are the label `sec:results_certification`, which is
invisible in the typeset output; "admissibility" survives as the standard continuum-mechanics term for
the positivity of the enthalpy.

---

## 4. What was deliberately left alone

* Every equation, derivation step and constitutive relation of §2.
* Every table, including the two whose headers were renamed.
* The scope paragraph of §4.2 in substance: the flexoelectric term is present, subdominant and
  measured, and the article still does not attribute the mechanism to it.
* The honest caveats: the share is not a reflectance; the maximum is not global; the fold carries a
  factor 128 less flux; $\ell$, $f$ and $H$ are synthetic; the corner is unresolved; the relation to
  the primary theory is unresolved; the manuscript is not compiled.
* The declaration placeholders (`AUTHOR INPUT REQUIRED`) — they are author decisions, not prose.
* The `\path{}` protections in captions and tables, and the static validator's inputs.

## 5. Deferred to round 11 (no figure or datapoint touched here)

| id | item |
|---|---|
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-1 | the `fig02` panel (c) axis label, now that the caption uses $L$ for the reference plane and $\ell$ for the gradient length |
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-2 | `fig05(c)` and `fig09(c)` plot $10^{-12}$–$10^{-16}$ quantities on log axes; the reader cannot tell a floor from a tolerance |
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-3 | three captions are still only decodable with the panel-source map (colour limits, panel-to-column mapping) |
| `ROUND11_SCIENTIFIC_OR_FIGURE_REVIEW_ITEM` R10-4 | whether the schematic panel `fig10(c)` belongs in a results figure at all |

## 6. Verification of the change

| check | result |
|---|---|
| `python paper_a_study/claim_audit.py` | **PASS** — 22 claims, 45 tokens, 5 deprecated strings guarded, figure order 1…10, 9 source-agreement rows passing |
| `python Paper_A_Final_Submission/scripts/static_check.py` | **PASS (exit 0)** — 8 files, 104 labels, 75 references, 13 cite keys, balanced environments |
| figure census | 10 `\includegraphics`, 10 `fig:` labels, in ascending first-citation order |
| table census | 8 tables, 3 in §2, 3 in §4, 2 in §5 |
| citation census | 32 `\cite`/`\cref`-style citation calls, 13 distinct keys, none added or removed |
| LaTeX build | **not attempted: no TeX engine. BUILD UNVERIFIED** |
