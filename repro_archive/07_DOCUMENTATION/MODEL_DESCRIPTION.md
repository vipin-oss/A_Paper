# MODEL_DESCRIPTION

Everything in this file is a statement about the model actually executed by
`01_PROGRAM/paper_a_study/model.py`.  Where the model differs from a fuller theory,
the difference is named.  No parameter in this document is invented: each one points
to the file that stores it.

---

## 1. Geometry, kinematics, and what is discretised

* A transversely isotropic (**6mm**) n-type ZnO plate of thickness `d`, faces at
  `z = ±d/2`, occupying the half-space `x < 0`, terminating in a **traction-free,
  charge-free edge at `x = 0`**, unbounded in `y`.
* Every field has the form `f(x,z) e^{i k_y y − i ω t}`, so a single tangential
  wavenumber `k_y` is conserved; **three displacement components are retained**.
  The formulation is therefore *two-and-a-half-dimensional* (2.5D): a discrete
  cross-section `(x,z)`, full 3-component kinematics, no discretisation of `y`.
* Fields: displacement `u_i(x,t)`, electrostatic potential `φ(x,t)`, electron-number
  perturbation `Δn(x,t)` measured from uniform doping `n_0`.  The polar `c` axis is
  `x_3 ≡ z`.  Latin indices 1,2,3; `,k` denotes a spatial derivative.
* Conventions fixed once: `E_i = −∂_i φ`; electron charge `−q`, `q > 0`;
  `μ̃` is the electrochemical potential **per carrier, in joules** (so each term in it
  is an energy, none is a dimensionless ratio).

Source: `02_OVERLEAF/sections/governing_equations.tex` §"Geometry, kinematics and the
gradient energy"; code `Plate.matrices`, `Plate.basis` in `01_PROGRAM/paper_a_study/model.py`.

## 2. Strain, strain gradient, gradient energy

```
ε_ij  = ½ (u_i,j + u_j,i)                     dimensionless
η_ijk ≡ ε_ij,k = ½ (u_i,jk + u_j,ik)          m^-1, symmetric in (i,j)
w_g   = ½ A_ijklmn η_ijk η_lmn = ½ ℓ² c_ijlm η_ijk η_lmk ,   A_ijklmn = ℓ² c_ijlm δ_kn
```

The **third and sixth slots** of `A` are the gradient directions.  This is the only
contraction for which the energy depends on the gradient of the strain through
`c_ijlm η_ijk η_lmk`; any other contraction breaks the major symmetry
`A_ijklmn = A_lmnijk` that a second derivative of an energy must have.  The two
candidate contractions are numerically distinguishable: the fundamental SH branch
below is reproduced to `2e-13` with the correct contraction and missed by a residual
of `3e6` with the alternative (`02_OVERLEAF/sections/numerical_methods.tex`,
`01_PROGRAM/paper_a_study/test_model.py::test_gradient_exact_fundamental_SH`).

The single-length (isotropic-gradient) form is used.  A general
`A_ijklmn = ℓ² c_ijlm δ_kn` with one length is assumed; **no statement in the paper
depends on a multi-length gradient theory**, and no multi-length constants are
claimed.

## 3. Enthalpy and the four constitutive relations

The enthalpy is the classical flexoelectric piezoelectric-semiconductor enthalpy plus
**one bilinear term**,

```
ΔH = Δn H_jkl ε_jk,l                    (H_jkl : energy × length = J·m)
```

so that the two conjugates follow by differentiation and carry no independent
constant:

```
σ_ij = ∂w/∂ε_ij = c_ijkl ε_kl − e_kij E_k + H_ijk Δn
τ_ijk = ∂w/∂η_ijk = A_ijklmn η_lmn + H_ijk Δn − f_lijk E_l ,   τ_ijk = τ_jik
D_i = −∂w/∂E_i = κ_ij E_j + e_ijk ε_jk + f_ijkl η_jkl
μ̃  = ∂w/∂Δn  = a Δn − q φ + H_jkl η_jkl ,        a = k_B T / n_0
```

Maxwell reciprocity of the two couplings (`η↔Δn` through `H`, `η↔E` through `f`) is
what the discrete operator is tested against at `±k_y` to `1e-13`
(`test_reciprocity_at_oblique_wavenumber`).

**Executed specialisation (important):** one flexoelectric component is retained,
`f ≡ f_3zz`, giving `D_z = e_zjk ε_jk + κ_zz E_z + f η_zzz` and
`τ_zzz = A_zzz lmn η_lmn − f E_z`.  **Not** included: the surface flexoelectric
effect, electric-field-gradient (higher-order) flexoelectricity, and any
multi-component flexoelectric tensor.  `f = 1e-9 C/m` is a **placeholder magnitude**
(see §7 and `a0/materials.json`, which lists it as `NOT_SOURCED`).

## 4. Balance laws

```
σ_ij,j − τ_ijk,jk + f_i = ρ ü_i              (mechanical, τ enters by double divergence)
D_i,i = −q Δn                                 (Gauss)
Δṅ = (μ_e / q) ∇·( n ∇μ̃ ) ≈ D ∇²Δn ...       (carrier continuity, linearised)
```

The double divergence `∂_i ∂_k τ_jik` is a force density — which is why `τ` is a
force per unit length (`N·m^-1`) and `A` a force (`N`).  Units of every quantity are
derived from one derivative of an energy in
`02_OVERLEAF/sections/governing_equations.tex`; the three easy-to-mis-state ones are
`A = N`, `τ = N/m`, `H = J·m`.

## 5. Boundary and initial conditions

| Boundary | Mechanical | Electric | Carrier |
|---|---|---|---|
| Faces `z = ±d/2` | traction-free and hyper-traction-free (natural) | `φ = 0` (**grounded**, default) or `D_z = 0` (**open**, with the constant mode removed) | blocking: normal carrier flux zero (natural) |
| Edge `x = 0` | traction-free, hyper-traction-free | **insulating**: `D_x(0,z) = 0` (natural) — the production default; `ground` (`φ(0,z)=0`) is retained only to reproduce the round-19 baseline | blocking |
| `x → −∞` | radiation/outgoing | decaying or outgoing | decaying or outgoing |

The **insulating edge is the model of record**.  The grounded edge is a *different
boundary-value problem*; it is selectable (`Plate(edge_electric='ground')`) solely so
that the round-19 baseline is exactly reproducible.  The shift between the two is
quantified in `06_VALIDATION/reports/PAPER_A_ROUND20_ELECTRICAL_EDGE_CONDITION_AUDIT.md`.

Time dependence is harmonic (`e^{−iωt}`), so no separate initial condition is
imposed: the problem solved is a **time-harmonic scattering problem at fixed real
frequency**, and "initial condition" is not part of the model.  For the transient
consistency check (Fig. 9a) the temporal route integrates the same system with the
same constitutive law; no initial-value problem is set.

## 6. Non-dimensionalisation

Lengths `÷ d`; stresses `÷ c_44`; time `÷ d/c_s` with `c_s = √(c_44/ρ)`; carrier
densities `÷ n_0`; energies per carrier `÷ k_B T`; potential `÷` the scale that makes
the electrostatic term `−q Δn φ` consistent; frequency `÷ c_s/d` (figures report
cycles via `c_s/(2πd)`).  Derived scales:

```
a  = k_B T / n_0                        (compressibility, J·m³)
L_D = √(κ33 k_B T / (q² n_0))            (Debye length, m)
```

Five dimensionless numbers govern the model (`02_OVERLEAF` Table `tab:groups`):

| Group | Definition | Value at the operating point |
|---|---|---|
| `Q` | `d / L_D` | 7.46e-2 |
| `α_d` | `D / (d c_s)` | 8.28e-1 |
| `λ` | `ℓ / d` | 2.50e-1 |
| `f` | `f_3zz / (d √(c_44 κ33))` | 2.56e-3 |
| `h` | `H / (d √(a c_44))` | `η × 2.12e-1` |

Worked arithmetic (from the manuscript, reproduced by the code):
`c_s = √(43.0 GPa / 5700 kg m⁻³) = 2746.6 m/s`; frequency unit
`c_s/(2πd) = 2.1857 GHz` at `d = 200 nm`; operating `ω = 7.6334 c_s/d` ⇒
`f = 16.684 GHz`; `a = 2.0828e-39 J·m³` at `T = 301.72 K`, where `T` is **not an
independent input** — it is the temperature implied by the Einstein relation for the
`(D, μ_e)` pair used, `T = qD/(μ_e k_B)`.

Normalised wavenumbers used everywhere: `K = k_x d`, `KY = k_y d`, `Ω = ω d/c_s`.
Operating values `K0 = 0.7361990195318475`, `KB0 = 0.2451746921716515`,
`KY0 = 0.12981175031447484`, `Ω0 = 7.633372404423294` are frozen in
`01_PROGRAM/paper_a_study/reference_constants.json` and guarded by
`test_reference_values_are_frozen`.

## 7. Parameters, their values, and their provenance

All values live in `01_PROGRAM/a0/materials.json` (material/transport) and
`01_PROGRAM/paper_a_study/reference_constants.json` (frozen derived values); the code
reads the former at import time.  The full machine-readable inventory, with a
`source` field per entry, is `09_ARCHIVE_METADATA/parameter_manifest.json`.

| Parameter | Symbol | Value (SI) | Source field |
|---|---|---|---|
| Elastic stiffnesses | `c11, c33, c12, c13, c44` | 210, 221, 121, 105, 43 GPa | literature band for bulk ZnO; source: `materials.json` → `SI`, DOI `10.1007/s10483-025-3272-7` for the ZnO material set |
| Piezoelectric constants | `e33, e31, e15` | 1.32, −0.57, −0.48 C/m² | same |
| Permittivity | `κ33` | 8.85e-11 F/m (κ33/ε0 = 10) | same |
| Mass density | `ρ` | 5700 kg/m³ | same |
| Doping | `n0` | 2e18 m⁻³ | **NOT_SOURCED** (chosen design value) |
| Electron mobility | `μ_e` | 0.0175 m²/V/s | **NOT_SOURCED** |
| Diffusivity | `D` | 4.55e-4 m²/s | **NOT_SOURCED**; note `D/μ_e = 0.026 V` ⇒ `T = 301.72 K` |
| Thickness | `d` | 200 nm | **NOT_SOURCED** (design choice) |
| Gradient length | `ℓ` | 50 nm | **NOT_SOURCED** |
| Flexoelectric constant | `f_3zz` | 1e-9 C/m | **NOT_SOURCED** (placeholder magnitude; measured influence −0.012 % at 1 nC/m, −1.176 % at 10 nC/m, `03_DATA/figure_data/flexo_control.json`) |
| Carrier–gradient coupling | `H` | production `H = 0`; sweeps at `H = η H_crit`, `η ∈ {−0.05, −0.025, 0, 0.025, 0.05}` | **NOT_SOURCED** |
| Schur bound | `H_bound` | 8.9660137e-22 J·m | derived: `s = H² (c⁻¹)_33 /(ℓ² a) < 1` with `(c⁻¹)_33 = 1/c*`, `c* = c33 − 2c13²/(c11+c12) = 154.4 GPa` |
| Plot normalisation | `H*` (`HCRIT` in code) | 4.0097064373759543e-22 J·m | `H_bound/√5` (the value at which `s = 0.2`); swept range `|H/H*| ≤ 0.05` ⇒ `|H| ≤ 2.0e-23 J·m`, `s ≤ 5e-4` |
| Temperature | `T` | 301.72 K | derived from the Einstein relation, as above |
| Reference plane | `L` | `10 d = 2 µm` | modelling choice (`REF_NORM = 10.0`) |

**No experimental measurement of `f` or `H` for this structure exists in this
archive**, and the manuscript says so.  The sweeps around `H = 0` are what make the
reported `R_B` interpretable without a sourced `H`.

## 8. Why the calculation is well posed (what is actually proved)

* The enthalpy is positive definite for `H` inside the strict 3D Schur bound
  `s = H² (c⁻¹)_33/(ℓ² a) < 1`, i.e. `|H| < H_bound = ℓ√(a c*)`; `Plate.__init__`
  **raises** outside it (`self.schur >= 1`).  Every reported calculation has
  `s ≤ 5e-4`.  This is an
  algebraic condition on constants, checked at construction, and the code refuses a
  violating `H` rather than regularising it.
* Mode classification (outgoing vs incoming) uses decay **and** axial power with a
  cut-off `τ = 2e-8 max(1,|k_x|)`; the count of outgoing roots must equal the number
  of edge conditions — a structural property, not a tolerance.
* The edge system is square (`182×182` at `n = 22`), row/column scaled, solved by SVD
  with the rank required to equal the column count at a `1e-12` relative cut-off; a
  deficient system raises `RuntimeError('rank deficiency')` instead of being
  regularised (`test_singular_edge_system_is_rejected`).
* Positive-definiteness/energy balance of each computed mode is checked by
  `temporal_energy_balance` to `5e-6` relative in the tests.

## 9. What the model deliberately leaves out

Named here so that no reader assumes more than was solved: surface elasticity,
surface flexoelectricity, electric-field-gradient flexoelectricity, a full
third-order flexoelectric tensor, doping gradients, non-blocking (ohmic) carrier
boundaries, thermal coupling and temperature gradients, finite-strain kinematics,
and anisotropy of the gradient length.  Each omission is a modelling choice, not an
unexamined assumption; the manuscript's limitations paragraph lists the ones that
affect the reported number.
