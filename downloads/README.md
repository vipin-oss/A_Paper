# Paper A — downloadable complete project

## Round 11 (current)

```
Paper_A_Complete_Project_round11.zip
224 entries · 3,030,613 bytes (3.03 MB)
SHA-256  6516d5f10d0ddadd1ec5b4b65fb78fe5a1adea7de69133eb58b780455f29aa12
```

**Direct one-click download** (no Git client, no checkout, no PowerShell):

<https://github.com/vipin-oss/A_Paper/raw/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round11.zip>

Open the link, press "Download", unzip, and start with `START_HERE.txt` at the top of
the archive.

### What round 11 is

A programming, numerical-reproducibility and figure-verification round. It changed
**no equation, no boundary condition, no solution method and no headline number**. It
audited 28 items before editing anything (`PAPER_A_ROUND11_STAGE1_PROGRAMMING_AND_FIGURE_AUDIT.md`),
repaired the confirmed defects, and then ran the full battery on a **cleanly
regenerated data directory with nothing restored**: **18 PASS, 0 FAIL, 1 SKIP**
(the skip is the LaTeX build — no engine in the authoring environment).

What it found:

* three sentences of the manuscript were contradicted by the data of their own
  figures — the coupling-induced frequency shift (quoted 60 kHz, measured 184 kHz,
  a factor of three), the $v_g$–$v_E$ agreement over "the whole branch" (6.4 % at
  the lowest sample), and the gradient-length percentages quoted at an abscissa the
  grid does not contain;
* two refinement spreads were quoted to two significant figures and tested by a 1 %
  equality test, which is why the round-10 battery failed on round-off; they are now
  registered and quoted as bounds, and the quadrature spread no longer mixes two
  Galerkin degrees;
* eight figure defects: a modal share labelled "reflectance", the gradient-length
  symbol used for the reference-plane distance and for the distance from the edge, an
  attenuation length labelled $L$, a schematic with no label, two residual panels
  showing round-off as structure, an inset that clipped the largest value it
  describes, and a panel xlabel cut by the canvas edge;
* four reproducibility hazards: a superseded generator that silently rewrites the
  datasets with an older schema, a battery that ran its tests before the records they
  read, an undocumented build order, and a hand-maintained panel map that had drifted
  away from the code it described.

### What round 11 did not change

The headline result, the tables, the figures' data, the 13 citations, the round-10
language and structure, the local (not global) character of the maximum, the
synthetic status of $\ell$, $f$ and $H$, the single-edge and corner caveats, the
**UNRESOLVED** novelty status, and the fact that the typeset manuscript is
**BUILD UNVERIFIED**.

### Read first, in this order

1. `PAPER_A_ROUND11_STAGE1_PROGRAMMING_AND_FIGURE_AUDIT.md` — the audit, written before the first edit
2. `PAPER_A_ROUND11_NUMERICAL_REPRODUCIBILITY.md` — the clean reproduction and the data comparison
3. `PAPER_A_ROUND11_FIGURE_BY_FIGURE_AUDIT.md` — ten figures, forty panels
4. `PAPER_A_ROUND11_PANEL_SOURCE_MATRIX.md` — which column every panel plots
5. `PAPER_A_ROUND11_CLAIM_REGISTRY_CORRECTION.md` — categories A–E
6. `PAPER_A_ROUND11_MUTATION_AND_REGRESSION_RESULTS.md` — 15 mutants, 47 tests
7. `PAPER_A_ROUND11_CORRECTION_HISTORY.md` — every change
8. `PAPER_A_ROUND11_FINAL_TECHNICAL_READINESS.md` — the closing verdict
9. `PAPER_A_CORRECTION_HISTORY.md` — cumulative history (round-11 addendum at the end)

### Verification performed on this archive

`unzip -t` reports no errors; the archive extracts to a scratch directory; **80 of 80**
`MANIFEST.json` hashes recompute correctly from the extracted tree; the archive
contains exactly **one** `main.tex`; `Paper_A_Final_Submission/scripts/static_check.py`
exits 0 (104 labels, 75 references, 13 citation keys, 13 bib entries).

---

## Superseded archives

| round | size | SHA-256 (first 8 / last 4) | note |
|---|---|---|---|
| round 10 | 2,960,652 B | `81d2452a…48c2` | manuscript structure and language; battery 17/1/1 (claim gate failed on round-off) |
| round 9 | 2,924,173 B | `85548a0c…a580` | plane-invariance correction |
| round 8 and earlier | — | — | retained for the record; not for review |

Only the round-11 archive should be used for review.
