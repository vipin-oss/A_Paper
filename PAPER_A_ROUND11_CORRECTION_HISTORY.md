# Paper A — Round 11: correction ledger

Every change made in this round, with the defect it repairs, the file it touches and
the evidence that the repair is real. Nothing in this list changes the research
model, the governing equations, the boundary conditions or the solution method.

Base commit: `1ff9166a5bdf27d5d3ed0adeb21472719654bfeb`. Branch:
`arena/ea7ca4dd-a-paper`.

---

## A. Numerical statements corrected because their own data contradicted them

| id | file | before | after | why |
|---|---|---|---|---|
| **D11** | `sections/results.tex` §4.1 | "the coupling shifts the frequency by at most $\pm\SI{60}{\kilo\hertz}$ … less than $4\times10^{-6}$" | "lowers the frequency by at most \SI{184}{\kilo\hertz}, at $k_xd=1.05$ where the carrier is \SI{16.87}{\giga\hertz}, that is $1.1\times10^{-5}$ … at the negative coupling the lowering stays below \SI{92}{\kilo\hertz}" | the stored data of the cited panel give $-\SI{183.7}{\kilo\hertz}$ at the top of the range and $-\SI{91.9}{\kilo\hertz}$ at the bottom; the old claim was three times too small |
| **D11** | `sections/discussion.tex` §5.2 | "shifts the dispersion by less than $4\times10^{-6}$" | "by at most $1.1\times10^{-5}$" | same datum |
| **D12** | `sections/results.tex` §4.1 | "$v_g$ and $v_E$ … agree to better than \SI{3.5}{\percent} over the whole branch (better than \SI{2}{\percent} in the interior)" | "to within \SI{3.5}{\percent} at every sample except the lowest, where the two differ by \SI{6.4}{\percent}" | measured: 6.45 % at $k_xd=0.15$, 3.43 % at 1.05, 3.40 % at 0.54, median 0.49 % |
| **D13** | `sections/results.tex` §4.3 | "+1.9 % at $k_xd=0.1$ … −1.8 %" | "+2.0 % at $k_xd=0.15$ … −1.9 %" | the solved grid starts at 0.15, not 0.1; stored values are +2.0 % / −1.9 % |
| **D10** | `sections/results.tex` §4.6 and §4.8, `sections/conclusions.tex` | "moves by $5.0\times10^{-9}$ … $7.3\times10^{-9}$"; "reproduced to $5.0\times10^{-9}$ … $5.6\times10^{-9}$"; "stable to $5.0\times10^{-9}$" | "stays below $10^{-8}$"; "reproduced to better than $10^{-8}$"; "stable to better than $10^{-8}$" | the quantities are floor-limited differences; two significant figures were not supportable (see D9) |

No other sentence in the manuscript was touched. The Introduction, the Formulation,
the Numerical methods (apart from the sentence above), the Discussion structure and
the Conclusions structure are unchanged from round 10.

## B. Validation and numerical diagnostics

| id | file | change |
|---|---|---|
| **D8** | `peak_search.py` | `quadrature_spread` is now computed at degree 22 only, over rules 64/128/192/256; the degree-30 rows stay in the record but are excluded from a spread that is named for the quadrature rule. A comment states the reason. |
| **D9** | `claims.json`, `claim_audit.py` | the two refinement spreads are registered with `kind = "bound"`, value $10^{-8}$; `agree()` implements inequality semantics (data ≤ bound and > 0) and reports the bound instead of a relative difference; the degree spread is now tested at **both** recorded wavenumbers, not one hand-picked key; the gate adds a source row for the coupling frequency shift (below). |
| **D11** | `claims.json`, `claim_audit.py` | new claim `coupling_frequency_shift_max = 183.7115` kHz, recomputed by the gate from `fig01_dispersion_velocity_attenuation.csv` and compared with the literal `\SI{184}{\kilo\hertz}` in §4.1. |

## C. Figures (labels, provenance, floors, one margin)

| id | figure | change |
|---|---|---|
| **D1** | fig02(c) | ylabel "backward reflectance $R_B$ (%)" → "$R_B$ at $L=2\,\mu$m (%)"; the in-panel note now says "backward modal share at $L=2\,\mu$m" |
| **D2** | fig04(a), (c) | ylabel "$\ell=2\,\mu$m" → "$L=2\,\mu$m"; the inset lifted clear of the descending flank |
| **D3** | fig06(a), (b), (c) | "distance from edge $\ell$" → "distance from the edge $L$"; "$R_B(\ell)$" → "$R_B(L)$"; "$L$ (mm)" (attenuation length) → "attenuation length (mm)" |
| **D4** | `figure_panel_sources.json` | regenerated from a `PANEL_SOURCES` table inside the plotting code on every render; the old hand-maintained map was wrong for most figures |
| **D5** | fig10(c) | in-panel italic label "schematic"; the caption statement that the arrows come from the solved flux is unchanged |
| **D6** | fig05(c) | shaded floor band at $10^{-13}$–$3\times10^{-12}$, label "round-off floor", ylabel "power-balance residual" |
| **D7** | fig09(a), (b), (c) | axes extended so no curve leaves the frame ($10^{-13}$ and $10^{-15}$); note "below $10^{-9}$: round-off floor"; ylabel "residual magnitude"; note "floor $\sim10^{-15}$: not a convergence trend" |
| **D11** | fig01(a) inset | `ylim` ±150 → −200…215 kHz so the $-\SI{183.7}{\kilo\hertz}$ minimum is inside the frame |
| **D22** | fig09(a),(b) | same change as D7 |
| **D24** | fig08 | bottom margin 0.098 → 0.150; the panel-(c) integral xlabel was cut by the canvas edge |

No figure was redesigned, no colour or marker convention changed, no data point was
removed, and no axis scale was changed except to include points that were already in
the data.

## D. Tests and harness

| id | file | change |
|---|---|---|
| **D14** | `test_model.py` | new `TestFigureProvenance`, 8 tests: panel map vs code, four panels + three formats, no "reflectance", $L$ vs $\ell$, floor statements, schematic label, CSV schema, no ink at the canvas edge |
| **D15** | `mutation_tests.py` | new mutants **M13** (registered bound tighter than the executed spread) and **M14** (the corrected label put back, tested through `PAPER_A_FIGURE_SRC`); docstring lists 15 mutations |
| **D27** | `run_all_checks.py` | the unit-test gate now runs **after** the producers whose records it reads (position 15 of 18); the docstring lists the true order. On a clean data directory the old order failed with five missing-record errors. |
| **D28** | this round's reports | the build order is documented: `build_figure_data.py` → `generate_final_figures.py` → copy PDFs → `run_all_checks.py` |
| **D25** | `regenerate_revised_data.py` | marked superseded in the docstring; `main()` refuses to run unless `PAPER_A_ALLOW_LEGACY_REGENERATION=1`, because it writes the same file names with an older 14-column schema |
| **D26** | `figure_data/*.csv` | the regenerated CSVs no longer carry `x_flux_fraction` (written by no current generator, read by no plotter); recorded as a schema note, no panel changes |
| **D26** | `figure_data/` | three files that the current pipeline does not produce are gone from the delivered set: `fig08_boundary_sensitivity.csv`, `fig10_field_source.json`, `figure_manifest.json`. No figure, no test and no gate reads them; the legacy scripts that do (`audit_figures.py`, `generate_revised_figures.py`, `validate_revised_data.py`) belong to the superseded pipeline of D25 and are not run by the battery. The delivered data directory now contains exactly what `build_figure_data.py` writes — 10 CSVs, 2 JSON, 1 build log — plus the records the battery generates. |

## E. Deliberately not changed

* the model, the governing equations, the boundary conditions, the Galerkin scheme,
  the Gauss–Legendre order, and every solver parameter;
* every headline number (2.31456 %, 94.6795 %, 0.5275 / 0.52752, 16.6547 GHz,
  62.2973 %, 98.5572 %, the corner band, the matched controls);
* the round-10 language, structure and captions, except the five sentences listed
  in section A;
* fig05(a) and fig07(b), which are legible and exact — restyling them would be
  appearance work;
* the novelty status (**UNRESOLVED**), the synthetic character of $\ell$, $f$, $H$,
  the single-edge and corner caveats, and the "not submission-ready" statement.

## F. One change that was made and then reverted in the same round

The first attempt at the fig02(c) label was "backward share $R_B$ at
$L=2\,\mu$m (%)". It is over-long for the canvas: the label overflowed the left edge
of the figure (the render showed the leading "b" cut off, and the same happened to
"relative power-balance residual" in fig05(c) and "residual magnitude
(dimensionless)" in fig09(c)). The three labels were shortened and a **pixel test**
now fails if any panel has ink in the first or last row or column of any figure.
This is recorded because it is the kind of damage a well-meant label fix can do.
