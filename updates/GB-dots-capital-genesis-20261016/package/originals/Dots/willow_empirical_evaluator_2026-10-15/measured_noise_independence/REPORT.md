# Willow fixed-DEM structural independence diagnostic

## Result
**No rejection at the prespecified 1% familywise threshold:** 0 of 9,288 same-check detector pairs rejected independence on the 25,000 diagnostic shots. Minimum Bonferroni-adjusted p = **0.0131265456851**, above 0.01. This is a narrow non-rejection, not evidence that the full noise model is correct or that all physical faults are independent. No threshold, family, decoder, or model was fitted after seeing results. The 25,000 reserved rows were not inspected by this analysis.

## Tested implication
For each of the two supplied fixed priors, a detector is a parity of independent Bernoulli error-line variables. Two detectors with disjoint incident error-line sets are therefore independent. The implication does not depend on the fixed marginal probabilities, including arbitrary fixed refits on the same support. It does not follow merely from independence of arbitrary physical faults.

The Stim format treats a complete `error(p)` instruction as one mechanism, including all `^`-separated components; detector targets are XORed across that line. Each supplied DEM has 20,039 error lines, including 14,497 lines with separators. No repeated detector targets cancel in these files. Neither file contains repeat/shift instructions; the parser explicitly rejects unsupported instructions rather than silently flattening them. Ideal-circuit detector coordinates exactly match both DEMs. See [primary Stim semantics](https://github.com/quantumlib/Stim/blob/main/doc/file_format_dem_detector_error_model.md).

## Prespecified family and sample
- Google Quantum AI Willow, d5_at_q8_7, X, 50 rounds, 50,000 published shots.
- Diagnostic 25,000 original zero-based indices: first half after sorting SHA256('astra-willow-split-v1:'+decimal index). Reserved half excluded.
- All 24 spatial checks, including spatial boundary checks; temporal-bulk layers t=1..49 only. Initial t=0/final t=50 excluded.
- Same-check pairs with temporal lag 2..10. Family size 24 × sum(49−lag) = 9,288.
- All 9,288 satisfy disjoint whole-error-line mechanism support in BOTH RL-optimized and SI1000 DEMs. Zero exclusions and zero overlaps.
- Independent interface auditor reproduced the exact family, coordinates, 20,039-line mechanism counts, and zero overlaps; audit artifact: `../measured_syndrome_audit/independent_dem_pair_audit.json`.

This worker wrote PROTOCOL.md and froze model-derived family before reading any measured detector values. The broad acquisition report had already been read and whole-dataset summary diagnostics previously existed; this is a diagnostic analysis, not an untouched confirmatory study.

## Statistics and leading result
Each pair uses one binary observation per diagnostic shot, without pooling different within-shot pairs as independent samples. Test is one-sided exact Fisher/hypergeometric for positive association, conditioned on both margins. Bonferroni over all 9,288 pairs controls familywise error at 0.01 under valid individual tests, without requiring independence between tests. Raw rejection threshold is 1.0766580534e-6.

Smallest-p pair (selected only for reporting, fully multiplicity-adjusted):
- D59 and D203, spatial check (11,9), times 2 and 8, lag 6
- N=25,000; both event margins=1,076 (4.304%)
- n11=80; n10=996; n01=996; n00=22,928
- Independence expected joint count from observed margins=46.31104
- Observed joint probability=.0032; excess joint probability=.0013475584 (0.134756 percentage points)
- Sample odds ratio=1.84900244; phi=.03271761
- Raw one-sided p=1.4132801125e-6; Bonferroni p=.0131265456851
- RL mechanism overlap=0; SI1000 mechanism overlap=0

Runner-up: D659/D827, same check (11,9), t=27/34, lag7; counts (97,1099,1171,22633), sample odds ratio1.70592, raw p3.2345001257e-6, adjusted p.03004203717. Neither passes the prespecified .01 threshold. Do not reinterpret using .05 after seeing these results.

Full 9,288 contingency tables, effects, p values and support checks are in pair_results.csv. results_summary.json contains top10 and lag summaries. There are zero rejections at every lag. Ranking does not establish independent replication; the leading effect estimate is selection-biased.

## Validation and resource limits
The selected index file exactly matches the deterministic split and its frozen SHA256. The analysis seeks and reads only the selected 150-byte detector rows, never loading the full detector file. b8 bits are unpacked little-endian; detector columns are packed into Python integers and counted using bit_count. The leading contingency table was independently recomputed by direct single-byte/bit reads of the same diagnostic rows. SciPy fisher_exact matches the hypergeometric tail exactly for the leading result.

The main run used 1.55 CPU seconds and 153,868 KiB peak RSS, below the 120-second/1-GiB caps. Separate structural-only and bit-check passes were also small. No installs or author code execution. The independent interface auditor reports exact detector parity/reference consistency, including sweep-frame handling; their all-row integrity/parity checks are not outcome analyses or reserved fitting and were not used for selecting this test family.

Hashes:
- PROTOCOL.md: 7b83a950b0110871bdeadaa183563db3149b95a8ded49b5226c45ee17f4fe78d
- frozen_family.json: b18692104a2940a6fcca69e5311c4f4f3381125dbb457d41b9d3f8337e6ebdf1
- diagnostic_indices.txt: 80d49493e16e51d3f2cfe8574ec3316ded74e0a51ae49865165e9def979ee2ae

## Interpretation and limits
The exact p values assume IID shots from a fixed joint distribution. Random row splitting does not establish IID; unknown shot chronology, wall-clock gaps, preparation sweep dependence, latent drift, and filtering remain limitations. Even if a future test rejects, it would challenge the supplied fixed-DEM independence implication under that sampling assumption, not identify a quantum or non-Markovian mechanism. Leakage, drift, sweep dependence, selection and unobserved heterogeneity could all produce association. This study provides no uniform fault-norm bound, hardware theorem, better-decoder claim, or bound on all correlations. Non-rejection has limited power and does not validate model independence.

No reserved confirmation is run. A future reserved-half test requires a separately frozen protocol and its own multiplicity handling; selecting this leading diagnostic pair does not make its diagnostic p confirmatory. r13 calibration values were not analyzed.

## Attribution and reproducibility
Data: [Google Quantum AI, Zenodo 13273331](https://zenodo.org/records/13273331), version 1.0.0, CC BY 4.0. Preserved source provenance and original bytes are documented in `../measured_syndrome_acquisition/REPORT.md`.

Run `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python analyze.py --structure-only` to rebuild structural family without detector values. Remove `--structure-only` to reproduce only the fixed diagnostic-half analysis; the script verifies split identity and enforces memory/CPU limits. Artifacts: PROTOCOL.md, analyze.py, frozen_family.json, pair_results.csv, results_summary.json, independent_bitcheck.json, REPORT.md.
