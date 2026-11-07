# Paper A — Round 17 worked calculations

**Branch** `arena/ea7ca4dd-a-paper` · base `a68bb76` · BUILD UNVERIFIED (no TeX
engine available; nothing below is a claim about a rendered page).

Six worked chains are now in the paper, each following the pattern *general
expression → actual stored inputs → evaluated result → interpretation*. Every
input is either a material constant already in the manuscript or a value
recomputed this round from `paper_a_study/model.py`; nothing was rounded to hit a
target, and where a chain reproduces a printed number the reproduction is stated
as an identity, not as agreement.

---

## W1 — the five dimensionless groups from the material file

**In the paper:** `sec:governing_nondim`, `eq:cs_worked`, `eq:a_worked`,
`eq:LD_worked`, `eq:alphad_worked`, `eq:lam_worked`.

| step | expression | inputs | result |
|---|---|---|---|
| wave speed | `c_s = √(c₄₄/ρ)` | 43.0 GPa, 5.70×10³ kg m⁻³ | **2.7466 km s⁻¹** |
| frequency unit | `c_s/(2πd)` | `d` = 200 nm | **2.1857 GHz** |
| operating point | `ω = 7.6334 c_s/d` | — | **16.684 GHz** (abstract says 16.68) |
| compressibility | `a = k_BT/n₀` | 1.3806×10⁻²³, 301.72 K, 2.0×10¹⁸ m⁻³ | **2.0828×10⁻³⁹ J m³** |
| Debye length | `L_D = √(κ₃₃k_BT/(q²n₀))` | 8.85×10⁻¹¹ F m⁻¹, 1.6022×10⁻¹⁹ C | **2.6797 µm** |
| charge group | `Q = d/L_D` | — | **0.074635** (code: 0.074634887) |
| transport group | `α_d = D/(d c_s)` | 4.55×10⁻⁴ m² s⁻¹ | **0.8283** |
| gradient group | `λ = ℓ/d` | 50 nm / 200 nm | **0.25** |
| coupling group | `h = H/(d√(a c₄₄))` | `d√(a c₄₄)` = 1.8927×10⁻²¹ J m | `h = H/1.8927×10⁻²¹` |

**Interpretations attached in the text:** `d/L_D = 1/Q = 13.4`, so the plate is
fourteen Debye lengths thick and the carrier perturbation is not a surface layer;
`Q² = 5.57×10⁻³` multiplies the potential–potential block; `d²/D = 8.8×10⁻⁸ s`
against `2d/c_s = 1.5×10⁻⁷ s`, so carrier and elastic time scales are *not*
separated — the reason the carrier cannot be condensed out of the eigenproblem;
the tabulated extreme `|H| = 2.0×10⁻²³ J m` is `h = ±1.06×10⁻²`.

**Consistency:** `T = 301.72 K` is not an independent input; it is what the
Einstein relation gives for the `(D, μ_e)` pair used, and the paper says so in
`tab:groups` and again in `eq:a_worked`.

---

## W2 — the discrete operator: sizes and scaling

**In the paper:** `sec:numerics_basis`, `eq:nw`, `eq:block_norms`.

`n_w = 5n + 3` unknowns per element (18 at `n=3`, 93 at `n=18`, 153 at the highest
degree examined), quartic of degree `4n_w` in `k_x` (372 at `n=18`), `2n_w`
decaying roots. Block Frobenius norms at degree 4, `h=0`:

```
‖A₀₀‖ = 1.89e4   ‖A₀₁‖ = 5.67e2   ‖A₁₁‖ = 2.35e2   ‖A₁₂‖ = 4.04   ‖A₂₂‖ = 7.12e-1
```

Ratio largest/smallest = `2.7×10⁴`. **Interpretation:** the spread is not a
numerical accident — it is `λ²c₃₃/c₄₄ = 0.32` in the gradient term against the
`O(10²)` elastic term, multiplied by the `2j(j+1)(2j+1)` growth of the stiffness
matrix with mode number. Hence row equilibration before the eigenvalue problem,
and the conditioning quoted in the paper refers to the equilibrated problem.

---

## W3 — the reported share, assembled end to end

**In the paper:** `sec:numerics_edge` (`eq:RB_worked`, `eq:RB_prop`,
`eq:RB_planes`, `eq:RB_value`) and Appendix A.6 (`eq:app_RB`).

| quantity | stored input | value |
|---|---|---|
| raw modal power (unit amplitude) | `modal_flux_audit.json`, degree 18 | −0.0178923 |
| scattering amplitude | same row | 1.13749 → `|a|²` = 1.2938 |
| power at the edge | product | **−0.0231505** |
| backward attenuation | `Im k_Bx` (per unit d) | −5.2306×10⁻⁶ |
| incident attenuation | `Im k_ix` | +5.4027×10⁻⁶ |
| reference distance | `L = 10 d` | 2 µm |
| power at `x=−L` | ×`e^{2Im k_B L}` = 0.9998954 | **−0.0231481** |
| incident at `x=−L` | `e^{2Im k_i L}` = 1.0001081 | 1.0001081 |
| **share** | ratio | **0.0231456 = 2.31 %** |

Stored `R_B` for that row is 0.023145607570647334, so the chain reproduces it to
all digits shown. **Interpretation:** the two exponentials move the fourth digit
in opposite directions (product departs from unity by 1.05×10⁻⁴); reporting the
share without the plane at which it was taken is ambiguous at that digit. The
branch maximum (0.9468 = 94.68 %) is evaluated the same way; the factor of forty
between the two is the subject of `sec:results_peak`.

**A first version of this chain applied the exponentials twice** (to a power
already evaluated at the plane) and gave 0.0231407. That was caught by comparing
with the stored `R_B` and corrected; the wrong version is recorded here because a
supervisor re-deriving the number should know the trap.

---

## W4 — degree-invariance of the physical power (the normalisation test)

**In the paper:** Appendix A.5, `eq:app_power_numbers`.

| degree | raw `𝒫_x` | `|a|` | `|a|²𝒫_x e^{2Im k L}` |
|---|---|---|---|
| 18 | −0.0178923 | 1.13749 | **−0.0231481** |
| 22 | −0.0154248 | 1.22510 | **−0.0231481** |
| 26 | −0.0132455 | 1.32205 | **−0.0231481** |
| 30 | −0.0113777 | 1.42644 | **−0.0231481** |

**Interpretation:** the raw modal power changes by 57 % across the four degrees
and the physical power does not change at all in the digits shown. That is the
statement that the eigenvector normalisation is applied correctly, and it is why
`tab:refinement` reports a degree spread of 7.2×10⁻⁷ rather than a drifting
value.

---

## W5 — the five matrix elements of Appendix A.2

| entry | expression | evaluation |
|---|---|---|
| compressibility | `−∫b_ib_j` | `−1` (mass matrix is the identity) |
| transport | `−(iα_d/ω)[(k_x²+k_y²)δ_ij + S_ij]` | `−i·1.80×10⁻³` (j=0); `−i·1.304`, `−i·6.512`, `−i·18.23` (j=1,2,3) |
| carrier–potential | `−Q(δ_ij − r_jδ_{i,j+2})` | `−0.074635` diag; `−0.033378` sub-diag (`Qr₀ = 0.074635×0.4472`) |
| gradient stiffness | `λ²(c₃₃/c₄₄)S_jj` | `0.0625×5.14×12 = 3.86` (i=j=1) |
| inertia | `−ω²δ_ij` | `−58.27` |

**Interpretation:** transport grows with mode number because the gradient energy
of a higher Legendre mode is larger — the discrete statement that diffusion
penalises thickness structure; the inertia/gradient-stiffness ratio
`58.27/3.86 = 15.1` sets the frequency of the first thickness mode of the
gradient operator.

---

## W6 — the coupling entry and why five profiles coincide

**In the paper:** `sec:results_boundary`, `eq:H_entry` (new equation in the
results section).

The coupling enters the two off-diagonal blocks as
`(A_uμ)_ij = h∫b_i''ψ_j dζ`. Evaluated by independent Gauss quadrature at degree
six, the matrix rows are

```
0, 0, 26.83, 91.65, 187.8, 315.9      (upper triangular)
```

so the coupling grows with mode number exactly as the second derivative does.
With `h = ±1.06×10⁻²` the largest entry is **3.35**, against an inertia entry of
58.3 and a compressibility entry of 1 **in the same row**. **Interpretation:** a
few per cent of the diagonal — enough to move the partition measurably
(`fig07`), not enough to change a normalised flux profile by more than the
0.9 % of peak stated in `fig08`. The two figures are consistent rather than
contradictory, and the paper says so in those words.

---

## What these calculations do *not* establish

* They do not validate the physics against measurement; the parameters
  `ℓ, f, H` remain synthetic and the synthesis is stated in `tab:provenance`.
* They do not replace the independent checks (exact SH limits, strong-form
  propagator, `C¹` finite elements); they are arithmetic on the same model.
* No number here was produced by fitting, smoothing or interpolation.
