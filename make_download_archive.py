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
STAGE = Path("/tmp/paper_a_round11_stage")   # outside the repo: no second main.tex
OUT = ROOT / "downloads" / "Paper_A_Complete_Project_round11.zip"

ROOT_REPORTS = [
    "PAPER_A_CORRECTION_HISTORY.md",
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
            "Paper A -- round 11: programming audit, numerical reproducibility, figure verification",
            "=========================================================================================",
            "",
            "Round 11 went back to the code and the figures. It changed no equation, no boundary",
            "condition, no solution method and no headline number. Twenty-eight items were audited",
            "(D1-D28) before any edit, the confirmed defects were repaired, and the whole battery was",
            "then run on a cleanly regenerated data directory with nothing restored. Read in this order:",
            "",
            "  PAPER_A_ROUND11_STAGE1_PROGRAMMING_AND_FIGURE_AUDIT.md  the audit, written before the first edit",
            "  PAPER_A_ROUND11_NUMERICAL_REPRODUCIBILITY.md           the clean reproduction and the data comparison",
            "  PAPER_A_ROUND11_FIGURE_BY_FIGURE_AUDIT.md              ten figures, forty panels, one by one",
            "  PAPER_A_ROUND11_PANEL_SOURCE_MATRIX.md                 which column every panel plots",
            "  PAPER_A_ROUND11_CLAIM_REGISTRY_CORRECTION.md           categories A-E, bounds, tolerances",
            "  PAPER_A_ROUND11_MUTATION_AND_REGRESSION_RESULTS.md     15 mutants, 47 tests, anti-regression list",
            "  PAPER_A_ROUND11_CORRECTION_HISTORY.md                  every change, with its evidence",
            "  PAPER_A_ROUND11_FINAL_TECHNICAL_READINESS.md           the closing verdict and what is still open",
            "  PAPER_A_CORRECTION_HISTORY.md                          cumulative history (round-11 addendum at the end)",
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
            "The battery of 2026-11-07, run on freshly generated data with no record restored, returned",
            "18 PASS, 0 FAIL, 1 SKIP (the skip is the LaTeX build: no engine). It includes 47 unit and",
            "scientific tests, 15 deliberate mutants all caught, 23 registered claims on 46 tokens with",
            "11 of 11 source-agreement rows passing, and the figure-provenance tests that keep the",
            "label defects of this round from returning. Log:",
            "validation/round11_battery_run_clean_reproduction.log.",
            "",
            "What round 11 found in the text: the coupling-induced frequency shift was quoted as at most",
            "60 kHz (<4e-6) while the data of its own figure give 183.7 kHz (1.09e-5); the v_g/v_E",
            "agreement was quoted as 3.5 % over the whole branch but is 6.4 % at the lowest sample; the",
            "two refinement spreads were quoted to two significant figures and tested by a 1 % equality",
            "test, which made the round-10 battery fail on round-off. All three sentences are corrected",
            "and registered. What it found in the figures: 'backward reflectance' on an axis that plots a",
            "modal share; the gradient-length symbol used for the reference-plane distance and for the",
            "distance from the edge; an attenuation length labelled L; a schematic with no label; two",
            "residual panels showing round-off as structure; an inset that clipped the largest value it",
            "describes; and a panel xlabel cut by the canvas edge. All eight are repaired and tested.",
            "",
            "Headline result (unchanged): R_B = 0.9467952 (94.68 %) at k_x d = 0.5275, a LOCAL maximum",
            "of the backward-modal share, flat to 0.01 pp over 0.5266 <= k_x d <= 0.5277. The incident",
            "flux there is 128 times smaller than at the operating point, so the share is not a statement",
            "about energy turned around. At the edge plane the same solve gives 0.9855722. Novelty",
            "against the primary 2025 source is UNRESOLVED (closed access); no priority claim is made,",
            "and the manuscript is not claimed to be submission-ready.",
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
