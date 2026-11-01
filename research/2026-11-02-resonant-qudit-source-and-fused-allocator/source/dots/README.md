# Autonomous resonant quantum sources with self-stabilizing allocation

1 November 2026. Proofs, executable finite-device comparisons, and preserved failures.

## Leading result

A specified finite-dimensional autonomous memory construction now has a resonant quantum syndrome source, physical self-stabilizing ownership control, and a formal positive noise-admission region. It does not require a trusted global clock or reliable ownership records. It admits sufficiently small continuing local coherent and dissipative errors on the modeled data and apparatus. The whole join received a separate internal mathematical review.

The key design change was selected by a stronger comparison, not by defending the first method. A noisy physical token beats dilute random starts in the actual two-probe model; the graph construction extends the mechanism with abort-on-contention locks and full owner-only cleanup. Native partial probes are never reset or paused merely because a lock was lost.

## What is actually specified

- Quantum source: resonant apparatus–data two-body Hamiltonians and explicitly stated onsite preparation, collective decay, and readout channels.
- Allocator: a qudit of dimension 8w+4D+10 per check and one physical qutrit per conflict edge; two-site classical ownership transitions.
- Remaining Boolean decoder machinery: its previously admitted at-most-three-site classical GKSL operations.
- Logical consumer: the specified Tanner-witness code family, ideal encoded input and ideal terminal decoder, with actual finite-depth frame and noise costs included.

Here w is check weight and D conflict degree. A qudit is not a qubit. Selective multilevel transitions, probe-coherence-preserving collective emission, reservoir purity, pumping and entropy disposal are required interfaces. The package does not derive an atomic implementation or grant these resources for free.

## Decisive finite-device comparison

For two overlapping ZZ/XX checks with g=gamma=1, using the SAME augmented hardware and its DONE/handoff stage:

- Physical token, flip rate .001g: retained error .000659917; per-check report rate .0668601g.
- Random starts .1g: retained error .06399953; rate .06030146g.
- Random starts .01g: retained error .00998576; rate .00938853g.

With preparation impurity .001, token error becomes .00165860. The comparison retains quantum overlap correlations and actual noisy token dynamics. It is not a full logical-memory simulation, a network throughput measurement, or a proof of superiority over every timed controller.

## Read first

1. HIGH_RATE_ALLOCATOR_MEMORY_JOIN.md: final scientific construction and complete scope.
2. audits/HIGH_RATE_ALLOCATOR_WHOLE_RECEIPT.md: separate whole-join review.
3. allocator/FUSED_GRAPH_PROTOCOL_REFRESH_THEOREM.md: all physical transitions, arbitrary-state regeneration, refresh, readiness and fixed degree-aware service rate.
4. source/EXPLICIT_TWO_BODY_QUDIT_SOURCE.md and TWO_BODY_STAGE_COMPLETION_OBSERVABILITY.md: actual source and conditional quantum completion.
5. audits/FINITE_PATCH_CORRECTOR_RECEIPT.md: conversion of earned microscopic service to a local positive generator inequality, with graph/precision costs.
6. NOISY_TOKEN_VS_RANDOM_SOURCE_RECEIPT.md and tests/token/: the decisive comparison.

RESONANT_MICROSCOPIC_SOURCE_MEMORY_JOIN.md preserves the separately received dilute-source predecessor. Its exact proof remains valid, but its accuracy–rate tradeoff is why the allocator was chosen. The root finite-patch proposal is preserved as history; later receipts determine which claims have been received.

## Checks and failures

- Full physical-data gauge reductions checked in all four Bell sectors; residuals about 1e-15.
- Actual retained-cache density and positive Poisson-observable solves, not error-per-report substitutions.
- All-state allocator SCC checks on edge, path, triangle and star graphs, up to 58,320 initial states. ACTIVE is only a structural completion edge in that check; its timing comes from the separate quantum theorem.
- Exact rational good-write cancellation cases.
- Earlier clock/verifier checks remain in foundation/.
- alternatives/raman/ retains the native Raman construction, cleanup results, matched-control benchmark, and the weight-four/weight-six conditional Stark obstruction. A surface-code rainbow ordering also cancels the dangerous fourth-order overlap term, with multi-check tests; it does not yet earn noisy Raman-network refresh.

Run scripts from their own directories using Python, NumPy and SciPy; foundation also uses SymPy. BELL_SECTOR=0,1,2,3 selects the four numerical sectors where supported. Tests are mathematical/numerical checks, not experiments. Numerical tolerances are not exact arithmetic.

## North-star judgment

This banks an essential enabling principle: physical asynchronous service and noisy ownership can be connected to a protected quantum-memory guarantee without a global time-growing simulation error. The next outcome must earn useful physical scale and geometry. The present Tanner/Boolean constants, finite-patch certification cost and non-Euclidean wiring can still be prohibitive. More detailed proofs alone do not establish a civilisation-changing capability.

No practical threshold, economical processor, fixed-qubit realization of every qudit, noisy terminal recovery, or fully two-body controller is claimed. A geometrically local protective phase and more direct physical interfaces are stronger remaining consequence gates.
