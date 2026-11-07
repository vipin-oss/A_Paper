# Downloadable project archive — round 9

`Paper_A_Complete_Project_round9.zip` — one-click download of the complete round-9 deliverable: the
authoritative manuscript, all ten vector figures, the solver and every verification script, every figure
dataset regenerated from the corrected transform, the eighteen-gate battery log, and the seven round-9
reports.

* Size: **2,924,173 bytes** (2.92 MB)
* Entries: **210**
* SHA-256: `85548a0c84f4c66a563f7d4bda21fd98b9565c4cf4fd6f61da03a1e36726a580`
* Also stored beside this file as `PACKAGE_SHA256.txt` (a checksum is never placed inside the archive it
  describes).
* Verified by extraction, a full per-entry CRC test, a re-hash of all **79** `MANIFEST.json` entries on
  the extracted copy (**79/79 match**), and `scripts/static_check.py` on the extracted copy (exit 0, no
  errors; warnings and the prose word count only).

Verify after download:

```
sha256sum Paper_A_Complete_Project_round9.zip     # must print the digest above
unzip -t Paper_A_Complete_Project_round9.zip      # every entry must pass
```

## Direct link (GitHub-hosted, no login required for a public repository)

```
https://github.com/vipin-oss/A_Paper/raw/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round9.zip
```

If GitHub serves that through a redirect that a browser refuses, the media host is equivalent:

```
https://media.githubusercontent.com/media/vipin-oss/A_Paper/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round9.zip
```

## What round 9 changed

Round 9 repaired one verified defect and nothing else. Three call sites moved a modal-power **ratio**
between planes with the **single-mode absolute decay**, which omits the incident attenuation; the ratio
transform is `exp[2(Im K_i − Im K_B)(L_from − L_to)]`, i.e. a **sum of magnitudes**. The largest
consequence was in the peak-search record: 0.965978 where the corrected transform and a direct solve at
the edge plane both give 0.985572 (1.96 percentage points).

* the reference-plane headline is **unchanged**: `R_B = 0.9467952` (94.68 %) at `k_x d = 0.5275`, a
  **certified local maximum** inside `0.465 < k_x d < 0.625`, flat to 0.01 pp over `0.5266–0.5277`;
* the edge-plane records were regenerated: search 0.9855722, density sweep up to 0.5804, coupling
  dataset 0.019304–0.025601, operating point 0.023151;
* four manuscript numbers were re-read, three table cells moved (0.0231 → 0.0232 on rounding;
  1.7e-9 → 3.8e-9 and 2.1e-8 → 2.3e-8 on regeneration), and the Fig. 9 paragraph was rewritten
  because it had been wrong about the round-off levels;
* the transform is now implemented once and imported everywhere, the edge share is a registered claim,
  a cross-script gate compares the two producers, and three new test classes (13 tests) cover it;
* packaging bug fixed: `build_submission_package.py` now runs the static validator *before* writing
  `MANIFEST.json`, so the manifest describes the file that is actually on disk.

Reading order: `START_HERE.txt` inside the archive. Details:
`PAPER_A_ROUND9_STAGE1_NORMALIZATION_AUDIT.md` (the defect, before any edit),
`PAPER_A_ROUND9_CORRECTION_HISTORY.md` (every edit),
`PAPER_A_ROUND9_PLANE_INVARIANCE_VALIDATION.md` (five planes, 2.3e-16),
`PAPER_A_ROUND9_MUTATION_REPORT.md` (13 mutants, 13 caught),
`PAPER_A_ROUND9_CLAIMS_AND_MANUSCRIPT_AUDIT.md`, `PAPER_A_ROUND9_TEST_RESULTS.md`,
`PAPER_A_ROUND9_DELIVERY_AND_STATUS.md`.

**Build status: UNVERIFIED.** No TeX engine exists in the authoring environment, so the archive contains
no PDF and claims none; an earlier compiled PDF would not certify this source.
`paper_a_study/`, `validation/verification_log.txt` and
`Paper_A_Final_Submission/static_validation.txt` are the evidence for everything else.

**Novelty remains UNRESOLVED** (primary 2025 source closed access); the corner-line boundary condition is
not certified; the material parameters ℓ, f and H are synthetic and labelled so. No submission-readiness
claim is made.

The previous archive `Paper_A_Complete_Project_round8.zip` (SHA-256
`ce2a335949afd2fd7d77dedabfb81d8f88149ffca6e354acc9f6887bad8aa800`) is kept for traceability and is
**superseded**.
