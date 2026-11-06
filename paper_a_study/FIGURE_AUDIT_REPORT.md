# Paper A figure-wise audit

Date: 2026-11-06

## fig01_dispersion
Status: **PASS** (3/3)

| Check | Result | Evidence |
|---|---|---|
| attenuation nonzero | PASS | min=4.036e+02 max=8.418e+04 |
| pdf text present | PASS | 430 chars |
| all panels labeled | PASS | a,b,c,d present |

Evidence: attenuation range 4.036e+02-8.418e+04 dB/m; zero-attenuation defect checked.

## fig02_material
Status: **PASS** (4/4)

| Check | Result | Evidence |
|---|---|---|
| attenuation nonzero | PASS | min=2.220e+02 max=1.894e+03 |
| R_B finite | PASS | min=-61.504694 max=3.540764 |
| pdf text present | PASS | 352 chars |
| all panels labeled | PASS | a,b,c,d present |

Evidence: R_B range -61.504694-3.540764; material sweep rows 150.

## fig03_geometry
Status: **PASS** (3/3)

| Check | Result | Evidence |
|---|---|---|
| data finite | PASS | 230 rows |
| pdf text present | PASS | 320 chars |
| all panels labeled | PASS | a,b,c,d present |

Evidence: 230 geometry rows; dispersion and gradient-length panels present.

## fig04_frequency
Status: **PASS** (3/3)

| Check | Result | Evidence |
|---|---|---|
| R_B positive | PASS | min=7.660e-08 max=1.742e-01 |
| pdf text present | PASS | 475 chars |
| all panels labeled | PASS | a,b,c,d present |

Evidence: R_B at 2 um range 7.660e-08-1.742e-01; frequency panels present.

## fig05_channel
Status: **PASS** (4/4)

| Check | Result | Evidence |
|---|---|---|
| H values present | PASS | [-0.05, -0.025, 0.0, 0.025, 0.05] |
| R_B positive | PASS | [0.022864467939464526, 0.023101260643054032, 0.023145619204273885, 0.02299642239541999, 0.0226575044141918] |
| pdf text present | PASS | 384 chars |
| all panels labeled | PASS | a,b,c,d present |

Evidence: R_B range 0.022658-0.023146; modal-power columns present.

## fig06_attenuation
Status: **PASS** (5/5)

| Check | Result | Evidence |
|---|---|---|
| incident attenuation length positive | PASS | min=2.999e-01 max=1.851e+01 |
| backward attenuation length positive | PASS | min=2.301e-01 max=1.912e+01 |
| incident survival finite | PASS | max=28.060 |
| pdf text present | PASS | 488 chars |
| all panels labeled | PASS | a,b,c,d present |

Evidence: incident attenuation length 2.999e-01-1.851e+01 mm; backward attenuation length 2.301e-01-1.912e+01 mm.

## fig07_coupling
Status: **PASS** (3/3)

| Check | Result | Evidence |
|---|---|---|
| R_B positive | PASS | min=1.303e-02 max=1.926e-02 |
| pdf text present | PASS | 479 chars |
| all panels labeled | PASS | a,b,c,d present |

Evidence: R_B edge range 1.303e-02-1.926e-02; coupling grid rows 95.

## fig08_boundary
Status: **PASS** (4/4)

| Check | Result | Evidence |
|---|---|---|
| both boundaries | PASS | ['ground', 'open'] |
| R_B nonnegative | PASS | [0.017040275921443155, 0.03260976462690671, 0.03250070484054633] |
| pdf text present | PASS | 379 chars |
| all panels labeled | PASS | a,b,c,d present |

Evidence: ground and open boundary rows present; R_B range 0.017040-0.032610.

## fig09_validation
Status: **PASS** (3/3)

| Check | Result | Evidence |
|---|---|---|
| data finite | PASS | 9 rows |
| pdf text present | PASS | 402 chars |
| all panels labeled | PASS | a,b,c,d present |

Evidence: 9 convergence rows; residual and power-error panels present.

## fig10_field
Status: **PASS** (4/4)

| Check | Result | Evidence |
|---|---|---|
| two planes | PASS | 2 planes |
| centroids finite | PASS | [-7.867235290621322e-07, -2.0891013992957306e-05] |
| pdf text present | PASS | 844 chars |
| all panels labeled | PASS | a,b,c,d present |

Evidence: two field planes; backward centroid y [-7.867235290621322e-07, -2.0891013992957306e-05].

