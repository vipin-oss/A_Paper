# Paper A — downloadable complete project

## Round 12 (current)

```
Paper_A_Complete_Project_round12.zip
231 entries · 3,075,445 bytes (3.08 MB)
SHA-256  dfe6b0c965932a693e4673496869a9657441416783dd1b0bdcd9d6683591da1b
```

**Direct one-click download** (no Git client, no checkout, no PowerShell):

<https://github.com/vipin-oss/A_Paper/raw/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round12.zip>

Open the link, press "Download", unzip, and start with `START_HERE.txt` at the top of
the archive.

### What round 12 is

A section-by-section review of the manuscript — mathematics, physics, language, and
what a journal requires — with every number traced to a stored record. It changed
**no equation, no constant, no boundary condition, no solver, no dataset, no figure
PDF and no reported number**.

Before any manuscript text was touched, two round-11 *reporting* defects were
corrected, because the text would otherwise have been reviewed against numbers that
do not exist:

* the round-11 "headline stability between runs" number (1.5×10⁻⁷) pooled a
  comparison at two **different** wavenumbers with one at a fixed wavenumber. At
  fixed wavenumber the difference is 7.5×10⁻¹⁰ (at $k_xd=0.52752$) and 1.0×10⁻¹⁰
  (at 0.5275); the 1.5×10⁻⁷ is the argmax-to-reported-sample offset, a sampling
  quantity, not a reproducibility one;
* the 8.4×10⁻⁶ that round 11 called the "branch-tracking-path sensitivity" is the
  **coarse-raster sampling error** (`restart_spread`, 8.69×10⁻⁶ relative). The
  tracking-path spread is exactly **0.0**: ascending, descending and single-step
  paths return identical values.

Then nineteen prose defects were repaired (`PAPER_A_ROUND12_EDIT_LEDGER.md`), ten of
them places where the text disagreed with the paper's own delivered data:

* the density and mobility sweeps were described with factors of nine, ten and five;
  the stored columns scale by exactly **three** (0.00084 → 0.00251 MHz, 0.244 → 0.732
  dB/mm), and the two sweeps are one sweep, because density and mobility enter
  through their product;
* the phase speeds were transposed (105.8 km/s belongs to $k_xd=0.15$, 20.0 to 1.05);
* two gradient-length percentages were attached to abscissae (0.15, 1.05) that the
  solved grid does not contain; the values are at 0.145 and 1.000;
* the attenuation length "falls by a factor of three" stood next to "falls from
  18.5 mm to 0.30 mm, a factor of sixty-two" — the stored lengths are 18.5, 0.538 and
  0.300 mm;
* the energy budget quoted five wrong numbers in six sentences: the four printed
  shares close to 8.3×10⁻⁶ (twice the signed interference term), the stored identity
  residual is 3.4×10⁻¹⁶, the stored power balances are 7.3×10⁻¹³ and 3.2×10⁻¹³, and
  0.99769 is the sum of the two **propagating** terms;
* the backward wavenumber was written $(0.333,-0.530)$ — two different ratios and
  the sign of the flux; the solved vector is $(0.24517,+0.12981)\propto(1,0.529)$,
  $27.9^\circ$ **above** the $+x$ axis, with the flux $(-1,-0.530)$ opposite it;
* a reproducibility paragraph quoted a sensitivity pair ($1.8\times10^{-12}\to
  5.6\times10^{-6}$) that exists in no record, and a build stamp of
  $\pm6\times10^{-6}$ with it; it now rests on the registered spreads;
* the appendix's test count had gone stale by eight (39 → 47), its timing by a
  factor of three, and its data-file count by one;
* "three-term polynomial" for a system whose displayed sum spans $k^0\ldots k^4$;
  $\alpha$ used for two different quantities; "Five limitations" before six
  paragraphs; $\ell$ for the distance from the edge in prose while the panel uses
  $L$; the abstract's "The figure" with no antecedent.

### One thing round 12 did **not** fix

`fig10(c)` draws the backward wavenumber arrow along $(0.333,-0.530)$, i.e. 58°
*below* the $+x$ axis; the solved wavenumber points 27.9° *above* it. The prose is
correct now; the frozen figure is not. Figure PDFs and plotting code are frozen for
this round, so it is reported in `PAPER_A_ROUND12_BLOCKING_ISSUES.md` (B1) and left
for the figure round. One line, one arrow.

### What round 12 did not change

The governing equations, the constitutive constants, the boundary conditions, the
solver, the discretisation, the material data, all ten figure PDFs, all datasets,
and every reported number: 2.31456 %, 94.6795 % at $k_xd=0.5275$, 16.6547 GHz,
0.9855722 at the edge plane, 99.77 % propagating, 62.2973 % at $k_xd=0.55$, the
34.2 / 11.1 / 1.21 % coupling decomposition, and the four certified values.

Also unchanged: the maximum is **local**, the parameters $\ell$, $f$, $H$ are
**synthetic**, the novelty status is **UNRESOLVED**, the corner field is
**unresolved**, the typeset article is **BUILD UNVERIFIED**, five declarations await
the author, and the manuscript is **not submission-ready** — for those reasons, not
for anything an editorial round can fix
(`PAPER_A_ROUND12_READINESS_ASSESSMENT.md`, which assesses numerical and scientific
readiness separately).

### Verification performed on this archive

`unzip -t` reports no errors; the archive extracts to a scratch directory; **80 of 80**
`MANIFEST.json` hashes recompute correctly from the extracted tree; the archive
contains exactly **one** `main.tex`; `Paper_A_Final_Submission/scripts/static_check.py`
exits 0 on the extracted tree (104 labels, 75 references, 13 citation keys, 13 bib
entries). Gates run on the source tree after this round's edits: 47 tests OK, 23
claims / 46 tokens / 11-of-11 source rows, 15 mutants caught, phase-speed audit PASS.

### Read first, in this order

1. `PAPER_A_ROUND12_PRELIMINARY_EVIDENCE_CORRECTIONS.md` — start here: the two round-11 fixes
2. `PAPER_A_ROUND12_SECTION_BY_SECTION_REVIEW.md` — the review, section by section
3. `PAPER_A_ROUND12_EDIT_LEDGER.md` — all nineteen edits, before and after
4. `PAPER_A_ROUND12_NUMERICAL_TRACEABILITY_AUDIT.md` — every number against its record
5. `PAPER_A_ROUND12_READINESS_ASSESSMENT.md` — numerical and scientific readiness
6. `PAPER_A_ROUND12_BLOCKING_ISSUES.md` — what is still open, and why
7. `PAPER_A_ROUND12_CORRECTION_HISTORY.md` — what was done, in order
8. `PAPER_A_CORRECTION_HISTORY.md` — cumulative history (round-12 addendum at the end)

The round-11 reports are included as well. Two of them carry "Corrected in round 12"
annotations where round 11 mislabelled a reproducibility number.

---

## Superseded archives

| round | size | SHA-256 (first 8 / last 4) | note |
|---|---|---|---|
| round 11 | 3,030,613 B | `6516d5f1…29aa12` | programming and figure audit; battery 18/0/1; two reproducibility labels corrected in round 12 |
| round 10 | 2,960,652 B | `81d2452a…48c2` | manuscript structure and language; battery 17/1/1 (claim gate failed on round-off) |
| round 9 | 2,924,173 B | `85548a0c…a580` | plane-invariance correction |
| round 8 and earlier | — | — | retained for the record; not for review |

Only the round-12 archive should be used for review.
