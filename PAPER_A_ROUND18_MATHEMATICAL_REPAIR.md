# Paper A — Round 18, Parts B–I: the mathematical repair

**Branch** `arena/ea7ca4dd-a-paper` · **BUILD UNVERIFIED** (no TeX engine here).
Companion files: `PAPER_A_ROUND18_PRE_EDIT_AUDIT.md` (what was wrong and where),
`PAPER_A_ROUND18_INDEPENDENT_RECHECK.md` (the second, solver-free script),
`PAPER_A_ROUND18_CORRECTNESS_VERDICTS.md`.

Every number below is produced by one of two scripts and is reproducible:

```
PYTHONPATH=. python paper_a_study/round18_mathematical_audit.py   # 43 checks, exit 0
PYTHONPATH=. python paper_a_study/round18_reference_checks.py     # 59 checks, exit 0
PYTHONPATH=. python paper_a_study/test_model.py                   # 52 tests, OK
```

---

## B. Legendre normalisation and the integration measure

Three coordinates now coexist in the manuscript without ambiguity, and the
appendix says which integral is taken in which:

| coordinate | interval | measure | Gram matrix |
|---|---|---|---|
| `z` | `[−d/2, d/2]` | `dz` | — |
| `ζ = 2z/d` | `[−1, 1]` | `dζ = 2dz/d` | `∫b_i b_j dζ = 2δ_ij` |
| `s = z/d = ζ/2` | `[−1/2, 1/2]` | `ds = dz/d = dζ/2` | `∫b_i b_j ds = δ_ij` |

`b_j(s) = √(2j+1) P_j(2s)`.  The chain is one line,

```
∫_{-1/2}^{1/2} b_i b_j ds = ½ (2j+1) ∫_{-1}^{1} P_i P_j dζ = ½ (2j+1) · 2δ_ij/(2j+1) = δ_ij,
```

with `½` the Jacobian of `s = ζ/2` and `2/(2j+1)` the Legendre normalisation.
The solver is written in `s` (`model.py`: `self.z, self.weights = leggauss(...);
self.z /= 2; self.weights /= 2`), so the identity mass is the `s`-statement and
the factor 2 is the `ζ`-statement.  Both are now printed, with the Jacobian named
(`eq:app_measures`, `eq:app_mass`), because writing the identity in the `ζ`
measure — which is what round 17 did — halves every scalar in §A.2.

**Evidence (independent 301-node rule, tol 1e-13):**

| N | `max abs(M − I)` in `ds` | `max abs(M − 2I)` in `dζ` |
|---|---|---|
| 5 | 8.2e-14 | 7.9e-14 |
| 6 | 1.1e-13 | 9.4e-14 |
| 7 | 1.3e-13 | 1.1e-13 |

and the solver's own mass matrix agrees with the identity to `1.4e-13`.

## C. Stiffness matrix, element by element, against the implementation

`S_ij = ∫ b_i' b_j' ds`, `b_j'(s) = 2√(2j+1)P_j'(2s)`.  Diagonal:

```
S_jj = 4(2j+1) ∫_{-1/2}^{1/2} (P_j'(2s))² ds = 2(2j+1) ∫_{-1}^{1}(P_j')²dζ = 2(2j+1)j(j+1).
```

Off-diagonal (`eq:app_S_off`): `S_ij = 2√((2i+1)(2j+1))∫P_i'P_j'dζ`, non-zero only
for `i+j` even, which is the two-band structure.

**At N = 6** (three routes: closed form, the independent 301-node rule, and the
production 64-node rule):

| | j=0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| i=0 | 0 | 0 | 0 | 0 | 0 | 0 |
| i=1 | 0 | **12** | 0 | 18.330 | 0 | 22.978 |
| i=2 | 0 | 0 | **60** | 0 | 80.498 | 0 |
| i=3 | 0 | 18.330 | 0 | **168** | 0 | 210.599 |
| i=4 | 0 | 0 | 80.498 | 0 | **360** | 0 |
| i=5 | 0 | 22.978 | 0 | 210.599 | 0 | **660** |

* diagonal against `2j(j+1)(2j+1)`: `max|err| = 3.8e-12, 1.0e-11, 2.2e-11` at
  `N = 5, 6, 7` (relative `≤ 2e-14`);
* independent rule against the solver: `3.5e-11, 1.0e-10, 2.4e-10` (absolute,
  relative `≤ 2e-13`);
* printed matrix against the computed one: `4.9e-5` absolute, i.e. the five-digit
  rounding of the print (relative `2e-7`);
* parity-violating entries (`i+j` odd): `≤ 4.6e-15`;
* the model's quadrature is `max(64, 2p+10)` nodes; the audit uses 301 and the
  reference script 40/60, so "independent quadrature order" holds in the sense
  required (a rule the production path does not use), and the manuscript's claim
  that refining 64 → 256 nodes changes no digit is a separate, pre-existing
  statement in `app:repro`.

The weighted identity `∫(1−ζ²)P_j'P_k' dζ = 2j(j+1)/(2j+1) δ_jk` is now labelled as
what it is (`eq:app_S_weighted`) and is *not* used as if it were `S_jj`.

## D. Carrier–potential index orientation

`ψ_j(s) = b_j − r_j b_{j+2}`, `r_j = √((2j+1)/(2j+5))`, `j = 0…N−3`; `ψ_j(±½) = 0`
to `8.9e-16` because `P_j(±1) = (∓1)^j` and `r_j` is exactly the cancellation
ratio.

| matrix | shape | entries | error |
|---|---|---|---|
| `(ψ_i, b_j)` | `n_φ × N` | `δ_ij − r_i δ_{j,i+2}` (band **above**, row index) | 1.1e-14 |
| `(b_i, ψ_j)` | `N × n_φ` | `δ_ij − r_j δ_{i,j+2}` (band **below**, column index) | 5.8e-15 |

The solver's charge matrix is the first.  Using `r_j` in place of `r_i` changes
the largest entry by **0.2981**; using the transposed matrix in the potential row
changes the block structure entirely.  The manuscript now prints both, names
which block carries which (`−C` in the potential row, `−Cᵀ` in the carrier row,
`eq:app_charge`, `eq:app_charge_T`), and the assembled block reproduces the
printed `A_{φμ}` to `8.7e-16`.

The dielectric matrix `eq:app_diel`
`κ33∫ψ_i'ψ_j' + κ11k_y²∫ψ_iψ_j` is written with the banded expansion
`S_ij − r_jS_{i,j+2} − r_iS_{i+2,j} + r_ir_jS_{i+2,j+2}`, sym- metric in the two
mixed terms, and the text says that the grounded basis removes a band of the
stiffness exactly as it removes a band of the mass.

## E. Worked transport arithmetic, `j = 0…3`

`A00|_{transport} = (−iα_d/ω)(k_y²δ_ij + S_ij)`, `A11|_{transport} = (−iα_d/ω)δ_ij`,
`α_d/ω = 0.828294/7.6334 = 0.108512`, `k_y² = 0.1298² = 0.016848`:

| j | `S_jj` | `k_y² + S_jj` | `(α_d/ω)(k_y²+S_jj)` | printed as | assembled `A00` diagonal |
|---|---|---|---|---|---|
| 0 | 0 | 0.016848 | 0.0018283 | `−i1.828e-3` | `−i1.828e-3` |
| 1 | 12 | 12.016848 | 1.303938 | `−i1.3039` | `−i1.303939` |
| 2 | 60 | 60.016848 | 6.512373 | `−i6.5124` | `−i6.512380` |
| 3 | 168 | 168.016848 | 18.231373 | `−i18.2314` | `−i18.231375` |
| 4 | 360 | 360.016848 | 39.065066 | (not printed) | `−i39.065142` |

`A11` diagonal `= −i0.108509`; with `k_x² = 0.541990` the two blocks reproduce
`(α_d/ω)(k_x² + k_y² + S_jj)` to `3.6e-15` (absolute) — that is the check that
fails if `k_x²` is put in `A00`, which is exactly the round-17 error (it would
have given `−i0.0607` for the first entry, 33× too large).

Charge block, same section: `(A00)_{φ_iμ_j} = −Q(δ_ij − r_iδ_{j,i+2})`, diagonal
`−Q = −0.074635`, band `+Qr_i = +0.033378, +0.048860, +0.055630, +0.059538`
(relative error `4.4e-7` against the closed form; `Qr₀ = Q/√5`), identical to the
solver at `8.7e-16`.

## F. Debye-length ratio: every site in the project

`Q = d/L_D = 0.074635`, `L_D/d = 1/Q = 13.3986`, `L_D = 2.6797 µm`,
`d = 200 nm`.  The plate is 7.5 % of a Debye length thick; the Debye length is
13.4 thicknesses.

| file | site | round-17 wording | verdict | round-18 state |
|---|---|---|---|---|
| `sections/governing_equations.tex` | 880–881 | "fourteen Debye lengths thin in the ratio d/L_D = 1/Q" | **reversed** | rewritten: `L_D/d = 1/Q = 13.40` |
| `sections/governing_equations.tex` | 553–555 | "`d/L_D = 0.075`: much thinner than the Debye length" | correct | kept |
| `sections/governing_equations.tex` | 839 | table row `Q`, `d/L_D`, `7.46e-2` | correct | kept |
| `sections/governing_equations.tex` | 954 | "`d/L_D = 0.075`, perturbation not confined to a surface" | correct | kept |
| `sections/discussion.tex` | 121 | "`Q = d/L_D = 0.075` places the plate inside that window" | correct | kept |
| `sections/results.tex` | 134 | "`Q = d/L_D = 0.075 < 1`: thinner than the Debye length" | correct | kept |
| `sections/numerical_methods.tex` | 76 | "`Q = d/L_D` the dimensionless charge" | correct | kept |
| `sections/governing_equations.tex` | 870–878 | `L_D` and `Q` derivation from `κ33`, `k_BT`, `q²n₀` | correct (recomputed `2.679712 µm`) | kept |
| `PAPER_A_ROUND17_WORKED_CALCULATIONS.md` | 33 | "`d/L_D = 1/Q = 13.4` … fourteen Debye lengths thick" | **reversed twice** | erratum note added in place |
| `PAPER_A_ROUND16_*.md` | 141 / 69 | "off by `1/Q = 13.4`" (a factor, not a ratio) | correct | kept |

Only one manuscript site was wrong, and it was wrong twice (the ratio and the
size statement built on it).  The nine correct sites were left untouched, which
is the point of the sweep: the repair is localised to the site that inverted the
ratio, and the round-17 report carries a dated erratum rather than a silent edit.

## G. Degree, basis and degree-of-freedom accounting

`N = n+1` basis functions per field, `n_u = 3N`, `n_φ = N−2` (grounded) / `N−1`
(open circuit), `n_μ = N`:

| degree `n` | `N` | `n_w` grounded | `n_w` open | `= 5n+3` | `= 5n+4` | quartic degree `4n_w` | decaying roots `2n_w` |
|---|---|---|---|---|---|---|---|
| 4 | 5 | 23 | 24 | 23 | 24 | 92 | 46 |
| 5 | 6 | 28 | 29 | 28 | 29 | 112 | 56 |
| 18 | 19 | 93 | 94 | 93 | 94 | 372 | 186 |
| **22** | **23** | **113** | **114** | **113** | **114** | **452** | **226** |
| 30 | 31 | 153 | 154 | 153 | 154 | 612 | 306 |

Each row is checked against the solver (`Plate(...).nw`), not against the
formula.  The reported results are at `n = 22` (confirmed by
`figure_data/peak_search.json`, rows `degree = 22`), so the operational sizes in
the text are 113 unknowns, quartic degree 452, 226 decaying roots.  `93` and
`372` are the `n = 18` values and are now attributed to that degree.

State operator `4n_w × 4n_w = 76 × 76` at `p = 4`; boundary vector length
`2n_u + n_φ + n_μ = 38`; edge operator `m × M = 38 × 23` at `p = 4` and
`150 × 93` at `p = 18`, square (`23 × 23`) only at `ℓ = 0`.

## H. Inertia against stiffness: what the ratio may and may not be used for

`−ω²δ_ij = −58.27δ_ij` and the `j = 1` gradient entry is `λ²(c33/c44)S_11 = 3.85`;
ratio `15.1`.  Round 17 read this as the thickness-mode frequency scale.  It is
not one: the thickness-mode frequency is an eigenvalue of the coupled quartic
`eq:quartic`, and no such eigenvalue is computed or quoted anywhere in the paper.
The repaired text (`eq:app_w5`) states the two entries, the ratio, and then says
that the ratio compares two matrix entries at one fixed frequency and nothing
more.  The same discipline is applied to the coupling block in Results §"the
coincidence of the five profiles", where the entry `h·580.5 = 6.13` is compared
with `ω² = 58.27` and with `2.16×10⁵` and the text says explicitly that the
operator is row-equilibrated before solution, so no entry ratio is a frequency.

## I. Equation-by-equation audit

### I.1 Appendix A (`sections/appendix_derivations.tex`)

| label | claim | check | result |
|---|---|---|---|
| `eq:app_measures` | `s = z/d`, `ds = dζ/2` | definition; sampler `z/2` | ok |
| `eq:app_mass` | `∫b_i b_j ds = δ_ij` | 3 degrees × 2 measures | 8.2e-14 … 1.3e-13 |
| `eq:app_S` | `S_jj = 2j(j+1)(2j+1)` | closed form vs quadrature | 3.8e-12 … 2.2e-11 |
| `eq:app_S_weighted` | weighted orthogonality `2j(j+1)/(2j+1)` | quadrature with weight | ok (labelled, not used for `S_jj`) |
| `eq:app_S_off` | `2√((2i+1)(2j+1))∫P_i'P_j'` | quadrature | 2e-13 relative |
| `eq:app_S_matrix` | `N = 6` matrix | three routes | 4.9e-5 (print rounding) |
| `eq:app_pot` | `ψ_j = b_j − r_jb_{j+2}`, `ψ_j(±½)=0` | direct evaluation | 8.9e-16 |
| `eq:app_charge` | `(ψ_i,b_j) = δ − r_iδ_{j,i+2}` | quadrature + solver | 1.1e-14 / 1.2e-14 |
| `eq:app_charge_T` | `(b_i,ψ_j) = δ − r_jδ_{i,j+2}` | quadrature | 5.8e-15 |
| `eq:app_diel` | banded dielectric matrix | derived from `S` bands; assembled block | ok |
| `eq:app_w1` | `−δ_ij`, `(A00)_{μ0μ0} = −1` | solver | 6.8e-15 |
| `eq:app_w2`, `eq:app_w2_values` | transport in `A00`/`A11` | solver, both blocks | 3.6e-15 |
| `eq:app_w3` | `−Q(δ − r_iδ_{j,i+2})` | solver | 8.7e-16 |
| `eq:app_w4` | `3.85, 19.27, 54.00, 115.64` | closed form | 8.8e-4 |
| `eq:app_w5` | `−58.27`, ratio `15.1` | definition | 1e-3 |
| `eq:app_block` | eight bilinear forms, `ds` measure | matches solver assembly | ok |
| `eq:app_edge`, `eq:app_edge_R` | `m = 2n_u+n_φ+n_μ`, `38 × 23` | built at `p = 4, 18`, `ℓ = 0` | ok |
| A.5 normalisation | `R_B` decomposition | chain recomputed | 4.2e-15 |
| A.6 chain | `1.1374909²(−0.0178923)…` | independent arithmetic | 3.7e-18 relative |

### I.2 Round-17 additions in the four main sections

| file | equation / claim | verdict |
|---|---|---|
| `governing_equations.tex` | `eq:sigmaZnO` (six components) | correct, 1e-15 … 2.3e-13 |
| | `eq:tauZnO` (`τ_zzz`, `−fE_z + HΔn`) | correct by inspection; `f`/`H` terms exercised by edge + dissipation tests |
| | `eq:DZnO` (three components) | correct, 8.9e-16 … 2.8e-14 |
| | `eq:contraction`, `eq:ibp_stress`, `eq:ibp_hyper` | correct (standard; signs consistent with `eq:momentum`) |
| | `eq:momentum`, `eq:effective` | correct |
| | `eq:momentum_expanded` | correct; matches `S = σ − ik_xτ⁰ − ik_yτ¹ − ∂_zτ²` |
| | `eq:Hterm` | correct (`−fE_z = +fφ'`, so `∂_z²(fφ' + HΔn)`) |
| | `eq:gauss`, `eq:gauss_expanded` | correct; divergence reproduced by the component checks |
| | `eq:continuity`, `eq:carrier_strong`, `eq:current` | correct; sign convention consistent with `+iα_d/ω` in the weak form |
| | `eq:sector_blocks` | correct (`A_{φμ} = −Q⟨ψ,b⟩`) |
| | `eq:coeffs` | correct; `A02 = A20 = 0` exactly, `A4 = A22` |
| `numerical_methods.tex` | `eq:block` | measure corrected to `ds` |
| | `eq:polynomial`, `eq:quartic` | correct; degree `4n_w` |
| | `A22 = A12 = 0` claim | **corrected**: `A12, A21, A22 ∝ ℓ²`, `A02 = A20 = 0` always |
| | `eq:nw` | **corrected**: `N = n+1`, `5n+3` / `5n+4`, 113 at the reported degree |
| | `eq:block_norms` | correct; five norms recomputed (`1.888e4, 567.0, 235.0, 4.04, 0.7115`) |
| `results.tex` | `eq:H_entry` and the coupling paragraph | **corrected**: carrier basis, `ds`, lower triangular, row norms `0,0,26.83,91.65,222.89,450.87,809.44`, largest entry 580.5, `h·580.5 = 6.13` |
| `discussion.tex` | `Q = d/L_D = 0.075` and the scale-separation paragraph | correct, kept |

## Summary of the edit footprint

| file | lines changed | nature |
|---|---|---|
| `sections/appendix_derivations.tex` | §A.1 rewritten, §A.2 rewritten, §A.3 measure, §A.4 rewritten | measures, indices, arithmetic, edge shape |
| `sections/numerical_methods.tex` | 6 edits | measure, `ℓ²` blocks, DOF accounting |
| `sections/governing_equations.tex` | 2 edits | Debye ratio, a stutter |
| `sections/results.tex` | 1 paragraph | coupling matrix |
| `paper_a_study/*.py` | 2 new audit scripts | evidence, no solver change |

No material constant, no solver line, no dataset, no figure and no reported
number was touched; `git diff --stat` shows only `.tex` files and the static
validation record.
