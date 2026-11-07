# Round 16 — Supervisor Decision

**Branch** `arena/ea7ca4dd-a-paper`, baseline `23ec30ee7817b85a791cff30624973b8ec453088`.
`main` untouched. Rounds 14–15 restructuring, prose and figures preserved.

**Question put to this round.** Is the carrier weak equation printed in the manuscript
equivalent to the carrier transport operator that the code assembles? The proposed
answer (flip the sign) was treated as a hypothesis, not as an instruction.

---

## 1. Outcome category

| Category | Verdict |
|---|---|
| **A — manuscript sign error only** | **YES for the audited question.** The printed transport term of `eq:weak_carrier` carried the wrong sign; the solver was correct and was not modified. |
| **B — nomenclature / convention error** | **YES, twice, found in passing and repaired:** a spurious charge $q$ in `eq:continuity` (dimensionally impossible against a number flux) and a missing dimensionless charge $Q=d/L_D$ in `eq:weak_gauss`. Both are transcription-level; neither changes a number. |
| **C — implementation error** | **NO.** No implemented coefficient or sign was found wrong anywhere in the audited sector. Nothing in `model.py` was changed. |
| **D — insufficient evidence** | **NO.** The carrier operator is agreed to $4.2\times10^{-14}$ (degree 4) and $9.7\times10^{-14}$ (degree 6) between two independent assemblies, and the sign is fixed a second and third way by dissipativity and by `eq:dissipation`. |

A single label would misrepresent the round: the *primary* discrepancy is class A, and
two class-B transcription defects were surfaced by the derivation the round was required
to perform. That is stated here rather than compressed into one word.

**No generic PASS is claimed.** The scope of what was verified is exactly what §3 lists.

## 2. The discrepancy, and the evidence

| ID | Discrepancy | Class | Evidence (independent of any earlier report) | Status |
|---|---|---|---|---|
| R16-1 | `eq:weak_carrier` transport sign: printed $-\ii\alpha_{\mathrm d}/\omega$, correct $+\ii\alpha_{\mathrm d}/\omega$ | A | (i) derivation from the implemented balance: $\partial_t\Delta n+\partial_iJ_i=0$, $\times\ii/\omega$, one IBP, $J_z=0$; (ii) operator comparison $4.2\times10^{-14}$; (iii) dissipativity: repaired sign gives $\operatorname{Im}\omega<0$ and $P_{\text{diss}}\ge0$ = `eq:dissipation`, printed sign gives growth | **repaired** |
| R16-2 | `eq:continuity`: $q\,\partial_t\Delta n+\partial_iJ_i=0$ with $J_i$ a number flux | B | dimensional analysis of the two terms ($\mathrm{C\,m^{-3}s^{-1}}$ vs $\mathrm{m^{-3}s^{-1}}$); with the printed $q$ the nondimensionalisation would give $\alpha_{\mathrm d}/q=5.2\times10^{18}$ instead of the $0.828$ that `eq:dissipation`, `eq:block` and the code all use | **repaired** (incl. the dependent amplitude statement at l. 534) |
| R16-3 | `eq:weak_gauss`: mobile charge printed as $\widehat N$ instead of $Q\widehat N$, $Q=d/L_D$ | B | the assembled $\varphi$–$\mu$ block equals $-Q\int\psi_ib_j$ to $3.7\times10^{-16}$ elementwise; the $\varphi$–$\varphi$ block contains the $Q^2$ screening to $1.1\times10^{-17}$; $Q=d/L_D$ to $2.9\times10^{-5}$, the residual being a rounded temperature | **repaired** |
| R16-4 | the unit of the carrier amplitude was implicit | B | `eq:block` gives the compressibility the unit coefficient of $-\langle\mathsf W_r,\mathsf W_s\rangle$, which fixes that unit; the scaling section did not say so | **repaired** (one sentence) |

### What the solver does, exactly

$$\mathcal L_{\text{impl}}=-\underbrace{\Bigl[\mathsf M+\frac{\ii\alpha_{\mathrm d}}{\omega}
\mathsf F\Bigr]}_{\text{repaired }eq:weak\_carrier},\qquad
\mathsf F=k_x^2\mathsf M+k_y^2\mathsf M+\mathsf S\succ0,$$

with $\max|\Re|=0$ on the transport block and $\min\operatorname{eig}\mathsf F
=5.588\times10^{-1}$. The implemented row is $-1$ times the repaired weak form; for a
homogeneous system that is a row operation and changes nothing. The two candidate signs
are $7.825\times10^{1}$ apart in operator norm — three orders of magnitude above any
plausible numerical artefact and thirty above the measured agreement error.

## 3. What was actually verified, and what was not

**Verified this round (executed, logs kept).**

| Check | Result |
|---|---|
| `scripts/static_check.py` | PASS — 112 labels, 86 references, 13/13 citations, 17021 words |
| `paper_a_study/test_model.py` | 52 tests, OK (23.8 s) |
| `paper_a_study/claim_audit.py` | PASS — 23 claims, 46 tokens, 11/11 source-agreement |
| `paper_a_study/mutation_tests.py` | PASS — 15 mutants, all caught |
| `paper_a_study/phase_speed_audit.py` | PASS |
| `paper_a_study/round16_carrier_sign_audit.py` | exit 0 — log `PAPER_A_ROUND16_AUDIT_LOG.txt` |
| Carrier row, independent assembly | $4.17\times10^{-14}$ (deg 4, 3 points), $9.68\times10^{-14}$ (deg 6, 3 points) |
| Reciprocity $\mathsf A_{01}=\mathsf A_{10}^{\mathsf H}$, $\mathsf A_{12}=\mathsf A_{21}^{\mathsf H}$, $\mathsf A_{22}=\mathsf A_{22}^{\mathsf H}$, $\mathsf A_{02}=\mathsf A_{20}=0$ | $3.2\times10^{-17}$, $9.2\times10^{-17}$, exact, exact |
| Non-Hermitian part located | $\mathsf A_{00}$ asymmetry $8.6\times10^{1}\to5.5\times10^{-13}$ and $\mathsf A_{11}$ $2.4\times10^{-1}\to7.1\times10^{-15}$ after removing the transport block |
| Contraction identity premise $\tau_{ijk}=\tau_{jik}$ | $0.00$ asymmetry in all three directions, two $k_y$ |

**Not executed, and therefore not claimed.**

* The full 18-gate clean-data battery. Not required: no solver, basis, quadrature,
  constant or boundary condition changed, and no dataset or figure was regenerated. Its
  last execution on freshly generated data remains
  `validation/round11_battery_run_clean_reproduction.log` (18 PASS, 0 FAIL, 1 SKIP — the
  skip is the LaTeX build).
* Elementwise comparison of the other 22 rows of the block system against an independent
  assembly. The mechanical audit is structural and algebraic (boundary terms,
  reciprocity, contraction premise), not elementwise.
* Figure re-inspection. No figure was touched this round; rounds 15's Fig. 5/Fig. 8
  inspections stand where they were made.
* Any PDF. See §5.

## 4. Files changed

| File | Change |
|---|---|
| `Paper_A_Final_Submission/sections/numerical_methods.tex` | R16-1 (sign), R16-1b (block sentence), R16-3 ($Q$ and its prose) |
| `Paper_A_Final_Submission/sections/governing_equations.tex` | R16-2, R16-2b, R16-4 |
| `Paper_A_Final_Submission/static_validation.txt` | regenerated by the static check |
| `paper_a_study/round16_carrier_sign_audit.py` | **new**, read-only audit script |
| `PAPER_A_ROUND16_AUDIT_LOG.txt` | **new**, its output |
| `PAPER_A_ROUND16_*.md` (six files) | **new** reports |
| `make_download_archive.py` | repointed to round 16, report list and `START_HERE.txt` narrative |
| `downloads/Paper_A_Complete_Project_round16.zip`, `downloads/README.md` | **new** archive and its entry |

No file under `paper_a_study/` that computes a physical quantity was modified. No
constant, boundary condition, dataset or figure was modified.

## 5. PDF status

**BUILD UNVERIFIED.** No TeX engine exists in this environment
(`pdflatex`, `latexmk`, `xelatex`, `lualatex`, `tectonic`, `bibtex` all absent) and none
can be installed from the reachable hosts. This is an environmental limitation and is
reported separately from source quality; the static checks above validate the source,
not the typeset output. The edits are local, keep the existing display widths, and add no
macro that the static whitelist rejects, but they have not been compiled.

## 6. Numerical and scientific impact

None. Every number in the paper — $R_B=0.9467952$ at $k_xd=0.5275$, the operating point
$0.0231456$, the propagating share $99.77\%$, the degree spread $6.22\times10^{-9}$, the
energy-identity residual $4\times10^{-12}$ — is produced by code that was not touched, from
equations whose scaled form is unchanged. The corrections are to the manuscript's display
of those equations.

## 7. Remaining issues

| Item | Status |
|---|---|
| Corner line force (M15-8) | **open**, unchanged, reported as open |
| Novelty against the primary 2025 source | **UNRESOLVED** (closed access) |
| Five `AUTHOR INPUT REQUIRED` declarations | **await the author** |
| $\ell$, $f$, $H$ | synthetic; unchanged |
| Mechanical block elementwise audit | **not executed** (scope) |
| Typeset build | **UNVERIFIED** (no engine) |

## 8. Readiness statement

* **Mathematical readiness of the carrier and Gauss sectors: VERIFIED** within the scope
  of §3 — the printed weak forms now reproduce the implemented operator, and the sign and
  the charge factor are each established two independent ways.
* **Mathematical readiness of the mechanical sector: PARTIALLY VERIFIED** — boundary
  terms, reciprocity and the contraction premise are checked; the corner line force is
  not, and no elementwise comparison was made.
* **Manuscript readiness: pending a typeset build** (environmental).
* **Submission readiness: NO** — open items in §7, and the build is unverified.

## 9. Archive

`downloads/Paper_A_Complete_Project_round16.zip`: one authoritative `main.tex`, all eight
section files, ten figures in PDF and PNG, the encoded datasets, the full `paper_a_study`
code (including the new audit script), the audit log, all round-16, round-15 and
round-14 reports, the supplement, `MANIFEST.json` with per-file hashes and the cumulative
correction history. Its size and SHA-256 are recorded in `downloads/README.md` and in the
delivery message rather than inside the archive, because a file cannot contain its own
hash. Integrity was verified with `unzip -t`, by re-running the static check inside the
extracted tree, and against `MANIFEST.json`.
