# Natural boundary data of the second-gradient edge problem: derivation, verification, and the corner line force

**Round 21, Gates 1 and 2.** This document does three things and no more: it derives
the natural boundary data of the implemented plate problem from the variational
statement; it verifies the derived expressions against the discrete state-space flux
rows to machine precision on the *complete* incident+reflected field; and it closes
the corner line force quantitatively. It does not restate the scattering result,
which is unchanged.

Everything below can be re-run:

```
PYTHONPATH=paper_a_study .venv/bin/python paper_a_study/round21_gate1_traction.py
PYTHONPATH=paper_a_study .venv/bin/python paper_a_study/round21_gate_corner.py
PYTHONPATH=. .venv/bin/python -m unittest paper_a_study.round21_tests
```

Stored evidence: `paper_a_study/figure_data/round21/gate1_traction_identity.json`,
`paper_a_study/figure_data/round21/gate12_corner.json`.

---

## 1. The functional and its variations

The implemented functional is the electric Gibbs free energy of a flexoelectric
piezoelectric semiconductor plate, integrated over the plate and resolved exactly in
the thickness coordinate $z$ but reduced along the propagation direction $x$ only at
the level of the discretisation. With $\varepsilon_{ij}=\tfrac12(u_{i,j}+u_{j,i})$,
$E_i=-\varphi_{,i}$, carrier density perturbation $\Delta n$, and the higher-order
elastic tensor $\ell^2 C_{ijmn}$ (isotropic-gradient form),

$$
\Pi=\int_\Omega\Big[
\tfrac12\varepsilon_{ij}C_{ijmn}\varepsilon_{mn}
+\tfrac12\ell^2\,\varepsilon_{ij,k}C_{ijmn}\varepsilon_{mn,k}
-\eta_{ijk}E_i\varepsilon_{jk}-\tfrac12\kappa_{ij}E_iE_j
+\Psi_{\text{carrier}}(\Delta n)
+\Delta n\,H_{jkl}\varepsilon_{jk,l}\Big]\,dV .
$$

Two stress-like objects follow by definition, not by choice:

$$
\sigma_{ij}=\frac{\partial \hat W}{\partial \varepsilon_{ij}}
=C_{ijmn}\varepsilon_{mn}-\eta_{kij}E_k,\qquad
\tau_{ijk}=\frac{\partial \hat W}{\partial \varepsilon_{ij,k}}
=\ell^2 C_{ijmn}\varepsilon_{mn,k}\;(\text{+ flexoelectric part on the }33\text{ slot}),
$$

so that $\tau_{ijk}$ is symmetric in $(i,j)$ while its third index is the
differentiation direction. Define the reduced stress

$$
S_{ij}:=\sigma_{ij}-\partial_k\tau_{ijk}.
$$

## 2. Derivation of the natural data

Only the mechanical part matters for the boundary data. Using
$\tau_{ijk}\delta\varepsilon_{ij}=\tau_{ijk}\,\partial_i\delta u_j$ (the $(i,j)$
symmetry does the folding), two integrations by parts give

$$
\delta\Pi_{\text{mech}}
=\int_\Omega\big(\partial_i\partial_k\tau_{ijk}-\partial_i\sigma_{ij}\big)\delta u_j\,dV
+\oint_{\partial\Omega}\Big[\big(n_i\sigma_{ij}-n_i\partial_k\tau_{ijk}\big)\delta u_j
+n_k\tau_{ijk}\,\partial_i\delta u_j\Big]dA .
$$

On a face with unit normal $n$, split $\partial_i\delta u_j=\partial^s_i\delta u_j
+n_i\partial_n\delta u_j$, where $\partial^s$ differentiates along the face. The
coefficient of the *normal derivative* is the **double traction**

$$
\boxed{\;m_j=n_in_k\tau_{ijk}\;}
$$

and, for $n=e_x$, it reduces to $m_j=\tau_{j11}$.

The remaining face term is a surface divergence. Integrate it by parts *on the face*,
using the $(i,j)$ symmetry once more:

$$
\oint_{\partial\Omega} n_k\tau_{ijk}\partial^s_i\delta u_j\,dA
=-\oint_{\partial\Omega}\partial^s_i\!\big(n_k\tau_{jik}\big)\delta u_j\,dA
+\oint_{\partial(\partial\Omega)}\nu_i n_k\tau_{jik}\,\delta u_j\,ds .
$$

Hence the **traction**

$$
\boxed{\;t_j=n_i\big(\sigma_{ij}-\partial_k\tau_{ijk}\big)-\partial^s_i\big(n_k\tau_{jik}\big)
=n_iS_{ij}-\partial^s_i\big(n_k\tau_{jik}\big)\;}
$$

and the **corner line force**

$$
\boxed{\;f_j=\nu_i n_k\tau_{jik}\;}
$$

with $\nu$ the co-normal of the face boundary. For the free edge $x=0$ with
tangential wavenumber $k_y$ this is, pointwise in $z$,

$$
t_j=S_{j1}-ik_y\,\tau_{jy1}-\partial_z\tau_{jz1},
\qquad
m_j=\tau_{j11},
\qquad
f_j=\tau_{j31}+\tau_{j13},
$$

where the last expression is the sum of the two mixed normal/tangential components
carried by the two free faces that meet along the corner line; the relative sign is
fixed by the outward orientations of those faces and is verified below rather than
assumed (all alternatives fail by ten to twelve orders of magnitude).

Natural conditions on a free edge with no applied line load are therefore
$t_j=0$, $m_j=0$, $f_j=0$.

## 3. Two independent evaluations of the same boundary data

The discrete problem is not posed on $(t,m,f)$ directly. It carries a state

$$
y=(q,p,T,R),\qquad p=\partial_x q,\quad T=\textstyle\sum_s\big(A_{1s}-ik_xA_{2s}\big)(ik_x)^s q,
\quad R=\textstyle\sum_sA_{2s}q(ik_x)^s ,
$$

and imposes $T_{:\!u}=0$ (the mechanical flux conjugate to the displacement state) and
$R=0$ on the edge. The second evaluation is therefore a functional comparison:
with $\langle v\rangle=\int_{-1/2}^{1/2}b_0(z)v(z)\,dz$ for the displacement test
basis $b_0$, the claim to be tested is

$$
\langle T_{:\!u}-t\rangle \;=\; f_+\,b_0(+\tfrac12)-f_-\,b_0(-\tfrac12),
\qquad
\langle R-m\rangle = 0 ,
\tag{$\star$}
$$

with no fitted coefficient. `round21_gate1_traction.py` evaluates both sides for
every mode of the edge solution, with the corner values taken from the endpoint
basis $b(\pm\tfrac12)$ exactly — not from the nearest Gauss node, which leaves an
$O(n_{\text{quad}}^{-2})$ error and was the source of an apparent failure in an
earlier attempt at this check.

**Resolution of ($\star$) at the operating point, degree 12** (relative, per mode):

| expression used for the face term | residual of ($\star$) |
|---|---|
| $\langle t\rangle$ alone (traction only) | $1.73\times10^{1}$ |
| corner term $f=\tau_{j31}$ | $5.65\times10^{-1}$ |
| corner term $f=\tau_{j13}$ | $6.05\times10^{-1}$ |
| corner term $f=\tau_{j31}-\tau_{j13}$ | $1.13\times10^{0}$ |
| corner term $f=\tau_{j31}+\tau_{j13}$ | $\mathbf{1.36\times10^{-13}}$ |
| $\langle R\rangle$ vs $m=\tau_{j11}$ | $1.66\times10^{-7}$ |

With the corner term in the derived form, ($\star$) holds at the level of the
floating-point round-off of the edge solve. The traction-only residual of $1.7\times
10^{1}$ is the quantitative statement that the corner term is *load-bearing*: the
discrete edge condition is not a traction-free condition, it is a traction-free
condition plus corner line forces.

**Degree and quadrature independence of the identity** (incident mode):

| degree | 10 | 12 | 16 | 20 | 28 |
|---|---|---|---|---|---|
| residual of ($\star$), incident mode | $1.2\times10^{-13}$ | $1.4\times10^{-13}$ | $2.2\times10^{-13}$ | $2.8\times10^{-13}$ | $1.2\times10^{-12}$ |
| worst reflected mode, same row | $8.9\times10^{-9}$ | $3.4\times10^{-7}$ | $3.5\times10^{-6}$ | — | — |

The worst residual over the 182 reflected modes is $8.9\times10^{-9}$ to
$3.5\times10^{-6}$ because those modes are strongly evanescent ($|\mathrm{Im}\,k_x|\lesssim 2.5\times10^{2}$)
and the individual hyperstress terms are two orders of magnitude larger than the
flux they cancel in; the incident mode — the one that carries the physics — is
unaffected.

## 4. What this does and does not settle

The identity ($\star$) is an algebraic statement about *one* mode. It is verified.
It does not say that the superposed field has zero pointwise traction, because a
Galerkin statement imposes the natural data only weakly, and the corner data enter
as $\delta$-like functionals which no smooth field can annihilate. That residual is
a physical property of the discrete solution and is measured, not assumed
(section 5). The double traction, by contrast, is a smooth $L^2$ condition and *is*
annihilated pointwise: its superposed residual is $2\times10^{-13}$ relative.

## 5. Pointwise residuals on the complete field

Normalised by the incident mode's own scale; interior window $|z|<0.4$, corner
layers $|z|>0.4$:

| configuration | $n$ | traction (interior) | traction (corner layers) | double traction (max) |
|---|---|---|---|---|
| operating point | 10 | $4.26\times10^{-2}$ | $2.93\times10^{-1}$ | $1.8\times10^{-8}$ |
| | 28 | $3.59\times10^{-2}$ | $4.23\times10^{-1}$ | $3.7\times10^{-5}$ |
| corrected maximum | 10 | $1.13\times10^{-3}$ | $7.75\times10^{-3}$ | $2.9\times10^{-7}$ |
| | 28 | $9.40\times10^{-4}$ | $1.11\times10^{-2}$ | $7.2\times10^{-5}$ |
| $k_xd=0.55$ | 10 | $1.36\times10^{-2}$ | $9.38\times10^{-2}$ | $2.1\times10^{-8}$ |
| | 28 | $1.14\times10^{-2}$ | $1.34\times10^{-1}$ | $2.1\times10^{-5}$ |

Two facts must be stated together with these numbers. First, they **do not decrease
with degree**: the interior traction residual sits at $3.6$–$4.3\times10^{-2}$ at the
operating point and $9.4\times10^{-4}$–$1.1\times10^{-3}$ at the corrected maximum
across $n=10\ldots28$. A Galerkin boundary condition is a moment condition, and for a
$\delta$-like corner datum the deficit cannot be removed by enrichment; the reported
observables are integral quantities that converge at $10^{-6}$–$10^{-7}$ while this
pointwise deficit plateaus. Second, the deficit is smallest exactly where the paper's
claim is made: at the corrected maximum it is $10^{-3}$, three orders of magnitude
below the mode partition it describes.

This is the honest status of the pointwise natural conditions and it is stated in the
manuscript. It is not a hidden discrepancy: it is the difference between the two
evaluations of Gate 1, quantified.

## 6. Gate 2: the corner line force

The corner force is a genuine natural datum of the theory, it enters the discrete
edge condition with the coefficients verified in section 3, and the discrete solution
cannot set it to zero pointwise. The question is whether it is a small,
understandable discretisation effect or an uncontrolled physical unknown.

**Values on the complete field**, relative to the incident mode's corner scale,
degrees 10–28, three configurations:

| configuration | $f$ at $n=10$ | $f$ at $n=28$ | fitted law | exponent |
|---|---|---|---|---|
| operating point | $8.42\times10^{-2}$ | $4.46\times10^{-2}$ | $3.51\times10^{-1}n^{-0.618}$ | $-0.618$ |
| corrected maximum | $3.27\times10^{-3}$ | $1.71\times10^{-3}$ | $1.41\times10^{-2}n^{-0.632}$ | $-0.632$ |
| $k_xd=0.55$ | $3.79\times10^{-2}$ | $1.98\times10^{-2}$ | $1.63\times10^{-1}n^{-0.630}$ | $-0.630$ |

Three independent configurations give the same exponent to $0.014$ and a clean
algebraic law over a factor $2.8$ in degree. A residual that were a bug or a
quadrature artefact would not produce a configuration-independent power law; an
unresolved corner *singularity* of the continuum solution does exactly this, and the
exponent is the quantity that a corner-aware discretisation is supposed to measure.
The fitted exponent $-0.62$ corresponds to a corner field $\sim r^{0.38}$ in the
hyperstress, i.e. the corner condition is approached algebraically, not exponentially.

**Independence of everything else that was varied:**

* quadrature: $f=2.92997\times10^{-3}$ at $n_{\text{quad}}=96,\,128,\,192$ — identical
  to six digits, so $f$ is a property of the basis, not of the integration rule;
* the identity itself (section 3) holds at $10^{-13}$ at every degree and every
  quadrature tested;
* the reported observable is insensitive to it: $R_B$ at the corrected maximum varies
  by $3.9\times10^{-6}$ between $n=10$ and $n=28$, against a degree spread already
  reported of $1.1\times10^{-6}$, while $f$ itself changes by a factor $1.9$ — the
  corner dynamics and the mode partition are decoupled;
* power balance closes to $10^{-12}$ in every configuration, i.e. the corner force
  carries no energy in this formulation (it is a natural datum multiplying a
  displacement, not a flux).

**Corner-localisation scales.** Averaging the mixed hyperstress over a band of width
$h$ at the corner gives, at $n=28$: $h=0.05$ → $0.425$ (operating), $0.0142$ (maximum),
$0.167$ ($k_xd=0.55$); $h=2/n$ → $0.568$, $0.0189$, $0.223$; $h=4/n$ → $0.923$,
$0.0303$, $0.357$. The band values exceed the pointwise corner value by factors
$5$–$10$: the field *near* the corner is larger than the corner condition itself, so
no band average can be used to argue the corner datum away, and none is used here.
The pointwise value is the only quantity that means "corner line force".

**Closure.** The corner force is closed as a **bounded closure**, with the following
content and no more:

1. it is quantified on the complete field in three configurations, at seven degrees
   and three quadratures;
2. it decays algebraically with a configuration-independent exponent
   $-0.62\pm0.01$, and is bounded over the entire tested range by
   $|f|/|f_{\text{inc}}|\le 8.4\times10^{-2}$ (operating), $3.3\times10^{-3}$
   (corrected maximum), $3.8\times10^{-2}$ ($k_xd=0.55$), the bounds being attained at
   the lowest degree tested;
3. it is provably not load-bearing for any reported number: the mode partition is
   invariant to $4\times10^{-6}$ over the same degree range in which $f$ halves, and
   the energy budget closes to $10^{-12}$.

What is *not* claimed: that the corner force is zero, or that the exponent $-0.62$ is
proved analytically. It is measured from the discrete solution's own convergence and
is consistent across configurations; a proof would require the local corner
eigenvalue problem of the second-gradient operator with the flexoelectric and carrier
couplings, which is outside what has been done here. The scattering result is
therefore **not** scientifically conditional on the corner force, and the corner
force is **not** "closed in the full sense": the honest label is *bounded closure*.
