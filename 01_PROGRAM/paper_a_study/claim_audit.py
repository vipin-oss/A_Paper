#!/usr/bin/env python3
"""Trace every quantitative claim in the manuscript to its stored source.

Three gates, all driven by ``paper_a_study/claims.json``:

1. Registry agreement.  Each claim lists the literal LaTeX strings that carry it
   and the number each string denotes.  The script requires that every string is
   still present in the file it is registered against, and that the number it
   denotes agrees with the registry value.  A number edited in the manuscript
   without editing the registry fails here.
2. Stale-value guard.  Deprecated values, whose reappearance would mean an
   outdated scientific statement, must not occur anywhere in the manuscript.
2b. Source agreement.  Three of the registered numbers are checked against the
   stored solver records as well as against the text: the headline against
   ``peak_search.json`` (which must be classified as a local maximum, and which
   must beat every sample of its own coarse raster), the incident wavenumber
   against the identity audit (which must be the *incident* root, neither the
   branch parameter nor the backward target), and the degree spread against the
   recorded gradings.  A registry that agrees with the manuscript but not with
   the data fails here.
3. Ordering and coverage.  Figures must be cited in numerical order on first
   citation, and every claim flagged ``in_abstract`` must appear in the abstract.

The script does not decide whether a claim is true --- that is the job of the
numerical suite --- only that manuscript and registry agree.

Usage:  python paper_a_study/claim_audit.py [--root Paper_A_Final_Submission]
Writes  figure_data/claim_audit.json
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "figure_data"
REGISTRY = HERE / "claims.json"


def read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parent / "Paper_A_Final_Submission"))
    ap.add_argument("--registry", default=str(REGISTRY),
                    help="registry to audit; the mutation suite points this at a copy")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    reg = json.loads(Path(args.registry).read_text())
    problems: list[str] = []
    rows: list[dict] = []

    for claim in reg["claims"]:
        for token in claim["tokens"]:
            text = read(root, token["file"])
            count = text.count(token["text"])
            if count == 0:
                problems.append(f"{claim['id']}: {token['text']!r} missing from {token['file']}")
                continue
            rel = abs(token["value"] - claim["value"]) / abs(claim["value"])
            ok = rel <= claim["tolerance_rel"]
            rows.append(dict(claim=claim["id"], file=token["file"], text=token["text"],
                             registered=claim["value"], denoted=token["value"],
                             relative_difference=rel, tolerance=claim["tolerance_rel"],
                             occurrences=count, pass_=ok))
            if not ok:
                problems.append(f"{claim['id']}: {token['text']!r} in {token['file']} "
                                f"denotes {token['value']} but the registry says "
                                f"{claim['value']} ({rel:.1e} > {claim['tolerance_rel']:.1e})")

    all_files = ["main.tex"] + sorted(str(p.relative_to(root))
                                      for p in (root / "sections").glob("*.tex"))
    for dep in reg["deprecated"]:
        for f in all_files:
            if dep["text"] in read(root, f):
                problems.append(f"deprecated value {dep['text']!r} reappeared in {f}: {dep['why']}")

    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}",
                         read(root, "main.tex"), re.S).group(1)
    for claim in reg["claims"]:
        if claim["in_abstract"]:
            hit = any(tok["text"] in abstract for tok in claim["tokens"] if tok["file"] == "main.tex")
            if not hit:
                problems.append(f"{claim['id']}: flagged in_abstract but absent from the abstract")

    # --- source agreement (gate 2b) -------------------------------------
    by_id = {c["id"]: c for c in reg["claims"]}
    rec = json.loads((DATA / "peak_search.json").read_text())
    ident = json.loads((DATA / "peak_identity_audit.json").read_text())
    refs = json.loads((HERE / "reference_constants.json").read_text())
    KB0 = float(refs["derived"]["KB0"])
    cls = rec["classification"]
    source_rows: list[dict] = []

    def agree(claim_id, data_value, tol, what):
        """Compare a stored number with the registry.

        A claim carrying ``"kind": "bound"`` is an inequality: the manuscript
        quotes an upper bound and the gate accepts any executed value at or
        below it.  This is the round-11 repair of defect D9: the two refinement
        spreads are differences of nearly equal numbers sitting on the
        round-off floor, so an equality test at 1 % fired on float noise while
        the headline moved by 8e-13.
        """
        claim = by_id.get(claim_id)
        if claim is None:
            problems.append(f"{claim_id}: missing from the registry ({what})")
            return
        if claim.get("kind") == "bound":
            value = float(data_value)
            ok = 0.0 < value <= claim["value"]
            source_rows.append(dict(claim=claim_id, data=value, what=what,
                                    bound=claim["value"], relative_difference=None,
                                    tolerance=None, pass_=ok))
            if not ok:
                problems.append(f"{claim_id}: the registered bound is {claim['value']} but the "
                                f"stored {what} is {value} "
                                f"({'not computed' if value <= 0 else 'above the bound'})")
            return
        rel = abs(float(data_value) - claim["value"]) / abs(claim["value"])
        source_rows.append(dict(claim=claim_id, data=data_value, what=what,
                                relative_difference=rel, tolerance=tol, pass_=rel <= tol))
        if rel > tol:
            problems.append(f"{claim_id}: registry says {claim['value']} but the stored "
                            f"{what} is {data_value} ({rel:.1e} > {tol:.1e})")

    if cls["classification"] != "numerically_resolved_sampled_local_maximum":
        problems.append(f"peak_search.json: classification is {cls['classification']!r}, "
                        "not 'numerically_resolved_sampled_local_maximum'")
    agree("R_B_certified_maximum", cls["R_B_reported"], 1e-4, "search-record headline")
    coarse_max = max(r["R_B"] for r in rec["coarse"])
    source_rows.append(dict(claim="coarse raster cannot reach the maximum",
                            data=coarse_max, what="max over rec.coarse",
                            relative_difference=(cls["R_B_reported"] - coarse_max)
                            / cls["R_B_reported"], tolerance=1e-3, pass_=True))
    if coarse_max >= cls["R_B_reported"]:
        problems.append("peak_search.json: a coarse sample reaches the reported maximum - "
                        "the maximum was read off a grid, not certified")
    if not (rec["domain"][0] < cls["K_at_max"] < rec["domain"][1]):
        problems.append("peak_search.json: the located maximum lies outside the scanned domain")

    peak_case = ident["cases"]["peak"]
    k_inc = float(peak_case["K_incident"][0])
    agree("incident_wavenumber_peak", k_inc, 1e-4, "identity-audit incident root")
    if abs(k_inc - KB0) < 0.2:
        problems.append(f"incident_wavenumber_peak: {k_inc} is within 0.2 of KB0 = {KB0}; "
                        "the case would have been labelled with the backward target")
    if abs(k_inc - cls["K_reported"]) < 1e-4:
        problems.append("incident_wavenumber_peak: the incident root equals the branch "
                        "parameter; the two are distinct quantities and are reported apart")
    # Round-11 defect D9: both refinement spreads are registered as upper
    # bounds and are tested against every entry the executed record contains,
    # not against one hand-picked key.
    for key, value in sorted(rec["verdict"]["degree_spread"].items()):
        agree("degree_stability_peak", value, 1e-2,
              f"search-record degree spread at K = {key}")
    agree("quadrature_stability_peak", rec["verdict"]["quadrature_spread"], 1e-2,
          "search-record quadrature spread (degree 22, four nodes rules)")

    # Round-11 defect D11: the largest frequency shift the coupling produces on
    # the plotted branch.  The text quotes it; the figure data carry it.
    f01 = list(csv.DictReader((DATA / "fig01_dispersion_velocity_attenuation.csv").open()))
    base_f = {float(r["K"]): float(r["frequency_GHz"]) for r in f01 if float(r["eta"]) == 0.0}
    shift = 0.0
    for r in f01:
        if float(r["eta"]) == 0.0:
            continue
        k = float(r["K"])
        if k in base_f:
            # the CSV stores GHz; the claim is registered in kHz
            shift = max(shift, abs(float(r["frequency_GHz"]) - base_f[k]) * 1e6)
    agree("coupling_frequency_shift_max", shift, 2e-3,
          "largest coupling-induced frequency shift on the plotted branch (kHz)")

    # Gate 2c: the edge-plane share must be the same number in every producer.
    # This is the round-9 defect: peak_search.py used a single-mode decay and
    # disagreed with mechanism_controls.py by 1.96 percentage points.
    ps_edge = None
    for row in rec.get("degree", []):
        if abs(row["K"] - cls["K_reported"]) < 1e-12 and row.get("degree") == 22:
            ps_edge = float(row["R_B_edge"])
            break
    if ps_edge is None:
        problems.append("peak_search.json: no degree-22 row at the reported wavenumber")
    else:
        agree("R_B_edge_certified_maximum", ps_edge, 1e-4, "search-record edge-plane share")
        mc = json.loads((DATA / "mechanism_controls.json").read_text())
        mc_edge = float([r for r in mc["branch_consistent_H_sweep"]["refined_peak"]
                         if r["eta"] == 0.0][0]["R_B_edge"])
        rel = abs(mc_edge - ps_edge) / ps_edge
        source_rows.append(dict(claim="cross-script edge fraction", data=mc_edge,
                                what="mechanism_controls vs peak_search",
                                relative_difference=rel, tolerance=1e-6, pass_=rel <= 1e-6))
        if rel > 1e-6:
            problems.append(f"cross-script edge fraction: peak_search says {ps_edge}, "
                            f"mechanism_controls says {mc_edge} ({rel:.1e} apart) - "
                            "the two scripts are not using the same plane transform")
        # the three tabulated edge shares, each against its own stored record
        for claim_id, case in (("R_B_edge_operating_point", "operating_point"),
                               ("R_B_edge_k055", "k055_sample")):
            # a four-decimal share cannot be compared more tightly than its
            # rounding (0.023151 -> 0.0232 is a 2e-3 relative step)
            agree(claim_id, float(mc[case]["no_coupling"]["R_B_edge"]), 5e-3,
                  f"mechanism_controls edge share ({case}, H = 0)")

    text = read(root, "sections/results.tex")
    order = [int(m.group(1)) for m in re.finditer(r"\\[cC]ref\{fig:fig(\d\d)\}", text)]
    firsts: list[int] = []
    for n in order:
        if n not in firsts:
            firsts.append(n)
    if firsts != sorted(firsts):
        problems.append(f"figures first cited out of order: {firsts}")

    print(f"claims registered: {len(reg['claims'])}   tokens checked: {len(rows)}")
    print(f"deprecated values guarded: {len(reg['deprecated'])}")
    print(f"figure first-citation order: {firsts}")
    print(f"source-agreement rows: {len(source_rows)} "
          f"({sum(1 for r in source_rows if r['pass_'])} passing)")
    print("PASS" if not problems else "FAIL")
    for p in problems:
        print("  -", p)
    # The record is written only when the real manuscript is audited.  The
    # mutation harness runs this script against a mutated *copy* (--root); if the
    # copy's verdict were written here it would overwrite the delivered record
    # with a FAIL produced on purpose.
    real_tree = Path(args.root).resolve() == (HERE.parent / "Paper_A_Final_Submission").resolve()
    if real_tree:
        DATA.mkdir(parents=True, exist_ok=True)
        (DATA / "claim_audit.json").write_text(json.dumps(
            dict(rows=rows, source_rows=source_rows, figure_order=firsts, problems=problems,
                 verdict="PASS" if not problems else "FAIL"), indent=2))
    else:
        print("  (mutation run: the delivered record is not overwritten)")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
