# Paper A — round 13: pre-edit closure audit

Written **before** any change was made in this round. Every item below was
reproduced from the current source, not taken from a previous report.

| | |
|---|---|
| Repository | `vipin-oss/A_Paper` |
| Branch | `arena/ea7ca4dd-a-paper` |
| HEAD at audit time | `3827543016ece4a9d0612e861bf75425457291bf` ("Round 12: section-by-section manuscript review; nineteen prose corrections") |
| Working tree | clean (`git status --short` empty) |
| `origin/main` | `b7d46065fcab8dfde0160b8c4db5f073ed084321` — unchanged since the branch was cut; this round does not touch `main` |
| Authoritative manuscript | `Paper_A_Final_Submission/main.tex`, 7 section files, 10 figures, 80 manifest entries |

Scope: the two blockers carried from round 12 (B1, B6), the report-level
misattribution flagged for this round, and a documentation sweep. No numerical
model, dataset, solver or result is a candidate for change.

---

## 1. The headline values, re-verified before editing

These are checks, not targets. Every one was read from a delivered record.

| quantity | expected | record | stored value | verdict |
|---|---|---|---|---|
| operating-point share | ≈0.0231456 | `peak_identity_audit.json` → `cases.operating_point.R_B` | 0.023145619184645957 | MATCH |
| reported peak | $k_xd=0.5275$ | `peak_identity_audit.json` → `cases.peak.K_branch` | 0.5275 | MATCH |
| refined argmax | $k_xd=0.52752$ | `peak_search.json` → `classification.reported_vs_argmax` | 0.52752 | MATCH |
| $R_B$ at the reported peak | 0.9467952 | `cases.peak.R_B` | 0.9467952305821763 | MATCH |
| $R_B$ at the refined argmax | 0.9467954 | `peak_search.json` → `classification.R_B_argmax` | 0.9467953677961777 | MATCH |
| frequency near the peak | ≈16.6547 GHz | `peak_certification.json` | 16.6547… | MATCH |
| $H/H^{*}=+0.05$ at the reported peak | ≈0.622973 | `mechanism_controls.json` → `refined_peak.full.R_B` | 0.6229733 | MATCH |
| reconstructed edge-plane share | ≈0.985572 | `peak_identity_audit.json` → `reference_plane.rows[0].R_B` | 0.9855722003583304 | MATCH |
| $H$-coupling change at the reference plane | ≈−34.2 % | `mechanism_controls.json` → `branch_consistent_H_sweep` | 0.9467952 → 0.6229733 = −34.2 % | MATCH |

No headline value is unsupported. Nothing in this round may change one.

---

## 2. B1 — the backward-wavenumber arrow in fig10(c)

| field | content |
|---|---|
| **ID** | B1 |
| **File and location** | `paper_a_study/generate_final_figures.py`, `def fig10()`, the schematic block, line 895: `arrow((0.333, -0.530), "#087E8B", r"${\bf k}_B$", (-0.82, 0.74), 0.74, ha="right")` |
| **Existing problem** | the arrow drawn as the backward **wavenumber** combines two incompatible ratios ($K_{Bx}/K_{ix}=0.333$ and $\lvert k_y\rvert/K_{Bx}=0.530$) and carries the sign of the **flux**. It therefore points at $\arctan2(-0.530,0.333)=-57.86^{\circ}$, i.e. 58° **below** the $+x$ axis, into the fourth quadrant, while the solved mode's wavenumber lies 27.9° **above** it. Its drawn length is also wrong: 0.463 against 0.558 for $\vect{k}_i$, a ratio of 0.829 where the solved magnitude ratio is 0.371. |
| **Source evidence** | a single edge solve at the figure's own configuration (`KY0 = 0.12981175031447484`, `OMEGA0 = 7.633372404423294`, `K0 = 0.7361990195318475`, `KB0 = 0.2451746921716515`, `degree = 22`) returns `backward_K = 0.2451746921716515 − 5.230595074070594e−06i`, `incident_K = 0.7361990195318475 + 5.402718679033664e−06i`, `ky = 0.12981175031447484`, `frequency = 16.68412313636555 GHz`, `negative_direction = True`. Hence $k_y/k_{Bx} = 0.5294663538257495$ and the phase direction is $\arctan2(k_y,k_{Bx}) = +27.8997139835^{\circ}$; $\lvert\vect{k}_B\rvert/\lvert\vect{k}_i\rvert = 0.3711022669787309$. Cross-check: the same solve returns `reflected_angle_deg = −27.8997139811`, i.e. $\arctan2(P_{By},-P_{Bx})$ — the flux measured against the backward axis — and $\lvert P_{By}/P_{Bx}\rvert = 0.5294663537700$. |
| **Configuration check** | the figure solve is the **H = 0** configuration: its frequency, 16.6841231 GHz, equals `mechanism_controls.json` → `operating_point.no_coupling.frequency_GHz` (16.6841231) and its share equals `operating_point.no_coupling.R_B` (0.0231456), which is the operating-point share quoted throughout the manuscript. `mechanism_controls.json` → `operating_point.full` is a different, coupling-on configuration (16.6839845 GHz, $k_{Bx}=0.2454907$, angle −27.8692°) and must **not** be used to draw this panel. The distinction matters at the 0.1 % level in $k_{Bx}$ and 0.03° in angle, and it is the reason the vector must be read from `fig10_field_metrics.json` and not from `mechanism_controls.json`. |
| **Consequence** | the panel shows the backward phase propagation in the wrong quadrant and with the wrong sign of $k_y$; a reader comparing panel (c) with the corrected §4.15 text ($\vect{k}_B\propto(1,0.529)$) sees a direct contradiction. No number in the paper depends on the drawing. |
| **Proposed correction** | derive all four directions from the stored records instead of literals: $\vect{k}_B$ from $(1,\;k_y/k_{Bx})$, $\vect{P}_B$ from $(P_{Bx},P_{By})$ normalised, $\vect{k}_i$ from $(1,\;k_y/k_{ix})$, $\vect{P}_i$ from $(1,\;P_{iy}/P_{ix})$; draw $\vect{k}_B$ with a length in the solved proportion to $\vect{k}_i$; add a guard called at render time that raises if the wavenumber is not in the first quadrant or departs from the stored direction. Add the wavenumber components to `fig10_field_metrics.json` so the direction has a stored source. |
| **Verification method** | one edge solve reproduced above; regeneration of `fig10_field_metrics.json` only (the field-map CSV must come back byte-identical); render of fig10 to PNG and visual inspection of panel (c); new regression test that fails on a reversed arrow; 47-test suite; `claim_audit`; figure-provenance tests. |
| **Classification** | **CONFIRMED** |

---

## 3. B6 — the `peak_search.py` docstring

| field | content |
|---|---|
| **ID** | B6 |
| **File and location** | `paper_a_study/peak_search.py`, module docstring, lines 28–32 |
| **Existing problem** | "The last one is not a discretisation error, but near a zero-group-velocity fold it **dominates the reproducibility of the printed digits**, so it is measured rather than assumed." The delivered measurement of that same quantity is **0.0**. |
| **Source evidence** | `peak_search.json` → `verdict.tracking_path_relative_spread = 0.0` (round 12 cleared this: ascending, descending and single-step paths return identical $R_B$ and $\omega$); the quantity that *is* $8\times10^{-6}$ is `verdict.restart_spread = 8.3617e-06`, the coarse-raster sampling error. Two different diagnostics, one sentence conflating them. |
| **Consequence** | a reader of the code is told the opposite of what the code's own output shows; a referee reading both would find a contradiction between the docstring and `peak_search.json`. |
| **Proposed correction** | rewrite the paragraph to state that the tracking-path sensitivity is measured independently, that the delivered three-path comparison returned zero spread to the stored precision, and that the larger difference near the fold is coarse-raster sampling, reported separately as `restart_spread`. |
| **Verification method** | diff of the docstring against `peak_search.json` keys; static check; the module is not re-executed (a ~6 min search that no change requires). |
| **Classification** | **CONFIRMED** |

---

## 4. The coupled-fraction configuration in the round-12 correction history

| field | content |
|---|---|
| **ID** | D1 |
| **File and location** | `PAPER_A_ROUND12_CORRECTION_HISTORY.md`, §"Not superseded by this round", and the same sentence copied into `downloads/README.md` |
| **Existing problem** | "… 99.77 % propagating, **62.2973 % at $k_xd=0.55$** …". The value 0.6229733 is `refined_peak.full.R_B`, i.e. $k_xd=0.5275$ with $H/H^{*}=+0.05$. At $k_xd=0.55$ the coupling-on share is 0.5221071. |
| **Source evidence** | `mechanism_controls.json`: `refined_peak.full.R_B = 0.6229733` (16.6545608 GHz, $\theta_E=-27.87^{\circ}$); `refined_peak.no_coupling.R_B = 0.9467952`; `k055_sample.full.R_B = 0.5221071`; `k055_sample.no_coupling.R_B = 0.5791800`. The manuscript itself is correct — `results.tex` §4.10 reads "at the maximum $R_B=0.9468$, $0.7711$, $0.6230$ for $H/H^{*}=0,+0.025,+0.05$" — so this is a report defect, not a manuscript defect. |
| **Consequence** | a reader checking the report against the records finds the number attached to the wrong abscissa; the same error in the download README propagates it to review. |
| **Proposed correction** | attach 62.2973 % to $k_xd=0.5275$ with $H/H^{*}=+0.05$; keep the four configurations distinct in the surrounding text. |
| **Verification method** | re-read of every occurrence of 0.62297 / 62.29 / 0.623 in all reports and in the manuscript; the manuscript occurrences are correct and are not edited. |
| **Classification** | **CONFIRMED** |

---

## 5. fig10 caption

| field | content |
|---|---|
| **ID** | D2 |
| **File and location** | `Paper_A_Final_Submission/sections/results.tex`, fig10 caption and the §4.15 sentence that describes the same panel |
| **Existing problem** | both call panel (c) "a schematic whose arrows are the solved **flux** directions", but two of the four arrows are wavenumbers ($\vect{k}_i$, $\vect{k}_B$). After B1 is corrected, the panel draws four arrows of two kinds and the caption names one kind. |
| **Source evidence** | the plotting code draws $\vect{k}_i,\vect{k}_B,\vect{P}_i,\vect{P}_B$; §4.15's own prose distinguishes the two pairs in three sentences. |
| **Consequence** | a caption that under-describes its own panel; after the arrow correction it would also mis-describe the corrected arrow as a flux. |
| **Proposed correction** | "the solved flux directions" → "the solved wavenumber and flux directions" in the caption and in the sentence that introduces the panel. Two words, no numeric content. |
| **Verification method** | static check; read of §4.15 in context. |
| **Classification** | **CONFIRMED** (minor) |

---

## 6. Other literals in the fig10 schematic

| field | content |
|---|---|
| **ID** | D3 |
| **File and location** | `generate_final_figures.py` lines 894, 896, 897 |
| **Existing problem** | $\vect{k}_i$ is drawn as $(1,0.176)$ and $\vect{P}_B$ as $(-1,-0.530)$, both hardcoded; $\vect{P}_i$ already reads `incident_Py` from the record. |
| **Source evidence** | the solved values are $k_y/k_{ix}=0.1763269807$ and $P_{By}/P_{Bx}=0.5294663538$ — the literals are correct to the precision drawn. |
| **Consequence** | none to the current figure; the values are correct. But three hardcoded numbers in one panel is how B1 happened, and a future change of operating point would silently move two arrows and not the others. |
| **Proposed correction** | derive all four from the record (as in §2). Same drawing to the eye; the numbers now have a source. |
| **Verification method** | the rendered panel must be visually unchanged except for $\vect{k}_B$. |
| **Classification** | **NOT A DEFECT** in the delivered figure; **CONFIRMED** as a maintainability hazard, corrected opportunistically inside B1's scope. |

---

## 7. Items examined and dismissed

| ID | item | finding | classification |
|---|---|---|---|
| N1 | does any *manuscript* sentence attach 0.6230 to $k_xd=0.55$? | no: `results.tex` §4.10 attaches it to "the maximum"; the 0.55 sentences quote 9.85 % and −0.009 % | NOT A DEFECT |
| N2 | is `mechanism_controls`' `operating_point.full` $k_{Bx}=0.2454907$ a contradiction of the figure's 0.2451747? | no: different configurations (coupling on vs off). The figure solve reproduces `operating_point.no_coupling` exactly, which is the manuscript's operating point | DIFFERENT QUANTITY |
| N3 | does round 12's $\vect{k}_B\propto(1,0.529)$ still hold? | yes: 0.5294663538 → 0.529 at the printed precision, angle +27.8997° → 27.9° | ALREADY RESOLVED |
| N4 | is $\lvert\vect{P}_B\rvert$ the same direction ratio as $\lvert\vect{k}_B\rvert$ by accident? | they agree here to $5\times10^{-11}$ in ratio, but they are different physical vectors with different signs; the figure now derives each from its own record rather than from the other | NOT A DEFECT |
| N5 | do the 47 tests currently pass on HEAD? | `Ran 47 tests in 21.450s — OK` (round 12, D.1) | ALREADY RESOLVED |
| N6 | are the ten figure PDFs in the manuscript directory the current renders? | `MANIFEST.json` hashes recompute, and round 11's provenance tests pin the panel map; regenerating fig10 will require re-copying and re-manifesting | ALREADY RESOLVED |
| N7 | has `main` moved? | `origin/main = b7d4606`, the branch point; untouched | ALREADY RESOLVED |

---

## 8. Build environment, checked before the audit is closed

| check | command | result |
|---|---|---|
| engines on PATH | `which pdflatex latexmk xelatex lualatex tectonic tex` | none |
| TeX tree | `ls /usr/share/texlive` | no such directory |
| system package index | `apt-get update` | `E: List directory /var/lib/apt/lists/partial is missing - Acquire (13: Permission denied)`; `sudo -n` available but the index cannot be fetched |
| package mirror reachability | `curl -sI https://deb.debian.org/debian/` | SSL connect error (rc 35) — the host is outside this environment's network policy |
| PyPI for an engine | `pip download tectonic`, `tectonic-bin`, `pytexlive`, `pylatex-tex` | no distribution; `latexmk` 0.0.2 exists but is a 2 KB wrapper around an external binary and ships no engine, no fonts, no packages |
| GitHub release binary | `api.github.com/.../releases/latest` reachable (tectonic 0.17.0, musl asset 10,151,914 B) | the asset download itself fails: `curl -L` returns SSL connect error (rc 35) |
| consequence | — | even a downloaded static engine bootstraps its package bundle from a host outside the allow-list, so no route to a compile exists here |

**Conclusion: BUILD UNVERIFIED — no compiler execution possible.** Report 4 records
the attempts verbatim. No fabricated build.

---

## 9. What this round will and will not change

**Will change:** the four direction literals and the $\vect{k}_B$ arrow in
`generate_final_figures.py`; one field added to `fig10_field_metrics.json`
(wavenumber components, so the direction has a stored source); one regression test;
one docstring; one sentence in the round-12 correction history and in the download
README; two words in the fig10 caption and one in §4.15; the fig10 PDF and PNG;
`MANIFEST.json`; the six round-13 reports; the round-13 archive.

**Will not change:** any equation, constitutive constant, boundary condition, carrier
model, discretisation, solver, tolerance, dataset value, table entry, reported number,
or the other nine figures. The field-map CSV must come back byte-identical, which is
the evidence that the plotted science is untouched.

**Will not close:** B2 (novelty, `UNRESOLVED`), B3 (corner line force), B4 (build,
unverified), B5 (author declarations).
