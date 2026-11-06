# Paper A — Round 6 final verification

**Branch** `arena/ea7ca4dd-a-paper` · **repository** `vipin-oss/A_Paper`
**Starting commit** `48029aa524a16165333678f7a59d5e0e9f4a695d` (round 5)
**Authoritative manuscript** `Paper_A_Final_Submission/main.tex`
**Date** 2026-11-06

This round fixes one confirmed LaTeX compilation defect, adds the static guard
that would have caught it, re-runs the full verification battery, rebuilds the
package, and states honestly what was and was not executed. No numerical result,
equation, figure or model was changed.

---

## 1. What was corrected

### 1.1 The defect

`\path` (hyperref/url) is **fragile**. A `\caption` argument is written to the
`.lof` file by `\protected@write`, which expands every token that is not
`\protect`-ed, so an unprotected `\path` in a caption aborts the build with

```
! Undefined control sequence.
\Url Error -> \url used in a moving argument.
l.69 ...fig01_dispersion_velocity_attenuation.csv
```

Round 5 introduced this defect when 50 long inline `\texttt{}` paths were
converted to `\path{}` to remove the overfull boxes reported by the round-4
audit. Fourteen of those conversions landed inside captions.

**Exact locations corrected** (all in
`Paper_A_Final_Submission/sections/results.tex`, `\protect\path{...}` applied):

| caption | line (after fix) | path |
|---|---|---|
| Fig. 1 | 69 | `fig01_dispersion_velocity_attenuation.csv` |
| Fig. 2 | 149 | `fig02_material_parameter_sweep.csv` |
| Fig. 3 | 184 | `fig03_geometry_sweep.csv` |
| Fig. 4 | 219 | `fig04_frequency_reflection.csv` |
| Table 2 (`tab:refinement`) | 234, 235 | `certify_peak.py`, `peak_certification.json` |
| Fig. 5 | 363 | `fig05_channel_power.csv` |
| Fig. 6 | 491 | `fig06_attenuation_distance.csv` |
| Fig. 7 | 528 | `fig07_coupling_sensitivity.csv` |
| Fig. 8 | 571 | `fig08_thickness_flux.csv` |
| Fig. 9 | 607, 608 | `fig09_validation_convergence.csv`, `fig09_temporal_spatial_consistency.csv` |
| Fig. 10 | 642 | `fig10_field_maps.csv`, `fig10_field_metrics.json` |

**Why `\protect` and not a wrapper macro.** The obvious alternative,
`\DeclareRobustCommand{\fpath}[1]{\path{#1}}`, is *not* safe here: `\path`
sets up character catcodes when it reads its argument, and an argument already
tokenised by an outer macro does not carry the catcodes `\path` expects. The
`\protect` form keeps `\path` reading its argument directly and only defers the
expansion inside the `\protected@write`; it is also the form the independent
reviewer verified. No `\url`, `\href` or `\nolinkurl` is used anywhere in the
manuscript (`grep` count 0), and no other fragile command appears in a caption
or a section title.

### 1.2 The guard

`Paper_A_Final_Submission/scripts/static_check.py` gained
`check_moving_arguments()`: it locates the balanced argument of every
`\caption`, `\section`, `\subsection`, `\subsubsection` and `\paragraph`, and
reports any `\path`/`\url`/`\href`/`\nolinkurl` there that is not preceded by
`\protect`. It runs inside `run_all_checks.py`, so the battery now fails on this
class of defect.

**The guard was mutation-tested, not merely written.** Removing a single
`\protect` from Fig. 1 and re-running the checker produced

```
FAIL
Problems:
  - sections/results.tex: line 69: fragile \path in a moving argument
    (\caption) - use \protect\path
```

and restoring the file returned `PASS`. The line number reported is the line of
the offending `\path`, not of the enclosing `\caption`.

### 1.3 Files changed in round 6

| file | change |
|---|---|
| `Paper_A_Final_Submission/sections/results.tex` | 14 × `\path` → `\protect\path` inside captions |
| `Paper_A_Final_Submission/scripts/static_check.py` | new moving-argument check; `protect` added to the macro whitelist |
| `Paper_A_Final_Submission/static_validation.txt` | regenerated |
| `PAPER_A_ROUND6_FINAL_VERIFICATION.md` | this report |
| `PAPER_A_FINAL_SCIENTIFIC_AUDIT.md` | round-6 addendum |
| `PACKAGE_README.md`, `downloads/README.md` | round-6 archive description and checksum |
| `Paper_A_Final_Submission/MANIFEST.json` | regenerated |
| `downloads/Paper_A_Complete_Project_round6.zip` | new archive |

No `.tex` content outside the fourteen caption commands was modified.

---

## 2. LaTeX build status and evidence

**Not compiled in this environment, and no claim to the contrary is made.**
There is still no TeX engine: `pdflatex`, `latexmk`, `tectonic`, `xelatex` and
`lualatex` are all absent, no package manager is available, and the network
path for a static binary is blocked. `run_all_checks.py` therefore prints
`[SKIP] LaTeX build: no TeX engine found`, exactly as before.

**Evidence that the source compiles, from the independent reviewer, not from
me:** the reviewer compiled this same tree with LaTeX + BibTeX after applying
precisely the `\protect\path` change, and reports a **30-page PDF**, complete
bibliography, resolved citations, **no overfull horizontal boxes**, all ten
figures present, and no manuscript-wide font reduction. Since my only
subsequent source changes are fourteen `\protect` insertions and a checker
script, that result carries over to this delivery — but it is the reviewer's
build, not mine, and it is described here as such.

Build command (unchanged):

```
cd Paper_A_Final_Submission
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

**Static presentation inspection performed here** (this is inspection, not
compilation):

| property | value |
|---|---|
| figures / `\includegraphics` | 10 / 10, all `width=0.95\textwidth` |
| tables | 9 (3 `tabularx`, 6 `tabular`) |
| float placement specifiers | `htbp`, `t`, `h` only |
| page geometry | `\usepackage[margin=22mm]{geometry}` |
| font-size switches | 0 × `\tiny`, 0 × `\scriptsize`; 1 × `\footnotesize` (path column of the reproduction table), 7 × `\small` (tables and captions) |
| labels / references | 100 / 149, all resolved by the static checker |
| citations | 11 used, 11 defined |
| fragile commands in moving arguments | 0 (checked) |

---

## 3. Numerical test results

Executed here, on this tree, with NumPy 2.4.6 / SciPy 1.17.1 / Matplotlib 3.11.2
on Python 3.11.2:

```
OVERALL: PASS
  unit and scientific tests (test_model) ................ PASS   20 tests, OK, 8.3 s
  dimensional and constitutive audit .................... PASS   25 identities
  quasistatic justification ............................. PASS
  flexoelectric control ................................. PASS
  admissibility re-derivation ........................... PASS   275 rows, 0 flips
  figure data and figure files .......................... PASS   10 PDFs
  phase-speed and e.m. reconciliation ................... PASS
  modal-flux rescaling proof ............................ PASS
  mechanism matched controls ............................ PASS
  corner assessment and regression ...................... PASS   cross-check PASS
  LaTeX static validation ............................... PASS
  LaTeX build ........................................... SKIP   no engine
```

**Test count: 20 passed, 0 failed, 0 skipped** in `test_model`; plus the nine
script-level checks above.

### Preserved values (re-read from the JSON on this tree, not retyped)

| quantity | value | source |
|---|---|---|
| operating-point incident wavenumber | `K0 = 0.736199` | `corner_assessment.json` |
| backward-mode wavenumber (distinct) | `KB0 = 0.245175` | `build_figure_data.py` |
| operating-point `R_B`, degree 30 | `0.023145624` (2.3146 %) | `peak_certification.json` |
| peak `R_B` (`k_xd = 0.55`), degree 30 | `0.579180059` (57.9180 %) | `peak_certification.json` |
| corner-band share, operating point | `0.9278 – 0.9961 %` | `corner_assessment.json` |
| corner-band share, peak | `1.1802 – 1.2643 %` | `corner_assessment.json` |
| certification cross-check | `PASS` (diff 0.0) | `corner_assessment.json` |

Unchanged and re-verified: phase speed 28.046 km/s, electromagnetic wavelength
5.6836 mm with `k_EM d = 2.211e-4` and `d/λ_EM = 3.519e-5`, modal-flux
normalisation and its 1.5e−15 rescaling invariance, the `H = 0` mechanism
controls with no backward port at `ℓ = 0`, the strain-gradient and
electrochemical-potential formulation, and the ten vector PDF figures
(byte-identical; no figure was regenerated in rounds 5 or 6).

---

## 4. ZIP verification

```
archive   downloads/Paper_A_Complete_Project_round6.zip
entries   163
integrity zipfile.testzip() -> None; unzip -t -> "No errors detected"
size      recorded in downloads/README.md and in the delivery message
sha256    recorded in downloads/README.md and in the delivery message
```

The exact size and SHA-256 are deliberately **not** written here: this report is
itself inside the archive, and a checksum cannot be embedded in the file it
describes without changing it. `downloads/README.md` (outside the archive) holds
the authoritative values, and the delivery message repeats them.

The round-6 archive is produced by `make_download_archive.py`, which stages
outside the repository, fixes the only generated timestamp, and therefore
normalises every staged mtime, so repeated builds are byte-identical (verified
by rebuilding after touching a source file). Its SHA-256 was verified
against the file committed to the branch, and the GitHub blob size and blob SHA
were compared with the local file to confirm that the served bytes are the
verified bytes.

Contents: `main.tex`, all seven section files, `references.bib` (11 verified
entries), the ten vector PDFs, `MANIFEST.json` (67 files, self-consistent),
`static_validation.txt`, the complete Python implementation and datasets,
`a0/ a0r/ a0s/`, `validation/verification_log.txt`, this report, the scientific
audit, the round-4 independent audit, and `START_HERE.txt`.

---

## 5. Remaining unresolved limitations

1. **No PDF built in this sandbox.** The 30-page build is the reviewer's. The
   repaired source is delivered; the build command is given above.
2. **The corner line force is not certified.** The corner-band diagnostic bounds
   the gradient energy near the corner and shows it does not accumulate under
   refinement; it does **not** bound the work a singular traction could do. The
   manuscript states the two facts separately and claims only the first.
3. **Novelty versus Qu et al., IJES 208 (2025) 104165 remains UNRESOLVED.** The
   comparison is equation-level against the free-energy decomposition reproduced
   in the open-access companion (Hu et al., IJMS 305 (2025) 110740); the primary
   article was not accessible. No priority claim is made.
4. **`ℓ`, `f` and `H` are synthetic.** No device-level ZnO prediction is made.
5. **The `ℓ = 0` control is a single-point statement** about this plate,
   frequency and `k_y`; its configurations follow a shifted branch frequency
   rather than being identical-frequency experiments.
6. **Page count is 30 in the reviewer's build**, not verified here; no page-level
   or line-break-level inspection of a PDF was possible in this environment.

---

## 6. Honest journal-readiness assessment

**Not ready for submission, and not claimed to be.**

What is now in good order: a single authoritative manuscript that compiles
(reviewer-verified) without layout defects; an exact energy identity closed to
1e−12; two reported partitions that are converged to 1e−7 and certified against
an independent refinement study; a mechanism that has been isolated with matched
controls and is no longer misattributed to the added coupling; a novelty
comparison that is explicit about what could and could not be inspected; and a
reproduction package whose scripts, exit statuses and datasets are consistent
with the text.

What still blocks a Q1 submission, in order of severity:

1. **Physical realism of the higher-order parameters.** `ℓ = 50 nm`,
   `f = 1 nC/m` and `H ≈ 0.05 H*` are modelling choices. The paper is honest
   about this, but a referee will ask what the numbers would be for a real ZnO
   film, and the present answer is "not measured".
2. **Novelty position.** The closest primary theory is inaccessible, so the
   contribution rests on the scattering formulation rather than on the added
   enthalpy. That is defensible but weaker than a priority claim, and it needs
   an editor's judgement, not another automated test.
3. **Elasticity scope.** The conclusion is a frequency-domain partition of a
   guided mode in an infinite plate with one edge — not a time-domain pulse
   measurement that an experiment could make directly.
4. **Corner certification.** A corner-eigenvalue analysis would close the last
   formal gap in the weak-form argument.

None of these is a defect that this round could repair by editing text or code;
they are scope and evidence limitations, and they are stated in the manuscript
where a referee will look for them.

---

## 7. What was executed here versus what was inherited

**Executed in this environment (round 6):** the caption repair; the mutation test
of the new static guard; the full `run_all_checks.py` battery (12 checks, 52 s);
`unittest paper_a_study.test_model` (20 tests); the static presentation
inventory above; package and archive rebuild; SHA-256 and blob verification.

**Inherited, not re-executed here:** the 30-page LaTeX/BibTeX build and the
no-overfull-box result (independent reviewer); `build_figure_data.py` and
`certify_peak.py` outputs (unchanged datasets, no demonstrated defect);
`generate_final_figures.py` (the ten PDFs are unchanged and shipped).

**Note on the environment.** This session began from a fresh checkout at the
base commit with no Python environment; the branch was restored from
`origin/arena/ea7ca4dd-a-paper` at `48029aa` and the interpreter environment was
rebuilt at the exact versions the appendix declares (Python 3.11.2, NumPy 2.4.6,
SciPy 1.17.1, Matplotlib 3.11.2) before any check was run. No source file was
altered by that recovery.
