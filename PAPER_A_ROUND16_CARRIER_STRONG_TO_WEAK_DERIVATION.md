# Round 16 — Carrier Equation: Strong to Weak, Step by Step

**Question.** Is the carrier weak equation printed as `eq:weak_carrier` equivalent to
the carrier operator that `paper_a_study/model.py` assembles? The proposed repair
(flip the sign of the transport term) was **not** assumed. The chain below is derived
from the implemented balance, with every charge factor and every complex factor
exposed.

All symbols follow the dimension ledger of
`PAPER_A_ROUND16_CONVENTIONS_AND_DIMENSIONS.md` §2. Steps 1–3 are dimensional;
step 4 performs the nondimensionalisation; steps 5–7 work entirely in scaled
variables. No step mixes the two families.

---

## Step 1 — The implemented balance, and a dimensional repair

The manuscript states the carrier balance as

$$\partial_t(\Delta n)+\partial_iJ_i=0,\qquad
J_i=-\frac{D\,n_0}{k_BT}\,\partial_i\widetilde\mu, \tag{1}$$

with $J_i$ the electron **number** flux ($\mathrm{m^{-2}s^{-1}}$) and $\Delta n$ the
number density ($\mathrm{m^{-3}}$).

Dimension check of the two terms of (1):

* $\partial_t\Delta n$: $\mathrm{m^{-3}s^{-1}}$;
* $\partial_iJ_i$: $\mathrm{m^{-1}}\cdot\mathrm{m^{-2}s^{-1}}=\mathrm{m^{-3}s^{-1}}$.

They agree. The same check on the form printed before this round,
$q\,\partial_t(\Delta n)+\partial_iJ_i=0$, fails: $q\partial_t\Delta n$ is
$\mathrm{C\,m^{-3}s^{-1}}$. A charge $q$ multiplies a **number** density only if the
flux beside it is a charge flux. The charge form is

$$\partial_t(-q\Delta n)+\partial_ij_i=0,\qquad j_i=-qJ_i, \tag{2}$$

which is (1) multiplied by $-q$; both forms are used in the manuscript and (2) is what
`eq:current` presents. The printed $q$ was therefore a transcription error, not a
convention: it was removed (item R16-2), and the whole downstream chain — including
`eq:dissipation` and the assembled blocks — is the $q$-free form.

## Step 2 — Constitutive linearisation

With the enthalpy of `eq:enthalpy`, the electrochemical potential of the electron gas
is $\widetilde\mu=\partial w/\partial\Delta n$ (unit J), and to the linear order used
in the paper

$$\widetilde\mu=\frac{k_BT}{n_0}\,\Delta n+q\varphi+H_{jkl}\,\eta_{jkl}, \tag{3}$$

so that

$$\partial_i\widetilde\mu=\frac{k_BT}{n_0}\,\partial_i\Delta n+q\,\partial_i\varphi
+H_{jkl}\,\partial_i\eta_{jkl}. \tag{4}$$

The three terms of (4) are the diffusion, drift and carrier–strain-gradient driving
forces; substituted into (1) they reproduce the current of `eq:current`,
$j_i=-qJ_i=qD\partial_i\Delta n-q\mu_en_0\partial_i\varphi+\dots$, with the Einstein
relation $Dn_0/(k_BT)=\mu_en_0/q$ used in the second term.

## Step 3 — Time-harmonic substitution, at fixed $k$

Insert the ansatz $\widehat f(z)e^{\ii(k_xx+k_yy-\omega t)}$ (convention 1):
$\partial_t\to-\ii\omega$, $\partial_x\to\ii k_x$, $\partial_y\to\ii k_y$,
$\partial_z=\dd/\dd z$. From (1),

$$-\ii\omega\,\Delta\widehat n+\ii k_x\widehat J_x+\ii k_y\widehat J_y+
\widehat J_z'=0 . \tag{5}$$

No charge appears in (5), consistently with step 1. Written as a residual of the
carrier amplitude it is

$$-\ii\omega\,\widehat N-\alpha_{\mathrm d}\Bigl(\widetilde\mu''-
(k_x^2+k_y^2)\widetilde\mu\Bigr)=0 \tag{6}$$

in scaled variables, i.e. $\partial_i\partial_i\to\partial_z^2-(k_x^2+k_y^2)$, which is
the code's residual at `model.py:302`:
`carrier = -1j*omega*f['N'][0] - self.alpha*(f['mu'][2] - (kx*kx+ky*ky)*f['mu'][0])`.

## Step 4 — Non-dimensionalisation, with the exact `model.py` scales

Scales (conventions 1, 7, 10; `model.py:36–41`): $z=d\zeta$, $t=(d/c_s)\tau$,
$\omega$ by $c_s/d$, $\Delta n$ by $n_0$ (so that $\widehat N=\Delta n/n_0$; the
*global* factor of the amplitude is fixed separately by the unit coefficient of the
compressibility in `eq:block`, and it cancels from a homogeneous equation), and
$\widetilde\mu$ by $k_BT$, which makes $\widetilde\mu/k_BT=\Delta n/n_0$ for the
linearised compressibility $a=k_BT/n_0$. Then
$\partial_z=(1/d)\partial_\zeta$, $\partial_t=(c_s/d)\partial_\tau\to-\ii\omega c_s/d$,
and (1) becomes, term by term,

$$\underbrace{\frac{c_s}{d}(-\ii\omega)\widehat N}_{\partial_t\Delta n}
+\underbrace{\frac{1}{d}\cdot\frac{1}{d}\Bigl[-\frac{Dn_0}{k_BT}\cdot k_BT\Bigr]
\partial_\zeta\partial_\zeta\widetilde\mu}_{\partial_iJ_i}=0 . \tag{7}$$

Dividing (7) by $c_s/d$ gives

$$-\ii\omega\,\widehat N-\frac{D}{d\,c_s}\,\partial_\zeta\partial_\zeta\widetilde\mu
=-\ii\omega\,\widehat N-\alpha_{\mathrm d}\,\partial_\zeta\partial_\zeta
\widetilde\mu=0,\qquad \alpha_{\mathrm d}=\frac{D}{d\,c_s}, \tag{8}$$

to which the tangential part adds $+\alpha_{\mathrm d}(k_x^2+k_y^2)\widetilde\mu$. The
ratio of the transport coefficient to the mass coefficient is $\alpha_{\mathrm d}$
itself, **not** $\alpha_{\mathrm d}/q$: the charge cancels because it never appears in
(1), and no choice of amplitude unit can alter a ratio inside one homogeneous equation. This is the numerical value
$0.828294163284$ that `model.py:39` produces to twelve digits, and it is
$\alpha_{\mathrm d}$ that `eq:dissipation` uses in
$P_{\text{diss}}=\tfrac12\alpha_{\mathrm d}\iint[(k_x^2+k_y^2)|\widetilde\mu|^2+
|\partial_z\widetilde\mu|^2]$. (The same calculation starting from the pre-round-16
form with $q$ in front of $\partial_t\Delta n$ would give $\alpha_{\mathrm d}/q$,
i.e. $5.2\times10^{18}$ — a decisive independent confirmation that the $q$ was
spurious.)

## Step 5 — Weak form

Multiply (8) by a test function $\Phi^{*}$ (convention 11, 12: the test is drawn from
the same space as the trial and is conjugated once) and integrate over the thickness:

$$-\ii\omega\int\widehat N\,\Phi^{*}\,\dd\zeta
-\alpha_{\mathrm d}\int\widetilde\mu''\,\Phi^{*}\,\dd\zeta=0 . \tag{9}$$

Integrate the second term by parts once:

$$-\ii\omega\int\widehat N\Phi^{*}
-\alpha_{\mathrm d}\Bigl[\widetilde\mu'\Phi^{*}\Bigr]_{-1}^{+1}
+\alpha_{\mathrm d}\int\widetilde\mu'\,\Phi^{*\prime}\,\dd\zeta=0 . \tag{10}$$

The boundary term is the natural one of the equation: with
$\widetilde\mu'=\partial_z\widetilde\mu\propto J_z$ it vanishes under the blocking
condition $J_z=0$ on both faces (`eq:bc_faces_carrier`), which is therefore the
natural boundary condition of the weak carrier equation and not an additional
constraint (convention 13). Including the tangential components, (10) becomes

$$-\ii\omega\int\widehat N\,\Phi^{*}\,\dd\zeta
+\alpha_{\mathrm d}\int\partial_i\widetilde\mu\,\partial_i\Phi^{*}\,\dd\zeta=0 ,
\qquad \partial_i\widetilde\mu\,\partial_i\Phi^{*}
=\widetilde\mu'\Phi^{*\prime}+(k_x^2+k_y^2)\widetilde\mu\,\Phi^{*}. \tag{11}$$

## Step 6 — Divide by $-\ii\omega$ and simplify $1/\ii=-\ii$

Divide (11) by $-\ii\omega$. Since $1/(-\ii\omega)=\ii/\omega$ and
$\ii\cdot(-\ii)=1$,

$$\boxed{\;\int_{-1}^{1}\Bigl[\widehat N\,\Phi^{*}
+\frac{\ii\alpha_{\mathrm d}}{\omega}\,\partial_i\widetilde\mu\,
\partial_i\Phi^{*}\Bigr]\dd\zeta=0\;} \tag{12}$$

**The sign of the transport term is plus.** The form printed before this round
carried $-\ii\alpha_{\mathrm d}/\omega$; that is the defect R16-1, and (12) is the
repair now in the manuscript.

## Step 7 — Conditional statement: what would change the sign

The candidate result is reported conditionally. The sign of the second term of (12)
would be negative if and only if one of the following held:

| Change | Effect on the sign | Used here? |
|---|---|---|
| time convention $e^{+\ii\omega t}$ | flips it | **no** — `eq:ansatz` fixes $e^{-\ii\omega t}$ |
| $\alpha_{\mathrm d}<0$ (i.e. $D<0$) | flips it | **no** — $D=\SI{4.55e-4}{m^2/s}>0$ |
| multiplying the whole equation by $-1$ | flips **both** terms, so the relative sign, which is what (12) displays, is unchanged | irrelevant |
| rescaling the carrier amplitude $\widehat N\to c\widehat N$, $c>0$ | multiplies both terms by $c$; no relative change | irrelevant |
| conjugating the equation instead of the test function | would make the transport term $-\ii\alpha_{\mathrm d}/\omega$ while leaving the mass term real | **not** the convention of convention 12 |

The last row is the only one that a reader could mistake for a legitimate alternative,
so it is excluded explicitly: the transport block is
$-\frac{\ii\alpha_{\mathrm d}}{\omega}\langle\mathsf M\mathsf G_r,\mathsf
M\mathsf G_s\rangle$ with the *test factor* conjugated (`model.py:185`), i.e. it is
$-\frac{\ii\alpha_{\mathrm d}}{\omega}\int(\partial_i\widetilde\mu)^{*}
(\partial_i\Phi)$, which for real basis functions and the $-\ii\omega$ convention is
the same as (12). No convention in use in the paper makes the printed minus correct.

## Step 8 — Three independent consistency checks

1. **Dissipation.** Multiplying (8) by $\widehat N^{*}$, integrating and using the
   blocking condition gives $-\ii\omega\|\widehat N\|^2=-\alpha_{\mathrm d}
   \int|\partial\widetilde\mu|^2$, i.e. $\omega=-\ii\alpha_{\mathrm d}
   \int|\partial\widetilde\mu|^2/\|\widehat N\|^2$: $\operatorname{Im}\omega<0$, and
   with $e^{-\ii\omega t}$ the mode decays at the rate
   $\tfrac12\alpha_{\mathrm d}\int[(k_x^2+k_y^2)|\widetilde\mu|^2+
   |\partial_z\widetilde\mu|^2]$, exactly `eq:dissipation`. With the printed minus the
   same calculation gives $\operatorname{Im}\omega>0$, i.e. **growth** and a negative
   dissipated power — a contradiction inside the manuscript, independent of the code.
   Numerically (audit log §2): $\kappa=1$ gives $\operatorname{Im}\omega=-1.0354$ with
   the repaired sign and $+1.0354$ with the printed one; $\kappa=3$ gives $-7.6617$ and
   $+7.6617$.
2. **The code's own dissipation functional** (`model.py:297`) is
   `0.5*alpha*sum(w*((kx^2+ky^2)|mu|^2+|mu'|^2))`, non-negative by construction, and it
   is the functional that the transport block $-\ii\alpha_{\mathrm d}/\omega F$ with
   $F\succ0$ generates.
3. **`eq:block`.** The seventh term of `eq:block` is
   $-\frac{\ii\alpha_{\mathrm d}}{\omega}\langle\mathsf M\mathsf G_r,\mathsf
   M\mathsf G_s\rangle$, i.e. the *negative* of (12) term by term, because each block
   is minus the residual of the weak equation. Under the repaired sign the two printed
   statements now agree; under the old sign `eq:block` and `eq:weak_carrier`
   contradicted each other by twice the transport form
   ($2\max|T|=7.82\times10^{1}$ in operator norm at the operating point).

## Step 9 — Result

The implemented operator is

$$\mathcal L=-\ii\omega\,\mathsf W-\alpha_{\mathrm d}\,\mathsf M\mathsf G^{\mathsf T}
\mathsf M\mathsf G ,$$

whose weak form is (12). Equivalently, the assembled carrier row equals $-1$ times
the left-hand side of (12). Since the reduced problem is homogeneous
($\mathsf A(k,\omega)\vect q=0$), multiplying one row by $-1$ is a row operation and
leaves the null space — and therefore every eigenvalue, mode shape and figure — exact.
The sign defect was **typographical in the manuscript only**; no result moves. This is
confirmed operator by operator in
`PAPER_A_ROUND16_CARRIER_OPERATOR_COMPARISON.md`.
