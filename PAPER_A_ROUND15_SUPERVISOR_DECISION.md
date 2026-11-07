# Round 15 — supervisor decision

Separate verdicts. No blanket pass. "Verified" always means *executed in this
round*; a round-14 result re-used is labelled as such.

| Area | Verdict | Basis |
| --- | --- | --- |
| **Constitutive mathematics** | **CORRECT, unchanged** | `eq:sigma`–`eq:mu` re-derived from `eq:enthalpy`; the added coupling still has exactly two conjugate partners; `D`/`σ`/`τ` sign conventions checked block by block against the assembled operator. No constant, tensor or coupling changed. |
| **Variational derivation** | **REPAIRED — now correct** | The false component identity `δη = δu_jk` was confirmed false (`0.962` component-wise) and replaced by the contracted identity, proved by relabelling and verified numerically (`3.3e-16`). The balance laws now follow from written integrations by parts with the sign of the double divergence justified. |
| **Carrier-continuity weak form** | **REPAIRED — now correct and faithful** | Round 14 showed the enthalpy term `μ̃N*` in place of the transport equation and omitted the mobile charge from Gauss's law. Both are corrected: (A) mechanical, (B) Gauss with charge, (C) time-harmonic continuity, (D) assembled block system. The implemented residual `−iωN − α_d∂∂μ̃` is exactly (C) multiplied by `iω`. |
| **Quartic operator** | **CORRECT; presentation repaired** | Regrouping verified as an identity (`≤3.6e-12` absolute at four wavenumbers); `A₀₂ = A₂₀ = 0` identically now stated; Hermiticity of the odd and leading blocks verified (`≤1.8e-12`); the non-Hermitian part identified as the carrier-transport form. |
| **Boundary conditions** | **CORRECT for faces and edge; CORNER UNRESOLVED** | Traction and double traction written out from the surface terms; face conditions annihilate them; edge conditions are the boundary rows. The corner line force is non-zero (`>1e-4`), not resolved, and reported as a limitation — not papered over with an added condition. |
| **Figure readability** | **Figure 5 PASS; Figure 8 PASS; both after full-size inspection** | F5: legend off the `10⁰` curve, floor annotation moved. F8: colliding tick labels fixed, dotted zero reference, coincidence of the five levels stated with the measured bound (`<0.9 %`), legend clear. Data unchanged; figure-data tests pass. Other eight figures were re-rendered unchanged this round. |
| **LaTeX build** | **NOT VERIFIED here — environmental** | No TeX engine in this environment (checked again). Static validation passes (112 labels, 85 refs, 13/13 citations, no macro violations). The nomenclature table — the one real typesetting defect found — is repaired at source. Buildability on the supervisor side is unaffected: no preamble, package or environment changed. |
| **Numerical integrity** | **INTACT** | 52/52 tests, claim audit PASS, mutation tests PASS, phase audit exit 0. No solver, constant, dataset or figure data was modified. |
| **Unresolved scientific limitations** | **UNCHANGED AND VISIBLE** | Corner line force; closed-form block entries not claimed; novelty `UNRESOLVED` (closest work closed access); `ℓ`, `f`, `H` synthetic; five `AUTHOR INPUT REQUIRED` declarations still unfilled; three of five author papers not obtainable, so the style comparison rests on two. |
| **Readiness for supervisor review** | **READY, with three named risks** | The mathematics is now stated correctly and matches what is implemented. The risks are: (i) no compiled page from this environment, so layout is unverified; (ii) the long `eq:block` may need a line-break at 22 mm margins; (iii) the corner term remains a physical limitation of the model. |

## What changed this round, in one paragraph

Three mathematical statements were wrong or incomplete and are now correct: the
strain-gradient variation (a contraction identity, not a tensor identity), the
"weak form" (three weak equations, not one, with the carrier transport equation
stated as such and the mobile charge restored in Gauss's law), and the quartic
block structure (two blocks vanish identically; the Hermitian structure is now
stated). Two notation/typesetting defects are repaired: `α` had two meanings, and
the nomenclature table declared five columns for four-column rows. Figures 5 and
8 were inspected at reading size and repaired. Nothing physical moved.

## What did **not** change

Material constants; the governing model; accepted boundary conditions; the
scattering solver; root classification; the peak `0.9467952` at `k_xd = 0.5275`
(still a **local** maximum of the declared window); `94.68 %` (still the backward
outgoing modal **self-power fraction**); `−34.2 %` / `+1.21 %` coupling effects;
the energy balance (`4×10⁻¹²`); every dataset; every reported number.

## Honest summary

The paper's mathematics now matches its implementation, and the two figures that
were previously flagged as unreadable were inspected and repaired rather than
declared fit. It is still not a typeset paper: no page exists from this
environment, one figure's long equation block may break badly at 22 mm margins,
and the corner force remains a genuine limitation of the model. A supervisor who
finds those three sentences acceptable can read the manuscript; a supervisor who
wants a rendered PDF must build it in an environment that has TeX.
