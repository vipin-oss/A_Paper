# Downloads

## Round 15 (current)

**`Paper_A_Complete_Project_round15.zip`** — 251 entries · 3,169,750 bytes
· SHA-256 `25318374679c8ac679ff510bee9c248937f7ef9a6a1429c949a3b24bca90b3d4`

https://github.com/vipin-oss/A_Paper/raw/arena/ea7ca4dd-a-paper/downloads/Paper_A_Complete_Project_round15.zip

Round 15 verified the round-14 mathematics independently and repaired what did not
survive that check:

- the strain-gradient variation is a **contraction** identity (`τ:δη = τ:δu_jk`),
  not the component identity that round 14 printed;
- the single "weak form" is now three honest ones — mechanical, Gauss with the
  mobile charge restored, and carrier continuity — plus the assembled block system;
- the quartic operator now states that `A02 = A20 = 0` identically and carries its
  Hermitian structure;
- `α` no longer denotes two things (`α_d` for the transport group), and the
  nomenclature table's five-column/four-cell defect is fixed;
- Figures 5 and 8 were inspected at reading size and repaired, with the five-level
  coincidence in Fig. 8 stated and measured.

No constant, boundary condition, solver, dataset or reported number changed.
Verification: `unzip -t` clean; `MANIFEST.json` 80 files; `scripts/static_check.py`
passes inside the extracted tree. The manuscript is **not compiled** here — no TeX
engine exists in this environment — so typeset output is **BUILD UNVERIFIED**.

## Earlier rounds

Rounds 8–14 remain in this directory with their own zips; round 14
(`Paper_A_Complete_Project_round14.zip`, SHA-256
`ccab4e57dbbac1067f2bf4a64355ba27f872aa6000cf6f0939c20760e49237c1`) is the
immediate predecessor.
