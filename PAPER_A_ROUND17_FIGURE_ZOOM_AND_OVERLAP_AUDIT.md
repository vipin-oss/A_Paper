# Paper A — Round 17 figure overlap, zoom and coincidence audit

**Branch** `arena/ea7ca4dd-a-paper` · base `a68bb76` · BUILD UNVERIFIED.

Every figure was re-rendered from `paper_a_study/figure_data/` with
`generate_final_figures.py` and inspected **one at a time at manuscript width**
(`FIGURE_WIDTH_IN = 6.50`, PNG 2600×2040) — no contact-sheet verdicts. The data
files were not modified this round: the only change under `figure_data/` is
`figure_panel_sources.json`, which records the new file sizes and hashes. Every
number below is unchanged from round 16.

---

## 1. What was wrong, and what was done

| Fig | Defect found at width | Repair | Verified in render |
|---|---|---|---|
| **01** | the "operating point / k_xd = 0.736" label sat **on** the flat part of the branch, then (second attempt) ran past the axes into panel (b)'s y-label | label moved into the empty wedge right of the marker, right-aligned at axes fraction (0.975, 0.085), leader shortened | yes |
| **02** | panel (c) read as a polygonal curve because the sweep is sampled on a coarse wavenumber raster (kinks at 0.45/0.53/0.55/0.60) | the samples are now drawn as open symbols in the curve's own colour, and the note says the symbols mark the sampled wavenumbers; no interpolation, no smoothing | yes |
| **03** | clean | none | byte-identical re-render |
| **04** | (a) markers every second point merged into a band around the maximum, and the inset sat over the descending branch with its tick labels on the main curve | marker stride 2 → 9, line width 1.5, inset moved to the empty upper-left, opaque, labelled `R_B (%)` removed from its axis (main axis carries the unit), frame drawn | yes |
| **05** | clean | none | byte-identical |
| **06** | clean | none | yes (legend spacing changed) |
| **07** | (a) a free-floating note covered the **x tick labels**; (c) three `k_yd` families were drawn in three greys and its legend covered a curve endpoint; shared top legend clipped at the right margin | (a) note → left-aligned panel title; (c) three distinct hues (blue/deep orange/purple), marker-coded, labelled by a three-row legend in the empty lower-left corner; shared legend made compact (`handlelength` 1.9→1.24, `columnspacing` 1.0→0.62) | yes |
| **08** | shared top legend clipped at the right margin; the statement about five coincident levels was in (b) only and referred to nothing | legend spacing fixed as above; the coincidence statement moved to (c) (the panel with empty upper-left space) and now names panels (a)–(c) **and** quotes the bound | yes |
| **09** | clean | none | byte-identical |
| **10** | clean; panel (c) is the schematic that must be preserved | none; (c) untouched | yes |

The legend clipping was a *global* defect: `h_legend()` builds one shared legend
at `y = 0.998` with five entries whose text is
`$H/H^{*}=-0.050$ … $+0.050$`. At 6.5 in the old spacing needed ≈487 pt against
468 pt of canvas, so the last entry was cut. The new spacing needs ≈427 pt.

---

## 2. Coincidence, stated rather than zoomed

Two figures show curves that coincide, and in neither case is a zoom inset
appropriate — a zoom of an exact coincidence is a picture of nothing. Both are
now labelled with a number and the mechanism is derived in the text.

**(a) `fig08` (a)–(c): the five coupling levels give one profile.** The panel
statement is "the five `H/H*` levels coincide in (a)–(c): agreement to <0.9 % of
the peak value". The measured separations are stored per level; the bound quoted
is the peak-normalised maximum difference. The mechanism is in
`sec:results_boundary`, `eq:H_entry`: the coupling enters only through
`h∫b_i''ψ_j`, whose rows at degree six are `0, 0, 26.83, 91.65, 187.8, 315.9`;
at `h = ±1.06×10⁻²` the largest entry is 3.35 against an inertia entry of 58.3 in
the same row. A few per cent of one block moves the partition measurably
(`fig07`) and a normalised profile hardly at all. The paper says exactly that,
so the two figures no longer look contradictory.

**(b) `fig02` (c): the five carrier densities give one curve.** The note states
the collapse and why (`n₀` and `μ` enter only as `n₀μ`), and the text adds the
explicit reasoning: `n₀` enters through `Q² = d²q²n₀/(κ₃₃k_BT)` multiplying the
single potential block `A_φμ`, `μ` through `α_d = μ_ek_BT/(q d c_s)`, and the
response depends on the product. No zoom is drawn because the separation is at
the line width.

**(c) Where a zoom *is* legitimate — `fig04` (a).** The top of the response is
≈10⁻³ wide in `k_x d` and 94.7 % high, so the main axis cannot resolve it: an
inset on the same, uncut data is the honest device, and it is the one used. The
inset limits are 0.518–0.538 in `k_x d` and 78–97 % in `R_B`, both printed, both
the same units as the parent axis.

**(d) Where coincidence is *not* exact — `fig07` (c).** The three `k_yd` slices
differ by up to **0.44 percentage points** at `H/H* = ±0.05` (−1.149/−1.208/
−1.416 at the negative end; −2.000/−2.098/−2.442 at the positive end) and by
0.10 in the middle. They are therefore *not* coincident, and they are now drawn
in three hues with three markers and a legend, not as three greys.

---

## 3. Colour, line style and marker discipline

* Mechanical/coupling families keep the five-level ramp defined in
  `H_STYLE`: teal `#087E8B` (○ solid), blue `#3867D6` (□ dash-dot), ink
  `#202A44` (◆ solid), gold `#E3A008` (△ dashed), crimson `#C83E58` (▽ dotted).
* Where a *different* parameter family is plotted (density in `fig02`, mobility
  in `fig02(d)`, the three slices in `fig07(c)`), it gets a different hue set,
  not five shades of one hue.
* No artificial vertical offsets are used anywhere: where curves coincide they
  are drawn on top of each other and the coincidence is stated in words with a
  bound. This is deliberate — offsets would be a fabricated separation.
* Every inset has printed limits, the same units as its parent axis, an opaque
  face, its own tick size, and no legend.

---

## 4. Residual figure risks

1. `fig01`(a): the leader line from the label to the star passes close to the
   rising branch between `k_xd = 0.78` and `0.85`. It does not cross the curve,
   but at a narrower column width it might.
2. `fig02`(c): the coarse raster is now visible by design; a reader who expects a
   smooth peak may read the polyline as under-resolution. The note says
   otherwise, and `fig04` resolves the same quantity on a dense sweep.
3. `fig06`(a) and (d): the small inset-free notes sit close to the bottom frame
   (≈2 pt clearance). Legible in the 2600 px render; not measured in the PDF.
4. None of this was checked in a compiled PDF. Column width, font substitution
   and float placement are unverified.
