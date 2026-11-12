FULL-CYCLE PHYSICAL CONTRACTS FOR CARBON CONCENTRATION, AMMONIA AND DISPATCHABLE HEAT
ROOT,12November2026Brisbane. Derived engineering constraints, conditional examples and actual source scopes. No physical device or experiment is asserted.

1. A common-cost floor changes fabrication decisions.
If useful devices cost Cnew=(P+Fnew)/Ynew and Cold=(P+Fold)/Yold, where P is a genuinely common port/package/test allowance, F is the differing process allowance and Y the actual working fraction, tenfold cost reduction requires
 Fold>=10*(Yold/Ynew)*(P+Fnew)-P.
With equal yields this is Fold>=9P+10Fnew. Using the optical return's illustrative partition P=2.270USD,Fnew=1.110USD gives31.53USD; even Fnew=0 needs20.43USD. Its modeled serial route allowance3.66USD is below either. This is conditional on the stated partition and common assumptions, not a general manufacturing lower bound. The return's full batch ledger also includes rework/other charged allowances; ROOT did not collect or run the linked code to reconcile every base-cost/allowance convention.
The complete available batch figures44622/10800=4.13167USD per working candidate versus40287/10800=3.73028 replication and43664/10800=4.04296 parallelprinting remain engineering estimates at90%yield, not quotations or measured yields. This identifies why an improved isolated route-writing step need not improve the useful complete operation.

2. Air separation, airflow and humidity must share one balance.
For an ideal binary mixture at T,P, inlet CO2 mole fraction x and captured CO2 fraction r into PURE product at the same pressure, let
 g(x)=x ln(x)+(1-x)ln(1-x),
 y=x(1-r)/(1-rx).
Per captured mole, reversible isothermal work is
 w=RT[(1-rx)g(y)-g(x)]/(rx).
It follows from the difference between final and initial ideal-gas Gibbs mixing energies. Finite capture changes the retentate composition; the infinite-dilution RTln(1/x) alone omits this term.
At T=298.15K,x=425e-6,r=.5, w=20005.59957J/mol=126.2707141kWh/tonneCO2. This is a PURE-product diagnostic; a95%product has a different terminal mixing term and must be calculated as such. It is not an attainable separator efficiency.
The processed inlet volume is RT/(P*M_CO2*x*r)=2616.055886m3/kgCO2 at P=101325Pa. A hypothetical50Pa total pressure drop and.6 fan efficiency costs60.5568492kWh/tonne in ideal fan-work accounting. The actual contactor/filter/duct/fan operating point is not supplied.

If moisture regeneration changes water loading by Delta_w kgH2O/kgdrymaterial and captures Delta_q molCO2/kgdrymaterial, evaporation before ACTUAL recovery is Delta_w/(M_CO2*Delta_q) kg/kg. At.5kg/kgwater and2molCO2/kgworkingcapacity it is5.68059169kgH2O/kgCO2. Faster drying alone cannot alter that ratio.
For a water reservoir evaporating reversibly into a fixed relative-humidity reservoir phi at the same T, the available chemical free energy is RTln(1/phi) per molwater. If this is the ONLY driving free energy for the ideal PURE separation above, phi=.3 requires at least2.74385071kgwater/kgCO2. Finite humidity change, heat transfer and irreversibility can increase the requirement. Purchased electrical work changes this budget. Neither latent heat nor an ambient humidity gradient is absent merely because no process heater is installed.
A diffusion time L^2/D can favor thinner active material, but D, real cyclic capacity, swelling and surface resistance must be measured. Thin supports/films also change material area, pressure drop, adhesion and cost. No material with independent freely chosen capacity, water affinity and diffusivity is constructed here.

Material replacement example ONLY: dry sorbent10USD/kg, actual cyclic uptake2molCO2/kg and10000 usefulcycles give11.36118USD/tonneCO2 sorbent-only cost. This does not establish those joint properties/lifetime. At.50kWh/kgCO2 and.05USD/kWh, electricity alone is25USD/t. Water, product purity/pressure, gas movement, contactor, manufacture, waste and capital still matter. Capturing into alkaline solution is not the same output as pure gas, and gas delivery is not permanent carbon removal.

Actually read primary scope:
Flory etal2508.02650v1 actual initial Materials/Methodspp2--4: commercialAER, belt/mesh conveyance between ambientair and an alkaline liquid; wet release and slow drying/loading are explicit. This supplies a physical apparatus, not pure-gas regeneration or the aspirational lowwater/highcapacity material. First subsequent governing navigation failed400Timeout; later methods/model/cost derivations were not read and the identity remains HELD.
Sinyangwe etal2606.26438v1 initial mechanism/equation1/five-stepdescription throughpp3--4: pressurization, sorption, air evacuation, vapor stripping and final desorption/condensation. It is a modeled process with stated experimental kinetic inputs, not an accepted whole cheap module. First subsequent governing navigation failed400Timeout; unread detailedmodel/optimization is not imported and the identity remains HELD.

3. Ammonia energy must use the complete terminal circuit and chemical cycle.
The useful nitrogen-reduction charge in an ordinary electrochemical route is3F per molNH3. With actual ammonia Faradaic efficiency etaF, recovered product mass m and terminal voltage U(t),
 E_electric=(integral U dQ + allauxiliarywork + chargedpreparation)/m,
 Q/m>=3F/(M_NH3*etaF).
Using M_NH3=.01703052kg/mol gives4721.197206Ah/kg. A12kWh/kg budget at etaF=.9 leaves charge-weighted complete voltage<=2.28755537V BEFORE auxiliaries;1kgNH3/day carries218.573945A on average. Pulsed duty must use time-average charge and actual output, not pulse-on rate.
The diagnostic U=7V,etaF=.36 gives91.8010568kWh/kg if voltage is treated constant. It is NOT the measured integrated energy of an experiment whose prehydridation and operating voltages differ. A reported9.12eV/NH3 electrodeposition-associated energy equals14.3524395kWh/kg; it is not a complete air/water product cost or an all-mechanism bound.

For a mediator cycle with free energies depositionD, nitridationN and protonationH, Hess's law fixes D+N+H to the same specified net reaction. If ion solvation/reference changes reduce D while nitride and product states are unchanged, corresponding terms in H or other supplied reservoirs change. A decrease in one reported half-cell potential is not automatically a decrease in the closed device input.
The full sustainable net chemistry is N2+3H2O -> 2NH3+1.5O2; hydrogen separation, proton donors, consumedmetal, solvents, salts, preloadedhydrogen and product recovery must close or be charged as inputs. The sustainable word is not earned by calling a sacrificial reservoir a mediator.

Actually read sources:
Azumah--Viswanathan2507.21121v1, entire4pages/equations1--12: electrodeposition/nitride/protonation free-energy bookkeeping and alloy/solvent conditions for a stated dissociative route. SHE/proton-reservoir conventions and route assumptions remain. It is theoretical and does not construct a new full-cell material or obstruct every ammonia architecture.
Ye etal, ACS EnergyLetters2026 DOI10.1021/acsenergylett.5c03617, publishedImperial manuscript actualpp1907--1911 read: an electricallyisolatedPd membrane couples aqueouswateroxidation to a dry nonaqueousLiNRR compartment, with actual water-isotope transfer, prehydridation charge, finite multi-volt losses and degradation observations. Reported36+/-4%FE includingprehydridation/-6mAcm2/6h is not a new full-plant energy/output rating. Unread laterpassages/SI not imported. Source https://spiral.imperial.ac.uk/bitstreams/fb14ca1a-5d95-41c8-b871-b5ac0874a8ba/download .
No alternative recovery of held cited originals follows.

4. A physical OFF state is a different heat-transfer operation.
For a simple coldsurface of areaA viewing a black source, Qabs=alpha_eff*Fview*sigma*A*(Th^4-Tc^4), with spectral/angular generalization needed for a real stack. ForA=.00961m2,Th=1648.15K,Tc=334.85K the blackbody scale is4014.038086W. To keep THAT branch below1W requires alpha_eff*Fview<=2.49125688e-4. The product is not assigned to an actual mirror. Additional supports, shields, gas and actuators add heat.
An electrical bypass leaves a cold optical absorber; reflectivecaps can reduce that waste. A cold reflective shutter still absorbs and needs cooling. A closure moved near the hot side changes the transport, but its back-face radiation/conduction/insulation, finite clearances, supports and actuation remain physical costs. Simply naming a hot valve or thermal switch does not supply one.
For the current conditional100W design:321.68-100/.35=35.9657143W hotdraw must disappear at unchanged output to reach35%NET. Its58USDnoncellcost/.95assemblyyield+9.80overhead=70.8526316USD/unit even with free cells. These are route-specific constraints, not all-converter negatives. Wholecycle electricity also pays OFF auxiliaries and hot standby, rather than quoting cell-only efficiency or a thermal store's retention.

A conditional Stirling comparator with rectification.98, controls.7W and introducedheatloss10W needs engine heat-to-AC efficiency>=((100+.7)/.98)/(100/.35-10)=.372686899 to meet the same100Wnet/35%target. Cost reduction must preserve that efficiency as well as cooling and all other whole-device terms.

New actual primary scope:
NASA20140017752, https://ntrs.nasa.gov/api/citations/20140017752/downloads/20140017752.pdf?attachment=true , actualpp1--3:88WAC38%850Chot90Ccold and real freepiston/linearalternator/gasbearing/clearance/heaterhead context. This is existing conversion performance, not a cheap aircooled converter/OFFstate.
NASA20080047457, https://ntrs.nasa.gov/api/citations/20080047457/downloads/20080047457.pdf?attachment=true , actualinitial complete-test statement and physicaldesign pp1--6: segmentedregenerator geometry/microfabrication and integration with axialconduction. A higher heattransfer/pressuredrop metric does not give a whole-engine efficiency improvement. Not all27pages or cited originals were read.

These calculations identify physical interfaces; they do not supply a new separator, ammonia catalyst, complete heat engine, factory or lifetime. No physical experiment or procurement occurred.
