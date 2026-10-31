# Independent review of the terminal-gap acquisition construction

## Verdict

Accept the stated sufficient recurrence theorem and exact raw-list construction at the present scope, after independent reconstruction of the argument and code inspection. The all-population proof does not depend on finite test states or on accepting the source preprint's broader theorem. The selector is acquired from finite graph paths and exact logarithm intervals; no exceptional-radius or stationary-distribution oracle is required.

This review is internal, not external peer review or a novelty clearance. No conclusion of general weak reversibility, exponential moments, polynomial runtime, or an acquired finite exceptional radius is accepted.

## Mathematical checks

1. The marked log-factorial identity is exact at every enabled boundary transition; designated continuation has precisely zero reward. Mismatch rewards remain in the one-step drift and are not discarded.
2. The scalar envelope sup_p(log p+C+qpH) tends to minus infinity when H does, so a path with arbitrarily small success probability does not invalidate propagation of terminal rarity. Its earlier low-probability stage supplies its own negative entropy reward.
3. In a divergent integer sequence in one communicating class, bounded coordinates can be fixed by subsequence extraction. Subtracting two sufficiently separated points therefore acquires a strictly positive vector in the stoichiometric subspace supported on exactly the divergent coordinates. This justifies the admissibility screen, including slower divergent coordinates with zero normalized logarithmic weight.
4. The cone certificate's outside-coordinate inequalities make its competitor source literally enabled after adding the terminal complex. The terminal is inside the carried linkage; this is the missing condition in the naive multiple-linkage extension. The positive weighted coordinate gain forces one strictly positive log-monomial gap and hence a rare terminal.
5. Only finitely many fixed paths are used. The contradiction argument gives a finite exceptional set without assuming its radius as input. Approximate minimization by certified rational intervals has ample error margin; the chosen drift is negative outside that set.
6. Positive recurrence of the original embedded chain does not require irreducibility of the episode-endpoint chain. The finite-set trace argument in the proof supplies the needed original-chain return estimate. Nonexplosion follows from infinitely many visits with a fixed finite exponential holding rate, and the positive lower bound on all nonzero mass-action total rates transfers finite embedded return means to physical time.
7. Finite stationary mean intensity refers to genuine population-changing jumps after null channels are discarded. No generic exponential count moment follows.
8. The common-linkage-span binary corollary's signed-invariant case is valid: if every top complex has exactly one divergent coordinate and no lower terminal exposes its bounded companion, then no lower complex contains any such companion. The signed functional is zero on every complex in that linkage and contradicts the globally supported positive stoichiometric direction when the linkage span equals the global span.

## Code and evidence checks

The exact basis enumeration solves standard-form nonnegative rational systems and verifies every proposed solution against all original rows. The separate verifier checks all boundary subsets and linkages and accepts only explicit positive-cone rows or an exact annihilating invariant; it does not invoke the finder. Its mathematical interface presupposes well-formed nonnegative integer complexes; the new top-level `compile_recurrence.py` explicitly validates that interface.

The atanh log-series remainder, rational range reduction, sign reversal for negative powers of two, and backward interval propagation were checked. All branch multipliers are nonnegative and at most one. Float conversion appears only in displayed diagnostics, never in a proof decision.

Original finder and selector runs were independently replayed into separate files and compared byte-for-byte. The separate receipt records completion. The earlier disconnected extra regression was not retried. Subsequent inspection of existing script/output bytes supports completion through the final result print (57 binary subset checks and three reordered negative controls), though the transport exit acknowledgement is unavailable; that supplemental evidence is distinct from the independently replayed main runs.

## Strong negative control

The unit-rate 0<->A,2A<->A+B example is stable and complex balanced, yet every finite current-linkage target-following episode has nonnegative increment on the stated divergent residual sequence and a strictly positive final expected reward. Thus rejection is correctly UNKNOWN, not instability. The harmonic correction is exact, including its a=0 spike; it exposes the infinite-fiber mechanism that the distinct pivot-star construction subsequently acquires.
