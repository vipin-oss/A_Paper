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
single-edge and corner caveats, and `BUILD UNVERIFIED` for the typeset PDF.

---

# Round 12 (2026-11-07) — section-by-section review of the manuscript

A final editorial and scientific pass over `main.tex` and its seven section files, with every number
traced to a stored record. Content frozen: no equation, constant, boundary condition, solver, dataset,
figure PDF or reported number changed (`PAPER_A_ROUND12_SECTION_BY_SECTION_REVIEW.md`).

First, two round-11 reporting defects were corrected, because later text would otherwise have been
reviewed against numbers that do not exist (`PAPER_A_ROUND12_PRELIMINARY_EVIDENCE_CORRECTIONS.md`):

| # | Item | Before (round 11) | After | Reason |
|---|---|---|---|---|
| P12-A1 | headline stability | "1.5×10⁻⁷ … below the 10⁻⁸ bound", pooled with a 1.86 % comparison at two different wavenumbers | 7.54×10⁻¹⁰ at fixed $k_xd=0.52752$ and 1.00×10⁻¹⁰ at fixed $0.5275$; the 1.46×10⁻⁷ is named for what it is (argmax vs reported sample, `offset_reported_vs_argmax` 1.37×10⁻⁷) | the pooled number measured sampling between two abscissae, not the reproducibility of a run |
| P12-A2 | "tracking-path sensitivity" | 8.4×10⁻⁶ / 9.0×10⁻⁶ ascribed to the branch-tracking path | tracking-path spread **0.0**; 8.36×10⁻⁶ is the coarse-raster sampling error (`restart_spread`, rel 8.69×10⁻⁶) | the three tracking paths return identical values; the reported number was the restart spread |

Then nineteen prose corrections (full before/after table in `PAPER_A_ROUND12_EDIT_LEDGER.md`):

| # | Item | Before | After | Reason |
|---|---|---|---|---|
| P12-1 | §4.1 phase-speed endpoints | 105.8 km/s at $k_xd=1.05$, 20.0 "near the cutoff" | transposed back to their abscissae (105.8 at 0.15, 20.0 at 1.05) | the data have the opposite assignment |
| P12-2 | §4.1 linewidth ordering | "a clear ordering in $H$" | smallest at $H=0$, rising with $\lvert H\rvert$, larger for $+H$ | the note goes $0<-0.025<+0.025<-0.05<+0.05$ |
| P12-3 | §4.1 attenuation maximum | "peaks sharply at $k_xd\approx0.52$" | the sampled maximum (0.54, 3.2 dB/mm) distinguished from the fold value (87.2 dB/mm) | the plotted grid steps over the fold |
| P12-4 | §4.3 density factor | nine times (twice) and ten times | a factor of three | $\Delta$k and $\Delta\alpha$ are exactly linear in $n_0$ (0.00084 → 0.00251 MHz) |
| P12-5 | §4.3 mobility factor | five times | a factor of three | the mobility column is identical to the density column; both sweeps are one sweep |
| P12-6 | §4.3 backward share | "reflectance" | "backward share" | the one loose use of the word in the article |
| P12-7 | §4.3 panel (c) tail | "falls to $10^{-7}$ at $k_xd=0.9$" | $<10^{-7}$ beyond 0.8; $1.6\times10^{-11}$ at 0.9 | four orders off at the quoted sample |
| P12-8 | §4.4 thickness wording | "the branch moves from 30.4 to 10.5 GHz" | those are the ends of the 120/180/220/320 nm family | one branch cannot be both |
| P12-9 | §4.4 gradient-length abscissae | 0.15 and 1.05 | 0.145 and 1.000 | neither 0.15 nor 1.05 is on the solved grid |
| P12-10 | §4.6 reproducibility | $1.8\times10^{-12}\to5.6\times10^{-6}$, "$\pm6\times10^{-6}$" | the registered spreads (degree 6.2×10⁻⁹, quadrature 4.3×10⁻¹⁰, tracking 0, sampling 8.4×10⁻⁶) | neither number exists in any record; a direct evaluation gives ~1.5×10⁻⁹ |
| P12-11 | §4.7 offset justification | "below the reproducibility of the frequency map" | "a difference between two abscissae, not between two runs" | two runs return the same sample |
| P12-12 | §4.9 energy budget | "close to 1.4×10⁻⁶", identity 1.9×10⁻¹⁷, balance 6.6×10⁻¹³, 0.99769 "sums all four" | four numbers close to 8.3×10⁻⁶ (twice the interference term), identity 3.4×10⁻¹⁶, balances 7.3×10⁻¹³ and 3.2×10⁻¹³, 0.9969 + 0.0008 | five arithmetic/provenance errors in one paragraph |
| P12-13 | §4.11 distance symbol | $\ell$ | $L$ | $\ell$ is the gradient length, and the panel uses $L$ |
| P12-14 | §4.11 attenuation change | "falls by a factor of three" | 18.5 → 0.54 → 0.30 mm (a factor of 62 to the fold) | self-contradictory in the same sentence |
| P12-15 | fig06 caption | "attenuation length $L$" | "attenuation length"; $\alpha_i$, $\alpha_B$ named | $L$ is the distance from the edge; the panel has three coefficients |
| P12-16 | §4.14 residual attribution | 3×10⁻¹⁵ and 2×10⁻¹³–10⁻¹² "six to seven orders below 10⁻⁸ and two to three below 10⁻¹⁰" | residual 2.7–3.3×10⁻¹⁵ (five orders below 10⁻¹⁰); balance 2.4×10⁻¹⁵–4.1×10⁻¹² (one to five orders below the 10⁻¹⁰ line) | two quantities, two tolerances, one sentence |
| P12-17 | §4.15 backward wavenumber | $(0.333,\,-0.530)$ | $(1,\,0.529)$; $\vect{P}_B\propto(-1,-0.529)$ | mixes $K_{Bx}/K_{ix}$ with $k_y/K_{Bx}$ and takes the flux sign; the solved vector points $+27.9^{\circ}$ |
| P12-18 | §3.1 polynomial | "three-term polynomial" | "polynomial of degree four" | the displayed sum spans $k^0\ldots k^4$ and the section itself says quartic |
| P12-19 | §2.7 / `tab:groups` | $\alpha$ | $\alpha_{\mathrm{d}}$, plus a clause that the dissipation integral is in scaled units | $\alpha$ also denotes the attenuation $2\lvert\Imag k_x\rvert$ from §3 onward |
| P12-20 | §5.5 limitations | "Five limitations" | "Six limitations" | six paragraphs follow |
| P12-21 | appendix | 39 tests, ~9 s, twelve data files | 47 tests, ~25 s, eleven files | all three counts had moved in round 11 |
| P12-22 | abstract | "The figure is a modal share"; "unchanged"; "the backward mode" | "The reported number"; "almost unchanged"; "the two partner modes" | no antecedent for "the figure"; 1.21 % is not "unchanged"; which flux changes matters |

**Verification after the corrections:** 47 tests OK; claim registry 23/46, 5 deprecated guarded,
10 figures in citation order, 11/11 source rows; 15 mutants caught; phase-speed audit PASS; static
check PASS (104 labels, 75 references, 13/13 citations, 16 634 words); LaTeX build not executed
(**BUILD UNVERIFIED**); full battery not re-executed because no producer, dataset or solver file
changed (`PAPER_A_ROUND12_CORRECTION_HISTORY.md` Phase D).

**Not superseded:** the research model, every headline number, the tables, the 13 citations, the
round-10 language and structure, the round-11 figure fixes, the `UNRESOLVED` novelty status, the
synthetic $\ell$, $f$, $H$, the single-edge and corner caveats, and `BUILD UNVERIFIED`.
**Still open:** B1 (fig10(c) arrow), B2 (prior art), B3 (corner field), B4 (build), B5 (author
declarations), B6 (`peak_search.py` docstring) — `PAPER_A_ROUND12_BLOCKING_ISSUES.md`.

---

# Round 13 (2026-11-07) — targeted closure: fig10(c), docstrings, packaging

A closure round, not a rewrite: close the two blockers round 12 left open, fix one
report-level misattribution and one caption, repair the two counts the round's own
new tests made stale. No equation, constant, boundary condition, solver, dataset,
table or reported number changed.

| # | Item | Before | After | Evidence |
|---|---|---|---|---|
| P13-1 | fig10(c) backward wavenumber arrow | `arrow((0.333, -0.530), … ${\bf k}_B$ …)`: one ratio from $K_{Bx}/K_{ix}$, one from $\lvert k_y\rvert/K_{Bx}$, the sign of the flux; drawn $57.9^{\circ}$ **below** $+x$, length ratio 0.829 | derived from the stored solve, $\vect{k}_B\propto(1,0.5295)$ at $+27.90^{\circ}$, length ratio 0.371 (= $\lvert\vect{k}_B\rvert/\lvert\vect{k}_i\rvert$), guarded at render time | edge solve at the figure's own configuration: $k_{Bx}=0.2451746921716515$, $k_y=0.1298117503$, `reflected_angle_deg` $=-27.8997$ |
| P13-2 | the other three fig10(c) arrows | literals $(1,0.176)$, $(1,P_{iy})$, $(-1,-0.530)$ | all four derived from `fig10_field_metrics.json` → `primary_wavenumbers` / `primary_flux` | three of the four agree with their literals to the precision drawn; only $\vect{k}_B$ moved |
| P13-3 | `fig10_field_metrics.json` | no wavenumber record | `primary_wavenumbers` block, 11 lines, written by the producer | regenerated `fig10_field_maps.csv` byte-identical, so the re-run was metadata-only |
| P13-4 | regression guard | the defect was invisible to 47 tests | `TestFigure10BackwardWavenumber`, 5 tests; a reversed arrow fails 3 of them; `fig10()` calls the guard | mutant copy in `/tmp/m16`: `FAILED (failures=2, errors=1)` |
| P13-5 | `peak_search.py` docstring | "the tracking-path sensitivity … dominates the reproducibility of the printed digits" | four diagnostics named separately; tracking spread 0.0, sampling error 8.4e-6 | `peak_search.json` → `verdict` |
| P13-6 | round-12 correction history and download README | "62.2973 % at $k_xd=0.55$" | "62.2973 % at $k_xd=0.5275$ with $H/H^{*}=+0.05$", with a dated note | `mechanism_controls.json`: `refined_peak.full.R_B` 0.6229733; `k055_sample.full.R_B` 0.5221071 |
| P13-7 | fig10 caption | "(c) schematic whose arrows are the solved flux directions" | "… the solved wavenumber and flux directions" | the panel draws both pairs |
| P13-8 | test count | 47 in the appendix (three places) and the package README | 52, ~25 s | the round's five new tests |
| P13-9 | round-12 status documents | "B1 open", "B6 open" | body unchanged, dated round-13 status note added at the top | the two defects are closed here |

**Verification after the corrections:** 52 tests OK; new class 5/5; reversal mutant
caught; claim registry 23/46, 5 deprecated guarded, 10 figures in order, 11/11 source
rows; 15 mutants caught; phase-speed audit PASS; static check PASS (104 labels, 75
references, 13/13 citations, 16 656 words); fig10 field map byte-identical; LaTeX
build not possible (**BUILD UNVERIFIED**); full battery not re-run because no producer
logic changed.

**Not superseded:** the research model, every headline number, the tables, the 13
citations, the round-10 language, the round-11 figure and registry work, the round-12
prose corrections, the `UNRESOLVED` novelty status, the synthetic $\ell$, $f$, $H$,
the single-edge and corner caveats, and `BUILD UNVERIFIED`.
**Still open after this round:** B2 (prior art), B3 (corner field), B4 (build),
B5 (author declarations). **Closed in this round:** B1, B6.

