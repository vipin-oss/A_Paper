# Round 14 — figure redesign audit

Ten figures, evaluated at journal reading size (single column ≈ 85 mm, double
column ≈ 170 mm). The reading-size test used here is the rendered PNG proof at
400 dpi, downsampled to the size the figure occupies in a printed column.

## 1. What was wrong

| Defect | Evidence | Fix in round 14 |
| --- | --- | --- |
| Families of five parameters were drawn as five shades of one hue (`RAMP_ELL` was five pinks; `RAMP_N0` five purples) | `figure_style.py`, ramps for carrier density, mobility, thickness, gradient length | each family is now a **different hue** — blue, green, orange, purple, neutral — with a lightness step that survives greyscale; no pastel member remains |
| Within a family, curves differed in colour only | fig02, fig03 plots | `ramp_styles()` gives every family member its own dash pattern **and** marker; no two curves can be confused in a greyscale print or by a colour-blind reader |
| Legends sat on top of the data | fig02(a), fig02(d), fig03(a), fig03(b) | family legends reduced from five rows to a compact three-column block, and axis headroom added so the box never covers a curve |
| F1's difference inset collided with the steep part of the dispersion curve and its tick labels ran into the main axis | fig01(a) | inset moved into the empty upper-middle region of the panel; y-ticks now carry $-180$ kHz, so the extreme shift is readable rather than clipped |
| F1 did not state the largest shift in the data set | data: $-183.7$ kHz at $k_xd=1.05$ for $H/H^*=+0.050$ | the value is now carried by the inset ticks and stated in the caption |
| F2's five carrier-density curves collapse onto one curve and the figure did not say why | data + non-dimensionalisation | the panel note now states that $n_0$ and $\mu$ enter only through the product $n_0\mu$ (verified: identical $Q$ and $\alpha$ to machine zero for equal products), so the collapse is a property of the model, not a plotting artefact |

## 2. Per-figure status

| Figure | Content | Round-14 change | Reading-size verdict |
| --- | --- | --- | --- |
| **F1** dispersion, velocity, linewidth, attenuation | five $H$ levels | palette unchanged (the $H$ triple is already teal/blue/ink/gold/crimson with distinct dashes and markers); inset relocated, ticks rescaled, $-183.7$ kHz made explicit | **pass, inspected at full size** |
| **F2** carrier density and mobility | two families of five | hue ramps, dash/marker per member, compact legends, headroom, equivalence note | **pass, inspected at full size** |
| **F3** thickness and gradient length | two families of five | hue ramps, dash/marker per member, legends no longer over data | **pass, inspected at full size** |
| **F4** frequency response, peak | five $H$ levels + zoom inset | no structural change; the narrow peak keeps its dedicated inset (the response is $10^{-3}$ wide in $k_xd$ and cannot be read on the main axis) | **pass at contact-sheet scale**; inset retained from round 12 |
| **F5** channel powers | fractions of incident power | unchanged | **residual risk** — annotation density is high at column width (see §3) |
| **F6** attenuation | five $H$ levels | unchanged | **pass at contact-sheet scale** |
| **F7** coupling sensitivity | $k_y$ slices, landscape, relative change | unchanged structurally; the relative-change panels (c,d) are the honest difference curves, not a synthetic subtraction | **pass at contact-sheet scale**; residual crowding in (c) legend |
| **F8** boundary and flux distributions | five $H$ levels | unchanged | **residual risk** — dense annotations at column width |
| **F9** validation | consistency, convergence | unchanged: temporal and spatial routes, residuals labelled as **residuals**, convergence separated from the precision floor | **pass at contact-sheet scale** |
| **F10** wave field and directions | field maps, direction diagram, flux ratios | **content frozen**: $k_B$ up-right at $+27.9^\circ$, $|k_B|/|k_i|=0.371$, $P_B$ down-left, drawn from the stored `primary_wavenumbers` | **pass, inspected at full size**; the round-13 correction is intact |

## 3. What is still not good enough

- **F5 and F8 annotations.** At true column width the text boxes in F5(c) and in
  F8(c,d) are crowded. They were not redesigned in this round, and no claim is
  made that they read cleanly at 85 mm. This is a known open defect.
- **Inspection coverage.** F1, F2, F3 and F10 were inspected at full size; F4,
  F6, F7 and F9 were inspected on a contact sheet after re-rendering; F5 and F8
  on the same sheet, where their crowding is visible but not resolvable. No
  figure was inspected as a *typeset* page, because there is no TeX engine in
  this environment and therefore no page to inspect.
- **No zoom of numerical noise.** No inset in the set magnifies a difference
  that sits at the level of floating-point error; where curves are numerically
  identical the figure says so in words (F2 patch, F7(c)) instead of separating
  them by an artificial offset.

## 4. Colour and greyscale audit

Every family member now differs in **three** channels — hue, lightness, and
dash/marker — and the coupling triple adds a fourth (marker fill).

Measured relative luminance (CIE, 0-100) of the five members of each ramp, and
the smallest step between neighbours:

| Ramp | L* of the five members | smallest adjacent step |
| --- | --- | --- |
| carrier density | 43.1, 27.1, 16.1, 8.8, 3.2 | 5.6 |
| mobility | 45.2, 29.0, 16.5, 8.3, 3.1 | 5.2 |
| thickness | 51.7, 37.1, 23.6, 12.7, 4.9 | 7.8 |
| gradient length | 52.1, 28.1, 14.0, 6.3, 2.5 | 3.8 |
| $k_y$ slices | 44.7, 26.4, 14.2, 6.6, 2.4 | 4.2 |

Five steps across a printable range cannot all be far apart in luminance, and
the smallest step (3.8 L*, the two darkest purples of the gradient-length family)
is **not** by itself a sufficient greyscale separation. The separation of those
two curves rests on their dash pattern and marker, which differ; this is stated
here so that the figure is not claimed to be greyscale-safe on luminance alone.
