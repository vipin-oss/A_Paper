# Paper A — extended numerical validation (round 7)

Everything in this report was **executed in this environment** during round 7
unless the row says otherwise. Environment: Python 3.11.2, NumPy 2.4.6, SciPy
1.17.1, Matplotlib 3.11.2, no TeX engine.

Battery entry point: `python paper_a_study/run_all_checks.py` →
**OVERALL: PASS**, 15 checks, one `SKIP` (LaTeX build, no engine).

---

## 1. Central validation table

| Test | Physical claim | Reference method | Configuration | Numerical error | Tolerance | Result | Independent? |
|---|---|---|---|---|---|---|---|
| `test_model` (22 tests) | discretisation, limits, reciprocity, energy, constants | analytic limits and stored references | several | 1e-9 … 1e-15 | as stated per test | **PASS** (9.6 s) | mixed (see §7) |
| classical limit ℓ=f=H=0 | SH modes ω² = c₆₆K² + (jπ)²/d² | closed form | 3 modes | 1e-9 | 1e-9 | **PASS** | yes |
| `verify_dimensions` | dimensional homogeneity, contraction A = ℓ²c δ, Schur bound | analytic exponents | 25 identities, 275 rows | exact | — | **PASS** | yes |
| `quasistatic_check` | d/λ_EM, k_EM d, ωτ_d | closed form | material file | exact | — | **PASS** | yes |
| `convergence_audit` | R_B converged in the Galerkin degree | degree sequence 14…30 | k_xd = 0.7362 and 0.5250 | 7.2e-7 / 2.1e-8 (18→30) | 1e-6 | **PASS** | no (same solver) |
| `quadrature_audit` | R_B converged in the quadrature rule | 64/128/192/256 nodes at fixed basis | both points | 6.9e-9 worst vs 256 nodes | 1e-7 | **PASS** | no (same solver) |
| `modal_flux_audit` | R_B invariant under eigenvector rescaling | analytic rescaling | both points | 1.5e-15 | 1e-10 | **PASS** | yes (analytic invariance) |
| `mechanism_controls` | which ingredient produces the partition | matched controls, 5 configurations × 3 points | 15 solves | balance ≤1.1e-12 | 1e-10 | **PASS** | no (controls, not a reference) |
| `corner_assessment` | corner band does not accumulate energy | cross-check vs refinement study | 2 points × 4 degrees | cross-check diff 0.0 | 1e-9 | **PASS** | partially (independent store) |
| `phase_speed_audit` | text agrees with solver on v_p, k_EM, ωτ_d | recomputation from the material file | — | 0 discrepancies | exact | **PASS** | yes |
| `claim_audit` | manuscript numbers match the registry | 14 claims / 36 tokens | whole manuscript | 0 mismatches | per claim | **PASS** | — |
| `mutation_tests` | the gates fire when they should | 5 deliberate defects | scratch copies | 5/5 caught | 5/5 | **PASS** | — |
| LaTeX build | document compiles | pdflatex + bibtex | — | — | — | **SKIP: no engine** | — |

## 2. Spectral convergence (executed)

`figure_data/convergence_audit.json`

```
operating point  k_xd = 0.736199
   n   dof        f/GHz           R_B  |dR_B|/R_B     K_B  residual   balance     cond
  14    73 16.684123136  0.0231455605    2.76e-06 0.245175   2.8e-15   4.7e-12     64.5
  18    93 16.684123136  0.0231456076    7.21e-07 0.245175   2.6e-15   1.4e-12     56.9
  22   113 16.684123136  0.0231456192    2.19e-07 0.245175   2.8e-15   8.3e-13    160.5
  26   133 16.684123136  0.0231456229    5.99e-08 0.245175   2.8e-15   1.1e-12     85.3
  30   153 16.684123136  0.0231456243    0.00e+00 0.245175   2.9e-15   5.7e-12    185.9
  successive relative changes: 2.0e-06 5.0e-07 1.6e-07 6.0e-08

branch maximum   k_xd = 0.525000
  14    73 16.654677690  0.9318914296    6.04e-08 0.524949   1.9e-15   5.1e-14     64.5
  18    93 16.654677690  0.9318914667    2.06e-08 0.524949   2.1e-15   1.4e-13     56.9
  22   113 16.654677690  0.9318914743    1.25e-08 0.524949   2.7e-15   9.8e-14    160.5
  26   133 16.654677690  0.9318914823    3.83e-09 0.524949   2.1e-15   5.2e-13     85.3
  30   153 16.654677690  0.9318914859    0.00e+00 0.524949   2.2e-15   1.8e-12    185.9
  successive relative changes: 4.0e-08 8.1e-09 8.6e-09 3.8e-09
```

Successive changes decrease monotonically; the sequence reaches the round-off
floor before an asymptotic slope can be established, so **no convergence rate is
fitted** and none is quoted in the manuscript.

## 3. Quadrature sufficiency (executed)

`figure_data/quadrature_audit.json`. The rule is Gauss–Legendre on [−1/2, 1/2]
with `max(64, 2·degree+10)` nodes; a `nquad` override was added to `Plate` for
this test only (default behaviour unchanged).

```
operating_point  64/128/192/256 nodes: R_B = 0.023145619, spread 1.2e-10
branch_maximum   64/128/192/256 nodes: R_B = 0.931891474, spread 6.9e-09
worst relative change vs the 256-node rule: 6.94e-09   → PASS at 1e-7
```

The 1e-7 tolerance is three orders below the 1e-4 relative precision at which
R_B is quoted, so the default rule cannot move a quoted digit. The branch
maximum shows the larger spread because the backward and incident wavenumbers
approach each other there (K_B/K_inc = 0.992).

## 4. Matched controls (executed)

`figure_data/mechanism_controls.json`, 15 edge solves at fixed k_x, k_y, n_0, ℓ,
reference plane and incident normalisation, frequency following the branch.

| Configuration | R_B (0.736) | R_B (0.525) | R_B (0.550) | port |
|---|---|---|---|---|
| full | 0.022866412 | 0.623427131 | 0.522107121 | backward |
| f = f_0, H = 0 | 0.023145619 | 0.931891474 | 0.579180033 | backward |
| f = 0, H = 0.05H\* | 0.022868592 | 0.623426652 | 0.522152893 | backward |
| f = 0, H = 0 | 0.023148416 | 0.931808234 | 0.579245317 | backward |
| ℓ = 0 (classical) | 0.077296 (specular) | 0.135106 (specular) | 0.125061 (specular) | **none** |

Branch-consistent H sweep at the branch maximum: R_B = 0.9319, 0.7714, 0.6234 at
H/H\* = 0, +0.025, +0.05 and 0.8628, 0.7010 at −0.025, −0.05. Edge-plane values
at H = 0 and H = +0.05H\*: 0.9407 and 0.7372 (−21.6 %), against −33.1 % at the
reference plane; the difference is propagation loss.

## 5. Corner assessment (executed, unchanged)

`corner_assessment.json` cross-check `PASS`, `R_B_spread_rel = 7.2e-7`.
Corner-band share 0.9278–0.9961 % at the operating point and 1.1802–1.2643 % at
k_xd = 0.550; peak/mean 0.098–0.102 and 0.122–0.126; share *decreases* by 6.8 %
and 6.6 % between degrees 18 and 30. This is evidence that the band does not
accumulate strain-gradient energy under refinement. **It is not a proof that a
corner line force is dynamically negligible**, and the manuscript says so.

## 6. Energy budget (executed)

Operating point: 1 = 0.023146 (backward) + 0.976651 (other propagating) +
1.985e-4 (dissipation) + 4.169e-6 (interference magnitude); rounded closure
1.4e-6, exact closure 3.4e-16, solver balance 7.3e-13.
Branch maximum: 0.931891 + 0.058109 (other) + 2.63e-5 (dissipation) with an
interference term of −9.97e-3; total outgoing 0.99000.

## 7. Independence, stated honestly

**Independent of the production path:** the exact classical SH limit; the
dimensional audit (exponent algebra, not the assembled operator); the
strong-form and C¹ finite-element checks of `numerical_methods` §verification;
the modal rescaling invariance (an analytic property); the phase-speed
reconciliation (closed-form material relations).

**Not independent:** the degree and quadrature studies use the same solver, and
they establish *convergence*, not correctness; the temporal/spatial route
agreement (2e-5) is an implementation cross-check, not a physical validation;
the matched controls are evidence about attribution, not about accuracy.

## 8. Gates: mutation tests (executed)

| Mutation | Gate | Result |
|---|---|---|
| M1 `\path` inserted into a caption | `static_check` | CAUGHT — "fragile \path in a moving argument" |
| M2 0.9319 → 0.9391 in the conclusions | `claim_audit` registry | CAUGHT |
| M3 deprecated 0.99985 re-inserted | `claim_audit` stale guard | CAUGHT |
| M4 `\cite{nosuchkey2024}` | `static_check` | CAUGHT |
| M5 c44 entered in Pa instead of GPa | `TestFrozenReferenceConstants` | CAUGHT |

M5 is the one that exposed a real gap: before this round every test compared the
code with itself, so a unit error passed the entire suite. It is now caught by
the literature-band test.

## 9. Not executed

* LaTeX/BibTeX compilation, page count, overfull boxes, float placement: **no
  engine** → **UNVERIFIED**.
* Rendered visual inspection of Fig. 4: depends on the above → **UNVERIFIED**
  (the PDF was regenerated from the refined dataset and its byte size is stable).
* Any comparison against the primary Qu et al. equations: closed access →
  **UNRESOLVED**.
