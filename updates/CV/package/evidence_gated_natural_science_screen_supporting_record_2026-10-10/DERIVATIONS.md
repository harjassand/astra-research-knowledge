# Independent physical checks

Date: 2026-10-10 UTC. These are derived constraints, not measurements of a new natural mechanism. Inputs and source status are pinned in `SOURCES.md`.

## 1. Faradaic and energy budget for the dark-oxygen electrolysis hypothesis

For water electrolysis,

`2 H2O -> 2 H2 + O2`

The oxygen-evolution half-reaction transfers four electrons per O2 molecule. Charge conservation therefore gives `Q = 4 F n(O2)`, and the ideal product ratio is `n(H2) / n(O2) = 2`. The reversible electrical work at standard conditions is `W_min = 4 F E_rev`; with `F = 96,485.33212 C mol-1` and `E_rev = 1.23 V`, this is `474.7 kJ per mol O2`.

The 2024 paper reports DOP fluxes of 1.7–18 mmol O2 m-2 d-1. If all of that O2 were produced by water electrolysis, the required current density would be

`j = 4 F r(O2) = 7.6–80.4 mA m-2`.

At 1.23 V this implies a reversible-limit power density of 9.3–98.9 mW m-2; using the paper's stated 1.23 V plus 0.37 V overpotential gives 12.2–128.6 mW m-2. For one reported 484 cm2 chamber footprint, the corresponding current is about 0.37–3.89 mA. The requirement is meaningful only if the reported O2 flux is real and is produced by water splitting; it is not a measurement of actual nodule current.

The paper reports local platinum-probe potential differences up to 0.95 V and says water oxidation at the site requires 1.23 V plus about 0.37 V overpotential. If 0.95 V were the complete loaded cell voltage, it would provide at most 77% of the reversible minimum and about 59% of the stated operating voltage. It is an open-circuit potential measured on recovered nodules with probes at selected positions, not a loaded voltage across an identified electrolysis circuit. Multiple internal redox couples, reaction at unmeasured sites, or another chemical pathway cannot be assessed without a full electron and energy inventory.

The primary paper reports neither integrated charge/current nor hydrogen production, and it identifies the energy source as unresolved. Thus the published record does not close the specified Faradaic test. The direct single-cell, water-splitting interpretation is incompatible with the reported potential if that potential is treated as the full cell voltage; the broader “geo-battery” hypothesis remains untested rather than disproven by this calculation. No alternative oxygen source is inferred.

Reproduction: `python3 dark_oxygen_budget.py` emits the results in `dark_oxygen_budget.json`. It uses only the constants and flux range listed above. No raw data were downloaded or reprocessed.

## 2. Conditional inner-core restoring and heat scales

The 2026 paper's waveform simulations classify ICB topography `h >= 1.5 km` over lateral scales `lambda = 1–30 km` as compatible with waveform dissimilarity; this is a model compatibility threshold, not a direct topography measurement. Its reported change-rate scale is 0.1–1 km/yr. A PREM density jump of 0.60 g cm-3 and ICB gravity about 4.4 m s-2 imply a simple buoyancy-pressure scale

`p_g ~ Delta_rho g h ~ 4 MPa`.

That is roughly 50,000 times the paper's reference magnetic stress of 80 Pa (`B0 deltaB / mu0`, for 10 mT fields). This comparison flags a missing force-balance term under the assumed relief geometry; it is not by itself a strict force balance because the vector orientation, finite geometry, phase-boundary kinetics, and rheology are not measured.

If a 1.5 km relief change is literal phase-boundary motion, the required latent-heat flux is `q_L = rho L h_dot`. With conditional values `rho = 1.2e4 kg m-3`, `L = 0.75 MJ kg-1` and the paper's 0.1–1 km/yr rate, `q_L` is about `2.9e4–2.9e5 W m-2`. This is a local energy scale; it does not rule out chemical partitioning or advective energy transport, but those would need a separate budget.

The primary waveform data were not obtained, and the paper itself states that coverage cannot locate exact scatterers or exclude changing scatterers below the ICB. No prospective waveform result was computed. The physical-scale checks therefore do not identify a cause.
