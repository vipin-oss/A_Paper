# Round 20 — independent finite/infinite spectral count

The round-19 claim was `rank A22 = n_u`, "hence 2(n_w−n_u) infinite eigenvalues".
Rank deficiency of a leading coefficient is a *necessary* condition, not a proof of
the count, and round 20 does not accept it as one. The structure is therefore
computed from the polynomial itself.

## 1. The polynomial and its linearisation

With the modal reduction the dispersion condition is the matrix polynomial

```
P(k) = A0 + k A1 + k² A2 + k³ A3 + k⁴ A4 ,
A0 = A[0,0],          A1 = +i(A[0,1] − A[1,0]),
A2 = +(A[1,1] − A[0,2] − A[2,0]),  A3 = +i(A[1,2] − A[2,1]),  A4 = A[2,2],
```

`n = n_w` square, built from the same blocks `matrices(ky, ω)` that the solver
uses. The companion pencil is the standard 4`n_w` block pencil
`([I,0,0,0; 0,I,0,0; 0,0,I,0; −A0,−A1,−A2,−A3], [I,0,0,0; 0,I,0,0; 0,0,I,0; 0,0,0,A4])`,
solved with a generalised eigensolver, independent of the balanced companion used
inside `model.waves`.

## 2. Counts

| degree | pencil size `4n_w` | finite | infinite | `2(n_w+n_u)` | `2(n_w−n_u)` | rank `A22` |
|---|---|---|---|---|---|---|
| 4 | 92 | **76** | **16** | 76 | 16 | 15 |
| 6 | 132 | **108** | **24** | 108 | 24 | 21 |

At degree 4: `n_u = 15`, `n_φ = 3`, `n_μ = 5`, `n_w = 23`; `n_w − n_u = 8` and
`2·8 = 16` infinite eigenvalues; `n_w + n_u = 38` and `2·38 = 76` finite ones,
which is also the edge row count `m = 38` (`NUMERICAL_IMPACT`, table 2).

## 3. Regularity and multiplicity

| check | degree 4 | degree 6 |
|---|---|---|
| `det P(k)` at three random complex `k` | ≥ 2.7e43 | ≥ 1.4e76 |
| finite eigenvalues that are simple (`min` gap / `max|k|`) | 0.223 / 42.5 → all simple | all simple |
| `min |det P(k)|` evaluated at finite roots | 3.6e34 | — |
| algebraic multiplicity at infinity | 16 = `2ν`, `ν = 8` | 24 = `2ν`, `ν = 12` |

The polynomial is regular (no identically singular pencil), every finite
eigenvalue is algebraically simple, and the count at infinity is exactly `2ν`.
The *count* is verified; the individual Segré characteristic at infinity (whether
each of the `ν` null directions contributes a partial multiplicity of exactly two)
is **not** resolved by this computation and is not claimed.

## 4. Agreement with the solver's own roots

The 76 finite eigenvalues of the pencil match the 76 roots returned by
`model.waves(ky, Ω)` to `6.6e-12` absolute, `1.6e-13` relative, with a median
mismatch of `4.7e-14`. Two different linearisations, two different eigensolvers,
same spectrum — the classification into finite and infinite roots used by the edge
solve is therefore independently confirmed, not inherited from the same code path.

## 5. Consequence for the edge system

`M = n_w + n_u` decaying states at degree 4 is `38`, matching `m = 38` rows
(full rank, condition number 8.9 after scaling at degree 6; 140.9 at degree 22 in
the charge-free configuration, 160.5 grounded). The squareness is a property of
case A/B/D above (`ℓ≠0`), and would not hold in case C/E where the state is
`2n_w`: there `m = n_u + n_φ + n_μ = n_w`, which the code also implements
(`boundary_vector` drops the `R` block when `λ = 0`).

## 6. What this report does not establish

It does not establish that the edge boundary-value problem is well posed — a full
rank edge matrix is *not* a proof of a valid free boundary (round-20 prohibition).
Well-posedness rests on the variational derivation and on the measured residuals,
and on the residual of the *other* configuration failing (report
`ELECTRICAL_EDGE_CONDITION_AUDIT`), which is what distinguishes a solved problem
from a solved-but-different one.
