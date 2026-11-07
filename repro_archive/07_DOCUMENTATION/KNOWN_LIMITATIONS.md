# KNOWN_LIMITATIONS

The complete list, written so that it can be checked against the manuscript.  Each entry
says what the limitation is, what it costs, and where it is admitted in the paper.

---

## 1. Limitations of the physics

| # | Limitation | What it costs | Where it is admitted |
|---|---|---|---|
| P1 | **`R_B` is a modal share, not a reflectance.** It is one member of the outgoing power partition (the backward channel), evaluated at the reference plane `L = 10d`. | You cannot quote it as "94 % of the energy comes back". The total propagating share is a different number (Fig. 5) and is close to 1 − dissipation, not to `R_B`. | Abstract, Fig. 5 caption, §"Results: channel power", conclusions; guarded by `test_backward_share_is_never_called_a_reflectance` |
| P2 | **The carrier–strain-gradient coupling `H` has no measured value**, and neither does the flexoelectric coefficient `f` for this structure. `H* = H_bound/√5` is a plotting normalisation, not a material constant. | The peak value depends on `H`; the paper therefore reports the sweep and the matched controls, not a materials prediction. Everything is confined to `s ≤ 5e-4` (strict convexity with a margin > 2000). | §"Material parameters and scope", Fig. 7, conclusions |
| P3 | **Single-component flexoelectricity** (`f ≡ f_3zz`), no surface flexoelectric effect, no electric-field-gradient flexoelectricity, no full third-order `f_ijkl`. | A real ZnO structure has more couplings; their omission is not quantified. The measured effect of `f` at the operating point is `−0.012 %` (1 nC/m) and `−1.176 %` (10 nC/m), so the omission is bracketed, not eliminated. | §"Constitutive relations", §"Scope" |
| P4 | **Linearised, isotropic-gradient (single-length) strain-gradient elasticity**, `A = ℓ² c ⊗ δ`. No multi-length gradient theory, no surface elasticity. | The dispersion is quantitatively right in structure but not calibrated; `ℓ = 50 nm` is a design value. | §"Gradient energy", limitations paragraph |
| P5 | **Blocking carrier boundaries** on faces and edge; no ohmic/conducting carrier boundary, no surface recombination. | A real contact changes the carrier profile and hence the reflection. Not quantified here. | §"Boundary conditions" |
| P6 | **Time-harmonic problem at fixed real frequency**: there is no initial-value problem, no transient, no pulse propagation. | The word "pulse" appears only for the dispersion context; no pulse dynamics is claimed. | §"Solution of the problem" |
| P7 | **Quasistatic electrostatics**, no retardation, no electromagnetic coupling beyond the reduced electrostatic limit; checked by `quasistatic_check.py` at the operating point. | Nothing at 16.7 GHz with these dimensions; the check quantifies the margin. | §"Electrostatic reduction" |
| P8 | **2.5D: one conserved `k_y`, no `y`-dependence of the geometry.** An edge that is not straight, or a finite-width plate, is outside the model. | The calculation does not describe a beam or a finite patch. | §"Geometry" |

## 2. Limitations of the numbers

| # | Limitation | Value |
|---|---|---|
| N1 | **The corner is closed only as a bounded closure.** The line-force magnitude falls `8.42e-2 → 4.46e-2` (operating), `3.27e-3 → 1.71e-3` (peak), `3.79e-2 → 1.98e-2` (`k055`) between `n = 10` and `n = 28`, i.e. exponent ≈ **−0.63**; the partition moves only `3.9e-6`. | A singular field is **not** resolved; no regularity claim is made. "Fully resolved" is false and is never claimed. |
| N2 | **The reported `R_B` carries a refinement spread**, not an experimental uncertainty: degree `1.10e-6`, quadrature `1.70e-9`, restart `3.24e-6`, tracking path `2.3e-7`. | Quote `0.9428718` with a spread of order `1e-6`, **not** as 8 significant figures of physical accuracy. |
| N3 | **The peak is a local maximum with a flat top** in the searched domain (`k_x d ∈ [0.5267, 0.5276]` within `1e-4` of the maximum; `[0.5265, 0.5280]` within `1e-3`). It is not established to be the global maximum of the branch. | The classification is `certified_local_maximum`, and the word "global" is not used. |
| N4 | **Case-C restriction.** The reported mechanism statement is restricted to the case solved (free, charge-free edge, insulating electrical condition, `H` inside the Schur bound); it is not extended to grounded or metallised edges. | The grounded variant is a different BVP and is retained only for baseline reproduction. |
| N5 | **The manuscript was never compiled** in the build environment (no TeX engine). | Layout, page breaks and overfull boxes are unverified; only structure, references, citations and figure paths were validated. |

## 3. Limitations of the evidence

| # | Limitation |
|---|---|
| E1 | **No experimental comparison exists**, and none is claimed: there is no measurement of `R_B` for this structure. |
| E2 | **No independent third-party numerical benchmark** of the same coupled edge problem exists in the literature reviewed; the defence is the reduction set (closed-form SH limits, strong-form roots, FE mesh, reciprocity), not a head-to-head comparison. |
| E3 | **No 3D finite-element cross-check** was possible in this environment; the independent FE check is 1D in the thickness (`MeshPlate`) and does not resolve the edge. |
| E4 | **The 2025 thermodynamic-consistency theory** (IJES 208, 104165) already provides the framework; the novelty claim is restricted to the reflection/edge-mode calculation. No priority claim beyond that is made. |
| E5 | **No Fisher-information / Cramér–Rao analysis** was performed; the sensitivity information is the finite-difference sweeps (`fig02`, `fig03`, `fig07`). |

## 4. Things that look like limitations but are not

* *"The battery has 1 SKIP"* — the SKIP is the missing TeX engine (N5), not a failing
  check; the other 22 checks pass.
* *"`results_legacy/` contains values that disagree with the paper"* — it is a historical
  folder, excluded from every claim and from every audit read.
* *"The archive omits a 29 MB SVG"* — regenerable in ~10 s; not referenced by the
  manuscript.
* *"Some labels are never referenced"* — `static_check.py` lists them as notes; unused
  labels are not errors.

## 5. If you want to remove a limitation

In rough order of scientific value per unit effort:

1. **N5** — compile on any machine with TeX Live (`04_REPRODUCTION/REPRODUCE_FROM_SCRATCH.md` §5). This is a 2-minute fix and it closes the only build-level unknown.
2. **E2/E3** — solve the same BVP in a commercial FE package with a refined edge mesh; compare `R_B` and the corner force. This is the check the project could not run.
3. **P2** — measure or compute `f_3zz` and `H` for ZnO; the sweeps tell you exactly how much the reported number would move.
4. **N1** — a graded/geometric edge mesh with an explicit singularity exponent fit; would either confirm `−0.63` or replace it.
