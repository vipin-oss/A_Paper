# Paper A — Round 4 independent scientific and manuscript audit

**Source:** `Paper_A_Complete_Project_round4.zip`, reported commit `37b915dcb32445feaaaa0356f67e99abab2860b7`.
**Independent check:** 6 November 2026. **Editorial judgment:** **Major revision before submission**, not Q1-ready. The figures and key numerical tests have improved, but there is one confirmed scientific-data attribution defect and visible PDF layout failures.

## Verified package and build

- ZIP contains **161 entries**, passes `ZipFile.testzip()`, size **2,629,767 bytes**, SHA-256 **`cb60652d0adf8499f64bed6d5d4bce1ea860396c460dbfc7bebbf9ed0404466b`** (matches supplied checksum).
- Authoritative `Paper_A_Final_Submission/main.tex`, 10 vector-PDF figures, `references.bib`, source model, control scripts and material inputs present.
- **Full LaTeX + BibTeX build independently successful**: `pdflatex`, `bibtex8` (with `BIBINPUTS` pointed to manuscript source), then twice `pdflatex`. **29-page compiled PDF**. No unresolved citations/references after proper build. Initial BibTeX failure when executed from a separate output directory was a **build-search-path issue**, not a missing bibliography.
- `python -m unittest paper_a_study.test_model -v`: **18/18 tests pass** (12.737 s in audit environment).
- `python -m paper_a_study.modal_flux_audit`, `python -m paper_a_study.phase_speed_audit`, `python -m paper_a_study.verify_dimensions`: all independently executed and PASS.

## Critical: corner-study uses the *backward* wavenumber as its *incident* operating wavenumber

**Exact source:** `Paper_A_Final_Submission/paper_a_study/corner_assessment.py`:

```python
from build_figure_data import KB0, KY0, plate, track, operating_mode
CASES = {'operating_point': KB0, 'peak': 0.55}
...
res, scr = p.edge(KY0, float(m['omega'].real), K, KB0)
```

`KB0=0.2451746921716515` is the **backward target root**, not the incident operating-point root `K0=0.7361990195318475`. Because `K` also enters branch tracking and `edge(..., incident_guess=K, target_guess=KB0)`, this incorrectly creates a **different incident scattering experiment** and then labels its result `operating_point`.

### Independent one-for-one replay (Galerkin degree 22)

| Diagnostic | Using intended incident `K0` | Using current erroneous `KB0` |
|---|---:|---:|
| `R_B` returned by solver | **0.02314561918** (2.3146%) | **0.54439742640** (54.4397%) |
| Corner-band gradient-energy share | **0.00995751730** (0.996%) | **0.02131477251** (2.131%) |
| Corner-band peak/mean diagnostic | **0.10210799066** | **0.20610064207** |

Both calls succeeded using the *same solver* and identical degree, `KY0`, and target `KB0`. Only the incident case's `K` differs. The stored `corner_assessment.json` reports **0.5444** as operating-point `R_B`; in contrast `peak_certification.json` and manuscript describe **0.0231456**. Thus its recorded corner shares for the **operating point are for the wrong case**.

**Required correction:** Import `K0` as well as `KB0`; set `CASES = {'operating_point': K0, 'peak': 0.55}`. Regenerate **all four degree rows** for the corrected operating case. Update `sections/discussion.tex` corner-band percentages and any audit findings claiming that `2.00–2.13%` applies to the operating point. Add a cross-file regression assertion that `corner_assessment.json`'s `operating_point.R_B` agrees with `peak_certification.json`'s matching degree to a meaningful tolerance. Retain the peak case only after independently checking its matching identifiers. Re-assess the strength of conclusions: a falling outer-band share alone does **not** certify that a mathematically possible corner line force has negligible scattering effect.

**Classification:** **CONFIRMED scientific provenance / case-selection defect — fix required**. This escaped the passing 18-test suite.

## Major: visible publication-layout defects in the compiled PDF

- Full compiled manuscript is **29 pages**, not Arena's prior uncompiled 26-page estimate. This is not itself a defect; the compiled PDF is authoritative.
- LaTeX final log contains overfull boxes **102.17 pt**, **4.14 pt**, and **372.96 pt**; the latter is the appendix file/role table. Page 28 shows text crossing its intended right margin and truncated content. Fix using a wrapped `tabularx`/`longtable`, appropriate columns and `\texttt{}` breaks; check figures and tables visually at final manuscript size.
- Appendix `sections/appendix_reproducibility.tex` says `phase_speed_audit.py` **"exits non-zero by design"**. In the current corrected project the script actually exits **0 on PASS** and nonzero on mismatch. The package instructions should say precisely that; the command block also repeats the incorrect description.
- Appendix file table and manuscript have occasional overly dense text/long inline code paths. Fix without wholesale rewriting or changing underlying figures.

**Classification:** **CONFIRMED layout/documentation corrections required**.

## Independently supported scientific improvements

- **Phase speed:** Recomputed approximately **28.046 km/s** from `K0`, `KY0`, `OMEGA0`, `d`, and `c_s`, consistent with `phase_speed_audit.json`; prior 2.8 km/s prose value is corrected.
- **EM wavelength:** `lambda_EM=5.68355 mm`, `k_EM*d=2.211e-4`, `d/lambda_EM=3.519e-5`; consistent and distinct from `1/k_EM=0.9046 mm`.
- **Mode-power normalization:** At degrees 18/22/26/30, raw eigenvector `P_x` changes under modal normalization, while `|a_B|²P_B` and normalized `R_B` remain stable; rescaling test independently PASS. Does **not** by itself prove a physically observable total reflectance.
- **Mechanism controls:** Stored data are consistent with a backward branch existing at `H=0`, and a specular rather than identified backward port in the `ell=0` control. This is a **single-parameter operating-configuration result**, not a general theorem; the control follows a shifted branch frequency, so the configurations should not be described as identical-frequency experiments.
- **Novelty:** Original equation-level priority relative to the complete Qu et al. article **remains unresolved**. Do not advertise a first-ever enthalpy term.
- **Parameters:** `ell`, `f`, `H` remain synthetic; numerical convergence does not establish experimental predictive validity.

## Requested focused final correction

1. Fix the **corner operating-point wavenumber selection**, regenerate degree-dependent corner diagnostic and manuscript text, and add a regression cross-check against peak certification.
2. Recompile with complete bibliography; repair the severe **appendix table 372.96-pt overflow** and other overfull lines, and inspect all 29 pages.
3. Correct appendix's inaccurate statement about `phase_speed_audit.py` exit status.
4. Check control-study attribution and keep explicit `H=0` mechanism and novelty qualifications; preserve the ten validated vector figures unless their data/interpretation genuinely change.
5. Include compiled PDF and reproducibility logs in next delivery; give a verified **one-click direct HTTPS ZIP link**, file size, SHA-256, full commit.

**Overall editorial verdict:** **REVISE**. The numerical foundation and scientific positioning are significantly improved, and actual LaTeX/BibTeX compilation is now demonstrated. The mislabeled corner-study operating point is a real scientific error that requires correction before the paper can be considered for submission. Additional unresolved novelty/material realism issues remain.
