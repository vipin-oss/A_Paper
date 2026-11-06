#!/usr/bin/env python3
"""Build the round-8 downloadable project archive.

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
STAGE = Path("/tmp/paper_a_round8_stage")   # outside the repo: no second main.tex
OUT = ROOT / "downloads" / "Paper_A_Complete_Project_round8.zip"

ROOT_REPORTS = [
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
    "PAPER_A_CORRECTION_HISTORY.md",
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
        "Paper A -- round-8 audit and correction deliverable\n"
        "==================================================\n\n"
        "Read in this order:\n"
        "  PAPER_A_ROUND8_STAGE1_AUDIT.md            the nine defects, proven, before any edit\n"
        "  PAPER_A_ROUND8_PEAK_CERTIFICATION.md      the certified maximum and its evidence\n"
        "  PAPER_A_ROUND8_ARTEFACT_AUDIT.md          why the high share is not an artefact\n"
        "  PAPER_A_ROUND8_CONVERGENCE_AND_CONTROLS.md  convergence, controls, bounds\n"
        "  PAPER_A_ROUND8_MANUSCRIPT_CHANGES.md      every edit, old -> new, and why\n"
        "  PAPER_A_ROUND8_CLAIMS_AND_TESTS.md        19 claims, 26 tests, 8 mutants\n"
        "  PAPER_A_ROUND8_DELIVERY_AND_STATUS.md     battery, archive, open items\n"
        "  PAPER_A_CORRECTION_HISTORY.md             cumulative history (round-8 addendum at the end)\n"
        "  PAPER_A_FINAL_SUBMISSION_READINESS.md     ten-category verdict, older round\n"
        "  PAPER_A_ROUND7_NOVELTY_AND_MECHANISM_REPORT.md  novelty UNRESOLVED\n\n"
        "The manuscript is Paper_A_Final_Submission/main.tex; the ten vector\n"
        "figures are in Paper_A_Final_Submission/figures/.\n\n"
        "BUILD STATUS: UNVERIFIED -- no TeX engine was available, so no PDF is\n"
        "included and none is claimed. Build with:\n"
        "  cd Paper_A_Final_Submission\n"
        "  pdflatex main && bibtex main && pdflatex main && pdflatex main\n\n"
        "Reproduce every number and figure (Python 3.11, numpy, scipy, matplotlib):\n"
        "  python paper_a_study/run_all_checks.py     # 18 checks + 26 unit tests, ~11 min\n"
        "  python paper_a_study/build_figure_data.py  # the CSV/JSON datasets\n"
        "  python paper_a_study/generate_final_figures.py\n\n"
        "Headline result: R_B = 0.9467952 (94.68 %) at k_x d = 0.5275, a certified\n"
        "LOCAL maximum of the backward-modal share, flat to 0.01 pp over\n"
        "0.5266 <= k_x d <= 0.5277; the incident flux there is 128 times smaller than\n"
        "at the operating point, so the share is not a statement about energy turned\n"
        "around. The earlier 93.19 % at 0.525 was a coarse-grid sample and is\n"
        "withdrawn. Novelty against the primary 2025 source is UNRESOLVED (closed\n"
        "access); no priority claim is made.\n")
    copied += 1
    # Fixed timestamp so that repeated builds are byte-identical.
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
