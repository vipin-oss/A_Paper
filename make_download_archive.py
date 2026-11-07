#!/usr/bin/env python3
"""Build the round-10 downloadable project archive.

Deterministic and read-only with respect to the sources: it copies from the
working tree into a staging directory, writes START_HERE.txt, PACKAGE_README.md
and PACKAGE_SHA256.txt, and zips the result.  It never modifies a source file.

    python make_download_archive.py

Excluded on purpose: the superseded manuscripts under archive/, earlier ZIPs,
bytecode caches, virtual environments, and the large derived figure exports
(paper_a_study/figures_final, paper_a_study/results, PNG contact sheets).
"""
from __future__ import annotations

import hashlib
import os
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGE = Path("/tmp/paper_a_round12_stage")   # outside the repo: no second main.tex
OUT = ROOT / "downloads" / "Paper_A_Complete_Project_round12.zip"

ROOT_REPORTS = [
    "PAPER_A_CORRECTION_HISTORY.md",
    "PAPER_A_ROUND12_PRELIMINARY_EVIDENCE_CORRECTIONS.md",
    "PAPER_A_ROUND12_SECTION_BY_SECTION_REVIEW.md",
    "PAPER_A_ROUND12_EDIT_LEDGER.md",
    "PAPER_A_ROUND12_NUMERICAL_TRACEABILITY_AUDIT.md",
    "PAPER_A_ROUND12_READINESS_ASSESSMENT.md",
    "PAPER_A_ROUND12_BLOCKING_ISSUES.md",
    "PAPER_A_ROUND12_CORRECTION_HISTORY.md",
    "PAPER_A_ROUND11_STAGE1_PROGRAMMING_AND_FIGURE_AUDIT.md",
    "PAPER_A_ROUND11_NUMERICAL_REPRODUCIBILITY.md",
    "PAPER_A_ROUND11_FIGURE_BY_FIGURE_AUDIT.md",
    "PAPER_A_ROUND11_PANEL_SOURCE_MATRIX.md",
    "PAPER_A_ROUND11_CLAIM_REGISTRY_CORRECTION.md",
    "PAPER_A_ROUND11_MUTATION_AND_REGRESSION_RESULTS.md",
    "PAPER_A_ROUND11_CORRECTION_HISTORY.md",
    "PAPER_A_ROUND11_FINAL_TECHNICAL_READINESS.md",
    "PAPER_A_ROUND10_STYLE_AND_STRUCTURE_AUDIT.md",
    "PAPER_A_ROUND10_AUTHOR_WRITING_STYLE.md",
    "PAPER_A_ROUND10_STRUCTURE_COMPARISON.md",
    "PAPER_A_ROUND10_LANGUAGE_AND_STRUCTURE_CHANGES.md",
    "PAPER_A_ROUND10_FINAL_MANUSCRIPT_STYLE_AUDIT.md",
    "PAPER_A_ROUND9_STAGE1_NORMALIZATION_AUDIT.md",
    "PAPER_A_ROUND9_CORRECTION_HISTORY.md",
    "PAPER_A_ROUND9_PLANE_INVARIANCE_VALIDATION.md",
    "PAPER_A_ROUND9_MUTATION_REPORT.md",
    "PAPER_A_ROUND9_CLAIMS_AND_MANUSCRIPT_AUDIT.md",
    "PAPER_A_ROUND9_TEST_RESULTS.md",
    "PAPER_A_ROUND9_DELIVERY_AND_STATUS.md",
    "PAPER_A_ROUND8_STAGE1_AUDIT.md",
    "PAPER_A_ROUND8_PEAK_CERTIFICATION.md",
    "PAPER_A_ROUND8_ARTEFACT_AUDIT.md",
    "PAPER_A_ROUND8_CONVERGENCE_AND_CONTROLS.md",
    "PAPER_A_ROUND8_MANUSCRIPT_CHANGES.md",
    "PAPER_A_ROUND8_CLAIMS_AND_TESTS.md",
    "PAPER_A_ROUND8_DELIVERY_AND_STATUS.md",
    "PAPER_A_STAGE1_COMPLETE_Q1_AUDIT.md",
    "PAPER_A_ROUND7_NOVELTY_AND_MECHANISM_REPORT.md",
    "PAPER_A_EXTENDED_NUMERICAL_VALIDATION.md",
    "PAPER_A_CLAIM_PROVENANCE_MATRIX.md",
    "PAPER_A_FINAL_SUBMISSION_READINESS.md",
    "PAPER_A_FINAL_SCIENTIFIC_AUDIT.md",
    "PAPER_A_ROUND4_INDEPENDENT_AUDIT.md",
    "PAPER_A_ROUND6_FINAL_VERIFICATION.md",
    "PAPER_A_FINAL_INDEPENDENT_CORRECTION_RESPONSE.md",
    "PAPER_A_FINAL_SCIENTIFIC_CORRECTION_AND_Q1_AUDIT.md",
    "PAPER_A_FINAL_SCIENTIFIC_CHECK.md",
    "PAPER_A_FIGURE_AUDIT_FINAL.md",
    "PAPER_A_PROGRESS.md",
    "PAPER_A_BLUEPRINT_V2_1.md",
    "PAPER_A_RESEARCH_REPORT.md",
    "PAPER_A_A0_CONSTITUTIVE_CHECK.md",
    "PAPER_A_A0_DISPERSION_FEASIBILITY.md",
    "PAPER_A_A0_MATERIALS.md",
    "PAPER_A_A0_PRIOR_ART.md",
    "PAPER_A_A0R_BACKWARD_WAVE_FEASIBILITY.md",
    "PAPER_A_A0R_DECISION.md",
    "PAPER_A_A0R_NOVELTY_COMPARISON.md",
    "PAPER_A_A0S_H_SENSITIVITY.md",
    "PAPER_A_A0S_MODEL_SELECTION.md",
    "PAPER_A_A0S_OPERATING_REGIME.md",
    ".gitignore",
]
ROOT_SCRIPTS = ["build_submission_package.py", "build_paper_a_package.py",
                "make_download_archive.py"]

SKIP_DIRS = {"__pycache__", "figures_final", "results", "cache", "private_sources"}
SKIP_SUFFIX = {".pyc", ".pyo", ".npy", ".npz", ".png", ".svg"}
SKIP_NAMES: set[str] = set()   # the two contact-sheet PDFs are small and useful
FIXED_EPOCH = 1767225600            # 2026-01-01T00:00:00Z, for reproducible zips


def keep(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.suffix in SKIP_SUFFIX or path.name in SKIP_NAMES:
        return False
    return True


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)

    copied = 0
    for name in ROOT_REPORTS + ROOT_SCRIPTS:
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, STAGE / name)
            copied += 1

    for top in ("Paper_A_Final_Submission", "paper_a_study", "a0", "a0r", "a0s",
                "validation"):
        base = ROOT / top
        if not base.exists():
            continue
        for src in sorted(base.rglob("*")):
            if src.is_dir() or not keep(src):
                continue
            rel = src.relative_to(ROOT)
            dst = STAGE / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1

    (STAGE / "START_HERE.txt").write_text(
        "\n".join([
            "Paper A -- round 12: section-by-section review of the manuscript",
            "==================================================================",
            "",
            "Round 12 read the whole manuscript, section by section, against the paper's own records:",
            "mathematics, physics, language, and what a journal requires. It changed no equation, no",
            "constant, no boundary condition, no solver, no dataset, no figure PDF and no reported",
            "number. Two round-11 reporting defects were corrected first, then nineteen prose defects",
            "were repaired, ten of them places where the text disagreed with the delivered data.",
            "Read in this order:",
            "",
            "  PAPER_A_ROUND12_PRELIMINARY_EVIDENCE_CORRECTIONS.md  start here: the two round-11 fixes",
            "  PAPER_A_ROUND12_SECTION_BY_SECTION_REVIEW.md         the review, section by section",
            "  PAPER_A_ROUND12_EDIT_LEDGER.md                       all nineteen edits, before and after",
            "  PAPER_A_ROUND12_NUMERICAL_TRACEABILITY_AUDIT.md      every number against its record",
            "  PAPER_A_ROUND12_READINESS_ASSESSMENT.md              numerical and scientific readiness",
            "  PAPER_A_ROUND12_BLOCKING_ISSUES.md                   what is still open, and why",
            "  PAPER_A_ROUND12_CORRECTION_HISTORY.md                what was done, in order",
            "  PAPER_A_CORRECTION_HISTORY.md                        cumulative history (round-12 addendum last)",
            "",
            "  The round-11 reports are included too. Two of them carry 'Corrected in round 12'",
            "  annotations where round 11 mislabelled a reproducibility number; read the correction",
            "  first, not after.",
            "",
            "The manuscript is Paper_A_Final_Submission/main.tex; the ten vector figures are in",
            "Paper_A_Final_Submission/figures/.",
            "",
            "BUILD STATUS: UNVERIFIED -- no TeX engine was available, so no PDF is included and none is",
            "claimed. Build with:",
            "  cd Paper_A_Final_Submission",
            "  pdflatex main && bibtex main && pdflatex main && pdflatex main",
            "",
            "Reproduce every number and figure (Python 3.11, numpy, scipy, matplotlib), in this order:",
            "  rm -f paper_a_study/figure_data/*            # empty data directory",
            "  python paper_a_study/build_figure_data.py    # 7 min: the CSV/JSON datasets",
            "  python paper_a_study/generate_final_figures.py   # 10 s: the ten figures",
            "  cp paper_a_study/figures_final/fig*.pdf Paper_A_Final_Submission/figures/",
            "  python paper_a_study/run_all_checks.py       # 13 min: the battery",
            "",
            "Gates run after this round's edits: 47 unit and scientific tests OK; 23 registered claims",
            "on 46 tokens with 11 of 11 source-agreement rows; 15 deliberate mutants all caught; the",
            "phase-speed audit PASS; the LaTeX static check PASS (104 labels, 75 references, 13 of 13",
            "citations, 16634 words). The full 18-gate battery was not re-run: no producer, dataset or",
            "solver file changed. Its last execution on freshly generated data is",
            "validation/round11_battery_run_clean_reproduction.log (18 PASS, 0 FAIL, 1 SKIP, the skip",
            "being the LaTeX build).",
            "",
            "What round 12 found in the text: the density and mobility sweeps were described with",
            "factors of nine, ten and five where the stored columns scale by exactly three; two",
            "gradient-length percentages were attached to abscissae that are not on the grid; the phase",
            "speeds were transposed; a reproducibility paragraph quoted a sensitivity pair that exists in",
            "no record; the energy budget quoted five arithmetic and provenance errors in six sentences;",
            "the backward wavenumber was drawn from two different ratios and given the flux's sign; and",
            "the appendix's test count had gone stale by eight. Nineteen items, all corrected against",
            "named records. One frozen figure annotation (fig10(c), the backward wavenumber arrow) is",
            "reported and not repaired: fig10_field.pdf is frozen for this round.",
            "",
            "Headline result (unchanged): R_B = 0.9467952 (94.68 %) at k_x d = 0.5275, a LOCAL maximum",
            "of the backward-modal share, flat to 0.01 pp over 0.5266 <= k_x d <= 0.5277. The incident",
            "flux there is 128 times smaller than at the operating point. At the edge plane the same",
            "solve gives 0.9855722. Novelty against the primary 2025 source is UNRESOLVED (closed",
            "access); no priority claim is made, the build is unverified, five declarations await the",
            "author, and the manuscript is not claimed to be submission-ready.",
        ]) + "\n")
    copied += 1
    os.utime(STAGE / "START_HERE.txt", (FIXED_EPOCH, FIXED_EPOCH))

    shutil.copy2(ROOT / "PACKAGE_README.md", STAGE / "PACKAGE_README.md")
    copied += 1

    # Normalise every staged mtime so that the archive depends only on content.
    for path in STAGE.rglob("*"):
        if path.is_file():
            os.utime(path, (FIXED_EPOCH, FIXED_EPOCH))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(STAGE.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(STAGE).as_posix())

    digest = sha256(OUT)
    n = len(zipfile.ZipFile(OUT).namelist())
    size = OUT.stat().st_size
    checksum = f"{digest}  {OUT.name}\n{size} bytes, {n} files\n"
    # The checksum file cannot live inside the archive it describes, so it is
    # written twice: into the staging tree (for inspection) and beside the ZIP
    # (where a downloader can actually read it).
    (STAGE / "PACKAGE_SHA256.txt").write_text(checksum)
    (OUT.parent / "PACKAGE_SHA256.txt").write_text(checksum)
    print(f"archive : {OUT}")
    print(f"files   : {n}   staged copies: {copied}")
    print(f"size    : {size:,} bytes ({size/1e6:.2f} MB)")
    print(f"sha256  : {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
