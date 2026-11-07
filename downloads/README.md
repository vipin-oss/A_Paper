# Paper A — downloadable complete project

## Round 13 (current)

```
Paper_A_Complete_Project_round13.zip
237 entries · 3,115,314 bytes (3.12 MB)
SHA-256  bc7cafd58d223918c4ab5a06520333cd711dfc8f568d8a99e5f91004b7c3cca5
```

**Direct one-click download** (no Git client, no checkout, no PowerShell):

<https://github.com/vipin-oss/A_Paper/raw/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round13.zip>

Open the link, press "Download", unzip, and start with `START_HERE.txt` at the top of
the archive — or go straight to `PAPER_A_ROUND13_SUPERVISOR_HANDOFF.md`, which is the
document written for a first read.

### What round 13 is

A **targeted closure round**. It closes the two defects round 12 left open, fixes one
misattributed number and one caption, and re-verifies everything those changes could
touch. It changes **no equation, no constant, no boundary condition, no solver, no
dataset, no table and no reported number** — and the fig10 field map, regenerated,
came back **byte-identical**.

**Figure 10(c): the backward-wavenumber arrow.** The panel drew $\vect{k}_B$ along
$(0.333,-0.530)$ — one ratio taken from $K_{Bx}/K_{ix}$, one from
$\lvert k_y\rvert/K_{Bx}$, and the sign of the *flux*. It pointed 57.9° **below** the
$+x$ axis and was 2.2× too long. The solve at the figure's own configuration gives
$k_{Bx}d=0.2451746921716515$, $k_yd=0.12981175031447484$, i.e.
$\vect{k}_B\propto(1,0.5295)$ at **+27.90°**, with
$\lvert\vect{k}_B\rvert/\lvert\vect{k}_i\rvert=0.371$ — while the **flux**
$\vect{P}_B\propto(-1,-0.5295)$ really does point down-left. All four arrows are now
derived from the stored solve (`fig10_field_metrics.json` → `primary_wavenumbers`, a
new block written by the producer), drawn at the solved proportions, and checked at
render time by a guard that aborts the build if the wavenumber leaves the first
quadrant. Five new tests pin it, and a deliberately reversed arrow fails three of
them.

**`peak_search.py`.** Its docstring said the branch-tracking-path sensitivity
"dominates the reproducibility of the printed digits". The delivered record says the
tracking spread is **0.0**; the quantity that is $8.4\times10^{-6}$ is the coarse
raster's sampling error (`restart_spread`). The docstring now names the four
diagnostics separately. The algorithm, the tolerances and `peak_search.json` are
untouched.

**Two smaller corrections.** The round-12 correction history and this README had
attached 62.2973 % to $k_xd=0.55$; it belongs to the **reported peak** at
$k_xd=0.5275$ with $H/H^{*}=+0.05$ (at 0.55 the coupling-on share is 0.5221). Both
files are corrected and carry a dated note — and the manuscript was right all along
(§4.10 attaches 0.6230 to "the maximum"). The fig10 caption said "(c) schematic whose
arrows are the solved flux directions" for a panel that draws both wavenumbers and
fluxes; two words added. The appendix's test count moved 47 → 52 with the five new
tests.

### What round 13 did not change

The headline result, every table, the 13 citations, the round-10 language, the
round-11 figure and registry work, the round-12 prose corrections, the other nine
figures (not even re-rendered), and every dataset except an eleven-line metadata
addition.

Also unchanged: the maximum is **local**, $\ell$, $f$ and $H$ are **synthetic**, the
novelty status is **UNRESOLVED**, the corner line force is **unresolved pointwise**,
the typeset article is **BUILD UNVERIFIED**, five declarations await the author, and
the manuscript is **not submission-ready**.

### Verification performed on this archive

`unzip -t` reports no errors; the archive extracts to a clean scratch directory; **80
of 80** `MANIFEST.json` hashes recompute from the extracted tree; the archive contains
exactly **one** `main.tex`, all **ten** figure PDFs, and the **six** round-13 reports;
`Paper_A_Final_Submission/scripts/static_check.py` exits 0 on the extracted tree (104
labels, 75 references, 13 citation keys, 13 bib entries); the archived
`figures/fig10_field.pdf` is byte-identical to the re-rendered source file.

Gates run on the source tree after this round's edits: **52 tests OK** (47 carried
over + 5 new), 23 claims / 46 tokens / 11-of-11 source rows, 15 mutants caught,
phase-speed audit PASS. The full 18-gate battery was not re-run — no producer logic
changed; its last clean execution remains round 11's **18 PASS / 0 FAIL / 1 SKIP**.

### Read first, in this order

1. `PAPER_A_ROUND13_SUPERVISOR_HANDOFF.md` — what changed, what to read, readiness
2. `PAPER_A_ROUND13_PRE_EDIT_CLOSURE_AUDIT.md` — the audit, written before the first edit
3. `PAPER_A_ROUND13_FIG10_VECTOR_VERIFICATION.md` — the arrow: solve, fix, inspection, test
4. `PAPER_A_ROUND13_DOCUMENTATION_CORRECTIONS.md` — docstring, misattribution, caption, counts
5. `PAPER_A_ROUND13_TARGETED_VALIDATION.md` — what was executed, and what was not
6. `PAPER_A_ROUND13_LATEX_BUILD_AND_PAGE_PROOF.md` — the build: attempted, impossible, unverified
7. `PAPER_A_CORRECTION_HISTORY.md` — cumulative history (round-13 addendum last)

The round-11 and round-12 reports are included too; two round-12 documents carry a
dated round-13 status note (B1 and B6 closed) with their bodies unedited.

---

## Superseded archives

| round | size | SHA-256 (first 8 / last 4) | note |
|---|---|---|---|
| round 12 | 3,075,445 B | `dfe6b0c9…da1b` | section-by-section review; nineteen prose corrections |
| round 11 | 3,030,613 B | `6516d5f1…aa12` | programming and figure audit; battery 18/0/1 |
| round 10 | 2,960,652 B | `81d2452a…48c2` | manuscript structure and language; battery 17/1/1 (claim gate failed on round-off) |
| round 9 | 2,924,173 B | `85548a0c…a580` | plane-invariance correction |
| round 8 and earlier | — | — | retained for the record; not for review |

Only the round-13 archive should be used for review.
