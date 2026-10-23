# Calculation contract, fixed before the principal replay

This is a mathematical kernel-law experiment, not sampled empirical evidence, a physical experiment, or an application speed comparison. There is no meaningful train/holdout split: the universal claims are proved and independently challenged. Numerical finite instances are supplementary implementation checks.

The principal implementation will construct arbitrary finite-state Metropolis kernels from target and proposal probabilities, then propagate probability laws by repeated squaring. It will not simulate or claim to have simulated every represented transition. Inputs are fixed at K=1, alpha=1/2 and p in {0.05, 0.01, 0.001}. No case selection on favorable outcomes is permitted.

Comparisons use total global candidate draws including the initialization draw. Pure IMH, local-then-global and global-then-local schedules have identical deterministic global-draw counts. The mixture is compared at the same expected global-draw count, with its total transition count stated separately. Local proposals and target-ratio work are additional costs.

Additional checks are: exact finite-pool SIR marginal laws by multinomial enumeration versus ordinary IMH; the proved weak-Poincare warm-start bound on a fixed four-state chain; a certified initialization budget computed from the stated KL assumption; and the analytic two-state lower sequence for the sharp asymptotic. The four-state warm test uses pi=(.01,.10,.29,.60), q=(.0001,.20,.30,.4999), initialization conditioned on the last state, R in {3,10,30,101}, and n in {1,10,100,1000}.

Acceptance: all kernels must preserve probability and satisfy the asserted invariance/reversibility to the declared arithmetic tolerance; all finite lower/upper inequalities must hold; IMH must not exceed SIR for the checked convex divergences; and selected numerical outputs must agree with the independent Decimal implementation to their reported precision. A failure is recorded and resolved before making a claim. Numerical agreement does not certify real arithmetic or replace the proofs.

Core replay uses only Python's standard library and 360 decimal digits. One 440-digit precision check will address cancellation in escape probabilities near 10^-109 and 10^-217. Plotting, if available, uses matplotlib only after the calculation. Record wall and CPU time, peak process RSS, arithmetic precision, input/source hashes, represented transitions and actual arithmetic operation counts. Full research/search/model resource totals are unknown.
