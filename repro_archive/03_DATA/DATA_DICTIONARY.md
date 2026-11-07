# DATA_DICTIONARY

Every column of every shipped CSV, and every JSON record, with its unit, its meaning and
where it is computed.  Written from the files themselves and from
`01_PROGRAM/paper_a_study/build_figure_data.py` (line references are to that file).

Conventions common to all files (see `README_DATA.md` §3): `K = k_x d`, `ky = k_y d`,
`eta = H/H*`, `R_B` = backward **modal share**, fluxes normalised to the incident power,
lengths `_um` in micrometres.

---

## 1. `fig01_dispersion_velocity_attenuation.csv` — 155 rows

Computed in `fig01()`.  `Ks = linspace(0.15, 1.05, 31)` × 5 `eta` levels.

| Column | Unit | Meaning |
|---|---|---|
| `eta` | — | `H/H*`, values `−0.05, −0.025, 0, 0.025, 0.05` |
| `K` | — | real incident `k_x d` |
| `ky` | — | `KY0 = 0.12981175031447484` |
| `frequency_GHz` | GHz | `Re ω · c_s/(2πd) / 1e9` (i.e. cycles, not angular) |
| `FWHM_MHz` | MHz | `−2 Im ω · c_s/(2πd) / 1e6`; temporal linewidth |
| `phase_speed_m_s` | m/s | `c_s · Re ω / |k|`, `|k| = hypot(K, ky)` |
| `group_speed_m_s` | m/s | `c_s · dω/dK` by central differences along the branch-tracked sequence |
| `energy_speed_m_s` | m/s | `c_s · P_x / E` (energy velocity, thickness-integrated power / stored energy) |
| `energy_speed_y_m_s` | m/s | the `y`-component of the energy velocity, same normalisation |
| `attenuation_dB_per_mm` | dB/mm | `8.686 · α / 1000`, `α = 2|Im k_x|` from the **spatial** root |
| `attenuation_length_mm` | mm | `1e3/α` |
| `K_spatial_real`, `K_spatial_imag` | — | the complex spatial root at real `Re ω` and real `K` |
| `modal_power` | normalised | `P_x` of the mode (thickness integrated) |
| `modal_energy` | normalised | stored energy of the mode |
| `dissipation_balance` | relative | residual of the modal energy balance |
| `mass_MAC` | — | modal assurance criterion against the tracked branch (1 = same mode) |
| `maximum_growth` | — | largest growth exponent over the cross-section (branch-admissibility diagnostic) |

## 2. `fig02_material_parameter_sweep.csv` — 130 rows

Computed in `fig02()`.  `n0 ∈ {1.0, 1.5, 2.0, 2.5, 3.0}e18 m⁻³`, `μ_e` scaled by
`{0.5, 0.75, 1, 1.25, 1.5}`, `Ks = linspace(0.30, 0.90, 13)`.

| Column | Unit | Meaning |
|---|---|---|
| `parameter` | — | `n0` or `mobility` |
| `value_SI` | m⁻³ or m²/V/s | the swept value |
| `K`, `ky` | — | normalised wavenumbers |
| `frequency_GHz`, `FWHM_MHz` | GHz, MHz | as in fig01 |
| `energy_speed_m_s` | m/s | as in fig01 |
| `attenuation_dB_per_mm` | dB/mm | as in fig01 |
| `status` | — | `computed` or `edge solve failed` |
| `error` | — | exception *type name* if the edge solve failed (empty otherwise) |
| `R_B_2um`, `R_B_edge` | — | backward modal share at the 2 µm plane and at the edge plane |
| `angle_deg` | degrees | reflected-wave angle; **diagnostic only, never used as a gate** |
| `edge_scaled_residual` | relative | scaled residual of the edge system |
| `power_balance_error` | relative | relative power-balance residual of the solve |
| `valid` | bool | `certified_backward(...)`: conservation (`R_B ≤ 1 + |P_cross|/P_inc`) **and** converged solve.  Rows with `R_B = 1.55…5.07` are excluded by physics, not by a plotting threshold |
| `x_flux_fraction` | fraction | share of the mode's flux carried in `x` |

## 3. `fig03_geometry_sweep.csv` — 210 rows

Computed in `fig03()`: plate thickness `d` and gradient length `ℓ` swept together so that
`ℓ/d` spans `0 … 0.5` (the `source` column records which of the two was varied).

| Column | Unit | Meaning |
|---|---|---|
| `parameter` | — | `thickness` or `ell` |
| `value_SI` | m | the swept physical value |
| `value_nm` | nm | the same value in nanometres |
| `K`, `ky` | — | normalised wavenumbers |
| `ell_over_d` | — | `λ = ℓ/d` |
| `frequency_GHz`, `FWHM_MHz` | GHz, MHz | as in fig01 |
| `source` | — | provenance tag of the row (`sweep` / `operating`) |

## 4. `fig04_frequency_reflection.csv` — 139 rows

Computed in `fig04()`: frequency sweep with the edge solved at each sample; this is the
file that carries the certified maximum.

| Column | Unit | Meaning |
|---|---|---|
| `eta`, `K`, `ky` | — | as above |
| `frequency_GHz`, `group_speed_m_s` | GHz, m/s | as above |
| `R_B_2um`, `R_B_edge`, `R_B_100um` | — | backward modal share at `2 µm`, at the edge plane, and at `100 µm` |
| `angle_deg` | degrees | reflected angle |
| `K_incident_real`, `K_incident_imag` | — | the **actual** incident wavenumber used (the incident mode is a root, not exactly `K`) |
| `incident_K_offset` | — | `Re k_inc − K` (how far the root sits from the nominal `K`) |
| `K_backward_real`, `ImK_backward` | — | backward-channel wavenumber |
| `K_ratio` | — | `Re k_B / Re k_inc` (0.996 at the peak) |
| `attenuation_backward_dB_per_mm`, `attenuation_incident_dB_per_mm` | dB/mm | `8.686·2|Im k|/d/1000` for each channel |
| `power_balance_error`, `edge_scaled_residual` | relative | solve diagnostics |
| `certified` | bool | same criterion as `valid` in fig02 |
| `error` | — | exception type name if not solved |
| `x_flux_fraction` | fraction | as above |

## 5. `fig05_channel_power.csv` — 5 rows (one per `eta`)

Computed in `channel_accounting()`: the **power partition** at the operating point.
This is the file that makes `R_B` interpretable, and the one that separates the backward
cross-flux from cross-polarisation (the `cross_interference_fraction` term is
interference of the *same* polarisation, not polarisation conversion).

| Column | Unit | Meaning |
|---|---|---|
| `eta` | — | coupling level |
| `R_B_2um`, `R_B_edge` | — | backward modal share at the two planes |
| `incident_self_power` | normalised | incident power at the reference plane |
| `backward_channel_fraction` | fraction | `−P_B/P_inc` at the reference plane (equals `R_B_2um` by construction) |
| `other_propagating_fraction` | fraction | all other propagating outgoing modes, net of the backward one |
| `evanescent_reactive_fraction` | fraction | sum `|P|` of evanescent modes at the plane (reactive bookkeeping, **not** transported energy) |
| `cross_interference_fraction` | fraction | interference term between incident and outgoing fields at the plane (can be negative) |
| `dissipated_fraction` | fraction | dissipation inside the control volume |
| `propagating_total_fraction` | fraction | total propagating outgoing share (closest thing to a reflectance) |
| `total_outgoing_fraction` | fraction | propagating + evanescent |
| `closure_residual` | relative | independent arithmetic check that plane power = incident + Σ self-powers + interference (measured `1.3e-17`) |
| `propagating_mode_count`, `evanescent_mode_count`, `outgoing_modes`, `negative_power_mode_count` | count | mode census at the operating point (7 / 175 / 182 / 160 at `eta = −0.05`) |
| `power_balance_error`, `edge_scaled_residual`, `svd_condition` | relative | solve diagnostics |

## 6. `fig06_attenuation_distance.csv` — 50 rows

Computed in `fig06()`: one channel's absolute power against observation distance.

| Column | Unit | Meaning |
|---|---|---|
| `eta` | — | coupling level |
| `distance_um` | µm | distance from the edge |
| `distance_um_norm` | — | the same in units of `d` |
| `R_B_isolated` | fraction | `R_B(2 µm)·exp(−α_B(l − 2 µm))`, `α_B = 2|Im K_B|/d`. **Not** a plane transformation of the ratio (the ratio needs the incident attenuation with the opposite sign) |
| `incident_survival` | fraction | `exp(−2 Im k_i ℓ) ≤ 1` — the fraction of incident amplitude surviving from a launch plane at distance `ℓ` |
| `backward_attenuation_dB_per_mm`, `incident_attenuation_dB_per_mm` | dB/mm | per-channel attenuation |
| `attenuation_length_incident_mm`, `attenuation_length_backward_mm` | mm | `1e3/α` per channel |
| `power_balance_error` | relative | solve diagnostic |

## 7. `fig07_coupling_sensitivity.csv` — 95 rows

Computed in `fig07()`: `k_y` detuning sweep.

| Column | Unit | Meaning |
|---|---|---|
| `eta`, `ky`, `frequency_GHz` | —, —, GHz | sweep coordinates |
| `R_B_2um`, `R_B_edge` | — | backward modal share at both planes |
| `angle_deg` | degrees | reflected angle |
| `Px_backward`, `Py_backward` | normalised | backward-channel flux components |
| `vEx_backward` | m/s | `x`-component of the backward energy velocity |
| `edge_scaled_residual`, `power_balance_error` | relative | solve diagnostics |
| `valid` | bool | certification flag |
| `error` | — | exception type if unsolved |
| `rel_change_percent` | % | relative change of `R_B` against the `ky = KY0` reference |
| `x_flux_fraction` | fraction | as above |

## 8. `fig08_thickness_flux.csv` — 320 rows

Computed in `fig08()`: through-thickness flux profiles at the reference plane.

| Column | Unit | Meaning |
|---|---|---|
| `eta` | — | coupling level |
| `z` | — | normalised thickness coordinate `z/d ∈ [−0.5, 0.5]` |
| `quadrature_weight` | — | Gauss–Legendre weight at that node (sums to 1 over the section) |
| `incident_Px`, `incident_Pz` | normalised | incident flux components |
| `backward_Px`, `backward_Pz` | normalised | backward-channel flux components |

Nodal values are **pointwise samples of a spectral reconstruction**; they are not the
natural boundary data (which are integrated against test functions).  See
`06_VALIDATION/reports/PAPER_A_ROUND21_GATE1_DERIVATION.md` for why sampling at the
nearest Gauss node is the wrong way to check a traction-free face.

## 9. `fig09_validation_convergence.csv` — 7 rows

Produced by `convergence_audit.py` (not `build_figure_data.py`).

| Column | Unit | Meaning |
|---|---|---|
| `degree` | — | polynomial degree |
| `basis_degree` | — | degree actually used by the assembly (equal to `degree`) |
| `quadrature_order` | — | Gauss nodes; 64 except 76 at degree 33 |
| `R_B` | — | backward modal share at the operating point |
| `K_B_real`, `K_B_imag` | — | backward wavenumber |
| `edge_scaled_residual` | relative | `~1e-15` |
| `power_error` | relative | `~1e-12…1e-15` |
| `outgoing_modes` | count | must grow with `degree` (118 → 270); structural check |
| `R_B_rel_error`, `K_B_rel_error` | relative | error against the reference row |
| `is_reference` | bool | true only for the `degree = 33` row |

## 10. `fig09_temporal_spatial_consistency.csv` — 11 rows

Produced by `convergence_audit.py`: temporal route vs spatial route at the same `ky`.

| Column | Unit | Meaning |
|---|---|---|
| `K`, `ky` | — | wavenumbers |
| `frequency_GHz` | GHz | `Re ω` from the temporal route |
| `omega_imag` | — | `Im ω` (temporal decay) |
| `K_temporal_real` | — | `K` from the temporal route (input) |
| `K_spatial_real`, `K_spatial_imag` | — | spatial root at the same real frequency |
| `abs_K_mismatch`, `rel_K_mismatch` | — | `|Δk|` and `|Δk|/|k|`; measured `5.6e-6 … 7.3e-6` absolute, `1.9e-5` relative |

## 11. `fig10_field_maps.csv` — 22801 rows

Computed in `fig10()`: 151 × 151 field map over `x, y` at the reference plane region.

| Column | Unit | Meaning |
|---|---|---|
| `x_um`, `y_um` | µm | map coordinates (plate at `x < 0`, edge at `x = 0`) |
| `incident_intensity` | normalised | `|u|²`-type intensity of the incident field, divided by the incident peak (peak `0.99923`) |
| `backward_intensity` | normalised | backward-channel intensity, same normalisation (peak `0.039355` at the `−2 µm` plane) |
| `total_intensity` | normalised | incident + backward + interference |

## 12. JSON records in `figure_data/`

| File | What it holds | Guarded by |
|---|---|---|
| `reference_constants.json` | frozen `K0, KB0, KY0, OMEGA0, HCRIT`, material values, literature bands, transport values | `test_reference_values_are_frozen`, `test_material_constants_are_physical` |
| `build_log.json` | the parameters each build used (degree, `nquad`, `H_crit_T`, …) | informational |
| `figure_panel_sources.json` | figure → data source → panel descriptions → columns → artifact `sha256`/bytes | `test_panel_map_agrees_with_the_plotting_code` |
| `peak_certification.json` | refinement ladder at four fixed wavenumbers (`operating_point`, `refined_peak`, `round7_sample`, `k055_sample`) with `R_B_finest`, angle, spread, certification | `test_stored_operating_point_matches_certification` |
| `peak_search.json` | coarse grid, plateau, refinement, classification `certified_local_maximum`, degree/quadrature/restart spreads, tracking paths | `test_reported_peak_matches_the_search_record` |
| `peak_identity_audit.json` | is the peak the backward branch or an artefact? (plane-independence, incident-vs-backward identity, edge-plane value `0.9824311`) | `test_incident_mode_is_not_the_backward_target`, `test_partition_is_independent_of_the_reference_plane` |
| `convergence_audit.json`, `quadrature_audit.json` | degree 14…34 and nodes 64…256 sweeps with spreads `1.10e-6` / `1.70e-9` | `test_degree_convergence`, `test_independent_C1_mesh_approaches_spectral_edge` |
| `modal_flux_audit.json` | rescaling invariance of the modal power: `R_B` before/after `0.019291601863`, relative difference `8.99e-15` | `test_modal_energy_flux_and_strong_residuals` |
| `mechanism_controls.json` | the matched controls (dispersion-only, coupling off/on, ±`H`, tenfold `f`) that decide whether the peak is a property of the branch or of the added term | `test_mechanism_controls_record_matches_the_shared_transform` |
| `corner_assessment.json` | corner line-force magnitudes at `n = 10, 28` for three configurations, exponent ≈ −0.63, partition shift `3.9e-6` | `test_corner_*`, `test_partition_insensitive_to_corner` |
| `gate1_*.json`, `round21_*.json` | Gate 1 natural-boundary identity (incident `5.7e-14…1.3e-12`, worst reflected `8.9e-9…3.5e-6`, plain traction `1.7e+1`) and Gate 2/3 corner and edge-default audits | `round21_tests.py` |
| `flexo_control.json` | effect of `f`: `−0.012 %` (1 nC/m), `−1.176 %` (10 nC/m) | `flexo_control.py` |
| `phase_speed_audit.json` | phase/energy-speed and EM-wavelength reconciliation (`k_EM d = 2.211005e-4` vs `2.2e-4`) | `phase_speed_audit.py` |
| `claim_audit.json` | the 10/10 source-agreement record linking `claims.json` to stored values | `claim_audit.py` |
| `fig10_field_metrics.json` | primary fluxes, angles, wavenumbers, `k_y` quadrature and centroid data for Fig. 10 | `test_figure_csvs_match_the_shared_transform` |
| `round19_baseline/` | the round-19 (grounded edge) records, kept so the round-20 correction can be audited | `regenerate_revised_data.py` reproduces them |
| `round21/` | the round-21 gate records | `round21_*` scripts |

## 13. `results_legacy/`

Outputs of rounds 4–12 (older SVGs, CSVs, JSONs).  **Historical only**; several numbers
in it are superseded (e.g. the pre-fix `v_p = 2800 m/s`, `λ_EM = 0.905 mm` quoted as
"evidence only" in `phase_speed_audit.json`).  Nothing in the manuscript or in
`claims.json` reads from this folder.  It is shipped so that a reader can see what
changed and when; `07_DOCUMENTATION/CHANGELOG.md` records the decisions.
