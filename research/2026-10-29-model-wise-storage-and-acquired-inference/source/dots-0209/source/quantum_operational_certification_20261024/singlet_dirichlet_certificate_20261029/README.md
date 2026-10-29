# Local symmetry tests for a high-rate encoded service
2026-10-29 research delta. Root-originated Dirichlet mechanism; developer and independent-review files retained.

## What changed
A task-specific, high-rate code certificate avoids an exponential global operator-norm lift. For ANY present CPTP channel, permutation-symmetry transition probabilities bound the actual singlet-code Bell loss. An ACTUAL fresh retired-key logical Pauli twirl converts that loss to reference-complete half-diamond error. No collective-noise model is assumed by this certificate. It certifies the specified reproducible channel/horizon, not future bath states or arbitrary time extrapolation.

## Governing files
* `THEOREM_v1.md`: complete-transposition gap, scalar commutant restriction, power-of-two code, positive test, confidence, control errors, strongest conventional comparisons. Independent accepted scope in `independent_audit/RECEIPT_v1.json`.
* `LOCAL_BELL_TRANSITION_TEST_v2.md`: replaces the original long-lived-ancilla test with pair Bell preparation/readout and a classical sign. Same O(n^(5/2)/ε) statistical coefficient. Independent accepted scope in `independent_audit/RECEIPT_v2.json`.
* `SINGLET_WEIGHTED_CERTIFICATE_v3.md`: uses full-singlet calibration mixture and weighted rectangular-map Poincare to reduce statistical coefficient to <2(n−1). New extension; see its own review if subsequently received.
* `WEIGHTED_BRANCH_PREPARATION_v4.md`: explicit signed branch preparations (pair singlet, or fixed four-qubit triplet-coupled singlet seed; randomized spectator routing). Avoids v3's input parity instrument; no quantum reference through storage. New extension; see its own review if subsequently received.
* `check_*` programs/data: reproducible finite-dimensional mathematical simulations, NOT physical measurements or large-n gate synthesis.

V1/v2 are preserved, not overwritten. V3 improves the calibration-state/statistical interface. V4 improves v3's physical preparation. All confidence claims are per prespecified fixed validation block unless a separate confidence-spending rule is supplied.

## Dependencies and unresolved points
The candidate frame and deterministic high-rate Schur compiler are supplied by `../unknown_collective_noise_encoder_20261029/`. The new certificate can validate any fixed candidate frame and does not import the candidate generator's collective-noise promise. Generic efficient discovery for arbitrary noise remains unsolved. Same-channel/reset/accurate-control/record-independence requirements remain real assumptions. Uniform-in-time full-memory protection belongs to the separate stronger joint-algebra theorem, not this validation result.

Direct logical 2-design survival validation is statistically stronger and requires no protected reference; it does execute the full logical state preparation and code service during each test. Our construction is a local-control/code-specific certification tradeoff, not a demonstrated total-resource advantage or historical novelty claim. Do not infer actual Schur complexity from a loose rank/unrank compiler upper bound.
