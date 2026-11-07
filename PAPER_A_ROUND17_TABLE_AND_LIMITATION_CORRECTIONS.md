# Paper A — Round 17 table, vocabulary and limitation corrections (Parts A, F, G, H, J)

**Branch** `arena/ea7ca4dd-a-paper` · base `a68bb76` · BUILD UNVERIFIED.

---

## 1. Tables: what was removed, what was kept

| Table | Action | Reason |
|---|---|---|
| `tab:units` | **removed** | duplicated units that the constitutive derivatives now give in prose; it made `τ` and `H` read as list items |
| `tab:conjugates` | **removed** | four rows = the four relations `eq:sigma`, `eq:tau`, `eq:D`, `eq:mu`; the unit column moved into the same prose paragraph. Its one cross-reference now points at `eq:sector_blocks` |
| `tab:novelty` | **removed** | it carried a `Status` column with `UNRESOLVED` / `ABSENT` / `ABSENT BY SCOPE` entries — audit vocabulary in a manuscript table. The comparison itself is preserved as prose (see §2) |
| `tab:groups` | kept | genuinely numerical: five groups, definitions, values, meaning |
| `tab:provenance` | kept, restated | factual: parameter, value with provenance, source. "Synthetic" is used as a plain statement about `ℓ`, `f`, `H`, not as a status code |
| `tab:refinement` | kept | numerical (degree refinement) |
| `tab:configurations` | kept | numerical (sweep configurations) |
| `tab:controls` | kept | numerical (control cases) |

Table count 8 → 5. No table was created to hold content removed from another.

## 2. Vocabulary: what was removed from the manuscript

`static_check.py` and a manual grep over `Paper_A_Final_Submission/sections/*.tex`
were both used. Current state: **zero** occurrences of `UNRESOLVED`, `ABSENT`,
`AUDIT`, `VERIFIED`, `PASS`, `FAIL`, `BLOCKED`, `TEST GATE`, `status` as a column
header.

The `tab:novelty` comparison survives as prose in `sec:disc_literature`, in the
form a reader of the paper needs:

* the added term `Δn H_jkl ε_jk,l` is **not** claimed as new;
* the formulations compared "already contain a flexoelectric coupling of strain
  gradients to the electric field, and the carrier density enters them through
  the free energy of the electron gas";
* the comparison "is made against the equations that could be inspected, and the
  full text of the 2025 reference was not among them; the question of whether
  that formulation already contains a term of this structure therefore remains
  open here";

so the uncertainty is stated in the paper in scientific language while the
status-column machinery is gone. **The unresolved prior-art question is recorded
in full in the internal round-16 audit material**
(`PAPER_A_ROUND16_*`, `PAPER_A_ROUND16_AUDIT_LOG.txt`), not in the manuscript.

Also reworded, because they read as validation reportage rather than as science:

* `numerical_methods.tex`: heading "Verification" → **"Consistency and independent
  checks"**; opening "The implementation is verified in five independent ways" →
  "The implementation is checked in five independent ways, each of which compares
  a computed quantity with a closed-form or independently discretised one";
* the reciprocity sentence "which verifies the symmetry of the discretised
  bilinear form" → "which exposes the symmetry of the discretised bilinear form";
* `results.tex` fig08 caption: "the local flux is reported as computed and was not
  independently validated" → "plotted as evaluated; no independent measurement
  constrains the through-thickness distribution".
* No test counts, no script names, no archive hashes, no development history, and
  no round numbers appear anywhere in the manuscript.

## 3. Limitations: six paragraphs → five numbered points

The discussion ended with six `\paragraph` limitations, two of which
("Geometry" and "The corner") contradicted each other in tone: the first argued
that the corner band carries 1 % of the gradient energy and that the share
*decreases* under refinement, the second conceded that this does not bound the
work of a corner line force. Both facts are true, and neither is now allowed to
shadow the other. The section is now:

1. **Geometry** — 2.5D, one edge, no corner resolution, no second edge.
2. **The corner** — the band evidence, quoted with its numbers (0.93–1.00 % at
   the operating point, 1.22–1.30 % at the maximum, 1.18–1.26 % at `k_xd = 0.55`;
   peak-to-mean 0.098–0.102, 0.126–0.130, 0.122–0.126, i.e. *below* the mean;
   share *decreasing* by 6.8 %, 6.6 %, 6.6 % between degree 18 and 30; degree
   spread 7.2×10⁻⁷ and 1.5×10⁻⁷), then the caveat in the same breath: this
   "is evidence about the energy and not a proof that the corner line force is
   dynamically negligible", because a small band fraction bounds the energy near
   the corner in the computed field but not the work a singular traction could do
   on admissible variations the basis cannot represent. **The line force is not
   called harmless anywhere in the paper.**
3. **The carrier model and the electrical condition** — linearisation about
   uniform doping; the open-circuit gauge removes a null space but does not make
   the open-circuit results independent.
4. **The parameters** — bulk constants, representative transport parameters,
   synthetic `ℓ, f, H`; percentages are model responses, not predictions.
5. **The constitutive attribution** — relation to published
   flexoelectric–semiconductor formulations remains open; no priority claimed.

Five points, at the end of the Discussion, no legal-style disclaimer, each
attached to the place in the model where it bites.

## 4. Numeric typography (`siunitx`)

The preamble had

```
group-separator={,}, group-minimum-digits=4
```

with `siunitx`'s default `group-digits=all`, which groups the *fractional* part
as well, so `16.6547` could set with a comma. It is now

```
group-digits=integer, group-minimum-digits=5,
output-decimal-marker={.}, group-separator={\,}
```

so only the integer part is grouped, only from five digits, the decimal marker is
pinned to a period, and the thousands separator (where it appears) is a thin
space rather than a comma — which is also what a reader of `\SI{1.6e-21}` expects
next to `10^{4}`. The change is in `main.tex` and is commented there.

## 5. Unverifiable consequences

* Whether the removed tables were referenced from the figures' captions in a way
  `\cref` now cannot resolve: the static check reports no undefined reference, so
  all remaining `\cref` targets exist.
* Whether the five-point list fits on one page with the preceding discussion:
  unknown without an engine.
* Whether `siunitx` accepts `output-decimal-marker={.}` in the installed version
  (v2 and v3 both do; only v1 does not).
