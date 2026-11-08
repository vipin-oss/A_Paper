# README_VERIFICATION -- how to check Paper A independently

Everything below uses only `numpy`, `scipy` and `matplotlib`; no network, no GPU, no
random numbers (the code is deterministic: results agree to the last printed digit
for 1 and 2 BLAS threads).

## Step 1 -- one command, about 30 seconds

```bash
cd 01_PROGRAM
python3 verify_paper_a.py
```

It recomputes, from the material inputs and the solver, and compares with the numbers
printed in the paper: the dimensionless groups, the positivity bound, the
electromagnetic ratios, the operating-point and fold mode, `R_B` at the operating
point (0.0192916), at the certified fold (0.9428718) and at k_x d = 0.55 (0.551910),
the three coupling effects (-1.21 %, -10.17 %, -36.1 %), the incident-flux ratio
(131), the total outgoing power (0.99980, 1.00050), the controls of Table 4, the
classical-plate fold (k_x d = 0.824, 13.686 GHz), the appendix worked example and the
Legendre stiffness matrix.  It stores nothing and reads no result file.  Expected
last line: `46 / 46 checks passed`, exit code 0.

## Step 2 -- unit and scientific tests, about 15 seconds

```bash
cd 01_PROGRAM/paper_a_study
python3 -m pytest test_model.py -q          # 52 passed
```

## Step 3 -- the full battery, about 10 minutes

```bash
cd 01_PROGRAM
python3 paper_a_study/run_all_checks.py     # expected: OVERALL: PASS
```

This includes the independent checks that do not share code with the production path
(closed-form shear-horizontal limits, strong-form ODE propagator, `C^1`
finite-element plate, energy identity, reciprocity), the degree and quadrature
refinement, the claim registry (every number in the manuscript traced to a stored
record) and fifteen deliberate-defect mutation tests that must all be caught.

## What is, and is not, independent

* Part 1 of `verify_paper_a.py` is plain arithmetic and does not import the solver.
* The finite-element plate (`MeshPlate`) and the strong-form propagators share the
  constitutive tables with the spectral solver but not its matrices or basis.
* Scripts named `round16_*` ... `round20_*`, `run_study.py`,
  `regenerate_revised_data.py` and the reports `FIGURE_5_VALIDATION_REPORT.md`,
  `FIGURE_AUDIT_REPORT.md` document earlier, superseded states of the model (they use
  the grounded-edge baseline and quote values such as R_B = 0.0231).  They are not part
  of the checks above and their numbers must not be compared with the paper.
