# Finite quench-evidence decision

Status: closest measured thermal-NOx gas-gas quench found, but NOT matched returned-product qualification. Stop this finite search; no experimentally qualified sub-ms recycle mixing response was established.

## Primary experiment

A. E. Zinchenko, S. I. Serbin, V. Y. Chernyak, *Investigation of the Quenching of Nitrogen Oxide Synthesis Products in Air Plasma*, Ukrainian Journal of Physics 67(1), 44–53 (2022), DOI https://doi.org/10.15407/ujpe67.1.44.

Publisher landing: https://ujp.bitp.kiev.ua/index.php/ujp/en/article/view/2021064
Publisher PDF: https://ujp.bitp.kiev.ua/index.php/ujp/en/article/download/2021064/2437/21209
Retrieved 2026-10-21 UTC. Local PDF and extracted text retained; rendered pp.47 and 51 inspected.

Relevant facts: 5 g/s plasma air, 1–5 g/s fresh quench air, additional 0.5 g/s swirling air; cold streams 300 K; model pressure 101325 Pa. Model inlet 3656 K and plume thermal power 31.34 kW. At 5 g/s quench, outlet approximately 2000 K; reported mean cooling 2.9e5 K/s. Both temperature and rate are indirect: wall calorimetry/enthalpy tables or CFD, with reported uncertainties ±8.2% and ±11.3%. No direct plasma-temperature measurement. Water cooling also removes substantial heat.

Preliminary outlet NOx almost 7 wt% at 1 bar; Testo 350-XL with Environics 4000 sample dilution. No paired inlet/outlet NOx flux or retained fraction. No measured pressure-loss result.

CFD is chemically unreactive and assumes thermal-equilibrium plasma properties, not a validated finite-rate radical/reheat calculation. Precooled reaction products are mentioned as an optional feed, not the tested coolant. Inlet/outlet residence inference is not a measured scalar-mixing-time distribution.

Source locations: setup pp.45–46; assumptions pp.46–47; conditions/table p.48; indirect method/rate/NOx pp.51–52.

## Reproducibility cautions found by inspection

- Equation (9), p.51, literally prints Vg = (TesIn − TesOut)/Les/(VaxIn + VaxOut)/2. With the variable definitions given, this has units K·s/m² rather than K/s. Treat as a suspected typesetting/formula error, not an author-confirmed correction. Do not silently repair it or derive a qualification time from it.
- Boundary-condition text p.47 says six coolant holes, whereas p.50 says four evenly spaced holes. This internal discrepancy precludes treating the schematic as a fully specified transferable injector geometry.
- No numerical quench-section length or injection-hole diameter was identified in the 10-page paper; Figure 2 is schematic. No explicit measured mixing-time or residence-time distribution is reported.
- The NOx datum is a preliminary output concentration, not an NO survival measurement. NO/NO2 fractions and the mass-basis/dilution reconstruction needed for a molar retention audit are not supplied beside that datum.

## Consequence for current recycle hypothesis

Do not substitute fresh-air data for a returned-product operating point. Do not carry the quoted global cooling rate into the 2700→1700 K / R≈0.85 model. Do not assume it establishes sub-ms mixing, because it lacks a directly measured temperature-history/mixing distribution, includes wall cooling, reaches only ~2000 K, and lacks the paired chemical and hydraulic balance.

The exact outstanding qualification observable is a joint measured response at specified fresh-hot and returned-product compositions, temperatures, pressures, and mass flows: parcel or spatial temperature/mixing-age distribution through the 2700→1700 K crossing (including hot tails and recombination reheat), synchronized inlet/outlet NO and NO2 molar fluxes with recycled NOx properly subtracted, and differential total pressure or recycle compression work. A mass-average exit temperature alone is insufficient.

## Patent boundary

US3439196A: https://patents.google.com/patent/US3439196A/en. Its description explicitly routes cool product gas from a downstream low-temperature zone into the MHD-duct/diffuser transition to avoid dilution and suppress diffuser reheat. It is conceptual prior art, not a measured injector qualification for the present dry-air operating point.

## Search stop and excluded leads

Finite targeted web/scite searches identified the selected experiment and two metadata-only alternatives: 10.1016/j.cej.2026.178575 (forced/intrinsic quenching study, no readable primary text returned) and 10.1021/i260037a021 (1971 quenching paper, no accessible body retrieved). Neither supplies evidence here. No claim of exhaustive nonexistence is made. Firecrawl search did not execute because its account had insufficient credits; no payment or top-up attempted. Public publisher access succeeded without a security bypass.
