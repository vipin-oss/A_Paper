#!/usr/bin/env python3
"""Final audit of the unpacked archive (requirement 10).

    python 04_REPRODUCTION/audit_archive.py [--root DIR]

Checks, and prints one line each:
  A. every required document exists and is non-empty
  B. no build-machine absolute path appears in any text file
  C. no junk (``__pycache__``, ``*.pyc``, ``*.tmp``, ``.DS_Store``) anywhere
  D. every ``\\input`` / ``\\includegraphics`` / ``\\bibliography`` target exists
  E. every figure PDF referenced by the manuscript has a non-zero size
  F. no duplicate artifact with the *same name but different bytes* (version conflict)
  G. no file larger than 40 MB, and any file over 5 MB is listed for the reader
  H. SHA256SUMS.txt (if present) agrees with the files on disk

Exit code 0 iff every check passes.  Nothing is repaired: differences are reported.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

REQUIRED = [
    "ARCHIVE_README.md", "FINAL_PACKAGE_STATUS.md", "SHA256SUMS.txt",
    "01_PROGRAM/README_PROGRAM.md", "01_PROGRAM/requirements.txt",
    "02_OVERLEAF/README_OVERLEAF.md", "02_OVERLEAF/main.tex", "02_OVERLEAF/references.bib",
    "03_DATA/README_DATA.md", "03_DATA/DATA_DICTIONARY.md",
    "04_REPRODUCTION/REPRODUCE_FROM_SCRATCH.md", "04_REPRODUCTION/RUN_ORDER.md",
    "04_REPRODUCTION/REPRODUCTION_TEST_RESULT.md",
    "05_DERIVATIONS/README_DERIVATIONS.md",
    "06_VALIDATION/README_VALIDATION.md", "06_VALIDATION/VALIDATION_MATRIX.md",
    "07_DOCUMENTATION/PROJECT_OVERVIEW.md", "07_DOCUMENTATION/MODEL_DESCRIPTION.md",
    "07_DOCUMENTATION/NUMERICAL_METHOD.md", "07_DOCUMENTATION/FIGURE_PROVENANCE.md",
    "07_DOCUMENTATION/CHANGELOG.md", "07_DOCUMENTATION/KNOWN_LIMITATIONS.md",
    "08_FINAL_OUTPUTS/README_FINAL_OUTPUTS.md", "08_FINAL_OUTPUTS/FINAL_RESULTS_TABLE.csv",
    "09_ARCHIVE_METADATA/run_manifest.json", "09_ARCHIVE_METADATA/parameter_manifest.json",
    "09_ARCHIVE_METADATA/file_manifest_sha256.csv",
    "09_ARCHIVE_METADATA/BUILD_RECORD.md",
]

TEXT_SUFFIX = {".md", ".txt", ".json", ".csv", ".py", ".sh", ".tex", ".bib", ".cfg",
               ".toml", ".yml", ".yaml"}
JUNK_NAMES = {"__pycache__", ".DS_Store", ".ipynb_checkpoints"}
JUNK_SUFFIX = {".pyc", ".pyo", ".tmp", ".swp", ".bak", ".orig"}
#: folders whose contents are *unedited historical records* (round reports, older
#: study outputs).  Old session paths and generic file names occur there by nature;
#: they are reported as WARN, not FAIL, because rewriting them would falsify the
#: record.  Nothing in the archive reads from these folders.
HISTORICAL = ("07_DOCUMENTATION/audit_history/", "03_DATA/results_legacy/",
              "03_DATA/figure_data/round19_baseline/", "03_DATA/figure_data/round21/",
              "01_PROGRAM/feasibility/", "01_PROGRAM/a0/results/")
#: independent sub-studies (A0 feasibility, a0r, a0s) legitimately reuse generic file
#: names such as requirements.txt / run_checks.py for *different* programs.
STUDY_FOLDERS = ("01_PROGRAM/a0/", "01_PROGRAM/feasibility/")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    args = ap.parse_args()
    root = Path(args.root).resolve()
    files = sorted(p for p in root.rglob("*") if p.is_file())
    fails = []

    def is_hist(rel: str) -> bool:
        return any(rel.startswith(h) for h in HISTORICAL)

    def report(ok, label, detail="", warn_only=False):
        tag = "PASS" if ok else ("WARN" if warn_only else "FAIL")
        print(f"[{tag}] {label}" + (f"  {detail}" if detail else ""))
        if not ok and not warn_only:
            fails.append(label)
        return ok

    print(f"auditing {root}  ({len(files)} files)\n")

    # A -- required documents
    missing = [r for r in REQUIRED if not (root / r).is_file() or (root / r).stat().st_size == 0]
    report(not missing, "A. required documents", "" if not missing else f"missing: {missing}")

    # B -- absolute build paths
    pat = re.compile(r"(/home/[A-Za-z0-9._-]+/|/Users/[A-Za-z0-9._-]+/|/tmp/[A-Za-z0-9._-]+/|"
                     r"[A-Za-z]:\\\\Users\\\\)")
    hits, hist_hits = [], []
    for p in files:
        if p.suffix.lower() not in TEXT_SUFFIX:
            continue
        try:
            txt = p.read_text(errors="ignore")
        except OSError:
            continue
        for m in pat.finditer(txt):
            rel = p.relative_to(root).as_posix()
            (hist_hits if is_hist(rel) else hits).append(f"{rel}: {m.group(0)}")
    report(not hits, "B. no absolute build-machine paths in live files",
           "" if not hits else f"{len(hits)} hit(s): {hits[:5]}")
    if hist_hits:
        print(f"[WARN] B'. historical records contain old session paths "
              f"({len(hist_hits)} hit(s), left unedited): {hist_hits[:3]}")

    # C -- junk
    junk = [str(p.relative_to(root)) for p in files
            if p.name in JUNK_NAMES or p.suffix in JUNK_SUFFIX
            or any(part in JUNK_NAMES for part in p.parts)]
    report(not junk, "C. no junk files", "" if not junk else f"{junk[:5]}")

    # D -- manuscript paths
    tex = root / "02_OVERLEAF"
    bad_refs = []
    if (tex / "main.tex").is_file():
        for f in sorted(tex.glob("*.tex")) + sorted((tex / "sections").glob("*.tex")):
            body = f.read_text(errors="ignore")
            for m in re.finditer(r"\\input\{([^}]+)\}", body):
                if not (tex / (m.group(1) if m.group(1).endswith(".tex") else m.group(1) + ".tex")).is_file():
                    bad_refs.append(f"{f.name}: \\input{{{m.group(1)}}}")
            for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", body):
                tgt = tex / m.group(1)
                if not (tgt.is_file() or tgt.with_suffix(".pdf").is_file()
                        or tgt.with_suffix(".png").is_file()):
                    bad_refs.append(f"{f.name}: \\includegraphics{{{m.group(1)}}}")
            for m in re.finditer(r"\\bibliography\{([^}]+)\}", body):
                if not (tex / (m.group(1) + ".bib")).is_file():
                    bad_refs.append(f"{f.name}: \\bibliography{{{m.group(1)}}}")
    report(not bad_refs, "D. manuscript \\input / \\includegraphics / \\bibliography targets",
           "" if not bad_refs else f"{bad_refs[:5]}")

    # E -- figure PDFs non-trivial
    figs = sorted((tex / "figures").glob("*.pdf")) if (tex / "figures").is_dir() else []
    tiny = [f.name for f in figs if f.stat().st_size < 5000]
    report(bool(figs) and not tiny, "E. manuscript figures present and non-trivial",
           f"{len(figs)} PDF(s)" + (f", suspiciously small: {tiny}" if tiny else ""))

    # F -- same name, different bytes
    by_name = defaultdict(list)
    for p in files:
        if p.name in {"SHA256SUMS.txt", "file_manifest_sha256.csv"}:
            continue
        by_name[p.name].append(p)
    conflicts, hist_conflicts = [], []
    for name, group in by_name.items():
        if len(group) < 2:
            continue
        hashes = {hashlib.sha256(p.read_bytes()).hexdigest() for p in group}
        if len(hashes) > 1:
            entry = f"{name}: {[str(p.relative_to(root)) for p in group]}"
            rels = [str(p.relative_to(root)) for p in group]
            # a clash is only a *version conflict* if it involves two or more
            # live (non-historical, non-sub-study) copies; one live copy plus
            # copies in a baseline/study folder is a documented structure.
            live = [r for r in rels if not (is_hist(r) or r.startswith(STUDY_FOLDERS))]
            (conflicts if len(live) > 1 else hist_conflicts).append(entry)
    report(not conflicts, "F. no conflicting artifacts outside historical folders",
           "" if not conflicts else f"{conflicts[:4]}")
    if hist_conflicts:
        print(f"[WARN] F'. generic file names repeat inside historical/baseline folders "
              f"or across independent sub-studies "
              f"({len(hist_conflicts)}): {hist_conflicts[:3]}")

    # G -- size
    big = [(p.relative_to(root).as_posix(), p.stat().st_size)
           for p in files if p.stat().st_size > 5 * 1024 * 1024]
    too_big = [b for b in big if b[1] > 40 * 1024 * 1024]
    report(not too_big, "G. no file over 40 MB",
           f"over 5 MB: {big}" if big else "no file over 5 MB")

    # H -- SHA256SUMS
    sums = root / "SHA256SUMS.txt"
    if sums.is_file():
        bad, checked = [], 0
        for line in sums.read_text().splitlines():
            if not line.strip():
                continue
            try:
                h, rel = line.split("  ", 1)
            except ValueError:
                bad.append(f"malformed: {line[:60]}")
                continue
            p = root / rel
            if not p.is_file():
                bad.append(f"missing: {rel}")
                continue
            checked += 1
            if hashlib.sha256(p.read_bytes()).hexdigest() != h:
                bad.append(f"hash mismatch: {rel}")
        report(not bad, "H. SHA256SUMS.txt agrees with disk",
               f"{checked} file(s) verified" + ("" if not bad else f"; {bad[:5]}"))
    else:
        report(False, "H. SHA256SUMS.txt agrees with disk", "SHA256SUMS.txt absent")

    print()
    if fails:
        print(f"AUDIT: FAIL ({len(fails)} check(s): {fails})")
        return 1
    print("AUDIT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
