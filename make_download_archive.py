#!/usr/bin/env python3
"""Build the round-10 downloadable project archive.

Deterministic and read-only with respect to the sources: it copies from the
working tree into a staging directory, writes START_HERE.txt, PACKAGE_README.md
and PACKAGE_SHA256.txt, and zips the result.  It never modifies a source file.

    python make_download_archive.py

Excluded on purpose: the superseded manuscripts under archive/, earlier ZIPs,
bytecode caches, virtual environments, and the large derived figure exports
(paper_a_study/figures_final, paper_a_study/results, PNG contact sheets).
"""
from __future__ import annotations

import hashlib
import os
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGE = Path("/tmp/paper_a_round21_stage")   # outside the repo: no second main.tex
OUT = ROOT / "downloads" / "Paper_A_Complete_Project_round21.zip"

ROOT_REPORTS = [
    "PAPER_A_ROUND21_FINAL_SUBMISSION_DECISION.md",
    "PAPER_A_ROUND21_GATE1_DERIVATION.md",
    "PAPER_A_CORRECTION_HISTORY.md",
    "PAPER_A_ROUND19_FINAL.md",
    "PAPER_A_ROUND19_PRE_EDIT_VERIFICATION.md",
    "PAPER_A_ROUND20_FINAL_SUPERVISOR_DECISION.md",
    "PAPER_A_ROUND20_NUMERICAL_IMPACT_AND_RECOMPUTATION.md",
    "PAPER_A_ROUND20_SPATIAL_SPECTRAL_COUNT_AUDIT.md",
    "PAPER_A_ROUND20_HYPERSTRESS_AND_CORNER_AUDIT.md",
    "PAPER_A_ROUND20_ELECTRICAL_EDGE_CONDITION_AUDIT.md",
    "PAPER_A_ROUND20_FACE_VS_EDGE_NORMAL_AUDIT.md",
    "PAPER_A_ROUND20_VARIATIONAL_BOUNDARY_DERIVATION.md",
    "PAPER_A_ROUND20_PRE_EDIT_BOUNDARY_AUDIT.md",
    "PAPER_A_ROUND19_HYPERSTRESS_AND_BOUNDARY_AUDIT.md",
    "PAPER_A_ROUND19_EDGE_SYSTEM_VERIFICATION.md",
    "PAPER_A_ROUND19_MODAL_POWER_RECALCULATION.md",
    "PAPER_A_ROUND19_POLYNOMIAL_OPERATOR_AUDIT.md",
    "PAPER_A_ROUND19_LATEX_AND_LAYOUT_REPAIR.md",
    "PAPER_A_ROUND18_FINAL_SUPERVISOR_REVIEW.md",
    "PAPER_A_ROUND18_PRE_EDIT_AUDIT.md",
    "PAPER_A_ROUND18_MATHEMATICAL_REPAIR.md",
    "PAPER_A_ROUND18_INDEPENDENT_RECHECK.md",
    "PAPER_A_ROUND18_CORRECTNESS_VERDICTS.md",
    "PAPER_A_ROUND18_REGRESSION_AND_PACKAGE.md",
    "PAPER_A_ROUND18_AUDIT_LOG.txt",
    "PAPER_A_ROUND17_FINAL_SUPERVISOR_REVIEW.md",
    "PAPER_A_ROUND17_MANUSCRIPT_RESTRUCTURING.md",
    "PAPER_A_ROUND17_MATHEMATICAL_DERIVATIONS.md",
    "PAPER_A_ROUND17_WORKED_CALCULATIONS.md",
    "PAPER_A_ROUND17_FIGURE_ZOOM_AND_OVERLAP_AUDIT.md",
    "PAPER_A_ROUND17_TABLE_AND_LIMITATION_CORRECTIONS.md",
    "PAPER_A_ROUND16_SUPERVISOR_DECISION.md",
    "PAPER_A_ROUND16_CONVENTIONS_AND_DIMENSIONS.md",
    "PAPER_A_ROUND16_CARRIER_STRONG_TO_WEAK_DERIVATION.md",
    "PAPER_A_ROUND16_CARRIER_OPERATOR_COMPARISON.md",
    "PAPER_A_ROUND16_MECHANICAL_AND_GAUSS_AUDIT.md",
    "PAPER_A_ROUND16_CORRECTION_HISTORY.md",
    "PAPER_A_ROUND16_AUDIT_LOG.txt",
    "PAPER_A_ROUND15_SUPERVISOR_DECISION.md",
    "PAPER_A_ROUND15_INDEPENDENT_MATHEMATICAL_AUDIT.md",
    "PAPER_A_ROUND15_COMPLETE_COUPLED_WEAK_FORM.md",
    "PAPER_A_ROUND15_BOUNDARY_VARIATION_AND_CORNER_AUDIT.md",
    "PAPER_A_ROUND15_FIGURE_5_8_VISUAL_REVIEW.md",
    "PAPER_A_ROUND15_LATEX_AND_NOMENCLATURE_AUDIT.md",
    "PAPER_A_ROUND15_PRE_EDIT_MATHEMATICAL_AUDIT.md",
    "PAPER_A_ROUND14_AUTHOR_STYLE_AND_PRESENTATION_FAILURE_AUDIT.md",
    "PAPER_A_ROUND14_MATHEMATICAL_DERIVATION_MATRIX.md",
    "PAPER_A_ROUND14_FIGURE_REDESIGN_AUDIT.md",
    "PAPER_A_ROUND14_MANUSCRIPT_STRUCTURE_CHANGES.md",
    "PAPER_A_ROUND14_DERIVATION_VERIFICATION.md",
    "PAPER_A_ROUND14_FINAL_MANUSCRIPT_PRESENTATION_REVIEW.md",
    "SUPPLEMENTARY_COMPUTATIONAL_REPRODUCIBILITY.md",
    "PAPER_A_ROUND13_SUPERVISOR_HANDOFF.md",
    "PAPER_A_ROUND13_PRE_EDIT_CLOSURE_AUDIT.md",
    "PAPER_A_ROUND13_FIG10_VECTOR_VERIFICATION.md",
    "PAPER_A_ROUND13_DOCUMENTATION_CORRECTIONS.md",
    "PAPER_A_ROUND13_LATEX_BUILD_AND_PAGE_PROOF.md",
    "PAPER_A_ROUND13_TARGETED_VALIDATION.md",
    "PAPER_A_ROUND13_SUPERVISOR_HANDOFF.md",
    "PAPER_A_ROUND12_PRELIMINARY_EVIDENCE_CORRECTIONS.md",
    "PAPER_A_ROUND12_SECTION_BY_SECTION_REVIEW.md",
    "PAPER_A_ROUND12_EDIT_LEDGER.md",
    "PAPER_A_ROUND12_NUMERICAL_TRACEABILITY_AUDIT.md",
    "PAPER_A_ROUND12_READINESS_ASSESSMENT.md",
    "PAPER_A_ROUND12_BLOCKING_ISSUES.md",
    "PAPER_A_ROUND12_CORRECTION_HISTORY.md",
    "PAPER_A_ROUND11_STAGE1_PROGRAMMING_AND_FIGURE_AUDIT.md",
    "PAPER_A_ROUND11_NUMERICAL_REPRODUCIBILITY.md",
    "PAPER_A_ROUND11_FIGURE_BY_FIGURE_AUDIT.md",
    "PAPER_A_ROUND11_PANEL_SOURCE_MATRIX.md",
    "PAPER_A_ROUND11_CLAIM_REGISTRY_CORRECTION.md",
    "PAPER_A_ROUND11_MUTATION_AND_REGRESSION_RESULTS.md",
    "PAPER_A_ROUND11_CORRECTION_HISTORY.md",
    "PAPER_A_ROUND11_FINAL_TECHNICAL_READINESS.md",
    "PAPER_A_ROUND10_STYLE_AND_STRUCTURE_AUDIT.md",
    "PAPER_A_ROUND10_AUTHOR_WRITING_STYLE.md",
    "PAPER_A_ROUND10_STRUCTURE_COMPARISON.md",
    "PAPER_A_ROUND10_LANGUAGE_AND_STRUCTURE_CHANGES.md",
    "PAPER_A_ROUND10_FINAL_MANUSCRIPT_STYLE_AUDIT.md",
    "PAPER_A_ROUND9_STAGE1_NORMALIZATION_AUDIT.md",
    "PAPER_A_ROUND9_CORRECTION_HISTORY.md",
    "PAPER_A_ROUND9_PLANE_INVARIANCE_VALIDATION.md",
    "PAPER_A_ROUND9_MUTATION_REPORT.md",
    "PAPER_A_ROUND9_CLAIMS_AND_MANUSCRIPT_AUDIT.md",
    "PAPER_A_ROUND9_TEST_RESULTS.md",
    "PAPER_A_ROUND9_DELIVERY_AND_STATUS.md",
    "PAPER_A_ROUND8_STAGE1_AUDIT.md",
    "PAPER_A_ROUND8_PEAK_CERTIFICATION.md",
    "PAPER_A_ROUND8_ARTEFACT_AUDIT.md",
    "PAPER_A_ROUND8_CONVERGENCE_AND_CONTROLS.md",
    "PAPER_A_ROUND8_MANUSCRIPT_CHANGES.md",
    "PAPER_A_ROUND8_CLAIMS_AND_TESTS.md",
    "PAPER_A_ROUND8_DELIVERY_AND_STATUS.md",
    "PAPER_A_STAGE1_COMPLETE_Q1_AUDIT.md",
    "PAPER_A_ROUND7_NOVELTY_AND_MECHANISM_REPORT.md",
    "PAPER_A_EXTENDED_NUMERICAL_VALIDATION.md",
    "PAPER_A_CLAIM_PROVENANCE_MATRIX.md",
    "PAPER_A_FINAL_SUBMISSION_READINESS.md",
    "PAPER_A_FINAL_SCIENTIFIC_AUDIT.md",
    "PAPER_A_ROUND4_INDEPENDENT_AUDIT.md",
    "PAPER_A_ROUND6_FINAL_VERIFICATION.md",
    "PAPER_A_FINAL_INDEPENDENT_CORRECTION_RESPONSE.md",
    "PAPER_A_FINAL_SCIENTIFIC_CORRECTION_AND_Q1_AUDIT.md",
    "PAPER_A_FINAL_SCIENTIFIC_CHECK.md",
    "PAPER_A_FIGURE_AUDIT_FINAL.md",
    "PAPER_A_PROGRESS.md",
    "PAPER_A_BLUEPRINT_V2_1.md",
    "PAPER_A_RESEARCH_REPORT.md",
    "PAPER_A_A0_CONSTITUTIVE_CHECK.md",
    "PAPER_A_A0_DISPERSION_FEASIBILITY.md",
    "PAPER_A_A0_MATERIALS.md",
    "PAPER_A_A0_PRIOR_ART.md",
    "PAPER_A_A0R_BACKWARD_WAVE_FEASIBILITY.md",
    "PAPER_A_A0R_DECISION.md",
    "PAPER_A_A0R_NOVELTY_COMPARISON.md",
    "PAPER_A_A0S_H_SENSITIVITY.md",
    "PAPER_A_A0S_MODEL_SELECTION.md",
    "PAPER_A_A0S_OPERATING_REGIME.md",
    ".gitignore",
]
ROOT_SCRIPTS = ["build_submission_package.py", "build_paper_a_package.py",
                "make_download_archive.py"]

SKIP_DIRS = {"__pycache__", "figures_final", "results", "cache", "private_sources"}
SKIP_SUFFIX = {".pyc", ".pyo", ".npy", ".npz", ".png", ".svg"}
SKIP_NAMES: set[str] = set()   # the two contact-sheet PDFs are small and useful
FIXED_EPOCH = 1767225600            # 2026-01-01T00:00:00Z, for reproducible zips


def keep(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.suffix in SKIP_SUFFIX or path.name in SKIP_NAMES:
        return False
    return True


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)

    copied = 0
    for name in ROOT_REPORTS + ROOT_SCRIPTS:
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, STAGE / name)
            copied += 1

    for top in ("Paper_A_Final_Submission", "paper_a_study", "a0", "a0r", "a0s",
                "validation"):
        base = ROOT / top
        if not base.exists():
            continue
        for src in sorted(base.rglob("*")):
            if src.is_dir() or not keep(src):
                continue
            rel = src.relative_to(ROOT)
            dst = STAGE / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1

    (STAGE / "START_HERE.txt").write_text(
        "\n".join([
            "Paper A -- round 21: submission candidate",
            "=========================================",
            "",
            "This package contains the manuscript, its implementation, its datasets, the",
            "verification battery and the scientific record. Read in this order:",
            "",
            "  PACKAGE_README.md                                  START HERE: what the paper claims",
            "  PAPER_A_ROUND21_FINAL_SUBMISSION_DECISION.md       round-21 decision, gates, classification",
            "  PAPER_A_ROUND21_GATE1_DERIVATION.md                natural boundary data: derivation and proof",
            "  Paper_A_Final_Submission/main.tex                  the manuscript",
            "",
            "Headline result: R_B = 0.9428718 at k_x d = 0.52719, a local maximum of the",
            "backward-modal share with a flat top over [0.5267, 0.5276] and a centre value",
            "0.9428521. The incident flux there is small compared with the operating point, whose",
            "share is a different number, 0.0192916. At the edge plane the maximum is",
            "0.9824311. The electrical condition on the reflecting edge is insulating",
            "(D_x = 0) everywhere; the grounded case is a labelled control only.",
            "",
            "Round-21 science, in one paragraph: the generalised traction, the double traction",
            "and the corner line force are derived from the variational statement and then",
            "verified against the discrete flux rows the solver imposes, on the complete",
            "incident+reflected field. The identity closes to 1.4e-13 for the incident guided",
            "mode at every degree from 10 to 28 and every quadrature rule tried; it is violated",
            "at the level of 1.7e+1 if the corner terms are dropped. The corner line force is",
            "therefore measured rather than assumed: it is <= 8.4e-2 of the incident corner",
            "scale over degrees 10..28, decays as n^-0.62 with the same exponent in three",
            "independent configurations, is unchanged to six digits under quadrature refinement,",
            "and does not enter any reported number (the partition moves by 3.9e-6 over the",
            "same range while the corner force halves). The pointwise traction residual of the",
            "complete field is likewise quoted, not suppressed: 9.4e-4 of the incident scale at",
            "the corrected maximum and 3.6e-2 at the operating point, not decreasing with degree,",
            "because a Galerkin boundary condition is a moment condition.",
            "",
            "BUILD STATUS: NO PDF. No TeX engine exists in the authoring environment and none",
            "could be installed (no deb mirror, no PyPI engine, the tectonic release host is",
            "blocked). The LaTeX source is statically validated only (labels, references,",
            "citations, macro whitelist, display widths). Page-by-page proofing is an external",
            "action. Build with:",
            "  cd Paper_A_Final_Submission",
            "  pdflatex -interaction=nonstopmode -halt-on-error main.tex",
            "  bibtex main",
            "  pdflatex -interaction=nonstopmode -halt-on-error main.tex",
            "  pdflatex -interaction=nonstopmode -halt-on-error main.tex",
            "  grep -n 'Overfull \\\\hbox' main.log",
            "",
            "Reproduce every number and figure (Python 3.11, numpy, scipy, matplotlib):",
            "  python paper_a_study/build_figure_data.py        # the CSV/JSON datasets",
            "  python paper_a_study/generate_final_figures.py   # the ten figures",
            "  cp paper_a_study/figures_final/fig*.pdf Paper_A_Final_Submission/figures/",
            "  python paper_a_study/round21_gate1_traction.py   # Gate 1: the boundary-data identity",
            "  python paper_a_study/round21_gate_corner.py      # Gate 2: the corner line force",
            "  python -m unittest paper_a_study.round21_tests   # 5 round-21 regression tests",
            "  python paper_a_study/run_all_checks.py           # the whole battery, one log",
            "",
            "Data for the round-21 gates: paper_a_study/figure_data/round21/",
            "  gate1_traction_identity.json    per-mode identity, degrees 8..16, two quadratures",
            "  gate12_corner.json              three configurations, degrees 10..28, three bands",
            "",
            "Open items that are not the author's to close blind: five author declarations",
            "(funding, competing interests, data availability, ethics, contributions) await the",
            "author and are listed outside the manuscript; the parameters ell, f and H are",
            "synthetic and are described as such; and the primary 2025 source is closed access,",
            "so the novelty comparison rests on its published title and abstract and on the",
            "open-access reproduction of its free-energy decomposition.",
        ]) + "\n")
    copied += 1
    os.utime(STAGE / "START_HERE.txt", (FIXED_EPOCH, FIXED_EPOCH))

    shutil.copy2(ROOT / "PACKAGE_README.md", STAGE / "PACKAGE_README.md")
    copied += 1

    # Normalise every staged mtime so that the archive depends only on content.
    for path in STAGE.rglob("*"):
        if path.is_file():
            os.utime(path, (FIXED_EPOCH, FIXED_EPOCH))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(STAGE.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(STAGE).as_posix())

    digest = sha256(OUT)
    n = len(zipfile.ZipFile(OUT).namelist())
    size = OUT.stat().st_size
    checksum = f"{digest}  {OUT.name}\n{size} bytes, {n} files\n"
    # The checksum file cannot live inside the archive it describes, so it is
    # written twice: into the staging tree (for inspection) and beside the ZIP
    # (where a downloader can actually read it).
    (STAGE / "PACKAGE_SHA256.txt").write_text(checksum)
    (OUT.parent / "PACKAGE_SHA256.txt").write_text(checksum)
    print(f"archive : {OUT}")
    print(f"files   : {n}   staged copies: {copied}")
    print(f"size    : {size:,} bytes ({size/1e6:.2f} MB)")
    print(f"sha256  : {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
