# Finite zirconia net-NOx-loss evidence decision

Date: 2026-10-21. Independent source qualification, not a trajectory, rate fit, or surface experiment.

## Decision

No applicable quantitative upper or lower bound on unforced net NO+NO2 destruction was established by this finite review. Keep the inert-surface cycle conditional. Do not use this finding to declare either inert zirconia or fatal product loss. The missing measurement is specific: net, species-resolved product loss per geometric exposed area after surface-inventory reset, on the actual dense/stabilized zirconia grade, under the operating dry oxidizing mixture and thermal history. None of the retrieved evidence supplies that observable at the required conditions.

## Contract and diagnostic meaning

Parent contract: dry original feed 79/21 N2/O2 at 1 atm; retained NO+NO2 at 300 K is the intermediate useful product; N2O is not counted. Gas spans 300–2700 K, solids up to about 2400 K, NOx approximately 1–4%. Parent frozen trajectory reports 2186.6299335 incident NOx molecules per exported molecule. A first-order effective destructive probability 0.05/2186.6299335 = 2.2866237781e-5 gives a nominal 5% loss allowance. This is a sensitivity scale, not a measured gamma, a validated first-order law, a guarantee under feedback, or a periodic-cycle result. Source binding remains the parent's surface_exposure_diagnostic.py/.json.

NO-to-NO2 interconversion preserves this product count. NO/NO2 adsorption can imitate destruction unless the surface is returned to its original state. NOx-to-N2O reduces the chosen useful-product count although fixed nitrogen is retained. Radical recombination can alter homogeneous chemistry and heat flux without being direct NOx destruction. These mechanisms require separate accounting.

## Primary evidence actually inspected

### AVCO 1974: closest high-temperature pebble-bed observation, not a bound

F. A. Hals, Auxiliary Component Development Work at Avco Everett Research Laboratory, Inc., SEAM 14 (1974), tables IV–V and following discussion. Original PDF and extracted text already held by parent; PDF SHA256 6c40ecbbc682c3bcca4eabc5dbfe5293b38b2ea5450c032145072b2ef5c28268.

https://edx.netl.doe.gov/storage/f/edx/2021/05/2021-05-20T05%3A54%3A25.768Z/5de6b860-fb30-4977-82a6-be759031afdf/id550_1974_f-a-hals_auxiliary-component-development-work-at-avco-everett-research-laboratory-inc.pdf

The report describes insignificant practical catalysis on zirconia/magnesia pebbles, without a numerical detection limit. Its quantitative tables instead concern 19.05 mm alumina, 99.5% purity, 3% porosity. Table V gives inlet bed temperatures 3050/3500 F (1949.82/2199.82 K), NO 4960–5080/7800 ppm, and geometric-area rates 6.6/7.0e-9 mol cm^-2 s^-1, normalizing by estimated area above 1000 K. These are NO disappearance observations in combustion gas. They do not furnish zirconia composition, zirconia-specific sensitivity, dry-air pO2, nitrogen product closure, or surface-inventory reset. The qualitative zirconia observation is useful against assuming inevitable large loss, but cannot certify gamma below 2.3e-5. The alumina rate is not transferred here.

### Killa et al. 2013: matching oxide family, wrong observable and regime

Kinetics of Nitric Oxide and Oxygen Gases on Porous Y-Stabilized ZrO2-Based Sensors, Molecules 18, 9901–9918. DOI 10.3390/molecules18089901.
https://pmc.ncbi.nlm.nih.gov/articles/PMC6270243/

Actual 8 mol% Y2O3-doped ZrO2 with Au electrodes; 46–50% porosity, 60–80 nm pores. Dry NO/NO2 0–100 ppm, O2 1–18%, N2 balance, 100 cm3/min, 600–700 C (873.15–973.15 K). Measurement applies 50 mV alternating voltage. It measures impedance, not an unforced net molar N2/N2O production flux. Its atomistic pathway is NO oxidation to NO2, and reported activation energies concern sensor response. Neither these barriers nor their extrapolation supply a destructive surface rate. No area-normalized net-loss rate is available for use here.

### Tsujimoto et al. 2011: composition false friend

Direct Decomposition of NO into N2 and O2 on C-type Cubic Y2O3–ZrO2 and Y2O3–ZrO2–BaO, BCSJ 84, 807–811. DOI 10.1246/bcsj.20100360.
https://academic.oup.com/bcsj/article-abstract/84/7/807/7343406

Publisher abstract identifies yttria-rich coprecipitated catalysts, e.g. (Y0.97Zr0.03)2O3.03, not a zirconia-rich dense YSZ refractory. Its strongest quantitative point is 90% NO-to-N2 conversion at 1173 K without O2 for the Ba-containing (Y0.89Zr0.07Ba0.04)2O3.03 composition. Some oxygen tolerance is reported qualitatively. No matched 21% O2, percent-level NO, dense refractory area rate is supplied by the accessible abstract. Full article was not obtained. This does establish a direct decomposition phenomenon in a different composition, not a transferable regenerator rate.

## Excluded and failed source paths

The 2008 related Y2O3–ZrO2 paper at https://www.sciencedirect.com/science/article/abs/pii/S0925838807009917 returned HTTP 403; no access circumvention attempted. Its search abstract was only a lead, not a rate source. Search leads involving electrochemical oxygen pumping, microwave stimulation, supplied reductants, metal-loaded zirconia, and N2O feed were not used as admitted unforced NOx-loss evidence. No inaccessible full article, search snippet or sensor barrier is promoted to a numeric bound.

## Exact measurement needed to close this uncertainty

1. Specify exposed ceramic composition/stabilizer, density/porosity, impurities, geometric area and roughness, and oxidation/sintering/cycling history. The model uses geometric sphere area, so BET-area rates cannot be inserted without a justified accessibility conversion.
2. Measure time-resolved inlet/outlet NO, NO2, N2O and fixed-N surface inventory across the operating thermal/oxygen range. Baseline homogeneous reaction and empty-reactor residence effects must be separated from surface effects. Gas and solid temperatures are distinct.
3. In N2 carrier, new N2 from NO is masked by a huge background. A suitable isotopic balance or comparably validated differential method would be needed for a low-loss bound. This is a specification, not a newly proposed authorized experiment.
4. Include cycle completion/desorption/oxidation reset; distinguish temporary storage from exported-product loss, and destructive pathways from NO/NO2 exchange. Bound detection/calibration error against the integrated ~5% allowance, not only against inlet NO signal.

Without this evidence, physically adverse and benign net surface histories remain compatible with the available sources. No Arrhenius extrapolation or kinetic trajectory has been run. A conditional mathematical surface-tolerance sweep could identify the threshold needed for a future claim, but could not establish material admissibility.

## Work and stopping boundary

Finite primary-source web inspection plus read-only inspection of existing AVCO source. New computation is only exact unit/diagnostic arithmetic in conversions.py. No paid access, external outreach, hardware, solver restart, or new chemistry experiment. Web service CPU/memory/cost are unavailable; local conversion resource receipt is saved separately. Stop this evidence search here: it has identified the precise missing observable and rejected the closest tempting misapplications, without asserting literature exhaustiveness.
