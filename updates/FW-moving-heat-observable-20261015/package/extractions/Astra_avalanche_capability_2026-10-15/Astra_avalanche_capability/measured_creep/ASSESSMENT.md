# Measured creep-lifetime acquisition: bounded success, physical calibration still blocked

## Result

Acquired 303 published individual Kevlar/epoxy composite-strand creep lifetimes: 100 at 440 ksi, 103 at 424.8 ksi, and 100 at 404.6 ksi. Independent Weibull-versus-exponential comparisons do not reject in any cohort. An exploratory KS check in the middle cohort has unadjusted p=.0323, but this is not significant under even a three-cohort Bonferroni adjustment and is not a firm memorylessness rejection. The two-cohort effective mean-life load exponent is approximately 47, conditional on comparable cohorts. Neither result identifies elementary fiber hazards or validates the thermal avalanche model.

## Exact source and provenance

Ernest Y. Robinson, *Design Prediction for Long Term Stress Rupture Service*, NASA archival citation 19950021870.

https://ntrs.nasa.gov/api/citations/19950021870/downloads/19950021870.pdf

Downloaded 911,443 bytes. SHA256 fd40e7c500fbeaa547debfe6f1a771bbf4a0966914ffc8b158c2fb9e2454ae3a. `nasa1995.pdf` is a filename based on the archive citation, not the publication year. The saved NASA API metadata verifies the conference-volume publication date as 1992-09-01.

Source trail:
- PDF page 2 (Introduction): explicitly identifies the LLNL Kevlar composite-strand observations from reference 2 as the data in Appendix B.
- PDF page 11 (References): reference 2 is R. E. Glaser, *Statistical Analysis of Kevlar 49/Epoxy Composite Stress-Rupture Data*, UCID-19849, Lawrence Livermore Laboratory, September 1983, also in Composites Technology Review (1985).
- PDF page 19: Appendix B caption, Kevlar composite-strand data tables and plots, based on reference 2.
- PDF page 21, printed page 1609: 440 ksi, R=.87, N=100, median=2.795 hours. Each of ranks 1–100 has a numerical 'Life - hrs' observation.
- PDF page 23, printed page 1611: 424.8 ksi, R=.84, N=103, median=12.52 hours; 103 numerical ranked observations.
- PDF page 25, printed page 1613: 404.6 ksi, R=.8, N=100, median=150.7 hours. Each of ranks 1–100 has a numerical 'Life - hrs' observation.

These are republished measurements, not an original instrument export. Observed hour columns are distinct from the table's rank-based probability, modulus estimates, and predicted normalized-life columns. No predicted values were extracted. The scanned tables were rendered and visually checked; upright numeric-table images are `page21rotated.png`, `page23rotated.png`, and `page25rotated.png`. CSV values preserve the table's hundredth-hour precision. Apparent OCR/transcription errors were corrected against those images before final computations.

All three selected tables contain an observed positive lifetime for each rank through the stated N and no censor marks, supporting complete-cohort analysis. The source separately shows an incomplete lower-load cohort (N=50, only four lifetimes) on PDF page 28; it was deliberately excluded because runout times and censoring histories were not recovered. Completeness of the selected published cohorts does not establish that there were no pre-publication exclusions or undocumented preselection.

The report's summary warns that historic datasets included spurious failures such as grip slippage and discusses cognizant-staff review. The clearest explicit cleaned-data description in the introduction concerns S-glass, so it must not be assumed that every Kevlar exclusion has been independently audited here.

## Metadata and remaining acquisition gap

Recovered: Kevlar 49/epoxy single-end composite strands, LLNL program, specified nominal stress in ksi, normalized load relative to median strength, elapsed hours, cohort size, complete published lifetime lists. These are strand tests, not individual bare fibers and not seven-fiber carbon microcomposites.

Not recovered: exact temperature/humidity, gauge length, matrix formulation/cure, specimen identifiers and batches, loading ramp, proof loading or preconditioning, inclusion/exclusion log, and original instrument data. Consequently this is a useful published-data statistical fixture, not a fully specified constitutive validation dataset. Temperature must not be guessed as room temperature. Common environment/batch across cohorts is an assumption, not verified metadata.

Primary-original acquisition blockers: Glaser UCID-19849/ADA305435 is indexed as containing raw data, but the opened public mirror's PDF route returned an HTML application shell; no original PDF acquired. Cornell's 2017 Engelbrecht-Wiggans dissertation repository lists a 41.52 MB PDF with a T1000 COPV example dataset, but its current and legacy download links returned empty/502 responses. The cited NASA/TM-20240007134 API record returned 404. No login, outreach, payment or third-party software execution was attempted.

## Independent statistical results

`analyze.py` is our own code, using installed NumPy/SciPy. It creates the CSVs and `results.json`. Each cohort is analyzed separately with exponential scale estimated from its sample mean and a two-parameter Weibull with zero location. Null p-values use 20,000 iid exponential cohorts with both models refitted; thus they are not naive known-parameter KS p-values. Seed 82976. Weibull shape CIs use 5,000 nonparametric bootstrap resamples. Published rounding is small compared with these lifetimes and treated as negligible; no microscopic interpretation is made.

- 440 ksi: mean 4.0046 h, median 2.795 h, Weibull shape .96260 (bootstrap 95% interval .8340–1.1426). Exponential-vs-Weibull LR p=.63162; refitted exponential KS p=.92645.
- 404.6 ksi: mean 209.168 h, median 150.7 h, Weibull shape 1.08391 (interval .9360–1.2908). LR p=.31603; refitted exponential KS p=.07990.

The endpoint tests fail to reject exponential specimen lifetimes. They do not prove memorylessness; modest sample sizes, latent heterogeneity and incomplete history metadata remain limitations. In particular, a nonexponential specimen lifetime would not refute exponential elementary clocks combined with load sharing, thresholds and avalanches.

A separate descriptive comparison gives mean-life ratio 52.2319 while load ratio is only 1.08749. If the two cohorts are comparable and mean life scales as stress^(-rho), the two-point effective rho is 47.1613 (nonparametric bootstrap 95% interval 44.0608–50.3512). Under independent exponential cohorts the exact F-based interval is 43.8472–50.4754. This challenges rho=2 as an **aggregate specimen mean-life law for these comparable cohorts**, which predicts only a 1.18264 ratio. The tiny model-conditional F-test p-value in results.json must not be promoted as robust evidence once cohort comparability is uncertain. Two endpoint stress levels cannot discriminate power-law from linear-stress activation. The additional held-out middle cohort is tested below; none establishes extrapolation to service loads.

No specimen-rate estimate is substituted for microscopic lambda_i. No time/temperature unit conversion or activation-energy calibration is claimed.

## Useful falsification experiment for the active model

The current count-only exponential model predicts stationary waiting times at fixed surviving set, fixed force and fixed temperature. It does not generally predict an exponential whole-specimen lifetime. A discriminating experiment must observe fiber breaks or local load-transfer state, not just final lifetimes.

Use matched microcomposites with recorded material/cure, geometry, calibrated temperature, force trajectory and synchronized break imaging. Compare constant-load controls to proof-load/hold/reload histories; record break positions, survivor identities, local strains and transfer lengths. At matched surviving set and current force/temperature, test whether next-event hazard depends on time since the last break or prior hold, and whether break-location probabilities depend on evolving transfer length. Matrix-creep transfer models predict such additional state dependence. Predeclare censoring and imaging detection limits, analyze risk intervals (including no-event intervals), and compare held-out event-history likelihood or time-rescaling residuals for the microscopic alternatives. Hidden thresholds/strength disorder can itself produce apparent aging after conditioning on counts only, so survivor count matching is insufficient. An independent strength/defect calibration or an explicit latent-disorder likelihood is required.

This dataset closes the 'no measured numerical observations acquired' gap, but not the coupled microcomposite physical-validation gate.

## Third-cohort check and multiple testing

The 424.8 ksi table has 103 observations, not 100. Its mean is 23.00243 h and median 12.52 h. Weibull shape=.91332, bootstrap 95% interval .80435–1.06269; refitted Weibull-versus-exponential LR p=.23459 and refitted exponential KS p=.03235. Because three cohorts and two different checks were examined, this isolated nominal KS result must not be promoted as a preselected confirmatory rejection. Bonferroni over just three KS checks gives .09705; including all six exploratory tests is still less decisive. Weibull alternatives also cannot detect every nonexponential distribution.

Using only the endpoint cohort means to set two aggregate mean-life laws, the middle-cohort predicted mean is 21.88790 h for log(mean life) linear in stress and 21.01969 h for log(mean life) linear in log stress. The observed 23.00243 h gives ratios 1.05092 (nonparametric bootstrap 95% interval .82057–1.33365) and 1.09433 (.85258–1.38847), respectively. Independent resampling of all three cohorts (20,000 replicates; same recorded RNG stream) propagates endpoint uncertainty. Neither mismatch is resolved by these data, and the two predictions differ only about 4%. Thus recovering a third cohort supplied a real held-out check, but did not identify the stress law. Wider stress separation, more precision, and verified comparable metadata are needed.

A complementary history check would reverse two prescribed load segments while holding their durations and integrated instantaneous specimen hazard fixed. A scalar memoryless specimen model predicts equal end-survival in the two sequences. Observed order dependence could reject that scalar model but would not uniquely identify matrix creep: internal load sharing, threshold selection and noncommuting state generators can also yield order dependence. This is a model-discrimination design, not a claimed novel experiment or result from the current data.
