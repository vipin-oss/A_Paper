# Paper A — correction history, round 7

Every correction below was made only after the defect was confirmed in Stage 1
(`PAPER_A_STAGE1_COMPLETE_Q1_AUDIT.md`). Nothing in the governing equations,
the material constants, the discretisation or the solver physics was changed.

Baseline: `405ed2acbf453a1f9df08cf88001d725077762e8` (round 6).

---

## A. Scientific corrections

### C-1 — Branch maximum of the backward channel (CRITICAL)

| | |
|---|---|
| File | `sections/results.tex` (§backward conversion, §refinement, tables 1 and 2), `main.tex` (abstract), `sections/discussion.tex`, `sections/conclusions.tex`, `figure_data/fig04_frequency_reflection.csv`, `figures/fig04_frequency.pdf` |
| Old | "the maximum along the branch is 57.92 % at k_xd = 0.55, where the group velocity passes through zero"; the sweep sampled k_xd on a 0.05 grid |
| New | maximum **93.19 % (R_B = 0.931891)** at **k_xd = 0.5250, f = 16.6547 GHz, v_g = −3 m/s**; 57.92 % retained as the certified value at k_xd = 0.550 |
| Reason | A 0.05 grid samples the region where the branch turns over at three points; the paper's own `tab:refinement` already printed 0.9319 at 0.5250, contradicting the headline |
| Source of the new value | `build_figure_data.fig04` on a refined grid (110 rows, 22 k_x × 5 coupling levels) and `convergence_audit.py` at degrees 14–30 |
| Recomputation | yes — 110 edge solves plus 10 convergence solves |
| Verification | degree stability 2.1e-8 (18→30), quadrature stability 6.9e-9, condition ≤1.9e2, residual ≤3e-15, power balance 1e-14 |
| Figures affected | `fig04_frequency.pdf` regenerated from the refined data (y-range raised from 66 % to 100 % so the new maximum is not clipped) |

### C-2 — Size and mechanism of the coupling effect (CRITICAL)

| | |
|---|---|
| File | `sections/results.tex` (§what creates the backward channel, table of controls), `sections/discussion.tex` (§mechanism, §literature), `main.tex`, `sections/conclusions.tex` |
| Old | "the modification is small … −1.21 % at the operating point and −9.85 % at the peak"; "the added coupling is a bounded perturbation" |
| New | −1.21 % at the operating point, −9.85 % at k_xd = 0.55, **−33.1 % at the branch maximum**; of the latter, −21.6 % survives when referred to the edge plane, so 11.5 points are propagation loss; the coupling acts through the added attenuation of the backward mode (decay rate 4.7e-4 → 8.4e-3 per unit thickness) |
| Reason | The controls had never been run at the true maximum; at the operating point the statement is correct, at the maximum it is not |
| Source | `mechanism_controls.py` with the added `branch_maximum` case and the branch-consistent sweep |
| Recomputation | yes — 5 configurations × 3 points plus 15 sweep solves |
| Verification | the ordering "dispersion unaffected / partition configuration-dependent / loss strongly affected" is now stated per configuration |

### C-3 — Total outgoing power in the abstract (MAJOR)

| | |
|---|---|
| Old | "0.99985 of the incident power" |
| New | "0.99980 at the operating point and 0.99000 at the branch maximum" |
| Reason | 0.99985 contradicts both the stored value (0.999797) and `tab:configurations` |
| Verification | registry claim `total_outgoing_operating_point`, tolerance 1e-4, `claim_audit` PASS |

### C-4 — Zero-group-velocity location (MINOR)

| | |
|---|---|
| Old | "v_g and v_E change sign at k_xd ≈ 0.55" |
| New | "just below k_xd = 0.53" (v_g = −10.0 m/s at 0.52, +4.1 m/s at 0.53) |
| Verification | `fig04` CSV, `convergence_audit.json` |

### C-5 — Flexoelectric contribution at the branch maximum (MINOR)

| | |
|---|---|
| Old | "changes it by −0.011 % at both points" |
| New | "−0.011 % at the operating point and less than 1e-4 % at the branch maximum" |
| Verification | `mechanism_controls.json`, full vs no-flexo rows |

### C-6 — Rounded energy partition (MINOR)

| | |
|---|---|
| Old | "the sum reproduces the flux at the plane to 3.4e-16" beside four-digit values |
| New | rounded closure 1.4e-6 stated explicitly, exact closure 3.4e-16, other propagating modes printed as 0.976651 |
| Verification | arithmetic recomputation from `peak_certification.json` |

## B. Editorial corrections

| # | File | Old | New | Reason |
|---|---|---|---|---|
| E-1 | `main.tex` | 18-word title with a subtitle | "Backward-branch negative reflection of guided waves at a free edge in a flexoelectric piezoelectric–semiconductor plate" (15 words) | 10–16-word preference; keeps system, phenomenon and mechanism |
| E-2 | `main.tex` | three-paragraph, ≈600-word abstract with round-off residuals and defensive phrasing | one paragraph, 220 words, four registered numbers, limitations in one clause | journal norm 180–220 words |
| E-3 | `main.tex` | 8 keywords | 6 | indexing norm |
| E-4 | `sections/conclusions.tex` | 8 paragraphs, ≈700 words, narrating what was "reversed and corrected" | 5 numbered results, ≈250 words, no history | style; no development history in the article |
| E-5 | 11 figure captions + 1 table caption | "Data: `fig01_….csv`", script names inside captions | removed; the appendix table already lists every file | typeset article text must not carry internal paths |
| E-6 | `results.tex`, `numerical_methods.tex`, `governing_equations.tex`, `conclusions.tex` | "the earlier version of this paper", "were previously described", "the honest reading", "genuinely independent", "which is exactly what happened" | rewritten to state the physics | §20 of the directive |
| E-7 | `main.tex` | no declarations | Data availability (true statement), competing interests, funding, CRediT, acknowledgements, ethics, generative-tool disclosure — author-controlled items marked **AUTHOR INPUT REQUIRED** | required back matter; nothing invented |
| E-8 | `governing_equations.tex`, `discussion.tex` | "Fourier-reduced three-dimensional formulation" | "two-and-a-half-dimensional (2.5D) Fourier-reduced formulation", with what is and is not discretised | prevents the model being read as a full 3D simulation |
| E-9 | `numerical_methods.tex`, `governing_equations.tex` | script and JSON paths in the running text | removed; content kept | reproducibility lives in the appendix |
| E-10 | `sections/introduction.tex` | gap statement "what has not been examined … is the scattering problem at an edge" | narrowed: plane-wave reflection coefficients already exist (Mondal et al. 2022); what is missing is the modal partition of a *guided* plate branch with carriers | the original wording overclaimed |
| E-11 | `appendix_reproducibility.tex` | "20 tests", 25-page-era file table | "22 tests", four new scripts and two new data files listed | consistency with the suite |

## C. Bibliographic corrections

| # | Entry | Action | Evidence |
|---|---|---|---|
| B-1 | `biswas2025rayleigh` | added — Biswas & Sahu, *Math. Mech. Solids* **30**(12) 2822–2842 (2025) | DOI 10.1177/10812865251315937 verified via OpenAlex |
| B-2 | `mondal2022scattering` | added — Mondal, Sahu & Nirwal, *Math. Methods Appl. Sci.* **45**(12) 7700–7714 (2022) | DOI 10.1002/mma.8272 verified via OpenAlex |
| B-3 | `shen2010theory`, `yang2020rayleigh`, `qu2022thermal`, `qu2022bending` | DOI added after title-match search | 10.1016/j.jmps.2010.03.001, 10.1016/j.ultras.2020.106105, 10.1016/j.mechmat.2022.104328, 10.1007/s10338-021-00296-y |
| B-4 | all other entries | title/journal/year/volume/pages re-checked | OpenAlex work records |

No citation was added to raise a count, and none was removed.

## D. Code and gate corrections

| # | File | Change | Reason |
|---|---|---|---|
| G-1 | `model.py` | optional `nquad` override (default unchanged) | quadrature sufficiency could not be tested at all before |
| G-2 | `build_figure_data.py` | refined k_x grid for Fig. 4 (0.01 over 0.46–0.60, 0.05 elsewhere) | C-1 |
| G-3 | `mechanism_controls.py` | `branch_maximum` case added | C-2 |
| G-4 | `generate_final_figures.py` | panel (c) of Fig. 4 re-ranged 0–100 % | otherwise the new maximum was clipped |
| G-5 | `test_model.py` | two regression tests added (frozen derived constants; literature bands on material constants) | a unit error previously passed the whole suite |
| G-6 | `convergence_audit.py`, `quadrature_audit.py` | new | turns two claims into executable evidence |
| G-7 | `claim_audit.py`, `claims.json` | new | manuscript ↔ registry consistency and stale-value guard |
| G-8 | `mutation_tests.py` | new | proves that the gates fire |
| G-9 | `run_all_checks.py` | four checks added; fig04 row count 50 → 110 | one entry point |

## E. Not corrected, deliberately

* **Governing equations, signs, tensor contractions, Schur bound** — re-derived
  and found correct.
* **Material constants** — unchanged; only pinned.
* **Corner argument** — already correct and already refuses to claim what the
  diagnostic cannot show.
* **Novelty statement** — cannot be closed; left explicitly unresolved rather
  than sharpened into a claim the evidence does not support.
* **ℓ, f, H values** — synthetic and labelled as such; no calibration invented.

---

# Round 8 addendum — supersedes the headline of C-1

Round 8 re-executed every quoted number instead of trusting the round-7 verdicts, and found that C-1
itself was a coarse-grid artefact: 0.9319 at k_xd = 0.5250 was the largest sample of a 0.01 raster, not a
maximum. The corrections below therefore **supersede C-1 and the peak column of C-2**. The full account is
in `PAPER_A_ROUND8_STAGE1_AUDIT.md` and `PAPER_A_ROUND8_MANUSCRIPT_CHANGES.md`.

| # | Item | Round 7 | Round 8 | Reason |
|---|---|---|---|---|
| R8-1 | location and value of the maximum | 0.931891 at k_xd = 0.5250 | **0.9467952 at k_xd = 0.5275** (argmax 0.52752, 0.9467954) | the 0.01 raster does not resolve the top; three-stage search 2e-3 → 1e-4 → 1e-5 with a flatness test and a stored classification |
| R8-2 | status of the maximum | "the maximum" | **certified local maximum** in the declared window, flat to 0.01 pp on [0.5266, 0.5277], never global | a sampled value must not be called a maximum |
| R8-3 | reference-plane rescaling in the artefact audit | backward attenuation only → 2 % plane dependence, rationalised in a note | net exponent 2(|Im k_ix| + |Im k_Bx|) → 2.4e-16 | both partner modes attenuate, in opposite directions |
| R8-4 | incident modal power in the audit | 1.0 (renormalised before the field was filled) | 3.967e-5 at the peak vs 5.075e-3 at the operating point, i.e. a factor **128** | the ratio is a ratio of two small fluxes; now stated in the abstract |
| R8-5 | coupling effect at the peak | −33.1 % (reference plane; edge comparison quoted as 21.6 %/11.5 points) | **−34.2 % reference plane, −11.1 % edge plane, 23.1 points of propagation loss**; re-searched, the ceiling falls to 0.6244 / 0.7013 | the old pair mixed a reference-plane figure with an edge-plane figure |
| R8-6 | corner-assessment guard | 1e-6 relative on the incident root | 2e-2 relative, documented as a *labelling* guard | 1e-6 silently excluded the certified peak (offset 7.4e-4) |
| R8-7 | `certify_peak.py` | case named `peak_candidate`, described as the peak | four fixed wavenumbers; docstring states it certifies and **never searches** | a refinement study at the wrong abscissa certifies nothing |
| R8-8 | Fig. 4 | 2 panels, 110 coarse rows, caption asserted a maximum | 2 × 2 panels, 139 rows with a fine raster, inset over the top, no row count in the text | the figure could not support its caption |
| R8-9 | gates | 22 tests, 5 mutants, fig04 = 110 rows, no search/identity step in the battery | **26 tests, 8 mutants, 139 rows, three new battery steps, source-agreement gate** | the suite could not detect a nearby higher admissible value |

**Not superseded:** the governing equations, the constitutive law, the 2.5D formulation, the material
constants, the operating-point value (0.0231456) and the k_xd = 0.55 value (0.5791801) were all re-executed
and confirmed to 4e-11 and 5e-8 respectively.

# Round 9 addendum — the plane transform of a modal-power *ratio*

Round 9 audited one quantity and nothing else: how the backward modal-power fraction `R_B = P_B/P_i` is
moved between planes parallel to the edge. The audit is in
`PAPER_A_ROUND9_STAGE1_NORMALIZATION_AUDIT.md` (written before any edit), the corrections in
`PAPER_A_ROUND9_CORRECTION_HISTORY.md`, and their verification in
`PAPER_A_ROUND9_PLANE_INVARIANCE_VALIDATION.md`, `PAPER_A_ROUND9_MUTATION_REPORT.md`,
`PAPER_A_ROUND9_CLAIMS_AND_MANUSCRIPT_AUDIT.md` and `PAPER_A_ROUND9_TEST_RESULTS.md`.

| # | Item | Round 8 | Round 9 | Reason |
|---|---|---|---|---|
| R9-1 | `peak_search.py` edge-plane share | `R_B·exp(2|Im K_B|·10)` — the backward decay alone: **0.965978** | shared transform: **0.985572** | a ratio of two modal powers needs both attenuations; the difference is 1.96 pp |
| R9-2 | fig02 / fig05 / fig07 `R_B_edge` columns | single-mode absolute decay | `edge_plane_fraction(R2, ki, kb, p.d)` | same defect, 130 / 5 / 95 rows; the density-sweep edge maximum moves 0.579855 → 0.580359 |
| R9-3 | `edge_plane_fraction` API | one argument `L` with two meanings (`L=0` returns the input, `L=REF_NORM` returns the edge value) | explicit `L_to`/`L_from`, exponent `2(Im K_i − Im K_B)(L_from − L_to)`, identities documented | the signature invited the mistake it then produced |
| R9-4 | cross-script check | none — two scripts disagreed about the same number and no gate noticed | `claim_audit.py` compares the search record with the matched controls to 1e-6, plus per-case edge rows | the defect survived round 8 for want of this gate |
| R9-5 | claim registry | no claim for any edge-plane share | `R_B_edge_certified_maximum`, `R_B_edge_operating_point`, `R_B_edge_k055` | an unregistered number is an unchecked number |
| R9-6 | tests and mutants | 26 tests, 8 mutants | **39 tests, 13 mutants**; three new classes cover the transform, plane invariance and cross-script agreement | the suite could not have caught R9-1 |
| R9-7 | printed spreads of the maximum | 5.6e-9 over degrees, 9.4e-10 over quadrature | **5.0e-9 / 7.3e-9 over degrees, 5.6e-9 over quadrature**; Table 5 edge row 0.0231 → 0.0232 | re-read from the regenerated records, not tuned; the conclusion (converged to < 1e-8) is unchanged |
| R9-8 | packaging | `MANIFEST.json` hashed before the static validator rewrote `static_validation.txt` | validator runs first | the archive failed its own manifest check on exactly that entry |

**Not superseded by round 9, deliberately:** the reference-plane headline `R_B = 0.9467952` at
`k_x d = 0.5275` (never produced by the defective transform), the `certified_local_maximum`
classification, the reference-plane definition of `R_B` (the transform was corrected towards the edge,
not the definition), `isolated_transfer` and the fig06 absolute quantities, the `R_B_100um` legacy column,
and the legacy runners whose exponent was already algebraically correct. The 94.68 % figure was not
adjusted to compensate for any of this.

# Round 10 addendum — presentation only, no scientific correction

Round 10 changed no result and corrected no defect. It changed the way the article is written: the
structure, the register and the figure captions. The audit that precedes it is
`PAPER_A_ROUND10_STYLE_AND_STRUCTURE_AUDIT.md`; the edit log is
`PAPER_A_ROUND10_LANGUAGE_AND_STRUCTURE_CHANGES.md`; the closing check is
`PAPER_A_ROUND10_FINAL_MANUSCRIPT_STYLE_AUDIT.md`. The entry is recorded here so that the history of the
manuscript is complete, and so that no later reader mistakes the rewording for a revision of the
physics.

| # | Item | `aabcb77` | Round 10 | Reason |
|---|---|---|---|---|
| P10-1 | title | "…at a free edge in a flexoelectric piezoelectric--semiconductor plate" | "…from the free edge of a flexoelectric piezoelectric semiconductor plate" | naming the process, not the chain of modifiers |
| P10-2 | abstract | 236 words, one third of them certification bookkeeping | 222 words: system, solution, two findings, coupling, caveats | the author's abstracts are findings, not delivery statements |
| P10-3 | register | *certified* 39, *audit* 19, *admissib\** 20, *solver* 21, *script* 18, *CSV* 12 | appendix only, except two label names and one data-availability sentence | an article is not a verification report |
| P10-4 | §3 / appendix | software tests, regression guards and reproducibility prose inside the method section | method in §3, the same prose in the appendix | separates the mathematics from the package |
| P10-5 | §2 | no limits subsection | §2.10 collects the four limits and the two reductions used in the text | the author's papers flag limiting cases; the material already existed |
| P10-6 | §4 titles | "Refinement study", "Certification of the maximum", "Why the high fraction is not an artefact" | "Convergence of the reported values", "Location of the maximum", "The maximum read as a modal share" | titles describe the physics, not the procedure |
| P10-7 | §5.5 | limitations in two long paragraphs plus an embedded rebuttal | five headed paragraphs in one subsection, the corner evidence separated from its limit | grouped, as the brief requires |
| P10-8 | `fig02` caption | "at $\ell=\SI{2}{\micro\metre}$" — a distance labelled with the gradient length | "at the reference plane $L=\SI{2}{\micro\metre}$" | a symbol error in a caption; no datum involved |
| P10-9 | `fig07` caption | "95/95 rows admissible" | removed; the grid is described in the text | row counts belong with the data |
| P10-10 | §6 | two of five items were precision statements | five physical findings, precision folded into the finding that it qualifies | conclusions state findings |

**Not superseded, not re-derived, not re-worded numerically:** every value of `claims.json` (45 tokens,
still PASS), the tables, the ten figures, the 13 citations, the operating-point and maximum values, the
`UNRESOLVED` novelty status, the synthetic parameters, the single-edge and corner caveats, and the
`BUILD UNVERIFIED` status of the typeset output.

---

# Round 11 (2026-11-07) — programming audit, numerical reproducibility, figure verification

Round 10 was a writing round; round 11 went back to the code and the figures. Twenty-eight
items were audited (D1–D28 in `PAPER_A_ROUND11_STAGE1_PROGRAMMING_AND_FIGURE_AUDIT.md`), the
confirmed ones were repaired, and the full battery was then run on a **cleanly regenerated
data directory** with nothing restored: **18 PASS / 0 FAIL / 1 SKIP** (`OVERALL: PASS`), the skip
being the LaTeX build, for which this environment has no engine.

| # | Item | Before | After | Reason |
|---|---|---|---|---|
| P11-1 | §4.1 coupling shift | "at most ±60 kHz … less than 4×10⁻⁶" | 184 kHz (1.1×10⁻⁵) at $k_xd=1.05$, 92 kHz for the negative coupling | the stored data of the cited panel give 183.7 kHz; the old figure was three times too small |
| P11-2 | §4.1 $v_g$ vs $v_E$ | "better than 3.5 % over the whole branch (2 % in the interior)" | "within 3.5 % except the lowest sample, where they differ by 6.4 %" | the interior bound was not supported either (3.40 % at $k_xd=0.54$) |
| P11-3 | §4.3 gradient-length percentages | +1.9 % at $k_xd=0.1$, −1.8 % | +2.0 % at $k_xd=0.15$, −1.9 % | the solved grid starts at 0.15 |
| P11-4 | refinement spreads | quoted as values (5.0×10⁻⁹, 5.6×10⁻⁹), tested by 1 % equality | quoted as bounds (<10⁻⁸), registered as bounds, tested as inequalities | they are differences of near-equal numbers on the round-off floor; the round-10 battery failed on their noise while the headline moved by 10⁻¹³ |
| P11-5 | quadrature spread | pooled degrees 22 and 30 | degree 22 only, four rules | a metric named for the quadrature rule must not contain degree error |
| P11-6 | fig02(c) axis | "backward reflectance" | "$R_B$ at $L=2\,\mu$m", note "backward modal share" | $R_B$ is a share; round 10 had fixed the same error in the *caption* only |
| P11-7 | fig04(a),(c) axis | "$R_B$ at $\ell=2\,\mu$m" | "$R_B$ at $L=2\,\mu$m" | $\ell$ is the gradient length |
| P11-8 | fig06 axes | $\ell$ for distance from the edge; $L$ for the attenuation length | $L$ for the distance; "attenuation length (mm)" | two symbols, two meanings, three labels |
| P11-9 | figure panel map | hand-maintained, wrong for most figures | generated from the plotting code on every render, with a test | provenance that drifts is worse than none |
| P11-10 | fig10(c) | a schematic with no label | in-panel "schematic" | a drawing inside a results figure must say so |
| P11-11 | fig05(c), fig09(c) | residuals at 10⁻¹²–10⁻¹⁵ plotted as if resolved | floor band/labels printed in the panel | a 16-fold change in a number of size 10⁻¹⁵ is not physics |
| P11-12 | fig01(a) inset | ±150 kHz, clipping the −183.7 kHz point | −200…215 kHz | the reader could not see the largest shift the text discusses |
| P11-13 | fig08(c) xlabel | cut by the canvas edge | bottom margin raised; pixel test added | invisible in a PDF viewer, visible in the render |
| P11-14 | test suite | 39 tests, none about figures | 47 tests, eight of them figure provenance | the seven figure defects were invisible to 39 passing tests |
| P11-15 | mutant suite | 13 mutants | 15 (bound semantics, figure label) | a bound that cannot fail is decoration |
| P11-16 | battery order | unit tests first, reading records not yet built | tests after the producers | on a clean directory the old order failed with five missing-record errors |
| P11-17 | legacy generator | `regenerate_revised_data.py` silently rewrote the datasets with a 14-column schema | refuses to run without an explicit opt-in | it caused two corrupted data states during this round's own work |

**Not superseded:** the research model, every headline number (2.31456 %, 94.6795 %, 0.5275 /
0.52752, 16.6547 GHz, 62.2973 %, 98.5572 %), the tables, the 13 citations, the round-10
language and structure, the `UNRESOLVED` novelty status, the synthetic $\ell$, $f$, $H$, the
single-edge and corner caveats, and `BUILD UNVERIFIED` for the typeset PDF. Round 12 has not
begun; this round stops here for supervisor review.
