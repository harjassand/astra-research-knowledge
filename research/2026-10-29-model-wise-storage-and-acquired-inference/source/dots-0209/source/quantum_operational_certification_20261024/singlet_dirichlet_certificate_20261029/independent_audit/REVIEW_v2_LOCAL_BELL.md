# Independent supplementary review: local Bell transition implementation
2026-10-29. Accepted; supplements REVIEW_v1.md without changing its core theorem.

Governing files: ../LOCAL_BELL_TRANSITION_TEST_v2.md and ../check_local_bell_v2.py/.json. These are hash-bound in RECEIPT_v2.json. Author program rerun matches stored JSON byte for byte.

For the selected pair's compatible twisted swap, uniformly chosen twisted Bell basis states give subnormalized ensemble states Pi_s/D after forgetting the triplet label and retaining only sign s. This includes maximally mixed spectators. Their total traces are 3/4 for s=+ and 1/4 for s=-, not 1/2 each. Final pair Bell measurement realizes the full-array effect Pi_t. Thus joint outcome probability is Tr[Pi_t N(Pi_s)]/D. Summation weighted by st gives Tr[S N(S)]/D. Since the outcomes are binary signs, their mismatch probability is exactly (1-Tr[S N(S)]/D)/2=delta/2. This proof is independent of unitality and of any noise model.

This is a genuine operational improvement: no coherent ancilla or protected quantum reference traverses N. It requires only pair Bell preparation, frame gates, local Bell readout, maximally mixed spectators, classical sign memory, and pair routing. Same-N role independence, fresh/reset trials, calibrated preparation/readout, frozen frame and service implementation budgets remain necessary. The previous ancilla isolation/coherence assumption is NOT required by this preferred v2 implementation. All logical-twirl key restrictions remain unchanged.

The original coefficient C, statistical penalty, finite-control bias amplification, comparison with actual encoded 2-design survival, and absence of future-bath guarantees remain as in v1. V2 supersedes the v1 controlled-SWAP interface as a necessary cost, not its valid alternative derivation. No historical novelty or hardware advantage is accepted.

Independent check_local_transition.py/.json explicitly prepares each of four twisted Bell states, runs arbitrary randomly generated global nonunital CPTP channels, and measures each Bell outcome on the pair. Nine cases n=2,3,4 agree with the autocorrelation formula to numerical tolerance. Odd n here tests the physical witness only; the singlet-code theorem still requires even n>=4. All checks pass.
