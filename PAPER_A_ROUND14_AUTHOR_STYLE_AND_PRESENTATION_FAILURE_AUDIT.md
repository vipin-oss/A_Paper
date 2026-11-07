# Round 14 — failure audit against the author's own published style

**Paper A:** *Backward-branch negative reflection of guided waves from the free
edge of a flexoelectric piezoelectric semiconductor plate.*
**Branch:** `arena/ea7ca4dd-a-paper`. **Round type:** presentation and
documentation reconstruction. No physical model, constant, boundary condition,
solver, root classification, numerical result or dataset was changed.

---

## 1. What this audit is, and what it is not

This is a reading of the round-13 manuscript against the mathematical style of
the author's own published articles, and against what a supervisor sees when he
opens the PDF. It is deliberately *not* another count of automated tests: the
round-13 report already established that the code passes its own gates. A paper
that passes its gates and reads like an engineering log is still a failed paper,
and that was the round-13 failure mode.

## 2. Evidence base, and its limit

Read in full, from the author's own Google Drive:

| Evidence | Reference | What it supplies |
| --- | --- | --- |
| **A1** | Gupta, Awwad, Ismail, Ahmad & Das, *Int. J. Numer. Methods Heat Fluid Flow* (2025), DOI 10.1108/HFF-04-2025-0254 | structured Purpose/Design/Findings abstract; nomenclature block; numbered equation cascade `(9.1)`–`(9.7)` inside a **Case-I / Case-II** limiting-case subdivision; nonlocal `ρ(1−ξ²∇²)∂²u/∂t²` |
| **A2** | Gupta, Barak & Ahmad, *Physica Scripta* **99** (2024) 025515, DOI 10.1088/1402-4896/ad1972 | five-paragraph introduction with dense citation clauses; "Fundamental equations" as the opening formulation section; "Limiting case" bullet list; harmonic ansatz `exp[i(k_xx − ωt)]` followed by **explicit real coefficient definitions** (`b₁₁ = ρω² − c₁₁k², …`); a titled "Solution procedure" |

**Limitation, stated plainly.** Five author papers were named in the round-14
brief (Physica Scripta 2024; Composite Structures 2025; IJNMF 2025; IJNMF 2026;
Scientific Reports 2026). Two were obtained and read in full (A1, A2). Three were
**not** obtained in this session: the Composite Structures 2025 article, the
IJNMF 2026 article and the Scientific Reports 2026 article. The comparison below
is therefore a comparison against **two** full texts, not five, and no claim of a
fresh direct comparison with the other three is made anywhere in this round. No
figure, sentence or symbol was copied from A1/A2; only structural habits were
adopted, because those habits are what a supervisor recognises as his own.

## 3. The observed style, as a matrix

| Dimension | A1 (IJNMF 2025) | A2 (Phys. Scr. 2024) | Round-13 Paper A | Round-14 Paper A |
| --- | --- | --- | --- | --- |
| Abstract | labelled Purpose / Design / Findings | one continuous paragraph | one continuous paragraph, numbers-first | kept continuous, numbers-first (a physics abstract, deliberately not a Purpose/Design form: the labelled form belongs to an engineering journal) |
| Nomenclature | present, column layout | present, column layout | **absent** | added after the abstract: 36 symbols in a two-column table |
| Formulation title | "Fundamental equations" | "Fundamental equations" | "Mathematical formulation" | "Mathematical formulation" (kept: it is the more accurate title for a variational derivation) |
| Equation numbering | per-section cascade `(9.1)…` | per-section cascade `(2.1)…` | global `(1)…(N)` | global, unchanged (renumbering would break every cross-reference in six reports for no scientific gain) |
| Derivation habit | states the constitutive assumption, then differentiates the potential, then names the partners | writes the ansatz, then **defines each coefficient explicitly** | states results of differentiation, gives no intermediate step | derivation of the constitutive partners from one enthalpy, with the variation identities and the two integrations by parts written out; strain and strain-gradient amplitudes tabulated under the ansatz |
| Limiting cases | "Case I / Case II" subdivision | bulleted "Limiting case" | a subsection, "Limits of the formulation" | kept as a subsection, with the algebraic collapse of the quartic operator stated and verified |
| Solution section | "Solution procedure" | "Solution procedure" | "Solution method" | **"Solution of the problem"**, opening with the weak form |
| Results | numbered effects, each tied to a figure | — | 14 subsections, each a report on a figure | merged into "Numerical results and discussion", discussion demoted to a subsection of it |
| Reproducibility | absent | absent | 205-line appendix of scripts, commands, versions and test counts | 37-line appendix on resolution, convergence and data availability; the software record moved to a separate supplementary document |

## 4. Section-by-section: how Paper A differs, and how it is better

1. **Introduction.** A1 and A2 open with a formulation and a citation cascade;
   Paper A opens with a physical loop (strain gradient → polarisation → carrier
   redistribution → field → strain) and closes with two questions that the
   article answers separately. Round 13 spoiled this by cutting the section into
   `1.1 The added coupling and its reciprocals` and `1.2 Scope and
   organisation`, a heading structure no article of A1/A2 uses for an
   introduction. Round 14 removes both headings: one continuous Introduction,
   seven paragraphs, no subsections, with the three equations it used to carry
   relocated to the formulation where the enthalpy is actually differentiated.
   *Improvement without copying:* the intro now states the same argument in the
   author's paragraph rhythm (claim, citation clause, consequence) but its
   content is a scattering problem, which neither A1 nor A2 treats.
2. **Mathematical formulation.** A1/A2 differentiate a potential and list the
   resulting coefficient relations; Paper A now does the same and goes further:
   the variation identities, the virtual work, the two integrations by parts and
   the sign of the double divergence are written out, and the reduction to a
   single propagation direction yields the quartic operator explicitly. This is
   the section where the round-13 manuscript was thinnest: it *stated*
   `ρü_j = ∂_iσ_ij − ∂_i∂_kτ_jik` and *stated* that the problem is quartic.
3. **Solution of the problem.** A2's "solution procedure" stops at the
   determinantal condition. Paper A gives the weak form, names the five
   contributions of the enthalpy term by term, connects the assembled polynomial
   to the quartic of the formulation section, and then treats root selection and
   edge matching — material A2 does not have.
4. **Numerical results and discussion.** A1/A2 report parametric trends; Paper A
   reports one scattering problem and must justify a partition. Round 13 split
   the reading (Results) from the meaning (Discussion) into two top-level
   sections, which reads as two papers. Round 14 merges them: 14 result
   subsections followed by one discussion subsection with five sub-subsections.
5. **Conclusions.** Unchanged in substance; the round-13 text already speaks of
   physics and not of code.
6. **Appendix.** This was the single worst stylistic failure of round 13: a
   reproduction appendix listing `test_model.py`, 52 tests, `~25 s`, mutation
   counts and shell commands, sitting inside a mathematics paper. It is gone;
   the article keeps the statements a referee needs (resolution, convergence,
   conservation, data availability) and the software record is now a separate
   document.

## 5. Residual defects this round did **not** fix

- **No compiled PDF.** No TeX engine exists in this environment (17 attempts in
  round 13; nothing changed). Typeset output remains **BUILD UNVERIFIED**. Every
  structural claim here is a claim about the LaTeX source, validated statically
  (108 labels, 82 references, 13/13 citations, environments balanced), not about
  a rendered page.
- **Figure inspection is partial.** F1, F2, F3 and F10 were inspected at full
  size after re-rendering; F4 and F7 at contact-sheet scale; F5, F6, F8 and F9
  only at contact-sheet scale. At that scale the annotation density of F5(c) and
  F8(c,d) remains hard to read at column width. This is a known, unfixed risk,
  not a passing judgement.
- **Equation numbering** is global rather than per-section. A supervisor reading
  A1/A2 will notice; changing it now would invalidate every cross-reference in
  the six round reports and in `claims.json` for a purely cosmetic gain. Flagged
  as an open cosmetic item for a future round.
- **Novelty remains UNRESOLVED.** The closest published work (Qu, Pan, Zhu &
  Deng, *Int. J. Eng. Sci.* **208** (2025) 104165) is closed access.

## 6. Judgement

| Criterion | Verdict |
| --- | --- |
| Reads as a mathematical research article rather than a log | improved, **not proven** (no rendered page) |
| Section order matches the author's habitual order | **met** |
| Introduction is one continuous section | **met** |
| Derivations are written, not asserted | **met** for the constitutive and variational steps; **partial** for the assembled coefficient matrices (structure and degree are derived, closed-form entries are not claimed) |
| Software/audit prose removed from the article | **met** |
| Style comparison grounded in the author's own papers | **met for two of five**; three unavailable and stated as such |

No blanket pass is claimed for this round.
