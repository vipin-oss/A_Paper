# FINAL_PACKAGE_STATUS

**Overall status: COMPLETE FOR THE SCIENCE, PARTIAL FOR THE TYPESETTING.**
The program, data, figures, derivations, validation and documentation are finished and
internally consistent; the manuscript source is complete and statically valid but has
**never been compiled**, because no TeX engine exists in the build environment.  That one
gap is stated everywhere it matters and is the only blocking item.

* **Archive:** `PAPER_A_COMPLETE_REPRODUCIBILITY_ARCHIVE.zip` (built 2026-11-07)
* **Source state:** repository commit `f0a61e4` (round 21) + the verification run of 2026-11-07
* **Scientific classification of the paper:** **B** — the work is complete and its claims
  are bounded, but two questions remain open by construction (a sourced `H`/`f`, and a
  resolved corner) and one by environment (the typeset proof).

---

## 1. Status by component

| Component | Status | Evidence |
|---|---|---|
| **Program** | **COMPLETE** | 39 scripts + `model.py`; full battery 22 PASS / 1 SKIP / `OVERALL: PASS` (`04_REPRODUCTION/logs/battery_2026-11-07.log`) |
| **Data** | **COMPLETE and reproducible** | 34 files; a full re-run reproduces 33 byte-identically, the 34th differs only in `verdict.elapsed_s` |
| **Figures** | **COMPLETE** | 10 figures × 4 panels × 3 formats; regenerate in 9.5 s; identical drawn text on re-render; 2 of 10 byte-identical apart from the creation-date stamp |
| **Manuscript** | **COMPLETE, NOT COMPILED** | `main.tex` + 8 sections + 10 figure PDFs + 13-entry bib; `static_check` PASS (173 labels, 111 refs, 13/13 citations) |
| **Overleaf** | **READY, UNVERIFIED AT BUILD** | every `\input`/`\includegraphics`/`\bibliography` path resolves; no `.cls`/`.bst` needed; no PDF exists |
| **Validation** | **COMPLETE within scope** | `06_VALIDATION/VALIDATION_MATRIX.md`: 22 rows executed; 5 explicit "not validated" rows (no experiment, no third-party benchmark, no 3D FE, no compiled proof) |
| **Reproduction test** | **PASS WITH NUMERICAL DIFFERENCE / PARTIAL** | `04_REPRODUCTION/REPRODUCTION_TEST_RESULT.md` |
| **Derivations** | **COMPLETE** | `05_DERIVATIONS/` (11 documents, incl. the Gate 1 identity and the round-20 boundary repair) |
| **Documentation** | **COMPLETE** | this folder + `07_DOCUMENTATION/` + `audit_history/` (round reports 4–21) |
| **Integrity** | **COMPLETE** | `SHA256SUMS.txt`, `09_ARCHIVE_METADATA/file_manifest_sha256.csv`, `audit_archive.py` PASS |
| **Typeset proof / PDF** | **MISSING — cannot be produced here** | no TeX engine; not installable (`apt`, PyPI both checked) |

## 2. The three headline numbers, with their honest qualification

| Quantity | Value | Qualification that must travel with it |
|---|---|---|
| `R_B` at the certified local maximum | **0.9428718** at `k_x d = 0.52719`, flat top `[0.5267, 0.5276]` | a **modal share** at the reference plane `L = 10 d`, **not** a reflectance; local maximum only, not proved global; refinement spread `1.1e-6` |
| `R_B` at the operating point (`K0`, `Ω0`) | **0.0192916**, reflected angle `−27.90°` | same definition; the operating point is not the maximum |
| Corner closure | **bounded closure**, exponent ≈ **−0.63**, partition shift `3.9e-6` | *not* a resolved singularity; the words "resolved"/"exact" do not apply and are not used |

## 3. Limitations that a reader must not have to discover alone

1. **No compiled manuscript.**  Layout, page breaks and overfull boxes are unverified.
2. **`H` and `f` are not sourced.**  No measured strain-gradient, flexoelectric or
   carrier–gradient constant exists for this structure in the material used; the paper
   reports sweeps and matched controls instead of a materials prediction.
3. **Modal share ≠ reflectance.**  Fig. 5 supplies the partition (closure `1.3e-17`).
4. **The corner is bounded, not resolved** (see §2).
5. **No experimental or third-party numerical benchmark** exists for this coupled edge
   problem; the defence is the reduction set (closed-form SH limits `1e-9`–`1e-10`,
   reciprocity `1e-13`, independent `H¹` mesh, strong-form roots).
6. **Sensitivity is finite-difference, not Fisher-information/CRLB** — no FIM analysis was
   performed and none is claimed.
7. **`03_DATA/results_legacy/` is historical** and disagrees with the paper in places by
   design; nothing reads from it.

## 4. Missing items, exhaustively

| Missing | Type | Consequence |
|---|---|---|
| `main.pdf` | produced artifact | no page proof; Overleaf compile is the first real build |
| TeX engine in the build environment | tool | the reason for the above |
| measured `f_3zz`, `H`, `ℓ` for ZnO | input data | all coupling results are parametric |
| 3D FE cross-check of `R_B` and the corner | validation | the corner verdict stays a bounded closure |
| author/affiliation/license metadata | metadata | `LICENSE_AND_AUTHORSHIP_NOTE.md` records them as NOT DOCUMENTED |
| 29 MB `fig10_field.svg` | size | excluded on purpose; regenerates in ~10 s |

## 5. Recommended action, in order

1. **Compile the manuscript on any machine with TeX Live** (`02_OVERLEAF/`, four
   `pdflatex`/`bibtex` passes) and fix only genuine layout issues.  This closes the single
   blocking gap; nothing else in the package depends on it.
2. **Attach author/affiliation/funding metadata** (a `CITATION.cff`) if the package is to
   be deposited.
3. **Submit** with the claims as bounded (`R_B` a modal share; corner a bounded closure;
   `H`/`f` unsourced) — the manuscript already states all three.
4. **If a reviewer demands an independent check**, the highest-value additions are a 3D FE
   solution of the same boundary-value problem and a measured/DFT value of `H` and `f`;
   `07_DOCUMENTATION/KNOWN_LIMITATIONS.md` §5 ranks the remaining options.

## 6. How to verify this status document

```bash
python 04_REPRODUCTION/audit_archive.py      # structure, paths, junk, SHA-256
python 04_REPRODUCTION/compare_outputs.py    # regenerated data vs shipped data
cd 01_PROGRAM && python paper_a_study/run_all_checks.py    # 22 PASS / 1 SKIP
```

Every status line above is produced by one of those three commands or by
`02_OVERLEAF/scripts/static_check.py`.  If a status and a command disagree, **the command
wins** — and that disagreement is a defect in this document, which should be corrected
rather than explained away.
