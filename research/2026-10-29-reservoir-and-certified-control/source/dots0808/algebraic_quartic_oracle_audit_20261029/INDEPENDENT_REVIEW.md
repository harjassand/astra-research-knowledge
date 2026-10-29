# Independent review: one exact algebraic quaternion optimum
2026-10-29. Scope: one acquired-bank edge, not a generic solver or hardware result.

## Decision
Accepted as an exact rational/algebraic global empirical-objective certificate for edge0 of the 29,916-probe permanent-one-axis bank. The certified rational upper minus global lower is 1.5957108509274682e-19. This is an alternative to the SOS lower relaxation on this one instance. It is not an improvement in physical recovery performance, a future-noise certificate, an all-input fast controller, or a historical novelty claim. The accepted general grid fallback remains necessary for the current all-input oracle contract.

## Globality argument independently checked
For homogeneous degree-four F, a unit-sphere stationary point satisfies gradient F=lambda q. If q0 is nonzero, homogeneity allows the real projective representative (1,x,y,z), satisfying fi−qi f0=0 for i=1,2,3. Every real global minimum is stationary by smooth compact sphere optimization. The chart equations therefore omit no real minimum except possibly the q0=0 boundary, checked separately.

I reconstructed the quartic from its previously independently checked exact bank coefficients, then computed the stationary ideal with SymPy's exact Buchberger method (author used f5b). Its grevlex basis has15 elements and40 standard quotient monomials. Independent FGLM conversion gives exactly the same three monic rational shape polynomials as the stored author basis. Leading monomials are x,y,z^40, pairwise coprime; the shape list is a Gröbner basis and represents40 complex points counting multiplicity. The univariate factor is squarefree. This checks actual ideal equivalence, not just that proposed points satisfy the equations.

An additional slower independent run reduced all three original generators to zero in the supplied shape basis and counted total real roots as4 via exact Sturm counting. With quotient dimensions both40, that inclusion also proves ideal equality. I interrupted that run before redundant per-interval Sturm counts; it is not the final complete evidence path. The replacement complete checker successfully terminates, recomputes the basis, isolates all real roots at a different rational precision, and verifies the four stored disjoint intervals have opposite endpoint signs. Complete total count4 plus four disjoint sign changes proves exactly one root per interval and no omitted real roots.

The independent boundary ideal includes fw(0,x,y,z), all three remaining Lagrange equations and x²+y²+z²−1. A fresh Buchberger computation returns[1], ruling out every normalized real boundary stationary point. It does not assert that no complex isotropic projective boundary ray exists; such rays are irrelevant to this real-sphere certificate and must be addressed separately in any future generic-family theorem.

## Objective intervals and feasible quaternion
Every real root of the univariate shape equation gives real x,y by the two rational polynomial relations. `check_value_intervals.py` independently evaluates those maps by exact rational interval Horner arithmetic, evaluates all quartic monomials on each resulting box, and divides by the strictly positive squared norm. It reproduces all four stored objective intervals exactly. Taking their smallest lower endpoint is therefore a global real-sphere lower bound. The mean-estimator scaling1/(4N) is retained; a negative empirical objective is not a negative physical fault probability.

The stored candidate quaternion is exactly rational and has squared norm1. Independent exact evaluation reproduces its stored upper value. The numerical proposal used to choose this feasible point has no authority over lower-bound completeness; any unit feasible quaternion would remain a valid upper bound. No eigenvalue ordering or exact tie decision is silently assumed.

## Software and resource boundary
These checks use SymPy exact rational Gröbner, FGLM and real-root routines, plus separately implemented Fraction interval arithmetic. They are reproducible exact-computation evidence, not an exported proof-assistant derivation or a formally verified symbolic-algebra kernel. Our complete recomputation took about85.6 seconds in this shared execution, while the author's reported timings differ; neither is a uniform latency guarantee. Large intermediate rational coefficients and degeneracy may affect future costs.

This specific script does not handle positive-dimensional stationary ideals, non-shape bases, nonradical cases, all boundary charts generically, or an arbitrary-input bit-complexity bound. No generic perturbation construction, universal completeness theorem, private source-clock schedule, or practical physical rotation accuracy is accepted by this receipt. Such a future theorem must be reviewed independently.

## Preserved evidence
- `check_ideal_and_roots.py`, `complete_check.log`, `ideal_and_roots_checks.json`: completed independent exact ideal, root and boundary check.
- `check_value_intervals.py`, `value_interval_checks.json`: all exact objective boxes and feasible upper.
- `check_ideal_and_roots_slow.py`: retained slower alternative; interrupted only after the three ideal reductions and total root count, superseded for completion by the first checker.
