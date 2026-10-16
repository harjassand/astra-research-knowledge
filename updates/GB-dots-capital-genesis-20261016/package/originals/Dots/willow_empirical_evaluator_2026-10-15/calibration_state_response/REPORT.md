# Initial-check-state versus later detector response: calibration-only result

## Result
The frozen 264-test family yields **80 significant associations across 13 of 24 checks** at Bonferroni family alpha 0.01 (individual threshold 3.78787878788e-05). These comprise **31/132 determined-tag tests** and **49/132 observed-gauge-proxy tests**. All 264 tests have both tag values represented. This is exploratory evidence of predictive information in the initial check tag, not held-out confirmation.

Strongest observed-gauge-proxy result: physical ancilla q13, coordinates [6.0, 10.0], detector t=3. Tag0: 1315/25259 detector events (5.2061%); tag1: 2649/24741 (10.7069%). Risk difference +5.5009 percentage points; sample odds ratio 2.18332; two-sided exact Fisher p=1.6157e-116; Bonferroni p=4.26545e-114.

Strongest determined ideal-preparation-tag result: physical ancilla q49, coordinates [11.0, 9.0], detector t=3. Tag is ideal constant 0 XOR sweep indices [22, 23], not noisy M0. Tag0: 692/20000 detector events (3.4600%); tag1: 1610/30000 (5.3667%). Risk difference +1.9067 percentage points; sample odds ratio 1.58231; two-sided exact Fisher p=4.55834e-24; Bonferroni p=1.2034e-21.

## Scope and verification
Only the authentic r13 calibration dataset, all 50,000 shots, was read. No r50 measurements, reserved or diagnostic data, author analysis code, decoder training, or parameter tuning were used. The protocol was written and hashed before reading measured shot arrays. The supplied own noiseless stabilizer simulation supplies first-measurement constants, sweep masks, and intrinsic gauge classifications. Actual circuit parsing independently verifies all 264 pairs of consecutive same-qubit raw measurement indices, check spatial coordinates, and zero-based detector time coordinates t=2,...,12. Every tested detector was reconstructed using raw bits plus simulated reference constants/sweep masks and compared exactly with the supplied detector stream: all 13.2 million comparisons agree. Every simulated gauge dependency cancels from each detector. t=1 is excluded as frozen because it directly contains the first measurement.

## Interpretation and limits
Under the full fixed state-independent Pauli circuit, uniform intrinsic gauge variables and suitably randomized known preparation tags should not carry additional detector-error information. The bare RL detector error model does not define a joint distribution with raw gauge variables, so this result does not by itself refute that DEM. Nor does it establish a quantum mechanism or decoder advantage.

Possible explanations include state-dependent readout or gates, time drift, nonrandom sweep assignment, or effects associated with using an actual noisy first measurement as a gauge proxy. The determined-tag findings do not depend on noisy first-measurement classification. Fisher inference assumes the relevant exchangeability/independent-shot sampling conditions; Bonferroni handles dependence among the 264 tests but does not cure drift, shot dependence, or sweep confounding. No post-hoc stratification, threshold adjustment, or causal identification was performed. No held-out performance was assessed.

## Reproducibility and resources
- PROTOCOL_FROZEN.md: pre-count fixed protocol.
- analyze.py: own parser, reconstruction, statistics; installed NumPy/SciPy only.
- all_results.csv and all_results.json: complete 264 rows, all four cells, marginals, risks, differences, odds ratios, p-values, tag types, and mappings.
- verified_mapping.json: actual circuit rec-index and coordinate mapping.
- check_summary.json: all 24 check tag marginals and significant times.
- summary.json: findings and SHA-256 provenance for protocol, script, reference, circuit, and the three measured arrays.

Analysis wall time 0.848 seconds; peak RSS 112.46 MiB. Hard CPU limit 120 seconds; hard address-space limit 1 GiB. Stopped after the prescribed test family; no further data exploration.
