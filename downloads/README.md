# Downloads

## Round 16 (current)

**`Paper_A_Complete_Project_round16.zip`** — 259 entries · 3,199,292 bytes
· SHA-256 `d848d387b07c59f1a7c98772cc6d10f239c82e98e312a50412c75daef1649dbb`

https://github.com/vipin-oss/A_Paper/raw/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round16.zip

Round 16 asked one question: is the carrier weak equation printed in the manuscript
equivalent to the carrier operator the code assembles? It is not, and the defect is in
the manuscript.

- **Carrier sign (class A).** `eq:weak_carrier` printed `− iα_d/ω ∂_iμ̃ ∂_iΦ*`; the
  correct sign is `+`. Derived from the implemented balance (dimensional continuity →
  `e^{−iωt}` → nondimensionalisation → one integration by parts with `J_z = 0`), then
  confirmed against an independent 200-node assembly of the carrier row to
  **4.2 × 10⁻¹⁴** (degree 4) and **9.7 × 10⁻¹⁴** (degree 6), with `H ≠ 0` so the
  carrier–strain-gradient column is exercised. The two candidate signs differ by
  7.8 × 10¹ in operator norm. Third confirmation: the repaired sign gives
  `Im ω < 0` and `P_diss ≥ 0` equal to `eq:dissipation`; the printed sign gives growth.
- **Continuity equation (class B).** `q ∂_t Δn + ∂_i J_i = 0` with `J_i` a *number*
  flux is dimensionally impossible (C·m⁻³s⁻¹ vs m⁻³s⁻¹). The `q` was removed, and the
  charge balance is now given explicitly as the same equation times `−q`.
- **Gauss's law (class B).** the mobile charge in `eq:weak_gauss` needs the
  dimensionless charge `Q = d/L_D = 0.0746349`; the assembled φ–µ block reproduces
  `−Q ∫ψ_i b_j` to 3.7 × 10⁻¹⁶ and the φ–φ block carries the `Q²` screening to
  1.1 × 10⁻¹⁷. Only the coefficient was wrong, not the sign.

No solver line, constant, boundary condition, dataset, figure or reported number
changed. The implemented row equals minus the repaired weak form — a row operation on a
homogeneous system, so no eigenvalue moves.

Verification: `unzip -t` clean; `MANIFEST.json` 80 files; `scripts/static_check.py`
passes inside the extracted tree (112 labels, 86 references, 13/13 citations, 17021
words); 52 tests OK; claim audit PASS; 15 mutants all caught; phase-speed audit PASS;
round-16 audit script exit 0 with its log inside the archive. The manuscript is **not
compiled** here — no TeX engine exists in this environment — so typeset output is
**BUILD UNVERIFIED**.

Read first: `PAPER_A_ROUND16_SUPERVISOR_DECISION.md`, then the four audit reports and
the reproducible log `PAPER_A_ROUND16_AUDIT_LOG.txt`.

## Earlier rounds

Rounds 8–15 remain in this directory with their own zips; round 15
(`Paper_A_Complete_Project_round15.zip`, 251 entries · 3,169,750 bytes · SHA-256
`25318374679c8ac679ff510bee9c248937f7ef9a6a1429c949a3b24bca90b3d4`) is the immediate
predecessor and remains the reference for the figure-5/8 repair, the three separated
weak forms and the nomenclature audit.
