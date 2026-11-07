# Paper A — Round 11: panel-source matrix

**Defect repaired here: D4.** The map that shipped up to round 10
(`paper_a_study/figure_data/figure_panel_sources.json`) was maintained by hand and
had drifted away from the plotting code: `fig04` was documented as
"(a) R_B edge / (b) R_B at 2 um / (c) R_B at 100 um / (d) Angle" while the figure
plots (a) $R_B(k_xd)$, (b) $\theta_E$, (c) $R_B(k_B/k_i)$, (d) $v_g$; `fig08` and
`fig09` were equally wrong, and `fig10(d)` was documented as "Flux arrows", which
is panel (c).

The map is now **derived from the plotting code**: `generate_final_figures.py`
carries a `PANEL_SOURCES` table, writes the JSON on every render
(`write_panel_sources()`), and `TestFigureProvenance.test_panel_map_agrees_with_the_plotting_code`
fails if the two ever differ. The table below is generated from that JSON.

Canvas contract for all ten figures: 6.50 × 5.10 in, `savefig.bbox = None`,
11 pt axis labels, 9 pt ticks, 2 × 2 panels, one shared $H/H^*$ legend in the
reserved top band. No title inside a panel; only the bold (a)–(d) tags.

Each panel is drawn from the CSV column(s) named in the last column; no panel
reads a value that is not in the stored data, and no panel interpolates.

### `fig01_dispersion`

**Data:** `fig01_dispersion_velocity_attenuation.csv`

| panel | what is plotted | column(s) | round-10 map said |
|---|---|---|---|
| (a) | frequency f(k_xd) for the five H levels, operating point marked | `frequency_GHz` | frequency f(k_xd) for the five H levels, operating point marked |
| (b) | phase speed (right axis), group and energy velocity (left axis) | `phase_speed_m_s; group_speed_m_s; energy_speed_m_s` | phase speed (right axis), group and energy velocity (left axis) |
| (c) | linewidth FWHM | `FWHM_MHz` | linewidth FWHM |
| (d) | carrier attenuation | `attenuation_dB_per_mm` | carrier attenuation |

### `fig02_material`

**Data:** `fig02_material_parameter_sweep.csv`

| panel | what is plotted | column(s) | round-10 map said |
|---|---|---|---|
| (a) | linewidth FWHM against carrier density n0 | `FWHM_MHz` | linewidth FWHM against carrier density n0 |
| (b) | attenuation against carrier density n0 | `attenuation_dB_per_mm` | attenuation against carrier density n0 |
| (c) | backward modal share R_B at the reference plane L = 2 um (all n0) | `R_B_2um` | backward modal share R_B at the reference plane L = 2 um (all n0) |
| (d) | linewidth FWHM against mobility | `FWHM_MHz` | linewidth FWHM against mobility |

### `fig03_geometry`

**Data:** `fig03_geometry_sweep.csv`

| panel | what is plotted | column(s) | round-10 map said |
|---|---|---|---|
| (a) | frequency against k_xd for the plate-thickness family | `frequency_GHz` | frequency against k_xd for the plate-thickness family |
| (b) | frequency against k_xd for the gradient-length family | `frequency_GHz` | frequency against k_xd for the gradient-length family |
| (c) | frequency change at k_xd = 0.50 against plate thickness | `frequency_GHz` | frequency change at k_xd = 0.50 against plate thickness |
| (d) | relative frequency change against k_xd for the gradient length | `frequency_GHz` | relative frequency change against k_xd for the gradient length |

### `fig04_frequency`

**Data:** `fig04_frequency_reflection.csv`

| panel | what is plotted | column(s) | round-10 map said |
|---|---|---|---|
| (a) | R_B at the reference plane L = 2 um against k_xd, peak resolved in an inset | `R_B_2um` | R_B at the reference plane L = 2 um against k_xd, peak resolved in an inset |
| (b) | energy angle theta_E | `angle_deg` | energy angle theta_E |
| (c) | R_B at L = 2 um against the wavenumber ratio k_Bx/k_ix | `R_B_2um; K_ratio` | R_B at L = 2 um against the wavenumber ratio k_Bx/k_ix |
| (d) | group velocity v_g | `group_speed_m_s` | group velocity v_g |

### `fig05_channel`

**Data:** `fig05_channel_power.csv`

| panel | what is plotted | column(s) | round-10 map said |
|---|---|---|---|
| (a) | modal power budget of the solved flux at H = 0 | `backward_channel_fraction; other_propagating_fraction; dissipated_fraction; cross_interference_fraction` | modal power budget of the solved flux at H = 0 |
| (b) | the same four fractions against H | `backward_channel_fraction; other_propagating_fraction; dissipated_fraction; cross_interference_fraction` | the same four fractions against H |
| (c) | relative power-balance residual against H (round-off floor, not a trend) | `power_balance_error` | relative power-balance residual against H (round-off floor, not a trend) |
| (d) | relative change of the reference-plane share, [R_B(H)-R_B(0)]/R_B(0) | `R_B_2um` | relative change of the reference-plane share, [R_B(H)-R_B(0)]/R_B(0) |

### `fig06_attenuation`

**Data:** `fig06_attenuation_distance.csv`

| panel | what is plotted | column(s) | round-10 map said |
|---|---|---|---|
| (a) | isolated-channel R_B against distance L from the edge | `R_B_isolated` | isolated-channel R_B against distance L from the edge |
| (b) | incident power surviving to distance L from the edge | `incident_survival` | incident power surviving to distance L from the edge |
| (c) | attenuation length L_alpha of both channels against H | `attenuation_length_incident_mm; attenuation_length_backward_mm` | attenuation length L_alpha of both channels against H |
| (d) | attenuation coefficient alpha of both channels against H | `incident_attenuation_dB_per_mm; backward_attenuation_dB_per_mm` | attenuation coefficient alpha of both channels against H |

### `fig07_coupling`

**Data:** `fig07_coupling_sensitivity.csv`

| panel | what is plotted | column(s) | round-10 map said |
|---|---|---|---|
| (a) | R_B against transverse wavenumber for the five H levels | `R_B_2um` | R_B against transverse wavenumber for the five H levels |
| (b) | the (k_y d, H) landscape drawn on the measured grid, no interpolation | `R_B_2um` | the (k_y d, H) landscape drawn on the measured grid, no interpolation |
| (c) | relative change of R_B against H along three declared slices | `rel_change_percent` | relative change of R_B against H along three declared slices |
| (d) | the same change against the transverse wavenumber | `rel_change_percent` | the same change against the transverse wavenumber |

### `fig08_boundary`

**Data:** `fig08_thickness_flux.csv`

| panel | what is plotted | column(s) | round-10 map said |
|---|---|---|---|
| (a) | backward x flux through the thickness, P_Bx(z)/P_inc | `backward_Px; incident_Px` | backward x flux through the thickness, P_Bx(z)/P_inc |
| (b) | backward z flux through the thickness, P_Bz(z)/P_inc | `backward_Pz; incident_Px` | backward z flux through the thickness, P_Bz(z)/P_inc |
| (c) | running through-thickness integral of the backward x flux | `backward_Px; quadrature_weight` | running through-thickness integral of the backward x flux |
| (d) | shape of the backward and incident modes at H = 0 | `backward_Px; incident_Px` | shape of the backward and incident modes at H = 0 |

### `fig09_validation`

**Data:** `fig09_validation_convergence.csv + fig09_temporal_spatial_consistency.csv`

| panel | what is plotted | column(s) | round-10 map said |
|---|---|---|---|
| (a) | relative error of the share against the Galerkin degree | `R_B_rel_error` | relative error of the share against the Galerkin degree |
| (b) | relative error of the backward wavenumber against the degree | `K_B_rel_error` | relative error of the backward wavenumber against the degree |
| (c) | scaled edge residual and relative energy-balance error (floor ~1e-15) | `edge_scaled_residual; power_error` | scaled edge residual and relative energy-balance error (floor ~1e-15) |
| (d) | temporal-generator versus complex spatial QEP mismatch against k_xd | `rel_K_mismatch` | temporal-generator versus complex spatial QEP mismatch against k_xd |

### `fig10_field`

**Data:** `fig10_field_maps.csv`

| panel | what is plotted | column(s) | round-10 map said |
|---|---|---|---|
| (a) | incident intensity map, normalised to the common maximum | `incident_intensity` | incident intensity map, normalised to the common maximum |
| (b) | backward intensity map on the same colour scale | `backward_intensity` | backward intensity map on the same colour scale |
| (c) | schematic of the plate and the edge; arrow directions taken from the solved flux | `figure_data/fig10_field_metrics.json` | schematic of the plate and the edge; arrow directions taken from the solved flux |
| (d) | backward x and y flux fractions against the transverse wavenumber | `Px_backward; Py_backward` | backward x and y flux fractions against the transverse wavenumber |

## Column coverage check

Every column named above exists in the file that is named for it, and every
plotted column is reproduced by `build_figure_data.py` from the solver (measured
in `PAPER_A_ROUND11_NUMERICAL_REPRODUCIBILITY.md`). Three columns that the
round-10 CSVs contained (`x_flux_fraction` in `fig02`, `fig04`, `fig07`) are no
longer written by the generator and are read by no plotting code; the regenerated
files therefore do not carry them, and no panel changes. That difference is
recorded as a schema note, not as an unexplained figure change.

`fig09` reads two files: the convergence sweep (`fig09_validation_convergence.csv`)
for panels (a)–(c) and the temporal-versus-spatial comparison
(`fig09_temporal_spatial_consistency.csv`) for panel (d). Both are listed as
sources above.

`fig10` panel (c) is the only panel that is not a plot of a data column: it is a
schematic whose arrow directions come from `fig10_field_metrics.json`
(`primary_flux`), and it is now labelled "schematic" inside the panel.
