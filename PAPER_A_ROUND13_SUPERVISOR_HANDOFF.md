# Paper A — round 13: supervisor handoff

**Read this one first.** It is short by design: what changed, what did not, and what
is left for you.

| | |
|---|---|
| Repository | `vipin-oss/A_Paper`, branch `arena/ea7ca4dd-a-paper` |
| Baseline this round started from | `3827543016ece4a9d0612e861bf75425457291bf` (round 12) |
| Delivery | `Paper_A_Complete_Project_round13.zip` — size, SHA-256 and the commit SHA are in `downloads/README.md` and in the delivery message that accompanies this archive |
| Manuscript | `Paper_A_Final_Submission/main.tex` (one tree, seven section files, ten figures) |
| Typeset PDF | **none.** `BUILD UNVERIFIED` — no TeX engine exists in the authoring environment and none could be installed (report 4, §1) |

---

## 1. What this round was

A **targeted closure round**. Not a rewrite, not a new study. It closed the two
defects that round 12 left open, corrected one report-level number and one caption,
found and fixed the two counts that its own new tests made stale, and re-verified
everything the changes could touch.

Scope was fixed in advance and is recorded in
`PAPER_A_ROUND13_PRE_EDIT_CLOSURE_AUDIT.md`, which was written **before** the first
edit and classifies every item as CONFIRMED, ALREADY RESOLVED, DIFFERENT QUANTITY,
UNVERIFIED or NOT A DEFECT.

---

## 2. What changed

### 2.1 Figure 10(c) — the one scientific-looking defect, now closed

The panel drew the backward **wavenumber** along $(0.333,-0.530)$: one ratio from
$K_{Bx}/K_{ix}$, one from $\lvert k_y\rvert/K_{Bx}$, and the sign of the **flux**.
It pointed $57.9^{\circ}$ below the $+x$ axis and was 2.2× too long. The solved mode
has $\vect{k}_B\propto(1,\,0.5295)$, i.e. $+27.9^{\circ}$ **above** the axis, and
$\lvert\vect{k}_B\rvert/\lvert\vect{k}_i\rvert=0.371$.

All four arrows in the panel are now derived from the stored solve
(`fig10_field_metrics.json` → `primary_wavenumbers`, a new block written by the
producer), drawn at the solved proportions, and checked at render time by a guard
that raises if the wavenumber is not in the first quadrant or departs from the solved
direction. Five new tests pin it; a deliberately reversed arrow fails three of them.

Evidence: `PAPER_A_ROUND13_FIG10_VECTOR_VERIFICATION.md` (before/after panel
images, the solve, the diff, the visual inspection).

### 2.2 `peak_search.py` — the docstring that contradicted its own output, now closed

It said the branch-tracking-path sensitivity "dominates the reproducibility of the
printed digits". The delivered spread is **0.0**; the quantity that is $8.4\times10^{-6}$
is the coarse raster's sampling error (`restart_spread`). The docstring now names the
four diagnostics separately and says which one is large near the fold. The algorithm,
the tolerances and `peak_search.json` are untouched.

### 2.3 One report-level misattribution, and one caption

* 62.2973 % was attached to $k_xd=0.55$ in the round-12 correction history and in
  the download README. It belongs to the **reported peak** $k_xd=0.5275$ with
  $H/H^{*}=+0.05$; at 0.55 the coupling-on share is 0.5221. Both files are corrected
  and carry a dated note. **The manuscript was right:** §4.10 attaches 0.6230 to "the
  maximum".
* The fig10 caption said panel (c)'s arrows are "the solved flux directions"; two of
  the four are wavenumbers. Two words added.

### 2.4 Two counts

The suite grew from 47 to 52 tests. The appendix said 47 in three places and the
package README in one; both now say 52 (~25 s, unchanged).

**Nothing else was touched.** No equation, constant, boundary condition, carrier
model, discretisation, solver, tolerance, dataset, table or reported number changed.
The fig10 field map — 22 801 rows — was regenerated and came back **byte-identical**.

---

## 3. What did not change

| | |
|---|---|
| Headline result | $R_B=0.9467952$ (94.68 %) at $k_xd=0.5275$, a **local** maximum inside the declared window, flat to 0.01 pp over $[0.5266,0.5277]$; refined argmax $0.9467954$ at $0.52752$; 16.6547 GHz; operating point 0.0231456; edge plane 0.9855722; $k_xd=0.55$ 0.5791800; propagating 99.77 % |
| Equations, constants, boundary conditions | untouched |
| All ten figures except fig10(c)'s arrow | untouched, byte for byte (the other nine PDFs were not even re-rendered) |
| Datasets | untouched except the eleven-line metadata block in `fig10_field_metrics.json` |
| Tables | untouched |
| Round-10/11/12 work | preserved; the two round-12 documents whose status changed carry a dated note, and their bodies are unedited |

---

## 4. Validation status

| gate | result |
|---|---|
| unit and scientific suite | `Ran 52 tests in 24.461s — OK` (47 carried over + 5 new) |
| new fig10 vector tests | 5/5 pass; a reversed arrow fails 3 of 5 |
| claim registry | PASS — 23 claims, 46 tokens, 5 deprecated guarded, 10 figures in citation order, 11/11 source rows |
| mutation harness | PASS — 15 mutants, 15 caught |
| phase-speed audit | PASS |
| static manuscript check | PASS — 104 labels, 75 references, 13/13 citations, 16 656 words |
| fig10 dataset reproducibility | field map byte-identical; metrics JSON deterministic across two runs |
| full 18-gate battery | not re-run — no producer logic changed; the last full run remains round 11's **18 PASS / 0 FAIL / 1 SKIP** |
| LaTeX build | **BUILD UNVERIFIED** |

---

## 5. Scientific status — unchanged, and stated plainly

| issue | status | where |
|---|---|---|
| **Novelty against Qu, Pan, Zhu & Deng (2025)**, *Int. J. Eng. Sci.* 208, 104165 | **UNRESOLVED.** The primary source is closed access and no legitimate copy is reachable here; the comparison stands against the free-energy decomposition as reproduced in an open-access paper, with attribution. **No priority claim is made**, and none should be inferred from the absence of a match | §5.3, `tab:novelty` |
| **Corner line force** | **unresolved pointwise.** The corner band carries 0.9–1.3 % of the strain-gradient energy and its share drifts 6.6–6.8 % between degrees 18 and 30, which is *not* proof that a singular corner traction vanishes. Closing it needs a corner-eigenvalue analysis or an enriched basis — a separate investigation | §2.9, §5.5, conclusions |
| **Synthetic parameters** | $\ell=50\ \mathrm{nm}$, $f_{3zz}=1\ \mathrm{nC/m}$ and every $H$ value are **synthetic**, labelled as such in the text and in the package README. No experimental calibration of ZnO is claimed | §4.2, §5 |
| "94.68 %" | a **backward outgoing modal self-power fraction**, not a total reflectance; the incident flux at the maximum is 128× smaller than at the operating point | §3.3, §4.8 |
| "maximum" | local to the declared search and parameter set, never global | §4.7 |

Round 13 changed none of these statuses, and could not have.

---

## 6. What you must supply before submission

Five declarations in `main.tex` are visible placeholders reading
`AUTHOR INPUT REQUIRED`. They were **not** filled in, because a wrong declaration is
worse than a visible gap.

| # | item | what is needed |
|---|---|---|
| 1 | Competing interests | a statement, or an explicit "none" |
| 2 | Funding | agency, scheme, sanction number and dates — or an explicit "none received" |
| 3 | Author contributions (CRediT) | the actual roles of the actual authors |
| 4 | Acknowledgements | anyone whose contribution is not authorship — or "none" |
| 5 | Generative-tool disclosure | the journal's policy applied to the tooling actually used; the wording is the author's, not the round's |
| 6 | Ethics | already answered: not applicable (no human or animal participants) |
| 7 | Data availability | already answered: public repository, nothing withheld — and the package substantiates it |

---

## 7. Your personal final-reading checklist

Suggested order, about 40 minutes for the manuscript and 20 for this round's evidence.

**Before opening the source**

1. Download the round-13 archive, unzip, open `START_HERE.txt`.
2. If you have LaTeX: run the four commands in report 4 §4 and read the PDF you get.
   Nothing in this package is a substitute for that — the typeset layout has never
   been seen by anyone.
3. Look at `figures/fig10_field.pdf` panel (c) at reading size: $\vect{k}_B$ up-right
   at the steeper angle, $\vect{P}_B$ down-left, $\vect{k}_i$ and $\vect{P}_i$
   up-right at the shallower angle, $\vect{k}_B$ visibly shorter than $\vect{k}_i$.

**The manuscript, in the order a referee reads it**

4. Title, abstract, keywords — does the abstract still promise only a modal share at
   a local maximum? (It should.)
5. §1 — the four sectors and the gap; no priority claim.
6. §2.7–2.9 — the scaled-units clause and $\alpha_{\mathrm{d}}$; the four limits.
7. §3.1 — "a polynomial of degree four"; §3.10–3.11 — the three admissibility
   conditions and the consistency-not-validation caveat.
8. §4.6–4.8 — the reproducibility paragraph, the flat top, and the "modal share, not
   a reflectance" paragraph. These are the three the referee will attack.
9. §4.9 — the energy budget with its four numbers and their factor-of-two note.
10. §4.10 — the coupling decomposition, with 0.6230 clearly attached to *the maximum*.
11. §4.15 and the fig10 caption — the two arrow pairs and the word "negative".
12. §5.3 and `tab:novelty` — the `UNRESOLVED` status and the symbol collision.
13. §5.5 — the six limitations, including the corner.
14. §6 — five results, one per sentence; the closing limitations paragraph.
15. Appendix — the package table (52 tests), the command list, the environment note.
16. Declarations — the five placeholders you are about to fill.

**The evidence for this round**

17. `PAPER_A_ROUND13_PRE_EDIT_CLOSURE_AUDIT.md` §2 and §3 — what was confirmed, and
    the solve that proves it.
18. `PAPER_A_ROUND13_FIG10_VECTOR_VERIFICATION.md` §5–6 — the visual inspection and
    the reversal test.
19. `PAPER_A_ROUND13_DOCUMENTATION_CORRECTIONS.md` §5 — the sweep, item by item.
20. `PAPER_A_ROUND13_TARGETED_VALIDATION.md` §2 — the byte-identical field map and
    the threading observation.

---

## 8. Submission readiness

| question | verdict |
|---|---|
| Are the numbers right? | **Yes, as far as this environment can establish.** 52 tests, 15 mutants, a claim registry, byte-identical regeneration of the one dataset that was re-run, and a figure whose annotations now come from the same records as its pixels |
| Is the manuscript internally consistent? | **Yes.** 104 labels, 75 references, 13/13 citations, claim audit clean, no known data-to-text contradiction |
| Is it typeset? | **No.** `BUILD UNVERIFIED` |
| Can it be submitted today? | **No.** Three things are missing and none of them is editorial: the declaration block (§6 above), the prior-art answer (§5), and a build you have looked at |
| Is there anything in this round you need to re-check? | One judgement call: the $\vect{k}_B$ arrow is drawn at the solved **magnitude** ratio to $\vect{k}_i$, so it is visibly short. That is physically right and visually less striking than the old, wrong arrow. If you prefer a schematic length to a to-scale one, change `length_i * dirs["magnitude_ratio"]` back to a fixed `0.55` — the direction, which is the part that was wrong, is guarded either way |

**Overall: numerically and internally ready; not submission-ready, for the three
non-editorial reasons above.** This round closes defects. It does not, and was not
meant to, close questions.
