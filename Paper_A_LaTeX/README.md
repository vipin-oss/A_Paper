# Paper A LaTeX project

This directory contains a modular LaTeX package for the 10 reproducible figures of the Paper A grounded ZnO plate study.

## Layout

- `main.tex` — document entry point.
- `references.bib` — citations used by the text.
- `sections/` — introduction, governing equations, numerical methods, supported results, discussion and conclusions.
- `figures/` — publication-quality PDF/PNG outputs.
- `scripts/` — copy of `generate_final_figures.py`, `figure_style.py` and `model.py`.
- `figure_data/` — CSV, JSON and NPY source arrays.

## Reproduce

```bash
OPENBLAS_NUM_THREADS=1 python -m paper_a_study.generate_final_figures
```

The historical production study remains available via:

```bash
OPENBLAS_NUM_THREADS=1 python -m paper_a_study.run_study
```

## Compile

No LaTeX engine is installed in this sandbox. The source is complete and compilable with a TeX Live / MiKTeX installation containing `amsmath`, `amssymb`, `mathtools`, `siunitx`, `subcaption`, `booktabs`, `hyperref` and `cleveref`. Run:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Provenance and limitations

- No new physical model, coupling mechanism or constitutive theory is introduced.
- Synthetic `A`, flexoelectric `f3333` and `H` values are not experimental calibrations.
- The primary accepted value remains the isolated backward-channel self-flux at 2 µm in the specified grounded 2-D plane-strain model.
- Novel over Qu et al. is not claimed.
- The original four historical figures are retained separately in `paper_a_study/`.
