# P2 electricity storage: available completed return

Chat: https://chatgpt.com/c/6af50a9c-b11c-83ec-9099-207cf9b858b8; latest actual user 9e7bc487-ba26-49b2-aba2-829cc55f3463; final ID prefix 27a65277. Observation 2026-11-12 01:37 UTC. Prompt/input evidence: P2_100H_STORAGE_ACTUAL_POSTED_MESSAGES_20261112.json.

Native final is truncated at 20,000 characters. The remainder is a transcription of rendered UI, with tables and mathematical formatting reconstructed where visible; this is not full native/database-byte identity. Working activity and helper expansions were not captured in full. Linked artifacts were not collected; their identity and eligibility remain unverified. No linked sources or components were opened.

The actual input was the three fragmented messages saved in the referenced JSON, not the complete approved source. The UI showed a nonempty unsent trailing draft beginning “Develop a smaller decisive prototype for later authorized physical execution” and ending “you may use all subagents avaible”; paragraphs were concatenated. It was preserved and not sent.

## Exact native prefix

## Result: I did not obtain a design that meets the entire contract

I developed a fixed **alkaline iron–chlorine storage architecture**, an executable cycle model, and an itemized lifetime cost model. The result is a rejection of that candidate at the chosen operating point:

- **59.45% modeled AC-to-AC efficiency**, below 65%.
- **$178 per useful delivered kWh** in an unquoted manufacturing scenario, above $15.
- **About $1,634/MWh delivered** under the specified schedule and the stated replacement assumptions, above $125/MWh.
- Formation, additive chemistry, and reversible separator life remain unvalidated. Consequently, even the calculated performance is **not a demonstrated physical result**.

I cannot honestly present this as a successful invention. It does, however, identify a concrete construction, its full intended return path, where its accounting closes, where its chemistry remains unclosed, and the experiments that could decisively reject or advance it.

**Deliverables**

- :chatgpt-content-reference{index="17"}[storage_design_report.pdf](sandbox:/workspace/scratch/9fde3438af2d/output/storage_design_report.pdf) — 12-page technical report with construction, balances, costs, comparisons, and evidence register.
- :chatgpt-content-reference{index="18"}[storage_model.zip](sandbox:/workspace/scratch/9fde3438af2d/output/storage_model.zip) — executable Python model, configuration, cycle traces, material and energy ledgers, cost breakdown, and annual cash flows.

The core model uses Python’s standard library:

```bash
python3 storage_cycle.py --output results
```

**Unless explicitly identified as published evidence, the candidate’s numerical properties and prices below are introduced engineering assumptions or calculations from them. They are not measurements or supplier quotations.**

---

## 1. The proposed operation

The candidate replaces an iron–air battery’s oxygen electrode with a sealed chlorine/chloride electrode. It stores energy in **metallic iron, chlorine, and the accompanying salt/caustic composition change**.

The intended net charging reaction is

\[
\boxed{
\mathrm{Fe(OH)_2+2NaCl
\;\xrightarrow{\ electricity\ }\;
Fe+2NaOH+Cl_2}
}
\]

Discharge reverses it.

The charging half-reactions are

\[
\begin{aligned}
\text{Negative:}\quad&
\mathrm{Fe(OH)_2+2e^-\rightarrow Fe+2OH^-},\\
\text{Positive:}\quad&
\mathrm{2Cl^-\rightarrow Cl_2+2e^-}.
\end{aligned}
\]

Two sodium ions cross from the chloride compartment to the hydroxide compartment per iron atom reduced. On discharge, chlorine is reduced, iron is oxidized, and sodium returns.

This pairing seeks a higher useful voltage and smaller positive-electrode polarization loss than iron–air. It also introduces substantial hardware: a chemically selective separator, chlorine storage and transfer equipment, and a real return path for parasitic gas and electrolyte imbalances.

### What existing work contributes

Manohar, Yang and Narayanan’s 2015 study is valuable evidence for the iron electrode. It used prepared carbonyl-iron electrodes, nickel grids, alkaline electrolyte, and a nickel-oxide counterelectrode. Its sulfide/bismuth results support investigating passivation control and additive management; they do not establish the whole storage cycle proposed here. Its working-electrode charge efficiency and extended cycling cannot simply be assigned to a thick hydroxide electrode operating for 100 hours between long holds. :chatgpt-content-reference{index="0"}

A separate experimental chlor-iron process supplies evidence for a pH-separated iron/chlorine electrolyser using a chlor-alkali membrane and chlorine-evolving interface. That work investigated iron production from oxide at **80°C**, rather than an ambient-temperature rechargeable store. It does not demonstrate the reverse operation used here. :chatgpt-content-reference{index="1"}

Nor is combining iron and chlorine itself a new invention: related metal/chlorine architectures appear in existing patent literature. :chatgpt-content-reference{index="2"}

### The clean starting state

The proposed active material begins as **assayed Fe(OH)₂**, with no useful metallic iron and no stored chlorine. A possible preparation route is

\[
\mathrm{FeCl_2+2NaOH\rightarrow Fe(OH)_2+2NaCl},
\]

followed by oxygen-excluded washing and preparation on a nickel/carbon scaffold. Precursor manufacture, purification, atmosphere control, waste treatment and electrode preparation are paid.

This is a consequential change from starting with carbonyl iron. Discharging only 20% of a metal-powder electrode’s theoretical capacity would leave substantial metallic fuel. It would not satisfy the clean starting-state requirement.

**The unresolved issue is whether the proposed hydroxide construction can be formed into the required accessible, durable electrode.** The model does not establish that manufacturing result.

---

## 2. One fixed physical construction

The same construction is used for the nominal calculation, tolerance case and cost estimate.

| Component | Fixed construction or quantity |
|---|---|
| Electrical stack | 40 series cells |
| Projected electrode/separator area | 400 cm² per cell; **1.60 m² total** |
| Active inventory | **36 kg Fe equivalent**, initially about **57.93 kg Fe(OH)₂** dry equivalent |
| Assumed accessible capacity | 20% of theoretical Fe capacity; **6,911 aggregate Ah summed over cells** |
| Iron electrode | 40 mm bed depth; 64 L total bed volume; nickel mesh/carbon conductive scaffold |
| Additives and inactive solids | 2.9 kg FeS, 2.9 kg Bi₂O₃, approximately 5.8 kg carbon/binder/process allowance, approximately 2 kg nickel scaffold |
| Negative liquid | Initially 60 L, including pore liquid; 468.75 mol NaOH and 56.25 kg water |
| Positive liquid | Initially 75 L; 375 mol NaCl and 68.10 kg water; acidity controlled for chlorine service |
| Chlorine interface | RuOₓ/Ti evolution interface with graphitized reduction/contact layer |
| Separator | N2050-type chlor-alkali composite as a test starting point |
| Chlorine storage | 12 L vessel, 25 bar design envelope, maximum 75% liquid fill |
| Approximate package | 0.8 × 0.9 × 0.9 m; screening mass about 250–300 kg |

Commercial chlor-alkali membranes provide a real starting component, but their existence does not establish acceptable low-temperature, repeatedly reversed battery operation. :chatgpt-content-reference{index="3"}

The base cycle reaches about **5.66 kg of metallic iron**, or 78.6% of the assumed accessible capacity. This provides a modeled capacity reserve; it does not prove that the reserve is physically accessible.

### Transport is an explicit limitation

The model uses an effective bed conductivity of \(10\ \mathrm{S/m}\), a distributed reaction, and a mean ionic path of \(L/3\):

\[
R_A=\frac{L}{3\kappa_{\rm eff}}+R_{A,\rm other}.
\]

At approximately \(3.7\ \mathrm{mA/cm^2}\), the bed contribution is about 0.05 V. This is a **transport assumption**, not a solution of the actual porous-electrode problem.

A reaction front, pore blockage, current crowding, hydroxide expansion or poor contact could make the loss substantially larger. The necessary measurements include through-bed potential, local phase conversion, electrolyte concentration and current distribution. Increasing the mass or area after discovering those losses would invalidate the fixed-design comparison.

### Practical AC interface

The specified interface is:

- Isolated **230 V rms, 50 Hz**, supplying 100 W continuously.
- Rated output up to **125 VA**, with load power factor at least 0.8.
- Voltage within **±2%**, frequency within **±0.1 Hz**.
- Voltage THD below **3%** within the declared load envelope.
- A defined load-step acceptance test, with settled voltage deviation below 5%.
- Power-factor-corrected charging input, PF at least 0.95.
- **200 W maximum total imported charging power**, including auxiliaries.

The topology uses an isolated DC/DC stage and inverter/rectifier. Both conversion directions are assumed to reach 97% at their actual operating powers. These are design acceptance requirements, not demonstrated converter results.

At the reference installation, the cost model includes **200 kW bidirectional conversion for 100 kW discharge**.

---

## 3. The complete intended charge–hold–discharge sequence

### Charge: 100 hours

The model solves for charging current while enforcing the fixed capacity and total import ceiling. The nominal current is approximately **1.478 A through the 40-cell stack**.

Charging simultaneously:

1. Reduces accessible Fe(OH)₂ to iron.
2. Produces chlorine.
3. Moves sodium into the hydroxide compartment.
4. Compresses and dries the chlorine that will be stored.
5. Handles parasitic hydrogen and oxygen.
6. Returns salt and water displaced by side reactions.

The integrated mean charging voltage is about **2.538 V per cell**.

### Hold: 144 hours

The proposed hold operation drains free liquid from the chlorine-facing channels to their reservoir, withdraws bulk chlorine to the storage vessel and isolates the loops.

The iron electrode remains humid and alkaline. Draining the opposite interface does **not** stop iron corrosion. The model assumes **99% useful charge retention over 144 hours**, and pays the electricity needed for hold controls and corrosion-related reset.

There is no routine supply of external oxygen or nitrogen. Initial evacuation/nitrogen and purification are manufacturing costs. In service, the process is intended to remain sealed; ambient air serves as the heat sink.

### Discharge: 100 hours

Chlorine is supplied to its reduction interface. Iron oxidizes within the selected Fe/Fe(OH)₂ window, sodium returns to the chloride compartment, and power conversion supplies **100 W net AC after internal loads**.

Mean discharge voltage is approximately **2.026 V per cell**.

### Hydrogen cannot be omitted from the return path

The principal negative-electrode parasitic reaction is

\[
\mathrm{2H_2O+2e^-\rightarrow H_2+2OH^-}.
\]

It changes the chemical inventory as well as wasting charge. The intended reset consumes unwanted oxygen with part of the hydrogen and uses the remaining hydrogen in a separate controlled chlorine-recombination/absorption circuit:

\[
\begin{aligned}
\mathrm{H_2+Cl_2}&\rightarrow\mathrm{2HCl},\\
\mathrm{2HCl+2NaOH}&\rightarrow\mathrm{2NaCl+2H_2O}.
\end{aligned}
\]

Hydrogen and chlorine are not intentionally stored together in bulk.

The nominal calculation produces approximately:

- **8.82 mol H₂** during charging;
- **0.55 mol O₂** during charging;
- another **1.17 mol H₂** from modeled corrosion across the operation.

The model therefore consumes some generated chlorine in reset. It does not count all evolved chlorine as retained energy.

### Water and atmospheric exposure

The assumed water drag is two water molecules per sodium ion during charge and 1.7 during discharge. Together with parasitic reset, this gives:

- About **7.3 kg maximum water displacement** between compartments.
- About **3.37 kg/cycle of required water recovery**.
- An introduced recovery penalty of **0.30 kWh/kg**, plus installed recovery hardware.

The actual separation process, purity requirement, osmosis and dissolved-gas carryover remain unqualified. A balanced salt/water equation is not evidence that a small recovery unit can accomplish it at the assumed cost and energy.

Oxygen ingress, carbon dioxide carbonation, chlorine crossover and water exchange must be measured over the full humidity range. The model assumes sealed operation; it does not supply measured seal leakage.

Chlorine storage also has a real pressure and thermal boundary. NIST data give roughly **10.1 bar saturation pressure at 35°C** and **14.5 bar at 50°C**. The model compresses from about 1.1 bar and assumes condensation at ambient plus 5°C. :chatgpt-content-reference{index="4"}

Wet electrolytic chlorine cannot be assigned ordinary dry-chlorine handling hardware without qualification. Drying, compatible wetted parts, containment and monitoring are necessary paid components. :chatgpt-content-reference{index="5"}

---

## 4. What the executable model closes—and what it does not

### Main chemical inventory

These are the modeled states **after the assumed rebalancing operation**.

| Inventory | Initially | End of charge | After 144-hour hold | End of discharge |
|---|---:|---:|---:|---:|
| Metallic Fe | 0 | 5.661 kg | 5.605 kg | 0 |
| Fe(OH)₂ | 57.927 kg | 48.817 kg | 48.908 kg | 57.927 kg |
| NaOH | 468.750 mol | 671.504 mol | 669.477 mol | 468.750 mol |
| NaCl | 375.000 mol | 172.246 mol | 174.273 mol | 375.000 mol |
| Stored Cl₂ | 0 | 7.188 kg | 7.116 kg | 0 |
| Total process water | 124.350 kg | 124.350 kg | 124.350 kg | 124.350 kg |

The ideal main reaction conserves elements and returns to its starting state.

**That is narrower than the physical closure you requested.** The following states remain unresolved:

| Missing physical result | Why it matters |
|---|---|
| Formation of the hydroxide electrode | Determines whether the clean initial state can acquire useful reversible capacity |
| Bi₂O₃/Bi transformation | Creates an additional charged inventory and formation demand |
| Sulfide depletion and oxidation products | Requires actual replenishment, preparation and waste treatment |
| Magnetite accumulation | Changes accessible capacity, reaction stoichiometry and recharge conditions |
| Hypochlorite/chlorate formation | Removes chlorine from the assumed reversible inventory |
| Membrane crossover, leakage and current reversal | Changes self-discharge, composition and service life |
| Spatial phase/current distribution | Determines whether the thick electrode behaves like the lumped model |
| Actual water/salt recovery process | Determines whether the assumed chemical reset is achievable |

For example, reducing the specified **2.9 kg Bi₂O₃ to Bi would require roughly 1,000 aggregate Ah**. That is material, and it is not part of the modeled Fe-only state variable. This alone prevents calling the supplied model a fully closed actual electrochemical invention.

### Integrated electrical ledger

The model integrates current and voltage; it does not multiply together unrelated best-case efficiencies.

| Imported electricity | kWh/cycle |
|---|---:|
| Cell-stack charging | 15.0009 |
| Charging conversion loss | 0.4639 |
| Charging pumps and controls | 0.2500 |
| Chlorine compression and drying | 0.4063 |
| Charge-phase water/salt reset | 0.5889 |
| Hold controls and hold reset | 0.1104 |
| **Total imported** | **16.8205** |

| Discharge energy | kWh/cycle |
|---|---:|
| Electricity produced by cell stack | 10.8911 |
| Discharge auxiliaries | −0.2500 |
| Water/salt reset | −0.3318 |
| Output conversion loss | −0.3093 |
| **Useful AC delivered** | **10.0000** |

Therefore,

\[
\boxed{\eta_{\rm AC}=\frac{10}{16.8205}=59.45\%}.
\]

Peak imported charging power is **167.97 W**. Thus the modeled nominal cycle meets the power ceiling and duration requirements, while failing efficiency.

The assumed 92% iron charge efficiency is already included in the charging extent. It is **not multiplied into the result again**.

### Thermal inventory and formation

The thermal screen assumes:

- Reaction enthalpy: 450 kJ/mol Fe.
- Module heat capacity: 160 Wh/K.
- Heat rejection coefficient: 8 W/K.

At 35°C ambient, the periodic calculation begins and ends at **38.21°C**, with approximately **0.513 kWh sensible heat above ambient**. Peak temperature is about **40.11°C**. Net heat rejection over the complete cycle is approximately **6.82 kWh**.

This explicitly declares the initial thermal inventory; it does not treat a warm periodic cycle as a cold first start.

An additional **30 kWh and 150-hour formation/commissioning allowance** is charged to the first module. It is an allowance, not a demonstrated procedure. Including it, the first-service electricity ratio is only about

\[
\frac{10}{30+16.8205}=21.4\%.
\]

The strict first-use 100-hour charging contract is therefore not met.

---

## 5. Tolerance, aging, partial operation and shutdown

The unfavorable case uses the **same dimensions, inventory and interface area**. It lowers accessible fraction to 18%, conductivity to 5 S/m, iron charge efficiency to 85%, hold retention to 95%, and conversion efficiency to 94%, while adding 0.10 V polarization in each direction.

| Same fixed hardware | Useful AC delivered | AC efficiency | Discharge duration |
|---|---:|---:|---:|
| Nominal assumptions, 35°C | 10.00 kWh | 59.45% | 100 h |
| Nominal assumptions, 20°C | 10.00 kWh | 58.65% | 100 h |
| Unfavorable tolerance case | **8.48 kWh** | **41.46%** | **84.8 h** |
| Optimistic interface assumptions | 10.00 kWh | 70.80% | 100 h |
| 50 W load case | 5.00 kWh | 58.50% | 100 h |

The optimistic case assumes 98% iron charge efficiency, lower polarization and 99.5% hold retention. It shows the performance requirement that a better interface would need to meet. It is not evidence that those properties coexist.

For partial discharge, the intended control operation is to stop current, isolate chlorine, retain the paired chemical inventories and resume from measured remaining SOC. Further hold loss must be subtracted. A safe shutdown retains charge; returning to the clean state requires controlled discharge through the converter or a metered dump load.

An emergency scrubber consumes reserve chemicals. Its replenishment and waste are fault costs, not a reversible normal-cycle operation.

The executable model can vary load and duration, but it does **not** establish phase-history-dependent restartability or local current redistribution after interrupted discharge. Those remain necessary experiments.

---

## 6. Installed capital at the same operating point

The manufacturing scenario is **1 GWh/year of useful storage capacity**, equivalent to 100 reference plants annually. Each reference plant contains 1,000 nominal chemical-module equivalents, with centralized power conversion and portions of gas processing and controls.

The scenario includes qualified active material rather than assigning scrap-iron prices to a prepared electrode.

| Installed-cost group | USD per 10 kWh module equivalent |
|---|---:|
| Prepared Fe(OH)₂, FeS and Bi₂O₃ | 205.72 |
| Carbon/binder/process consumables and nickel scaffold | 100.00 |
| Electrolyte, purified water, initial atmosphere and purification | 45.00 |
| Separator | 400.00 |
| Chlorine interfaces | 128.00 |
| Frames, gaskets and manifolds | 72.00 |
| Electrode preparation, formation labor and formation electricity | 60.60 |
| Liquid tanks and chlorine vessel allocation | 95.00 |
| Compression, drying, gas reset and water recovery | 145.00 |
| Pumps, heat rejection and plumbing | 35.00 |
| Charging/discharging power conversion | 40.00 |
| Controls, containment equipment, enclosure and busbars | 85.00 |
| Factory overhead, QA and yield allowance | 195.00 |
| Transport, installation, initial waste and contingency | 175.00 |
| **Total** | **1,781.32** |

That gives

\[
\boxed{C_{\rm installed}\approx \$1.781\text{ million}/10\text{ MWh}
=\$178.13/\text{useful kWh}.}
\]

The target is $150,000 for that plant.

These are unquoted allowances and several are optimistic. They do not establish a procurement-ready factory estimate.

The separator assumption alone is **$250/m²**, contributing **$40/useful kWh**. For context, historical industrial chlor-alkali documentation describes expensive membranes and periodic replacement; it is not a present quotation for this battery. :chatgpt-content-reference{index="6"}

More decisively, **making the separator free still leaves approximately $138/kWh**. This design cannot reach the target through one inexpensive catalyst or membrane substitution.

### First builds

Separate research-build allowances are:

| Build | Unquoted allowance | What it can establish |
|---|---:|---|
| Electrode/membrane coupon campaign | $5,000–10,000 | Formation, reverse-current stabi


## Rendered remainder

[Rendered continuation of the partial table at the native-prefix boundary; formatting reconstructed from the visible accessibility view.]

### First builds

Separate research-build allowances are:

| Build | Unquoted allowance | What it can establish |
|---|---|---|
| Electrode/membrane coupon campaign | $5,000–10,000 | Formation, reverse-current stability, crossover, cold conductivity |
| One full-geometry cell | $15,000–30,000 | 400 cm² interface, 40 mm bed, 0.9 kg Fe equivalent; transport and inventory behavior |
| First 100 W / 10 kWh module | $40,000–80,000 | Integrated gas, thermal, control and AC operation |

The single-cell target is approximately 0.25 kWh. Its laboratory overhead cannot be normalized away to claim full-module AC efficiency.

## 7. Complete delivered-energy economics under declared life assumptions

Your schedule calculation is correct: n_max = 8760(0.9)/344 = 22.9186 cycles/year before additional downtime. At 8% real discount over 20 years, CRF = 0.1018522. Thus capital costing K dollars per useful kWh contributes LCOS_capital = 1000 K CRF/n dollars per MWh.

### The narrow margin even for a hypothetical successful store

At $15/kWh installed, 65% efficiency and 2% annual capital maintenance:

| Annual cycles | $20/MWh charging | $40/MWh charging |
|---|---:|---:|
| 22.9186 | $110.52/MWh | $141.29/MWh |
| 12 | $183.08/MWh | $213.85/MWh |
| 6 | $335.40/MWh | $366.17/MWh |

These are favorable subtotals excluding replacements, fade and additional site costs. At maximum utilization and $20 charging, only about $14.48/MWh remains below the target. Under those same favorable assumptions, achieving $125/MWh requires capital below approximately $9.28/kWh at 12 cycles/year, or $4.64/kWh at six cycles/year, before replacements and other omitted costs.

### Life assumptions used for the proposed hardware

The model pays for:
- Capacity decline of 1%/calendar year plus 0.02%/cycle, applied exponentially.
- Increasing electrode polarization and declining charge selectivity.
- Iron-assembly replacement after ten years.
- Membrane/gasket service every four years.
- Gas-system service every five years.
- Power-electronics replacement after ten years.
- Additional commissioning and replacement downtime.
- Routine maintenance, site labor, land/insurance, consumables and waste.
- Sulfide replenishment and an explicit preparation-energy assumption.
- Decommissioning at 10% of initial capital, with no salvage credit.

These are life scenarios, not measured degradation. The 20-year financial horizon does not turn them into established material life. The discounted calculation uses actual modeled delivery and imports in each year, including idle electricity and replacement outages:

| Use | $20/MWh charging | $40/MWh charging |
|---|---:|---:|
| Maximum allowed schedule | $1,634/MWh | $1,668/MWh |
| 12 cycles/year | $3,069/MWh | $3,104/MWh |
| 6 cycles/year | $6,103/MWh | $6,139/MWh |

The specified expenses are included; the numbers are not an actual field-cost forecast. Unknown failure modes could change them substantially. Listed lifetime electricity—including operation, standby, formation and the declared replacement-sulfide preparation—gives about 57.9% delivered electricity per listed input. Other unmeasured manufacturing energy is not covered, so this is not a full life-cycle energy assessment.

## 8. Comparison with strong alternatives

No public evidence I retrieved establishes an incumbent meeting every element of this contract simultaneously. That is a limitation of the available evidence, not a proof of impossibility.

### Lithium-ion/LFP: the efficient commercial benchmark

The 2025 technology baseline uses 85% round-trip efficiency for utility battery modeling. It concerns shorter-duration systems; it does not establish the exact 344-hour duty. BloombergNEF’s 2025 survey reports stationary battery packs averaging $70/kWh. [Visible link: https://atb.nlr.gov/electricity/2025/utility-scale_battery_storage?utm_source=chatgpt.com] At that survey price, even generously treating pack capacity as installed useful AC capacity gives about $311/MWh in capital financing alone on this schedule. Using a better converter or 90% efficiency would not remove that capacity-cost term. LFP remains a strong practical option for delivering the service. The evidence cited does not support the $15/kWh installed target. An honest comparison would size its converter for this duty and manage standby intelligently, rather than leave an oversized short-duration system idling at tiny load.

### Iron–air: closest public capacity-cost ambition

Form’s 2025 CEC report describes EPRI validation of real DC modules exceeding 100-hour discharge. Measured efficiency is proprietary; the report distinguishes DC testing from AC interface modeling. [Visible link: https://www.energy.ca.gov/sites/default/files/2025-11/CEC-500-2025-045.pdf?utm_source=chatgpt.com] Separately, Form’s public planning assumptions specify 40–45% AC efficiency and approximately $15–20/kWh installed at much larger scale and future manufacturing volume. These are planning inputs, not a quotation for the present 100 kW plant. [Visible link: https://formenergy.com/wp-content/uploads/2024/06/Form-Energy-Navigating-the-Pacific-Northwest-Energy-Challenges-06.26.2024.pdf?utm_source=chatgpt.com] At those planning efficiencies, 10 kWh delivered needs roughly 22.2–25 kWh input. The published planning case therefore misses both the 65% requirement and the intended 100-hour/200 W charging envelope. This does not establish that every future iron–air configuration must do so.

### Vanadium flow: strong life and inventory separation

Invinity’s published Endurium specifications give maximum total efficiencies of 69–70%, with specified electrolyte temperature and auxiliary qualifications, for a different duration range. [Visible link: https://invinity.com/wp-content/uploads/2025/03/Invinity-Endurium%E2%84%A2-Data-Sheet-MAR0020-2025-04b.pdf?utm_source=chatgpt.com] This is close enough to the efficiency target to deserve serious consideration. At 69%, only about 0.89 kWh per 10 kWh delivered remains for additional losses before falling below 65%. A 100-hour implementation should decouple tank inventory from stack power and reduce hold pumping. Keeping the auxiliary consumption of a high-power commercial stack while claiming optimized 100-hour capacity would be unfair. Conversely, a newly optimized small stack needs its own price, efficiency and lifetime evidence. The retrieved specifications do not establish $15/useful kWh.

### Thermal storage: compare electricity with electricity

Malta’s published pumped-heat design specifies 55–60% power-to-power efficiency at large scale. Its higher cogeneration figure includes heat, which cannot substitute for the required AC output. [Visible link: https://maltainc.com/wp-content/uploads/2025/08/DipticoMar2025-1.pdf?utm_source=chatgpt.com] That particular design misses the efficiency threshold before adapting it to 100 kW or accounting for the specified hold. It is not a thermodynamic proof against all thermal architectures.

### Mechanical storage: credible efficiency, different physical setting

The operating Yingcheng compressed-air project is reported at 300 MW/1,500 MWh, with approximately 70% conversion efficiency attributed to an investor. It uses underground salt caverns and a five-hour discharge schedule. [Visible link: https://english.cas.cn/newsroom/cas_media/202501/t20250113_898557.shtml?utm_source=chatgpt.com] Modern compressed air and pumped hydro therefore should not be dismissed as inherently inefficient. But cavern development, reservoirs, head, machinery and site conditions cannot be imported into a 100 kW/10 MWh cost calculation as free infrastructure. The cited plant does not establish this module or installation contract.

### Reversible solid oxide storage: a particularly relevant emerging competitor

Noon reported containerized operation for thousands of hours and more than 200 hours of storage capacity in January 2026. Its announcement does not provide the full AC ledger, 144-hour hold result or installed price. [Visible link: https://www.noon.energy/post/noonenergyannouncessuccessful100hourbattery?utm_source=chatgpt.com] Its CEC program explicitly develops 100 kW/10 MWh, with a system-efficiency demonstration goal of at least 50% and commercialization targets below $20/kWh. Those are goals, not measured limits or quotations. [Visible link: https://www.energizeinnovation.fund/projects/scale-ultra-low-cost-long-duration-battery-fully-reliable-renewable-power?utm_source=chatgpt.com] It would also be wrong to represent all reversible solid oxide storage by a poor electrolyser/fuel-cell pair. Published computational 100 kW designs reach approximately 65–74%, depending on gas and water management. Those calculations are not a measured full schedule with six-day thermal standby. [Visible link: https://www.sciencedirect.com/science/article/pii/S0306261916303749?utm_source=chatgpt.com] The proposed iron–chlorine construction has no demonstrated advantage over Noon.

## 9. The missing invention and the decisive experiment

The useful capability sought is specific: Store a large hydroxide inventory behind a small, inexpensive power interface, while retaining short transport paths, low polarization, low corrosion during isolation, and an inexpensive physical return path for every side product.

One possible research opening is a distributed chlorine/ion-transport interface inside a thick hydroxide electrode. That could separate expensive interface area from bulk capacity more effectively than the fixed planar construction. But the required component does not yet follow from naming a material. It must simultaneously be chlorine-resistant, selective, reversible, manufacturable, repairable and inexpensive. Furthermore, this candidate’s non-membrane costs already exceed the target by a large factor. A successful invention must improve the electrode construction and supporting apparatus together. I would not build the nominal module on the basis of this result. The decisive smaller experiment is a full-thickness cell using the intended packing, separator and useful conversion fraction, beginning from assayed hydroxide and measured additive states. Its acceptance campaign should establish:

1. Formation: imported energy, gas production and the final Fe/Bi/S phase inventory.
2. The complete schedule: 100-hour charge, 144-hour hold and 100-hour discharge at both ambient-temperature limits.
3. Actual inventories: salt, caustic, water, chlorine, hydrogen, oxygen, sulfide, bismuth and iron phases.
4. Transport and restart: local conversion through the thick bed, partial discharge, isolation and resumed operation.
5. A physical reset: measured unit operations returning the declared starting states.
6. Durability: calendar exposure and repeated operation consistent with paid replacement intervals.

A successful nominal module would then need to deliver 10 kWh with no more than 15.3846 kWh total operating import, within the charging-power limit and stated power quality, using the same fixed hardware. The supplied model is useful for rejecting inconsistent assumptions and testing their economic consequences. It does not close the actual additive, phase and separator chemistry, and it does not meet your cost or efficiency targets. Claiming that it did would require inventing material properties and lifetime data, rather than inventing a demonstrated storage system.
