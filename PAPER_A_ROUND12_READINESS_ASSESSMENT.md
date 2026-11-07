# Paper A — round 12: readiness assessment

Two readiness questions, answered separately, because they have different answers
and different owners. Nothing in this document changes either answer by being
written down.

Baseline `75d86dc9710d69e2100a85fa5c8b56e9681f7744`; every gate below was run on
the edited tree of this round.

> **Round-13 status (added 2026-11-07, text below unchanged).** The one numerical
> blemish recorded here — fig10(c) — is closed, and the test suite has grown from 47
> to 52 checks. The scientific verdict of §2 (**NOT READY**, for the prior-art question
> and the author declarations) is unchanged: round 13 closes defects, not questions.
> The current assessment is `PAPER_A_ROUND13_SUPERVISOR_HANDOFF.md`.

---

## 1. Numerical readiness — **PASS**, with one carried figure defect

### 1.1 What was executed in this round

| gate | command | result |
|---|---|---|
| unit and scientific tests | `python -m unittest paper_a_study.test_model` | `Ran 47 tests in 21.450s` — **OK** |
| claim registry and stale guard | `python paper_a_study/claim_audit.py` | 23 claims, 46 tokens, 5 deprecated values guarded, 10 figures in first-citation order, 11/11 source-agreement rows — **PASS** |
| gate mutation tests | `python paper_a_study/mutation_tests.py` | 15 mutants, all caught — **PASS** |
| manuscript/solver consistency for §2.6 | `python paper_a_study/phase_speed_audit.py` | **PASS** (exit 0) |
| LaTeX static validation | `python Paper_A_Final_Submission/scripts/static_check.py` | 8 files, 104 labels, 75 references, 13 citation keys, 13 bib entries — **PASS** |
| LaTeX build | `pdflatex` / `latexmk` / `tectonic` | **not executed: no TeX engine in this environment** |

Not re-executed, and why: the 18-gate battery (`run_all_checks.py`) regenerates every
dataset from an empty directory in about 13 minutes. This round touches no producer,
no data file and no solver file, so re-running it would re-measure the round-11
state, not this round's. The last full execution remains
`validation/verification_log.txt` / `validation/round11_battery_run_clean_reproduction.log`:
**18 PASS / 0 FAIL / 1 SKIP, `OVERALL: PASS`**, the skip being the LaTeX build.

### 1.2 What the numbers rest on

| layer | evidence |
|---|---|
| determinism of the solve | 47 tests, including plane invariance to 2×10⁻¹⁶ and the cross-script edge-fraction identity |
| the maximum | three-stage raster, two independent restarts returning the same sample, four degrees, four quadrature rules, three tracking paths identical |
| the reported uncertainties | degree 5.6×10⁻⁹ / 6.2×10⁻⁹, quadrature 4.3×10⁻¹⁰, restart sampling 8.36×10⁻⁶ (all below the registered 10⁻⁸ bound except the last, which is a sampling error and is not registered as a bound) |
| fixed-configuration reproducibility | 7.5×10⁻¹⁰ and 1.0×10⁻¹⁰ relative across two full data builds (round 10 → round 11), and ~10⁻¹⁰ between the paired evaluations stored inside one delivery |
| the manuscript agrees with the records | 20 printed numbers corrected this round and 61 confirmed; the registry gate passes |
| the figures agree with the datasets | round-11 figure-by-figure audit (40 panels) plus 8 provenance tests that now run inside the 47 |

### 1.3 The one thing numerically not clean

**B1**: the frozen panel fig10(c) draws the backward wavenumber along
$(0.333,-0.530)$, i.e. 58° below the $+x$ axis; the solved wavenumber points 27.9°
above it. The prose no longer repeats the wrong vector, so the manuscript text is
consistent with the data and the *figure* is not. This is a rendering defect of one
arrow in one schematic panel. It does not affect any number, and it cannot be fixed
inside this round because figure code and accepted figure PDFs are frozen.

Verdict on numerical readiness: **PASS for the numbers; one figure annotation
defect open (B1).**

---

## 2. Scientific and originality readiness — **NOT READY**

This is the part the numbers cannot answer.

| question a referee will ask | state | evidence |
|---|---|---|
| Is the added carrier–strain-gradient enthalpy in the primary 2025 theory? | **UNRESOLVED** | the IJES 208, 104165 article is closed access, no preprint or repository copy is indexed, and the comparison is made against the free-energy decomposition reproduced in an open-access computational paper (Hu et al., Eqs. 4a–4e). §5.3 and `tab:novelty` say so, and no priority claim is made |
| Is the effect new, or is it the known backward branch of a strain-gradient plate with a new loss term? | **partly answered, in the paper's favour** | §3.7: the conversion is present with $H=0$, removed with $\ell=0$, and the coupling moves it by 1.21 % at the operating point and 34.2 % at the fold. The paper therefore claims a scattering calculation and a quantified modifier, not a new mechanism |
| Is the observable measurable? | **argued, not demonstrated** | §5.1 argues that a total-reflectance measurement sees unity everywhere and that modal resolution is required. No experimental configuration, tolerance or error budget is proposed |
| Is the parameter set physical? | **no, and the paper says so** | $\ell$, $f_{3zz}$, $H_{jkl}$ are synthetic; $H$ is fixed by the positivity bound, not by a specimen; $T$ follows from the Einstein relation |
| Is the geometry realistic? | **no, and the paper says so** | 2.5D, one edge, no second edge, no three-dimensional corner; corner line force unresolved pointwise (**B3**) |
| Are the transport assumptions appropriate? | **stated, with an explicit bound** | linearised drift–diffusion about uniform doping and zero bias; $Q=d/L_D=0.075<1$ is quoted both as the reason the perturbation is not surface-confined and as the limit of the model |
| Can a referee reproduce it? | **yes, better than most** | package, datasets, scripts, logs, SHA-256 manifest, ordered recipe, exit-status contract, and this round's corrections make the prose match the records |
| Is the typeset article verified? | **no** | **BUILD UNVERIFIED** (**B4**) |
| Are the declarations complete? | **no** | five `AUTHOR INPUT REQUIRED` items (**B5**) |

Verdict on scientific and originality readiness: **NOT READY.** The paper is
publishable in substance only after (i) the prior-art question is settled with the
primary source in hand, and (ii) the author supplies the declarations. Neither is an
editorial task, and neither was attempted here.

---

## 3. The six diagnostics, in one place

| # | diagnostic | value | where it lives | what it does **not** mean |
|---|---|---|---|---|
| 1 | tracking-path sensitivity | 0.0 (three paths identical) | `verdict.tracking_path_relative_spread` | it does not mean the answer is insensitive to the branch — only that the tracking order does not matter |
| 2 | coarse-search sampling error | 8.36×10⁻⁶ absolute (8.69×10⁻⁶ relative) | `classification.gain_over_coarse`, `verdict.restart_spread` | it is not a discretisation error and not jitter |
| 3 | restart / bracketing comparison | both brackets → same interval, same sample | `restarts[]` | it validates the bracket, not the refinement |
| 4 | Galerkin-degree convergence | 5.6×10⁻⁹ (argmax), 6.2×10⁻⁹ (reported) | `verdict.degree_spread` | it does not bound the error in the physical model |
| 5 | quadrature convergence | 4.3×10⁻¹⁰ (degree 22, four rules) | `verdict.quadrature_spread` | as above |
| 6 | fixed-configuration run-to-run | 7.5×10⁻¹⁰ / 1.0×10⁻¹⁰ relative, round 10 → 11 | cross-commit comparison (Part A) | it is only two builds; no larger set of repeats exists in the package |

Two round-11 statements confused these (Part A). The manuscript now cites
diagnostics 1, 4 and 5 in §4.6 and 2, 3 in §4.7, and nothing else.

---

## 4. Status vocabulary

| label | applied to |
|---|---|
| **PASS** | the numerical gates above; the manuscript/record agreement after this round |
| **MINOR REVISION** | the manuscript's prose state at the start of this round — 19 defects, none touching a result |
| **UNVERIFIED** | the typeset build; the prior-art comparison; the pointwise corner field |
| **BLOCKED** | fig10(c) (B1); the declarations (B5) until the author answers |
| **not submission-ready** | the article as a whole, for the reasons in §2 |

---

## 5. What a referee would still ask, and where the answer is

| likely request | answer available now |
|---|---|
| "Show that the share is not an artefact of a small denominator." | §4.8: 128× incident-flux drop, three tracking paths identical, degree/quadrature spreads, mode overlap 0.999995, second candidate 2.0$\lvert k_x\rvert$ away |
| "Is this a global maximum?" | No — §4.7: local, within a declared window, flat top ±0.0009 |
| "Why call it a share and not a reflectance?" | §3.3, §4.8, §5.1: 94.68 % modal versus 99.77 % propagating; the interference term is quoted separately |
| "What happens at the edge plane?" | §4.8 and `tab:configurations`: 0.9856 at the maximum, 0.0232 at the operating point |
| "Why is the coupling not the story?" | §4.10, §4.12, §5.2: 1.21 % at the operating point against a 1.35 factor in $k_y$, and the 34.2 % at the fold is mostly propagation loss (23.1 of 34.2 points) |
| "Is the flexoelectric term doing anything?" | §4.2: −0.012 % at the operating point, and the paper declines to attribute the effect to it |
| "Can I reproduce table 1?" | appendix: `certify_peak.py`, the four fixed wavenumbers, the stored `peak_certification.json` |
| "Where is the build?" | nowhere: **B4** |
