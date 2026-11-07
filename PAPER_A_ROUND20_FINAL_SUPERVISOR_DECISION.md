# Round 20 — final decision for supervisor review

Stop point: the boundary audit is complete, the discrepancy is established and
named, the model has been repaired, the affected results have been recomputed and
the manuscript, registry and tests have been brought into agreement **with the
corrected problem**. The round does **not** claim that the package is verifiable:
the PDF was never compiled, the corner field is unresolved and the traction was
not reduced to a pointwise identity.

## 1. Outcome category

| submission | verdict | category |
|---|---|---|
| **R20-1** (face versus edge normals) | substantiated against the *appendix*, which applies the face quantities `Σ_3j, τ_3j3, D_z, J_z` to the edge `x=0`; the article body and the solver are correct | **A — documentation error** |
| **R20-2** (`q[ip]` = grounded edge) | substantiated: the delivered datasets solve `φ(0,z)=0`, not `D_x(0,z)=0` | **B — implementation error, scientific blocker** |

Both are reported; neither is repaired by relabelling. The word "charge-free" is
never applied to the grounded configuration, `x`-normal and `z`-normal conditions
are never treated as interchangeable, and no result was adjusted to preserve a
number that was already in the manuscript.

## 2. The correct model

Free edge `x = 0` of the layer: no essential datum. Natural conditions on the
potential test functions and the two mechanical test blocks,

```
weak generalised traction  (σ_ix − ∂_kτ_ixk − ∂_j^s τ_ixj),   τ_ijx = 0,
D_x = 0   (natural, φ free),                                  J_x = 0,
```

with `τ_ijx = ℓ²c_ijkl η_klx` and the **corner line force** `f_j = ν_i n_k τ_ijk`
as the one part of the variation that these conditions do not annihilate.

This is the model the article states. It is now the default
(`Plate(edge_electric='insulating')`, `build_figure_data.EDGE_ELECTRIC`).

## 3. What produced the delivered numbers, and what changes

The delivered numbers are the grounded-edge solution. Recomputing the same
observables for the correct problem:

| quantity | delivered | corrected |
|---|---|---|
| `R_B` at the certified maximum (`k_xd = 0.52719`) | 0.9468 (`k_xd=0.5275`) | **0.9428718** |
| `R_B` at the flat-top centre `k_xd = 0.52752` | — | 0.9428521 |
| edge-plane share at the maximum | 0.9856 | **0.9824** |
| `k_xd = 0.55` | 0.5792 | **0.5519** |
| operating point | 0.0231 | **0.0193** |
| propagating share at the maximum | 99.77 % | **99.92 %** |
| coupling-induced change at the maximum | −34.2 % | **−36.1 %** |
| degree stability of the maximum | 1e-8 | **1.1e-6** (bound restated as 1e-5) |

The qualitative physics survives — one certified local maximum on a flat top, a
near-unity backward share at a zero-group-velocity fold, a two-orders-of-magnitude
smaller operating-point share — but the numbers move, the operating-point share by
16.7 %, and the degree convergence of the maximum degrades by two orders of
magnitude.

## 4. Tests and checks run

| check | result |
|---|---|
`round19_tests.py` (round-19 baseline, pinned `edge_electric='ground'`) | 7/7 PASS
`round20_boundary_audit.py` (ten boundary checks, 39 assertions) | all PASS
`test_model.py` (unit and scientific tests) | 52/52 PASS
`claim_audit.py` (23 claims, 46 tokens, 10 cross-script rows) | PASS
`mutation_tests.py` (deliberate defects) | PASS
`static_check.py` | PASS (170 labels, 108 references)
`run_all_checks.py` battery | **OVERALL: PASS** — 17 of 18 checks PASS, 1 SKIP (no engine)
LaTeX build | **NOT EXECUTED — no engine in this environment (BUILD UNVERIFIED)**

Every failed check encountered during the repair was repaired at its cause:
the grounded-corner test now constructs the grounded configuration explicitly, the
degree-convergence test and threshold carry the measured charge-free spread, the
peak abscissa in the search, the identity audit, the mechanism controls and the
tests is the certified argmax, and the claim registry was re-derived from the
regenerated data rather than edited to match prose.

## 5. Acceptance gates

| gate | verdict | evidence |
|---|---|---|
| 1. normals correct on each surface | **PASS** | `eq:bc_edge` x-normal; appendix fixed; solver row ≡ `τ_j11` (1.1e-13) |
| 2. hyperstress contractions used correctly | **PASS** | `τ_j11` vs `τ_j13`/`τ_j33` differ by 1.10/1.04; `τ_ijx` elastic-only |
| 3. complete mechanical variation | **PARTIAL** | traction verified variationally (1.2e-14) but not reduced pointwise; no pointwise claim made |
| 4. Dirichlet `φ` (grounded configuration) | **PASS** | `r_φ = 1.6e-15` |
| 5. Neumann `D_x` (charge-free configuration) | **PASS** | `r_{D_x} = 8.5e-13` |
| 6. carrier blocking | **PASS** | `r_J = 4.5e-10` |
| 7. double traction | **PASS** | `r_m = 3.8e-13` |
| 8. edge-row construction | **PASS** | `m = 2n_u+n_φ+n_μ` = 38/150/182/246, full rank, cond 141 |
| 9. finite/infinite classification | **PASS** | 76+16 at degree 4, 108+24 at degree 6, regular pencil |
| 10. power balance | **PASS** | 8.3e-13, zero edge absorption |
| corner line force resolved | **NOT VERIFIED** | share 1.2e-2 drifting 6.8 % with the band |
| pointwise traction identity | **NOT VERIFIED** | four families fail by 0.3–6.2 relative |
| PDF compilation | **NOT VERIFIED** | no TeX engine |
| material parameters physical | **NOT VERIFIED** | synthetic ℓ, f, H (unchanged from earlier rounds) |

## 6. Overall verdict

**NOT VERIFIED.** The discrepancy is found, its cause is named, the model is
repaired and the corrected results are recomputed, certified and consistent with
the manuscript and the registry — but four gate items remain open (pointwise
traction, corner field, PDF build, physical parameters), and per the round-20
protocol a critical failure cannot be overridden by passing unit tests, nor can a
blanket PASS be issued.

Nothing further is changed without supervisor direction. The specific decisions
requested are:

1. Accept the certified-maximum abscissa (`k_xd = 0.52719`) as the reported
   location, replacing the flat-top centre `0.52752`.
2. Accept the restated degree-stability bound (1e-5 rather than 1e-8) and the
   reduced precision of the peak value that follows from it.
3. Decide whether the corner line force must be resolved (a new discretisation
   element) or may remain a stated limitation.
