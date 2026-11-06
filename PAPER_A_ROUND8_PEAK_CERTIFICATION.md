# Paper A — Round 8: certification of the maximum

**Question this report answers:** *what is the maximum of the backward-mode partition along the acoustic
branch, at what wavenumber, and on what evidence may it be called a maximum at all?*

**Data:** `paper_a_study/figure_data/peak_search.json` (355.3 s of solver time in this run),
`peak_certification.json`, `fig04_frequency_reflection.csv` (139 rows).
**Programs:** `peak_search.py` (search), `certify_peak.py` (fixed-wavenumber certification, never searches).

---

## 1. The objective, stated before the search

The quantity maximised is the one defined by the manuscript's eq. (R_B):

> the modal self-power of the **identified backward outgoing mode** at the **reference plane**
> (10 thicknesses from the edge), divided by the **incident power at the same plane**, with the incident
> mode normalised to unit power.

Three exclusions are part of the definition and are never relaxed:

* the other outgoing modes are **not** added to the numerator;
* the interference (cross) term is **not** added;
* the **edge-plane** value is reported beside the reference-plane value and never substituted for it.

The objective is therefore a *share*, not a reflectance, and it is evaluated by the same solver call that
returns every other column of the record, so the search cannot drift into a different experiment than the
one the table reports.

Two ways of writing the same number are kept apart throughout:

| quantity | symbol in the records | value at the maximum |
|---|---|---|
| branch parameter at which the case is posed | `K` (k_x d) | 0.5275 |
| incident axial wavenumber returned by the solver | `K_incident[0]` | 0.5282 |
| backward axial wavenumber returned by the solver | `K_backward[0]` | 0.5261 |
| offset between the first two | `incident_K_offset` | 7.36 × 10⁻⁴ (0.14 %) |

The first is an input, the second and third are outputs, and at a zero-group-velocity fold they are not
equal. Conflating them is defect D5 of the Stage-1 audit.

## 2. The search, staged and classified

| stage | raster | interval | points | largest sample |
|---|---|---|---|---|
| coarse | 2 × 10⁻³ | 0.465 – 0.625 | 81 | 0.527 → R_B = 0.9467870 |
| plateau | 1 × 10⁻⁴ | 0.5265 – 0.5285 | 21 | inside the flat top |
| refined | 1 × 10⁻⁵ | 0.5272 – 0.5278 | 61 | 0.52752 → R_B = 0.9467954 |

* The searched window 0.465 ≤ k_x d ≤ 0.625 is **the whole interval in which a backward port exists** at
  this k_y; outside it the solver returns no admissible backward mode, so there is nothing to maximise.
* Within that window the response is **single-humped**: no second local extremum.
* The reported case is k_x d = 0.5275, R_B = **0.946795230** (94.6795 %); the located argmax is
  k_x d = 0.52752, R_B = 0.946795368, i.e. 1.4 × 10⁻⁷ higher, below the reproducibility of the frequency
  map (±6 × 10⁻⁶ in R_B).
* Top of the response: every sampled k_x d in **[0.5266, 0.5277]** lies within **0.01 percentage point**
  of the maximum; every sampled k_x d in [0.5265, 0.5281] within 0.1 percentage point. The half-width of
  the flat top is 9.2 × 10⁻⁴.
* The classification recorded with the data is **`certified_local_maximum`**, with the explicit statement
  that it is local to the declared window and is *not* a global maximum over k_y, thickness or material
  sets, none of which is searched here.

### What the classification deliberately does not say

`coarse_only_would_certify` is recorded as `true`. On this particular response a 2 × 10⁻³ raster would
already have bracketed the top — the coarse maximum 0.9467870 is only 8.4 × 10⁻⁶ below the refined value.
That fact is reported because it is true, and it is **not** used as a licence: the classification depends
on the flatness test and on the refined raster, not on the luck of a coarse grid. A different response
with the same coarse appearance would be classified as a largest admissible sample, and the record would
say so.

## 3. Restarts, degrees, quadrature, tracking paths

| test | what it varies | result |
|---|---|---|
| restart from [0.520, 0.532], 10⁻³ raster | bracketing | K = 0.527, R_B = 0.9467870 |
| restart from [0.524, 0.536], 10⁻³ raster | bracketing | K = 0.527, R_B = 0.9467870 |
| spread between restarts | — | 8.4 × 10⁻⁶, i.e. *both sit at the coarse bracket* |
| Galerkin degrees 14, 18, 22, 26, 30, 34 | discretisation | spread 5.6 × 10⁻⁹ at 0.52752; 6.2 × 10⁻⁹ at 0.5275 |
| Gauss–Legendre 64, 128, 192, 256 (degree 22) | quadrature | spread 9.4 × 10⁻¹⁰ |
| Gauss–Legendre 64, 256 (degree 30) | quadrature | same order |
| tracking along the branch: 31 points ascending, 31 descending, 1 single step | path dependence | relative spread **0.0** |

The restarts test the *bracketing* and are reported as such; they do not test the refinement, which is
what the two finer rasters do. The manuscript says exactly this.

## 4. Fixed-wavenumber certification (`certify_peak.py`)

Four wavenumbers are certified, and the script is incapable of searching for them:

| case | k_x d | R_B at n = 30 | θ_E (deg) | max relative change, n = 18 → 30 |
|---|---|---|---|---|
| operating point | 0.7362 | 0.023146 | −27.8997 | 7.2 × 10⁻⁷ |
| certified maximum | 0.5275 | 0.946795 | −13.8506 | 1.7 × 10⁻⁹ |
| earlier sample | 0.5250 | 0.931891 | −13.8888 | 2.1 × 10⁻⁸ |
| k_x d = 0.55 | 0.5500 | 0.579180 | −14.4487 | 1.5 × 10⁻⁷ |

All four are `certified: true`. The **0.5250 row is kept on purpose**: it is the value the previous
version of the paper called the maximum, it is converged, and it is 1.49 percentage points below the
certified maximum. Keeping it makes the correction auditable instead of erasing it.

## 5. Figure 4

Regenerated from the new data (`figures/fig04_frequency.pdf`, 42 143 B), 2 × 2 panels, no hardcoded row
count in the caption:

* (a) R_B against k_x d, coarse raster with the fine raster superposed, star at the maximum, inset
  (0.518–0.538, 78–97 %) showing that all five coupling levels collapse onto one curve through the top;
* (b) the energy angle θ_E along the same window;
* (c) R_B against k_Bx/k_ix, the collapse that identifies the mechanism;
* (d) group velocity, dashed line at the maximum.

Every plotted row is admissible; 139 rows.

## 6. Verdict

**R_B,max = 0.9467952 (94.6795 %) at k_x d = 0.5275, f = 16.6547 GHz, certified local maximum of a
single-humped, flat-topped response, stable to 6 × 10⁻⁹ in degree, 9 × 10⁻¹⁰ in quadrature and exactly in
tracking path, and not claimed as a global maximum.**

The previous headline (93.19 % at 0.5250) was a coarse-grid sample and is withdrawn.
