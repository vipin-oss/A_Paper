# Downloadable project archive — round 5

`Paper_A_Complete_Project_round5.zip` — one-click download of the complete
Paper A project after the round-5 corrections.

* Size: **2 644 649 bytes** (2.64 MB)
* Files: **162**
* SHA-256: `b7a6478f7d3a0fc1dc62da558f701fc0f809c9467be5c5150f674624bbe3554f`
* Reproducible: two consecutive builds of the archive are byte-identical
  (`make_download_archive.py` fixes the only generated timestamp).

Direct link (GitHub answers with a redirect to the raw host):

```
https://github.com/vipin-oss/A_Paper/raw/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round5.zip
```

Mirror on a second host, in case the redirect target is blocked by a proxy:

```
https://media.githubusercontent.com/media/vipin-oss/A_Paper/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round5.zip
```

Contents:

* `PAPER_A_FINAL_SCIENTIFIC_AUDIT.md` — the audit report, including the round-5
  addendum (corner configuration fix, LaTeX layout repairs, appendix exit-status
  correction, preserved results, final verification, open items).
* `PAPER_A_ROUND4_INDEPENDENT_AUDIT.md` — the external audit that motivated the
  round-5 changes, included verbatim as evidence.
* `Paper_A_Final_Submission/` — authoritative manuscript (`main.tex`, seven
  section files, eleven verified bibliography entries, ten vector PDF figures,
  `static_validation.txt`, `MANIFEST.json`, README).
* `paper_a_study/` — solver, figure drivers, verification suite and the audit
  scripts `phase_speed_audit.py`, `modal_flux_audit.py`, `mechanism_controls.py`,
  `corner_assessment.py`, plus all CSV/JSON data.
* `a0/ a0r/ a0s/` — material, regime and prior-art evidence; `validation/` — the
  full check battery log; `START_HERE.txt`.

Excluded deliberately: the superseded manuscripts under `archive/`, earlier ZIP
archives, the large derived figure exports (`paper_a_study/figures_final`,
`paper_a_study/results`, PNG contact sheets), caches and virtual environments.

The manuscript is **statically validated and not compiled here**: no TeX engine
exists in the authoring sandbox (no `pdflatex`, `latexmk`, `tectonic`, `xelatex`
or `lualatex`). The independent round-4 audit compiled the same source with
LaTeX + BibTeX into a 29-page PDF; the round-5 layout repairs are at source
level. Build with

```
cd Paper_A_Final_Submission
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

GitHub release assets cannot be uploaded from this environment (`uploads.github.com`
is unreachable), so the archive is served from the repository tree instead.

---

## Superseded archives kept for provenance

* `Paper_A_Complete_Project_round4.zip` — 2 629 767 bytes, SHA-256
  `cb60652d0adf8499f64bed6d5d4bce1ea860396c460dbfc7bebbf9ed0404466b`
  (exactly the archive the independent round-4 audit examined).
  **Contains the corner-assessment defect** (backward wavenumber used as the
  operating-point incident wavenumber). Do not review against it.
* `Paper_A_Complete_Project_293f1fd.zip` — 5 909 423 bytes, SHA-256
  `8f0ba9524cf042ef879dfee972676c7c4d559befddd2517dc427a836feec5ef3`.
  Round-3 package; predates the phase-speed, electromagnetic-wavelength and
  mechanism corrections.
