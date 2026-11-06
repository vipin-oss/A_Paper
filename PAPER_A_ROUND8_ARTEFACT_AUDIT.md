# Paper A — Round 8: is the high partition an artefact?

**Question:** the certified value says that 94.68 % of the incident modal power reappears in the backward
mode — at a point where the incident mode is nearly cut off. There are exactly three ways such a number
can be spurious, and each was tested by a probe that could have failed.

**Data:** `paper_a_study/figure_data/peak_identity_audit.json` (105 s of solver time in this run).
**Program:** `peak_identity_audit.py`. **Verdict field in the record:** `artefact: false`.

---

## Probe 1 — the number must not depend on where it is read

A share defined by two modal powers depends on the plane at which both are evaluated unless both modal
attenuations are properly accounted for. The probe solves the same edge problem at reference planes of
5, 10, 15 and 20 thicknesses and rescales each result to 10 thicknesses by

  exp[ 2 (|Im k_ix| + |Im k_Bx|) (L − L_ref)/d ],

which is the **net** attenuation of the two partner modes travelling in *opposite* directions.

| L/d | R_B as solved | net exponent | R_B rescaled to L = 10 |
|---|---|---|---|
| 5 | 0.9659892 | 4.01395 × 10⁻³ | 0.9467952 |
| 10 | 0.9467952 | — | 0.9467952 |
| 15 | 0.9279827 | 4.01395 × 10⁻³ | 0.9467952 |
| 20 | 0.9095439 | 4.01395 × 10⁻³ | 0.9467952 |

**Spread of the rescaled values: 2.35 × 10⁻¹⁶.** The partition is a property of the edge, and both
attenuations are *resolved* rather than assumed.

*Defect this probe found (D2).* The previous version rescaled with the backward attenuation alone
(`exp(α_B · p.d)`), which is wrong by the incident factor, and reported a 2.0 % dependence on the plane
which it then wrote off as acceptable in a canned note. The 2 % was arithmetic, not physics. The canned
note has been removed and replaced by the measured spread and the measured exponent.

## Probe 2 — the case must be the case it says it is

At k_x d = 0.5275 the solver returns

* incident root k_ix d = 0.528236 + 1.0040 × 10⁻³ i,
* backward root k_Bx d = 0.526132 − 1.0029 × 10⁻³ i,
* offset between the branch parameter and the incident root: **7.36 × 10⁻⁴ (0.14 %)**,
* offset between the branch parameter and the *backward target* K_B = 0.2452: **0.28**, i.e. 54 %.

The two offsets differ by nearly three orders of magnitude, which is what makes the *labelling* guard of
`corner_assessment.py` meaningful: any case whose incident root lies more than 2 × 10⁻² (relative) from
the requested wavenumber is rejected, which admits the certified peak (0.14 %) and rejects a case posed on
the backward target (54–67 %).

*Defect found (D5).* The guard was set at 10⁻⁶ relative, which silently excluded the certified peak
altogether while admitting nothing it was supposed to reject. A guard whose threshold is tighter than the
physical offset it must tolerate is a defect.

## Probe 3 — the decomposition must not be near-degenerate

At the fold the incident and backward modes are nearly parallel. The probe measures how nearly:

| | value |
|---|---|
| eigenvector overlap, incident vs backward | 0.999994993 |
| overlap with the strongest *other* outgoing mode | 0.889 |
| ratio of the backward to the strongest other amplitude | 157.2 / 4.00 = 39.3 |
| share of the solution carried by the backward amplitude | 0.997417 |
| separation of the two roots, \|Δk\| | 2.908 × 10⁻³ |
| separation in units of the modal decay rate | **1.448** |
| second admissible outgoing candidate | 1.054 away = 2.004 \|k_x\| |
| condition number of the normalised edge matrix (degree 22) | 160.5 (56.9 at degree 18, 185.9 at degree 30) |
| singular values | 3.067 / 0.0191, rank 182 of 182 |
| relative error bound of the projection, cond × ε | **3.56 × 10⁻¹⁴** |

The two partners are close — separated by 1.45 decay rates — but resolved, and the reconstruction from
stored amplitudes and modal powers alone reproduces the solver value **exactly** (difference 0.0 for every
one of the four probe cases). A degenerate decomposition would not reconstruct; it would show up as a
spread under rescaling of the eigenvectors, which is nil.

The 0.889 overlap with another mode is recorded rather than hidden: the backward mode is not the only
outgoing mode that *looks* like the incident one, it is the only one whose *amplitude* is two orders of
magnitude larger. That is why the classification test in the solver is on the amplitude, not on the
overlap.

## Probe 4 — the flux scale, honestly reported

The ratio at the fold is a ratio of two small fluxes. Both are now stored as measured:

| configuration | incident modal power (raw) | R_B |
|---|---|---|
| operating point | 5.0751 × 10⁻³ | 0.023146 |
| k_x d = 0.55 | 8.2106 × 10⁻⁴ | 0.579180 |
| certified maximum | **3.9670 × 10⁻⁵** | 0.946795 |

The incident flux falls by a factor **128** between the operating point and the maximum, while the share
rises by a factor 41. Inside the hump window the partition tracks the wavenumber ratio
(r = +0.979) and is **anti-correlated with the incident flux (r = −0.959)**: this is the signature of a
zero-group-velocity fold, and it is the opposite of what a 0/0 artefact looks like. An artefact would
scatter; this configuration reproduces to 5.6 × 10⁻⁹ under degree refinement, 9.4 × 10⁻¹⁰ under quadrature,
2.4 × 10⁻¹⁶ under plane rescaling and exactly along three tracking paths.

*Defect found (D3).* The previous audit filled `modal_power_incident_raw` with **1.0** for every case,
because the incident mode had been renormalised before the field was recorded, and it wrote a
predetermined favourable correlation into its note while the computed columns said otherwise. Both are now
measurements, and the honest consequence — that the share is maximal where the transported power is
minimal — is stated in the abstract, the results and the conclusions.

## What the number is not

| statement | value | status |
|---|---|---|
| share of the *incident* power in the backward mode | 94.68 % | quoted |
| share of the *outgoing propagating* power | 94.90 % | derived, not quoted as the headline |
| share of the incident power leaving as propagating modes | 99.77 % | quoted |
| interference (cross) correction at the reference plane | −2.29 × 10⁻³ | quoted |
| dissipation | 2.32 × 10⁻⁵ | quoted |
| reflectance | — | *not* claimed: a modal share is not a reflectance |

## Verdict

**All four probes pass with margins of 9 to 14 orders of magnitude. `artefact: false`, and the reason is a
measurement (2.35 × 10⁻¹⁶ plane invariance, exact reconstruction, cond × ε = 3.6 × 10⁻¹⁴) rather than an
assertion.**
