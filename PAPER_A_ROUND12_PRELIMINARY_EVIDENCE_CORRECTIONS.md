# Paper A — round 12, Part A: preliminary evidence corrections

**Status of this document.** Written and applied **before** any manuscript edit, as
instructed. It concerns two numerical statements in the round-11 reports, not the
manuscript, not the model and not the data.

Baseline at the start of round 12: `75d86dc9710d69e2100a85fa5c8b56e9681f7744`
(`arena/ea7ca4dd-a-paper`, tree clean, remote HEAD equal to local HEAD).
Round-11 data commit used for the comparison: `1ff9166` (round 10 delivered tree).

---

## 1. What was checked, and how

The two round-11 reports made quantitative statements about *reproducibility*. Both
were re-derived from the delivered records rather than from the reports:

```
git show 1ff9166:paper_a_study/figure_data/peak_search.json
git show 75d86dc:paper_a_study/figure_data/peak_search.json
```

The fields used are `classification.K_at_max`, `classification.R_B_at_max`,
`classification.K_reported`, `classification.R_B_reported`,
`classification.offset_reported_vs_argmax`, `classification.gain_over_coarse`,
`verdict.degree_spread`, `verdict.quadrature_spread`,
`verdict.tracking_path_relative_spread`, `verdict.restart_spread`, and the
per-path `tracking_path.paths.*` records. No solver run was performed for Part A.

---

## 2. Defect A-1 — the jitter was measured between two different wavenumbers

### What round 11 said

`PAPER_A_ROUND11_NUMERICAL_REPRODUCIBILITY.md`, headline table:

| quantity | round 10 | round 11 | difference |
|---|---|---|---|
| $R_B$ at the certified maximum | 0.9467953685099261 | 0.9467952305821763 | $1.5\times10^{-7}$ |

followed by "The $1.5\times10^{-7}$ movement is the solver's reproducible jitter".
The same pairing appears as a row of
`PAPER_A_ROUND11_FINAL_TECHNICAL_READINESS.md`.

### Why it is wrong

The two numbers are not the same configuration:

* `0.9467953685099261` is `R_B_at_max` at $k_xd=0.52752$;
* `0.9467952305821763` is `R_B_reported` at $k_xd=0.5275$.

Their difference is the stored `offset_reported_vs_argmax` = $1.372\times10^{-7}$,
i.e. the difference between two abscissae 2 × 10⁻⁵ apart on a branch whose top is
flat to 0.01 percentage point. It is not a change between runs.

### Like-for-like values (both commits, same configuration)

| quantity | round 10 (`1ff9166`) | round 11 (`75d86dc`) | absolute | relative |
|---|---|---|---|---|
| $R_B$ at the argmax, $k_xd=0.52752$ | 0.9467953685099261 | 0.9467953677961777 | $7.137\times10^{-10}$ | $7.539\times10^{-10}$ |
| $R_B$ at the reported sample, $k_xd=0.5275$ | 0.9467952306769204 | 0.9467952305821763 | $9.474\times10^{-11}$ | $1.001\times10^{-10}$ |
| $k_xd$ at the argmax | 0.52752 | 0.52752 | 0 | 0 |
| classification | `certified_local_maximum` | `certified_local_maximum` | — | — |

So the true run-to-run movement is $7.5\times10^{-10}$ and $1.0\times10^{-10}$
relative — four to five orders of magnitude smaller than the number the round-11
report published. Neither movement reaches the seventh printed digit, which is why
no manuscript number changed in round 11 or in this round.

### Independent confirmation inside one delivery

Both delivered trees store **two independent evaluations of every certified
configuration**: one in the Galerkin-degree sweep and one in the quadrature sweep
(`peak_certification.json`, `peak_search.json` `degree[]` and `quadrature[]`).
Within the round-11 delivery the two evaluations of the reported configuration
agree to $1\times10^{-10}$ relative, i.e. to the same order as the cross-commit
comparison. Fixed-configuration reproducibility at the $10^{-10}$ level is
therefore *measured in the delivered data*, not inferred from it. No larger
population of repeats exists in `figure_data/`, so nothing stronger than a
$10^{-10}$ bound is claimed.

---

## 3. Defect A-2 — $8.36\times10^{-6}$ was labelled "tracking-path spread"

### What round 11 said

`PAPER_A_ROUND11_NUMERICAL_REPRODUCIBILITY.md`, §3 bound table:

| quantity | value | bound |
|---|---|---|
| tracking-path spread (three paths) | $8.36\times10^{-6}$ (absolute, $R_B$) | reported separately |

### Why it is wrong

`verdict.tracking_path_relative_spread` is **0.0** in both commits, and the three
stored paths return the identical value:

| path | points | $R_B$ | $\omega$ |
|---|---|---|---|
| ascending | 31 | 0.9467952305821763 | 7.619899227279142 |
| descending | 31 | 0.9467952305821763 | 7.619899227279142 |
| single step | 1 | 0.9467952305821763 | 7.619899227279142 |

The number $8.3617\times10^{-6}$ is `verdict.restart_spread`, and its content is:

* every restart is run on a raster of $\Delta k_xd=10^{-3}$ inside its own bracket
  (`[0.520,0.532]`, `[0.524,0.536]`, 13 points each);
* both restarts return the same sample, $k_xd=0.527$, with
  $R_B=0.9467870061383709$;
* the refined maximum is $0.9467953677961777$ at $k_xd=0.52752$;
* the difference is $8.36\times10^{-6}$ absolute, $8.69\times10^{-6}$ relative.

That is the **coarse-search sampling error** of a $10^{-3}$ raster, plus a
**bracketing-agreement** result (both brackets give the same interval and the same
sample). It is not a tracking-path sensitivity.

---

## 4. The six diagnostics, kept separate from now on

The two defects above came from pooling distinct quantities. The delivered data
support six separate statements, and the round-12 reports keep them separate:

| # | diagnostic | stored quantity | value in the round-11 delivery |
|---|---|---|---|
| 1 | tracking-path sensitivity | `verdict.tracking_path_relative_spread` | $0.0$ (three paths identical) |
| 2 | coarse-search sampling error | `classification.gain_over_coarse` / `verdict.restart_spread` | $8.36\times10^{-6}$ absolute, $8.69\times10^{-6}$ relative |
| 3 | restart / bracketing comparison | `restarts[].K`, `restarts[].R_B` | same sample and same value from both brackets |
| 4 | Galerkin-degree convergence | `verdict.degree_spread` | $5.61\times10^{-9}$ (argmax), $6.22\times10^{-9}$ (reported) |
| 5 | quadrature convergence | `verdict.quadrature_spread` | $4.32\times10^{-10}$ (degree 22, grades 64/128/192/256) |
| 6 | fixed-configuration run-to-run reproducibility | cross-commit comparison, §2 above; and the paired evaluations inside one delivery | $7.5\times10^{-10}$ / $1.0\times10^{-10}$ relative |

A seventh quantity belongs to none of these: the sensitivity of $R_B$ to the
frequency at which the spatial problem is solved. It is discussed — and measured —
in `PAPER_A_ROUND12_NUMERICAL_TRACEABILITY_AUDIT.md` §5, because the manuscript
made a numerical claim about it that the delivered records do not contain.

---

## 5. What was changed, and what was not

Edited (reporting only):

| file | change |
|---|---|
| `PAPER_A_ROUND11_NUMERICAL_REPRODUCIBILITY.md` | headline table replaced by two like-for-like rows; the jitter sentence replaced by the corrected comparison; the "tracking-path spread" row split into a tracking-path row (0.0) and a restart row ($8.36\times10^{-6}$), each with a "Corrected in round 12" note |
| `PAPER_A_ROUND11_FINAL_TECHNICAL_READINESS.md` | the "headline is stable across runs" row corrected in place, with the old pairing quoted so the record stays auditable |

Not edited, deliberately:

* no manuscript sentence depended on either defect — checked by reading every
  occurrence of `10^{-6}`, `10^{-7}`, `tracking` and `restart` in
  `Paper_A_Final_Submission/`;
* no dataset, figure, solver file, constant or boundary condition;
* the round-11 reports are otherwise left as issued, so the two corrections are
  visible as annotations rather than as silent rewrites.

One further inconsistency was found while checking the provenance of the same
statements and is **not** repaired here: the module docstring of
`paper_a_study/peak_search.py` still says that the tracking-path sensitivity
"dominates the reproducibility of the printed digits", which the stored zero
contradicts. It is a documentation defect in frozen code, recorded as **B6** in
`PAPER_A_ROUND12_BLOCKING_ISSUES.md` with the exact replacement text.
