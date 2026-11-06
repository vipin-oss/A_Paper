# Paper A — Final scientific correction and Q1 audit

**Title.** Negative reflection of guided waves in a flexoelectric
piezoelectric–semiconductor plate with carrier–strain-gradient coupling

| | |
|---|---|
| Repository | `https://github.com/vipin-oss/A_Paper` |
| Branch | `arena/ea7ca4dd-a-paper` |
| Base commit of this phase | `4b4af80` |
| Date | 2026-11-06 |
| Manuscript | `Paper_A_LaTeX/main.tex` (+ `sections/`) |
| Submission package | `Paper_A_Submission_2026-11-06/` and `.zip` |
| Compilation | **UNVERIFIED** — no TeX engine in the authoring environment |
| Static validation | **PASS** (`Paper_A_LaTeX/static_validation.txt`) |
| Verification suite | **18/18 OK** in 7.9 s, reproduced from a clean extraction |

---

## 1. Summary

This phase completed the manuscript and closed the four open scientific
questions of the previous phase.  Ten audit items were examined; six were
confirmed defects and have been corrected, one was incorrect as stated, one is
unresolved and is declared as such, and two were confirmed in the solver but
misstated in the prose.

| Item | Subject | Classification | Action |
|---|---|---|---|
| A | Grounded vs open-circuit boundary conditions | **CONFIRMED** (manuscript) | labels and BC block rewritten from the solver |
| B | Complete formulation, geometry, reciprocity | **CONFIRMED** | formulation rewritten; terminology corrected to Fourier-reduced 3-D |
| C | Fig. 5 energy identity | **CONFIRMED** (3 real bugs) | identity rebuilt; closure `~1` → `3.8e-16` |
| D | Certification of 2.315 % and 57.92 % | **INCORRECT** (the concern) | both certified across degree 18→30 |
| E | `v_p`, `v_g`, `v_E` definitions and signs | **CONFIRMED** | definitions separated; sign change attributed to `v_g`, `v_E` only |
| F | Validation, residuals, route independence | **CONFIRMED** (partly) | two routes labelled as consistency, independent checks separated |
| G | Material provenance | **CONFIRMED** | provenance table added; synthetic parameters marked |
| H | Novelty vs Qu et al. and Fang & Wei | **UNRESOLVED** | declared unresolved; no priority claim |
| I | Reproducibility of the package | **CONFIRMED** | package rebuilt and re-run from a clean extraction |
| J | LaTeX defects | **CONFIRMED** | preamble fixed; source statically validated; not compiled |

The two headline numbers survive every check applied to them.  No conclusion had
to be withdrawn.

---

## 2. Item-by-item audit

### Item A — grounded vs open-circuit boundary conditions

**Issue as reported.** The manuscript may have swapped the grounded and
open-circuit electrical conditions, and may have conflated the surface, edge and
corner conditions.

**Classification: CONFIRMED, in the manuscript only.  The solver was always
correct.**

**Location.** `Paper_A_LaTeX/sections/governing_equations.tex` (previous
version, boundary-condition block); authoritative behaviour in
`paper_a_study/model.py` lines 56–61 and 71–80.

**Evidence.** The solver states its own convention in a comment (`model.py`
lines 57–60) and implements it:

```python
# 'ground' enforces phi=0 on both faces (two constraints).  For the
# open-circuit case the constant potential mode is a null vector;
# removing it (zero-mean gauge) is required for a non-singular system.
self.np = self.n-2 if electric=='ground' else self.n-1
...
if self.electric=='ground':
    ratio = np.sqrt((2*np.arange(self.np)+1)/(2*np.arange(self.np)+5))
    pb = [v[:,:self.np] - v[:,2:]*ratio[None,:] for v in b]   # phi(+-1)=0
elif self.electric=='open':
    pb = [v[:,1:] for v in b]                                  # constant mode dropped
```

So `ground` ⇒ `φ = 0` on **both** faces, essential, `np = n-2`; `open` ⇒
natural `D_z = 0`, gauge removed, `np = n-1`.  The previous section text had
the two labels the other way round and omitted the shear traction, the double
traction and the carrier-blocking conditions.

**Correction.** The boundary-condition subsection now states, separately for the
plate faces `z = ±d/2`, the reflecting edge `x = 0` and the radiation condition:
`σ_{iz} = 0`, `τ_{ijz} = 0` and `J_z = 0` on the faces; `φ = 0` (grounded, eq.
`bc_grounded`) or `D_z = 0` (open, eq. `bc_open`); `σ_{ix} = 0`, `τ_{ijx} = 0`,
`D_x = 0`, `J_x = 0` at the edge.  The text states explicitly that the earlier
version interchanged the labels and that the solver never did.

**Validating test.** `test_independent_classical_grounded_and_open` and
`test_independent_nonzero_f_H_temporal` integrate an eight-state and a
twelve-state strong-form system whose boundary rows are coded independently
(`model.py` lines 390 and 472) and match the spectral frequencies to `1e-10`
for **both** electrical cases.  `test_independent_weak_corner_reconstruction`
asserts `grounded_phi_max < 1e-10` and `edge_double_traction_rms < 1e-10`.

**Remaining limitation.** The corner at `x = 0, z = ±d/2` carries a weak line
force that the discretisation does not resolve; the test asserts
`corner_line_force_max > 1e-4` deliberately, and the paper does not claim a
resolved pointwise corner traction.

**Status: CORRECTED.**

---

### Item B — completeness and correctness of the formulation

**Issue as reported.** The formulation must be complete (enthalpy, kinematics,
conjugates, hyperstress, `D`, electrochemical potential, flux, balances, BCs,
power flux), reciprocal, dimensionally consistent and thermodynamically stable,
and the true geometry must be stated.

**Classification: CONFIRMED.**  The previous section was incomplete and used the
wrong geometric label.

**Location.** `sections/governing_equations.tex`, rewritten in full.

**Evidence and corrections.**

*Geometry.* The solver retains `u_x, u_y, u_z`, all six strain components and a
single conserved `k_y` (`model.py`, `state_operator`, `matrices(A, omega)` take
both `K` and `ky`).  It is therefore a **Fourier-reduced three-dimensional**
formulation, not plane strain.  The manuscript now says exactly that and
explains why the plane-strain label would misdescribe the solver.

*Reciprocity.* The enthalpy
`H = ½ε:c:ε + ½∇ε:A:∇ε − ½E:κ:E − e:ε·E − a(Δn)²/2 + H Δn:∇ε − f E:∇ε`
gives `σ = c:ε − e·E`, `τ = A:∇ε + H Δn − f E`,
`D = κ·E + e:ε + f:∇ε`, `μ̃ = a Δn + H:∇ε`.  The Maxwell relation
`∂²H/∂(Δn)∂∇ε = ∂²H/∂∇ε∂(Δn) = H` holds identically, which is what the pair
`Δτ = H Δn`, `Δμ̃ = H ∇ε` expresses.  Reciprocity is verified numerically at
`±k_y` to `1e-13` (`test_reciprocity_at_oblique_wavenumber`), including the `H`
term, which is the non-trivial part.

*Stability.* The enthalpy is positive definite only if the Schur complement
condition `H²(c⁻¹)₃₃/(ℓ²a) < 1` holds.  The solver enforces it and raises
`ValueError` outside it (`test_material_units_and_schur` asserts the raise at
`H = 2e-21`).  All reported couplings satisfy it with a margin of twenty.

*Units.* `test_material_units_and_schur` checks `D/μ = 0.026 V` (i.e.
`k_BT/q` at 300 K) and `c_s = 2746.608754 m/s`; `test_H_changes_only_prescribed_constitutive_terms`
verifies that switching on `H` changes `τ_zz` by exactly `h·N` and leaves `σ`,
`D` and `N` unchanged to `2e-12`.

*One residual asymmetry, declared.* The flexoelectric term `−f E:∇ε` produces
the direct effect in `D` and the converse effect in `σ` only through `∇E`, which
is not an independent variable here.  The manuscript states that the retained
flexoelectric coupling is the direct one and that the electric-field-gradient
terms are not resolved; this is a stated modelling choice, not a hidden one.

**Status: CORRECTED.**

---

### Item C — Fig. 5 energy identity

**Issue as reported.** The channels of the edge energy balance are not
automatically independent or additive; the figure may have mixed transported,
reactive and interference contributions.

**Classification: CONFIRMED.  Three genuine implementation bugs were found and
fixed.**  This was the most serious defect of the phase, because it produced a
plausible-looking figure from a wrong identity.

**Location.** `paper_a_study/build_figure_data.py`, function `fig05`
(lines of the decay weighting, the evanescent sum and the closure residual).

**Evidence (before correction).**

1. The modal propagation factor used `L = REF_NORM * p.d`, but `REF_NORM = 10`
   is already expressed in plate thicknesses (2 µm at `d = 200 nm`).  Every mode
   was therefore propagated ten times too far, and a spurious reactive
   remainder of `4e-5` survived at the reference plane.
2. The "evanescent reactive fraction" was summed with the same wrong weighting,
   so it inherited the error.
3. The closure residual was constructed from `edge_power` instead of from the
   left-hand side of the identity
   `P_inc + Σ_j P_j + P_cross = P_edge − P_diss`, and consequently evaluated to
   order unity even when the physics was right.

**Correction.** `L = REF_NORM`; the evanescent sum recomputed with the correct
factor; the residual built from `total_power_left = P_inc + Σ_j P_j + P_cross`.
The figure was then rewritten as four panels that state the physics the identity
actually supports: (a) the partition of the incident power at `H = 0` on a
logarithmic axis, (b) the four fractions against `H/H*`, (c) the power-balance
error against the `1e-6` acceptance line, (d) the relative change of the
backward channel.

**Evidence (after correction).** At `H = 0`: backward `2.3146e-2`, other
propagating outgoing `0.9767`, dissipated `1.99e-4`, interference `-4.17e-6`,
evanescent content `≤ 6.2e-28`, **closure residual `≤ 3.8e-16`**, solver power
balance `4.5e-13 … 2.1e-12`.

**Validating test.** `test_interference_inclusive_finite_volume_power` requires
`power_balance_relative < 1e-9` and `|edge_power| < 1e-10` for
`L = 2d, 10d, 30d`, and asserts that the cross term is non-zero
(`|P_cross| > 1e-8`) so that the interference term cannot be silently zeroed.
`test_temporal_energy_dissipation_balance` requires `relative_balance < 5e-6`
with a positive dissipation for `H = 0, ±H_test`.

**Remaining limitation.** The reactive content is only meaningful at the edge
plane; at the reference plane it is `O(10⁻²⁸)` and is reported as such rather
than being added to the transported budget.

**Status: CORRECTED.**

---

### Item D — certification of the 2.315 % and 57.92 % values

**Issue as reported.** The operating-point return and the `~58 %` peak must be
independently re-verified; if the peak cannot be certified it must be excluded
from the conclusions.

**Classification: INCORRECT — as a concern.**  Both values certify.

**Location.** `paper_a_study/certify_peak.py` (new),
`paper_a_study/figure_data/peak_certification.json`.

**Evidence.** Four cases re-solved at Galerkin degrees 18, 22, 26 and 30 with
identical physics:

| case | `k_xd` | `R_B` (degree 30, 2 µm plane) | `θ_E` (deg) | max rel. change 18→30 | edge condition | residual |
|---|---|---|---|---|---|---|
| operating point | 0.7362 | 0.023145624251493125 | −27.8997 | 7.21e-07 | 1.6e+02 | ≤1e-12 |
| peak candidate | 0.5500 | 0.579180058557786 | −14.4487 | 1.46e-07 | 1.6e+02 | ≤1e-12 |
| lower flank | 0.5250 | 0.9318914858855936 | −13.8888 | 2.06e-08 | 1.6e+02 | ≤1e-12 |
| upper flank | 0.5750 | 0.3486943696944105 | −15.2297 | 2.62e-07 | 1.6e+02 | ≤1e-12 |

The backward mode's self-power is negative in every case
(`-0.9998 … -0.9900`), which confirms it is outgoing; `|cos θ_E|` is
`0.884 / 0.968 / 0.971 / 0.965`, so the measured projection is resolved.  The
branch-tracked sweep and the independent density sweep agree at the peak to
`7e-4` relative (`0.579180` vs `0.579593`).

**Correction to the manuscript.** A peak subsection was added
(`sec:results_peak`, Table 3) and the abstract quotes the refinement figures.
The peak is retained in the conclusions.

**Admissibility rule.** The previous gate `|angle| < 80°` was a plotting
threshold and has been removed (`certified_backward` in
`build_figure_data.py`, `admissible()` in `reclassify_csv.py`).  It is replaced
by the conservation bound `0 ≤ R_B ≤ 1 + |P_cross|/P_inc` (with a `1e-2` cross
bound justified by the measured `1e-3…1e-2` interference) together with
`power_balance_error < 1e-6` and `edge_scaled_residual < 1e-8`.  The energy
angle is retained as a **diagnostic** (`x_flux_fraction`) and never as a gate.
Re-deriving the flags under the new rule changed 30 of 130 rows in Fig. 2
(100 → 130 admissible) and none in Figs. 4 and 7 (50/50 and 95/95).

**Remaining limitation.** The certification covers degrees and the admissibility
criteria; it does not constitute an experimental validation of the synthetic
coupling, which is stated in §6.

**Status: VERIFIED / NO CHANGE NEEDED to the numbers.**

---

### Item E — the three velocities

**Issue as reported.** `v_p`, `v_g` and `v_E` must be defined with units,
signs, complex conventions and directions; a positive magnitude does not change
sign; negative reflection must not be inferred from a dispersion slope.

**Classification: CONFIRMED.**  The previous text plotted three quantities on
one axis and read a sign change as evidence of negative reflection.

**Location.** `sections/results.tex`, subsection `sec:results_dispersion`.

**Correction.** The three definitions are now given separately:
`v_p = ω/|k|` (a magnitude, right axis, monotone, never signed),
`v_g = c_s ∂ω/∂k_x` and `v_E = P_x/E` (both signed, left axis, agreeing to
`< 3.5 %`).  The text states that the sign change at `k_xd ≈ 0.55` belongs to
`v_g` and `v_E`, that `v_p` cannot change sign, and that **a backward branch is
not by itself evidence of negative reflection** — the branch exists in the
infinite plate; the edge creates the conversion.

**Evidence.** Fig. 1(b): `v_p ∈ [20.0, 105.8] km/s` (all positive);
`v_g ∈ [−187.8, +1097.3] m/s`; `v_E ∈ [−188.8, +1136.3] m/s`.  Ties to the
operating-point regression value `K0 = 0.7362`, `ω = 7.6334`.

**Status: CORRECTED.**

---

### Item F — validation, residuals and route independence

**Issue as reported.** Residuals, boundary-condition residuals, modal
convergence, energy conservation, reflection coefficients, backward
classification, complex-root stability, attenuation direction, turning points,
limiting cases and uncertainty must be reassessed; the two solution routes must
not be presented as independent physical validation.

**Classification: CONFIRMED, in part.**  The checks existed and passed; the
prose over-sold them.

**Location.** `sections/numerical_methods.tex`
(`sec:numerics_verification`), `sections/results.tex`
(`sec:results_validation`).

**Evidence (current, all reproduced from a clean extraction).**

| Check | Result |
|---|---|
| verification suite | 18/18 OK, 7.9 s |
| exact classical SH modes | `1e-9` |
| exact strain-gradient fundamental SH | `1e-10` |
| independent classical strong form (grounded **and** open) | `1e-10` |
| independent gradient strong form with `f`, `H ≠ 0` | `1e-10` |
| independent `C¹` finite-element plate → spectral edge result | monotone, `< 3e-5` |
| strong-form residuals (momentum, Gauss, carrier, traction, double traction, blocking) | `< 1e-8` |
| scaled edge residual | `≤ 1e-12` |
| reciprocity at `±k_y` | `1e-13` |
| degree convergence 18→30 | `≤ 7.2e-7` |
| energy-identity closure | `3.8e-16` |
| singular edge system | rejected with an error |

**Correction.** The temporal/spatial agreement (`2e-5`) is now described as an
implementation consistency check, explicitly **not** an independent physical
validation, and the genuinely independent checks (strong-form propagators,
`C¹` FE plate) are listed as such.  The singular-system rejection is reported as
a test rather than described as a robustness claim.

**Remaining limitation.** There is no experimental data and no comparison with
an independent research group's numbers; the verification is internal
consistency plus exact limits.  This is stated in the manuscript.

**Status: CORRECTED (wording and separation), tests PASS.**

---

### Item G — material provenance

**Issue as reported.** Which parameters are literature, which derived, which
synthetic, and which configurations numerically chosen?

**Classification: CONFIRMED.**  No provenance table existed in the manuscript.

**Location.** `a0/materials.json`; new Table 2 in
`sections/discussion.tex` (`tab:provenance`).

**Evidence.** `a0/materials.json` records every constant with a provenance tag:
literature (`c_ij`, `e_ij`, `κ_ij`, `ρ` from Zhang et al. 2025, Table 1),
derived (`D = μk_BT/q = 4.55e-4 m²/s`), scenario (`n_0 = 1…3e18 m⁻³`,
`d = 120…320 nm`), and **synthetic** (`ℓ = 50 nm`, `f_33 = 1 nC/m`, `H` tensor).
The entries `flexoelectric_tensor`, `strain_gradient_tensor`, `H_tensor`,
`sample_doping`, `sample_thickness`, `surface_properties` are `null` and marked
`NOT_SOURCED`; no invented value was substituted.

**Correction.** The manuscript now states that the reported percentages are the
response of this model and not predictions for a named specimen, and gives the
stability bound under which `H` was chosen.

**Status: CORRECTED.**

---

### Item H — novelty relative to Qu et al. and Fang & Wei

**Classification: UNRESOLVED.**  This is a declared limitation, not a defect
that was fixed.

**Evidence.** The accessible metadata and abstracts of Qu, Jin & Yang (2020,
J. Appl. Phys. 127, 194502) and Qu, Zhang, Gao & Jin (2022, Mech. Mater. 171,
104328) describe carrier redistribution driven by mechanical fields and by
temperature gradients, which corresponds to the `μ̃` used here, but the material
we could access does not state a constitutive coupling of the form
`ΔH = Δn H_{jkl} ε_{jk,l}`.  The full primary equations could not be obtained.
The work attributed in the brief to "Fang & Wei" could not be identified from
the available metadata, and no bibliographic entry was invented for it.

**Correction.** `sections/discussion.tex` (`sec:disc_literature`) states the
relation to Qu et al. and to the Fang & Wei work as **unresolved**, makes no
claim of priority, equivalence or superiority, and confines the paper's own
claim to what its numbers show: the edge-scattering problem with this coupling
is well posed, its energy budget closes exactly, and the coupling moves the
backward channel by a bounded and reproducible amount.

**Status: UNRESOLVED — declared in the manuscript.**

---

### Item I — reproducibility

**Issue as reported.** The final archive must contain `a0/materials.json` and
all indispensable inputs and must reproduce from a clean extraction with correct
relative paths.

**Classification: CONFIRMED.**  The previous package did not contain
`a0/materials.json`, and two legacy scripts depended on `.npy` caches that the
repository `.gitignore` excludes.

**Location.** `build_submission_package.py` (new);
`Paper_A_Submission_2026-11-06/`.

**Evidence and correction.** The package now ships `a0/materials.json`,
`model.py`, every driving script, the verification suite, all 12 CSVs and 5
JSONs the figures read, the manuscript, the ten vector PDFs and the static
checker — 48 files, 2.2 MB.  All scripts resolve paths from
`Path(__file__).resolve().parent` and the package root, so relative paths hold.
The `.npy`-dependent legacy scripts are excluded and the exclusion is documented
in the package README.

**Verification performed on a clean extraction (`/tmp/pkg`, byte copy of the
archive).**

1. `python -m unittest paper_a_study.test_model` → 18/18 OK.
2. `python paper_a_study/reclassify_csv.py` → fig02 130/130, fig04 50/50,
   fig07 95/95, **0 further flips**, i.e. the shipped flags are already the ones
   the rule produces.
3. `python Paper_A_LaTeX/scripts/static_check.py` → PASS.
4. `python paper_a_study/generate_final_figures.py` → all 10 PDFs re-rendered
   from the shipped CSVs.
5. `python paper_a_study/build_figure_data.py` → re-solved the whole study from
   `a0/materials.json` and wrote a fresh set of CSVs.  Comparing them field by
   field with the shipped files: **121 297 numeric fields, maximum relative
   difference 0** — bit-identical.  The three files that also carry the
   `x_flux_fraction` column (Fig. 2, 4, 7) agree on every common field with
   `max_rel_diff = 0` and **0 flag differences**, i.e. the post-processing step
   written for this phase changes nothing but adds a diagnostic column.

**Status: CORRECTED and VERIFIED.**

---

### Item J — LaTeX defects

**Issue as reported.** `\siunitxsetup` (v3-only), `\boldsymbol` redefinition,
undefined commands, citations, figures and overfull equations; compile with an
available engine or declare **COMPILATION UNVERIFIED**.

**Classification: CONFIRMED.**

**Location.** `Paper_A_LaTeX/main.tex`; `sections/*.tex`;
`references.bib`.

**Evidence (before).** `\siunitxsetup` aborts on siunitx v2; a `\newcommand`
redefinition of `\boldsymbol` is a hard "already defined" error under amsmath;
`sections/appendix_reproducibility.tex` did not exist although `main.tex`
`\input` it; three bibliography keys were placeholders
(`zhang2010zno`, `suscavace2006`, bare `qu2020coupling`, `wei2019plate`,
`fang2019sh`) and two of them could not be matched to any real publication.

**Correction.** `\sisetup` in place of `\siunitxsetup`; the `\boldsymbol`
redefinition removed (only `\newcommand{\vect}` remains); the missing appendix
written; `references.bib` rebuilt with nine entries whose journal, volume, pages
and year are verifiable (DOIs where seen), including Zhang et al. 2025 AMM 46(7)
1331–1346 (the source of the material constants) and Wang et al. 2025 AMM 46(6)
1069–1088 (closest prior art).  No placeholder entry remains.  The
`\tableofcontents` was removed (not appropriate for a journal submission), the
placeholder e-mail was removed, and unused macros were deleted.

**Validating test.** `Paper_A_LaTeX/scripts/static_check.py` — written for this
purpose — checks brace balance, `$`/`\[` balance, environment nesting,
`\cite` ↔ bib keys, `\ref`/`\cref`/`\eqref` ↔ `\label`, duplicate labels,
existence of all ten figure files, document structure (`document`,
`\maketitle`, abstract, Introduction, Conclusions) and macros against a
whitelist.  Result: **PASS**, 93 labels, 53 references, 9 citation keys, 9 bib
entries, no undefined reference, no unknown macro.

**Compilation.** One installation attempt was made and failed: `apt-get` has no
root and no repository access in the sandbox, and no TeX distribution or
wheel-based engine is available from the reachable package indices.  **The
manuscript has never been compiled.**  Overfull boxes, float placement and
page breaking are therefore unknown.  This is stated in the header comment of
`main.tex`, in the appendix (`app:repro_limits`) and in §5 below.

**Status: CORRECTED; COMPILATION UNVERIFIED.**

---

## 3. Register of numerical corrections made in this phase

| Quantity | Before | After | Cause |
|---|---|---|---|
| Fig. 5 evanescent reactive content | `4e-5` | `≤ 6.2e-28` | `L = REF_NORM·d` → `L = REF_NORM` |
| Fig. 5 closure residual | `≈ 1` | `≤ 3.8e-16` | residual built from `edge_power` → from the identity's LHS |
| Fig. 5 backward fraction at `H = 0` | `≈2.30e-2` (inconsistent budget) | `2.3146e-2` | recomputed with corrected weights |
| Fig. 2 admissible rows | 100/130 | 130/130 | `\|θ_E\| < 80°` gate removed |
| Fig. 4, Fig. 7 admissible rows | 50/50, 95/95 | unchanged | already conservation-based |
| Fig. 6 survival factor | up to `28.06` | `≤ 1` (min `0.0356`) | reciprocal convention (fixed in `4b4af80`) |
| Fig. 1 velocity panel | three speeds on one axis | `v_p` on a separate axis; signs attributed to `v_g`, `v_E` | definition error |
| Fig. 9(d) | "independent validation" | "implementation consistency" | over-claim |
| Manuscript BC block | grounded/open interchanged | solver-faithful, three surfaces | text-only defect |

No material parameter, no governing equation, no boundary condition and no
reference value was altered: every change is either an implementation bug in a
figure-data script, a mis-statement in the prose, or a bibliography repair.

---

## 4. Verification evidence at package time

* `paper_a_study/test_model.py`: **18 tests, all OK, 7.9 s**, from the clean
  extraction.
* Peak refinement: `peak_certification.json`, four cases, `certified: true` for
  all four, max relative change `7.2e-7`.
* Energy identity: `fig05_channel_power.csv`, closure `≤ 3.8e-16`, solver
  balance `≤ 2.1e-12`.
* Static validation: `PASS` (`Paper_A_LaTeX/static_validation.txt`).
* Clean-extraction rebuild of the full study from `a0/materials.json` was
  executed from the archive copy: all nine datasets rebuilt, **9 CSVs
  bit-identical**, the other three identical on every common field with the
  added `x_flux_fraction` diagnostic and zero flag changes.

---

## 5. Compilation status

**COMPILATION UNVERIFIED.**

No TeX engine (`pdflatex`, `latexmk`, `tectonic`, `xelatex`, `lualatex`) exists
in the authoring environment; one installation attempt was made and failed for
lack of privilege and repository access.  No PDF of the manuscript was produced
and none is claimed.  Everything checkable without an engine passes (§2, item J).
A reader who compiles the source should expect to adjust float placement and
possibly a few line breaks; the build command is
`pdflatex main && bibtex main && pdflatex main && pdflatex main`.

---

## 6. Remaining unresolved issues and limitations

1. **Novelty (item H).**  The relation of `ΔH = Δn H_{jkl} ε_{jk,l}` to the
   published flexoelectric-semiconductor constitutive relations is unresolved;
   the primary equations were not accessible.  No priority claim is made.
2. **Synthetic parameters.**  `ℓ`, `f_33` and `H` are synthetic.  Percentages
   are model responses, not specimen predictions.
3. **Linearity.**  Drift–diffusion is linearised about uniform doping and zero
   bias; the large-perturbation regime is out of scope.
4. **Single edge, infinite extent.**  No second edge, no finite plate, no
   resolved corner traction.
5. **Open-circuit gauge.**  A zero-mean gauge removes the electrostatic null
   vector; it changes no field, but it also means the open-circuit results are
   not an independent validation.
6. **Typesetting.**  Unverified (no engine).
7. **No experimental comparison.**  Internal consistency and exact limits only.

---

## 7. Editorial readiness verdict

**Not ready for submission as it stands — one blocking item, and it is not
scientific.**

The manuscript is scientifically complete: formulation, boundary conditions,
solution method, ten figures with data, results, discussion, limitations,
appendix, and a bibliography with no placeholder entry.  The two headline
numbers are certified, the energy identity closes to `3.8e-16`, and the package
reproduces from a clean extraction.  The audits that were open at the start of
this phase are closed except for the novelty comparison, which is declared.

What blocks submission is that **the manuscript has never been typeset**.  A
journal will not accept sources that the author has not compiled, and
overfull equations, float placement and reference formatting cannot be assessed
without a build.  The second gap, which a Q1 referee will raise, is the
synthetic character of `ℓ`, `f_33` and `H`: the paper is honest about it, but a
referee may still judge that the central quantitative claim (a `57.9 %` modal
partition) rests on parameters that were chosen for convenience rather than
measured.

So: **content ready for supervisor review; not yet ready for a journal
submission.**  The remaining work is (i) compile once in an environment with
TeX and fix whatever the log reports, and (ii) either justify the synthetic
parameter values against the literature more strongly or scope the claims to a
dimensionless statement.  Neither requires new physics or new figures.

*Stopped here for supervisor review.*
