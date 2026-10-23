# Iron-shell pressure-pulse audit

## Finding

A total-pressure down/up pulse at fixed H2O/H2 ratio is not, by itself, a change in the Fe/FeO oxygen-potential driving force. For

\[
\mathrm{FeO+H_2\rightleftharpoons Fe+H_2O},\qquad
\Delta_rG=\Delta_rG^\circ+RT\log\!\left(f_{\mathrm{H_2O}}/f_{\mathrm{H_2}}\right),
\]

the ideal-gas total pressure cancels when both partial pressures scale together. The same cancellation holds for the gas terms in hematite-to-iron reduction. At high pressure the relevant condition is the **fugacity ratio**, not merely a fixed partial-pressure ratio; its pressure dependence must be calculated or measured. A pulse can still alter rates, gas transport, heat transfer, or transient stress, and reaction can continue if the baseline gas is already reducing. The claim to test is therefore a persistent kinetic/mechanical conditioning effect, not a pressure-induced equilibrium shift.

The most serious experimental obstacle is that a pressure transient changes both the TGA signal and the gas/sample interface on the same timescale. A TGA mass trace during the pulse is not an oxygen-conversion trace unless buoyancy, flow drag, actual sample temperature, and outlet composition are separately controlled. A pressure pulse also does not measure permeability: a persistent change must be measured afterward at a common baseline with an imposed and recorded flow/pressure drop across the sample.

## Reproducible scales

The included [calculation script](pressure_pulse_bounds.py) evaluates ideal-gas density, cell gas inventory, turnover, outlet-ratio perturbation, and stoichiometric oxygen balances. Its illustrative case is 800 °C, 10 mol% inlet steam (H2O/H2 = 1/9), a 100 mL hot volume, and standard flow interpreted at 0 °C and 1 atm. These are scale examples, not specifications for a proposed rig.

| Quantity | Calculated scale | Interpretation |
|---|---:|---|
| Gas density, 1 bar | 0.04052 kg m−3 | H2/H2O = 90/10 mol% at 1073.15 K |
| Apparent buoyancy step, 1→2 bar | 40.5 µg per cm³ displaced | The suspended sample **and holder** volume is unknown and must be calibrated |
| Apparent buoyancy step, 1→10 bar | 364.7 µg per cm³ displaced | Linear in pressure in this ideal-gas example |
| Buoyancy scale at 1 bar, 50/50 H2/H2O | 112.2 µg per cm³ | Composition matters even at fixed pressure |
| Temperature sensitivity at 1 bar | 0.0378 µg cm−3 K−1 | A 10 K offset is about 0.38 µg per cm³ in this mixture |
| 100 mL hot-gas inventory at 1 bar | 1.12 mmol | Excludes connecting lines and regulator volume |
| Minimum inventory-fill time for a 1 bar step | 7.5 s at 200 sccm; 3.0 s at 500 sccm | Ideal lower bound; excludes controller, line, and vent/BPR dynamics |
| Hot-volume residence time at 10 bar, 200 sccm | 75 s | If standard molar flow is held fixed; at 1 bar it is 7.5 s |
| Unregulated leak of 1 sccm from 100 mL at 1073 K | 66 Pa/s pressure drift; 25 min inventory/leak time at 1 bar | A regulator can mask pressure decay while ingress still changes gas composition |
| Unheated 298→1073 K feed sensible-heat load | about 3.5 W at 200 sccm; 8.7 W at 500 sccm | Cp=30 J mol−1 K−1 scale; preheating and a sample thermocouple are needed |

At fixed standard molar flow, raising pressure reduces actual volumetric flow and lengthens residence time in proportion to pressure. If the controller instead preserves hot-zone linear velocity, it must raise molar throughput, increasing reactant/water supply and heat load. These are different protocols and cannot be collapsed into “same flow.” The cited instrument demonstration explicitly increased flow from 200 to 500 mL/min NTP at elevated pressure to partly offset the velocity loss, and used identical-condition blank subtraction for buoyancy.

For a reacting sample, inlet ratio is not sample-side ratio. Let \(r_{in}=F_{H2O,in}/F_{H2,in}\), and let \(\chi\) be the fraction of inlet H2 consumed locally. Ignoring other reactions and transient holdup,

\[
r_{out}=\frac{r_{in}+\chi}{1-\chi}.
\]

With \(r_{in}=1/9\), only 1% local H2 depletion raises the outlet ratio by 10.1% relative to the inlet value. The script also checks stoichiometric demand for 2–3.5 g Fe2O3 pellets: complete reduction consumes 37.6–65.8 mmol H2 and removes 0.60–1.05 g oxygen. At 200–500 sccm for 120 min the integrated demand is about 1.4–6.1% of the pure-H2 feed for those limiting pairings. This is a whole-run average balance, not a prediction of the instantaneous outlet peak. Online H2/H2O measurement is needed to bound actual local ratio during a pulse.

## Instrument and material boundary

The manufacturer’s high-pressure TGA application note reports a 50-bar instrument, a steam option and two reaction lines; its iron-pellet setup used a custom platinum-wire holder, 2–3.5 g pellets, and blank-run subtraction under matched conditions. This is evidence that specialized pressure TGA and iron reduction can be done, not evidence that the exact humid fixed-ratio pressure waveform has been validated or that a normal TGA can be retrofitted. The same note reports a large pressure-associated change in reduction rate under pure H2, but flow was also increased at elevated pressure; it is not an isolated pressure effect, an equilibrium test at fixed H2O/H2 ratio, or evidence of pressure-only shell conditioning.

A realizable test needs, at minimum, a pressure-rated thermobalance and holder; calibrated H2 and steam delivery that preserve the ratio through the pressure ramp; heated lines that avoid condensation; pressure measured near the sample and at the outlet; sample-zone temperature measurement; flow measurement; matched empty-holder/reference runs through the full waveform; and outlet H2/H2O analysis. Those components are not free baseline controls. The instrument source demonstrates a custom holder and blank correction, while the older primary thermobalance paper explicitly treats gas-density-dependent buoyancy correction as a central pressure-measurement problem.

Pressure stability is not a substitute for leak/composition stability. In a fixed, isothermal 100 mL volume at 1073 K, a constant 1 sccm standard leak corresponds to about 66 Pa/s pressure drift and a 25-minute inventory/leak time at 1 bar. A pressure controller may hide this drift by make-up flow, while inward leakage still adds O2/N2 and changes the feed composition. Set a permitted leak from the actual H2O/H2 and impurity tolerance, and demonstrate it with a leak test and logged make-up flow; the pressure-decay number alone does not certify the ratio.

The pressure waveform itself must be slow/fast relative to the unknown pore-pressure equilibration time. For a connected porous particle with permeability \(k\), porosity \(\phi\), gas viscosity \(\mu\), characteristic shell length \(\ell\), and mean pressure \(P\), a linearized isothermal Darcy estimate is

\[
\tau_p\sim\frac{\phi\mu\ell^2}{kP}.
\]

If the ramp is much slower than \(\tau_p\), pore pressure tracks external pressure and there is little sustained differential pressure across a shell. If much faster, a transient differential may occur, but its magnitude/duration depend on the unknown pore network. A whole packed bed has a separate hydraulic pressure drop. A uniform chamber-pressure change is not a bed pressure-drop measurement, and a pressure-gradient result on a packed bed does not establish an individual-grain shell effect.

## Separate case: composition pulse at fixed total pressure

A redox phase pulse can instead hold total pressure fixed and change the H2O/H2 ratio. That is a different operation from the fixed-ratio pressure pulse above: it changes oxygen potential, but it also changes gas molecular mass, buoyancy, heat capacity, and likely transport properties. For an explicitly illustrative 800 °C, 1 bar ideal-gas case, changing steam from 10 to 30 mol% changes mixture molar mass by 3.1999 g/mol. The resulting balance shift is

\[
\Delta m_{\rm buoy}=-V_{\rm disp}\frac{P\,\Delta\bar M}{RT}
 =-35.86\;\mu\mathrm{g}\;\text{per cm}^3\text{ displaced},
\]

with the negative sign denoting a lower apparent sample mass as the heavier mixture increases buoyancy. At 10 bar the ideal scale is −358.6 µg/cm³. The inlet H2O/H2 ratio also changes from 1/9 to 3/7, so this is a real redox excursion rather than a pressure-only perturbation.

For comparison, if a 3.5 g pellet contains 67.8 wt% Fe and **all** of that Fe is initially metallic, oxidation of 0.1% of its Fe inventory adds just

\[
3.5(0.678)(0.001)\frac{15.999}{55.845}\;\mathrm{g}
=0.000680\;\mathrm{g}=680\;\mu\mathrm{g}\;\text{O}.
\]

The 1 cm³ buoyancy step is 5.28% of this uptake; a 19 cm³ displaced volume would make the two scales comparable. If only a fraction \(f_0\) of the total Fe is metallic initially, multiply the oxygen-uptake comparison by \(f_0\). The 19 cm³ figure is a scale comparison, not an estimate of the actual hangdown/holder displaced volume.

The feed heat-flow also changes even if total standard molar flow is held fixed. With an explicit illustrative mean heat-capacity assumption \(C_{p,H2}=29\) and \(C_{p,H2O}=36\;\mathrm{J\,mol^{-1}K^{-1}}\) over 298→1073 K, the 10→30 mol% steam shift changes sensible-heat delivery by about 0.16 W at 200 sccm or 0.40 W at 500 sccm. These are order-of-magnitude estimates, not vendor performance predictions; actual heat transfer needs sample-temperature measurement.

Therefore the composition controller needs a full dynamic blank through the same pressure, flow, steam, and temperature waveform, plus outlet gas and solid oxygen inventory. The manufacturer note’s matched blank-run subtraction is a reported experimental procedure, not a guarantee about the residual error for this different composition transient. Neither a nominal balance sensitivity nor a pressure-rating specification establishes dynamic blank accuracy. Use corrected solid oxygen uptake, not raw thermogravimetric mass, as the chemical readout.

For a bed-level permeability claim, measure \(Q\) versus \(\Delta P\) across a known bed at common baseline pressure, composition, temperature, and packing before and after treatment, with inlet/outlet taps at the bed. Compare using the same gas viscosity and geometry; propagate flow, pressure, dimensions, and temperature uncertainty. For a grain-shell claim, use a single-grain geometry and establish pressure equilibration or directly bound internal/external pressure lag. A TGA alone supplies neither permeability nor pore-pressure lag.

## Required pulse protocol and mass ledger

The comparison should return to one specified baseline \((P_0,T_0,r_0,Q_0)\), where \(Q_0\) is explicitly either molar standard flow or hot-zone volumetric flow. Log both inlet settings and outlet H2/H2O. After returning, wait at least five **measured** hot-volume residence times and longer if outlet composition or mass is still drifting; the 100 mL/200 sccm example is 38 s at 1 bar, before tubing and adsorption/desorption delays. “Same inlet ratio” does not guarantee the same sample-side ratio while oxygen is being removed.

Record an empty-holder/reference pulse using the same gas composition, pressure path, flow, holder, and thermal history. During the pulse, model apparent mass as sample/holder mass minus displaced-gas buoyancy plus flow-dependent force; subtracting an empty pan without matching the holder/sample displaced volume is insufficient. After return to baseline, a surviving mass shift may be real reduction, volatile loss, or solids carried out of the holder. Fe2O3→Fe has a 30.1% theoretical oxygen mass loss, but a balance cannot distinguish that oxygen loss from lost fines. Collect and weigh downstream fines and assay the recovered solid’s phase/oxygen state. Close an oxygen balance with inlet/outlet H2O and H2, initial/final solid oxygen, and all captured solids; do not call raw TGA mass difference “reduction.”

For permeability, perform the post-pulse \(Q\)-\(\Delta P\) measurement at the common baseline separately from the TGA mass trace. A persistent change must exceed its propagated measurement uncertainty and survive identical packing/handling controls. Cracking or shrinkage of a pellet, bed settling, and fines movement can all alter hydraulic response without a grain-shell permeability change.

## Positive control: shallow Fe↔FeO excursion

Use a matched aliquot to make a short, shallow redox excursion at the same sample temperature: choose a calibrated H2O/H2 fugacity ratio on the FeO-forming side of the Fe/FeO boundary, then one on the reducing side, and finally restore the common baseline ratio. This is a chemical-transformation control for whether the apparatus and post-baseline permeability assay can resolve a persistent change; it does not validate pressure-only causation. Keep this on a separate matched aliquot or run order that does not contaminate the pressure-only before/after comparison.

The oxygen inventory is large enough to require explicit bookkeeping: Fe→FeO takes up 0.2865 g O per g Fe (28.65% mass gain relative to Fe); FeO→Fe releases 0.2227 g O per g FeO (22.27% mass loss relative to FeO). For a fully reversed excursion, integrated water consumed during oxidation should match water produced during reduction after correcting for gas holdup/leakage, and the final solid oxygen inventory should return to its initial value. A net apparent mass loss after the excursion can instead be renewed reduction beyond the starting state, unrecovered fines, or residual buoyancy/thermal offset. Measure gas oxygen transfer, retained-solid phase/oxygen, and all collected carryout before interpreting it as a persistent structural effect.

## Evidence boundary

1. Sasaki, Homma, Yamada & Makino, [“Thermobalance for thermogravimetric measurement under pressure”](https://doi.org/10.2116/bunsekikagaku.18.1179), *Bunseki Kagaku* 18 (1969), 1179–1183. Primary instrument paper: pressure-dependent gas-density buoyancy correction is identified as important; the apparatus included an electronic correction circuit.
2. TA Instruments, [“Investigating Direct Reduction of Iron Ore in Hydrogen” (TA487)](https://www.tainstruments.com/applications-notes/investigating-direct-reduction-of-iron-ore-in-hydrogen-ta487/). Manufacturer application experiment, not an independent peer-reviewed validation: reports high-pressure iron-pellet TGA conditions, custom platinum-wire holder, increased flow at elevated pressure, matched blank subtraction, and optional online gas analysis.

The pressure-only mechanism remains **unestablished**. The strongest bounded conclusion is that fixed-ratio total-pressure cycling can probe kinetic/transport/mechanical response, but it does not change ideal-gas redox equilibrium; current measurement needs would make a pulse-in-TGA trace ambiguous without pressure-matched buoyancy/flow corrections, sample-side gas and temperature measurements, and a separate baseline permeability test. The shallow Fe↔FeO excursion is a necessary positive control if transformation strain is the intended comparison.
