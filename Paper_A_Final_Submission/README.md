# Paper A — authoritative submission directory

**Backward-branch negative reflection of guided waves at a free edge in a
flexoelectric piezoelectric–semiconductor plate**

This is the single authoritative manuscript tree for Paper A.  There is no
other `main.tex` in the repository; the earlier project is archived, explicitly
labelled as superseded, under `../archive/legacy_manuscript_2026-11-06/`.

---

## 1. Contents

```
main.tex                       article source (abstract, six sections, appendix)
references.bib                 thirteen entries, every one cited and resolved
sections/                      introduction, governing_equations, numerical_methods,
                               results, discussion, conclusions, appendix_reproducibility
figures/                       ten vector PDFs used by main.tex, in first-citation order
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

**Build status: UNVERIFIED.**  No TeX engine exists in the authoring
environment, so no PDF has been produced from this revision.  The source was
validated statically instead (environment balance, 100 labels resolved, 61
references, 13/13 citations resolved, no undefined macro, no fragile command in a
moving argument) by `scripts/static_check.py`; the result is stored in
`static_validation.txt`.  The round-6 reviewer build (30 pages) predates this
revision and must not be quoted as evidence for it.  See
`../PAPER_A_FINAL_SUBMISSION_READINESS.md`, category 9.

## 3. Reproduce the numbers and the figures

From the repository root (the package copy is identical to it):

```bash
python paper_a_study/run_all_checks.py            # full battery, fifteen checks, ~70 s
python paper_a_study/build_figure_data.py         # CSV/JSON, ~6 min
python paper_a_study/generate_final_figures.py    # ten PDFs, ~20 s
```

Individual checks:

```bash
python -m unittest paper_a_study.test_model       # 22 scientific tests
python paper_a_study/verify_dimensions.py         # dimensional / constitutive audit
python paper_a_study/quasistatic_check.py         # electromagnetic + carrier ratios
python paper_a_study/flexo_control.py             # measured flexoelectric contribution
python paper_a_study/certify_peak.py              # degree refinement of the two values
python paper_a_study/reclassify_csv.py            # admissibility flags (no re-solving)
python paper_a_study/modal_flux_audit.py          # rescaling + degree proof of R_B
python paper_a_study/mechanism_controls.py        # matched controls (Table: controls)
python paper_a_study/corner_assessment.py         # corner-band energy diagnostic
python paper_a_study/phase_speed_audit.py         # phase-speed / e.m. reconciliation
python paper_a_study/convergence_audit.py         # degree convergence, no fitted rate
python paper_a_study/quadrature_audit.py          # quadrature sufficiency
python paper_a_study/claim_audit.py               # manuscript vs claim registry
python paper_a_study/mutation_tests.py            # five deliberate defects, scratch copies
python Paper_A_Final_Submission/scripts/static_check.py
```

## 4. Reference values

| Quantity | Value |
|---|---|
| `R_B` at the operating point, 2 µm plane | `0.023145624` |
| energy angle there | `-27.8997` deg |
| `R_B` at the branch maximum (`k_x d = 0.525`) | `0.931891` (93.19 %) |
| `R_B` at `k_x d = 0.55` (certified, 57.92 %) | `0.579180` |
| energy-identity closure, `H = 0` | `3.4e-16` (rounded partition closes to `1.4e-6`) |
| power balance at the operating point | `7.3e-13` |
| refinement, degree 18 → 30: operating point / branch maximum | `7.2e-7` / `2.1e-8` relative |
| quadrature change, 64 → 256 nodes | `6.9e-9` relative |
| edge-system condition number | `1.86e2` |
| flexoelectric contribution to `R_B` (operating point) | `-0.01 %` |
| `k_EM d` (retardation parameter) | `2.211e-4` |
| `d/λ_EM` | `3.519e-5` |
| phase speed `v_p` at the operating point | `28.046 km/s` |
| `R_B` with `H = 0` at the branch maximum (branch-consistent baseline) | `0.931891` |
| corner-band gradient-energy share, operating point | `0.928 – 0.996 %` |
| corner-band gradient-energy share, `k_x d = 0.55` | `1.180 – 1.264 %` |
| `R_B` at `H/H* = +0.05`, branch maximum | `0.623427` (−33.10 %) |
| `R_B` at `H/H* = +0.05`, `k_x d = 0.55` | `0.522107` (−9.85 %) |
| group velocity at the branch maximum | `-3 m/s` |
| backward port with `ℓ = 0` | none (specular fallback) |
| carrier relaxation `ω τ_d` | `1.65e3` |

## 5. Round-7 reports

Six reports at the repository root (also inside this archive) document the
round-7 audit and the corrections applied: `PAPER_A_STAGE1_COMPLETE_Q1_AUDIT.md`
(43 findings with evidence), `PAPER_A_ROUND7_NOVELTY_AND_MECHANISM_REPORT.md`,
`PAPER_A_EXTENDED_NUMERICAL_VALIDATION.md`,
`PAPER_A_CORRECTION_HISTORY.md`, `PAPER_A_CLAIM_PROVENANCE_MATRIX.md` and
`PAPER_A_FINAL_SUBMISSION_READINESS.md` (ten-category verdict: **MAJOR
REVISION**, novelty unresolved, build unverified).

## 6. Notes

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
