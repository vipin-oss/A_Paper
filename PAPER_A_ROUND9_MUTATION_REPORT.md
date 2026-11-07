# Paper A — Round 9: mutation report

**Question:** do the gates actually fire? A check that has never failed is not a check.

**Answer:** 13 deliberate defects were injected, one at a time, and **13 were caught** by the gate that
is supposed to catch them. No gate was "tested" by observation alone, and no coverage is claimed for a
defect that was never injected.

Implementation: `paper_a_study/mutation_tests.py`, record: `paper_a_study/figure_data/mutation_tests.json`
(`13 mutants, verdict PASS`).

---

## 1. How the mutations run

* **Isolated copies.** M1–M4, M6 and M8 copy `Paper_A_Final_Submission/` to a fresh
  `tempfile.TemporaryDirectory()`, edit the copy, run the gate against it (`--root <copy>`), and delete
  the copy. The working tree is never touched.
* **In-process, restored.** M5, M7, M9, M10, M10b, M11 and M12 patch a module attribute or a dictionary
  entry in memory, run the gate, and restore the original in a `finally` block. The run afterwards
  re-executes the unaffected suite, and the next gate in the battery (`claim_audit`) confirms the
  records are unchanged — so a leak would be visible as a second failure.
* **One defect at a time.** No mutant is combined with another; each is expected to make exactly its
  target gate fail, and the recorded `evidence` field holds the failing line.
* **No mutation survives the run.** The stage directories are temporary, and the delivered tree
  contains the unmutated sources.
* **No mutation reaches the delivered record.** Found and fixed this round: `claim_audit.py` wrote
  `figure_data/claim_audit.json` even when it was auditing a mutated *copy*, so a run of this battery
  left a record reading `FAIL` next to 13 caught mutants — a false alarm in the shipped data. The
  script now writes its record only when it audits the real manuscript, and the record is verified to
  read `PASS` after the battery runs.

Each mutant patches the *consumer* module's own attribute. That detail matters: `paper_a_study.*` and
the script-style `build_figure_data` that the solver scripts import are two distinct module objects, and
patching only one of them leaves the other — and therefore the script under test — unmutated. The first
attempt at M9–M12 did exactly that and reported `MISSED`; the harness now patches every copy that is
present in `sys.modules`, and the new tests look the transform up by attribute rather than binding it
at import.

---

## 2. The thirteen mutants

| id | defect injected | gate that caught it | evidence (abridged) |
|---|---|---|---|
| M1 | `\path` in a figure caption without `\protect` | `static_check.py` | `fragile \path in a moving argument (\caption)` |
| M2 | registered headline edited 0.9468 → 0.9486 | `claim_audit.py` registry | claim `headline_R_B` token missing / value mismatch |
| M3 | deprecated total outgoing power 0.99985 re-inserted | `claim_audit.py` stale guard | deprecated value present in `results.tex` |
| M4 | undefined citation `\cite{nosuchkey2024}` | `static_check.py` | `undefined citation key nosuchkey2024` |
| M5 | `c44` entered in Pa instead of GPa | `TestFrozenReferenceConstants` | stored constant differs from the reference value |
| M6 | superseded coarse-grid maximum 93.19 at 0.525 reinstated | `claim_audit.py` stale guard | `93.19` present in `main.tex` |
| M7 | peak case labelled with the backward root `KB0` instead of its incident root | `TestCornerAssessmentCaseSelection` | case label and solved root disagree |
| M8 | incident wavenumber replaced by `KB0` in the registry | `claim_audit.py` source agreement | `KB0` within 0.2 of the incident root |
| M9 | edge-plane transform reduced to the backward decay only (the round-8 defect) | `TestCrossScriptEdgeFraction` | `fig05 CSV vs shared transform: 6.7e-03` |
| M10 | sign of the plane-transform exponent flipped | `TestCrossScriptEdgeFraction` | stored edge share no longer reproduced |
| M10b | the same flipped exponent, checked by an invariance test that uses **no stored record** | `TestPlaneInvariance` | `reconstructed edge value depends on the plane: 6.4e-04` |
| M11 | reference plane moved from 10 to 8 thicknesses | `TestCrossScriptEdgeFraction` | stored edge share no longer reproduced |
| M12 | thickness `d` replaced by the gradient length `ℓ` (`L`/`ℓ` confusion) | `TestCrossScriptEdgeFraction` | `fig05 CSV vs shared transform: 1.0e+00` |

M9–M12 and M10b are new this round; they exist because the round-8 suite could not have caught the
defect that round 9 had to repair. M10b is deliberately redundant with M10 but exercises a different
kind of test: M10 is caught by comparing against a stored record, M10b by an invariance property that
uses no record at all. If the stored data were ever silently regenerated from a broken transform, M10
would pass and M10b would still fail.

---

## 3. What the mutation battery proves, and does not

**Proves:**

* the static validator catches fragile moving arguments and undefined citations;
* the claim registry catches edited headline numbers, re-inserted deprecated values and a
  mislabelled root;
* the unit suite catches a unit error in a frozen constant and a case-labelling error;
* the three new plane tests catch every plausible way of getting the two-mode ratio transform wrong
  (halved exponent, flipped sign, wrong reference distance, `L`/`ℓ` confusion);
* a mutation applied to one module object but not its twin does **not** propagate — the harness detail
  above — which is itself a finding about how the scripts import each other.

**Does not prove:**

* that the physics is right. Mutations test the gates, not the model.
* coverage of the search, the quadrature audit or the corner assessment beyond the two mutants aimed at
  them (M6, M7). Those gates are exercised by their own records, not by injection.
* that the LaTeX document compiles. No engine exists here, and no mutation was aimed at compilation.

---

## 4. Cleanup state

* No mutation is present in the delivered tree: `git status` shows only the round-9 corrections, and
  the post-battery `claim_audit.py` run — which reads the same records the mutants touched — passes.
* The scratch directories (`tempfile.TemporaryDirectory`) are removed by the harness; nothing is
  written outside `figure_data/mutation_tests.json`.
* `figure_data/mutation_tests.json` is part of the package and is regenerated by
  `paper_a_study/run_all_checks.py`.
