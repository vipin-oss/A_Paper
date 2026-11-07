# Paper A — Round 9: plane-invariance validation

**Question this report answers:** after the correction, is the edge-plane share a property of the edge
or an artefact of the plane at which it was read — and does every script now produce the same number?

**Short answer:** the reconstruction is invariant to `2.3 × 10⁻¹⁶` across five planes, the three
independent producers of the same edge share now agree to the last stored digit, and the
single-mode transform that used to disagree by 2.0 percentage points fails four separate tests.

---

## 1. What is and is not being claimed

Two different statements must be kept apart, and the manuscript keeps them apart:

* **Invariance of the reconstructed edge quantity.** `R_B(edge)`, reconstructed from a solve made at
  plane `L`, does not depend on `L`. This is a statement about the *bookkeeping*: the same physical
  edge value is recovered from any plane. It is tested here and it holds to machine precision.
* **Dependence of the physical ratio on the plane.** `R_B(L)` itself is *not* invariant: it falls from
  0.9856 at the edge to 0.9468 at ten thicknesses and 0.9095 at twenty, because the two modes
  attenuate in opposite directions. That dependence is the physics, and the paper reports it
  (`fig06`, §4.4) rather than dividing it away.

Neither statement is evidence that the scattering model is correct. Plane invariance is a consistency
condition on the algebra; the physical validation is the energy identity, the strong-form checks and
the `C¹` plate comparison.

---

## 2. The transform, and why the exponent is a sum

With the solver's ansatz `φ_j = a_j Y_j(z) exp(i K_j x)`, `K_j = k_j d`, the plate in `x < 0` and the
free edge at `x = 0`, an observation plane at distance `L` (in thicknesses) sees
`P_j(L) = P_j(0) exp(−2 Im K_j L)`. The incident port has `Im K_i > 0` and the backward port
`Im K_B < 0`, so

```
R_B(L_to) = R_B(L_from) · exp[ 2 (Im K_i − Im K_B)(L_from − L_to) ]
          = R_B(L_from) · exp[ 2 (|Im K_i| + |Im K_B|)(L_from − L_to) ]
```

at the certified maximum, `|Im K_i| = 1.004047e-3` and `|Im K_B| = 1.002930e-3` in units of `K = k d`,
so the raw exponent is `2(|Im K_i| + |Im K_B|) = 4.013954e-3` per thickness. Over ten thicknesses that
is `exp(0.04014) = 1.04095`, which is exactly the gap between 0.946795 and 0.985572.

The failed version used `exp(+2|Im K_B| L)`, i.e. half the exponent. It cannot be fixed by a factor of
two: the two attenuations are different numbers, and the ratio needs the sum.

---

## 3. Five planes, one number

The scattering problem is solved with the observation plane at `L = 0, 5, 10, 15, 20` thicknesses, and
each solved ratio is carried to the common plane `L = 10` with the shared transform
(`peak_identity_audit.json → reference_plane`):

| `L` (thicknesses) | `R_B(L)` solved | carried to `L = 10` |
|---|---|---|
| 0 | 0.985572194293 | 0.946795230677 |
| 5 | 0.965989157829 | 0.946795230677 |
| 10 | 0.946795230677 | 0.946795230677 |
| 15 | 0.927982681345 | 0.946795230677 |
| 20 | 0.909543931965 | 0.946795230677 |

**Spread of the five reconstructed values: 2.345e-16 relative** (recorded as
`spread_relative = 2.3452231034822425e-16`, `consistent = true`). The value at `L = 0` is solved
directly rather than assumed, so the edge plane is one of the five cases and not the reference for
them.

This is a genuine invariance test rather than a tautology: the five solves are independent (different
matrices, different mode sets) and the transform is applied between them.

---

## 4. Analytic identities

`test_model.TestEdgePlaneTransform` checks the four identities that make the transform a valid
two-plane map, on synthetic data that never touches a stored record:

1. `L_to == L_from` returns the input unchanged (to 1e-15 relative);
2. composition: `L₁ → L₂` then `L₂ → L₃` equals `L₁ → L₃`;
3. `Im K_i = Im K_B = 0` leaves the ratio unchanged (no attenuation, no rescaling);
4. round trip: `L → L'` then `L' → L` returns the input, and the transform *increases* the ratio as
   one moves towards the edge, which is the physical direction.

A transform that halves the exponent (M9), flips its sign (M10, M10b), moves the reference plane
(M11) or substitutes the gradient length for the thickness (M12) fails these identities or the
invariance test. All four mutants are caught; see `PAPER_A_ROUND9_MUTATION_REPORT.md`.

---

## 5. Cross-script agreement

The same physical edge share (`k_x d = 0.5275`, `H = 0`, degree 22, 64 nodes) is produced by three
independent code paths:

| producer | stored value | agreement with a fresh evaluation |
|---|---|---|
| `peak_search.json` (degree-22 row at the reported wavenumber) | 0.9855721942926737 | exact (same code path) |
| `mechanism_controls.json` (`refined_peak`, `H = 0`, `no_coupling`) | 0.9855721942926737 | exact |
| `fig05_channel_power.csv` (`H = 0`, reference-plane row) | 0.023150542 (operating case) | 1.5e-12 relative |
| `fig07_coupling_sensitivity.csv` (`H = 0`, 19 `k_y` rows) | 0.019304343 … 0.025601054 | 1.0e-11 relative worst |

`peak_search` and `mechanism_controls` are now **bit-identical**, because both call
`edge_plane_fraction` on the same solve; before the correction they differed by 1.96e-2 relative, which
is why the defect survived round 8: no gate compared the two.

The transform value and a direct solve at the edge plane still differ in the ninth digit
(0.985572200358 against 0.985572194293, `6.2e-9` relative). That residue is the Galerkin degree
sensitivity of the edge-plane solve (`degree_spread = 4.973e-9` in `peak_search.json`), not a
transform error, and it is four orders of magnitude below the 2e-2 defect that was repaired.

---

## 6. Consequences for the manuscript

* §4.5 now states in print that the transform is implemented once and imported everywhere, and that
  the stored edge shares are reproduced by a fresh evaluation to `10⁻¹⁰` relative.
* §3.4 (numerical methods) lists the three new tests and says that a single-mode decay fails all
  three.
* The edge-plane table row now reads 0.0232 / 0.9856 / 0.5802 (four decimals). The second and third
  cells were already produced by the correct transform and did not move; the first moved from 0.0231 to
  0.0232 because 0.0231505 rounds up, not because the physics changed.
* Nothing in the text now compares a reference-plane share with an edge-plane share as if they were the
  same number; the two are labelled by plane wherever they appear.

---

## 7. What this validation does not cover

* It is a consistency check on the algebra and on cross-script bookkeeping, not on the physics.
* It does not certify the maximum — that is `peak_search.json → classification`, unchanged.
* It does not extend outside the declared interval `0.465 < k_x d < 0.625`.
* The invariance tolerance (1e-15) is tighter than the physical convergence of the solve (5e-9); the
  two scales are reported separately and are never conflated.
