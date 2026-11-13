# Working exact component sampler after bridge-Q reduction

## Implementation

exact_component_sampler.py now executes the actual fixed-grid circuit with:
1. exact rational category sampling;
2. edge-ID-aware multigraph bridge preprocessing;
3. exact output-equivalent bridge-Q replacement by productXX flips;
4. terminal-coherent-Q Z measurement, propagating any subsequent bridge flips;
5. chronological conditional quantum components with sparse Gaussian-integer amplitudes;
6. exact rational Born sampling using integer norm sums;
7. conservative component-entry and integer-bit caps with fixed-output fallback.

It is NOT MPS. No floating quantum arithmetic or numerical truncation is used. The optional dense test mode uses floats only as an independent reference check. Randomness is modeled as unbiased integer draws; experiments use seeded Python random streams.

## State and correlation invariant

Every active component stores an arbitrary joint amplitude dictionary over its physical sites. Components are only independent CONDITIONED on the complete already sampled classical history. Ordinary D coupling two uncertain components merges their full amplitude arrays; it never assumes cycle-block independence. Q similarly merges endpoint components. A known-basis control gives a local phase rather than a merge. Product bridge flips act locally and do not merge components.

Measurement selects the full joint component amplitudes consistent with the outcome. Surviving amplitudes remain together. Any physical bit constant across ALL retained keys is then inferred exactly and removed, with its value recorded; this includes the partner of a measured two-site parity block. Removing a fixed bit does not split the remaining correlated component. No environment or survivor correlations are erased.

## Exact arithmetic

D multiplies amplitudes by3±4i, omitting the common denominator5. Q updates them by12psi−5iXXpsi, omitting13. Overall component scale is irrelevant to normalized Born probabilities. Merge takes a tensor product of unnormalized Gaussian-integer arrays. A measurement probability is a ratio of integer squared-norm sums; integer rejection sampling draws that ratio exactly. When a component becomes completely classical, its overall scalar is discarded.

This realizes the same formal bit-complexity construction as the tiny exhaustive backend. Amplitude support can still be exponential. The cap is checked before Cartesian-product merges or Q support expansion. Integer-bit cap failures are also reported; intermediate integer products can have up to a constant-factor larger bit length before the check.

## Error and cost

Without caps, the process samples the exact final distribution, using the circuit-output bridge identity and deferred-measurement identity. With caps and fallback, full-output TV error is at most the algorithm's abort probability. There is no MPS truncation term or floating-roundoff term in the quantum evolution.

An observed zero-abort sample is NOT a theorem that abort probability is zero. Apply the frozen-algorithm holdout confidence protocol or derive a graph tail before advertising a small unconditional TV error. Category flags and all measurement outcomes must not be rejected/resampled after abort.

Runtime includes category sampling, bridge preprocessing, amplitude evolution and final output. Reported live payload bits count basis-key and Gaussian-integer bit lengths, excluding Python object overhead and some temporary allocations. They are not an RSS measurement. Cost scales polynomially in explicit circuit length and integer bit length, and exponentially in the retained component's logical support size.

## Validation and benchmark

A100-seed8-qubit20-layer test at r=.03,epsilon=.05 compared every sampled measurement probability to an independently evolved dense trajectory of the SAME bridge-reduced process. Maximum discrepancy was1.34e−15 in the floating reference. This is an implementation test, not equality of an original unreduced conditional pure trajectory.

Separately, bridge_dephasing/check.py establishes exact original-vs-reduced full-output probabilities on rational overlapping examples, and exact_gaussian_backend.py sums ALL category/reset/early outcomes of the original small channel with exact agreement. Together these checks cover distinct parts of the construction; they do not replace its general proof.

exact_component_benchmark.py/json executes unfiltered actual16x16 and32x32 depth100 records at r=.03,epsilon=.02/.05,20 independently seeded trials each, with component entry cap4096 and integer-bit cap20000. Benchmarks include failures. Comparisons to compact direct MPS must distinguish exact-arithmetic payload metrics from numerical-array storage and respect each method's actual abort/error budget.
