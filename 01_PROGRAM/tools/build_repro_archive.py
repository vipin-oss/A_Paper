#!/usr/bin/env python3
"""Build the single self-contained reproducibility archive for Paper A.

    .venv/bin/python build_repro_archive.py

Creates PAPER_A_COMPLETE_REPRODUCIBILITY_ARCHIVE/ at the repository root with
the nine required folders, copies only relevant material (no .git, no venv, no
caches, no derived zips, no 29 MB intermediate SVGs), and then hashes and zips
the tree.  The documentation files inside the tree are maintained as real files
in the repository (repro_archive/) and copied in, so that the archive can be
rebuilt exactly.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "PAPER_A_COMPLETE_REPRODUCIBILITY_ARCHIVE"
STAGE = Path("/tmp") / NAME
DOCS = ROOT / "repro_archive"
ZIP_OUT = ROOT / "downloads" / f"{NAME}.zip"

#: files that are large intermediates and are regenerated, not delivered
SKIP_FILES = {
    "paper_a_study/results/fig10_field.svg",          # 29 MB intermediate
    "paper_a_study/figures_final/fig10_field.svg",    # 29 MB intermediate
}
SKIP_DIRS = {".git", ".venv", "__pycache__", "downloads", ".pytest_cache",
             "private_sources"}
#: path prefixes that are shipped somewhere else (figures -> 08, data -> 03)
SKIP_PREFIXES = ("paper_a_study/figures_final", "paper_a_study/results",
                 "paper_a_study/figure_data")


def copytree(src: Path, dst: Path) -> int:
    n = 0
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(ROOT).as_posix()
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if rel in SKIP_FILES or path.suffix in {".pyc", ".pyo"}:
            continue
        if any(rel == pre or rel.startswith(pre + "/") for pre in SKIP_PREFIXES):
            continue
        target = dst / path.relative_to(src)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            n += 1
    return n


def copytree_allow(src: Path, dst: Path) -> int:
    """Like copytree but only the file-level skips apply (for explicit targets)."""
    n = 0
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(ROOT).as_posix()
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if rel in SKIP_FILES or path.suffix in {".pyc", ".pyo"}:
            continue
        target = dst / path.relative_to(src)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            n += 1
    return n


def copy_files(names, dst: Path) -> int:
    n = 0
    for name in names:
        src = ROOT / name
        if src.is_dir():                     # a doc subfolder, e.g. 04_REPRODUCTION/logs
            target = dst / src.name
            target.mkdir(parents=True, exist_ok=True)
            for f in sorted(src.rglob("*")):
                if f.is_file():
                    (target / f.relative_to(src)).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, target / f.relative_to(src))
                    n += 1
            continue
        if not src.exists():
            print(f"  MISSING (not copied): {name}")
            continue
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst / src.name)
        n += 1
    return n


def main() -> int:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    for d in ("01_PROGRAM", "02_OVERLEAF", "03_DATA", "04_REPRODUCTION",
              "05_DERIVATIONS", "06_VALIDATION", "07_DOCUMENTATION",
              "08_FINAL_OUTPUTS", "09_ARCHIVE_METADATA"):
        (STAGE / d).mkdir(parents=True)

    counts = {}
    # ---- 01 PROGRAM -----------------------------------------------------
    counts["01_PROGRAM"] = copytree(ROOT / "paper_a_study", STAGE / "01_PROGRAM" / "paper_a_study")
    counts["01_PROGRAM"] += copytree(ROOT / "a0", STAGE / "01_PROGRAM" / "a0")
    counts["01_PROGRAM"] += copytree(ROOT / "a0r", STAGE / "01_PROGRAM" / "feasibility" / "a0r")
    counts["01_PROGRAM"] += copytree(ROOT / "a0s", STAGE / "01_PROGRAM" / "feasibility" / "a0s")
    counts["01_PROGRAM"] += copy_files(
        ["Paper_A_Final_Submission/scripts/static_check.py",
         "build_submission_package.py", "make_download_archive.py",
         "build_repro_archive.py", "sync_paper_a_figures.py"],
        STAGE / "01_PROGRAM" / "tools")
    counts["01_PROGRAM"] += copy_files(list(DOCS.glob("01_PROGRAM/*")), STAGE / "01_PROGRAM")

    # ---- 02 OVERLEAF ----------------------------------------------------
    counts["02_OVERLEAF"] = copy_files(
        ["Paper_A_Final_Submission/main.tex", "Paper_A_Final_Submission/references.bib"],
        STAGE / "02_OVERLEAF")
    counts["02_OVERLEAF"] += copytree(ROOT / "Paper_A_Final_Submission/sections", STAGE / "02_OVERLEAF" / "sections")
    counts["02_OVERLEAF"] += copytree(ROOT / "Paper_A_Final_Submission/figures", STAGE / "02_OVERLEAF" / "figures")
    # static_check.py must sit one level below the manuscript root: it computes
    # ROOT = Path(__file__).resolve().parents[1].  Hence 02_OVERLEAF/scripts/.
    counts["02_OVERLEAF"] += copy_files(
        ["Paper_A_Final_Submission/scripts/static_check.py"],
        STAGE / "02_OVERLEAF" / "scripts")
    counts["02_OVERLEAF"] += copy_files(
        ["Paper_A_Final_Submission/static_validation.txt"], STAGE / "02_OVERLEAF")
    counts["02_OVERLEAF"] += copy_files(list(DOCS.glob("02_OVERLEAF/*")), STAGE / "02_OVERLEAF")

    # ---- 03 DATA --------------------------------------------------------
    counts["03_DATA"] = copytree_allow(ROOT / "paper_a_study/figure_data",
                                      STAGE / "03_DATA" / "figure_data")
    counts["03_DATA"] += copytree_allow(ROOT / "paper_a_study/results",
                                        STAGE / "03_DATA" / "results_legacy")
    counts["03_DATA"] += copy_files(list(DOCS.glob("03_DATA/*")), STAGE / "03_DATA")

    # ---- 04 REPRODUCTION ------------------------------------------------
    counts["04_REPRODUCTION"] = copy_files(list(DOCS.glob("04_REPRODUCTION/*")), STAGE / "04_REPRODUCTION")
    counts["04_REPRODUCTION"] += copytree(ROOT / "validation", STAGE / "04_REPRODUCTION" / "logs")
    if Path("/tmp/repro_logs").exists():
        counts["04_REPRODUCTION"] += copytree(Path("/tmp/repro_logs"), STAGE / "04_REPRODUCTION" / "logs")

    # ---- 05 DERIVATIONS -------------------------------------------------
    counts["05_DERIVATIONS"] = copy_files(
        ["PAPER_A_ROUND21_GATE1_DERIVATION.md",
         "PAPER_A_ROUND20_VARIATIONAL_BOUNDARY_DERIVATION.md",
         "PAPER_A_ROUND20_FACE_VS_EDGE_NORMAL_AUDIT.md",
         "PAPER_A_ROUND20_HYPERSTRESS_AND_CORNER_AUDIT.md",
         "PAPER_A_ROUND19_HYPERSTRESS_AND_BOUNDARY_AUDIT.md",
         "PAPER_A_ROUND15_COMPLETE_COUPLED_WEAK_FORM.md",
         "PAPER_A_ROUND16_CARRIER_STRONG_TO_WEAK_DERIVATION.md",
         "PAPER_A_ROUND16_CONVENTIONS_AND_DIMENSIONS.md",
         "PAPER_A_ROUND17_MATHEMATICAL_DERIVATIONS.md",
         "PAPER_A_ROUND17_WORKED_CALCULATIONS.md",
         "PAPER_A_ROUND14_MATHEMATICAL_DERIVATION_MATRIX.md"],
        STAGE / "05_DERIVATIONS")
    counts["05_DERIVATIONS"] += copy_files(list(DOCS.glob("05_DERIVATIONS/*")), STAGE / "05_DERIVATIONS")

    # ---- 06 VALIDATION --------------------------------------------------
    counts["06_VALIDATION"] = copy_files(list(DOCS.glob("06_VALIDATION/*")), STAGE / "06_VALIDATION")
    counts["06_VALIDATION"] += copy_files(
        ["PAPER_A_ROUND21_FINAL_SUBMISSION_DECISION.md",
         "PAPER_A_ROUND20_FINAL_SUPERVISOR_DECISION.md",
         "PAPER_A_ROUND20_ELECTRICAL_EDGE_CONDITION_AUDIT.md",
         "PAPER_A_ROUND20_NUMERICAL_IMPACT_AND_RECOMPUTATION.md",
         "PAPER_A_ROUND20_PRE_EDIT_BOUNDARY_AUDIT.md",
         "PAPER_A_ROUND20_SPATIAL_SPECTRAL_COUNT_AUDIT.md",
         "PAPER_A_EXTENDED_NUMERICAL_VALIDATION.md",
         "PAPER_A_ROUND9_PLANE_INVARIANCE_VALIDATION.md",
         "PAPER_A_CLAIM_PROVENANCE_MATRIX.md"],
        STAGE / "06_VALIDATION" / "reports")
    counts["06_VALIDATION"] += copy_files(
        ["paper_a_study/FIGURE_5_VALIDATION_REPORT.md",
         "paper_a_study/figure_validation_report.json",
         "Paper_A_Final_Submission/static_validation.txt"],
        STAGE / "06_VALIDATION" / "reports")

    # ---- 07 DOCUMENTATION ----------------------------------------------
    counts["07_DOCUMENTATION"] = copy_files(list(DOCS.glob("07_DOCUMENTATION/*")),
                                            STAGE / "07_DOCUMENTATION")
    counts["07_DOCUMENTATION"] += copy_files(["PAPER_A_CORRECTION_HISTORY.md"],
                                             STAGE / "07_DOCUMENTATION")

    # ---- 08 FINAL OUTPUTS ----------------------------------------------
    counts["08_FINAL_OUTPUTS"] = copy_files(
        ["Paper_A_Final_Submission/MANIFEST.json",
         "Paper_A_Final_Submission/static_validation.txt",
         "PAPER_A_FINAL_SCIENTIFIC_AUDIT.md"],
        STAGE / "08_FINAL_OUTPUTS")
    counts["08_FINAL_OUTPUTS"] += copytree_allow(ROOT / "paper_a_study/figures_final",
                                                 STAGE / "08_FINAL_OUTPUTS" / "figures_final")
    counts["08_FINAL_OUTPUTS"] += copy_files(list(DOCS.glob("08_FINAL_OUTPUTS/*")),
                                             STAGE / "08_FINAL_OUTPUTS")

    # ---- 09 METADATA ----------------------------------------------------
    counts["09_ARCHIVE_METADATA"] = copy_files(list(DOCS.glob("09_ARCHIVE_METADATA/*")),
                                               STAGE / "09_ARCHIVE_METADATA")

    # ---- root files -----------------------------------------------------
    counts["root"] = 0
    # every remaining root-level report (the full audit corpus) -> documentation/audit_history
    placed = set()
    for sub in STAGE.rglob("*"):
        if sub.is_file():
            placed.add(sub.name)
    hist = STAGE / "07_DOCUMENTATION" / "audit_history"
    hist.mkdir(parents=True, exist_ok=True)
    n_hist = 0
    for md in sorted(ROOT.glob("*.md")):
        if md.name in placed:
            continue
        shutil.copy2(md, hist / md.name)
        n_hist += 1
    counts["07_DOCUMENTATION"] += n_hist
    for extra in DOCS.glob("root/*"):
        shutil.copy2(extra, STAGE / extra.name)
        counts["root"] += 1

    # ---- integrity ------------------------------------------------------
    manifest = STAGE / "09_ARCHIVE_METADATA" / "file_manifest_sha256.csv"

    def hash_tree(exclude=()):
        out = []
        for path in sorted(STAGE.rglob("*")):
            rel = path.relative_to(STAGE).as_posix()
            if path.is_file() and path.name != "SHA256SUMS.txt" and rel not in exclude:
                out.append((rel, path.stat().st_size,
                            hashlib.sha256(path.read_bytes()).hexdigest()))
        return out

    # the manifest cannot contain its own hash (it would change itself), so it is
    # excluded from its own rows and covered by SHA256SUMS.txt instead.
    rows_manifest = hash_tree(exclude={"09_ARCHIVE_METADATA/file_manifest_sha256.csv"})
    manifest.write_text("path,bytes,sha256\n"
                        + "".join(f"{p},{b},{h}\n" for p, b, h in rows_manifest))
    rows = hash_tree()                      # now includes the finished manifest
    (STAGE / "SHA256SUMS.txt").write_text(
        "".join(f"{h}  {p}\n" for p, b, h in rows))

    # ---- zip ------------------------------------------------------------
    ZIP_OUT.parent.mkdir(parents=True, exist_ok=True)
    if ZIP_OUT.exists():
        ZIP_OUT.unlink()
    with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(STAGE.rglob("*")):
            if path.is_file():
                zf.write(path, Path(NAME) / path.relative_to(STAGE))

    digest = hashlib.sha256(ZIP_OUT.read_bytes()).hexdigest()
    total = sum(1 for p in STAGE.rglob("*") if p.is_file())
    print(json.dumps(dict(stage=str(STAGE), files_total=total, per_folder=counts,
                          zip=str(ZIP_OUT), zip_bytes=ZIP_OUT.stat().st_size,
                          zip_sha256=digest,
                          built_utc=datetime.now(timezone.utc).isoformat(timespec="seconds")),
                     indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
