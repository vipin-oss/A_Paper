# Paper A — claim provenance matrix (round 7)

Every number that the manuscript presents as a result is listed here with the
stored dataset it comes from, the file and the literal string that carries it,
and the gate that keeps the two in step. The registry is machine-readable
(`paper_a_study/claims.json`) and is enforced by `claim_audit.py`, which runs
inside `run_all_checks.py`; a mutation of any register
(`mutation_tests.py`, M2/M3) makes it fail.

Generated from the registry; do not edit by hand.

| Claim | Value | Source | Manuscript occurrences | Verification |
|---|---|---|---|---|
| `R_B_operating_point` | 0.0231456 | figure_data/peak_certification.json: rows[case=operating_point, degree=30].R_B | `main.tex`: `2.31`; `sections/results.tex`: `2.3146\times10^{-2}`; `sections/results.tex`: `0.023\,146`; `sections/conclusions.tex`: `2.31` | PASS (registry + string present) |
| `R_B_branch_maximum` | 0.931891 | figure_data/peak_certification.json: rows[case=peak_lower, degree=30].R_B | `main.tex`: `93.19`; `sections/results.tex`: `0.931\,891`; `sections/results.tex`: `0.9318915`; `sections/conclusions.tex`: `93.19` | PASS (registry + string present) |
| `R_B_at_k055` | 0.57918 | figure_data/peak_certification.json: rows[case=peak_candidate, degree=30].R_B | `sections/results.tex`: `0.579\,180`; `sections/results.tex`: `0.5791801` | PASS (registry + string present) |
| `total_outgoing_operating_point` | 0.999797 | figure_data/mechanism_controls.json: cases[operating_point][no_coupling].total_outgoing_propagating | `main.tex`: `99.98`; `sections/results.tex`: `0.99980`; `sections/discussion.tex`: `0.99980`; `sections/conclusions.tex`: `99.98` | PASS (registry + string present) |
| `total_outgoing_branch_maximum` | 0.989999 | figure_data/mechanism_controls.json: cases[branch_maximum][no_coupling].total_outgoing_propagating | `main.tex`: `99.0`; `sections/results.tex`: `0.99000`; `sections/discussion.tex`: `0.99000`; `sections/conclusions.tex`: `99.0` | PASS (registry + string present) |
| `H_effect_operating_point` | 0.0121 | figure_data/mechanism_controls.json: branch_consistent_H_sweep[operating_point][eta=+0.05] | `main.tex`: `1.21`; `sections/results.tex`: `1.21`; `sections/discussion.tex`: `1.21`; `sections/conclusions.tex`: `1.21` | PASS (registry + string present) |
| `H_effect_branch_maximum` | 0.331 | figure_data/mechanism_controls.json: branch_consistent_H_sweep[branch_maximum][eta=+0.05] | `main.tex`: `33.1`; `sections/results.tex`: `33.1`; `sections/discussion.tex`: `33.1`; `sections/conclusions.tex`: `33.1` | PASS (registry + string present) |
| `energy_identity_residual` | 3.4e-16 | figure_data/peak_certification.json: identity closure recorded in the validation log | `sections/results.tex`: `3.4\times10^{-16}`; `sections/conclusions.tex`: `3.4\times10^{-16}` | PASS (registry + string present) |
| `solver_power_balance` | 7.3e-13 | figure_data/mechanism_controls.json: cases[*][*].power_balance_relative | `sections/results.tex`: `7.3\times10^{-13}` | PASS (registry + string present) |
| `frequency_operating_point` | 16.684 | figure_data/peak_certification.json: rows[case=operating_point, degree=30].omega * fscale | `main.tex`: `16.68`; `sections/results.tex`: `16.68` | PASS (registry + string present) |
| `K0_operating_wavenumber` | 0.736199 | paper_a_study/build_figure_data.py: K0 | `sections/results.tex`: `0.7362`; `sections/numerical_methods.tex`: `0.7362` | PASS (registry + string present) |
| `KB0_backward_wavenumber` | 0.245175 | paper_a_study/build_figure_data.py: KB0 | `sections/numerical_methods.tex`: `0.2452` | PASS (registry + string present) |
| `corner_band_operating_point` | 0.009278 | figure_data/corner_assessment.json: operating_point corner_share_range | `sections/discussion.tex`: `0.93$--$1.00$` | PASS (registry + string present) |
| `corner_band_k055` | 0.011802 | figure_data/corner_assessment.json: peak corner_share_range | `sections/discussion.tex`: `1.18$--$1.26$` | PASS (registry + string present) |

## Gates behind the numbers

* **Degree convergence** — `figure_data/convergence_audit.json`, verdict
  `True` at tolerance 1e-06; largest
  change between degree 18 and 30 is
  7.21e-07.
* **Quadrature sufficiency** — `figure_data/quadrature_audit.json`, verdict
  `True` at tolerance 1e-07; worst
  change against the 256-node rule is
  6.94e-09.
* **Registry agreement** — `figure_data/claim_audit.json`, verdict
  `FAIL`, 35 tokens checked, figure first-citation order
  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].
* **Stale-value guard** — three deprecated strings must not reappear:
  0.99985 (mislabelled total outgoing power), 28.06 (reciprocal survival factor),
  and the phrase "the maximum along the branch is" (superseded by the certified
  branch maximum).

## Deliberate non-claims

The corner-band percentages (0.9278–0.9961 % and 1.1802–1.2643 %) are registered
only through their rounded wording in the text. They are diagnostics of the
strain-gradient energy near the corner and are **not** registered as evidence
about corner line forces, which the manuscript states are uncertified.
