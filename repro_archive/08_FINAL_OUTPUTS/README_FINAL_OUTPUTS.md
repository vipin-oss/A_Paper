# README_FINAL_OUTPUTS

The finished artifacts: the ten figures in three formats, the manuscript's figure copies,
the machine-readable results table, and the manifest that came with the submission
package.  The manuscript **source** lives in `02_OVERLEAF/`; this folder holds outputs,
not a second copy of `main.tex`.

```
08_FINAL_OUTPUTS/
  figures_final/          fig01…fig10 in pdf, png, svg   (SVG of fig10 excluded: 29 MB)
  FINAL_RESULTS_TABLE.csv every headline number, with the exact JSON key it came from
  make_results_table.py   regenerates that CSV from the stored records (no hand typing)
  MANIFEST.json           the submission package manifest (88 files, sha256 per file)
  static_validation.txt   the last static LaTeX validation output
  PAPER_A_FINAL_SCIENTIFIC_AUDIT.md   the scientific audit of the shipped state
```

---

## 1. The figures

| File stem | Manuscript figure | Panels | pdf bytes |
|---|---|---|---|
| `fig01_dispersion` | Fig. 1 — dispersion, phase/group/energy speed, linewidth, attenuation | 4 | 39,540 |
| `fig02_material` | Fig. 2 — doping and mobility sweep | 4 | 38,976 |
| `fig03_geometry` | Fig. 3 — thickness and gradient length | 4 | 37,074 |
| `fig04_frequency` | Fig. 4 — frequency sweep of `R_B`, angle, wavenumber ratio, group speed | 4 | 39,532 |
| `fig05_channel` | Fig. 5 — the power partition (the figure that makes `R_B` a share, not a reflectance) | 4 | 34,588 |
| `fig06_attenuation` | Fig. 6 — return against distance; per-channel attenuation | 4 | 33,797 |
| `fig07_coupling` | Fig. 7 — `k_y` detuning sensitivity | 4 | 35,714 |
| `fig08_boundary` | Fig. 8 — through-thickness flux profiles | 4 | 39,257 |
| `fig09_validation` | Fig. 9 — convergence, residuals, temporal-vs-spatial consistency | 4 | 33,815 |
| `fig10_field` | Fig. 10 — incident/backward field maps, metrics, flux vector plot | 4 | 48,618 |

The `pdf` files here are byte-identical to `02_OVERLEAF/figures/*.pdf` (they are the same
files as delivered); both sets' SHA-256 values appear in
`09_ARCHIVE_METADATA/file_manifest_sha256.csv`.  `png` is for inspection, `svg` for
editing.

**Size note:** `fig10_field.svg` is ~29 MB (a dense vector map) and is excluded from the
archive.  `generate_final_figures.py` recreates it in ~10 s; nothing in the manuscript
uses it.

## 2. `FINAL_RESULTS_TABLE.csv`

25 rows, each with `quantity, value, unit, source_file, source_key, note`.  Every value is
read from a JSON record by `make_results_table.py` — nothing is transcribed — so the table
cannot drift from the data.  It includes:

* the certified maximum `R_B = 0.942871839272569` at `k_x d = 0.52719`, flat top
  `[0.5267, 0.5276]`, classification `certified_local_maximum`;
* the operating point `R_B = 0.019291537`, angle `−27.90°`;
* the off-peak sample `k_x d = 0.55 → 0.551909484`;
* the refinement spreads (`1.10e-6`, `1.70e-9`, `3.24e-6`);
* the degree and quadrature audit verdicts (`8.84e-6` vs tol `1e-5`; `7.77e-9` vs `1e-7`);
* the flux components at the reference plane and the reflected angle from Fig. 10;
* the matched-control `R_B` of every mechanism variant;
* the corner line force at `n = 10` and `n = 28` for the three configurations, and the
  Gate 1 identity residuals (`id_incident`, `id_plain_worst`).

Regenerate with:

```bash
python 08_FINAL_OUTPUTS/make_results_table.py
```

## 3. `MANIFEST.json`

The manifest of the submission package (88 files, SHA-256 per file, sizes, and the source
path each was copied from).  It is the audit trail for "what was submitted"; the archive's
own integrity manifest is `09_ARCHIVE_METADATA/file_manifest_sha256.csv` plus
`SHA256SUMS.txt` at the archive root.

## 4. What is *not* here, and why

| Missing | Why |
|---|---|
| `main.pdf` | never compiled — no TeX engine existed. Not claimed anywhere. |
| a second copy of the manuscript source | `02_OVERLEAF/` is the single source of record; duplicating it would create the version-conflict risk the archive is meant to avoid |
| `fig10_field.svg` | 29 MB, regenerable, unused by the manuscript |
| the round-21 delivery zip | superseded by this archive; shipping both would be two "final" packages |

## 5. How to check this folder is coherent

```bash
python 04_REPRODUCTION/compare_outputs.py     # data vs shipped data
sha256sum -c ../SHA256SUMS.txt                # integrity of every file (POSIX)
```
