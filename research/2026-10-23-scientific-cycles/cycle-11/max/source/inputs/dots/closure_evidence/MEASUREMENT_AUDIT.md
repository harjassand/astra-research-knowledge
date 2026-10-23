# Cycle10: measured nitrogen-closure and calibration recovery

## Decision

No independently measured original-nitrogen liquid/gas closure was recovered. The finishing route is **not admitted as high-retention, zero-NOx, oxygen-only, or energetically advantageous**. This is an evidence/access boundary, not physical exclusion and not a claim that the authors never made additional measurements.

The strongest established Cycle9 result remains oxygen-associated nitrate formation in concentrated, illuminated droplets. The newly recovered archive adds useful calibration and sample-mapping evidence, but not nitrogen conservation. Wallace et al. adds a materially better-tested photochemical interpretation; it does not close the nitrogen inventory.

## Provenance boundary

The assigned Cycle9 START_HERE, OMITTED_ACCESS_RECORDS.json, REPORT, CONTINUATION, and nitrite_finishing notes/metadata were read. The omitted Meroni excerpts and omitted Monroe HTML were **not** locally available and were not claimed as read. New web retrieval obtained article passages afresh; those returned passages are saved separately under web_*.json. These files are excerpts/results, not complete locally downloaded article HTML.

No numerical fitting, new reaction-law construction, parameter transplantation, model trajectory, outreach, spending, or hardware action was performed.

## Meroni GRL 2026: freshly recovered measurement definition

Primary: https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025GL120957

The paper uses nitrate/perchlorate Raman-integral ratios with five nitrate standards and 1 M perchlorate. It describes perchlorate as stable/nonreacting; it does not present an independent chlorine-inventory measurement in the recovered article sections. Bulk IC after 1,000-fold dilution shows no nitrate peak compared with a 1 mM nitrate reference. That supports a qualitative starting/bulk control, not a quantitative nitrate detection-limit budget. Nitrite-band disappearance is qualitative.

The main text supplies no independent final nitrite plus nitrate plus emitted-N inventory in the recovered sections. No isotope-control description was found in the indexed main text; the SI remained inaccessible. Thus neither isotope provenance nor tracer conservation was newly certified.

The Zenodo API still reports revision 6, updated 2025-12-23, with the same ten filenames, sizes and MD5 values as the provided Cycle9 metadata. There is no newly listed closure/isotope file. This is a catalog comparison, not a proof about unshared measurements.

Dataset: https://zenodo.org/records/17965118

## Monroe ACS 2025: final article definition

Primary: https://pmc.ncbi.nlm.nih.gov/articles/PMC12086856/
DOI: https://doi.org/10.1021/acsearthspacechem.5c00014

The article explicitly infers nitrite loss by subtracting formed nitrate from initial 4 M nitrite, assuming stoichiometric equivalence and no concentration enhancement. It reports four pure-O2 droplets, nitrate formation (8.0 +/- 5) x 10^-4 M/s, and three N2 controls. This is not an independent retained-N balance.

The final methods describe 0-4 M nitrate calibrants held at 4 M ionic strength using NaCl. An immersion-oil Raman feature normalizes instrument response; it is not a co-dissolved inventory tracer. No isotope-control description was found in the indexed main text. SI access did not succeed, so SI contents remain unknown.

## New primary-data recovery: Monroe's archive, bounded and verified

Primary dataset: https://zenodo.org/records/12537668
Exact archive endpoint: https://zenodo.org/api/records/12537668/files/HONO_Zenodo.zip/content

The current deposit is revision 4, updated 2024-08-04; its metadata describes a manuscript submitted to Chemical Science in 2024. It predates the final ACS article.

The full 4,511,100,478-byte archive was **not** downloaded. A 1,000,000-byte terminal range contained the complete ZIP64 directory: all 397 entries, with count, central-directory size and absolute position verified against ZIP64 end records and repository file size. Eleven small files were then selectively recovered. Every recovered member's length and CRC32 matches its directory record. Total archive bytes transferred: **1,072,474**; extracted content: **115,875** bytes. The full-archive published MD5 was not independently verified.

Files and exact offsets/CRC/source ranges are in monroe_zip_member_list.json and monroe_selected_recovery_log.json. TRANSFER_RECEIPT.json records the transfer.

### What the small files actually establish

1. The calibration README labels five standards as nitrite/nitrate mixtures at total 4 M: 3+1, 2+2, 1+3, 0+4, and 4+0. For the 4+0 case, it instructs use of approximately the first 50 frames before reactant introduction. These are potentially matrix-matched nitrite/nitrate standards. They differ from the final paper's NaCl-matrix description. The recovered material does not resolve which standards were used for the final published fits.

2. The archive's NO2_O2_blanks directories label three droplets “house_air.” The final article describes four pure-O2 droplets. This is an unresolved deposit-to-final-paper mapping seam, not proof of an author error, falsified gas label, or contradiction in the actual experiment.

3. README_HONO explains that the RunParameters fields for droplet radius, initial NO2, O2, and O3 are unused in this dataset. Consequently values such as 100 under initial NO2, 0.21 or 1 under O2, and 0.00274 under O3 must **not** be treated as measured run conditions. Calibration-curve identifiers 16 and 19 do not map themselves to a recovered numerical calibration equation.

4. The README defines kineticsarray.csv's three columns as elapsed seconds, nitrate concentration relative to time zero, and nitrate concentration. It does not define independent nitrite, gas-N, total-N, or isotope channels. The two retrieved traces' first rows at 10 s have concentration-column values 0.374665369871412 and 1.09131317794641. Their final rows are respectively (6000 s, 4.34486989908694) and (5670 s, 2.61053540946193). These are exact archived processed values, **not** newly certified molar inventories, final-paper yields, or feed-blank determinations. The README column description does not explicitly give units, and processing/calibration mapping remains unresolved.

5. The early nonzero values cannot distinguish initial nitrate, rapid pre-observation formation, or processing offset. They neither authorize subtracting an assumed contamination baseline nor validate zero background. The recovered intensity-based alternative columns are not independent chemical replicate measurements.

6. The third droplet README identifies an older processing version and directs readers to a saved slope column. No fit was rerun and no saved slope was promoted into a finishing law.

The complete member-name list and recovered READMEs do not identify a separately named isotope, gas-analysis, or total-N-balance deliverable. The unretrieved large spectral matrices were not examined. The finding is therefore “not recovered/identified in this bounded read,” not “absent from every byte” or “never measured.”

## Wallace October 2026 preprint: closure-specific implication

Primary: https://arxiv.org/html/2610.17021v1
Version dated 2026-10-12; preprint status retained.

Figure 3 compares measured and simulated nitrate after independently normalizing both at 3,000 s. The discussion explicitly notes that the model omits transfer from water into oil, including likely losses of NO, N2O, or NO2, and oil/surfactant electron sinks. Its nitrate kinetic agreement therefore cannot be treated as an absolute nitrate yield or conserved-N validation.

The full local HTML includes main text and SI, and no isotope experiment was located. This source supplies an alternative photon-driven explanation, with measured light-dependence controls handled by the parent investigation, not an original-N closure. Photochemical identification and nitrogen-retention qualification remain separate questions.

## Access limits, with exact outcomes retained

- Wiley direct main-article request: HTTP 403. Fresh web retrieval succeeded for article passages.
- Wiley published SI click: web tool internal error. SI remains uninspected.
- PMC direct article request: HTTP 203, 5,581-byte interstitial, not article text. Fresh web retrieval succeeded.
- ACS SI link and PMC supplementary link: web tool internal errors.
- ACS Figshare DOI supplement: web inaccessible; direct request HTTP 403.
- Europe PMC fullTextXML: timeout, no content recovered.
- NCBI OA endpoints attempted at old and canonical paths: HTTP 404.
- HAL article record: explicit Anubis access-denied page. No attempt was made to bypass it.
- Zenodo metadata and archive byte ranges: HTTP 200/206 successes.
- arXiv full HTML: HTTP 200 success.

The failed PMC HTML is explicitly marked non-evidence in direct_access_log.json. Access records are retained to avoid mistaking failed pages for inspected primary content.

## Admission and stopping condition

The bounded recovery has established the measurement definitions and the available archive mapping as far as the small primary records permit. More raw-spectrum downloads would not, by themselves, create independent gas-N or starting-inventory measurements, and would risk turning this task back into a fit exercise. The search stops here.

Needed for finishing-route admission remains an independently quantified starting-N inventory and paired retained-liquid/emitted-N inventory, with actual matrix calibration and tracer conservation or another defensible inventory method, at relevant capture-liquid conditions. The present data support a mechanistic lead, not practical full-retention finishing.

