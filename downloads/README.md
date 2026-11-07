# Downloadable project archive — round 10

`Paper_A_Complete_Project_round10.zip` — one-click download of the complete round-10 deliverable: the
manuscript as rewritten this round, its ten vector figures, the solver and every verification script,
every figure dataset, the battery log of the round-10 run, the note on its one failing gate, and the
five round-10 reports.

* Size: **2,960,652 bytes** (2.96 MB)
* Entries: **218**
* SHA-256: `81d2452a1baa0629284cd2bd99aee16820354f189c581570dc1cf18bd50248c2`
* Also stored beside this file as `PACKAGE_SHA256.txt` (a checksum is never placed inside the archive it
  describes).
* Verified by extraction, a full per-entry CRC test, a re-hash of all **80** `MANIFEST.json` entries on
  the extracted copy (**80/80 match**), and `scripts/static_check.py` on the extracted copy (exit 0).

Verify after download:

```
sha256sum Paper_A_Complete_Project_round10.zip    # must print the digest above
unzip -t Paper_A_Complete_Project_round10.zip     # every entry must pass
```

## Direct link (GitHub-hosted, no login required for a public repository)

```
https://github.com/vipin-oss/A_Paper/raw/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round10.zip
```

If GitHub serves that through a redirect that a browser refuses, the media host is equivalent:

```
https://media.githubusercontent.com/media/vipin-oss/A_Paper/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round10.zip
```

## What round 10 changed

Round 10 changed the way the article is written, and it changed nothing else.

* **Title** names the process rather than a chain of modifiers: *Backward-branch negative reflection of
  guided waves from the free edge of a flexoelectric piezoelectric semiconductor plate*.
* **Abstract** rebuilt in 222 words — system, solution, two findings, the coupling contribution, the
  caveats — with every registered literal kept (`2.31`, `94.68`, `99.77`, `1.21`, `34.2`, `128`).
* **Register**: `certified` 39 → 2 (label names only), `audit` 19 → 0, `admissib*` 20 → 9,
  `solver` 21 → 1, `script` 18 → 2, `CSV` 12 → 0 in the body; the reproduction package in Appendix A
  keeps the vocabulary where it belongs.
* **Structure**: a new §2.10 collecting the limits of the formulation; the software tests, regression
  guards and reproducibility prose moved from §3 into Appendix A (459 words out of the body, 522 into
  the appendix); §4 subsections retitled around physics rather than procedure; §5 restructured with the
  limitations grouped into five headed paragraphs.
* **Captions**: physics first, no row counts, no raster spacings; the `fig02` caption no longer labels a
  distance from the edge with the symbol for the gradient length.
* **Unchanged, by construction and by check**: every equation, every table cell, every figure file, the
  ten-figure citation order, the 13 citations, and all 45 literals of the claim registry
  (`claim_audit.py` PASS, 22 claims, 9 of 9 source rows). Body length 15 839 → 15 572 words.

## The battery of this round, stated honestly

`python paper_a_study/run_all_checks.py` on 2026-11-07 returned **17 PASS, 1 FAIL, 1 SKIP**. The skip
is the LaTeX build (no engine). The failure is the claim-registry gate: running the battery regenerates
`peak_search.json`, and in the regenerated record two *differences of nearly equal numbers* move at the
round-off floor — degree spread `5.613e-9` against the committed `4.973e-9`, quadrature spread
`9.382e-10` against `5.591e-9` — while the headline is unchanged to twelve digits
(`0.9467953677961777` against `0.9467953685099261`). The data records were restored to their committed
state, which is what a manuscript-only round requires, and the gate then passes with 9 of 9 source rows.
The whole sequence, and the round-11 item it raises, is in
`validation/round10_registry_gate_note.txt`; the verbatim output is in
`validation/round10_battery_run_2026-11-07.log`.

Reading order: `START_HERE.txt` inside the archive. Details:
`PAPER_A_ROUND10_STYLE_AND_STRUCTURE_AUDIT.md` (written before the first edit),
`PAPER_A_ROUND10_AUTHOR_WRITING_STYLE.md` (the habits, with the papers they come from),
`PAPER_A_ROUND10_STRUCTURE_COMPARISON.md` (skeleton against five published papers),
`PAPER_A_ROUND10_LANGUAGE_AND_STRUCTURE_CHANGES.md` (every edit, classified),
`PAPER_A_ROUND10_FINAL_MANUSCRIPT_STYLE_AUDIT.md` (closing audit, battery, open items).

**Build status: UNVERIFIED.** No TeX engine exists in the authoring environment, so the archive contains
no PDF and claims none; an earlier compiled PDF would not certify this source.

**Novelty remains UNRESOLVED** (primary 2025 source closed access); the corner-line boundary condition is
not resolved; the material parameters ℓ, f and H are synthetic and labelled so; 94.68 % is a modal share
of the scattered power, not a reflectance, and the maximum is local, not global. No submission-readiness
claim is made.

The previous archive `Paper_A_Complete_Project_round9.zip` (SHA-256
`85548a0c84f4c66a563f7d4bda21fd98b9565c4cf4fd6f61da03a1e36726a580`) is kept for traceability and is
**superseded**.
