# P2 ambient to 200 C steam: complete available return

Same Pro chat: https://chatgpt.com/c/6af520d7-3fcc-83ec-8bf0-80e8531141ea. Exact source prompt: P2_FULL_AMBIENT_HEAT_TO_200C_STEAM_INVENTION_PRO_20261112.txt, sent once. Visible response complete by 2026-11-12 09:06 UTC.

Capture limits: rendered final DOM innerText may duplicate or distort mathematics and tables; it is not native/database text, whose final ID and full text remain unknown. Expanded top-level visible activity follows, with original visible prompt; nested command, web, file, Library and helper contents were not captured. The outputs panel said no outputs yet; any linked artifacts and their identities and eligibility are unverified and were not collected. No producer code was executed or unavailable source recovered.

## Complete available rendered final

Result

I have not established an invention that meets your requirements. I developed and executed a concrete ambient-air-to-steam construction, including its phase-transfer mechanism, machinery, finite heat exchangers, water boundary, startup model, installation budget and component replacements. The final audited construction misses the efficiency, capital, heat-cost and small-unit campaign targets. A competent conventional arrangement is also cheaper in the matched model.

That conclusion applies to this construction and its assumptions. The thermodynamic limit leaves room for COP 2; this work does not establish an obstruction to economical high-temperature heat pumps.

Requirement	Final result
Reference output	Modeled 1 MW net-added heat as 200°C steam; physical quality acceptance remains untested
Complete reference COP ≥2.0	1.938, requiring 515.90 kW
Repeat installed capital ≤US$500/kW	US$1,385/kW
Heat cost ≤US$35/MWh at $40 electricity, 90% use	US$48.79/MWh
At least 25% cheaper than strongest applicable alternative	Not established; the matched conventional construction is cheaper
Cold 100-hour small-unit campaign: ≥1 MWh heat, ≤500 kWh electricity	684.51 kWh for 1 MWh in the model
Laboratory demonstration	None performed

The final heat cost includes a correction made during the service audit: full renewal of the injection tips and thermal face caps costs more than the earlier maintenance allowance.

The deliverables contain the complete calculations and assumptions:

heat_amplifier_report.html — engineering report, component geometry, itemized installation and prototype budgets, operating sequence, comparisons and primary evidence.
heat_amplifier_model.zip — executable Python model, full computed states, cash flows, inventory calculations, manufacturing assumptions and reproduction instructions.

All candidate performance below is conditional modeling, not measured performance. All project prices are introduced engineering budgets, not supplier quotations.

1. The product boundary and the available thermodynamic margin

I selected the return condition as 90°C liquid water at 1.5 bar absolute. Every comparator receives that same stream.

Using CoolProp 7.2.0 water properties, whose underlying equation of state is IAPWS-95, the reference states are as follows. 
CoolProp 8.0.0 documentation

Quantity	Value
Saturation pressure at 200°C	15.549279 bar absolute
Dry saturated-vapor enthalpy	2,792.007 kJ/kg
Saturated-liquid enthalpy at 200°C	852.271 kJ/kg
Return-water enthalpy	377.101 kJ/kg
Added heat per kilogram of dry steam	2,414.906 kJ/kg
Steam flow for 1 MW added heat	0.414095 kg/s, or 1,490.74 kg/h

The meter boundary is

𝑄
˙
a
c
c
e
p
t
e
d
=
𝑚
˙
a
c
c
e
p
t
e
d
(
ℎ
o
u
t
−
ℎ
r
e
t
u
r
n
)
.
Q
˙
	​

accepted
	​

=
m
˙
accepted
	​

(h
out
	​

−h
return
	​

).

The return already brings approximately 130.02 kW of sensible enthalpy above 15°C water. That energy is an input throughout the model. Of the added megawatt, approximately 803.23 kW supplies evaporation and 196.77 kW supplies liquid heating.

The reference calculation uses dry saturated vapor. At the minimum acceptable dryness 
𝑥
=
0.995
x=0.995, slightly more mass—about 0.4%—is needed for the same added heat. Actual acceptance must use measured outlet enthalpy; pressure and temperature alone cannot establish dryness.

I specified industrial steam for indirect process heating, with these introduced acceptance limits:

Dryness 
𝑥
≥
0.995
x≥0.995.
Nonvolatile contamination no greater than 1 mg/kg.
Oil no greater than 0.1 mg/kg.
Foreign refrigerant no greater than 0.01 mg/kg.
Return-water dissolved solids no greater than 1 mg/kg, with filtered return and RO/EDI makeup.

These are design contracts, not a claim of pharmaceutical or direct-food-contact qualification. Off-spec steam is diverted and receives no useful-heat credit.

Reversible bound

For this exact return and output boundary,

𝑊
˙
min
⁡
=
𝑚
˙
[
Δ
ℎ
−
𝑇
𝑎
Δ
𝑠
]
.
W
˙
min
	​

=
m
˙
[Δh−T
a
	​

Δs].

At 15°C ambient, this gives 375.07 kW minimum work, or a perfectly glide-matched COP of 2.66615. At 5°C and 35°C, the corresponding bounds are approximately 2.5204 and 3.0148.

Thus COP 2 is thermodynamically possible. The difficulty is producing the required pressure, temperature distribution and heat-transfer rate while keeping the complete installation below 500 kW input and US$500,000 capital.

2. The mechanism I investigated

The candidate uses an ammonia heat pump to make low-pressure steam, followed by six stages of mechanically driven, continuously water-injected steam compression.

The operation investigated was a combination of:

Crank-synchronous injection during compression, so evaporation limits gas overheating while increasing the final steam mass.
Finite interstage evaporation vessels, allowing carried droplets to finish evaporating using already supplied gas enthalpy.
Removable pressure-end cassettes containing valves, injectors and supported thermal face caps, giving access to the parts most likely to need service.
Direct mechanical pressure conversion, with opposed double-acting pistons connected to a crank and electric motor.

The last item avoids the constant-pressure hydraulic throttling error encountered in some liquid-piston representations. It is conventional mechanical architecture and does not itself establish novelty.

Ambient air
Ammonia source andcompressors
Common grid meter
Finite double-wall heatexchanger
70°C steam generator
90°C condensate return
Metered high-pressureinjection
Six-stage steam converter
Fans, pumps, treatment andcontrols
Separator and accepted200°C steam
Customer process
Prior art matters here

Internally sprayed, variable-mass steam compression was published by Qiu, Gu and Cai in 2004. Later work addresses water-injected compressor behavior, and the 2017 HighEFF study already examined staged, directly water-injected steam compression toward 200°C. Generic injection, cascades, pressure staging and interstage heat management therefore cannot be claimed as the invention. 
inderscience.com
+2

The potential contribution would have had to be a demonstrated improvement in the combined phase-transfer, valve, wall-loss, manufacture and service operation. The calculations did not establish that improvement.

Thermodynamic arrangement

The reference ammonia cycle has two compression stages with flash intercooling:

Low-side saturation state: approximately 9.65°C and 6.074 bar.
Intermediate pressure: 16.432 bar.
Condensation: 75°C and 37.096 bar.
Mixed compressor suction: 13.65°C.
Liquid subcooling to approximately 72°C.

A finite double-wall exchanger transfers heat to water boiling at 70°C and 0.312 bar absolute. The water vapor then passes through the steam compressor.

The main product flows are:

Stream	Reference flow
Steam entering the compression train	0.315434 kg/s
Return water added through injection	0.098661 kg/s
Accepted steam	0.414095 kg/s
Declared hot condensate return	0.414095 kg/s

Injection receives its water from the declared return. No additional hot-return stream supplies the source heat.

3. Machinery and fabrication
Steam cylinders and valves

The industrial train uses two opposed double-acting cylinders per stage, giving twelve physical cylinders and four working faces per stage. The selected stroke is 250 mm, operating at 5 Hz, or 300 rpm.

Stage	Pressure, bar absolute	Approximate bore	Interstage vapor volume
1	0.312 → 0.600	653 mm	3.71 m³
2	0.600 → 1.152	492 mm	1.93 m³
3	1.152 → 2.213	370 mm	1.00 m³
4	2.213 → 4.252	279 mm	0.50 m³
5	4.252 → 8.171	211 mm	0.25 m³
6	8.171 → 15.699	160 mm	0.12 m³

The final stage includes a delivery-pressure allowance before the 15.549-bar product boundary.

The low-pressure inlet handles roughly 1.6 m³/s. This makes the first stage physically large despite the modest electrical power. Its valves require roughly 0.26 m² total open area, divided among the working faces.

A pressure-operated valve cannot be assigned negligible opening loss. For example, moving a 0.5 kg assembly through 5 mm in 10 ms requires order 50 N, corresponding to roughly 770 Pa over a 0.065 m² opening before spring and flow losses. The baseline therefore charges 1,000 Pa cracking pressure, plus flow-dependent loss.

Existing oil-free, double-acting crosshead steam compressors establish a relevant manufacturing class. Spilling lists approximately 1–20 t/h machines, but its standard inlet range starts above this candidate’s vacuum stages. Its existence does not supply the proposed complete map or small-scale performance. 
spilling.de

Pressure structure and thermal faces

The preliminary construction uses:

Honed 316L pressure shells.
Hollow, ribbed steel pistons.
12 mm shell walls for the preliminary pressure screen.
Approximately 20 mm ribbed heads.
External-pressure stiffeners on the low-pressure stages.
Carbon-ring and rod-packing arrangements with an isolated, lubricated crosshead.
Fully supported 0.75 mm PEEK face segments on nonsliding surfaces; the bores remain steel.

For a 660 mm low-pressure bore, an ideal elastic buckling calculation gives approximately 1.31 MPa. Applying a separately introduced 0.2 imperfection factor gives 0.262 MPa, compared with 0.101 MPa full vacuum. The high-stage hoop-stress screen is approximately 10.5 MPa, rising to 31.4 MPa with an introduced local concentration factor of three.

These are preliminary screens. They do not certify ports, welds, ovality, head ligaments or thermal fatigue.

PEEK’s published conductivity and density support a thermal calculation, but its glass transition is about 143°C, below the hottest gas in this machine. Fully backed, nonsliding caps avoid assigning it the global pressure load; they still require qualification against hot cyclic deformation, attachment failure and contamination. Steam-sterilization suitability is not evidence of the required mechanical life. 
Datasheet (DE)

At the selected speed and utilization, each working face experiences approximately 142 million pressure cycles per year. Valve opening and closing motions are roughly twice that number. Component renewal is therefore central to the economics.

Injection is a real pressure operation

The selected rail is 153.7 bar absolute, maintaining at least 138 bar differential at the final stage. The modeled injection/feed pumping load is 2.39 kW; the construction needs roughly a 3 kW hot-water pump rated above 155 bar.

Commercial 316 stainless impaction-pin nozzles provide an obtainable manufacturing starting point. MeeFog specifies a 150 µm orifice and reports mean droplets below 10 µm at approximately 138 bar under its fogging conditions. Those data do not establish droplet behavior in hot, pressurized steam. 
MeeFog

The budget allocates approximately 200 equivalent nozzle tips, timed manifolds, filtration and metering. Pump heat is credited to the injection water only because the represented pump has a heat-recovery jacket. It is not counted again elsewhere.

4. What the model solves—and what remains a hypothesis

The steam path closes the variable-mass enthalpy balance:

𝑑
(
𝑚
ℎ
)
=
𝑚
 
𝑣
m
i
x
 
𝑑
𝑝
+
𝑑
𝑊
g
a
s
,
l
o
s
s
+
ℎ
i
n
j
 
𝑑
𝑚
.
d(mh)=mv
mix
	​

dp+dW
gas,loss
	​

+h
inj
	​

dm.

The model uses finite droplet evaporation, with a 
𝑑
2
d
2
-law approximation:

𝑑
(
𝑑
2
)
𝑑
𝑡
=
−
4
 
𝑁
𝑢
 
𝑘
𝑣
(
𝑇
𝑔
−
𝑇
s
a
t
)
𝜌
𝑙
ℎ
𝑓
𝑔
.
dt
d(d
2
)
	​

=−
ρ
l
	​

h
fg
	​

4Nuk
v
	​

(T
g
	​

−T
sat
	​

)
	​

.

Injection timing, compression duration, gas superheat, residual liquid and poststage residence are coupled. The bulk enthalpy follows the selected path, but the gas itself remains hotter while droplets are present. It is not granted an equilibrium, nearly isothermal compression stroke.

The base calculation uses:

Introduced ammonia isentropic efficiency of 0.82.
Industrial motor efficiency of 0.96.
A mass-weighted droplet distribution spanning approximately 5–20 µm.
Explicit ring, gland, valve and bearing losses.
A wall thermal-admittance calculation.
Finite interstage residence.
Separate pressure drops and auxiliaries.

These are not measured simultaneous maps. The wall term is a work-loss surrogate based on entropy generation, not a validated transient wall calculation. Droplet collision, wall capture, re-entrainment, seal leakage and local two-phase flow remain qualification requirements.

Complete reference power
Imported load	kW
Ammonia compressors	190.26
Steam-compressor drive	303.96
Injection/feed pumping	2.39
Ambient-source fans	10.03
Makeup conditioning and header trace	2.97
Source circulation pump	0.65
Controls, vacuum, treatment, cooling and ventilation	2.20
Transformer and cable losses	3.43
Total	515.90

This gives

C
O
P
g
r
i
d
=
1000
515.895
=
1.93838
.
COP
grid
	​

=
515.895
1000
	​

=
1.93838
	​

.

The independently assembled energy ledger closes as

515.895
+
520.644
=
1000.000
+
36.046
+
0.493
k
W
.
515.895+520.644=1000.000+36.046+0.493kW.

Here 520.644 kW is net heat removed from the external air stream after downstream fan heat; 36.046 kW is other rejection; and 0.493 kW leaves as wastewater enthalpy above the makeup reference.

Numerical energy residuals are below 0.002 W. That verifies bookkeeping, not the physical adequacy of the constitutive assumptions.

A simultaneous optimistic qualification bundle—finer droplets, lower wall and friction losses, and 0.90 ammonia-compressor efficiency—reaches COP 2.047. This identifies a demanding joint requirement. It is not evidence that those improvements coexist, and it retains the expensive installation.

5. Finite air source, water treatment and inventories
Ambient exchanger

The main source has 120 m² face area, plus a separate 4 m² parallel-air superheater branch. The selected construction uses six rows of aluminium tubes, 4 mm fin spacing and 0.15 mm fins.

Its approximate material quantities are:

18 km of tube.
2.78 tonnes of tube aluminium.
2.60 tonnes of fins.
2.533 m³ internal tube volume.

All-aluminium ammonia coolers are an existing commercial construction. The selected geometry, pressure rating, distribution and lifetime remain introduced requirements. 
colmaccoil.com

At the reference point:

Air flow: 125.8 kg/s, approximately 103 m³/s.
Gross source heat: 530.7 kW.
Mixed coil outlet: approximately 10.83°C before fan reheating.
Main-bank 
𝑈
𝐴
UA: approximately 226.9 kW/K.
Fan power: 10.03 kW.

The calculation couples fin efficiency, heat-transfer area and pressure drop using published fin-and-tube methods. It still introduces the internal boiling coefficient and distribution behavior; those cannot be treated as independently guaranteed favorable constants. 
ACHP 1.5 documentation

The additional superheater is necessary. Assigning suction superheat without providing its finite exchanger would hide both heat-transfer area and a local temperature approach.

Hot interface

The ammonia/water interface provides 225 m² of double-wall heat-transfer surface. The model separates desuperheating, condensation, subcooling and steam superheating zones. At the reference point, the calculated requirement is approximately 185 m² at an introduced overall coefficient of 700 W/m²K; the local minimum temperature approach is about 2 K.

Independent barriers and monitored vent paths separate approximately 37-bar ammonia from the vacuum water circuit. A leak trips product acceptance.

Water and gas inventories

The steady water ledger includes:

Blowdown: 7.45 kg/h.
Condensed purge discharge: 2.98 kg/h.
Makeup entering at 15°C: 10.44 kg/h.
Electrical makeup conditioning: approximately 0.929 kW.

Dissolved air, vacuum leakage and purge water are distinct streams. The model budgets a purge condenser, vacuum pump and discharge. It does not accumulate noncondensables indefinitely or obtain useful work from dissolved-gas release.

The industrial ammonia allocation totals 750 kg, distributed among the evaporator, separators, economizer, hot exchanger, receivers and manifolds. A paid 2 m³ recovery vessel can accommodate the whole charge within the selected fill limit. Annual loss is budgeted at 1%, with leak search, recovery and replacement.

These are explicit inventory allocations and loss assumptions. Actual holdup, solubility, carryover and recovery performance remain unmeasured.

6. Operation, grid interface and seasonal limits

The plant receives a paid 750 kVA, 11 kV/415 V, 50 Hz connection, transformer, protection, metering, cable trenches and earthing. Separate variable-speed drives operate the ammonia machinery and approximately 355 kW steam motor.

The electrical design requirements are power factor ≥0.98 and current distortion ≤5% at the connection point, subject to an actual network study. Transformer losses are included.

The operating sequence is explicit:

Cold start: establish water quality, prime circulation, evacuate through the purge condenser, warm inventories with metered electricity and build the pressure stages. Startup output is rejected until qualified.
Accepted production: control steam pressure through speed, hold the low-pressure steam source with ammonia capacity, and synchronize injection with crank position and measured flow.
Partial output: reduce speed and adjust injection, fans and pumps. The model evaluates 75%, 50% and 25% load.
Idle: isolate the product. The financial case uses cold idle with 350 W controls and paid subsequent restarts.
Shutdown: stop injection, unload and isolate, collect condensate through a closed drain/quench route, and maintain lubrication until rotation stops. Spring-return valves provide the power-loss state. Control-energy depletion must be restored at the common meter.
Service: cool, drain and prove zero pressure before removing head cassettes, valves, injectors or vessel internals; recover ammonia before opening its circuit.

Instant accepted steam from a cold machine is not supplied by this design.

Location and weather

I used the Archerfield/Rocklea industrial area of Brisbane as a plausible site class, with Archerfield station 040211 as the climate anchor. The installation pays for 300 m² of industrial space, road/crane access, foundations, drainage, enclosure and 20 m each of steam and return integration. Actual ground bearing, flood elevation, noise propagation, customer water chemistry and utility augmentation are unmeasured. 
bom.gov.au

The land allowance uses a historical Brisbane industrial-land estimate with an explicitly introduced currency conversion. It is not a parcel quotation. 
CBRE Australia

Condition	Complete modeled COP
5°C, full output	1.842
15°C, full output	1.938
35°C, full output	2.151
15°C, 75% output	1.946
15°C, 50% output	1.923
15°C, 25% output	1.844

The three specified temperatures at 60% RH give dry source-coil conditions in the selected calculation. Humid nights and frost events require additional treatment.

A reconstruction from monthly climate means gives a dry seasonal COP of 1.993. It is not an annual performance forecast. It does not establish the joint distribution of temperature, humidity, fouling and defrost. An illustrative penalty of 1,000 productive hours at COP 1.3 reduces the annual value to approximately 1.867.

The lack of a qualified wet-weather and restart model is another reason the complete invention is not established.

7. Manufacture and lifetime cost

The repeat-production assumption is 50 systems per year for four years, totaling 200 plants. It pays material yield, forming, machining, assembly, factory occupation, tooling allocation, testing, rejects and site labor. It does not establish demand or a demonstrated production rate.

Repeat installation
Capital group	US$ thousands
Ambient source, fans, circulation and superheater	154.94
Steam and ammonia converter cores	400.00
Hot interface, water plant, dwell vessels, recovery and protection	229.75
Grid equipment and connection	120.00
Civil works, enclosure, integration, controls, commissioning and spares	166.00
Additional converter tooling allocation	12.50
Fabrication/integration contingency	162.48
Paid land	139.50
Total	1,385.16

The US$250,000 steam-core allowance includes pressure materials, crank and crosshead, machining, rings, valves, injection equipment, thermal caps, motor/drive, assembly and factory testing. The report decomposes that allowance rather than treating it as an unexplained price per kilowatt.

First installation and development
Boundary	Introduced budget
Repeat installed plant	US$1.385 million
First installation with allocated factory tooling	US$1.985 million
First factory and first installation, paying all tooling cash	US$5.219 million
Separate complete research prototype	US$295,680
Factory, first industrial installation and prototype together	US$5.515 million

The first-unit allocation is not the cash required to establish the factory.

Service and replacement

The calculation uses 20-year finance at 8% real discount, while assigning separate component lives:

Routine service, inspection, cleaning, chemistry, leakage and repair reserve: US$30,667/year.
Steam valve/seal service: every 15,768 operating hours.
Full injector-tip and thermal-cap renewal: US$12,000 every 8,000 hours.
Ammonia overhaul: 31,536 hours.
Fan renewal: 39,420 hours.
Major steam-train rebuild: 78,840 hours.
Ammonia core replacement: 94,608 hours.
Source-coil replacement: 15 calendar years.
Double-wall exchanger: 12 calendar years.
Controls: 10 years; treatment media: three years.
Retirement and fluid recovery: US$80,000, with land residual accounted separately.

These lives remain hypotheses. At lower use, operating-hour replacements move later; calendar deterioration does not.

The energy ledger also pays a 1.5% average service-age penalty, twelve cold starts per year and idle controls. Ninety percent utilization means 7,884 MWh/year delivered, without applying another availability multiplier.

Electricity price	Utilization	Complete reference heat cost
US$40/MWh	90%	US$48.79/MWh
US$40/MWh	60%	US$60.17/MWh
US$80/MWh	90%	US$69.75/MWh
US$80/MWh	60%	US$81.14/MWh

At $40 electricity and 90% use, the cost comprises approximately $20.96 electricity, $17.89 capital recovery, $3.89 routine service, $6.17 replacements and −$0.13 net retirement/residual per MWh.

Reducing installed capital by 25% still gives $44.31/MWh. Even granting the reversible COP while retaining this construction and service ledger gives $43.07/MWh. This shows that improving the compressor alone cannot rescue this particular installation budget.

8. Comparison with competent alternatives

The strongest explicitly constructed conventional comparator uses the same paid ammonia plant and vacuum boiler, followed by staged steam compression with interstage water injection. It receives the same source exchangers, water boundary, grid, site and common auxiliaries.

Matched construction	Modeled COP or net efficiency	Installed capital	Heat cost at $40 electricity, 90% use
Candidate	1.938	$1.385m	$48.79/MWh
Conventional six-stage NH₃ + MVR	1.913	$1.307–1.393m	$46.53–47.64/MWh
Conventional twelve-stage NH₃ + MVR	1.920	$1.324–1.410m	$46.67–47.78/MWh
Resistance boiler	0.988	$0.463m	$48.18/MWh
Gas boiler, fuel $25/MWh LHV	0.93 plus auxiliaries	$0.423m	$34.34/MWh

The candidate’s modeled efficiency advantage over conventional MVR is small. Its complete cost is approximately 2–5% higher, depending on the conventional machinery budget.

The conventional maps and separator endpoints also require qualification. They are favorable, explicit comparison assumptions, not a claim that a supplier has guaranteed this assembled point. Crucially, the comparison does not make the incumbent expensive merely because a public quotation is absent.

The boilers receive smaller paid sites and appropriate connections. Resistance pays for a new 1.25 MVA electrical connection; gas pays for its branch, meter, regulator and flue. Existing Bosch boiler classes cover the required flow and pressure. 
bosch-industrial.com
+1

Advanced existing heat pumps

AtmosZero’s measured supplier-sheet values are valuable evidence of actual construction. They are not a demonstrated all-auxiliary 15°C-air-to-200°C-steam point. Its published cost range also excludes integration. The follow-up paper exposes further measurement-boundary limitations, which prevent treating its reported COP as the required common-boundary result. 
heatpumpingtechnologies.org
+1

SPH’s AHEAD arrangement receives approximately 70°C water from another heat pump. The top heat pump and MVR performance cannot be assigned to the complete ambient-source system. 
spheat.de
+1

Ecop’s integrated rotary construction and Enerin’s Stirling field work are substantive alternatives. Ecop’s stated lift envelope requires additional staging for this duty; Enerin’s shaft-power and source-condition boundaries require conversion to the complete electrical/air-source boundary. Neither is dismissed because it lacks a public matched quotation. 
heatpumpingtechnologies.org
+1

The model therefore retains favorable conventional sensitivities, including COP 2 at $650,000 installed. These are budget challenges rather than product claims. Such a case costs about $31.88/MWh under its explicit service assumptions. Merely reaching COP 2 and $500/kW would not automatically establish 25% savings against it.

Fuel and carbon sensitivity

At $40 electricity and no added carbon price, the paid gas-boiler model costs:

$23.59/MWh heat at $15/MWh LHV fuel.
$34.34/MWh at $25 fuel.
$50.47/MWh at $40 fuel.

Direct gas emissions use 0.20196 tCO₂/MWh LHV; upstream methane is excluded. 
V2_Ch1_Introduction_Final.doc

At $40 gas, zero-carbon electricity and an additional $100/tCO₂ charge, the candidate becomes about 32% cheaper than gas alone. Conventional MVR remains cheaper than the candidate, so this does not establish the required strongest-alternative advantage.

At the modeled complete electricity consumption, operational carbon parity with the gas boiler occurs near 0.42 tCO₂/MWh of grid electricity. Carbon charges must only be added when absent from the energy tariff.

9. The nominal 10 kW unit and cold campaign

The small unit is sized independently. It has a 12 kW nameplate to provide production headroom for a nominal 10 kW campaign:

One hour startup.
Ninety-eight hours accepted production.
One hour restoration.
Required accepted production rate: 10.2041 kW.

Its stroke is approximately 57 mm, with 12 mm rods and bores decreasing from roughly 145 mm to 37 mm. It uses separate small-machine efficiency assumptions. Surface losses, packing friction, controls and laboratory access do not scale down in proportion to heat output.

Small vacuum compressor hardware exists, including relevant Roots-machine flow ranges. It does not supply all later pressure stages or the required complete efficiency. 
atlascopco.com

Campaign quantity	Modeled result
Accepted net-added heat	1,000.0 kWh
Hot inventory raised from cold	6.319 kWh thermal
Startup electricity	7.153 kWh
Shutdown and residual debit	0.310 kWh
Separate test/load-loop auxiliaries	8.000 kWh
Production-point COP	1.495
Total electricity	684.507 kWh
Campaign COP	1.461

The more favorable small-unit qualification bundle still imports 584.09 kWh.

The startup/restoration calculation integrates finite heat capacity and a cooler limited to 15 kW. Residual ending heat is explicitly debited. It is a lumped-enthalpy calculation; full pressure equalization, oil return, films and restart control have not been demonstrated.

Complete prototype budget
Scope	US$
Ambient source and ammonia equipment	29,400
Steam train, drive, hot interface, water equipment and dwell vessels	63,500
Load condenser and cooldown connections	10,000
Electrical, thermal, mass, quality and optical metrology	30,000
Controls and matched-control conversion	8,000
Engineering, fabrication and pressure testing	82,500
Commissioning, access, operators, fluids and disposal	23,000
Contingency	49,280
Total	295,680

There is no laboratory performance result to report. This is a priced research construction, and the current model predicts that it would fail the requested energy limit.

10. What a decisive experiment must establish

The decisive measurement is accepted steam heat divided by all common-meter electricity, across the entire cold campaign.

The paid test would:

Begin with documented cold water, ammonia, oil, pressure and control-energy inventories.
Record common-meter and branch electricity, crank torque/speed, cylinder pressure, injection flow, temperatures and droplet distributions.
Measure accepted steam using mass, actual return enthalpy and independent load calorimetry.
Measure dryness and contamination through calorimetry and representative sampling; reject off-spec production.
Restore or debit every inventory within the 100-hour boundary.
Compare against competently tuned interstage injection, sharing the same source, water boundary and meters.
Demonstrate an actual cassette replacement, including cooling, fluid recovery, paid labor, rejected output and restart energy.

A COP estimate of exactly 2.00 would not be a pass. Measurement uncertainty must leave the upper import bound at or below 500 kWh and the lower accepted-heat bound at or above 1 MWh.

A successful test could establish the coupled conversion, phase quality, inventory behavior and service access at that scale. It would not establish industrial compressor maps, billions of valve motions, outdoor exchanger life or 200-unit manufacturing yield.

The remaining problem is consequently specific: the proposed in-cylinder phase-transfer mechanism has not supplied enough whole-system benefit to pay for its machinery and service. Reaching the target requires a substantial, jointly supported reduction in conversion loss, installed equipment and recurring renewal cost. The present construction supplies no such demonstrated advantage, and it does not resolve the earlier electricity-storage endpoint.

## Available expanded top-level activity

heading "You said:" [level=4]
    - generic: "Invent an economical heat amplifier that turns electricity and ambient heat into useful200C industrial steam, with a manufacturable low-loss conversion mechanism and a complete paid operating cycle. Can a new pressure/phase/heat-transfer or regenerative mechanism produce this useful heat at materially lower full cost than the strongest applicable existing technology? Develop the complete operation. Vapor compression, cascades, Stirling heat pumps, mechanical vapor recompression, liquid injection and heat recovery already exist; their names or an ideal Carnot cycle are not the invention. You may choose any working fluid, chemistry, mechanical or other representation that supplies the stronger real operation. The reference industrial output is1MW of NET ADDED useful heat delivered as dry saturated200C steam at its corresponding saturation pressure, with dryness at least99.5%. Define actual pressure, enthalpy, water quality and acceptable contamination. The input is a specified90C liquid-condensate return stream. Measure useful heat as m*(h_steam,out-h_return,in), with treatment, makeup, blowdown, pumps, pressure changes and rejected heat accounted for. Returned-water enthalpy is an INPUT and is not newly produced heat. Any extra hot return consumed as a heat source is a separate paid resource and cannot count as ambient heat. If the installation supplies or reheats that90C input, pay the operation explicitly and recompute the complete boundary. Give the same declared return stream to every comparator. The only low-grade external heat source in the reference case is ambient air at15C/60%relative humidity/approximately1bar. Construct actual source flow, exchanger, fans, source-fluid circuit, water/condensate and every pressure/thermal inventory. No warm industrial-waste stream, free source heat pump, initially hot matrix, ideal phase separator or infinite isothermal bath is supplied. Also evaluate5C and35C ambient conditions, part load and seasonal operation at a plausible industrial location. Target complete grid-side heating COP>=2.0 at the reference condition: useful net-added steam heat divided by ALL imported electricity, including compression/actuation, fans, pumps, motors, conditioning, heating, controls, phase handling, startup and restoration. Beyond the declared return-water input, only grid electricity and the specified ambient stream may supply net operating energy. Cyclic chemistry is allowed if its regeneration is paid inside that boundary; consumed fuel cannot supply the endpoint. Construct a nominal10kW unit and a cold100-hour campaign producing at least1MWh net-added accepted steam heat with at most500kWh imported electricity; size any production headroom and startup power honestly. Initial stored heat, pressure, batteries and working-fluid inventories must be returned or explicitly debited. Give laboratory performance and first-build cost separately from the industrial plant. At1MW, target all-in repeat-installed capital<=US$500/kW useful heat and complete heat cost<=US$35/MWh at US$40/MWh electricity,90%utilization,20-year finance and8%real discount. Evaluate US$80/MWh and60%utilization separately. Include real production quantity, factory tooling/yield/labor, all heat/mass-transfer surfaces, pressure machinery, working-fluid preparation, grid connection, building/pipe integration, metrology, service, replacement, refrigerant loss/treatment, outages, waste and retirement. The finance horizon grants no20-year compressor, valve, seal, lubricant or heat exchanger life. The reference15C cost calculation is not automatically an annual seasonal result. The full invention must also establish a consequential matched advantage: at least25%lower complete heat cost than the strongest technically applicable competent alternative at the same source, return/output steam, scale, utilization and energy boundary, with uncertainty and relevant carbon/fuel sensitivities exposed. Compare advanced existing heat pumps and paid cascade/MVR combinations as well as resistance and gas boilers. Missing public supplier costs are not evidence of an expensive comparator. If an existing machine already supplies the operation better, credit it rather than relabel it as the new mechanism. Your pressure-gas construction supplies actual useful machinery: direct opposed displacers avoid a constant-pressure throttling error, pressure-dependent plate geometry couples heat capacity to flow, and the finite thermal/valve/line/species/battery/service ledgers expose real operations. Its conditional68.03%AC model still requires US$12.371million and US$742/MWh, with unqualified wet-temperature/startup/life boundaries. Even FREE initial capital leaves aboutUS$192.54/MWh on its unchanged service/charging ledger. That is not a negative for all storage. This new heat-output question does not answer the old electricity-storage endpoint. Reuse the pressure/phase/finite-heat/inventory/manufacturing machinery where it helps, without transferring its maps or material life to hot refrigerants. Two concrete existing hardware starting points: AtmosZero Project68 supplier sheet, September2025: https://heatpumpingtechnologies.org/content/uploads/sites/81/2026/01/supplier56atmoszero20250926.pdf Its supplier-marked measured COP1.73 uses12->9C source and90->150C sink;2.04 uses35->32C source. Some other rows are calculated. The reported165C field arrangement adds MVR. Its600--1000EUR/kW investment range excludes integration, and expected life is not observed component life. The sheet explicitly lacks third-party validation. It is a real bounded industrial construction, not a supplied15C-to-200C saturated-steam machine or quotation. SPH ThermBooster Project68 supplier sheet, September2025: https://spheat.de/neu/wp-content/uploads/2026/03/supplier7sph20250926.pdf Its tabulated COPs are calculated. The AHEAD example receives70C water from another heat pump, generates120C steam, and uses a separate compressor to reach184C. The quoted stage COP is not the entire ambient-to-steam COP. High-temperature piston/lubrication/cascade manufacture is a useful construction, but a possible200C envelope or a20-year financial/service statement does not establish the new coupled point. Give existing technologies their competent actual strengths. Optional independently derived contracts: - With INTRODUCED rounded cp=4.18kJ/kgK and latent heat1940kJ/kg,90C liquid to saturated200C steam adds2399.8kJ/kg and5.20619kJ/kgK entropy. Against15C ambient, ideal reversible work is899.64kJ/kg and perfectly glide-matched COP2.6675. One MW corresponds to.4167kg/s steam; its incoming90C water carries130.64kW sensible heat above15C that is NOT credited as newly delivered heat. Replace these surrogates with actual phase properties and complete enthalpy balances. - A single205C hot level and10C evaporation level have reversible COP2.4521 before real losses. The COP2 target allows500kW/MWheat, only92.18kW above that ideal cycle. Introduced30kW auxiliaries and96%motor efficiency leave43.38kW shaft irreversibility above the ideal work. Neither those approaches nor an efficient motor/compressor is supplied. Changing the heat-delivery temperature glide can alter the bound at its real equipment cost. - An INTRODUCED dry-sensible500kW air-source duty from15C to11C against10C evaporation needs125kg/s air, UA201kW/K and about5030m2 effective area at an introduced40W/m2K. At100Pa/60%fan efficiency it already needs17.36kW fan power. Humidity, films, frost/defrost, fins, pressure drop, fouling and noise are additional coupled geometry problems, not independent favorable constants. - For two heat pumps, whole inverse COP at the top-output boundary is1/COP_top+(1-1/COP_top)/COP_bottom. Introduced4.4 and3.0 give2.0625 BEFORE any further MVR or other operation. This is not a measured performance claim for either supplier. Any steam-mass/enthalpy change or injection requires the complete new ledger. - At the500USD/kW capital/COP2 targets and90%use, the35USD/MWh reference heat target leaves about67334USD/year for ALL service, labor, replacements and removal after power and capital recovery; at60%use,about27914USD/year. Cheap heat surfaces alone do not supply that entire factory/service operation. Discover the physical mechanism that closes these coupled work, flux, quality and manufacture requirements. A possible opening is phase-change heat transfer or temperature-glide recovery integrated with a pressure converter, reducing a large cycling solid matrix. That remains a hypothesis: liquid injection can change composition, valve behavior, erosion, entropy and the temperature at which heat is actually useful. Lower compression work is not automatically useful200C heat. Other mechanisms and representations remain open; no regenerator effectiveness, special fluid, perfect separator or free control is granted. Construct actual component geometry, material/working-fluid states and preparation, compression/expansion or reaction paths, electrical interface, phase separation, steam generation, lubrication/sealing, startup/shutdown, finite source/sink exchange and repeated maintenance. Resolve water/refrigerant/species carryover, local temperatures, pressure drops, stability, degradation and useful output simultaneously. Do not multiply peak component efficiencies or transfer a warm-source catalogue COP across a much larger lift. Build and execute a complete engineering and lifetime-cost model anchored to obtainable components and actual governing behavior, with new joint physical claims labeled honestly. Identify the operation and matched advantage actually supplied, rather than only a target or design optimization. Design a smaller decisive experiment for later execution with actual preparation, itemized costs, common-boundary calorimetry/electricity, phase/quality measurements, inventory restoration and a competent matched control. A proposal, high outlet temperature, unclosed hot stock or isolated compressor efficiency alone does not answer the full invention question. Failure of one route is not an all-heat-pump obstruction. The suggested papers and supplied premises are starting points, not a limit on your research. You may read them, seek additional papers, literature, available Astra work or other sources, change mathematical representations, introduce different ideas and methods, and challenge my framing while pursuing the full question. You choose your sources and approach without further permission. you may use all subagents avaible"
    - button "Show less" [expanded]:
      - generic: Show less
    - button "Copy message":
    - button "Share prompt":
    - button "Edit message":
    - button "Worked for 88m 29s" [expanded] [active]:
      - generic: Worked for 88m 29s
    - paragraph: I’ll treat this as a new heat-production problem and establish the steam, return-water and ambient-air balances first. I’ll develop the conversion mechanism alongside a competent heat-pump/MVR comparison, so any claimed advantage comes from the complete operating cycle and installed cost.
    - generic: Ran command
    - region "Subagent activity":
      - button "Heat cycle mechanism"
      - text: ","
      - button "Heat incumbents"
      - text: and
      - button "Heat hardware cost"
      - text: started working
    - generic: Searching 2 websites
    - paragraph: Defined 90°C return state
    - paragraph: Estimated direct-steam sizing and calculated pressure rise
    - paragraph: Evaluated staged steam compression
    - paragraph: Compared cycle options and estimated pentane cycle flow
    - region "Subagent activity":
      - button "Heat cycle mechanism"
      - text: ","
      - button "Heat incumbents"
      - text: and
      - button "Heat hardware cost"
      - text: updated
    - paragraph: Evaluated cyclopentane cycle
    - paragraph: Explored the wet-compression cycle
    - generic: Ran command
    - paragraph: Developed differential two-phase pistons and refined paired Stirling cycle
    - paragraph: "The steam balance is now fixed: at 200°C, saturation pressure is about 15.55 bar absolute, and the plant needs roughly 0.414 kg/s of steam for 1 MW of added heat from the declared 90°C return. The reversible limit is about COP 2.67 at 15°C ambient. That leaves a demanding loss budget, so I’m checking both compression losses and the cost of moving enough heat through finite exchangers."
    - generic: Searched 28 websites
    - region "Subagent activity":
      - button "Heat cycle mechanism"
      - text: updated
    - paragraph: Prepared prototype test boundary
    - paragraph: Compared uncertain cost ranges
    - paragraph: Estimated MVR power demand
    - paragraph: Compared paired chamber pressures and hot-piston seals
    - paragraph: Evaluated direct contactor
    - paragraph: Compared air-contact designs
    - paragraph: Explored regenerative heat pumps
    - paragraph: Explored direct-contact refrigerant transfer
    - paragraph: Checked ammonia-water cycle losses and compressor heat recovery
    - paragraph: Assessed osmotic expander design
    - button "Ran a command, searched the web"
    - generic: Ran a command, searched the web
    - paragraph: Evaluated heat-pump designs and estimated rotor manufacturing costs
    - paragraph: Evaluated staged gas designs
    - paragraph: Checked water-piston heating and stability
    - paragraph: Estimated coating thermal response
    - paragraph: Refined vane-compressor heat paths
    - paragraph: Locked compressor design
    - paragraph: Checked rotor stress limits
    - paragraph: Evaluated heat-pump concepts
    - paragraph: Compared candidate-fluid performance
    - paragraph: Compared refrigerant candidates
    - paragraph: Awaited missing price input and checked saturated-steam COP
    - paragraph: Evaluated six-stage compressor design
    - paragraph: Sized stage chambers
    - paragraph: Evaluated preflash atomization
    - paragraph: Modeled film heat balance
    - paragraph: Explored centrifugal wet compression
    - paragraph: Tested the coupled physics model and clarified compressor operation
    - paragraph: Inspected heater-flow data
    - paragraph: Compared compressor architectures and evaluated hot-water recirculation
    - paragraph: Compared steam-engine configurations
    - paragraph: "The literature narrows the novelty claim: continuous water-injected steam compression and rotating heat-transfer compressors already exist. The promising opening would need a specific improvement in losses, manufacture or service. So far, the water-injected route reaches COP 2 only under demanding compressor assumptions, and the source-exchanger geometry materially affects both fan power and capital. I’m resolving those together rather than treating either as a fixed allowance."
    - region "Subagent activity":
      - button "Heat hardware cost"
      - text: ","
      - button "Heat cycle mechanism"
      - text: and
      - button "Heat incumbents"
      - text: updated
    - paragraph: Modeled a possible mechanism and evaluated cycle alternatives
    - paragraph: Researched ultrasonic atomization feasibility
    - paragraph: "The strongest conventional route is closer to the target than the supplier examples alone suggest: a properly sized ammonia stage followed by steam compression models near COP 1.9. Distributed water injection could reduce the remaining work, but droplet evaporation must finish during the compression stroke. I’m checking that constraint alongside manufacturing and service costs; it could decide whether the proposed improvement is useful."
    - button "Read files, searched the web"
    - generic: Read files, searched the web
    - region "Subagent activity":
      - button "Heat cycle mechanism"
      - text: updated
    - button "Read files, searched the web"
    - generic: Read files, searched the web
    - paragraph: Formulated and refined the compression balance ODE
    - paragraph: Checked staged-compression model
    - region "Subagent activity":
      - button "Heat hardware cost"
      - text: updated
    - button "Read files, searched the web"
    - generic: Read files, searched the web
    - paragraph: Sized steam-train geometry
    - button "Read files, searched the web"
    - generic: Read files, searched the web
    - paragraph: Built model configuration and implemented humidity model
    - paragraph: Reconciled return-stream heat budget and set makeup resistance power
    - paragraph: Refined the cycle heat balance
    - paragraph: Sized the 750 kVA plant
    - paragraph: Analyzed compressor service life
    - paragraph: Compared matched BOM costs and estimated film heat capacity
    - paragraph: The cost target is now the larger gap. The first complete budget is about $1.3 million for a 1 MW plant, including paid space, electrical connection, the ambient-air exchanger and component replacements. Commercial all-aluminum ammonia coils offer a credible way to reduce that budget, but the modeled saving is about $50,000. Even a hypothetical $500,000 plant at COP 2 saves only about 8% against a competitive conventional heat-pump scenario, so the required 25% advantage still needs a substantial, demonstrated improvement.
    - region "Subagent activity":
      - button "Heat incumbents"
      - text: updated
    - generic: Searched for Read agent code, patched scripts, and ran heat storage installation
    - paragraph: Tabulated startup heat loads and set initial vessel state
    - paragraph: Calculated ammonia inventory and electrical stock preheating
    - paragraph: Modeled small-machine cases
    - paragraph: Checked steam-bore stability
    - paragraph: Estimated demister capture
    - generic: Read files
    - paragraph: Checked wall-model assumptions
    - region "Subagent activity":
      - button "Heat cycle mechanism"
      - text: updated
    - paragraph: Prepared package layout and designed model settings
    - paragraph: Refined steam-loss compensation
    - paragraph: Estimated boiler heat losses
    - paragraph: Checked energy residual and derived ledger closure
    - paragraph: Refined pump heat accounting
    - button "Edited a file"
    - generic: Edited a file
    - region "Subagent activity":
      - button "Heat hardware cost"
      - text: finished
    - paragraph: Separated ambient heat streams and defined thermal stock
    - region "Subagent activity":
      - button "Heat hardware cost"
      - text: updated
    - button "Ran a command"
    - generic: Ran a command
    - region "Subagent activity":
      - button "Heat cycle mechanism"
      - text: updated
    - paragraph: Calculated final cost totals
    - paragraph: Prepared two-stage report with prototype costs
    - paragraph: Separated first-unit cost bases
    - paragraph: Checked cylinder geometry
    - button "Read files, searched the web"
    - generic: Read files, searched the web
    - paragraph: Implemented startup/cooldown integration and residual heat accounting
    - paragraph: Setting lumped thermal parameters
    - paragraph: Checked cooling calculations
    - region "Subagent activity":
      - button "Heat hardware cost"
      - text: and
      - button "Heat incumbents"
      - text: updated
    - paragraph: Calculated ammonia inventory
    - paragraph: "The first integrated model is just below COP 2, and the mechanical audit has identified additional hardware it needs: finite evaporation time requires several cubic metres of interstage vessels at 1 MW. Those vessels also add startup heat and service cost. I’m adding them to the budget and cold-campaign calculation. The current 10 kW model misses the 500 kWh limit, so it is not yet a successful design."
    - button "Edited a file, read files, searched the web"
    - generic: Edited a file, read files, searched the web
    - paragraph: Set startup thermal parameters and cooling
    - paragraph: Calculated industrial restart costs
    - paragraph: Fixed replacement service holes
    - region "Subagent activity":
      - button "Heat hardware cost"
      - text: updated
    - paragraph: Updated condenser heat accounting
    - region "Subagent activity":
      - button "Heat cycle mechanism"
      - text: finished
    - paragraph: Applied water-parameter patch
    - paragraph: Added pressure checks
    - paragraph: Checked vessel thickness
    - button "Read files, searched the web"
    - generic: Read files, searched the web
    - region "Subagent activity":
      - button "Heat cycle mechanism"
      - text: updated
    - text: Edited
    - link "01a1ce9f-af79-7622-8b8b-f5cf54c61da9:exec-e9d2bc59-d3f5-4fe5-a895-9207ef14c6c2:exec-e9d2bc59-d3f5-4fe5-a895-9207ef14c6c2"
    - paragraph: Updated comparator cost variants
    - paragraph: Prepared report plots
    - button "Edited a file"
    - generic: Edited a file
    - paragraph: Waited for IAPWS steam quality
    - region "Subagent activity":
      - button "Heat cycle mechanism"
      - text: updated
    - paragraph: Refined factory tooling assumptions
    - region "Subagent activity":
      - button "Heat cycle mechanism"
      - text: finished
    - paragraph: Prepared module copies using example report outputs
    - button "Edited files"
    - generic: Edited files
    - paragraph: Tabulating carbon-grid cases
    - generic: Searching 3 websites
    - paragraph: Prepared the HTML report and defined the new operation
    - generic: Searched for Read heat storage agent source, patched files, and ran full installation
    - paragraph: Updated source-zone data
    - button "Edited a file"
    - generic: Edited a file
    - paragraph: Tested model heat-transfer limits
    - paragraph: Closed process isolation and rejected lab energy meters
    - paragraph: Reviewed emergency trip containment and sized control UPS capacity
    - paragraph: Assessed seasonal frost operation and 1MW resist trim
    - paragraph: Added wet-source calculation
    - paragraph: Derived wet-coil model and checked condensate energy balance
    - paragraph: Prepared wet-model inputs and quantified wet-mode uncertainty
    - region "Subagent activity":
      - button "Heat hardware cost"
      - text: updated
    - paragraph: Reloaded latest source and prepared converter cache
    - paragraph: Checked wall-loss calibration
    - button "Edited a file"
    - generic: Edited a file
    - paragraph: The audits have resolved two more coupled assumptions. Producing the assumed fine spray needs roughly 150 bar water pressure and a larger paid pump, and ammonia suction superheat needs its own finite exchanger section. The model now includes both. These changes keep the industrial estimate close to COP 2, but they do not establish the required capital cost, 25% matched saving or small-unit campaign performance. I’m consolidating the results, code and test design into the final report.
    - generic: Ran command
    - region "Subagent activity":
      - button "Heat hardware cost"
      - text: finished
    - paragraph: Prepared report file and refined cost targets
    - paragraph: Checked Python CPU usage and built inventory geometry
    - paragraph: Checked receiver inventory
    - paragraph: Checked startup water balance
    - button "Ran a command"
    - generic: Ran a command
    - paragraph: Checked inventory consistency
    - paragraph: Calibrated conventional baseline
    - paragraph: Compared conventional COP with interstage superheat settings
    - paragraph: Prepared matched-cost comparison using current price inputs
    - button "Ran a command"
    - generic: Ran a command
    - paragraph: Refined the core manufacturing estimate
    - paragraph: Checked cylinder clearances
    - paragraph: Evaluated double-wall plate design
    - button "Ran a command"
    - generic: Ran a command
    - paragraph: Checked prototype hardware
    - button "Edited a file"
    - generic: Edited a file
    - paragraph: Reformatted and rewrote dense report text
    - paragraph: Verified current files
    - generic: Ran command
    - paragraph: The current construction does not meet the combined targets. Its executed reference case gives a conditional COP of 1.94, about US$1.39 million installed, and US$47.80/MWh of heat. I’m finishing the audit and reproducible model, with particular attention to whether the proposed mechanism offers an advantage over a competent conventional cascade and steam compressor. So far, that advantage has not been established.
    - region "Subagent activity":
      - button "Heat hardware cost"
      - text: ","
      - button "Heat cycle mechanism"
      - text: and
      - button "Heat incumbents"
      - text: updated
    - paragraph: Located the waterproperties definition
    - region "Subagent activity":
      - button "Heat hardware cost"
      - text: updated
    - paragraph: Reviewed report caveats
    - paragraph: Reopened primary references
    - generic: Read files
    - paragraph: "The comparator audit is important here: using the same paid air source, grid connection, site and water-treatment equipment, a conventional staged steam-compression design models heat at roughly US$46.5–47.8/MWh. The proposed in-cylinder injection mechanism offers too little energy saving to offset its added hardware and service burden. The small unit also remains well outside the campaign target: about 685 kWh imported for 1 MWh of accepted steam heat."
    - region "Subagent activity":
      - button "Heat hardware cost"
      - text: updated
    - button "Read files, searched the web"
    - generic: Read files, searched the web
    - paragraph: Prepared the report bundle
    - button "Edited a file"
    - generic: Edited a file
    - region "Subagent activity":
      - button "Heat hardware cost"
      - text: finished
    - paragraph: Updated service allowance
    - button "Ran a command"
    - generic: Ran a command
    - region "Subagent activity":
      - button "Heat cycle mechanism"
      - text: ","
      - button "Heat hardware cost"
      - text: and
      - button "Heat incumbents"
      - text: updated
    - paragraph: Checked output package and modeled lower-cost designs
    - paragraph: "The service audit caught an underfunded item: the renewal allowance for injection tips and thermal face caps was lower than their initial parts cost. I’ve increased it to cover full replacement plus labor and am rerunning the cost ledger. That raises the estimated heat cost; it does not change the COP result. The report also separates what a laboratory test could establish from the lifetime and production claims that would remain open."
    - generic: Ran command
    - paragraph: Loaded README results and checked module dependencies
    - paragraph: Refined net energy balance including lubrication heat
    - region "Subagent activity":
      - button "Heat cycle mechanism"
      - text: finished
    - paragraph: Audited compressor efficiency and flagged untested oil rejection
    - generic: Read files
    - paragraph: Added first-launch total
    - generic: Read files
    - paragraph: Refined the topology diagram
    - paragraph: Checked the power balance
    - paragraph: Verified rotor-cycle calculations
    - paragraph: Rechecked nozzle flow estimates
    - button "Ran a command, searched the web"
    - generic: Ran a command, searched the web
    - paragraph: The final audited estimate is US$48.79/MWh at US$40/MWh electricity and 90% use, after correcting the replacement allowance. The standalone code package now reproduces the reference COP and cost, including checks on the modeled energy balance and finite heat exchangers. I’m saving the report and executable model with the measured evidence, introduced assumptions and unresolved physical claims clearly separated.
    - generic: Ran command
    - paragraph: Declared component averages
    - button "Edited a file"
    - generic: Edited a file
    - paragraph: Saving files to Library.
    - generic: Ran command
    - paragraph: Reviewed calculated values and checked system qualification
    - paragraph: Verified steam-flow ledger and checked steam enthalpy
    - paragraph: Reviewed pressure model and flagged unsupported joint operation
    - paragraph: Prepared validation sources
    - paragraph: Refined prototype cost model and recalculated total
    - 
