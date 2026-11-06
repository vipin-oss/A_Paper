# Paper A — response to the independent scientific review

**Manuscript.** Negative reflection of guided waves in a flexoelectric
piezoelectric–semiconductor plate with carrier–strain-gradient coupling
**Authoritative source.** `Paper_A_Final_Submission/main.tex`
**Date.** 2026-11-06
**Branch.** `arena/ea7ca4dd-a-paper`
**Compilation.** **NOT EXECUTED in this environment** — no TeX engine is
available. Static validation only. See issue **J**.

---

## Summary table

| # | Issue | Severity | Status |
|---|---|---|---|
| A | Two competing LaTeX projects in the archive | critical (delivery) | **PASS** — one authoritative tree, old one archived and labelled |
| B | Strain-gradient modulus stated in Pa; four-index hyperstress | **critical (mathematics)** | **PASS** — re-derived, units and indices consistent |
| C | Electrochemical potential mixed dimensionless and energy terms | **critical (mathematics)** | **PASS** — energy-valued convention, sign-consistent with the solver |
| D | Title says flexoelectric, experiments may use f = 0 | critical (scope) | **PASS** — executed model stated; contribution measured (−0.01 %) |
| E | Quasistatic assumption asserted, not verified | major | **PASS** — three ratios computed at the operating point |
| F | Governing equations / boundary conditions vs solver | major | **PASS** — eight conditions re-verified against code and tests |
| G | Results and energy accounting; two configurations | major | **PASS** — comparison table added; identity verified to 3.4e-16 |
| H | `\siunitxsetup`, `\boldsymbol` redefinition | blocking (build) | **PASS (source fixed)** / **UNRESOLVED (no engine)** |
| I | Manuscript completeness | major | **PASS** — 11 700 words, ten figures, appendix |
| J | Compilation | blocking | **UNRESOLVED** — no TeX engine in this environment |
| K | Verification battery | major | **PASS** — 7 checks + 18 tests, log in `validation/` |
| L | Novelty vs Qu et al. | — | **UNRESOLVED** — declared, no claim made |

---

## A. Two competing LaTeX projects

**Original defect.** The reviewed archive contained `Paper_A_LaTeX/` and
`Paper_A_Final_Submission/manuscript/` as two apparently final manuscripts with
different lengths, different section lists and different equations.

**Location.** Both directories at the archive root.

**Evidence.** `Paper_A_Final_Submission/manuscript/` (635 lines, sections
including `abstract.tex` and `reductions.tex`) dates from commit `dffc147`.
`Paper_A_LaTeX/` (≈1 500 lines) dates from `e6fa02b`–`4f118e9` and carries the
corrected boundary conditions, the certified numbers of the refinement study and
the nine verified bibliography entries. It is the later and more complete of the
two, and its data files match the figure data actually used.

The archive was therefore **not** in the state described in the review: the
reviewer's 13-page build came from the older project, and every mathematical
defect listed in the review (Pa-valued gradient modulus, `\tau_{ijkl}`, the
dimensionless electrochemical potential, `\siunitxsetup`) is present in that
older project and absent from the newer one. Both statements are verifiable: the
old file still contains `\siunitxsetup` at line 13 and
`A_{ijklmn}=\ell^2C_{ijkl}\delta_{mn}` at line 33, while the new source contains
neither.

**Correction.**

* `Paper_A_Final_Submission/` is now the single authoritative tree: `main.tex`,
  `sections/`, `figures/`, `references.bib`, `scripts/static_check.py`, the
  solver, the figure data, the material file and the validation records.
* The old project is moved to `archive/legacy_manuscript_2026-11-06/` with an
  `archive/README.md` that names each of its defects and points to this document.
* The intermediate snapshot directory `Paper_A_Submission_2026-11-06/` and its
  ZIP were removed so that three copies do not circulate; its content is
  recoverable from commit `4f118e9`.
* `build_submission_package.py` now **refuses to run** if a `main.tex` exists
  anywhere outside `archive/`, so the repository cannot drift back into two
  manuscripts.

**Verification.** `python build_submission_package.py` exits 0 with a single
manuscript; `find . -name main.tex` returns two paths, one of which is under
`archive/`.

**Remaining limitation.** The archive keeps the old sources on purpose; a reader
must heed the `archive/README.md` label.

**Status: PASS.**

---

## B. Strain-gradient tensor: units and indices

**Original defect.** The older manuscript states
`A_{ijklmn} = \ell^2 C_{ijkl}\delta_{mn}` and then says that `A` has the units
of the elastic stiffness (N/m² = Pa). It also writes a four-index hyperstress
`\tau_{ijkl} = A_{ijklmn}\varepsilon_{mn,l}`, uses it in
`\sigma_{ij} = C:\varepsilon - \partial_l\tau_{ijkl}` and again in the balance
law.

**Location.** `archive/legacy_manuscript_2026-11-06/sections/governing_equations.tex`
lines 33, 42, 51, 58, 61, 89.

**Mathematical evidence.**

1. *Units.* With `w_g = ½ A η η` and `[η] = 1/m`, `[A] = (J/m³)·m² = N = J/m`,
   not Pa. The manuscript's own table was wrong by one factor of length.
2. *Indices.* The energy written in the same file,
   `½ A_{ijklmn}\varepsilon_{ij,l}\varepsilon_{kl,m}`, contracts the two
   gradient indices with each other; `δ_{mn}` in the stated `A` contracts the
   second gradient index of the first factor with a free index of the second,
   which is not a contraction at all. Written in slot order,
   `A_{ijklmn} = \ell^2 C_{ijkl}\delta_{mn}` pairs an elastic index with a
   gradient index and destroys the major symmetry
   `A_{ijklmn} = A_{lmnijk}` that a second derivative of an energy must have.
   The correct contraction is
   `A_{ijklmn} = \ell^2 c_{ijlm}\delta_{kn}` (third and sixth slots are the
   gradient directions), for which
   `½A_{ijklmn}\eta_{ijk}\eta_{lmn} = ½\ell^2 c_{ijlm}\eta_{ijk}\eta_{lmk}`.
3. *Order of the hyperstress.* The conjugate of the third-order `η_{ijk}` is
   third order, `τ_{ijk} = ∂w/∂η_{ijk}`; a fourth-order `τ_{ijkl}` cannot be the
   conjugate of a third-order kinematic variable. The balance then reads
   `ρü_j = ∂_iσ_{ij} − ∂_i∂_kτ_{jik}`, not `σ = C:ε − ∂_lτ_{ijkl}`, which
   double-counts the gradient term (once inside `σ`, once in the divergence).

**Correction.** Section 2 of the manuscript (`sec:governing_kinematics`,
`sec:governing_constitutive`, `sec:governing_balance`) now derives, in order:

1. `η_{ijk} = ε_{ij,k}` with `[η] = m⁻¹`;
2. `A_{ijklmn} = \ell^2 c_{ijlm}\delta_{kn}` as a sixth-order tensor,
   `[A] = N`;
3. energetic hyperstress `τ_{ijk} = A_{ijklmn}\eta_{lmn}`;
4. reciprocal hyperstress contribution `H_{ijk}\Delta n` and flexoelectric
   contribution `−f_{lijk}E_l`;
5. effective stress `Σ_{ij} = σ_{ij} − ∂_kτ_{ijk}`;
6. balance `ρü_j = ∂_iΣ_{ij}`, equivalently
   `ρü_j = ∂_iσ_{ij} − ∂_i∂_kτ_{jik}`;
7. higher-order boundary terms: double traction `t_{ij} = n_kτ_{ijk}`, the
   corner line force, and its unresolved status.

A new table (`tab:units`) gives the SI base-unit exponent of every quantity in
the formulation.

**Verification.** `paper_a_study/verify_dimensions.py` performs two independent
checks and both pass:

* 25 dimensional-homogeneity identities in (L, M, T, I), including
  `[A] = [L²][c] = (1,1,−2,0) = N` and `[τ] = [w]/[η] = (0,1,−2,0) = N/m`;
* a *tensor-contraction* test that does not rely on the algebra: the two
  candidate contractions predict different exact shear-horizontal branches, and
  the solver's own spectrum matches `ω² = c_{66}K²(1+\ell²K²)` (the
  `δ_{kn}` contraction) to `2.2e-13`, while the alternative is off by
  `3.1e+6`. The implemented contraction is therefore the one now stated in the
  manuscript.

No numerical model was changed: the solver already implemented the correct
contraction; only the manuscript was wrong.

**Remaining limitation.** The energy `w_g` is the isotropic single-length model;
the full 21-constant strain-gradient tensor of a `6mm` crystal is not resolved.

**Status: PASS.**

---

## C. Electrochemical potential

**Original defect.** The older manuscript writes
`\widetilde\mu = qφ/(k_BT) + Δn/n_0 + Δ\widetilde\mu` — two dimensionless ratios
plus an energy — and separately the constitutive term `H_{jkl}\varepsilon_{jk,l}`.
The three objects cannot be added.

**Location.** `archive/…/sections/governing_equations.tex` line 82.

**Mathematical evidence.** The wrong form has no consistent dimension: a
potential measured in volts is being added to a number. The solver, by contrast,
is internally consistent and uses an energy convention:

* in `model.py::fields`, the carrier variable is reconstructed as
  `N = mu + Q·phi − h·u''`, i.e. `μ = a Δn − qφ + H:η` up to the internal
  scaling;
* the electrostatic sign is the *electron* sign: `−qφ`, not `+qφ`;
* `D_z` is assembled as `e:ε − κ ∂_zφ + f ε_{zz,z}`, so `φ` is the physical
  potential and `E = −∇φ`.

**Correction.** `eq:mu` now reads
`μ = aΔn − qφ + H_{jkl}η_{jkl}` with `a = k_BT/n_0` in J m³, so every term is
an energy per carrier (J). `eq:continuity` writes the number flux
`J_i = −(Dn_0/k_BT)∂_iμ`, and `eq:current` gives the charge current

```
j_i = qD ∂_iΔn − q μ_e n_0 ∂_iφ + (q D n_0/k_BT) H_{jkl} ∂_iη_{jkl}
```

with the electron drift and diffusion signs derived, not asserted. The
dimensionless form used internally by the solver is given separately with its
exact scale factors, so the manuscript states one convention and maps it to the
other.

**Verification.**

* `verify_dimensions.py`: `[aΔn] = [qφ] = [Hη] = J`, `[H] = J·m`,
  `[a] = J·m³`, `[J_n] = m⁻²s⁻¹`, `[j] = A·m⁻²` — all pass.
* A direct numerical probe of the solver's fields at a solved mode reproduces
  `D_z = e:ε − κ∂_zφ + fε_{zz,z}` to exactly `0.0` (machine zero) and
  `μ = N − Qφ + h u''` to `4.3e−19`.
* The Einstein relation is verified in the model file: `D/μ_e = 0.0260 V`, i.e.
  `k_BT/q` at `T = 301.7 K`, the temperature now quoted in the manuscript.

**Remaining limitation.** The carrier gas is linearised about uniform doping and
zero bias; the strongly non-equilibrium regime is out of scope.

**Status: PASS.**

---

## D. Flexoelectric content versus the title

**Original defect (as reviewed).** The manuscript states that the numerical
experiments set `f = 0` while the title says "flexoelectric".

**Location.** `archive/…/sections/reductions.tex` and the old `abstract.tex`.

**Evidence about the *current* calculations.** The executed model does **not**
set `f = 0`: `Plate(...)` defaults to `flexo = 1e-9 C/m`, giving the
dimensionless coupling `f₃zz/(d√(c₄₄κ₃₃)) = 2.563×10⁻³`, and the flexoelectric
terms appear in both `D_z` and `τ_{zzz}`. But the coefficient is synthetic and
its effect is small, so the review's concern is substantively correct even
though its premise (f ≡ 0) is not.

**Correction.** A new subsection `sec:results_scope` states exactly which
sectors are active, gives the retained `f₃zz = 1 nC/m` and its provenance, and
reports a *measured* control: `paper_a_study/flexo_control.py` re-solves both
configurations with `f = 0`, `f = 1 nC/m` and `f = 10 nC/m`.

| configuration | f = 0 | f = 1 nC/m | f = 10 nC/m | effect of 1 nC/m |
|---|---|---|---|---|
| operating point | 0.0231484 | 0.0231456 | 0.0228697 | **−0.012 %** |
| peak | 0.5792453 | 0.5791800 | 0.5727683 | **−0.011 %** |

The abstract, the discussion and the conclusions now say that the reported
numbers are those of the strain-gradient piezoelectric–semiconductor
specialization with the carrier coupling, evaluated inside the flexoelectric
framework, and that the paper does **not** claim a calibrated flexoelectric
mechanism. The title is unchanged because the research direction is fixed, but
it is now explicitly a statement about the framework.

**Remaining limitation.** A genuinely flexoelectric-dominated regime would need
a larger, sourced `f₃zz` and a thinner plate; that is not attempted here and the
paper says so.

**Status: PASS (scope corrected, no result invented).**

---

## E. The quasistatic approximation

**Original defect.** The electrostatic reduction was justified by a generic
statement about small devices, without ratios.

**Correction and evidence.** `sec:governing_electric` now evaluates three
independent ratios at the operating point, computed by
`paper_a_study/quasistatic_check.py` (data in
`figure_data/quasistatic_audit.json`):

| ratio | value | meaning |
|---|---|---|
| `d/λ_EM`, `λ_EM = c/(ω√κ_r)` | `2.21e-4` | retardation negligible |
| `(d/λ_EM)²` | `4.89e-8` | size of the neglected correction |
| `v_p/c` | `9.36e-5` | magnetic energy / electric energy `≈ 8.8e-9` |
| `ω τ_d`, `τ_d = κ₃₃/σ_e` | `1.65e3` | **carriers are not quasistatic** |
| `d/L_D` | `0.0746` | plate thinner than the Debye length |

The second and fourth lines are the substance. Retardation is negligible by
five orders of magnitude, so the electrostatic reduction is sound; but the
carrier relaxation is three orders of magnitude *slower* than the wave, so the
model must not — and does not — assume instantaneous charge equilibrium. The
full continuity equation is retained. The manuscript now makes exactly this
distinction instead of hiding behind a small-device argument.

**Remaining limitation.** No electromagnetic radiation mode is included; the
justification is quantitative at the reported operating points only (it would
fail for a plate of order `λ_EM`).

**Status: PASS (explanation defect, not a model defect).**

---

## F. Governing equations and boundary conditions

**Re-checked, one by one, against `model.py` and the test suite.**

| condition | manuscript | code | status |
|---|---|---|---|
| grounded faces | `φ = 0`, `z = ±d/2`, essential | `basis()` ground branch, `np = n−2` | consistent |
| open circuit | `D_z = 0`, natural, zero-mean gauge | `open` branch, `np = n−1` | consistent |
| mechanical faces | `σ_iz = 0`, `τ_ijz = 0` | natural rows, traction residuals `< 1e-8` | consistent |
| blocking faces | `J_z = 0` | blocking residual `< 1e-8` | consistent |
| edge | `σ_ix = 0`, `τ_ijx = 0`, `D_x = 0`, `J_x = 0` | edge rows of `B` | consistent |
| corner | declared unresolved line force | `corner_line_force_max > 1e-4` by design | consistent |
| momentum | `ρü_j = ∂_iσ_ij − ∂_i∂_kτ_jik` | `S = σ − ∂_kτ` used for tractions | consistent |
| Gauss | `∂_iD_i = −qΔn` | `D = e:ε − κ∇φ + fη` | consistent |

The grounded/open-circuit labels are the ones introduced in the previous
revision and were **not** reverted; the solver remains as it was.

**Terminology.** The formulation is described as *Fourier-reduced
three-dimensional* (three displacement components, full strain and strain
gradient, one conserved `k_y`), never as plane strain.

**Verification.** `test_independent_classical_grounded_and_open` and
`test_independent_nonzero_f_H_temporal` match independently coded strong-form
systems for both electrical cases to `1e-10`;
`test_independent_weak_corner_reconstruction` checks `φ = 0` to `1e-10` on the
faces and asserts the corner line force is non-zero.

**Status: PASS.**

---

## G. Results, energy accounting and the two configurations

**Energy identity.** Verified against the current code and data, not against a
previous report. `build_figure_data.py::fig05` computes
`P_inc + ΣP_j + P_cross` and compares it with `P_edge − P_diss`; at `H = 0` the
closure is `3.4e-16` and the solver's own balance is `7.3e-13`. The evanescent
content at the reference plane is `4.8e-28`, not a transported power. The three
terms are described as self-powers, interference and loss — never as
independent channels.

**Two configurations.** New Table 4 (`tab:configurations`) lists, for both, the
frequency, thickness, carrier concentration, `H/H_ref`, the two wavenumbers,
reference plane, incident and backward attenuation, normalisation, group
velocity, isolated backward return, energy angle, total outgoing propagating
power, interference, dissipation, condition number and residual.

| | operating point | peak |
|---|---|---|
| `R_B` | 0.0231456 | 0.5791801 |
| total outgoing propagating power | 0.99980 | 0.99881 |

Both are labelled *isolated backward-channel returns*; the manuscript states in
the abstract, in `sec:results_peak` and in `sec:disc_meaning` that `R_B` is a
modal partition and **not** a total reflectance, and the total-outgoing column
is given so a reader can see the difference.

**Status: PASS.**

---

## H. LaTeX defect (compilation error)

**Original defect.** `\siunitxsetup` (siunitx v3 only; aborts on v2) and a
`\newcommand` redefinition of `\boldsymbol` (already defined by amsmath).

**Location.** `archive/…/main.tex` line 13 and the preamble of the same file;
in the authoritative source both were already corrected at commit `e6fa02b`.

**Correction (verified in the authoritative source).** `\sisetup` with
v2/v3-compatible keys; no redefinition of `\boldsymbol` (only
`\newcommand{\vect}`); `cleveref` loaded after `hyperref`; no `\tableofcontents`;
no placeholder e-mail; all packages standard.

**Verification.** `Paper_A_Final_Submission/scripts/static_check.py`: PASS —
96 labels, 55 references, 9 citation keys against 9 bibliography entries, no
undefined reference, no unknown macro, all ten figure files present, balanced
braces, balanced `$` and `\[ \]`, correctly nested environments, no non-ASCII
characters anywhere in the sources.

**Remaining limitation.** Static checking is not compilation. The source has not
been typeset here; overfull boxes and float placement are unknown.

**Status: PASS for the source repair; UNRESOLVED for the build (issue J).**

---

## I. Manuscript completeness

Expanded, not padded. The article now contains, in order: abstract with
keywords; introduction with the literature and the added coupling;
mathematical formulation (kinematics, units table, enthalpy, conjugates,
balances, electric model with quasistatic ratios, boundary conditions, energy
identity, non-dimensionalisation, thermodynamic admissibility); solution
method and verification; results in eleven subsections; discussion (meaning,
mechanism, literature, provenance, limitations); conclusions; and a
reproducibility appendix.

The additions that respond to this review are: the units table, the derivation
sequence of issue B, the electron-sign transport chain of issue C,
`sec:results_scope`, `sec:governing_electric`, `tab:configurations`, and the
resolved-index power flux.

Word count ≈ 11 700 (including mathematical tokens). Ten vector figures,
unchanged in content and style.

**Status: PASS.**

---

## J. Compilation

**Attempts made in this environment, all unsuccessful:**

1. `apt-get install texlive-latex-base` → permission denied (no root, no
   `dpkg` lock).
2. PyPI: `texlive`, `tectonic`, `tectonic-bin`, `texlive-bin` → no
   distribution exists on the reachable index.
3. GitHub release binary for Tectonic → the release host
   (`release-assets.githubusercontent.com`) is not reachable from the sandbox
   (TLS handshake rejected).
4. `raw.githubusercontent.com` fallback → not reachable.

**Consequence.** No PDF of the manuscript exists and none is claimed. The
manuscript has been *statically* validated only. This is stated in the header
comment of `main.tex`, in `README.md`, in the appendix (`app:repro_limits`) and
in `validation/verification_log.txt`.

**What was done instead.** Every failure mode that can be detected without an
engine was checked by script, and the two known killers from the review
(`\siunitxsetup`, `\boldsymbol`) are gone. The build command is documented:

```
cd Paper_A_Final_Submission
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

**Status: UNRESOLVED in this environment.** Not claimed as compiled.

---

## K. Verification battery

`python paper_a_study/run_all_checks.py` (log: `validation/verification_log.txt`):

| check | result |
|---|---|
| 18 scientific unit tests | PASS, 7.9 s |
| dimensional / constitutive audit (25 identities + contraction test) | PASS |
| quasistatic ratios | PASS |
| flexoelectric control | PASS |
| admissibility re-derivation (0 flips) | PASS |
| figure data and figure files | PASS |
| LaTeX static validation | PASS |
| TeX build | SKIPPED (no engine) |

Two clean-extraction reproductions were run in the previous phase and remain
valid: the full study re-solved from `a0/materials.json` reproduces the shipped
CSVs bit-identically (121 297 numeric fields, maximum relative difference 0).
The new checks (`verify_dimensions`, `quasistatic_check`, `flexo_control`) are
deterministic and were run three times with identical output.

An analytical identity check is never described as experimental validation; the
manuscript states that the temporal/spatial comparison is an implementation
check and that the independent evidence is the strong-form and `C¹`
finite-element comparisons.

**Status: PASS.**

---

## L. Bibliographical entries and novelty

Nine entries, all cited, all with verifiable journal, volume, pages and year;
DOIs where they were observed. The material-constant source is Zhang et al.,
*Appl. Math. Mech.-Engl. Ed.* **46**(7) 1331–1346 (2025); the closest prior art
is Wang et al., **46**(6) 1069–1088 (2025). No placeholder keys remain
(`zhang2010zno`, `suscavace2006`, `qu2020coupling`, `wei2019plate`,
`fang2019sh` are gone).

**Novelty remains UNRESOLVED.** The primary constitutive equations of Qu et al.
were not accessible; the work attributed to Fang & Wei could not be identified
from available metadata and no entry was invented for it. `sec:disc_literature`
states the relation as unresolved and makes no priority, equivalence or
superiority claim.

---

## Remaining genuine scientific issues

1. **Synthetic parameters.** `ℓ = 50 nm`, `f₃zz = 1 nC/m` and `H` are synthetic;
   `H` is nonetheless bounded by an explicit convexity condition
   (`H ≤ 0.022 H_bound`, `s ≤ 5e-4`). Reported percentages are model responses.
2. **Flexoelectric subdominance.** Measured at −0.01 %; the title describes the
   framework, not the dominant term. Stated in four places.
3. **Novelty** relative to Qu et al. unresolved and declared.
4. **Single edge**, no second edge, corner line force not resolved pointwise.
5. **Linearised transport** about uniform doping and zero bias.
6. **No experimental comparison.**
7. **Typesetting unverified** (issue J).

## Editorial readiness

**Not ready to be submitted.** Two things are missing and neither is a
mathematical error: the manuscript has never been compiled, and the numerical
evidence rests on a synthetic coupling whose influence on the reported partition
is a fraction of a percent. The formulation, the boundary conditions, the energy
identity, the two certified values and the dimensional structure are now
consistent with the solver and with each other, and an independent reader can
reproduce them from the package. What a Q1 referee would still press on is the
synthetic parameterisation of the mechanism, not the correctness of the
derivation.
