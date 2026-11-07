# Paper A — round 13: documentation corrections

Three corrections to records, one caption, and two counts that this round's own
new tests made stale. No equation, constant, boundary condition, solver, dataset or
reported number was touched.

Baseline `3827543016ece4a9d0612e861bf75425457291bf`.

---

## 1. `peak_search.py` — the docstring contradicted its own output (B6)

### Before

```
Convergence is measured three ways and reported separately: Galerkin degree,
quadrature order, and -- because R_B is evaluated on a tracked branch -- the
sensitivity to the branch-tracking path.  The last one is not a discretisation
error, but near a zero-group-velocity fold it dominates the reproducibility of
the printed digits, so it is measured rather than assumed.
```

Two things are wrong with it. It calls three diagnostics "four" quantities'
worth of confusion by naming four keys for three, and — the substantive error — it
asserts that the tracking-path sensitivity dominates the printed digits. The
module's own output says the opposite: `peak_search.json` →
`verdict.tracking_path_relative_spread = 0.0`, and the quantity that is large near
the fold is `verdict.restart_spread = 8.361657806821299e-06` (8.69e-6 relative),
the coarse raster's sampling error.

### After

```
Convergence is measured on four separate diagnostics, each reported under its own
key and none of them allowed to stand in for another:

  * ``degree_spread``             Galerkin degree, 22 vs 26/30;
  * ``quadrature_spread``         quadrature rule at a fixed degree;
  * ``tracking_path_relative_spread``
                                  because R_B is evaluated on a tracked branch,
                                  the same value is reached from below, from above
                                  and in a single step.  In the delivered data the
                                  three paths agree to the last stored digit and
                                  the spread is 0.0, so tracking order is not a
                                  source of error here;
  * ``restart_spread``            the sampling difference between the coarse
                                  raster's best sample and the refined maximum.
                                  This is the one that is large near the
                                  zero-group-velocity fold (8.4e-6 absolute,
                                  8.7e-6 relative in the delivered run); it is a
                                  discretisation of the search, not a dependence
                                  on the path taken to the fold.

The distinction matters: an earlier revision of this docstring called the
tracking-path sensitivity the dominant term, which the delivered numbers
contradict.  Nothing about the search itself depends on that wording -- the
four diagnostics are computed independently and stored -- but the record should
describe what is stored, not what was assumed before it was measured.
```

### Why no calculation changed

The docstring is a module-level string literal. Nothing imports it, nothing parses
it, and the search code below it is byte-identical. `peak_search.json` was **not**
regenerated: it is a ~5-minute search whose inputs did not change, and re-running
it would produce a new timestamp and call it a result. The keys named in the
docstring were checked against the delivered record before the text was written:

| key in the docstring | present in `peak_search.json` → `verdict` | value |
|---|---|---|
| `degree_spread` | yes | dict (argmax 5.6e-9, reported 6.2e-9) |
| `quadrature_spread` | yes | 4.3174455076703166e-10 |
| `tracking_path_relative_spread` | yes | 0.0 |
| `restart_spread` | yes | 8.361657806821299e-06 |

---

## 2. The 0.622973 configuration (D1)

### Where the error was

`PAPER_A_ROUND12_CORRECTION_HISTORY.md`, §"Not superseded by this round", and the
same sentence copied into `downloads/README.md`:

> … 99.77 % propagating, **62.2973 % at $k_xd=0.55$** …

### What the records say

| configuration | $H/H^{*}$ | $R_B$ | record |
|---|---|---|---|
| `refined_peak` (the reported peak, $k_xd=0.5275$) | 0 | 0.9467952 | `mechanism_controls.json` |
| `refined_peak` | +0.05 | **0.6229733** | `mechanism_controls.json` → `refined_peak.full.R_B` |
| `k055_sample` ($k_xd=0.55$) | 0 | 0.5791800 | `k055_sample.no_coupling.R_B` |
| `k055_sample` | +0.05 | 0.5221071 | `k055_sample.full.R_B` |

So 62.2973 % belongs to the **reported peak with the coupling at its tabulated
extreme**, not to $k_xd=0.55$. At 0.55 the coupling-on share is 52.21 % and the
coupling-off share is 57.92 %.

### Correction

Both files now read "62.2973 % at $k_xd=0.5275$ with $H/H^{*}=+0.05$", and both
carry a dated note giving the wrong abscissa, the right one, and the two 0.55 values
— the evidence is annotated rather than deleted.

### The manuscript was right all along

`results.tex` §4.10:

> "The branch-consistent sweep is monotone in $|H|$: at the maximum $R_B=0.9468$,
> $0.7711$, $0.6230$ for $H/H^{*}=0$, $+0.025$, $+0.05$ and $0.8636$, $0.7006$ for
> $-0.025$, $-0.05$."

"At the maximum" is the reported peak. The 0.55 sentences in the same subsection
quote 9.85 % and −0.009 %, which are the `k055_sample` deltas and are correct. The
manuscript is **not** edited for this item.

### The four configurations, kept apart

The five nearby abscissae are now used consistently in every current document:

| label | value | what it is |
|---|---|---|
| operating point | $k_xd=0.7362$ | the H = 0 baseline of §4.1–4.3, $R_B=0.0231456$, 16.6841 GHz; also the configuration drawn in fig10 |
| reported high-fraction point | $k_xd=0.5275$ | the released headline, $R_B=0.9467952$, 16.6546 GHz |
| refined argmax | $k_xd=0.52752$ | the raster's own maximum, $R_B=0.9467954$, 1.4e-7 above the reported one |
| earlier sample | $k_xd=0.525$ | the round-7 sample, `round7_sample`, $R_B=0.9318915$ |
| independent sample | $k_xd=0.55$ | the flank check, `k055_sample`, 0.5791800 at H=0 |

---

## 3. The fig10 caption under-described its own panel (D2)

| | |
|---|---|
| Location | `sections/results.tex`, the `\caption` of `fig:fig10` |
| Before | "(c) schematic whose arrows are the solved **flux** directions of the incident and backward modes" |
| After | "(c) schematic whose arrows are the solved **wavenumber and flux** directions of the incident and backward modes" |
| Reason | the panel draws $\vect{k}_i$, $\vect{k}_B$, $\vect{P}_i$, $\vect{P}_B$; after the B1 correction it is the *distinction* between the wavenumber pair and the flux pair that the panel exists to show, and the caption named only one pair |

The §4.15 sentence that introduces the panel ("Panel (c) is a schematic, but its
arrows are not drawn by hand: they are the solved directions") already general, and
is unchanged.

---

## 4. Two counts this round made stale

Adding five tests changes the suite from 47 to 52. The appendix states the count in
three places; they are now 52 (and the suite's runtime stays at ~25 s).

| location | before | after |
|---|---|---|
| `appendix_reproducibility.tex`, file table | "the 47 automated checks of §3" | "the 52 automated checks" |
| `appendix_reproducibility.tex`, prose | "an automated suite of 47 tests" | "an automated suite of 52 tests" |
| `appendix_reproducibility.tex`, command list | "# 47 tests, ~25 s" | "# 52 tests, ~25 s" |
| `PACKAGE_README.md`, command list | "# 47 tests, ~21 s" | "# 52 tests, ~25 s" |

The historical reports keep their own counts: `PAPER_A_ROUND11_*` and
`PAPER_A_ROUND12_*` describe 47 tests because 47 is what their rounds ran. Round 13
records the change here and in the correction history rather than editing those
documents.

---

## 5. Consistency sweep, item by item

Every current document and the manuscript were read for the eight classes of defect
the round was asked to look for.

| class | finding |
|---|---|
| wrong wavenumber/value pairings | **one found and fixed** (D1, 62.2973 % ↔ 0.55, in two files). All other pairings checked against `mechanism_controls.json`, `peak_identity_audit.json`, `peak_search.json` and `peak_certification.json`; the four nearby abscissae are as in §2's table |
| incorrect physical-plane labels | none. 0.9467952 is the reference plane $L=10d$; 0.9855722 is the edge plane; 0.5791800 is at $k_xd=0.55$; the manuscript states the plane at every occurrence |
| modal share vs total reflectance | none in the manuscript. "Reflectance" appears six times and every one is contrastive ("is not a reflectance", "closest to a reflectance"); `claim_audit` and `test_backward_share_is_never_called_a_reflectance` both guard the phrase |
| tracking spread vs sampling error | **one found and fixed** (B6, the docstring). The manuscript does not confuse them: §4.6 quotes the degree and quadrature spreads, §4.7 quotes the argmax offset as a difference of abscissae |
| unsupported reproducibility statements | none remain; the round-12 removal of the 1.8e-12 → 5.6e-6 pair is intact and no new one was introduced |
| superseded numerical values | none in current documents. The round-10/11/12 values survive only inside those rounds' own reports, each of which is dated and scoped to its round |
| incorrect figure-panel references | none. `claim_audit` confirms figures are first cited in order 1…10; the panel map matches the plotting code (`test_panel_map_agrees_with_the_plotting_code`) |
| stage references | none in the manuscript; reports name their own rounds, which is what they are for |
| contradictory build statuses | none. Every current document says the same thing: **BUILD UNVERIFIED — no compiler execution possible**, and none presents an older PDF as current |
| stale counts | **two found and fixed** (§4: 47 → 52 in the appendix, three places, and in the package README) |

Two round-12 documents were annotated rather than rewritten, because their text is
the record of what round 12 found: `PAPER_A_ROUND12_BLOCKING_ISSUES.md` now opens
with a dated round-13 status note (B1 and B6 closed, B2/B3/B4/B5 still open), and
`PAPER_A_ROUND12_READINESS_ASSESSMENT.md` likewise.

---

## 6. What was deliberately not touched

* `peak_search.json`, `peak_certification.json`, `mechanism_controls.json`,
  `peak_identity_audit.json`, all eleven figure CSVs except the fig10 metrics
  addition: not regenerated, not edited.
* Every historical report's numbers: kept, with dated notes where a status changed.
* The manuscript's §4.10, §4.15 and every other numeric sentence: unchanged, because
  the numbers in them were already correct.
