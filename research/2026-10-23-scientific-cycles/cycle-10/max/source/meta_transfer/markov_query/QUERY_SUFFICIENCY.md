# Exact query sufficiency: conventional Markov aggregation

This is an analytical argument for the new adapter, not a new theorem claimed for Pro3.

Let P be a finite stochastic matrix, o(x) the binary indicator of the specified native event, and B a partition on which o is constant. Suppose for every two states x,x' in the same block and every destination block D,

    sum_{y in D} P(x,y) = sum_{y in D} P(x',y).

Define the common value as Q(B(x),D). It is nonnegative and each row sums to one. For any initial distribution and any past block history with positive probability, the conditional law of the current native state is supported in the current block. Averaging its next-block probabilities therefore gives precisely the corresponding row of Q, independently of that conditional native law. The projected process is thus a Markov chain with initial block masses and kernel Q. Since o is constant on each block, this proves equality of every finite binary observation-word probability.

The first-hit time, survival through a finite horizon, first-hit time jointly with final membership, and whether a path has hit, exited and reentered are all deterministic functions of that binary observation word. Their complete laws are consequently preserved. No absorbing replacement of the actual post-hit kernel is permitted when computing final occupancy or returns.

For the executable refinement, begin with the observation partition. At each round, split each existing block by the tuple of exact transition sums into all current blocks. A stable result has the property above. Every strict round increases the number of blocks, so termination requires at most N minus the initial number of blocks strict rounds. Any observation-respecting strongly lumpable partition refines every intermediate partition, by induction: its equal transition sums into its own blocks imply equal sums into unions of those blocks. Therefore the terminal partition is the coarsest strongly lumpable refinement of the observation partition. This is not a claim of the smallest possible representation for only one start, one horizon or one restricted collection of queries.

The experiment uses the admitted original expansion_native32 kernel at its original horizon64. The original source's level quotient concerns the entire terminal level. A proper terminal subset is not a function of that quotient. Splitting only the terminal level into selected/unselected vertices still need not suffice: native parents with different numbers of selected children have different one-step subset probabilities even though they share both level and observation.

The integer implementation is exact. If P=M/d with integer M and initial law a/q, each step maps a numerator vector v to vM and multiplies its denominator by d. Backward continuation probabilities use M times the backward vector and the same denominator. Thus all first-hit/final-membership products at the fixed horizon have the common denominator q*d^H. Exact rational reduction is used for output comparisons only; no floating-point comparison determines a partition or verification result.

The explicit return calculation has four path phases: never hit; hit but never subsequently exited; exited after a hit but not yet reentered; reentered at least once. Destination observation updates these phases, while native transitions always use P. The fourth phase continues under the full P and counts reentry even if the path is outside the event again at the final horizon.

All of this is conventional exact probabilistic partition refinement and Markov aggregation. Its receiving use here checks the scope of an observation-equivalence principle on another actual scientific model. It is not evidence of a novel algorithm, autonomous representation invention, a newly feasible scientific result, or stronger general intelligence.
