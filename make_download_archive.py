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
STAGE = Path("/tmp/paper_a_round10_stage")   # outside the repo: no second main.tex
OUT = ROOT / "downloads" / "Paper_A_Complete_Project_round10.zip"

ROOT_REPORTS = [
    "PAPER_A_CORRECTION_HISTORY.md",
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
            "Paper A -- round 10: structure, language and presentation",
            "==========================================================",
            "",
            "Round 10 changed the way the article is written. It changed no equation, no number,",
            "no table cell, no figure, no dataset and no line of code. Read in this order:",
            "",
            "  PAPER_A_ROUND10_STYLE_AND_STRUCTURE_AUDIT.md       what was there before any edit, and why it changed",
            "  PAPER_A_ROUND10_AUTHOR_WRITING_STYLE.md            the author's habits, with the papers they come from",
            "  PAPER_A_ROUND10_STRUCTURE_COMPARISON.md            section skeleton against five published papers",
            "  PAPER_A_ROUND10_LANGUAGE_AND_STRUCTURE_CHANGES.md  every edit, classified, and what was left alone",
            "  PAPER_A_ROUND10_FINAL_MANUSCRIPT_STYLE_AUDIT.md    the closing audit, the battery, the open items",
            "  PAPER_A_CORRECTION_HISTORY.md                      cumulative history (round-10 addendum at the end)",
            "",
            "The manuscript is Paper_A_Final_Submission/main.tex; the ten vector figures are in",
            "Paper_A_Final_Submission/figures/.",
            "",
            "BUILD STATUS: UNVERIFIED -- no TeX engine was available, so no PDF is included and none is",
            "claimed. Build with:",
            "  cd Paper_A_Final_Submission",
            "  pdflatex main && bibtex main && pdflatex main && pdflatex main",
            "",
            "Reproduce every number and figure (Python 3.11, numpy, scipy, matplotlib):",
            "  python paper_a_study/run_all_checks.py      # the gates, ~10 min on two cores",
            "  python paper_a_study/build_figure_data.py   # the CSV/JSON datasets",
            "  python paper_a_study/generate_final_figures.py",
            "",
            "The battery of 2026-11-07 returned 17 PASS, 1 FAIL, 1 SKIP. The failing gate is the claim",
            "registry: the regenerated search record moves two spreads that are differences of nearly",
            "equal numbers (degree spread 5.613e-9 vs the committed 4.973e-9; quadrature spread",
            "9.382e-10 vs 5.591e-9) while the headline is unchanged to twelve digits. The records were",
            "restored to their committed state, as a manuscript-only round requires, and the gate then",
            "passes on 9 of 9 source rows. See validation/round10_registry_gate_note.txt.",
            "",
            "Headline result: R_B = 0.9467952 (94.68 %) at k_x d = 0.5275, a LOCAL maximum of the",
            "backward-modal share, flat to 0.01 pp over 0.5266 <= k_x d <= 0.5277. The incident flux there",
            "is 128 times smaller than at the operating point, so the share is not a statement about",
            "energy turned around. At the edge plane the same solve gives 0.9855722; the two differ by the",
            "net attenuation of the two partner modes over ten thicknesses. Novelty against the primary",
            "2025 source is UNRESOLVED (closed access); no priority claim is made, and the manuscript is",
            "not claimed to be submission-ready.",
        ]) + "\n")
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
