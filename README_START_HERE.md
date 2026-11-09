# PAPER A -- complete package for independent checking

Paper: *Backward-branch negative reflection of guided waves from the free edge of a
flexoelectric piezoelectric semiconductor plate*.  Author: Dr Vipin Gupta.

You (the checker) are asked to decide, independently, whether the equations, the
program and the numbers in this paper are correct and consistent.  Everything needed is
in this zip.  No network, no GPU and no random numbers are used.

## 1. What is inside

| Folder | Content |
|---|---|
| `02_MANUSCRIPT/` | LaTeX source (`main.tex`, `sections/*.tex`, `references.bib`, `figures/`) and `PAPER_A.pdf` (49 pages, 12 pt) |
| `01_PROGRAM/` | the Python solver and every check (`paper_a_study/model.py` is the solver) |
| `01_PROGRAM/paper_a_study/figure_data/` | stored datasets behind every figure and table |
| `03_EXPECTED_OUTPUTS/` | the output the author's run produced, to compare with yours |
| `CHECKER_BRIEF.md` | what to check, the equation-to-code map, the claims table, and the weak points |

`01_PROGRAM/Paper_A_Final_Submission/` holds a synced copy of `main.tex` and `sections/` kept
only because some automated checks read the manuscript from that location.  The master copy is
`02_MANUSCRIPT/`; after any edit there, copy `main.tex` and `sections/` across.

**Read `HANDOFF_NOTES.md` first** if you are resuming this project after a break: it records
the decisions taken, the standing rules, what is verified, and what is still open.

## 2. Run it (three steps, nothing else is needed)

Requirements: Python 3.11 or newer, `numpy`, `scipy`, `matplotlib`
(`pip install -r 01_PROGRAM/requirements.txt`).  The author's run used Python 3.13.18,
numpy 2.5.3, scipy 1.18.1, matplotlib 3.11.2 (see `03_EXPECTED_OUTPUTS/ENVIRONMENT_USED.txt`).

```bash
cd 01_PROGRAM

# Step 1 (about 30 s): recompute the headline numbers from scratch, no stored result used
python3 verify_paper_a.py            # last line must read: 46 / 46 checks passed

# Step 2 (about 15 s): unit and scientific tests
cd paper_a_study && python3 -m pytest test_model.py -q      # 52 passed
cd ..

# Step 3 (about 10 min): the complete battery, including 15 deliberate-defect tests
python3 paper_a_study/run_all_checks.py                     # last line: OVERALL: PASS
```

Optional, about 10 min: the independent two-dimensional finite-element check (Table `tab:fe2d`):

```bash
cd 01_PROGRAM/paper_a_study && python3 fe2d_validate.py op     # rewrites figure_data/fe2d_validation.csv
```

Compare your output with `03_EXPECTED_OUTPUTS/`.  Differences in the last 2-3 printed
digits (about 1e-12 relative) are normal across machines; the tolerance of every
check is printed next to it.

## 3. What a pass does and does not mean

* A pass means: the program reproduces every number printed in the manuscript, and the
  program is internally consistent (independent closed-form limits, an independent
  strong-form integrator, an independent C1 finite-element plate, an energy identity
  closing to 1e-12, reciprocity, mutation tests).
* It does **not** by itself prove that the physical model is the right one, that the
  synthetic parameters (gradient length, flexoelectric constant, coupling constant H) are
  realistic, or that the idea is novel.  Those are judgements for a referee and are
  stated openly in the paper (Section 5.5, Limitations).
* Please also do the by-hand derivations listed in `CHECKER_BRIEF.md` section 4; they use
  no code and are the strongest independent evidence.

## 4. Please report

1. Every number that does not reproduce (with the command and your output).
2. Every equation in the paper that you derive differently, with your derivation.
3. Every place where the text claims more than the data support.
4. Awkward or unclear wording (the paper is written in American spelling).
Use the format in `CHECKER_BRIEF.md` section 7.
