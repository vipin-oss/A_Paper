# Round 15 — boundary variation and corner audit

## 1. The surface terms of the mechanical variation

From the virtual work with the contraction identity `eq:contraction`, the two
integrations by parts produce, on a surface with unit normal `n`:

  ∮ [ n_j σ_ij − n_j ∂_k τ_ijk ] δu_i dS + ∮ n_k τ_ijk δu_ij dS .               (1)

The first integral is the classical traction `t_i = n_jΣ_ij` with
`Σ_ij = σ_ij − ∂_kτ_ijk`, the effective stress of `eq:effective`. The second
carries the normal derivative of the virtual displacement and defines the double
traction `r_ij = n_kτ_ijk`. Both are present in the model:

- on the faces `z = ±d/2`, `eq:bc_faces_mech` sets `σ_iz = 0` and `τ_ijz = 0`,
  i.e. both brackets vanish;
- at the edge `x = 0`, `eq:bc_edge` sets `σ_ix = 0`, `τ_ijx = 0`, `D_x = 0`,
  `J_x = 0`. These are imposed as boundary rows of the edge system, not as
  integrals, because the edge problem is solved in `x` by the mode expansion.

## 2. The boundary-of-boundary term

When the edge meets a face, the surface integral of (1) is taken over a surface
with a boundary — the corner line — and Stokes' theorem turns the surface
divergence of the double-traction work into a line integral along it. The density
of that line force is

  f_k = n_z τ_kjz |_{x=0} ,                                                      (2)

evaluated on the limit of the face conditions. This is the Mindlin corner force
of a second-gradient theory. It is **not** zero when the face and edge conditions
are both imposed, and it cannot be removed by choosing the two conditions
independently: it is the price of a theory in which the traction and the double
traction are both prescribed on the same free surface.

## 3. What this model does at the corner

- The weak form of (1) is imposed exactly at the corner: the corner is a
  quadrature point of the thickness integrals at `x = 0`.
- The line force (2) is **non-zero** there; `corner_assessment.py` measures a
  density `>1e-4` in the normalised units of the study.
- Its energy share is bounded and reported: the corner band contributes less than
  the quoted tolerance to the partition, which is the reason the reported
  `R_B` values do not rest on it.
- The geometry solved is therefore a plate with a straight edge and a corner
  field that is **not resolved pointwise**.

## 4. Status: unresolved, and correctly reported as such

This round did **not** repair the corner term, and did not add a boundary
condition to make the formulation formally complete. Adding a condition would
change the physical problem; the corner force is a genuine open item of the
model, and it is stated as a limitation in `sec:disc_limitations` and in the
appendix. It is not a defect introduced by round 14 or round 15, and nothing in
the round-15 rewriting of the weak form depends on it.

One thing the rewriting *did* change is the accuracy of the statement: the
surface terms of the two integrations by parts are now written out
(`eq:ibp_stress`, `eq:ibp_hyper`), so a reader can see for himself that the
corner contribution exists rather than being told that the boundary terms
vanish. They vanish on the faces; they do not vanish at the corner.

## 5. Electrical and carrier boundary terms

- Gauss: the surface term is `n_zD_zψ*`. The grounded case imposes `φ = 0`
  essentially; the open-circuit case imposes `D_z = 0` as the natural condition.
  The open circuit has a genuine null vector (the additive constant of `φ`),
  removed by the zero-mean gauge; that is a property of the equation, not a
  numerical artefact, and it is stated in the text.
- Carrier: the surface term is `n_zĴ_zΦ*`, and the blocking condition `J_z = 0`
  makes it vanish. No corner term arises here, because the carrier equation is
  first order in the flux and produces a single surface term per face.
