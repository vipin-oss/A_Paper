#!/usr/bin/env python3
"""Run the complete verification battery and write one log.

    python paper_a_study/run_all_checks.py

Each check is executed as a subprocess so that a failure in one does not hide
the result of the others.  The log is written to `validation/` at the repository
root and is copied into the submission package by `build_submission_package.py`.

The battery is:

1. unit and scientific tests      (test_model)
2. dimensional / constitutive     (verify_dimensions)
3. quasistatic justification      (quasistatic_check)
4. flexoelectric control          (flexo_control)
5. admissibility re-derivation    (reclassify_csv, no re-solving)
6. figure-data integrity          (this file, inline)
7. phase-speed / e.m. reconciliation (phase_speed_audit, 0 = text agrees)
8. modal-flux rescaling proof     (modal_flux_audit)
9. mechanism matched controls     (mechanism_controls)
10. corner assessment + regression (corner_assessment)
11. LaTeX static validation       (Paper_A_Final_Submission/scripts/static_check.py)

TeX/BibTeX compilation is attempted only if an engine is present; otherwise the
log records explicitly that no engine was found.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "paper_a_study"
SUB = ROOT / "Paper_A_Final_Submission"
VALID = ROOT / "validation"
PY = sys.executable

RESULTS: list[tuple[str, bool, str]] = []


def run(name: str, cmd: list[str], cwd: Path, timeout: int = 1800) -> bool:
    t0 = datetime.now()
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          timeout=timeout)
    dt = (datetime.now() - t0).total_seconds()
    tail = (proc.stdout or "").strip().splitlines()[-6:]
    ok = proc.returncode == 0
    RESULTS.append((name, ok, f"{dt:.1f}s exit={proc.returncode}"))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  ({dt:.1f}s)")
    for line in tail:
        print("      " + line)
    if not ok and proc.stderr:
        print("      stderr: " + proc.stderr.strip().splitlines()[-1])
    return ok


def figure_data_chk() -> bool:
    """Every CSV the figures read exists and has the expected row counts."""
    expected = {
        "fig01_dispersion_velocity_attenuation.csv": 155,
        "fig02_material_parameter_sweep.csv": 130,
        "fig04_frequency_reflection.csv": 50,
        "fig07_coupling_sensitivity.csv": 95,
        "fig09_validation_convergence.csv": None,
    }
    data = STUDY / "figure_data"
    ok = True
    for name, rows in expected.items():
        path = data / name
        if not path.exists():
            print(f"      missing {name}")
            ok = False
            continue
        n = len(path.read_text().strip().splitlines()) - 1
        if rows is not None and n != rows:
            print(f"      {name}: {n} rows, expected {rows}")
            ok = False
    for stem in ["fig01_dispersion", "fig02_material", "fig03_geometry",
                 "fig04_frequency", "fig05_channel", "fig06_attenuation",
                 "fig07_coupling", "fig08_boundary", "fig09_validation",
                 "fig10_field"]:
        if not (SUB / "figures" / f"{stem}.pdf").exists():
            print(f"      missing figure {stem}.pdf")
            ok = False
    RESULTS.append(("figure data and figure files", ok, ""))
    print(f"[{'PASS' if ok else 'FAIL'}] figure data and figure files")
    return ok


def main() -> int:
    VALID.mkdir(exist_ok=True)
    print(f"verification run {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print()

    run("unit and scientific tests",
        [PY, "-m", "unittest", "paper_a_study.test_model"], ROOT, 1800)
    run("dimensional and constitutive audit",
        [PY, "paper_a_study/verify_dimensions.py"], ROOT, 600)
    run("quasistatic justification",
        [PY, "paper_a_study/quasistatic_check.py"], ROOT, 600)
    run("flexoelectric control",
        [PY, "paper_a_study/flexo_control.py"], ROOT, 900)
    run("admissibility re-derivation",
        [PY, "paper_a_study/reclassify_csv.py"], ROOT, 600)
    figure_data_chk()
    run("phase-speed and e.m. reconciliation",
        [PY, "-m", "paper_a_study.phase_speed_audit"], ROOT, 600)
    run("modal-flux rescaling proof",
        [PY, "-m", "paper_a_study.modal_flux_audit"], ROOT, 900)
    run("mechanism matched controls",
        [PY, "-m", "paper_a_study.mechanism_controls"], ROOT, 1800)
    run("corner assessment and regression",
        [PY, "-m", "paper_a_study.corner_assessment"], ROOT, 1200)
    run("LaTeX static validation",
        [sys.executable, "scripts/static_check.py"], SUB, 300)

    engine = next((e for e in ("pdflatex", "latexmk", "tectonic", "xelatex",
                               "lualatex") if shutil.which(e)), None)
    if engine:
        run(f"LaTeX build ({engine})", [engine, "-interaction=nonstopmode",
                                        "main.tex"], SUB, 900)
    else:
        RESULTS.append(("LaTeX build", None, "no TeX engine found"))
        print("[SKIP] LaTeX build: no TeX engine found in this environment")

    ok = all(r[1] is not False for r in RESULTS)
    lines = [
        f"Paper A verification run {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "=" * 60, "",
    ]
    for name, res, note in RESULTS:
        tag = "PASS" if res else ("SKIP" if res is None else "FAIL")
        lines.append(f"{tag:5s} {name:38s} {note}")
    lines += ["", f"OVERALL: {'PASS' if ok else 'FAIL'}",
              "", "TeX compilation: " + ("executed" if engine else
              "NOT EXECUTED - no engine available; source is statically validated only")]
    (VALID / "verification_log.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[-6:]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
