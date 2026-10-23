# Expansion-quench evidence and actual wall-quench comparator

21 October 2026 UTC. Source inspection and algebra only. No new chemical/flow trajectory, no spending, no outreach. The parked lamella/packed-bed programs and retired engines were not reopened.

## Decision

1. A nozzle's low static temperature is not completed cooling. Primary aerodynamic-quench experiments explicitly require heat extraction during the supersonic section before shock/deceleration; otherwise the static temperature rises again. Expansion can buy chemical time, but is not itself a total-enthalpy sink or free pressure restoration.
2. A real dry N2/O2 wall-quench comparator exists: Van Alphen et al.'s 2022 effusion nozzle. Its experimental result is useful and considerably stronger than an imposed instantaneous-quench boundary. However, the gas divider partially melted; the CFD then omitted it. This apparatus is NOT an admitted intact-material, full-reset comparator for the saved 2700 K, 79/21-air contract.
3. At 80/20 N2/O2 and 2 L/min, the raw triplicates show about 3.37% higher total NO+NO2 with the nozzle and 22.58% lower discharge-energy cost. This is not an isolated retention measurement: power, arc anchoring and complete upstream state change. The controlled equal-power comparison is modeling, not experiment.
4. Gross room-side heat-rejection area is not the obvious barrier at this laboratory power. The known exhaust collector can in principle reject the approximately159 W discharge load without a high average outside temperature. That does not establish low local divider temperature. The observed melt shows that an average heat/area argument alone misses the load-bearing local constraint.

## Primary sources and archived receipts

A. S. Van Alphen et al., Chemical Engineering Journal 443 (2022),136529, DOI https://doi.org/10.1016/j.cej.2022.136529 . Peer-reviewed author manuscript archived at https://repository.uantwerpen.be/docstore/d%3Airua%3A12367 . Saved as 2022_effusion_author.pdf/.txt. Publisher-layout version was read through https://orbi.umons.ac.be/bitstream/20.500.12907/44435/1/1-s2.0-S1385894722020241-main.pdf ; direct file download returned503, so no local publisher-layout PDF is claimed.

A-SI. Author-hosted Supporting Information: https://medialibrary.uantwerpen.be/files/7783/31c2c67d-42b6-4b48-b443-f4a3d1b1b703.pdf . Saved as 2022_effusion_si.pdf/.txt. Some formulas are genuinely blank in this hosted PDF, verified by rendering, not merely lost in text extraction. Numeric tables and the melt statement are legible. The SI byline differs from final-journal metadata; treat this as the retrieved author-hosted supplement, not independently certified byte-identical to the publisher supplement. Key statements also agree with the author's later thesis chapter4, locally archived for corroboration.

B. M.B.Colket III et al., Nitric Oxide Measurement Study, Volume II: Probe Methods (May1980), FAA-EE-80-29/EPA-460/3-80-014/NASA CR-159862. Official full report: https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=9100XLYM.TXT . Saved HTML and extracted text.

C. T.Rakel and K.Schaber, Rapid quenching by supersonic expansion and injection of water, Chemical Engineering Science66(2011),1622–1630, DOI https://doi.org/10.1016/j.ces.2010.12.027 . Publisher abstract/introduction: https://www.sciencedirect.com/science/article/abs/pii/S0009250910007402 . This is a gasdynamic hardware cross-check, not dry nitrogen-fixation evidence. Its stated cooling magnitude exceeds10^6K/s; avoiding downstream reheating required evaporation in the supersonic region. Water injection violates the unchanged dry-gas contract unless water, separation and reset are charged. No NO-retention number is borrowed from it.

## 2022 apparatus: what was actually measured

The main paper uses high-purity N2 and O2, a1mm tangential inlet, a nickel cathode, stainless anode/body and a ceramic cathode enclosure. The central experiment is a2L/min feed referenced at1atm,293.15K. Wider parameter scans cover1–10L/min,60–200mA and N2/O2 ratios0.25–4. Atmospheric-pressure operation is reported; no measured pressure-drop map or upstream compressor duty was found.

The nozzle's six radial0.8mm holes force the gas against the steel and redirect it; it is a heat-sink geometry, not a demonstrated Laval expansion. Fig.2 dimensions are OD18.90mm, bore15mm, drawn cavity21.50mm and8mm rear steel wall. Their sum is29.50mm; prose calling the cavity29.5mm is ambiguous. The gas divider is1mm wide,2mm high and15mm long. The nozzle is enclosed in a stainless exhaust collector of25mm diameter and295mm length. SI uses25.2mm outside diameter for exterior convection. Rendered dimension receipt: nozzle_dimensions.png.

At80/20 dry feed, source Table2 reports3.88±0.01% NOx at159W with nozzle, versus3.77±0.02% at199W without. The main table's equal159W no-nozzle entry is explicitly simulated:2.76%, versus3.30% simulated with nozzle. The simulation underpredicts measured nozzle yield. It cannot establish an exact retention fraction of the real hot gas.

Raw SI TablesS.2/S.4 triplicate arithmetic means are:
- With: 158.913 W; NO = 2.260%; NO2 = 1.62667%; sum = 3.88667%; EC = 2.94385 MJ/mol using the paper's equation.
- Without: 198.583 W; NO = 2.28333%; NO2 = 1.47667%; sum = 3.760%; EC = 3.80266 MJ/mol.
Arithmetic means are a transparent reanalysis, not a claim to reproduce the authors' weighting. Source and recomputation are preserved unchanged in 2022_effusion_table_audit.json and 2022_effusion_audit_summary.json; audit_effusion_tables.py reproduces them.

The ratio gives+3.37% totalNOx and−22.58% discharge EC. NO alone slightly falls: the total increase is mostly observed NO2. This is why the observable must remain NO+NO2, not NO alone. Source2.1MJ/mol is a different1.5L/min,50/50 operating point, not the dry-air point, nor simultaneous with the5.9% headline concentration.

No deliberately controlled equal-power experimental comparison was found in the recovered manuscript or SI. Nearby powers among different replicate points are not a controlled equal-state experiment. The same nozzle also changes arc attachment/ignition and power needed to sustain the discharge.

## Measurement and electrical boundary

NO and NO2 are measured separately with an Emerson-Rosemount X-STREAM analyzer. Main text names NDIR plus UV; the retrieved SI describes NDIR and shows separate calibration curves. SI uses nitrogen zero gas, span calibration and calibration curves, and sample flow980–1000sccm. It reports lower sample flow can overestimate concentration and high flow can create cell-pressure error. No complete downstream NOx mass-closure or sample-line-loss budget was found. Pure conversion NO→NO2 preserves the requested count; losses to walls/condensation or other NxOy would not. Thus changes in NO:NO2 ratio are not proof of lost fixed nitrogen, but totalNOx should not be treated as fully certified end-to-end mass closure.

Energy cost is discharge averageVI divided by totalNOx production, using24L/mol. It excludes an explicitly itemized whole-plant supply/compression/cooling/reset balance. The setup has a25kΩ ballast plus a distinct25Ω current-measurement resistor. If the listed135mA is mean series-circuit current, Jensen's inequality gives ballast dissipation≥R Imean²=455.625W. This is a conditional circuit lower bound, not measured wall-plug power; the current convention and circuit waveform need confirmation before assigning an exact total. It cannot be erased by reporting discharge power alone.

Two printed SI EC values fail the same paper's equation by much more than rounding:158.41W/3.90%/2Lmin gives2.92449 rather than2.51MJ/mol;112.98W/2.51%/2Lmin gives3.24086 rather than2.23. This limited audit is preserved; no corrected source data or hidden fitting was introduced.

## Thermal and material admission

SI p.32 explicitly records partial melting of the gas divider and removal of that divider from CFD geometry. Screenshot: si_melted_divider.png. This is direct evidence against treating the original geometry as unchanged cyclic equipment. It is not evidence that every wall-quench design must fail.

A65-minute50/50,2L/min experiment reaches a stableNOx concentration within30s. This rules out only the simplest interpretation that the displayed product is a fleeting initial cold-wall signal. It does not certify unchanged steel, corrosion resistance, no material expenditure or thermal-cycle reset. No lifetime test was found.

The model uses oxidized304 material properties, exterior emissivity0.8, ambient293.15K, free convection and radiation. SI expressly says no forced exterior airflow. Its exterior convection correlation uses room-temperature air properties and tabulates h(T). Cylinder h at500/600/1000K is18.56/20.61/25.86Wm−2K−1. There is no reported integrated wall heat export and no numerical maximum steel temperature in the recovered main/SI. Core gas maxima4615/5129K in Fig.6 are not steel temperatures. The coarse blue steel map cannot validate the missing local, partially melted divider.

Independent gross surface envelope: Acollector=π(0.0252)(0.295)=0.0233546m². At a capTs, the upper rejection for that lateral area, with SI assumptions, is
A[h(Ts)(Ts−293.15)+0.8σ(Ts^4−293.15^4)].
It yields148W at500K,277W at600K and1479W at1000K. This is a necessary area/load screen, not a sufficient device design. It assumes the whole area reaches the cap; actual nonuniform temperature lowers heat removal. It omits other exterior reactor area. The internal nozzle itself does not freely view ambient. Heat transport from the arc attachment through the divider/back wall to the collector is unqualified. All159W treated as heat is a conservative gross-load stress test; the chemical energy retained reduces final heat rejection. No heat-recovery or gas-quench speed claim follows. Reproduce with check_surface_envelope.py; results are in surface_envelope.json.

## EPA expansion/wall-quench receipt

This is combustion-gas sampling, not dry2700K fixation. Its applicability is hardware and measurement discipline.

- Three pressure taps in the straight section plus one after the bend corroborated the shock/pressure model. Aerodynamic operation needed approximately0.12atm back pressure; approximately50torr was needed to extend supersonic flow through the whole section, beyond available sampling-pump throughput.
- For the1280K IFRF example, model-inferred shock position/time was5.2cm/45µs at0.12atm, followed by recovery to1080K and cooling below1000K by170µs. At1/3atm the corresponding shock was0.9cm/8.6µs, recovery1205K, and below1000K only by750µs. Time above1000K was125 versus740µs. These temperatures/times are MODEL results, not direct resolved thermal measurements.
- The authors considered direct supersonic thermometry impractical because the probe thermocouple itself causes a shock. Downstream temperatures within50K of prediction were explicitly considered potentially fortuitous.
- TableIV-F: at back pressure≥205torr versusapproximately95torr, FT12 idle NO was395 versus385ppm and NOx480 versus478ppm; maximum-continuous NO740 versus740ppm and NOx800 versus790ppm. No meaningful retention benefit from deeper expansion was established in these already-cool exhaust conditions.
- At90torr the pumping train supplied only1ft³/h, barely enough for the analyzer. The report does not supply full-cycle pumping energy.

Thus actual NO measurements support a conventional water-cooled-wall comparator as effective for those sampled exhausts, not a claim of99.9% retention for the saved heater state. Pressure and thermal history must be measured, not inferred from a nozzle label.

## Next bounded admission test

The appropriate next object is a dry, finite wall quench that avoids arc attachment to the critical cooling surface, with measured hot-state input, totalNOx input/output, pressure loss, complete steady thermal balance, wall hot spots and intact geometry. Match original fresh feed and final300K/1atm relaxed modes, and charge actual electrical/supply/cooling/reset resources. Merely adding a nozzle to the saved ideal trace, or importing the2.1MJ/mol headline, does not meet that contract. The present source pass identifies that admission target; it does not launch its simulation or claim it exists.
