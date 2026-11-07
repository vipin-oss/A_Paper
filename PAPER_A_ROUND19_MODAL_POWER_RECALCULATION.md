# Paper A — Round 19: modal-power recalculation (R19-4)

## 1. The rule for this round

One Galerkin degree end-to-end: **n = 22** for the reported results. Every number in the worked
modal-power calculation must come from **one stored row**, and the two quantities that are
often confused must stay apart:

* the **operating-point share**, R_B = 0.0231456 (2.31 %) at k_x d = 0.7362;
* the **local peak**, R_B = 0.9467952, at k_x d = 0.5275.

They are different rows of different searches and neither implies the other.

## 2. What the round-18 text did

The appendix chain quoted

```
𝒫_x = −0.0178923,  |a_B|² = 1.2938,  →  −0.0231505,  × 0.9998954 / 1.0001081 = 0.0231456
```

The first two numbers are the **n = 18** row; the product, the exponentials and the final value
are the reported **n = 22** row. The product is insensitive to the mixture (it is
degree-independent to seven digits), so the printed answer never moved — but the inputs did not
belong to one row, which is exactly what R19-4 forbids.

## 3. The degree-22 row, end to end

```
row n = 22 (operating point, k_y d = 0.1298, ω d/c_s = 7.633372)
  |a_B|            = 1.2250974        |a_B|²         = 1.500864
  𝒫_x (raw)        = −0.015424813     |a_B|²|𝒫_x|   = 0.023150542
  Im k_Bx          = −5.230595e-6     exp(2 Im k_Bx L) = 0.9998954
  Im k_ix          = +5.402719e-6     exp(2 Im k_ix L) = 1.0001081
  P_inc(−L)        = 1.0001080602
  −P_B(−L)/P_inc   = 0.0231481203/1.0001080602 = 0.0231456192  → 0.0231456
```

Both attenuation exponents are degree-independent to the seven digits quoted (they agree at
n = 18, 22, 26, 30), so the degree enters the ratio only through |a_B|²|𝒫_x|.

## 4. Why the mixing was invisible

| degree | 𝒫_x (raw) | |a_B| | |a_B|²|𝒫_x| | −P_B(−L)/P_inc | R_B |
|---|---|---|---|---|---|
| 18 | −0.017892253 | 1.1374910 | 0.023150530 | 0.0231481087 | 0.0231456076 |
| **22** | **−0.015424813** | **1.2250974** | **0.023150542** | **0.0231481203** | **0.0231456192** |
| 26 | −0.013245459 | 1.3220476 | 0.023150546 | 0.0231481237 | 0.0231456229 |
| 30 | −0.011377729 | 1.4264378 | 0.023150547 | 0.0231481254 | 0.0231456243 |

The raw power falls by 36 % and the amplitude rises by 25 % between n = 18 and n = 30 while
their product moves by 7.2e-7 relative — the eigenvector normalisation cancels, as it must.
That cancellation is why an author can mix rows without noticing, and why the manuscript now
prints the product explicitly (eq:RB_worked) with the remark that 𝒫_x and |a_B| alone measure
the normalisation and not the port.

The explicit rescaling experiment stored beside these rows (every eigenvector multiplied by an
independent random complex factor before re-solving) leaves R_B unchanged to 3.5e-17.

## 5. What changed in the manuscript

* `numerical_methods.tex`, eq:RB_worked and its follow-up sentence: n = 22 inputs, the product
  printed, the degree-dependence stated.
* `appendix_derivations.tex`, Appendix A.6: eq:app_RB now carries the n = 22 chain, with a new
  eq:app_RB_inputs listing the five stored quantities and the statement that they come from one
  row; the operating-point/local-peak separation is a separate paragraph.
* eq:RB_planes split into two lines (layout only, no number changed).

No dataset was regenerated: all cited values are read from `paper_a_study/figure_data/modal_flux_audit.json`,
which is unchanged since round 18.
