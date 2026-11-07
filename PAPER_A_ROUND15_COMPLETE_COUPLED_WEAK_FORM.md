# Round 15 — the complete coupled weak form

This document derives the three weak equations of the solved problem from the
field equations, then shows how the assembled matrix follows from them. It is
the mathematical content behind `eq:weak_mech`, `eq:weak_gauss`,
`eq:weak_carrier` and `eq:block` of the manuscript. Notation is that of §2; a
prime is `d/dz`, a hat an amplitude of the ansatz `eq:ansatz`.

---

## 1. Starting point: the three field equations

Mechanical balance (`eq:momentum`):

  ρ ü_j = ∂_i σ_ij − ∂_i ∂_k τ_jik ,   σ_ij = c_ijkl ε_kl − e_kij E_k ,
  τ_ijk = A_ijklmn η_lmn + H_ijk Δn − f_lijk E_l .                                  (1)

Gauss's law (`eq:gauss`), with E_i = −∂_iφ:

  ∂_i D_i = −q Δn ,   D_i = κ_ij E_j + e_ijk ε_jk + f_ijkl η_jkl .                  (2)

Carrier continuity (`eq:continuity`), J_i being the electron *number* flux:

  q ∂_t Δn + ∂_i J_i = 0 ,   J_i = −(D n₀/k_BT) ∂_i μ̃ ,
  μ̃ = a Δn − qφ + H_jkl η_jkl ,   a = k_BT/n₀ .                                     (3)

The three equations are coupled through (1)–(3): `Δn` enters the hyperstress,
`η` enters `μ̃`, and `φ` enters both.

---

## 2. The mechanical weak equation

Multiply (1) by a test displacement `v_j*`, integrate over the thickness at fixed
`x` and integrate by parts once on `∂_iσ_ij` and twice on `∂_i∂_kτ_jik`. The
second integration produces a boundary term in `n_k τ_ijk ∂_j v_i*` and one in
`n_j ∂_k τ_ijk v_i*`:

  −∫ ρ ü_j v_j* dζ + ∫ σ_ij ε_ij*(v) dζ + ∫ τ_ijk η_ijk*(v) dζ
  − [ n_j σ_ij v_i* ] − [ n_j t_ijk v_i* ] + [ n_k τ_ijk ∂_j v_i* ] = 0 .           (4)

With the time-harmonic substitution `∂_t → −iω` (so `ü → −ω²û`) and vanishing
traction and double traction on the faces, (4) is exactly the manuscript's
`eq:weak_mech`:

  ∫ [ σ̂_ij ε̂_ij*(v) + τ̂_ijk η̂_ijk*(v) ] dζ = ω² ∫ ρ û_i v_i* dζ .                 (5)

**Why the surface terms vanish here.** On z = ±d/2 the faces are
traction-free and double-traction-free (`eq:bc_faces_mech`), so both bracket
terms of (4) vanish there. At the edge x = 0 the same brackets supply the edge
conditions `eq:bc_edge`; in this article the edge problem is solved in the
`x` direction by the mode expansion and not by a weak statement in `x`, so the
edge brackets appear as boundary rows of the edge system, not as integrals.
The corner term is discussed in the separate boundary audit.

---

## 3. The electrical weak equation

Multiply (2) by a test potential `ψ*` and integrate by parts once:

  −∫ D_i ∂_i ψ* dζ − ∫ q Δn ψ* dζ + [ n_z D_z ψ* ] = 0 .                            (6)

Since `E_i(ψ) = −∂_iψ`, and since the natural boundary term `n_zD_zψ*` is exactly
the open-circuit condition, (6) is the manuscript's `eq:weak_gauss`:

  −∫ D̂_i Ê_i*(ψ) dζ − q ∫ Δn̂ ψ* dζ = 0 .                                           (7)

The grounded case replaces the surface term by the essential condition
`φ = 0` on both faces, which the potential space enforces exactly (the
`P_j − √((2j+1)/(2j+5)) P_{j+2}` combinations of `eq:basis`).

**Correction made in round 15.** The round-14 version of this equation carried
no charge term at all: it displayed `−∫D̂_i Ê_i*(ψ) = 0`, which is the statement
for a dielectric without free carriers and is *not* Gauss's law for this
problem. The charge term is present in the assembled matrix (it is the `⟨W,W⟩`
block, with `N = μ̃ + Qφ` the dimensionless carrier amplitude), so the numbers
were never affected; the displayed equation was.

---

## 4. The carrier weak equation

Equation (3) is first order in time and second order in space. With the
time-harmonic substitution:

  −iω q N̂ + ∂_i Ĵ_i = 0 ,   Ĵ_i = −(D n₀/k_BT) ∂_i μ̃ .                              (8)

Multiply (8) by a test function `Φ*`, integrate, and integrate the flux term by
parts. The boundary term `n_z Ĵ_z Φ*` is the blocking condition `J_z = 0`
(`eq:bc_faces_carrier`), so it vanishes on the faces:

  −iω q ∫ N̂ Φ* dζ + (D n₀/k_BT) ∫ ∂_i μ̃ ∂_i Φ* dζ = 0 .                            (9)

Divide (9) by `−iω q` and non-dimensionalise. With `α_d = D/(d c_s)` the transport
group and with frequencies measured in `c_s/d`, the factor multiplying the
gradient term becomes `i α_d/ω`, and (9) is the manuscript's `eq:weak_carrier`:

  ∫ [ N̂ Φ* − (i α_d/ω) ∂_i μ̃ ∂_i Φ* ] dζ = 0 .                                      (10)

**This is not the same statement as the enthalpy term `μ̃N*`.** The enthalpy
variation contributes `μ̃ δ(Δn)`; equation (10) is the divergence of the flux
balance, and it is the *elimination of `Δn` in favour of `μ̃`* that makes the
carrier unknown the electrochemical potential rather than the density. That
elimination is exact here because `μ̃` is algebraic in `(Δn, φ, η)` — the
relation `Δn = (μ̃ + qφ − H:η)/a` is invertible at fixed `φ` and `η` — so no
approximation is involved and the solver may carry `μ̃` as its unknown, which it
does.

---

## 5. The assembled block system

The three equations are discretised in one matrix because they are coupled. The
unknown vector is `q = (û₁, û₂, û₃, φ̂, μ̃)` of dimension `3n + n_φ + n`; the
matrix is stored as nine blocks `A_rs`, `r,s ∈ {0,1,2}`, indexed by the power of
`k_x` carried by the test factor and the trial factor. Each block is one
quadrature of the integrands of §2–§4 against the Legendre basis:

| Term of `eq:block` | Integral | From |
| --- | --- | --- |
| `⟨B_r, C B_s⟩` | ∫ ε̂*(v)ᵀ C ε̂(u) | (5) |
| `λ²⟨∂B_r, C ∂B_s⟩` | ∫ ℓ² ∂_ζη̂*(v)ᵀ C ∂_ζη̂(u) | (5) |
| `⟨G_r, e B_s⟩ + ⟨B_r, eᵀ G_s⟩` | ∫ (E*(ψ)ᵀ e ε̂ + ε̂*(v)ᵀ eᵀ Ê) | (5) and (7) |
| `−⟨G_r, κ G_s⟩` | −∫ Ê*(ψ)ᵀ κ Ê | (7) |
| `f(⟨G_r, ∂B_s⟩ + c.c.)` | ∫ f (E* ∂η̂ + ∂η̂* E) | (5) and (7) |
| `−(iα_d/ω)⟨MG_r, MG_s⟩` | −(iα_d/ω)∫ ∂μ̃* ∂μ̃ | (10) |
| `−⟨W_r, W_s⟩` | −∫ (N̂* − h ∂²û₃*)(N̂ − h ∂²û₃) | (7) charge term, compressibility and the added coupling, completed into one square |
| `−ω²⟨U,U⟩ δ_{r0}δ_{s0}` | −ω² ∫ ρ û* û | (5) inertia |

The engineering shear components are used in `B_r` (no factor ½), which is
consistent with the Voigt form of `C`; this is a bookkeeping choice and cancels
between the two appearances of the shear strain in the quadratic form.

The square is the thermodynamic statement: the enthalpy `a(Δn)² + 2HΔn η_zzz +
(h²/a)η_zzz²` is positive definite in `(Δn, η_zzz)` precisely when it is a square,
which is the admissibility condition of §2.11. Writing it as one square is also
what makes the coupling symmetric in the assembled matrix, and it is why a single
vector `W` supplies both the charge term of (7) and the coupling of (5).

**Elimination.** The solver does not invert `μ̃` inside the matrix; it carries
`μ̃` as a degree of freedom in the spatial route and, in the temporal route,
solves the `W` rows for `μ̃` explicitly (`μ̃ = N + solve(W, F U − Q wᵀ φ)`), so
that `φ` is the only field eliminated before the generalised eigenproblem in
`ω²`. Both routes therefore solve the same three equations of §2–§4; the
elimination is a linear-algebra step applied to the same weak system, not a
different model.

---

## 6. What this does and does not establish

- It establishes that the displayed weak equations are the weak forms of (1)–(3)
  and that the block construction of the manuscript reproduces the assembled
  matrix term by term (each entry is a quadrature of a listed integrand).
- It does **not** establish that the discretisation is accurate: that is the
  business of the convergence and independent-scheme checks, which are unchanged.
- It does **not** resolve the corner term (§ boundary audit).
- The eigenvalues are unchanged by this round: no matrix entry, dataset or
  solver line was modified.
