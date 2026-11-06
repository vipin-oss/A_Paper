# Paper A — novelty and mechanism report (round 7)

## 1. Novelty against the primary literature: status UNRESOLVED

**Target.** Qu, Y., Pan, E., Zhu, F., Deng, Q., *A thermodynamically consistent
theory for flexoelectronics: interaction between strain gradient and electric
current in flexoelectric semiconductors*, Int. J. Eng. Sci. **208**, 104165
(2025), DOI 10.1016/j.ijengsci.2024.104165.

**Access check executed this round** (OpenAlex work record, `LIT`):

```
open_access.status = "closed"
open_access.oa_url = null
any_repository_has_fulltext = false
locations_count = 1
```

No repository, preprint or author copy is indexed. The primary constitutive
equations therefore **could not be inspected**, and no comparison against them
is possible in this round either. Any statement that the added term is absent
from that article would be unsupported.

**Substitute comparison (open access).** Hu, H., Liu, Z., Liu, Q., Jiang, X.,
Zhuang, X., Rabczuk, T., *Computational flexoelectronics: a framework for
analyzing PN junctions in flexoelectric semiconductors*, Int. J. Mech. Sci.
**305**, 110740 (2025), DOI 10.1016/j.ijmecsci.2025.110740 — OpenAlex
`oa_status = "hybrid"`, i.e. readable. This article reproduces the Qu et al.
free-energy decomposition with attribution in its Eqs. (4a)–(4e).

### Equation-level matrix

| # | Element | Qu et al. 2025 as transcribed in Hu et al. Eqs. (4a)–(4e) | This paper | Status |
|---|---|---|---|---|
| 1 | Independent state variables | ε, g = ∇ε, e = −∇φ, n, p | ε, g, e, Δn (single carrier) | same variables, one carrier |
| 2 | Mechanical energy | ½C_ijkl ε_ij ε_kl + ½H_ijklmn g_ijk g_lmn | same, with A ≡ H (fourth-order in strain, second order in gradient) | **equivalent**, notation differing |
| 3 | Dielectric coupling | Ψ_Diele = −η_ijk e_i ε_jk − μ_lijk e_l g_ijk | same structure (piezoelectric + flexoelectric) | **equivalent** |
| 4 | Carrier energy | Ψ_Carrier = n{k_Bϑ[n ln(n/N_C) − 1] + E_C0} + p{…} — a function of n and p alone | same, linearised about n_0, plus Δn H_jkl ε_jk,l | **differs by the added term** |
| 5 | Electrochemical potential | ∂Ψ/∂n = μ_n + qψ, no strain-gradient contribution | + H_jkl ε_jk,l | differs by the reciprocal of the added term |
| 6 | Higher-order stress | τ_ijk = ∂Ψ/∂g_ijk (hyperstress) | same + H_ijk Δn | differs by the reciprocal |
| 7 | Reciprocal thermodynamic structure | Coleman–Noll, all couplings from one potential | same construction, the added term enters with both reciprocals | **same methodology** |
| 8 | Carrier transport | drift–diffusion, D = (k_Bϑ/q)M, SRH recombination | linearised drift–diffusion, no recombination | narrower |
| 9 | Boundary conditions | mechanical + electrical + carrier | same classes, plus higher-order traction and a corner term discussed explicitly | comparable |
| 10 | Reduction under a change of variables | — | no transformation of the inspected decomposition reproduces Δn H_jkl ε_jk,l, because the inspected carrier energy has no strain-gradient argument | **not equivalent**, as far as the inspected equations go |

**What can and cannot be claimed.**

* Can be claimed: within the decomposition that is open access and that
  reproduces the primary theory, the carrier sector depends on n and p alone, so
  a bilinear Δn × strain-gradient enthalpy is an addition rather than a change
  of variables.
* Cannot be claimed: priority, absence from Qu et al. (2025), or equivalence.
  Both the manuscript and this report say so explicitly, and the manuscript's
  comparison table marks the status "absent in the inspected equations".

### Where the contribution does stand independently of that question

1. **The scattering problem.** The literature verified in this round treats
   dispersion in half-spaces and layered media (Biswas & Sahu 2025; Wang et al.
   2025; Zhang et al. 2025), and reflection at a free surface only as plane-wave
   reflection coefficients in a half-space (Mondal, Sahu & Nirwal 2022). No
   prior work located here partitions a *guided plate branch* into the discrete
   outgoing spectrum of a free edge.
2. **The backward branch as the operative object.** The conversion is a property
   of the strain-gradient plate branch, quantified at 93.19 % at its maximum.
3. **The quantified role of the carrier coupling.** One per cent at the
   operating point, a third at the branch maximum, mediated by the added
   attenuation — a statement about a specific, reproducible configuration.

## 2. Mechanism: what the controls establish

All configurations hold k_x, k_y, n_0, ℓ, the reference plane and the incident
normalisation fixed; only the named ingredient changes, and the frequency follows
the branch because switching an ingredient off changes the dispersion.

| Configuration | R_B (k_xd = 0.736) | R_B (k_xd = 0.525) | R_B (k_xd = 0.550) | Backward port |
|---|---|---|---|---|
| full (f_0, H = +0.05H\*) | 0.022866 | 0.623427 | 0.522107 | yes |
| f = f_0, H = 0 | 0.023146 | 0.931891 | 0.579180 | yes |
| f = 0, H = +0.05H\* | 0.022869 | 0.623427 | 0.522153 | yes |
| f = 0, H = 0 | 0.023148 | 0.931808 | 0.579245 | yes |
| ℓ = 0, f = 0, H = 0 | 0.077296 (specular) | 0.135106 (specular) | 0.125061 (specular) | **no** |

Readings, each traceable to the table:

1. **The branch, not the coupling, produces the conversion.** With H = 0 the
   same branch returns 93.19 % at its maximum. Removing the strain-gradient
   sector removes the backward port altogether: the only negative-power outgoing
   mode left is the specular reflection at K = −k_inc.
2. **The flexoelectric sector is neutral here** (≤ 0.011 % at every reported
   point). The paper consequently does not claim a flexoelectric mechanism.
3. **The coupling acts through loss.** At the branch maximum the axial decay rate
   of the backward mode rises from 4.7e-4 to 8.4e-3 per unit thickness when H is
   switched on, so R_B falls from 0.9319 to 0.6234 (−33.1 %); referred to the
   edge plane the reduction is 21.6 %, so 11.5 points are propagation loss over
   the ten thicknesses to the reference plane and the remainder is a genuine
   reduction of the conversion.
4. **The ordering is configuration-dependent, not universal.** k_y moves the
   partition by a factor 1.35 across the solved box and H by 1.21 % at the
   operating point; at the branch maximum H is the larger of the two effects
   (−33.1 %). The manuscript states the ordering per configuration rather than
   globally.

**Why 93 % is not "total reflection".** At the branch maximum the total outgoing
propagating self-power is 0.99000 of the incident power and the interference
correction is −9.97e-3, so the partition is 93.19 % backward, 5.81 % into the
other propagating modes, with 1 % of interference content at the reference
plane. The manuscript quotes the modal share and the energy statement separately
and never calls R_B a reflectance.

**Slow-mode reading (inference, labelled as such).** The maximum sits where the
group velocity vanishes (v_g = −3 m/s against 355 m/s at the end of the window).
A slow branch spends longer near the edge per unit length, so the evanescent
spectrum has more opportunity to redistribute energy before the wave leaves.
This is an interpretation consistent with the data; it is not derived.

## 3. What changed in the *scientific* claim

| | Round 6 | Round 7 |
|---|---|---|
| Maximum of R_B | 57.92 % at k_xd = 0.55 | **93.19 % at k_xd = 0.5250** (0.5792 retained as the value at k_xd = 0.55) |
| Position of the maximum | "at the zero-group-velocity point" | at the zero-group-velocity point (v_g = −3 m/s), **confirmed** by a refined sweep instead of assumed from a coarse one |
| Coupling effect | "bounded perturbation" | −1.21 % at the operating point, −9.85 % at k_xd = 0.55, **−33.1 %** at the branch maximum, mediated by attenuation |
| Novelty | unresolved | **still unresolved**, now with the access status documented machine-checkably and the gap statement narrowed to the guided-plate-edge problem |
