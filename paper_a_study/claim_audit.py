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
3. Ordering and coverage.  Figures must be cited in numerical order on first
   citation, and every claim flagged ``in_abstract`` must appear in the abstract.

The script does not decide whether a claim is true --- that is the job of the
numerical suite --- only that manuscript and registry agree.

Usage:  python paper_a_study/claim_audit.py [--root Paper_A_Final_Submission]
Writes  figure_data/claim_audit.json
"""
from __future__ import annotations

import argparse
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
    args = ap.parse_args()
    root = Path(args.root).resolve()

    reg = json.loads(REGISTRY.read_text())
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
    print("PASS" if not problems else "FAIL")
    for p in problems:
        print("  -", p)
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "claim_audit.json").write_text(json.dumps(
        dict(rows=rows, figure_order=firsts, problems=problems,
             verdict="PASS" if not problems else "FAIL"), indent=2))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
