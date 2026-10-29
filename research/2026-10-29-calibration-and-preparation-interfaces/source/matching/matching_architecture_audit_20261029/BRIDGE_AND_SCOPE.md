# Independent matching-survival architecture derivation
2026-10-29. Governing spectral premise remains separately reviewed. No novelty or hardware superiority claim.

Let P be the d-dimensional singlet projector and rho_M=|M><M| the uniform perfect-matching product-singlet ensemble. Assume E rho_M=P/d and its Hilbert–Schmidt operator frame has eigenvalue 1/d on I_P, with all traceless eigenvalues at most lambda/d. For n>=4 the author's candidate is lambda=3/(n+2). This document proves the operational bridge, not that spectral premise.

For arbitrary CPTP source N with Kraus A_a define B_a=P A_a P, alpha_a=Tr(B_a)/d, and leakage l=sum_a||(I-P)A_a P||_HS^2/d. Let F_P=sum_a|alpha_a|^2, the raw entanglement fidelity relative to identity on P. Trace preservation gives sum_a||B_a-alpha_a P||_HS^2/d=1-l-F_P. The actual test prepares |M>, invokes N, and accepts iff every original matched pair measures singlet. This is precisely the rank-one projector rho_M, not a coarse total-spin projector. Therefore

q=1-sum_a E_M |Tr(rho_M B_a)|^2
 >= (1-lambda)(1-F_P)+lambda*l.

Leakage and nonunitality have not been discarded: leakage makes the inequality stronger. If Q is any K-dimensional subcode of P, then

K(1-F_Q)=min_{beta_a} sum_a||(A_a-beta_a I)Q||_HS^2
 <= sum_a||(A_a-alpha_a I)Q||_HS^2
 <= sum_a||(A_a-alpha_a I)P||_HS^2=d(1-F_P).

Here raw F_Q uses the physical output overlap with the same code subspace. Any TP decoder that inverts Q exactly and replaces leakage with a fixed logical state has entanglement fidelity at least F_Q: its added Kraus contributions are nonnegative squares. Consequently its logical Bell loss e satisfies

e <= [d/(K(1-lambda))] q.

Thus the candidate coefficient is C=(d/K)(n+2)/(n-1), including K=d where admissible. n=2 has d=1 and no traceless subspace; the advertised coefficient can be used conservatively but is not its sharp spectral result.

## Memory and hidden-role guard
The reviewed recovered files GOVERNING_v1.md, GENERIC_TWO_DESIGN_CONTROLLER_v7.md and CORRELATED_INPUT_MEMORY_FILTER_v3.md in sequential_singlet_guard_20261029 were inspected. Their load-bearing requirement is an all-current-channel positive test inequality. The inequality above supplies it. For every input memory density matrix sigma, fixing the same joint carrier-memory CPTP instrument induces N_sigma; hence e(sigma)<=C q(sigma). Both are linear positive functionals of sigma after the service's private logical Pauli conjugation is averaged and its key retired. Therefore E_bad_service<=C E_test_failure as memory effects. This is the required uniform operator bound, not a merely fitted average.

Fresh test probes are independent of payload/memory. The padded service input and test input need not have identical density matrices; distinguishability through the carrier itself is already included in arbitrary N_sigma. However their source map, duration and physical port must be identical conditional on past accessible records. Current role/matching/frame/pad information cannot arrive as an extra classical, timing, routing or control side channel. The existing negative-binomial guard and actual outer Pauli correction then apply with the new C. For arbitrary initially correlated payload-memory inputs the accepted ideal remains id_payload tensor B_acc, not a scalar multiple of identity on payload. It can filter/steer correlated states. Soundness is subnormalized, not a guaranteed normalized posterior error or guaranteed yield.

## Executed checks and adversarial setting disclosure
check.py/check.json execute 40 complex CPTP fixtures (n=4,6), including strong and 0.001 weak arbitrary nonunital/leaking perturbations, random subcodes and the exact leakage-sensitive inequality. They are numerical checks, not the spectral proof.

The same program gives a sharp secrecy counterexample at n=4,d=2. If matching M leaks before the call, let A_M=I-2P+2rho_M. This is unitary, fixes the prepared |M>, so every matching test passes. Its trace on P is zero, so the raw logical entanglement fidelity on the full two-dimensional singlet code is zero. Every matching therefore allows test success one and logical Bell loss one. One cannot select a different N_M for each test and apply the fixed-N witness. Leaked role is an even simpler failure: identity on tests and a bad channel on services.

## Control, geometry and comparison
All n/2 pair outcomes must pass. With independent detector failure p, even perfect collective operation has false-reject baseline 1-(1-p)^(n/2), approximately np/2. No independence is assumed in the theorem; uniform full-instrument calibration allowances are required. On a trusted all-to-all layout, preparation and Bell readout need O(n) two-qubit primitives and constant ideal parallel depth; actual routing, addressing and source-boundary padding remain charged. On a nearest-neighbour line random matching preparation alone has quadratic expected entangling-gate cost; see separately reviewed ROUTING_BOUND.md. A matched test does not solve hardware locality.

If test preparation/readout differs in total binary-failure probability by at most delta uniformly over all source memory states, use e<=C(q_actual+delta). A primitive-by-primitive complete-instrument telescoping budget can provide such delta, but an average SPAM fit does not. Service decoder/pad/buffer errors have their own complete-protocol budget. Exact random matching requires unbiased finite-integer draws; truncation or distributional TV error must be charged.

The conventional logical state-2-design test has exact coefficient (K+1)/K, asymptotically one. Matching full-code C tends to one but is larger at finite n; for a power-of-two subcode, d/K can approach two. Matching's possible gain is avoiding the full logical encoder/decoder and randomized logical-state circuit on test calls, not better universal statistical sensitivity. At n=4,K=d=2 its coefficient is 2, versus 1.5 for the six-state logical test. No overall practical advantage follows without same-connectivity calibrated circuit/resource comparison. The earlier weighted-pair test's linear coefficient lower bound is unaffected because all-pair survival is a different experiment.
