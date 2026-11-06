# Downloadable project archive — round 4

`Paper_A_Complete_Project_round4.zip` — one-click download of the complete
Paper A project after the round-4 scientific audit.

* Size: **2 629 767 bytes** (2.63 MB)
* Files: **161**
* SHA-256: `cb60652d0adf8499f64bed6d5d4bce1ea860396c460dbfc7bebbf9ed0404466b`

Direct link (GitHub answers with a redirect to the raw host):

```
https://github.com/vipin-oss/A_Paper/raw/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round4.zip
```

Mirror on a second host, in case the redirect target is blocked by a corporate
proxy:

```
https://media.githubusercontent.com/media/vipin-oss/A_Paper/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round4.zip
```

Contents: `PAPER_A_FINAL_SCIENTIFIC_AUDIT.md` (the round-4 audit, issues A–F and
sections 9–11), `Paper_A_Final_Submission/` (authoritative manuscript: `main.tex`,
seven section files, eleven bibliography entries, ten vector PDF figures,
`static_validation.txt`, `MANIFEST.json`, README), `paper_a_study/` (solver,
figure drivers, verification suite, the round-4 audit scripts
`phase_speed_audit.py`, `modal_flux_audit.py`, `mechanism_controls.py`,
`corner_assessment.py`, all CSV/JSON data), `a0/ a0r/ a0s/` (material, regime and
prior-art evidence), `validation/` (verification log), the earlier audit and
progress documents, and `START_HERE.txt`.

Excluded deliberately: the superseded manuscripts under `archive/`, earlier ZIP
archives, the large derived figure exports (`paper_a_study/figures_final`,
`paper_a_study/results`, PNG contact sheets), caches and virtual environments.

The manuscript is **statically validated and not compiled**: no TeX engine is
available in the authoring sandbox. Build it with

```
cd Paper_A_Final_Submission
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

GitHub release assets cannot be uploaded from this environment (the asset host
`uploads.github.com` is unreachable), so the archive is served from the
repository tree instead.

---

The round-3 archive `Paper_A_Complete_Project_293f1fd.zip` (5 909 423 bytes,
SHA-256 `8f0ba9524cf042ef879dfee972676c7c4d559befddd2517dc427a836feec5ef3`) is
retained in this directory for provenance. It is **superseded**: it predates the
round-4 corrections to the phase speed, the electromagnetic wavelength and the
attribution of the negative reflection, and it should not be used for review.
