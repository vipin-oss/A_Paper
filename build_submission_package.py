#!/usr/bin/env python3
"""Assemble the final Paper A submission directory.

Copies the manuscript, the ten vector figures, the solver, the figure-driving
scripts, the verification suite, the material file and every CSV/JSON the
figures are drawn from into a single self-contained directory that reproduces
the paper from a clean extraction.

    python build_submission_package.py

The script refuses to run if any required file is missing, so a silent partial
package cannot be produced.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Paper_A_Submission_2026-11-06"

STUDY_FILES = [
    "__init__.py",
    "model.py",
    "build_figure_data.py",
    "certify_peak.py",
    "reclassify_csv.py",
    "generate_final_figures.py",
    "figure_style.py",
    "make_atlas.py",
    "test_model.py",
]

FIGURE_STEMS = [
    "fig01_dispersion",
    "fig02_material",
    "fig03_geometry",
    "fig04_frequency",
    "fig05_channel",
    "fig06_attenuation",
    "fig07_coupling",
    "fig08_boundary",
    "fig09_validation",
    "fig10_field",
]

SECTIONS = [
    "introduction.tex",
    "governing_equations.tex",
    "numerical_methods.tex",
    "results.tex",
    "discussion.tex",
    "conclusions.tex",
    "appendix_reproducibility.tex",
]


def need(path: Path) -> Path:
    if not path.exists():
        sys.exit(f"missing required file: {path.relative_to(ROOT)}")
    return path


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "a0").mkdir(parents=True)
    (OUT / "paper_a_study" / "figure_data").mkdir(parents=True)
    (OUT / "Paper_A_LaTeX" / "sections").mkdir(parents=True)
    (OUT / "Paper_A_LaTeX" / "figures").mkdir(parents=True)
    (OUT / "Paper_A_LaTeX" / "scripts").mkdir(parents=True)

    copied: list[Path] = []

    def put(src: Path, dst: Path) -> None:
        shutil.copy2(need(src), dst)
        copied.append(dst)

    # material source of truth
    put(ROOT / "a0" / "materials.json", OUT / "a0" / "materials.json")

    # study code
    for name in STUDY_FILES:
        put(ROOT / "paper_a_study" / name, OUT / "paper_a_study" / name)

    # data actually read by the plotting script
    for src in sorted((ROOT / "paper_a_study" / "figure_data").iterdir()):
        if src.suffix in {".csv", ".json"}:
            put(src, OUT / "paper_a_study" / "figure_data" / src.name)

    # manuscript
    put(ROOT / "Paper_A_LaTeX" / "main.tex", OUT / "Paper_A_LaTeX" / "main.tex")
    put(ROOT / "Paper_A_LaTeX" / "references.bib",
        OUT / "Paper_A_LaTeX" / "references.bib")
    for name in SECTIONS:
        put(ROOT / "Paper_A_LaTeX" / "sections" / name,
            OUT / "Paper_A_LaTeX" / "sections" / name)
    put(ROOT / "Paper_A_LaTeX" / "scripts" / "static_check.py",
        OUT / "Paper_A_LaTeX" / "scripts" / "static_check.py")
    put(ROOT / "Paper_A_LaTeX" / "static_validation.txt",
        OUT / "Paper_A_LaTeX" / "static_validation.txt")
    for stem in FIGURE_STEMS:
        put(ROOT / "Paper_A_LaTeX" / "figures" / f"{stem}.pdf",
            OUT / "Paper_A_LaTeX" / "figures" / f"{stem}.pdf")

    total = sum(p.stat().st_size for p in copied)
    print(f"copied {len(copied)} files, {total/1e6:.2f} MB")
    print("output:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
