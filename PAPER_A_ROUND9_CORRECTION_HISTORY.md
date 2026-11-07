# Paper A — Round 9: correction history

**Pre-edit state:** `081cc8e5c2f887c084de4992a856c9aedf335c45` (round 8), branch
`arena/ea7ca4dd-a-paper`.
**Scope:** repair the single verified defect found in the Stage-1 audit
(`PAPER_A_ROUND9_STAGE1_NORMALIZATION_AUDIT.md`), re-derive every record that depended on it, and
tighten the gates so the defect cannot return. Nothing else was redesigned: the model, the search
interval, the reference-plane definition of `R_B` and the headline `0.9467952` are untouched.

---

## 1. The defect, in one paragraph

`R_B` is a **ratio** of two modal powers, `P_B / P_i`. Moving it between planes parallel to the edge
therefore requires the attenuation of *both* modes:

```
R_B(L_to) = R_B(L_from) · exp[ 2 (Im K_i − Im K_B)(L_from − L_to) ]
          = R_B(L_from) · exp[ 2 (|Im K_i| + |Im K_B|)(L_from − L_to) ]     (Im K_i > 0 > Im K_B)
```

The exponent is a **sum of magnitudes**, because the incident mode attenuates on the way in and the
backward mode on the way out. Three call sites used only the backward single-mode decay
`exp(+2|Im K_B| L)`, which is the transform of an *absolute* channel power (`isolated_transfer`), not
of a ratio. The largest consequence was in `peak_search.py`, the script that locates and certifies the
maximum: it reported an edge-plane share of **0.965978** where the shared transform and a direct
solution at `L = 0` both give **0.985572** — a 1.9594 percentage-point error, and the only place where
two scripts disagreed on the same physical number.

The reference-plane value `R_B = 0.9467952306769204` at `k_x d = 0.5275` never depended on the
transform: it is `backward_reflection_self_power` read directly from the solve at
`L = REF_NORM = 10`. **94.68 % is unchanged**, and it was not adjusted to compensate for anything.

---

## 2. Source edits

| # | file | change | old → new | why |
|---|---|---|---|---|
| S1 | `paper_a_study/build_figure_data.py` | `edge_plane_fraction(R_at, ki, kb, d, L_to=0.0, L_from=REF_NORM)` re-expressed with explicit plane arguments; derivation, scope and identity checks in the docstring | `net = 2(abs(ki.imag)+abs(kb.imag))/d; R*exp(net*L*d)` with a single `L` meaning “distance towards the edge” → `2((ki.imag − kb.imag)/d)(L_from − L_to)d` | the old signature made `L = 0` return the input and `L = REF_NORM` return the edge value, i.e. one argument with two meanings; the new form is the equation above verbatim |
| S2 | `paper_a_study/build_figure_data.py` | fig02 `R_B_edge` | `isolated_transfer(R2, kb, p.d, 0.0)` → `edge_plane_fraction(R2, ki, kb, p.d)` | single-mode decay used as a ratio transform |
| S3 | `paper_a_study/build_figure_data.py` | fig05 `R_B_edge` | `R2*exp(α_B·REF_NORM·d)` → `edge_plane_fraction(R2, ki, kb, p.d)` | incident attenuation omitted |
| S4 | `paper_a_study/build_figure_data.py` | fig07 `R_B_edge` | `R2*exp(α_B·REF_NORM·d)` → `edge_plane_fraction(R2, ki, kb, p.d)` | same defect, 95 rows |
| S5 | `paper_a_study/build_figure_data.py` | `isolated_transfer` docstring | silent about scope → states explicitly that it is a single-channel absolute transfer, is *not* a ratio transform, and differs from one by 2.0 pp at the certified maximum | the function itself is correct for Figure 6 and stays |
| S6 | `paper_a_study/peak_search.py` | the duplicated formula is **deleted**; the module imports `edge_plane_fraction` from `build_figure_data` | `R_B*exp(2|Im K_B|·10)` → shared transform | the confirmed cross-script defect; 181 coarse/plateau/refined rows + 12 degree rows + 6 quadrature rows |
| S7 | `paper_a_study/mechanism_controls.py` | three call sites now pass `p.d` instead of `1.0`, with a comment that `d` cancels in the ratio but must not be assumed to be a thickness | `…, 1.0)` → `…, p.d)` | cosmetic: the ratio is bit-identical, but the `1.0` implied that `d` is not the thickness |
| S8 | `paper_a_study/peak_identity_audit.py` | inline `R*exp(net(L−10))` replaced by two calls of the shared transform (plane → edge → plane); the audit additionally solves at `L = 0` | second implementation → one implementation | removes the last duplicate exponent; `L = 0` is now a case, not an assumption |
| S9 | `paper_a_study/claims.json` | `edge_plane_fraction`-dependent claims registered: `R_B_edge_certified_maximum`, `R_B_edge_operating_point`, `R_B_edge_k055`, plus the re-measured spreads (§5) | — | the edge fraction had no claim at all, which is why the defect survived round 8 |
| S10 | `paper_a_study/claim_audit.py` | new gate: the degree-22 edge share in `peak_search.json` must equal `mechanism_controls.json` to 1e-6 relative; per-case edge rows for the operating point and `k_x d = 0.55`; the record is now written only when the real manuscript is audited | — | cross-script agreement is now a gate, not a hope |
| S11 | `paper_a_study/mutation_tests.py` | five new mutants (M9, M10, M10b, M11, M12) that patch the transform in memory and require the new tests to fail | 8 mutants → 13 | see `PAPER_A_ROUND9_MUTATION_REPORT.md` |
| S12 | `paper_a_study/test_model.py` | three new test classes: `TestEdgePlaneTransform`, `TestPlaneInvariance`, `TestCrossScriptEdgeFraction` | 26 → 39 tests | see `PAPER_A_ROUND9_TEST_RESULTS.md` |
| S13 | `build_submission_package.py` | the static validator now runs *before* `MANIFEST.json` is written | manifest hashed before the validator rewrote `static_validation.txt` | the round-9 archive initially failed its own manifest check on exactly that one entry |

Files that were inspected and deliberately **not** changed: `isolated_transfer` semantics (correct for
Figure 6), fig06 `R_B_isolated` / `incident_survival` (absolute channel quantities), the
`peak_identity_audit` reconstruction at a fixed plane (both factors already refer to the same plane, so
only the backward decay belongs), `legacy/run_study.py:52` and
`legacy/regenerate_revised_data.py:287,545` (algebraically identical to the corrected form), fig04
`R_B_edge` (already correct) and fig04 `R_B_100um` (a single-channel extrapolation, correctly labelled,
not plotted and not quoted).

---

## 3. Regeneration

Every record that reads the transform was rebuilt from the corrected sources, serially and
single-threaded (two solver scripts on two cores make each about ten times slower):

| step | command | time | artefact |
|---|---|---|---|
| data | `python paper_a_study/build_figure_data.py` | 193 s | 13 CSVs/JSONs (`fig01` 41.8 s, `fig02` 67.9 s, `fig04` 40.2 s, `fig07` 24.3 s) |
| schema repair | `python paper_a_study/reclassify_csv.py` | 0.2 s | restored `x_flux_fraction` to `fig02`/`fig04`/`fig07` (130 / 139 / 95 rows, 0 classifications flipped) |
| peak search | `python paper_a_study/peak_search.py` | 145.6 s | `peak_search.json` |
| matched controls | `python paper_a_study/mechanism_controls.py` | 77 s | `mechanism_controls.json` |
| identity audit | `python paper_a_study/peak_identity_audit.py` | 9 s | `peak_identity_audit.json` |
| certification | `python paper_a_study/certify_peak.py` | 6 s | `peak_certification.json` |
| figures | `python paper_a_study/generate_final_figures.py` | 7 s | 10 vector PDFs |

The figure data is regenerated even though no panel plots `R_B_edge`: the CSVs are part of the
published data package and would otherwise ship a column that contradicts the corrected transform.

---

## 4. What the correction moved, and what it did not

Edge-plane column, committed (round 8) against regenerated (round 9):

| record | rows | round 8 range | round 9 range | largest relative change |
|---|---|---|---|---|
| `fig02_material_parameter_sweep.csv` | 130 | 3.0e-9 … 0.579854674 | 3.0e-9 … 0.580359068 | 1.4e-3 |
| `fig05_channel_power.csv` | 5 | 0.022855335 … 0.023148041 | 0.023008259 … 0.023150542 | 6.7e-3 |
| `fig07_coupling_sensitivity.csv` | 95 | 0.019173219 … 0.025598324 | 0.019304343 … 0.025601054 | 6.8e-3 |
| `peak_search.json` (deg 22, `k_x d = 0.5275`) | 1 | 0.965978366 | 0.985572194 | 2.0e-2 |

Every non-edge column was compared column by column with the round-8 data: real quantities agree to a
relative 1e-6 or better, and only the round-off columns (`closure_residual`,
`power_balance_error`, `edge_scaled_residual`) move freely, as they must. No classification and no
discrete column changed. The reference-plane headline is reproduced exactly:
`R_B(0.5275) = 0.9467952306769204`, `R_B(argmax = 0.52752) = 0.9467953685099261`,
`classification = certified_local_maximum`.

---

## 5. Records re-read against the regenerated data

The correction moved four numbers that the manuscript quotes. Each was re-derived from the stored
record rather than adjusted by hand:

| quantity | round 8 text | round 9 text | source |
|---|---|---|---|
| spread of the maximum over degrees 14–34 | 5.6e-9 | **5.0e-9** | `peak_search.json → degree_spread["0.52752"] = 4.973e-9` |
| same, at the reported wavenumber | 6.2e-9 | **7.3e-9** | `degree_spread["0.52750"] = 7.281e-9` |
| spread over 64–256 quadrature nodes | 9.4e-10 | **5.6e-9** | `quadrature_spread = 5.591e-9` |
| `max|ΔR_B|/R_B`, certified maximum / earlier sample (Table 3) | 1.7e-9 / 2.1e-8 | **3.8e-9 / 2.3e-8** | `peak_certification.json`, degrees 18–30 |
| operating-point edge share (Table 5) | 0.0231 | **0.0232** | `mechanism_controls.json → operating_point/no_coupling/R_B_edge = 0.023150542` |
| Fig. 9 panels (a)–(c) description | “3e-6 and 4e-12 at n = 14 … both remain at 1e-12–1e-13, four to five orders below 1e-8 and 1e-10” | rewritten: channel error 3e-6 → 1e-7, wavenumber at the 1e-12 floor, residual 3e-15, balance 2e-13…1e-12, six to seven and two to three orders below | `fig09_validation_convergence.csv` |
| round-off digits in §5.1 | 3.4e-16, 7.3e-13, 3.2e-13 | **1.9e-17, 6.6e-13, 3.0e-13** | `fig05_channel_power.csv` (H = 0), `mechanism_controls.json → refined_peak/full` |

The 0.0231 → 0.0232 change is a rounding decision, not a physics change: 0.0231505 rounds to 0.0232 at
four decimal places and rounded to 0.0231 only because the table had been filled from a truncated
intermediate. The registry tolerance for that row is 5e-3, because a four-decimal share cannot be
compared more tightly than its own rounding.

---

## 6. What stays fixed, on purpose

* **The reference plane.** `R_B` is still defined at `L = REF_NORM = 10` thicknesses; the edge plane
  is a derived, reported quantity. The transform was corrected towards the edge, not the definition.
* **94.68 %.** Unchanged, uncorrected, unadjusted. The defect never touched it.
* **The classification.** `certified_local_maximum` inside the declared search interval
  (0.465, 0.625), flat top, not a global maximum, not a statement about energy turned around.
* **The single-mode function.** `isolated_transfer` remains, correctly, for absolute channel decay.
* **Tolerances.** New assertions compare at 1e-6 relative, not 1e-9: the defect scale is 2e-2, and
  cross-plane agreement of float arithmetic is only good to about 1e-6.
* **The 94.68 % / 98.56 % distinction.** The two numbers are different quantities at different planes;
  the paper now says so in print (§4.5), and no reader is invited to compare them as one number.

---

## 7. Verification of this correction

* unit and scientific tests: **39 passed in 8.9 s** (`python -m unittest paper_a_study.test_model`);
* `claim_audit.py`: **PASS**, 22 claims, 45 tokens, 9 source-agreement rows, 5 deprecated values guarded;
* `mutation_tests.py`: **PASS**, 13 mutants injected and 13 caught;
* `run_all_checks.py`: **18 gates PASS**, LaTeX build not executed (no engine);
* the plane invariance itself: see `PAPER_A_ROUND9_PLANE_INVARIANCE_VALIDATION.md`.

**Not verified:** the LaTeX build. No TeX engine exists in this environment, and an earlier compiled
PDF does not certify the current source. The source is statically validated only.
