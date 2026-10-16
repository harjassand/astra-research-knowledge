# Result: staggered parity product via causal testers

A complete proof of the previously open arbitrary-staggered product is in `PROOF.md`. A separate internal mathematical reviewer read the full artifact and found no substantive gap; their normalization clarifications are incorporated. This is not external validation or peer review.

The decisive new construction is an independent tester for each parity. The tester keeps its parity qubit private, exposes only a coherent copy to an unrestricted joint prover, and performs fixed norm-budgeted X rotations and its own prescribed pinches. Every prover action preserves each private parity between rotations, so each individual tester has acceptance probability at most its exact own-gap Q. Every admissible broad-parity Hamiltonian can be approximated at exactly unchanged own-gap action by this architecture: pad sector dimensions, remove the baseline, express each off-diagonal contraction as the average of two unitaries, and Trotterize parity-diagonal conjugates of X.

Gutoski–Watrous positive causal domination then tensors for the all-pass outcome. The proof spells out the comb normalization constraints and the positive tensor inequality, rather than inferring a product from marginal probabilities.

Consequently the ideal finite-bath broad parity model satisfies the sharp Q1 Q2 upper bound for the minimal staggered schedule, and the same argument handles arbitrary finite selected sets and fixed own-coordinate schedules. Original factorized virtual-seed interactions are a subclass. Independent sink constructions give equality over arbitrary finite baths.

No hardware, finite-width control, scalability, or physical-fault conclusion is asserted. The earlier abstract entire-function counterexamples remain valid because they lack the independent causal tester realization with the specified singleton bound.

Primary theorem: G. Gutoski and J. Watrous, *Toward a General Theory of Quantum Games* (2007), Theorem 9, https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf .
