# Paper A — Round 19: polynomial and operator audit (R19-5, R19-6)

## 1. R19-5 — "banded by two"

### What was there

Appendix A.1 said the stiffness matrix is "banded by two", and the round-18 supervisor asked
whether that is true of the assembled matrix. It is not.

### What the matrix is

`S_ij = ∫_{-1}^{1} b_i'(s) b_j'(s) ds` with `b_j` the integrated Legendre basis, computed here
from an independent 60-point quadrature and compared with the printed 6×6 matrix:

```
S(6) = [ 0      0       0      0       0      0     ]
       [ 0     12       0     18.330   0     22.978 ]
       [ 0      0      60      0      80.498  0     ]
       [ 0     18.330   0    168       0    210.60  ]
       [ 0      0      80.498  0     360      0     ]
       [ 0     22.978    0    210.60    0    660    ]
```

Measurement: the maximum absolute difference from the quadrature is 8.5e-4 (tolerance
1e-4 × 660). Opposite-parity entries are 2.4e-15, i.e. zero. Row 5 has **three** non-zeros
spanning **four** columns; a banded-by-two matrix would have two non-zeros spanning two.

### What replaces it

> the matrix is real and symmetric and it vanishes between basis functions of opposite parity,
> but the same-parity entries are not confined to a band. At N = 6 the entry S₁₅ = 22.978
> couples indices four apart, and at any N the row i has non-zero entries in every column j ≤ i
> of the same parity, so the matrix is not tridiagonal and has no fixed bandwidth.

This matters for a reader who might think the band structure makes the edge solve cheap: the
edge matrix B is dense whatever the bandwidth of S, because B is assembled from eigenvector
traces, not from S.

## 2. R19-6 — the powers of k_x

### What was there

> The strain operator carries the k_x power in its first slot, B₀ contains i k_x b_j for ε_xx and
> B₁ contains b_j for the ∂_x¹ part, so that the k_x power of a block is the sum of the powers in
> its two factors.

That sentence describes a bookkeeping in which ε_xx already carries one power and the block
index adds another — which double counts, exactly as the master prompt suspected.

### What is now in the appendix

One split, stated once (eq:app_strain_split), with the coefficient vectors independent of k_x:

```
ε_ij = ε⁽⁰⁾_ij + i k_x ε⁽¹⁾_ij
```

and the six components tabulated: ε_xx has (0, b_j); ε_yy (i k_y b_j, 0); ε_zz (b_j', 0);
ε_yz (b_j' and i k_y b_j, 0); ε_xz (b_j', b_j); ε_xy (i k_y b_j, b_j). No component carries
more than one power, so the split terminates at first order.

The block is *defined* as the coefficient of (−i k_x)^r (i k_x)^s:

```
A_rs = ⟨ε⁽ʳ⁾, C ε⁽ˢ⁾⟩ + λ² ⟨∂_z ε⁽ʳ⁾, C ∂_z ε⁽ˢ⁾⟩ + …            (eq:app_ar_s)
```

Two consequences are now written out:

* `A₂₂ = λ²⟨ε⁽¹⁾, Cε⁽¹⁾⟩ ≠ 0` — the quartic term — and its rank is n_u, not n_w, because ε⁽¹⁾
  lives on the displacement slots only. Measured: rank = 15 = n_u at degree 4.
* `A₀₂ = A₂₀ = 0` because no strain component carries two powers of i k_x; the k⁴ term needs one
  factor from each side of the gradient energy. Measured: ‖A₀₂‖/‖A₀₀‖ = ‖A₂₀‖/‖A₀₀‖ = 0 to
  1e-14.

### The closed form and its signs

With `p(k) = Σ_{r,s} (−i k)^r (i k)^s A_rs` the coefficient matrices in powers of k are

```
A₀ = A₀₀ ,  A₁ = i(A₀₁ − A₁₀) ,  A₂ = (A₁₁ − A₀₂ − A₂₀) ,  A₃ = i(A₁₂ − A₂₁) ,  A₄ = A₂₂
```

and `p(k) = A₀ + k A₁ + k² A₂ + k³ A₃ + k⁴ A₄`. The signs of A₂ and A₃ were recorded wrongly in
the round-18 working notes; they are re-derived here and checked against `Plate.polynomial()`
to 4e-17 (see test T1). The manuscript does not print this closed form, but the pencil test
depends on it, and the sign error would have made the linearisation look wrong when it is not.

### The pencil

```
[Z I Z Z ; Z Z I Z ; Z Z Z I ; −A₀ −A₁ −A₂ −A₃] x = k [I I I A₄] x
```

gives all 2(n_w + n_u) finite eigenvalues of the polynomial to 6.6e-12 (degree 4) and 3.9e-10
(degree 6). The form with A₄ placed on the left-hand side does not, and is not used.

### Where f can appear

Because f₃₃₃₃ pairs E_z (no k_x power) with ∂_z ε_zz (no k_x power), f enters A₀₀ and no other
block — measured: with f = 0 only A₀₀ changes, by 5.3978492 (2.9e-4 relative), and A₁₂, A₂₂,
A₀₂ are unchanged to 1e-13. This is stated in a new paragraph of Appendix A.3 and is tested as
T2. It is also the formal reason the double-traction audit can move f without moving the
quartic coefficient.

## 3. Files touched

* `sections/appendix_derivations.tex` — eq:app_strain_split, eq:app_ar_s, eq:app_A22, the
  strain-split table, the f-placement paragraph; the "banded by two" sentence replaced.
* `sections/numerical_methods.tex` — eq:finite_roots and the root-count paragraph (see
  `PAPER_A_ROUND19_EDGE_SYSTEM_VERIFICATION.md` §7 of the final report).
