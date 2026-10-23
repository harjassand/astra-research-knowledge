# Cycle 6: electrodeless split-feed jet quenching, not a completed reset device

22 October 2026 UTC. Free primary-source inspection and plotted-data readout. No outreach, purchases, CAPTCHA interaction, hardware action, or new kinetic/flow trajectory.

## Decision

Select Vashisth et al., Chemical Engineering Journal 543 (2026), 178575, DOI https://doi.org/10.1016/j.cej.2026.178575, as the strongest *recovered matched-total-feed experimental comparison* for this pass. It is an operating dry-air, electrodeless microwave reactor with a 10 SLM plasma feed and a separate 10 SLM cold-air jet feed, compared with a conventional 20 SLM plasma feed. This avoids making the quench surface an arc attachment. At equal reported microwave/plasma power and 1 bar reactor pressure, the measured outlet NOx rises and the source's microwave-boundary energy cost falls.

Admit that whole-apparatus result and this architecture as a real comparator. Do NOT admit it as an identified isolated quench mechanism, a certified intact steady-reset device, a measured heat-recovery system, a wall-plug efficiency result, or a retrofit of the saved heater. Critical thermal, material, power-metering and species-flow evidence remains missing. Cold-feed mixing redistributes energy within the apparatus; it is not itself net heat export.

The most important new comparator is present, not absent: Fig. 13b also compares non-quenched 10 SLM operation with 10+10 SLM forced quenching, using NO molar flow rather than just concentration. But that comparison is CFD only. It cannot be promoted into an experimental 10 SLM hot branch plus late, chemically inactive 10 SLM dilution control.

## Primary sources and receipts

1. 2026 full publisher-layout paper, openly deposited by Chalmers: https://research.chalmers.se/publication/552848/file/552848_Fulltext.pdf . Institutional record: https://research.chalmers.se/publication/552848 . Saved as `2026_forced_intrinsic.pdf` and `.txt`. The institutional PDF was downloaded successfully. No request was made to solve or bypass the publisher CAPTCHA previously encountered by the project.
2. The same group's predecessor apparatus/thermal study: Tatar et al., CEJ 497 (2024), 154756, DOI https://doi.org/10.1016/j.cej.2024.154756 . Open institutional PDF: https://research.chalmers.se/publication/542707/file/542707_Fulltext.pdf . Saved as `2024_intrinsic.pdf` and `.txt`.
3. Shen et al., DOI https://doi.org/10.1088/1361-6463/ade3e6, arXiv https://arxiv.org/html/2504.20952v1 . Inspected to classify it, not used as measured hardware evidence. It is an atmospheric-pressure CSTR/PFR forced-wall-cooling model. Its modeled apparatus does not supply the missing material/thermal proof. No renewed missing-state-package audit was undertaken.

Hashes of the archived PDFs are in `SHA256SUMS.txt`. Original embedded plot rasters were extracted without redrawing: `page9_image0/1.jpeg` are Fig. 7; `page10_image0/1.jpeg` are Fig. 8; `page14_image0/1.jpeg` are Fig. 13; `page15_image0.jpeg` is Fig. 14. Whole-page renders preserve captions and context.

## Supplementary-file scope limit

A bounded check of the public Chalmers record and embedded PDF links found only the main PDF and article DOI, not a direct supplementary file. One web-tool retrieval of the public ScienceDirect article returned HTTP 403; it was not retried and no CAPTCHA was solved. Exact-identifier public-index queries produced no supplementary-file link. The actual supplement was therefore not inspected. All absence statements below about metering, uncertainty/duration, dimensions and material/reset evidence are limited to the recovered MAIN ARTICLES. Main-text references to simulated fields in Figs. S1/S2 do not establish the supplement's complete contents. Full receipt: `SUPPLEMENT_ACCESS.txt`.

## Actual geometry, feed and power boundary

2026 section 2 and Fig. 1 describe a quartz tube of 26 mm internal diameter inside a WR340 waveguide, energized by a 2.45 GHz solid-state microwave generator rated at 3 kW. Actual experimental settings are 400, 500, 600 and 700 W, at reactor pressure 1 bar. The abstract's 400–800 W phrase is not evidence for an 800 W measured point: Fig. 7 and the experimental text stop at 700 W.

The working gas is dried compressed air. Total original feed is 20 standard L/min for both measured configurations. The split case sends 10 SLM tangentially to sustain the plasma and 10 SLM through two opposed perpendicular jets toward the centerline immediately downstream of the plasma. The 10 SLM is the combined quench flow, not 10 SLM per jet. The ordinary case sends the full 20 SLM through the primary feed. No water or argon quench stream is added.

The 2026 main text does not give a measured dry-air analysis. Its 2024 predecessor explicitly uses a 79/21 N2/O2 composition in modeling; dried compressed atmospheric air is not automatically certified binary 79/21 gas. No humidifier/dryer energy or compressor energy is reported. SLM reference temperature and pressure are not explicitly stated in the recovered main text.

Jet position is stated as x/D = 8.08, hence about 210 mm for D = 26 mm, within the paper's coordinate convention. Numerical jet-orifice diameter, wall thickness, and manufacturing drawing are not supplied in the recovered main article. A model heat source has maximum radius 2.4 mm. Its shape and power distribution are imposed identically across modeled configurations, informed by auto-exposed plasma images. That is a CFD control, not a measured proof that the actual upstream plasma states are identical when the feed is halved.

The 2026 source calls P plasma power or input power and defines SEC as input power per mol fixed N. It does not describe forward/reflected microwave measurements, coupler calibration, electrical supply efficiency, or wall-plug metering. The 2024 predecessor Table 4 explicitly labels 400 W as absorbed power. That makes an absorbed-microwave interpretation plausible for the platform but does not certify the 2026 metering convention. All numerical energy-cost findings here remain at the reported power boundary.

## Measured comparison and transparent digitization

Fig. 7 black circles are measured outlet NOx; red diamonds are CFD. Fig. 8 gives corresponding SEC. The following values are digitized from the original embedded raster, not supplied raw data. The paper's main text summarizes a roughly 14–17% experimental SEC reduction. The plot readout gives approximately 13–18% across all four settings, consistent with a modest rounding/summary discrepancy rather than an exact universal 14% lower bound.

| Reported P (W) | 20 SLM NOx (%) | 10+10 SLM NOx (%) | 20 SLM SEC (MJ/mol N) | 10+10 SLM SEC | Concentration gain |
|---:|---:|---:|---:|---:|---:|
| 400 | 0.853 | 0.988 | 3.21 | 2.77 | 15.8% |
| 500 | 1.064 | 1.220 | 3.23 | 2.80 | 14.7% |
| 600 | 1.206 | 1.421 | 3.40 | 2.88 | 17.8% |
| 700 | 1.343 | 1.625 | 3.56 | 2.94 | 21.1% |

Readout uncertainty is about ±0.0124 percentage points for concentration and ±0.018 MJ/mol for SEC, using ±2 pixels. The drawn concentration error-bar halfwidths are approximately 0.022–0.034 percentage points for the single-feed case and 0.028–0.040 percentage points for the split case. SEC error-bar halfwidths are about 0.05–0.06 MJ/mol. These describe the drawn bars only: replication count and whether they mean SD, SEM or confidence limits are not stated in the recovered main article. Do not interpret them as a known statistical confidence interval. See `digitization_receipt.json`, `digitized_experiments.csv`, and `digitize_figures.py`.

At 400 W, the paired plotted SECs imply approximately 124 and 145 micromol fixed N/s under the source's power definition. At 700 W they imply approximately 197 and 238 micromol/s. This is inversion of their SEC, not an independently calibrated molar-flow measurement. Do not use these as additional independent evidence.

## NO + NO2 and original-feed accounting

The FTIR is a Bruker Invenio R with MCT detector. Its gas cell is maintained at 0.2 bar to reduce line broadening and prevent N2O4 condensation. The paper labels its measured observable NOx, and discusses nitrogen-oxide production. However, the recovered main text does not give separate measured NO and NO2 fractions, explicit NOx-sum processing, calibration curves, full sample-line loss accounting or a measured total outlet molar-flow correction. The CFD species are only N2, O2, NO, N and O; its NO output cannot by itself verify the requested experimental NO+NO2 sum. Pure NO-to-NO2 conversion preserves the desired count, but unquantified N2O4 or other losses do not.

Conditional normalization can nevertheless show that simple NO2-induced gas contraction is too small to erase the apparatus comparison. If the relaxed outlet contains only N2, O2, NO and NO2, let x = xNO + xNO2 and z = xNO2. Atom balance gives nout/nfresh = 1/(1+z/2), so fixed N per original feed mole is x/(1+z/2). For unknown split 0 <= z <= x it lies in [x/(1+x/2), x]. At the digitized 400 W centers this is 0.008491–0.008527 versus 0.009828–0.009876 mol fixed N/mol original feed. At 700 W it is 0.013337–0.013426 versus 0.016123–0.016254. Thus even the extreme NO2 splits leave a clear positive comparison at the central plotted values.

These are conditional inventory bounds, not certified experimental confidence bounds: they assume the plotted NOx equals the exact requested sum, the four-species relaxed inventory, and no wall/separation losses or leaks. They do not justify doubling the split-feed yield by dividing only by its 10 SLM plasma branch. All 20 SLM remains original feed.

## The 10 SLM ordinary control really exists, but only in CFD

Section 4.2 and Fig. 13 compare modeled axial NO molar flow for three cases: 20 SLM single-feed, 10 SLM single-feed, and 10+10 SLM split-feed. Eq. 15 integrates species molar concentration times normal velocity over a cross-section. Hence this comparison is not an artifact of plotting diluted mole fractions.

At 400 W the authors report a 5.7% modeled outlet NO-flow gain against the 20 SLM case and 9.8% against the 10 SLM case. The latter is the relevant precursor for a partial-treatment-plus-late-dilution ordinary control: chemically inactive 10 SLM dilution added after the 10 SLM reactor would leave its NO molar output unchanged. This is a favorable controlled inference from the source model, not a measured control. The paper does not report a measured 10 SLM reactor plus late-dilution experiment in the recovered main article. Nor does it report measured hot-branch inlet/outlet NOx to isolate retention.

The 54.3% and nearly 70% quenching-efficiency numbers in Fig. 13 are model-specific fractions of the gap between an interior modeled NO-flow peak and an intrinsically quenched outlet. They are NOT absolute hot-state retention fractions, experimental conversion fractions, or efficiencies of the electrical-to-chemical process.

The model's preservation of upstream NO-flow curves is consistent with a downstream intervention but does not establish equality of measured plasma state. Halving primary gas flow changes its nominal P/Q from 1.2 to 2.4 kJ per standard L at 400 W, even though total-feed SEI remains 1.2 kJ per standard L. The whole-device result remains valid without claiming otherwise.

## Thermal integrity, coolant, pressure and reset

2026 explicitly says direct temperature measurements were not performed for the current 1 bar configuration. Its thermal benchmark is the earlier 0.65 bar, single-feed apparatus. Therefore the roughly 3500 K to below 800 K plasma-tail drop, the forced-jet wall-temperature field, and the radical/destruction maps are CFD, not direct measured quench trajectories.

The 2024 platform provides genuine relevant evidence: in-situ Raman temperatures and wall-temperature measurements are reported during steady operation. Fig. 8 contains wall points near 350–400 K at axial positions about 0.18–0.28 m for 20 SLM, 400 W, 0.65 bar; the source concludes the wall temperatures pose no integrity problem. These observations support the possibility of a hot electrodeless plasma surrounded by a cool quartz enclosure. They are not measurements of the added opposed jets at 1 bar and cannot establish the latter's maximum hot spot or long-term survival.

No numerical run duration, repeated restart/thermal-cycle result, before/after dimensional inspection, material mass loss, contamination assay, or long-duration intact-geometry demonstration was found in either recovered main article. Continuous FTIR measurement is not a quantified lifetime experiment. The 2026 paper's steady wall thermal condition is a modeling balance, not calorimetry.

No external water/cryogenic coolant is described. The cold reactant-air stream is the quench medium; ambient free convection and radiation are the modeled final wall heat sinks. No integrated measured heat flux, coolant enthalpy balance, heat-exchanger duty or useful heat-recovery output is given. The source does not close the apparatus to 300 K, 1 bar relaxed product, or provide a recycle/reset energy budget.

The reactor is at 1 bar but the diagnostic gas cell is at 0.2 bar, and Fig. 1 labels the outlet as going to a vacuum pump and FTIR. This is not proof the entire product is compressed back from 0.2 bar; sampling architecture/throughput is not quantified. It also does not authorize zero vacuum energy. Jet delivery pressure, measured differential pressure, compressor/dryer efficiency and pump consumption are missing. A CFD static-pressure map is not an electrical pumping balance.

## What this changes

A real matched-total-feed, matched-reported-power dry-air apparatus gain is now established without attaching an arc to the heat sink, and a modeled 10 SLM partial-treatment comparator is available. This is substantially better evidence than an imposed cooling trajectory or the failed divider. It narrows the next admission gap to experimentally identified power, product-flow, thermal/material and whole-device reset boundaries. It does not remove the finite heat-export obligation or demonstrate a regenerative cycle.
