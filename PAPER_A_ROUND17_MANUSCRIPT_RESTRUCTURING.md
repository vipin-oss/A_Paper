# Paper A — Round 17 manuscript restructuring (Parts A and B)

**Branch** `arena/ea7ca4dd-a-paper` · **base** `a68bb76` (round 16) · **date** 2026-11-07
**Verdict on the TeX build: BUILD UNVERIFIED.** No TeX engine exists in this
environment (`pdflatex`, `latexmk`, `xelatex`, `lualatex`, `tectonic`, `bibtex`
all absent), so nothing in this report is a claim that the PDF compiles or that
any page was inspected. The static checks that *can* be run were run and pass;
they are named where they are used.

---

## 1. What changed, file by file

| File | Sub-sections before | after | Equations before | after | Net lines |
|---|---|---|---|---|---|
| `governing_equations.tex` | 11 | **5** | 28 | 44 | +461 / −97 |
| `numerical_methods.tex` | 5 | **3** | 10 | 16 | +95 / −20 |
| `results.tex` | 15 | **7** | 0 | 1 | +76 / −55 |
| `discussion.tex` | 1 wrapper | **5** (as `\section` + 4 `\subsection` + limitations) | 1 | 1 | +226 / −180 |
| `appendix_derivations.tex` | — | **new, 6** | — | 16 | new file |
| `main.tex` | — | — | — | — | +10 / −4 |

Prose word count (including math tokens, `static_check.py`): 17 021 → **20 036**.
Labels 112 → **160**; references 86 → **98**. Citations unchanged at 13/13.

The delta is derivation, not restatement: every added equation is a step that
was previously skipped, and no equation restates another. `static_check.py`
reports **PASS** (labels/refs/citations/macro whitelist/document structure) at
keyword level; it does not and cannot check TeX syntax.

---

## 2. Part A — the dimensions table and the symbols

**Removed:** `tab:units` (five-row dimensions table). It duplicated information
that the equations themselves carry, and it was the table that made the
introduction of `\tau_{ijk}` and `H_{jkl}` read as a list rather than a
derivation.

**Replaced by** one paragraph in `sec:governing_constitutive` that derives each
unit from the derivative that produces it:

* `u_i` → m; `ε_ij` dimensionless; `η_ijk` → m⁻¹ (all three stated where they
  first appear, not in a list);
* `σ_ij = ∂w/∂ε_ij` and `c_ijkl` → Pa; `τ_ijk = ∂w/∂η_ijk` → **N m⁻¹**, with the
  reason stated in words (*a force per unit length, and not a stress*);
* `A_ijklmn = ∂τ/∂η` → **N** (*a force, one factor of length times the
  stiffness*);
* `e_kij` → C m⁻²; `κ_ij` → F m⁻¹; `f_ijkl = ∂D_i/∂η_jkl = ∂τ_jkl/∂E_i` → C m⁻¹;
* `Δn` → m⁻³; `μ̃` → J; `a = k_BT/n_0` → J m³; `H_jkl = ∂μ̃/∂η_jkl` → **J m**.

The three non-classical units (N for `A`, N m⁻¹ for `τ`, J m for `H`) are named
explicitly as the ones that are easy to mis-state. No second table was created,
and the Nomenclature is untouched.

**Second table audit.** `tab:conjugates` (conjugate pairs, force, relation, unit
of force, origin) was removed for the same reason: its four rows are exactly the
four relations `eq:sigma`, `eq:tau`, `eq:D`, `eq:mu`, and its unit column is now
prose. The one cross-reference to it (`numerical_methods.tex`, "the six blocks of
`tab:conjugates`") now points at `eq:sector_blocks`, which is where the blocks are
actually defined.

**Tables retained (5):** `tab:groups` (dimensionless groups — numerical),
`tab:provenance` (parameter provenance — factual), `tab:refinement`,
`tab:configurations`, `tab:controls` (all numerical). No table in the manuscript
carries a status column any more (see the table report).

---

## 3. Part B — sub-section counts

### Mathematical formulation: 11 → 5

| New heading | Absorbs | Labels stacked under it |
|---|---|---|
| Geometry, kinematics and the gradient energy | geometry + kinematics | `sec:governing_variational`, `sec:governing_kinematics` |
| Constitutive relations and the balance laws | enthalpy/constitutive + balance laws | `sec:governing_constitutive`, `sec:governing_balance` |
| The electric model, the boundary conditions and the energy flux | electrostatics + BCs + power flux | `sec:governing_electric`, `sec:governing_bc`, `sec:governing_energy` |
| Plane-wave reduction and the characteristic polynomial | (reduced) | `sec:governing_reduction` |
| Non-dimensionalisation, limits and admissibility | nondim + limits + admissibility | `sec:governing_nondim`, `sec:governing_limits`, `sec:governing_stability` |

The section-opening roadmap was rewritten to describe this five-part order, so
the reader is not told about a structure the section no longer has.

### Solution: 5 → 3

| New heading | Absorbs |
|---|---|
| Thickness discretisation and the assembly of the blocks | basis + weak forms + block assembly |
| Modes, the free-edge system and the conditions on a reported share | temporal/spatial routes + edge matching + admissibility |
| Consistency and independent checks | verification list, reworded (see the vocabulary report) |

### Results: 15 → 7

| New heading | Absorbs |
|---|---|
| Dispersion, wave speeds and the operating point | dispersion + material specialisation/flexoelectric role |
| Dependence on carrier density, thickness and frequency | three parameter sweeps |
| The branch maximum and its convergence | convergence + location of the maximum |
| The maximum read as a modal share and the energy budget of the edge | modal share + energy budget |
| What creates the backward channel, and how far it survives | mechanism + attenuation |
| Coupling sensitivity and the through-thickness flux | `(k_y,H)` sweep + flux profiles |
| Independent cross-checks and the near field | cross-checks + field figure |

All 15 original labels survive, so every existing `\cref` still resolves — the
static check confirms 98 references against 160 labels with no undefined target.

### Discussion

The file previously began with a `\subsection` and therefore rendered as a
sub-section of *Numerical results and discussion*. That was a structural defect,
and it is the reason the results section carried the word *discussion* in its
title. It is now a `\section{Discussion}` with four `\subsection`s
(observable, mechanism, literature, provenance) and the limitations as five
numbered points at its end. The results section is now titled *Numerical
results*. Intro remains a single `\section` with no sub-sections, as required.

### Appendix

A new mathematical Appendix A (`app:derivations`, six sub-sections) precedes the
existing numerical-resolution appendix, which becomes Appendix B. Appendix A is
mathematics only: no commands, no paths, no test vocabulary.

---

## 4. What was deliberately *not* done

* No science was changed. The material constants, the constitutive model, the
  boundary conditions, the carrier operator with its `+iα_d/ω` transport sign,
  the energy-flux definitions and the local-peak classification are untouched;
  the figure **data** files are byte-identical (the only change under
  `figure_data/` is the recorded hash of the re-rendered PDFs/PNGs).
* No section was shortened by deleting content. Prose that moved between
  sub-sections moved verbatim except where a report below records an edit.
* No new table was introduced to replace a removed one.
* No claim of compilation, and no claim that the paper is publication-ready.

## 5. Residual structural risks (unverifiable without an engine)

1. `cleveref` *is* loaded (`main.tex` line 30), so the stacked labels on one
   heading resolve to one section number; what cannot be checked without an
   engine is whether `\cref{a,b,c}` prints the number once or repeats it, and
   whether any `\cref` that used to point at a *sub*-section number now prints a
   parent number (the target is unchanged, the depth is not).
2. `main.tex` now inputs `sections/appendix_derivations` before
   `sections/appendix_reproducibility`; both use `\section`, so they letter A and
   B automatically *provided* neither contains a `\section*`.
3. The `siunitx` change (`group-digits=integer`, `group-minimum-digits=5`,
   `output-decimal-marker={.}`) requires `siunitx` v2.5+ or v3; both accept these
   keys, but only an engine can confirm the installed version.
