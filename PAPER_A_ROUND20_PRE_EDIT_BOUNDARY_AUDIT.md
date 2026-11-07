# Round 20 — pre-edit boundary audit

Baseline: commit `baa9800da173b385253b6881c2a0e2868b9eed0a` (round 19), branch
`arena/ea7ca4dd-a-paper`, package `Paper_A_Complete_Project_round19.zip`
(3,332,017 B, 288 entries, sha256 `749858dc…c494c4b8`).

This round audits the physics of the reflecting edge, not the layout of the
manuscript. Two submissions were made against round 19 and neither the manuscript
nor the solver was assumed correct:

* **R20-1 (geometry / normals).** The article states the edge conditions at
  `x=0` as `σ_ix=0, τ_ijx=0, D_x=0, J_x=0` (`eq:bc_edge`), while Appendix A.4
  is said to use the *face* (z-normal) quantities `Σ_3j, τ_3j3, D_z, J_z`.
* **R20-2 (electrical condition).** `model.boundary_vector` supplies `q[self.ip]`
  — potential coefficients — as the fourth-row block, which looks like
  `φ(0,z)=0` (grounded) rather than the stated `D_x(0,z)=0` (charge-free).

## What the audit had to settle

1. Which boundary-value problem the delivered numbers were produced from.
2. Whether the manuscript's four edge conditions are the complete free-edge set
   (they are not automatically: the Mindlin decomposition produces a surface
   divergence and a corner line force).
3. Whether the appendix's normal directions are right, independently of the
   solver.
4. Whether `σ_ix=0, τ_ijx=0` is sufficient, necessary or over-prescribing.
5. What changes numerically if the electrical row is corrected.

## Method

Everything below was established by *measurement on the code that produced the
delivered data*, not by reading it:

* `boundary_vector` was found to return, for `λ>0`,
  `[T[:nu], R, q[ip], T[im]]` and the four blocks were identified numerically
  (action log 1094–1096): `R ≡ τ_j11` to 1.1e-13, `T[im] ≡ −J_x` to 8.9e-12,
  `T[ip] ≡ D_x` to 6.0e-15, and the mechanical block `T[:nu]` equals
  `(A10+ikA11−k²A12−ik(A20+ikA21−k²A22))q` to 1.2e-14, i.e. it is the weak-form
  generalised traction, not a pointwise component.
* Residuals were evaluated on the **complete superposed field** — incident mode
  plus every outgoing mode with its solved amplitude — projected on the same
  test functions and normalised by the same functional applied to the incident
  mode alone, so `r_φ` and `r_{D_x}` are ratios of the boundary functional of the
  field actually reported.
* Two independent eigenvalue checks were run: the full matrix polynomial (for the
  finite/infinite structure) and the geometric ray/plane arguments are *not*
  used anywhere.

## Code change made before the audit, with the baseline preserved

`model.Plate.__init__` gained `edge_electric='ground'` and `boundary_vector`
selects `flux = T[ip]` for `'insulating'` versus `q[ip]` for `'ground'`. The
default is `'ground'`, so every round-19 number is reproduced unchanged by the
default path; the switch only adds a configuration that had never been solved.
The one-line physical reading is that the two configurations differ in a single
row and are not equivalent.

## Files written by the round

`paper_a_study/round20_recompute.py` (two-configuration residuals, peak search),
`paper_a_study/round20_boundary_audit.py` (ten checks), and
`paper_a_study/figure_data/round20_edge_condition_audit.json` (all numbers).

## Status of the audit itself

BUILD UNVERIFIED throughout: no LaTeX engine is available in this environment,
so nothing in this round claims a compiled or visually inspected PDF.
