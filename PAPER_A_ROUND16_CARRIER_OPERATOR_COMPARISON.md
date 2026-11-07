# Round 16 — Carrier Operator: Independent Comparison

**Claim under test.** The carrier block of `paper_a_study/model.py` equals the weak
form `eq:weak_carrier` (round-16 repaired sign) up to an overall factor of $-1$,
including the mass term, the transport term, the carrier–potential coupling, the
carrier–strain-gradient coupling, the frequency factors and the complex signs.

**Method.** A second, independent implementation was written for the carrier row
alone (`paper_a_study/round16_carrier_sign_audit.py`, function `carrier_row`). It uses
`numpy.polynomial.legendre.Legendre.basis(j).deriv(r)` and a 200-node Gauss–Legendre
rule, and never calls `Plate.matrices`, `Plate.form`, `Plate.strains`,
`Plate.operators` or `Plate.fields`. The model side is read out of the assembled
blocks by summing them with the polynomial weights,
$\sum_{r,s}(-\ii k_x)^{r}(\ii k_x)^{s}\mathsf A_{rs}$, exactly as `eq:polynomial`
states. Log: `PAPER_A_ROUND16_AUDIT_LOG.txt`.

---

## 1. The reference row

With $\zetta$ the scaled thickness coordinate on $[-1/2,1/2]$ and
$b_j=\sqrt{2j+1}\,P_j(2\zeta)$, $j=0,\dots,n-1$, the mass matrix is
$\mathsf M_{ij}=\int b_ib_j$, verified as $\max|\mathsf M-\mathsf I|=4.65\times10^{-14}$.
The grounded potential space is rebuilt as
$\psi_j=b_j-\sqrt{(2j+1)/(2j+5)}\,b_{j+2}$, $j=0,1,2$, which is how
`model.py:80–82` builds it. The row is then

$$\text{row}_{i}=\underbrace{-\mathsf M_{ij}}_{\text{compressibility}}
\;\underbrace{-\frac{\ii\alpha_{\mathrm d}}{\omega}\Bigl[k_x^2\mathsf M_{ij}
+k_y^2\mathsf M_{ij}+\mathsf S_{ij}\Bigr]}_{\text{transport},\ \mathsf S_{ij}=\int b_i'b_j'}
\;\underbrace{-Q\int b_i\psi_j}_{\text{potential}}
\;\underbrace{+\,h\int b_i b_j''}_{\text{strain gradient}}$$

with $h=5.669\times10^{-4}$ for the $H$ used below.

## 2. Layout of the row (this was the round-16 trap)

The unknown vector is $\vect q=(\widehat u_1,\widehat u_2,\widehat u_3,
\widehat{\boldsymbol\varphi},\widetilde{\boldsymbol\mu})$ of dimension
$3n+n_\varphi+n$; at `degree=4`, $n=5$, $n_\varphi=3$, $n_w=23$, so the columns are
$u_1{:}0\!-\!4$, $u_2{:}5\!-\!9$, $u_3{:}10\!-\!14$, $\varphi{:}15\!-\!17$,
$\mu{:}18\!-\!22$, and the carrier test rows are $18\!-\!22$. A first attempt at this
comparison (recorded as a dead end in the round-16 working notes) summed the blocks
against the wrong column map and captured only the $\varphi$-coupling column: its
`max|row|` was $7.463\times10^{-2}$, i.e. exactly $Q$, and its relative deviation of
$5\times10^{2}$–$10^{3}$ was an artefact of the mis-mapping, not a property of the
model. The comparison below uses the layout above and is the one quoted everywhere.

## 3. Results

| degree | $k_x$ | $k_y$ | $\omega$ | $\max|\text{row}|$ | $\max|\text{diff}|$ | relative |
|---|---|---|---|---|---|---|
| 4 | $+0.7362$ | $0.1298$ | $7.6334$ | $3.914\times10^{1}$ | $1.63\times10^{-12}$ | $4.16\times10^{-14}$ |
| 4 | $+0.5275$ | $0.0000$ | $6.9000$ | $4.326\times10^{1}$ | $1.81\times10^{-12}$ | $4.17\times10^{-14}$ |
| 4 | $-0.3000$ | $0.2000$ | $4.0000$ | $7.458\times10^{1}$ | $3.10\times10^{-12}$ | $4.15\times10^{-14}$ |
| 6 | $+0.7362$ | $0.1298$ | $7.6334$ | $1.186\times10^{2}$ | $1.15\times10^{-11}$ | $9.67\times10^{-14}$ |
| 6 | $+0.5275$ | $0.0000$ | $6.9000$ | $1.311\times10^{2}$ | $1.26\times10^{-11}$ | $9.65\times10^{-14}$ |
| 6 | $-0.3000$ | $0.2000$ | $4.0000$ | $2.262\times10^{2}$ | $2.19\times10^{-11}$ | $9.68\times10^{-14}$ |

Worst relative deviation: $4.17\times10^{-14}$ at degree 4, $9.68\times10^{-14}$ at
degree 6. Negative and positive $k_x$, real frequencies, $k_y=0$ and $k_y\neq0$ are all
included; the agreement is at the level of the quadrature, on every column of the row
(displacements, potential and carrier), not only on the diagonal.

Both degrees carry $H=\SI{1.073e-24}{}$ — just below the strict Schur bound
$\SI{1.073e-21}{}$ computed by `model.py:54` — so $h=5.669\times10^{-4}\neq0$ and the
carrier–strain-gradient column is exercised. At the default $H=0$ that column is
identically zero and the test would be vacuous (this is why the default configuration
is not used here).

## 4. Row scaling: why the comparison is against $-1\times$ the weak form

The reference row above is minus the left-hand side of the repaired
`eq:weak_carrier`: the code assembles $\mathsf A\vect q=0$ with each block being minus
the residual of its weak equation (that is what makes the elastic and inertial blocks
come out with the signs of $\int\sigma:\varepsilon^{*}-\omega^2\int\rho\widehat u v^{*}$,
which is the printed `eq:weak_mech`). For the carrier row this means the implemented
operator is

$$\mathcal L_{\text{impl}}=-\Bigl[\mathsf M+\frac{\ii\alpha_{\mathrm d}}{\omega}
\mathsf F\Bigr],\qquad \mathsf F=k_x^2\mathsf M+k_y^2\mathsf M+\mathsf S,$$

while the repaired weak form is $\mathsf M+\frac{\ii\alpha_{\mathrm d}}{\omega}\mathsf
F$ set to zero. The two differ by the *row operation* $\text{row}\to-\text{row}$.
Because the reduced problem is homogeneous, that operation does not change the null
space, the dispersion polynomial `eq:quartic`, any eigenvalue, mode or figure. It is
recorded here so that no reader mistakes the minus sign in `eq:block` for a
discrepancy, and the manuscript now says so explicitly in the sentence that introduces
the seventh block.

**The two candidate signs, on the same footing.** The transport contribution alone is
$\mp\frac{\ii\alpha_{\mathrm d}}{\omega}\mathsf F$ with
$\mathsf F\succ0$ ($\min\operatorname{eig}\mathsf F=5.588\times10^{-1}$ at the operating
point) and purely imaginary coefficients ($\max|\Re|=0$). The two candidates are
therefore separated by $2\max|T|=7.825\times10^{1}$ in operator norm — thirty orders of
magnitude above the $10^{-13}$ agreement error, so the comparison does discriminate the
two signs decisively, and it selects the *plus* sign of (12).

## 5. Dissipativity check

With $e^{-\ii\omega t}$ and $\mathsf F\succ0$, the transport operator
$-\ii(\alpha_{\mathrm d}/\omega)\mathsf F$ produces decay: for the pure carrier mode the
strong form $-\ii\omega\widehat N-\alpha_{\mathrm d}\partial_i\partial_i\widetilde\mu=0$
gives $\operatorname{Im}\omega=-\alpha_{\mathrm d}|\kappa|^2/\|\widehat N\|^2<0$, whose
dissipated power coincides with `eq:dissipation`. The printed-minus operator produces
$\operatorname{Im}\omega>0$ instead (numerical values in
`PAPER_A_ROUND16_CARRIER_STRONG_TO_WEAK_DERIVATION.md` §8).

## 6. Boundary conditions

* Carrier: no boundary row exists in the assembled matrix for the $\mu$ block, i.e.
  $\partial_z\widetilde\mu\propto J_z=0$ is imposed *naturally*, by omission — which is
  what (10)–(12) require. Discretely: both the reference row and the model row have
  no contribution from the faces, and the boundary term of (10) is not represented in
  either. Agreement on this point is structural rather than numerical.
* Gauss: grounded $\widehat\varphi=0$ is essential and is built into the potential
  space by eliminating the two highest modes (`model.py:80–82`); the open-circuit
  condition $D_z=0$ is natural. The reference row reproduces the grounded space to
  $4.47\times10^{-1}$ in the *raw* orthonormality measure
  $\max|\int b_i\psi_j-\delta_{ij}|$ — that number is not a defect: it is the single
  entry $(i=2,j=0)$, equal to $-\sqrt{1/5}$, where the elimination folds $b_2$ into
  $\psi_0$; both the model and the reference contain it identically, and the
  $4\times10^{-14}$ row agreement above is the operative check.

## 7. What this comparison does not establish

* It does not test the mechanical or electric blocks; those are audited separately in
  `PAPER_A_ROUND16_MECHANICAL_AND_GAUSS_AUDIT.md`.
* It is one row of a $23\times23$ block set. It is the row that the round-16 question
  concerns, but a full elementwise comparison of the other 22 rows is *not* claimed.
* The model's quadrature uses $\max(64,2n+10)=64$ nodes at `degree=4`; the reference
  uses 200. Both are exact for the polynomials involved (degree $\le 2n+4$), and the
  agreement confirms it, but the reference is not a different *discretisation*, only a
  different assembly path.
* Eigenvalue agreement alone is not offered as evidence anywhere in this round. The
  evidence is the operator identity above, obtained with the model's own basis but an
  independent quadrature and an independent index map.
