# Paper A — Round 11: claim registry correction

The registry (`paper_a_study/claims.json`) is the contract between the manuscript
and the stored solver records. Round 10 registered 22 claims but treated all of
them as *values with a tolerance*, which forced the two refinement spreads (which
are differences of nearly equal numbers lying on the round-off floor) into a
1 %-equality test. On freshly generated data that test fired on float noise while
the headline moved by $8\times10^{-13}$ — the single FAIL of the round-10 battery
(defect **D9**).

Round 11 splits the registry into five categories, changes the gate to respect the
category, and adds one claim that the manuscript quoted but the registry did not
track (**D11**).

---

## Category A — headline values

Point values of the solution, compared with a tolerance that is set by the
*rounding of the printed literal*, never by the solver's noise.

| claim | value | printed as | tolerance | source |
|---|---|---|---|---|
| `R_B_operating_point` | 0.0231456 | 2.31 % / 0.023\,146 | 0.5 % | `peak_certification.json` |
| `R_B_certified_maximum` | 0.946795 | 94.68 % / 0.946\,795 | 0.2 % | `peak_search.json` classification |
| `R_B_at_located_argmax` | 0.946795 | 0.9467952 / 0.9467954 | 0.2 % | `peak_search.json` |
| `R_B_earlier_sample` | 0.931891 | 0.931\,891 | 0.2 % | `peak_search.json` |
| `R_B_k055_sample` | 0.579180 | 0.579\,180 | 0.2 % | `mechanism_controls.json` |
| `R_B_edge_certified_maximum` | 0.9856 | 0.9856 / 98.5572 % | 0.5 % | `peak_search.json` (degree-22 edge row, cross-checked against `mechanism_controls.json` to $10^{-6}$) |
| `R_B_edge_operating_point` | 0.0232 | 0.0232 | 0.5 % | `mechanism_controls.json` |
| `R_B_edge_k055` | 0.5802 | 0.5802 | 0.5 % | `mechanism_controls.json` |
| `total_outgoing_peak` | 0.99769 | 99.77 % / 0.99769 | 0.2 % | `peak_search.json` |
| `total_outgoing_operating` | 0.99980 | 0.99980 | 0.2 % | `mechanism_controls.json` |
| `wavenumber_ratio_peak` | 0.996 | 0.9960 / 0.996 | 0.2 % | `peak_search.json` |
| `incident_wavenumber_peak` | 0.5282 | 0.5282 | 0.2 % | `peak_identity_audit.json` (must be the *incident* root, not $k_B=0.24517$) |
| `incident_power_ratio_fold` | 128 | 128 / $1.28\times10^{2}$ | 2 % | `peak_identity_audit.json` |
| `coupling_frequency_shift_max` **(new)** | 183.7115 kHz | \SI{184}{\kilo\hertz} | 0.2 % | `fig01_dispersion_velocity_attenuation.csv`, recomputed by the gate |

The new claim exists because §4.1 quoted a frequency shift the registry did not
track, and the quoted number was wrong by a factor of three.

## Category B — convergence bounds (inequality, not equality)

| claim | bound | meaning | source |
|---|---|---|---|
| `degree_stability_peak` | $\le10^{-8}$ | relative spread of the maximum over Galerkin degrees 14…34, at both the located argmax and the reported wavenumber | `peak_search.json` `verdict.degree_spread[*]` |
| `quadrature_stability_peak` | $\le10^{-8}$ | relative spread of the maximum over the quadrature rules 64…256 nodes **at fixed degree 22** | `peak_search.json` `verdict.quadrature_spread` |

Gate semantics: `kind = "bound"` makes the check an inequality — every entry the
record contains must be $\le$ the bound and $>0$ (a zero would mean the metric was
never computed). The manuscript quotes "below $10^{-8}$" in §4.6, §4.8 and
conclusions; it no longer quotes $5.0\times10^{-9}$ or $5.6\times10^{-9}$, which
were two significant figures of a quantity whose leading digit moves between runs.

This is not a loosened tolerance: it is a *stated, verified* bound. The measured
values stay three orders of magnitude below it, and the gate still fails if a
genuinely unconverged spread ($10^{-5}$, or any value above the bound) appears —
that is mutation **M13**.

## Category C — residuals, compared as absolute magnitudes

| claim | value | what it is | tolerance |
|---|---|---|---|
| `reference_plane_closure` | $2\times10^{-16}$ | composition of two plane transformations must return the input; the residual is compared absolutely, not relatively, because a relative test on a number that is zero to machine precision is meaningless | half an order of magnitude |
| (same treatment) `power_balance_error`, `edge_scaled_residual` | $10^{-15}$…$10^{-12}$ | reported in fig05(c) and fig09(c) as floors, with the floor printed in the panel | — |

## Category D — percentages derived from a stored source

| claim | value | derivation |
|---|---|---|
| `coupling_change_operating` | $-1.21\%$ | $[R_B(H/H^*=+0.05)-R_B(0)]/R_B(0)$ at the operating point, reference plane |
| `coupling_change_peak` | $-34.2\%$ | the same at the certified maximum |
| `coupling_change_peak_edge_plane` | $+11.1\%$ | the same after the edge-plane transform |
| `coupling_change_k055_edge_plane` | $+2.007\%$ | the same at $k_xd=0.55$ |
| `coupling_change_k055_reference_plane` | $-9.85\%$ | the same at $k_xd=0.55$, reference plane |
| `attenuation_peak_backward` | $87.1$ dB/mm | $\alpha_B$ at the certified maximum |

Each is recomputed from the same record that produces the two endpoint values, so
a change in either endpoint propagates into the percentage; the tolerances
(2–5 %) allow the rounding of the printed percentage but nothing more.

## Category E — exact constants

Material and geometric constants ($c_{44}$, $e_{14}$, $\varepsilon$, $n_0$, $\mu$,
$d=200$ nm, $\ell=50$ nm, $\rho$) are not registered here: they live in
`paper_a_study/reference_constants.json` and are frozen by
`TestFrozenReferenceConstants` (mutation **M5** puts $c_{44}$ in Pa instead of GPa
and is caught). They are exact inputs, not derived claims, and a percentage
tolerance on them would be wrong.

## Deprecated values (must never reappear)

| value | why |
|---|---|
| `0.99985` | the old total outgoing fraction before the corner/evanescent bookkeeping was corrected |
| `28.06` | attenuation at a superseded plane |
| `93.19` | the coarse-grid maximum at $k_xd=0.525$, superseded by the certified $94.6795$ |
| `33.1` | the old coupling change at the peak (now $34.2$) |
| `110 rows` | the old figure-data row count, a property of the data never quoted in the text |

## What the gate now checks

1. every registered literal is present in the named file (46 tokens, 5 deprecated
   strings guarded in all 9 tex files);
2. the number each literal denotes agrees with the registry within its category
   tolerance;
3. headline claims are additionally compared with the stored records
   (`peak_search.json`, `peak_certification.json`, `peak_identity_audit.json`,
   `mechanism_controls.json`, the fig01 CSV) — 11 source-agreement rows;
4. figures are first cited in the order 1…10;
5. every claim flagged `in_abstract` is present in the abstract.

Round-11 result on freshly regenerated data: **23 claims, 46 tokens, 11 of 11
source rows passing, PASS** — with no stored record restored (see
`PAPER_A_ROUND11_MUTATION_AND_REGRESSION_RESULTS.md` for the mutant that proves the
bound can still fail).
