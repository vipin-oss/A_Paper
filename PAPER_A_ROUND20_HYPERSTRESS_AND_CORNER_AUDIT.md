# Round 20 — hyperstress components, limiting cases, corner line force

All figures measured with `paper_a_study/round20_boundary_audit.py`, degree 6,
tracked mode at the operating point, on a fixed coefficient vector where a
parametric law is being isolated.

## 1. The three hyperstress vectors the model distinguishes

`fields()` returns `τ^{(x)}, τ^{(y)}, τ^{(z)}` — the hyperstress components whose
third index is the gradient direction. They are different tensors:

| pair | relative difference (max abs) |
|---|---|
| `τ_j11` vs solver double-traction row | 1.1e-13 (identical) |
| `τ_j13` vs `τ_j11` | 1.10 |
| `τ_j33` vs `τ_j11` | 1.04 |

Symmetry in the gradient-pair indices: 0.0 (`τ_jil = τ_jli`), as the strain
gradient `η_jil = η_jli` requires.

Only the z-derivative component is affected by the two gradient couplings:

| statement | measured |
|---|---|
| `τ` scales as `λ² = (ℓ/d)²` (ℓ doubled at fixed coefficients) | 4.0000 (expected 4) |
| flexoelectric part linear in `f` (f doubled) | 2.0000 |
| flexoelectric part has no constant term (f halved) | 0.5000 |
| `H`-part grows as `H²` (`Δ(0.5H)/Δ(0.25H)`) | 4.00 |
| `H`-part has no linear term (`Δ(0.75H)/Δ(0.25H)`) | 9.00 |
| magnitude at `0.25 H_crit` (`h = 5.30e-2`) | 1.04e-2 of `max|τ|` |
| `f`/`H` contribution to the x-derivative component | 0.0 (to 1e-30) |

The quadratic `H` law is structural, not fitted: `N = μ + Qφ − h u_zz` is affine
in `h`, and `τ` carries `h N`, so the deviation from `h = 0` is `hQφ − h²u_zz`
with the linear term subdominant by construction of `N`. The exponent is *not*
assumed in the article's text, which must therefore not describe the `H`-entry of
the hyperstress as linear.

**Consequence for the edge condition.** `τ_ijx = ℓ² C_ijkl η_klx`: elastic only.
The edge double traction therefore exists **iff `ℓ ≠ 0`**, and neither `f` nor
`H` can create or remove it. This is the opposite of the inference in Appendix
A.4 (report `FACE_VS_EDGE_NORMAL_AUDIT`, section 3).

## 2. Six limiting cases

`N_s` is the state dimension, `m` the edge row count, `M` the number of outgoing
modes. `n_u = 3N`, `n_φ`, `n_μ` and `n_w = n_u+n_φ+n_μ` at polynomial degree
`N = n−1`. Numbers are for `n = 4` (`15,3,5,23`), `n = 18` (`57,17,19,93`),
`n = 22` (`69,21,23,113`), `n = 30` (`93,29,31,153`).

| case | parameters | order in `k_x` | hyperstress at the edge | ICs / admissible variables | `N_s` | finite eigs | `M` | `m` (rows) | matrix | corner line force |
|---|---|---|---|---|---|---|---|---|---|---|
| **A** full | `ℓ, f, H ≠ 0` | 4 | `τ_ijx = ℓ²Cη_{,x}`; face `τ_ijz` carries `ℓ², f, H` | `u, ∂_z u` up to 3, `φ, μ`; traces available | `2n_w+2n_u` = 76/300/364/492 | `2(n_w+n_u)` = 76/300/364/492 | `n_w+n_u` = 38/150/182/246 | `2n_u+n_φ+n_μ` = 38/150/182/246 | `B ∈ C^{m×M}`, square | present |
| **B** no flexo | `f=0, ℓ≠0, H≠0` | 4 | elastic `ℓ²`; face gains `ℓ²,H` | same as A | same | same | same | same | square | present |
| **C** no strain gradient | `ℓ=0, f≠0` | 2 | `τ ≡ 0` (no `ℓ²`), face `−fE_z` | `u, φ, μ` only; **no axial trace** | `2n_w` | `2n_w` | `n_w` | `n_u+n_φ+n_μ` | square, but double traction **unavailable** | absent (no `τ`) |
| **D** no carrier coupling | `H=0, ℓ≠0` | 4 | `ℓ²Cη_{,x}`; face `ℓ², f` | as A | as A | as A | as A | as A | square | present |
| **E** classical | `ℓ=f=H=0` | 2 | identically zero | `u, φ, μ` | `2n_w` | `2n_w` | `n_w` | `n_u+n_φ+n_μ` | square; double traction degenerates to `0=0` | absent |
| **F** carrier only | `ℓ=0, H≠0` | — | — | — | — | — | — | — | **rejected by the constructor** (`H violates full 3D strict Schur bound`) | — |

Case C is admitted as a documented restriction only (no reported run uses it);
case F is not a case of the model at all — it is refused at construction rather
than quietly solved. The earlier round-19 statement that the double-traction block
"survives in four of the five cases" is replaced by: it survives in A, B and D,
because the *edge* component is elastic-only.

Verified independently of the table: at degree 4 the pencil has exactly
`2(n_w+n_u) = 76` finite eigenvalues and `2(n_w−n_u) = 16` at infinity
(report `SPATIAL_SPECTRAL_COUNT_AUDIT`).

## 3. Corner line force

`f_j = ν_i n_k τ_ijk` on `x=0 ∩ z=±d/2`. It is not annihilated by the traction
and double-traction conditions, so the free-edge problem is complete only when it
is either resolved or shown not to matter. Measured on the delivered data
(`figure_data/corner_assessment.json`, round 19; band parameter `0.4`):

| case | corner share of the boundary functional | degree/band drift | peak/mean |
|---|---|---|---|
| operating point | 9.28e-3 … 9.96e-3 | −6.8 % | 0.098 … 0.102 |
| refined peak | 1.217e-2 … 1.303e-2 | −6.6 % | 0.125 … 0.130 |
| `k_xd=0.55` | 1.180e-2 … 1.264e-2 | −6.6 % | 0.122 … 0.126 |

The share is 1 % of the boundary functional and drifts by 6.6–6.8 % with the
discretisation parameter, i.e. it is **not converged**. It is not used to carry any
reported number: the scattering power balance closes to `8.3e-13` and the edge
absorbs zero power in both electrical configurations, so the flux partition does
not rest on the corner energy. The corner *field* remains unresolved, and this
report does not claim otherwise.

## 4. Observation recorded, not acted on

With this discretisation the flexoelectric and `H` contributions enter the
z-derivative hyperstress only (`model.py:281`, `l == 2`). Whether that is the
intended restriction of `f_3333` to a single gradient direction is a constitutive
question outside the boundary audit; it was **not** changed, and no reported
number depends on resolving it this round. Recorded for the supervisor.
