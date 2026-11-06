# Paper A — final submission readiness (round 7)

**Verdict: MAJOR REVISION — not submittable yet, and not claimed to be.**
The manuscript is scientifically coherent, its numbers are now consistent across
abstract, results, tables, discussion and conclusions, and every headline number
is machine-checkable. Two things still stand between it and a Q1 submission:
the primary to Q1 journal is not compilable in this environment (so the
typesetting is unverified), and the novelty position against Qu et al. (2025)
remains unresolved.

Commit and archive identifiers are in the delivery message and in
`downloads/README.md`; a file cannot contain the checksum of the archive that
contains it.

---

## 1. Category verdicts

| # | Category | Status | Basis |
|---|---|---|---|
| 1 | Mathematical correctness | **PASS** | Energy identity closes to 3.4e-16; signs re-derived; dimensional audit of 25 identities PASS; Schur bound enforced; reductions to the classical, piezoelectric, strain-gradient and H = 0 limits stated and checked |
| 2 | Numerical verification | **PASS** | 22 tests + 15 battery checks PASS; degree convergence 7.2e-7 / 2.1e-8; quadrature 6.9e-9; rescaling invariance 1.5e-15; 5/5 mutations caught |
| 3 | Physical interpretation | **MINOR REVISION** | The slow-mode reading is inference, and is labelled as such; the coupling is now correctly described as loss-mediated and configuration-dependent; no claim that H creates the effect |
| 4 | Scientific originality | **UNVERIFIED** | Novelty vs Qu et al. (2025) unresolved (closed access, no repository copy). The scattering problem itself is a defensible independent contribution; no priority claim is made |
| 5 | Material realism | **MAJOR REVISION** | ℓ = 50 nm, f = 1 nC/m and H ≤ 2.0e-23 J·m are synthetic; the elastic constants are literature values. Stated in three places, but a referee will still ask for a specimen-calibrated case |
| 6 | Reproducibility | **PASS** | One entry point (`run_all_checks.py`), datasets and scripts inside the archive, deterministic rebuild, frozen reference constants, claim registry |
| 7 | Manuscript quality | **MINOR REVISION** | Abstract 220 words, conclusions ≈250 words, title 15 words, 6 keywords, no internal paths in captions, no revision history. Author-controlled declarations are placeholders |
| 8 | Bibliographic quality | **PASS** | 13 entries, all verified against an external record this round; 4 DOIs added; 2 directly relevant papers added; no unverified entry |
| 9 | Typesetting | **UNVERIFIED** | No TeX engine here; the source is statically validated (balanced environments, 100 labels resolved, 13/13 citations, no undefined macro, no fragile command in a moving argument). The independent reviewer's 30-page build refers to round-6 source, not to this revision |
| 10 | Journal-specific compliance | **NOT APPLICABLE** | No target journal selected; a checklist is provided in §4 |

## 2. What this revision established

* The headline number is now **93.19 %** at k_xd = 0.5250, certified, converged
  and quadrature-sufficient — and it is the corrected reading of the paper's own
  earlier table, not a new claim.
* The coupling's role is quantified at three configurations (**−1.21 %,
  −9.85 %, −33.1 %**) instead of one, and explained as attenuation of the
  backward branch rather than as a partition modifier of unknown size.
* Every quoted number is registered, and a mutation of any registered number now
  fails the battery.
* Two previously uncited, directly relevant papers are now cited, and the gap
  statement is narrowed to what those papers do not do.
* A material-unit error can no longer pass the test suite.

## 3. Remaining limitations (unchanged or newly explicit)

1. **No PDF was produced here.** Build status is UNVERIFIED. The round-6
   reviewer build (30 pages) predates this revision and must not be quoted as
   evidence for it.
2. **Novelty vs Qu et al., IJES 208 (2025) 104165 is unresolved.** The access
   status was checked and recorded (`oa_status = closed`). Comparison is against
   the open-access transcription in Hu et al., IJMS 305 (2025) 110740. No
   priority claim.
3. **Corner line forces are uncertified.** The corner-band diagnostic bounds one
   energy fraction and shows it does not grow under refinement; it says nothing
   about the work of a singular traction. The manuscript states both facts.
4. **ℓ, f, H remain synthetic**, carriers are linearised about uniform doping,
   there is one edge, and self-heating and screening nonlinearity are neglected.
5. **The branch maximum is nearly degenerate with the incident wavenumber**
   (K_B/K_inc = 0.992). The value is admissible and converged, but a referee
   should be told this explicitly — the manuscript does tell them, in the caption
   of the sweep and in the discussion.
6. **The corner diagnostics were not re-run at the new branch maximum**; they are
   reported at the operating point and at k_xd = 0.55. This is stated in the text.

## 4. Target-journal checklist (to be completed once a journal is chosen)

| Item | Status |
|---|---|
| Journal selection | **AUTHOR INPUT REQUIRED** |
| Article class / template | currently `article` + 22 mm margins; a journal template will change the page count |
| Abstract limit | 220 words — within most limits (150–250), verify against the chosen journal |
| Title length | 15 words |
| Figure format | vector PDF, 10.5 cm width, ≥ 7 pt text |
| Reference style | `plain`; switch to the journal style (e.g. `elsarticle-num`) when known |
| Declarations | data availability truthful; competing interests / funding / CRediT / generative-tool disclosure marked AUTHOR INPUT REQUIRED |
| Supplementary material | the complete package; check the journal's size limit and whether code may be included |
| Cover letter | **AUTHOR INPUT REQUIRED** |

## 5. AUTHOR INPUT REQUIRED (nothing invented here)

1. Author list, affiliations and corresponding-author details (currently one
   author and one affiliation).
2. Competing-interests statement.
3. Funding agency, sanction number and date, or a statement that none applied.
4. CRediT contribution statement.
5. Acknowledgements.
6. Generative-tool disclosure per the chosen journal's policy.
7. Journal selection, template and reference style.
8. Cover letter.
9. Approval of the scientific repositioning: the paper now reports **93.19 %** at
   the branch maximum rather than 57.92 %, and the coupling as a **−33.1 %**
   effect there. This changes a headline number the author previously approved,
   and it needs an explicit decision.
10. Access to Qu et al. (2025) — from a subscription or an author copy — to close
    the novelty question. Without it the paper must keep its "no priority claim"
    wording.

## 6. Recommendation

Submit after: (a) a successful LaTeX/BibTeX build with page and float inspection,
(b) the author's decision on the repositioned headline result, (c) the
declarations filled in, and (d) one of the two outcomes on novelty — either the
primary article is obtained and the comparison completed, or the current wording
(independent addition, no priority claim, comparison limited to the inspected
decomposition) is accepted as final. Nothing else in the repository is blocking.
