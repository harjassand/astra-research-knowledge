# P1 air-carbon concentrator: available completed return

Chat: https://chatgpt.com/c/6af4eae7-8470-83ec-bfab-1401d237fac7
Question: P1_FULL_REGENERATIVE_LOW_WATER_AIR_CARBON_CONCENTRATOR_PRO_20261112.txt, posted f488894c-2221-4f0c-ae45-b1cfe5d3f26c. Final: fccc47d6-03ca-5423-9f66-f3bfe40cfecb. Observed 2026-11-11 23:17 UTC; UI Pro, completed, empty composer.

The native response is truncated at 20,000 characters. The remainder is transcribed from rendered UI, with table and mathematical formatting reconstructed where visible; it is not full native/database-byte identity. Visible activity text is excerpted below, not a full expansion of nested activity or helpers. Producer-linked dac_design_and_model.zip has unverified identity/eligibility and was not collected; no linked sources or components were opened.

## Available visible activity excerpts

“I’ll work through the full air-to-product process and test the proposed mechanism against the energy, water, purity and cost limits. I’ll use parallel reviews of the separation chemistry, process engineering and current DAC results, then build an executable balance model and a decisive prototype design.”

“The first useful finding is that the biggest gaps appear at regeneration and product delivery. Recent experiments provide credible capture mechanisms, but several low energy or cost figures exclude the equipment or chemistry needed to close the loop. I’m now checking two complete alternatives: an electrochemical carbon pump with water recovery, and a heat-pump-regenerated solid sorbent. The comparison will include humidification, vacuum duty and the area required at useful rates.”

“Humidity recovery does not currently rescue the electrochemical route: the best low energy result uses very humid air, and meeting your water limit from dry ambient air would require roughly 97–98% water recovery, with substantial exchanger area and CO₂ crossover to account for.”

“The solid-amine route has a clearer water balance, so I’m developing that as the concrete engineering candidate. Its unresolved limits are electricity consumption and cost; I’m keeping those as explicit pass/fail tests rather than assigning optimistic values to make the design pass. I’m using the runtime and file-delivery skills for the executable model and calculation record.”

“The detailed balance has exposed two more consequential limits. First, a small commercial vacuum pump can use several times the entire electrical allowance by itself. Second, resin lifetime can dominate the projected cost even when electricity is cheap.”

“I also found that a relevant kilogram-scale sorbent pilot produced only about 50–55% CO₂ because of leakage. Using its measured working capacity unchanged for your 95% product would overstate performance. The model now accounts for concentrated-product regeneration, finite drying and adsorption rates, temperature rise, and pump flow at operating pressure.”

“The model and independent balance reviews are complete. The engineering candidate misses the energy target: its favorable hardware sensitivity is about 1.46 kWh/kg, while the commercial laboratory-component case is much higher. The cost estimate also misses $100/t, and linking replacement cost to cyclic degradation makes the lifetime requirement particularly demanding.”

“I’m packaging the model, assumptions, results and prototype procedure. I’ll distinguish these candidate-specific failures from what remains possible with a different separator.”

## Exact native prefix

# Result: the full invention target remains unsolved

**I cannot substantiate a new concentrator that meets all of your requirements.** I worked through the chemistry, water recovery, contactors, regeneration, product collection, auxiliary power and economics, and developed an executable model of a concrete engineering candidate. That candidate misses the purchased-energy and cost targets substantially.

The investigation does establish three useful conclusions:

1. **Your targets are not ruled out by thermodynamics.** A failure of the designs examined here does not obstruct every possible separator.
2. **The strongest low-energy electrochemical result I found does not transfer directly to your dry ambient envelope.** Supplying and recovering the required humidity becomes a major operation.
3. **A commercial-amine process provides a physically credible route to regenerated, concentrated CO₂ with low recurring freshwater demand, but its complete equipment and regeneration duties remain too expensive for this contract.**

I have therefore treated this as an **unsuccessful invention investigation with a worked design**, rather than declaring that a promising material calculation solves the problem.

The complete calculation package is here:

**:chatgpt-content-reference{index="16"}[dac_design_and_model.zip](sandbox:/workspace/scratch/6b2ea2175905/dac_design_and_model.zip)**

It contains the executable Python model, all parameter values, eleven scenarios, carbon and water balances, numerical checks, source records, construction details and the proposed experiment. No physical experiment was performed.

---

## 1. What the targets actually permit

At 1 kg/day, the electrical allowance is only

\[
\frac{0.50\ {\rm kWh}}{24\ {\rm h}}
=\boxed{20.8\ {\rm W\ average}}.
\]

That must cover the complete machine. A continuously running 5 W auxiliary consumes almost one-quarter of the allowance.

Using your thermodynamic contract, the ideal separation work at 25°C and 50% capture is approximately

\[
W_{\min}=0.1263\ {\rm kWh/kg}.
\]

Thus the target allows roughly four times the ideal gas-separation work. That is demanding, but physically possible in principle.

The airflow requirement is similarly consequential:

\[
V_{\rm air}\approx 2616\ {\rm m^3/kg}
\]

before accounting for losses between capture and delivered product. At exactly 1 kg/day, this is about **109 m³/hour**. Retained carbon at shutdown, rejected product and collection losses increase the airflow per delivered kilogram.

### The economic allowance is particularly restrictive

For a nominal 1 tonne/day installation at 90% annual utilization:

\[
Q_{\rm year}=328.5\ {\rm tonnes/year}.
\]

A $100/t capture-and-delivery cost allows total annual spending of **$32,850**.

At the maximum permitted electricity and water use:

| Item | Cost per delivered tonne |
|---|---:|
| Electricity: 500 kWh/t at $0.05/kWh | $25 |
| Water: 2 m³/t at $2/m³ | $4 |
| Remaining for equipment, financing, materials, replacement, labour and everything else | **$71** |

With an 8% discount rate, 15-year equipment life, 3% annual maintenance and $10,000/year for shared labour, site and administration, the maximum installed capital is

\[
C_{\max}
=
\frac{328.5(100-25-4)-10{,}000}
{0.11683+0.03}
\approx
\boxed{\$90{,}700}.
\]

That calculation still provides **no separate allowance for sorbent replacement**.

This does not prove that $100/t is impossible. It means that a proposed separator must have unusually inexpensive equipment, high useful productivity and durable active material simultaneously.

---

## 2. What the strongest relevant evidence currently demonstrates

I checked the literature and current company disclosures through **12 November 2026**. I found no publicly documented demonstration establishing the entire specified contract.

The comparisons below preserve the actual output and accounting boundaries.

| Approach | Supported result | Consequence for this contract |
|---|---|---|
| **Nickel-hydroxide electrochemical membrane capture** | A 25 cm² durability cell eventually reached about **0.46 kWh/kg**; a nine-cell stack demonstrated **0.83 kWh/kg** over 48 hours. The supplementary information explicitly excludes blower and compression work from these capture-and-release figures. | The best cell number leaves almost no auxiliary allowance. Humid operation and the dry-ambient water balance remain additional requirements. :chatgpt-content-reference{index="0"} |
| **Moisture-driven resin conveyor into alkaline liquid** | Approximately 1 g/day bench and 100 g/day outdoor operation. Published economic scenarios give **$229/t practical** and **$72/t aspirational** for delivery into solution. | The useful output differs from gaseous CO₂. The published additional extraction, purification and compression estimate is a separate modeled operation. :chatgpt-content-reference{index="1"} |
| **Vacuum moisture swing** | A process model reports a representative **0.694 kWh/kg**, with **1.4–3.5 kg water/kg CO₂**. | Vapor transport and compression remain material duties despite ambient heat input. This is modeled performance, not a complete hardware demonstration. :chatgpt-content-reference{index="2"} |
| **Local electrochemical alkalinity with a proton-transfer mediator** | An integrated laboratory route produces concentrated CO₂. Closing mediator regeneration through oxygen evolution requires **17.8–25.8 GJ/t**, equivalent to **4.94–7.17 kWh/kg**. | A lower-energy alternative consumes glycerol. That chemical input cannot be treated as a regenerated mediator. :chatgpt-content-reference{index="3"} |
| **Integrated heat-pump DAC models** | One 2025 study reports a modeled **0.461 kWh/kg** and **$63.2/t**. | These are process-model results. They do not establish manufactured humid-air equipment meeting this complete contract. :chatgpt-content-reference{index="4"} |
| **Industrial KOH/calcium regeneration** | A detailed, pilot-informed engineering study estimated $94–232/t at approximately 1 Mt/year, with substantial fuel consumption and delivery at 15 MPa. | Its scale, heat supply and delivery pressure differ materially from your operation. Its lowest modeled cost cannot be assigned to a 1-tonne/day electrical module. :chatgpt-content-reference{index="5"} |

Commercial progress also matters. Mission Zero reports third-party verification of **98.56% CO₂ purity** and an operating 250-tonne/year deployment. Climeworks reported substantial operating improvements at Mammoth in September 2026. These disclosures establish useful progress, but do not disclose enough matched energy, water, utilization and cost information to certify your numerical contract. :chatgpt-content-reference{index="6"}

### A purity correction that changes the engineering

A relevant kilogram-scale amine-resin pilot demonstrated cyclic capture, but its product contained only approximately **50–55% CO₂ because of air leakage**. Its measured working capacity therefore cannot be transferred unchanged to a well-sealed device producing 95% CO₂: removing the leakage raises the regeneration CO₂ partial pressure and can leave more CO₂ on the resin. :chatgpt-content-reference{index="7"}

That is a consequential coupling between leakage, apparent capacity and useful output.

---

## 3. The first candidate: an electrochemical carbon pump with humidity recovery

The first architecture I pursued combined an oxygen-compatible electrochemical carbon pump with a countercurrent water-vapor exchanger.

The intended operation was:

- Dry ambient air receives moisture from the depleted exhaust.
- A hydrated electrochemical membrane transfers captured carbon into a concentrated product compartment.
- The depleted humid air returns most of its moisture to the incoming air.
- Electricity drives the carbon transfer and all auxiliaries.

This gives water an actual return path. It also introduces a large additional separator.

### The required recovery is approximately 98%

For a 50%-capture stream, the calculated gross water transfer needed to raise the entire admitted air stream to 90% RH is:

| Ambient condition | Gross water transfer |
|---|---:|
| 20°C, 40% RH | 22.9 kg water/kg CO₂ |
| 25°C, 30% RH | 37.5 kg/kg |
| 30°C, 20% RH | 59.2 kg/kg |

At the warm, dry corner:

- 95% recovery leaves **2.96 kg/kg**.
- 97% recovery leaves **1.78 kg/kg**.
- 98% recovery leaves **1.18 kg/kg**.

Those figures precede initial wet inventories, product moisture, leaks, drains and treatment losses.

A hydrophobic porous membrane does not automatically solve this problem. Preventing liquid penetration does not prevent water-vapor transport.

### An attainable membrane still produces a large device

A documented PEO–polyurethane composite membrane provides a concrete manufacturing route: coat and crosslink a thin polymer layer on a microporous support. One patent example reports approximately **7,600 GPU water permeance** and **56 GPU CO₂ permeance**, while also describing sensitivity to conditioning and crystallization. These are component measurements, with differing water and CO₂ test conditions, rather than demonstrated DAC recuperator performance. :chatgpt-content-reference{index="8"}

Using that water permeance in a balanced countercurrent exchanger,

\[
\epsilon_w=\frac{\mathrm{NTU}}{1+\mathrm{NTU}},
\qquad
\mathrm{NTU}=\frac{U_wA}{\dot V},
\]

98% recovery requires \(\mathrm{NTU}=49\). At the airflow for 1 kg/day, the calculated membrane area is approximately

\[
\boxed{235\ {\rm m^2}}
\]

before adding further gas-film resistance.

Short, wide channels can keep friction low. They do not eliminate the membrane, supports, sealing, manifolds or manufacturing yield requirements.

Finite CO₂ permeability creates another penalty: incoming CO₂ can pass directly into the depleted exhaust through the humidity exchanger. Using the reported component selectivity provisionally, a 98%-water-recovery exchanger would require approximately **60% removal inside the capture cell** to achieve 50% removal from the original outside-air stream.

**This candidate did not close.** Its electricity, exchanger area, water recovery, CO₂ crossover and cost requirements were not jointly supported by the available component evidence. I therefore did not insert a perfect humidity exchanger into the model.

---

## 4. The concrete engineering candidate developed in full

The second route uses a commercial primary-amine resin, shallow contactors, electrical heat pumping, vacuum regeneration and measured batch collection.

It provides a physically understandable complete operation. **It does not establish a new separation mechanism or a target-compliant invention.** Thermal recovery and heat-pump-assisted adsorption already have substantial prior art.

### 4.1 Material and chemical balance

The active material is **Lewatit VP OC 1065**, a commercially manufactured macroporous, crosslinked polymer with primary amine groups. Its manufacturer identifies atmospheric CO₂ adsorption as an application. :chatgpt-content-reference{index="9"}

The relevant reversible binding includes carbamate and hydrated bicarbonate pathways, schematically:

\[
2RNH_2+CO_2
\rightleftharpoons
RNHCOO^-+RNH_3^+,
\]

and

\[
RNH_2+CO_2+H_2O
\rightleftharpoons
RNH_3^++HCO_3^-.
\]

The model uses measured empirical water/CO₂ equilibrium relationships rather than assigning all sites one ideal reaction.

There is **no recurring acid, alkali, nitrogen sweep or sacrificial regenerant**. Regeneration changes temperature and gas chemical potential. The resin returns to a lean state; lost active capacity triggers replacement costs.

Preparation is explicit:

- Determine delivered wet mass and dry-equivalent resin mass.
- Screen fines and measure extractable carbon and nitrogen.
- Collect any wash or conditioning discharge.
- Establish initial carbon inventory through a metered commissioning cycle.
- Charge drying of wet shipped resin separately.

Starting with a preloaded resin and selling its first release as captured atmospheric carbon is excluded.

### 4.2 Geometry

The deliberately conservative demonstrator design uses **25 kg dry resin**, providing throughput margin while making the equipment penalty visible.

| Component | Design specification |
|---|---|
| Sorbent beds | Four beds, each 6.25 kg dry resin |
| Vacuum housings | Preliminary envelope: approximately 450 mm internal diameter × 300 mm length |
| Air path through resin | 20 mm |
| Parallel resin face | Approximately 1.04 m² per bed |
| Internal thermal surface | Approximately 3 m² per bed |
| Measured gas-void target | 16 L per bed |
| Maximum admitted airflow | 180 m³/hour total |
| Regeneration temperature | 98°C resin; approximately 108°C heating-fluid supply |
| Regeneration pressure | 8 kPa absolute |
| Product delivery | Nominally 1.00 bar after compression and regulation |

The beads sit in removable retained-bead cassettes with mesh supports and microchannel thermal plates. The thermal surface and resin spacing must support approximately **500 W during desorption with a 10 K driving difference**.

The proposed dimensions are fabrication starting points. Pressure-vessel integrity, packing volume and distributed temperature measurements remain required engineering checks.

At modeled operating flows, the total air pressure drop is approximately **50 Pa**, including the declared clean-filter, support and header allowances. Fouling is monitored; filter replacement is charged.

### 4.3 Cycle and switching

Each bed follows a five-hour cycle:

| Step | Duration | Function |
|---|---:|---|
| Adsorption | 225 minutes | Capture from individually metered ambient-air flow |
| Cold evacuation | 10 minutes | Remove pore air before heating |
| Heating | 15 minutes | Raise resin temperature |
| Desorption | 40 minutes | Release CO₂ and co-adsorbed water |
| Cooling | 10 minutes | Recover sensible heat and begin cooling before readmission |

Beds are staggered by 75 minutes, so three can adsorb while one regenerates.

Cold evacuation targets 1 kPa before heating. This reduces residual air and hot oxygen exposure. Leakage remains in the purity, pumping and degradation balances.

The model permits finite cooling and adsorption heating. It does not instantaneously return a regenerated bed to ambient temperature.

### 4.4 Vapor handling and product collection

The regeneration stream passes through:

1. A **15°C refrigerated condenser**.
2. A demister.
3. Oil-free vacuum pumps.
4. An aftercooler.
5. A closed mixing buffer.
6. Dry-basis CO₂ analysis and regulated delivery.

The refrigerated condenser is essential to the stated duty. At low total pressure, an ambient condenser may recover little or no water.

For example, at 100 mbar total pressure, a roughly equimolar CO₂/water mixture has water partial pressure near 50 mbar. A condenser at 35°C has a water saturation pressure around 56 mbar, so it would not condense that stream. Drawing a condenser in the diagram would not remove the vapor from the pump load.

Each product batch is homogenized and tested before release. This makes batch-average purity a useful output specification. Off-spec gas, residual gas in the vessel, dissolved carbon in condensate and collection losses are charged.

Water vapor can remain in the delivered gas because your specification is **95% CO₂ on a dry basis**, rather than a specified product dew point.

### 4.5 Thermal and water return paths

A closed thermal circuit contains:

- Approximately 6 kg water in insulated thermal storage.
- Approximately 0.8 kg in other circulating volumes.
- Paid circulation, heat pumping and refrigeration.

The schedule requires thermal storage: only one bed regenerates at a time, so the design cannot claim immediate hot-bed-to-cold-bed heat exchange. The model’s 60% sensible-heat recovery is a **hardware requirement to measure**, not an established property.

Water captured from air is collected in a weighed, segregated condensate vessel. It is not automatically credited as clean makeup water. Reuse would require an actual return connection and appropriate chemical treatment or verification.

---

## 5. Equilibria, finite rates and the executable model

The model uses the published Young water/CO₂ equilibrium formulation, with finite-rate updates and explicit temperature dependence. The high-temperature binary region remains partly extrapolated and requires cyclic validation. :chatgpt-content-reference{index="10"}

An example shows why dry equilibrium uptake is insufficient.

At 30°C and 20% RH, the fitted equilibrium uptake varies substantially along a 50%-removal contactor. Regeneration against concentrated CO₂ leaves a nonzero lean loading. The useful quantity is therefore

\[
\Delta q_{\rm cycle}
=
q_{\rm rich,actual}-q_{\rm lean,actual},
\]

after finite adsorption, finite drying, finite desorption and temperature transients.

The rate uncertainty is material. A 2026 study reports CO₂ linear-driving-force coefficients of approximately

\[
3.7\times10^{-4}\ {\rm s^{-1}}
\quad\text{and}\quad
2.0\times10^{-3}\ {\rm s^{-1}}
\]

from different measurement methods. The model exposes this range rather than selecting only the faster value. :chatgpt-content-reference{index="11"}

### What is calculated

The executable model includes:

- Four asynchronous bed inventories.
- Water-dependent CO₂ affinity.
- Finite adsorption and desorption.
- Adsorption heat release and finite cooling.
- Coupled CO₂/water regeneration composition.
- A finite desorption heat-transfer limit.
- Air pressure drop and fan work.
- Pumping constrained by suction flow at operating pressure.
- Condensation, residual vapor, leakage and dry-product purity.
- Startup energy and initial liquid inventory.
- Initial/final carbon and water inventories.
- Cyclic degradation linked to replacement cost.

**The 50% removal condition is a control hypothesis, not an independently validated breakthrough prediction.** The controller reduces admitted air as modeled uptake falls. A real machine must demonstrate the corresponding inlet/outlet carbon balance.

Likewise, throttling modeled release to a pump capacity is a screening approximation. Actual pressure dynamics and wet pump curves remain experimental gates.

### Complete-run results

The following are **conditional model calculations**, not measured device performance.

| Input condition | Delivered CO₂ over 100 h | Average production | Purchased electricity |
|---|---:|---:|---:|
| 20°C, 20% RH | 6.02 kg | 1.45 kg/day | 6.53 kWh/kg |
| 20°C, 40% RH | 5.97 kg | 1.43 kg/day | 8.17 kWh/kg |
| 25°C, 30% RH | 5.89 kg | 1.41 kg/day | 7.39 kWh/kg |
| 30°C, 20% RH | 5.78 kg | 1.39 kg/day | 6.68 kWh/kg |
| 30°C, 40% RH | 5.71 kg | 1.37 kg/day | 8.43 kWh/kg |
| Changing conditions across the envelope | 5.86 kg | 1.41 kg/day | 7.45 kWh/kg |

Higher humidity increases the water that must be regenerated and condensed. Higher temperature reduces capture affinity. The coupled result cannot be represented by one dry capacity number.

### Why the commercial-component electricity is so high

For the nominal 100-hour run:

| Electrical use | Energy |
|---|---:|
| Heating and refrigeration | 20.71 kWh |
| Vacuum and delivery | 21.60 kWh |
| Air fan | 0.49 kWh |
| Controls | 0.20 kWh |
| Liquid circulation and cooling fans | 0.50 kWh |
| Other startup | 0.05 kWh |
| **Total** | **43.55 kWh** |

The vacuum allowance uses two 135 W diaphragm-pump-class units at 80% duty. The manufacturer’s power and endpoint specifications are available, but the required wet operating-flow curve remains a procurement/test condition. :chatgpt-content-reference{index="12"}

These electricity figures are **not a necessary lower bound for TVSA**. Better compressors and thermal integration can reduce them.

I therefore also ran a favorable hardware sensitivity with:

- Efficiency-based vacuum work.
- 85% sensible recovery.
- Heating COP of 2.5.
- Lower auxiliary power.
- No degradation during the run.



## Rendered remainder

[Rendered continuation beginning at the end of the exact native prefix; formatting and mathematical glyphs transcribed from the visible accessibility view.]

- A favorable aggregate heating/cooling recovery bound.

That case gives approximately 1.46 kWh/kg, still almost three times your target. It evaluates this design and inventory; it is not an optimization over every possible thermal separator.

### Carbon and water closure

In the nominal modeled run, approximately:
- 6.82 kg CO₂ is removed from admitted air.
- 5.89 kg reaches useful product.
- 0.55 kg remains on the resin at shutdown.
- The remainder is assigned to vents, collection loss and condensate.

The retained carbon is not counted as delivered product. Initial operating water is approximately 6.80 kg. Service and leakage allowances add 0.30 kg. Charging the entire initial fill gives approximately 1.21 kg water/kg delivered CO₂ in the nominal case. However, the wet-delivery scenario adds 25 kg of preparation water and its drying duty. It raises the initial-fill-plus-makeup ratio to approximately 5.55 kg/kg. That scenario also favors throughput by not delaying capture for preparation. It cannot certify a 100-hour run beginning with wet shipped material. Ambient heat and evaporation free energy have separate ledgers. The nominal thermal route draws ambient heat through the heat pump; it receives no purchased hot stream. It does not obtain its separation work from a large uncharged evaporation cycle. Numerical carbon and water balances close to floating-point tolerance. Halving the time step changes nominal output and specific energy by less than 0.02%. Those checks establish arithmetic consistency only.

## 6. Production-scale economics and lifetime

A favorable industrial redesign of this candidate still requires substantial resin inventory, vacuum housings, heat-transfer area, valves and thermal equipment. The scoping equipment allowance is:

| Equipment | Allowance |
|---|---:|
| Contactors and vacuum housings | $210,000 |
| Thermal plates and circuits | $90,000 |
| Heat-pump equipment | $60,000 |
| Blowers, filters and ducts | $20,000 |
| Vacuum and product handling | $35,000 |
| Switching equipment | $35,000 |
| Controls | $20,000 |
| Structures and plumbing | $35,000 |
| Engineering, installation, yield and contingency | $70,000 |
| Equipment excluding resin | $575,000 |

These are engineering allowances, not supplier quotations. At the favorable modeled productivity, normalization to 1 tonne/day requires approximately 18 tonnes of dry resin. Assuming an unquoted bulk price of $15/kg adds approximately $271,000 initially. With 90% utilization, 8% financing, 15-year equipment life and a hypothetical three-year resin replacement interval:

| Contribution | Approximate $/t |
|---|---:|
| Equipment capital | 204 |
| Resin purchase and renewal | 320 |
| Maintenance | 53 |
| Labour | 46 |
| Site and insurance | 11 |
| Filters and waste | 6 |
| Electricity | 73 |
| Water | 1 |
| Total | $712/t |

Even with free resin, the equipment-capital contribution in this budget exceeds the entire $100/t target.

### A desired lifetime changes the answer drastically

The model links degradation to replacement rather than assigning a favorable life independently. For example, a loss of 0.05% of capacity per five-hour cycle sounds small. At 90% utilization it reaches 80% remaining capacity after approximately 446 cycles ≈ 0.283 calendar years. That produces much higher renewal costs than a three-year assumption. This degradation rate is a scenario, not a measurement of the proposed device. But actual durability evidence prevents treating long life as free: one representative study found 31.2% capacity loss after 180 cycles for Lewatit under its ambient-air/vacuum protocol, compared with much smaller loss under an inert testing protocol. [Visible source: https://www.sciencedirect.com/science/article/pii/S1385894724003863?utm_source=chatgpt.com] A successful 100-hour run would establish neither a three-year life nor the required manufacturing economics.

### First demonstrator cost

The first 1-kg/day-class apparatus is a separate cost problem. A retrieved laboratory listing prices 100 g of Lewatit at $83.18, before adjusting for delivered moisture. Bulk industrial supply requires a quotation. [Visible source: https://www.thomassci.com/p/fluka-lewatit-vp-oc-1065?utm_source=chatgpt.com] For 25 kg dry-equivalent resin, custom housings, pumps, thermal equipment, metrology and assembly, an honest first-build allowance is approximately $65,000–110,000 using small-pack procurement. A suitable industrial lot could reduce this, but that quotation is not an existing asset. I would not commission that full demonstrator on the claim that this investigation has established a route to the targets.

## 7. The smaller decisive prototype

The useful next physical experiment is a four-cassette, 0.5 kg dry-resin apparatus, with the same bead size, air-path thickness, thermal spacing and regeneration conditions. Its provisional production target is 20–30 g/day, with approximately 4–7 m³/hour of ordinary air. Its purpose is to establish actual cyclic inventories, regeneration against concentrated product, water transport and component performance.

### Build and access

This needs a chemical-engineering laboratory or comparable workshop with:
- Four vacuum-rated small vessels and 125 g resin cassettes.
- Distributed thermocouples and absolute/differential pressure sensors.
- Individually measured air branches.
- A closed thermal circuit.
- Refrigerated trap, demister and oil-free vacuum equipment.
- A homogenizing product bag or receiver.
- Two low-range CO₂ measurements for inlet/outlet air.
- A product CO₂ analyzer and independent GC verification.
- RH/temperature sensing, calibrated gas flow, balances and wall electricity metering.
- Access to TIC/TOC, nitrogen and resin-capacity assays.

Actual environmental conditioning used to test all four input corners is metered and included in the experiment budget. It is not credited as a free onboard inlet-conditioning system.

### Experimental sequence

1. Characterize the starting material. Measure dry mass, water, initial carbon, amine/base inventory and extractables.
2. Measure empty-system blanks and leakage. Test both cold and hot assemblies.
3. Commission with complete accounting. Record preparation energy, condensate and discharge.
4. Run the cyclic device for 100 hours, including all envelope corners and transitions.
5. Measure every accepted product batch. Record rejected carbon and residual vapor.
6. Reassay the final material and liquids. Repeat adsorption after final regeneration.
7. Extend the run if needed to distinguish regeneration from initial-inventory consumption.

### Numerical pass/fail conditions

| Measurement | Required result |
|---|---|
| External single-pass removal | At least 50% during every accepted adsorption interval |
| Accepted product | At least 95.0% dry CO₂ |
| Delivery pressure | 1.00 ± 0.02 bar absolute |
| Carbon balance | Within ±3% |
| Water balance | Within ±5% |
| Electrical ledger | Branch meters agree with wall meter within ±2% |
| Regeneration | Repeated return to the same lean state within measured uncertainty |
| Initial alkalinity exclusion | Cumulative delivered carbon exceeds twice the independently measured initial carbon-equivalent alkalinity, with no replenishment |
| Contamination | Quantified amines, particles, dissolved carbon/nitrogen and any metal carryover |
| Component maps | Actual wet pump flow/power, condenser slip, bed temperatures, heat-transfer conductance and COP |

If the initial-inventory criterion is not reached within 100 hours, the experiment continues. It does not declare regeneration from a favorable first release. All laboratory auxiliary electricity remains visible. A tiny prototype passing material-cycle tests would not automatically satisfy 0.50 kWh/kg at its own scale or at 1 kg/day.

### Total prototype budget

An allowance of approximately $13,000–15,000 covers the instrumented apparatus, resin, fabrication, calibration/chemical checks, environmental-test access or rental, electricity and consumables. These are unquoted budget allowances. Existing institutional equipment may reduce purchase outlay, while access and calibration costs remain real. Success would establish a genuine regenerative operation and measured component maps. It would not establish factory yield, multi-year durability, $100/t, sequestration or negative emissions.

## 8. What a successful invention still has to change

The remaining opening is more specific than “find a better sorbent.” For a thermal route, consider a favorable allocation of 0.10 kWh/kg to nonthermal auxiliaries and a heating COP of 2.5. The remaining electricity allows approximately 1.0 kWh of regeneration heat per kilogram CO₂. A CO₂ binding heat around 70 kJ/mol already uses approximately 0.44 kWh/kg of that thermal budget. Water regeneration, sensible heat and losses must fit into the balance. For example, if unrecovered sensible heat and other thermal losses use 0.15 kWh/kg, the remaining allowance permits only roughly 0.6 kg regenerated water/kg CO₂ at ordinary water-desorption enthalpies. That requirement must be achieved together with useful concentrated-product working capacity, short cycles, inexpensive contactors and durable material. Faster drying alone does not change the water-per-CO₂ ratio. For the electrochemical route, the missing combination is similarly concrete:
- Low full-cycle electrical work.
- Adequate flux at that work.
- Operation in 20–40% RH air or inexpensive verified humidity recovery.
- Limited CO₂ crossover.
- Low supported-area cost.
- Proven cyclic lifetime.
- Pure product and complete regeneration.

I have not completed the requested invention. The delivered work identifies two serious architectural paths, closes the main accounting in a concrete candidate, and shows why that candidate cannot presently support the energy or cost claim. The invention question remains open; a successful answer requires a measured improvement in the coupled material–contactor–regeneration operation, beyond the improvements substantiated here.
