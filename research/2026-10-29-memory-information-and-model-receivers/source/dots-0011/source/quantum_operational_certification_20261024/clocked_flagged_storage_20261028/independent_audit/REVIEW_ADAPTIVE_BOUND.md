# Independent review: adaptive single-carrier concurrence comparator

28 October2026. **PASS at the explicit one-retained-carrier, unmonitored mandatory-channel scope.** This is a correct application of established concurrence theory, not a new entanglement law. The encoded performance numbers remain deterministic model calculations governed by their separate clock audit.

## Governing primary result and proof

The reviewer fetched and inspected Konrad et al., arXiv:0708.0180v3, Eq(8)–(9), https://arxiv.org/html/0708.0180v3 . The primary result gives pure-state factorization and mixed-state contraction of two-qubit concurrence under a channel acting on one side. Its normalized Bell Choi concurrence is the required multiplier.

The author correctly uses homogeneous concurrence on subnormalized history states. A local one-qubit Kraus operator multiplies pure-state concurrence by its determinant magnitude. The sum of determinant magnitudes for a trace-preserving instrument is at most one by the singular-value arithmetic-geometric mean inequality. Convex-roof optimal decomposition and convexity extend this to mixed inputs and coarse records. Applying this separately to every genuine classical history proves that arbitrary record-conditioned local instruments cannot increase the sum of branch concurrences. Compulsory channels multiply that sum by their uniform Choi-concurrence bounds.

The terminal Bell-overlap inequality follows from the pure-state Schmidt bound and an optimal concurrence decomposition; summing all outcomes gives F_e<=(1+product c_j)/2. Classical records may remain available until final decoding. This does not require a fresh learned controller or source ignorance. Postselecting histories changes the statement: the probability-weighted inequality p_s F_s<=(p_s+product c_j)/2 is correct, whereas the unconditional ceiling must not be applied to success-only fidelity.

## Actual primitive channels and clock factor

Unitary rotations before/after the native amplitude damping do not change its Bell Choi concurrence. For survival amplitude c=sqrt(1−gamma), the spin-flip eigenvalues are c²,0,0,0; the contraction is c. A dephasing segment with coherence factor q=exp(−lambda*d) has concurrence q, not q². Products over fixed background intervals therefore give exp(−lambda*tau) per round, regardless of allowed intermediate local controls. The source's best site has c=399/401, so adaptive site choices are covered by that uniform multiplier. Native source exposure and background window remain the separate modes of the declared model; native-phase background is not double counted.

The theorem permits arbitrary finite partitions of a fixed-generator dephasing exposure with interspersed ideal operations, and limits when the resulting protocol is well defined. It does not permit controls to change the stipulated noise generator, remove a compulsory exposure, obtain its environment record, or retain a noiseless quantum subsystem across that exposure.

## Independent checks and negative controls

The independent checker verifies the primitive spin-flip characteristic polynomials exactly and performs80 genuinely history-dependent four-round simulations with16 terminal classical histories each. Local weak instruments and outcome-conditioned unitaries are independently generated per history. Noise Kraus outcomes are summed, not supplied as controller records. Weighted concurrence, total Bell fidelity and declared-subset probability-weighted bounds all pass. These floating stress tests illustrate the proof; they are not its justification.

An independent monitored-dephasing counterexample recovers Bell fidelity1 by undoing the revealed Z flip. It confirms that environment monitoring would invalidate the permitted-resource class. A noiseless retained quantum bypass likewise evades the bound and is explicitly excluded. Within the permitted class, initial Z measurement, classical record storage and final repreparation attain Bell fidelity1/2; compulsory noisy qubit uses can still occur on an irrelevant re-prepared carrier.

At T32 the model's encoded F_e=.9382103189 for background integral .01 exceeds the analytic single-carrier ceiling .8093915928. At .03 the stored encoded calculation gives .7966446464 versus ceiling .6631398429; that .03 encoded result was not independently re-simulated in the separate representative clock audit, although its source is preserved. At .1 the independently replayed encoded F_e=.3683350556 is below the attainable classical1/2 strategy, not merely below an upper bound. Numerical differences here are model evaluations, not measurement confidence or outward-rounded certificates.

## Scope of the comparison

The controller may know the source exactly, use free ideal adaptive local instruments and retain arbitrary classical records. At each mandatory interval it has only one two-dimensional quantum carrier holding retained quantum information; fresh ancillas must be measured/discarded before that interval. Pre-shared entanglement, retained quantum ancillas, coherent history registers, reference access and noise-environment monitoring are not included. Those exclusions are load-bearing, not claims that every unencoded laboratory strategy satisfies them.

This is a substantive strengthening beyond a fixed-control or terminal-only decoder comparison, but remains one carrier versus redundant quantum coding, with unequal resource bills. An equally informed conventional seven-qubit implementation can use the same standard code. No generic passive-memory lifetime, threshold, new-code superiority, hardware achievement or unrestricted all-quantum-strategies optimum is established.
