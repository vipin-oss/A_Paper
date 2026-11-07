# Paper A — round 12: section-by-section review

**What this round is.** A final editorial and scientific review of the manuscript
`Paper_A_Final_Submission/main.tex` and its seven section files, section by
section, against four criteria: mathematics, physics, language, and what a journal
requires. Content is frozen: no governing equation, constitutive constant,
boundary condition, solver, dataset, figure PDF or numerical result was changed.
Nineteen prose defects were found and repaired (`PAPER_A_ROUND12_EDIT_LEDGER.md`),
one frozen figure defect is reported instead of repaired
(`PAPER_A_ROUND12_BLOCKING_ISSUES.md`, B1), and the two round-11 reporting errors
were corrected before any of this (`PAPER_A_ROUND12_PRELIMINARY_EVIDENCE_CORRECTIONS.md`).

Baseline `75d86dc9710d69e2100a85fa5c8b56e9681f7744`. Sections were read in full, in
order, with the stored records open beside them.

**Headline: how much was wrong.** Ten of the nineteen edits are places where the
prose disagreed with the paper's own delivered data — factors of three, units of
µs vs mm, a swapped pair of abscissae, a vector that is not a direction. None of
them changes a result, a table entry or a figure. That pattern is worth stating
plainly at the start: the numerical work of this paper has been verified
exhaustively (ten figures, 47 tests, 15 mutants, 18-gate battery), and the prose
around it had not been verified against it with the same care until this round.

---

## 0. How each section was read

For every section the same checklist was applied, and the answers are recorded per
section below.

| # | check | what failing looks like |
|---|---|---|
| 1 | every displayed equation is dimensionally consistent and its symbols are defined once | a formula in scaled units written as if it were dimensional; one symbol with two meanings |
| 2 | every number equals a stored value at the printed precision | a factor of three written as a factor of nine |
| 3 | every number is traceable to a named record | an amplification quoted from nowhere |
| 4 | no claim is stronger than its evidence | "the maximum" for a local maximum; "reflectance" for a modal share |
| 5 | logical connectives survive a hostile reading | "five limitations" before six paragraphs |
| 6 | register is the author's: declarative, technical, no promotion | "novel", "significantly", "we believe" |
| 7 | nothing depends on a symbol that the frozen figures do not use | $\ell$ for a distance |
| 8 | submission-level statements are accurate and honestly incomplete | declarations that invent a funder or a CRediT role |

---

## 1. Title, abstract and keywords — `main.tex`

**Read.** Title, abstract (one paragraph), six keywords, declarations, appendix
include, bibliography hook, and the build note in the source comments.

| criterion | finding |
|---|---|
| Mathematics | none: the abstract carries no formula beyond symbols already defined in the body |
| Physics | the abstract's four quantitative statements (2.31 %, 94.68 %, 99.77 %, factor 128) all match the records; the "modal share, not a reflectance" disclaimer is present and correct |
| Language | two defects, both repaired: "The figure is a modal share" (no antecedent for "the figure" in an abstract), and "Removing the coupling leaves the partition unchanged" without the qualifier that the removal is the *added* coupling and the change is 1.21 % (L12-19) |
| Submission-level | the abstract states the synthetic status of $\ell$, $f$, $H$ and the unresolved corner in its last two sentences, which is what a referee asks for first; the keywords are specific and none is a slogan |

**One structural observation, not an edit.** The abstract does not mention that the
reported maximum is *local within a declared window*. It says "reaches 94.68 % at
$k_xd=0.5275$, where the incident and backward wavenumbers differ by 0.4 % and the
group velocity vanishes" — true, and the locality is stated in §3.6, §4 and the
conclusions. Adding a fifth qualification to a 250-word abstract would cost more
than it buys; the decision is recorded here so that it is a decision.

**Declarations.** Five items are marked `AUTHOR INPUT REQUIRED` (competing
interests, funding, CRediT, acknowledgements, generative-tool disclosure) and one
is answered on the merits (ethics: not applicable). Data availability points at the
public repository and claims no withheld dataset, which the package substantiates.
No funder, affiliation, role or disclosure text was invented — **B5**.

---

## 2. §1 Introduction — `sections/introduction.tex`

**Read in full.** Motivation (guided-mode scattering at an edge), the four sectors
of the model, the notion of a backward branch, the gap in the literature, the
contributions, and the road map.

| criterion | finding |
|---|---|
| Mathematics | no equations; symbols introduced here ($R_B$, $k_xd$, $H$, $\ell$) are the ones used later |
| Physics | the one substantive claim — that strain-gradient elasticity supplies a branch whose energy flux opposes its phase velocity — is supported by §3.1 and §3.7 and, in the limit $\ell=0$, removed (§2.9, §3.7). No defect |
| Language | consistent register; no promotional phrasing; the contributions are stated as computations performed, not as advances claimed |
| Submission-level | the introduction does not claim priority against the 2025 primary source; that claim is explicitly withheld in §5.3 and the status remains `UNRESOLVED` |

**No edit.** The introduction was the cleanest section in the manuscript.

---

## 3. §2 Governing equations — `sections/governing_equations.tex`

**Read in full,** including the tables of units, conjugates and dimensionless
groups, the four sector limits, and the thermodynamic-admissibility subsection.
Symbols were checked against the solver's own names where a mismatch would be
material.

| criterion | finding |
|---|---|
| Mathematics | one real defect and one notation defect. **(a)** The dissipation integral of §2.7 is written in the scaled variables of §2.8 (dimensionless $\widetilde\mu$, dimensionless $\alpha_{\mathrm{d}}=D/dc_s$, scaled $k$ and $z$) but was presented as a dimensional companion of a dimensional energy identity; the text now says which variables it is written in. **(b)** The same symbol $\alpha$ was used for that dimensionless group and, from §3 onward, for the spatial attenuation $2\lvert\Imag k_x\rvert$; the group is now $\alpha_{\mathrm{d}}$ and the collision is stated once (L12-16) |
| Dimensional audit | every group in `tab:groups` recomputed from `a0/materials.json`: $Q=0.0746$, $\alpha_{\mathrm{d}}=0.828$, $\lambda=0.250$, $f=2.56\times10^{-3}$, $h=\eta\times0.212$ — all MATCH. $H^{*}=H_{\text{bound}}/\sqrt5=4.01\times10^{-22}$ (so $s=0.2$ at the plotting normalisation), $H_{\text{ref}}=d\sqrt{ac_{44}}=1.89\times10^{-21}$, $c^{*}=154.4$ GPa, $s\le4.8\times10^{-4}$ at the tabulated extreme. The Schur bound, its attainment value $8.97\times10^{-22}$ and the "margin of two thousand" are arithmetically consistent with each other |
| Physics | the four limits of §2.9 are each checkable against §3 and the test suite: $\ell=f=H=0$ (classical), $H=0$ (strain-gradient dielectric), carriers without gradient, gradient without carrier coupling. The claim that removing the gradient sector removes the backward branch is the same claim the matched controls test in §3.7 and is not overstated here |
| Language | the sign conventions of §2.3–2.5 are stated once and used consistently; no promotional phrasing |
| Submission-level | the synthetic status of $\ell$, $f$, $H$ is stated in §2.8–2.9 rather than deferred to the limitations, which is the right place |

**Watcher's note.** The dissipation formula is the *only* place in the manuscript
where a displayed equation is not in the units its neighbours use. It is now
labelled; it is not changed, because changing it would change what the solver
computes and the energy identity closes to $3.4\times10^{-16}$ in the units
actually used.

---

## 4. §3 Solution method — `sections/numerical_methods.tex`

**Read in full.** Galerkin basis and the two electrical spaces, the degree-four
polynomial system, the temporal and spatial routes, edge matching and the
classification rule, the three admissibility conditions, and the five verification
paths.

| criterion | finding |
|---|---|
| Mathematics | one defect, repaired: the semi-discrete system was called a "three-term polynomial" while the displayed double sum spans the five powers $k_x^{0\ldots4}$ and the same section calls it "the quartic problem". It is now "a polynomial of degree four", and the following sentence no longer repeats the count (L12-15) |
| Checked, unchanged | the outgoing criterion (half-space decay for complex roots, sign of the axial power for real ones) matches `model.py` `edge()`; the $10^{-12}$ rank cut, the $1.6\times10^{2}$ condition number and the $10^{-12}$ scaled residual are the values at the production degree; the three admissibility conditions (conservation, degree convergence, flux-fraction resolution) are the three the figures actually record |
| Physics | the statement that the two solution routes are a consistency check rather than a physical validation is stated and repeated in §3.11 and in the fig09 caption — a rare and correct piece of self-limitation |
| Language | one long sentence in §3.2 on the routes was left alone: it is grammatical and the author's |
| Submission-level | the reader can reproduce the classification rule from the text alone |

---

## 5. §4 Results — `sections/results.tex` (the section that needed the work)

Eleven of the nineteen edits are here. They are grouped by subsection.

### §4.1 Dispersion and wave speeds

* **Phase-speed endpoints transposed** (L12-01): the text attached 105.8 km/s to
  $k_xd=1.05$ and 20.0 km/s to "near the cutoff"; the data have the opposite
  assignment. A reader who plots the panel can see this in one glance.
* **"A clear ordering in $H$" for the linewidth** (L12-02): there is no ordering in
  signed $H$ — the curves run $0<-0.025<+0.025<-0.05<+0.05$ at $k_xd=1.05$. The
  text now says smallest at $H=0$, rising with $\lvert H\rvert$, more strongly for
  positive coupling.
* **"Peaks sharply at $k_xd\approx0.52$"** (L12-02): the plotted raster steps over
  the fold by 0.03, so its own maximum is at the sample 0.54; the fold value
  (87.2 dB/mm at $H=0$) is tabulated elsewhere. The text now distinguishes the
  sampled maximum from the physical one and points to the table.
* Checked and unchanged: the 184 kHz / 1.1×10⁻⁵ dispersion shift, the 3.5 %/6.4 %
  $v_g$–$v_E$ agreement, the −188/−189 → +1097/+1136 m/s span, the sign change
  just below 0.53, the 1.4 kHz–0.27 MHz linewidth range and the
  0.23–456 dB/mm attenuation range. All MATCH.

### §4.2 Material specialisation

* Checked and unchanged: $f_{3zz}=1$ nC/m as a low-end synthetic value, the
  $10^{-4}$-level contribution of the flexoelectric term (−0.012 % at the operating
  point, −0.009 % at 0.55, 0.0004 % at the maximum), and the framing that the paper
  does *not* attribute the effect to flexoelectricity. This is the section that
  keeps the title honest, and it does.

### §4.3 Carrier density and mobility

* **A factor-of-three sweep was described as factors of nine, ten and five**
  (L12-05). The stored columns scale exactly linearly with $n_0$ and with $\mu$;
  the same triple of wrong factors appeared in two sentences. Both now read "a
  factor of three", and the text adds the reason (the two sweeps are the same
  sweep, because density and mobility enter through their product).
* **"Reflectance" for the backward share** (L12-06): the one place in the article
  where the word was used loosely rather than contrastively.
* **Panel (c) tail** (L12-06): "falls to $10^{-7}$ at $k_xd=0.9$" describes a value
  the data put four orders lower ($1.6\times10^{-11}$); the $10^{-7}$ level is
  crossed near 0.8.
* Checked and unchanged: $R_B=0.5796$ at 0.55, the 0.2 % collapse of the five
  density curves, the $Q=0.075<1$ interpretation.

### §4.4 Thickness and gradient length

* **Abscissae** (L12-04): the gradient-length percentages are the values at
  $k_xd=0.145$ and $1.000$; the text said 0.15 and 1.05, and the grid contains
  neither. (Round 11 had already moved this sentence once, from 0.1/1.05.)
* **Wording** (L12-03): 30.4 GHz and 10.5 GHz are the two ends of the *family*
  (120 nm and 320 nm), not of one branch; "the branch moves from … to …" implied a
  single curve.

### §4.5 Backward conversion along the branch

* Checked and unchanged, all MATCH: 0.0399 at 0.30 (16.676 GHz), 0.9468 at 0.5275
  (16.6547 GHz), 0.0173 at 0.75 (16.688 GHz), the 16° span of the energy angle, the
  0.9960 wavenumber ratio, $\lvert v_g\rvert<1$ m/s at the fold against
  −180 / +355 m/s at the window ends, the single-humped response over the window.

### §4.6 Convergence of the reported values

* **An untraceable sensitivity pair** (L12-07): the paragraph claimed that
  $1.8\times10^{-12}$ relative frequency change moves $R_B$ by $5.6\times10^{-6}$
  and concluded a $\pm6\times10^{-6}$ reproducibility. Neither number exists in the
  records, and a direct evaluation gives an amplification of order $10^{3}$, i.e.
  $\sim1.5\times10^{-9}$ (see the traceability audit §5). The paragraph now rests on
  the registered spreads — degree $6.2\times10^{-9}$, quadrature
  $4.3\times10^{-10}$, three tracking paths identical — plus the fact that the
  argmax-to-sample offset $1.4\times10^{-7}$ is three orders inside the flat top.
* Checked and unchanged: the $\pm0.0009$ half-width, the four certified values and
  their spreads in `tab:refinement`, the 1.9×10² condition bound, the 3×10⁻¹⁵
  residual bound, the 97.1 %/88.4 % flux fractions.

### §4.7 Location of the maximum

* **A justification removed** (L12-08): "$1.4\times10^{-7}$ lower, which is below
  the reproducibility of the frequency map" — the difference is between two
  abscissae and is itself reproducible; the clause is now "a difference between two
  abscissae, not between two runs".
* Checked and unchanged: the three-stage raster (0.002 / 10⁻⁴ / 10⁻⁵), the
  intervals 0.5266–0.5277 and 0.5265–0.5281, the two restarts returning the same
  sample, the statement that the result is a local maximum within a declared window
  and not a global one.

### §4.8 The maximum read as a modal share

* Checked and unchanged, and this is the subsection a referee will read twice:
  small denominator (128×), branch identity (0.999995 overlap, 1.45 decay rates,
  second candidate 2.0$\lvert k_x\rvert$ away, condition 1.6×10², error bound
  4×10⁻¹⁴), reference-plane invariance (2×10⁻¹⁶), and the sentence "the maximum is
  a modal share and not a reflectance" with 94.68 % / 94.90 % / 99.77 %
  distinguished. All MATCH.

### §4.9 Energy budget

* **Arithmetic and provenance** (L12-09): "As rounded, these four numbers close to
  $1.4\times10^{-6}$; … the identity closes to $1.9\times10^{-17}$, and the computed
  power balance to $6.6\times10^{-13}$ … which sums to $0.99769$ … closes to
  $3.0\times10^{-13}$". The four printed numbers close to $8.3\times10^{-6}$ —
  exactly twice the interference term, because the outgoing shares are magnitudes
  and the interference term is signed — the stored identity residual is
  $3.4\times10^{-16}$, the stored power balance $7.3\times10^{-13}$ at the operating
  point and $3.2\times10^{-13}$ at the maximum, and 0.99769 is the sum of the *two
  propagating* terms, not of all four. All five numbers replaced, with the reason
  for the factor two stated.
* Checked and unchanged: the evanescent budget at the plane ($4.8\times10^{-28}$)
  and at the edge ($4.4\times10^{-6}$), the fixed-frequency sweep −2.11 %/+2.1 %/
  −1.15 %/−1.21 % and the 6.3×10⁻⁵ dispersion shift that separates it from the
  branch-consistent comparison.

### §4.10 What creates the backward channel

* Checked and unchanged, all MATCH against `mechanism_controls.json`: the five
  matched controls (including the specular entry marked "sp"), the 1.21 / 9.85 /
  34.2 % reductions, the 11.1 % edge-plane comparison and the 23.1 points of
  propagation loss, the rejected `−9.85 %` sign (2.01 % at the edge plane), the
  monotone sweep 0.9468 / 0.7711 / 0.6230 / 0.8636 / 0.7006, the re-searched argmax
  (0.5218, 0.5248, 0.5275, 0.5261, 0.5309) and the ceilings 0.6244 / 0.7013.

### §4.11 Distance, survival and attenuation

* **Symbol collision** (L12-10): the distance from the edge was written $\ell$, the
  gradient length, in a paragraph that also quotes $\ell=50$ nm elsewhere; the
  frozen panel uses $L$. Round 11 fixed this in the labels and left it in the prose.
* **A contradicted factor** (L12-11): "falls by a factor of three at the extremes of
  the coupling range" stands in the same sentence as "falls from \SI{18.5}{mm} to
  \SI{0.30}{mm}, a factor of sixty-two". The stored attenuation lengths are 18.5,
  0.538 and 0.300 mm; the clause is now replaced by the two values.
* **Caption** (L12-12): "attenuation length $L$" is now "attenuation length", and
  the two loss coefficients are named $\alpha_i$ and $\alpha_B$ as in the panel.
* Checked and unchanged: 0.469/0.454 dB/mm at $H=0$, 16.2/23.0 at −0.05, the 0.47
  and 29 dB/mm extremes, the 0.0356 survival minimum at 1 mm.

### §4.12 Coupling sensitivity in $(k_y,H)$

* Checked and unchanged: $R_B$ 0.01896–0.02560 over the box, the 1.35 factor in
  $k_y$, the ≤2.44 % change in $H$, the 5×19 measured grid with no interpolation.

### §4.13 Through-thickness flux

* Checked and unchanged: the extremes $-0.0367$ and $+0.0317$ in normalised units, the sign
  change inside the plate, the non-vanishing transverse flux at the free surfaces,
  and the caption's honest "not independently validated".

### §4.14 Convergence and cross-checks

* **Order-of-magnitude attribution** (L12-13): "the residual stays at 3×10⁻¹⁵ and
  the energy-balance error between 2×10⁻¹³ and 10⁻¹², six to seven orders below the
  10⁻⁸ tolerance and two to three orders below the 10⁻¹⁰ tolerance" mixes two
  quantities and two tolerances, and the stored balance spans
  $2.4\times10^{-15}$–$4.1\times10^{-12}$. Rewritten per quantity, with the panel's
  two lines named correctly.
* Checked and unchanged: 3×10⁻⁶ → 10⁻⁷ channel error, the 10⁻¹² wavenumber floor,
  the 2×10⁻⁵ route agreement, and the explicit statement that panel (d) is a
  consistency check and not a physical validation.

### §4.15 Wave field and flux directions

* **A vector that is not a direction** (L12-14): $\vect{k}_B\propto(0.333,-0.530)$
  mixes $K_{Bx}/K_{ix}=0.333$ with $\lvert k_y\rvert/K_{Bx}=0.530$ and takes the
  sign of the flux. The solved wavenumber is $(0.24517,\,+0.12981)$, i.e.
  $\vect{k}_B\propto(1,0.529)$, pointing at $+27.9^{\circ}$; $\vect{P}_B$ is
  $(-1,-0.530)$, pointing at $-152^{\circ}$. The prose now states both correctly and
  draws the physical distinction (flux opposite to its own phase direction). **The
  frozen panel (c) still draws the old vector — B1.**
* Checked and unchanged: the 10.0°/27.9° field angles, the intensity normalisation,
  the two negative flux components against $k_y$.

---

## 6. §5 Discussion — `sections/discussion.tex`

**Read in full,** including the literature comparison, the novelty table and the
limitations.

| criterion | finding |
|---|---|
| Mathematics | none |
| Physics | three checks, all sound: the mechanism (wavenumbers approaching at a zero-group-velocity fold) is the one §4.5 measures; the "maximal share, minimal transported power" pair is stated with its 128× number; the coupling acts through loss, with the 62× attenuation change against the ≤1.1×10⁻⁵ dispersion shift |
| Literature | the comparison is made against the equations that could be inspected (Hu et al.'s reproduction of the Qu et al. decomposition), the closed-access primary source is named as not inspectable, the symbol collision between $H_{ijklmn}$ (stiffness) and this paper's $H_{jkl}$ is flagged, and no priority claim is made. Status `UNRESOLVED` in the table and in the text |
| Language | one count error, repaired: "Five limitations" followed six paragraphs (L12-17) |
| Submission-level | the limitations are unusually honest: the corner paragraph separates "the global partition is insensitive" from "the pointwise corner field is unresolved" in exactly the terms a referee would demand |

---

## 7. §6 Conclusions — `sections/conclusions.tex`

**Read in full.** Five numbered results plus a closing limitations sentence.

* Checked: "Five results follow" precedes exactly five items. 2.31 %, 94.68 %,
  16.6547 GHz, 0.4 %, 10⁻⁸ stability between degrees 14 and 34, 99.98 % and 99.77 %,
  the 128× flux drop, the $H=0$ invariance, the $\ell=0$ removal, the 1.21/34.2/
  23.1 % decomposition — all MATCH.
* **The closure number in item 1 was the one number in the manuscript that was
  right where the results section was wrong**: it quotes $3.4\times10^{-16}$, which
  is the stored `closure_residual` at the operating point. §4.9 has been brought
  into agreement with it (L12-09), not the other way round.
* No edit to this file.

---

## 8. Appendix — `sections/appendix_reproducibility.tex`

**Read in full.** Package contents, the automated checks, the reproduction recipe,
the environment, the provenance records and "what is not reproducible here".

| criterion | finding |
|---|---|
| Numbers | three counts were stale: the suite had 47 tests, not 39 (three places), the figure data are eleven CSVs, not twelve, and the suite takes about 25 s, not 9 s (L12-18) |
| Mathematics | none |
| Physics | the appendix is where the plane-invariance and mode-identification tests are described; the description matches the tests |
| Language | the command list and the exit-status paragraph are precise and are worth keeping as they are |
| Submission-level | "no TeX engine was available … the content is validated and the typeset output is not" is exactly the statement a repository-based submission needs — and it remains true after this round (BUILD UNVERIFIED) |

---

## 9. Cross-cutting checks

| check | result |
|---|---|
| every figure cited in order of first appearance | `claim_audit.py`: `[1,2,3,4,5,6,7,8,9,10]` |
| every cross-reference resolves, every citation key exists | `static_check.py`: 104 labels, 75 references, 13 citation keys, 13 bib entries, PASS |
| every registered claim still present with its token | `claim_audit.py`: 23 claims, 46 tokens, 11/11 source-agreement rows, 5 deprecated values still guarded, PASS |
| prose-word count | 16 355 → 16 634 (this round) |
| no promotional phrasing introduced | `grep -niE "novel|first time|significantly|dramatically|remarkabl|paves the way|robust framework|we believe|cutting-edge"` over `main.tex` and `sections/*.tex` returns two hits, both the label and the cross-reference of `tab:novelty` |
| no reference to rounds, audits or scripts in the manuscript prose | the only script names in the manuscript are the readable ones in the appendix (path table and command list), which are part of the reproduction contract |
| the words "reflectance"/"reflectivity" are never applied to 94.68 % | six occurrences remain, all contrastive ("not a reflectance", "closest to a reflectance"); the one loose use is L12-06 |

---

## 10. Findings that are not edits

| id | finding | disposition |
|---|---|---|
| F-1 | fig10(c) draws $\vect{k}_B$ along $(0.333,-0.530)$, i.e. $58^{\circ}$ below the $+x$ axis; the solved wavenumber points $27.9^{\circ}$ above it | **B1**, blocking for the figure round; prose corrected (L12-14) |
| F-2 | fig01(d) cannot show the fold maximum, because its grid steps over $k_xd=0.5275$ | not blocking: the text now says so and points to `tab:configurations` |
| F-3 | `peak_search.py`'s docstring says the tracking-path sensitivity "dominates the reproducibility of the printed digits"; the stored spread is 0.0 | **B6**, documentation only, code frozen |
| F-4 | the manuscript nowhere states the frequency-to-share amplification, which the review measured at $\sim10^{3}$ | deliberate: a number whose only record would be a review-time run does not belong in a paper whose datasets are shipped |
| F-5 | the abstract does not repeat the "local maximum" qualifier | deliberate, see §1 |
| F-6 | six contrastive uses of "reflectance" remain | deliberate: they are the disclaimer |
| F-7 | the novelty status against Qu et al. (2025) is `UNRESOLVED` | **B2**; not an editorial matter |
| F-8 | the corner line force is unresolved pointwise | **B3**; stated in the paper as a limitation, correctly |

---

## 11. Outcome of the section review

The manuscript's scientific content survived the review unchanged: no equation, no
constant, no boundary condition, no dataset, no figure PDF, no reported value. What
changed is the accuracy of the prose around that content — nineteen items, ten of
them disagreements with the paper's own data, two of them claims with no data
behind them.

Readiness is reported separately and is not implied by finishing this review:
`PAPER_A_ROUND12_READINESS_ASSESSMENT.md`.
