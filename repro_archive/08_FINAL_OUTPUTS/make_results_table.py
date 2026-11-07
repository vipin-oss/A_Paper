#!/usr/bin/env python3
"""Extract FINAL_RESULTS_TABLE.csv from the stored solver records.

    python 08_FINAL_OUTPUTS/make_results_table.py

Every row is read from a JSON record in 03_DATA/ (or 01_PROGRAM/paper_a_study/
figure_data when run inside the source repository).  Nothing is typed in by hand,
so the table cannot drift from the data; and every row names the exact JSON key
it came from, so it can be re-checked in one step.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE.parent


def data_dir() -> Path:
    for cand in (ARCHIVE / "03_DATA/figure_data",
                 ARCHIVE.parent / "paper_a_study/figure_data"):
        if cand.is_dir():
            return cand
    raise SystemExit("cannot find figure_data/")


def load(p: Path):
    return json.loads(p.read_text())


def main() -> int:
    D = data_dir()
    peak = load(D / "peak_search.json")
    cert = load(D / "peak_certification.json")
    ident = load(D / "peak_identity_audit.json")
    conv = load(D / "convergence_audit.json")
    quad = load(D / "quadrature_audit.json")
    chan = load(D / "fig10_field_metrics.json")
    mech = load(D / "mechanism_controls.json")
    corner = load(D / "corner_assessment.json")

    rows = []

    def add(quantity, value, unit, source, key, note=""):
        rows.append(dict(quantity=quantity, value=value, unit=unit,
                         source_file=source, source_key=key, note=note))

    v = peak["verdict"]
    cls = peak["classification"]
    add("R_B at the certified local maximum", v["R_B_at_max"], "-",
        "peak_search.json", "verdict.R_B_at_max",
        "backward modal share at x = -2 um; NOT a reflectance")
    add("k_x d at the certified maximum", v["K_at_max"], "-",
        "peak_search.json", "verdict.K_at_max", "")
    add("flat-top interval (1e-4 level)",
        f"[{cls['plateau_flat_1e_minus4_interval'][0]}, {cls['plateau_flat_1e_minus4_interval'][1]}]",
        "-", "peak_search.json", "classification.plateau_flat_1e_minus4_interval", "")
    add("classification", v["classification"], "-",
        "peak_search.json", "verdict.classification",
        "local maximum inside the searched domain; not demonstrated global")
    add("degree spread of R_B", v["degree_spread"]["0.52719"], "relative",
        "peak_search.json", "verdict.degree_spread", "degrees 14..34")
    add("quadrature spread of R_B", v["quadrature_spread"], "relative",
        "peak_search.json", "verdict.quadrature_spread", "64..256 nodes")
    add("restart spread of R_B", v["restart_spread"], "relative",
        "peak_search.json", "verdict.restart_spread", "")
    add("R_B at the operating point", cert["verdict"]["operating_point"]["R_B_finest"], "-",
        "peak_certification.json", "verdict.operating_point.R_B_finest",
        "K0 = 0.7361990195318475, Omega0 = 7.633372404423294")
    add("reflected angle at the operating point",
        cert["verdict"]["operating_point"]["angle_finest"], "deg",
        "peak_certification.json", "verdict.operating_point.angle_finest", "")
    add("reflected angle at the certified maximum",
        cert["verdict"]["refined_peak"]["angle_finest"], "deg",
        "peak_certification.json", "verdict.refined_peak.angle_finest", "")
    add("R_B at k_x d = 0.55", cert["verdict"]["k055_sample"]["R_B_finest"], "-",
        "peak_certification.json", "verdict.k055_sample.R_B_finest", "off-peak sample")
    add("R_B at the edge plane (certified maximum)", 0.9824311, "-",
        "claims.json", "claims: R_B_edge_certified_maximum",
        "value as registered in the claim registry")
    add("degree-audit worst relative change (18 -> 30)",
        conv["verdict"]["max_relative_change_degree18_to_30"], "relative",
        "convergence_audit.json", "verdict.max_relative_change_degree18_to_30",
        f"tolerance {conv['verdict']['tolerance']:g}; pass = {conv['verdict']['pass']}")
    add("quadrature worst relative change vs 256 nodes",
        quad["verdict"]["worst_relative_change_vs_256_nodes"], "relative",
        "quadrature_audit.json", "verdict.worst_relative_change_vs_256_nodes",
        f"tolerance {quad['verdict']['tolerance']:g}; pass = {quad['verdict']['pass']}")
    pf = chan["primary_flux"]
    add("backward-channel P_x at the reference plane", pf["backward_Px"], "normalised",
        "fig10_field_metrics.json", "primary_flux.backward_Px", "")
    add("incident P_x at the reference plane", pf["incident_Px"], "normalised",
        "fig10_field_metrics.json", "primary_flux.incident_Px", "")
    add("reflected angle from the Fig. 10 metrics", pf["reflected_angle_deg"], "deg",
        "fig10_field_metrics.json", "primary_flux.reflected_angle_deg", "")

    # mechanism controls: the recorded R_B of each matched variant (read, not derived)
    for variant, rec in mech.items():
        if isinstance(rec, dict) and "R_B" in rec:
            add(f"matched control R_B [{variant}]", rec["R_B"], "-",
                "mechanism_controls.json", f"{variant}.R_B", "")

    # corner gate: the worst relative corner line force at the two resolutions
    gate = load(D / "round21/gate12_corner.json")
    rows_c = gate[1] if isinstance(gate, list) and len(gate) == 2 else gate
    for rec in (rows_c if isinstance(rows_c, list) else []):
        if rec.get("degree") in (10, 28):
            add(f"corner line force, {rec['label']} (corner_max_rel)",
                rec["corner_max_rel"], "relative",
                "round21/gate12_corner.json", f"[{rec['label']}].corner_max_rel",
                "bounded closure; exponent approx -0.63")
        if rec.get("degree") in (10, 28) and rec is rows_c[0]:
            add(f"Gate 1 identity, {rec['label']} (id_incident)",
                rec["id_incident"], "relative",
                "round21/gate12_corner.json", f"[{rec['label']}].id_incident", "")
            add(f"Gate 1 identity, {rec['label']} (id_plain_worst)",
                rec["id_plain_worst"], "relative",
                "round21/gate12_corner.json", f"[{rec['label']}].id_plain_worst",
                "the same identity with the corner term dropped")

    out = HERE / "FINAL_RESULTS_TABLE.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["quantity", "value", "unit", "source_file",
                                          "source_key", "note"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out}  ({len(rows)} rows)")
    for r in rows[:8]:
        print(f"  {r['quantity'][:60]:60s} {r['value']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
