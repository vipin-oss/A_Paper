# A0-S evidence and access ledger

Date: 2026-11-05. This is a bounded source audit, not a broad novelty review.

## 1. Primary low-density transport evidence

M. Suscavage et al., **High Quality Hydrothermal ZnO Crystals** (1999), DOI [10.1557/S109257830000260X](https://link.springer.com/article/10.1557/S109257830000260X). Primary HTML inspected in chunks 0–2.

- The light-green, high-resistivity hydrothermal sector has room-temperature **electron concentration about 2 × 10¹² cm⁻³ = 2 × 10¹⁸ m⁻³** and **Hall mobility about 175 cm² V⁻¹ s⁻¹ = 0.0175 m² V⁻¹ s⁻¹**, from temperature-dependent Hall measurements.
- The dark-green sector's much higher density is a different sector. No density from one sector is paired with another sector's mobility.
- A donor fit gives an approximately 0.34 eV donor, ND ≈ 7 × 10¹⁵ cm⁻³ and NA ≈ 10¹⁵ cm⁻³. These defect concentrations are **not** the free-electron concentration used in drift–diffusion.
- The experiment concerns **bulk crystals / c-plane slices**, with growth-sector, face and surface-preparation effects. It is not a demonstration of a released, uniformly doped 200–1000 nm plate.
- The journal year is **1999**; the host's 2020 posting date must not be mistaken for the experimental publication year.

**Assumptions, not observations:** Hall factor unity / Hall-to-drift transfer; frequency-independent local mobility; post-thinning retention of n and mobility; homogeneous fixed-charge background; applicability of the retained isothermal linear transport model. The exact Hall measurement temperature is not jointly calibrated to the model temperature.

**Derived diffusion coefficient:** D = M × 0.026 V = 0.000455 m² s⁻¹. This preserves the retained Einstein ratio, corresponding to an effective T ≈ 301.717 K. D was not measured by this primary source. Approximate room-temperature transfer is not exact same-sample temperature calibration.

## 2. Retained literature-model constants

Zhang et al., *Applied Mathematics and Mechanics* 46(7), 1331–1346 (2025), DOI [10.1007/s10483-025-3272-7](https://www.amm.shu.edu.cn/article/2025/0253-4827/0253-4827-2025-07-1331.shtml). Table 1, governing equations and Appendix A previously inspected; the carrier/thickness discussion rechecked for A0-S.

- Retain `a0/materials.json`: printed-precision elastic, piezoelectric, dielectric and density constants; M = 0.01 m² V⁻¹ s⁻¹ and D = 0.00026 m² s⁻¹.
- n0 = 10¹⁹ m⁻³ appears in the source's modelling figures. **This is a literature-model operating input, not a joint measurement on our candidate plate.**
- That paper's 3 μm total-thickness plate and D3 = J3 = 0 face closure are not the same experiment or electrostatic exterior as our vacuum problem.
- The source attributes constants to a book; underlying same-specimen measurements and uncertainty covariance remain unaudited. No measured f, A or H is supplied for this checkpoint.

## 3. Thickness evidence has a limited role

The 200, 500 and 1000 nm values are **design thicknesses**. They are not invented measurements. The small grid tests the disclosed observation that the existing fixed physical synthetic length ℓ = 50 nm becomes significant at d = 200 nm; it is not an optimization over unpublished carrier densities.

Search-level primary abstract / secondary descriptions of S.-S. Lin and J.-L. Huang, *Effect of thickness on the structural and optical properties of ZnO films by rf magnetron sputtering*, *Surface and Coatings Technology* 185, 222–227 (2004), DOI [10.1016/j.surfcoat.2003.11.014](https://doi.org/10.1016/j.surfcoat.2003.11.014), concern submicron c-axis-textured/polycrystalline supported films. A secondary description, DOI [10.3390/cryst12040528](https://doi.org/10.3390/cryst12040528), describes a 200–600 nm film range. **Full primary experimental text was not obtained in this bounded check.** These descriptions support an order-of-magnitude processing scale only; they do not establish a released, homogeneous single-crystal 6mm plate, the required electrical faces, or the same n/M pair. The 1 μm upper design value bridges the retained A0-R reference.

Search hits describing a 120 nm SiN membrane and 100 nm sacrificial ZnO were rejected as evidence of a free 100 nm ZnO plate. Composites, wires and supported heterostructures were not relabelled as our geometry.

## 4. H calibration: not obtained

*Strain Gradient Modulated Exciton Evolution and Emission in ZnO Fibers*, *Scientific Reports* 7, 40658 (2017), DOI [10.1038/srep40658](https://www.nature.com/articles/srep40658), primary chunks 0 and 4 inspected after one bounded coefficient query.

The reported strain-gradient-dependent exciton evolution / luminescence, optical band-gap gradients and piezoelectric-field explanation are **not a measurement of the electron-number chemical-potential coefficient H_jkl** in `Δn H_jkl ε_jk,l`. Exciton and optical energies were not divided by a strain gradient to manufacture H. No new exciton field or deformation-potential coupling was introduced. A defensible physical H range remains **null**.

The existing ℓ = 50 nm and A = ℓ² C ⊗ I remain **synthetic**. Stability-normalized H values are also synthetic; stability does not imply physical plausibility. f = 0 is an explicitly incomplete control limit, not a measured vanishing flexoelectric response or a change to the full-model objective.

## 5. Qu: one legitimate bounded recheck, still unresolved

Y. Qu, E. Pan, F. Zhu and Q. Deng, *A thermodynamically consistent theory for flexoelectronics: Interaction between strain gradient and electric current in flexoelectric semiconductors*, *International Journal of Engineering Science* 208, 104165 (2025), DOI [10.1016/j.ijengsci.2024.104165](https://doi.org/10.1016/j.ijengsci.2024.104165).

A0-S performed one fresh repository-targeted query: `"Qu" "104165" "repository" flexoelectronics Appendix`. It did not expose the primary Appendix C equations. The previously unsuccessful publisher/PDF/API routes and completed connected-file searches were **not repeatedly retried**. Their outcomes are retained in `PAPER_A_A0R_NOVELTY_COMPARISON.md` and `a0r/protocol.json`.

**NOVELTY UNRESOLVED.** The proposed coupling's absence, equivalence, novelty, or special-case relationship to Qu has not been established. The consequential primary-equation comparison must await legitimate access; no content was reconstructed from the title or citing-paper snippets.

## 6. Universal constants and source boundaries

q, kB and ε0 retain the earlier NIST provenance in `a0/materials.json`. The vacuum light speed c = 299792458 m s⁻¹ is exact by the SI definition. It is used only for a conservative light-line / exponent diagnostic, not to turn the quasistatic model into a solved Maxwell radiation problem.

No publisher PDF, private paper, large dataset, fitted empirical coefficient, new carrier concentration, or measured uncertainty interval was fabricated. The complete numeric screen and all ordinary-parameter/H probes must be read with these provenance distinctions.
