# Independent strong-equation validation used in A0-S

This document derives an **independent uniform-plate check**, not another material model, new field, or edge solver. It is restricted to the explicitly executed subset **f = 0, A_ijklmn = ℓ² C_ijkl δ_mn**, with the retained reciprocal H. No claim is made that this uncalibrated subset represents the complete flexoelectric ZnO material. The eight-state classical check is retained for ℓ = H = 0.

## 1. Scaling and constitutive equations

Use total thickness d; z = x3/d ∈ [−1/2,1/2], K = k d, Ω = ω d/cs, cs = √(c0/ρ), c0 = c44(reference). The convention is exp(i k x1 − i ω t). Let κ0 = κ33(reference), θ = qD/M, a = θ/n0. Normalizations are

\[
u_i=dU_i,\quad \phi=d\sqrt{c_0/\kappa_0}\,\Phi,
\quad\nu=\sqrt{c_0/a}\,N,
\quad\widetilde\mu=\sqrt{a c_0}\,\mu.
\]

Here the first symbol is displacement **u_i**, not carrier perturbation ν. Below all elastic, piezoelectric and dielectric coefficients are dimensionless:

\[
\bar C=C/c_0,\quad \bar e=e/\sqrt{c_0\kappa_0},
\quad \bar\kappa=\kappa/\kappa_0,
\quad\lambda=\ell/d,\quad
\bar h_\alpha=H_\alpha/(d\sqrt{a c_0}),
\]

\[
Q=qd/\sqrt{\kappa_0 a},\qquad
\alpha=D/(d c_s),\qquad \epsilon=\epsilon_0/\kappa_0.
\]

Bars are suppressed in the following equations. Prime means d/dz. Engineering strain is

\[
\boldsymbol\varepsilon=(iKU_1,U_3',U_1'+iKU_3)^T,
\quad G\Phi=(iK\Phi,\Phi')^T.
\]

For sagittal plane strain, with C in the (11,33,13-engineering) order,

\[
\sigma=C\varepsilon+e^TG\Phi,\quad
D=e\varepsilon-\kappa G\Phi,
\]

\[
m^x=\lambda^2 iK C\varepsilon+(0,0,h_c)^T N,
\quad m^z=\lambda^2 C\varepsilon'+(h_b,h_a,0)^T N,
\quad S=\sigma-iKm^x-(m^z)',
\]

\[
\mu=N+h_aU_3''+(h_b+h_c)iKU_1'-h_cK^2U_3-Q\Phi,
\quad \Gamma_3=-\alpha\mu',\quad \Gamma_1=-\alpha iK\mu.
\]

The tensor identifications are H333 = ha, H113 = H223 = hb, H131 = H311 = H232 = H322 = hc. They are three components of **one reciprocal energy coupling**, not three extra interactions. The full three-dimensional Schur bound, including the inactive plane-strain components, is checked separately and is not replaced by the weaker reduced denominator below.

Bulk equations are

\[
 iKS_{11}+S_{13}'=-\Omega^2 U_1,\qquad
 iKS_{13}+S_{33}'=-\Omega^2 U_3,
\]

\[
 iKD_1+D_3'=-QN,\qquad
 \Gamma_3'=i\Omega N-\alpha K^2\mu.
\]

## 2. Twelve-state first-order system

Choose auxiliary state variables

\[
y=(U_1,U_3,V_1,V_3,\Phi,N,T_1,T_3,R_1,R_3,D_3,\Gamma_3)^T,
\]

where V_i = U_i', R1 = m^z_13, R3 = m^z_33 and

\[
T_1=S_{13}-iKm^z_{11},\qquad T_3=S_{33}-iKR_1.
\]

These are derivatives and conjugate stresses/fluxes of the existing fields, **not additional physical fields**. Define

\[
\gamma=V_1+iKU_3,\quad s_{11}=c_{11}iKU_1+c_{13}V_3,
\quad s_{33}=c_{13}iKU_1+c_{33}V_3.
\]

The algebraic derivative equations are

\[
U_1'=V_1,\quad U_3'=V_3,
\quad V_1'=R_1/(\lambda^2c_{44})-iKV_3,
\]

\[
V_3'=(R_3-h_aN)/(\lambda^2c_{33})-iK(c_{13}/c_{33})V_1,
\quad\Phi'=(e_{31}iKU_1+e_{33}V_3-D_3)/\kappa_{33}.
\]

Set Z11 = λ²(c11 iK V1 + c13 V3′) + hb N. The hyperstress equations are

\[
R_1'=(1+\lambda^2K^2)c_{44}\gamma+e_{15}iK\Phi-iKh_cN-iKZ_{11}-T_1,
\]

\[
R_3'=(1+\lambda^2K^2)s_{33}+e_{33}\Phi'-iKR_1-T_3.
\]

Eliminating U3‴ from μ′ = −Γ3/α gives

\[
\left(1-\frac{h_a^2}{\lambda^2c_{33}}\right)N'
=-\frac{\Gamma_3}{\alpha}
-\frac{h_aR_3'}{\lambda^2c_{33}}
-iK\left(h_b+h_c-\frac{h_ac_{13}}{c_{33}}\right)V_1'
+h_cK^2V_3+Q\Phi'.
\]

The remaining equations are

\[
T_1'=-\Omega^2U_1-iK[(1+\lambda^2K^2)s_{11}+e_{31}\Phi'],
\]

\[
T_3'=-\Omega^2U_3-iK[(1+\lambda^2K^2)c_{44}\gamma+e_{15}iK\Phi-iKh_cN],
\]

\[
D_3'=-iK[e_{15}\gamma-\kappa_{11}iK\Phi]-QN,
\quad\Gamma_3'=i\Omega N-\alpha K^2\mu.
\]

All derivatives on each right-hand side have already been expressed by y. Consequently **y′ = F(K,Ω)y** is a constant 12 × 12 first-order system constructed directly from physical constants. It reuses no Galerkin basis, mechanical matrix, carrier matrix, or differentiation matrix.

### Parity and faces

The retained family has U1 even and U3, Φ, N odd. At z = 0 the independent nonzero states are **(U1,V3,T3,R1,D3,Γ3)**. At the top face the six conditions are

\[
T_1=T_3=R_1=R_3=\Gamma_3=0,
\qquad D_3-\epsilon K\Phi=0.
\]

The bottom conditions follow by parity, including the opposite normal sign in the electrical condition. Form B = Bface exp(F/2) Pmid. A zero of its equilibrated determinant, with a small relative singular value, supplies independent complex ω or k. Row/column equilibration does not change the zeros. The exterior is still the **quasistatic positive-phase sheet qES = K**. A negative Re K solution on that analytic sheet grows in the exterior and is rejected, regardless of determinant accuracy.

For A = H = 0, the order drops and the separately retained eight-state classical system is used; no singular λ → 0 substitution is made into the twelve-state operator.

## 3. Energy and strong-field verification

The strong solution is reconstructed from the boundary null vector using exp(zF), normalized to ∫(|U1|² + |U3|²) dz = 1. An **independent 80-point Gauss quadrature**, not the Galerkin quadrature, computes its energy, carrier dissipation and power. Constitutive quantities are reconstructed directly from the state and F derivatives.

The time-averaged energy contains kinetic, elastic, gradient-elastic, dielectric, carrier and reciprocal H cross energies, and the exact Laplace exterior contribution. The dissipated power is

\[
\mathcal D=\frac\alpha2\int_{-1/2}^{1/2}
 (|K\mu|^2+|\mu'|^2)\,dz\ge0.
\]

The cross-section power contains mechanical/electrical/chemical power, the tangential-hyperstress face correction and exterior power. With v = −iΩU,

\[
P_{\rm face}=-\left[\frac12\Re(m^z_{11}v_1^*+m^z_{13}v_3^*)\right]_{-1/2}^{1/2},
\quad
P_{\rm vac}=-\frac{\Omega\epsilon}{4}
 (|\Phi(-1/2)|^2+|\Phi(1/2)|^2).
\]

Omitting either term can invalidate the direction or balance test. For a real drive and k = β + iκ,

\[
2\,\Im K\,P_x=\mathcal D,\qquad
v_E=c_sP_x/\mathcal E,
\]

\[
L_A=d/|\Im K|,\quad L_E=d/(2|\Im K|),
\quad E(L)/E(0)=e^{-L/L_E},
\quad E(\lambda_{\rm phase})/E(0)=e^{-4\pi|\Im K|/\Re K}.
\]

A positive-phase backward root requires Re K > 0, Px < 0 and Im K < 0; loss then decays **in the direction of its energy flow**, not necessarily as x1 increases. Numerical checks compare strong and Galerkin powers, energies and dissipations, as well as complex roots and the full boundary/field residuals.

## 4. Conditioning is not a model change

Raw high-degree gradient-elastic stiffness can amplify eigensolver roundoff, especially in complex-k Newton steps. A0-S exactly eliminates the high mechanical polynomial DOFs:

\[
D_{\rm cond}=D_{ll}-D_{lh}D_{hh}^{-1}D_{hl},\qquad
u_h=-D_{hh}^{-1}D_{hl}u_l.
\]

Here **u_h** denotes high mechanical modal coefficients, not the carrier perturbation ν. The eight low mechanical DOFs use polynomial degrees ≤ 7; the remaining DOFs are **solved out, not truncated**. Provided Dhh is nonsingular, det D = det Dhh det Dcond. The determinant identity, governing residuals, p = 24/28/32 convergence, and independent strong-equation solutions validate this conditioning step. Original A0 and A0-R sources are hash-retained and not edited.

This check certifies numerical agreement within the stated subset only. It does **not** certify empirical f/A/H, thin-plate transport, an exact electromagnetic radiation condition, coupling novelty, edge conversion, or negative reflection.
