# PFOS encounter-to-cleavage operation: independent audit

**Scope:** non-photochemical PFOS / perfluoroalkyl-sulfonate treatment concept for dilute, complex water. This is a bounded design audit, not a novelty opinion or efficacy claim. The core chemistry comparison uses three primary papers. The quantitative follow-up adds only the specific PSR2 uptake/capacity data needed for loading arithmetic and one matched resin-radiolysis study to assess the reuse risk; none supplies EB-on-resin efficacy data.

## 1. Frozen first hypothesis: retire as an independent lead

The pre-literature idea in `MECHANISM_FREEZE_01.md` was to capture PFOS on a recoverable cationic porous monolith, then mill it with CaO/Fe so interfacial mechanical activation cleaves C–S and the mineral traps fluoride. The central operation—capture PFOS on carbonaceous material and mechanically mill the loaded phase—is now too close to an existing PFOS/GAC process to stand as an independent lead. A 2025 primary study reports PFOS adsorbed on commercial GAC destroyed by milling with stainless-steel balls/jars, with approximately quantitative fluoride recovery; their proposed mechanism is stainless-steel electron donation mediated by conductive carbon. The paper also reports detection of transient PFOA/PFBA and H/F-exchange products, and no detectable C3–C8 perfluoroalkane in jar headspace. My added CaO/Fe and monolith are material substitutions, not a demonstrated mechanistic distinction. Keep the earlier note as provenance, but do not present it as new chemistry.

This retirement is narrow: the existing study used PFOS-loaded GAC, not the proposed monolith/mineral formulation or a complex-water continuous capture train. It nonetheless defeats the novelty of the core encounter-to-milling mechanism. It also means my initial proposed CaF2 sink is not necessary to obtain high fluoride recovery in the cited GAC/stainless-steel system; I have no evidence that CaO improves anything.

## 2. Second, distinct candidate: anion-exchange capture followed by thin-film electron-beam radiolysis

### Unit operation and proposed chemistry

1. Capture dilute PFOS from water on a strong-base anion-exchange resin in a fixed bed. The quantitative fixture is now PSR2 Plus Cl-like gel polystyrene–divinylbenzene with quaternary-ammonium sites, because a primary PFOS uptake study reports loading data for that resin. The earlier macroporous choice is not supported by those loading numbers. This is the selective/concentrating step, not a destruction claim. Record breakthrough for PFOS and co-occurring sulfonates and quantify the competing-anion/organic matrix.
2. Transfer wet loaded beads to a sealed, recirculating, shallow irradiation cassette with enough aqueous phase to keep the resin pores hydrated. Irradiate with a metered accelerated-electron beam under two source-matched conditions: neutral, deaerated water without alcohol; and an aerated aqueous phase with 10 mM 2-propanol. The chemical hypothesis is that water radiolysis supplies hydrated electrons and, in the second condition, 2-propanol-derived reducing radicals support reductive PFOS transformation near the exchange sites. This is not photochemistry and it is distinct from the first candidate's mechanical activation.
3. Drain and collect the liquid, rinse and extract the resin, capture headspace in a fluoride/organofluorine-compatible trap, then either regenerate the resin with a measured brine wash and reuse it or retain it as a waste phase. Regeneration eluate is an additional PFOS-bearing stream and must be included in the destruction train; regeneration itself does not count as destruction.

The direct PFOS radiolysis paper supports the *solution-phase* chemistry only: it identifies hydrated electrons as the most active species, reports reducing radicals from formate/2-propanol, and finds neutral deaerated solutions or aerated solutions with 10 mM 2-propanol favorable. It reports EB treatment of 0.1 mg/L PFOS in neutral deaerated water, but that observation does not establish resin-bound access, complex-water tolerance, complete defluorination, or an attractive dose/energy at scale. Treat those transfer questions as the main risks. The quantitative follow-up in `EB_QUANTITATIVE_CHALLENGE.md` derives the clean-water D90 extrapolation and resin-site energy scenarios, and records why reuse is unproven: the closest radiation-stability evidence reports exchange-site loss and leaching from related gel anion exchangers under gamma irradiation.

### Minimum falsification matrix

Use matched aliquots with the same measured initial PFOS and total fluorine:

- beam on / beam off for PFOS-loaded resin;
- neutral deaerated / aerated with 10 mM 2-propanol (the source-reported favorable conditions);
- an alcohol-free aerated control and, if resources allow, a deaerated 2-propanol condition to isolate oxygen/alcohol interaction;
- PFOS in solution without resin, at the same PFOS concentration and beam dose;
- loaded non-ionic PS-DVB gel beads lacking quaternary-ammonium sites, if available;
- unloaded resin plus PFOS-free matrix as a radiation/resin blank.

If PFOS is added to external liquid with an unloaded resin, treat that as a preparation-order control: it distinguishes initially free from initially resin-bound PFOS only if beam-on partitioning and transfer during irradiation are independently measured, since PFOS may bind before or during EB. Run a single-PFOS standard first, then a defined competing-anion/organic matrix, then real water. Evidence of cleavage requires parent loss *and* quantified conversion of the initial fluorine to inorganic fluoride, with identified/recovered organofluorine products and closed mass balance. Poor capture, resin damage/leaching, or no gain over solution-only radiolysis are process concerns; none alone disproves that some interfacial PFOS reaction occurred. Missing fluorine prevents a cleavage claim. Adsorption followed by extraction of unchanged PFOS is not cleavage.

### Required inventory, readouts, and operating costs

At every boundary, retain and assay feed, bed effluent, cassette liquid, resin rinse, resin extract/solid, regeneration eluate, gas trap, filters, vessel-wall rinse, and analytical blanks. For each phase measure parent and target short-chain PFAS by isotope-dilution LC-MS/MS, non-target organofluorines by LC-HRMS/19F NMR where feasible, extractable/total organic fluorine by combustion ion chromatography, and inorganic fluoride by ion chromatography. Sulfur accounting should include sulfate and residual sulfonate/solid sulfur; carbon accounting is needed before using “mineralization” (TOC plus inorganic carbon/CO2 and identified fluorinated carbon products). Close F as

`F_input = F_inorganic(aqueous + solids) + F_organic(all liquids + resin + filters + headspace traps) + F_unrecovered`.

Report closure uncertainty and do not hide an unclosed remainder in “degradation.” Measure absorbed dose (kGy) and total wall-plug electricity for the accelerator, cassette pumping, bed capture, rinses, and resin regeneration. Report energy per mass of PFOS captured, per mass of PFOS transformed, and per mole of input F recovered as fluoride. Include 2-propanol use and recovery, brine regeneration volume/salt load, resin capacity loss per cycle, accelerator utilization, and spent-resin disposal. The high-dose operation cannot be called low-energy from pseudo-first-order kinetics alone.

## 3. Strong incumbent comparison (not a head-to-head ranking)

**Capture + destruction / mechanochemical.** The direct GAC/stainless-steel milling paper most closely matches my retired first mechanism and reports near-quantitative fluoride recovery for PFOS-loaded GAC without an added co-milling reagent. That result is a stronger and simpler starting benchmark than adding CaO/Fe. Its reported batch ratio and milling conditions are laboratory conditions; no same-feed comparison or wall-plug energy figure appears in the evidence reviewed here. It does not establish performance for dissolved complex water until capture and transfer are included.

**Hydrothermal alkaline.** The GAC milling paper's own discussion contrasts hydrothermal treatment of PFAS-laden GAC at roughly 350 °C and 16.5 MPa with about 1 M NaOH and near-complete defluorination. This is a mature chemical route to benchmark for concentrated wet regenerates, but it brings pressurized hot-caustic equipment and heat duty. I have not independently audited that cited hydrothermal primary paper in this three-paper source budget, so do not treat the comparison as a quantitative ranking.

**Electrochemical oxidation.** The primary BDD study reports PFOS oxidation to sulfate, fluoride, CO2, and trace TFA; in its flow-through reactor, the rate was mass-transfer limited and pseudo-first-order, with a 5.3-minute half-life at 20 mA/cm². It identifies direct electron transfer as the likely rate-limiting step. This is an aqueous oxidation benchmark, distinct from radiolytic reduction; it does not establish lower whole-system energy or total-F closure versus the proposed capture-plus-EB train.

**Electron-beam radiolysis.** The PFOS radiolysis study is the chemical basis for candidate 2. The cited 0.1 mg/L solution result is especially relevant to dilute feeds, but is not evidence for selective resin encounter or a favorable field energy balance. The proposed novelty, if any, is only the process configuration and transfer hypothesis: capture onto an exchanger, then irradiate hydrated resin in a thin cassette. Reuse is unvalidated, and the elementary reducing chemistry itself is prior art.

## 4. Status and next decisive test

- Candidate 1 (capture + mechanochemical cleavage): **retired as an independent novelty lead** because the core PFOS-loaded-carbon milling operation is already reported.
- Candidate 2 (anion-exchange capture + hydrated thin-film EB reduction): **unvalidated process hypothesis**. The chemistry has solution-phase precedent; transfer from solution to wet resin and the full energy/material balance remain open. Treat the quantitatively anchored PSR2-like exchanger as single-use until measured capacity and selectivity survive EB cycling; the class-matched gamma study makes resin damage a concrete risk, not a presumed failure fraction.
- No claim of complete PFOS mineralization, selectivity across PFAS, successful resin regeneration, complex-water compatibility, environmental safety, or practical cost is established.

The single decisive next test is the matched resin-loaded versus resin-free PFOS EB experiment at equal dose and equal initial total-F, first in clean water and then in a defined competitive-ion/organic matrix, with whole-vessel fluorine and sulfur accounting plus before/after exchange-capacity, breakthrough/selectivity, and resin-leachate measurements. See `EB_QUANTITATIVE_CHALLENGE.md` for the explicit controls and conditional energy ledger. Stop if resin loading confers no treatment benefit or if the measured dose and resin replacement/regeneration burden erase the benefit of concentrating the feed.

## Sources (three primary papers)

1. Zhu et al., “Additive-Free Ball Milling in Stainless Steel Mills Enables Destruction of PFAS on Granular Activated Carbon,” *Environmental Science & Technology Letters* (2025), [DOI 10.1021/acs.estlett.5c00976](https://doi.org/10.1021/acs.estlett.5c00976). Used to retire the first concept and for the cited hydrothermal-GAC context.
2. Trojanowicz et al., “Application of ionizing radiation in decomposition of perfluorooctane sulfonate (PFOS) in aqueous solutions,” *Chemical Engineering Journal* 379 (2020), 122303, [DOI 10.1016/j.cej.2019.122303](https://doi.org/10.1016/j.cej.2019.122303). Used for the EB/radiolytic reducing-chemistry precedent; it does not test resin-bound PFOS.
3. Carter & Farrell, “Oxidative Destruction of Perfluorooctane Sulfonate Using Boron-Doped Diamond Film Electrodes,” *Environmental Science & Technology* 42 (2008), 6111–6115, [DOI 10.1021/es703273s](https://doi.org/10.1021/es703273s). Used as the aqueous electrochemical oxidation comparator.
