# Paper A — Round 18, Part J: the independent numerical reference

**Script:** `paper_a_study/round18_reference_checks.py` · **exit status 0** ·
59 checks, `RESULT: every printed number reproduced independently`.

## What "independent" means here

The script

1. **imports nothing from `paper_a_study.model`** — not the model, not the
   material dictionary, not the basis, not the quadrature;
2. types every material constant in by hand from the manuscript table
   (`c11, c12, c13, c33, c44, e31, e33, e15, κ11, κ33, ρ, d, n₀, μe, D, ℓ, f3zz,
   H, q, k_B`);
3. rebuilds the Legendre basis from `numpy.polynomial.legendre` coefficient
   arrays, differentiating with `legder` and evaluating with `legval`;
4. uses quadrature orders **40, 60 and 301**, which are not the production rule
   (`max(64, 2n+10)`, i.e. 64 nodes at the degrees used here);
5. compares against **the strings now printed in the manuscript**, not against
   the solver's output;

so agreement cannot come from a shared code path.  The production-side audit
(`round18_mathematical_audit.py`) is the complementary script: it *does* call the
solver, and asks whether the solver computes what the text says.

## Group 1 — dimensionless groups (15 checks)

| quantity | recomputed here | printed | relative difference |
|---|---|---|---|
| `c_s = √(c44/ρ)` | 2746.6088 m/s | 2746.6088 | `1.7e-8` |
| `c_s/(2πd)` | 2.1856818 GHz | 2.1857 | `8.3e-6` |
| `T` from Einstein `qD/(μk_B)` | 301.7175 K | 301.7 | `5.8e-5` |
| `a = k_BT/n₀` | 2.0828296e-39 J m³ | 2.0828e-39 | `3.0e-14` |
| `L_D` | 2.679712e-6 m | 2.6797e-6 | `4.5e-6` |
| `Q = d/L_D` | 0.074634887 | 0.074635 | `1.5e-6` |
| **`L_D/d = 1/Q`** | **13.39856** | **13.3986** | `3.0e-6` |
| `α_d = D/(dc_s)` | 0.82829416 | 0.8283 | `7.1e-6` |
| `λ = ℓ/d` | 0.25 | 0.25 | `0` |
| `f = f3zz/(d√(c44κ33))` | 2.5630917e-3 | 2.5631e-3 | `3.3e-6` |
| `H_ref = d√(a c44)` | 1.8927406e-21 J m | 1.8927e-21 | `2.1e-5` |
| `c* = c33 − 2c13²/(c11+c12)` | 154.38369 GPa | 154.38 | `2.4e-5` |
| `H_bound = ℓ√(a c*)` | 8.9659762e-22 | 8.966e-22 | `2.7e-6` |
| `H* = H_bound/√5` | 4.0097064e-22 | 4.0097e-22 | `1.6e-6` |
| `h = |H|/H_ref` at `2e-23` | 0.010566688 | 0.010567 | `3.0e-5` |

The largest relative difference in the whole group, `5.8e-5`, is on `T = 301.7 K`
and is pure print rounding of the target.  The Schur number is recomputed as
`H²/(c33 ℓ² a) = 3.476e-4` and is reported as a bound (`schur < 1`), not as a
fitted number.

## Group 2 — normalisation and measure (12 checks)

* mass in the `ds` measure equals the identity to `4.0e-14 … 5.5e-14` at
  `N = 5, 6, 7`;
* the **same** integral in the `dζ` measure equals `2I` to `7.9e-14 … 1.1e-13`;
* stiffness diagonal against `2j(j+1)(2j+1)`: `4.7e-11` absolute on a scale of
  660, i.e. `7e-14` relative;
* the three printed rows of the `N = 6` matrix reproduce to `4.9e-5` absolute
  (the five-digit rounding of the print), relative `2e-7`;
* entries that must vanish by parity: `2.4e-15`.

## Group 3 — grounded space and index orientation (7 checks)

`ψ_j(±½) = 0` to `8.9e-16`; `(ψ_i,b_j) = δ_ij − r_iδ_{j,i+2}` and
`(b_i,ψ_j) = δ_ij − r_jδ_{i,j+2}` both to `5.8e-15`; `Qr₀ = Q/√5 = 0.0333777`;
the band values `0.033378, 0.048860, 0.055630, 0.059538` to `4.4e-7`.
Mis-placing the band coefficient `r_i ↔ r_j` changes the `(0,2)` entry by
`0.2981` and, since the band also shifts, the matrix by `0.7454`.

## Group 4 — the five worked elements of Appendix A.2 (6 checks)

transport diagonal `−i1.828e-3 … −i18.2314` (`3.9e-5` on the largest, relative
`2e-6`); `A11` value `0.108509` (`1e-4` relative); gradient entries
`3.8547, 19.273, 53.966, 115.64` (`8.8e-4` relative `7.6e-6`); inertia
`−58.2688`; ratio `15.116`; compressibility `−1` exactly.

## Group 5 — accounting (10 checks)

`n_w` grounded/open at degrees 4, 5, 18, 22, 30 = `23/24, 28/29, 93/94, 113/114,
153/154`, all equal to `5n+3` / `5n+4` exactly; quartic degrees
`92, 112, 372, 452, 612`; decaying roots `2n_w`; edge rows `38` and columns `23`
at degree four.

## Group 6 — the reported share, end to end (4 checks)

```
|a|^2                = 1.2938855
|a|^2 P_B            = -0.023150588
× 0.9998954          = -0.023148167
÷ 1.0001081          = 0.0231456 (magnitude)   →  R_B = 0.9467952
```

reproduced to `3.7e-18 … 2.8e-6` relative (the last is print rounding).  This is
the only place in the paper where the headline number is assembled by hand, so it
is also the only place where an arithmetic slip could silently move it.

## Group 7 — the coupling block at degree six (5 checks)

row norms `0, 0, 26.8328, 91.6515, 222.8901, 450.8658, 809.4443` (`4.6e-5`
absolute); largest entry `580.4826` (`4.4e-6` relative); `h × 580.4826 = 6.1338`;
ratio to `ω² = 58.2688` = `0.10527`; every entry above the diagonal
`≤ 9.3e-12`, i.e. the block is lower triangular with two bands.

## What this script does *not* do

It does not re-derive the modal solution: no eigenvalue problem, no edge solve,
no power partition is recomputed here (they are recomputed by the production
solver and asserted in `test_model.py`, 52 tests, `OK`, 21.6 s).  It is a check on
*the arithmetic and the linear algebra of the printed statements*, which is the
scope the round-18 brief gives Part J.
