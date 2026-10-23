# Recuperator wall and surface-reaction feasibility checkpoint

Date: 2026-10-21. Scope: literature evidence plus algebra on the existing gas-model results. No new material, hardware campaign, spending, or outreach. No new coupled simulation.

## Decision

The favorable continuous counterflow gas model is not yet a physically qualified recuperator. The failed premise is an unqualified, effectively zero-resistance, chemically inert separating wall at the temperatures demanded by the coupled profiles. This is not a proof that all ceramic heat recovery fails.

The best long-duration, actual recuperator-wall evidence located is SiC at 1375 °C (1648 K) for 12–15 months. A current manufacturer's dense gas-tight sintered-SiC tube rating extends to 1650 °C (1923 K), but does not specify corresponding lifetime, 1 mm channels, or concentrated NO service. These are different evidence levels, not universal ceramic temperature ceilings.

The saved model's necessary wall-temperature bounds are 1937 K for the 1800 K handover with a 1 mm finite-front quench, 2072 K for the original 1800 K/20 mm case, and 2637–2653 K for the 2400 K/20 mm cases. Thus even the lowest candidate lies above the cited SiC use rating. The hottest cases also exceed alumina's melting point, not just a recommended service temperature. Zirconia remains a physically meaningful material family, but no matched thin, gas-tight, continuous separator-wall temperature/lifetime qualification was found.

## Actual apparatus evidence

1. Penty and Bjerklie, 1982, low-pressure industrial SiC recuperators: tubes demonstrated 12–15 months at an explicitly stated material temperature of 1375 °C. This is stronger evidence than quoting a furnace gas temperature. https://doi.org/10.1002/9780470318140.ch10

2. Saint-Gobain tube brochure: HEXOLOY SE sintered SiC is rated to 1650 °C in air; open-ended tubes are described as dense and gas-tight. Standard examples are millimetre-thick, millimetre-to-centimetre bore tubes, not this 1 mm-channel core. This is manufacturer use data, not a documented endurance experiment for the proposed duty. https://www.ceramicsrefractories.saint-gobain.com/sites/hps-mac3-cma-pcr/files/2023-04/speciality-ceramics-ceramic-tubes-thermocouple-sensor-brochure-2021-web-2028665.pdf

3. Fox, 1998: pure CVD SiC and Si3N4 were exposed for 100 h in dry flowing oxygen between 1200 and 1600 °C. Oxide was adherent through 1550 °C; 1600 °C produced silica spallation. This is relevant oxidation evidence, but is not a lifetime ceiling for all commercial SiC grades. https://doi.org/10.1111/j.1151-2916.1998.tb02431.x

4. NASA TN D-1598, 1963: the Langley 11-inch tunnel used an actual zirconia pebble-bed air heater at approximately 4500 °R = 2500 K. The bed used 3/8-inch spheres. Propane/oxygen-enriched-air combustion heated the bed; the burner was then isolated and compressed air flowed oppositely through it. Typical test flow lasted 60 s, extendable to 120 s, with 1–3 h reheating afterward and about 24 h from cold start. This is direct-contact cyclic regeneration, not simultaneous heat conduction across a gas-tight partition. The report measured only 7 psi compressive strength at 4460 °R = 2478 K for its particular refractory and deliberately reduced temperature with bed depth to manage load. Dust contamination was a stated limitation. https://ntrs.nasa.gov/api/citations/19630003222/downloads/19630003222.pdf

5. NASA's 1964 comparative material test provides a stronger boundary than melting points: successful air-heater operation near 4100 °F = 2533 K was considered only marginally acceptable, requiring appreciable annual maintenance and low velocities to limit zirconia dust. Calcia-stabilized materials lost static-load capacity sharply; recommended hot-zone loadings were only about 4–6 psi. Fully stabilized and partially stabilized products differed in thermal shock, inversion stability, and load capability. These results concern the tested historical refractory grades, not every modern dense zirconia. Alumina/magnesia contact with zirconia caused reactions below their individual maximum temperatures. https://ntrs.nasa.gov/api/citations/19640020188/downloads/19640020188.pdf

6. NIST's validated high-purity sintered-alumina compilation gives melting at 2050 ± 4 °C (2323 K), and explicitly documents high-temperature creep. Thermal conductivity is 6.23 W/(m K) at 1500 °C, not its much larger room-temperature value. It would be unjustified to assign this value unchanged to a much hotter wall, or infer a device lifetime from melting point. https://srdata.nist.gov/CeramicDataPortal/Pds/Scdaos

## Surface NO destruction: measured evidence, not an automatic veto

AVCO's 1974 measurements used 19.05 mm alumina pebbles, 99.5% purity, 3% porosity, in combustion gas. High-temperature inlet bed temperatures were 3050/3500 °F (1950/2200 K), with inlet NO about 0.50/0.78%. Geometric outer-area-normalized rates were 6.6/7.0 × 10^-9 mol/(cm² s). The high-temperature area denominator included bed surface estimated above 1000 K. The gas O2/redox composition is not sufficiently specified to reproduce dry air/NO conditions. The authors also reported negligible practical catalysis for magnesia and zirconia pebbles, without a transferable detection-limit bound. Therefore neither universal inertness nor inevitable catastrophic NO loss follows.

Source: Hals, Gannon and Kivel, SEAM 14 (1974), Tables IV–V, printed pp. II.3.6–7. https://edx.netl.doe.gov/storage/f/edx/2021/05/2021-05-20T05%3A54%3A25.768Z/5de6b860-fb30-4977-82a6-be759031afdf/id550_1974_f-a-hals_auxiliary-component-development-work-at-avco-everett-research-laboratory-inc.pdf

### Algebraic conversion, clearly conditional

For round channels, wall area / mass flow = 4 L/(D G). At L = 0.02 m, D = 0.001 m and G = 1 kg/(m² s), this is 80 m² s/kg. Applying the measured 7.0 × 10^-5 mol/(m² s) uniformly gives 0.0056 mol NO lost/kg, about 0.36% of the low-temperature candidate's retained NOx. This is a borrowed-flux sensitivity, not an upper bound at different gas composition, porosity, temperatures, or radical content.

The finite-front 1800 K candidate starts at 1.43496 MJ/mol. Holding thermal duty fixed, the borrowed loss changes it to 1.44018 MJ/mol. With perfect heater and capture and no auxiliaries, the complete loss allowance for a 1.5 MJ/mol target is 4.336%; uniform geometric-area NO flux must then be below 8.37 × 10^-4 mol/(m² s). These budget numbers come from the model, not measured performance. Including the borrowed loss raises the required product of heater efficiency and capture fraction to about 0.9601. There is almost no practical margin for the rest of the process.

For an effective first-order wall sink j = k_eff C_NO, the fixed-profile attenuation is exp[-k_eff (4/D) τ]. Integrating the saved hot-temperature profile with nominal molecular-air density gives τ ≈ 6.733 ms and k_eff ≤ 1.646 × 10^-3 m/s for that perfect-efficiency loss budget. Residence and this coefficient are approximate because complete hot-species profiles were not saved. The geometric constant-flux conversion does not require the density approximation. None of these algebraic screens includes chemistry/temperature feedback from surface reactions.

### Radical recombination is a separate boundary condition

Experiments on sintered zirconia measured atomic-oxygen recombination between 900 and 2500 K at 200 Pa air pressure, with phase-dependent behaviour. This establishes that zirconia cannot simply be declared noncatalytic to radicals; it does not supply a 1 atm NO-destruction coefficient. Surface radical removal can change homogeneous NO chemistry in either direction, while recombination heat changes wall heat flux. A correct model needs separate O/N recombination and NO surface pathways with their own applicability ranges. https://doi.org/10.1016/j.matchemphys.2010.03.059

NASA TN D-2878, 1965, also discusses alumina's surface-mediated NO decomposition and explicitly distinguishes it from homogeneous reactions. Its pressure/concentration regime differs from the current concept. Report number verified from the downloaded title page. https://ntrs.nasa.gov/api/citations/19650016997/downloads/19650016997.pdf

## Construction condition and next mechanism

Small pressure difference makes pressure stress easier, but cannot provide missing thermal-shock, creep, sealing, interdiffusion, or catalysis evidence. Any tube/monolith proposal must specify a real thickness and measured k(T), use R_wall = t/k(T) (or the cylindrical equivalent), allow expansion, keep unsuitable joints out of the hot zone, and demonstrate compatible hot-zone surface behaviour. No architecture meeting all of these requirements at the present temperature profiles was established here. A maximum-use label is insufficient qualification.

The supported alternative mechanism is direct-contact regenerative storage, because an actual zirconia bed operated in air near 2500 K without a thin separating wall. It still requires a closed periodic material/energy balance, reset/reheat accounting, switching and purge/entrainment accounting, finite solid conductivity and heat capacity, mechanical loading/thermal cycles, pressure drop, and chemistry on the actual exposed area. The cited apparatus is evidence that this mechanism exists, not evidence that the proposed NO process gains an efficiency advantage.

## Reproducibility and limits

surface_screen.py reproduces the algebra from the parent's saved counterflow.json and finite_quench.json. surface_screen.json records source-file hashes and case-level results. Downloaded NASA/AVCO primary PDFs and extracted text are in sources/. The 1974 table scan was visually checked. This checkpoint neither validates the original gas kinetics nor changes any baseline simulation. The unresolved blocker is matched materials/geometry/surface evidence, not lack of a speculative material choice.

### Layout-specific clarification for the proposed two-bed next operation

The cited Langley apparatus is one reusable bed, not merely a single-use experiment, but each air-test discharge was followed by a separately fuel-fired recharge. Heating products travelled down; test air travelled up after switching/isolation. It demonstrates reversible gas/solid heat exchange and material cycling, not a paired-bed system with a fixed central electric heater, cold-end-only reversal valves, continuous NO generation, or net recuperation across a periodic process. AVCO likewise reports cyclic, separately fuel-fired regenerative air heating, not the proposed two-bed NO synthesis loop. Those references therefore support the existence of the direct-contact unit operation, while leaving the proposed complete topology and closed cycle unestablished.

## Receiving composition correction
The initial algebraic screen also iterated raw shooting rows that later failed the
boundary/energy gate. The reported lower-case example used a valid row and is
unchanged, but those failed rows must not feed further design decisions.
The original source/result are preserved as surface_screen_initial_ungated.*.
The current surface_screen.py explicitly filters boundary, energy, mass and
positivity failures, and its cheap saved-data algebra was rerun. It does not rerun
a gas trajectory. Use the gated surface_screen.json for subsequent reuse.
