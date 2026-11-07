#!/usr/bin/env python3
"""Build 09_ARCHIVE_METADATA/run_manifest.json from a battery log plus the
figure/audit artifacts that exist.

    python 04_REPRODUCTION/make_run_manifest.py [--log PATH]

Default log: <program>/validation/verification_log.txt (written by
paper_a_study/run_all_checks.py).  If no log is found the manifest is still
written, with status "NOT RUN IN THIS BUILD" for every step -- it never invents
a result.
"""
from __future__ import annotations

import json
import re
import hashlib
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE.parent


def find(rel: str) -> Path:
    p = ARCHIVE / rel
    if p.exists():
        return p
    repo = ARCHIVE.parent
    mapping = {"01_PROGRAM/paper_a_study/": "paper_a_study/",
               "01_PROGRAM/a0/": "a0/",
               "01_PROGRAM/validation/": "validation/",
               "01_PROGRAM/tools/": "",
               "03_DATA/figure_data/": "paper_a_study/figure_data/",
               "02_OVERLEAF/": "Paper_A_Final_Submission/",
               "08_FINAL_OUTPUTS/figures_final/": "paper_a_study/figures_final/",
               "09_ARCHIVE_METADATA/": "repro_archive/09_ARCHIVE_METADATA/"}
    for src, dst in mapping.items():
        if rel.startswith(src):
            return repo / (dst + rel[len(src):])
    return ARCHIVE / rel


# step name in the log  ->  (command, main outputs, kind)
STEPS = [
    ("dimensional and constitutive audit", "python paper_a_study/verify_dimensions.py",
     ["paper_a_study/figure_data/dimension_audit.json"], "audit"),
    ("quasistatic justification", "python paper_a_study/quasistatic_check.py",
     ["paper_a_study/figure_data/quasistatic_audit.json"], "audit"),
    ("flexoelectric control", "python paper_a_study/flexo_control.py",
     ["paper_a_study/figure_data/flexo_control.json"], "audit"),
    ("admissibility re-derivation", "python paper_a_study/reclassify_csv.py",
     ["paper_a_study/figure_data/fig02_material_parameter_sweep.csv"], "audit"),
    ("figure data and figure files", "(inline)", [
        "paper_a_study/figure_data/fig01_dispersion_velocity_attenuation.csv",
        "paper_a_study/figure_data/figure_panel_sources.json"], "data"),
    ("phase-speed and e.m. reconciliation", "python -m paper_a_study.phase_speed_audit",
     ["paper_a_study/figure_data/phase_speed_audit.json"], "audit"),
    ("modal-flux rescaling proof", "python -m paper_a_study.modal_flux_audit",
     ["paper_a_study/figure_data/modal_flux_audit.json"], "audit"),
    ("mechanism matched controls", "python -m paper_a_study.mechanism_controls",
     ["paper_a_study/figure_data/mechanism_controls.json"], "audit"),
    ("corner assessment and regression", "python -m paper_a_study.corner_assessment",
     ["paper_a_study/figure_data/corner_assessment.json"], "audit"),
    ("certified peak (four fixed wavenumbers)", "python -m paper_a_study.certify_peak",
     ["paper_a_study/figure_data/peak_certification.json"], "result"),
    ("peak search and classification", "python -m paper_a_study.peak_search",
     ["paper_a_study/figure_data/peak_search.json"], "result"),
    ("peak identity and artefact audit", "python -m paper_a_study.peak_identity_audit",
     ["paper_a_study/figure_data/peak_identity_audit.json"], "audit"),
    ("spectral convergence", "python paper_a_study/convergence_audit.py",
     ["paper_a_study/figure_data/convergence_audit.json",
      "paper_a_study/figure_data/fig09_validation_convergence.csv"], "audit"),
    ("quadrature sufficiency", "python paper_a_study/quadrature_audit.py",
     ["paper_a_study/figure_data/quadrature_audit.json"], "audit"),
    ("unit and scientific tests", "python -m unittest paper_a_study.test_model",
     ["paper_a_study/test_model.py (52 tests)"], "test"),
    ("natural boundary data identity", "python paper_a_study/round21_gate1_traction.py",
     ["paper_a_study/figure_data/round21/gate1_traction_identity.json"], "gate"),
    ("corner line force gate", "python paper_a_study/round21_gate_corner.py",
     ["paper_a_study/figure_data/round21/gate12_corner.json"], "gate"),
    ("insulating edge default audit", "python paper_a_study/round21_edge_default_audit.py",
     ["paper_a_study/figure_data/round21/gate3_edge_default.json"], "gate"),
    ("round-21 regression tests", "python -m unittest paper_a_study.round21_tests",
     ["paper_a_study/round21_tests.py"], "test"),
    ("claim registry and stale guard", "python paper_a_study/claim_audit.py",
     ["paper_a_study/figure_data/claim_audit.json"], "test"),
    ("gate mutation tests", "python paper_a_study/mutation_tests.py",
     ["paper_a_study/figure_data/mutation_tests.json"], "test"),
    ("LaTeX static validation", "python scripts/static_check.py (cwd = manuscript)",
     ["02_OVERLEAF/static_validation.txt"], "manuscript"),
    ("LaTeX build", "pdflatex main && bibtex main && pdflatex main ×2",
     ["02_OVERLEAF/main.pdf"], "manuscript"),
]

# steps that are not part of run_all_checks.py
EXTRA = [
    ("figure data build", "cd paper_a_study && python build_figure_data.py",
     ["paper_a_study/figure_data/*.csv", "paper_a_study/figure_data/*.json"], "data"),
    ("figure generation", "cd paper_a_study && python generate_final_figures.py",
     ["paper_a_study/figures_final/fig01..fig10.{pdf,png,svg}"], "figure"),
    ("parameter manifest", "python 04_REPRODUCTION/make_parameter_manifest.py",
     ["09_ARCHIVE_METADATA/parameter_manifest.json"], "metadata"),
    ("archive build", "python 01_PROGRAM/tools/build_repro_archive.py",
     ["PAPER_A_COMPLETE_REPRODUCIBILITY_ARCHIVE.zip"], "metadata"),
]

# format A (console):  "[PASS] peak search and classification  (3832.3s)"
# format B (log):      "PASS  peak search and classification         3832.3s exit=0"
# format C (log, no time): "PASS  figure data and figure files           "
# format D (log, skip):   "SKIP  LaTeX build                            no TeX engine found"
LINE_A = re.compile(r"^\[(?P<status>PASS|FAIL|SKIP)\]\s+(?P<name>.+?)\s*(?:\((?P<t>[0-9.]+)s\))?$")
LINE_B = re.compile(r"^(?P<status>PASS|FAIL|SKIP)\s{2}(?P<name>\S.*?)\s+(?P<t>[0-9.]+)s\s+exit=")
LINE_C = re.compile(r"^(?P<status>PASS|FAIL|SKIP)\s{2}(?P<name>\S.*?)\s*$")
LINE_D = re.compile(r"^(?P<status>SKIP)\s{2}(?P<name>\S.*?)\s{2,}\S")


def parse_log(path: Path) -> dict:
    out = {}
    if not path.exists():
        return out
    for raw in path.read_text().splitlines():
        line = raw.rstrip()
        m = (LINE_A.match(line.strip()) or LINE_B.match(line)
             or LINE_D.match(line) or LINE_C.match(line))
        if m:
            gd = m.groupdict()
            secs = gd.get("t")
            out[gd["name"].strip()] = dict(status=gd["status"],
                                           seconds=float(secs) if secs else None)
    return out


def size_of(rel: str):
    for pattern_ok in (True,):
        p = find(rel)
        if p.is_file():
            return dict(bytes=p.stat().st_size,
                        sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        if "*" in rel or "{" in rel:
            return None
    return None


def main() -> int:
    log = find("01_PROGRAM/validation/verification_log.txt")
    if not log.exists():
        log = HERE / "logs/battery_2026-11-07.log"
    parsed = parse_log(Path(log))

    def rel(p: Path) -> str:
        p = Path(p).resolve()
        for base in (ARCHIVE, Path(__file__).resolve().parent.parent.parent):
            try:
                return p.relative_to(base.resolve()).as_posix()
            except ValueError:
                continue
        return p.name
    steps = []
    for name, cmd, outputs, kind in STEPS:
        rec = parsed.get(name, {})
        steps.append(dict(step=name, kind=kind, command=cmd, outputs=outputs,
                          status=rec.get("status", "NOT RUN IN THIS BUILD"),
                          seconds=rec.get("seconds")))
    doc = dict(
        title="Paper A run manifest",
        generated_by="04_REPRODUCTION/make_run_manifest.py",
        generated_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        battery_log=rel(Path(log)),
        battery_log_sha256=(hashlib.sha256(Path(log).read_bytes()).hexdigest()
                            if Path(log).exists() else None),
        interpreter="Python 3.11.2",
        dependencies=dict(numpy="2.4.6", scipy="1.17.1", matplotlib="3.11.2"),
        seeds="none used (fully deterministic)",
        environment_note=("TeX engine absent in the build environment: the LaTeX build "
                          "step is recorded as SKIP, never as PASS."),
        steps=steps,
        not_in_battery=[dict(step=n, command=c, outputs=o, kind=k) for n, c, o, k in EXTRA],
        artifacts={o: size_of(o) for _, _, outs, _ in STEPS for o in outs
                   if size_of(o) is not None},
    )
    out = (ARCHIVE / "09_ARCHIVE_METADATA/run_manifest.json"
           if (ARCHIVE / "01_PROGRAM").is_dir() else HERE.parent / "09_ARCHIVE_METADATA/run_manifest.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=1) + "\n")
    n_pass = sum(1 for s in steps if s["status"] == "PASS")
    n_skip = sum(1 for s in steps if s["status"] == "SKIP")
    n_fail = sum(1 for s in steps if s["status"] == "FAIL")
    print(f"wrote {out}\n  steps {len(steps)}: {n_pass} PASS, {n_skip} SKIP, {n_fail} FAIL\n  log: {log}")
    for s in steps:
        secs = "" if s["seconds"] is None else f"{s['seconds']:.1f}s"
        print(f"  {s['status']:8s} {secs:>9s}  {s['step']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
