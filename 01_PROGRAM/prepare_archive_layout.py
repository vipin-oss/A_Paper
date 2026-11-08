#!/usr/bin/env python3
"""Re-create the source-repository layout inside the unpacked archive.

    cd 01_PROGRAM && python prepare_archive_layout.py
    cd 01_PROGRAM && python paper_a_study/run_all_checks.py

The programme was written in a repository whose root holds `paper_a_study/`,
`a0/` and `Paper_A_Final_Submission/` side by side.  The archive separates the
programme (`01_PROGRAM`) from the manuscript (`02_OVERLEAF`), so a handful of
scripts -- `run_all_checks.py`, `claim_audit.py`, `mutation_tests.py`,
`round19_layout_check.py`, `round21_edge_default_audit.py` -- look for a sibling
`Paper_A_Final_Submission/` that does not exist until this script makes it.

The shim is **symlinks only**: no manuscript file is duplicated, so there is one
and only one copy of `main.tex` and of the figures in the archive.  Re-running is
idempotent; `--remove` deletes the shim again.
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

PROGRAM = Path(__file__).resolve().parent          # .../01_PROGRAM
ARCHIVE = PROGRAM.parent
MANUSCRIPT = ARCHIVE / "02_OVERLEAF"
SHIM = PROGRAM / "Paper_A_Final_Submission"

ENTRIES = ["main.tex", "references.bib", "sections", "figures", "scripts/static_check.py"]

#: (link path relative to 01_PROGRAM, target relative to the link's parent).
#: tests and audits read paper_a_study/figure_data/, which the archive keeps in
#: 03_DATA/figure_data; the link makes both views the same bytes.
DATA_LINK = ("paper_a_study/figure_data", "../../03_DATA/figure_data")
#: the figure tests read paper_a_study/figures_final/, which the archive keeps in
#: 08_FINAL_OUTPUTS/figures_final.  NOTE: regenerating figures therefore writes into
#: the shipped folder -- that is intended (it is the same artifact), and it will change
#: the PDF/PNG SHA-256 values recorded in 09_ARCHIVE_METADATA/.
FIG_LINK = ("paper_a_study/figures_final", "../../08_FINAL_OUTPUTS/figures_final")


def remove() -> int:
    for link, _ in (DATA_LINK, FIG_LINK):
        dst = PROGRAM / link
        if dst.is_symlink():
            dst.unlink()
            print(f"removed link {dst}")
    if SHIM.is_symlink() or SHIM.is_file():
        SHIM.unlink()
    elif SHIM.exists():
        shutil.rmtree(SHIM)
    print(f"removed {SHIM}")
    return 0


def build() -> int:
    if not MANUSCRIPT.is_dir():
        print(f"ERROR: no manuscript at {MANUSCRIPT}")
        return 2
    if SHIM.exists() and not SHIM.is_dir():
        SHIM.unlink()
    SHIM.mkdir(exist_ok=True)
    (SHIM / "scripts").mkdir(exist_ok=True)
    for name in ENTRIES:
        src = MANUSCRIPT / name
        if not src.exists():
            print(f"  missing in the manuscript folder, not linked: {name}")
            continue
        dst = SHIM / name
        if dst.is_symlink() or dst.exists():
            dst.unlink()
        os.symlink(os.path.relpath(src.resolve(), dst.parent.resolve()), dst)
        print(f"  {dst.relative_to(PROGRAM)} -> {os.readlink(dst)}")
    for link, target in (DATA_LINK, FIG_LINK):
        dst = PROGRAM / link
        if not dst.exists():
            os.symlink(target, dst)
            print(f"  {link} -> {target}")
        else:
            print(f"  {link} already exists (left alone)")

    print(f"\nshim ready: {SHIM}\nrun the battery from {PROGRAM}:\n"
          f"  python paper_a_study/run_all_checks.py")
    return 0


if __name__ == "__main__":
    if "--remove" in sys.argv[1:]:
        raise SystemExit(remove())
    raise SystemExit(build())
