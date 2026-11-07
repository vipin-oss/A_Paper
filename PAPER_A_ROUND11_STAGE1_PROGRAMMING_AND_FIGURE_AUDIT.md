# Paper A — Round 11, Stage 1: programming and figure audit (written before any edit)

**Branch:** `arena/ea7ca4dd-a-paper` · **HEAD verified before starting:** `1ff9166a5bdf27d5d3ed0adeb21472719654bfeb`
(remote `arena/ea7ca4dd-a-paper` identical; working tree clean; `main` untouched).
**Baseline archive:** `downloads/Paper_A_Complete_Project_round10.zip`.
**Round 10 writing is accepted as the foundation** and is not revisited here.

What was inspected: `paper_a_study/` (every active script below), `figure_data/` (all CSV/JSON),
`figures_final/*.pdf` with their committed PNG renders at publication size, the ten captions in
`sections/results.tex`, the registry `claims.json`, `claim_audit.py`, `run_all_checks.py`,
`mutation_tests.py`, `test_model.py`, and the round-9/round-10 reports.

Every row below is evidence-backed. **No edit was made before this file was written.**

---

## 1. Evidence base for the figure audit

The ten figures were inspected twice: as committed vector PDFs
(`paper_a_study/figures_final/*.pdf`, the files copied into `Paper_A_Final_Submission/figures/`) and
as their committed raster renders (`*.png`, same directory) at full publication size. The renders are
the ones reproduced below in the discussion; a visual finding is only recorded when it is legible in
the render, not merely suspected from code.

Panel-to-column mapping was established from the plotting code (`generate_final_figures.py`, function
per figure) and cross-checked against `figure_data/figure_panel_sources.json`.

---

## 2. Audit table

| ID | Exact location | Verified defect | Evidence | Severity | Scientific impact | Corrective action | Recalculation required? |
|---|---|---|---|---|---|---|---|
| **D1** | `generate_final_figures.py:274` (`fig02`, panel c ylabel) | The axis calls `R_B` a **reflectance**. The whole manuscript insists it is a *modal share*, not a reflectance (abstract, §3.3, §4.7, §5.1). The label also omits the reference plane. | CONFIRMED DEFECT — render of `fig02_material.png`: ylabel reads "backward reflectance $R_B$ (%)"; manuscript §4.7: "The maximum is a modal share and not a reflectance" | high (contradicts the paper's central caveat) | terminology only; no datum | relabel "$R_B$ at $L=2\,\mu$m (%): backward modal share" | no |
| **D2** | `generate_final_figures.py:398, 437` (`fig04`, panels a and c ylabel) | The reference-plane distance 2 µm is written **$\ell$**, the symbol of the strain-gradient length used everywhere else (§2.2, `tab:groups`, §4.2). | CONFIRMED DEFECT — render `fig04_frequency.png`: "$R_B$ at $\ell=2\,\mu$m (%)" | high (symbol collision with a physical parameter) | none | use $L=2\,\mu$m | no |
| **D3** | `generate_final_figures.py:556, 558, 571, 583` (`fig06`) | Panels (a),(b) x-axis "distance from edge $\ell$ ($\mu$m)" and (a) ylabel "$R_B(\ell)$" use $\ell$ for a distance from the edge; panel (c) ylabel "$L$ (mm)" uses $L$, the reference-plane distance, for the **attenuation length**. | CONFIRMED DEFECT — render `fig06_attenuation.png`: three different meanings on two symbols | high | none | (a),(b): $L$; (c): $L_\alpha$ (attenuation length) | no |
| **D4** | `paper_a_study/figure_data/figure_panel_sources.json` | The panel-source map is **stale and wrong** for most figures. Examples: `fig04` is documented as "(a) R_B edge / (b) R_B at 2 um / (c) R_B at 100 um / (d) Angle", while the figure plots (a) $R_B(k_xd)$, (b) $\theta_E$, (c) $R_B(k_B/k_i)$, (d) $v_g$; `fig05`, `fig06`, `fig07`, `fig08`, `fig09`, `fig10` are equally mismatched (fig10 is documented as "Flux arrows" for panel (d), which is a line plot of $P_{Bx},P_{By}$). | CONFIRMED DEFECT — JSON compared with `generate_final_figures.py` panel by panel | high (it is the only machine-readable panel provenance) | none | regenerate from the plotting code, with the plotted columns | no |
| **D5** | `generate_final_figures.py`, `fig10` panel (c) | A hand-drawn schematic (arrows, plate outline) is presented inside a results figure with **no label saying it is a schematic**. The code comment says so; the reader cannot. | CONFIRMED DEFECT — render `fig10_field.png`: panel (c) is a diagram, caption says only "schematic whose arrows are the solved flux directions" | moderate | none (arrows are solved directions) | add an in-panel "schematic" label; caption keeps the statement | no |
| **D6** | `generate_final_figures.py:513` (`fig05`, panel c) | The panel plots `power_balance_error` ($1.1\times10^{-13}$–$2.5\times10^{-12}$) on a log axis against a $10^{-6}$ threshold, with no statement that the plotted values are the **double-precision floor**. The visible undulation (1.3e-12 → 2.7e-13 → 9e-13) is numerical noise, but it reads as resolved structure. | CONFIRMED DEFECT — render `fig05_channel.png` panel (c); data column `power_balance_error` in `fig05_channel_power.csv` | high (visual exaggeration of round-off) | none | add a floor band/annotation at $10^{-12\pm1}$, relabel the axis "relative power-balance residual", keep the data | no |
| **D7** | `generate_final_figures.py:779` (`fig09`, panel c) | The panel that plots residuals ($10^{-15}$–$10^{-12}$) has ylabel "magnitude" and a text note but no numerical floor. Panels (a),(b) let curves run off the bottom of the axes ($|\Delta R_B|/R_B$ reaches $\sim10^{-9}$ against `ylim` $10^{-9}$). | CONFIRMED DEFECT (label); PRESENTATION ONLY (clip) | moderate | none | ylabel "residual magnitude (dimensionless)"; floor statement $\sim10^{-15}$; axes limits set so no curve is clipped | no |
| **D8** | `paper_a_study/peak_search.py:189–194` | `quadrature_spread` is computed over the rows `(22,64),(22,128),(22,192),(22,256),(30,64),(30,256)` — **it mixes the Galerkin degree with the quadrature order**. The quantity is labelled "quadrature spread" but is not a quadrature measure. | CONFIRMED DEFECT — source read; `quadrature_audit.py` (the dedicated study) uses a fixed degree | moderate (mis-labels a diagnostic) | none | restrict the spread to the four degree-22 rows, keep the degree-30 rows for reporting | yes, `peak_search.py` re-run |
| **D9** | `claims.json` + `claim_audit.py:157–160` | `degree_stability_peak` (5e-9) and `quadrature_stability_peak` (5.6e-9) are registered as **values with a 1 % tolerance**, but they are *differences of nearly equal numbers* lying on the numerical floor. Re-running the search moves them by 10–30 % while the headline moves by $8\times10^{-13}$. The battery therefore returns a **false FAIL** (round 10: 17 PASS / 1 FAIL / 1 SKIP). | CONFIRMED DEFECT — round-10 battery log; committed vs regenerated records: 4.973e-9/7.281e-9 against 5.613e-9/6.220e-9; 5.591e-9 against 9.382e-10 | high (a gate that fires on noise teaches the reader to ignore it) | none | register both as **bounds** with bound semantics in the gate, verified against every executed run; keep the source-agreement comparison as an inequality | yes |
| **D10** | `sections/results.tex` §4.6 and §4.8, `sections/conclusions.tex` item 2 | The text quotes the two spreads to two significant figures ("stable to $5.0\times10^{-9}$", "$5.6\times10^{-9}$"), a precision the quantity does not support. | CONFIRMED DEFECT — as D9 | moderate | none | state bounds ("below $10^{-8}$") consistent with every run on record | no |
| **D11** | `sections/results.tex` §4.1, `sections/discussion.tex` §5.2, `generate_final_figures.py` `fig01` inset | The text claims the coupling shifts the frequency "by at most $\pm\SI{60}{\kilo\hertz}$ … less than $4\times10^{-6}$ in relative terms" and (twice) "by less than $4\times10^{-6}$". The stored data of the very panel cited give a maximum $\lvert\Delta f\rvert=\SI{183.7}{\kilo\hertz}$ at $k_xd=1.05$ ($1.09\times10^{-5}$ relative), $\SI{161.2}{\kilo\hertz}$ up to $k_xd=0.90$, and $\SI{140.4}{\kilo\hertz}$ at $k_xd=0.75$. All five shifts are negative (the coupling lowers the carrier), and the inset, drawn with $\pm150$ kHz, **clips the $H/H^*=+0.05$ curve at the bottom of its frame** (it reaches $\SI{-183.7}{\kilo\hertz}$). | CONFIRMED DEFECT — `fig01_dispersion_velocity_attenuation.csv`, computed over all 31 wavenumbers and all five $H$ levels; visible in `fig01_dispersion.png`, where the $H/H^*=+0.05$ curve leaves the inset frame at its lower edge | **high** (a quantitative claim contradicted by its own figure data, and hidden by a clipped panel) | the result is unchanged; the sentence is wrong | widen the inset to contain $\pm200$ kHz; correct the two sentences; register the corrected claim | no (data unchanged) |
| **D12** | `sections/results.tex` §4.1 | "they agree with each other to better than $\SI{3.5}{\percent}$ over the whole branch". The stored ratios give 6.45 % at $k_xd=0.15$ (the first sample), 3.43 % at 1.05 and 3.40 % at 0.54; every other sample is below 3 % and the median is 0.49 %. | CONFIRMED DEFECT (overstated bound) | moderate | none | state the measured maximum and where it occurs | no |
| **D13** | `sections/results.tex` §4.3 | "$\ell=\SI{90}{\nano\metre}$ shifts the frequency by $\SI{+1.9}{\percent}$ at $k_xd=0.1$ … $\SI{+10.2}{\percent}$ at $k_xd=1.0$". The solved grid starts at $k_xd=0.15$ and ends at 1.05; the stored values are $+2.0\%$ and $+10.2\%$. | PRESENTATION ONLY | low | none | quote the actual abscissae and the stored percentages | no |
| **D14** | `paper_a_study/test_model.py` | No test inspects figure labels, panel provenance or the numerical floor. The defects D1–D7 were therefore invisible to 39 passing tests. | CONFIRMED DEFECT (coverage) | high | none | add a `TestFigureProvenance` class (labels, panel map, floor statements, no "reflectance" for $R_B$) | no |
| **D15** | `paper_a_study/mutation_tests.py` | No mutant exercises the bound-style claim or a figure-label defect, so D9 and D1 would not be caught if they returned. | CONFIRMED DEFECT (coverage) | moderate | none | add mutants M13 (bound violated) and M14 (figure label reverted) | no |
| **D16** | `sections/results.tex` §4.10, `fig06` data | The attenuation-length and loss-coefficient statements (18.5 mm → 0.30 mm, 0.47 → 29 dB/mm) were re-read from `fig06_attenuation_distance.csv` and agree with the plotted quantities. | ALREADY CORRECT | — | — | none | no |
| **D17** | `peak_search.py` headline and classification | `K_at_max = 0.52752`, `R_B_at_max = 0.9467954`, `certified_local_maximum`; a coarse raster cannot reach it; the maximum is interior to the scanned domain. Re-read from the committed record. | ALREADY CORRECT | — | — | none | no |
| **D18** | Round-9 plane transform (`model.py`, all producers) | One implementation of $R(L_{\rm to})=R(L_{\rm from})\exp[2(\Imag K_i-\Imag K_B)(L_{\rm from}-L_{\rm to})]$, imported by every producer; cross-script agreement $10^{-6}$; the old single-mode form appears nowhere in the production path. | ALREADY CORRECT | — | — | none | no |
| **D19** | `claim_audit.py` gates | Deprecated strings (0.99985, 28.06, 93.19, 33.1, "110 rows") guarded; figure-citation order checked; abstract membership checked; source agreement on 9 rows; the round-9 defect and the round-8 stale maximum are both still detectable. | ALREADY CORRECT | — | — | keep every check when D9 is repaired | no |
| **D20** | LaTeX build | No `pdflatex`, `latexmk`, `tectonic`, `xelatex` or `lualatex` exists in this environment. | UNVERIFIED (environmental) | — | — | keep **BUILD UNVERIFIED**; no PDF claimed | no |
| **D21** | Byte-identity of regenerated PDFs | Matplotlib writes a creation timestamp into PDF metadata; byte-identity across runs is therefore not a meaningful criterion. Agreement must be judged on plotted data, geometry and labels. | NOT APPLICABLE (by design) | — | — | compare data and text, not bytes; state the criterion in the report | no |
| **D22** | `fig09` panels (a),(b) — data below the axis limit | The curves are clipped by `ylim` (values reach $10^{-9}$ and $10^{-14}$). Registered with D7. | PRESENTATION ONLY | low | none | extend the axis limits and annotate the floor | no |
| **D23** | `fig03` panel (d) and the §4.3 percentages | Stored: $\ell=90$ nm gives $+2.0\%$ at $k_xd=0.15$ and $+10.2\%$ at 1.05; $\ell=35$ nm gives $-1.9\%$ and $-4.9\%$. The text's $-1.8\%$ is a rounding of $-1.9\%$. | PRESENTATION ONLY | low | none | align the text with the stored values (D13) | no |
| **D24** | `generate_final_figures.py`, `fig08` gridspec | The xlabel of panel (c) is a tall integral expression and is **cut by the bottom edge of the canvas**: the stored PNG has ink in its last three rows (`rows[-3:] = [95, 92, 107]`), which no other figure has. | CONFIRMED DEFECT (presentation) — pixel test on `fig08_boundary.png`, and visible in the render | low | none | raise the bottom margin of that figure only (`bottom=0.150`), keep the canvas contract | no |

---

## 3. What is *not* a defect (explicitly recorded so that no later reader "fixes" it)

* The headline numbers of the round-10 baseline all reproduce: operating point 2.31456 %, refined
  maximum 94.6795 %, $k_xd=0.5275$ / argmax 0.52752, 16.6547 GHz, $H/H^*=+0.05$ reference-plane
  62.2973 %, baseline edge-plane 98.5572 %.
* The round-9 plane transform, the admissibility re-derivation, the corner-band shares, the matched
  controls and the 39 scientific tests are consistent with the data; none of them required a change.
* The Gauss–Legendre order (≥ 64 for every degree used) and the Galerkin range 14–34 are adequate; no
  new convergence experiment is invented here.
* Log axes on `fig01(c,d)`, `fig02(a,b,d)`, `fig05(a,b)`, `fig06(a,b)` are legitimate: those quantities
  span three decades or more. Only the *residual* panels (D6, D7) need floor statements.
* The schematic of `fig10(c)` is retained: its arrows are the solved directions, and it carries
  information the maps do not. It needs a label, not removal.

---

## 4. Repair plan for Stage 2 (in the order executed)

1. **Registry and spreads (D8, D9, D10).** Fix `quadrature_spread` to a degree-pure quantity; register
   both spreads as bounds; teach `claim_audit.py` bound semantics; restate the two manuscript
   sentences as bounds; verify that a genuinely wrong convergence figure (spread $10^{-5}$) still
   fails the gate.
2. **Numerical sentences contradicted by their own data (D11, D12, D13).** Correct the three
   sentences of §4.1/§4.3/§5.2 to the stored values, register the corrected $\Delta f$ claim, widen the
   `fig01` inset so the curve is not clipped.
3. **Figure defects (D1–D5, D6, D7, D22).** Relabel `fig02(c)`, `fig04(a,c)`, `fig06(a,b,c)`; label
   the `fig05(c)` and `fig09(c)` floors; label the `fig10(c)` schematic; rebuild
   `figure_panel_sources.json` from the plotting code.
4. **Coverage (D14, D15).** Add figure-provenance tests and two mutants.
5. **Clean reproduction.** Delete the generated datasets, regenerate them from the solver, regenerate
   the ten figures, and run the full battery **without restoring any old JSON**. The acceptance
   criterion is zero unexplained FAIL.
6. **Reports, package, ZIP, commit, push.** Then stop for supervisor review; Round 12 not started.

---

## 5. Severity summary

| class | ids | count |
|---|---|---|
| CONFIRMED DEFECT — scientific statement contradicted by data | D11, D12 | 2 |
| CONFIRMED DEFECT — numerical diagnostic / gate | D8, D9, D10 | 3 |
| CONFIRMED DEFECT — figure labels, provenance, floor, schematic | D1–D7, D24 | 8 |
| CONFIRMED DEFECT — test coverage | D14, D15 | 2 |
| PRESENTATION ONLY | D13, D22, D23, D24 | 4 |
| ALREADY CORRECT | D16–D19 | 4 |
| UNVERIFIED / NOT APPLICABLE | D20, D21 | 2 |

The two items that change what a reader would conclude are **D11** (a quoted coupling-induced frequency
shift three times smaller than the stored data) and **D9** (a validation gate that fails on round-off);
both are repaired below, and both are added to the class of defects the suite can detect.
