# Round 16 — Correction History

Baseline: `23ec30ee7817b85a791cff30624973b8ec453088` (round 15), branch
`arena/ea7ca4dd-a-paper`. Four corrections were made, all in
`Paper_A_Final_Submission/sections/`, all at the level of transcription. **No code
that computes a number was modified**; the only new `.py` file is the read-only audit
script `paper_a_study/round16_carrier_sign_audit.py`.

| ID | File | Lines | Class | Before | After |
|---|---|---|---|---|---|
| R16-1 | `numerical_methods.tex` | 85–99 (`eq:weak_carrier` and its prose) | **A** sign | $-\dfrac{\ii\alpha_{\mathrm d}}{\omega}\partial_i\widetilde\mu\,\partial_i\Phi^{*}$ | $+\dfrac{\ii\alpha_{\mathrm d}}{\omega}\partial_i\widetilde\mu\,\partial_i\Phi^{*}$ |
| R16-1b | `numerical_methods.tex` | 139–144 (sentence introducing `eq:block`) | A, explanatory | "the seventh is \eqref{eq:weak_carrier}; the eighth is …" | plus: "whose transport term enters with the opposite sign because each block is minus the residual of the weak equation rather than the equation itself" |
| R16-2 | `governing_equations.tex` | 301–308 (`eq:continuity` and prose) | **B** dimension | $q\,\partial_t(\Delta n)+\partial_iJ_i=0$ | $\partial_t(\Delta n)+\partial_iJ_i=0$, plus one clause naming the charge balance obtained by multiplying by $-q$ |
| R16-2b | `governing_equations.tex` | 534 | B, dependent | $-\ii\omega q\widehat N+\partial_i\widehat J_i=0$ | $-\ii\omega\widehat N+\partial_i\widehat J_i=0$ |
| R16-3 | `numerical_methods.tex` | 70–79 (`eq:weak_gauss` and prose) | **B** coefficient | $-\int\widehat N\psi^{*}\dd\zeta$ | $-Q\int\widehat N\psi^{*}\dd\zeta$, with $Q=d/L_D$ named in the prose |
| R16-4 | `governing_equations.tex` | 573–576 (`sec:governing_nondim`) | B, supporting | — | one sentence fixing the unit of the carrier amplitude by the unit coefficient of $-\langle\mathsf W_r,\mathsf W_s\rangle$ in `eq:block` |

(Line numbers refer to the state after the edits; the diff is reproduced verbatim in the
round-16 audit trail.)

## Detail

### R16-1 — carrier weak-form sign (class A)

Evidence, in order of independence:

1. **Derivation from the implemented balance.** Starting from the dimensionally
   consistent number balance, $\partial_t\Delta n+\partial_iJ_i=0$, multiplying the
   time-harmonic residual $-\ii\omega\widehat N-\alpha_{\mathrm d}
   \partial_i\partial_i\widetilde\mu=0$ by $\ii/\omega$ and integrating by parts with
   $J_z=0$ on the faces gives $\int[\widehat N\Phi^{*}+(\ii\alpha_{\mathrm d}/\omega)
   \partial_i\widetilde\mu\,\partial_i\Phi^{*}]=0$. Full chain:
   `PAPER_A_ROUND16_CARRIER_STRONG_TO_WEAK_DERIVATION.md`.
2. **Independent operator comparison.** The implemented carrier row equals
   $-\,[\text{repaired weak form}]$ term by term to $4.2\times10^{-14}$ (degree 4,
   three kinematic points) and $9.7\times10^{-14}$ (degree 6), with $H\neq0$ so that the
   carrier–strain-gradient column is exercised. The two candidate signs differ by
   $2\max|T|=7.82\times10^{1}$: `PAPER_A_ROUND16_CARRIER_OPERATOR_COMPARISON.md`.
3. **Dissipativity.** The repaired sign gives $\operatorname{Im}\omega<0$ and a
   non-negative dissipated power equal to `eq:dissipation`; the printed sign gives
   growth ($\operatorname{Im}\omega=+1.0354$ at $\kappa=1$).

Because the reduced problem is homogeneous, the row operation $\text{row}\to-\text{row}$
does not change any eigenvalue, dataset, figure or result. The defect was in the
manuscript only — **the solver was right and was not touched**.

The prose was rewritten rather than silently re-signed: the manuscript now shows the two
steps ($\times\ii/\omega$ and one integration by parts), states $\ii(-\ii)=1$
explicitly, and identifies the boundary term that the blocking condition removes.

### R16-2 — spurious charge in the continuity equation (class B)

$q\,\partial_t(\Delta n)$ has units $\mathrm{C\,m^{-3}s^{-1}}$; $\partial_iJ_i$ with $J_i$
the *number* flux has $\mathrm{m^{-3}s^{-1}}$. They cannot be added. The charge balance is
the same equation multiplied by $-q$, with $j_i=-qJ_i$; both statements now appear, and the
dependent amplitude statement at l. 534 was brought into line.

Independent corroboration: with the printed $q$, the nondimensionalisation of
`sec:governing_nondim` would give the transport coefficient $\alpha_{\mathrm d}/q=
5.2\times10^{18}$, not the $\alpha_{\mathrm d}=0.828$ that `eq:dissipation`, `eq:block`
and the code all use.

### R16-3 — mobile-charge coefficient in Gauss's law (class B)

The scaled Gauss law is $\widehat\partial_i\widehat D_i=-Q\widehat N$ with
$Q=d/L_D=0.0746349$, not $-\widehat N$. The discrete $\varphi$–$\mu$ block equals
$-Q\int\psi_ib_j$ to $3.7\times10^{-16}$ elementwise, and the $\varphi$–$\varphi$ block
contains the $Q^2$ screening term to $1.1\times10^{-17}$. The printed unit coefficient
was therefore off by $1/Q=13.4$. The **sign** of the charge term was correct; only the
coefficient was missing. Details:
`PAPER_A_ROUND16_MECHANICAL_AND_GAUSS_AUDIT.md` §4.

### R16-4 — the carrier amplitude unit (class B, supporting)

`eq:block` gives the compressibility the unit coefficient of
$-\langle\mathsf W_r,\mathsf W_s\rangle$, which fixes the unit of $\widehat N$. That unit
had been left implicit while the scaling table spoke of densities in units of $n_0$; one
sentence now states it, so that the $Q$ of R16-3 and the $\alpha_{\mathrm d}$ of R16-1 can
be read off the scaling section without a hidden factor.

## What was deliberately not changed

| Item | Why |
|---|---|
| `eq:momentum`, `eq:effective`, `eq:virtual_work`, `eq:contraction` | audited this round; correct as printed, including the *contracted* (not component) form of the identity |
| `eq:gauss`, `eq:D`, `eq:mu`, `eq:current`, `eq:dissipation` | dimensionally exact and consistent with the code |
| `eq:block`, `eq:quartic`, `eq:polynomial` | sign structure verified against the assembled blocks; the transport term is minus the weak form by construction, now stated |
| `eq:weak_mech` | signs of the inertial and hyperstress terms correct |
| $\alpha_{\mathrm d}$, $Q$, $h$, $\lambda$, $f$ | no constant changed; all five reproduce from the material file |
| corner line force (M15-8) | unresolved; left as an open item rather than papered over |
| figures 1–10, datasets, `paper_a_study/*.py` solver code | outside the scope of a sign audit; no numerical result may move in this round |

## Preservation of earlier evidence

Rounds 14 and 15 are untouched: their six reports each, the restructured sections
(introduction, results, discussion, conclusions, appendix), the repaired Fig. 5 and
Fig. 8, and `PAPER_A_CORRECTION_HISTORY.md` remain byte-identical except for the six
edits listed above.
