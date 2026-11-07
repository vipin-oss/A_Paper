# Round 15 — independent mathematical audit

Round-14 baseline `18e3cb6`. This is the review that decides whether the
mathematics written in round 14 is correct, not whether the code still runs.
Every claim below was re-derived from the enthalpy and checked against the
implemented operator; nothing was accepted from the round-14 report.

## 1. Findings and dispositions

| ID | Finding | Class | Disposition |
| --- | --- | --- | --- |
| M15-1 | `δη_ijk = δu_i,jk` asserted as a component identity | **CONFIRMED ERROR** | Repaired: component relation kept, contracted identity `τ:δη = τ:δu_jk` proved and used |
| M15-2 | One integral presented as "the weak form"; carrier equation shown as an enthalpy term | **CONFIRMED ERROR** | Repaired: three weak equations (A)–(C) plus the assembled block system (D) |
| M15-2b | Gauss's law displayed without the mobile charge | **CONFIRMED ERROR** | Repaired: charge integral restored |
| M15-3 | Nine blocks implied to exist; two vanish identically | **INCOMPLETE / MISLEADING** | Repaired: `A₀₂ = A₂₀ = 0` stated, with the reason |
| M15-5 | `α` used for the transport group while §2.9 reserves `α` for attenuation | **NOTATION ERROR** | Repaired: `α_d` everywhere for the transport group |
| M15-6 | Nomenclature table declared five columns for four-cell rows | **CONFIRMED ERROR (typesetting)** | Repaired: four-column spec, notation de-collided |
| M15-4 | Quartic regrouping | **ALREADY CORRECT** | Verified again (new run, new wavenumbers) |
| M15-7 | Piezoelectric sign pair | **ALREADY CORRECT** (convention) | Checked block by block; recorded |
| M15-8 | Corner line force | **UNVERIFIED / unresolved** | Reported, not repaired |
| M15-9 | Strain and curvature amplitudes under the ansatz | **ALREADY CORRECT** | Independent finite-difference check (new seed set) |

## 2. M15-1 — the strain-gradient variation, derived

`η_ijk = ½(u_i,jk + u_j,ik)`, so

  δη_ijk = ½(δu_i,jk + δu_j,ik).                                              (1)

This is **not** `δu_i,jk`: the two terms differ by the antisymmetric part in
`(i,j)`. What is true is the contraction. Because `η_ijk = η_jik` by construction,
only the symmetric part of `∂w/∂η` is defined, and the hyperstress is symmetric in
its first two indices,

  τ_ijk = ½(∂w/∂η_ijk + ∂w/∂η_jik) = τ_jik .                                  (2)

Then

  τ_ijk δη_ijk = ½ τ_ijk δu_i,jk + ½ τ_ijk δu_j,ik
              = ½ τ_ijk δu_i,jk + ½ τ_lji δu_i,lk        (relabel i↔j, then j→l)
              = ½ τ_ijk δu_i,jk + ½ τ_jil δu_i,lk        (by (2))
              = τ_ijk δu_i,jk .                            (3)

**Numerical confirmation** (round 15, fresh random draw): component-wise deviation
`max|δη − δu| = 0.962`; contracted values `τ:δη = −0.450615573385995` and
`τ:δu = −0.450615573385994`, difference `3.3e-16`. The identity is a contraction
identity and nothing more.

**Propagation.** The two integrations by parts use (3), not (1). The resulting
volume term is `ρü_j = ∂_iσ_ij − ∂_i∂_kτ_jik` with the minus sign carried by the
two sign changes of the second integration by parts; the sign is unchanged from
round 13 and is now justified in the text rather than asserted.

## 3. M15-2 — the weak equations, separated

See `PAPER_A_ROUND15_COMPLETE_COUPLED_WEAK_FORM.md` for the derivation. The
manuscript now states, in order:

- (A) `∫[σ̂_ij ε̂*_ij(v) + τ̂_ijk η̂*_ijk(v)] = ω²∫ρ û_i v*_i` — mechanical balance;
- (B) `−∫D̂_i Ê*_i(ψ) − ∫N̂ψ* = 0` — Gauss's law with the mobile charge;
- (C) `∫[N̂Φ* − (iα_d/ω)∂_iμ̃∂_iΦ*] = 0` — time-harmonic carrier continuity.

Three statements that were previously one. In particular (C) is *not* the
enthalpy term `μ̃N*`: it is the flux balance divided by `−iωq`, and its natural
boundary term is the blocking condition.

**Is the solver doing (A)–(C)?** Yes, and this is checkable without trusting the
prose: the residual function of the solver contains the momentum, Gauss,
carrier-continuity, traction, double-traction and blocking residuals separately,
and all of them are below `10^{-8}` in the normalised measure at the modes used
(`fig:fig09(c)`, test suite). The carrier residual implemented is
`−iωN̂ − α_d ∂_i∂_iμ̃`, which is exactly (C) multiplied through by `iω`.

**The elimination.** `μ̃` is algebraic in `(Δn, φ, η)`, so carrying `μ̃` as the
unknown is exact. The temporal route solves the `W` rows for `μ̃` and the spatial
route carries it; both solve the same three equations. No approximation is
introduced by the elimination, and none is claimed.

## 4. M15-3 — the quartic, with the two vanishing blocks

From `Σ_{r,s}(−ik_x)^r(ik_x)^s A_rs`:

| power | coefficient | check |
| --- | --- | --- |
| k⁰ | `A₀₀` | `(−i)⁰(i)⁰ = 1` |
| k¹ | `i(A₀₁ − A₁₀)` | `(−i)⁰(i)¹ = i`, `(−i)¹(i)⁰ = −i` |
| k² | `A₁₁ − A₀₂ − A₂₀` | `(i)² = −1`, `(−i)(i) = +1`, `(−i)² = −1` |
| k³ | `i(A₁₂ − A₂₁)` | `(−i)(i)² = +i`, `(−i)²(i) = −i` |
| k⁴ | `A₂₂` | `(−i)²(i)² = +1` |

**Numerical identity check** (round 15): max |regrouped − direct assembly| =
`2.3e-13, 4.6e-13, 1.8e-12, 3.6e-12` at `k = 0.17, −0.53, 0.99, 2.40`, against
entries of order `1.4e6` — the regrouping is an identity.

**Block norms** at the operating point: `‖A₀₀‖ = 1.76e6`, `‖A₀₁‖ = ‖A₁₀‖ = 2.04e4`,
`‖A₁₁‖ = 2.20e3`, `‖A₁₂‖ = ‖A₂₁‖ = 1.33e1`, `‖A₂₂‖ = 9.55e-1`,
`‖A₀₂‖ = ‖A₂₀‖ = 0` **identically** — not small, zero: no field of the enthalpy
carries two derivatives in the propagation direction. With `ℓ = 0` (and `f = H = 0`)
`‖A₂₂‖ = ‖A₁₂‖ = 0` as well, which is why the classical limit is quadratic. The
manuscript now says both things.

**Symmetry.** `A₁₂ = A₂₁^H` (`1.7e-15`), `A₂₂ = A₂₂^H` (`8.1e-17`),
`A₀₁ = A₁₀^H` (`1.8e-12`). `A₀₀` and `A₁₁` are not Hermitian; their
non-Hermitian part is exactly the carrier-transport bilinear form `−(iα_d/ω)⟨·,·⟩`,
which is the loss. A Hermitian operator with loss confined to one bilinear form is
the correct structure for this problem, and it is now stated instead of being left
for the reader to discover.

## 5. M15-7 — the piezoelectric sign, examined and not charged

The paper's pair `σ = cε − eE`, `D = κE + eε` derives from `w ∋ −eEε`. The
assembled pair `+⟨G,e,B⟩` (in the potential row) and `+⟨B,eᵀ,G⟩` (in the
displacement row) is the *same* pair once the sign of the electric-field operator
is carried with the unknown: `G = −E` in the solver's convention, and the solver's
own strong-form residual uses `D₃ = e₃₁ε_xx + e₃₃ε_zz + …` with the paper's sign.
Row-wise the two conventions agree term by term, and the independent strong-form
propagator (no spectral matrices) reproduces the spectral frequencies to `1e-10`.
**No sign error is demonstrated, and none is claimed.** This is recorded as a
convention note, not as a repair: changing the sign would change physics.

## 6. M15-9 — amplitude relations, re-checked

Finite-difference evaluation of `u_i = û_i exp[i(k_xx + k_yy)]` (fresh random
`k_x, k_y, û`): the six strain amplitudes and two curvature amplitudes of
`eq:strain_amplitudes`–`eq:eta_amplitudes` agree to `≤ 7.4e-11` in absolute value
against exact values of order `0.1–0.9`. Unchanged from round 14, re-executed here
with a different seed set.

## 7. What remains unresolved

- **The corner line force (M15-8).** See the boundary audit. The weak form is
  imposed at the corner; the line-force density there is non-zero (`>1e-4`); the
  reported partitions do not rest on the energy it carries, but the strong
  boundary representation is not complete. This is a genuine limitation of the
  model as implemented, not a writing defect.
- **Closed-form block entries** are still not given as algebraic expressions in
  the material constants; the construction of `eq:block` is given instead, which
  is sufficient to regenerate every entry and is what the implementation does.
  A hand-derived entry list would have to be transcribed from the code and could
  disagree with it; the referee's rule is to state what is implemented.
- **No compiled page.** No TeX engine in this environment (checked again this
  round: `pdflatex`, `latexmk`, `xelatex`, `lualatex`, `tectonic` all absent).
  Static validation passes; typeset output is unverified here.

## 8. Executed in this round

| Check | Result |
| --- | --- |
| `unittest paper_a_study.test_model` | 52 tests, OK, 23.1 s |
| contraction identity (M15-1) | `3.3e-16` under contraction, `0.962` component-wise |
| quartic regrouping (M15-4) | `≤3.6e-12` absolute at four wavenumbers |
| block Hermiticity (M15-3) | `≤1.8e-12` on the three Hermitian pairs |
| amplitude relations (M15-9) | `≤7.4e-11` |
| `claim_audit.py` | PASS — 23 claims, 46 tokens, 5 deprecated guarded, figures 1–10 in order, 11/11 source rows |
| `mutation_tests.py` | PASS — every injected defect caught |
| `phase_speed_audit.py` | exit 0 |
| `scripts/static_check.py` | exit 0, no findings |
| LaTeX build | **not possible** in this environment |

The full clean-data battery was **not** re-run: no producer, solver, constant or
dataset changed this round. Figure producers changed (layout only), and the
figure-data agreement tests are part of the 52.
