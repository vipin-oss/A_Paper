# FIGURE_PROVENANCE

Every figure in the manuscript, traced from the plotted ink back to the solver call.
The machine-readable version of the same map is
`03_DATA/figure_data/figure_panel_sources.json` (per-panel description, columns read,
and `sha256` + byte size of each shipped `pdf`/`png`/`svg`), and it is enforced by
`test_panel_map_agrees_with_the_plotting_code` and
`test_every_figure_is_mapped_with_four_panels`.

**Universal chain (applies to all ten figures):**

```
01_PROGRAM/paper_a_study/model.py            physics + spatial/temporal solvers
        │
        ├─ build_figure_data.py              → 03_DATA/figure_data/*.csv|*.json
        │      (DEGREE=22, nquad=64, KY0, OMEGA0, K0, KB0, REF_NORM=10 d)
        │
        └─ generate_final_figures.py         → 08_FINAL_OUTPUTS/figures_final/*.{pdf,png,svg}
               (figure_style.py: rcParams, fonts, colour cycle, panel labels)
```

Commands (from the repository root, environment from
`04_REPRODUCTION/REPRODUCE_FROM_SCRATCH.md`):

```bash
cd paper_a_study
python build_figure_data.py          # ≈ 8 min, writes figure_data/
python generate_final_figures.py     # ≈ 10 s,  writes figures_final/
```

Delivered figure PDFs are copied into the manuscript by
`build_submission_package.py` (and are already present in `02_OVERLEAF/figures/`).
Expected outcome: all 16 CSVs and ~20 JSONs regenerate, all 10 figures are written in
three formats, and the CSVs reproduce to the last stored digit (see
`04_REPRODUCTION/REPRODUCTION_TEST_RESULT.md` for the measured comparison).

## 1. Map from figure to data

| Figure | Data source (in `03_DATA/figure_data/`) | panels | columns read | delivered PDF sha256 (first 16) | bytes |
|---|---|---|---|---|---|
| fig01_dispersion | fig01_dispersion_velocity_attenuation.csv | 4 | (a) `frequency_GHz`; (b) `phase_speed_m_s`, `group_speed_m_s`, `energy_speed_m_s`; (c) `FWHM_MHz`; (d) `attenuation_dB_per_mm` | `e457dde5b4d389cf…` | 39540 |
| fig02_material | fig02_material_parameter_sweep.csv | 4 | (a) `FWHM_MHz`; (b) `attenuation_dB_per_mm`; (c) `R_B_2um`; (d) `FWHM_MHz` | `07db661a9749abb6…` | 38976 |
| fig03_geometry | fig03_geometry_sweep.csv | 4 | (a)–(d) `frequency_GHz` | `06e429b4bc09a19e…` | 37074 |
| fig04_frequency | fig04_frequency_reflection.csv | 4 | (a) `R_B_2um`; (b) `angle_deg`; (c) `R_B_2um`, `K_ratio`; (d) `group_speed_m_s` | `06ea81fe6ff1f02b…` | 39532 |
| fig05_channel | fig05_channel_power.csv | 4 | (a) `backward_channel_fraction`, `other_propagating_fraction`, `dissipated_fraction`, `cross_interference_fraction`; (b) same; (c) `power_balance_error`; (d) `R_B_2um` | `610fe18dcf15bfae…` | 34588 |
| fig06_attenuation | fig06_attenuation_distance.csv | 4 | (a) `R_B_isolated`; (b) `incident_survival`; (c) `attenuation_length_incident_mm`, `attenuation_length_backward_mm`; (d) `incident_attenuation_dB_per_mm`, `backward_attenuation_dB_per_mm` | `48a7b5cd6778b338…` | 33797 |
| fig07_coupling | fig07_coupling_sensitivity.csv | 4 | (a) `R_B_2um`; (b) `R_B_2um`; (c) `rel_change_percent`; (d) `rel_change_percent` | `8b094ad9fcc0c476…` | 35714 |
| fig08_boundary | fig08_thickness_flux.csv | 4 | (a) `backward_Px`, `incident_Px`; (b) `backward_Pz`, `incident_Px`; (c) `backward_Px`, `quadrature_weight`; (d) `backward_Px`, `incident_Px` | `2d09161589d6092f…` | 39257 |
| fig09_validation | fig09_validation_convergence.csv (+ `fig09_temporal_spatial_consistency.csv`) | 4 | (a) `R_B_rel_error`; (b) `K_B_rel_error`; (c) `edge_scaled_residual`, `power_error`; (d) `rel_K_mismatch` | `62ea76d9f0dd3596…` | 33815 |
| fig10_field | fig10_field_maps.csv (+ `fig10_field_metrics.json` for panel (c); panel (d) reads `Px_backward`, `Py_backward` from the metrics file) | 4 | (a) `incident_intensity`; (b) `backward_intensity`; (c) metrics JSON; (d) metrics JSON | `8c1ea289d101ac3d…` | 48618 |

Row counts of the sources (data rows, header excluded): fig01 155, fig02 130,
fig03 210, fig04 139, fig05 5, fig06 50, fig07 95, fig08 320, fig09_validation 7,
fig09_temporal 11, fig10_field_maps 22801.

## 2. Per-figure expected results (what a correct re-run must reproduce)

| Figure | Anchor value(s) that must come back | Stored in |
|---|---|---|
| fig01 | `f = 16.684 GHz` at the operating point; dispersion of the five `H` levels; `k_EM d = 2.211005e-4` vs `2.2e-4` (`rel 4.98e-3`) | `fig01_*.csv`, `phase_speed_audit.json` |
| fig02 | 130 rows, all `status = admissible`, 0 flipped; `R_B_2um` stable inside the literature bands | `fig02_*.csv`, `reclassify` check |
| fig03 | 210 rows; `ℓ/d` sweep from 0 to 0.5 | `fig03_*.csv` |
| fig04 | `R_B(2 µm) = 0.9428718` at `k_x d = 0.52719`; `0.5519095` at `k_x d = 0.55`; angle `−13.85°` at the peak, `−27.90°` at the operating point | `peak_search.json`, `peak_certification.json` |
| fig05 | partition closes to `1.3e-17` at `η = −0.05`; `backward_channel_fraction = 0.0190511` there; `other_propagating = 0.9739`; dissipation `0.006906` | `fig05_channel_power.csv` |
| fig06 | isolated return follows `R_B(l) = R_B,edge exp(−α_B l)`; `α_B = 87.1 dB/mm` at the peak | `fig06_*.csv`, `claims.json: attenuation_peak_backward` |
| fig07 | relative change of `R_B` under `k_y` detuning: `1.21 %` at the operating point, `36.1 %` at the peak | `fig07_*.csv`, `claims.json` |
| fig08 | thickness flux profiles with `quadrature_weight`; nodal values are **not** pointwise boundary data (see `06_VALIDATION/reports/PAPER_A_ROUND21_GATE1_DERIVATION.md`) | `fig08_*.csv` |
| fig09 | `R_B` relative spread across degrees 14…33 `= 1.6e-6…2.6e-5` about the reference; `K_B` mismatch `< 4e-12`; temporal-vs-spatial `rel_K_mismatch ≈ 1.9e-5` | `fig09_*.csv` |
| fig10 | incident peak 0.99923, backward peak 0.039355 at the `−2 µm` plane; `backward_Px = −0.0154248`, `backward_Py = −0.0081669`; reflected angle `−27.90°` | `fig10_field_metrics.json` |

## 3. Traps a re-runner must know (all are enforced by tests)

1. **`R_B` is a modal share of the backward channel, never a reflectance.**  The total
   propagating share is a different number reported in Fig. 5, and
   `test_backward_share_is_never_called_a_reflectance` fails if the wording drifts.
2. **The reference plane is `L = 10 d = 2 µm`** and the gradient length is `ℓ`, not the
   other way round (`test_the_reference_plane_is_L_and_the_gradient_length_is_l`).
3. **Attenuation comes from complex spatial roots**, `α = 2|Im k_x|`; it is *not* the
   imaginary part of `√(K² + k_y²)` at real `K`, which vanishes identically.
4. **Group velocity** is `c_s dω/dk_x` by central differences on a branch-tracked
   sequence; the older columns that divided by `|k|³` (and the duplicated energy-speed
   column) were **discontinued**, not fixed.
5. **`incident_survival` is `exp(−2 Im k_i ℓ) ≤ 1`**; the reciprocal was shipped once
   and is wrong.
6. **The flux arrow must oppose the wavenumber** for the backward branch
   (`test_flux_opposes_the_wavenumber`), and the drawn backward wavenumber must be the
   solved one (`test_drawn_backward_wavenumber_is_the_solved_one`).
7. **Residual panels declare their round-off floor** — a `1e-16` residual is not
   "better physics" (`test_residual_panels_declare_their_round_off_floor`).
8. **No panel ink touches the canvas edge** (`test_no_panel_ink_touches_the_canvas_edge`).
9. The panel-(c) schematic of Fig. 10 is annotated as a schematic
   (`test_the_schematic_panel_is_labelled`).

## 4. Size hazard

`paper_a_study/figures_final/fig10_field.svg` and `paper_a_study/results/fig10_field.svg`
are each **29 MB** (dense vector field maps).  They are **not** shipped in this archive;
the PDF (48,618 B) and PNG are, and the SVG regenerates in ~10 s from
`generate_final_figures.py`.  Nothing in the manuscript includes the SVG.
