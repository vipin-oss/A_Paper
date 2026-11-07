# Round 20 — face-versus-edge normal audit (R20-1)

## 1. The two surfaces are different problems

The body is `{−d/2 < z < d/2} × {x > 0}`. Its faces `z = ±d/2` have normal
`n = (0,0,±1)`; its reflecting edge `x = 0` has `n = (±1,0,0)`. The four
conditions on each surface are the same *kinds* of statement but are built from
different components of the same tensors. They are not interchangeable, and a
numerical identity on one surface says nothing about the other.

| quantity | face `z=±d/2` | edge `x=0` |
|---|---|---|
| traction | `Σ_3j = σ_3j − ∂_kτ_3jk` (+ surface divergence) | `Σ_1j = σ_1j − ∂_kτ_1jk` (+ surface divergence) |
| double traction | `τ_3j3 = n_jn_kτ_ijk` | `τ_1j1` |
| normal electric displacement | `D_z` | `D_x` |
| normal carrier flux | `J_z` | `J_x` |
| conjugate essential datum | `u_j`, `∂_z u_j`, `φ`, `μ` | `u_j`, `∂_x u_j`, `φ`, `μ` |

Both columns are physically correct *for their own surface*: `D_z = 0` is the
open-circuit face condition the article uses, and `D_x = 0` is the charge-free
edge condition. The audit question is only whether each statement is attached to
the surface it belongs to.

## 2. What the article says

* `eq:bc_edge` (governing equations): `σ_ix = 0, τ_ijx = 0, D_x = 0, J_x = 0` at
  `x = 0`. **Correct normals.**
* `eq:bc_faces_mech`, `eq:bc_faces_carrier`, and the open-circuit `D_z = 0`
  statement: **correct face normals.**

## 3. What Appendix A.4 says

The appendix opens the edge subsection with "At the edge `x = 0` the conditions
`(eq:bc_edge)` are imposed weakly" and then lists

> the traction `Σ_{3j}` on the `n_u = 3N` displacement test functions, the double
> traction `τ_{3j3}` on the same `n_u` test functions, the normal electric
> displacement `D_z` on the `n_φ` potential test functions and the normal carrier
> flux `J_z` on the `n_μ` carrier test functions,

and argues the double-traction block from

> `τ_{3zz} = ℓ²[c₁₃(η_xxz + η_yyz) + c₃₃η_zzz] − fE_z + HΔn`.

This is R20-1, and it is **substantiated**: at `x = 0` the appendix uses the *face*
components. The row **count** it derives is nevertheless right —
`m = 2n_u + n_φ + n_μ` — and the code matches it exactly
(`[T[:nu], R, q[ip]/T[ip], T[im]]`, `edge_size = 38/150/182/246` for
`n = 4/18/22/30`), so the error is in the labels and in the hyperstress formula,
not in the structure of the edge system.

The consequence is not cosmetic. `τ_{3zz}` is the z-normal trace; the edge
condition uses `τ_{ijx}`, which in this model is

```
τ_ijx = ℓ² C_ijkl η_klx      (no f, no H term enters the x-derivative component)
```

— measured, not assumed: at fixed coefficient vector the `f`- and `H`-parts of
the hyperstress change the z-derivative component by 0.0 (to 1e-30) when the
x-derivative component is compared (audit check 6). So the sentence that the
double-traction block "survives in four of the five limiting cases" because
`−fE_z` carries no `ℓ` is exactly the inference the round-19 protocol forbids:
`τ_ijx` is elastic-only, so the edge double traction exists iff `ℓ ≠ 0`, i.e. in
cases A, B, D and not in C or E — which happens to agree with the appendix's
conclusion but not with its reasoning.

## 4. What the solver does

Measured at degree 6, operating point, on the tracked mode:

| candidate component | relative distance from the solver's double-traction row |
|---|---|
| `τ_j11` (x-normal) | **1.1e-13** |
| `τ_j13` | 1.10 |
| `τ_j33` (z-normal) | 1.04 |

The solver's double-traction row is the x-normal `τ_ij1`. The solver is therefore
correct on R20-1 and the appendix is wrong; the manuscript body is right. This was
checked independently of the appendix and of any eigenvector bookkeeping: the
three candidates differ by O(1) from each other, so the identification is not a
tolerance argument.

The mechanical block is *not* a pointwise component at all — it is the weak
generalised traction `A10+ikA11−k²A12−ik(A20+ikA21−k²A22)` identified to
1.2e-14. The appendix's `Σ_{3j}` description would be equally wrong even with the
index fixed to 1, because `σ_ix` alone does not vanish pointwise (see
`VARIATIONAL_BOUNDARY_DERIVATION`, section 5).

## 5. Essential versus natural, per surface

| condition | face `z=±d/2` | edge `x=0` | essential? |
|---|---|---|---|
| traction | `Σ_3j = 0` (natural) | `Σ_1j = 0` (natural) | no |
| double traction | `τ_3j3 = 0` (natural) | `τ_1j1 = 0` (natural) | no |
| electric (charge-free) | `D_z = 0` (natural) | `D_x = 0` (natural) | no |
| electric (equipotential) | `φ = φ_e` (essential) | `φ = 0` (essential) | yes |
| carrier blocking | `J_z = 0` (natural) | `J_x = 0` (natural) | no |

The only place the article's configuration could legitimately become essential is
the electrical row, and that is precisely the row the round-19 solver altered
(R20-2). No essential datum is prescribed anywhere in the article's edge problem.

## 6. Verdict on R20-1

| item | verdict |
|---|---|
| `eq:bc_edge` normals | **correct** (x-normal) |
| face conditions | **correct** (z-normal) |
| Appendix A.4 edge normals | **wrong** — face components used for the edge |
| Appendix A.4 `τ_3zz` argument | **wrong** component, and the wrong kind of inference |
| Appendix A.4 row count `m = 2n_u+n_φ+n_μ` | correct |
| solver double-traction normal | **correct** (x-normal, 1.1e-13) |
| solver traction | correct variationally; the manuscript's pointwise shorthand is not |
| classification | **Outcome A for R20-1** — a documentation error, no arithmetic follows from it |
