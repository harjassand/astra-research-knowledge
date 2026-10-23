# Ordinary hydrogen peroxide control: paired nitrite/nitrate evidence

## Outcome
A materially better dilute finishing comparator is recovered: the H2O2 control in Yang et al., Nature Communications 16,5437 (2025), DOI 10.1038/s41467-025-60696-3. It measures nitrite and nitrate separately by IC, not nitrate-subtraction nitrite or a normalized signal. The source-data workbook and complete SI are recovered. It supports high retained nitrate concentration at a nominal peroxide dose, but does not fully establish independent instrument/reagent calibration or an exact withdrawal-corrected absolute product inventory.

Primary article: https://pmc.ncbi.nlm.nih.gov/articles/PMC12217076/
Dataset: https://doi.org/10.6084/m9.figshare.28210994.v1
Dataset API: https://api.figshare.com/v2/articles/28210994
Dataset download: https://ndownloader.figshare.com/files/54471086
SI/archive: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12217076/supplementaryFiles

## Exact measurement rows
Source sheet `Supplementary Fig. 1a`, cells A4:G8, provides time, nitrite, nitrate, sum, and three errors. It has a unit-label typo: headers say µM while main Figure1a labels identical nitrite numbers mM. SI PDF page6 axis independently says mM and its caption says initial nitrite0.5mM/peroxide1mM. Read the row numbers as mM on that triangulated basis, retaining the unmodified source.

Time(min),nitrite(mM),nitrate(mM),inorganicN(mM)
0,0.475,0.007089102950030104,0.48208910295003005
10,0.0965883668903803,0.37244140417859795,0.46902977106897825
20,0.019759759759759757,0.4515590200445434,0.4713187798043032
30,0.005165165165165165,0.4688461130554672,0.4740112782206323
40,0.0018468468468468466,0.4718554459645774,0.47370229281142423

All reported errors in SI Figure1 are standard deviations from experimental replicates. Individual replicate measurements/count and covariance are not supplied in these sheets. The sum column is arithmetic, not an independently measured total-N channel. The sum-column SD sometimes equals the sum/difference of component SD, so it must not be treated as independent uncertainty evidence.

The net concentration increase is0.4647663430145473mM and nitrite decrease0.4731531531531531mM. Their quotient is about98.23%, consistent with the article's rounded98.3±0.4% but not proof of the exact replicate-level calculation. Initial nitrate must be subtracted for net production; final nitrate/initial nitrite is a different quantity. There is no explicit98.3% equation in the recovered SI/peer-review text. The source supports original-N attribution by reagent chemistry and paired initial/final measurements rather than isotope labeling.

## Conditions and boundary
SI Table3 experiment18: nominal H2O2=1mM, nitrite=0.5mM, pH3, IC, no continuous-air bubbling. Experiment17 is no-peroxide blank. Main methods specify100mL solution,250mL jacketed quartz reactor,298K,dark,sealed,stirred. General methods mention2h, but this H2O2 data series ends40min. At specific times approximately1mL aliquots were withdrawn and NaOH-quenched before IC. Do not treat final concentration times initial100mL as measured final retained amount. Use explicit assumptions about sampling volumes, time-zero sampling, replacement and whether sampled product counts as recovered. Those details are not resolved by the source table.

The1mM peroxide is a prescribed dose; independent peroxide stock assay, actual delivered dose uncertainty, peroxide consumption/residual measurement, and acid/base delivered amounts are not identified. Nor are IC calibration standards, curves, matrix spike/recovery or blank detection limits. The peer-review comparison to Lee/Lind kinetics is a kinetic consistency check, not analytical calibration.

SI page6 confirms nitrogen-species time courses and reagent conditions. SI page19 separates the0.1mM nitrite/1mM peroxide kinetic experiments from the0.5mM finishing control, preventing transplant of the pseudo-first-order coefficient into the finishing data.

## Side products and blanks
Do not import organic-peroxide deficits into H2O2. The three organic-peroxide arms show substantial missing inorganic N and organic products; H2O2 has a much smaller paired-ion residual. No full H2O2 gas-species inventory is recovered, but its absence alone does not invalidate paired liquid product measurement. The deficit cannot be identified specifically as emitted NOx. A closed-vessel clean solution cannot establish the same retention in continuously sparged captured liquid or an organic-rich matrix.

Main Figure1a source workbook blank NO2 values (mM) are0.46771724958902555 at0min,0.4608298849271583 at30min,0.45224193639816335 at60min,0.44277535287115244 at90min,0.43651153562723205 at120min. No blank nitrate or error column is supplied. Background decay is slow rather than numerically zero. Do not invent a blank correction from unpaired or time-mismatched measurements.

## Retrieval and integrity
- source_data.xlsx:3,826,256bytes. Computed MD5 matches Figshare metadata6c40577dde066864fa158afacfa09e0b.28sheets. Small sheets extracted to JSON; targetedCSV exports preserve units verbatim.
- supplementary.zip: complete EuropePMC response,15members; PythonZipFile.testzip passed all CRCs. supplementary_manifest.json records sizes/CRC32. SI1,683,430bytes,CRC32 79f63b9a. Peer review1,198,589bytes,CRC32 cfa0188b. SI first extracted from the completed deflate member while transfer continued, then independently re-extracted/tested from completedZIP. No unknown code executed.
- SI_fig1.png is renderedPDFpage6, inspected visually for units.
- SI.txt/peer_review.txt are pdftotext layout extractions. No explicit calibration section identified after readingSI and relevant reviewer text/searching calibration/standard/yield.
- PMCweb read succeeded. PMC direct supplementary fetch producedHTML, notPDF. CDNencoded/unescaped URLs produced upstream error text. These failed files are not evidence. Firecrawl scrape did not run because connected account credits were exhausted; no retry or purchase.

## Scoped decision
Admit as a published, source-data-backed, dilute dark H2O2 nitrate-retention comparator with nominal reagent dose and independently resolved nitrite/nitrate channels. Do not call it independently calibrated in the stronger metrological sense without standards/stock-assay evidence. Near-stoichiometric liquid conversion is positive; exact retained original-N moles per delivered peroxide and complete process energy remain conditional. A detailed gas inventory is unnecessary for stating that scoped positive result.
