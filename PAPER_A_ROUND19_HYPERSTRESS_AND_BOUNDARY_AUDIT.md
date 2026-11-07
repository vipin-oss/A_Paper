# Paper A — Round 19: hyperstress and boundary audit (R19-2)

## 1. The claim that was in the manuscript

Appendix A.4 said, of the edge conditions:

> the double traction τ_3j3 on the same n_u test functions (**a block that exists only when the
> strain-gradient length is non-zero, since τ_3j3 vanishes with it**)

and then, of the degrees of freedom:

> With the flexoelectric coupling switched off the R_τ block is absent and m = n_u + n_φ + n_μ = 23 = n_w is square.

Both sentences are wrong, and they are wrong in the direction the supervisor identified: the
double traction does not vanish when f = 0, and it does not vanish when ℓ = 0 either.

## 2. What the constitutive model actually says

From the manuscript's own constitutive law (eq:tauZnO), in the component that the edge sees:

```
τ_3zz = ℓ²[ c13 (η_xxz + η_yyz) + c33 η_zzz ] − f E_z + H Δn      (eq:app_edge_tau)
```

Three additive terms with three different parameter dependencies:

* the elastic part vanishes with ℓ², and only with ℓ²;
* the flexoelectric part vanishes with f;
* the carrier part vanishes with H.

So τ_3zz ≡ 0 requires ℓ = f = H = 0 simultaneously. Setting f = 0 leaves two terms; setting
ℓ = 0 leaves two different terms.

## 3. The five cases

| case | parameters | τ_3zz | state N_s | rows m | double traction |
|---|---|---|---|---|---|
| A | ℓ ≠ 0, f ≠ 0, H ≠ 0 | all three terms | 2n_w + 2n_u | 2n_u + n_φ + n_μ | required |
| B | f = 0, ℓ ≠ 0 | ℓ² and H | 2n_w + 2n_u | 2n_u + n_φ + n_μ | required |
| C | ℓ = 0, f ≠ 0 | −fE_z and H | 2n_w | n_u + n_φ + n_μ | **not available** |
| D | H = 0, ℓ ≠ 0 | ℓ² and f | 2n_w + 2n_u | 2n_u + n_φ + n_μ | required |
| E | ℓ = f = H = 0 | 0 | 2n_w | n_u + n_φ + n_μ | absent (identically zero) |

The variable that changes between the two blocks of cases is not f or H but **order**. At
ℓ ≠ 0 the state carries the axial trace u₃ and its derivative, 2n_w + 2n_u unknowns, and the
double traction is a genuine condition on them. At ℓ = 0 the hyperelastic term is gone, the
state collapses to 2n_w, and there is no ∂_x u₃ trace for a double traction to act on.

## 4. Case C, stated as a restriction rather than repaired

Case C is the one the round-18 text silently assumed away by tying the block to ℓ. It is not a
case this formulation can solve: it would require a double-traction condition while offering
only the second-order state of case E. The formulation therefore **admits ℓ = 0 only in the
classical limit f = H = 0**, and the manuscript now says so — in Appendix A.4 as an explicit
restriction and in §`sec:governing_bc` as a two-sentence clause after eq:bc_edge.

This is the honest classification:

* it is **not** a solver bug: the code refuses the combination rather than producing a number;
* it is **not** a hidden approximation: no reported run has ℓ = 0 (every reported run has
  λ = ℓ/d = 0.25);
* it **is** a restriction of the model class, and a referee is entitled to see it stated. It is
  listed among the round-19 limitations for that reason.

Removing the double-traction rows because a *different* coupling vanishes would have been the
error the master prompt forbids; instead the block is kept wherever τ ≠ 0 and the one case where
τ ≠ 0 but no condition exists is excluded from the model.

## 5. Consequences for the dimension count

For cases A, B and D:

```
m = 2n_u + n_φ + n_μ,      N_s = 2n_w + 2n_u,      M = N_s/2 = n_w + n_u,
n_w = 3N + n_φ + n_μ  ⇒  M = 2n_u + n_φ + n_μ = m .
```

For case E:

```
m = n_u + n_φ + n_μ,       N_s = 2n_w,             M = n_w = n_u + n_φ + n_μ = m .
```

Both are square, for the same reason: the number of decaying states is half the state
dimension. The next report turns this into the R19-3 verification.

## 6. Numbers

At degree 4, case A: n_u = 15, n_φ = 3, n_μ = 5 ⇒ m = 38; N_s = 76; M = 38. At degree 22:
n_u = 69, n_φ = 21, n_μ = 23 ⇒ m = 182; N_s = 364; M = 182.

## 7. Files touched

* `sections/appendix_derivations.tex` — Appendix A.4 rewritten: eq:app_edge_rows,
  eq:app_edge_tau, the five-case table, the case-C restriction, eq:app_edge, eq:app_edge_R,
  eq:app_edge_square.
* `sections/governing_equations.tex` — two-sentence clause after eq:bc_edge.
