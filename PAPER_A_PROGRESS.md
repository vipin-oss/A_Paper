# Paper A — progress and resume state

Updated: 2026-11-06 (second correction phase).  Branch `arena/ea7ca4dd-a-paper`.

## Where the work stands

One authoritative manuscript: `Paper_A_Final_Submission/main.tex` (+ `sections/`,
`figures/`, `references.bib`).  The old project is archived under
`archive/legacy_manuscript_2026-11-06/` and labelled superseded.

Content is complete and statically validated.  It has **never been compiled**:
no TeX engine exists in the sandbox (apt, PyPI and the GitHub release host all
fail; see the response document, issue J).

## Closed in this phase

* **A** two manuscripts → one authoritative tree; builder refuses a second
  `main.tex`; old project archived with a defect list.
* **B** strain-gradient modulus: `A = ell^2 c delta` with the gradient slots
  third and sixth (`A_(ijk)(lmn) = l^2 c_(ij)(lm) delta_(kn)`), units N not Pa;
  third-order hyperstress; balance `rho u'' = div sigma - div div tau`;
  effective stress; double traction; units table.  Verified by a contraction
  test against the exact SH branch (2e-13 vs 3e6).
* **C** electrochemical potential is energy-valued (J per carrier) with the
  electron sign: `mu = a dn - q phi + H : eta`; flux, current, Einstein relation
  derived; verified against the solver fields to machine zero.
* **D** flexoelectric scope: `f_3zz = 1 nC/m` is retained and synthetic; its
  measured contribution is −0.01 % (operating point and peak).  New
  `sec:results_scope`.
* **E** quasistatic: `d/λ_EM = 2.2e-4`, `(v_p/c)² = 8.8e-9`,
  `ω τ_d = 1.65e3` (carriers NOT quasistatic, full continuity retained).
* **F** eight boundary/balance conditions re-verified against code and tests.
* **G** comparison table for the two configurations; energy identity re-checked
  (3.4e-16).
* **H** `\sisetup` (no `\siunitxsetup`, no `\boldsymbol` redefinition);
  static check PASS.
* **K** `run_all_checks.py` + `validation/verification_log.txt`.

## Open

* **Compilation** — UNRESOLVED here.  Next environment with TeX:
  `cd Paper_A_Final_Submission && pdflatex main && bibtex main && pdflatex main && pdflatex main`.
* **Novelty** vs Qu et al. — UNRESOLVED, declared, no claim.
* Synthetic `ℓ`, `f`, `H`; linearised transport; single edge.

## Do not repeat

* Do not re-run `build_figure_data.py` unless the physics changes.
* Do not reintroduce a second `main.tex`; the builder will refuse.
* Do not quote the peak as a reflectance.
