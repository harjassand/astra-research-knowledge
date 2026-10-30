# Autonomous 2D QCA: exact comparator boundary and native bridge
2026-10-30. Research derivation, not independent acceptance. Earlier accepted memory/recipient results remain unchanged.

## Useful finding

The relevant missing operation is not another protected finite Clifford frame. It is a native, finite-rate implementation of a universal asynchronous error-correcting QCA, with a local fault-path theorem under continuous joint-bath perturbations. The finite channel compiler can be made exact on clean histories. Neither its noisy schedule conversion nor the asynchronous threshold theorem is automatic.

## Primary source contract (compact summary)

Dünnweber, Styliaris and Trivedi, [arXiv:2601.20818v3](https://arxiv.org/html/2601.20818v3), prove a discrete-time 2D dissipative QCA threshold under a common-environment fault-path norm condition, including correlated/non-Markovian noise. The construction is universal, uses fixed local rules and polylogarithmic overhead, and assumes appropriately encoded initialization. Section VI supplies a preparation-depth discussion and final highest-level decoding. Section VII outlines a continuous implementation using bounded-support atomic CPTP attempted updates, buffered classical control, finite marching-soldier clocks and clock repair. Its continuous noise discussion is limited to added local unitary jumps; engineered-jump perturbations and a formal continuous threshold proof are left open. Thus this primary construction is stronger than our current finite-frame capability, but does not already prove our native continuous apparatus interface.

## Comparison with the strongest constructive alternative

With reliable externally scheduled local gates, the paper's discrete construction and conventional concatenated fault tolerance already supply universality against strong correlated-noise models. The new task cannot claim universality itself as novel. What it must earn is removal of synchronized atomic update control while retaining physical finite local dimensions, bounded rates, two-site Hamiltonians and onsite resolved resets. The gain would be a resource-model bridge, not an unconditional computational speedup, practical threshold or autonomous factory.

Encoded initialization, program preparation and final decoding remain charged premises of the source construction unless separately implemented. Our accepted native memory theorem is specialized to energy-decreasing correction maps and does not imply stability of arbitrary computation channels. The asynchronous section's proposed clock repair and recursive damage accounting must themselves be formalized before any whole universal theorem is asserted.

## New local work

1. `EXACT_NATIVE_ATTEMPT_COMPILER.md`: finite Stinespring construction, full-footprint ownership, exact rollback, coarse DATA-independent attempted-update schedule, and retained-environment scope.
2. `NOMINAL_BURST_KERNEL_AND_OPEN_SEAM.md`: deterministic bounded emission count per local operator insertion; a nominal one-root return/delay norm estimate; precise remaining inclusive fault-path and asynchronous threshold obligations.
3. `check_clean_channel_and_reset_obstruction.py`: arbitrarily small dissipator calibration need not retain nominal SUCCESS as an actual recorded subchannel. This prevents importing a Poisson record proof without a new norm argument.

No whole native universal-QCA theorem is claimed.
