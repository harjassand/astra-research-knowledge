# Proposed next patch, not executed or experimentally run

Preserve simulator.cpp, simulator, their hashes, and both phases' raw results unchanged. Create separately named simulator_equalreads.cpp and simulator_equalreads only if approved.

## Minimal intended change

Add an explicit correction-budget multiplier beta to the trial entry point, default 1. Accept sweep only with beta=1; allow Toom beta=1 or beta=4. Leave geometry, sweep kernel, Toom kernel, noise rate, RNG streams, readout and logical scoring untouched.

Replace total proposal intensity N*(1+6*alpha) by N*(beta+6*alpha), and event-type noise probability 6*alpha/(1+6*alpha) by 6*alpha/(beta+6*alpha). Both expressions must change together. Conditional noise faces remain uniform over 6 N; conditional correction sites remain uniform over N for sweep or 6 N for Toom.

For Toom beta=4, each face attempts at 4/6=2/3 per unit time. Total logical syndrome inspections are then 2*(4 N)=8 N per unit time, matching the sweep's 8 N. Physical face noise remains alpha and the reported noise/correction-face ratio is alpha/(2/3)=1.5*alpha. This is an equal-logical-check-read convention, still not a hardware/energy/latency equivalence.

Add fields beta, total_correction_attempt_rate, toom_face_attempt_rate (when applicable), check_read_rate, and normalization; derive lambda_over_face_attempt_rate as 6*alpha/beta. Preserve explicit method validation and pin a new hash/manifest. Existing beta=1 endpoints must reproduce all nontiming outputs exactly with identical seeds; new metadata fields are ignored only for that legacy regression comparison.

## Required independent audit before any new pilot

1. Diff confirms only sampler rates, interface validation and truthful metadata changed.
2. Symbolic thinning check: noise event intensity N*(beta+6 alpha)*6 alpha/(beta+6 alpha)=6 Nalpha; correction intensity Nbeta.
3. Re-run existing algebra/kernel/readout suites against the new executable; beta=1 deterministic regression against frozen old binary.
4. Validate rejected unsupported beta/method/rate combinations and new rate fields.
5. Freeze a separate approved bounded grid before executing beta=4 memory endpoints.

Using the same base seed across beta values no longer yields common physical noise event times under the current superposed-clock sampler, because total proposal rates differ. Each trajectory remains correctly distributed, but do not claim identical noise histories or the existing exact common-proposal coupling. Independent physical-noise clock coupling would require a larger separately reviewed scheduler change; it is unnecessary for this minimal patch.

Endpoint-chain persistence is useful for future common-readout comparisons but should be a separate instrumentation patch with independent audit and a versioned binary format. Do not combine it into this minimal rate-normalization change without a new scope decision.
