# PAPER A — A0-R novelty comparison

**Checkpoint:** focused supervisor correction, 2026-11-05.

**Finding: NOVELTY UNRESOLVED.** Qu's actual Appendix C constitutive equations were not accessible. No finding of absence, equivalence, or special-case inclusion is justified.

The objective, ZnO material family, plate/reflecting-edge geometry and single added interaction remain those of [Blueprint V2.1](PAPER_A_BLUEPRINT_V2_1.md). This is an evidence correction, not a new blueprint or a manuscript. No edge solver was built.

## 1. Exact comparison requested

The proposed additional free-energy/enthalpy density is

\[
\Delta\mathcal H=\nu H_{jkl}\varepsilon_{jk,l},\qquad \nu=\Delta n.
\]

Here \(\nu\) is **electron number-concentration perturbation**, not automatically interchangeable with charge density, electron fraction, or a concentration defined using another volume measure. With constant coefficients, its two reciprocal constitutive contributions are

\[
\Delta\tau_{jkl}=H_{jkl}\nu,\qquad
\Delta\widetilde\mu=H_{jkl}\varepsilon_{jk,l}.
\]

The complete chemical potential in the retained linear model is

\[
\widetilde\mu=a\nu+H_{jkl}\varepsilon_{jk,l}-q\phi,
\qquad a=k_BT/n_0>0,
\]

and the particle flux is \(\Gamma_i=-L_{ij}\widetilde\mu_{,j}\), \(L_{ij}=n_0M_{ij}/q\). Consequently H also changes the drift–diffusion driving force. The extra hyperstress cannot be omitted while keeping the chemical force.

The direct primary-equation comparison would identify

\[
H_{jkl}\stackrel{?}{=}
\left.\frac{\partial^2\psi_Q}
{\partial\nu\,\partial\varepsilon_{jk,l}}\right|_{\rm reference}
\]

in Qu's consistently linearized potential, with the corresponding reciprocal law and boundary terms. **This derivative has not been evaluated from Qu: the required equations were not obtained.** The displayed expression is a comparison criterion, not a reconstructed Qu equation.

## 2. Bounded Qu-only access result

**Primary target:** Y. Qu, E. Pan, F. Zhu and Q. Deng, *A thermodynamically consistent theory for flexoelectronics: Interaction between strain gradient and electric current in flexoelectric semiconductors*, *International Journal of Engineering Science* **208**, 104165 (2025), DOI [10.1016/j.ijengsci.2024.104165](https://doi.org/10.1016/j.ijengsci.2024.104165).

| Access route | Actual result | Does it expose Appendix C's constitutive equations? |
|---|---|---|
| [ScienceDirect full-article route](https://www.sciencedirect.com/science/article/pii/S0020722524001496), abstract and attempted PDF routes | Preview/organizational-access content. Appendix C is named, but its equations are not supplied. | **No** |
| [Public Elsevier article XML request](https://api.elsevier.com/content/article/pii/S0020722524001496?httpAccept=text%2Fxml) | Metadata, not the full mathematical article. A successful response is not full-text access. | **No** |
| Exact-title/identifier searches for Qu, Appendix C and an accessible PDF | No accessible primary Appendix C found. Citing-paper snippets were not substituted for it. | **No** |
| Connected Drive, nontrashed full-text/name search using `104165`, `flexoelectronics`, `Flexoelectronics`, `Qu 2025` | **0 matching files**, search reported complete. Earlier exact-identifier/title searches also found no copy. | **No** |

The access ledger is retained in [`a0r/protocol.json`](a0r/protocol.json). No paywall was bypassed, no inaccessible equation number was invented, and no broad literature expansion was undertaken. This bounded access check is complete; the **substantive comparison remains incomplete**.

## 3. Equation-by-equation comparison status

| Required item | Proposed one-H model: inspected/derived | Qu Appendix C: actually inspected | Determination |
|---|---|---|---|
| Carrier variable and density measure | \(\nu=\Delta n\), number-concentration perturbation in the retained small-strain convention; no identification with Qu's volume measure assumed | Not available | Conversion unresolved |
| Cross term \(\nu H:\nabla\varepsilon\) in energy | Explicitly present | Not available | Presence/absence unresolved |
| Chemical term \(H:\nabla\varepsilon\) | Explicitly present | Not available | Equivalence unresolved |
| Reciprocal hyperstress \(H\nu\) | Explicitly present | Not available | Equivalence unresolved |
| Linearization and coefficient specialization | Small strain, isothermal, 6mm, constant coefficients | Relevant Appendix C equations unavailable | Special-case relation unresolved |
| Integration-by-parts and surface terms | Explicit identity below | Relevant surface/constitutive equations unavailable | Functional equivalence unresolved |

Qu's title, thermodynamic framing, or the phrase “strain gradient and electric current” cannot determine these entries. Conversely, the failure to retrieve an equation is **not evidence that the coupling is absent**.

### Conventions that must be reconciled when the primary equations become available

1. **Density normalization:** if a source uses \(r=\nu/n_0\), the coefficient multiplying \(r\nabla\varepsilon\) is \(n_0H\). If it uses electron charge perturbation \(\rho_e=-q\nu\), the corresponding coefficient is \(-H/q\). Chemical energy per carrier and voltage per charge are different quantities.
2. **Finite-to-small deformation:** compare potentials in the same volume measure and reference state before identifying linear coefficients. A finite-deformation general framework may contain the linear term as a specialization; its title alone cannot establish that.
3. **Engineering shear:** in sagittal plane strain,
   \[
   H:\nabla\varepsilon
   =h_a u_{3,33}+(h_b+h_c)u_{1,13}+h_c u_{3,11}.
   \]
   The factors associated with \(2\varepsilon_{13}\) must be handled consistently.
4. **Integration by parts:** for constant H,
   \[
   \int_V\nu H_{jkl}\varepsilon_{jk,l}\,dV
   =-\int_VH_{jkl}\nu_{,l}\varepsilon_{jk}\,dV
   +\int_{\partial V}\nu H_{jkl}\varepsilon_{jk}n_l\,dS.
   \]
   A strain–carrier-gradient representation is not automatically a different mechanism. Dropping the surface integral changes the finite-plate problem.
5. **Elimination is conditional:** local neutral equilibrium gives \(A_{\rm eff}=A-H\otimes H/a\). Charged finite-rate drift–diffusion generally produces a frequency-/wave-number-dependent, nonlocal response instead. A renormalized coefficient in one closure does not establish equivalence of the complete dissipative boundary-value problem.

## 4. Retained mathematical status, not a novelty claim

The existing exact checks give three independent 6mm coefficients:

\[
H_{333}=h_a,\quad H_{113}=H_{223}=h_b,\quad
H_{131}=H_{311}=H_{232}=H_{322}=h_c.
\]

Their units are J m with the number-concentration convention. Reciprocity, symmetry allowance and stability make the interaction **mathematically permissible**; none proves that it is unpublished.

A0-R tests all three directions within this **same one coupling**, using explicitly synthetic \(A=\ell^2 C\otimes I\). No additional coupling or field is introduced. The physical H range is still unknown; the full-3D Schur bound is an admissibility condition, not a measured range. See the [feasibility report](PAPER_A_A0R_BACKWARD_WAVE_FEASIBILITY.md).

The earlier equation-level finding for Zhang's classical model remains limited to its inspected first-gradient equations. The earlier Fang/Wei equation/table gaps are retained as limitations, **not expanded into another search programme** during this correction.

## 5. Supervisor conclusion

- **Actual Qu Appendix C comparison completed? No.**
- **H absent from Qu? Not established.**
- **H equivalent to Qu's coupling? Not established.**
- **H a special case of Qu? Not established.**
- **Permitted novelty wording: NOVELTY UNRESOLVED.**

A primary copy of Qu's Appendix C and its definitions is the finite missing evidence. No claim that this is a new constitutive interaction should enter a manuscript without that comparison. No further literature search, manuscript work or later phase is started here.

**STOP after the A0-R [decision](PAPER_A_A0R_DECISION.md).**
