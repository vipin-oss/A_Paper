# Paper A — focused plate-edge study

**Topic:** Negative Reflection in a Flexoelectric Piezoelectric-Semiconductor Plate.

**Sole added interaction:** `Δ𝓗 = Δn H_jkl ε_jk,l`.

## Start here

### [PAPER_A_RESEARCH_REPORT.md](PAPER_A_RESEARCH_REPORT.md)

One consolidated mathematical report contains the H-dependent equation/boundary changes, sourced ZnO inputs, dispersion, solved oblique edge conversion, four numerical figures, matched H effects, validation and limitations. This is the current simplified study, not another approval-gated phase.

### What was calculated

- A fully specified **static/local, grounded and carrier-blocking** plate with all elastic polarizations, nonzero **synthetic** static flexoelectricity, and reciprocal H coupling.
- At a common numerical drive of **16.684123136 GHz**, H = 0 gives a solved backward-channel self-flux return of **2.315%**, measured 2 μm from the edge. Its energy angle is **−27.90°**, with actual energy velocity pointing left and down. A computed angular-spectrum channel beam supports this direction; the result is not inferred from a backward slope alone.
- Matched synthetic H = ±2.0048532 × 10⁻²³ J m chiefly increases carrier loss. Same-plane return at 100 μm changes from **2.291%** at H = 0 to **1.469% / 1.067%**. H does **not** create the backward branch in this example.
- Separate temporal/spatial formulations, independent classical eight-state and nonzero-f/H full-thickness twelve-state propagators, degree refinement, a different C¹ cubic-Hermite discretization, and interference-inclusive power accounting are checked.

### What was not established

- **Published-baseline reproduction:** Wei (2026) is the closer structural reference, but complete Wei/Fang governing equations remain inaccessible. The explicitly specified calculation is **not attributed to them as a verified reproduction**.
- **Calibration/experimental feasibility:** A, f and H are synthetic; bulk Hall transport is transferred to a designed 200 nm plate; losses other than carrier dissipation and full Maxwell radiation are not modeled.
- **Coupling novelty:** Qu's relevant Appendix C remains inaccessible. Novelty is provisional, not claimed established.
- **Local corner-stress certification:** convergence is of the variational boundary functional and integrated channel coefficient, not pointwise corner stress. Most reflected power remains in other channels; this is not near-unity negative reflection of the complete field.

## Reproduce the focused study

Python 3.11, with pinned dependencies in [`a0/requirements.txt`](a0/requirements.txt). No server, external dataset or publisher full text is needed to run the independently specified model.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r a0/requirements.txt
OPENBLAS_NUM_THREADS=1 .venv/bin/python -m unittest paper_a_study.test_model -v
OPENBLAS_NUM_THREADS=1 .venv/bin/python -m paper_a_study.run_study
```

**Validation:** 143/143 focused numerical checks, 18/18 new tests, and 50/50 retained regression tests passed; all ten retained source/blueprint fingerprints match. The runner takes about 45 seconds here; the new tests about four seconds. `paper_a_study/cache/`, environments and large modal arrays are ignored. Code and small CSV/JSON/SVG evidence are retained.

### Implementation and evidence

- [`paper_a_study/model.py`](paper_a_study/model.py): temporal generator, canonical spatial state, full edge solve, physical power/residual reconstruction, independent strong propagators and C¹-mesh cross-check.
- [`paper_a_study/run_study.py`](paper_a_study/run_study.py), [`test_model.py`](paper_a_study/test_model.py).
- [`protocol.json`](paper_a_study/results/protocol.json), [`primary_edge.json`](paper_a_study/results/primary_edge.json), [`validation.json`](paper_a_study/results/validation.json), [`sha256.json`](paper_a_study/results/sha256.json).
- [`dispersion.csv`](paper_a_study/results/dispersion.csv), [`H_sensitivity.csv`](paper_a_study/results/H_sensitivity.csv), [`frequency_scan.csv`](paper_a_study/results/frequency_scan.csv), [`convergence.csv`](paper_a_study/results/convergence.csv), [`independent_roots.csv`](paper_a_study/results/independent_roots.csv).
- Figures: [dispersion/H](paper_a_study/results/dispersion_and_H.svg), [edge conversion](paper_a_study/results/edge_conversion.svg), [H sensitivity](paper_a_study/results/H_parameter_effect.svg), [computed channel beam](paper_a_study/results/computed_channel_beam.svg).

## Preserved historical records

The blueprint and A0/A0-R/A0-S reports/code/results are preserved. Their old STOP/no-edge/no-manuscript instructions applied to those completed tasks and **do not override the subsequently authorized simplified study**. Their open/vacuum and f = 0 numerical values are not results for the new grounded, nonzero-f model.

- [Blueprint V2.1](PAPER_A_BLUEPRINT_V2_1.md), unchanged.
- A0-S: [operating regime](PAPER_A_A0S_OPERATING_REGIME.md), [H sensitivity](PAPER_A_A0S_H_SENSITIVITY.md), [model selection](PAPER_A_A0S_MODEL_SELECTION.md). Historical numerical checks: 1,254 formal, 136 final-audit and 22 tests, all passed.
- A0-R: [novelty comparison](PAPER_A_A0R_NOVELTY_COMPARISON.md), [backward feasibility](PAPER_A_A0R_BACKWARD_WAVE_FEASIBILITY.md), [decision](PAPER_A_A0R_DECISION.md). Historical checks: 65 and 16 tests, passed.
- A0: [materials](PAPER_A_A0_MATERIALS.md), [prior art](PAPER_A_A0_PRIOR_ART.md), [constitutive check](PAPER_A_A0_CONSTITUTIVE_CHECK.md), [dispersion](PAPER_A_A0_DISPERSION_FEASIBILITY.md). Historical checks: 52 and 12 tests, passed.
- [Earlier source-access/transport ledger](a0s/SOURCES.md) and [earlier f = 0 strong-system derivation](a0s/STRONG_VALIDATION.md).

Optional retained regressions (the old 100-case screening programme is not needed for the focused result):

```bash
OPENBLAS_NUM_THREADS=1 .venv/bin/python -m unittest discover -s a0 -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 .venv/bin/python -m unittest discover -s a0r -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 .venv/bin/python -m unittest discover -s a0s -p 'test_*.py' -v
```

No supplied production solver was modified. Changes are saved on the Arena session branch; no commit or push is needed for preservation.
