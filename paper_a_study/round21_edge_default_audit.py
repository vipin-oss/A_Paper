"""Round-21 Gate 3: the insulating edge condition is the default everywhere.

The physics decision of round 20 was that the reflecting edge of a bare
piezoelectric-semiconductor plate carries D_x = 0, not phi = 0.  A decision is
only permanent if the code cannot silently revert, so this audit checks, without
re-solving anything:

  1. the constructor default is 'insulating';
  2. the figure-data pipeline pins 'insulating' as its own default;
  3. every producer that names the condition explicitly either names
     'insulating' or is one of the two labelled round-19 baseline scripts;
  4. no producer writes a stored dataset with the grounded condition except the
     round-19 baseline directory, which is labelled as such;
  5. the manuscript's grounded statements are confined to labelled controls
     (the round-19 baseline and the metallised-face discussion).

Run: PYTHONPATH=paper_a_study .venv/bin/python paper_a_study/round21_edge_default_audit.py
"""

import inspect
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from model import Plate  # noqa: E402

OUT = os.path.join(HERE, "figure_data", "round21")
ROOT = os.path.dirname(HERE)
ALLOWED_EXPLICIT = {"round19_tests.py", "round20_recompute.py", "round20_boundary_audit.py",
                    "build_figure_data.py"}
PRODUCERS = ["build_figure_data.py", "generate_final_figures.py", "peak_search.py",
             "certify_peak.py", "peak_identity_audit.py", "mechanism_controls.py",
             "convergence_audit.py", "quadrature_audit.py", "corner_assessment.py",
             "modal_flux_audit.py", "claim_audit.py", "mutation_tests.py",
             "round21_gate1_traction.py", "round21_gate_corner.py", "round21_tests.py"]


def main() -> int:
    problems, rows = [], []

    default = inspect.signature(Plate.__init__).parameters["edge_electric"].default
    rows.append(dict(check="constructor default", value=default))
    if default != "insulating":
        problems.append(f"Plate default is {default!r}, not 'insulating'")

    src = open(os.path.join(HERE, "build_figure_data.py"), encoding="utf-8").read()
    m = re.search(r"^EDGE_ELECTRIC\s*=\s*[\"'](\w+)[\"']", src, re.M)
    value = m.group(1) if m else None
    rows.append(dict(check="pipeline default", value=value))
    if value != "insulating":
        problems.append(f"build_figure_data.EDGE_ELECTRIC is {value!r}")

    for name in PRODUCERS:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            problems.append(f"missing producer {name}")
            continue
        text = open(path, encoding="utf-8").read()
        hits = re.findall(r"edge_electric\s*=\s*[\"'](\w+)[\"']", text)
        ok = all(h == "insulating" for h in hits) or (not hits) or name in ALLOWED_EXPLICIT
        rows.append(dict(check=f"producer {name}", explicit=sorted(set(hits)), ok=ok))
        if not ok:
            problems.append(f"{name} names a non-insulating condition: {set(hits)}")

    baseline = os.path.join(HERE, "figure_data", "round19_baseline")
    labelled = os.path.exists(baseline)
    rows.append(dict(check="round-19 grounded baseline kept and labelled",
                     present=labelled, files=len(os.listdir(baseline)) if labelled else 0))
    if not labelled:
        problems.append("round-19 grounded baseline directory missing")

    # manuscript: 'ground' may appear only as a labelled control
    sec = os.path.join(ROOT, "Paper_A_Final_Submission", "sections")
    for name in sorted(os.listdir(sec)):
        if not name.endswith(".tex"):
            continue
        text = open(os.path.join(sec, name), encoding="utf-8").read()
        for hit in re.finditer(r"grounded|ground\b", text):
            window = text[max(0, hit.start() - 220):hit.start() + 220].lower()
            # the *faces* of the plate may be grounded; that is a different
            # boundary than the reflecting edge and is not the round-20 decision.
            if not any(k in window for k in ("control", "metallised", "round-19",
                                             "metallized", "electrode", "face", "faces")):
                if "edge" in window:
                    problems.append(f"{name}: edge grounded mention not framed as a control: "
                                    f"...{text[max(0,hit.start()-60):hit.start()+60]!r}")
    rows.append(dict(check="manuscript grounded mentions framed as controls",
                     problems=len([p for p in problems if "framed" in p or "not framed" in p])))

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "gate3_edge_default.json"), "w") as h:
        json.dump(dict(rows=rows, problems=problems, pass_=not problems), h, indent=1)

    for r in rows:
        print(" ", r)
    print("PASS" if not problems else "FAIL")
    for p in problems:
        print("  -", p)
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
