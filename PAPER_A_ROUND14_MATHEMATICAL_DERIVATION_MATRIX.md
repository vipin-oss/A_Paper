# Round 14 — mathematical derivation dependency matrix

Scope: every derivation the article depends on, the starting relation, the
operation performed, the intermediate result now present in the source, the final
relation, where it sits, and whether a step is still missing.
Categories: **AC** already complete · **IA** needs intermediate algebra (now
supplied) · **VD** needs variable definition (now supplied) · **BS** needs
boundary substitution · **DC** needs derivation of a coefficient · **NE** needs
numerical example · **PE** needs physical explanation · **UV** unverified.

File names below are section sources under `Paper_A_Final_Submission/sections/`.

| # | Starting relation | Operation | Intermediate now in the manuscript | Final relation | Location | Cat. | Missing step? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | geometry: plate $x<0$, faces $z=\pm d/2$, $6mm$ ZnO, fields $(u_i,\varphi,\Delta n)$ | fix conventions | electric field $E_i=-\partial_i\varphi$, charge $-q$, $\widetilde\mu$ in joules | sign and unit conventions used everywhere | §2.1 | AC/VD | no |
| 2 | $\varepsilon_{ij}=\tfrac12(u_{i,j}+u_{j,i})$ | differentiate | $\eta_{ijk}=\varepsilon_{ij,k}=\tfrac12(u_{i,jk}+u_{j,ik})$, symmetric in $(i,j)$ | strain-gradient definition and its dimension | §2.2 | AC | no |
| 3 | gradient energy $w_g=\tfrac12A_{ijklmn}\eta_{ijk}\eta_{lmn}$ | choose contraction, check major symmetry | $A_{ijklmn}=\ell^2c_{ijlm}\delta_{kn}$, third/sixth slots as gradient directions; alternative contraction shown to break $A=A^{\mathsf T}$ | $w_g=\tfrac12\ell^2c_{ijlm}\eta_{ijk}\eta_{lmk}$ | §2.2 | IA/PE | no (spectral test in §3.6 + units table) |
| 4 | added term $\Delta\mathcal{H}=\Delta n\,H_{jkl}\varepsilon_{jk,l}$ | differentiate the potential twice | $\partial\Delta\mathcal{H}/\partial\varepsilon_{jk,l}=H_{jkl}\Delta n$; $\partial\Delta\mathcal{H}/\partial\Delta n=H_{jkl}\varepsilon_{jk,l}$; Maxwell identity between them | eqs. `eq:added_hyperstress`, `eq:added_mu` | §2.3 | IA | no — **moved here from the introduction in round 14** |
| 5 | enthalpy $w(\varepsilon,\eta,E,\Delta n)$ | $\sigma=\partial w/\partial\varepsilon$, $\tau=\partial w/\partial\eta$, $D=-\partial w/\partial E$, $\widetilde\mu=\partial w/\partial\Delta n$ | the four differentiations written term by term from the seven-term $w$ | eqs. `eq:sigma`–`eq:mu` | §2.3 | AC | no |
| 6 | reciprocity claim for $H$ and $f$ pairs | Maxwell identity | same tensor appears in both conjugate relations; identity named | operator symmetry | §2.3 | PE | no (symmetry verified numerically at $\pm k_y$ to $10^{-13}$) |
| 7 | virtual work of the internal fields | variation identities, two integrations by parts | $\delta\varepsilon_{ij}$ and $\delta\eta_{ijk}=\delta u_{i,jk}$; $\int\sigma\delta\varepsilon=-\int\sigma_{ij,j}\delta u_i+\oint n_j\sigma_{ij}\delta u_i$; $\int\tau\delta\eta=\int\partial_k\partial_j\tau_{ijk}\delta u_i-\oint n_j\partial_k\tau_{ijk}\delta u_i+\oint n_k\tau_{ijk}\delta u_{i,j}$ | $\rho\ddot u_j=\partial_i\sigma_{ij}-\partial_i\partial_k\tau_{jik}$ with the sign of the double divergence justified | §2.4 | **IA, new in round 14** | no |
| 8 | same variation, $\delta\varphi$ | integrate by parts | — | $\partial_iD_i=-q\Delta n$ | §2.4 | AC/BS | no |
| 9 | same variation, $\delta(\Delta n)$ | substitute Einstein relation $D=\mu_ek_BT/q$ | $Dn_0/k_BT=\mu_en_0/q$ | $q\partial_t\Delta n+\partial_iJ_i=0$, $J_i=-(Dn_0/k_BT)\partial_i\widetilde\mu$ | §2.4 | IA | no |
| 10 | $\widetilde\mu$ from #4 and #5 | substitute into $J_i$ | three-term current: diffusion, drift, carrier–strain-gradient | $j_i=qD\partial_i\Delta n-q\mu_en_0\partial_i\varphi+(qDn_0/k_BT)H_{jkl}\partial_i\eta_{jkl}$ | §2.4 | IA | no |
| 11 | field equations + boundary physics | evaluate surface terms of #7 | traction $n_i\Sigma_{ij}$, double traction $n_k\tau_{ijk}$, blocking $J_z=0$, grounded/open $D_z$ or $\varphi=0$ | eqs. `eq:bc_faces_mech`–`eq:bc_grounded`, `eq:bc_edge` | §2.6 | BS | no (corner line force explicitly unresolved) |
| 12 | plane-wave invariance along $y$ and in time | write $f=\widehat f(z)e^{i(k_xx+k_yy-\omega t)}$; substitute $\partial_t\to-i\omega$, $\partial_x\to ik_x$, $\partial_y\to ik_y$, $\partial_z\to\mathrm{d}/\mathrm{d}z$ | six strain amplitudes and the strain-gradient amplitudes written explicitly; $\widehat\eta_{xxx}=-k_x^2\widehat u_1$, $\widehat\eta_{zzz}=\widehat u_3''$ | amplitude system in $(u_1,u_2,u_3,\varphi,N)$ | §2.8 | **IA/VD, new in round 14** | no |
| 13 | amplitude system | power counting on the two balance laws | stress term at most $k^2$, hyperstress term at most $k^4$; no field in $w$ carries more than one gradient | quartic operator $\mathsf A_{00}+ik_x(\mathsf A_{01}-\mathsf A_{10})+k_x^2(\mathsf A_{11}-\mathsf A_{02}-\mathsf A_{20})+ik_x^3(\mathsf A_{12}-\mathsf A_{21})+k_x^4\mathsf A_{22}$ | §2.8 eq. `eq:quartic` | **DC/IA, new** | coefficient *entries* not claimed in closed form — see flag F-1 |
| 14 | quartic | Galerkin projection on Legendre modes | test functions, $\int_{-1}^1$ weak form, surface terms identified with the face conditions, five named enthalpy contributions | $\big[\sum_{r,s}(-ik_x)^r(ik_x)^s\mathsf A_{rs}\big]\mathbf q=0$ | §3.1 eqs. `eq:weak_form`, `eq:polynomial` | IA | no |
| 15 | assembled polynomial | companion linearisation | state vector of $2M$ components | eigenvalues $k_x^{(j)}$ and states | §3.2–3.3 | AC | no |
| 16 | root set | classification by $\Imag k_x$ and axial power | outgoing criterion with tolerance $\tau=2\times10^{-8}\max(1,|k_x|)$ | outgoing/incoming split | §3.3 eq. `eq:classification` | AC/PE | no |
| 17 | outgoing states | edge conditions $x=0$ | ansatz $\mathbf y(0)=\mathbf y_{\text{inc}}+\sum_ja_j\mathbf y^{(j)}$; system $\mathsf B\mathbf a=-\mathbf b_{\text{inc}}$, SVD with rank at $10^{-12}$ cut-off | $\mathbf a$ | §3.3 eq. `eq:edge_ansatz` | AC | no — the written system is the one the solver solves (`Plate.edge`) |
| 18 | modal self-power at a plane | reference-plane transform | $R_B=-P_B e^{2\Imag k_{Bx}L}/P_{\text{inc}}e^{2\Imag k_{ix}L}$; two exponentials retained | $R_B$ at $L=2\,\mu$m | §3.3 eq. `eq:RB` | IA | no — denominator is $P_{\text{inc}}$ at the *same* plane |
| 19 | power flux | energy identity | four-term flux, signed self-powers, interference term | $P_{\text{inc}}+\sum_jP_j+P_{\text{cross}}=P_{\text{edge}}-P_{\text{diss}}$ | §2.7 eqs. `eq:Px_int`, `eq:energy_identity` | AC | no (residual $4\times10^{-12}$) |
| 20 | non-dimensionalisation | scale by $c_s,d,\kappa$ etc. | $\lambda=\ell/d$, $Q=qd/\sqrt{\kappa_{33}a}$, $\alpha=D/(dc_s)$, $h=H/(d\sqrt{a c_{44}})$ | dimensionless groups | §2.9 | AC/VD | no |
| 21 | limits | set parameters to zero | SH closed forms, classical plate, flexo off, $H=0$ controls | limit statements | §2.10 | AC/NE | no |
| 22 | admissibility | strict Schur bound on the enthalpy | $H^2c^{-1}_{33}/(\ell^2a)<1$ enforced at construction | positive-definite enthalpy | §2.11 | AC | no |
| 23 | reported share | three admissibility conditions | conservation bound, degree convergence, energy-angle resolution | a share is reported only when all three hold | §3.4 | AC | no |

## Flags carried forward (not repaired, by design)

- **F-1.** The *entries* of $\mathsf A_{rs}$ are not given as closed-form
  algebraic expressions in $c_{ijkl}$, $e_{kij}$, $f$, $H$ and the basis
  integrals. What is derived and stated is their **structure** (which terms
  contribute, and that the total degree in $k_x$ is four), and that structure is
  what the implementation assembles. A closed-form entry list would have to be
  transcribed from the code; presenting a hand-derived formula that the code does
  not implement would be an invented derivation. Flagged rather than fabricated.
- **F-2.** The corner line force at the edge–face intersection is not resolved;
  the weak form is imposed at the corner and the line-force density is non-zero
  there ($>10^{-4}$). Unchanged from rounds 12–13.
- **F-3.** Three of the five author papers named in the brief were not obtained;
  no stylistic claim rests on them.
- **F-4.** No TeX engine, therefore no rendered page. All structural verification
  is static.
