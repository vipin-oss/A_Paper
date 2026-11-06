# PAPER A — A0 bounded prior-art and equation audit

**Date:** 2026-11-05 UTC  
**A0 decision:** **REVISE** — do not call ν H_jkl ε_jk,l a new coupling until the specified primary constitutive laws, especially Qu Appendix C, have been inspected.

## 1. Scope and evidence discipline

This audit is limited to the **four papers requested**. Searches for copies of those same papers were access attempts, not an expanded novelty program. No claim of a first-ever coupling follows from an abstract, title, citation list, choice of material, or the fact that a paper studies SH rather than Lamb waves.

The relevant question is narrow:

> Does the existing energy contain `ν B_jkl ε_jk,l`, or does its carrier chemical/electrochemical potential already contain `B_jkl ε_jk,l`, together with the reciprocal hyperstress?

Here ν = Δn is **electron number concentration**, not charge density or relative concentration. Tensor order, units, reference-volume convention, and a possible integration by parts must be reconciled before declaring a difference.

**Important access limitation:** only Zhang's governing equations and material table were retrieved in full. The publisher returned previews for Fang, Wei, and Qu, including on the attempted PDF routes. Targeted title/identifier searches did not yield an accessible primary full text. A targeted search of the connected Drive for these identifiers/titles returned zero matching files. Consequently, an exact constitutive-equation audit of those three papers is **unfinished**. Their unavailable equation numbers are not invented below.

## 2. Primary-source ledger

| Label | Requested primary source | Retrieved mathematical content | Not retrieved |
|---|---|---|---|
| **F25** | X. Fang, L. Wang, J. Lou, H. Fan, J. Du, *Flexoelectricity and size effects on SH surface waves in a nanoscale piezoelectric semiconductor layered medium*, *Applied Mathematical Modelling* **141**, 115928 (2025), [DOI](https://doi.org/10.1016/j.apm.2025.115928), [publisher preview](https://www.sciencedirect.com/science/article/abs/pii/S0307904X25000034) | Abstract, introduction, section snippets; free-surface potential continuity displayed as Eq. (20), with references to Eqs. (13b), (16) | Energy, full constitutive equations, carrier law, material table |
| **W26** | C. Wei, Z. Guo, J. Tang, W. Huang, *Dynamic flexoelectric effect in semiconductors: A study on wave propagation*, *Applied Mathematical Modelling* **150**, Part A, 116353 (2026), [DOI](https://doi.org/10.1016/j.apm.2025.116353), [publisher preview](https://www.sciencedirect.com/science/article/abs/pii/S0307904X25004275) | Abstract, introduction and snippets describing Sections 2–5; displayed plane-wave ansatz in the dispersion snippet | Numbered constitutive/chemical-potential equations, complete series field equations |
| **Q25** | Y. Qu, E. Pan, F. Zhu, Q. Deng, *A thermodynamically consistent theory for flexoelectronics: Interaction between strain gradient and electric current in flexoelectric semiconductors*, *International Journal of Engineering Science* **208**, 104165 (2025), [DOI](https://doi.org/10.1016/j.ijengsci.2024.104165), [publisher preview](https://www.sciencedirect.com/science/article/abs/pii/S0020722524001496) | Introduction, section map, snippets explicitly referencing Eqs. (2.6a,b), (2.11), (2.15), (4.19), and **Appendix C** | Actual chemo-mechanical energy/chemical-potential law and Appendix C equations |
| **Z25** | L. Zhang, Z. Zhao, X. Hu, G. Nie, J. Liu, *Exact multi-field coupling modeling and analysis of piezoelectric semiconductor plates*, *Applied Mathematics and Mechanics* **46**(7), 1331–1346 (2025), [DOI](https://doi.org/10.1007/s10483-025-3272-7), [full journal HTML](https://www.amm.shu.edu.cn/article/2025/0253-4827/0253-4827-2025-07-1331.shtml) | Full Sections 2–5, Appendix A, Table 1, and reference attribution | No material f, A or H constants: these are not part of its displayed model |

The 2025 DOI of W26 is consistent with its 2026 issue date; it is not a second paper. Q25's DOI contains 2024 while its volume is dated March 2025. Neither date convention establishes novelty.

## 3. Exact equation-level findings

### 3.1 Z25 — direct inspection completed

**Locations:** Section 2, **Eqs. (1)–(5)**; Section 4.2, **Eqs. (30)–(31)**; **Table 1**; **Appendix A**.

- Eq. **(1)** collects `(u1,u2,u3,φ,ν)` as generalized unknowns and `(σ,D,J)` as responses.
- Eq. **(2)** is a generalized first-gradient constitutive relation.
- Eq. **(3)** lists its nonzero coefficient blocks. In conventional notation these give

  ```text
  σ_jk = C_jkmn ε_mn − e_ijk E_i,
  D_i  = e_ijk ε_jk + κ_ij E_j,
  J_i  = q n0 M_ij E_j + q d_ij ν_,j.
  ```

  In particular, the `J=5,K=4` generalized block is `−q0 n0 μ_il` and the `J=K=5` block is `q0 d_il`. All other unlisted blocks are zero. There is no strain-gradient kinematic variable, no hyperstress, and no direct carrier–strain-gradient force in this specified model.
- Eq. **(4)** contains momentum balance, `div D = −q0 ν`, and `div J = q0 ν_,t`. These signs are consistent with conventional electron current and positive q0.
- Eq. **(5)** is the classical five-field boundary prescription. It must **not** be reused unchanged for two fourth-order mechanical equations in the present plane-strain gradient model.
- Eqs. **(30)–(31)** give free-surface vibration conditions and a characteristic determinant. The accompanying text explicitly treats the frequency as **complex** because carriers move. Its time convention is `exp(+iωt)` in Eq. **(6)**; the A0 implementation uses `exp(−iωt)`, so the stable imaginary-frequency sign reverses.

**Conclusion for Z25:** the proposed H term is **absent from the inspected constitutive system**, and cannot be generated merely by rewriting its existing drift–diffusion law. This establishes absence in **Z25 only**, not novelty relative to the other three papers.

### 3.2 F25 — relevant equations not accessible

The retrieved preview describes flexoelectricity, strain-gradient elasticity, electric-field gradient and micro-inertia in a ZnO/diamond SH configuration. Those existing mechanisms must not be relabeled as this paper's new mechanism.

The accessible free-surface snippet displays **Eq. (20)** as continuity of electric potential with vacuum, and refers to **Eqs. (13b), (16)**. These are **not** the carrier chemical-potential or enthalpy equations and do not resolve H's presence. The fact that an SH specialization can suppress some tensor contractions also would not prove their absence from the full constitutive model.

**Exact H-related equation reference:** **unavailable — full text needed**.  
**Finding:** **unresolved**, not “H absent.”  
**Material cross-check:** **unresolved**, not “same constants as Zhang.”

### 3.3 W26 — relevant equations not accessible

The preview describes dynamic flexoelectricity, micro-inertial contributions, nonlocal/size-dependent effects, and a second-order plate expansion. Its numerical snippet identifies **Nb–SrTiO3**, not ZnO. None of those existing effects is added to the fixed one-coupling Paper A model.

The retrieved section map identifies **Section 2** (series-form field equations), **Section 3** (second-order truncation), and **Section 4** (dispersion). The constitutive/chemical-potential equations themselves, with their numbers, are not exposed.

**Exact H-related equation reference:** **unavailable — full text needed**.  
**Finding:** **unresolved**. A centrosymmetric numerical example would forbid an odd-rank polar H for that material, but does not by itself determine what the paper's general constitutive theory permits.

### 3.4 Q25 — the most consequential unresolved check

The introduction explicitly says **“Appendix C provides the constitutive equations for chemo-mechanical couplings.”** This is a source-verified reason to inspect that appendix before claiming the proposed coupling as new.

The preview's constitutive section mentions carrier continuity **Eqs. (2.6a,b)**, electrostatics **Eq. (2.11)** and motion **Eq. (2.15)**. Its analytical-solutions snippet points to the linearized problem **Eq. (4.19)**. These references are visible, but **their complete equation bodies do not establish the H law**. They must not be represented as if Appendix C had been read.

**Required exact locations:** the Section 3 free-energy dependence and carrier chemical-potential derivatives, the linearization leading to **Eq. (4.19)**, and **Appendix C**.  
**Exact H-related equation numbers within those locations:** **unavailable — full text needed**.  
**Finding:** **unresolved, with a specific close-prior-art warning**. This is not evidence that Q25 definitely contains H, nor evidence that it does not.

## 4. Equivalence test to apply to those three full texts

This is a mathematical test derived for A0, **not a transcription of an unavailable paper**.

1. **Direct enthalpy test.** Search for a bilinear carrier/strain-gradient term, allowing notation such as `N, δn, η_ijk, G_ij,k` and a different tensor order. Translate the carrier normalization before comparing numerical coefficients.
2. **Chemical-potential test.** If the existing law contains

   `μ_n^chem = a ν + B_jkl ε_jk,l + ...`,

   integration with respect to ν gives `½aν² + ν B_jkl ε_jk,l + ...`. Up to normalization/sign conventions, this is the proposed H energy. It is **not a new coupling** merely because its reciprocal hyperstress is now displayed.
3. **Reciprocity test.** A reversible energy law also gives `τ_jkl^(carrier) = ν B_jkl`. If a published transport law lacks this reciprocal term, distinguish “thermodynamically completing/restricting a published law” from discovering a new coupling. Do not assume that absence without the equations.
4. **Integration-by-parts test.** For constant H,

   ```text
   ∫ ν H_jkl ε_jk,l dV
     = ∮ ν H_jkl ε_jk n_l dS − ∫ H_jkl ν_,l ε_jk dV.
   ```

   An existing carrier-gradient/strain law may therefore describe the same bulk interaction. The surface functional and corresponding natural boundary conditions must be compared too; dropping them can create a false difference.
5. **Mediated versus direct interaction.** Carrier redistribution caused by ordinary flexoelectric polarization plus electrostatics is not automatically a direct constitutive ν–strain-gradient term. Conversely, calling a coefficient “chemical,” “band-edge,” or “deformation potential” does not make it different if the same derivative law results.
6. **Elimination test.** Neutral, instantaneous algebraic carrier relaxation reduces H to a gradient-modulus correction; charge-retaining or finite-rate elimination is generally nonlocal/frequency-dependent. The explicit exceptions and a numerical comparison are in `PAPER_A_A0_CONSTITUTIVE_CHECK.md`. They prevent an overstated claim of independent physics in an equivalent limit.

## 5. Permitted contribution statement at A0

Safe wording:

> We examine whether a symmetry-allowed direct carrier–strain-gradient coupling, retained reciprocally in hyperstress and electrochemical transport, supplies an identifiable model extension for backward guided-mode conversion in a ZnO plate.

Unsafe wording now:

- “The H coupling is introduced for the first time.”
- “None of Fang, Wei, Qu or Zhang contains it.”
- “The proposed physics is new because those papers used another material, wave polarization, or plate approximation.”
- “Negative reflection follows from a backward dispersion segment.”

If Q25 or the other specified equations already contain the same term, the claim **that H itself is new must be withdrawn**. That would require the user's decision on the contribution; it is not permission to add another field or independently redesign Paper A.

## 6. Finite closure request and stopping rule

Obtain the full texts of **F25, W26 and Q25**, including F25's material table and Q25 Appendix C. Then fill exactly three missing equation-audit rows, cross-check conventions/parameters, and decide whether H is a genuine extension of the selected base or only a specialization/rewrite.

No additional papers, physical couplings, alternative materials, Papers B/C, or new theoretical program are authorized by this audit. The A0 reports are delivered with the evidence gap explicit; the novelty gate remains closed until these finite checks are completed.
