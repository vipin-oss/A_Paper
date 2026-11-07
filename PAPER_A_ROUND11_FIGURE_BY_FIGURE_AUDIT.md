# Paper A — Round 11: figure-by-figure audit

Ten figures, forty panels, inspected three ways: (i) the committed vector PDF,
(ii) its committed raster at publication size (2600 × 2040 px, i.e. 400 dpi on the
6.50 × 5.10 in canvas), read panel by panel, and (iii) the code that draws them
against the CSV/JSON columns it reads. A finding is recorded only when at least
two of the three views agree.

Status vocabulary
-----------------
* **EXACT DATA AGREEMENT** — the panel's plotted columns are reproduced by a clean
  re-run of the generator to the stated tolerance, and the panel is legible and
  correct.
* **VISUAL-SEMANTIC** — the panel is legible and its meaning is correct, but the
  statement it makes is qualitative (ordering, coincidence, shape), so it is
  judged as a visual claim and cross-checked against the data.
* **DIFFERENCE EXPLAINED** — something differs between the delivered and the
  regenerated rendering, and the difference has a measured cause.
* **FAIL** — the panel contradicts the data or the text.
* **UNVERIFIED** — could not be decided here.

Reproduction tolerance per panel is the maximum relative difference between the
delivered CSV and the freshly generated one, restricted to the columns that panel
plots (`PAPER_A_ROUND11_NUMERICAL_REPRODUCIBILITY.md` gives the full table).

---

## fig01 — dispersion, wave speeds, linewidth, attenuation
`fig01_dispersion.pdf` · data `fig01_dispersion_velocity_attenuation.csv`

| panel | status | evidence |
|---|---|---|
| (a) $f(k_xd)$, five levels, operating point | **EXACT DATA AGREEMENT** (0.0 relative on `frequency_GHz`); **defect D11 repaired** | The inset plotted $\Delta f$ with `ylim = (-150, 150)` kHz while the $H/H^*=+0.05$ curve reaches $-\SI{183.7}{\kilo\hertz}$: the curve left the frame and the reader could not see the largest shift the text discusses. The inset is now $[-200, 215]$ kHz with ticks at $\pm150$, and every point is inside the frame. |
| (b) phase, group and energy velocity | **EXACT** ($2.8\times10^{-9}$, $1.9\times10^{-10}$) | Left axis signed velocities, right axis phase speed; the zero-crossing just below $k_xd=0.53$ is visible; the dashed phase curve is on its own coloured axis and cannot be misread as negative. |
| (c) linewidth | **EXACT** ($4.6\times10^{-6}$) | Log axis justified (three decades). |
| (d) attenuation | **EXACT** ($3.9\times10^{-8}$) | Log axis justified (two decades). |

The **text was wrong, not the panel**: §4.1 claimed the coupling shifts the
frequency "by at most $\pm\SI{60}{\kilo\hertz}$ … less than $4\times10^{-6}$",
while the stored data of this very panel give $\SI{183.7}{\kilo\hertz}$
($1.09\times10^{-5}$) at $k_xd=1.05$ and $\SI{92}{\kilo\hertz}$ for the negative
coupling. The sentence now quotes the measured values and the number is
registered (`coupling_frequency_shift_max`).

---

## fig02 — carrier density and mobility
`fig02_material.pdf` · data `fig02_material_parameter_sweep.csv`

| panel | status | evidence |
|---|---|---|
| (a) FWHM vs $n_0$ | **EXACT** ($3.7\times10^{-6}$) | five ordered families, log axis. |
| (b) attenuation vs $n_0$ | **EXACT** ($7.5\times10^{-8}$) | — |
| (c) backward share at $L=2\,\mu$m | **EXACT** ($3.5\times10^{-8}$); **defect D1 repaired** | The axis read "backward **reflectance** $R_B$ (%)", contradicting the paper's central caveat that $R_B$ is a modal share. It now reads "$R_B$ at $L=2\,\mu$m (%)" with the in-panel note "backward modal share at $L=2\,\mu$m". The five $n_0$ curves coincide within $0.2\%$ as the note says. |
| (d) FWHM vs mobility | **EXACT** | log axis. |

---

## fig03 — geometry families
`fig03_geometry.pdf` · data `fig03_geometry_sweep.csv`

| panel | status | evidence |
|---|---|---|
| (a) $f$ vs $k_xd$ for the thickness family | **EXACT** ($5.9\times10^{-12}$) | five thicknesses, separated. |
| (b) $f$ vs $k_xd$ for the gradient-length family | **EXACT** | five lengths, nearly coincident — the point of the panel. |
| (c) $\Delta f$ at $k_xd=0.50$ vs thickness | **EXACT** | — |
| (d) $\Delta f/f_0$ vs $k_xd$ for $\ell$ | **EXACT** | sign change across $\ell=50$ nm is visible. |

The §4.3 percentages quoted in the text ($+1.9\%$ at $k_xd=0.1$, $-1.8\%$) were
recomputed from this file: the stored values are $+2.0\%$ at $k_xd=0.15$ (the
first solved point — the grid does not contain 0.1) and $-1.9\%$; the text now
quotes those (D13).

---

## fig04 — reference-plane share, energy angle, wavenumber ratio, group velocity
`fig04_frequency.pdf` · data `fig04_frequency_reflection.csv`

| panel | status | evidence |
|---|---|---|
| (a) $R_B$ vs $k_xd$ with peak inset | **EXACT** ($2.0\times10^{-8}$); **defect D2 repaired** | Axis read "$R_B$ at $\ell=2\,\mu$m", using the gradient-length symbol for the reference-plane distance. It now reads $L=2\,\mu$m. The inset, which touched the descending flank, is lifted clear. |
| (b) energy angle | **EXACT** ($3.3\times10^{-9}$) | — |
| (c) $R_B$ vs $k_{Bx}/k_{ix}$ | **EXACT** ($5.6\times10^{-9}$); **D2 repaired** | the collapse of all five $H$ levels onto one curve is the panel's claim and it holds. |
| (d) group velocity | **EXACT** ($3.6\times10^{-6}$) | zero crossing marked by the dashed line at the reported wavenumber. |

---

## fig05 — channel power accounting
`fig05_channel.pdf` · data `fig05_channel_power.csv`

| panel | status | evidence |
|---|---|---|
| (a) modal budget at $H=0$ | **EXACT** ($1.7\times10^{-11}$) | four channels placed at their measured fractions on a log axis. |
| (b) the same four vs $H$ | **EXACT** ($1.7\times10^{-11}$) | — |
| (c) power-balance residual | **DIFFERENCE EXPLAINED**; **defect D6 repaired** | All five residuals lie between $2.5\times10^{-13}$ and $1.3\times10^{-12}$, i.e. at the double-precision floor, against an acceptance threshold of $10^{-6}$. The panel now shades the floor band and labels it "round-off floor"; the axis reads "power-balance residual". The visible undulation is noise and is no longer presented as resolved structure. |
| (d) relative change of the share | **EXACT** | — |

---

## fig06 — distance from the edge, survival, attenuation lengths
`fig06_attenuation.pdf` · data `fig06_attenuation_distance.csv`

| panel | status | evidence |
|---|---|---|
| (a) $R_B(L)$ | **EXACT** ($5.9\times10^{-9}$); **defect D3 repaired** | Axis read "distance from edge $\ell$ ($\mu$m)" with $\ell$, the gradient length, and the ordinate read $R_B(\ell)$. Both now use $L$. |
| (b) incident survival | **EXACT** ($6.5\times10^{-9}$); **D3 repaired** | same symbol repair. |
| (c) attenuation length | **EXACT** ($2.1\times10^{-8}$); **D3 repaired** | The axis used $L$ (mm) for the attenuation length while $L$ means distance from the edge. It now reads "attenuation length (mm)"; no symbol is reused with two meanings. |
| (d) attenuation coefficient | **EXACT** | $\alpha=2|\Imag k|$ note retained. |

---

## fig07 — transverse-wavenumber coupling
`fig07_coupling.pdf` · data `fig07_coupling_sensitivity.csv`

| panel | status | evidence |
|---|---|---|
| (a) $R_B$ vs $k_yd$ | **VISUAL-SEMANTIC** ($1.4\times10^{-11}$) | the panel's claim is that $H$ matters far less than $k_y$; the five curves overlap to within a few percent while $k_y$ changes $R_B$ by $35\%$. Verified against the CSV: the $k_y$ range alone spans $0.0190$–$0.0256$. |
| (b) $(k_yd, H)$ landscape | **VISUAL-SEMANTIC** | drawn on the measured grid, no interpolation — stated in the caption and true of the code (`pcolormesh` on the kernel grid). |
| (c) $\Delta R_B/R_B$ vs $H$ | **VISUAL-SEMANTIC** ($6.0\times10^{-9}$) | three declared slices. |
| (d) $\Delta R_B/R_B$ vs $k_yd$ | **VISUAL-SEMANTIC** | — |

No change was made to this figure: it is clear, it agrees with its data, and its
only defect would have been the stale panel map, which is fixed at the source.

---

## fig08 — through-thickness flux profiles
`fig08_boundary.pdf` · data `fig08_thickness_flux.csv`

| panel | status | evidence |
|---|---|---|
| (a) $P_x^{B}(z)/P^{inc}$ | **EXACT** | five profiles with the characteristic change of sign through the thickness. |
| (b) $P_z^{B}(z)/P^{inc}$ | **EXACT** ($1.9\times10^{-9}$) | — |
| (c) running through-thickness integral | **EXACT**; **defect D24 repaired** | The xlabel is a tall integral expression and was **cut by the bottom edge of the canvas** (the stored PNG had ink in its last three rows, which no other figure has). The bottom margin of this figure was raised to 0.150; a pixel test now asserts that no panel has ink in the first or last row or column of any figure. |
| (d) backward vs incident mode shape | **EXACT** | normalised shapes, declared in the axis label. |

---

## fig09 — convergence and residual diagnostics
`fig09_validation.pdf` · data `fig09_validation_convergence.csv` and `fig09_temporal_spatial_consistency.csv`

| panel | status | evidence |
|---|---|---|
| (a) $\lvert\Delta R_B\rvert/R_B$ vs degree | **DIFFERENCE EXPLAINED** ($2.0\times10^{-4}$); **defect D7/D22 repaired** | The curve fell below the axis minimum ($10^{-9}$) and left the frame. The axis now runs to $10^{-13}$ and the note says "below $10^{-9}$: round-off floor". |
| (b) $\lvert\Delta k_B\rvert/\lvert k_B\rvert$ vs degree | **DIFFERENCE EXPLAINED** (values $\sim10^{-13}$); **D7 repaired** | axis extended to $10^{-15}$. |
| (c) edge residual and energy-balance error | **DIFFERENCE EXPLAINED** (edge residual $1.8\times10^{-1}$ relative, power error $1.6\times10^{1}$ relative — both are changes *of numbers near $10^{-15}$*, i.e. the floor); **D7 repaired** | the ordinate now reads "residual magnitude" and the note reads "floor $\sim10^{-15}$: not a convergence trend". The two tolerance lines ($10^{-8}$, $10^{-10}$) are unchanged. |
| (d) temporal vs spatial mismatch | **EXACT** ($2.5\times10^{-6}$ on $\omega_i$) | agreement $\approx2\times10^{-5}$ as the note says. |

The large *relative* differences in panel (c) are the clearest illustration of why
this round insisted on floor statements: a 16-fold change in a quantity whose
value is $10^{-15}$ is not a change in the physics. After the label, the panel and
the data agree about what the reader is looking at.

---

## fig10 — field maps and flux directions
`fig10_field.pdf` · data `fig10_field_maps.csv`, `fig10_field_metrics.json`

| panel | status | evidence |
|---|---|---|
| (a) incident intensity map | **EXACT** | shared colour scale, normalised to a common maximum. |
| (b) backward intensity map | **EXACT** ($1.5\times10^{-7}$) | same scale as (a), so the two are directly comparable. |
| (c) schematic | **VISUAL-SEMANTIC**; **defect D5 repaired** | The panel is a drawing, not a plot. It carries an in-panel italic label "schematic"; the caption already states that every arrow direction is taken from the solved flux. Nothing was removed. |
| (d) $P_{Bx}/P_{ix}$, $P_{By}/P_{ix}$ vs $k_yd$ | **EXACT** | both fractions negative, as the caption says. |

---

## Cross-figure checks

* **No ink at the canvas edge** in any of the ten 400 dpi renders (pixel test,
  now a unit test).
* **Shared legend** in the reserved top band, never over data, in
  fig01, 04, 06, 08.
* **Figure first-citation order** 1→10 in `results.tex` (checked by the registry
  gate).
* **Captions readable without the code**: every caption names its data file and
  the quantity in each panel; none refers to a variable that is not in the paper.
* **Two panels were left deliberately unchanged** although they could be
  restyled: fig05(a) (the four-channel budget) and fig07(b) (the measured
  landscape). They are already legible and their data are exact; restyling them
  would be appearance work, which this round does not do.

## Summary

| status | figures |
|---|---|
| EXACT DATA AGREEMENT | fig01, fig02, fig03, fig04, fig05, fig06, fig08, fig10 |
| VISUAL-SEMANTIC (and exact) | fig07, and fig10(c) within fig10 |
| DIFFERENCE EXPLAINED (floor values, now labelled) | fig09 |
| FAIL | none |
| UNVERIFIED | none — all ten were rendered, read and cross-checked |

Eight label/graphic defects were repaired (D1, D2, D3, D5, D6, D7, D11 inset,
D22, D24); no figure was redesigned, no axis was rescaled except to stop a curve
from leaving the frame, and no data point was removed.
