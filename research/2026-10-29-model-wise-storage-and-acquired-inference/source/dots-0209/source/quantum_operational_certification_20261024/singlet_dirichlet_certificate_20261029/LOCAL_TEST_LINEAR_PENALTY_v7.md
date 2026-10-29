# The weighted one-edge test has an unavoidable linear statistical penalty

This is a new supplementary lower bound, not a revision of frozen v1–v6. It concerns exactly their uniformly random edge, singlet-weighted sign-transition test and logical-output fixed-state leakage completion. It is not a lower bound for all local measurements or all quantum verification protocols.

Let n≥4 be even, P the full singlet projector, d its dimension, and E any K-dimensional subcode of P, K≥2. Use ideal frame coordinates. Consider the physical unitary error Z_i on one fixed site. Since a single-site spin operator has no singlet-to-singlet matrix element, P Z_i P=0. Thus the actual decoded logical channel, with the stated fixed-state leakage replacement τ, is exactly ρ↦Tr(ρ)τ. Its entanglement fidelity is 1/K², independent of τ. The actual logical Bell loss is therefore e=1−1/K², not 1. The latter value would instead be projected/erasure Bell loss and must not be substituted silently.

For an edge not containing i, Z_i commutes with its swap, so the sign never flips. For edge (i,j), S_ij Z_i S_ij=Z_j. In P/d, rotational and permutation invariance plus total spin zero give <Z_i Z_j>=−1/(n−1). Hence its sign-flip probability is

q_ij=[1−<Z_j Z_i>]/2=n/[2(n−1)].

A uniformly random complete-graph edge contains i with probability 2/n. Consequently q=1/(n−1), and

**e/q=(n−1)(1−1/K²).**

Every uniform inequality e≤Cq for this test and decoder therefore requires C≥(n−1)(1−1/K²). The reviewed upper bound C=(d/K)(n−1)<2(n−1) has the correct linear order. For the n=4 full singlet qubit code this gives C≥9/4, while the current theorem supplies C=3 (and the deliberately conservative finite fixtures used C=6). This note does not establish the exact optimum constant for fixed-state completion.

By contrast the full-logical two-design survival test has exact coefficient (K+1)/K≤3/2, at the price of full logical state preparation and encoder/decoder controls per test. Thus tightening spectral/martingale constants alone cannot remove the one-edge witness's linear sample-cost disadvantage. A substantial improvement would need a different control/measurement interface or parallel multi-edge statistic with its own proved memory-safe instrument inequality. Known quantum authentication/error-correction methods remain independent strong competitors.

The accompanying check_local_penalty_v7.py verifies this physical error and actual decoded constant channel for n=4,6,8. It is finite-dimensional algebra, not a hardware test or an operational lower bound against other protocols.
