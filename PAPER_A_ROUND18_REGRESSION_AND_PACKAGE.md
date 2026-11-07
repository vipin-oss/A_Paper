# Paper A — Round 18: regression battery, static validation, package

**Branch** `arena/ea7ca4dd-a-paper` · base `c33cec6` · **BUILD UNVERIFIED**.

Because round 18 is a *repair* round, the regression question is narrow and can be
answered exactly: did anything that produces a number move?  Nothing did —
`git diff --stat` over the round contains five files, all of them `.tex` plus the
validator's own record:

```
 Paper_A_Final_Submission/sections/appendix_derivations.tex  | 313 +++++++-------
 Paper_A_Final_Submission/sections/governing_equations.tex   |  14 +-
 Paper_A_Final_Submission/sections/numerical_methods.tex     |  38 +--
 Paper_A_Final_Submission/sections/results.tex               |  32 +-
 Paper_A_Final_Submission/static_validation.txt              |  10 +-
```

`paper_a_study/model.py`, every producer under `paper_a_study/`, every dataset
under `paper_a_study/figure_data/` and every figure are byte-identical to
round 17.  The battery was nevertheless re-run, because "no producer changed" is
a claim that is worth testing rather than asserting.

---

## 1. Static validation

```
$ python Paper_A_Final_Submission/scripts/static_check.py
PASS
files checked: 9
labels: 161   references: 103
citation keys used: 13   bib entries: 13
```

* no duplicate label, no undefined reference, no reference to a label that
  disappeared in the rewrite (`eq:app_S_scaled` was renamed to `eq:app_S` and its
  one consumer in `numerical_methods.tex` was repointed in the same edit);
* no macro outside the whitelist (`\rm` inside `n_{\rm u}` was replaced by
  `\mathrm{u}` when the new appendix text introduced it);
* the 161 labels include the 12 that the repaired appendix now carries
  (`eq:app_measures`, `eq:app_mass`, `eq:app_S_off`, `eq:app_charge_T`,
  `eq:app_w2_values`, `eq:app_edge_R`, …); the never-referenced list is a warning
  list, not a failure, and contains only equations that are quoted by name in
  prose.

Word count and citation count are unchanged from round 17 to within the words
added and removed by the repairs (the validator's own record,
`static_validation.txt`, travels in the package).

## 2. Unit and physics suite

```
$ python paper_a_study/test_model.py
Ran 52 tests in 21.648s
OK
```

Two of those assertions pin the headline:

* `test_model.py:396` — `R = 0.9467952307` at the reported operating point;
* `test_model.py:562` — `assertGreater(ps, 0.9467952)` on the certified peak.

Both pass, so the number the manuscript reports is the number the solver still
produces after the edits.  The suite also covers the singular-edge rejection, the
temporal/spatial polynomial equivalence, reciprocity at oblique wavenumber, and
the energy–dissipation balance, i.e. the four sectors the repaired appendix
describes.

## 3. The two round-18 scripts

| script | checks | failures | exit | log |
|---|---|---|---|---|
| `round18_mathematical_audit.py` | 43 | 0 | 0 | `PAPER_A_ROUND18_AUDIT_LOG.txt` |
| `round18_reference_checks.py` | 59 | 0 | 0 | printed; grouped in `PAPER_A_ROUND18_INDEPENDENT_RECHECK.md` |

The audit log is shipped verbatim in this archive so that every PASS line and
every number behind this round can be read without running anything.

A note on how those numbers were obtained, because two of them were wrong on the
first attempt and were repaired rather than relaxed:

* the first constitutive block compared `sigma` against physical units: five
  FAILs, all of them a scaling convention, fixed by dividing the elastic part by
  `c44` and the electric part by `√(c44κ33)`;
* the flexoelectric term in the `D_z` check used `f3zz/(√(c44κ33))` instead of
  `f3zz/(d√(c44κ33))`, a factor `d`; the failing value was `6.0` against a scale
  of `122`, and the corrected group `2.563e-3` is the manuscript's own.

Neither was suppressed, and the log shipped here is the final, passing run.

## 4. Package

`build_submission_package.py` refreshed `Paper_A_Final_Submission/`:
**83 files, 2.93 MB**, `MANIFEST.json` rewritten with a SHA-256 per file, and the
static validator re-run *before* hashing so the manifest describes the file that
exists on disk.  The two round-18 scripts are now part of the shipped study tree.

`make_download_archive.py` was repointed from round 17 to round 18 (stage
`/tmp/paper_a_round18_stage`, output
`downloads/Paper_A_Complete_Project_round18.zip`, the six round-18 reports and
the audit log added to the root report list, and `START_HERE.txt` rewritten for
this round).

Build immediately **before** these last two reports were written:

```
archive : downloads/Paper_A_Complete_Project_round18.zip
files   : 275
staged  : 276 copies
size    : 3,284,221 bytes (3.28 MB)
sha256  : c6c43bf7654c55d91d4fc09d3bac57d93a595e762de91abd89de1618d6578b02
```

The final archive, rebuilt after this report and the final review were written,
has **277 entries** (the two extra files are the two reports); its size and
SHA-256 are in `downloads/PACKAGE_SHA256.txt`, which is authoritative because an
archive cannot contain its own hash and every edit to this text changes it.

That earlier build contains every report except this one and
`PAPER_A_ROUND18_FINAL_SUPERVISOR_REVIEW.md`, which were written after it.  The
archive is then rebuilt so that it contains them; the final hash is in
`downloads/PACKAGE_SHA256.txt` beside the ZIP, and in the hand-off message for
this round.  An archive cannot contain its own hash, so this report quotes the
build that immediately preceded it and names the file where the final value lives
— rather than quoting a hash that the reader cannot reproduce.

Reproducibility of the archive itself: every staged file is timestamped to
`FIXED_EPOCH = 2026-01-01T00:00:00Z` and written in sorted order with a fixed
compression level, so two builds of identical content produce the same SHA-256;
this was checked by building twice and comparing (identical).

## 5. What was *not* re-run, and why

* figure datasets and figures — no producer, dataset or figure changed;
* the 18-gate `run_all_checks.py` battery — its last clean run stands
  (`validation/round11_battery_run_clean_reproduction.log`, 18 PASS, 0 FAIL,
  1 SKIP, the skip being the LaTeX build);
* the LaTeX build — impossible here (no engine, no installable engine, the
  tectonic host is blocked).  **BUILD UNVERIFIED**; the supervisor-side commands
  are in `START_HERE.txt` and in the final review.

## 6. Files added to the repository this round

| file | purpose |
|---|---|
| `paper_a_study/round18_mathematical_audit.py` | 43 checks against the solver |
| `paper_a_study/round18_reference_checks.py` | 59 checks with no import from the solver |
| `PAPER_A_ROUND18_AUDIT_LOG.txt` | the audit log, verbatim |
| `PAPER_A_ROUND18_*.md` (six) | this round's reports |

No file was deleted or renamed.  The one historical report touched is
`PAPER_A_ROUND17_WORKED_CALCULATIONS.md`, which carries a dated erratum line for
an inverted Debye ratio in its own prose; it is marked as an erratum, not
silently edited.
