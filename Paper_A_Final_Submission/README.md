# Paper A — authoritative submission directory

**Negative reflection of guided waves at a free edge in a flexoelectric
piezoelectric–semiconductor plate: the strain-gradient backward branch**

This is the single authoritative manuscript tree for Paper A.  There is no
other `main.tex` in the repository; the earlier project is archived, explicitly
labelled as superseded, under `../archive/legacy_manuscript_2026-11-06/`.

---

## 1. Contents

```
main.tex                       article source (abstract, eight sections, appendix)
references.bib                 eleven entries, every one resolved against the text
sections/                      introduction, governing_equations, numerical_methods,
                               results, discussion, conclusions, appendix_reproducibility
figures/                       ten vector PDFs used by main.tex
scripts/static_check.py        source validation that needs no TeX engine
static_validation.txt          result of the last run: PASS
MANIFEST.json                  SHA-256 of every file in this directory

a0/materials.json              material constants and their provenance tags
paper_a_study/                 solver, figure drivers, verification scripts
paper_a_study/figure_data/     every CSV and JSON the figures are drawn from
validation/verification_log.txt  the last full check battery
```

## 2. Build

```bash
cd Paper_A_Final_Submission
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Standard TeX Live or MiKTeX is sufficient; the packages used are geometry,
fontenc, lmodern, amsmath, amssymb, mathtools, siunitx, graphicx, booktabs,
caption, subcaption, hyperref and cleveref, all standard.  `cleveref` is loaded
last, after `hyperref`, and siunitx is configured with `\sisetup` (valid in both
v2 and v3).

**Compilation status of this copy: not compiled.**  No TeX engine exists in the
authoring environment; the source was validated statically (balance, references,
citations, figure files, macros).  See
`../PAPER_A_FINAL_SCIENTIFIC_AUDIT.md`, section 11.

## 3. Reproduce the numbers and the figures

From the repository root (the package copy is identical to it):

```bash
python paper_a_study/run_all_checks.py            # full battery, ~20 s
python paper_a_study/build_figure_data.py         # CSV/JSON, ~6 min
python paper_a_study/generate_final_figures.py    # ten PDFs, ~20 s
```

Individual checks:

```bash
python -m unittest paper_a_study.test_model       # 20 scientific tests
python paper_a_study/verify_dimensions.py         # dimensional / constitutive audit
python paper_a_study/quasistatic_check.py         # electromagnetic + carrier ratios
python paper_a_study/flexo_control.py             # measured flexoelectric contribution
python paper_a_study/certify_peak.py              # degree refinement of the two values
python paper_a_study/reclassify_csv.py            # admissibility flags (no re-solving)
python paper_a_study/modal_flux_audit.py          # rescaling + degree proof of R_B
python paper_a_study/mechanism_controls.py        # matched controls (Table: controls)
python paper_a_study/corner_assessment.py         # corner-band energy diagnostic
python paper_a_study/phase_speed_audit.py         # phase-speed / e.m. reconciliation
python Paper_A_Final_Submission/scripts/static_check.py
```

## 4. Reference values

| Quantity | Value |
|---|---|
| `R_B` at the operating point, 2 µm plane | `0.023145624` |
| energy angle there | `-27.8997` deg |
| `R_B` at the peak (`k_x d = 0.55`) | `0.579180059` |
| energy-identity closure, `H = 0` | `3.4e-16` |
| power balance at the operating point | `7.3e-13` |
| peak refinement, degree 18 → 30 | `1.5e-7` relative |
| edge-system condition number | `1.86e2` |
| flexoelectric contribution to `R_B` | `-0.01 %` |
| `k_EM d` (retardation parameter) | `2.211e-4` |
| `d/λ_EM` | `3.519e-5` |
| phase speed `v_p` at the operating point | `28.046 km/s` |
| `R_B` with `H = 0` at the peak (branch-consistent baseline) | `0.579180` |
| corner-band gradient-energy share, operating point | `0.928 – 0.996 %` |
| corner-band gradient-energy share, peak | `1.180 – 1.264 %` |
| `R_B` at `H/H* = +0.05`, peak | `0.522107` (−9.85 %) |
| backward port with `ℓ = 0` | none (specular fallback) |
| carrier relaxation `ω τ_d` | `1.65e3` |

## 5. Notes

* The strain-gradient modulus has the units of a force (N), not of a stiffness;
  the hyperstress has units N/m.  The derivation and the table are in
  `sections/governing_equations.tex`.
* The electrochemical potential is energy-valued (J per carrier) with the
  electron sign, `mu = k_B T dn/n0 - q phi + H : eta`.
* The flexoelectric sector is present but subdominant: `f_3zz = 1 nC/m`,
  contribution `-0.01 %`.  The paper does not claim a calibrated flexoelectric
  mechanism.
* `paper_a_study/figure_data/fig08_boundary_sensitivity.csv` is retained from a
  withdrawn panel and is not read by any figure.
* No `.npy`/`.npz` files are shipped or required.
