# Paper A — Round 9, Stage 1: modal-power normalisation audit

**Scope:** the reference-plane ↔ edge-plane transformation of the backward modal-power fraction `R_B`,
everywhere it is computed in the package.
**Status of this report:** pre-edit. It records the derivation, the reproduction of the discrepancy and
the dependency map *before* any source file was changed. The corrections are in
`PAPER_A_ROUND9_CORRECTION_HISTORY.md`; their verification is in
`PAPER_A_ROUND9_PLANE_INVARIANCE_VALIDATION.md`.

**Repository state at the start of the audit:** `081cc8e5c2f887c084de4992a856c9aedf335c45`
(round 8), branch `arena/ea7ca4dd-a-paper`.

---

## 1. The convention the solver actually uses

Everything below follows from the ansatz implemented in `model.py::Plate.waves` / `Plate.edge`:

* the plate occupies `x < 0`, the free edge is the plane `x = 0`, the transverse coordinate is `z`
  with `z ∈ [0, d]`;
* a mode is `phi_j(x, z) = a_j Y_j(z) exp(i K_j x)` with **`K_j = k_j d` dimensionless** and time
  dependence `exp(-i ω t)`;
* therefore, for a plane at distance `L` (in thicknesses) from the edge, `x = -L d`:

  ```
  a_j(L) = a_j(0) exp(-i K_j L)      |a_j(L)| = |a_j(0)| exp(-Im K_j · L)
  ```

* an **outgoing** mode is classified as `Im K < -tol`, or `|Im K| ≤ tol` with negative x-power. The
  **backward** port satisfies `Re K_B > 0` and `P_x < 0`; the **incident** mode satisfies `Im K_i > 0`
  (it is the incoming wave, attenuating on its way in) and `Re K_i > 0`.
* the modal x-power of mode `j` at a plane is `P_j(L) = power_j |a_j(L)|²`, with `power_j` the
  signed x-power per unit amplitude (`Plate.power`). Hence `P_j(L) = P_j(0) exp(-2 Im K_j L)`.

## 2. Derivation of the plane transformation

Write the fraction at a plane at distance `L`:

```
R_B(L) = P_B(L) / P_i(L)
```

For the backward mode, `Im K_B < 0`, so moving *away* from the edge (increasing `L`) multiplies its
power by `exp(-2 Im K_B L) = exp(+2|Im K_B| L)` — it grows, which is the attenuation read backwards.
For the incident mode, `Im K_i > 0`, so its power at `L` is `exp(-2|Im K_i| L)` **smaller** than at the
edge. Dividing one by the other:

```
R_B(L_to) = R_B(L_from) · exp[ 2 (Im K_i – Im K_B) (L_from – L_to) ]
          = R_B(L_from) · exp[ 2 (|Im K_i| + |Im K_B|) (L_from – L_to) ]     (Im K_i > 0 > Im K_B)
```

**The exponent is a sum of magnitudes, not a difference of the same sign.** The two modes attenuate in
opposite directions, and because the quantity is a *ratio* the two attenuations enter in the same sense.
Equivalently, with the power-attenuation coefficients `α_j = 2|Im k_j|` in m⁻¹,

```
R_B(edge) = R_B(plane) · exp[ (α_i + α_B) L_phys ].
```

At the certified maximum the numbers are `|Im K_i| = 1.004047e-3` and `|Im K_B| = 1.002930e-3`, so
`2(|Im K_i| + |Im K_B|) = 4.013954e-3` per thickness and the ten-thickness factor is
`exp(0.040140) = 1.04095`.

## 3. Reproduction of the discrepancy (before any edit)

The peak-search script carried its own copy of the transform:

```
R_B_edge = R_B * exp(2 * abs(Im K_B) * 10)
```

which is the backward decay alone — half the exponent. At the reported maximum (`k_x d = 0.5275`,
`H = 0`, degree 22):

| quantity | value |
|---|---|
| `R_B` at the reference plane (read from the solve) | 0.9467952306769204 |
| edge share from the script's single-mode formula | 0.965978366 |
| edge share from the two-mode transform | 0.985572200 |
| edge share from a direct solve at `L = 0` | 0.985572194 |
| discrepancy between the script and the other producers | **1.9594 percentage points (2.0e-2 relative)** |

`mechanism_controls.py` already used the correct transform (through the shared helper) and reported
0.9855722, so the two scripts disagreed about the same physical number and nothing in the package
compared them. That is the defect this round repairs.

## 4. Independent consistency checks of the transform

* The transform is not tested only against itself: solving the same scattering problem with the
  observation plane at `L = 0, 5, 10, 15, 20` thicknesses and carrying each result to a common plane
  gives the same value to `2.4e-16` (`peak_identity_audit.json → reference_plane`).
* The transform at `L = 10` reproduces the `L = 15` solve to `3e-11` relative, which is the resolution
  of the solver, not of the algebra.
* The exponent contains `d` twice, so `d` cancels identically; the physical form
  `exp((α_i + α_B) Δx)` gives the same number. This is why the `1.0` passed as `d` in
  `mechanism_controls.py` was numerically harmless — and why it was still wrong to leave it there.

## 5. Dependency map

Every place in the package where a plane transformation is, or looks as if it is, applied:

| site | code | formula used | correct? | classification | action |
|---|---|---|---|---|---|
| `edge_plane_fraction` | `build_figure_data.py:150` | `net = 2(abs(ki.imag)+abs(kb.imag))/d; R*exp(net*L*d)`, signature `L=REF_NORM` | equals §2 for `Im K_i>0>Im K_B`, but the argument is mis-named: `L=0` returns the input, `L=REF_NORM` returns the edge value | **CORRECT, API misleading** | re-expressed as `exp[2(ImK_i−ImK_B)(L_from−L_to)]` with explicit `L_to/L_from`; identities documented and tested |
| `isolated_transfer` | `build_figure_data.py:166` | `R*exp(-α_B(ℓ-2µm))` | single-mode absolute decay, correct for its own purpose | **DIFFERENT PHYSICAL QUANTITY** (valid) | docstring now states it is not a ratio and must not be used as one |
| fig02 `R_B_edge` | `build_figure_data.py:238` | `isolated_transfer(R2, kb, p.d, 0.0)` | uses the single-mode decay as if it were a ratio | **INCORRECT** | replaced by `edge_plane_fraction(R2, ki, kb, p.d)` |
| fig04 `R_B_edge` | `build_figure_data.py:331` | `edge_plane_fraction(R2, ki, kb, p.d)` | §2 | **CORRECT** | none |
| fig04 `R_B_100um` | `build_figure_data.py:366` | `R2*exp(-α_B(100µm-2µm))` | single-mode extrapolation of one channel, not a fraction at that plane | **DIFFERENT PHYSICAL QUANTITY** (legacy column, correctly labelled) | documented; not used by any current figure or quoted value |
| fig05 `R_B_edge` | `build_figure_data.py:439` | `R2*exp(α_B·REF_NORM·d)` | omits the incident attenuation | **INCORRECT** | shared transform |
| fig06 `R_B_isolated`, `incident_survival` | `build_figure_data.py:509-510` | `R2*exp(-α_B(ℓ-2µm))`, `exp(-α_i ℓ)` | absolute single-channel quantities, as the caption states | **CORRECT** | none |
| fig07 `R_B_edge` | `build_figure_data.py:507` | `R2*exp(α_B·REF_NORM·d)` | omits the incident attenuation | **INCORRECT** | shared transform |
| `peak_search` rows | `peak_search.py:80` | `R_B*exp(2|Im K_B|·10)` | omits the incident attenuation — **the confirmed cross-script defect** | **INCORRECT** | imports `edge_plane_fraction`; the duplicated formula is deleted |
| `mechanism_controls` (3 sites) | `mechanism_controls.py:80,120,148` | shared function, but `d` passed as `1.0` | correct ratio transform; the `1.0` cancels but invites the assumption that `d` is a thickness | **CORRECT (cosmetic defect)** | `p.d` passed; comment added |
| `peak_identity_audit` plane rescaling | `peak_identity_audit.py:96` | inline `R*exp(net(L-10))` | correct exponent, second implementation | **CORRECT, duplicated** | refactored to call the shared transform twice (plane → edge → plane) |
| `peak_identity_audit` reconstruction | `peak_identity_audit.py:136` | `-|a_B|²p_B exp(2K_B.imag·10)/P_inc` | both factors refer to the **same** plane, so only the backward decay appears | **CORRECT — different quantity** | none |
| `run_study.propagate_R` | `run_study.py:52` (legacy) | `exp(2(K_i.imag−K_B.imag)·L/d)` | mathematically identical to §2 | **CORRECT** (legacy, superseded) | none |
| `regenerate_revised_data` | `regenerate_revised_data.py:287,545` (legacy) | `exp(2(ki−kb).imag·L/d)` | identical to §2 | **CORRECT** (legacy) | none |
| manuscript `tab:configurations` edge shares | `results.tex:407` | 0.0231 / 0.9856 / 0.5802 | from `mechanism_controls`, shared function | **CORRECT** (one cell off by rounding) | 0.0231 → 0.0232 |
| manuscript −11.1 % edge-plane coupling change | `results.tex:539`, `discussion.tex:87`, `conclusions.tex:34` | from `mechanism_controls` edge shares | shared function | **CORRECT** | none |
| figures | `generate_final_figures.py` | plots `R_B_2um` only; labels read "at ℓ = 2 µm" | figures show the reference-plane quantity | **CORRECT** | none |
| claims registry | `claims.json` | no claim refers to the search's `R_B_edge` | — | **CORRECT but uncovered** | new claim + source-agreement row added for the edge fraction |

## 6. What the defect did and did not touch

**Did touch:** the edge-plane column of the density and mobility sweep (130 rows), the coupling sweep
(95 rows), the channel-power dataset (5 rows), and the search record (181 coarse/plateau/refined rows
+ 12 degree rows + 6 quadrature rows). The largest error is 2.0 % at the certified maximum, 0.7 % at the
operating point and 0.68 % in the coupling sweep.

**Did not touch:** the reference-plane headline `R_B = 0.9467952306769204` at `k_x d = 0.5275` (read
directly from the solve), the classification `certified_local_maximum`, the incident-flux ratio, the
energy identity, the coupling percentages at the reference plane, the figures (no panel plots
`R_B_edge`), and the manuscript's headline number.

## 7. Stage 1 verdict

* One defect of a single mathematical kind, in four places (`peak_search`, fig02, fig05, fig07); the
  shared helper itself was correct but under-specified, and one script carried a duplicate.
* The correction is confined to the edge-plane column and to one table cell that moved on rounding.
* Two further actions follow from the audit and are *not* maths fixes: the API must express
  `L_from`/`L_to` explicitly, and a cross-script gate must exist so that two scripts can never again
  disagree about the same number without a gate noticing.
