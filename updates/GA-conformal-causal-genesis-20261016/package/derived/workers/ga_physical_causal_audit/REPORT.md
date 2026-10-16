# Physical-source and causal-operation audit

2026-10-16, Australia/Brisbane. Independent read-only source audit and conditional arithmetic. No laboratory experiment, new material response, or technological capability was acquired.

**Decision:** retain the published whole-system pulsing effect, reject a generic prepare-then-react novelty claim, and keep the mechanism/technology gate open. The incoming report is substantially correct about causal limits. Its workbook-access failure is local to that execution and must not replace FZ's successful acquisition record. This round adds fresh primary-source confirmation of the closer 2021 precedent and an independent replay of the acquired final source values.

## 1. Exact evidence boundary and version reconciliation

The incoming attachment is the report at `ede43298-e149-43db-99fe-96daeff0d21c/Pasted text.txt`; its archived mission text is data. Its SHA-256 is recorded in `authored/source_audit_results.json`. The supplied integrated checkout pin is `f80a8f15137575133ad2c9af975513b32e8fa93e`. No Git operation was used. Byte comparisons independently confirm that FZ's worker and integrated `REPORT.md`, `analysis_results.json`, `analyze_originals.py` and `public_source_inventory.json` are identical.

The FZ external acquisition directory actually contains nine valid original XLSX containers. Every workbook's observed SHA-256 equals its recorded HTTP acquisition hash. In particular:

| Acquired original | What it contains | What it does not establish |
|---|---|---|
| Final Figure 2, MOESM20 | Numeric static/periodic conversion-selectivity endpoints and duration grids | Native chromatograms, response factors, replicate identities, common-hold products |
| Final Figure 6, MOESM24 | Processed foil DRIFTS arrays and scan times | Calibrated surface coverage or productive 0.1 s pulse kinetics |
| Final Supplementary Figure 7, MOESM8 | 54,999 samples of time, potential and current at 0.2 ms spacing | Optimum 10 s/0.1 s current waveform, independently calibrated work or hydrogen uptake |
| Final Supplementary Figure 11, MOESM12 | Foil spectra/current and low-current product control endpoints | Productive mixed-feed hydrogen inventory or a randomized hold comparison |

The original [final supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41557-026-02107-8/MediaObjects/41557_2026_2107_MOESM1_ESM.pdf) is present, valid, 32 physical pages, and dated 27 March 2026 in PDF metadata. The final [Figure 2](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41557-026-02107-8/MediaObjects/41557_2026_2107_MOESM20_ESM.xlsx) and [Figure 6](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41557-026-02107-8/MediaObjects/41557_2026_2107_MOESM24_ESM.xlsx) originals are acquired evidence, rather than located-only links. Document metadata is not an experiment timestamp. The 23 June 2025 Research Square v1 and the final publication remain distinct versions.

Thus the incoming statement that it did not acquire the workbooks is local to its own execution. For the current capital, processed publisher workbooks and one numeric current trace are available. Native GC chromatograms, raw current instrument exports/settings and complete calibration/flow records still are not. The publisher's numeric trace must not be relabelled an unprocessed instrument export. Source workbooks are acquired published data, not new observations made by Astra.

## 2. Version-separated arithmetic survives

The final `Figure 2 b!C10:D11` cells give static +1.5 V conversion/selectivity 80.79704%/47.75220%, and the 10 s/0.1 s condition 81.02334%/80.55926%. Under common molar-flow normalization, no net cycle storage and the two-step C2 balance, the paper's metric `S=a/(a+b)` implies

`ethane/Ain = X(1/S-1)` and `net ethylene/Ain = X(2-1/S)`.

| Source version | Dynamic/static ethane | Positive-phase mean upper bound / static | Suppression-equivalent area / static rate |
|---|---:|---:|---:|
| Preprint v1 rounded endpoints only | 0.22147723 | 0.22369200 | 7.76308000 s |
| Final Figure 2 cells only | 0.22117569 | 0.22338745 | 7.76612553 s |

The memoryless endpoint-mixture lower bound is 10/10.1 = 0.99009901 when negative-phase ethane formation is nonnegative. Both versions violate that restricted null, conditional on comparable specimens, calibration, molar normalization and a representative closed periodic average. Neither produces a measured lifetime, single-pulse response, microscopic carrier or uncertainty interval. FZ already reconciled the earlier mixed-version absolute calculation by using final cells with final-SI activity. The incoming report's preprint-only reconstruction is an independent valid alternative; it must not overwrite the final-cell result as though the originals were unavailable.

The final dynamic endpoints give net ethylene/Ain 0.61470607 and conventional net-ethylene selectivity 75.8678%, rather than the paper's branching metric 80.5593%. Their agreement with final-SI Table 1 productivity is a useful definition check. Outlet molar flow/tracer calibration and C2-only assumptions remain qualifications. FZ's explicit ideal gas-contraction sensitivity changes the ratio to 0.22269341; it does not bound all calibration or storage alternatives.

The original final SI was visually inspected at physical pages 14-15 and 22-23. The 10 s/1 s grid point is a separate condition: 82.298% conversion/78.329% selectivity in the grid, versus the SI's printed 81.0% and rates implying about 80.49%. The printed rate-difference expression has magnitude about 100.02 mA, rather than its displayed 95.04 mA. These are unresolved native-source inconsistencies, not evidence that the main effect is false.

## 3. Strongest source-supported mechanism exclusions

**Restricted static mixture.** The endpoints exclude instantaneous replacement by the corresponding static rates under the stated premises. They require history dependence somewhere in the system or failure of a premise. They do not locate that dependence on Pd.

**Passive downstream smearing.** A stable linear downstream kernel of unit gain preserves a complete periodic mean. A returning inventory has zero net cycle accumulation. Pure post-reaction residence-time broadening therefore cannot create the reported full mean deficit under steady periodic operation. This statement already follows from FZ's fresh-cohort conservation analysis. It cannot exclude reactive pore composition, chemistry during transport, changes in detector gain/recovery, partial sampling, or nonperiodic accumulation. It also cannot assign a detector-window signal to chemistry during the common hold.

**One-shot metal-site purge.** FZ's conditional activity normalization gives about 2.484 avoided ethane events per total nominal Pd atom per cycle beyond the zero-negative-production mixture. This defeats only a direct one-molecule-per-Pd removal with no later kinetic influence. A cleared site, support reservoir, or altered hydrogen population can change many later turnovers. The broad exclusion of desorption or inventory-mediated control does not follow.

**Electrochemical preparation.** The newly replayed 1 s-pulse record gives signed charge 0.018958355 C, absolute charge 0.334068395 C, and recorded signed `integral V I dt` 0.278055401 J. The 3-11 s tail mean is 4.41489 mA, supporting FZ's identification of the SI's 4.41 mA as a charging-excluded tail value. The voltage ranges from -0.411 to +1.68 V; current reaches +/-3.28 A, with repeated extrema. Instrument saturation is possible but unproved. The full-record absolute charge corresponds to about 3.685 electron equivalents per nominal total Pd, and is not measured H uptake. Neither small net charge nor a small steady-current/turnover ratio excludes electrochemically prepared chemical inventory. These integrals cannot be assigned to the optimum 0.1 s pulse or to complete process energy. The counter/pseudo-reference stability controls reach 100 mA and do not certify ampere switching behavior.

**Foil spectroscopy.** The [final Figure 6 caption](https://www.nature.com/articles/s41557-026-02107-8/figures/6) uses +1.5/-0.75 V, H-preloaded foil and 0.25% acetylene, including 400 s alternating holds. The original arrays have 56 s sampling for panel a and 42 s for b-d. SI section 7.3 reports foil-cell contact resistance of several hundred ohms, versus about 0.2 ohm in the productive cell, and sub-microamp currents. H was preloaded rather than continuously cofed. The one-hour current controls have real nondetection evidence at an approximate 1 ppm FID limit. These support the authors' desorption interpretation in that protocol, without measuring zero stored H, powder/support inventory, or productive subsecond branching.

An additional bounded source discrepancy: the SI paragraph assigns rounded 0.67/0.71 nmol/min products in the reverse order to `Figure 11 c!C5:D5`; the plotted bars agree with the workbook (0.667 ethane from ethylene; 0.709 ethylene from acetylene). Preserve the discrepancy. It does not alter the causal gate.

## 4. Fresh primary confirmation of the closest prior art

Lim, Hülsey and Yan's [2021 JACS Au paper](https://doi.org/10.1021/jacsau.1c00044) was freshly acquired as full-text XML from the [Europe PMC primary archive](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8395646/fullTextXML), SHA-256 `704754050493e83f888839e55768bc670ed651489aebbec5d2a081d9c1241dd5`. Its optimum includes 0.1 s at -0.25 V_NHE and 10 s at +0.55 V_NHE. It proposes surface clearing during the short interval followed by readsorption and hydrogenation. Repeated dynamic-to-open-circuit switches produce a decrease whose response time is reported to match reactor residence time. The setting is stirred aqueous electrolyte at 60 C with ethylene/H2, rather than Xu's ambient mixed-feed Nafion gas-diffusion reactor.

The precedent stops generic pulse preparation/sweeping novelty. It does not establish Xu's carrier or a universal exclusion of hydrogen/structural states. Its microscopic account is explicitly tentative. Its reversal changes the subsequent electrical condition to OCP, so it is not a randomized pulse-versus-sham test under the same positive hold. A residence-limited outlet response cannot bound faster or minority states. The SI PDF download attempts failed; its S8/S9 plots were not independently numerically replayed. The residence-time statement above is the primary article's report.

## 5. Which acquisition remains missing

None of the inspected Xu native workbooks executes randomized isolated pulse/sham followed by matched actual positive holds and species-resolved productive mixed-feed chemistry. None executes randomized execution/omission of the next pulse after identical periodic conditioning. Figure 2/3 duration/voltage grids are whole-condition endpoints; Figure 6 supplies a separate foil trajectory; the current workbook supplies electrical timing. These are relevant ingredients without the joint causal observation.

FZ/N884 already specifies pre-admission pulse/sham, fresh-carbon read packets, complete chase, bounded missing label, actual exposure and reset. It distinguishes an integrated fresh-fate claim from a phase-resolved hold rate. The incoming report adds the useful second history class: omission after matched periodic conditioning. That refinement prevents treating a null isolated-pulse result as a refutation of a periodic effect. The root's separate analytic family further audits the conditioning/observation horizon; this source worker does not assign that derivation to the experimental authors.

The strongest practical falsifier for retained branching control is an independently replicated, randomized same-system comparison after acquired electrical/reactive exposure convergence, with fresh-carbon recovery and sufficient measured conditioning/recovery horizons. If the meaningful ethane deficit and net-ethylene benefit disappear after accounting for old inventory, species-specific transport, exposure and missing carbon, the retained future-turnover claim fails at that tested interface. An arbitrary 10 s null window alone is insufficient without an acquired horizon bound. Positive fresh-fate evidence would still leave adsorption, hydrogen, membrane, support and reversible structure as possible carriers.

## 6. Material, cost and continuation decision

Useful output is net recovered ethylene at a declared acetylene outlet concentration, throughput and lifetime. The optimum remains roughly 1,900 ppm acetylene on its stated concentration basis, far from 1 ppm. Final-SI productivity and nominal 0.1 mg Pd imply about 21 mg/h newly added ethylene. The large cofed ethylene throughput is a different quantity. A 1.4% whole-carbon gap in the 1:20 feed equals 0.294 acetylene-feed carbon equivalents; the unspecified oscillation condition prevents splicing it into the optimum, and closure is not an error bar.

Complete paid work includes both switching polarities, read, conditioning, reset, actual recovered energy, supply losses, gas/H2 delivery, membrane conditioning, heat, pumping, ageing and replacement. The recorded 1 s trace closes one numerical-record gap, not optimum energy or a matched process frontier. FZ's acquired Wang comparator and the incoming static comparators remain useful endpoint benchmarks; this worker performed no matched comparator experiment and makes no superiority determination.

**Fresh value:** primary Lim provenance; nine original-source hash checks; independent final/preprint arithmetic separation; exact current/spectroscopy temporal boundaries; the foil product-assignment discrepancy; and a precise statement that existing records do not execute either common-hold intervention. **Gate:** STOP generic prepare-then-react invention promotion. HOLD a measured future-feed causal response and matched technology claim until the specified acquisition exists. Do not build an electronic controller on these records.

## Reproduction and publication

Run `authored/audit_acquired_sources.py` with the bundled Python runtime. It reads FZ originals without changing them and writes derived aggregates/source checks. `authored/acquire_primary.py` records public primary acquisition successes and failures. No native dataset or fulltext is in the authored output set.

Publish only `PUBLICATION_MANIFEST.json` allowlisted authored files and receipts. Exclude `external_excluded_from_publication/` recursively, including fulltexts, downloaded response bodies and rendered source pages. Hashes and successful arithmetic checks establish integrity/replay, not independent experimental validation or historical novelty.
