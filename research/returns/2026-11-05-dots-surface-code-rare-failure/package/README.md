# Finite-confidence estimation of rare surface-code failures

This package implements and audits a classical estimator for a specified surface-code noise model. It produces a finite-sample probability interval with explicit conversion and truncation bounds, without assuming that a failure-conditioned Markov chain has mixed.

## Demonstrated circuit result

The main circuit example is a rotated distance-13 Z-basis logical-memory circuit with 13 rounds, 169 data qubits and 337 used data-plus-ancilla qubits. Uniform depolarizing channels, reset flips, measurement flips and before-round data noise all have the specified rational rate 0.001.

The exact projection retains one syndrome family and the final logical observable. It preserves that complete marginal law, including its correlated local fault mechanisms, through a proved independent factorization. It does not preserve the unused syndrome family or emulate a joint correlation-aware decoder. The fixed minimum-weight decoder uses the supplied integer costs 4/5 and deterministic tie convention.

A precommitted 100,000-trial run of the score-folded sampler produced:

- **1,249 accepted canonical witnesses**.
- Estimated **13-round logical-memory failure probability: 2.64809 × 10^-8**.
- **99.9% interval: [2.40981 × 10^-8, 2.90208 × 10^-8]**.
- The interval includes the complete circuit-conversion and dyadic-rounding bound, below 8.791 × 10^-17.
- No arbitrary path-length cutoff or omitted-path tail.
- 48.69 seconds sampling, 5.10 seconds exact confidence, and 0.25 seconds loading an already certified table. Peak process memory was approximately 166.5 MiB. A fresh serial setup measured 3.20 seconds acquisition, 9.76 seconds table construction and 3.04 seconds integer certification, totaling 16.06 seconds including process startup/output. Adding the separately measured production stage gives 70.09 seconds total stage cost. This is a sum of separate shared-host measurements, not one uninterrupted benchmark or a speed record. The rebuilt graph, table and normalizer matched the frozen production exactly.

The finite score quotient and its exact terminal correction remove most of the initial tilted-proposal overhead on this instance. Every table inequality was checked with exact integers and independently rechecked with arbitrary-precision arithmetic. This does not remove the known worst-case witness-overlap obstruction.

The circuit interval targets exact rational p = 1/1000. The distinct literal binary64-parameter Stim sampling law is not assigned the tiny rational-conversion bound; floating detector-error-model comparisons are diagnostic only. The physical noise rates are specified inputs, not measured device rates. The result is model-certified, not a hardware-reliability certificate. A matched optimized circuit-level MCMC time-to-accuracy comparison has not been established.

## Repeated-measurement result

For an unrotated distance-21 code with 841 physical qubits, 21 data-error rounds, 20 noisy syndrome observations, and perfect initial/final syndrome closure:

- Every data-Z and syndrome-bit fault is independently present with probability 0.001.
- The model contains 26,061 independent fault locations and 8,820 detector checks.
- A fixed minimum-weight matching decoder and deterministic tie convention are used.
- 10,000 proposal trials produced 898 accepted canonical witnesses.
- The estimated **21-round block failure probability** is 3.9033 × 10^-23.
- The **99.9% interval** is [3.5058 × 10^-23, 4.3280 × 10^-23], under the stated random-bit and decoder assumptions.
- The omitted-long-path bound is below 3.8 × 10^-74 and is already included in the upper endpoint.
- The original full calculation took 27.02 seconds before output serialization. A separate complete-process replay reproduced the exact result in 20.46 seconds with approximately 573 MiB peak memory. These are shared-host measurements, not a controlled speed comparison.

The noise rates are specified model inputs, not measurements of a device. This is a phenomenological repeated-measurement model, not a circuit-depolarizing model. The final interval concerns the entire 21-round block, not a separately certified per-cycle rate.

An additional code-capacity example uses distance 13, 313 qubits and ideal checks. Its separately allocated 99.9% interval is [3.6126 × 10^-16, 4.0213 × 10^-16]. Each of the three fixed examples has its own 99.9% allocation. All three together have at least 99.7% coverage by a union bound; they are not a simultaneous 99.9% claim.

## What the construction does

Every failure of the specified minimum-weight decoder supplies a simple residual logical path with at least half its matching cost on faulty edges. With unit weights this is at least half the edges. The program samples from an implicitly counted nonbacktracking-path cover, conditions ordinary noise on a path-majority event, and accepts only one deterministic witness for each failing error pattern. This turns the target probability into a known normalizer times an ordinary binomial success probability.

The proposal and confidence calculations use exact integer/rational arithmetic. In the first implementation a geometric bound covers omitted long witnesses. In the circuit implementation, a finite score-residue table is a verified rational upper solution; unused probability is an explicit rejection, and an exact terminal coin removes score-folding bias. Repeated vertices are rejected immediately, so the circuit sampler needs no length cutoff. The implementation uses a seeded pseudorandom generator for reproducibility; the statistical guarantee assumes independent ideal random bits. The minimum-weight contract of the decoder library is also an explicit assumption, tested independently on exhaustive and larger finite instances.

The canonical-cover principle is established prior art, including Karp–Luby–Madras and path-reliability importance sampling. This package does not claim to invent IID rare-event sampling. The specialized construction is the tractable geometric cover and correction-derived witness for this QEC target.

## What the comparison establishes

The comparison includes published single-flip MH, locally balanced Zanella, exchange, and warm-start splitting/Bennett-ratio methods on exactly the same unrotated distance-13 code-capacity graph and decoder. This executed comparison is not a circuit-level comparison. The public mcmc4qec source was inspected and pinned. Numerical comparator runs independently implement its published mathematics; they are **not executions or runtime benchmarks of the upstream package**.

The fixed-budget comparator runs did not establish convergence or match the candidate's precision. Consequently this package does not report a measured time-to-equal-accuracy speedup, optimal splitting tuning, or superiority over every importance sampler. Its demonstrated distinction is the finite-confidence specification on the stated instance.

Existing splitting methods already report probabilities below 10^-20. A small numerical probability alone is not a new capability.

## Important limits

- Acceptance can fall exponentially on other planar graph families. An exact serial-diamond counterexample and an ordinary square-code scaling screen are included. There is no general polynomial-time or all-distance guarantee.
- The method depends on a geometric witness cover and minimum-weight decoding. It is not a general black-box estimator for arbitrary decoders or arbitrary quantum codes.
- Confidence within a stochastic model does not validate that model against physical hardware.
- The circuit result concerns the specified single-basis logical event and fixed quantized decoder. The earlier floating circuit pilots are retained as feasibility evidence and must not be mistaken for separately certified estimates or a timing-to-matched-accuracy comparison.
- A positive representation, an exact decomposition, and a numerical convergence diagnostic are not by themselves efficient estimators.

## Reproduce

Use Python 3.12 and install the pinned dependencies in `requirements.txt` in a virtual environment. No private data or external account is required.

From this package's root, reproduce the main circuit run using the supplied certified table:

```sh
python qec_score_resolvent_20261105/exact_sampler.py \
  --shots 100000 --seed 202611051864 --output reproduced_circuit.json
```

Expected categories are 1,249 accepted, 15,559 non-simple, 88 negative-score, 280 folding rejections, 49,495 non-failures, 33,329 other witnesses and zero null outcomes. The output's 99.9% interval includes conversion bias. This reuses the supplied table; it does not rebuild it.

To verify the table independently, run:

```sh
python qec_score_resolvent_audit_20261105/check_certificate.py
python qec_score_resolvent_audit_20261105/finite_exact_audit.py
python qec_score_resolvent_audit_20261105/verify_production.py
```

To rebuild the floating proposal and then its exact certificate, a C++17 compiler named `g++` is needed:

```sh
python qec_score_resolvent_20261105/screen.py --moduli 64 --save
python qec_score_resolvent_20261105/build_certificate.py
```

The floating solver is only a proposal generator. The exact integer checker determines whether a rebuilt table is valid; a different valid table can change the fixed-seed proposal stream while preserving the target law. Keep the supplied frozen table when reproducing the reported counts.

For the repeated-measurement example:

```sh
python canonical_qec_witness_20261105/check_small_exact.py
python canonical_qec_witness_20261105/phenomenological_frozen.py \
  --distance 21 --rounds 21 --p 1/1000 --length 150 \
  --shots 10000 --seed 2026110521 --confidence --out reproduced_d21.json
```

The fixed-seed counts should be 898 accepted, 41 non-simple, 4,874 non-failures and 4,187 other witnesses. The exact fractions, graph edge order, original outputs, dependency versions and source hashes are included.

For the original distance-13 run:

```sh
python canonical_qec_witness_20261105/sampler_initial_d13.py \
  --distance 13 --p 1/1000 --length 55 \
  --shots 10000 --seed 20261105 --out reproduced_d13.json
```

A low-memory variant reconstructs only the suffix tables actually requested by sampled path lengths. It reproduced the same distance-21 result with about 181 MiB peak memory, at a different measured runtime. An optional confidence helper uses floating beta quantiles only to propose endpoints, then certifies them with exact integer inequalities and falls back to exact bisection. These are implementation options, not new sampling principles.

## Where to look

- `qec_score_resolvent_20261105/THEOREM.md`: the score-folded circuit sampler and exact correction.
- `qec_score_resolvent_audit_20261105/`: independent all-row and finite-cyclic-model checks.
- `canonical_qec_witness_20261105/THEOREM_AND_SCOPE.md`: the first sampler, truncation, arithmetic and scope.
- `canonical_qec_adversarial_audit_20261105/AUDIT.md`: independent small-model, decoder, temporal-noise, normalizer and confidence checks.
- `canonical_qec_scaling_audit_20261105/REPORT.md`: exact exponential counterexample and measured acceptance scaling.
- `mcmc4qec_matched_comparison_20261105/REPORT.md`: strong comparison, provenance and unresolved limits.
- `canonical_qec_circuit_gate_20261105/`: circuit acquisition and feasibility experiments, separately labeled.
- `canonical_qec_circuit_audit_20261105/AUDIT.md`: independent audit of the circuit projection.

The release manifest lists the files and their SHA-256 hashes. Dependency and upstream licenses remain with their respective owners.
