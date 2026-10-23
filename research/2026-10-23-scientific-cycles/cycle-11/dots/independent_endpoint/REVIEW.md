# Independent endpoint challenge: conditional acceptance

## Result

Direct reading of `peroxide_evidence/source_data.xlsx`, Supplementary Fig. 1a, with independent Decimal arithmetic reproduces the candidate's H2O2 endpoint. The check imports neither `endpoint_ledger.py` nor its inputs/results. `check.py` and `results.json` preserve the raw header and data, workbook SHA256, computations and adversarial alternatives.

The defensible statement is: **At the reported pH 3, 298 K, dilute dark batch conditions, the published IC means support approximately 45.9 micromol net accumulated nitrate in retained plus sampled liquid at 40 minutes per nominal 100 micromol H2O2 charged, or 0.459 mol/mol, conditional on a 100 mL starting batch, four 1 mL pre-endpoint samples including t=0, no replacement, representative well-mixed sampling, and consistent concentration/dilution correction.** This is an observed endpoint accounting reconstruction, not a fitted kinetics result, new experiment, certified delivered-dose assay or process superiority result.

## Accounting proof

With nitrate concentrations A0...A4 in mM and equal sample volume v in mL:

P = (100 - 4v) A4 + v (A0+A1+A2+A3) - 100 A0.

For v=1, retained gross nitrate = 45.2981228126 micromol; sampled gross nitrate = 1.29993564023 micromol; initial nitrate = 0.708910295003 micromol. Therefore P=45.8891481578 micromol. Subtracting the whole initial inventory correctly includes initial nitrate partitioned into withdrawn samples. It is equivalent to computing net growth relative to A0 in every partition. Subtracting initial nitrate only from the final volume would be inconsistent.

The endpoint sample can be counted as retained or withdrawn: 95 A4 + sum(A0...A4) = 96 A4 + sum(A0...A3). It must not be counted twice. The code asserts this identity.

Counting 100 mL at the final concentration AND adding withdrawn nitrate gives a false 47.77657 micromol net product, an overcount of 1.88742 micromol. Counting sampled nitrate twice with the correct 96 mL volume gives a false 47.18908 micromol. Merely ignoring withdrawals gives 46.47663 micromol, 0.58749 micromol high relative to the stated four-sample scenario.

The source says aliquots of approximately 1 mL at specific times, not a metrologically exact withdrawal history. If t=0 is an independent initial determination rather than a withdrawal from the dosed batch, the three-intermediate-sample accounting gives 46.35391 micromol / nominal dose = 0.463539. The 0, 1, 2 mL calculations are sensitivity scenarios, not experimental uncertainty bounds or new no-sampling experiments. If withdrawal preceded reagent charging, both starting inventory and dose timing must be reconciled; one cannot silently retain the four-after-charge assumptions.

## Denominator and rejected interpretations

At v=1, net product / original nitrite inventory is 96.6087%; net product / nitrite lost is 98.2086%; net product / nominal peroxide charged is 45.8891%. Thus the reported approximately 98.3% yield is consistent with a consumed-nitrite selectivity-like quantity, not a peroxide-charge efficiency. It also must not be directly multiplied by initial feed inventory: that gives 46.6925 micromol; multiplying by peroxide dose gives 98.3 micromol, more than twice the independently counted product.

A 1 mM charge in 100 mL is nominally 100 micromol H2O2. No consumption or decomposition correction belongs in the denominator of product per initially charged reagent. Such a correction would change the question to product per consumed reagent. The reciprocal 2.179 mol nominal H2O2 charged/mol net nitrate is a charge ratio, not reaction stoichiometry or measured reagent destruction. Net stoichiometry is one H2O2 per nitrite oxidized to nitrate. No independent peroxide assay or full dose-calibration uncertainty has been established; the result therefore does not satisfy a stronger independently calibrated delivered-dose claim.

## Units and uncertainty

The workbook labels its ~0.475 concentration entries microM. The main methods specify 0.5 mM nitrite/1 mM peroxide, and SI Figure 1 caption and the independently visually checked plotted axis use mM. This is an identifiable workbook-header error, not grounds for silently changing the raw file. The check preserves the microM header and separately adopts mM with provenance. Literal microM nitrate divided by the unchanged stated 1 mM peroxide dose would give 0.000458891, a thousandfold difference. Nitrite-based ratios alone cannot settle this seam because their units cancel.

SI captions explicitly describe replicate standard deviations, not standard errors or confidence intervals. Unknown replicate count, cross-time covariance, blank/calibration uncertainty, volume uncertainty and dose uncertainty prevent a certified CI. For product coefficients (-99,1,1,1,96), the simultaneous coordinate-wise plus/minus-one-source-SD box gives 45.0623 to 46.7160 micromol, or 0.450623 to 0.467160 per nominal dose. This is a deterministic sensitivity rectangle, not a confidence region or a statement of likely coverage. Assuming independent time points would give 0.61190 micromol quadrature SD, but independence is not established.

A concrete covariance warning: if the reported inorganic-N SD is the SD of nitrite+nitrate, its values imply same-time nitrite/nitrate correlations effectively -1 at t=0 and +1 at the other four times. These extreme correlations may reflect very few paired replicates or the source's error construction; they do not reveal cross-time covariance or establish the replicate count. Treating nitrite and nitrate as independently measured random errors when evaluating closure/selectivity is therefore unsupported. The product-only ledger does not need nitrite SD, but its time covariance remains unknown. The nominal-denominator SD rectangle also omits peroxide uncertainty entirely.

## Scientific acceptance and limits

Accept this as concrete evidence of ordinary dark, dilute conversion of aqueous nitrite predominantly into nitrate, with an explicitly reconstructed liquid endpoint product per nominal reagent charge. It is stronger than merely citing nitrite disappearance or 98.3% selectivity. Initial nitrate subtraction prevents known pre-existing nitrate from being credited as product. IC measures the product itself; one need not measure every gas or all nitrogen species to define this narrow quotient.

To upgrade from net nitrate accumulation to independently established original-nitrite-derived product, establish that the nitrate increment is not from changing blanks, N-containing impurities, matrix/interference or dilution artifacts. That can be done by sufficiently validated assays and controls; isotopic tracking is one option, not an automatic requirement. Missing gas measurements do not themselves defeat the quotient, while the approximately 0.84 micromol inorganic-N shortfall cannot be assigned to a specific fate from these data alone.

The retained-plus-sampled analytical boundary is not an isolated or recovered nitrate product stream: samples are quenched and analyzed. It must be matched on a comparator and must not be labeled saleable recovery. The source's dark reaction is a useful conventional counterexample to a need for photons, not an infinite photon-efficiency calculation: division by zero delivered photons is undefined. It gives no matched resource superiority over a photochemical candidate and no plant-energy, throughput, recovery, full-mass-closure, or independently calibrated dose guarantee. Matching concentration, inventory, endpoint quality, time and recovery boundary remains required for any comparative claim.

Source: Yang et al., DOI 10.1038/s41467-025-60696-3; source data DOI 10.6084/m9.figshare.28210994. Local source text directly confirms dark stirring at 298 K, total volume 100 mL, nominal concentrations, approximately 1 mL aliquots and immediate NaOH quench/IC. SI Figure 1 caption confirms pH 3 and replicate-SD error bars.
