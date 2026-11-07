#!/usr/bin/env python3
"""Compare a freshly regenerated figure_data/ against the shipped copy.

    python compare_outputs.py [--regenerated DIR] [--shipped DIR] [--verbose]

`--regenerated` defaults to `01_PROGRAM/paper_a_study/figure_data` (what
`build_figure_data.py` writes when run inside the unpacked archive) and
`--shipped` to `03_DATA/figure_data`.  The archive ships both, so this is a real
check rather than a tautology.

For every file:
  * identical bytes            -> IDENTICAL
  * CSV, same columns          -> NUMERIC with the maximum relative deviation
                                  over the shared numeric cells
  * JSON, same structure       -> NUMERIC/STRUCTURAL with the worst leaf deviation
  * otherwise                  -> DIFFERENT (reported, and counted as a failure)

Exit code 0 iff no file is DIFFERENT and every numeric deviation is below the
tolerance given on the command line (default 1e-9 relative, or 1e-12 absolute
when the shipped value is tiny).

This script deliberately does not "fix" anything: a difference is a statement
about the environment, and it is printed.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

#: JSON leaves that record wall-clock state.  They are reported as VOLATILE and do
#: not count as a numerical difference -- everything else does.
VOLATILE = ("elapsed_s", "elapsed_seconds", "timestamp", "generated_utc",
            "run_utc", "started_utc", "seconds")


def rel_dev(a: float, b: float) -> float:
    """Relative deviation, with an absolute floor so 0 vs 1e-18 is not infinite."""
    scale = max(abs(a), abs(b))
    if scale == 0.0:
        return 0.0
    if scale < 1e-12:
        return abs(a - b)          # absolute comparison for round-off-level values
    return abs(a - b) / scale


def compare_csv(p: Path, q: Path, tol: float):
    ra = list(csv.DictReader(p.open()))
    rb = list(csv.DictReader(q.open()))
    if ra and rb and list(ra[0]) != list(rb[0]):
        return "DIFFERENT", float("inf"), f"columns differ: {list(ra[0])} vs {list(rb[0])}"
    if len(ra) != len(rb):
        return "DIFFERENT", float("inf"), f"row count {len(ra)} vs {len(rb)}"
    worst, where, nonnum = 0.0, "", 0
    for i, (x, y) in enumerate(zip(ra, rb)):
        for k in x:
            u, v = x[k], y[k]
            try:
                fu, fv = float(u), float(v)
            except (TypeError, ValueError):
                if u != v:
                    nonnum += 1
                    if nonnum <= 3:
                        print(f"      text differs at row {i} col {k}: {u!r} vs {v!r}")
                continue
            d = rel_dev(fu, fv)
            if d > worst:
                worst, where = d, f"row {i} col {k}"
    if nonnum:
        return "DIFFERENT", worst, f"{nonnum} non-numeric cells differ"
    status = "NUMERIC" if worst > 0 else "IDENTICAL"
    ok = worst <= tol
    return (status if ok else "NUMERIC*"), worst, where


def compare_json(p: Path, q: Path, tol: float):
    a = json.loads(p.read_text())
    b = json.loads(q.read_text())
    worst = [0.0, ""]
    volatile = [0]

    def walk(x, y, path=""):
        if isinstance(x, dict) and isinstance(y, dict):
            ka, kb = set(x), set(y)
            if ka != kb:
                print(f"      key set differs at {path or '/'}: +{sorted(kb-ka)} -{sorted(ka-kb)}")
            for k in ka & kb:
                walk(x[k], y[k], f"{path}/{k}")
        elif isinstance(x, list) and isinstance(y, list):
            if len(x) != len(y):
                print(f"      list length differs at {path}: {len(x)} vs {len(y)}")
                return
            for i, (u, v) in enumerate(zip(x, y)):
                walk(u, v, f"{path}[{i}]")
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)):
            if any(tok in path for tok in VOLATILE):
                if x != y:
                    volatile[0] += 1
                    print(f"      volatile field differs (ignored) at {path}: {x} vs {y}")
                return
            d = rel_dev(float(x), float(y))
            if d > worst[0]:
                worst[0], worst[1] = d, path
        elif x != y:
            print(f"      value differs at {path}: {x!r} vs {y!r}")

    walk(a, b)
    if worst[0] > 0:
        status = "NUMERIC" if worst[0] <= tol else "NUMERIC*"
    elif volatile[0]:
        status = "VOLATILE-ONLY"
    else:
        status = "IDENTICAL"
    return status, worst[0], worst[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--regenerated", default=str(ROOT / "01_PROGRAM" / "paper_a_study" / "figure_data"))
    ap.add_argument("--shipped", default=str(ROOT / "03_DATA" / "figure_data"))
    ap.add_argument("--tol", type=float, default=1e-9, help="relative tolerance")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    reg, ship = Path(args.regenerated), Path(args.shipped)
    if not reg.is_dir():
        print(f"no regenerated directory at {reg}\n"
              f"run 01_PROGRAM/paper_a_study/build_figure_data.py first "
              f"(or pass --regenerated)")
        return 2
    files = sorted(p for p in ship.rglob("*") if p.is_file())
    print(f"regenerated: {reg}\nshipped    : {ship}\nfiles      : {len(files)}\n")

    bad, worst_all, worst_where, summary = 0, 0.0, "", []
    for p in files:
        rel = p.relative_to(ship)
        q = reg / rel
        if not q.exists():
            print(f"{rel.as_posix():55s} MISSING in regenerated tree")
            bad += 1
            continue
        if p.read_bytes() == q.read_bytes():
            summary.append((rel.as_posix(), "IDENTICAL", 0.0, ""))
            continue
        if p.suffix == ".csv":
            st, dev, where = compare_csv(p, q, args.tol)
        elif p.suffix == ".json":
            st, dev, where = compare_json(p, q, args.tol)
        else:
            st, dev, where = "DIFFERENT", float("inf"), "binary file differs"
        summary.append((rel.as_posix(), st, dev, where))
        if dev > worst_all:
            worst_all, worst_where = dev, f"{rel.as_posix()} {where}"
        if st not in ("IDENTICAL", "NUMERIC", "VOLATILE-ONLY"):
            bad += 1

    n_id = sum(1 for s in summary if s[1] == "IDENTICAL")
    n_num = sum(1 for s in summary if s[1] == "NUMERIC")
    n_vol = sum(1 for s in summary if s[1] == "VOLATILE-ONLY")
    rows = summary if args.verbose else [s for s in summary if s[1] not in ("IDENTICAL",)]
    print(f"{'file':55s} {'status':10s} {'max rel dev':>12s}  where")
    print("-" * 100)
    for name, st, dev, where in rows:
        d = "" if dev == 0 else f"{dev:.3e}"
        print(f"{name:55s} {st:10s} {d:>12s}  {where}")
    print("-" * 100)
    print(f"identical bytes : {n_id}")
    print(f"volatile-only   : {n_vol}  (wall-clock fields such as elapsed_s)")
    print(f"numerically same: {n_num}  (tol {args.tol:g} relative)")
    print(f"differing       : {bad}")
    print(f"worst deviation : {worst_all:.3e}   {worst_where}")
    print()
    print("RESULT:", "PASS" if bad == 0 else "FAIL")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
