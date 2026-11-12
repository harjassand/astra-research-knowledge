# P3 centrate nitrogen recovery — complete available visible return

Source question: `P3_FULL_CENTRATE_TO_CONCENTRATED_NITROGEN_FERTILIZER_INVENTION_PRO_20261113.txt` (13820 ASCII bytes; SHA256 bda762b154908e31443cc8d91b355f87d3439d62a27562193f519f84ef31eb7d).

Source chat: https://chatgpt.com/c/6af4eb36-d13c-83ec-811c-00db062459b3 ; Pro; completed return observed 2026-11-12 16:53 UTC.

Capture limits: user-visible rendered text and expanded top-level activity; math and tables may have rendering gaps. Nested commands, web, files and subagent views were not opened; native final identity, prefix and database bytes are unverified. Linked HTML and ZIP were not collected: original archive identity and transfer eligibility remain unverified under existing holds.

## Available final response

I have not produced a defensible invention that meets your combined requirements. I developed and executed a specific process design, then audited its chemical inventories, water removal, hydraulics and replacement costs. The resulting construction fails the energy and economic targets. Its initially favorable nitrogen-recovery calculation also depends on material states that have not been established.

I would reject this architecture for the requested service rather than describe it as an economical new process.

The complete deliverables are:

centrate_recovery_report.html — process construction, balances, specifications, cost model, comparison and experiment.
centrate_recovery_model.zip — executable Python, numerical results, sensitivities, equipment budget and inventory audit.

The distinction between the favorable calculation and a physically qualified operation is consequential:

Test	Result from the developed construction
Nitrogen in the favorable reference calculation	4.613 kg potential product N from 4.960 kg admitted TAN, or 93.0%
Additional guard-medium and retained-liquid inventory scenario	4.147 kg potential product N, or 83.6%, before checking the resulting sodium contamination
Favorable cold-campaign energy calculation	46.24 kWh, or 10.02 kWh/kg potential product N
Ordinary pressure-pump/letdown RO implementation	Approximately 73.05 kWh, or 15.84 kWh/kg at the favorable nitrogen yield
Favorable industrial installed budget	$5.10 million, before qualifying the unresolved operations
Favorable industrial gross service cost	$9.96/kg N at $80/MWh and 90% utilization
Demonstrated product qualification, lifetime or 30% advantage	None

No physical experiment was performed. The reported masses are model outputs, not measured accepted fertilizer.

1. The operation I constructed

The candidate is four-compartment electrodialysis metathesis using purchased neutral sodium sulfate, followed by hardness control, reverse osmosis and a separate concentration finish.

The proposed operating improvement is to keep the extracting centrate near pH 8 with metered CO₂ while keeping the sodium-rich counterion return separate until nitrogen extraction is complete. This avoids deliberately adding the replacement sodium back into the feed-facing extraction circuit.

The principal chemistry, for the bicarbonate portion of the feed, is:

2
 
N
H
4
H
C
O
3
+
N
a
2
S
O
4
→
(
N
H
4
)
2
S
O
4
+
2
 
N
a
H
C
O
3
.
2NH
4
	​

HCO
3
	​

+Na
2
	​

SO
4
	​

→(NH
4
	​

)
2
	​

SO
4
	​

+2NaHCO
3
	​

.

That reaction recovers previously fixed nitrogen. It does not synthesize ammonia.

A repeating unit contains these four liquid compartments:

Compartment	Ion movement	Destination
Centrate diluate	NH₄⁺ and competing cations leave through a cation-exchange membrane; dirty anions leave through an anion-exchange membrane	Depleted liquor
Product	Receives feed cations and sulfate	Guard, RO, concentration, qualification
Sodium-sulfate donor	Supplies sulfate to product and sodium to the separate return	Replenished with purchased salt; water makeup and bleed measured
Segregated return	Receives sodium, bicarbonate, chloride and other feed anions	Mixed with depleted liquor after extraction

The complete liquid organization is:

The chemical saving is real, but it is a substitution

This arrangement avoids using one full equivalent of bulk NaOH merely to release ammonia. It substitutes a different chemical requirement:

Ideal sodium-sulfate consumption: 5.0705 kg Na₂SO₄/kg N.
Ideal sodium addition to the returned liquor: 1.6413 kg Na/kg N.
Executed reference, including competing ions and purges: 6.278 kg purchased Na₂SO₄/kg potential product N.

The sodium sulfate is consumed feedstock. It is not a regenerating mediator.

The end electrodes use isolated sulfate rinse circuits. Their small hydrogen and oxygen streams are vented separately. After gas separation, the electrode-generated acidity and alkalinity can be recombined to restore the rinse. Their terminal voltage, gas production, water consumption and handling remain inside the ledger.

What is—and is not—new

Electrodialysis metathesis, selective membranes, segregated compartments, RO and ammonia recovery are established. The proposed CO₂/speciation control is an operating hypothesis that could improve this particular arrangement. It is not sufficient to claim a new economical nitrogen-recovery mechanism.

Published ED work supports the importance of competing cations and the increasingly unfavorable removal tail. Kaniadakis and colleagues’ study explicitly examines simulated reject-water compositions; its membrane-selection results do not establish this complete real-centrate operation. 
PubMed

Likewise, Reyes Alva and colleagues provide valuable real-liquor evidence for membrane contactors, UF and repeated cleaning. Their reported 23.2 g N/L product and particular pilot energy consumption do not supply the requested concentrated, low-cost plant. 
mdpi.com

2. Actual feed, attainable materials and dimensions
A real source, without inventing a site assay

I selected fresh municipal-sludge centrate at Luggage Point Resource Recovery Centre, Brisbane, before recovery-only pretreatment, as the proposed physical source. Its operating sidestream treatment is documented at a relevant scale, with ammonium removal exceeding 90%. That also makes it an important competent alternative. It does not provide permission to sample the stream or free access to its facilities. 
info.awa.asn.au

A future campaign would require a paid collection agreement and measured fresh batches. The design uses a covered 1,200 L balance tank, approximately eight 620 L batches, and a target residence below four hours. On-site pH, temperature, EC, dissolved gases and alkalinity must be measured before storage or aeration changes the feed.

The following numerical reference is introduced and charge-balanced, not presented as measured Luggage Point water:

Quantity	Reference
TAN	1,000 mg N/L
pH and temperature	8.00 and 25°C
Alkalinity	70.0 meq/L = 3.50 g CaCO₃/L
Na / K	150 / 100 mg/L
Ca / Mg	100 / 50 mg/L
Chloride / total phosphorus	500 mg Cl/L / 50 mg P/L
Dissolved inorganic carbon	753.5 mg C/L
Sulfate	185.6 mg/L
Acetate	200 mg COD/L equivalent
Other COD / total COD	800 / 1,000 mg/L
TSS	400 mg/L
Organic nitrogen, separate from TAN	60 mg N/L
Conductivity screen	8.08 mS/cm

The code solves inorganic carbon from alkalinity and sulfate from electroneutrality. If a sensitivity requires additional sodium to maintain a physically possible composition, that addition is exposed. It does not combine all independent endpoints while pretending the resulting liquid is electrically possible.

This reference can still be supersaturated with precipitable salts. Charge balance is not evidence of freedom from calcite, struvite or gypsum deposition.

The nominal module

The small construction uses:

40 electrical series repeats, each with 0.4 m² active area.
16 m² total active receiving area and four membrane sheets per repeat.
64 m² active IEM film, with 25% spare area and an explicit 90% assembly yield.
Approximately 0.4 × 1.0 m channels, 0.7 mm deep.
A maximum current density of 80 A/m², corresponding to 32 A through each 0.4 m² cell.
A 1.5 kW isolated DC supply, low-pressure circulation and differential-pressure interlocks.
A 100 µm screen and approximately 4 m² of small pressurized UF, with paid backwashing and reject collection.

The proposed membrane choices are commercial CIMS-type monovalent CEM, a commercial donor CEM and FAS-PET130-type AEMs. They would be purchased, cut, inspected, conditioned in measured nitrogen-free stock, assembled into PP frames with EPDM seals, and leak-tested.

Their desirable properties cannot be combined by assumption. Measured low hydraulic permeability in one membrane does not establish the same permeability in a more selective membrane. Xu and colleagues’ water-transport measurements show that commercial IEM choice can substantially change osmosis and electro-osmosis, but their conditions do not qualify this centrate/sulfate combination. 
PMC

Real liquid inventories

The product channels alone hold about 11.2 L. A two-litre receiver would therefore have been physically inadequate.

The revised construction pays for:

25 kg nitrogen-free product-circuit water per batch;
75 kg separate-return water per batch;
a 100 L donor stock at 7.5 wt% Na₂SO₄, containing 8.025 kg salt and 98.975 kg water;
two electrode-rinse stocks totaling 10 L.

The donor is replenished with dry salt and measured water. If osmosis dilutes it, the model produces a salt-bearing bleed. A fixed small purge is not imposed independently of its water balance.

Product-side hardware

A roughly 18 L lead/lag aminophosphonic resin guard is proposed to remove hardness before concentrated sulfate deposits in the product circuit. AmberSep IRC747 is a real brine-hardness resin; its behavior in this ammonium-rich fertilizer matrix remains unqualified. 
dupont.com

The RO pressure system is separate from the ED stack. DuPont’s XUS180802 provides an actual 2.5-inch, 2.0 m² element rated to 120 bar through 30°C. Its rating falls to 103 bar at 35°C. A generic “120 bar” description therefore cannot establish the 35°C operating case. 
dupont.com

The finishing stage is a closed 45°C vacuum vessel with a condenser, vent catch, measured condensate and electric heating. The industrial version has a costed vapor recompressor and cleanable heat exchangers.

3. What the executed model actually computes

The supplied code uses finite batch inventories and two-second integration. It includes competing cations, carbonate/phosphate/acetate speciation, a declining limiting current, salt back-diffusion, four water-transfer interfaces, resistance growth, downstream nitrogen loss and a complete reference campaign schedule.

The core transport representation is:

𝑗
≤
min
⁡
 ⁣
[
𝑗
max
⁡
,
 
0.65
𝐹
𝑘
𝑚
∑
𝑖
𝑧
𝑖
2
𝑏
𝑖
𝑐
𝑖
]
,
j≤min[j
max
	​

,0.65Fk
m
	​

i
∑
	​

z
i
2
	​

b
i
	​

c
i
	​

],
𝐽
𝑁
=
𝑡
𝑁
𝑗
𝐹
−
𝑃
𝑁
(
𝑐
p
r
o
d
u
c
t
−
𝑐
f
e
e
d
)
,
J
N
	​

=
F
t
N
	​

j
	​

−P
N
	​

(c
product
	​

−c
feed
	​

),
𝑉
r
e
p
e
a
t
=
Δ
𝜇
𝐹
+
𝑗
𝑅
a
r
e
a
+
𝜂
c
o
n
c
e
n
t
r
a
t
i
o
n
+
𝑉
e
n
d
40
.
V
repeat
	​

=
F
Δμ
	​

+jR
area
	​

+η
concentration
	​

+
40
V
end
	​

	​

.

The reference uses introduced values of:

𝑘
𝑚
=
2
×
10
−
5
k
m
	​

=2×10
−5
 m/s;
effective current utilization 0.94 before ion competition;
divalent relative partition 0.02;
neutral-salt back-permeability 
2
×
10
−
9
2×10
−9
 m/s;
all four membrane resistances and all four liquid-channel resistances;
cumulative fouling and resistance growth across batches.

These are constitutive assumptions to test, not simultaneous measured performance.

The computed average current density is only about 24 A/m², substantially below the initial 80 A/m² ceiling. Deep removal spends time in a dilute, competing-ion tail. That is why thousands of square metres emerge at industrial scale.

For each membrane interface, water transfer is calculated from signed osmosis plus electro-osmosis. Feed level is maintained with purchased polished makeup. Return concentration rises as it collects ions. Product concentration follows its actual water and salt inventory.

Concentration is a separate physical duty

The revised ED receiver reaches only approximately 1.2 wt% N.

Binary ammonium-sulfate activity data imply an osmotic pressure around 82 bar at 4 wt% N and approximately 125 bar at 5.5 wt% N at 25°C. These are calculations based on primary activity data and the published thermodynamic assessment, rather than ideal van’t Hoff estimates at these concentrations. 
Springer Nature Link
+1

The model then introduces:

a mixed-salt osmotic multiplier of 1.18;
a concentration-polarization factor of 1.08;
a 3 bar hydraulic allowance.

At 4 wt% N, those leave only about 12.75 bar useful RO driving pressure. A mixed-salt factor of 1.40 eliminates that margin. Consequently, the reference stops RO at 4 wt% N and pays for the remaining concentration to 5.2 wt% N.

RO nitrogen rejection is explicitly finite. Permeate nitrogen goes to treatment; it is not returned to the same product loop while simultaneously being counted as removed water.

Two unresolved operations materially change the answer

First, the hardness guard can itself store ammonium.

Using the model’s nominal capacity basis:

17.46
 
L
×
1.75
 
e
q
/
L
=
30.55
 
e
q
.
17.46 L×1.75 eq/L=30.55 eq.

After the modeled hardness loading, about 24.44 equivalents remain available for other counterions. If 85% of those sites hold NH₄ during regeneration, the guard retains approximately 0.291 kg N and releases approximately 0.478 kg additional sodium toward the product.

That is a test scenario, not a measured affinity. It cannot be replaced with an assumption of zero ammonium uptake.

Second, liquid left in equipment is not delivered fertilizer.

The estimated free liquid in the guard and two litres of 4 wt%-N RO liquor contain another 0.175 kg N. Sending it to cleaning lowers recovery; recovering it requires a measured displacement or rinse operation and additional concentration.

The inventory audit gives:

Guard state and liquid disposition	Potential product N	Recovery of admitted TAN
Negligible extra NH₄ uptake; all useful liquid recovered	4.613 kg	93.0%
Negligible extra uptake; guard/RO wet liquid goes to cleaning	4.438 kg	89.5%
85% occupancy of remaining guard sites; liquid recovered	4.322 kg	87.1%
85% occupancy; wet liquid goes to cleaning	4.147 kg	83.6%

The last case also increases product sodium beyond the chosen buyer specification. Its additional regeneration allowance is approximately 1.515 kg pure HCl and 1.662 kg pure NaOH.

A five-void-volume rinse of the estimated retained liquid would use about 44.9 kg water and add about 34.3 kWh of small-scale resistance-finishing duty if sent to product. That addresses free liquid only; it does not regenerate bound ammonium for free.

4. The complete 100-hour reference campaign

The favorable numerical schedule is:

Interval	Operation
0–4 h	Opening inventories, feed/water acceptance, nitrogen-free leach blanks, preparation and feed-derived membrane conditioning
4–approximately 34 h	Eight fresh feed batches with cumulative fouling and metered CO₂
Approximately 12–39 h	Pipelined RO and concentration
Approximately 39–63 h	Whole-lot 24-hour retention qualification at 25°C
Through 96 h	Prebooked analytical panel and release decision
Before 100 h	Delivery of accepted material only; cleaning, stock accounting and thermal shutdown

The eight producer batches are combined into one final product lot. Otherwise the destructive-sample allowance would not support eight independent complete contaminant-release panels.

The favorable nitrogen ledger is:

Destination	kg N
Admitted TAN	4.960000
Potential accepted product, conditional on all gates	4.612980
Pretreatment reject	0.047600
Feed characterization samples	0.002000
Depleted main liquor	0.121400
Membrane reset liquor	0.053071
Final membrane residual	0.000267
Miscellaneous product-polishing reject	0.014207
Gas/condensate catch sent to treatment	0.012400
RO permeate	0.011378
Destructive product samples	0.080000
Storage-loss allowance	0.004698

The code closes that stated ledger numerically. The additional guard and retained-liquid scenarios above are mandatory qualifications to it.

The reference includes 0.2976 kg organic N separately. It is assigned to returned liquor, solids, samples and measured carryover. None is presumed converted into fertilizer ammonium.

Cold-campaign energy
Duty	Favorable screen, kWh
Complete ED electrical input after rectification	6.865
Favorable RO pressure-work calculation	2.316
Electric concentration heating	22.963
Vacuum, pretreatment, circulation, controls, preparation, cleaning and hold	6.098
Allocated physical analytical energy	8.000
Total	46.242

Removing the entire analytical allowance still leaves 8.29 kWh/kg potential product N. The failure is not attributable merely to research assays.

There is a further hydraulic qualification. Low net RO pressure work and a low concentration-polarization factor cannot coexist without an actual pressure-balanced circulation arrangement or a purchased recovery device.

An ordinary implementation—pumping approximately 0.30 m³/h through the 2.0 m² element and throttling retentate back to an atmospheric tank—pays the pressure work on every pass. Including its cooling fan and nitrogen-free commissioning allowance gives approximately 73.05 kWh for the campaign. The lower-energy circulation arrangement remains an unqualified equipment requirement.

Thus neither electrical bookkeeping nor retained liquid provides a route to the requested 3 kWh/kg.

5. Product qualification and all outlets
Proposed fertilizer use

The declared use is controlled dilution and blending for nonfood soil-grown ornamentals or turf, with a hypothetical nursery customer 20 km away.

This is a proposed research acceptance contract. No buyer, agronomic approval or regulatory authorization has been secured.

The target is 5.2 wt% N, equivalent to roughly 24.5 wt% ammonium sulfate before accounting for accompanying salts. The reference also contains sodium and potassium sulfates; it cannot be described as pure ammonium sulfate.

Property	Proposed acceptance condition
Nitrogen strength	5.0–6.0 wt%, nominal 5.2 wt%
Nitrogen speciation	At least 99% of N as ammonium
Sulfate relationship	Total molar SO₄/NH₄ of 0.50–0.62, with charge balance corrected for measured accompanying cations
Free acid and pH	Formal excess H₂SO₄ ≤0.05 wt%; measured pH 4.0–6.5
Organic carbon	≤100 mg/L
Suspended solids	≤10 mg/L; no visible precipitate
Sodium	Proposed Na/N ≤0.20 kg/kg
Chloride	Proposed ≤500 mg/L
Storage	At least 99% N retained over 24 h at 25°C in the actual container

The report supplies provisional buyer-specific limits for Cd, Pb, As, Hg, Cr(VI), Ni, Cu, Zn, Fe and Mn; targeted PFAS, VOC and PAH limits; and pathogen criteria.

These limits require matrix validation. In particular:

bulk nitrogen needs independent TAN and total-N/speciation measurements;
free acid requires titration and ion-balance interpretation;
high salt can compromise trace-organic extraction and instrumental detection limits;
CEMs do not universally block neutral organics;
resin and membrane extractables count toward product TOC;
a final filter does not establish pathogen absence.

The actual combined product would be stored in an opaque, closed HDPE container with an appropriate vent and nitrogen catch. A failed lot goes to a charged treatment outlet.

Water and return streams

The favorable reference requires approximately:

1.421 tonnes polished water, including opening/restored stocks;
1.895 tonnes potable intake at the introduced 75% treatment recovery;
474 kg potable-treatment reject;
276 kg product RO permeate;
27.1 kg evaporator condensate;
28.96 kg consumed sodium sulfate;
0.532 kg purchased CO₂.

The separate ordinary-RO implementation adds its commissioning-water allowance.

Before ancillary rejects, depleted feed plus the segregated return is approximately 5.59 m³. Its TAN is about 22 mg/L, compared with approximately 24.5 mg/L before mixing. The model counts recovered mass, so this dilution is not credited as recovery.

Returned sodium is roughly 1.6 g/L, compared with 150 mg/L in the reference feed. Carbonate alkalinity is largely returned as sodium bicarbonate. CO₂ trimming changes inorganic carbon and pH; it does not create alkalinity.

The declared outlets are:

UF solids and retentate → paid sludge handling;
depleted liquor → the plant’s agreed biological-treatment return;
donor bleed, regeneration and cleaning → separately measured equalization and treatment;
RO permeate, condensate and vent catches → measured residual-N treatment;
hazardous analytical residuals → licensed laboratory waste;
spent membranes, resins and filters → charged replacement and disposal.

No credit is taken for destroying COD. Remaining COD, organic nitrogen, salinity and residual chemicals remain plant-treatment loads. If the receiving plant cannot accept the sodium or contaminants, this outlet fails and a different paid disposal route is required.

At 35°C, temperature limits require actual cooling. At 15°C, returning the liquor at at least 20°C requires purchased heating after any physically available process-heat transfer. Neither case receives free waste heat.

6. Industrial cost and the strongest relevant alternatives
Favorable factory budget

The industrial calculation uses:

1,000 kg potential accepted N/day nameplate;
90% accepted-output utilization: 328,500 kg/year;
20-year finance at 8% real discount;
a hypothetical manufacturing quantity of 20 plants/year;
approximately 4,319 m² active repeat area;
approximately 21,596 m² installed IEM film, including reserve area;
approximately 2.52 m³ guard resin;
500 m² RO area;
four 25 m³ product/qualification tanks.

The film area follows the finite removal tail. It is not obtained by assigning the initial peak current to the whole recovery interval.

Cost group	Favorable $/kg N
Capital, working stock and retirement	1.606
Scheduled materials, replacement assembly and service	5.205
Operations, technical labor, QA and site overhead	0.340
Sodium sulfate	1.256
Makeup-water service	0.569
Electricity	0.232
Other reagents and cleaning consumables	0.196
Waste and downstream treatment	0.244
Product delivery, 20 km	0.308
Total	9.957

These are introduced engineering estimates, not vendor quotations. The installed equipment total is approximately $5.10 million, plus $20,000 working stock.

The reference charges recurring membrane-cassette assembly and QA, rather than buying film repeatedly while allowing free rebuilding. Operator allocation is 730 loaded hours/year, with additional technical and scheduled changeout labor. It assumes a shared operating site; a dedicated operator is not supplied.

The financial screen is already poor before the unresolved guard and hydraulic operations are qualified.

Even eliminating every fixed-cost category would leave approximately $2.80/kg N of variable expense at the stated prices. Removing the 20 km product delivery still leaves about $2.50/kg N. Therefore a membrane price reduction alone cannot achieve the requested complete advantage.

Lifetime cannot be granted

The favorable budget assumes:

Component	Introduced service life
IEM film	12,000 operating h
Seals	24,000 h
RO elements	16,000 h
Guard resin	2 years
Structural, power and thermal components	7–12 years

Those are not measured lives.

There is an additional consistency requirement: if the short-run model’s introduced resistance-growth rate of 0.15% per operating hour continued, a 20% resistance increase would occur in only 133 hours. Executing that replacement sensitivity produces a cost near $459/kg N.

That is not a prediction of actual membrane failure. It shows why a post-conditioning plateau or effective restoration must be demonstrated before using the 12,000-hour case. Keeping irreversible growth below 20% over 12,000 hours requires an average slope below approximately 
1.7
×
10
−
5
 
h
−
1
1.7×10
−5
h
−1
.

Matched alternatives

The following are deliberately favorable industrial engineering cases, not matched offers. They use the same raw-feed handoff, fertilizer service, return-treatment obligation, concentration, utilization and 20 km product delivery. Competing processes receive their own efficient water requirements.

Alternative	Installed $M	Purchased process energy, kWh/kg service N	Gross $/kg N
Competent HFMC stripping with bulk conditioning	1.10	1.28	2.49
Heat-integrated vacuum/thermal recovery	1.18	9.13	2.02
Ion-exchange concentration and regenerated capture	1.33	1.78	2.58
ED/BPM concentration and ammonia capture	1.32	4.63	2.44
Efficient PN/A removal plus purchased AS fertilizer	0.98	1.53 locally purchased	2.49

The thermal case pays for 1.13 kWh electricity and 8 kWh heat/kg N at $0.02/kWh thermal. Its low cost does not mean it meets the 3 kWh energy target.

The PN/A case destroys wastewater nitrogen, largely to N₂, and buys a separate fertilizer supply. Nitrate, biomass, residual COD and polishing remain accounted obligations. Its local process-energy figure is not the embodied energy of purchased fertilizer.

Published optimized HFMC estimates also caution against choosing an expensive pilot as the incumbent: converting their reported dry-ammonium-sulfate units gives approximately $1.14–3.50/kg N, although their boundary and feed range differ from this complete service. 
pure.kaist.ac.kr

At the favorable $2.02/kg N thermal-service case, a 30% advantage requires approximately $1.42/kg N. For co-located product use, the corresponding threshold is about $1.20/kg N. These are break-even tests, not claims that a particular supplier will quote those prices.

Sensitivities that destroy the candidate
Change	Consequence in the executed screens
Electricity $40 / $80 / $160 per MWh, 90% utilization	Approximately $9.84 / $9.96 / $10.19 per kg N
60% utilization, same electricity cases	Approximately $10.61 / $10.72 / $10.95 per kg N
Film life 6,000 h	Approximately $14.98/kg N
Film life 24,000 h	Approximately $7.37/kg N
Film $30/m², salt $0.10/kg and 24,000 h life	Still approximately $4.81/kg N
Fivefold transfer coefficient and much higher current, alongside favorable materials	Reduced area, but much greater electrical loss; still fails cost and energy
0.7 g N/L, with more feed admitted to preserve N input	More sodium competition and water duty; proposed product sodium limit fails
High Ca/Mg/chloride/P	Roughly doubled guard duty; sodium and precipitation risks increase
Greater solids rejection and faster organic fouling	Recovery uncertainty margin falls below 90%
Mixed-salt osmotic multiplier 1.40	RO endpoint loses its pressure margin
35°C	Actual RO pressure derating and cooling must be paid
Frequent full resets	Retained-media nitrogen and rinse duty can consume the recovery margin

At 20% load, whole banks should be isolated. Leaving all membrane area wet at low current continues passive osmosis and back-diffusion. Starts, drains, holding and renewed quality acceptance therefore need a real operating strategy.

7. First-build budget and the decisive smaller experiment
First full demonstrator

The introduced first-build budget is approximately $122,000:

Group	Budget
Equipment, fabrication, engineering and contingency	$102,200
First water, reagents, cleaning and disposal	$1,800
Campaign labor, feed acquisition, analytical access and calibration	$17,700
Metered electricity	Several dollars, depending on hydraulic implementation

This is separate from the repeat-plant model. It is not a quotation, and it does not guarantee pressure-equipment availability or analytical turnaround.

The separate first-stock energy screen assigns approximately 1,778 kWh to procured membrane manufacture, including spares and assembly yield, and approximately 2,500 kWh to hardware fabrication. These are exposed assumptions, not supplier environmental declarations.

At industrial scale, the assumed sodium-sulfate preparation energy of 1 kWh/kg salt would add approximately 6.28 kWh embodied energy/kg N every cycle. It cannot be amortized away over twenty years. Its financial manufacturing cost is already contained in the salt purchase price and is not charged again as a second electricity bill.

The smaller experiment

I would not commission the full demonstrator from this evidence. A smaller test should first measure the operations that the favorable calculation cannot supply.

Hardware and feed

100 L fresh, unspiked actual centrate.
Approximately 76 L for repeated candidate runs, with the balance assigned to matched recovery and handling controls.
Ten ED repeats, each 0.025 m²: 0.25 m² active receiving area.
Commercial membranes, approximately 0.4 L receiver fill per 10 L feed, a separately metered return and a finite sulfate donor.
A scaled hardness guard whose initial/final ammonium, sodium and hardness inventories are measured.
Paid access to a suitable pressure-rated RO test system and a small measured concentration vessel.
One actual final product container for the 24-hour test.

Pressure hardware cannot be inferred from an ordinary laboratory filtration cell. Sterlitech lists a 2,000 psi Sepa CFX option at $8,178.12 for the cell, with holder, pressure generation and other equipment additional. Configuration and ratings must be confirmed before use. 
Sterlitech
+1

UQ’s ACWEB laboratory lists external analytical services and relevant nutrient, ion, carbon, metal and gas instruments. That establishes a possible paid service provider, not a booking or free instrument allocation. 
University of Queensland

Measurements

The experiment needs:

common wall-energy metering and terminal voltage/current logging;
independent mass balances on all four circuits;
RO feed, recycle, permeate, concentrate and final hold-up measurements;
thermal input, condenser duty and cooling measurements;
dissolved and gas-phase nitrogen capture;
TAN, total N, organic N, nitrate/nitrite, alkalinity/DIC and all major ions;
product TOC, solids, metals, targeted persistent contaminants and biological assays;
complete membrane and guard elution at reset;
precipitate identification and membrane/resin mass-loss measurements.

An expected potential product signal of order 60–70 g N is many thousands of times larger than a targeted cumulative material/reagent blank below 10 mg N. This is sufficient to test useful recovery, although the full contaminant panel will consume a significant fraction of such a small product batch.

Controls

Run, on split actual feed:

CO₂ control enabled versus disabled.
Segregated-return operation versus an intentionally mixed-return diagnostic.
A competent acid-capture reference.
No-current and nitrogen-free material blanks.
At least three production/drain/reset cycles on the same materials.

A separately labeled 
15
N
H
4
15
NH
4
	​

 control can distinguish feed ammonium from prepared salts or nitrogen-bearing materials. Its added nitrogen must be weighed and charged. The unspiked actual-feed run remains the basis for a native-nitrogen recovery claim.

Numerical decision criteria

The component experiment should require:

measured nitrogen closure within 97–103%;
no unidentified gas or retained-material nitrogen;
achieved 5.2 wt% N product, rather than a concentrated synthetic receiver;
the declared quality panel and at least 99% N retention over 24 hours;
quantified guard ammonium uptake, sodium release and regeneration chemistry;
quantified water transport and actual RO pumping duty;
repeatable restoration without more than 10% loss of useful transfer performance over the defined short test;
at least a 15% reduction in area × operating time per gross recovered N for the proposed CO₂-control operation, without increased rejection, contamination or uncounted chemical consumption.

That last result would establish an incremental operating effect. It would not establish the requested invention.

A genuine process-level pass would still need the ≥90% all-admitted accepted recovery, complete cold energy, capital, gross cost and matched 30% advantage requirements. A 100 L diagnostic cannot establish multi-year life or factory economics.

A realistic small-program allowance is approximately $40,000–55,000 with paid facility access. Buying the full pressure hardware can add another $25,000–35,000. Feed, fabrication, instrumentation, isotope work, matrix validation, operator time and disposal are all part of that allowance.

What this development establishes

The neutral-salt construction solves a real bookkeeping problem: it gives the displaced ammonium counterions an explicit physical destination and avoids pretending that local alkalinity is free. Its proposed CO₂ control also has a testable effect on the extraction tail.

It does not supply the requested economical capability. The favorable case already spends too much on salt, water service and durable transport area. Finite guard inventories, retained liquid, real RO circulation and uncertain material life make the result worse.

A successful invention would have to reduce those coupled burdens together. An isolated voltage improvement, high ammonium uptake, or a cheaper sheet price would not be enough. I have left the failed construction, the executed models and the discriminating experiment available in full, without presenting the missing material properties or operating equipment as accomplished science.

## Visible links in the final

- centrate_recovery_report.html: https://chatgpt.com/library?file_id=libfile_ba69b6a9a72c819196c2fee8a9a8ca4e&account_id=personal
- centrate_recovery_model.zip: https://chatgpt.com/library?file_id=libfile_a59d1d16f8ac8191a5a3778d490b5b1b&account_id=personal
- PubMed: https://pubmed.ncbi.nlm.nih.gov/41864006/?utm_source=chatgpt.com
- mdpi.com: https://www.mdpi.com/2077-0375/15/2/62?utm_source=chatgpt.com
- info.awa.asn.au: https://info.awa.asn.au/water-e-journal/luggage-point-anita-mox-sidestream-treatment?utm_source=chatgpt.com
- PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC13426454/?utm_source=chatgpt.com
- dupont.com: https://www.dupont.com/products/ambersepirc747ups.html?utm_source=chatgpt.com
- dupont.com: https://www.dupont.com/content/dam/water/amer/us/en/water/public/documents/en/RO-FilmTec-XUS180804-and-XUS180802-PDS-45-D01735-en.pdf?utm_source=chatgpt.com
- Springer Nature Link
+1: https://link.springer.com/article/10.1007/s10953-025-01431-w?utm_source=chatgpt.com
- pure.kaist.ac.kr: https://pure.kaist.ac.kr/en/publications/economic-optimization-of-hollow-fiber-membrane-contactors-for-amm/?utm_source=chatgpt.com
- Sterlitech
+1: https://www.sterlitech.com/sepa-cfx-high-foulant-cell-assembly-316-ss-1160356?utm_source=chatgpt.com
- University of Queensland: https://acweb.uq.edu.au/node/2455?utm_source=chatgpt.com

## Available expanded activity

Worked for 117m 4s

I’ll start with a documented real centrate and close its nitrogen, carbonate and charge balances before choosing the recovery mechanism. I’ll develop the plant and cost model alongside the incumbent comparison, so any proposed advantage has to survive pretreatment, product qualification, cleaning and return-liquor treatment.

Centrate feed quality, Centrate mechanisms and Centrate economics started working
Ran a command, searched the web

Estimated post-recovery charge balance

Evaluated acid-gradient separation

Estimated ammonium capture

Evaluated NH3 recovery architecture

Assessed ePTFE membrane geometry

Checked water balance

Checked CO₂ degasser sizing

Checked contaminant transfer bounds and set product limits

Calculated pH and alkalinity

Calculated alkalinity balance

Searched 9 websites

Estimated neutralization heat budget

Explored nitrogen precipitation

Explored closed-loop heat recovery

Refined ammonium sulfate specifications and assessed ammonium selectivity

Assessed ammonium membrane selectivity

Estimated sulfate-acid limits

Two findings are shaping the design. Removing CO₂ can raise pH, but it does not create alkalinity: recovering ammonia consumes roughly one alkalinity equivalent per mole of nitrogen. Also, several reported “concentrated” products are still below 5 wt% nitrogen because water crosses with the ammonia. I’m checking an acid-driven ion-transfer route as well as stripping, to see whether it can avoid those costs without transferring unacceptable contaminants into the fertilizer.

Centrate mechanisms updated
Read files, searched the web

Evaluated WAC pretreatment

Assessed membrane support feasibility

The direct acid-exchange route has a serious bottleneck: as the receiver becomes concentrated ammonium sulfate, its proton-carrying capacity falls, while water still tends to enter and dilute it. A favorable exchange equilibrium does not establish a useful production rate. I’m checking whether a staged process can resolve those two problems with real equipment and still beat an efficient conventional plant.

Centrate mechanisms and Centrate economics updated

Modeled a carbonate process

Read files, searched the web

Explored buffer-drain design

Centrate mechanisms updated
Ran a command, searched the web

Calculated staged membrane area

Searched 20 websites

Evaluated hydrogen recycling

Centrate mechanisms, Centrate economics and Centrate feed quality updated

Selected CEM model inputs

Modeled water-network sources

Evaluated membrane water transport

Modeled candidate CO2 catalysts

Compared membrane support designs

Evaluated sodium sulfate metathesis

The strongest design to carry into the full model is a four-stream electrodialysis arrangement that keeps wastewater anions out of the fertilizer. Its main difficulty is now clear: concentrated product draws in water, and controlling that flow adds membrane area, pressure hardware and maintenance. I’ll include those costs explicitly and compare them with the best conventional cases; the calculation may reject the design rather than validate it.

Centrate mechanisms and Centrate economics updated

Built the EDM model

Centrate feed quality finished

Checked 40-cell sizing

Estimated carbonate pH and compared CO2 supply costs

Sized donor stream conditions

Prepared Python speciation model and balanced return charge

Modeled current allocation

Checked sulfate water activity

Centrate economics and Centrate mechanisms updated

Designed low-pressure form and calculated acid-wash reset

Set the mass-transfer coefficient

Checked calcium sulfate precipitation

Compared hardness pretreatment options

Read files, searched the web
Centrate economics updated
Read files, ran a command, searched the web
Centrate mechanisms and Centrate economics updated

Calculated water balance

Evaluated FKS75 guard sizing

Assessed membrane options

Evaluated NASICON electrode

Centrate feed quality updated

Built an ion-balance model

Set up ion-flux model

Refined the water-flux model

Balanced the RO loop

Centrate economics, Centrate feed quality and Centrate mechanisms finished
Edited a file

A useful limit has emerged from measured ammonium-sulfate solution data: even pure product at 5.5 wt% N has about 125 bar osmotic pressure at 25°C. A 120-bar RO unit therefore cannot finish it. I’ve added a paid evaporation step after partial RO concentration. The design is becoming physically more complete, but membrane replacement and the small module’s heating and analytical duties are eroding its prospects.

Searching 4 websites

Checked the multicell energy model

Ran command

Recalculated guard-bed economics

Refined the sodium ledger

Sized return-liquor cooling

Updated campaign model gates

Set up ionic balances and accounted for shunt current

Implemented ion-state tracking

Edited a file, searched the web

Sized the four-circuit pump

Validated the process model

Edited 01a1d032-450f-73a9-b6eb-4c7028d38106:exec-08c62176-7199-4ef6-b519-213624a83e47:exec-08c62176-7199-4ef6-b519-213624a83e47

Checked helper imports and wrote integrated production code

Estimated industrial energy use

Implemented feed-pH control model

Edited a file

Prepared the salt ledger

Added five hydraulic strips

Ran a command

Extended physics-cost analysis

Calculated contaminant leakage limits

Checked buyer acceptance

Refined the delivered-cost case

Edited a file

Checked the cost breakdown

Planned prototype batch sizes

Refined prototype sampling plan

Budgeted a prototype test cell

Refined the decisive experiment and defined the vendor threshold

Evaluated Na-selective membrane and checked primary evidence

Prepared Luggage Point samples

Added hard-feed parameters

Traced salt-accounting gaps and built an exact salt ledger

Adjusted feed and initial nitrogen accounting

The campaign model now includes competing ions, changing pH, water transfer, concentration, medium reset and the 24-hour hold. It can conditionally recover the required nitrogen mass, but the small module uses about 10 kWh/kg N. The industrial cost calculation also fails by a wide margin once membrane area and replacement are tied to the modeled

Edited a file, searched the web

Prepared product assay checks and estimated chloride carryover

Quantified structural nitrogen

Prepared paired tracer and blank controls

Checked initial and final TKN

Modeled the ED water balance

Updated water-treatment inputs

Prepared the report template and assembled the report bundle

Integrated conditioning mass

Refined energy accounting

Checked process heat-floor feasibility

The executed model now includes first-use membrane loading, cleaning losses, samples, water transfer and product qualification time. It conditionally accounts for enough nitrogen, but the design fails the challenge: the small campaign uses about 10 kWh/kg N, and the scaled plant costs far more than $2/kg N once membrane area and replacement are included. I’m finishing the comparison and prototype criteria so the result shows what would need to change, without presenting the modeled recovery as validated performance.

Ran a command, searched the web

Reviewed current context

I’m checking the final balances against the actual membrane area, product-water removal and replacement schedule. I’ll keep modeled performance separate from measured evidence and make the cost comparison explicit, including favorable cases for established recovery methods.

Ran command
Centrate mechanisms, Centrate economics and Centrate feed quality updated

Reviewed remaining model code

Read files, searched the web

Checked primary references and estimated gas-stripping needs

Updated RO permeate balance and coded explicit paid-N loss

Refined the product-balance model

The final audit found two losses that need explicit treatment: ammonium carried into the RO permeate, and the water used to fill and reset the four liquid circuits. I’m adding them to the ledger. They make the candidate less favorable; neither changes the conclusion that it misses the cost and cold-campaign energy targets.

Centrate feed quality and Centrate mechanisms updated

Refactored the process model and modeled batch product yield

Set donor concentration

Refactored batch loop and updated batch wrapper

Centrate feed quality and Centrate mechanisms updated
Edited 01a1d032-450f-73a9-b6eb-4c7028d38106:exec-72612b62-0cd5-4c4e-940f-593089663a67:exec-72612b62-0cd5-4c4e-940f-593089663a67

Checked water-balance accounting

Reworked campaign water calculations and derived RO concentration balance

Defined four-water topology and checked return-water ion balance

Checked water balance

Edited a file

Checked ion accounting

Centrate mechanisms finished

Refined regeneration volume estimates

Refined industrial scaling model

Centrate economics updated

The revised calculation now tracks water across all four membrane interfaces and includes salt-bearing donor bleed. It predicts about 1.2 wt% N leaving the electrodialysis stage, so RO and evaporation must supply the remaining concentration. The cold campaign is now about 10 kWh/kg N. I’m also charging replacement-cassette assembly and the added treatment water in the factory model.

Edited 01a1d032-450f-73a9-b6eb-4c7028d38106:exec-6cea6066-60fe-41c4-b729-4935a5f45d57:exec-6cea6066-60fe-41c4-b729-4935a5f45d57

Ran integrated campaign

Assessed UF reject concentration

Assessed custom pressure housing

Centrate feed quality updated
Edited a file, ran a command, searched the web

Rechecked flux-area estimates

Tested optimistic costs and audited neutral-organic permeation

Edited a file, searched the web

Checked process heat balance

Added MVR sensible heat

Edited a file

Prepared static report visuals

Read files

The cost model still rejects the design after favorable sensitivity tests. Even with much cheaper membranes, longer life and faster ion transport, the coupled case remains above the cost target and raises electrical losses. The report will include the full balances, the remaining measurement gaps, and a smaller experiment aimed at testing a specific improvement rather than commissioning the failed plant design.

Read files, searched the web
Centrate feed quality, Centrate economics and Centrate mechanisms updated

Checked pump selection

Calculated return-heater energy

Edited 01a1d032-450f-73a9-b6eb-4c7028d38106:exec-1240fc2d-8b6a-4216-84fd-8ca92aa6635b:exec-1240fc2d-8b6a-4216-84fd-8ca92aa6635b

Verified primary source facts and checked bioelectrochemical NH₃ capture

Assessed conditional reactor feasibility

Prepared combined-lot sampling

Planned 100 L prototype

Sized prototype module

Checked model thresholds

Checked nitrogen balance

Refined cost accounting

Checked membrane power sizing

Added Pitzer citations

Checked computed pressure bounds

Compared freeze-process energy costs

Ran a command
Centrate feed quality updated

Gathered primary sources

Audited current source files

Refined feed-sample nitrogen ledger

Edited a file

Checked nitrogen blanks and reagent ammonium contamination

Checked gypsum scaling risk

Sized guard-bed capacity

Checked membrane transport assumptions

Edited a file

Checked report calculations

Calculated current mass values

Validated report syntax

The complete reference campaign now accounts for 4.613 kg N out of 4.960 kg admitted TAN, conditional on quality tests passing. Its modeled process energy is 46.24 kWh; the corresponding industrial estimate is about $9.96/kg N. I’m packaging the design, executable models and prototype plan, with the favorable comparator cases and unqualified assumptions visible.

Read files, searched the web

Added RO cooling constraints

Added nitrogen-free RO wash

Modeled RO flush recovery

Updated the tail-flush timeline

Recalculated RO flush costs

Quantified reverse osmosis holdup losses

Adjusted RO nitrogen balance

Awaited guard-capacity data

Bounded carrier nitrogen state

Checked guard nitrogen balance

Centrate feed quality updated

Added guard fraction parameter

Revised nitrogen recovery model

Edited 01a1d032-450f-73a9-b6eb-4c7028d38106:exec-e0cadd7f-3a39-47fe-b08b-6ca43fad0b96:exec-e0cadd7f-3a39-47fe-b08b-6ca43fad0b96

Refined favorable-case bounds

Rechecked outlet nitrogen balance

A further inventory check materially weakens the recovery claim. The hardness resin may take up ammonium as well as calcium and magnesium, and liquid left in the guard and RO unit cannot count as delivered product. I’ve added explicit bounds: a plausible test scenario lowers potential product recovery from 93% to about 84%, with extra regeneration and sodium release. Recovering that nitrogen would need another paid separation or rinse-concentration step.

Edited 01a1d032-450f-73a9-b6eb-4c7028d38106:exec-dd2fdb69-327e-40f6-9e06-53ed2978583e:exec-dd2fdb69-327e-40f6-9e06-53ed2978583e

Reconciled baseline calculation inputs

Checked RO pump feasibility

Sized the internal pump housing

Quantified pressure-loop duty

Modeled RO circulation

Compared pressure-loop ledgers and defined a conservative RO case

Sized industrial RO pumping

Edited a file
Centrate feed quality and Centrate economics updated

Recalculated full-cycle performance

Edited a file

Prepared ZIP archive and selected archive files

Updated RO area inputs

Applied final report corrections

Edited a file

Separated first-wash accounting

Prepared complete HTML report

Refined nitrogen-loss bounds

Checked nitrogen quality

Checked salt-price feasibility and NaOH sodium restoration

Finalized plant analytical schedule

Edited a file

Validated cost model inputs

Ran final checks

Mapped process topology and revised lifetime cost model

Added aging-failure contract

Refined membrane aging model

Flagged baseline model inconsistency

Edited a file

Prepared native library and archive

Parsed transfer metadata

Read files

Regenerated model inventory

Chose ionic-strength algorithm

Checked stack flux limits

Edited a file

Saved the final artifact package

Recorded membrane reset

Used Library integration, ran commands

Checked source citations

Checked product mass balance

Revised nitrogen ledger and flagged untested operations

Checked file links and energy table

Compiled revised cost table

Reviewed TA2–5 model inputs

Checked Luggage Point data

Refined thermal cost comparisons

Checked process cost
