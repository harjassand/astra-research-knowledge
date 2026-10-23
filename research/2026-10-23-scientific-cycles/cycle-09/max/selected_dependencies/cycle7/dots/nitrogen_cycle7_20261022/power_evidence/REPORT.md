# Cycle 7: bounded power, pressure and persistent-operation evidence audit

22 October 2026 UTC. Read-only primary literature investigation; no outreach, purchase, hardware, unavailable-supplement hunt, or new plasma trajectory.

## Finding

The bounded search recovers actual microwave-metering and operating-procedure evidence from two close Maastricht apparatus papers. It strengthens the interpretation that the group's “plasma power” means net microwave power, not AC wall-plug demand. It does **not** identify the 2026 opposed-jet reactor's electrical input, pressure cost, long-time wall state or relaxed outlet enthalpy. In particular, it supplies neither a measured penalty that defeats the split-feed gain nor a measured correction that certifies a whole-system gain.

The directly compared 2026 single-feed/split-feed experimental result stays admitted at the reported-power boundary. The newly recovered evidence improves classification, not closure.

## 1. Direct target and predecessor, inspected first

- Vashisth et al., CEJ 543 (2026) 178575, section 2: https://research.chalmers.se/publication/552848/file/552848_Fulltext.pdf . DOI https://doi.org/10.1016/j.cej.2026.178575 . Local received text: `cycle7_received/owner_cycle6/nitrogen_cycle6_20261022/electrodeless_evidence/2026_forced_intrinsic.txt`.
- Tatar et al., CEJ 497 (2024) 154756, sections 2.1 and 4.2 and Table 4: https://research.chalmers.se/publication/542707/file/542707_Fulltext.pdf . DOI https://doi.org/10.1016/j.cej.2024.154756 . Local received text: same folder, `2024_intrinsic.txt`.

The target uses 26 mm quartz, WR340, a nominal 3 kW 2.45 GHz solid-state source, 400–700 W reported plasma settings, total 20 SLM dried air, and 1 bar. Neither recovered main text specifies AC supply metering. The predecessor explicitly labels its 400 W comparison as absorbed power. That predecessor measures gas and wall temperatures at 0.65 bar; the target explicitly reports no new direct temperature measurement at 1 bar. The target's modeled pressure distribution and heat-transfer boundary are not electrical pumping measurements or calorimetry.

The predecessor's cool walls are **not** reassigned to the opposed-jet target. The 0.2 bar FTIR cell pressure is **not** multiplied by the whole process throughput to manufacture a vacuum load. No measured jet delivery pressure, total dry-air supply electricity, pump duty, or long-duration target wall/geometry record was found in these main articles. This is an evidence boundary, not proof the quantities are zero or large.

## 2. Closely related 2025 apparatus: net microwave power is explicitly metered

Helsloot, Samadi, Iqbal, van Rooij and Butterworth, “Trace Methane Destruction within the Effluent of Microwave Plasma,” ACS Omega 10 (2025), 26392–26402. https://doi.org/10.1021/acsomega.4c10550 . Accessible full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC12224103/ , Experimental Details → Microwave Plasma Reactor; FTIR Analysis and Exhaust Diagnostics; Table 1.

A Muegge solid-state source (<1 kW, 2450 MHz), water-loaded isolator and HOMER autotuner/directional coupler are specified. Forward minus reflected microwave power defines plasma power. A Welch membrane pump samples exhaust for the low-pressure FTIR cell. The quartz bore is 26 mm, with a single 1 mm downstream inlet. Its dry-air experiment uses 20+5 SLM, 1020 mbar and 290–615 W, with methane in the downstream stream. No AC-input curve, pump electricity, or wall heat balance is reported in the inspected article.

Inference limit: strong same-lab metering precedent, not proof of target instrumentation. The source rating and downstream geometry differ from the target. Its orifice size, sample flow, reflective loss, and pressure-control details must not be imported into target calculations. The water-loaded isolator is a source-protection heat sink, not demonstrated process heat recovery.

## 3. Closely related 2026 apparatus: small reflected power and timed chemical settling

Azevedo et al., “Transport Control in a Microwave Plasma Reactor to Enhance Ethylene Selectivity in Methane Coupling,” Plasma Processes and Polymers 23 (2026), e70224. https://doi.org/10.1002/ppap.70224 . Accessible primary full text: https://onlinelibrary.wiley.com/doi/full/10.1002/ppap.70224 , sections 2.1–2.2 and 3.1.

This Maastricht apparatus specifies a PinkRF 3 kW 2.45 GHz solid-state source, WR340, water-loaded isolator, three-stub autotuner and 27 mm quartz bore. Reflected power remained below 1% of forward power across tested conditions. Methane operation is at 25–75 mbar, with parallel scroll pumps. Samples follow at least four minutes of continuous flow after setting changes, with steady composition verified. Operational maps distinguish wall adhesion, deposits and unstable regimes. These are actual apparatus/procedure observations, not a measured wall-plug efficiency or thermal endurance qualification.

Inference limit: matching can be excellent on related equipment, but neither the <1% figure nor four-minute procedure is established for the 1 bar opposed-air-jet target. A chemical settling criterion is not a zero wall-storage derivative measurement. Generator brand is not established for the target simply because rating and group match. The specified pump throughput rating is not measured electrical draw.

## 4. One earlier direct loading measurement, expressly nontransferable

van de Steeg et al., “Plasma activation of N2, CH4 and CO2: an assessment of the vibrational non-equilibrium time window,” PSST 29 (2020) 115001, DOI https://doi.org/10.1088/1361-6595/abbae4 . The author's 2022 thesis reproduces this work as chapter 3: https://pure.tue.nl/ws/portalfiles/portal/197469051/20220301_CO_Steeg_hf.pdf . Download archived here as `2022_vandesteeg_thesis.pdf` and extracted text.

Chapter 3, section 3.2 and Fig. 3.1 (printed pages 52–53) reports measured forward/reflected microwave traces for an Ampleon 800 W-peak, 200 microsecond pulse, 4 SLM, 25 mbar experiment. Matching deteriorates during the pulse as plasma density develops. This is directly measured evidence that generator settings and net deposition need not track identically through a changing load. It is **not** evidence for the magnitude of this effect in continuous 1 bar air jets, and is not used to correct their power.

## 5. Exact admissibility condition, not an assumed loss

Let q0 and q1 be the actual fixed-N molar outputs of matched conventional and split-feed operation; let r=q1/q0. Let E0 and E1 be measured complete electrical demands at an identical system boundary and final product state. Split-feed has lower electrical cost iff:

    E1 / E0 < r.

Using only the existing central concentration/SEC plot readouts as the conditional production ratio, r is about 1.158, 1.147, 1.178 and 1.211 at 400, 500, 600 and 700 W. Thus those centers allow about 15.8%, 14.7%, 17.8% and 21.1% greater complete power before losing the apparent advantage. These are not statistical confidence margins and still inherit Cycle 6's product-flow/speciation conditions.

If, and only if, each mode has the same measured generator AC demand S at a given reported setting, write E0=S+A0 and E1=S+A0+DeltaA. The condition becomes:

    DeltaA < (r - 1) (S + A0).

This explicitly shows why unknown common losses do not automatically erase the relative gain: identical extra demand can cancel in the power ratio or favor the higher output per shared overhead. Conversely, neither identical reported RF settings nor total airflow proves S or auxiliary demands identical. Without measurement, no sign or magnitude of DeltaA is assigned.

If one additionally assumes the reported P is absorbed RF, equal conversion efficiency eta, and zero baseline auxiliary demand, the allowable differential auxiliary demand is (r−1)P/eta. The values at eta=1 would be about 63, 74, 107 and 148 W; these are **conditional reference thresholds**, not actual device pumping losses, upper limits on admissible overhead, or a wall-plug result. No generic generator efficiency is substituted.

## 6. Physics needed for closure

At steady operation the net energy inputs equal product enthalpy export plus external heat export and any other outgoing energy. Before steady thermal operation, apparatus energy storage must also be included. An internal cold reactant branch redistributes enthalpy; it does not alone remove heat from the full apparatus. But there is no evidence-based numerical thermal-loss penalty available here.

A matched boundary needs paired AC power, forward/reflected microwave readings and meter calibration, actual auxiliary work for equal delivered feed and final product conditions, corrected molar NO+NO2 output, and a documented steady thermal/endurance interval with wall and outlet information. If useful heat is credited, its delivered duty and temperature require measurement; rejected heat must not be simultaneously credited and charged as missing chemical energy. None of the retrieved nearby apparatus measurements supplies this paired target boundary.

## Search stop and access receipt

Scope was the target, its already recovered 2024 predecessor, and three narrowly linked primary apparatus investigations above. No target supplement search was repeated. A broad manufacturer-efficiency survey was deliberately not performed because the exact target supply/model and load map remain unidentified.

The web tool read the PMC and Wiley primary full texts successfully. A separate curl attempt to archive PMC returned a challenge page, preserved as `PMC_CURL_CHALLENGE_NOT_ARTICLE.html`, not article evidence; no challenge was solved. The TU/e PDF download succeeded and its text was inspected even though the web tool's direct PDF retrieval failed. No refusal or security block was bypassed. Source URLs and section references above are the reproducible evidence trail.
