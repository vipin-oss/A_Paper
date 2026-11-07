#!/usr/bin/env python3
"""Do the gates actually fire?  Deliberate mutations, each expected to be caught.

A check that has never failed is not a check.  This script copies the manuscript
to a scratch directory, introduces one known defect at a time, runs the gate that
is supposed to catch it, and confirms that the gate fails.  The working tree is
never modified: M1-M4, M6 and M8 are applied to a temporary copy of the
manuscript, and M5, M7, M9, M10, M10b, M11 and M12 are applied in process to
attributes that are restored in a ``finally`` block immediately afterwards.

    M1  \\path inserted in a caption without \\protect  -> static_check
    M2  a registered headline number edited             -> claim_audit registry
    M3  a deprecated value re-inserted                  -> claim_audit stale guard
    M4  an invalid citation key                         -> static_check
    M5  a material constant in the wrong units          -> TestFrozenReferenceConstants
    M6  the superseded coarse-grid headline re-inserted  -> claim_audit stale guard
    M7  the peak case relabelled with the backward root  -> TestCornerAssessmentCaseSelection
    M8  the incident wavenumber set to KB0 in the registry -> claim_audit source agreement
    M9  the edge-plane transform reduced to the backward decay  -> cross-script edge test
    M10 the sign of the plane-transform exponent flipped        -> cross-script + invariance
    M11 the reference plane moved from 10 to 8 thicknesses      -> cross-script edge test
    M12 the thickness d replaced by the gradient length l       -> cross-script edge test
    M10b the same flipped exponent, checked by an invariance test that uses no
        stored record at all                                    -> plane invariance
    M13 a refinement spread registered as a bound is itself too small
        (a genuinely unconverged result)                        -> claim_audit bound
    M14 the figure label corrected in round 11 put back        -> TestFigureProvenance

Writes figure_data/mutation_tests.json.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SRC = REPO / "Paper_A_Final_Submission"
DATA = HERE / "figure_data"


def run(cmd: list[str], cwd: Path, env: dict | None = None) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
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
        mutate(copy / "sections" / "conclusions.tex", "94.68", "94.86")
        rc, out = run([sys.executable, str(HERE / "claim_audit.py"), "--root", str(copy)], REPO)
        results.append(dict(id="M2", defect="registered headline 0.9468 edited to 0.9486",
                            gate="claim_audit registry", expected="FAIL", caught=rc != 0,
                            evidence=[l for l in out.splitlines() if "94.86" in l][:1]))

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

        copy = make_copy(tmpdir / "m6")
        mutate(copy / "main.tex", "94.68", "93.19")
        rc, out = run([sys.executable, str(HERE / "claim_audit.py"), "--root", str(copy)], REPO)
        results.append(dict(id="M6",
                            defect="superseded coarse-grid maximum (93.19 at 0.525) reinstated",
                            gate="claim_audit stale guard", expected="FAIL", caught=rc != 0,
                            evidence=[l for l in out.splitlines() if "93.19" in l][:1]))

        copy = make_copy(tmpdir / "m8")
        registry = json.loads((HERE / "claims.json").read_text())
        for claim in registry["claims"]:
            if claim["id"] == "incident_wavenumber_peak":
                claim["value"] = 0.2451746921716515          # KB0, the backward root
                for tok in claim["tokens"]:
                    tok["value"] = 0.2451746921716515
        path = tmpdir / "registry_m8.json"
        path.write_text(json.dumps(registry))
        rc, out = run([sys.executable, str(HERE / "claim_audit.py"), "--root", str(copy),
                       "--registry", str(path)], REPO)
        results.append(dict(id="M8",
                            defect="incident wavenumber replaced by the backward target KB0",
                            gate="claim_audit source agreement", expected="FAIL",
                            caught=rc != 0,
                            evidence=[l for l in out.splitlines()
                                      if "KB0" in l or "incident root" in l][:1]))

        # M13: the bound semantics must bite.  The registry is given a bound
        # (1e-10) tighter than the spread the solver actually produces (~5e-9),
        # which is what an unconverged or wrongly-computed spread would look
        # like.  A bound that can never fail would be decoration.
        copy = make_copy(tmpdir / "m13")
        registry = json.loads((HERE / "claims.json").read_text())
        for claim in registry["claims"]:
            if claim["id"] == "degree_stability_peak":
                claim["value"] = 1e-10
                for tok in claim["tokens"]:
                    tok["value"] = 1e-10
        path = tmpdir / "registry_m13.json"
        path.write_text(json.dumps(registry))
        rc, out = run([sys.executable, str(HERE / "claim_audit.py"), "--root", str(copy),
                       "--registry", str(path)], REPO)
        results.append(dict(id="M13",
                            defect="registered refinement bound tighter than the executed spread",
                            gate="claim_audit bound", expected="FAIL", caught=rc != 0,
                            evidence=[l for l in out.splitlines() if "bound" in l][:1]))

        # M14: the label defect corrected in round 11 is put back in a copy of the
        # plotting code; the provenance test must catch it.
        m14 = tmpdir / "m14"
        m14.mkdir()
        text = (HERE / "generate_final_figures.py").read_text()
        old_label = '    c.set_ylabel(r"$R_B$ at $L=2\\,\\mu$m (%)")'
        if old_label not in text:
            raise RuntimeError("M14: the fig02 label to mutate was not found")
        (m14 / "generate_final_figures.py").write_text(
            text.replace(old_label, '    c.set_ylabel("backward reflectance $R_B$ (%)")', 1))
        env = dict(os.environ, PAPER_A_FIGURE_SRC=str(m14))
        rc, out = run([sys.executable, "-m", "unittest",
                       "paper_a_study.test_model.TestFigureProvenance."
                       "test_backward_share_is_never_called_a_reflectance"], REPO, env=env)
        results.append(dict(id="M14", defect="R_B labelled a reflectance again",
                            gate="TestFigureProvenance", expected="FAIL", caught=rc != 0,
                            evidence=[l for l in out.splitlines() if "reflectance" in l][-1:]))

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

    from paper_a_study import corner_assessment as _ca  # noqa: E402

    keep = _ca.CASES["refined_peak"]
    _ca.CASES["refined_peak"] = 0.2451746921716515        # KB0, not the incident root
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(
            test_model.TestCornerAssessmentCaseSelection)
        res = unittest.TextTestRunner(verbosity=0).run(suite)
        caught = not res.wasSuccessful()
        evidence = [str(res.failures[0][1]).strip().splitlines()[-1]] if res.failures else []
    finally:
        _ca.CASES["refined_peak"] = keep
    results.append(dict(id="M7", defect="peak case labelled with KB0 instead of its incident root",
                        gate="TestCornerAssessmentCaseSelection", expected="FAIL",
                        caught=caught, evidence=evidence))


    # ---- the plane transform: five mutants, three test classes --------------
    # ``paper_a_study.build_figure_data`` and the script-style
    # ``build_figure_data`` that the solver scripts import are two distinct
    # module objects (the scripts insert their own directory on sys.path), so a
    # mutation has to be applied to every copy that is loaded, and the tests
    # must look the function up by attribute rather than bind it at import.
    from paper_a_study import build_figure_data as _bfd  # noqa: E402

    targets = [_bfd]
    sys.path.insert(0, str(HERE))
    import build_figure_data as _bfd_top  # noqa: E402
    if _bfd_top is not _bfd:
        targets.append(_bfd_top)
    originals = {id(m): m.edge_plane_fraction for m in targets}

    def set_transform(fn):
        for m in targets:
            m.edge_plane_fraction = fn

    def restore_transform():
        for m in targets:
            m.edge_plane_fraction = originals[id(m)]

    def run_case(cls):
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        res = unittest.TextTestRunner(verbosity=0).run(suite)
        ev = []
        for holder in (res.failures, res.errors):
            ev += [str(t[1]).strip().splitlines()[-1] for t in holder][:1]
        return (not res.wasSuccessful()), ev

    real = originals[id(_bfd)]

    def backward_only(R, ki, kb, d, L_to=0.0, L_from=_bfd.REF_NORM):
        # the round-8 defect: one channel's decay used as a ratio transform
        return float(R * np.exp(2.0 * abs(kb.imag) * (L_from - L_to)))

    def flipped_sign(R, ki, kb, d, L_to=0.0, L_from=_bfd.REF_NORM):
        return float(R * np.exp(-2.0 * ((ki.imag - kb.imag) / d) * (L_from - L_to) * d))

    def wrong_reference(R, ki, kb, d, L_to=0.0, L_from=_bfd.REF_NORM):
        return real(R, ki, kb, d, L_to=L_to, L_from=8.0)

    def thickness_for_length(R, ki, kb, d, L_to=0.0, L_from=_bfd.REF_NORM):
        return float(R * np.exp(2.0 * (ki.imag - kb.imag) * (L_from - L_to) / 50e-9))

    mutants = [
        ("M9", "edge-plane transform reduced to the backward decay only "
               "(omits the incident attenuation)",
         "TestCrossScriptEdgeFraction", backward_only),
        ("M10", "sign of the plane-transform exponent flipped (wrong direction of "
                "propagation)", "TestCrossScriptEdgeFraction", flipped_sign),
        ("M11", "reference plane moved from 10 to 8 thicknesses (wrong reference "
                "distance)", "TestCrossScriptEdgeFraction", wrong_reference),
        ("M12", "thickness d replaced by the gradient length l (L and l confused)",
         "TestCrossScriptEdgeFraction", thickness_for_length),
    ]
    for mid, defect, cls_name, fn in mutants:
        set_transform(fn)
        try:
            caught, evidence = run_case(getattr(test_model, cls_name))
        finally:
            restore_transform()
        results.append(dict(id=mid, defect=defect, gate=cls_name, expected="FAIL",
                            caught=caught, evidence=evidence))

    # M10b: the same flipped exponent, checked by an invariance test that reads
    # no stored record at all.  If the records were ever regenerated from a
    # broken transform, M10 would pass and this one would still fail.
    set_transform(flipped_sign)
    try:
        caught, evidence = run_case(test_model.TestPlaneInvariance)
    finally:
        restore_transform()
    results.append(dict(id="M10b", defect="flipped exponent, checked by an invariance test "
                        "that uses no stored values", gate="TestPlaneInvariance",
                        expected="FAIL", caught=caught, evidence=evidence))

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
