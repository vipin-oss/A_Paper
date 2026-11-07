#!/usr/bin/env python3
"""Refresh the authoritative Paper A submission directory.

`Paper_A_Final_Submission/` is the single authoritative manuscript tree: it
holds `main.tex`, the section files, `references.bib` and the ten vector
figures.  This script copies the *generated* material into it -- the solver, the
figure drivers, the verification suite, the figure data, the material file and
the validation records -- and refuses to run if a second `main.tex` exists
anywhere outside `archive/`, so the repository cannot drift back into two
competing manuscripts.

    python build_submission_package.py

It then writes `MANIFEST.json` (SHA-256 of every file in the package).
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Paper_A_Final_Submission"

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
    "verify_dimensions.py",
    "quasistatic_check.py",
    "flexo_control.py",
    "phase_speed_audit.py",
    "modal_flux_audit.py",
    "mechanism_controls.py",
    "corner_assessment.py",
    "peak_search.py",
    "peak_identity_audit.py",
    "claim_audit.py",
    "mutation_tests.py",
    "run_all_checks.py",
    "round18_mathematical_audit.py",
    "round18_reference_checks.py",
    "round19_tests.py",
    "round19_layout_check.py",
]

FIGURE_STEMS = [
    "fig01_dispersion", "fig02_material", "fig03_geometry", "fig04_frequency",
    "fig05_channel", "fig06_attenuation", "fig07_coupling", "fig08_boundary",
    "fig09_validation", "fig10_field",
]

REQUIRED_MANUSCRIPT = ["main.tex", "references.bib"] + [
    f"sections/{n}" for n in
    ["introduction.tex", "governing_equations.tex", "numerical_methods.tex",
     "results.tex", "discussion.tex", "conclusions.tex",
     "appendix_reproducibility.tex"]
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def need(path: Path) -> Path:
    if not path.exists():
        sys.exit(f"missing required file: {path.relative_to(ROOT)}")
    return path


def main() -> int:
    # exactly one manuscript in the repository
    stray = [p for p in ROOT.rglob("main.tex")
             if "archive" not in p.parts and OUT not in p.parents]
    if stray:
        sys.exit("second manuscript found: " + ", ".join(
            str(p.relative_to(ROOT)) for p in stray))

    for name in REQUIRED_MANUSCRIPT:
        need(OUT / name)
    for stem in FIGURE_STEMS:
        need(OUT / "figures" / f"{stem}.pdf")

    for sub in ("a0", "paper_a_study/figure_data", "validation"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)

    copied = []
    shutil.copy2(need(ROOT / "a0" / "materials.json"), OUT / "a0" / "materials.json")
    copied.append(OUT / "a0" / "materials.json")

    for name in STUDY_FILES:
        dst = OUT / "paper_a_study" / name
        shutil.copy2(need(ROOT / "paper_a_study" / name), dst)
        copied.append(dst)

    for src in sorted((ROOT / "paper_a_study" / "figure_data").iterdir()):
        if src.suffix in {".csv", ".json"}:
            dst = OUT / "paper_a_study" / "figure_data" / src.name
            shutil.copy2(src, dst)
            copied.append(dst)

    for src in sorted((ROOT / "validation").glob("*.txt")) if (ROOT / "validation").exists() else []:
        dst = OUT / "validation" / src.name
        shutil.copy2(src, dst)
        copied.append(dst)

    # Run the static validator *before* hashing: it rewrites
    # ``static_validation.txt``, and a manifest computed before that run would
    # describe a file that no longer exists on disk.
    checker = OUT / "scripts" / "static_check.py"
    if checker.exists():
        subprocess.run([sys.executable, str(checker)], cwd=OUT,
                       capture_output=True, text=True, check=False)

    manifest = {}
    for path in sorted(OUT.rglob("*")):
        if path.is_file() and path.name != "MANIFEST.json":
            manifest[str(path.relative_to(OUT))] = sha256(path)
    (OUT / "MANIFEST.json").write_text(json.dumps(
        {"files": manifest, "count": len(manifest)}, indent=2) + "\n")

    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"package: {OUT}")
    print(f"files:   {len(manifest)}")
    print(f"size:    {total/1e6:.2f} MB")
    print(f"refreshed: {len(copied)} generated files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
