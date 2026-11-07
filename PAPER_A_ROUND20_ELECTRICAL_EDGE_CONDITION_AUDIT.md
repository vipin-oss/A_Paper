# Round 20 — electrical edge condition (R20-2): which BVP produced the numbers

## 1. Trace of the fourth row block

`Plate.boundary_vector` (round-19 code) returns, for `λ>0`,

```
[ T[:nu] ,  R ,  q[self.ip] ,  T[self.im] ]
```

`ip` and `im` are the slices of the potential and carrier coefficients of the
modal vector `q`. Each block was identified numerically at the operating point
(degree 4, `k_x = 0.5481 − 0.3791i`) rather than from the source:

| block | identity | deviation |
|---|---|---|
| `R` | `τ_j11` | 2.4e-14 (audit, degree 6: 1.1e-13) |
| `T[ip]` | `D_x` | 6.0e-15 |
| `T[im]` | `−J_x` | 8.9e-12 |
| `T[:nu]` | `(A10+ikA11−k²A12−ik(A20+ikA21−k²A22))q` | 1.2e-14 |

`q[self.ip]` are the *coefficients* of the potential's z-expansion, so setting
them to zero sets `φ(0,z) ≡ 0` for every `z`: a **Dirichlet (grounded /
metallised) edge**. The article's `eq:bc_edge` requires `D_x(0,z) = 0`, which is
the **natural** condition and is what `T[ip]` supplies. The submission R20-2 is
therefore substantiated at the level of the row.

Both rows are legitimate boundary conditions — they just describe different
devices (a free charge-free edge versus an electroded one). They are not
equivalent, and the solver cannot satisfy both.

## 2. Measured residuals on the full superposed field

Residual = norm of the boundary functional of the *complete* field (incident mode
plus every outgoing mode with its solved amplitude), projected on the same test
functions, divided by the same functional of the incident mode alone. Degree 22.

| case | condition | `R_B` | `r_φ` | `r_{D_x}` | `r_{J_x}` | `r_m` |
|---|---|---|---|---|---|---|
| operating point `k_xd=0.7361990` | grounded (delivered) | **0.0231456** | 1.6e-15 | **1.778** | 4.5e-10 | 3.8e-13 |
| operating point | charge-free | **0.0192916** | **1.231** | 8.5e-13 | 4.5e-10 | 4.0e-13 |
| `k_xd=0.550` | grounded (delivered) | **0.5791800** | 1.7e-15 | **0.559** | 1.3e-10 | 1.1e-13 |
| `k_xd=0.550` | charge-free | **0.5519100** | **0.438** | 4.0e-13 | 1.4e-10 | 1.1e-13 |
| peak (new argmax, `k_xd=0.527175`) | charge-free | **0.9428718** | 0.0366 | 4.5e-14 | — | — |

Each configuration annihilates its own row to machine precision and violates the
other by 44–178 % of the incident scale. The delivered solver is the grounded one:
`φ` is satisfied at 1.6e-15 and `D_x` is violated by a factor 1.78.

Two independent confirmations that the *delivered* numbers are the grounded ones,
and not merely that the row exists:

* the recomputation with the default solver reproduces the published operating
  point `0.0231456` and the published `k_xd=0.55` value `0.5791800` to all digits;
* switching only the one row to `T[ip]` (no other change) moves them to
  `0.0192916` and `0.5519100`.

## 3. Which problem produced the reported results

**The grounded (metallised-edge) problem**, in every delivered dataset. The
charge-free problem the article describes had never been solved before this round:
the row `T[ip]` was reachable only by editing the source, which is why the
discrepancy survived six earlier audit rounds.

## 4. Rerun of the reported configuration under the correct condition

Backward-channel search with the charge-free edge, degree 22, domain
`0.465 ≤ k_xd ≤ 0.625`:

* coarse raster `2e-3`, single dominant peak; bracket `±0.01`, plateau step
  `5e-4`; refinement step `2.5e-5`;
* **argmax `k_xd = 0.527175`**, `R_B = 0.9428718`, plateau flat to `1.65e-5` over
  `±5e-4`;
* degree 22 → `0.9428718`, degree 26 → `0.9428717` (agreement `1e-7`);
* `r_{D_x} = 4.5e-14`, `r_φ = 0.0366` at the peak (the incident mode carries only
  3.7 % of the boundary potential functional at near-total reflection);
* edge matrix square and full rank, condition number 140.9 (deg 22) / 77.3
  (deg 26) after scaling, scaled residual `2.7e-15`, power balance `8.3e-13`,
  edge absorbed power zero, outgoing power `0.999905` of the incident.

Published (grounded) value for comparison: `0.9467952` at `k_xd = 0.5275`.

| quantity | delivered (grounded) | corrected (charge-free) | change |
|---|---|---|---|
| peak share `R_B` | 0.9467952 | **0.9428718** | −0.414 % |
| argmax `k_xd` | 0.5275 | 0.527175 | −0.06 % |
| `k_xd = 0.55` | 0.5791800 | **0.5519100** | −4.71 % |
| operating point | 0.0231456 | **0.0192916** | −16.65 % |

The qualitative statement survives (a near-unity backward channel at a local
maximum); the numbers do not, and the operating-point share moves by a sixth.

## 5. Decision

**Outcome B — implementation error, a scientific blocker of the first kind**: the
solver did not solve the boundary-value problem the article states, and no
round-19 number that involves the edge can be presented as a solution of the
article's problem.

The repair is a *configuration*, not a fudge: one row of the boundary operator,
selected by an explicit, validated keyword (`edge_electric`), defaulting in
`build_figure_data.plate()` to `'insulating'` — the article's problem. The
grounded configuration is retained and documented as a distinct problem (it is a
legitimate metallised-edge device, and reproducing round 19 requires it), with
`edge_electric='ground'`.

Nothing was tuned: the charge-free peak was found by the same raster/bracket/
refine procedure that produced `0.9467952`, and its value (`0.9429`) was not
adjusted toward or away from any previously published number. The word
"charge-free" is not applied anywhere to the grounded configuration.

## 6. What remains unproven in this section

The *mechanical* traction row was not reduced to a pointwise identity and is not
claimed to be one (see `VARIATIONAL_BOUNDARY_DERIVATION`, section 5, and
`FINAL_SUPERVISOR_DECISION`, gate 3). The electrical and carrier rows, the double
traction, the squareness/rank of the edge system and the power balance are
verified.
