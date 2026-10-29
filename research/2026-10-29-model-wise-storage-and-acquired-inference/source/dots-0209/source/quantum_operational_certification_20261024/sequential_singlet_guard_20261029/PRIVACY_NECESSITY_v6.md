# Explicit failures when current controls or retired keys leak
2026-10-29. Boundary counterexamples, not attacks on the stated private-control theorem.

## Current role leakage
If the apparatus learns TEST versus SERVICE before acting, it can implement identity on every test and complete logical depolarization on every service. Every symmetry test passes, yet the serviced quantum information is destroyed; the outer code cannot reconstruct an arbitrarily depolarized entire codeword. The hazard relation e_h≤Cq_h fails because there is no single current N_h for both roles. Digital randomness does not prevent a physical timing/pulse/routing side channel from doing this.

## Current edge leakage, even with a common formal role map
For n=4, the entire singlet space has dimension2 and every transposition S_ij restricts to a traceless logical unitary. If the currently tested edge e is revealed before the call, the apparatus can choose N_e=Ad_S_e. Its own edge autocorrelation is perfect: S_e commutes with itself, so every swap-sign test on that edge passes. However its code Bell fidelity is |Tr(E†S_eE)|²/4=0, so its logical Bell loss is1.

This can be phrased without handing over a role bit: choose a current edge on EVERY call, test or service, leak that edge, and let the source apply its corresponding swap. Then TEST always passes and SERVICE always has a nonidentity virtual Pauli label after its private logical twirl. The source's dependence on current edge defeats the uniform-random-edge expectation for one fixed N_h. It is not a valid source under the theorem.

By contrast, the weighted test input averaged over its private signed branch/preparation choices is exactly P/d0 for EVERY selected edge. Thus quantum access to the prepared carrier alone gives no information about the edge. An external preparation-control leak is qualitatively different and must be excluded by real isolated controls/padding, not by asserting that the quantum state is masked.

## Late release of a service key is not harmless to the joint-output claim
Even without a bath, let U=exp(i theta Z). Averaging a private conjugating Pauli key gives a logical Pauli channel with half-diamond error epsilon=sin²(theta). If the conjugation sign is later included as an accessible classical key record, the flagged channel retains the two coherent branches exp(±i theta Z); its half-diamond distance from the correspondingly flagged ideal channel is |sin(theta)|=sqrt(epsilon). A maximally entangled input already witnesses this value.

Therefore permanently retiring the key is needed for the stated logical-output-plus-all-accessible-memory bound, not merely until the source's last use. No key-recycling or late-public-release theorem is imported. Existing authentication protocols with proven key-recycling interfaces would require their own exact security contract.

`check_privacy_failures_v6.py/.json` verifies all six n=4 swap examples and the late-key flagged-channel distance. These are exact finite mathematical counterexamples up to floating-point arithmetic, not device measurements.
