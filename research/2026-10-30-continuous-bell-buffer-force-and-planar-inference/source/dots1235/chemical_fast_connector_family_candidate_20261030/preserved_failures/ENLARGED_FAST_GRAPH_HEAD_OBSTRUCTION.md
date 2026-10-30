# Exact head obstruction to replacing the fast conservative graph arbitrarily

Status: personally checked counterexample, not a recurrence counterexample. New notes; frozen theorem untouched.

Consider the same connector 0 -> A+B -> 3A+4B -> 0, and the strongly connected pure-triple fast graph

    3A+4B <-> 3C+4B <-> 3D+4B <-> 3A+4B,

with any fixed positive constants. Let N=A+C+D and retain the earlier residual s=B-g_N, g_N=4 floor(N/3)+(N mod3).

At A=1,C=2,D=0 and B large, every fast source is disabled, clearing is disabled, immigration has rate 1, and activation has rate B. Since N=3, immigration changes s by zero and activation increases s by one. Consequently

    P(first nonzero residual move is up) >= B/(1+B) -> 1.

This directly falsifies the uniform O(1/s) first-up estimate for this enlarged graph. Neither large-N access to clearing nor a slowly growing cap repairs the finite head.

## The obstruction is representation-dependent, not physical instability
Here C mod3 and D mod3 are conserved. Set R=(C mod3)+(D mod3), M=N-R. Fast moves preserve M, and its completely inactive fibers have M=A in {0,1,2}. Using B-g_M instead removes the specific false up event: the counterexample has M=1, not3. This modular normalization is an earned invariant, not an assumed phase equilibrium. A full corrected first-exit proof has not been claimed here.

More importantly, this particular network is already deficiency zero: five complexes, one linkage class, four-dimensional stoichiometric span, hence delta=5-1-4=0. It is weakly reversible and thus lies in the standard complex-balanced/product-form regime. It cannot support a novelty claim. Its value is an adversarial test: the uncorrected residual mechanism fails even on a conventionally tractable positive-recurrent network.

For a general mixed cubic conservative graph, the inactive phase set and its connector-induced transitions need not be described by modular species residues. The genuine missing step is an earned finite-head phase normalization or matrix-valued return certificate. Scalar total-population residuals are not sufficient merely because every large conservative fiber reaches killing.
