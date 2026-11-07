# Paper A — round 13: Figure 10(c) backward-wavenumber verification

**Outcome: corrected, regenerated, inspected, and guarded.** One arrow in one
schematic panel changed. Nothing else in Figure 10 changed.
Baseline `3827543016ece4a9d0612e861bf75425457291bf`.

---

## 1. What was wrong

`paper_a_study/generate_final_figures.py`, `fig10()`, panel (c), before:

```python
arrow((1.0, 0.176), "#C83E58", r"${\bf k}_i$", (-1.16, -0.50), 0.55)
arrow((0.333, -0.530), "#087E8B", r"${\bf k}_B$", (-0.82, 0.74), 0.74, ha="right")
arrow((1.0, p["incident_Py"]), "#B4552A", r"${\bf P}_i$", (-1.16, 0.12), 0.50)
arrow((-1.0, -0.530), "#6C3F8D", r"${\bf P}_B$", (-0.26, 0.06), 0.46, ha="right")
```

The $\vect{k}_B$ vector carries two defects in one pair of numbers.

1. **It mixes two different ratios.** The first component, `0.333`, is
   $K_{Bx}/K_{ix}=0.24517/0.73620$. The second, `−0.530`, is
   $\lvert k_y\rvert/K_{Bx}=0.12981/0.24517$. A direction needs one normalisation,
   not two.
2. **It takes the sign of the flux.** For a backward mode the phase wavevector and
   the energy flux are antiparallel, so $k_y>0$ while $P_{By}<0$. The old arrow
   used $P_B$'s sign on a $k_B$ glyph.

The result pointed $57.86^{\circ}$ **below** the $+x$ axis — the fourth quadrant —
where the solved wavevector lies $27.90^{\circ}$ **above** it. Its length was wrong
too: drawn 0.463 against 0.558 for $\vect{k}_i$, a ratio of 0.829, where the solved
magnitude ratio is 0.371.

Old panel (rendered from the file that shipped in round 12):

`/tmp/fig10_panel_c_old.png` — the arrow runs down-right, through the
$\vect{P}_i$ label.

---

## 2. The physically derived direction

Everything below comes from one edge solve at **the figure's own configuration**,
reproduced in this round (not copied from a report):

```
Paper = Plate(degree=22)                       # H = 0, no carrier-strain-gradient coupling
ky_d     = 0.12981175031447484
omega    = 7.633372404423294
incident k_x d = 0.7361990195318475 + 5.402718679033664e-06 i
backward k_x d = 0.2451746921716515 - 5.230595074070594e-06 i
frequency      = 16.68412313636555 GHz
negative_direction = True
```

| quantity | value | how |
|---|---|---|
| backward phase direction | $\vect{k}_B\propto(1,\;k_y/k_{Bx})=(1,\,0.5294663538)$ | $\Re k_{Bx}$ and $k_y$ are both real and positive |
| backward phase angle | $+27.8997139835^{\circ}$ | $\arctan2(k_y,\Re k_{Bx})$ |
| incident phase direction | $\vect{k}_i\propto(1,\,0.1763269807)$, $+10.0000000000^{\circ}$ | same construction |
| backward flux direction | $\vect{P}_B\propto(-1,\,-0.5294663538)$, i.e. $-152.10^{\circ}$ | $P_{Bx}=-0.0154248131$, $P_{By}=-0.0081669195$ |
| flux angle against the backward axis | $-27.8997139811^{\circ}$ | `reflected_angle_deg` $=\arctan2(P_{By},-P_{Bx})$ |
| magnitude ratio | $\lvert\vect{k}_B\rvert/\lvert\vect{k}_i\rvert=0.3711022670$ | $\sqrt{k_{Bx}^2+k_y^2}/\sqrt{k_{ix}^2+k_y^2}$ |

Three independent statements agree on the angle: the wavevector construction
($+27.8997^{\circ}$), the stored `reflected_angle_deg` ($-27.8997^{\circ}$ measured
against $-x$), and the pure flux ratio ($\lvert P_{By}/P_{Bx}\rvert=0.5294663538$).
They agree here to $5\times10^{-11}$ in ratio, which is a property of this mode, not
an identity — so the figure derives each vector from its own record instead of
assuming they coincide.

### Coordinate convention used by panel (c)

The plate occupies $x<0$ with the free edge at $x=0$; the outward normal is $+x$
(horizontal arrow, rightwards) and $+y$ is the vertical arrow, upwards. The
incident wave travels toward the edge ($+x$, $+y$: up-right). The backward mode's
**phase** also advances toward the edge ($+x$, $+y$: up-right, but at the steeper
angle), while its **energy** leaves the edge ($-x$, $-y$: down-left). That is what
"negative reflection" means in this paper, and panel (c) is the one place where it
is drawn rather than described.

### Which configuration is drawn

The figure solve is the **H = 0** configuration — the operating point of §4. Its
frequency, 16.6841231 GHz, and its share, 0.0231456, equal
`mechanism_controls.json` → `operating_point.no_coupling`
(16.6841231 GHz, 0.0231456), not `operating_point.full` (16.6839845 GHz,
$k_{Bx}=0.2454907$, $-27.8692^{\circ}$). The two differ by 0.13 % in $k_{Bx}$ and
0.03° in angle, which is exactly why the arrow is now read from
`fig10_field_metrics.json` rather than from a neighbouring record or a literal.

---

## 3. The code change

### 3.1 A stored source for the direction

`paper_a_study/build_figure_data.py`, `fig10()`: the metrics payload gained one
block, written from the solve that already produced the panel:

```python
primary_wavenumbers=dict(
    ky_d=float(res["ky"]),
    incident_kx_d=float(res["incident_K"].real),
    incident_im_kx_d=float(res["incident_K"].imag),
    backward_kx_d=float(res["backward_K"].real),
    backward_im_kx_d=float(res["backward_K"].imag),
    incident_phase_angle_deg=float(np.degrees(np.arctan2(res["ky"], res["incident_K"].real))),
    backward_phase_angle_deg=float(np.degrees(np.arctan2(res["ky"], res["backward_K"].real))),
    magnitude_ratio_backward_over_incident=float(
        np.hypot(res["backward_K"].real, res["ky"]) / np.hypot(res["incident_K"].real, res["ky"])),
    configuration="H=0 (no carrier-strain-gradient coupling), the operating point of section 4",
)
```

That producer was then re-run. The diff to `fig10_field_metrics.json` is
**eleven added lines and nothing else** — no existing value moved:

```json
 "primary_wavenumbers": {
  "ky_d": 0.12981175031447484,
  "incident_kx_d": 0.7361990195319493,
  "incident_im_kx_d": 5.402718792523917e-06,
  "backward_kx_d": 0.2451746921714963,
  "backward_im_kx_d": -5.2305951976365535e-06,
  "incident_phase_angle_deg": 9.999999999990488,
  "backward_phase_angle_deg": 27.899713983558208,
  "magnitude_ratio_backward_over_incident": 0.37110226697849763,
  "configuration": "H=0 (no carrier-strain-gradient coupling), the operating point of section 4"
 }
```

`fig10_field_maps.csv` — the 22 801-row field map behind panels (a) and (b) — came
back **byte-identical** (`cmp` reports no difference), which is the evidence that
the re-run changed metadata only. (It is byte-identical when the producer runs with
the same BLAS threading as the delivered build. Forcing `OMP_NUM_THREADS=1` shifts
the intensities by at most $1.5\times10^{-7}$ relative — thread-order round-off, not
physics; the shipped file is the threaded result and was restored exactly.)

### 3.2 The directions, derived instead of written

```python
def fig10_directions(metrics):
    pw = metrics["primary_wavenumbers"]
    flux = metrics["primary_flux"]
    ky = float(pw["ky_d"])
    k_i = np.array([1.0, ky / float(pw["incident_kx_d"])])
    k_B = np.array([1.0, ky / float(pw["backward_kx_d"])])
    P_i = np.array([1.0, float(flux["incident_Py"]) / float(flux["incident_Px"])])
    P_B = np.array([float(flux["backward_Px"]), float(flux["backward_Py"])])
    P_B = P_B / abs(P_B[0])
    return dict(k_i=k_i, k_B=k_B, P_i=P_i, P_B=P_B,
                magnitude_ratio=float(pw["magnitude_ratio_backward_over_incident"]))
```

All four arrows now come from the record. Three of them are numerically unchanged
to the eye ($\vect{k}_i$: 0.176 → 0.176327; $\vect{P}_i$: identical form;
$\vect{P}_B$: −0.530 → −0.529466); only $\vect{k}_B$ moves, and it moves to a
different quadrant.

### 3.3 A guard that runs at render time

```python
def check_backward_wavenumber(direction, metrics, tol=1e-9):
    ...
    if d[0] <= 0.0 or d[1] <= 0.0:
        raise ValueError("fig10(c): the backward wavenumber must point into +x,+y; ...")
    expected = np.array([1.0, float(pw["ky_d"]) / float(pw["backward_kx_d"])])
    ...
```

`fig10()` calls it before drawing, so a reversed or re-derived arrow aborts the
build instead of shipping.

### 3.4 The drawing call

```python
arrow(dirs["k_i"], "#C83E58", r"${\bf k}_i$", (-1.16, -0.50), 0.55)
length_i = 0.55 * float(np.linalg.norm(dirs["k_i"]))
arrow(dirs["k_B"], "#087E8B", r"${\bf k}_B$", (-1.00, 0.34),
      length_i * dirs["magnitude_ratio"] / float(np.linalg.norm(dirs["k_B"])),
      ha="right", label_dy=0.10)
arrow(dirs["P_i"], "#B4552A", r"${\bf P}_i$", (-1.16, 0.12), 0.50)
arrow(dirs["P_B"], "#6C3F8D", r"${\bf P}_B$", (-0.26, 0.06), 0.46, ha="right")
```

$\vect{k}_B$ is drawn at the solved magnitude ratio to $\vect{k}_i$
(0.207 units against 0.558): the backward wavevector really is the shorter one, and
the panel now says so. The label is lifted by `label_dy=0.10` because the first
render put it on top of a short shaft (see §5).

---

## 4. Regeneration

Only `fig10_field` was re-rendered, deliberately: the other nine figures would come
back with a new PDF `CreationDate` and no changed content, which would look like
nine changes. Commands and outputs:

```
$ python -c "import generate_final_figures as g; g.fig10()"
[PosixPath('paper_a_study/figures_final/fig10_field.pdf'),
 PosixPath('paper_a_study/figures_final/fig10_field.png')]
$ cp paper_a_study/figures_final/fig10_field.pdf Paper_A_Final_Submission/figures/fig10_field.pdf
$ md5sum Paper_A_Final_Submission/figures/fig10_field.pdf paper_a_study/figures_final/fig10_field.pdf
c7aa3d09aa0d1c2b09fa30fcabccf8ab  .../Paper_A_Final_Submission/figures/fig10_field.pdf
c7aa3d09aa0d1c2b09fa30fcabccf8ab  .../paper_a_study/figures_final/fig10_field.pdf
```

The manuscript copy is the render; the render is the copy. Size 48 618 B.

---

## 5. Visual inspection

The PNG proof (`paper_a_study/figures_final/fig10_field.png`, 2600×2040 at 400 dpi)
was cropped to panel (c) and inspected at publication reading size.

**First render.** $\vect{k}_B$ pointed correctly up-right, but its label sat on the
shaft: a 0.207-unit arrow leaves no room for a label offset along $-x$. Rejected
and fixed by lifting the label 0.10 units in $+y$ (`label_dy`).

**Second render** (the delivered one):

| check | result |
|---|---|
| quadrant | $\vect{k}_B$ in the first quadrant, up-right, steeper than $\vect{k}_i$ ✔ |
| angle rendering | $\vect{k}_B$ visibly steeper than $\vect{k}_i$ (27.9° vs 10.0°); $\vect{P}_B$ visibly parallel to $\vect{k}_B$ and opposite in sign ✔ |
| distinguishability | four colours, four labels, no overlap: $\vect{k}_i$ (crimson), $\vect{k}_B$ (teal), $\vect{P}_i$ (rust), $\vect{P}_B$ (violet) ✔ |
| relative length | $\vect{k}_B$ ≈ 0.37 of $\vect{k}_i$ ✔ |
| label visibility | "${\bf k}_B$" clear above the arrowhead; "${\bf k}_i$", "${\bf P}_i$", "${\bf P}_B$" clear ✔ |
| clipping | no annotation touches the panel or canvas edge; the canvas-edge test passes ✔ |
| in-panel text | "ZnO plate, $d$ = 200 nm", "schematic", "edge", "$x$", "$y$" all legible and unmoved ✔ |
| panels (a),(b),(d) | unchanged — same data, same rendering path, not re-drawn ✔ |

---

## 6. Regression guard

Five tests added in `paper_a_study/test_model.py`,
`TestFigure10BackwardWavenumber`:

| test | what it pins |
|---|---|
| `test_drawn_backward_wavenumber_is_the_solved_one` | the drawn direction equals $(1,k_y/k_{Bx})$ rebuilt from the JSON, is in the first quadrant, and the two numbers the manuscript quotes (0.529, 27.9°) still hold |
| `test_the_drawn_length_keeps_the_solved_magnitude_ratio` | the stored magnitude ratio equals $\lvert\vect{k}_B\rvert/\lvert\vect{k}_i\rvert$ and is below 0.5 |
| `test_flux_opposes_the_wavenumber` | $\vect{k}_B\cdot\vect{P}_B<0$, both $\vect{P}_B$ components negative, both $\vect{P}_i$ components positive |
| `test_reversed_arrow_is_rejected` | the guard accepts the solved vector and raises `ValueError` for $-\vect{k}_B$, for $(k_{Bx},-k_y)$ and for the old literal $(0.333,-0.530)$ |
| `test_the_renderer_calls_the_guard` | `fig10()` calls the guard, so the check is not test-only |

```
$ python -m unittest paper_a_study.test_model.TestFigure10BackwardWavenumber -v
Ran 5 tests in 0.287s
OK
```

**Deliberate reversal, executed.** A copy of the renderer with
`k_B = -np.array([1.0, ky / float(pw["backward_kx_d"])])` was placed in `/tmp/m16`
and the same class was run against it:

```
$ PAPER_A_FIGURE_SRC=/tmp/m16 python -m unittest paper_a_study.test_model.TestFigure10BackwardWavenumber
FAIL: test_flux_opposes_the_wavenumber
AssertionError: 1.2803346198043053 not less than 0.0 : for a backward mode the flux
points opposite to the phase vector
Ran 5 tests in 0.289s
FAILED (failures=2, errors=1)
```

Three independent tests fail on a reversed arrow: the direction comparison, the
guard expectation, and the flux-opposition test. The defect cannot return silently.

---

## 7. What this does **not** claim

* The figure was **not** recalculated. The field maps, the flux components, the
  intensity panels and panel (d)'s curves are the round-12 data, byte for byte. Only
  one schematic arrow moved and the other three arrows changed from literals to
  derived values that agree with their literals.
* No number in the manuscript changed as a result of this correction; the text
  already described the correct direction (§4.15: $\vect{k}_B\propto(1,0.529)$,
  $\vect{P}_B\propto(-1,-0.529)$). The figure has been brought to the text, not the
  other way round.
* The caption was adjusted by two words ("the solved flux directions" → "the solved
  wavenumber and flux directions") because the panel draws both kinds of arrow.
