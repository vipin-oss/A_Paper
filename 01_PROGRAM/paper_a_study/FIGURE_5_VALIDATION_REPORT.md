# Paper A Figure 5 scientific validation report

Date: 2026-11-06

Figure: `fig05_channel` — Reflection-channel conversion and modal energy

Dataset: `paper_a_study/figure_data/fig05_channel_power.csv`


## Valid H cases

- Number of valid matched H cases: 5

- Plotted H/H* values: [-0.05, -0.025, 0.0, 0.025, 0.05]

- All five cases are finite, matched at the same fixed drive, geometry, normalization, and 2 μm reference plane.


## Plotted values and relative change

| H/H* | R_B absolute (%) | Relative change vs H=0 (%) | R_B degree uncertainty (abs.) |
|---:|---:|---:|---:|
| -0.050 | 2.286447 | -1.214706 | 0.000005803 |
| -0.025 | 2.310126 | -0.191650 | 0.000005860 |
| 0.000 | 2.314562 | 0.000000 | 0.000005871 |
| 0.025 | 2.299642 | -0.644601 | 0.000005835 |
| 0.050 | 2.265750 | -2.108886 | 0.000005753 |

- H=0 relative-change limit: exact zero by construction.

- Maximum observed relative change: -2.108886% at H/H*=0.050.

- Maximum degree-refinement uncertainty in absolute R_B: 5.871e-06 percentage points; in relative terms 2.536e-04%.


## Definitions checked

- `R_B` is the isolated backward-channel self-power ratio from the full edge solve, not total reflectance.

- Total outgoing fraction is the sum of finite absolute outgoing self-powers normalized by the finite incident self-power; interference is retained analytically in the full edge power balance.

- Propagating and evanescent components are separated by `|Im K|`; evanescent values are local modal self-power fractions, not far-field transported power.


## Final panel arrangement

- (a) Absolute isolated backward-channel return with H=0 degree-refinement uncertainty marker.

- (b) Relative coupling-induced change with respect to H=0.

- (c) Total outgoing self-power fraction.

- (d) Propagating and evanescent outgoing self-power fractions.


## Validation outcome

- Figure audit: 36/36 checks passed; Figure 5 passes all four checks.

- No governing equations, material, coupling definition, boundary conditions, or research objective were changed.

- No negative values were converted to absolute values to pass checks.


## Generated files

- `fig05_channel.pdf`: 35921 bytes, sha256=77618ae7152fe8de197d63b910c47d281e3d86d32a9fbb0e28f690e1d948b01d
- `fig05_channel.png`: 593320 bytes, sha256=2c451b0c7a10b2ddaaa34bda408cd36e431cbb04a917976c98fdc6004121669f
- `fig05_channel.svg`: 84708 bytes, sha256=04dd82f981e108e79afe975d18df3dc0a7ed21df8448e531fb5441a764455574
- `fig05_channel_power.csv`: 1252 bytes, sha256=07e0cbeaff18176f611c6be01d594b8513908520bff1506c9d97f88e3b5349c2
