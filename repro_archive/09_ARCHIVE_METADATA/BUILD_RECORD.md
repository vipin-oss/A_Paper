# BUILD_RECORD

How this archive was assembled, so that it can be rebuilt byte-for-byte in principle and
audited in practice.

**Builder:** `01_PROGRAM/tools/build_repro_archive.py` (in the source repository:
`build_repro_archive.py` at the root) — the script is shipped, so the build is not a
manual process.
**Built:** 2026-11-07 (UTC), from the repository working tree at commit `f0a61e4`
(branch `arena/ea7ca4dd-a-paper`), plus this round's verification run.
**Output:** `PAPER_A_COMPLETE_REPRODUCIBILITY_ARCHIVE.zip`, one top-level folder of the
same name.

## 1. Environment used to build and verify

| Item | Value |
|---|---|
| OS | Linux (x86-64) sandbox |
| Python | 3.11.2 |
| numpy / scipy / matplotlib | 2.4.6 / 1.17.1 / 3.11.2 |
| `pip freeze` | `environment_pip_freeze.txt` (this folder) |
| TeX engine | **none available** — no `pdflatex`, `latexmk`, `xelatex`, `lualatex`, `tectonic` |
| network | not used by any script |

## 2. Inclusion rules

Included: the program of record (`paper_a_study/`, `a0/`, feasibility studies under
`feasibility/`), the manuscript source and its figure PDFs, all figure data and audit
records, the legacy results (labelled), the derivations, the validation evidence, the ten
figures in three formats, the documentation set, and the integrity manifests.

Excluded, with reason:

| Excluded | Reason |
|---|---|
| `.git/`, `.venv/`, `__pycache__/`, `*.pyc` | development state, not content |
| `downloads/`, all round zips (7–21) | superseded deliverables; two "final" packages would be a version conflict |
| `paper_a_study/figures_final/fig10_field.svg`, `paper_a_study/results/fig10_field.svg` | 29 MB each, regenerable in ~10 s, unused by the manuscript |
| `a0s/private_sources/` (if present) | private third-party sources; referenced nowhere |
| the 29 MB intermediate SVGs under `results/` | same as above |
| `main.pdf` | **does not exist** — never compiled |

## 3. Duplicate-avoidance rule

No file is shipped twice.  The manuscript exists once (`02_OVERLEAF/`); the figures exist
once per format (in `08_FINAL_OUTPUTS/figures_final/`, with the PDF copies that the
manuscript needs in `02_OVERLEAF/figures/`, which are the same bytes — the manifest shows
them as distinct paths with identical hashes, which is stated rather than hidden); the
data exist once (`03_DATA/figure_data/`, which is also where `build_figure_data.py` writes
when re-run inside the archive).  Every older report is in
`07_DOCUMENTATION/audit_history/` with its date in the filename, and the current statement
is `FINAL_PACKAGE_STATUS.md` — historical records are labelled as such in
`06_VALIDATION/README_VALIDATION.md`.

## 4. Integrity manifests

| File | Contents |
|---|---|
| `SHA256SUMS.txt` (archive root) | `sha256␠␠path` for every file in the archive |
| `09_ARCHIVE_METADATA/file_manifest_sha256.csv` | `path,bytes,sha256` for every file |
| `09_ARCHIVE_METADATA/run_manifest.json` | every battery step: command, outputs, status, seconds, log hash |
| `09_ARCHIVE_METADATA/parameter_manifest.json` | every parameter: value, unit, source, status (SOURCED / DERIVED / NOT_SOURCED / NOT AVAILABLE) |

## 5. Reproducing this build

```bash
cd <repository root>
python build_repro_archive.py        # writes /tmp/PAPER_A_COMPLETE_REPRODUCIBILITY_ARCHIVE
                                     # and downloads/PAPER_A_COMPLETE_REPRODUCIBILITY_ARCHIVE.zip
```

The builder prints a JSON summary (file counts per folder, zip bytes, zip SHA-256).  The
SHA-256 of the zip is recorded in `FINAL_PACKAGE_STATUS.md` and repeated in the final
response of the session that produced it; because zip entries carry file timestamps, a
rebuild on a different day will produce a different zip hash with identical contents —
compare the **contents** (`file_manifest_sha256.csv`), not the container hash.

## 6. Audit checklist applied before the zip was written

* every required document present (`README_PROGRAM`, `README_OVERLEAF`, `README_DATA`,
  `DATA_DICTIONARY`, `REPRODUCE_FROM_SCRATCH`, `RUN_ORDER`, `run_manifest.json`,
  `parameter_manifest.json`, `FIGURE_PROVENANCE`, `PROJECT_OVERVIEW`,
  `MODEL_DESCRIPTION`, `NUMERICAL_METHOD`, `CHANGELOG`, `KNOWN_LIMITATIONS`,
  `ARCHIVE_README`, `FINAL_PACKAGE_STATUS`, `SHA256SUMS.txt`,
  `file_manifest_sha256.csv`) — checked by `04_REPRODUCTION/audit_archive.py`
* no absolute paths of the build machine in any shipped text file (checked by the same
  script)
* no `.pyc`, `__pycache__`, `.DS_Store`, `*.tmp`, `*.log` from a build outside `logs/`
* every `\input` / `\includegraphics` / `\bibliography` target present (checked by
  `02_OVERLEAF/static_check.py`)
* every number quoted in the documentation traceable to a stored JSON/CSV (spot-checked
  against `08_FINAL_OUTPUTS/FINAL_RESULTS_TABLE.csv`)

**Result of that audit on this build** (`python 04_REPRODUCTION/audit_archive.py`):

```
[PASS] A. required documents
[PASS] B. no absolute build-machine paths in live files
[WARN] B'. historical records contain old session paths (4 hits, left unedited)
[PASS] C. no junk files
[PASS] D. manuscript \input / \includegraphics / \bibliography targets
[PASS] E. manuscript figures present and non-trivial   10 PDF(s)
[PASS] F. no conflicting artifacts outside historical folders
[WARN] F'. generic file names repeat inside baseline/study folders (10, documented)
[PASS] G. no file over 40 MB
[PASS] H. SHA256SUMS.txt agrees with disk   374 file(s) verified
AUDIT: PASS
```

The two WARNs are structural, not defects: the historical round reports in
`07_DOCUMENTATION/audit_history/` are shipped unedited (one of them quotes an old session
path), and the A0/a0r/a0s sub-studies legitimately reuse generic file names
(`requirements.txt`, `run_checks.py`, `validation.json`) for different programs.

## 7. Two defects found while assembling the archive (and fixed)

1. **Stale manuscript figures.**  Three of the ten PDFs in
   `Paper_A_Final_Submission/figures/` were older renders than
   `paper_a_study/figures_final/` — their embedded annotation text differed (fig02, fig07,
   fig08).  The ten PDFs were refreshed from the canonical set and the submission
   `MANIFEST.json` rebuilt; all ten pairs are now byte-identical, which is what
   `02_OVERLEAF/README_OVERLEAF.md` claims.
2. **Two versions of the styling module.**  `Paper_A_Final_Submission/scripts/
   figure_style.py` was a 102-line earlier version of the 275-line canonical
   `paper_a_study/figure_style.py`.  The canonical file was copied in (identical SHA-256),
   the manifest rebuilt, and the archive ships a single copy.

No reported number changed: `claim_audit` (10/10 source-agreement) and `static_check`
(PASS) were re-run after both fixes.  Both are recorded in
`07_DOCUMENTATION/CHANGELOG.md`.
