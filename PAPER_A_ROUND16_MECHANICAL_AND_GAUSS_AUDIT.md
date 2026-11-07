# Round 16 — Mechanical and Gauss Audit

Two objects are audited here: the mechanical integration by parts with **all** of its
boundary terms, and Gauss's law with the mobile charge. Log:
`PAPER_A_ROUND16_AUDIT_LOG.txt` §3–§5.

---

## 1. Mechanical balance: signs of the two integrations by parts

Printed strong form (`eq:momentum`):
$\rho\ddot u_j=\partial_i\sigma_{ij}-\partial_i\partial_k\tau_{jik}$, with the effective
stress $\Sigma_{ij}=\sigma_{ij}-\partial_k\tau_{ijk}$ (`eq:effective`) so that
$\rho\ddot u_j=\partial_i\Sigma_{ij}$.

Virtual work (`eq:virtual_work`): $\delta W=\int_V[\sigma_{ij}\delta\varepsilon_{ij}+
\tau_{ijk}\delta\eta_{ijk}-D_i\delta E_i+\widetilde\mu\,\delta(\Delta n)]\dd V$.
With the time convention $\partial_t\to-\ii\omega$ the inertial term is
$\omega^2\int\rho\widehat u_jv_j^{*}$ with a **plus** sign on the right-hand side, so the
weak statement is

$$\int[\widehat\sigma_{ij}\widehat\varepsilon^{*}_{ij}(\vect v)
+\widehat\tau_{ijk}\widehat\eta^{*}_{ijk}(\vect v)]\dd\zeta
=\omega^2\int\rho\,\widehat u_j v_j^{*}\dd\zeta . \tag{1}$$

Integrating $\partial_i\sigma_{ij}$ once and $\partial_i\partial_k\tau_{jik}$ twice, and
using the contraction identity of §2 for the hyperstress, gives

$$\underbrace{\int\sigma:\varepsilon^{*}(\vect v)}_{\text{one IBP}}
=\underbrace{\bigl[t_jv_j^{*}\bigr]}_{\text{traction}}-\int(\partial_i\sigma_{ij})v_j^{*},$$

$$\underbrace{\int\tau\vdots\eta^{*}(\vect v)}_{\text{two IBPs}}
=\underbrace{\bigl[n_k\tau_{jik}\varepsilon^{*}_{ji}\bigr]}_{\text{double traction}}
-\underbrace{\bigl[n_k\partial_k\tau_{jik}v_j^{*}\bigr]}_{\text{surface divergence}}
+\int(\partial_i\partial_k\tau_{jik})v_j^{*},$$

so that (1) is equivalent to

$$\bigl[\Sigma_{3j}v_j^{*}+\tau_{ji3}\varepsilon^{*}_{ji}\bigr]_{-1}^{+1}
-\int\bigl(\partial_i\Sigma_{ij}+\omega^2\rho\widehat u_j\bigr)v_j^{*}\dd\zeta=0 .
\tag{2}$$

| Term | Origin | Sign in (2) | Vanishes because | Code |
|---|---|---|---|---|
| traction $t_j=n_i\Sigma_{ij}$ | first IBP on $\sigma$, minus the surface divergence of $\tau$ | $+$ | free face, `eq:bc_faces_mech` | `tr = e['S'][:,:,2]` (`model.py:300`) |
| double traction $n_k\tau_{jik}$ | second IBP on $\tau$ | $+$ | double-traction-free face | `rr = tensor_matrix(e['tau'][2])[:,:,2]` (`model.py:302`) |
| surface divergence $n_k\partial_k\tau_{jik}$ | second IBP on $\tau$ | $-$ (absorbed into $\Sigma$) | contained in $\Sigma_{ij}$ | `S = sigma - 1j*kx*tau[0] - 1j*ky*tau[1] - dtau[2]` (`model.py:190`) |
| edge / corner line forces | tangential derivatives on the faces | not present | infinite plate, no in-plane edges; the in-plane derivatives are Fourier multipliers | `state_operator` still carries natural corner forces in weak form (`model.py:206`) — item **M15-8, still unresolved**, not touched in round 16 |

The strong residual used in the auditors' checks is
`force + omega**2*u` with `force = 1j*kx*S[:,:,0] + 1j*ky*S[:,:,1] + Sz[:,:,2]`
(`model.py:294–296`), i.e. exactly $\partial_i\Sigma_{ij}+\omega^2\rho\widehat u_j$: the
sign of the inertial term in the code matches the plus in (1), which is the sign that
the $e^{-\ii\omega t}$ convention dictates. No defect found here.

## 2. The round-15 contraction identity: still applied correctly

`eq:contraction` states $\tau_{ijk}\delta\eta_{ijk}=\tau_{ijk}\delta u_{i,jk}$, and the
text of `governing_equations.tex` (l. 234–247) says in so many words that the two terms
of `eq:var_kinematics` "are not equal component by component, and this article does not
use them as such". That is the correct status: it is a **contracted** identity, valid
because $\eta_{ijk}=\eta_{jik}$ and $\tau_{ijk}=\tau_{jik}$ annihilate the antisymmetric
part of $\delta u_{i,jk}$.

The premise was checked in the code rather than asserted: for random coefficient
vectors at $k_y=0$ and $k_y=0.1298$,

$$\max|\tau_{ij}-\tau_{ji}|=0.00\times10^{0}\quad\text{for }l=x,y,z
\qquad(\text{scale }4.9\times10^{1},\,2.2\times10^{2}).$$

So $\tau$ is symmetric in its first pair to the last bit, the antisymmetric part is
annihilated exactly, and the identity may be used. The **component** statement
$\tau_{ijk}\delta\eta_{ijk}=\tau_{ijk}\delta u_{i,kj}$ (without symmetrisation) is not
used anywhere, and would be wrong.

## 3. Reciprocity and the location of the loss

At two kinematic points, with $n_w=23$:

| Pair | Relation | Measured relative asymmetry | Reading |
|---|---|---|---|
| $\mathsf A_{01}$, $\mathsf A_{10}$ | $\mathsf A_{01}=\mathsf A_{10}^{\mathsf H}$ | $3.22\times10^{-17}$ / $5.98\times10^{-17}$ | piezoelectric reciprocity holds |
| $\mathsf A_{12}$, $\mathsf A_{21}$ | $\mathsf A_{12}=\mathsf A_{21}^{\mathsf H}$ | $9.17\times10^{-17}$ | carrier–strain-gradient reciprocity holds |
| $\mathsf A_{22}$ | $\mathsf A_{22}=\mathsf A_{22}^{\mathsf H}$ | $0.00$ (exact) | quartic block real and symmetric |
| $\mathsf A_{02}$, $\mathsf A_{20}$ | both vanish | $0.00$ | round-15 item M15-3 confirmed |
| $\mathsf A_{00}$ | non-Hermitian | $4.87\times10^{-3}$ / $4.40\times10^{-3}$ | see below |
| $\mathsf A_{11}$ | non-Hermitian | $1.73\times10^{-3}$ / $1.56\times10^{-3}$ | see below |

Removing **only** the transport block from $\mathsf A_{00}$ and $\mathsf A_{11}$ restores
Hermiticity:

| Block | $\max$ asymmetry, raw | $\max$ asymmetry after removing $-\ii\frac{\alpha_{\mathrm d}}{\omega}
\langle\mathsf M\mathsf G_r,\mathsf M\mathsf G_r\rangle$ |
|---|---|---|
| $\mathsf A_{00}$ | $8.64\times10^{1}$ | $5.45\times10^{-13}$ |
| $\mathsf A_{11}$ | $2.40\times10^{-1}$ | $7.11\times10^{-15}$ |

so the carrier transport form is the **only** non-Hermitian contribution to the
construction, as the round-15 text asserts, and the loss sits where the physics puts it
(the carriers), not in the elastic, piezoelectric or flexoelectric blocks.

## 4. Gauss's law and the mobile-charge factor

Printed strong law: $\partial_iD_i=-q\Delta n$ (`eq:gauss`), $D_i=e_{ijk}\varepsilon_{jk}
+\kappa_{ij}E_j$, $E_i=-\partial_i\psi$. Dimensions: $[\partial_iD_i]=\mathrm{C\,m^{-3}}$
and $[q\Delta n]=\mathrm{C\,m^{-3}}$ — consistent.

**Scaling chain.** With lengths by $d$, $D_i$ by $\sqrt{c_{44}\kappa_{33}}$, and the
carrier amplitude by $\sqrt{c_{44}/a}$ (the unit fixed by the unit coefficient of
$-\langle\mathsf W_r,\mathsf W_s\rangle$ in `eq:block`),

$$\widehat\partial_i\widehat D_i=-\frac{q\,n_0\,d}{\sqrt{c_{44}\kappa_{33}}}\,\Delta\widehat n
=-Q\,\widehat N,\qquad Q=\frac{d}{L_D}=\frac{q\,d}{\sqrt{\kappa_{33}k_BT/n_0}}
\tag{3}$$

and indeed $q\,n_0d/\sqrt{c_{44}\kappa_{33}}=Q\sqrt{n_0k_BT/c_{44}}$ equals $Q$ times the
amplitude unit, so the two sides of (3) are the same statement. The code's residual
(`model.py:297–298`) is $\widehat\partial_i\widehat D_i+Q\widehat N$, i.e. (3).

**Does $\widehat N$ absorb $q$?** No. No charge survives the scaling: $q$ appears only
through $Q$, which is dimensionless and equal to $d/L_D$. Numerically $Q=0.074634887243$
(`model.py:38`) against $d/L_D=0.074637$ recomputed from the constants with $T=301.7$ K
— the $2.9\times10^{-5}$ difference is the rounded temperature, since the code derives
$T$ from the Einstein relation, $T=qD/(\mu_ek_B)=301.65$ K, which reproduces $Q$
identically by construction.

**Comparison with `eq:weak_gauss`.** The discrete $\varphi$-test row was rebuilt from
scratch on the model's own quadrature rule:

| Entry | Reconstructed | Assembled $\mathsf A_{00}$ | Deviation |
|---|---|---|---|
| $(\varphi_i,\mu_j)$ | $-Q\int\psi_ib_j$ | same | $3.72\times10^{-16}$ elementwise |
| $(\varphi_i,\varphi_j)$ | $-\kappa_{33}\int\psi_i'\psi_j'-\kappa_{11}k_y^2\int\psi_i\psi_j-Q^2\int\psi_i\psi_j$ | same | $1.13\times10^{-17}$ ($k_y=0$), $1.78\times10^{-15}$ ($k_y=0.1298$) |

The first row is the mobile charge: the assembled coupling carries the coefficient $Q$,
not $1$. The $Q^2$ term in the second row is the Debye screening produced by completing
the square in $\widehat N=\widetilde\mu+Q\widehat\varphi-h\partial_\zeta^2\widehat u_3$;
its presence is further evidence that the charge factor in the theory is $Q$.

Therefore the printed $-Q\int\widehat N\psi^{*}=0$ is the correct statement and the
earlier $-\int\widehat N\psi^{*}$ was off by $1/Q=13.4$. This is item **R16-3**,
repaired. Note that it is *not* a sign error: the sign of the charge term was right; the
coefficient was not.

## 5. What the audit did not do

* It did not re-derive the flexoelectric or piezoelectric constitutive signs from the
  material file; round 15 (M15-7) did that and it was confirmed there.
* It did not resolve the corner line force (M15-8). That item remains open and is
  reported as open, not as repaired.
* It did not compare the mechanical block elementwise against an independent assembly.
  The reciprocity and non-Hermiticity statements above are properties of the assembled
  blocks; the full elementwise mechanical comparison is outside what round 16 executed
  and is not claimed.
