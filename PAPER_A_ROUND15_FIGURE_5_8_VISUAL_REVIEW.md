# Round 15 — Figure 5 and Figure 8 visual review

Both figures were rendered, inspected at full page size (the 400 dpi proof
downsampled to the width the figure occupies in a printed column), repaired, and
re-inspected. The data behind both figures were **not** touched: every plotted
value comes from the same stored CSVs as round 14, and the figure-data agreement
tests pass.

---

## Figure 5 — channel powers

### Defects found (before)

| Panel | Defect |
| --- | --- |
| (b) | The four-entry legend sat directly on the `other prop.` curve at `10⁰`: the square markers passed behind the legend box, and the top decade of the axis was empty. |
| (c) | The text `round-off floor` was placed at the bottom-right, on top of the shaded band and against the right axis frame, where it collided with the last data marker. |
| (a) | No defect: the categorical marker plot is legible. |
| (d) | No defect. |

### Repairs applied (minimal, layout only)

1. Panel (b): y-limit raised from `3.0e1` to `3.0e2`, so the legend occupies two
   empty decades and no curve passes behind it.
2. Panel (c): the floor annotation moved to the empty middle band
   (`4e-10`, left-aligned) and reworded to `round-off floor of the solver`.

### After

- (b): legend clear of all four curves; the `10⁰` curve is fully visible.
- (c): threshold line labelled `10⁻⁶`, floor annotation in empty space, data and
  shaded band untouched.
- (a), (d): unchanged and legible.

**Verdict: PASS at reading size, after inspection of the repaired render.**

---

## Figure 8 — through-thickness boundary profiles

### Defects found (before)

| Panel | Defect |
| --- | --- |
| (a), (b) | Five curves were drawn but only one is visible — the levels coincide — with nothing said. The zero reference was a solid dark vertical line that reads as a sixth data curve. |
| (b) | x tick labels collided: `−0.0050−0.00250.0000…` ran together into an unreadable string. |
| (c) | Five overlapping curves, no statement that they coincide. |
| (d) | Legend at lower left sat on the incident profile. |

### Repairs applied

1. (a), (b): the zero reference is now a thin dotted line in the neutral palette,
   so it cannot be mistaken for data.
2. (b): explicit ticks at `−0.006, −0.003, 0, 0.003, 0.006` with three-decimal
   labels and an x-range of `±0.0068`; the collision is gone.
3. (b): a boxed note states what the figure is actually showing — *all five
   `H/H*` levels: profiles agree to < 0.9 % of the peak* — in the empty right-hand
   region of the panel. The 0.9 % is measured from the stored data
   (max relative spread `8.26e-3` for `P_x`, `6.09e-3` for `P_z`), not asserted.
4. (d): legend moved to the upper-left, reduced to `6.8 pt` with a shorter handle;
   it no longer overlaps either profile.
5. Caption: now states the coincidence, the measured bound, and that the dotted
   vertical line is a zero reference and not a sixth curve.

### After

- (a): single visible profile, dotted zero line, no clutter.
- (b): legible ticks, note in empty space, no overlap.
- (c): unchanged curve, coincidence now declared in the caption.
- (d): legend clear of both curves.

**Verdict: PASS at reading size, after inspection of the repaired render, for
panels (a)–(d).** The residual limitation is stated: because the five profiles
coincide, panels (a)–(c) cannot show the coupling dependence, and the figure does
not pretend to; the coupling dependence is quantified in Figure 7.

---

## What is *not* claimed

- No page was rendered by a TeX engine (none exists here); "reading size" means
  the rendered figure at its manuscript width, not a typeset page.
- No figure data was regenerated; only layout, ticks, legend placement and
  annotation text changed.
- Figure 10 was not touched: the backward wavenumber remains up-right at
  `+27.9°`, `|k_B|/|k_i| = 0.371`, and the flux `P_B` down-left, as protected by
  the round-13 test class.
