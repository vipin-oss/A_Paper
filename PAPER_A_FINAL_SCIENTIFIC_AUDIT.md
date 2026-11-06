# Paper A — Round-4 targeted scientific audit

**Branch** `arena/ea7ca4dd-a-paper` · **repository** `vipin-oss/A_Paper`
**Authoritative manuscript** `Paper_A_Final_Submission/main.tex`
**Date of run** 2026-11-06 · **Auditor role** independent verification (mathematical
physics / continuum mechanics / numerical wave propagation), acting on a
supervisor instruction that listed six issues A–F plus §9–§11.

This report records, for every issue, the six required evidence fields: the file
and source location, the original claim, what was checked, the calculation, the
error classification, the physical consequence, the correction applied, the
verification, and the remaining uncertainty. Statuses are restricted to
**CONFIRMED—FIXED**, **ALREADY CORRECT**, **UNRESOLVED—LIMITATION**,
**FAILED—CLAIM WITHDRAWN**. No issue is closed on a generic PASS.

Everything below is machine-reproducible from the scripts named in each item;
the machine-readable records are in `paper_a_study/figure_data/`.

---

## 0. Summary table

| Issue | Object | Status | One-line outcome |
|---|---|---|---|
| A | Phase speed `v_p` | **CONFIRMED—FIXED** | Text said 2.8 km/s; the solver and the surrounding text give 28.046 km/s. Reporting error, corrected; no code change. |
| B | `λ_EM`, quasistatic ratios | **CONFIRMED—FIXED** | The manuscript's `λ_EM` was `1/k_EM` (missing 2π) and `d/λ_EM` was `k_EM d`. Wavelength, ratio and the retardation parameter corrected; conclusion unchanged. |
| C | Modal flux normalisation | **ALREADY CORRECT** | `R_B` invariant to eigenvector rescaling at 1.5e−15 and to degree 18→30 at 1.5e−7. Only the *label* of the raw `backward_Px` column was wrong; it is an unscaled eigenvector power. |
| D | Mechanism / attribution | **CONFIRMED—FIXED** | All of the 57.92 % exists at `H=0`; removing the strain-gradient sector removes the backward branch entirely. Abstract, title, results, discussion and conclusions rewritten; `H` quantified as −1.21 % / −9.85 %. |
| E | Novelty vs. Qu et al. (2025) | **UNRESOLVED—LIMITATION** | Metadata verified; the free-energy decomposition could be inspected only through an open-access companion. In the inspected equations `Ψ_Carrier` carries no strain gradient, so the added term is *absent* there — not proof of absence from the full article. Comparison table added, symbol collision flagged. |
| F | Corner effects | **UNRESOLVED—LIMITATION** | Corner-sensitive diagnostic run: the outer band holds 1.2–2.1 % of the gradient energy and its share *falls* with degree. Global partitions are corner-insensitive; pointwise corner fields are not certified. |
| §9 | Admissibility | **ALREADY CORRECT**, one gap **FIXED** | `H*` was used 20+ times and never defined, and two different normalisations (`H*`, `H_ref`) coexist. Defined, separated, and the numerical-vs-experimental uncertainty distinction stated. |
| §10 | Figures / manuscript | **CONFIRMED—FIXED** | Ten PDFs retained unchanged; captions of Figs. 5 and 7 now state that their `H` sweeps are at fixed frequency. Title no longer implies that the added coupling produces the reflection. |
| §11 | Build & reproducibility | **PASS with a stated limitation** | Full suite PASS (20 tests + 10 audits, round 5), LaTeX static check PASS, 11/11 citations resolved. **No TeX engine in the authoring sandbox**: the round-4 PDF was compiled by the independent auditor (29 pages), not here. |

---

## A. Phase speed and wavenumber consistency

**Source location.** `sections/governing_equations.tex`, retardation paragraph
(now lines 247–266); the value was `v_p=(\omega/|\vect{k}|)=\SI{2.8}{\kilo\metre\per\second}`.

**Original claim.** The guided mode at the operating point travels at 2.8 km/s,
hence `v_p/c = 9.4e−5`.

**What was checked.** Every definition of `k_x d`, `k_y d`, `ω`, `f`, `d`, `v_p`
in the manuscript and the solver; Hz vs rad/s; `k` vs `2π/λ`; full thickness vs
half-thickness; nondimensional vs dimensional; SI vs plotting units; signed vs
magnitude. `d` is the **full** thickness, 200 nm, and the nondimensionalisation
is `K = k_x d`, `Ω = ω d / c_s` with `c_s = 2746.6088 m/s`.

**Calculation** (`paper_a_study/phase_speed_audit.py` →
`figure_data/phase_speed_audit.json`).

```
d      = 2.000e-7 m          c_s = 2746.6088 m/s
K0     = 0.7361990195318475  KY0 = 0.1298117503144748
OMEGA0 = 7.633372404423294
ω = Ω0 c_s/d   = 1.048294e11 rad/s     f = ω/2π = 16.684123 GHz
k_x = K0/d     = 3.680995e6 rad/m      k_y = KY0/d = 6.490588e5 rad/m
|k| = hypot(k_x,k_y) = 3.737780e6 rad/m
v_p = ω/|k|    = 2.804591e4 m/s = 28.046 km/s
v_p/c = 9.3551e-5
```

The figure data are self-consistent to 2.4e−12 when `v_p` is recomputed from
each row's own frequency, so this is not a plotting-unit or nondimensional
error. `results.tex` already quoted 20.0–105.8 km/s along the branch, which
contains 28.0 km/s; only the governing-equations paragraph disagreed.

**Classification.** Manuscript reporting error (a factor 10.016 in the prose),
not a code error, not a convention, not a figure label.

**Physical consequence.** The stated `v_p/c = 9.4e−5` was inconsistent with the
stated `v_p` by the same factor; the *conclusion* (quasistatic, magnetic energy
negligible) was and remains correct, because it is controlled by `v_p/c`, which
was already right.

**Correction.** `\SI{2.8}{\kilo\metre\per\second}` → `\SI{28.0}{%
\kilo\metre\per\second}`; the derived `(v_p/c)^2` refined from `9e−9` to
`8.8e−9`. **No output was multiplied by ten**; the number was recomputed from
`ω/|k|` and the manuscript now states the inputs.

**Verification.** `phase_speed_audit.py` recomputes the chain from the material
file and compares every manuscript number against it, exiting non-zero if any
disagrees. Before the edit it flagged `v_p` as a MISMATCH (relative 0.90). After
the edit it returns **PASS** with `v_p` at relative 1.6e-3 (the rounding of
28.046 to 28.0), the frequency at 2.5e-4, and the figure-data self-consistency
at 2.4e-12. The pre-fix values are not deleted: they are stored in the audit
record under `historical_pre_fix`.

**Remaining uncertainty.** None: the quantity is algebraic in inputs that are
themselves validated by `verify_dimensions.py` (25 identities).

---

## B. Electromagnetic wavelength and quasistatic scaling

**Source location.** Same paragraph: `λ_EM = c/(ω√κ_r) = 0.905 mm`,
`d/λ_EM = 2.2e−4`, `(d/λ_EM)^2 = 4.9e−8`; abstract `main.tex` line 78.

**Original claim.** The electromagnetic wavelength in the medium is 0.905 mm and
the plate is 2.2e−4 wavelengths thick.

**Calculation.** `k_EM = ω√κ_r/c`, `λ_EM = 2π/k_EM = v_EM/f`.

```
κ_r = κ33/ε0 = 10           ω = 1.048294e11 rad/s
k_EM   = 1.105503e3 rad/m
λ_EM   = 5.683555e-3 m  = 5.6836 mm      ( = v_EM/f )
1/k_EM = 9.04566e-4 m  = 0.9046 mm
k_EM d = 2.211005e-4        d/λ_EM = 3.518925e-5
(k_EM d)^2 = 4.888545e-8    (d/λ_EM)^2 = 1.238e-9
```

**Classification.** Missing factor 2π in the written formula: the manuscript
wrote `c/(ω√κ_r)`, which is `1/k_EM`, and called it the wavelength. The number
0.905 mm is *correct as* `1/k_EM` (ratio 0.9995) and wrong as `λ_EM` (factor
2π). The label `d/λ_EM = 2.2e−4` was in fact `k_EM d`. A second, independent
error followed: `(d/λ_EM)^2` was quoted as the retardation parameter, whereas
retardation is controlled by `(k_EM d)^2 = 4.889e−8`; the quoted 4.9e−8 was
numerically right but attached to the wrong symbol.

**Physical consequence.** None for the quasistatic conclusion — every smallness
parameter (`k_EM d`, `d/λ_EM`, `v_p/c`) is ≤ 2.3e−4, and the full continuity
equation is retained (`ωτ_d = 1.65e3`). The defect was in the arithmetic trail,
which is exactly what a referee recomputes first.

**Correction.** The paragraph now reads `k_EM = 1.106e3 1/m`,
`λ_EM = 2π/k_EM = v_EM/f = 5.68 mm`, `1/k_EM = 0.905 mm`, `d/λ_EM = 3.52e−5`,
`k_EM d = 2.2e−4`, retardation order `(k_EM d)^2 = 4.9e−8`; the abstract line
now reads `d/λ_EM = 3.52e−5 ... (k_EM d = 2.2e−4)`.
`paper_a_study/quasistatic_check.py` was corrected to compute
`λ_EM = 2π/k_EM` and to record **both** `k_EM d` and `d/λ_EM`, so the audit file
can no longer be misread (`figure_data/quasistatic_audit.json`).

**Verification.** `quasistatic_check.py` PASS, all six ratios printed with their
definitions; `(k_EM d)^2 = 4.889e−08`, `ωτ_d = 1654.4`, `d/L_D = 0.0746`.
`phase_speed_audit.py` now checks `λ_EM = 5.68 mm`, `1/k_EM = 0.905 mm`,
`k_EM d = 2.2e−4` and `d/λ_EM = 3.52e−5` against the reconstruction and returns
PASS (residuals 6e−4, 5e−4, 5e−3 and 3e−4 respectively — the last digit is
rounding in the prose, not a physics discrepancy).

**Remaining uncertainty.** The `κ_r = 10` and `σ_e = 5.6e−3 S/m` are the
representative values already declared as such in the parameter table; a
different permittivity changes `λ_EM` by `√κ_r` but cannot bring `k_EM d` near
unity.

---

## C. Modal flux normalisation and convergence

**Source location.** `paper_a_study/model.py::Plate.edge` (normalisation and
target selection), `::Plate.power`, `::Plate.mode_diagnostics`;
`build_figure_data.py` (`backward_Px`); manuscript
`eq:RB`, `tab:refinement`, `tab:configurations`.

**Original claim under test.** (i) The reported `R_B` is an artefact of the
eigenvector normalisation returned by the generalised eigenproblem; (ii) the
raw `backward_Px` column of the CSV is a flux and should converge under degree
refinement.

**What was checked** (`paper_a_study/modal_flux_audit.py` →
`figure_data/modal_flux_audit.json`).

1. Raw modal power of the backward mode, normalisation factor, scattering
   amplitude, incident power and normalised fraction at degrees 18/22/26/30.
2. Explicit rescaling test: multiply the eigenvector by a random complex factor,
   recompute the whole chain.
3. The same at the 57.92 % peak.

**Result.**

| deg | raw `P_B` (op. point) | `|a_B|` | `|a_B|²P_B` | `R_B` |
|---|---|---|---|---|
| 18 | −1.789225e−2 | 1.1375 | −2.314811e−2 | 0.023145608 |
| 22 | −1.542481e−2 | 1.2251 | −2.314812e−2 | 0.023145619 |
| 26 | −1.324546e−2 | 1.3220 | −2.314812e−2 | 0.023145623 |
| 30 | −1.137773e−2 | 1.4264 | −2.314813e−2 | 0.023145624 |

The raw modal power spreads by **36.4 %** (operating point) and **55.7 %**
(peak) across the refinement, while `|a_B|²P_B` and `R_B` are invariant to
**7.2e−7** (operating point) and **1.5e−7** (peak). The rescaling test returns
`R_B = 0.023145619185` unchanged to **1.5e−15**.

At the peak (`k_xd = 0.55`): raw `P_B` −1.256764e−3 → −5.563739e−4,
`|a_B|` 21.487 → 32.294, `|a_B|²P_B` = −5.797169e−1 at every degree,
`R_B` 0.579179974 → 0.579180059.

**Classification.** The claim of (i) is **rejected**: the normalisation is
compensated exactly by the scattering amplitude, which is what the
`y/sqrt(P)` step in `edge()` is for. The claim of (ii) is **confirmed as a
reporting defect only**: `backward_Px` is the *unscaled eigenvector* power and
must not be read as a physical flux; it is a diagnostic, and it is now labelled
as such.

**Physical consequence.** None for `R_B`. Had the raw column been quoted as a
physical flux, the backward channel would have appeared to depend on the
Galerkin degree at the 40–55 % level — a spurious non-convergence.

**Correction.** `R_B` is retained and certified. The CSV column and the figure
caption that display it now say *unscaled eigenvector power*; the physical
quantity is `|a_B|²P_B`.

**Verification.** Invariance under arbitrary rescaling (1.5e−15) and under
degree refinement (1.5e−7), both reproduced by a script in the package.

**Remaining uncertainty.** The audit certifies the *self*-power of the
identified mode at the reference plane. It does not certify a total
reflectance, and the manuscript says so in three places.

---

## D. What actually produces the backward channel

**Source location.** `main.tex` abstract (old sentence "The
carrier–strain-gradient coupling `H` shifts the backward channel …"), title,
`sections/discussion.tex` mechanism subsection, `sections/conclusions.tex`.

**Original claim.** The strong negative reflection is an effect of the added
carrier–strain-gradient coupling, which shifts the backward channel by "at most
2.4 %".

**What was checked** (`paper_a_study/mechanism_controls.py` →
`figure_data/mechanism_controls.json`). Matched controls at both reported
points; everything except the named ingredient held fixed (same `k_x`, same
`k_y`, same `n_0`, same `ℓ`, same reference plane `L = 10d`, same unit incident
self-power). The frequency is allowed to *follow the branch*, because switching
an ingredient off changes the dispersion and comparing two different branches at
one frequency is not a control.

| configuration | op. point `f` (GHz) / `R_B` | peak `f` (GHz) / `R_B` | `K_B` (peak) | port |
|---|---|---|---|---|
| full (`f₀`, `H/H* = +0.05`) | 16.6840 / 0.022866412 | 16.6549 / 0.522107121 | +0.50378 − 3.14e−3 i | backward |
| `f = f₀`, `H = 0` | 16.6841 / 0.023145619 | 16.6550 / 0.579180033 | +0.50380 − 4.52e−5 i | backward |
| `f = 0`, `H/H* = +0.05` | 16.6840 / 0.022869165 | 16.6549 / 0.522152893 | +0.50379 − 3.14e−3 i | backward |
| `f = 0`, `H = 0` | 16.6841 / 0.023148416 | 16.6550 / 0.579245317 | +0.50381 − 5.0e−5 i | backward |
| `ℓ = 0` (classical) | 16.2077 / 0.077295714 | 15.9943 / 0.125061107 | **−0.7362 = −k_inc** | **no backward port** |

Incremental effects against `f = H = 0`:

```
operating point:  full −1.2182 %   f only −0.0121 %   H only −1.2064 %
peak           :  full −9.8642 %   f only −0.0113 %   H only −9.8563 %
```

Power balances ≤ 2.0e−12; the classical case has 113 outgoing modes instead of
182.

**Decisive observation.** In the classical control the mode that the target
heuristic returns has `Re K_B = −k_x,inc` **exactly** (`−0.7362` against
`+0.7362`; `−0.5500` against `+0.5500`) and its reflected angle is the mirror
of the incident one (+10.00° vs +10.00°, +13.28° vs +13.28°). It is the
specular reflection, i.e. the time-reverse of the incident mode, and it has
negative `x`-power for the trivial reason that reversing the wave reverses its
flux. `Plate.edge` already refuses to call it backward
(`negative_direction = False`), and the audit script now records
`port = "no_backward_port"` and `backward_is_specular = True` explicitly. The
old reading — "the baselines still show backward reflection, so negative
reflection is not new" — mis-read this fallback. **Without the strain-gradient
sector there is no backward branch at all**, so the negative reflection is a
property of the higher-order branch, not of the added coupling.

**Branch-consistent `H` sweep** (k_x fixed, frequency tracked; the sweep the
manuscript now quotes):

```
operating point  H/H* = 0, ±0.025, ±0.05 → R_B = 0.023146, 0.023116, 0.023062,
                                            0.022974, 0.022866
peak             H/H* = 0, ±0.025, ±0.05 → R_B = 0.579180, 0.573994, 0.561783,
                                            0.546268, 0.522107
```

Referred to the edge plane instead of the 10-thickness reference plane, the peak
comparison is `0.579704 → 0.555972`, i.e. −4.09 % rather than −9.85 %; the
remaining 5.8 points are the increased attenuation of the backward mode, whose
axial decay rate rises from 4.52e−5 to 3.14e−3 per unit thickness.

**Classification.** Narrative/attribution error of the highest severity in the
paper, plus a comparison-design error in the earlier control (fixed frequency
across a changing dispersion). Not a solver error: every number above is
reproducible from the unmodified solver.

**Physical consequence.** The headline claim survives, with a corrected cause:
the conversion is a strain-gradient (higher-order branch) effect, largest at the
zero-group-velocity point, and the added coupling *reduces* it slightly.

**Correction.** Title, abstract, introduction (two passages), a new results
subsection ("What creates the backward channel", `tab:controls`), the discussion
mechanism subsection, and the conclusions were rewritten. The fixed-frequency
sweeps of Figs. 5 and 7 remain in the paper, now explicitly labelled as
forced-frequency responses, with the branch-consistent numbers quoted alongside.

**Verification.** `mechanism_controls.py` reproduces the whole table in ~1 min;
`tab:controls` is generated from `mechanism_controls.json`; the degree
refinement of the `H/H* = +0.05` peak value was re-run separately
(0.522107071 / 0.522107121 / 0.522107138 / 0.522107142 at degrees 18/22/26/30,
residual ≤ 4e−12), so the 9.85 % is not a resolution artefact.

**Remaining uncertainty.** `H` is synthetic; the two extreme signs of `H` are
both admissible (`s ≤ 5e−4`). The "no backward port at `ℓ = 0`" statement is a
statement about this plate, this frequency and this `k_y`; it is not a theorem
that a classical piezoelectric-semiconductor plate can never support a backward
mode.

---

## E. Novelty against the primary literature

**Source locations.** `sections/discussion.tex` (relation to literature),
`references.bib`.

**Metadata verification.** *Qu, Y., Pan, E., Zhu, F., Deng, Q., "A
thermodynamically consistent theory for flexoelectronics: interaction between
strain gradient and electric current in flexoelectric semiconductors",
International Journal of Engineering Science **208** (2025) 104165,
doi:10.1016/j.ijengsci.2024.104165.* Verified against the publisher record, and
the author list is **Qu, Pan, Zhu, Deng** — not "Qu, Jin, Yang", which is the
2020 *J. Appl. Phys.* paper. Added to `references.bib` as `qu2025thermodynamic`
(it was cited in prose but absent from the bibliography).

**Access status (recorded honestly).** The IJES article itself is not open
access and was **not** obtained. Its free-energy decomposition is reproduced,
with attribution, in the open-access companion *Hu, Liu, Liu, Jiang, Zhuang,
Rabczuk, Int. J. Mech. Sci.* **305** (2025) 110740, doi:10.1016/j.ijmecsci.2025.110740,
Eqs. (4a)–(4e), which states that it follows the theory of Qu et al. That
reproduction is what was compared against, and the paper now says so explicitly
and cites the companion (`hu2025computational`).

**The inspected equations.**

```
Ψ_Gib = Ψ_Mech(ε,g) + Ψ_Elec(e) + Ψ_Diele(ε,g,e) + Ψ_Carrier(n,p)
Ψ_Mech   = ½ C ε:ε + ½ A g⋮g
Ψ_Diele  = −η e·ε − μ e·g
Ψ_Carrier = Ψ_Carrier(n,p)          ← no strain-gradient argument
∂Ψ_Gib/∂n = μ_n + qψ                ← thermodynamic restriction
```

**Finding.** Because `Ψ_Carrier` does not depend on `g`, the electrochemical
potential of that framework carries **no** strain-gradient contribution, and the
strain gradient reaches the carriers only indirectly through the flexoelectric
polarisation in Gauss's law. A direct bilinear term `Δn H_jkl ε_jk,l` is
**absent from the inspected postulate**; within those equations it is an
independent addition, not a change of variables and not a special case of a more
general tensor. The paper does **not** claim it is absent from the full IJES
article.

**Symbol collision (new finding, corrected).** In Qu et al. and in the companion,
`H_ijklmn` is the **sixth-order strain-gradient elasticity tensor**, with
different units from our third-order carrier coefficient `H_jkl` (J·m). The
manuscript uses `A_ijklmn` for the former; the discussion now states the
collision explicitly so that an admissibility bound quoted for `H_jkl` cannot be
misread as a bound on `H_ijklmn`.

**Classification.** `UNRESOLVED—LIMITATION` for the priority question,
upgraded from a bare "could not settle" to an equation-level statement with a
named source and an explicit access caveat. `tab:novelty` records
`absent in the inspected equations` for Qu et al. (2025) and (2020/2022),
`absent by scope` for the dielectric wave papers, and `absent` for the
piezoelectric-semiconductor wave papers. No "first-ever" claim, no priority
claim.

**Assessment of what the contribution is.** With the corrected attribution, the
contribution is the *scattering* formulation — the partition of a guided mode
into the outgoing branches of a free edge, resolved branch by branch and
certified by an exact energy identity — plus the demonstration that the added
enthalpy is admissible (`s ≤ 5e−4`) and its incremental effect bounded. The
paper now says this in the discussion.

**Remaining uncertainty.** Full constitutive equations of IJES 208 (2025)
104165 could not be inspected; classification is limited to the reproduced
decomposition.

---

## F. Higher-order corner effects

**Source location.** `sections/discussion.tex`, limitations;
`paper_a_study/corner_assessment.py` → `figure_data/corner_assessment.json`.

**Question.** The spectral Galerkin basis is smooth through the thickness, while
the free edge meets the free faces at two corners where a higher-order edge
problem may be singular. Does that contaminate the 57.92 % peak, the weak form,
or the modal amplitudes?

**What was done** (corner-sensitive, not a global-fraction inference). For
degrees 18/22/26/30, at both reported points, the strain-gradient energy density
`λ²|∇ε|²_C` was evaluated on the edge plane `x = 0` from the **coherent** sum of
all outgoing modes plus the incident mode (interference retained), and its
distribution was split into an inner region and an outer corner band
`|z| > 0.4 d/2` (faces at `±0.5`).

**Round-4 configuration error (found by the independent audit, fixed in round 5).**
The round-4 script set `CASES = {'operating_point': KB0, ...}` and used that
value both for branch tracking and as the `incident_guess` of `Plate.edge`.
`KB0 = 0.2451746921716515` is the **backward-mode** wavenumber; the operating-point
incident wavenumber is `K0 = 0.7361990195318475`. The script therefore solved a
different scattering experiment and labelled it `operating_point`:

| diagnostic (degree 22) | with `K0` (correct) | with `KB0` (round 4) |
|---|---|---|
| `R_B` | 0.02314561918 | 0.54439742640 |
| corner-band share | 0.9958 % | 2.1315 % |
| band peak/mean | 0.10211 | 0.20610 |

The stored `corner_assessment.json` reported 0.5444 as the operating-point `R_B`
while every other file reported 0.0231456 — a self-inconsistency that the 18
physics tests could not see, because each file was internally consistent.

**Correction.** The script now imports `K0` as well as `KB0`, sets
`CASES = {'operating_point': K0, 'peak': peak_candidate}`, where the peak value is
taken from `certify_peak.CASES` rather than restated; it asserts that the
wavenumber returned by the solver for the incident port equals the requested
incident wavenumber (`|Re ΔK| < 10⁻⁶`); it cross-checks every operating-point row
against `peak_certification.json` at the same degree; and it writes
`certification_cross_check` into the JSON. Two regression tests were added to
`test_model.py` (now 20 tests): one asserts that `CASES['operating_point'] == K0`
and `!= KB0`, the other that the stored `R_B` agrees with the certification file
row by row to `1e-9`.

**Corrected results** (`figure_data/corner_assessment.json`):

| case | incident `K` | corner-band share | peak/mean in the band | drift, degree 18→30 | spread of `R_B` |
|---|---|---|---|---|---|
| operating point | 0.736199 | 0.928 – 0.996 % | 0.098 – 0.102 | −6.83 % | 7.2e−7 |
| peak | 0.550000 | 1.180 – 1.264 % | 0.122 – 0.126 | −6.62 % | 1.5e−7 |

Certification cross-check: **PASS** (operating-point `R_B` equals the
`peak_certification.json` value at every degree, difference 0.0 in the stored
digits).

**Reading.** The band carries about one per cent of the gradient energy, its
density is *below* the plate mean (peak/mean < 0.13), and its share **decreases**
with refinement instead of growing; a corner singularity would produce the
opposite trend. The global partition is therefore insensitive to the corner at
the 1e−7 level.

**What this does *not* show.** A small outer-band fraction bounds the energy that
sits near the corner in the computed field; it does not bound the work a singular
corner traction could do on admissible variations, because the polynomial basis
cannot represent that singularity. The manuscript now states the two facts
separately and drops any implication that the corner has been "shown harmless".
A statement about corner forces would need a corner-eigenvalue analysis or
corner-enriched functions.

**Classification.** `UNRESOLVED—LIMITATION`. Certified: the reported *global*
partitions, the weak-form consistency, the energy identity, and the case
selection (by regression test). Not certified: the pointwise corner field, the
associated line force, and its dynamical effect.

**Correction to the manuscript.** The limitations paragraph was rewritten with
the corrected percentages, the incident-wavenumber identification of each case,
the cross-check against `tab:refinement`, and an explicit paragraph separating
"the partitions are corner-insensitive" from "the corner force is negligible".

**Remaining uncertainty.** As stated: a dedicated corner-eigenvalue analysis (or
a 3-D model) would be required to certify pointwise corner tractions. Per the
instruction, no new 3-D model was introduced.

---

## §9. Admissibility and uncertainty

**Status: `ALREADY CORRECT`, with one gap `CONFIRMED—FIXED`.**

*Already correct.* The Schur condition
`s = H²(c⁻¹)₃₃/(ℓ² a) < 1` is derived with the **reduced** modulus
`c* = c₃₃ − 2c₁₃²/(c₁₁+c₁₂) = 154.3837 GPa` (not `c₃₃`), the bound
`H_bound = ℓ√(a c*) = 8.965976e−22 J·m` follows, the solver refuses to run
outside it, and all reported solutions sit at `s ≤ 5e−4`. The strain-gradient
contraction and all 25 dimensional identities pass (`dimension_audit.json`),
including the check that `H` has units J·m.

*Gap fixed.* The symbol `H*` was used in 20+ places (every `H/H*` axis) and was
**never defined**, while a second normalisation `H_ref = d√(a c₄₄) = 1.89e−21 J·m`
appeared in one table. Both are now defined in the admissibility subsection:
`H* = H_bound/√5 = 4.0097e−22 J·m` (the value at which `s = 0.2`, a plotting
convention), and `H_ref` is stated to be the thickness-based reference of the
enthalpy, explicitly not interchangeable with `H*`. The three equivalent
statements of the swept extreme — `|H| ≤ 2.0e−23 J·m`, `0.05 H*`,
`0.022 H_bound` — are consistent to three digits and are now all given.

*Uncertainty distinction (added).* The manuscript now states that no
strain-gradient elasticity measurement fixes `ℓ`, `f` or `H`, so the reported
intervals are modelling choices with **no experimental uncertainty**, whereas
the numerical uncertainty of a reported `R_B` is its refinement spread
(below 1e−6 relative). No device-level ZnO validation is claimed anywhere.

---

## §10. Figures and manuscript consistency

* **Ten vector PDFs retained, none regenerated.** No figure's *data* changed in
  this round: `mechanism_controls.py` adds new numbers in new tables, it does
  not alter any plotted curve. The claims attached to Figs. 5 and 7 were
  narrowed instead: both are now captioned as fixed-frequency sweeps, with the
  branch-consistent alternative in `tab:controls`.
* **Title.** "… with carrier–strain-gradient coupling" → "… : the
  strain-gradient backward branch". The old title implied that the added
  coupling produces the reflection; the new one names the mechanism the controls
  actually established.
* **Abstract, introduction, results, discussion, conclusions** are now
  consistent with `tab:controls`; the abstract states the mechanism, the two
  baseline values, the two coupling percentages and the removal of the branch at
  `ℓ = 0`.
* **Operating points, captions, table entries** re-checked against the CSVs and
  JSONs; `tab:configurations` values unchanged (they are all `H = 0`
  quantities).
* **Symbols/units**: `λ_EM`, `1/k_EM`, `k_EM d`, `v_p`, `v_g`, `v_E`, `R_B`,
  `P_cross`, `H*`, `H_ref`, `H_bound`, `A_ijklmn` vs `H_jkl` are each defined
  once and used consistently after this round.
* **Physics vocabulary**: the paper keeps separate `R_B` (isolated backward
  self-power), total outgoing propagating power, `P_cross` (interference, not a
  channel), dissipated power, reactive evanescent content, and group vs phase
  velocity. No figure plots a reactive near-field quantity as transported
  energy.

---

## §11. Build, reproducibility and validation

Environment: Python 3.11.2, NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.11.2.

```
run_all_checks.py  ................................................ OVERALL: PASS
  test_model (20 checks) .......................................... PASS
  verify_dimensions (25 identities, contraction residual 2.2e-13) .. PASS
  quasistatic check (6 ratios) .................................... PASS
  flexoelectric control ........................................... PASS
  admissibility re-derivation (130/50/95 rows, 0 flips) ........... PASS
  figure data + figure files present .............................. PASS
  LaTeX static validation ......................................... PASS
      labels 100, references 61, citations 11/11, 8 files, ~13 879 tokens
  LaTeX build ..................................................... SKIP
```

New in this round: `phase_speed_audit.py`, `modal_flux_audit.py`,
`mechanism_controls.py`, `corner_assessment.py`, and the four JSON records
`phase_speed_audit.json`, `modal_flux_audit.json`, `mechanism_controls.json`,
`corner_assessment.json`. `quasistatic_check.py` was corrected to use
`λ_EM = 2π/k_EM`.

**TeX: no engine is available in this environment** (no `pdflatex`/`latexmk`/
`tectonic`; no package manager access; the network path used for a static
binary is blocked). The manuscript is therefore **statically validated but
compilation-unverified**. To build:

```
latexmk -pdf main.tex          # or:
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

`static_check.py` verifies balanced environments, every `\cite` key against
`references.bib`, every `\ref`/`\cref` against a `\label`, the presence of all
ten figure files, and a macro whitelist; it does not replace a compiler.

---

## What is still not established

1. **No compiled PDF** (no TeX engine). Layout-level defects (overfull boxes,
   wide tables) can only be found by compiling.
2. **Pointwise corner fields are not certified** (§F), and no 3-D model was
   introduced.
3. **The full constitutive equations of Qu et al. (IJES 2025)** were not
   accessible; the novelty statement is limited to the reproduced free-energy
   decomposition, and is marked `UNRESOLVED` for priority.
4. **The higher-order constants `ℓ`, `f`, `H` are synthetic.** No device-level
   ZnO prediction is made and none should be read into the percentages.
5. **The `ℓ = 0` control is a single-point statement** (this plate, frequency
   and `k_y`), not a general no-go theorem for classical piezoelectric
   semiconductors.

None of the above is a reason to call the paper Q1-ready. The round-4 defects
A–F are resolved to the evidence standard demanded; the paper's central claim is
now correctly attributed, and the remaining limitations are stated where a
referee will look for them.


---

# Round 5 addendum (2026-11-06)

The independent round-4 audit (`PAPER_A_ROUND4_INDEPENDENT_AUDIT.md`) confirmed
the package integrity, compiled the manuscript to 29 pages, re-ran the tests, and
found three defects. All three are corrected here; nothing else was rewritten.

## R5-1. Corner-study case selection — CONFIRMED—FIXED

Detailed in section F above. Summary of the change:

* `CASES` now maps `operating_point → K0 = 0.7361990195318475` and
  `peak → certify_peak.CASES['peak_candidate']`; `KB0 = 0.2451746921716515` is
  retained only as the `target_guess` that selects the backward port.
* The script asserts `|Re K_incident,returned − K_requested| < 1e-6` for every
  row, so a case can no longer be mislabelled silently.
* It cross-checks the operating-point rows against `peak_certification.json` and
  writes `certification_cross_check: PASS` into the JSON.
* Two regression tests were added (`test_model.py`, now 20 tests).
* Regenerated numbers: operating point 0.928–0.996 % corner-band share,
  peak/mean 0.098–0.102; peak 1.180–1.264 %, peak/mean 0.122–0.126.
* Manuscript limitations paragraph rewritten; the claim is now split into
  "the partitions are corner-insensitive" (supported) and "the corner line
  force is negligible" (**not** claimed).

**Unaffected, as required.** The corrected corner study changes nothing in the
reflection or energy-conservation results: its operating-point `R_B` now equals
the independently certified value at every degree (difference 0.0 in the stored
digits), and the peak rows were already correct (`R_B` 0.579179974 → 0.579180059
across degrees, matching `peak_certification.json`). The ten figures were not
touched.

## R5-2. LaTeX layout — CONFIRMED—FIXED (source level), compilation unverified here

The auditor reported overfull boxes of 102.17 pt, 4.14 pt and 372.96 pt, the
last being the appendix file/role table. Diagnosed by inspection of the source:

* **372.96 pt — appendix table.** `tab:package` was a two-column `tabular` with
  unbreakable `\texttt{}` paths (~45 characters) and prose in a plain `l`
  column, so the table had no defined width at all. Replaced by a
  `tabularx{\textwidth}` with a 0.34-`\textwidth` path column in
  `\ttfamily\footnotesize` and an `X` role column, both `\raggedright`, and the
  paths are now typeset with `\path{}` so they may break at `/`, `.` and `_`.
* **Long inline paths.** Fifty inline `\texttt{}` occurrences of paths ≥ 23
  characters (in results, discussion, numerical methods and governing equations)
  were converted to `\path{}` so that they can break inside a paragraph. These
  are the likely source of the 102.17 pt and 4.14 pt lines.
* **The two wide tables added in round 4** (`tab:controls`, `tab:novelty`) were
  also converted to `tabularx{\textwidth}`, so their width is the text width by
  construction and cannot overflow.
* `\usepackage{tabularx}` added; `\setlength{\emergencystretch}{2em}` added to
  absorb residual line-breaking slack **without changing any font size**.
* The appendix command block was shortened to ≤ 50 characters per line so that
  `verbatim` cannot overflow.

**Compilation status: unverified in this sandbox** — there is still no TeX
engine (no `pdflatex`/`latexmk`/`tectonic`/`xelatex`/`lualatex`, no package
manager access, and the network path for a static binary is blocked). The
structural argument above is why the previously overflowing constructs can no
longer overflow, but it is not a compiled check. The auditor's own 29-page build
establishes that the rest of the document compiles.

## R5-3. Appendix exit-status documentation — CONFIRMED—FIXED

`phase_speed_audit.py` returns **0 when the manuscript agrees with the
recomputation** and non-zero when it does not; it has done so since the round-4
values were corrected. The appendix previously said "exits non-zero by design",
which described the pre-correction state. Both the file table and the command
block now state the actual contract, and a new paragraph lists the exit status of
every script. Every command in the block was re-run on the shipped tree:

| command | exit | note |
|---|---|---|
| `run_all_checks.py` | 0 | OVERALL: PASS |
| `-m unittest paper_a_study.test_model -v` | 0 | 20 tests, 8.6 s |
| `reclassify_csv.py` | 0 | 275 rows re-derived, 0 flips |
| `phase_speed_audit.py` | 0 | all manuscript values agree |
| `modal_flux_audit.py` | 0 | rescaling 1.5e−15, degree 1.5e−7 |
| `mechanism_controls.py` | 0 | controls + branch sweep rewritten |
| `corner_assessment.py` | 0 | cross-check PASS |
| `scripts/static_check.py` | 0 | PASS, 11/11 citations |
| `build_figure_data.py`, `certify_peak.py`, `generate_final_figures.py`, `make_atlas.py` | not re-run | their outputs are unchanged and shipped; re-running them rewrites the same CSVs |

`build_figure_data.py` and `certify_peak.py` were **not** re-run in round 5 on
purpose: their outputs are the validated datasets and no defect in them was
demonstrated. `corner_assessment.py` was re-run and its JSON rewritten.

## R5-4. Preserved results

Untouched and re-verified in round 5: `v_p = 28.046 km/s`; `λ_EM = 5.6836 mm`,
`1/k_EM = 0.9046 mm`, `k_EM d = 2.211e−4`, `d/λ_EM = 3.519e−5`; the flux-normalised
`R_B` definition and its rescaling invariance; the `H = 0` mechanism controls
(57.92 % at the peak, no backward port at `ℓ = 0`); the 57.92 % peak
configuration; the strain-gradient and electrochemical-potential formulation; and
the ten vector PDF figures, byte-identical.

## R5-5. Final verification for this delivery

```
OVERALL: PASS
  test_model (20 checks) ................................. PASS
  verify_dimensions (25 identities) ...................... PASS
  quasistatic check ...................................... PASS
  flexoelectric control .................................. PASS
  admissibility re-derivation (275 rows, 0 flips) ........ PASS
  figure data + figure files ............................. PASS
  phase-speed and e.m. reconciliation .................... PASS
  modal-flux rescaling proof ............................. PASS
  mechanism matched controls ............................. PASS
  corner assessment + regression ......................... PASS
  LaTeX static validation ................................ PASS
  LaTeX build ............................................ SKIP (no engine here)
```

## R5-6. Still open

1. No compiled PDF produced **in this sandbox**; the layout fixes are argued
   structurally, not observed. The auditor's build is the reference compilation.
2. The corner line force is not certified (section F).
3. Novelty against Qu et al. (IJES 208 (2025) 104165) remains **UNRESOLVED**;
   no priority claim is made.
4. `ℓ`, `f` and `H` remain synthetic; no device-level ZnO prediction.
5. The `ℓ = 0` control is a single-point statement about this plate, frequency
   and `k_y`, not a general theorem; and its configurations follow a shifted
   branch frequency rather than being identical-frequency experiments, which
   the manuscript states.


---

# Round 6 addendum (2026-11-06)

One confirmed **compilation** defect, introduced by the round-5 layout repair,
is fixed here. No numerical, mathematical or figure content changed.

## R6-1. Fragile `\path` in captions — CONFIRMED—FIXED

**Evidence.** The independent reviewer's build aborted with
`! Undefined control sequence. \Url Error -> \url used in a moving argument.`
at `results.tex` line 69. **Cause:** round 5 converted 50 long inline paths from
`\texttt{}` to `\path{}` to remove the 372.96 pt / 102.17 pt overfull boxes;
fourteen of those conversions are inside `\caption` arguments, which are
written to the `.lof` by `\protected@write` and therefore require `\protect`.
**Fix:** `\protect\path{...}` at all fourteen sites (lines 69, 149, 184, 219,
234, 235, 363, 491, 528, 571, 607, 608, 642 of `sections/results.tex`).
`\DeclareRobustCommand` wrapping was rejected because `\path` sets catcodes on
its argument and a pre-tokenised argument does not carry them.
**Guard:** `scripts/static_check.py` now checks every `\caption`, `\section`,
`\subsection`, `\subsubsection` and `\paragraph` argument for unprotected
`\path`, `\url`, `\href`, `\nolinkurl`, and `run_all_checks.py` fails on a
hit. The guard was mutation-tested: deleting one `\protect` reproduces a FAIL
naming `sections/results.tex: line 69`, restoring it returns PASS.
**Verification:** static check PASS; the reviewer's build of this source is a
30-page PDF with no overfull boxes. **Not compiled here** — no TeX engine.

## R6-2. Environment recovery (process note, no source change)

The session started from a fresh checkout at the base commit without a Python
interpreter environment. The branch was restored with
`git fetch origin arena/ea7ca4dd-a-paper` + `git reset --hard` to `48029aa`
(working tree clean, zero difference from the audited tree), and the
environment was rebuilt at the versions the appendix declares. This is recorded
because it affects reproducibility provenance, not content.

## R6-3. Re-verification on the restored tree

`run_all_checks.py` → **OVERALL: PASS** (20 tests, 9 script-level checks);
corner cross-check PASS; the preserved values read back from JSON are
0.023145624 (2.3146 %), 0.579180059 (57.9180 %), corner shares
0.9278–0.9961 % and 1.1802–1.2643 %.

Unchanged open items: no PDF built in this sandbox, corner line force
uncertified, novelty vs Qu et al. **UNRESOLVED**, `ℓ`/`f`/`H` synthetic,
`ℓ = 0` control a single-point statement.
