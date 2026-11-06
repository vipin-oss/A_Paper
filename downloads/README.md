# Downloadable project archive — round 8

`Paper_A_Complete_Project_round8.zip` — one-click download of the complete round-8 deliverable: the
authoritative manuscript, all ten vector figures, the solver and every verification script, all figure
datasets (including the two new peak records), the eighteen-gate battery log, and the seven round-8 reports.

* Size: **2,884,887 bytes** (2.88 MB)
* Entries: **201**
* SHA-256: `ce2a335949afd2fd7d77dedabfb81d8f88149ffca6e354acc9f6887bad8aa800`
* Also stored beside this file as `PACKAGE_SHA256.txt` (a checksum is never placed inside the archive it
  describes).
* Verified by extraction, a full per-entry CRC test, a re-hash of all **78** `MANIFEST.json` entries
  (78/78 match) and a re-run of `scripts/static_check.py` on the extracted copy (exit 0).

Verify after download:

```
sha256sum Paper_A_Complete_Project_round8.zip     # must print the digest above
unzip -t Paper_A_Complete_Project_round8.zip      # every entry must pass
```

## Direct link (GitHub-hosted, no login required for a public repository)

```
https://github.com/vipin-oss/A_Paper/raw/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round8.zip
```

If GitHub serves that through a redirect that a browser refuses, the media host is equivalent:

```
https://media.githubusercontent.com/media/vipin-oss/A_Paper/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round8.zip
```

## What changed since round 7

The round-7 headline (93.19 % at k_xd = 0.525) was a coarse-grid sample. The response has a flat top
1e-3 wide, and a staged search places the maximum at **k_xd = 0.5275**, R_B = **0.9467952 (94.68 %)** —
a **certified local maximum**, flat to 0.01 percentage point over 0.5266 ≤ k_xd ≤ 0.5277, not claimed to be
global. The incident modal flux at that point is **128 times smaller** than at the operating point, so the
share is maximal where the transported power is minimal; the paper now says so in the abstract, results,
discussion and conclusions. The coupling's effect at the peak is −34.2 % at the reference plane and
−11.1 % at the edge plane (23.1 points of propagation loss), and re-searching at each coupling level drops
the ceiling to 0.6244 / 0.7013 at the extremes of H. Reading order: `START_HERE.txt` inside the archive.
Details: `PAPER_A_ROUND8_STAGE1_AUDIT.md` (nine defects) and
`PAPER_A_ROUND8_MANUSCRIPT_CHANGES.md` (every edit).

**Build status: UNVERIFIED.** No TeX engine exists in the authoring environment, so the archive contains no
PDF and claims none. `paper_a_study/`, `validation/verification_log.txt` and
`Paper_A_Final_Submission/static_validation.txt` are the evidence for everything else.

The previous archive `Paper_A_Complete_Project_round7.zip` (SHA-256
`bd9a665595f4a9e9f82601e4d022138ac73179856ac594ef4556b136ba020f69`) is kept for traceability and is
**superseded**.
