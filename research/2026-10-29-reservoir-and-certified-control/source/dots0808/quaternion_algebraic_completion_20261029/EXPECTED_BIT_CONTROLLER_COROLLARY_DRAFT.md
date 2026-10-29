# Conditional controller composition — author derivation, review pending

Dependencies: accepted GENERIC_TEMPLATE_THEOREM_DRAFT.md and ../quaternion_oracle_controller_20261029/FINITE_FTPL_DRAFT.md. No new quantum source promise is introduced.

Fix rational probe probability p independent of horizon T. The35 accumulated feedback coefficients are integer counts times fixed rational factors: native Pauli settings/outcomes generate constant-size rational coefficients, with probe importance factor1/p. Hence their bit lengths are O(log(T+2)). Choose FTPL amplitude R as a conservative dyadic within factor2 of720 sqrt(T/(35p)), midpoint bank size M the least power2>=140T², and oracle tolerance R/(4T²). These choices and the resulting quartic query have bit length O(log(T+2)).

Replacing each complete grid query by the accepted theoretical fixed-template perturbative oracle gives expected poly(log(T+2)) bit operations per edge per round, with fixed possibly astronomical constants. The persistent feedback state remains35 rational coefficients of O(log(T+2)) bits per edge; temporary solver workspace is a different resource. This expected complexity statement is conditional on an implemented fixed template and its exact arithmetic model; the present package does not execute it.

The prior regret proof survives the optimizer's additional fresh private randomness. Its finite-difference approximate-optimality inequalities hold pointwise for EVERY returned epsilon-optimal action, and can then be averaged over the new randomness. Thus the same per-edge actual-history fixed-comparator bound holds:

 E sum_t delta_t(C_t) <= E sum_t delta_t(C*) +720 sqrt(35T/p)+720.

This does not require a stable argmin, excitation gap, full environment reconstruction, or a uniquely identifiable frame. It is not policy regret or a comparison to the best actual encoder fidelity. The oracle is almost-surely terminating; optional grid totalization requires the separately declared bit-operation cap composition, not an uncharged timeout.

The expected bit-cost improvement is NOT automatically a physical expected-latency improvement. The current source must remain independent of the new private computation/randomness. Candidate-dependent solve time can violate this through clocks or metadata. Deterministic worst-case padding can still pay the enormous grid bound; genuine clock isolation/buffering is an additional physical interface, not established here. Exact rational rotations remain within the earlier trusted-control model, with gate synthesis and calibration errors separately charged. Ordinary informed adaptive baselines may use the same oracle.
