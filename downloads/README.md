# Downloadable project archive — round 6 (final)

`Paper_A_Complete_Project_round6.zip` — one-click download of the complete
Paper A project after the round-6 caption repair.

* Size: **2 652 884 bytes** (2.65 MB)
* Files: **163**
* SHA-256: `1d3bce3995132a5115fd2cc6501643c2dd470c382f8b38b24700623fddafef69`
* Reproducible: repeated builds are byte-identical. `make_download_archive.py`
  stages outside the repository and normalises every staged mtime, so the
  archive depends on file content only — verified by rebuilding after touching
  a source file.

Direct link (GitHub answers with a redirect to the raw host):

```
https://github.com/vipin-oss/A_Paper/raw/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round6.zip
```

Mirror on a second host, in case the redirect target is blocked by a proxy:

```
https://media.githubusercontent.com/media/vipin-oss/A_Paper/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round6.zip
```

Contents:

* `PAPER_A_ROUND6_FINAL_VERIFICATION.md` — what was corrected, files changed,
  build status and evidence, test results, ZIP verification, remaining
  limitations, journal-readiness assessment.
* `PAPER_A_FINAL_SCIENTIFIC_AUDIT.md` — the full audit, with the round-4, round-5
  and round-6 addenda.
* `PAPER_A_ROUND4_INDEPENDENT_AUDIT.md` — the external audit that motivated the
  round-5 corrections, verbatim.
* `Paper_A_Final_Submission/` — authoritative manuscript: `main.tex`, seven
  section files, eleven verified bibliography entries, ten vector PDF figures,
  `MANIFEST.json`, `static_validation.txt`, `README.md`.
* `paper_a_study/` — solver, figure drivers, verification suite, the four audit
  scripts (`phase_speed_audit.py`, `modal_flux_audit.py`,
  `mechanism_controls.py`, `corner_assessment.py`) and all CSV/JSON data.
* `a0/ a0r/ a0s/` material, regime and prior-art evidence; `validation/` the full
  battery log; `START_HERE.txt`.

**Compilation status.** The manuscript is **not compiled here**: this sandbox has
no TeX engine. The independent reviewer compiled this source (with the
`\protect\path` caption fix applied) to a **30-page PDF** with complete
bibliography, resolved citations and **no overfull boxes**. Build with

```
cd Paper_A_Final_Submission
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

GitHub release assets cannot be uploaded from this environment
(`uploads.github.com` is unreachable), so the archive is served from the
repository tree.

---

## Superseded archives kept for provenance

* `Paper_A_Complete_Project_round5.zip` — 2 644 649 bytes, SHA-256
  `b7a6478f7d3a0fc1dc62da558f701fc0f809c9467be5c5150f674624bbe3554f`.
  **Fails to compile as shipped**: fourteen captions contain an unprotected
  `\path`. Review against the round-6 archive instead.
* `Paper_A_Complete_Project_round4.zip` — 2 629 767 bytes, SHA-256
  `cb60652d0adf8499f64bed6d5d4bce1ea860396c460dbfc7bebbf9ed0404466b`.
  Contains the corner-assessment case-selection defect.
* `Paper_A_Complete_Project_293f1fd.zip` — 5 909 423 bytes, SHA-256
  `8f0ba9524cf042ef879dfee972676c7c4d559befddd2517dc427a836feec5ef3`.
  Round-3 package; predates the phase-speed, electromagnetic-wavelength and
  mechanism corrections.
