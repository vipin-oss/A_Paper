# CHECKER_BRIEF

## 1. The claims (what the paper says, in five lines)

1. At k_x d = 0.7362 (16.684 GHz) a guided mode reflected at the free edge puts 1.93 % of
   the incident power into the backward mode; along the same branch the share reaches
   94.29 % at the zero-group-velocity fold (numerically resolved maximum) k_x d = 0.52719 (16.6547 GHz).
2. These are **modal shares, not reflectances**: the propagating outgoing modes carry
   0.99980 (operating point) and 1.00050 (fold) of the incident power.
3. The backward branch belongs to the plate (strain-gradient length places the fold); it
   exists with the added coupling H = 0, and in the classical plate (fold at k_x d = 0.824).
4. The added carrier--strain-gradient coupling H acts through conduction loss: it lowers
   the share by 1.21 % (operating point), 10.17 % (k_x d = 0.55), 36.1 % (fold) at
   |H| = 0.05 H*.  The flexoelectric constant changes the share by 0.012 % or less.
5. The edge problem is solved by a Legendre--Galerkin expansion (degree 22), validated
   against an independent C1 finite-element plate, exact limits and an energy balance
   closing to 1e-12.  The corner line force is bounded, not zero (Section 5.5).

## 2. Headline numbers and where they are produced

| Quantity | Value in paper | Reproduced by |
|---|---|---|
| R_B, operating point | 0.0192916 | `verify_paper_a.py`; `figure_data/peak_certification.json` |
| R_B, certified fold | 0.9428718 | same |
| R_B, k_x d = 0.55 | 0.551910 | same |
| coupling effect | -1.21 %, -10.17 %, -36.1 % | `verify_paper_a.py`; `figure_data/mechanism_controls.json` |
| total outgoing power | 0.99980, 1.00050 | `verify_paper_a.py` |
| incident modal power ratio | 131 | `verify_paper_a.py` |
| classical fold | k_x d = 0.824, 13.686 GHz | `verify_paper_a.py`; `paper_a_study/lambda_continuation.py` |
| degree/quadrature spread of R_B | 1e-6 | `convergence_audit.py`, `quadrature_audit.py` |
| every other number in the text | -- | `paper_a_study/claim_audit.py` (registry `claims.json`) |

## 3. Equation-to-code map (`01_PROGRAM/paper_a_study/model.py`)

| Paper | Code |
|---|---|
| ZnO constants, Voigt matrices C, e, kappa (Eqs. CZnO, ZnOe) | `Plate.__init__`, lines 32-84 |
| Dimensionless groups Q, alpha_d, lambda, f, h (Table groups) | `Plate.__init__` (`self.Q`, `self.alpha`, `self.lam`, `self.f`, `self.h`) |
| Schur positivity bound (Eq. schur) | `Plate.__init__` (`self.schur`) |
| Legendre basis, grounded potential space (Eqs. basis, app_pot) | `Plate.basis`, line 85 |
| Strain and strain-gradient amplitudes (Eqs. strain_amplitudes, eta_amplitudes) | `Plate.strains`, line 102 |
| Blocks A_rs and the quartic in k_x (Eqs. block, quartic, coeffs) | `Plate.operators` (158), `Plate.matrices` (184), `Plate.polynomial` (201) |
| First-order state form, root classification (Eq. classification) | `Plate.state_operator` (204), `Plate.waves` (258), `Plate.edge` (331) |
| Power flux P_x (Eq. Px_int) | `Plate.power`, line 237 |
| Edge rows: traction, double traction, D_x, J_x, corner force (Eqs. bc_edge, corner_force) | `Plate.boundary_vector`, line 245 |
| Edge matching, R_B (Eqs. edge_ansatz, RB), energy identity, dissipation | `Plate.edge`, lines 331-392 |
| Temporal route, group velocity, branch tracking | `Plate.temporal`, line 111 |
| Exact classical SH limit; strong-form propagators | `classical_strong_root` (393), `gradient_strong_root` (484) |
| Independent C1 finite-element plate | `MeshPlate`, line 504 |
| Temporal energy balance | `temporal_energy_balance`, line 543 |

## 4. Derive these by hand (no code)

1. T = qD/(mu k_B) = 301.7 K; a = k_B T/n0; L_D = sqrt(kappa33 k_B T/(q^2 n0)) = 2.680 um;
   Q = d/L_D = 0.0746; alpha_d = D/(d c_s) = 0.8283 with c_s = sqrt(c44/rho) = 2746.6 m/s.
2. c* = c33 - 2 c13^2/(c11 + c12) = 154.4 GPa; H_bound = l sqrt(a c*) = 8.97e-22 J m;
   H* = H_bound/sqrt(5); the largest |H| used is 0.05 H* = 2.0e-23 J m, i.e. 0.022 H_bound.
3. Electrostatic reduction: k_EM d = 2.2e-4, omega*tau_d = 1.65e3 (Section 2.3).
4. Mass and stiffness element matrices of the basis b_j = sqrt(2j+1) P_j(2s): Gram = identity,
   S_jj = 2 j (j+1)(2j+1); the N = 6 matrix of Appendix A.1.
5. Euler-Lagrange equations from the enthalpy (Eq. enthalpy): momentum
   rho u'' = d_i sigma_ij - d_i d_k tau_jik, Gauss d_i D_i = -q dn, carrier continuity; the
   reciprocity of H (tau gets H dn, mu~ gets H eta_zzz).
6. The power identity P_inc + sum P_j + P_cross = P_edge - P_diss, and R_B = -P_B e^{2 Im k_B L}
   / (P_inc e^{2 Im k_i L}).
7. Worked example of Section 3.2 / Appendix A.6: 0.0192957 x 0.9998954 / 1.0001081 = 0.0192916.

## 5. Choices in the model that a checker should look at critically

* The edge is electrically insulating: D_x = 0 (natural).  The grounded-edge variant
  (`edge_electric='ground'`) is a different boundary-value problem and is kept only for
  the superseded baseline.
* The backward mode is selected as the outgoing root whose real wavenumber is closest to
  the target k_Bx.  The paper argues uniqueness (second candidate 2.0|k_x| away,
  condition number 1.6e2) -- check `peak_identity_audit.json`.
* R_B is evaluated at L = 10 d with both attenuations; the edge-plane value is reported
  separately.  The modal share can exceed the "reflected" fraction because of the
  interference term (1.0005 at the fold).
* The corner line force is not zero; it decays algebraically with the Galerkin degree and
  the reported partition does not depend on it (Section 5.5).
* gradient length, flexoelectric constant and H are synthetic.  The paper says so.
* The added bilinear term Delta n H_jkl eps_jk,l is not claimed to be new; the paper
  compares it only with the free-energy decomposition reproduced by Hu et al. (2025) of
  Qu et al. (2025).  The full text of Qu et al. was not read.

## 6. Files in the program that are history, not method

`round16_*` ... `round20_*`, `run_study.py`, `regenerate_revised_data.py`,
`validate_revised_data.py`, `FIGURE_5_VALIDATION_REPORT.md`, `FIGURE_AUDIT_REPORT.md`
and `01_PROGRAM/feasibility/` document earlier or superseded states of the model.  They
quote old values such as R_B = 0.0231 and must not be compared with the paper.

## 7. Report format

For every finding give: (a) location (file and line, or Section/Eq. number), (b) what is
wrong or unclear, (c) your own value or derivation, (d) severity: *error* (a number or
equation is wrong), *risk* (supported only weakly), *style* (wording).  Please state
explicitly which checks you actually ran and which you only read.
