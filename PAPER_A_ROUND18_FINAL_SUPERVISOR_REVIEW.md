# Paper A — Round 18, final supervisor review

**Branch** `arena/ea7ca4dd-a-paper` · base `c33cec6` (round 17) · **BUILD
UNVERIFIED — no TeX engine exists in this environment, none could be installed,
no PDF was produced and no page was visually inspected.**

**Read this file first.** It answers three questions: what was wrong, what was
done, and what is still open.

---

## 1. Outcome in one paragraph

All seven flagged items were confirmed as real defects, and nine further defects
were found by auditing every calculation round 17 introduced.  The repairs are
limited to a measure, an index orientation, a count, a statistic, a ratio and one
wrong attribution; **no material constant, solver line, dataset, figure,
boundary condition, modal classification or reported number was changed.**  The
manuscript's mathematics is now internally consistent, and every number it prints
is reproduced to the printed precision by a script that shares no code with the
solver.  The headline result is unchanged and re-asserted by the test suite:
`R_B = 0.9467952` (94.68 %) at `k_xd = 0.5275`.  The paper is mathematically
verified and still **not** submission-ready, for the four non-mathematical reasons
listed in §5.

## 2. What was wrong (Part A, condensed)

Seven flagged, all confirmed:

| # | defect | class |
|---|---|---|
| 1 | orthonormality stated in the `ζ` measure, where the Gram matrix is `2δ`, not `δ` | normalisation (measure) |
| 2 | stiffness diagonal derived without the chain-rule `4` and the Jacobian `½` | normalisation |
| 3 | charge matrices transposed against each other (`r_i` vs `r_j`): largest entry differs by **0.2981** | index orientation |
| 4 | transport entry printed as `−(iα/ω)(k_x²+k_y²+S)δ` inside `A00`; that bracket evaluated gives `−i0.0607` where the solver has `−i0.001828` | arithmetic |
| 5 | edge operator quoted as `4n × M` "four statements per field"; truth is `m = 2n_u+n_φ+n_μ = 38` against `M = 23`, overdetermined and solved least-squares | structure |
| 6 | "fourteen Debye lengths thin in the ratio `d/L_D = 1/Q`": `Q = 0.0746`, `L_D/d = 13.4`, the plate is 7.5 % of a Debye length thick | reversed ratio |
| 7 | `n_w = 5n+3` read with `n` basis functions per field; `n_w = 93` and quartic degree 372 attributed to the reported degree, which is `n = 22` → 113 unknowns, degree 452 | accounting |

Nine further defects found:

| # | defect |
|---|---|
| 8 | "largest single entry" of the gradient block quoted as 3.85; the largest is 115.64 |
| 9 | inertia/stiffness ratio read as a thickness-mode frequency |
| 10 | `A22 = A12 = 0` claimed at every `ℓ`; they vanish only at `ℓ = 0` (`A02 = A20` are the ones that vanish always) |
| 11 | the weighted Legendre identity `(1−ζ²)` attributed to the unweighted integral |
| 12 | block inner product written in `dζ` while the identity mass is in `ds` (two places) |
| 13 | coupling matrix in Results called upper-triangular with rows 187.8/315.9 and largest entry 3.35; it is lower triangular, rows `0,0,26.83,91.65,222.89,450.87,809.44`, largest entry 580.5, `h·580.5 = 6.13` |
| 14 | an `R y(0)` display that restated the edge ansatz instead of the linear system |
| 15 | a duplicated clause in the carrier-variation sentence |
| 16 | the `ψ`-basis used where the carrier basis belongs in the coupling block |

Sixteen defects, seven of them the flagged ones; the classification table with
line numbers is `PAPER_A_ROUND18_PRE_EDIT_AUDIT.md`.

## 3. What was done (Parts B–J, condensed)

* **Measure.** Three coordinates named (`z`, `ζ`, `s`), every element matrix
  declared an `s`-integral, both Gram forms printed with the Jacobian between
  them, the chain-rule factor shown in `S_jj`, and the `N = 6` stiffness matrix
  printed in full.
* **Index orientation.** `(ψ_i,b_j)` and `(b_i,ψ_j)` written with their shapes and
  bands; the text says which block carries `−C` and which `−Cᵀ`, and states the
  `0.2981` that the wrong reading costs.
* **Worked arithmetic.** Five element values re-derived and printed with their
  scales; the transport diagonal shown as the sum of the transverse wavenumber
  and the stiffness diagonal, with `A11` carrying the axial one.
* **Accounting.** `N = n+1`, `n_w = 5n+3` grounded / `5n+4` open, a table at
  `n = 4, 5, 18, 22, 30`, and the reported degree (`n = 22`) identified from the
  stored datasets rather than assumed.
* **Edge system.** Rows counted from the test functions each condition multiplies;
  the overdetermination, the least-squares SVD solve and the `ℓ = 0` square case
  stated.
* **Debye sweep.** Every site in the project inspected: one manuscript sentence
  was wrong (and wrong twice), nine were right and untouched, and the round-17
  report that repeated the inversion carries a dated erratum.
* **Interpretation.** Two sentences that inferred physics from an isolated entry
  ratio were replaced by the scale statement the numbers support.
* **Two independent scripts.** 43 checks against the solver
  (`round18_mathematical_audit.py`, exit 0) and 59 checks with no import from the
  solver (`round18_reference_checks.py`, exit 0).  Their disagreement is the only
  thing that could have kept a mistake alive, and there is none.

## 4. The four verdicts

| axis | verdict | basis |
|---|---|---|
| Analytical correctness | **PASS**, conditional on the conventions now printed (`E = −∇φ`, Voigt factor 2, scaled fields) | every closed form re-derived; `τ_zzz` by inspection (documented gap) |
| Arithmetic correctness | **PASS** | max abs `2.2e-11` (stiffness), max rel `5.8e-5` (print rounding of `301.7 K`); the `R_B` chain to `4.2e-15` |
| Text ↔ implementation | **PASS** | 43 solver-side checks, 0 failures; `model.py` byte-identical |
| Physical interpretation | **PASS with stated limits** | Debye ratio and both entry-ratio statements repaired; four irreducible limits listed in §5 |

Details and the falsification conditions are in
`PAPER_A_ROUND18_CORRECTNESS_VERDICTS.md`.

## 5. What remains open (not repairable by mathematics)

1. **Build unverified.** No TeX engine here, none installable.  Build with:
   ```
   cd Paper_A_Final_Submission
   pdflatex -interaction=nonstopmode -halt-on-error main.tex
   bibtex main
   pdflatex -interaction=nonstopmode -halt-on-error main.tex
   pdflatex -interaction=nonstopmode -halt-on-error main.tex
   ```
   The static validator (`scripts/static_check.py`, PASS, 161 labels / 103
   references / 13 of 13 citations) covers label and macro integrity but cannot
   catch an overfull box, a float placement or a two-column overflow.
2. **Synthetic parameters.** `ℓ = 50 nm`, `f3zz = 1e-9`, and the tabulated
   `|H| = 2×10⁻²³ J m` are illustrative; `H* = 4.01×10⁻²² J m` is an
   order-of-magnitude bound, not a measurement.
3. **Corner line force** is enforced weakly, not pointwise; the edge balance is
   quoted as a residual, not as a pointwise traction.
4. **Novelty against the primary 2025 source** remains open (closed access); only
   a prose comparison exists.
5. **Five author declarations** (funding, data statement, ethics, competing
   interests, author contributions) still await the author.

## 6. Deliverables of this round

| file | content |
|---|---|
| `PAPER_A_ROUND18_FINAL_SUPERVISOR_REVIEW.md` | this file |
| `PAPER_A_ROUND18_PRE_EDIT_AUDIT.md` | Part A: sixteen defects, classified, with evidence |
| `PAPER_A_ROUND18_MATHEMATICAL_REPAIR.md` | Parts B–I: the repair, equation by equation |
| `PAPER_A_ROUND18_INDEPENDENT_RECHECK.md` | Part J: the solver-free reference and its 59 checks |
| `PAPER_A_ROUND18_CORRECTNESS_VERDICTS.md` | the four verdicts, separately argued |
| `PAPER_A_ROUND18_REGRESSION_AND_PACKAGE.md` | suite, static check, archive build |
| `PAPER_A_ROUND18_AUDIT_LOG.txt` | the 43-check log, verbatim |
| `paper_a_study/round18_mathematical_audit.py` | audit script, exit 0 |
| `paper_a_study/round18_reference_checks.py` | reference script, exit 0 |
| `downloads/Paper_A_Complete_Project_round18.zip` | the complete project (see `PACKAGE_SHA256.txt` for size and hash) |

**Structure and style preserved:** introduction continuous, nomenclature intact,
five formulation subsections, three solution subsections, seven results
subsections, one mathematical appendix with six subsections, five limitations, no
new table, no new subsection added to record a repair, no command line in the
manuscript, and no test vocabulary in the prose (enforced by the static
validator, which PASSes).

## 7. Next action

Hand the archive to the supervisor for the LaTeX build and the page-level read.
Nothing further should be changed in this round: the mathematics has been
verified twice from opposite directions, and every remaining item in §5 needs
either a TeX engine, an experimental number or an author decision — none of which
this environment can supply.
