# Round 16 — Conventions and Dimensions

**Scope.** This file fixes the fourteen conventions on which every later statement of
round 16 depends, states each one exactly, and records where it is *stated* in the
manuscript and where it is *implemented* in the code. Nothing here is taken from a
previous audit report; each row was checked against the source text and against
`paper_a_study/model.py` in this checkout.

**Repository state at the time of writing.** branch `arena/ea7ca4dd-a-paper`,
starting HEAD `23ec30ee7817b85a791cff30624973b8ec453088`, working tree clean before
the first edit. `main` was not touched.

---

## 1. The fourteen conventions

| # | Convention | Exact statement | Stated at | Implemented at | Verdict |
|---|---|---|---|---|---|
| 1 | Time dependence | $f=\widehat f(z)\,e^{\ii(k_xx+k_yy-\omega t)}$, hence $\partial_t\to-\ii\omega$ | `governing_equations.tex`, `eq:ansatz` (l. 497) | `model.py:302` `-1j*omega*f['N'][0]`; `model.py:151` `omega=1j*s` | consistent |
| 2 | Spatial transform | $\partial_x\to\ii k_x$, $\partial_y\to\ii k_y$; $k_x$ is *retained* (polynomial), $k_y$ is a parameter | `eq:ansatz` derivative block (l. 501–512) | `model.py:97–100` (`strains`), `model.py:167–168` (`MG`), `model.py:196` (`polynomial`) | consistent |
| 3 | Number flux | $J_i=-\dfrac{Dn_0}{k_BT}\partial_i\widetilde\mu$, units $\mathrm{m^{-2}s^{-1}}$ | `eq:continuity` (l. 302–304) | carried implicitly by the gradient operator `MG` (`model.py:167–168`) with coefficient $\alpha_{\mathrm d}$ (`model.py:39,185`) | consistent |
| 4 | Charge current | $j_i=-qJ_i$ (electron sign) | `eq:current` (l. 312–316) | not stored; enters only through $\widehat N$ and $Q$ | consistent |
| 5 | Charge sign in Gauss | $\partial_iD_i=-q\Delta n$, "the minus sign being the charge of the electron" | `eq:gauss` (l. 295–298) | `model.py:297–298` residual `∇·D + Q*N` | consistent |
| 6 | Electrochemical potential | $\widetilde\mu=\partial w/\partial\Delta n$, unit **J** | `tab:conjugates` (l. 333) | `f['mu']`; scaled by $k_BT$ (l. 476) | consistent |
| 7 | Diffusivity | $D=\SI{4.55e-4}{m^2/s}$ | `reference_constants.json`, `tab:groups` | `Plate(diffusivity=.000455)` | consistent |
| 8 | Mobility | $\mu_e=\SI{0.0175}{m^2 V^{-1}s^{-1}}$ | `tab:groups` caption (l. 587) | `Plate(mobility=.0175)` | consistent |
| 9 | Einstein relation | $D=\mu_ek_BT/q$, equivalently $T=qD/(\mu_ek_B)$; the temperature is *not* independent | l. 306–310, caption of `tab:groups` | `model.py:37` `self.a=CONST['q']*diffusivity/(mobility*n0)` | consistent |
| 10 | Carrier diffusivity group | $\alpha_{\mathrm d}=D/(dc_s)$, $c_s=\sqrt{c_{44}/\rho}$ | `eq:dissipation` (l. 472), `tab:groups` | `model.py:39` `self.alpha=diffusivity/(d*self.cs)`, `model.py:185` | consistent (0.828294163284 reproduced to 12 digits) |
| 11 | Test functions | $(\vect v,\psi,\Phi)$ drawn from the same spaces as the trials | `numerical_methods.tex` (l. 52) | basis objects `b`, `pb` shared by trial and test | consistent |
| 12 | Conjugation | inner product $\langle\vect a,\vect b\rangle=\int_{-1}^{1}\vect a^{*\mathsf T}\vect b\,\dd\zeta$; the test factor is conjugated **once** | `numerical_methods.tex` (l. 122–125) | `form` does *not* conjugate (`model.py:91–92`); callers pass `B[r].conj()` / `MG[r].conj()` (`model.py:180,185`) | consistent |
| 13 | Boundary flux sign | $J_z=0$ is the natural condition of the carrier equation; $D_z=0$ that of Gauss's law; grounded $\widehat\varphi=0$ is essential and built into the space | `bc_faces_carrier`, `numerical_methods.tex` l. 71 | `model.py:80–88` (`ground` / `open` spaces) | consistent |
| 14 | Thickness orientation | $z\in[-d/2,d/2]$, scaled $\zeta$, faces at $\zeta=\pm1$, outward normal $\pm\vect e_z$; quadrature on $[-1/2,1/2]$ with the chain factor $2$ carried by the basis | `numerical_methods.tex` l. 30–47 | `model.py:66–79` (`basis`), `model.py:66` comment | consistent |

**Who conjugates.** Convention 12 is the one that is easiest to get wrong and it is the
one that decides the carrier sign, so it is recorded explicitly: `Plate.form` is a
plain `einsum` (`model.py:91–92`) and never conjugates; the conjugation is applied by
the caller through `left.conj()`. Inside `matrices` this happens for every block
(`B[r].conj()`, `G[r].conj()`, `MG[r].conj()`, `U.conj()`). The carrier transport
block is therefore $-\frac{\ii\alpha_{\mathrm d}}{\omega}\langle \mathsf M\mathsf G_r,
\mathsf M\mathsf G_s\rangle$, a pure phase times a *positive* real form, which is what
the dissipativity test of round 16 confirms ($\max|\Re|=0$, $\min\operatorname{eig}F=5.588\times10^{-1}>0$).

---

## 2. Dimension ledger

No equation in this report, and none in the round-16 derivation report, mixes a
dimensional with a scaled quantity. The two families are:

| Quantity | Dimensional | Scaled | Scale |
|---|---|---|---|
| length, coordinate | $z$ | $\zeta$ | $d$ |
| time | $t$ | $\tau$ | $d/c_s$ |
| frequency | $\omega$ (rad/s) | $\omega$ (dimensionless) | $c_s/d$ |
| displacement | $u_i$ | $\widehat u_i$ | $u_0$ (elastic) |
| stress / hyperstress | $\sigma,\tau$ | $\widehat\sigma,\widehat\tau$ | $c_{44}$ |
| strain | $\varepsilon$ | $\widehat\varepsilon$ | $u_0/d$ |
| potential | $\varphi$ | $\widehat\varphi$ | $d\sqrt{c_{44}/\kappa_{33}}$ |
| electric displacement | $D_i$ | $\widehat D_i$ | $\sqrt{c_{44}\kappa_{33}}$ |
| carrier density | $\Delta n$ | $\widehat N$ | $\sqrt{c_{44}/a}$, $a=k_BT/n_0$ |
| electrochemical potential | $\widetilde\mu$ (J) | $\widetilde\mu$ (dimensionless) | $k_BT$ |
| number flux | $J_i$ | — | $\sqrt{c_{44}/a}\,c_s$ |
| charge current | $j_i$ | — | $q\sqrt{c_{44}/a}\,c_s$ |

The carrier normalisation row is the one that matters for the Gauss factor: the
manuscript's `eq:block` writes the compressibility as $-\langle\mathsf W_r,\mathsf
W_s\rangle$ with unit coefficient, which fixes the unit of $\widehat N$ as
$\sqrt{c_{44}/a}$; with that unit the scaled Gauss law is
$\widehat\partial_i\widehat D_i=-Q\widehat N$ with $Q=d/L_D$, which is what the
code assembles (`model.py:297`) and what round 16 verifies numerically to
$3.7\times10^{-16}$ (see `PAPER_A_ROUND16_MECHANICAL_AND_GAUSS_AUDIT.md`).

---

## 3. Two dimensional inconsistencies found and repaired

| ID | Where | Before | After | Why |
|---|---|---|---|---|
| R16-2 | `eq:continuity` | $q\,\partial_t(\Delta n)+\partial_iJ_i=0$ with $J_i$ a **number** flux | $\partial_t(\Delta n)+\partial_iJ_i=0$, with a sentence stating that the charge balance is the same equation multiplied by $-q$ | $q\partial_t\Delta n$ has units $\mathrm{C\,m^{-3}s^{-1}}$ and $\partial_iJ_i$ has $\mathrm{m^{-3}s^{-1}}$: the printed pair cannot be equal. The charge form is $\partial_t(-q\Delta n)+\partial_ij_i=0$ |
| R16-3 | `eq:weak_gauss` | $-\int\widehat N\psi^{*}$ | $-Q\int\widehat N\psi^{*}$ | the scaled charge of `eq:gauss` is $Q\widehat N$, not $\widehat N$; verified against the assembled $\varphi$–$\mu$ block |

Both are transcription-level. Neither changes a constant, a boundary condition, a
dataset, a figure or a result: the code contains no $q$ in either place, and
$Q=0.0746349$ is the value it already used.

Two related statements were checked and left alone:

* `eq:gauss` itself, $\partial_iD_i=-q\Delta n$: dimensionally exact
  ($\mathrm{C\,m^{-3}}$ on both sides).
* the amplitude statement "$\partial_i\widehat J_i=\ii\omega\widehat N$" of
  `sec:governing_reduction` (l. 534): the spurious $q$ that had been carried there was
  removed in the same pass (item R16-2b), so the amplitude statement now agrees with
  `eq:continuity` and with `eq:weak_carrier`.

---

## 4. What was *not* changed

* No material constant, no boundary condition, no quadrature rule, no basis, no
  solver line, no dataset, no figure. `git diff` for round 16 touches two `.tex`
  files and no `.py` file that computes anything; the only new `.py` file is the
  audit script `paper_a_study/round16_carrier_sign_audit.py`, which is read-only
  with respect to the model.
* The round-14/15 restructuring, the author's prose style and all ten figures are
  untouched.
* `main` is untouched; nothing was pushed anywhere but `arena/ea7ca4dd-a-paper`.
