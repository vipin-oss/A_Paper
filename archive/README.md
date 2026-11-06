# Archived, superseded material

This directory holds material that is **not** part of the final Paper A
submission.  Nothing here should be read as a current result.

## `legacy_manuscript_2026-11-06/`

The earlier manuscript project (main.tex + sections including `abstract.tex`
and `reductions.tex`, its own `figures/`, `figure_data/` and `outputs/`).  It was
superseded by the authoritative manuscript in `../Paper_A_Final_Submission/`.

It contains the defects that the independent review reported, and it is kept
only as a record of the earlier state:

* `main.tex` loads siunitx with `\siunitxsetup`, which does not exist in
  siunitx v2 and aborts the build;
* `sections/governing_equations.tex` states the strain-gradient modulus as
  `A = ell^2 C delta` throughout but then says that `A` carries the units of
  `C` (Pa), which is wrong: `A` has the units of a force, N = J/m;
* the same file writes a four-index hyperstress `tau_ijkl` together with a
  three-index strain gradient, and contracts it once in the balance law;
* `sections/governing_equations.tex` builds the electrochemical potential as
  the sum of two dimensionless ratios and an energy-valued term.

All four are corrected in `../Paper_A_Final_Submission/`, with the evidence
recorded in `../PAPER_A_FINAL_INDEPENDENT_CORRECTION_RESPONSE.md`.
