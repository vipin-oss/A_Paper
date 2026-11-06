# Paper A — Round 8: convergence, controls and the bound on the claim

Every number in this report was recomputed this round. Sources: `peak_certification.json`,
`peak_search.json`, `mechanism_controls.json`, `corner_assessment.json`, `convergence_audit.json`,
`quadrature_audit.json`.

---

## 1. Discretisation: the value does not move

**Degree (degree 14 → 34, six settings).** At the reported wavenumber the spread is 6.2 × 10⁻⁹ of the
value; at the located argmax 5.6 × 10⁻⁹. At the operating point, degree 18 → 30, the largest successive
change is 7.2 × 10⁻⁷. Both are far below the fourth significant figure that is quoted.

| case | R_B (n = 30) | max successive relative change, n = 18 → 30 |
|---|---|---|
| operating point | 0.023145624 | 7.2 × 10⁻⁷ |
| certified maximum | 0.946795230 | 1.7 × 10⁻⁹ |
| earlier 0.5250 sample | 0.931891486 | 2.1 × 10⁻⁸ |
| k_x d = 0.55 | 0.579180059 | 1.5 × 10⁻⁷ |

**Quadrature (Gauss–Legendre 64, 128, 192, 256).** At a fixed basis (degree 22) the spread is
9.4 × 10⁻¹⁰; at degree 30 with 64 and 256 nodes it is the same order. The rules are not the limiting
error.

**Tracking path.** Reaching k_x d = 0.5275 in 31 steps from below, 31 steps from above, and in one step
gives the same R_B bit for bit (spread 0.0). The eigenvalue-tracking step is therefore not influencing the
answer.

**Restarts.** Two independent 10⁻³ restarts from [0.520, 0.532] and [0.524, 0.536] return the same
bracket and the same sample (8.4 × 10⁻⁶ below the refined maximum). This tests bracketing only.

**Frequency map.** The branch is stored on a 1.8 × 10⁻¹²-relative frequency grid; that granularity maps to
±6 × 10⁻⁶ in R_B, which is two orders of magnitude *larger* than the degree and quadrature spreads, and is
therefore the quoted reproducibility of the headline.

## 2. Coupling sweep at the certified maximum (branch-consistent)

ε = ±H/H* at fixed k_x d = 0.5275, everything else at the full model:

| ε | R_B | change | edge-plane share | change | Im k_Bx |
|---|---|---|---|---|---|
| +0.050 | 0.622973 | −34.20 % | 0.876125 | −11.11 % | −8.531 × 10⁻³ |
| +0.025 | 0.771091 | −18.56 % | 0.933223 | −5.31 % | −4.771 × 10⁻³ |
| 0 | 0.946795 | — | 0.985572 | — | −1.003 × 10⁻³ |
| −0.025 | 0.863553 | −8.79 % | 0.962736 | −2.32 % | −2.721 × 10⁻³ |
| −0.050 | 0.700570 | −26.01 % | 0.907656 | −7.91 % | −6.486 × 10⁻³ |

Two readings, both reported in the paper:

1. the change is **asymmetric** in sign(ε) — a larger |ε| does not mean a larger loss;
2. at the reference plane the loss is 34.2 %, at the edge plane 11.1 %: the remaining 23.1 points are
   attenuation of the backward mode between the edge and the plane. The two figures are never compared
   with each other; they are reported side by side with the plane named.

## 3. Re-optimised peak at each coupling level

The coupling need not merely lower the value at a fixed wavenumber; it can also move the extremum. Each
level was re-searched from scratch (coarse 10⁻³ over [0.518, 0.538], then 10⁻⁴):

| ε | located k_x d | R_B |
|---|---|---|
| +0.050 | 0.5218 | 0.624389 |
| +0.025 | 0.5248 | 0.771453 |
| 0 | 0.5275 | 0.946795 |
| −0.025 | 0.5261 | 0.863645 |
| −0.050 | 0.5309 | 0.701315 |

The ceiling falls from 0.9468 to 0.6244 / 0.7013 at the two extremes, and the displacement is **not
monotone in sign(ε)**: +0.05 moves the extremum down by 0.0057, −0.05 moves it up by 0.0034, +0.025 down
by 0.0027, −0.025 up by 0.0014. Fixed-baseline and re-optimised comparisons are kept in separate columns
in the manuscript and are never mixed in one sentence.

## 4. Matched controls at the peak and on the flank

| model | peak (0.5275) | flank (0.55) |
|---|---|---|
| full (ε = +0.05) | 0.622973 | 0.522107 |
| no flexoelectricity | 0.622971 | 0.522153 |
| no carrier coupling (H = 0) | 0.946795 | 0.579180 |
| no flexoelectricity, H = 0 | 0.946801 | 0.579245 |
| classical (ℓ = f = H = 0) | 0.134050 | 0.125061 |

* Removing the **strain-gradient sector** removes the backward branch altogether: the classical model has
  no backward port at this k_y, and its largest admissible outgoing share is 13.4 % — a different
  scattering problem, flagged `no_backward_port`, not a smaller version of the same one.
* Removing the **flexoelectric term** changes R_B in the fifth significant figure at both points.
* Removing the **carrier coupling** at the peak changes the share by 34.2 % — but only through the extra
  attenuation of the backward mode; the branch and hence the possibility of the conversion is supplied by
  the strain-gradient sector alone.

## 5. Corner band and degree drift (the limitation that survives)

At every configuration the corner band (the outer 20 % of the thickness, where the double tractions are
enforced) carries:

| case | corner share of the strain-gradient energy | peak/mean inside the band | drift, n = 18 → 30 |
|---|---|---|---|
| operating point | 0.93 – 1.00 % | 0.098 – 0.102 | −6.8 % |
| certified maximum | 1.22 – 1.30 % | 0.125 – 0.130 | −6.6 % |
| k_x d = 0.55 | 1.18 – 1.26 % | 0.122 – 0.126 | −6.6 % |

The share is **below** the mean everywhere (peak/mean < 1), so the band is not an energy sink, and it
*decreases* with degree instead of growing, which is what a spurious boundary layer would not do. The
6.6–6.8 % drift is nonetheless a real residual: the corner-line boundary condition is **not certified**,
and the paper says so in the abstract and in the limitations. No number in this paper depends on the
corner band to better than the third digit.

The certification cross-check (`corner_assessment.py`) passes: the stored corner values agree with
`peak_certification.json` row by row (difference 0.0).

## 6. What the claim is bounded by

| bound | magnitude | where stated |
|---|---|---|
| local, not global, maximum | window 0.465–0.625 at one k_y | abstract, results, conclusions |
| flat top | ±9 × 10⁻⁴ in k_x d | results |
| reproducibility | ±6 × 10⁻⁶ in R_B | results |
| discretisation | 6 × 10⁻⁹ (degree), 9 × 10⁻¹⁰ (quadrature) | results, appendix |
| corner line | not certified | abstract, limitations |
| transported power at the fold | factor 128 below the operating point | abstract, results, discussion, conclusions |
| material set | synthetic (ℓ, f, H) | abstract, limitations |

**No experimental accuracy is claimed anywhere in this paper. The residuals quoted (10⁻¹³ – 10⁻¹⁶) are
numerical residuals of a linear solve, and the manuscript now says so wherever it quotes them.**
