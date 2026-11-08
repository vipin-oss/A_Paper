#!/usr/bin/env python3
"""Sync Paper A figure-final artifacts into the LaTeX project and update hashes."""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STUDY_FIGS = ROOT / "paper_a_study" / "figures_final"
STUDY_DATA = ROOT / "paper_a_study" / "figure_data"
LATEX_FIGS = ROOT / "Paper_A_LaTeX" / "figures"
LATEX_DATA = ROOT / "Paper_A_LaTeX" / "figure_data"
RESULTS = ROOT / "paper_a_study" / "results"

STEM_DATA = {
    "fig01_dispersion": "fig01_dispersion_velocity_attenuation.csv",
    "fig02_material": "fig02_material_parameter_sweep.csv",
    "fig03_geometry": "fig03_geometry_sweep.csv",
    "fig04_frequency": "fig04_frequency_reflection.csv",
    "fig05_channel": "fig05_channel_power.csv",
    "fig06_attenuation": "fig06_attenuation_distance.csv",
    "fig07_coupling": "fig07_coupling_sensitivity.csv",
    "fig08_boundary": "fig08_boundary_sensitivity.csv",
    "fig09_validation": "fig09_validation_convergence.csv",
    "fig10_field": "fig10_field_metrics.json",
}
STEM_RESULT_SVG = [
    "fig01_dispersion",
    "fig02_material",
    "fig05_channel",
    "fig06_attenuation",
    "fig07_coupling",
    "fig10_field",
]
STEMS = [
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
EXTENSIONS = ["pdf", "png", "svg"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sync_figure_files() -> None:
    for stem in STEMS:
        for ext in EXTENSIONS:
            source = STUDY_FIGS / f"{stem}.{ext}"
            target = LATEX_FIGS / f"{stem}.{ext}"
            if source.exists():
                shutil.copy2(source, target)
            else:
                print(f"missing figure source: {source}")

    for stem, name in STEM_DATA.items():
        source = STUDY_DATA / name
        target = LATEX_DATA / name
        if source.exists():
            shutil.copy2(source, target)
        else:
            print(f"missing data source: {source}")

    for stem in STEM_RESULT_SVG:
        source = STUDY_FIGS / f"{stem}.svg"
        target = RESULTS / f"{stem}.svg"
        if source.exists():
            shutil.copy2(source, target)
        else:
            print(f"missing result source: {source}")


def update_manifest() -> None:
    entries = []
    for stem in STEMS:
        for ext in EXTENSIONS:
            path = LATEX_FIGS / f"{stem}.{ext}"
            if path.exists():
                entries.append(
                    {
                        "file": f"{stem}.{ext}",
                        "bytes": path.stat().st_size,
                        "sha256": sha256(path),
                    }
                )
    LATEX_DATA.joinpath("figure_manifest.json").write_text(
        json.dumps(entries, indent=2) + "\n"
    )


def update_panel_sources() -> None:
    panel_sources_path = LATEX_DATA / "figure_panel_sources.json"
    if panel_sources_path.exists():
        payload = json.loads(panel_sources_path.read_text())
    else:
        payload = {"figures": []}

    panels = {
        item.get("figure"): item.get("panels", [])
        for item in payload.get("figures", [])
    }
    sources = {
        item.get("figure"): item.get("data_source")
        for item in payload.get("figures", [])
    }

    figures = []
    for stem in STEMS:
        entry = {
            "figure": stem,
            "data_source": STEM_DATA[stem],
            "panels": panels.get(stem, []),
        }
        for ext in EXTENSIONS:
            path = STUDY_FIGS / f"{stem}.{ext}"
            if path.exists():
                entry[ext] = {
                    "file": str(path),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
        figures.append(entry)

    payload = {"figures": figures}
    panel_sources_path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    sync_figure_files()
    update_manifest()
    update_panel_sources()
    print("Paper A figure-final assets synced to LaTeX project.")


if __name__ == "__main__":
    main()
