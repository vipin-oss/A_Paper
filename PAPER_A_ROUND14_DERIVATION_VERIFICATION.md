# Round 14 — derivation verification

Every derivation added or rewritten in round 14 was checked by a route that is
independent of the derivation itself. The routes used are: symbolic expansion,
finite-difference evaluation of the field identities, exact algebraic collapse at
a limit, an operator identity inside the solver, and the existing solver-level
tests. Nothing below is a restatement of the derivation.

## 1. Strain and strain-gradient amplitudes under the ansatz (new §2.8)

**Route: finite-difference differentiation of the plane-wave field, independent
of the algebra.** With $k_x=0.7$, $k_y=0.31$, amplitudes $A_1=1.3$, $A_2=0.6$,
$A_3=0.9$ and $u_i=\widehat u_i e^{i(k_xx+k_yy)}$, each component of
`eq:strain_amplitudes` and two components of `eq:eta_amplitudes` were compared with
central differences (step $10^{-6}$):

| Identity | \|numerical − formula\| | magnitude of the exact value |
| --- | --- | --- |
| $\widehat\varepsilon_{xx}=ik_x\widehat u_1$ | 4.4e-11 | 9.1e-01 |
| $\widehat\varepsilon_{yy}=ik_y\widehat u_2$ | 2.6e-11 | 1.9e-01 |
| $\widehat\varepsilon_{xy}=\tfrac12 i(k_x\widehat u_2+k_y\widehat u_1)$ | 3.2e-11 | 4.1e-01 |
| $\widehat\varepsilon_{xz}=\tfrac12(\widehat u_1'+ik_x\widehat u_3)$ | 3.6e-11 | 3.2e-01 |
| $\widehat\varepsilon_{yz}=\tfrac12(\widehat u_2'+ik_y\widehat u_3)$ | 8.5e-12 | 1.4e-01 |
| $\widehat\eta_{xxx}=-k_x^2\widehat u_1$ | 7.4e-11 | 6.4e-01 |
| $\widehat\eta_{xxy}=ik_x\cdot ik_y\widehat u_1$ | 4.8e-11 | 2.8e-01 |

The residual is at the difference-scheme truncation level; the identities hold.

## 2. The quartic operator `eq:quartic` (new §2.8)

**Route: expansion identity inside the solver's own assembly.** The assembled
operator is `Σ_{r,s} (−ik_x)^r (ik_x)^s A_rs` with $r,s\in\{0,1,2\}$
(`Plate.matrices`, `Plate.polynomial`). The power-by-power form printed in the
paper is the same sum regrouped. Evaluated at $k_x=0.31$, $-0.77$ and $1.9$:

- max |expanded − solver polynomial| = 1.1e-13, 2.3e-13, 9.1e-13, against entries
  of magnitude 2.16e5 (relative ≈ 1e-18).

So `eq:quartic` is an identity, not an approximation, and the degree-four claim is
a property of the *implementation* and not only of the prose.

## 3. Classical collapse at $\ell=0$ (stated in §2.8 and §3.1)

**Route: exact algebraic collapse.** Rebuilding the plate with $\ell=0$,
$f=0$, $H=0$ (the model's own construction forbids $\ell=0$ with $f\ne0$):

- $\|\mathsf A_{22}\| = 0$ exactly, $\|\mathsf A_{12}\| = 0$ exactly,
  $\|\mathsf A_{00}\| = 8.19\times10^{3}$.

The fourth- and third-order blocks vanish identically, so the quartic reduces to
the quadratic piezoelectric-semiconductor problem. This is what the paper now
states, and it is a property of the strain-gradient sector only — consistent
with the mechanism controls, in which removing the coupling $H$ does **not**
remove the branch.

## 4. The claim that $n_0$ and $\mu$ enter only through $n_0\mu$ (figure 2 note)

**Route: direct evaluation of the non-dimensional parameters for equal products.**
$Q=qd/\sqrt{\kappa_{33}a}$ with $a=qD/(\mu_en_0)$, hence $Q\propto\sqrt{\mu_en_0}$.

| configuration | $Q$ | $\alpha$ |
| --- | --- | --- |
| $n_0=2\times10^{18}$, $\mu=0.0175$ | 0.0746348872427758 | 0.8282941632839342 |
| $n_0=1\times10^{18}$, $\mu=0.0350$ | 0.0746348872427758 | 0.8282941632839342 |
| $n_0=2\times10^{18}$, $\mu=0.0088$ | 0.0529254053307528 | 0.8282941632839342 |

Equal products give bit-identical dimensionless parameters; unequal products do
not. The collapse of the five carrier-density curves in F2 is therefore a property
of the model, and the figure now says so.

## 5. Variational derivation of the balance laws (new §2.4)

**Route: sign and index consistency checks, plus the solver's boundary rows.**

- The two integrations by parts give
  $\int\sigma\delta\varepsilon=-\int\sigma_{ij,j}\delta u_i+\oint n_j\sigma_{ij}\delta u_i$
  and
  $\int\tau\delta\eta=\int\partial_k\partial_j\tau_{ijk}\delta u_i-\oint n_j\partial_k\tau_{ijk}\delta u_i+\oint n_k\tau_{ijk}\delta u_{i,j}$;
  the volume terms give $\rho\ddot u_j=\partial_i\sigma_{ij}-\partial_i\partial_k\tau_{jik}$
  only if the hyperstress carries two sign changes — which it does, and which is
  now the stated reason for the minus sign rather than an assertion.
- Index check: $\tau_{ijk}$ symmetric in $(i,j)$, so $\delta\eta_{ijk}=\delta u_{i,jk}$
  is legitimate; the boundary terms are exactly the traction
  $n_i\Sigma_{ij}$ and the double traction $n_k\tau_{ijk}$ used in §2.6.
- Solver check: the strong-form residual function
  (`model.strong_gradient_matrix`) is written with the same traction,
  double-traction and blocking rows, and the existing residual tests pass
  (residuals below $10^{-8}$ in the normalised measure).

## 6. Regression after the round-14 edits

| Check | Result |
| --- | --- |
| `python -m unittest paper_a_study.test_model` | **52 tests, OK** (21.6 s) |
| `claim_audit.py` | **PASS** — 23 claims, 46 tokens, 5 deprecated values guarded, figures 1–10 in first-citation order, 11/11 source-agreement rows |
| `scripts/static_check.py` (manuscript) | **PASS**, exit 0 — 108 labels, 82 references, 13/13 citations |
| Figure producers | re-rendered all ten; only style, legend placement and inset geometry changed; no dataset regenerated |
| Full battery (`run_all_checks.py`) | **not re-run**: no producer or solver changed. The last full run remains the round-11 record (18 PASS / 0 FAIL / 1 SKIP), which is *not* re-claimed as a round-14 result. |
| LaTeX compilation | **not performed** — no TeX engine in this environment. **BUILD UNVERIFIED.** |

## 7. What was not verified, and is therefore not claimed

- The entries of $\mathsf A_{rs}$ are not given in closed form, so no closed-form
  matrix identity is claimed (flag F-1).
- The corner line force is not resolved (flag F-2).
- No typeset page was inspected, because none exists in this environment.
