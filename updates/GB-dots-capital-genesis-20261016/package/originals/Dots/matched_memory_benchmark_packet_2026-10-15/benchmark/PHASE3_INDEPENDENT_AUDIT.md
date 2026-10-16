# Independent phase3 equal-check-read patch audit

## Review scope

Separate immutable beta-multiplier implementation, retaining the original source, executable, decoder and prior experimental outputs. This is a normalization comparison of instantaneous one-sector Pauli dynamics, not empirical validation of a new coherent-noise theorem.

Reviewed diff: equalreads.patch. Only correction-rate parameter, its validation, rate metadata and optional CLI argument change. Geometry, microscopic kernels, random streams, syndrome-only readout and scoring are byte-identical to prior version.

## Rate derivation

With N=L^4 and kappa=1, total event intensity is R=N(beta+6alpha). Noise event probability6alpha/(beta+6alpha) yields total noise intensity6Nalpha and uniform-face noise intensityalpha. Correction intensity isNbeta. For Toom uniform-face attempts have ratebeta/6; beta4 therefore gives2/3 per face. Its nominal two-check read intensity is2*4N=8N, equal to sweep beta1 with eight checks per attempt. The reported noise/face-attempt ratio6alpha/beta is correct.

This equates expected algorithmic syndrome-bit inspections, not exact realized counts, hardware effort, energy, latency or successful corrections. Common numerical seed at differing beta does NOT provide identical noise histories: changed merged proposal rate and thinning change physical noise event times and membership.

## Frozen hashes

- Original source:5f6badc5b613f78ce08a8c649f61e9b5b05bfb593f2624a4706affccab983070
- Original executable:7915b8f4fd4d2a5aa19df3352f0d7d679227bada888a67793e7292f32639b454
- Phase3 source:e2f5ee6f3a27f71cbd58c79f67cfd0c4e9d41236bf496727a7bfa36372f8f2ff
- Phase3 executable:f521b01cf16a74118ab38e6cf20e05f317cdf0ba256521c80b6166d8ead67692

Original hashes rechecked unchanged. Sweep output face_attempt_rate0 is an inapplicable sentinel because its update clocks vertices; the manifest/report must not mistake it for a face-based sweep rate.

## Validation status

Independent 704 microscopic truth-table cases PASS against new binary. Full 5,150-case deterministic external readout suite PASS. Builder beta1 regression passes both methods under default and explicit beta1, matching all22 legacy non-timing fields. Built-in exhaustive tests and unsupported-method/beta rejection checks also PASS.

## Gate approved:2026-10-15 21:02 UTC

PASS only for phase3_manifest.json: three Toom beta4 endpoints at L32,alpha.001,T5,seeds101/102/103. Aggregate cap90CPU seconds and1GiB address space. Runner and immutable binary hash checked. No additional beta4 experiments or new sweep trajectories authorized by this gate. Rate correctness and preserved decoder are established by diff review, algebra and regression; beta4 empirical result interpretation remains bounded by the tiny sample and fixed readout.

## Completed-run audit:2026-10-15 21:03 UTC

Exactly3/3 authorized endpoints completed. Raw grid, seed identities, multiplier/rate fields, 2 checks per correction attempt, and RNG-draw accounting checked independently. Resource report:7.480083CPU seconds and108,104KiB maximum RSS, below90CPU-second and1GiB bounds. Original and new source/binary hashes rechecked unchanged.

Outcome: seed101 is a logical failure under global fallback; seeds102 and103 are local-only successes. Seed101 has8,733 components of which8,732 qualify locally, illustrating the all-or-nothing readout sensitivity. These three outcomes do not establish a statistically meaningful ranking. Existing equal-read sweep outcomes are0/3 failures; Toom beta4 is1/3. Seed labels across beta are not matched physical-noise trajectories. No extra beta4 replay was run because the authorization bounded execution to3 endpoints; reproducibility evidence is the frozen implementation/manifest and the successful beta1 legacy seed regression.
