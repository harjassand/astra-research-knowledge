# P2 dispatchable heat engine: available completed return

Chat: https://chatgpt.com/c/6af4d842-e094-83ec-b337-6041f65820c8
Question: P2_FULL_DISPATCHABLE_HEAT_ENGINE_WITH_PHYSICAL_OFF_STATE_PRO_20261112.txt, user 22da44f1-306f-4f6e-b144-959fc7ea91b9. Final: 6623639e-1a33-5fbb-8aaf-b427822c32e7. Observed 2026-11-12 00:17 UTC; UI Pro, completed, empty composer.

The native response is truncated at 20,000 characters. The remainder is transcribed from rendered UI, with table and mathematical formatting reconstructed where visible; it is not full native/database-byte identity. Activity text is excerpted below, not a full expansion of nested activity or helpers. Linked deliverables remain uncollected; their identities/eligibility are unverified. No linked sources or components were opened.

## Available visible activity excerpts

“I’ll treat the thermal disconnect and restart as part of the converter itself. I’ll compare a Stirling-based design with photon-conversion alternatives, then carry the strongest candidate through the ON/OFF heat balance, manufacturing cost and both storage duties.”

“The OFF mechanism now uses insulating jaws that remain inside the store wall and close after the heat pipe withdraws. Keeping them at the same depth preserves their temperature profile and avoids repeatedly inserting a cold plug. The storage design has exposed a separate cost problem: freezing salt around small heat collectors requires substantial heat-spreading hardware. I’m comparing that with a larger, fully liquid store that may be simpler to build.”

“A geometry check caught a substantial loss: withdrawing the heat pipe to reduce output also exposes more hot pipe, so its protective enclosure grows and stores additional heat. That invalidated the earlier, smaller loss estimate. I’m now checking one fixed geometry sized specifically for the graphite store, with the longer enclosure and its warm-up energy included. The $50 production target is still unsupported; the current cost estimate is higher even before lifetime qualification.”

“The fixed design now has a clear result. Its nominal steady calculation is only about 35.0%, and ordinary component variation takes it below the target. The physical disconnect cuts steady leakage to roughly 0.7–0.9 W, but the insulation draws extra heat after closure; at the hottest condition, the model takes about six hours to fall below 1 W. I’ll report those as failures of this design, alongside the energy saved, rather than count the transient as a free OFF state.”

“The cost model now puts this candidate at about $183 per 100 W unit at the requested manufacturing scale, well above the $50 target. I also found an important restart penalty: the moving insulation takes hours to reach its thermal state, so its stored heat must be tracked across cycles. I’m closing that cycle balance and packaging the executable model, with the steady-state calculation kept separate from the performance the complete device has not established.”

“The restart calculation makes the limitation sharper: after a two-hour warmup, the daily case stays below 35% throughout its ten-hour delivery period. The long run reaches 35% only after about 27 hours of generation, under the assumed engine-performance transfer. The modeled storage system also loses the daily cost comparison against the battery scenarios; a modest long-duration advantage appears only with the assumed low graphite price and long component life.”

## Exact native prefix

## Result

**I developed a concrete candidate with a physical thermal disconnect, but it does not meet your combined specification.** Its nominal steady calculation comes close to 35% net efficiency at a much easier temperature, yet the margin disappears under ordinary variation and during restart. Its closure also exceeds 1 W after shutdown, and its production cost is substantially above $50.

The candidate is a **free-piston Stirling converter supplied by a retractable sodium heat pipe, with segmented insulating jaws that remain inside the store wall when the heat pipe withdraws**. The useful mechanism is physical removal of the conducting path followed by restoration of the insulated boundary. I worked through the moving insulation, the resident closure, air cooling, electrical auxiliaries, manufacturing allocation and storage duties.

The deliverables contain the geometry, calculations, source data, executable models, saved results and proposed experiment:

- [:chatgpt-content-reference{index="16"}](https://chatgpt.com/library?file_id=libfile_72cdfb5ef6ec81918bd54bc7e1ad79bc&account_id=personal)
- [:chatgpt-content-reference{index="17"}](https://chatgpt.com/library?file_id=libfile_1a39e439d12c8191bb6ad5aa8af33a33&account_id=personal)

**All candidate performance figures below are calculations, not measurements.** In particular, transferring NASA-class Stirling efficiency to the proposed manufacturing route remains an untested claim.

| Requirement | Candidate result | Assessment |
|---|---|---|
| 100 W useful regulated DC | 24 V, 4.167 A; proposed 50–100 W operating range | Conditional on custom engine performance |
| At least 35% net efficiency | **35.0115%** after complete thermal settling at a 1000°C source well | Only **0.094 W** of heat-input margin |
| Hot surfaces no hotter than 1400°C | Store/interface intended for 910–1100°C; engine acceptor 760°C | Temperature requirement is plausible |
| At most 1 W thermal OFF | **0.75–0.97 W settled**, but **1.63–4.15 W** calculated shutdown peaks | Immediate OFF fails |
| At most 0.1 W electrical standby | **0.05 W** complete-system budget | Plausible, unvalidated |
| At most $50 per complete unit | **$183.04**, before lifetime replacements | Fails by 3.66× |
| Efficient daily operation | **34.68–34.93%** during the modeled ten-hour generating interval after restart | Never reaches 35% during that interval |
| Useful storage advantage | Daily storage loses against the matched battery scenarios; long-duration advantage is conditional | No established system advantage |

This is a failed specific architecture, not an impossibility result for heat engines, TPV, or thermal storage.

---

## 1. The proposed physical operation

### Why choose Stirling here?

Small mechanical conversion already has relevant measured performance. NASA/Sunpower reported **88 W AC at 38% heat-to-AC efficiency, with 850°C hot and 90°C rejection temperatures**. That machine depended on engineered gas bearings, an alternator, a high-temperature heater head, a regenerator, centering and small clearances. Those subsystems cannot be replaced by an assumed cheap engine. :chatgpt-content-reference{index="0"}

A later NASA report provides measured performance maps at a **760°C acceptor**. I use approximately **39.5% at a 65°C rejector** as the empirical anchor, with an explicitly conditional temperature interpolation. :chatgpt-content-reference{index="1"}

Thus the proposed contribution is the **store interface and its disconnection operation**. The engine’s efficiency is credited to prior work.

### Geometry

The reservoir is graphite in a nitrogen enclosure. A blind well accepts the sodium heat pipe without hot mechanical contact. The condenser sits above the evaporator, permitting gravity return.

During generation, insertion depth controls heat transfer. During shutdown, the heat pipe, engine and surrounding hood withdraw together. Fifteen stages of insulating jaws then close the penetration. Each jaw stays at its original axial position, limiting the heat that must be moved between hot and cold regions.



::chatgpt-content-reference{index="18"}



The drawing is a functional section, not a qualified fabrication drawing. The cold bellows, seal arrangement and jaw linkage still require mechanical development.

| Subsystem | Proposed construction |
|---|---|
| Hot pickup | HAYNES 230 bulb, **25 mm diameter × 120 mm long**, 0.5 mm wall |
| Heat-pipe stem | **12 mm outside / 11.4 mm inside diameter**, approximately 0.66 m vapor path |
| Hot clearance | **0.30 mm nominal radial gap**, with 0.20–0.40 mm evaluated |
| Store penetration | **60 mm diameter through 500 mm insulation**; the entire penetration is charged |
| Closure | **15 axial stages**, interrupted parking pockets, 0.15 mm nominal seams |
| Closure structure | 150 μm mullite skins and two 3 mm mullite rods |
| Moving insulation | **240 mm outside diameter** hood; approximately 3.28 kg at the nominal position |
| Mechanical withdrawal | **650 mm travel**, cold self-locking actuator |
| Engine | Proposed 77 mm diameter, approximately 190–210 mm long; 3.5 MPa mean helium pressure |
| Engine dynamics | 105 Hz; 32 mm piston bore; 2.5 mm amplitude; 4.02 cm³ swept volume |
| Radiator | **240 × 200 × 60 mm**, 48 aluminum fins, 1.68 W fan |
| Electrical output | **24 V regulated**, 2.083–4.167 A over 50–100 W |
| Standby supply | 16 Wh battery, protection and charger; recharge losses included |

The nitrogen enclosure extends around the withdrawn hot assembly; the cooling fins remain outside it. The sodium circuit is evacuated and sealed during manufacture. There is no operating vacuum pump.

The gravity-return requirement matters at plant scale: **all converters must mount above the store**. Covering a spherical store with identical converters would incorrectly give downward-facing modules a gravity-return capability.

### What is new—and what is prior art?

The particular integration explored here is:

1. Variable-overlap, noncontact hot pickup.
2. Withdrawal of the complete metal heat-transfer path.
3. A segmented closure whose parts remain at their axial temperature stations.
4. Explicit accounting for both resident and moving thermal inventories.

Withdrawal of heat pipes itself is old. A 1981 patent describes removable heat pipes used to suppress heat transfer. I therefore make no patent-novelty claim for that principle. :chatgpt-content-reference{index="2"}

---

## 2. The full ON balance

I choose **1000°C at the maintained source well** for the nominal converter calculation, **760°C at the engine acceptor**, and **24 V DC output**. The proposed storage application would vary the well temperature, initially targeting 910–1100°C.

The boundary includes the full port, supports, hot enclosure and all heat-transfer paths introduced by the converter. Converter-induced changes to neighboring insulation losses are charged. Unmodified store-wall losses are accounted for separately in the plant calculation.

At steady state,

\[
Q_{\rm hot}=P_{\rm net}+Q_{\rm ambient}.
\]

During transitions,

\[
Q_{\rm hot}+P_{\rm electrical\,import}
=
P_{\rm load}+Q_{\rm ambient}
+\frac{dU_{\rm converter}}{dt}.
\]

### Electrical and thermal operating point

With 98% rectification/regulation efficiency, a 1.68 W fan and 0.20 W controls,

\[
P_{\rm AC}
=
\frac{100+1.68+0.20}{0.98}
=
103.959\ {\rm W}.
\]

The cooling calculation gives a **51.08°C rejector**. Interpolating the measured engine reference to that temperature gives a conditional core efficiency of **40.291%**.

The complete heat balance is then:

| Hot-side withdrawal | W |
|---|---:|
| Heat required by the transferred engine map | 258.022 |
| Additional proposed pressure-neck conduction | 7.312 |
| Pipe, hood, source-plane perturbation, full port and supports | 20.287 |
| **Total \(Q_{\rm hot}\)** | **285.620** |

The corresponding output-side balance is:

| Output or rejected heat | W |
|---|---:|
| Useful regulated DC | 100.000 |
| Engine and neck heat rejection | 161.374 |
| Rectification/regulation loss | 2.079 |
| Control dissipation | 0.200 |
| Fan dissipation | 1.680 |
| Other converter heat rejected to ambient | 20.287 |
| **Total** | **285.620** |

Therefore,

\[
\eta_{\rm net}=\frac{100}{285.620}=35.0115\%.
\]

But the requirement permits \(285.714\) W. **The apparent success is only 0.094 W away from failure.** That is much smaller than the uncertainty in the engine transfer, insulation, cooling or measurement.

The added neck conduction is deliberately conservative: I charge the entire new neck because the old head’s contribution cannot reliably be removed from the measured engine map. This is a screening penalty, not a prediction of the exact difference between the original and proposed engines.

### Finite hot-side transfer

Heat crosses the annular nitrogen gap by conduction and radiation:

\[
Q_{\rm gap}
=
\frac{2\pi L k_g(T_m)(T_s-T_p)}
{\ln(r_o/r_i)}
+
\frac{2\pi r_iL\sigma(T_s^4-T_p^4)}
{1/\epsilon_p+(r_i/r_o)(1/\epsilon_s-1)}.
\]

At the nominal point:

- Sodium vapor temperature: **774.06°C**.
- Inserted overlap: **37.38 mm**.
- Gas conduction: **164.22 W**.
- Radiation: **114.89 W**.
- Total pickup: **279.11 W**.

The difference between pickup and engine input goes into pipe/head insulation losses.

This radiation term is a reciprocal two-surface exchange. There is no cold mirror or credited photon-return efficiency. Radiation absorbed by the enclosure becomes heat and enters the balance. The nominal emissivity, 0.65, is a gray surrogate; 0.45 is used in a sensitivity case. A measured spectral/angular integral would be required for qualification.

The gas conductivity uses an Argonne air correlation as a nitrogen surrogate, with an explicit extrapolation allowance. Its documented temperature range ends below part of this application. That limitation is exposed rather than treated as known nitrogen data. :chatgpt-content-reference{index="3"}

### Sodium transport and air rejection

At 774°C, the NIST saturation relation gives approximately **30.94 kPa sodium vapor pressure**. The 280 W transport screen gives about **62 mg/s vapor flow**, **7.46 m/s velocity**, and **24 Pa vapor pressure drop**, corresponding to approximately 0.072 K saturation-temperature drop. :chatgpt-content-reference{index="4"}

A transferred flooding correlation gives approximately 458 W capacity at 60° inclination. That is useful screening margin, but it does **not** establish sodium wetting, condensing-film performance, noncondensable-gas control or frozen restart.

The radiator calculation includes air heat capacity, fin efficiency, channel pressure drop and thermal contact resistance:

- Airflow: **0.01716 m³/s**.
- Pressure drop: **14.54 Pa**.
- Fin efficiency: **0.585**.
- \(UA\): **18.63 W/K**.
- Rejector-to-ambient resistance: **0.0983 K/W**.
- Heat through the cooler: **163.65 W**.

The fan’s published endpoints and maximum electrical power anchor the calculation; the interpolated pressure-flow curve is a surrogate requiring installed-assembly measurement. :chatgpt-content-reference{index="5"}

### Fixed-hardware sensitivities

I did not enlarge components after these cases failed.

| Case at a 1000°C well | \(Q_{\rm hot}\) | Net efficiency |
|---|---:|---:|
| Nominal, fully settled | 285.620 W | 35.0115% |
| Insulation conductivity +20% | 289.595 W | 34.531% |
| Reference engine efficiency −1 percentage point | 292.535 W | 34.184% |
| Airflow −25%, convection −15%, worse contact | 288.023 W | 34.719% |
| Additional internal engine loss of 3 W | 288.712 W | 34.637% |
| 75 W useful load | 224.705 W | 33.377% |
| 50 W useful load | 166.902 W | 29.958% |

The 50–100 W envelope is useful electrically, but the part-load map remains provisional.

---

## 3. The OFF mechanism works physically, but misses the specified OFF operation

Withdrawal removes the metal path. The jaws restore an insulating column across the port. The OFF model includes:

- The whole 60 mm penetration.
- Insulation and supporting mullite.
- Gas conduction through seams.
- Radiation through fifteen seam stages.
- An edge-loss allowance.
- The inherited temperature profile of the resident jaws.

The parking pockets are represented by a **twofold conductivity multiplier**. Fixed opaque webs remove a continuous axial chimney, but the multiplier is **not a demonstrated upper bound** on every three-dimensional gas, radiation and structural path.

For insulation, the calculation uses manufacturer temperature-dependent conductivity and heat capacity, with explicit extrapolation above the tabulated range. PANEL1200’s conductivity rises from approximately 0.029 W/m·K at 200°C to 0.044 W/m·K at 800°C. Its temperature classification and short shrinkage test do not establish the life of a moving closure. :chatgpt-content-reference{index="6"}

### Calculated shutdown transient

The jaws do not begin OFF in their final steady temperature profile. Their enthalpy is retained when they move radially.

| Source well | Settled withdrawal | Maximum resolved withdrawal | Time until below 1 W | Heat withdrawn over 14 h | Over 144 h |
|---|---:|---:|---:|---:|---:|
| 910°C | 0.751 W | 1.626 W | 0.61 h | 7.85 Wh | 100.22 Wh |
| 1000°C | 0.848 W | 2.760 W | 2.40 h | 11.75 Wh | 117.96 Wh |
| 1100°C | 0.966 W | 4.146 W | 6.10 h | 16.38 Wh | 139.27 Wh |

The solver uses one-second initial steps, but the reduced spatial model does not validate actual first-minute contact and radiation behavior. **It already predicts failure without resolving those details.**

At 1100°C, even the first fourteen-hour average is approximately **1.17 W**. Increasing insulation conductivity by 20%, doubling seams and increasing structural conductivity gives settled leakage of approximately **1.005, 1.146 and 1.321 W** across the three source temperatures.

A settled nominal subwatt value therefore does not establish a compliant OFF state.

### Electrical standby

The complete budget is **0.05 W**, including controls, battery management and allocated monitoring. Over 144 hours that consumes 7.2 Wh. A 16 Wh battery also accommodates the proposed start/stop electrical allowance.

The actuator is self-locking, with no holding current. Its **0.10 Wh complete stroke-cycle allowance** is included within a **2 Wh start/stop electrical budget**. Battery recharge is paid at 94% efficiency.

These are attainable-looking component budgets, but no endurance or standby-power measurement has been performed.

---

## 4. Restart exposes a second failure: heating the converter’s own insulation

The nominal moving insulation contains **129.4 Wh** above ambient. Hot metal and engine components add approximately **28 Wh**, and the cold assembly adds approximately **6 Wh**.

A separate conserved transient model tracks these inventories. It does not reset the hood to ambient or to its steady temperature between modes.

Its energy-equivalent insulation temperature is about 198°C. The calibrated thermal resistances and heat capacity give an **ON time constant of approximately 7.64 hours**.

### Daily cycle

The moving-insulation inventory is:

- Start of generation: **36.93 Wh**.
- After ten hours generating: **104.94 Wh**.
- After twelve hours withdrawn: **27.10 Wh**.
- After a two-hour connected ramp: **36.93 Wh**, closing the periodic cycle.

While that insulation warms, source withdrawal exceeds the fully settled value.

| Generating interval | Beginning | End | First reaches 35% |
|---|---:|---:|---:|
| Daily ten-hour delivery | 34.678% | 34.925% | Never during delivery |
| Cold/long 100-hour delivery | 34.601% | 35.0116% | About 26.82 hours after generation begins |

**Two hours to reach hot-metal temperature is not two hours to reach rated efficiency.**

The schedule also has a direct OFF violation: the final two hours of each nondelivery window are connected preparation. The assembly is actually withdrawn for **12 hours or 142 hours**, rather than the entire 14 or 144 hours. The moving model draws roughly 38 W on average during preparation.

### Full-run energy accounting

The moving model requires approximately 90 Wh daily or 102 Wh long-duration additional source heat above the settled-ON baseline. Replenishing resident-jaw inventory adds approximately 14 or 23 Wh in the corresponding conservative screens.

A **200 Wh periodic restart allowance** covers those modeled cases. It is an accounting allowance, not a synchronized prediction of the complete three-dimensional transition.

A first cold resident assembly adds about **88 Wh**. Nominal cold-start excess is then approximately 190 Wh, while a tested cooling sensitivity reaches approximately 208 Wh. Consequently, 200 Wh is not a robust cold-start allowance.

For transparent full-run arithmetic:

- A 100-hour run charged with **200 Wh periodic restart heat** and the electrical start/stop budget gives approximately **34.76%** net heat-to-electric energy efficiency.
- Using a provisional **300 Wh cold-start reserve** gives approximately **34.64%**.
- Adding the 144-hour OFF allowance and standby electricity gives approximately **34.44%**.

These are charged budget scenarios. The 300 Wh reserve is not a demonstrated startup bound, and none establishes 35% from the first rated watt.

---

## 5. Materials, fabrication and service margins

The proposed engine is sufficiently specified to expose important engineering constraints, but it is not a completed replacement for the ASC internals.

The trial regenerator is a 34/25 mm outer/inner-diameter annulus, 30 mm long, with 90% porosity and 20 μm metal fibers. A flow screen gives approximately **16.5 W pumping loss** and **4.9–19.6 W axial conduction**, depending on effective matrix conductivity.

These are diagnostics inside the engine-performance question; they are not added again on top of a measured engine efficiency. A high calculated heat-transfer NTU does not prove engine efficiency. NASA’s segmented-foil regenerator work illustrates precisely this problem: improved component metrics did not automatically produce improved complete-engine performance when axial conduction was included. :chatgpt-content-reference{index="7"}

The proposed HAYNES 282 pressure neck has three 20 mm sections, increasing from 0.20 to 0.60 mm wall thickness toward the hot end. Temperature-dependent manufacturer properties produce the 7.31 W conduction penalty. :chatgpt-content-reference{index="8"}

Calculated peak hoop stresses are approximately **346, 231 and 115 MPa**. These are membrane screens, not creep-fatigue qualification.

Other consequential requirements are:

- Approximately **10 μm cold bearing clearance**, with micrometre-scale roundness and alignment.
- About **50 μm pickup centering/straightness**.
- Compensation for roughly **0.28 mm bulb-diameter expansion** and **5.5 mm stem expansion**.
- Floating alignment between the metal pickup and graphite blocks.
- A qualified helium/sodium separating wall and welds.
- Clean gas bearings, stable flexures and controlled displacer phase.
- Sodium wetting, frozen restart and compatibility over repeated cycles.
- Jaw abrasion and seam growth, insulation shrinkage and bellows fatigue.

The proposed fabrication sequence is conventional in its constituent processes: form and age the pressure head; machine and join heat exchangers; lap the cold cartridge; assemble regenerator, flexures and alternator; fill and seal helium; clean, evacuate and fill sodium; manufacture the staged insulation cartridge; assemble motion, containment, cooling and electronics; then leak-test and qualify.

**The unproven step is preserving the complete engine’s performance and life through that manufacturing route.**

At 105 Hz, a 100-hour run contains 37.8 million oscillations. Twenty years of regular service involves tens of billions. A 100-hour model or trial cannot establish the needed fatigue, creep or contamination life.

---

## 6. Production cost: the architecture misses $50 before replaceme


## Rendered remainder

[Rendered continuation of the partial heading at the native prefix end. Tables and mathematical typography were transcribed from the visible accessibility view.]

## 6. Production cost: the architecture misses $50 before replacements

At 10 MW/year, production is 100,000 accepted 100 W units/year.

| Item | Modeled cost per unit |
|---|---:|
| Engine, including 90% yield and precision-line capital | $61.82 |
| Sodium pipe manufacture, cleaning, filling and test | $12.00 |
| Purchased hood and resident insulation stock | $47.23 |
| Ceramic skins, links and laps | $3.00 |
| Motion and sealed bellows/receiver | $20.00 |
| Radiator, fan and contact spreader | $12.00 |
| Electronics and 16 Wh battery/charger | $11.00 |
| Frame, final assembly/test and other tooling | $10.50 |
| Final 97% yield allowance | $5.49 |
| Complete purchase cost | $183.04 |

These are manufacturing scenarios, not procurement quotations. Whole-stock allocation matters:

- A 1 × 2 m H282 sheet supplies 136 head blanks at the specified pitch. Purchased allocation is about 97 g per head, versus about 50 g finished.
- The hood requires ten insulation annuli. The cost model allocates two per 600 × 400 mm panel, paying for five complete panels. Three mathematically fit in a tight zigzag, but leave only 0.83 mm between circles and zero outside margin; that yield is not credited.
- Port disks are allocated in complete production lots, with offcuts paid.
- Scrap-sale proceeds are not credited.

The precision line is modeled at $3.5 million, recovered over five years, with utilization and maintenance charged. Four grinders at 4000 scheduled hours and 75% overall equipment effectiveness allow only 7.2 aggregate grinding minutes per accepted unit. The closure requires three million jaw halves annually. Its assumed ceramic cost and yield are unproved. Testing every unit for 100 hours would require approximately 2500 simultaneous fixtures at 4000 fixture-hours/year; the cost model instead assumes short production tests and longer qualification sampling. Even removing the entire $47 insulation allocation and halving the $62 engine allocation leaves roughly $105/unit. No constructed process closes the remaining gap to $50. Replacement is additional. The illustrative component scenario gives approximately $288 per unit including discounted replacement/service, with an assumed major replacement at year ten. That lifetime is not established. If a $185 unit plus service lasted only 1000 generating hours, replacement alone would add approximately $2120/MWh AC. Life is a first-order economic requirement.

## 7. Storage duties, complete energy costs—and an important coupling failure

I evaluated a 100 kW DC plant containing 1000 complete modules, avoiding a separate tiny store for each 100 W converter. Both duties use horizontal graphite slabs with all converters above them:

| Store geometry | Daily duty | Long-duration duty |
|---|---:|---:|
| Graphite mass | 36.0 tonnes | 401.3 tonnes |
| Hot top area | 60 m² | 144 m² |
| Graphite thickness | 0.371 m | 1.720 m |
| Insulation thickness | 0.500 m | 0.500 m |
| Approximate outer diameter | 9.74 m | 14.54 m |
| Charging window | 6 h | 48 h |

The assumed effective graphite conductivity is 50 W/m·K. Measured high-quality graphite can support this order of conductivity, but block joints reduce it. Low-cost porous graphite has been measured around 10 W/m·K up to 1000°C. The model’s $3/kg price for material and joints meeting the higher conductivity is an unachieved procurement target. [Visible link: https://www.osti.gov/servlets/purl/1355904/?utm_source=chatgpt.com]

### The active-length audit

The original store screen spread heat extraction over the full 120 mm well, including its bottom. The converter only credits the inserted sidewall. Correcting that assumption while retaining the original store masses gives:

| Fixed active sidewall length | Daily end well temperature | Long end well temperature |
|---|---:|---:|
| 66.94 mm | 898.7°C | 900.2°C |
| 23.72 mm | 873.0°C | 874.4°C |

At 66.94 mm, the nominal gap transfers only approximately 257/260 W at those end temperatures, below the roughly 282 W requirement including pipe/hood losses. A controller could increase overlap as the store cools, but this changes the location and distribution of extraction. A physically closed variable-overlap trajectory has not been established. Consequently, the following figures are conditional energy and cost budgets assuming the specified electricity is delivered, not qualified plant outputs. The audit script is included; the store was not silently enlarged to restore the desired result.

### Complete energy budgets

The plant assumptions are:

- 286 W/module during delivery.
- 1 W/module throughout nondelivery.
- 200 Wh/module periodic preparation allowance.
- 5 Wh/module closure-transient allowance.
- 98% electricity-to-heat efficiency.
- 96% DC-bus/inverter efficiency.
- 94% recharge efficiency for OFF/start electrical consumption.
- Finite store/insulation temperature evolution and ambient rejection.
- Converter ports removed from native-wall area before their complete losses are added.

| Conditional cycle quantity | 10 h delivery / 14 h nondelivery | 100 h delivery / 144 h nondelivery |
|---|---:|---:|
| Heat during delivery | 2860 kWh | 28,600 kWh |
| Native store-wall loss | 285.0 kWh | 7838.5 kWh |
| Charger rating | 572.1 kW | 782.0 kW |
| Total grid input | 3435.5 kWh | 37,548.1 kWh |
| Assumed useful DC output | 1000 kWh | 10,000 kWh |
| Assumed useful AC output | 960 kWh | 9600 kWh |
| Conditional DC round-trip efficiency | 29.11% | 26.63% |
| Conditional AC round-trip efficiency | 27.94% | 25.57% |

For example, daily thermal input is 2860 + 14 + 200 + 5 + 285.016 = 3364.016 kWh. Dividing by 0.98 and adding battery/control recharge produces 3435.542 kWh of grid input. Initial heating is also charged. The complete initial store/insulation thermal inventories are approximately 20.26 MWh and 196.08 MWh. Minimum cold heating times are roughly 36 and 256 hours, before drying or allowable thermal-ramp constraints. Initial inventory and hot unavailable periods reduce the twenty-year all-energy AC efficiencies to approximately 27.64% and 24.69% in the budget model.

### Delivered-energy cost

The cost calculation uses twenty years, 8% real financing, 90% availability, 20% installation, annual maintenance, charger, inverter, containment, gas system, supports and replacements. It assumes major converter replacement in year ten, partial insulation replacement in year ten, inverter replacement in year twelve, and fan/battery service in years five and fifteen.

| Conditional economic result | Daily | Long duration |
|---|---:|---:|
| Installed cost | $646,172 | $2,379,667 |
| Annual cycles | 328.5 | 32.31 |
| Generating capacity factor | 37.5% | 36.89% |
| Delivered cost with $20/MWh charging | $353/MWh AC | $1027/MWh AC |
| Delivered cost with $40/MWh charging | $425/MWh AC | $1108/MWh AC |

The long store’s graphite alone costs approximately $1.204 million under the $3/kg assumption. At $10/kg, the conditional delivered cost rises to roughly $2300/MWh at $20/MWh charging.

### Does withdrawal pay?

Including restart heat and all paid electrical auxiliaries, withdrawal saves grid energy only if the permanently coupled comparator’s stopped thermal draw exceeds approximately:

- 15.84 W for the daily duty.
- 2.49 W for the long-duration duty.

Those are derived thresholds, not measured incumbent idle losses. Against an illustrative 20 W warm-idle engine, twenty-year present-value energy savings are only $3.83/unit daily and $16.32/unit long-duration at $20/MWh charging, doubled at $40/MWh. The physical closure costs tens of dollars. The supplied 77 W TPV shutter would be a poor standby comparator. Beating it does not establish an advantage over a well-designed conventional engine interface.

## 8. Comparison with strong alternatives

Existing Stirling: NASA/Sunpower supplies the strongest relevant small-engine anchor. A fixed-coupling version with the same cooler, electronics and source is the appropriate comparator. Its stopped leakage and restart must be measured. Existing sodium variable-conductance heat pipes used with radioisotope Stirling systems deliberately bypass heat during engine stops; that demonstrates a different operation from conserving a store’s heat. [Visible link: https://ntrs.nasa.gov/api/citations/20160004351/downloads/20160004351.pdf?utm_source=chatgpt.com]

TPV: The Tervo result is important, but newer air-bridge work is particularly relevant: Roy-Layinde and colleagues reported 43.8 ± 0.5% at 1435°C, using electrical measurements and optically calculated absorbed heat. That is only 35°C above this brief’s limit. It keeps TPV a serious alternative; it does not establish a complete net module, optical return path, OFF interface or $50 production cost. [Visible link: https://www.sciencedirect.com/science/article/pii/S2542435122004834?utm_source=chatgpt.com]

Thermal-battery companies: Antora’s current description includes carbon storage up to 2400°C, heat delivery and steam-turbine power, with TPV integration described for future products. Fourth Power publishes graphite/TPV utility-storage specifications and dispatch/lifetime targets. Those deserve credit, but neither page supplies matched evidence for this 100 W, temperature-limited, complete ON/OFF operation. [Visible link: https://www.antora.com/technology?utm_source=chatgpt.com] Rondo has an operating industrial-heat offering and describes steam-turbine CHP. Its stated combined heat-and-electricity efficiency cannot be used as electrical round-trip efficiency; its products page gives an approximately 4:1 heat-to-electricity delivery ratio for the CHP case. [Visible link: https://www.rondo.com/products?utm_source=chatgpt.com]

Battery comparison: I used an 85% AC round-trip-efficiency assumption, consistent with the NREL 2024 ATB’s 2–10-hour storage assumption. Extending it to 100 hours is my scenario, not an ATB validation. Hardware prices below are scenarios, not current quotations; charging-power sizing, installation, financing and replacement are paid. [Visible link: https://atb.nrel.gov/electricity/2024b/utility-scale_battery_storage?utm_source=chatgpt.com]

| Matched delivered-energy scenario | Daily cost at $20 / $40 charging | Long-duration cost at $20 / $40 charging |
|---|---:|---:|
| This thermal candidate, conditional | $353 / $425 | $1027 / $1108 |
| Battery energy hardware at $100/nominal kWh | $100 / $124 | $658 / $682 |
| Battery energy hardware at $180/nominal kWh | $149 / $172 | $1149 / $1173 |

All values are dollars per MWh AC. The thermal candidate loses daily. Its conditional long-duration advantage over the $180/kWh battery scenario disappears against the lower-cost battery case—and has not survived the thermal-transfer, price and lifetime qualification gates.

## 9. A decisive prototype, rather than a favorable demonstration

The proposed experiment is fully specified in the deliverable. No physical experiment has been performed.

### Build sequence

First build three sodium heat pipes, two full jaw/hood assemblies and the actual sealed motion system. Replace the engine temporarily with a controlled approximately 280 W thermal dummy. This tests transport, closure, actuation, contamination and frozen restart. It establishes no heat-to-electric efficiency. Then install the custom engine, actual radiator, fan, electronics and battery. Access to an engine-development partner is required; an ASC is not assumed to be an available catalog component. Use a guarded graphite source at 910, 1000 and 1100°C, with 35°C inlet air. The ordinary comparator is the same engine and cooling system with permanent heat-pipe coupling.

### Measurements

The full attachment footprint, radial perturbation, supports and hot connections belong inside the heat meter. For OFF, use a low-power electrical-substitution/null calorimeter, calibrated with approximately 0.2–5 W substitutions. Do not infer 1 W by subtracting two approximately 500 W measurements with 1% uncertainty. Meter:

- Reservoir heater input, separately from electrical output.
- Alternator AC and regulated load DC.
- Every imported auxiliary supply.
- Battery energy with matching initial/final state of charge.
- Startup, actuation, standby and shutdown.
- Changing resident and moving thermal inventory.
- Rejected heat as an independent balance check.

### Numerical pass/fail gates

| Test | Required gate |
|---|---|
| Rated delivery | 100 W net at 24 V ±2% for 100 hours |
| Efficiency | Lower 95% bound at least 35% |
| Thermal OFF | Upper 95% bound at most 1 W from closure onward |
| Electrical standby | Upper bound at most 0.1 W |
| Energy closure | Approximately 1% or better, with inventory included |
| Cycling | 100 heated withdrawal/restart cycles as an initial qualification screen |
| Manufacturing | 100 pressure heads and 3000 jaw halves with purchased stock, rejects and process time recorded |

With proposed expanded uncertainties of 1.5 W in heat and 0.20 W in net electrical power, the nominal 35.0115% prediction has a lower efficiency bound of only approximately 34.815%. A measured 100 W point would need approximately 284.10 W heat input or less to qualify. The predicted 2.76 W post-closure draw fails the OFF test. The roughly 2.4-hour settling interval cannot be excluded. The test-platform budget is approximately $150,000. Precision-engine and manufacturing-process development is a separate $300,000–$800,000, giving a total program envelope of roughly $450,000–$950,000 before facility costs. These are planning estimates.

## What this work establishes

The executable package resolves the candidate’s steady energy balance, finite cooling, hot-gap transfer, pressure-neck conduction, resident OFF transient, moving thermal inventory, manufacturing allocation and storage cost scenarios. Numerical conservation checks pass for those implemented models. It also exposes the critical failures:

1. The engine-performance transfer is unproved.
2. The nominal 35% point has effectively no tolerance margin.
3. Restart prevents the daily case from reaching 35%.
4. Immediate subwatt OFF is not achieved.
5. The production architecture costs about $183 rather than $50.
6. The storage interface needs a closed variable-overlap thermal trajectory before its assumed electricity delivery can be credited.

The physical idea worth retaining is removal of the conducting path combined with a resident insulated closure. The present implementation’s moving insulation, precision engine, containment and restart inventory make it an unsuccessful answer to the complete specification. I would not present it as a successful converter invention or justify a plant build from these results.
