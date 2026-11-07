# Paper A — round 12 edit ledger

One row per substantive edit, with the before and after text, the evidence it rests
on, and exactly one category. Categories used in this round:

* **MATHEMATICAL CORRECTNESS** — a displayed statement, symbol or count is wrong.
* **NUMERICAL CONSISTENCY** — the prose disagrees with the delivered records.
* **EVIDENCE TRACEABILITY** — the prose asserts something the delivered records do
  not contain.
* **NOTATION** — one symbol, two meanings.
* **LANGUAGE** — wording, without a change of content.
* **SUBMISSION-LEVEL** — text a journal or a referee requires to be accurate.

Counts: 19 edits — 2 MATHEMATICAL CORRECTNESS, 10 NUMERICAL CONSISTENCY,
2 EVIDENCE TRACEABILITY, 4 NOTATION, 1 LANGUAGE (recorded jointly as
SUBMISSION-LEVEL).
No edit changes a governing equation, a constitutive constant, a boundary
condition, the solver, a dataset, a figure PDF or a numerical result.

Baseline `75d86dc9710d69e2100a85fa5c8b56e9681f7744`. Evidence paths are relative to
`paper_a_study/figure_data/`.

---

## L12-01 — phase-speed endpoints were attached to the wrong wavenumbers

| | |
|---|---|
| File | `sections/results.tex` §3.1 |
| Before | "decreases monotonically from \SI{105.8}{\kilo\metre\per\second} at $k_xd=1.05$ to \SI{20.0}{\kilo\metre\per\second} near the cutoff" |
| After | "decreases monotonically from \SI{105.8}{\kilo\metre\per\second} near the cutoff at $k_xd=0.15$ to \SI{20.0}{\kilo\metre\per\second} at $k_xd=1.05$" |
| Evidence | `fig01_dispersion_velocity_attenuation.csv`, $\eta=0$: `phase_speed_m_s` = 105 771 at $k_xd=0.15$ and 20 038 at $k_xd=1.05$ |
| Category | NUMERICAL CONSISTENCY |

The two values were right and their abscissae were transposed, so the sentence
described the phase speed as decreasing towards the cutoff when it increases
towards it.

## L12-02 — the linewidth and attenuation descriptions of fig01

| | |
|---|---|
| File | `sections/results.tex` §3.1 |
| Before | "grows monotonically with $k_xd$, with a clear ordering in $H$. The attenuation … ranges from \SI{0.23}{\deci\bel\per\milli\metre} to \SI{456}{\deci\bel\per\milli\metre}, peaks sharply at $k_xd\approx0.52$ and is positive everywhere" |
| After | linewidth "is smallest at $H=0$ and rises with $|H|$, further for positive than for negative coupling"; attenuation "is largest on the slow part of the branch, but the plotted grid of $\Delta k_xd=0.03$ resolves that maximum only at its own sample, $k_xd=0.54$: the fold itself carries \SI{87.2}{\deci\bel\per\milli\metre} at $H=0$ (\cref{tab:configurations}), which a raster of that spacing cannot show" |
| Evidence | `fig01…csv` linewidth at $k_xd=1.05$: 0.266 MHz ($\eta=+0.05$), 0.144 ($-0.05$), 0.0853 ($+0.025$), 0.0242 ($-0.025$), 0.0047 (0) — monotone in $H$ only up to sign asymmetry. Attenuation maximum over the $\eta=+0.05$ column: 455.7 dB/mm at the sample $k_xd=0.54$; the three tabulated configurations give 87.2 dB/mm at $k_xd=0.5275$ (`peak_certification.json`, case `refined_peak`, incident attenuation) |
| Category | NUMERICAL CONSISTENCY |

There is no ordering in $H$ at fixed wavenumber: the curve order is
$0 < -0.025 < +0.025 < -0.05 < +0.05$. Panel (d) cannot resolve the fold peak
either, because its grid steps over 0.5275 by 0.03; the prose now says so and
points to the table that does resolve it.

## L12-03 — thickness family described as a single abscissa

| | |
|---|---|
| File | `sections/results.tex` §3.3 |
| Before | "between \SI{120}{\nano\metre} and \SI{320}{\nano\metre} the branch moves from \SI{30.4}{\giga\hertz} to \SI{10.5}{\giga\hertz}" |
| After | "across the family between \SI{120}{\nano\metre} and \SI{320}{\nano\metre} the branch lies between \SI{10.5}{\giga\hertz} and \SI{30.4}{\giga\hertz}" |
| Evidence | `fig03_geometry_sweep.csv`: $d=120$ nm spans 28.34–30.43 GHz, $d=320$ nm spans 10.46–10.74 GHz, so 30.4 and 10.5 are the two ends of the *family*, not of one curve |
| Category | NUMERICAL CONSISTENCY |

## L12-04 — gradient-length percentages quoted at abscissae the grid does not contain

| | |
|---|---|
| File | `sections/results.tex` §3.3 |
| Before | "\SI{+2.0}{\percent} at $k_xd=0.15$ and … \SI{+10.2}{\percent} at $k_xd=1.05$" |
| After | "at $k_xd=0.145$ and … at $k_xd=1.00$" |
| Evidence | `fig03…csv` $k_xd$ grid is 0.100, 0.145, …, 1.000; the quoted percentages (+2.05, +10.21 for $\ell=90$; −1.93, −4.93 for $\ell=35$) are the values at 0.145 and 1.000 |
| Category | NUMERICAL CONSISTENCY |

Round 11 had moved this sentence from 0.1/1.05 to 0.15/1.05; the grid contains
neither 0.15 nor 1.05.

## L12-05 — density and mobility factors were three times too large

| | |
|---|---|
| File | `sections/results.tex` §3.4 |
| Before | "raises the linewidth (a) and the attenuation (b) by roughly a factor of nine and a factor of ten respectively"; "the linewidth changes by a factor of about five" |
| After | "by a factor of three each --- the conduction loss is linear in the density over this range ---"; "by the same factor of three"; plus "The two sweeps are in fact identical row by row, because the density and the mobility enter the conduction term only through their product." |
| Evidence | `fig02_material_parameter_sweep.csv`: at every $k_xd$, $n_0=1\times10^{18}$ → 3×10¹⁸ gives 0.00084 → 0.00251 MHz and 0.244 → 0.732 dB/mm (factor 3.0); the $\mu$ sweep reproduces the same column values to all stored digits |
| Category | NUMERICAL CONSISTENCY |

## L12-06 — "reflectance" used for the backward share, and the tail of panel (c)

| | |
|---|---|
| File | `sections/results.tex` §3.4 |
| Before | "while the reflectance is unchanged to the same $0.2$ per cent"; "falls to $10^{-7}$ there [at $k_xd=0.9$]" |
| After | "while the backward share is unchanged to the same $0.2$ per cent"; "falling below $10^{-7}$ beyond $k_xd=0.8$ and reaching $1.6\times10^{-11}$ at the last sample" |
| Evidence | `fig02…csv`: $R_B=3.04\times10^{-7}$ at 0.80, $5.07\times10^{-10}$ at 0.85, $1.55\times10^{-11}$ at 0.90 |
| Category | NOTATION |

$R_B$ is the backward modal share; the paper reserves the word "reflectance" for
the total outgoing fraction it explicitly declines to claim, and the abstract and
the captions already say so. The tail value at the last sample is four orders below
the number printed before.

## L12-07 — precision of the printed digits rested on an untraceable pair of numbers

| | |
|---|---|
| File | `sections/results.tex` §3.5 |
| Before | "One sensitivity sets the precision of the printed digits. … a relative change of $1.8\times10^{-12}$ in the frequency moves $R_B$ by $5.6\times10^{-6}$. The maximum is therefore reproducible to about $\pm6\times10^{-6}$" |
| After | "The precision of the printed digits is set by the spreads of \cref{tab:refinement} … the degree-22 value changes by $6.2\times10^{-9}$ between degrees 14 and 34, the quadrature rule changes it by $4.3\times10^{-10}$, and the three tracking paths … return the identical number. The difference between the located argmax and the reported sample, $1.4\times10^{-7}$, is three orders of magnitude smaller than the \SI{0.01}{} percentage point over which the top is flat" |
| Evidence | `peak_search.json` `verdict.degree_spread["0.52750"] = 6.220088e-09`, `verdict.quadrature_spread = 4.317e-10`, `verdict.tracking_path_relative_spread = 0.0`, `classification.offset_reported_vs_argmax = 1.372e-07`. The removed pair has no stored source and is contradicted by direct evaluation — `PAPER_A_ROUND12_NUMERICAL_TRACEABILITY_AUDIT.md` §5 |
| Category | EVIDENCE TRACEABILITY |

## L12-08 — the argmax/reported-sample difference was called "below the reproducibility of the frequency map"

| | |
|---|---|
| File | `sections/results.tex` §3.6 |
| Before | "$1.4\times10^{-7}$ lower, which is below the reproducibility of the frequency map" |
| After | "$1.4\times10^{-7}$ lower --- a difference between two abscissae, not between two runs" |
| Evidence | as L12-07: the two values are individually reproducible to $10^{-9}$; their difference is a property of the two wavenumbers |
| Category | EVIDENCE TRACEABILITY |

## L12-09 — the energy budget closure numbers

| | |
|---|---|
| File | `sections/results.tex` §3.6 |
| Before | "As rounded, these four numbers close to $1.4\times10^{-6}$; evaluated at full precision the identity closes to $1.9\times10^{-17}$, and the computed power balance to $6.6\times10^{-13}$ … the interference term … which sums to $0.99769$ … the same identity closes to $3.0\times10^{-13}$" |
| After | "The first two sum to $0.999797$ … adding the dissipation and the interference correction leaves $0.9999917$, short of unity by $8.3\times10^{-6}$, which is twice the interference term, because the outgoing shares are quoted as magnitudes while the interference term is signed. The identity itself closes to $3.4\times10^{-16}$ relative — the stored residual of the budget — and the computed power balance to $7.3\times10^{-13}$ … which together account for $0.99769$ … The same power balance closes there to $3.2\times10^{-13}$" |
| Evidence | `fig05_channel_power.csv` row $\eta=0$: `closure_residual` = 3.4468e−16, `power_balance_error` = 7.3071e−13, `cross_interference_fraction` = −4.1692e−6 (twice which is 8.34e−6, the arithmetic deficit of the four printed numbers); `peak_certification.json` case `refined_peak`, degree 22: `balance` = 3.206e−13 |
| Category | NUMERICAL CONSISTENCY |

Three of the five numbers printed before are not in any delivered record
($1.4\times10^{-6}$, $1.9\times10^{-17}$, $6.6\times10^{-13}$), and the sentence
"which sums to $0.99769$" attached the propagating total to a four-term sum that
gives 0.99542. The replacement states what the four printed numbers actually add
up to and why the deficit is twice the interference term, which is a property of the
reporting convention and not of the solution.

## L12-10 — distance from the edge was written $\ell$, the symbol for the gradient length

| | |
|---|---|
| File | `sections/results.tex` §3.9 |
| Before | "decays with the observation distance (panel a) as $\exp(-\alpha_B\ell)$ … the minimum … is $0.0356$ at $\ell=\SI{1000}{\micro\metre}$" |
| After | "decays with the observation distance $L$ (panel a) as $\exp(-\alpha_B L)$ … at $L=\SI{1000}{\micro\metre}$, a millimetre from the edge" |
| Evidence | the frozen panel uses $L$ (`distance from the edge  $L$ ($\mu$m)` in `generate_final_figures.py`); $\ell$ is 50 nm in the same article and is the gradient length throughout |
| Category | NOTATION |

Round 11 fixed this collision in the figure labels; the prose kept it.

## L12-11 — "falls by a factor of three" contradicted "a factor of sixty-two" in the same sentence

| | |
|---|---|
| File | `sections/results.tex` §3.9 |
| Before | "is largest at $H=0$ ($\approx\SI{18}{\milli\metre}$) and falls by a factor of three at the extremes of the coupling range, and the loss coefficient follows" |
| After | "falls by more than an order of magnitude at either extreme of the coupling range --- to \SI{0.54}{\milli\metre} at $H/H^{*}=-0.05$ and to \SI{0.30}{\milli\metre} at $+0.05$ ---" |
| Evidence | `fig06_attenuation_distance.csv`: `attenuation_length_incident_mm` = 18.5 at $H=0$, 0.538 at −0.05, 0.300 at +0.05 |
| Category | NUMERICAL CONSISTENCY |

## L12-12 — the fig06 caption used $L$ for the attenuation length

| | |
|---|---|
| File | `sections/results.tex`, caption of `fig:fig06` |
| Before | "(c) attenuation length $L$ and (d) loss coefficient $\alpha$" |
| After | "(c) attenuation length and (d) loss coefficient $\alpha_i$ (incident) and $\alpha_B$ (backward)" |
| Evidence | the frozen panel legends are `$\alpha_i$ incident` and `$\alpha_B$ backward`; $L$ is now used, in the same paragraph, for the distance from the edge |
| Category | NOTATION |

## L12-13 — "six to seven orders below the $10^{-8}$ tolerance" was attached to the wrong quantity

| | |
|---|---|
| File | `sections/results.tex` §3.11 |
| Before | "the residual stays at $3\times10^{-15}$ and the energy-balance error between $2\times10^{-13}$ and $1\times10^{-12}$, six to seven orders below the $10^{-8}$ tolerance and two to three orders below the $10^{-10}$ tolerance drawn in the panel" |
| After | "the residual stays at $3\times10^{-15}$, six to seven orders below the $10^{-8}$ tolerance drawn in the panel, and the energy-balance error stays between $2\times10^{-15}$ and $4\times10^{-12}$, one to five orders below the $10^{-10}$ line. Both are round-off in a relative measure, and the panel is there to show that neither drifts with the degree" |
| Evidence | `fig09_validation_convergence.csv` `power_error` over the seven degrees: 2.40e−13, 3.98e−12, 9.90e−13, 7.31e−13, 4.14e−12, 2.41e−15, 6.40e−13 — a range of 2.4e−15…4.1e−12, not 2e−13…1e−12; `edge_scaled_residual` 2.66e−15…3.28e−15, i.e. 6.5 decades below 1e−8. Panel (c) of the frozen figure draws both the 1e−8 and the 1e−10 lines |
| Category | NUMERICAL CONSISTENCY |

## L12-14 — the backward wavenumber vector of fig10(c)

| | |
|---|---|
| File | `sections/results.tex` §3.12 |
| Before | "$\vect{k}_i\propto(1,0.176)$, $\vect{k}_B\propto(0.333,-0.530)$, $\vect{P}_i\propto(1,0.176)$ and $\vect{P}_B\propto(-1,-0.530)$, taken from the computed flux" |
| After | "The two wavenumbers point into the plate, $\vect{k}_i\propto(1,0.176)$ and $\vect{k}_B\propto(1,0.529)$, because $k_y$ is positive and both axial wavenumbers are real and positive. The incident flux follows its wavenumber, $\vect{P}_i\propto(1,0.176)$, whereas the backward flux is $\vect{P}_B\propto(-1,-0.529)$" |
| Evidence | `peak_identity_audit.json` case `operating_point`: `K_backward = [0.2451747, −5.23e−06]` with $k_yd=0.1298118$, so $\vect{k}_B\propto(1, 0.1298118/0.2451747) = (1,0.5295)$; `fig10_field_metrics.json` `primary_flux`: $P_{Bx}=-0.015425$, $P_{By}=-0.008167$ → $\vect{P}_B\propto(-1,-0.5295)$ |
| Category | MATHEMATICAL CORRECTNESS |

The old vector $(0.333,-0.530)$ is neither a direction nor a ratio of the same two
components: 0.333 is $K_{Bx}/K_{ix}$ while 0.530 is $|k_y|/K_{Bx}$, and its sign is
the sign of the *flux*, not of the wavenumber. The direction it encodes
($-58^{\circ}$ from $+x$) is not the direction of any solved vector; the solved
wavenumber points at $+27.9^{\circ}$. The same wrong vector is drawn in the frozen
panel (c) — **B1** in `PAPER_A_ROUND12_BLOCKING_ISSUES.md`.

## L12-15 — "three-term polynomial" for a quartic

| | |
|---|---|
| File | `sections/numerical_methods.tex` §3.1 |
| Before | "assembled as a three-term polynomial in the propagation wavenumber $k_x$" |
| After | "assembled as a polynomial of degree four in the propagation wavenumber $k_x$"; the following sentence now reads "That degree is the order of the hyperelastic operator" |
| Evidence | the displayed expansion $\sum_{r=0}^{2}\sum_{s=0}^{2}(-\ii k_x)^r(\ii k_x)^s \mathsf{A}_{rs}$ carries the powers 0…4, i.e. five coefficients; the same section calls it "the quartic problem" |
| Category | MATHEMATICAL CORRECTNESS |

## L12-16 — $\alpha$ carried two meanings, and the dissipation integral was written in scaled variables without saying so

| | |
|---|---|
| File | `sections/governing_equations.tex` §2.7, `tab:groups` |
| Before | "$P_{\text{diss}}=\tfrac12\alpha\iint[(k_x^2+k_y^2)|\widetilde\mu|^2+|\partial_z\widetilde\mu|^2]\dd z$, $\alpha=D/(d\,c_s)$"; `tab:groups` row "$\alpha$" |
| After | the same integral with $\alpha_{\mathrm{d}}=D/(d\,c_s)$, followed by "written in the scaled variables of \cref{sec:governing_nondim} … and it is the conduction loss inside the control volume. The symbol $\alpha$ itself is used later for the spatial attenuation $2|\Imag k_x|$ of a mode (\cref{sec:numerics})"; `tab:groups` row "$\alpha_{\mathrm{d}}$" |
| Evidence | the solver's `diss` is `0.5*alpha*Σ w[(|kx|²+ky²)|μ|²+|∂zμ|²]` with dimensionless $\mu$ and $\alpha$ (`model.py`, `mode_diagnostics`/`temporal_energy_balance`), so the displayed integral is the scaled one; $\alpha=2|\Imag k_x|$ is used six times in §3 and §4 and appears in the frozen fig06 legends |
| Category | NOTATION |

The identity $\eqref{eq:energy_identity}$ is stated in physical units, so an
integral that is not was a latent dimension error. Nothing in the equation or the
computation changed; the text now says which variables it is written in. The
diffusion ratio keeps its value, its meaning and its place in the five groups.

## L12-17 — "Five limitations" introduced six

| | |
|---|---|
| File | `sections/discussion.tex` §5.5 |
| Before | "Five limitations bound the conclusions" |
| After | "Six limitations bound the conclusions" |
| Evidence | the six paragraphs that follow: Geometry, The corner, The carrier model, The parameters, The electrical condition, The constitutive relation |
| Category | NUMERICAL CONSISTENCY |

## L12-18 — the reproduction appendix under-counted the package

| | |
|---|---|
| File | `sections/appendix_reproducibility.tex` |
| Before | "the 39 automated checks"; "an automated suite of 39 tests"; "39 tests, ~9 s"; "the twelve data files behind the figures" |
| After | "the 47 automated checks"; "an automated suite of 47 tests"; "47 tests, ~25 s"; "the eleven data files behind the figures" |
| Evidence | `python -m unittest paper_a_study.test_model` → `Ran 47 tests in 22.911s … OK`; `ls paper_a_study/figure_data/*.csv` → 11 files |
| Category | NUMERICAL CONSISTENCY |

## L12-19 — abstract: "the figure", and an unqualified "unchanged"

| | |
|---|---|
| File | `main.tex`, abstract |
| Before | "The figure is a modal share of the scattered power and not a reflectance"; "Removing the coupling leaves the partition unchanged, so the conversion belongs to the strain-gradient branch; at its tabulated extreme it lowers the share by \SI{1.21}{\percent}…, chiefly by attenuating the backward mode" |
| After | "The reported number is a modal share of the scattered power and not a reflectance"; "Removing the added coupling leaves the partition almost unchanged, so the conversion belongs to the strain-gradient branch; at its tabulated extreme the coupling lowers the share by \SI{1.21}{\percent}…, chiefly by attenuating the two partner modes" |
| Evidence | "the figure" has no antecedent in the abstract; the removal moves the share by 1.21 %, so "unchanged" needed its qualifier; §3.7 attributes the reduction to the attenuation of both partner modes |
| Category | LANGUAGE (SUBMISSION-LEVEL) |

---

## Edits considered and rejected

| candidate | why not |
|---|---|
| Replace the six occurrences of "reflectance" that contrast with $R_B$ | they are the disclaimer, not a misuse; removing them would strengthen the very claim the paper avoids |
| Rewrite §2 to shorten the constitutive derivation | the derivation is load-bearing for the added term's symmetry, and no defect was found in it |
| Update the "~15 min" battery estimate in the appendix | the round-11 log records 18 gates in about 13 min of wall time; the printed figure is a bound, and no measured number contradicts it |
| Change the four-decimal frequencies in `tab:configurations` | they agree with the stored values; the rounding is at the last printed digit |
| Renumber sections or move tables | out of scope for an editorial round with a frozen numerical content |
| Adjust fig01(d) or fig10(c) | figures are frozen this round; both are reported (B1, and §3.1 of the section review) |
