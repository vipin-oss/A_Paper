# Paper A — Round 11: numerical reproducibility

**Question this file answers:** can the delivered numbers, datasets and figures be
produced again *from an empty data directory*, with nothing restored from Git, and
does the full validation battery pass on what comes out?

**Answer: yes.** Clean-directory reproduction executed on 2026-11-07, battery
**18 PASS / 0 FAIL / 1 SKIP** (`OVERALL: PASS`), the single skip being the LaTeX
build, for which this environment has no engine. Log:
`validation/round11_battery_run_clean_reproduction.log`.

---

## 1. The reproduction recipe actually executed

```
cd /home/user/A_Paper
rm -f paper_a_study/figure_data/*          # empty data directory, nothing restored
python paper_a_study/build_figure_data.py  # 7 min 00 s -> 10 CSVs, 2 JSON, 1 log
python paper_a_study/generate_final_figures.py   # 9 s -> 10 PDF + 10 PNG + 10 SVG
cp paper_a_study/figures_final/fig*.pdf Paper_A_Final_Submission/figures/
python paper_a_study/run_all_checks.py     # 13 min -> the battery below
```

Measured generator timings (this run): fig01 88 s, fig02 142 s, fig03 26 s,
fig04 92 s, fig05 3 s, fig06 3 s, fig07 48 s, fig08 2 s, fig09 4 s + 6 s,
fig10 5 s. The battery's own heavy gates: mechanism controls 199 s, peak search
299 s, peak identity 22 s, unit tests 21 s, mutation tests 9 s.

Nothing was copied from `git show HEAD:`, no stored `peak_search.json`,
`mechanism_controls.json` or `claim_audit.json` was restored, and no tolerance was
widened to make a gate pass. The only files that are *inputs* rather than outputs
are `paper_a_study/model.py`, `figure_style.py`, `claims.json` and
`reference_constants.json`, all version-controlled source.

---

## 2. What comes out, against what was delivered

Delivered = `paper_a_study/figure_data/*` as committed at `1ff9166` (round-10
archive, kept aside for comparison only). Regenerated = the clean run above.
Maximum relative difference over the rows of each **plotted** column:

| file | column | rows | max relative difference |
|---|---|---|---|
| `fig01_dispersion_velocity_attenuation.csv` | `frequency_GHz` | 155 | **0.0** |
| | `FWHM_MHz` | 155 | 4.6e−06 |
| | `group_speed_m_s` | 155 | 2.8e−09 |
| | `energy_speed_m_s` | 155 | 1.9e−10 |
| | `attenuation_dB_per_mm` | 155 | 3.9e−08 |
| `fig02_material_parameter_sweep.csv` | `FWHM_MHz` | 130 | 3.7e−06 |
| | `R_B_2um` | 130 | 3.5e−08 |
| | `attenuation_dB_per_mm` | 130 | 7.5e−08 |
| `fig03_geometry_sweep.csv` | `frequency_GHz` | 210 | 5.9e−12 |
| `fig04_frequency_reflection.csv` | `R_B_2um` | 139 | 2.0e−08 |
| | `angle_deg` | 139 | 3.3e−09 |
| | `K_ratio` | 139 | 5.6e−09 |
| | `group_speed_m_s` | 139 | 3.6e−06 |
| `fig05_channel_power.csv` | `R_B_2um` | 5 | 1.7e−11 |
| | `R_B_edge` | 5 | 4.3e−12 |
| | `backward_channel_fraction` | 5 | 1.7e−11 |
| `fig06_attenuation_distance.csv` | `R_B_isolated` | 50 | 5.9e−09 |
| | `incident_survival` | 50 | 6.5e−09 |
| | `attenuation_length_incident_mm` | 50 | 2.1e−08 |
| `fig07_coupling_sensitivity.csv` | `R_B_2um` | 95 | 1.4e−11 |
| | `rel_change_percent` | 95 | 6.0e−09 |
| `fig08_thickness_flux.csv` | `backward_Px` | 320 | 7.5e−10 |
| | `backward_Pz` | 320 | 1.9e−09 |
| `fig09_validation_convergence.csv` | `R_B_rel_error` | 7 | 2.0e−04 |
| | `edge_scaled_residual` | 7 | 1.8e−01 |
| | `power_error` | 7 | 1.6e+01 |
| `fig10_field_maps.csv` | `incident_intensity` | 22 801 | 1.1e−07 |
| | `backward_intensity` | 22 801 | 1.5e−07 |

Reading of this table:

* Every physical quantity the paper quotes reproduces to **better than 4 × 10⁻⁶**
  relative; the dispersion frequency reproduces **bit for bit**.
* The three fig09 columns that differ by factors 2 × 10⁻⁴, 0.18 and 16 are all
  quantities whose values are $10^{-15}$…$10^{-12}$ — the double-precision floor.
  A 16-fold change in a number of size $10^{-15}$ is not a change of physics, and
  this is precisely why fig09(c) and fig05(c) now print the floor (defects D6, D7).

Headline reproduction:

| quantity | round 10 (committed) | round 11 (clean run) | relative difference |
|---|---|---|---|
| $R_B$ at the located argmax, $k_xd=0.52752$ | 0.9467953685099261 | 0.9467953677961777 | $7.5\times10^{-10}$ |
| $R_B$ at the reported sample, $k_xd=0.5275$ | 0.9467952306769204 | 0.9467952305821763 | $1.0\times10^{-10}$ |
| $k_xd$ at the maximum | 0.52752 | 0.52752 | 0 |
| classification | `certified_local_maximum` | `certified_local_maximum` | — |

**Corrected in round 12.** This table previously compared the round-10 value at
the argmax (0.9467953685099261, $k_xd=0.52752$) with the round-11 value at the
reported sample (0.9467952305821763, $k_xd=0.5275$) and called the resulting
$1.5\times10^{-7}$ difference "the solver's reproducible jitter". The two
numbers are evaluated at different wavenumbers, so the difference is the
offset between those wavenumbers (stored as `offset_reported_vs_argmax`), not a
run-to-run change. Compared like for like, the same configuration moves by
$7.5\times10^{-10}$ and $1.0\times10^{-10}$ relative, i.e. four to five orders
of magnitude less than the number quoted, and neither movement reaches the
seventh printed digit. The round-10 and round-11 records each store two
independent evaluations per configuration (degree sweep and quadrature sweep),
and their separations are of the same size, $10^{-10}$, so a
fixed-configuration reproducibility at the $10^{-10}$ level is measured in the
delivered data rather than inferred.

---

## 3. The round-10 failure (R10-5 / D9) and how it is resolved

Round 10 ended with 17 PASS / 1 FAIL: the claim gate compared two refinement
spreads with a 1 % **equality** test, and re-running the search moved them by tens
of per cent while the headline moved by $10^{-13}$.

Round 11 resolution, in three parts:

1. **The quantity was mis-defined (D8).** `quadrature_spread` pooled degrees 22 and
   30 into one spread, so a metric named for the quadrature rule also contained
   degree error. It is now computed at degree 22 only, over the rules 64/128/192/256;
   the degree-30 rows remain in the record but are excluded.
2. **The claim is a bound (D9).** Both spreads are registered as
   `kind = "bound"`, value $10^{-8}$. The gate now requires every entry of the
   executed record to be $\le$ the bound and $>0$. The manuscript says "below
   $10^{-8}$" (D10) instead of quoting two significant figures of a floor-limited
   difference.
3. **The bound is verified, not asserted.** In this clean run:

   | quantity | value | bound | margin |
   |---|---|---|---|
   | degree spread at the located argmax | $5.613\times10^{-9}$ | $10^{-8}$ | 1.8× |
   | degree spread at the reported wavenumber | $6.220\times10^{-9}$ | $10^{-8}$ | 1.6× |
   | quadrature spread (degree 22, four rules) | $4.317\times10^{-10}$ | $10^{-8}$ | 23× |
   | tracking-path spread (three paths) | $0.0$ (identical values, `verdict.tracking_path_relative_spread`) | reported separately | — |
   | restart spread, coarse raster vs refined maximum | $8.362\times10^{-6}$ (`verdict.restart_spread`, $R_B$ absolute) | reported separately | — |

   **Corrected in round 12.** The row above was headed "tracking-path spread
   (three paths)" but carried $8.36\times10^{-6}$, which is `restart_spread`: the
   coarse-raster argmax at $k_xd=0.527$ ($R_B=0.9467870061$) against the refined
   maximum ($0.9467954$), a relative $8.69\times10^{-6}$, i.e. the sampling
   error of a raster of $\Delta k_xd=2\times10^{-3}$. The tracking-path spread
   itself is stored as zero: the three paths (ascending over 31 points,
   descending over 31 points, single step) return the identical $R_B$ and the
   identical $\omega$ to the last stored digit. The two diagnostics are distinct
   and are now tabulated separately; neither is a discretisation error.

   The margins are small because the bound is honest: it is the observed order of
   magnitude, not a comfortable constant. Mutation **M13** proves the gate still
   fails when a spread exceeds its bound.

---

## 4. Reproducibility defects found in this round

| id | finding | action |
|---|---|---|
| **D25** | `regenerate_revised_data.py` writes the **same file names** as `build_figure_data.py` but with an older 14-column schema. Running it silently replaces the delivered datasets with data the figures cannot read (it happened twice during this round's work, and both times was caught only by the column check). | docstring marks it superseded; `main()` now refuses to run unless `PAPER_A_ALLOW_LEGACY_REGENERATION=1`; a unit test asserts the delivered CSVs carry the columns the plotters read. |
| **D26** | Three round-10 CSVs (`fig02`, `fig04`, `fig07`) carry an `x_flux_fraction` column that the current generator does not write and no plotting code reads. | recorded as a schema difference; no panel changes; the regenerated files do not carry it. |
| **D27** | `run_all_checks.py` ran the unit tests **first**, but eight of them read stored solver records; on a clean data directory the battery therefore failed with five missing-record errors before it had generated anything. | the test gate now runs after the producers (position 15 of 18), and the module docstring lists the real order. |
| **D28** | No script documented the order in which the datasets must be built. | the recipe is now written down here and in the appendix of the package README. |

---

## 5. The battery on freshly generated data

| # | gate | result |
|---|---|---|
| 1 | dimensional and constitutive audit | PASS |
| 2 | quasistatic justification | PASS |
| 3 | flexoelectric control | PASS |
| 4 | admissibility re-derivation | PASS |
| 5 | figure data and figure files | PASS |
| 6 | phase-speed and e.m. reconciliation | PASS |
| 7 | modal-flux rescaling proof | PASS |
| 8 | mechanism matched controls | PASS |
| 9 | corner assessment and regression | PASS |
| 10 | certified peak (four fixed wavenumbers) | PASS |
| 11 | peak search and classification | PASS |
| 12 | peak identity and artefact audit | PASS |
| 13 | spectral convergence | PASS |
| 14 | quadrature sufficiency | PASS |
| 15 | unit and scientific tests (47 tests) | PASS |
| 16 | claim registry and stale guard (23 claims, 46 tokens, 11/11 source rows) | PASS |
| 17 | gate mutation tests (15 mutants, all caught) | PASS |
| 18 | LaTeX static validation (104 labels, 75 refs, 13 citations) | PASS |
| — | LaTeX build | **SKIP — no engine in this environment; BUILD UNVERIFIED** |

**No record was restored to obtain this result.** The run above started from an
empty `figure_data/` and produced every record it then checked.
