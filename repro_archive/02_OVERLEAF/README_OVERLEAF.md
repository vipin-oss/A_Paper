# README_OVERLEAF

The manuscript source, complete and self-contained.  This folder is what you upload to
Overleaf (or compile locally).  It needs **no class file, no bibliography style file and
no external figure**: everything referenced is inside this folder.

```
02_OVERLEAF/
  main.tex                 \documentclass[10pt,a4paper]{article} + preamble + 8 \input
  sections/                introduction, governing_equations, numerical_methods,
                           results, discussion, conclusions,
                           appendix_derivations, appendix_reproducibility
  figures/                 fig01_dispersion.pdf … fig10_field.pdf   (10 PDFs, 396 KB)
  references.bib           13 entries, all cited
  scripts/static_check.py  the validator described in §5 (runs without TeX)
```

---

## 1. How to compile

```bash
pdflatex main
bibtex   main
pdflatex main
pdflatex main          # second pass resolves cleveref/siunitx cross-references
```

Overleaf: upload the contents of this folder as a project, set `main.tex` as the main
document, compiler **pdfLaTeX** (not XeLaTeX/LuaLaTeX), and click Recompile.  The
sequence above is what Overleaf's default pdfLaTeX + BibTeX run performs; it is written
out because `cleveref` needs the second pass to resolve cross-references.

**Expected output:** a PDF with no undefined references and no undefined citations.
There is **no expected-error list to ignore**; if the build reports an undefined
citation or reference, something in this folder was modified.

## 2. Packages required (all standard in TeX Live `latex-extra` / Overleaf's full scheme)

`geometry`, `fontenc`, `lmodern`, `amsmath`, `amssymb`, `mathtools`, `siunitx`,
`graphicx`, `booktabs`, `tabularx`, `caption`, `subcaption`, `hyperref`, `cleveref`.

`siunitx` is used in both v2 and v3 form: the preamble sets options through
`\sisetup` only (the previous source used `\siunitxsetup`, which exists only in v3 and
aborted a v2 build).  No `\SI` option that is v3-only is used.

Deliberately **not** required: no `.cls`, no `.bst` (the build uses `plain`, shipped with
every TeX distribution), no shell-escape, no external data file read by `pgfplots`
(all figures are finished PDFs), no internet access.

## 3. Paths — verified, not assumed

Every one of the following was checked file-by-file against this folder
(`static_check.py`, run on 2026-11-07, exit 0):

| Kind | Count | Detail |
|---|---|---|
| `\input{sections/…}` | 8 | `introduction`, `governing_equations`, `numerical_methods`, `results`, `discussion`, `conclusions`, `appendix_derivations`, `appendix_reproducibility` — all present, all `\input` (no `\include`, so no `.aux` splitting) |
| `\includegraphics{figures/…}` | 10 | `fig01_dispersion`, `fig02_material`, `fig03_geometry`, `fig04_frequency`, `fig05_channel`, `fig06_attenuation`, `fig07_coupling`, `fig08_boundary`, `fig09_validation`, `fig10_field` — every file present as `.pdf`, extension omitted in source as usual |
| `\bibliography{references}` | 1 | `references.bib` present, **13 entries**, all 13 cited in the text |
| `\bibliographystyle{plain}` | 1 | `plain.bst` is part of the TeX distribution; nothing to ship |
| `\label` / `\ref` / `\cref` | 173 labels, 111 reference sites | zero undefined, zero duplicated.  `static_check.py` additionally *lists* labels that are defined but never referenced (e.g. `sec:results_attenuation`, `eq:RB_worked`); these are informational notes, not errors |
| `\cite` keys | 13 distinct | all resolve; zero missing, zero unused |

To re-run that verification without a TeX engine:

```bash
python scripts/static_check.py     # exit 0 = PASS; prints the counts above
```

## 4. What was NOT done (stated, not hidden)

**This manuscript has never been compiled in the authoring environment.**  No
`pdflatex`, `latexmk`, `xelatex`, `lualatex` or `tectonic` was available there (`tectonic`
is also absent from PyPI, and the `texlive` package was not installable).  Consequently:

* no `main.pdf` exists anywhere in this archive — none is claimed;
* the validation performed is **static**: balanced environments, resolved references,
  resolved citations, present figure files, no undefined macros, no duplicate labels;
* the **typeset layout is unverified** (page breaks, float placement, overfull boxes are
  not observable without a build);
* nothing in the science was changed to make a build "work", because no build was run —
  the preamble repairs that *are* present (`\sisetup` instead of `\siunitxsetup`;
  `\vect` as an alias instead of a redefinition of `\boldsymbol`) fix genuine hard
  errors in the previous source and are documented in
  `07_DOCUMENTATION/CHANGELOG.md`.

If your first compile on a full TeX Live produces a warning about an overfull hbox or a
float moved to a later page, that is the unverified-layout risk above, not a scientific
discrepancy.

## 5. Consistency between the paper and the code

* Every number quoted in the paper is stored in `03_DATA/figure_data/*.json` and
  registered in `01_PROGRAM/paper_a_study/claims.json` (40 live claims, 6 deprecated).
  `claim_audit.py` cross-checks manuscript ↔ registry ↔ stored data and fails on any
  mismatch (last run: 10/10 source-agreement, PASS).
* The figures in `figures/` are byte-identical to
  `08_FINAL_OUTPUTS/figures_final/*.pdf`; their SHA-256 values are in
  `09_ARCHIVE_METADATA/file_manifest_sha256.csv` and in
  `03_DATA/figure_data/figure_panel_sources.json`.
* The manuscript's reproducibility appendix (`sections/appendix_reproducibility.tex`)
  names the scripts and the run order; it agrees with
  `04_REPRODUCTION/RUN_ORDER.md`.

## 6. Editing rules if you must touch the source

1. Do not change a number in the text without changing it in `claims.json` — the audit
   is a guard, not a formality.
2. Keep `R_B` described as a **modal share**; calling it a reflectance is a scientific
   error and a test failure.
3. Keep the three limitations and the case-C restriction in place; they are the
   manuscript's honesty budget and are checked for presence.
4. Re-run `python scripts/static_check.py` after any structural edit.
