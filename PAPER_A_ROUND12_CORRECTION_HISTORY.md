# Paper A — round 12 correction history

Chronological record of round 12. One line per action, with the evidence that
justified it. The per-edit before/after table is `PAPER_A_ROUND12_EDIT_LEDGER.md`;
this file records the order in which things were done and why.

Baseline and end point: `75d86dc9710d69e2100a85fa5c8b56e9681f7744` (start), branch
`arena/ea7ca4dd-a-paper`. The round-12 commit is recorded in the delivery message
and in `downloads/README.md`.

---

## Phase 0 — session start, before any edit

| # | action | result |
|---|---|---|
| 0.1 | `git fetch` + `git reset --hard origin/arena/ea7ca4dd-a-paper` | local tree equal to remote `75d86dc…`; clean |
| 0.2 | recreate the analysis environment (`python -m venv`, numpy/scipy/matplotlib) | numpy 2.4.6, scipy 1.17.1, matplotlib 3.11.2 |
| 0.3 | check for a TeX engine | none (`pdflatex`, `latexmk`, `tectonic` absent) → **BUILD UNVERIFIED** stands |
| 0.4 | pre-edit gates: `static_check`, `claim_audit`, `test_model`, `mutation_tests`, `phase_speed_audit` | PASS / PASS (23 claims, 46 tokens, 11-11) / 47 tests OK / 15 mutants caught / PASS |

---

## Phase A — the two round-11 reporting defects, corrected first

| # | action | evidence |
|---|---|---|
| A.1 | extract `peak_search.json` at `1ff9166` (round 10) and at `75d86dc` (round 11) with `git show`, and compare the classification block field by field | both records carry the same four fields; no solver run needed |
| A.2 | compute the like-for-like differences at each of the two wavenumbers | $7.54\times10^{-10}$ relative at $k_xd=0.52752$, $1.00\times10^{-10}$ at $0.5275$ |
| A.3 | reproduce the round-11 number and identify what it actually measures | $1.4568\times10^{-7}$ = argmax of one run vs reported sample of the other = `offset_reported_vs_argmax` $1.372\times10^{-7}$ at the printed precision |
| A.4 | establish what $8.36\times10^{-6}$ measures | `restart_spread` = coarse-raster argmax (0.9467870061 at $k_xd=0.527$) vs refined maximum, relative $8.69\times10^{-6}$ |
| A.5 | establish what the tracking-path spread is | $0.0$: ascending (31 points), descending (31 points) and single-step paths return the identical $R_B$ and $\omega$ |
| A.6 | look for a larger population of repeats inside the delivery | each certified configuration is evaluated twice (degree sweep and quadrature sweep); the pair agrees to $\sim10^{-10}$; no larger set exists |
| A.7 | write `PAPER_A_ROUND12_PRELIMINARY_EVIDENCE_CORRECTIONS.md` | the six diagnostics tabulated separately; nothing else touched |
| A.8 | annotate `PAPER_A_ROUND11_NUMERICAL_REPRODUCIBILITY.md` (headline table, §3 bound table) and `PAPER_A_ROUND11_FINAL_TECHNICAL_READINESS.md` (stability row) | corrections visible in place, old pairings quoted so the record stays auditable |

Phase A changed no manuscript text, because no manuscript sentence depended on
either defect — verified by reading every occurrence of `10^{-6}`, `10^{-7}`,
`tracking` and `restart` in `Paper_A_Final_Submission/`.

---

## Phase B — reading and auditing the manuscript

Read in full, in this order: `main.tex`; §1 introduction; §2 governing equations;
§3 solution method; §4 results; §5 discussion; §6 conclusions; appendix. Each
section was read with the stored records open beside it, against the eight-point
checklist of `PAPER_A_ROUND12_SECTION_BY_SECTION_REVIEW.md` §0.

Every number was then traced to a record: 61 matched, 20 did not, 2 had no source at
all, 1 belongs to a frozen figure instead of the text
(`PAPER_A_ROUND12_NUMERICAL_TRACEABILITY_AUDIT.md`).

---

## Phase C — corrections

| # | id | file | correction | category |
|---|---|---|---|---|
| C.1 | L12-01 | results §4.1 | phase-speed endpoints restored to their abscissae (105.8 km/s at $k_xd=0.15$, 20.0 at 1.05) | NUMERICAL CONSISTENCY |
| C.2 | L12-02 | results §4.1 | linewidth ordering in $H$ replaced by the asymmetry the data show; attenuation peak distinguished from the sampled maximum | NUMERICAL CONSISTENCY |
| C.3 | L12-03 | results §4.4 | 30.4/10.5 GHz stated as the family's span, not one branch's | NUMERICAL CONSISTENCY |
| C.4 | L12-04 | results §4.4 | gradient-length abscissae 0.15/1.05 → 0.145/1.00 (the solved grid) | NUMERICAL CONSISTENCY |
| C.5 | L12-05 | results §4.3 | density factors nine and ten, mobility factor five → three, three, three; the two sweeps identified as the same sweep | NUMERICAL CONSISTENCY |
| C.6 | L12-06 | results §4.3 | "reflectance" → "backward share"; panel (c) tail restated ($<10^{-7}$ beyond 0.8, $1.6\times10^{-11}$ at 0.9) | NOTATION |
| C.7 | L12-07 | results §4.6 | the untraceable $1.8\times10^{-12}\to5.6\times10^{-6}$ pair and the $\pm6\times10^{-6}$ bound replaced by the registered spreads | EVIDENCE TRACEABILITY |
| C.8 | L12-08 | results §4.7 | "below the reproducibility of the frequency map" → "a difference between two abscissae, not between two runs" | EVIDENCE TRACEABILITY |
| C.9 | L12-09 | results §4.9 | five closure numbers corrected to the stored ones; the factor two between the four printed numbers and the identity explained | NUMERICAL CONSISTENCY |
| C.10 | L12-10 | results §4.11 | distance-from-edge symbol $\ell$ → $L$ | NOTATION |
| C.11 | L12-11 | results §4.11 | "falls by a factor of three" → the two stored attenuation lengths (0.54 and 0.30 mm against 18.5 mm) | NUMERICAL CONSISTENCY |
| C.12 | L12-12 | results, fig06 caption | "$L$" removed from the attenuation length; $\alpha_i$/$\alpha_B$ named as in the panel | NOTATION |
| C.13 | L12-13 | results §4.14 | residual/tolerance attribution corrected; energy-balance range 2×10⁻¹⁵–4×10⁻¹² | NUMERICAL CONSISTENCY |
| C.14 | L12-14 | results §4.15 | $\vect{k}_B\propto(0.333,-0.530)$ → $(1,0.529)$; the flux-opposite-to-phase statement made explicit | MATHEMATICAL CORRECTNESS |
| C.15 | L12-15 | numerical methods §3.1 | "three-term polynomial" → "polynomial of degree four" | MATHEMATICAL CORRECTNESS |
| C.16 | L12-16 | governing §2.7, `tab:groups` | $\alpha$ → $\alpha_{\mathrm{d}}$ with a one-sentence disambiguation, and the dissipation integral labelled as scaled | NOTATION |
| C.17 | L12-17 | discussion §5.5 | "Five limitations" → "Six limitations" | NUMERICAL CONSISTENCY |
| C.18 | L12-18 | appendix | 39 → 47 tests (three places), ~9 s → ~25 s, twelve → eleven data files | NUMERICAL CONSISTENCY |
| C.19 | L12-19 | `main.tex` abstract | "The figure" → "The reported number"; "unchanged" → "almost unchanged"; "the backward mode" → "the two partner modes" | LANGUAGE |

Every correction was made against a named record. None of them touched an equation,
a constant, a boundary condition, a solver file, a dataset or a figure PDF.

---

## Phase D — verification after the corrections

| # | gate | result |
|---|---|---|
| D.1 | `python -m unittest paper_a_study.test_model` | `Ran 47 tests in 21.450s` — OK |
| D.2 | `python paper_a_study/claim_audit.py` | 23 claims, 46 tokens, 5 deprecated guarded, 10 figures in order, 11/11 source rows — PASS |
| D.3 | `python paper_a_study/mutation_tests.py` | 15 mutants, all caught — PASS |
| D.4 | `python paper_a_study/phase_speed_audit.py` | PASS (exit 0) |
| D.5 | `python Paper_A_Final_Submission/scripts/static_check.py` | 104 labels, 75 references, 13 citation keys, 13 bib entries — PASS; word count 16 634 |
| D.6 | LaTeX build | not executed: no engine — **BUILD UNVERIFIED** |
| D.7 | full battery | not re-executed: no producer, dataset or solver file changed in this round; the round-11 log remains the last full execution (18 PASS / 0 FAIL / 1 SKIP) |

Two side-effect records changed, as intended: `static_validation.txt` (word count)
and `figure_data/claim_audit.json` (the count of 10⁻⁸ bound tokens, 7 → 8, because
§4.6 now states the bound explicitly).

---

## Phase E — packaging

| # | action |
|---|---|
| E.1 | `build_submission_package.py`: refresh `Paper_A_Final_Submission/` from the generator tree, rewrite `MANIFEST.json` |
| E.2 | `make_download_archive.py`: round-12 reports added to `ROOT_REPORTS`, stage and archive names moved to round 12, `START_HERE.txt` rewritten for this round |
| E.3 | `downloads/README.md`: round 12 as current, round 11 moved into the superseded table with its size and SHA-256 |
| E.4 | `unzip -t`, extraction to a scratch directory, `MANIFEST.json` re-hash, single-`main.tex` check, `static_check` on the extracted tree |
| E.5 | commit and push to `arena/ea7ca4dd-a-paper` only |

---

## Not superseded by this round

The governing equations, the constitutive constants, the boundary conditions
(including the corner line force), the solver, the discretisation, the material
data, all ten figure PDFs, all datasets, and every reported number: 2.31456 %,
94.6795 % at $k_xd=0.5275$ / 0.52752, 16.6547 GHz, 0.9855722 at the edge plane,
99.77 % propagating, 62.2973 % at $k_xd=0.5275$ with $H/H^{*}=+0.05$, the
34.2 / 11.1 / 1.21 % coupling decomposition, and the four certified values with
their spreads.  *(Corrected in round 13: this sentence first attached 62.2973 % to
$k_xd=0.55$, the wrong abscissa. The value is `mechanism_controls.json` →
`refined_peak.full.R_B`, i.e. the refined peak at $H/H^{*}=+0.05$; at
$k_xd=0.55$ the coupling-on share is 0.5221071 and the coupling-off share is
0.5791800. The manuscript was correct throughout — §4.10 attaches 0.6230 to
"the maximum".)*

Also unchanged in status: the prior-art comparison **UNRESOLVED**, the corner field
**unresolved**, $\ell$, $f$, $H$ **synthetic**, the maximum **local**, the typeset
article **BUILD UNVERIFIED**, and the article **not submission-ready** — the last
for the two non-editorial reasons in `PAPER_A_ROUND12_READINESS_ASSESSMENT.md` §2,
not for anything this round could fix.
