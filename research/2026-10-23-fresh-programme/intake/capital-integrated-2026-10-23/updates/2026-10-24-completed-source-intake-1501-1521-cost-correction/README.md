# Safe shared-actuator acquisition cost correction — 24 October 2026

This append-only correction fixes one resource-bound transcription in the [15:01/15:21 source intake](../2026-10-24-completed-source-intake-1501-1521/README.md). The initial checkpoint, README, and manifest remain byte-identical because their hashes are pinned; this record supersedes only the specialized safe-acquisition exponent. The [correction manifest](source_manifest.json) records the exact prior hashes and the pinned source range.

## Corrected cost distinction

The [safe shared-actuator source](../2026-10-24-completed-source-intake-1501-1521/source/dispatch/U_frozen_safe_shared_actuator_acquisition_20261024/next_unit/differential_noise_frontier/SAFE_SHARED_ACTUATOR_ACQUISITION.txt) gives a conservative elapsed safe-acquisition bound

`O(d_L^-2 eta_P^-5 log(K/alpha_c))`,

plus its preparation logarithms, the earlier contrast stage, and readout/reset work (source lines 354–361). At `eta_P ~ delta^(4m+10)`, it gives safe-source time `delta^(-20m-50)`, before confidence, contrast, and preparation logarithms and classical work (lines 390–393).

The distinct earlier specimen-operation time is `delta^(-4m-19/2) log(1/delta)`. The source says safe acquisition can dominate that operation time and asserts no total-cost improvement. The earlier intake summary mistakenly used the specimen-operation exponent as the safe-source-time exponent; do not use that exponent for acquisition cost.

## Scope

This corrects the cost transcription only. The supplied shared-response premises, source-reported internal review, missing physical response data and hardware, and unknown affordability or advantage remain unchanged. The preserved root, the other four selected roots, and their receipt bytes are not changed or duplicated.
