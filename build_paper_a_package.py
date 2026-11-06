#!/usr/bin/env python3
"""Create the complete, integrity-checked Paper A review package.

This script only copies and fingerprints existing artifacts. It does not rerun
the mathematical model and does not modify any source file.
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "PAPER_A_COMPLETE_RESEARCH_PACKAGE.zip"

# Exact repository sources included in the archive. Caches, bytecode caches,
# virtual environments, downloaded publisher PDFs and hidden private sources are
# deliberately omitted; their absence is stated explicitly below.
ROOT_REPORTS = [
    "PAPER_A_RESEARCH_REPORT.md",
    "PAPER_A_FINAL_SCIENTIFIC_CHECK.md",
    "PAPER_A_BLUEPRINT_V2_1.md",
    "PAPER_A_A0R_BACKWARD_WAVE_FEASIBILITY.md",
    "PAPER_A_A0R_DECISION.md",
    "PAPER_A_A0R_NOVELTY_COMPARISON.md",
    "PAPER_A_A0S_H_SENSITIVITY.md",
    "PAPER_A_A0S_MODEL_SELECTION.md",
    "PAPER_A_A0S_OPERATING_REGIME.md",
    "PAPER_A_A0_CONSTITUTIVE_CHECK.md",
    "PAPER_A_A0_DISPERSION_FEASIBILITY.md",
    "PAPER_A_A0_MATERIALS.md",
    "PAPER_A_A0_PRIOR_ART.md",
]
DIRECTORIES = ["a0", "a0r", "a0s", "paper_a_study"]
PYTHON_ROOT_FILES = ["a0/requirements.txt", "build_paper_a_package.py"]

EXCLUDED = sorted(
    {
        "a0/cache/",
        "a0/__pycache__/",
        "a0r/cache/",
        "a0r/__pycache__/",
        "a0s/cache/",
        "a0s/__pycache__/",
        "a0s/private_sources/",
        "paper_a_study/cache/",
        "paper_a_study/__pycache__/",
        ".venv/",
        "*.py[cod]",
        "*.npz",
        "*.npy",
    }
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def select_files() -> list[str]:
    files: set[str] = set(ROOT_REPORTS)
    files.update(PYTHON_ROOT_FILES)
    for directory in DIRECTORIES:
        for path in (ROOT / directory).rglob("*"):
            if path.is_file():
                rel = path.relative_to(ROOT).as_posix()
                # Preserve all source, result, protocol, report and script
                # artifacts while excluding caches and bytecode.
                parts = path.relative_to(ROOT).parts
                if any(part.startswith("__pycache__") or part == "cache" for part in parts):
                    continue
                if rel.endswith((".pyc", ".pyo", ".npz", ".npy")):
                    continue
                files.add(rel)
    return sorted(files)


def main() -> None:
    selected = select_files()
    absent = [name for name in ROOT_REPORTS if not (ROOT / name).exists()]
    if absent:
        raise RuntimeError(f"Required reports absent before packaging: {absent}")

    lines: list[str] = []
    lines.append("# Paper A Complete Research Package")
    lines.append("")
    lines.append("**Fixed topic:** Negative reflection of guided waves in a flexoelectric piezoelectric-semiconductor plate with carrier–strain-gradient coupling.")
    lines.append("")
    lines.append("This package is a static review bundle of the existing repository results. It contains no new model, no manuscript, no retraining and no rerun. `paper_a_study/` is the focused current result; `a0/`, `a0r/` and `a0s/` are the completed historical controls and their retained evidence.")
    lines.append("")
    lines.append("## Read in this order")
    lines.append("")
    lines.append("1. `PAPER_A_RESEARCH_REPORT.md` — governing equations, boundary conditions, model specialization, numerical results, validation and limitations.")
    lines.append("2. `PAPER_A_FINAL_SCIENTIFIC_CHECK.md` — the five-point backward-reflection, geometry, H comparison, novelty and figure/validation audit.")
    lines.append("3. `PAPER_A_BLUEPRINT_V2_1.md` — the preserved research blueprint and decision history.")
    lines.append("4. `a0/`, `a0r/`, `a0s/` — historical source/material, complex dispersion and operating-regime records, including their protocol files and numerical evidence.")
    lines.append("5. `a0/materials.json`, `a0/requirements.txt`, `a0s/SOURCES.md`, and `a0s/STRONG_VALIDATION.md` — sourced material parameters, definitions, provenance and historical validation.")
    lines.append("")
    lines.append("## Exact reproduction commands")
    lines.append("")
    lines.append("From the repository root containing this package (after extracting it, restore the top-level directory structure exactly as shown):")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 -m venv .venv")
    lines.append(".venv/bin/python -m pip install -r a0/requirements.txt")
    lines.append("")
    lines.append("# Current focused model, figures and all reported numerical results")
    lines.append("OPENBLAS_NUM_THREADS=1 .venv/bin/python -m paper_a_study.run_study")
    lines.append("")
    lines.append("# Current focused unit tests")
    lines.append("OPENBLAS_NUM_THREADS=1 .venv/bin/python -m unittest paper_a_study.test_model -v")
    lines.append("")
    lines.append("# Historical regression tests, retained as review evidence")
    lines.append("OPENBLAS_NUM_THREADS=1 .venv/bin/python -m unittest discover -s a0 -p 'test_*.py' -v")
    lines.append("OPENBLAS_NUM_THREADS=1 .venv/bin/python -m unittest discover -s a0r -p 'test_*.py' -v")
    lines.append("OPENBLAS_NUM_THREADS=1 .venv/bin/python -m unittest discover -s a0s -p 'test_*.py' -v")
    lines.append("```")
    lines.append("")
    lines.append("The focused run is deterministic in this environment and takes approximately 45 seconds. It regenerates all four SVG figures, all CSV/JSON result files and the 22-entry `paper_a_study/results/sha256.json` manifest.")
    lines.append("")
    lines.append("## Current-result figures and their source data")
    lines.append("")
    lines.append("| Figure | Exact file | Generated from |")
    lines.append("|---|---|---|")
    lines.append("| Matched dispersion, H shift and temporal damping | `paper_a_study/results/dispersion_and_H.svg` | `paper_a_study/results/dispersion.csv`, `paper_a_study/results/H_sensitivity.csv` |")
    lines.append("| Solved edge channel power and signed energy angle | `paper_a_study/results/edge_conversion.svg` | `paper_a_study/results/frequency_scan.csv` |")
    lines.append("| Matched H parameter effect | `paper_a_study/results/H_parameter_effect.svg` | `paper_a_study/results/H_sensitivity.csv` |")
    lines.append("| Computed incident and backward channel beam | `paper_a_study/results/computed_channel_beam.svg` | `paper_a_study/results/beam_validation.json` and the 17/25-node Hermite angular-spectrum solve in `paper_a_study/run_study.py` |")
    lines.append("")
    lines.append("The original-resolution PNG previews generated by the same runner are retained at `paper_a_study/cache/*.png`. The canonical report figures are the four SVG files above.")
    lines.append("")
    lines.append("## Material parameters and literature references")
    lines.append("")
    lines.append("### Sourced classical ZnO constants")
    lines.append("")
    lines.append("`a0/materials.json` contains the classical six-constant elastic tensor, piezoelectric coefficients, absolute permittivities, density, SI charge and Boltzmann definitions, and an explicit `NOT_SOURCED` block. The classical constants originate from Zhang et al., Applied Mathematics and Mechanics 46(7), 1331–1346 (2025), DOI `10.1007/s10483-025-3272-7`. That source attributes them to Yang's book; this package does not add a sample-specific measurement audit.")
    lines.append("")
    lines.append("### Carrier inputs")
    lines.append("")
    lines.append("Room-temperature bulk Hall concentration `n0 = 2e18 m^-3` and mobility `M = 0.0175 m^2/(V s)` come from the light-green high-resistivity sector of Suscavage et al., *High Quality Hydrothermal ZnO Crystals*, 4, 287–292 (1999), DOI `10.1557/S109257830000260X`. The retained diffusivity `Dn = 0.000455 m^2/s` is derived from `Dn/M = 0.026 V`, equivalent to about 301.7 K, and is not a measured diffusivity of that Hall sample. The bulk-to-released-film, Hall-to-drift and DC-to-GHz transfers remain assumptions.")
    lines.append("")
    lines.append("### Synthetic inputs")
    lines.append("")
    lines.append("The strain-gradient length `ell = 50 nm`, strain-gradient tensor `A = ell^2 C (x) I`, static flexoelectric coefficient `f_3333 = 1 nC/m`, and all H values are explicitly synthetic. They are not measured ZnO constants. `H* = 4.0097064373759543e-22 J m` is defined at fixed reference `nref = 1e19 m^-3`.")
    lines.append("")
    lines.append("### Literature and access limitations")
    lines.append("")
    lines.append("| Work | Role / status |")
    lines.append("|---|---|")
    lines.append("| Wei et al., *Dynamic flexoelectric effect in semiconductors: A study on wave propagation*, Applied Mathematical Modelling 150A, 116353 (2026), [DOI: 10.1016/j.apm.2025.116353](https://doi.org/10.1016/j.apm.2025.116353) | Structural reference only. Complete governing equations were not accessible; its numerical material is Nb-doped SrTiO3, not ZnO. |")
    lines.append("| Fang et al., *Flexoelectricity and size effects on SH surface waves in a nanoscale piezoelectric semiconductor layered medium*, Applied Mathematical Modelling 141, 115928 (2025), [DOI: 10.1016/j.apm.2025.115928](https://doi.org/10.1016/j.apm.2025.115928) | Preview only. It is a ZnO/diamond Love-type SH layer problem, not a complete plate baseline for this model. |")
    lines.append("| Qu et al., International Journal of Engineering Science 208, 104165 (2025), [DOI: 10.1016/j.ijengsci.2024.104165](https://doi.org/10.1016/j.ijengsci.2024.104165) | Metadata/preview only. The relevant appendix was inaccessible, so novelty over its published constitutive equations remains **provisional**; no equivalence or absence claim is made. |")
    lines.append("| Zhang et al., DOI `10.1007/s10483-025-3272-7` | Accessible equations, Table 1 and Appendix A; source of classical ZnO constants. |")
    lines.append("| Suscavage et al., DOI `10.1557/S109257830000260X` | Bulk Hall concentration/mobility evidence; not released-film GHz transport. |")
    lines.append("| NIST CODATA SI definitions: [e](https://physics.nist.gov/cgi-bin/cuu/Value?e), [k](https://physics.nist.gov/cgi-bin/cuu/Value?k), [epsilon0](https://physics.nist.gov/cgi-bin/cuu/Value?ep0) | Exact SI definitions used in `a0/materials.json`. |")
    lines.append("")
    lines.append("No publisher-copyrighted full text is included. The URLs above are the external review access points; the complete governing model could not be reproduced from them.")
    lines.append("")
    lines.append("## Governing equations and boundary conditions")
    lines.append("")
    lines.append("The complete equations, definitions, H-derived changes, face boundary-term changes, corner functional, assumptions and limitations are in Sections 1–4 of `PAPER_A_RESEARCH_REPORT.md`. The focused model is an explicitly specified static/local electric-enthalpy ZnO specialization. Its sole additional coupling is `Delta H = nu H : g`, where `nu = Delta n` and `g = grad eps`. It is **not** a claimed transcription of Wei or Fang.")
    lines.append("")
    lines.append("The plate occupies `x < 0`, `-d/2 < z < d/2`, and is infinite in `y`. The faces and the edge are mechanically free, electrically grounded at `phi = 0`, and carrier-blocking. The edge calculation uses the weak free-edge traction/double-traction, grounding and blocking conditions, including the natural corner line-force functional. Complex `k_x` is selected by decay into `x < 0`; propagating roots are selected by physical power direction. All 182 outgoing modes are included at degree 22.")
    lines.append("")
    lines.append("## Validation artifacts")
    lines.append("")
    lines.append("- `paper_a_study/results/validation.json` — 143/143 focused numerical checks, including explicit unresolved non-numerical requirements.")
    lines.append("- `paper_a_study/test_model.py` — 18/18 focused tests, including temporal energy balance, independent strong roots, classical recovery, edge convergence and weak boundary reconstruction.")
    lines.append("- `paper_a_study/results/sha256.json` — 22-file fingerprint manifest for the focused source, material and result artifacts.")
    lines.append("- `paper_a_study/results/independent_roots.csv`, `classical_validation.csv`, `convergence.csv`, `edge_weak_residuals.csv`, `temporal_energy_balance.csv` — independent numerical-validation datasets.")
    lines.append("- `a0/results/validation.json`, `a0r/results/validation.json`, `a0s/results/validation.json`, `a0s/results/final_audit.json` — historical check ledgers and audit output.")
    lines.append("- `a0r/results/retained_a0_sha256.json` and `a0s/results/retained_sha256.json` — retained historical source/result fingerprints.")
    lines.append("- `a0s/audit_outputs.py`, `a0r/run_checks.py` and `a0/run_checks.py` — retained validation/audit scripts.")
    lines.append("")
    lines.append("## File inventory")
    lines.append("")
    lines.append("| Directory / file | Contents and purpose |")
    lines.append("|---|---|")
    lines.append("| `PAPER_A_RESEARCH_REPORT.md` | Complete focused mathematical report. |")
    lines.append("| `PAPER_A_FINAL_SCIENTIFIC_CHECK.md` | Final five-point scientific check and terminology correction. |")
    lines.append("| `PAPER_A_BLUEPRINT_V2_1.md` | Preserved V2.1 blueprint and decision record. |")
    lines.append("| `PAPER_A_A0_*.md` | A0 source, constitutive, dispersion and feasibility reports. |")
    lines.append("| `PAPER_A_A0R_*.md` | A0-R decision, backward-wave feasibility and novelty-comparison records. |")
    lines.append("| `PAPER_A_A0S_*.md` | A0-S model, operating-regime and synthetic-H reports. |")
    lines.append("| `a0/materials.json` | Sourced ZnO constants, SI definitions, synthetic-input declarations and provenance. |")
    lines.append("| `a0/requirements.txt` | Pinned Python dependencies used by all retained scripts. |")
    lines.append("| `a0/constitutive_check.py`, `a0/dispersion.py`, `a0/run_checks.py`, `a0/test_a0.py` | A0 constitutive checks, dispersion calculation, runner and tests. |")
    lines.append("| `a0/results/` | A0 dispersion CSV/SVG, convergence, synthetic-H sensitivity and validation. |")
    lines.append("| `a0r/complex_dispersion.py`, `a0r/run_checks.py`, `a0r/test_a0r.py`, `a0r/protocol.json` | A0-R complex temporal/spatial dispersion code and protocol. |")
    lines.append("| `a0r/results/` | A0-R temporal/spatial CSV/SVG, scenario summaries, material probes, convergence and validation. |")
    lines.append("| `a0s/dispersion_screen.py`, `a0s/run_checks.py`, `a0s/audit_outputs.py`, `a0s/test_a0s.py`, `a0s/protocol.json` | A0-S operating-regime screen, runner, independent audit and tests. |")
    lines.append("| `a0s/results/` | A0-S screening, validation, matched controls, independent propagator, audit and summary datasets. |")
    lines.append("| `a0s/SOURCES.md`, `a0s/STRONG_VALIDATION.md` | Historical source and strong-validation records. |")
    lines.append("| `paper_a_study/model.py` | Focused 2D plane-strain plate/edge model, temporal/spatial generators, independent propagators, energy balance and weak edge reconstruction. |")
    lines.append("| `paper_a_study/run_study.py` | Deterministic focused runner that generates all four figures and focused CSV/JSON evidence. |")
    lines.append("| `paper_a_study/test_model.py` | Focused unit-test suite. |")
    lines.append("| `paper_a_study/__init__.py` | Package marker. |")
    lines.append("| `paper_a_study/results/` | Four canonical SVG figures, all figure/result datasets, protocol and fingerprints. |")
    lines.append("| `build_paper_a_package.py` | Packaging and integrity-check script. It performs no research calculation. |")
    lines.append("")
    lines.append("## Explicit missing or omitted files")
    lines.append("")
    lines.append("| Omitted item | Reason |")
    lines.append("|---|---|")
    lines.append("| Publisher full text of Wei, Fang or Qu | Access was not available; no full-text copy was retained. The package states this explicitly rather than reproducing inaccessible equations. |")
    lines.append("| `a0/cache/`, `a0r/cache/`, `a0s/cache/` | Generated PNG/log scratch and historical QA previews; the corresponding CSV/SVG source data are retained. Focused PNG previews are included under `paper_a_study/cache/` because they are the original-resolution figure renderings. |")
    lines.append("| `a0*/__pycache__/` and `*.pyc` | Python bytecode caches, regenerable from source. |")
    lines.append("| `.venv/` | Environment-specific virtual environment, regenerable from `a0/requirements.txt`. |")
    lines.append("| `a0s/private_sources/` and `a0*/private_sources/` | Not present in this repository; no private publisher material was retained. |")
    lines.append("| `*.npz` / `*.npy` | No large modal arrays were committed; the CSV/JSON datasets and reproducible scripts contain the same reported results. |")
    lines.append("| Any production solver or production-solver modification | None was used or supplied. The historical packages are isolated research scripts. |")
    lines.append("| Final manuscript | The task explicitly requires no manuscript. |")
    lines.append("")
    lines.append("## Integrity checks")
    lines.append("")
    lines.append("`build_paper_a_package.py` verifies that every selected file exists, that no selected file is outside the repository root, that the ZIP opens, and that the retained SHA-256 manifests match. It also writes `PACKAGE_SHA256.txt`, one `sha256` line per file in package path order.")
    lines.append("")
    lines.append("The focused report reports 143/143 numerical checks, 18/18 focused tests, and 50/50 retained historical regression tests. These counts apply to the current focused model and results, not to the inaccessible published baselines.")
    lines.append("")
    lines.append("## Result scope")
    lines.append("")
    lines.append("The reported 2.315% backward-channel return is an isolated-channel self-power at 2 μm from the edge in an explicitly specified 2D plane-strain grounded model. It is a model-level negative edge conversion, not ordinary reflection or retroreflection. It is not a verified Wei/Fang reproduction, a calibrated ZnO prediction, a resolved pointwise corner stress, or an experimental device result. The H coupling remains provisional with respect to Qu et al.")
    lines.append("")

    readme = "\n".join(lines) + "\n"
    (ROOT / "PACKAGE_README.md").write_text(readme)
    files = sorted(set(selected) | {"PACKAGE_README.md"})

    if ARCHIVE.exists():
        ARCHIVE.unlink()
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for rel in files:
            path = ROOT / rel
            if not path.is_file():
                raise RuntimeError(f"Package source missing: {rel}")
            if not path.resolve().is_relative_to(ROOT.resolve()):
                raise RuntimeError(f"Refusing path outside repository root: {rel}")
            archive.write(path, rel)

    # Verify archive integrity, file list and SHA-256 manifests.
    with zipfile.ZipFile(ARCHIVE) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"ZIP test failed at: {bad}")
        names = set(archive.namelist())
        for rel in files:
            if rel not in names:
                raise RuntimeError(f"Missing ZIP entry: {rel}")
        if len(names) != len(files):
            raise RuntimeError("Unexpected ZIP entry count")

    # Retained manifests must match the included files.
    for manifest_rel, paths in [
        ("a0r/results/retained_a0_sha256.json", None),
        ("a0s/results/retained_sha256.json", None),
        ("paper_a_study/results/sha256.json", None),
    ]:
        manifest = json.loads((ROOT / manifest_rel).read_text())
        for rel, digest in manifest.items():
            actual = sha256(ROOT / rel)
            if actual != digest:
                raise RuntimeError(f"SHA256 mismatch for {rel} in {manifest_rel}")

    manifest_lines = []
    for rel in files:
        manifest_lines.append(f"{sha256(ROOT / rel)}  {rel}")
    (ROOT / "PACKAGE_SHA256.txt").write_text("\n".join(manifest_lines) + "\n")

    # Add the generated manifest itself as a final integrity record.
    with zipfile.ZipFile(ARCHIVE, "a", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr("PACKAGE_SHA256.txt", "\n".join(manifest_lines) + "\n")

    # Final verification after manifest insertion.
    with zipfile.ZipFile(ARCHIVE) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"Final ZIP test failed at: {bad}")
        names = set(archive.namelist())
        if len(names) != len(files) + 1 or "PACKAGE_SHA256.txt" not in names:
            raise RuntimeError("Final ZIP entry mismatch")

    total = sum((ROOT / rel).stat().st_size for rel in files)
    print(f"Created {ARCHIVE}")
    print(f"Files: {len(files)} plus PACKAGE_SHA256.txt; uncompressed payload: {total:,} bytes")
    print("ZIP integrity: PASS")
    print("Retained SHA-256 manifests: PASS")


if __name__ == "__main__":
    main()
