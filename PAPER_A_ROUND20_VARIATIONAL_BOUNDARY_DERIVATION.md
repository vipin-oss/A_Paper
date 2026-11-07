# Round 20 — independent variational derivation of the free-edge conditions

Nothing in this report is taken from the manuscript or from the solver; the
derivation is from the enthalpy that the article itself states, and the numbers
quoted at the end are the measured boundary residuals of the delivered solver.

## 1. Enthalpy and its first variation

With `η_jkl = ∂_l ε_jk`, `E_i = −∂_i φ`, and the volume `Ω = {−d/2<z<d/2} ×
{x>0}`,

```
W = ½ C_ijkl ε_ij ε_kl + ½ ℓ² C_ijkl η_mij η_mkl
    − e_kij E_k ε_ij − ½ κ_ij E_i E_j
    + f_ijkl E_i η_jkl + H Δn η(333-components) + W_carrier(n, ∇n)
```

Only `f_3333` is retained in this article, and the `H` coupling acts on the same
gradient component; both are the `k_z`-gradient entries, which is why the
hyperstress that carries them is the *z-derivative* one (verified numerically,
report `HYPERSTRESS_AND_CORNER`, checks 3–6).

Taking the first variation with `δE_i = −∂_i δφ`, `δη_jkl = ∂_l δε_jk`, and the
carrier variation written in terms of the electrochemical potential `μ`,

```
δΠ = ∫_Ω [ σ_ij δε_ij + τ_ijk ∂_k δε_ij + D_k ∂_k δφ + J_k ∂_k δμ ] dV + BC,
σ_ij = C_ijkl ε_kl − e_kij E_k,        τ_ijk = ∂W/∂η_ijk,
D_k  = e_kij ε_ij + κ_kj E_j + f-part, J_k = −(q D / (μ_c n₀)) ∂_k μ  (reduced form),
```

i.e. the constitutive objects that appear in the article, with the two gradient
couplings entering `τ` and `D` respectively.

## 2. First integration by parts (volume)

```
∫_Ω τ_ijk ∂_k δε_ij dV = ∮_∂Ω n_k τ_ijk δε_ij dS − ∫_Ω (∂_k τ_ijk) δε_ij dV .
```

The volume term combines into the equilibrium of the *generalised* stress
`σ_ij − ∂_k τ_ijk`; together with `δΠ/δu_i = 0` this is the volume equation the
article states. Nothing about the edge is decided here.

## 3. Second integration by parts (the face terms)

Writing `δε_ij = ½(∂_i δu_j + ∂_j δu_i)` on `∂Ω` and splitting each surface
derivative into a tangential part and a normal part,
`∂_i = ∂_i^s + n_i ∂_n`,

```
∮ (σ_ij − ∂_k τ_ijk) δε_ij = −∮ ∂_j(σ_ij−∂_kτ_ijk) δu_i  +  ∮ n_j(σ_ij−∂_kτ_ijk) δu_i ,
∮ n_k τ_ijk δε_ij        = ∮ n_k τ_ijk ½(∂_i^s δu_j + ∂_j^s δu_i)
                          + ∮ (n_i n_k τ_ijk) ∂_n δu_j .
```

On a free surface `δu_j` **and** `∂_n δu_j` are independent data: prescribing
`u` fixes the first, prescribing the normal derivative fixes the second, and a
natural condition must annihilate each coefficient separately. Hence

* **double traction** (coefficient of `∂_n δu_j`):  `m_j = n_i n_k τ_ijk = 0`;
* **generalised traction** (coefficient of `δu_j`): `t_j = n_i(σ_ij − ∂_k τ_ijk)
  − ∂_i^s(n_k τ_ikj) = 0`, the second term being the surface divergence of the
  normal hyperstress.

The tangential half `½(∂_i^s δu_j + ∂_j^s δu_i)` is *not* independent data: it is
a surface derivative of `δu_j`, so moving it onto the coefficient is the only
option and it produces

* **corner line force** on `∂∂Ω` (`x=0 ∩ z=±d/2`):  `f_j = ν_i n_k τ_ijk`,
  with `ν` the co-normal of the edge inside the face.

The electrical and carrier conditions come from the two scalar variations, whose
surface terms are `∮ D_k n_k δφ` and `∮ J_k n_k δμ`:

* **electrical**: `D_n = 0` *natural* if `φ` is free; `φ` *essential* if the
  surface is an equipotential (a metallised edge).
* **carrier**: `J_n = 0` natural (blocking), `μ` (or `n`) essential otherwise.

## 4. What the four stated conditions are

With `n = (±1,0,0)` on the reflecting edge,

| stated | derived object | status |
|---|---|---|
| `σ_ix = 0` | `t_i = n_j(σ_ij−∂_kτ_ijk) − ∂_j^s(n_kτ_ikj) = 0` | the *weak/weak-form* name of the generalised traction; **not** a pointwise identity for `σ_ix` alone |
| `τ_ijx = 0` | `m_i = n_j n_k τ_ijk = 0` | correct: the x-normal double traction |
| `D_x = 0` | `D_n = 0` (natural) | correct *iff* the edge is charge-free (no electrode) |
| `J_x = 0` | `J_n = 0` (natural) | correct for a blocking edge |

Necessary, sufficient, over-prescribed?

* **Necessary**: both mechanical conditions are conjugate to independent boundary
  data (`δu_i` and `∂_n δu_i`); neither can be dropped. In the discrete problem
  they are `2n_u` equations for `n_u` displacements and `n_u` axial traces.
* **Sufficient**: with `t = 0`, `m = 0`, `D_n = 0`, `J_n = 0` the edge problem is
  square — `m = 2n_u + n_φ + n_μ = n_w + n_u = M`, verified for the delivered
  solver (`edge_size == outgoing_modes`, rank full, condition number 141–161 after
  scaling, report `NUMERICAL_IMPACT`).
* **Not over-prescribed**: dropping either mechanical block would leave `n_u`
  trace unknowns unconstrained; dropping the electrical row and keeping `φ` free
  is the charge-free configuration; *imposing* `φ = 0` as well would over-prescribe
  the electrical side (both `φ` and `D_n` fixed), which is exactly what the
  round-19 solver did.

## 5. Where the manuscript's shorthand is literally false, and where it is right

Measured on the delivered solver (full superposed field, x = 0, degree 22):

| configuration | weak traction residual | pointwise `σ_x1 − i k τ_j11` |
|---|---|---|
| grounded, operating point | 2.8e-15 | **0.333** |
| charge-free, operating point | 2.7e-15 | **0.345** |
| grounded, `k_xd=0.55` | 2.8e-15 | 0.098 |
| charge-free, `k_xd=0.55` | 2.2e-15 | 0.106 |

The implemented traction *is* the variational flux (identified algebraically to
1.2e-14 as `A10+ikA11−k²A12−ik(A20+ikA21−k²A22)`), and the pointwise combination
`σ_ix − i k τ_ijx` does **not** vanish anywhere on the solution. Four plausible
pointwise families were tested on the superposed field and none reproduces the
implemented row (0.93–2.65 relative deviation, actions 1099–1102).
Consequence for the manuscript: `eq:bc_edge` is a statement about the *weak*
boundary functional. Written as "`σ_ix=0`" it is false pointwise, and the
correction must say so in the article's own language.

## 6. Corner

The line force `f_j = ν_i n_k τ_ijk` is not annihilated by `t=0` and `m=0`; it is
a genuine part of the variation and is reported, not claimed small (report
`HYPERSTRESS_AND_CORNER`, section 5).
