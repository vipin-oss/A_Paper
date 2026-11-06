#!/usr/bin/env python3
"""Do the gates actually fire?  Deliberate mutations, each expected to be caught.

A check that has never failed is not a check.  This script copies the manuscript
to a scratch directory, introduces one known defect at a time, runs the gate that
is supposed to catch it, and confirms that the gate fails.  The working tree is
never modified: every mutation is applied to the copy, except the last, which is
applied in process and reverted.

    M1  \\path inserted in a caption without \\protect  -> static_check
    M2  a registered headline number edited             -> claim_audit registry
    M3  a deprecated value re-inserted                  -> claim_audit stale guard
    M4  an invalid citation key                         -> static_check
    M5  a material constant in the wrong units          -> TestFrozenReferenceConstants

Writes figure_data/mutation_tests.json.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SRC = REPO / "Paper_A_Final_Submission"
DATA = HERE / "figure_data"


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)


def make_copy(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    dst = root / "manuscript"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return dst


def mutate(path: Path, old: str, new: str) -> None:
    s = path.read_text()
    if s.count(old) != 1:
        raise RuntimeError(f"{path}: {s.count(old)} occurrences of {old!r}")
    path.write_text(s.replace(old, new))


def main() -> int:
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)

        copy = make_copy(tmpdir / "m1")
        mutate(copy / "sections" / "results.tex", "$H=0$ at fixed frequency.}",
               "$H=0$ at fixed frequency, data in \\path{fig05_channel_power.csv}.}")
        rc, out = run([sys.executable, str(copy / "scripts" / "static_check.py")], copy)
        results.append(dict(id="M1", defect="\\path inserted in a caption without \\protect",
                            gate="static_check", expected="FAIL", caught=rc != 0,
                            evidence=[l for l in out.splitlines() if "fragile" in l][:1]))

        copy = make_copy(tmpdir / "m2")
        mutate(copy / "sections" / "conclusions.tex", "93.19", "93.91")
        rc, out = run([sys.executable, str(HERE / "claim_audit.py"), "--root", str(copy)], REPO)
        results.append(dict(id="M2", defect="registered value 0.9319 edited to 0.9391",
                            gate="claim_audit registry", expected="FAIL", caught=rc != 0,
                            evidence=[l for l in out.splitlines() if "93.91" in l][:1]))

        copy = make_copy(tmpdir / "m3")
        mutate(copy / "sections" / "results.tex", "0.99980", "0.99985")
        rc, out = run([sys.executable, str(HERE / "claim_audit.py"), "--root", str(copy)], REPO)
        results.append(dict(id="M3", defect="deprecated total outgoing power 0.99985 re-inserted",
                            gate="claim_audit stale guard", expected="FAIL", caught=rc != 0,
                            evidence=[l for l in out.splitlines() if "0.99985" in l][:1]))

        copy = make_copy(tmpdir / "m4")
        mutate(copy / "sections" / "introduction.tex", "\\cite{shen2010theory,deng2020impact}",
               "\\cite{shen2010theory,deng2020impact,nosuchkey2024}")
        rc, out = run([sys.executable, str(copy / "scripts" / "static_check.py")], copy)
        results.append(dict(id="M4", defect="undefined citation key \\cite{nosuchkey2024}",
                            gate="static_check", expected="FAIL", caught=rc != 0,
                            evidence=[l for l in out.splitlines() if "nosuchkey" in l][:1]))

    sys.path.insert(0, str(REPO))
    from paper_a_study import model  # noqa: E402
    from paper_a_study import test_model  # noqa: E402

    original = model.SI["c44"]
    model.SI["c44"] = original * 1e9            # GPa entered as Pa
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(
            test_model.TestFrozenReferenceConstants)
        res = unittest.TextTestRunner(verbosity=0).run(suite)
        caught = not res.wasSuccessful()
        evidence = [str(res.failures[0][1]).strip().splitlines()[-1]] if res.failures else []
    finally:
        model.SI["c44"] = original
    results.append(dict(id="M5", defect="c44 entered in Pa instead of GPa",
                        gate="TestFrozenReferenceConstants", expected="FAIL",
                        caught=caught, evidence=evidence))

    ok = True
    for r in results:
        status = "CAUGHT" if r["caught"] else "MISSED"
        ok &= r["caught"]
        print(f"{r['id']}  {status:7s} {r['gate']:32s} {r['defect']}")
        for line in r["evidence"]:
            print(f"        {line.strip()[:120]}")
    print("\nverdict:", "PASS" if ok else "FAIL")
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "mutation_tests.json").write_text(json.dumps(
        dict(mutations=results, verdict="PASS" if ok else "FAIL"), indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
