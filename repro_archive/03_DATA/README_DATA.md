# README_DATA

Everything the figures, the tables and the claims are made of.  No number in the
manuscript exists only in the manuscript: each one is stored here and cross-checked by
`01_PROGRAM/paper_a_study/claim_audit.py`.

```
03_DATA/
  figure_data/            ← the data of record (16 CSVs + ~20 JSON audit records)
    *.csv                 one file per figure (plus fig09 split into two)
    *.json                audits, certifications, frozen constants, claim-adjacent records
    round19_baseline/     the round-19 baseline records (grounded edge), kept for comparison
    round21/              the round-21 gate records
    figure_panel_sources.json   figure → data source → panels → columns → artifact sha256
    build_log.json        the parameters each build actually used
  results_legacy/         older CSV/JSON/SVG outputs of rounds 4–12 (historical, labelled)
  DATA_DICTIONARY.md      every column of every CSV: unit, meaning, provenance
```

---

## 1. What is data of record, and what is not

| Status | What | Why it is here |
|---|---|---|
| **Data of record** | `figure_data/*.csv`, `figure_data/*.json` | regenerate from `build_figure_data.py` / the audits; the figures and the manuscript read them |
| **Frozen constants** | `01_PROGRAM/paper_a_study/reference_constants.json` | `K0`, `KB0`, `KY0`, `OMEGA0`, `HCRIT`, the material values and their literature bands; guarded by `test_reference_values_are_frozen` |
| **Audit records** | `figure_data/peak_search.json`, `peak_certification.json`, `convergence_audit.json`, `quadrature_audit.json`, `modal_flux_audit.json`, `mechanism_controls.json`, `corner_assessment.json`, `gate1_*.json`, `round21_*`, … | the evidence behind every tolerance and verdict in the paper |
| **Historical** | `results_legacy/`, `figure_data/round19_baseline/` | superseded by the round-20/21 corrections; shipped so the corrections can be audited, **not** to be quoted as current |

If a value here disagrees with the manuscript, the audit fails.  If a value here
disagrees with an older report in `06_VALIDATION/reports/`, the newer record here wins
and the report's date tells you which round it belonged to.

## 2. How the data are produced

```bash
cd 01_PROGRAM/paper_a_study
python build_figure_data.py        # ≈ 8 min → figure_data/*.csv, *.json
```

Each row is computed by `model.Plate` at the stated settings; nothing is transcribed
from an earlier CSV, interpolated from a plot, or copied from a table in a paper.
The audits are separate programs (`certify_peak.py`, `peak_search.py`,
`convergence_audit.py`, `quadrature_audit.py`, `modal_flux_audit.py`,
`mechanism_controls.py`, `corner_assessment.py`, `round21_*.py`) run by
`run_all_checks.py`.

## 3. Conventions that hold in every file

* **Coordinates.** The plate occupies `x < 0`, the edge is at `x = 0`, `z ∈ [−d/2, d/2]`,
  `y` is unbounded.  The incident wave has `Re k_x > 0` (travelling towards the edge)
  and `Im k_x > 0` (decaying in `+x`, i.e. growing towards the edge).  Lengths in
  micrometres are suffixed `_um`; normalised lengths are in units of `d`.
* **Normalised vs SI.** `K`, `ky`, `K_incident_*`, `K_backward_*`, `K_spatial_*` are
  multiplied by `d` (dimensionless).  Columns with an SI suffix (`_m_s`, `_dB_per_mm`,
  `_GHz`, `_MHz`, `_mm`, `_um`, `_SI`) are physical.
* **`eta`** is the coupling level `H/H*` with `H* = 4.0097064373759543e-22 J·m`
  (`HCRIT`); `eta = 0` means the added carrier–gradient term is switched off, which is
  the matched control, not a separate model.
* **Sign of the carrier.** The electron charge is `−q`, so `Δn > 0` is an excess of
  electrons and the electrostatic term in `μ̃` is `−qφ`.
* **Power.** `P_x` is the thickness-integrated axial power flux per unit `y`-length in
  normalised units; it is **negative** for a mode carrying energy in `−x` (away from the
  edge).  A backward-channel share is therefore `−P_B/P_inc > 0` after the reference-
  plane factors.
* **`R_B`** is the backward **modal share**, never a total reflectance.  The total
  propagating share is `propagating_total_fraction` in `fig05_channel_power.csv`.
* **Precision.** All CSVs are written with 12 significant digits
  (`repr`-level `float`), all JSON with full double precision.  Reducing the digits is
  safe for reading but will fail byte-level reproduction checks.

## 4. Regeneration and verification

| Step | Command | Expected |
|---|---|---|
| regenerate data | `python build_figure_data.py` | 16 CSVs + JSONs rewritten, same values |
| regenerate figures | `python generate_final_figures.py` | 10 figures × 3 formats |
| check the data against the manuscript | `python run_all_checks.py` (check 5 + check 16) | `figure data and figure files` PASS, `claim registry` PASS |
| check figure→data map | `pytest test_model.py -k panel` | PASS (4-panel map complete, columns present) |

A byte-level comparison of a fresh regeneration against the shipped files is recorded
in `04_REPRODUCTION/REPRODUCTION_TEST_RESULT.md`.

## 5. What is deliberately absent

* No raw experimental data: **there is none** — the paper is a calculation, and it says
  so.
* No vendor/measured material files: the material constants are literature values,
  stored in `01_PROGRAM/a0/materials.json` with a DOI; the non-sourced ones are marked
  `NOT_SOURCED` there and in `09_ARCHIVE_METADATA/parameter_manifest.json`.
* No 29 MB intermediate SVG field maps (regenerable in ~10 s; see
  `07_DOCUMENTATION/FIGURE_PROVENANCE.md` §4).
* No private or third-party material: `a0s/private_sources/` (git-ignored in the
  repository) is **not** shipped anywhere in this archive.
