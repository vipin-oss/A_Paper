# Paper A — figure-wise scientific and visual audit (final)

_Negative reflection of guided waves in a flexoelectric piezoelectric–semiconductor plate with carrier–strain-gradient coupling_

Audit date: 2026-11-06. Branch: `arena/ea7ca4dd-a-paper`.
Every statement below was checked against the committed CSV/JSON in
`paper_a_study/figure_data/` and against the rendered PDFs in
`paper_a_study/figures_final/` (rasterised at 150 dpi for inspection).
A PASS is recorded only when **both** the scientific gate and the visual gate
are satisfied; a data check never certifies a PDF and a good-looking PDF never
certifies the physics.

## 0. Gate definitions used here

**Scientific gate.** Every plotted row satisfies
`0 ≤ R_B ≤ 1`, `|θ_E| < 80°`, power balance `< 10⁻⁶` and scaled edge residual
`< 10⁻⁸`. Rows that fail are written to the CSV but are never drawn.
Attenuation is always `α = 2|Im k|` of a solved complex root; no zero is
invented for a real root.

**Visual gate.** Canvas exactly 6.50 × 5.10 in (`\textwidth` of `main.tex`),
`savefig.bbox = None` (no silent rescaling), 11 pt serif axis labels, 9–9.5 pt
ticks, 9 pt legends, 11 pt bold panel tags, 1.8–2.2 pt data lines, the five
mandated `H` colours with their matched dash+marker, no bar plots, no 1×4
micro-panel strips, no annotation overlapping data, no label clipped by the
canvas, perceptually uniform maps carrying units.

## 1. Reproducibility chain

```
paper_a_study/figure_style.py          style, palette, canvas contract
paper_a_study/build_figure_data.py     solves → figure_data/*.csv, *.json
paper_a_study/generate_final_figures.py plots only → figures_final/*.pdf
paper_a_study/make_atlas.py            two-page vector atlas
```

`generate_final_figures.py` reads nothing but the CSVs; it never solves. A
figure can therefore be re-rendered without re-running the physics, and the
physics can be re-run without touching the plots.

## 2. Figure-by-figure audit

### Figure 1 — dispersion and wave speeds (`fig01_…attenuation.csv`)
*Scientific.* (a) all five `H/H*` levels coincide over the whole zone; the
inset resolves their difference, which stays inside ±60 kHz on a 16.7 GHz
carrier. (b) `v_p = ω/|k|` uses the **full** wavevector (not `k_x` alone),
`v_g = ∂ω/∂k_x` is numerical, `v_E = P_x/E` comes from the thickness-integrated
Poynting flux divided by the stored energy; the three change sign near
`k_x d ≈ 0.55`, which is the backward-branch signature. (c)/(d) FWHM and
`α = 2|Im k_x|` (0.5 → 5·10² dB mm⁻¹ across the zone, never zero).
*Visual.* Shared `H` legend regenerated as one row of five and it now fits the
canvas (verified bounding box 0.06–0.94 in figure fraction). The former
clipped `frequency`/`linewidth` labels were fixed by `left = 0.128`; the (a)
inset no longer covers the operating-point star and the leader line no longer
collides with the (c) axis. **PASS.**

### Figure 2 — carrier density and mobility (`fig02_…sweep.csv`, 130 rows, 100 certified)
*Scientific.* Density and mobility raise linewidth and attenuation but leave
the backward reflectance untouched: (c) collapses five densities onto one
`R_B(k_x d)` curve peaking at **58.0 %** near `k_x d = 0.55`, the point where
`v_g → 0`. The non-physical `R_B` values of the earlier build (3.04, 5.07,
1.55 at `K = 0.80/0.85/0.90`) are quarantined: those rows carry
`|θ_E| = 89.99°`, fail the gate and are **not drawn** — the curves simply stop.
*Visual.* (c) now plots the physical quantity (`R_B` in %), not the ±0.05 %
deviation that made the panel look like noise; the "all five levels lie on this
curve" note replaces the inset that used to cover the rising branch. (d)
legend moved clear of the curves. **PASS.**

### Figure 3 — thickness versus gradient length (`fig03_…sweep.csv`, 210 rows)
*Scientific.* The two families are separated instead of being mixed and the
duplicate GHz/THz panel is gone. Thickness is the dominant scale (10.5 →
28.3 GHz between 320 and 120 nm); the gradient length is a weak,
wavenumber-dependent perturbation (`Δf/f₀` from −4.9 % to +10.2 % for
`ℓ = 35…90 nm` against the `ℓ = 50 nm` reference).
*Visual.* Flat-legend overlap in (a)/(b) removed by two-column legends with
short labels; the former heat-map panel (whose colour bar had no unit and whose
colour was constant along `k_x d`) is replaced by a line panel that shows the
same data honestly. **PASS.**

### Figure 4 — backward conversion along the guided branch (`fig04_…reflection.csv`, **50/50 certified**)
*Scientific.* The fixed-frequency sweep was ill-posed (a single valid point,
the rest at `θ_E = −90°`); the figure now follows the branch instead. `R_B`
runs 1.71 → 57.92 % and peaks where `v_g → 0`, i.e. the effect is a slow-mode
effect. `k_Bx/k_ix = 0.287…0.916`, so the backward port is genuinely
propagating. **No row with `|θ_E| → 90°` is plotted**, so no invalid
"reflectance" enters panel (a).
*Visual.* The old 1×4 strip became a 2×2; the scatter-plus-colourbar spaghetti
in (c) was replaced by an `R_B(v_g)` curve with the `v_g = 0` guide line, and
the colorbar that collided with panel (d) was removed. **PASS.**

### Figure 5 — energy budget of the edge problem (`fig05_channel_power.csv`)
*Scientific.* Incident power is normalised to one and split into three
physical channels: backward far field 2.299 % (identical to `R_B_edge`),
dissipation 1.99·10⁻⁴…6.87·10⁻³ and reactive near field
4.4·10⁻⁶…4.2·10⁻⁵. The **forward-propagating channel is exactly zero** and the
figure says so instead of hiding it. The near-field entries are labelled
reactive and are never presented as transported power. Balance error
2·10⁻¹² … 2.1·10⁻¹², three orders below the 10⁻⁶ acceptance line.
*Visual.* The five-point refinements are preserved: five `H` levels, matched
markers, the same `R_B` values. The rejected "99.9 % evanescent self-power"
panel is gone; (a) is a log dot plot, (b) the channel response, (c) the balance
error against the acceptance line, (d) the relative change. No `H` colour is
used for a non-`H` series. **PASS.**

### Figure 6 — distance, survival, attenuation (`fig06_…distance.csv`)
*Scientific.* `incident_survival ≤ 1` everywhere (it previously reached
28.06); the survival factor is now normalised to its edge value, so the curve
cannot exceed the unitary line. Attenuation lengths and loss coefficients come
from the solved complex roots and are positive for every `H`, with the largest
loss at `H = 0`, consistent with the reflectance maximum of Fig. 4.
*Visual.* The four over-long rotated labels that overflowed the canvas were
replaced by symbol labels (`R_B(ℓ)`, `L`, `α`), the "unitary limit" caption was
moved off the curve, and both legends were moved out of the data. **PASS.**

### Figure 7 — coupling sensitivity in (k_y, H) (`fig07_…sensitivity.csv`, **95/95 certified**)
*Scientific.* The transverse wavenumber dominates: `R_B = 1.90…2.56 %` over
the declared box and the coupling moves it by −2.44 … 0 %. Panel (b) draws the
**measured 5 × 19 grid cell by cell** — nothing outside the box is
interpolated.
*Visual.* The 19-curve rainbow carpet and the 3-D surface are removed; three
declared `k_y d` slices are used in (c) and the full grid appears once, in (b).
**PASS.**

### Figure 8 — through-thickness flux distribution (`fig08_…flux.csv`, 5 × 64 rows)
*Scientific.* The earlier open-boundary panel is **not** shown as a PASS. The
demonstrated defect was the electric-potential null space of the open-circuit
weak form; it was repaired with an explicit gauge (a null-space removal, not
physics), but that repair does not by itself certify a boundary comparison, so
the panel was replaced by a diagnostic that is fully controlled: the
distribution of the backward flux through the thickness. `P_x^B` changes sign
inside the plate while its thickness integral stays negative (−0.02307 …
−0.02315, matching `R_B`); `P_z^B` does not vanish at the free surfaces, which
is exactly why the reactive near field must stay in the budget.
*Visual.* All four labels shortened to `z/d`; the in-panel `H` legend was
deleted in favour of the single shared legend; the two modes are compared in
(d). **PASS.**

### Figure 9 — convergence and cross-checks (`fig09_*.csv`)
*Scientific.* `|ΔR_B|/R_B` falls from 2.8·10⁻⁶ to the round-off floor by
`n = 26`; `|Δk_B|/|k_B| ≈ 4·10⁻¹²`; the scaled edge residual and the
energy-balance error stay at 10⁻¹²–10⁻¹³, below the 10⁻⁸ / 10⁻¹⁰ tolerances.
Panel (d) compares the temporal generator with the complex spatial QEP: the two
routes agree to 1.9·10⁻⁵. They are **two solution routes for the same
dispersion relation**, and the note says so — no "independent methods" claim is
made.
*Visual.* Panels (b) and (d) previously plotted **nothing** because their
y-limits excluded the data; the limits were corrected (both now show data) and
the empty-looking panels are gone. Labels shortened to `|ΔR_B|/R_B`,
`|Δk_B|/|k_B|`, `|Δk|/|k|`. **PASS.**

### Figure 10 — solved field and flux directions (`fig10_field_maps.csv`, `fig10_field_metrics.json`)
*Scientific.* (a)/(b) show incident and backward intensity on a shared
logarithmic scale (`LogNorm(vmin = 2·10⁻⁴ vmax)`, equal aspect). Every arrow in
(c) is taken from the solved thickness-integrated flux: incident
`k_i ∝ (1, 0.176)` (10.0°), backward `k_B ∝ (0.333, −0.530)` (θ_E = −27.9°),
`P_i ∝ (1, 0.176)`, `P_B ∝ (−1, −0.530)` with `P_Bx = −1.54·10⁻²`,
`P_By = −8.17·10⁻³` (both negative). No cartoon arrows.
*Visual.* The schematic labels were moved to the arrow tips with the correct
alignment, "edge" was moved off the arrow bundle, the colour bar gained a unit
label, and panel (d) lost the note that covered its curve. **PASS.**

## 3. Residual limitations (stated, not hidden)

1. The model is 2-D plane strain with a specified in-plane tangential
   component; it is not a 3-D oblique edge solution.
2. The `H`, `A` and `f₃₃₃₃` values are synthetic and are never presented as
   measured ZnO constants.
3. The certification window removes rows near `|θ_E| = 90°`; the reported
   ranges therefore describe the certified part of the branch only.
4. No claim of novelty over Qu et al. is made.
5. The open-circuit gauge removes a null space; it is not an independent
   validation of the open-boundary response.

## 4. Verification commands

```bash
cd paper_a_study
/home/user/.venv/bin/python generate_final_figures.py     # 10 vector PDFs
/home/user/.venv/bin/python make_atlas.py                 # two-page atlas
/home/user/.venv/bin/python - <<'PY'
import pymupdf, pathlib
for p in sorted(pathlib.Path("figures_final").glob("*.pdf")):
    d = pymupdf.open(p)[0]
    assert abs(d.rect.width/72 - 6.5) < 1e-6 and abs(d.rect.height/72 - 5.1) < 1e-6
print("canvas OK")
PY
```
