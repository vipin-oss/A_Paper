# Paper A — round 12: blocking issues and open items

Six items are open. Two are defects in frozen artefacts, one is a documentation
defect in frozen code, one is a missing tool, one is a missing author input, and one
is a scientific question that no amount of editing can close. Each entry states what
is wrong, what it affects, why it was not fixed here, and what would close it.

Baseline `75d86dc9710d69e2100a85fa5c8b56e9681f7744`.

> **Round-13 status (added 2026-11-07, text below unchanged).** B1 is **closed**
> (the arrow is now derived from the stored solve, guarded at render time, and
> pinned by five tests — `PAPER_A_ROUND13_FIG10_VECTOR_VERIFICATION.md`) and B6 is
> **closed** (the docstring now separates the four diagnostics —
> `PAPER_A_ROUND13_DOCUMENTATION_CORRECTIONS.md`). B2, B3, B4 and B5 remain open
> exactly as described here. The entries below are the record of what round 12
> found, not a current list of blockers.

---

## B1 — fig10(c) draws the backward wavenumber in the wrong direction

**Severity: blocking for the figure round; no effect on any number.**

| | |
|---|---|
| Artefact | `Paper_A_Final_Submission/figures/fig10_field.pdf`, panel (c); source `paper_a_study/generate_final_figures.py`, `def fig10`, the line `arrow((0.333, -0.530), … r"${\bf k}_B$" …)` |
| What is drawn | an arrow from $(-0.82,0.74)$ to about $(-0.57,0.35)$: direction $+x,-y$, i.e. $58^{\circ}$ below the $+x$ axis, length 0.46 |
| What the solver gives | `peak_identity_audit.json`, `cases.operating_point`: $K_B=(0.2451747,\,-5.23\times10^{-6})$ with $k_yd=0.1298118$, so $\vect{k}_B\propto(1,\,0.529)$: direction $+x,+y$, i.e. $27.9^{\circ}$ **above** the $+x$ axis, and $\lvert\vect{k}_B\rvert$ is about half $\lvert\vect{k}_i\rvert$ |
| Where the wrong vector came from | it mixes two ratios — $K_{Bx}/K_{ix}=0.333$ and $\lvert k_y\rvert/K_{Bx}=0.530$ — and takes the sign of the *flux*, not of the wavenumber |
| Text | corrected in this round (L12-14): the prose now states $\vect{k}_B\propto(1,0.529)$, $\vect{P}_B\propto(-1,-0.529)$ and explains that the flux is opposite to the mode's own phase direction |
| Why not fixed here | figure code and accepted figure PDFs are frozen for this round |
| What closes it | one line: `arrow((1.0, 0.529), … r"${\bf k}_B$" …)` with a length scale of about 0.35 to keep the aspect honest, then re-render fig10, re-run `generate_final_figures.py` (which rewrites the panel-source map and the SHA-256s), and re-run the 47 tests |

The flux arrows ($\vect{P}_i$, $\vect{P}_B$) and the intensity maps are correct and
were re-verified against `fig10_field_metrics.json` in this round.

---

## B2 — novelty against the primary 2025 theory is unresolved

**Severity: blocking for submission; not an editorial matter.**

| | |
|---|---|
| Source | Qu, Pan, Zhu, Deng, *Int. J. Eng. Sci.* **208** (2025) 104165, DOI 10.1016/j.ijengsci.2024.104165 |
| Status | closed access; no repository, preprint or accepted-manuscript copy is reachable from this environment; the equations could not be inspected |
| What the paper does about it | compares against the free-energy decomposition as reproduced, with attribution, in an open-access computational paper (Hu et al., Eqs. 4a–4e); states in §5.3 and in `tab:novelty` that the added term is an independent addition *within the equations inspected*; makes no priority claim; and withdraws the claim explicitly in the conclusions' limitations paragraph |
| What would close it | the PDF, or an author's reply, or an institutional access route — then a one-paragraph revision of §5.3 and the status column of `tab:novelty` |
| Risk if left open | a referee who has the paper in hand may find the added term already present; the manuscript's language survives that outcome only because it never claims novelty of the term |

---

## B3 — the corner line force is unresolved pointwise

**Severity: limitation, correctly stated in the paper; not a defect to repair.**

| | |
|---|---|
| State | the outer-band strain-gradient energy share ($0.93$–$1.00$ %, $1.22$–$1.30$ %, $1.18$–$1.26$ % at the three configurations) *decreases* by 6.6–6.8 % between degrees 18 and 30, and the peak-to-mean ratio inside the band is below unity; a corner singularity would show the opposite trend |
| Why that is not a proof | a polynomial basis cannot represent the singular corner traction, so a small band fraction bounds the energy near the corner but not the work a singular corner line force could do |
| Where it is stated | §2.9 (formulation), §5.5 "Geometry" and "The corner", conclusions' closing paragraph, and `corner_assessment.py` behind all three |
| What would close it | a corner-eigenvalue analysis of the higher-order edge problem, or a formulation with corner-enriched functions — a research task, not a revision |

---

## B4 — the typeset manuscript is unverified

**Severity: blocking for submission in any venue that requires a PDF.**

| | |
|---|---|
| State | no TeX engine exists in this environment (`pdflatex`, `latexmk`, `tectonic` all absent); the source is validated statically only: 8 files, balanced environments, 104 labels, 75 references resolved, 13 citation keys against 13 bib entries, all ten figure files present |
| Consequence | the PDF quoted by this project does not exist; no older PDF is cited, and none is shipped as if it were current |
| Risk | undefined macros or package-version differences (notably `siunitx` v2 vs v3) can still fail at build time even though the source is consistent |
| What closes it | a TeX Live (or `tectonic`) environment; `cd Paper_A_Final_Submission && pdflatex main && bibtex main && pdflatex main && pdflatex main`, then a read of the page proofs for overfull boxes — the source sets `\emergencystretch` for exactly that reason |

---

## B5 — five declarations need the author

**Severity: blocking for submission; must not be invented.**

| item | state in `main.tex` |
|---|---|
| competing interests | `AUTHOR INPUT REQUIRED` |
| funding (agency, sanction number, date, or an explicit "none") | `AUTHOR INPUT REQUIRED` |
| CRediT / author contributions | `AUTHOR INPUT REQUIRED` |
| acknowledgements | `AUTHOR INPUT REQUIRED` |
| use of generative tools | `AUTHOR INPUT REQUIRED` — the journal's policy must be applied, and the statement must describe the tooling actually used |
| ethics | answered: not applicable (no human or animal participants) |
| data availability | answered: public repository, no dataset withheld, which the package substantiates |

No funder, affiliation, role or disclosure wording was drafted, because a wrong
declaration is worse than a visible gap. The placeholders are deliberately
conspicuous and are counted by the static check as part of the source.

---

## B6 — `peak_search.py`'s docstring contradicts its own output

**Severity: documentation only; code frozen this round.**

| | |
|---|---|
| Location | `paper_a_study/peak_search.py`, module docstring, last paragraph |
| Text | "Convergence is measured three ways and reported separately: Galerkin degree, quadrature order, and — because $R_B$ is evaluated on a tracked branch — the sensitivity to the branch-tracking path. The last one is not a discretisation error, but near a zero-group-velocity fold it dominates the reproducibility of the printed digits, so it is measured rather than assumed." |
| Contradiction | the measurement returns 0.0 (`verdict.tracking_path_relative_spread`), in this delivery and in the previous one; what is large near the fold is the *coarse-search sampling error* ($8.36\times10^{-6}$), a different quantity |
| Proposed replacement | "… and the sensitivity to the branch-tracking path. The last one is not a discretisation error and is measured rather than assumed; in the delivered data it is zero to the last stored digit, while the sampling error of the coarse raster is $8\times10^{-6}$ and is reported separately as `restart_spread`." |
| Why not applied | this round freezes code; a docstring change would also require a regeneration of any record that hashes the file |

---

## Carried observations, not blocking

| id | observation | why it is not an issue |
|---|---|---|
| O1 | fig01(d)'s grid ($\Delta k_xd=0.03$) cannot show the attenuation maximum at the fold | the text now says so and points to `tab:configurations`, which evaluates 87.2 dB/mm at $k_xd=0.5275$ |
| O2 | the abstract does not repeat the "local maximum" qualifier | the body states it three times; a fifth qualification would crowd a 250-word abstract |
| O3 | six contrastive uses of "reflectance" remain | they are the disclaimer that keeps 94.68 % from being read as a reflectance |
| O4 | the frequency-to-share amplification ($\sim10^{3}$) is measured but not printed | a number whose only record would be a review-time run does not belong in a paper whose datasets ship |
| O5 | the battery was not re-executed in this round | no producer, dataset or solver file changed; the round-11 log remains the last full execution |
| O6 | `static_validation.txt` and `claim_audit.json` are rewritten by every audit run | they are records of the last run, tracked on purpose; this round's diffs are the word count (16 355 → 16 634) and the count of the 10⁻⁸ bound tokens (7 → 8) |
