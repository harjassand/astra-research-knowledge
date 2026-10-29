# Independent review: positive-probe small-loss bridge
2026-10-29. Final receiving review: ACCEPTED at exact convex-body oracle mathematical scope. A finite resource-certified controller is NOT accepted.

## Primary proof actually inspected
Read Ito–Hirahara–Soma–Yoshida, NeurIPS2020, Algorithm1, Theorem1 and supplemental AppendixB, including truncation covariance comparison, deterministic density potential, scalar stability bound, and final expectation conversion. Their argument uses exact scalar feedback; its implementation discussion §4.4 does not itself supply this application's error budget. Sources:
https://proceedings.neurips.cc/paper/2020/file/15bb63b28926cd083b15e3b97567bbea-Paper.pdf
https://proceedings.neurips.cc/paper/2020/file/15bb63b28926cd083b15e3b97567bbea-Supplemental.pdf

## Physical probe and conditional stochastic extension
A uniformly random twisted Bell state, with its sign recorded privately, followed by the same sign measurement gives mismatch probability q=delta/2. Maximally mixed spectators produce the required full-data normalized trace. Only the average OVER private Bell labels is maximally mixed; an individual label's state is not. Changes among positive-sign triplets must not count as failure.

The loss is a PSD quadratic q(C)=vec(C)^T H vec(C), with Tr H≤3 from Haar second moments and q≤1. A zero true action implies H vec(Ctrue)=0, so q(C)≤3||C−Ctrue||F². A horizon-dependent epsilon-net therefore has a fixed comparator with total expected loss≤3T epsilon² on the actual adaptive histories.

For convex-rounding E[a|x]=x and exact second moment S=E xx^T, stochastic scalar Z with E[Z|a]=ell·a gives E[Z S^-1 x]=ell. When0≤Z≤1, Z²≤Z. The potential/stability argument is pathwise in the estimated vectors and bounded scalar; it does not need exact expected feedback at any additional step. Conditional expectation is taken only after those inequalities. Consequently its standard stability form specializes to
 X−L*≤4d eta gamma² X+d log(T)/eta+3.
With gamma=4log(10dT), eta=1/(8d gamma²), the step-size restriction holds for d≥1,T≥2, and
 X≤2L*+16d²gamma²log(T)+6.
This is an exact-oracle expected-loss theorem, not a high-probability result or a controller runtime statement. Quantum memory may affect future losses through actual outcomes; the argument requires only that the current joint channel and memory marginal precede current private action randomization.

## Geometry and radial remedy
The raw feature hull has fixed trace; density in an ambient45-dimensional volume is undefined. Relative-affine measure repairs the proof, with moment inversion on linear span and entropy exponent affine dimension. The cleaner root remedy is radial thickening: use actions alpha phi(C), alpha∈[1/2,1], whose hull is full-dimensional in the retained linear span. No zero action is added. Sample a genuine C with mean feature equal to the convex target after accounting for alpha, and feed Z=alpha Y. Then actual loss q≤2 virtual loss, while Z²≤Z. The comparator at alpha1/2 yields actual cumulative q≤6T epsilon²+32d²gamma²log(T)+12. This avoids interpreting a fractional matrix as a physical rotation.

## One-edge access, not free simultaneous feedback
Let rho=p/(n−1) be the probability that a given edge is queried on this round, independently of its privately sampled candidate. Feed that learner Z_i=1[edge queried] alpha Y, without importance amplification. Its effective loss vector is rho ell_i; the scalar remains in[0,1]. Applying the same theorem and dividing by rho gives
 E sum q_i(C_i,t)≤6T epsilon²+(32d²gamma²log(T)+12)/rho.
Summing edges therefore incurs a(n−1)^2/p term, not merely n−1. Actual current-state loss is used even on non-query rounds, with the effect bound inherited from the accepted full-memory star-transfer theorem. Probes can change source memory arbitrarily; current role, selected edge and candidate controls remain hidden at the shared source boundary. A three-role readiness statement would still need this loss bound, finite caps, control budgets and the established Markov/guard composition explicitly combined.

## Independent executed diagnostics
`independent_checks.py/.json`:30 arbitrary nonunital two-qubit channels, direct Bell-sign outcome enumeration, commutator and PSD-quadratic probability agree. Retained-bath collective channel has true-action mismatch below2e−32. Exact-expectation convex-rounding estimator checks have residual below8e−15, including independent query thinning. The small rational27-action net has linear feature rank24 and affine rank23, directly exposing the geometry issue. These are interface/algebra diagnostics, not execution of the continuous bandit algorithm.

## Unresolved finite implementation
Finite net enumeration gives an explicit optimization oracle; convex decomposition is a finite LP. It does NOT supply samples from the tilted/truncated continuous density or certified second moments. Replacing S by S_hat biases the estimator by (S_hat^-1 S−I)ell. Controlling its pairing with an extreme comparator can require its leverage in S^-1; a fixed unexamined numerical tolerance is not enough. The density can concentrate, and the supplied source's generic approximation claim does not instantiate cumulative bias, sampling variation, truncation errors or bit precision here.

Fixed feature dimension allows very expensive polytope triangulation and computable exponential integrals in principle, but no polynomial bit-complexity/conditioning proof or implemented sampler has been received. Thus the accepted exact finite square-root-loss construction remains the operational fallback. Constant physical control noise can also produce linear comparator loss; maintaining the ideal polylogarithmic comparison requires an explicit accuracy budget. No executed learning superiority, practical speedup, historical novelty or arbitrary-noise positive yield follows from this conditional bridge.

## Final v2 receipt scope
The frozen RADIAL_ORACLE_THEOREM_v2.md incorporates radial thickening, bounded scaled-Bernoulli feedback, rational-net approximation, masked edge access, and the implementation limitations above. Its universal35-dimensional claim is now justified by ten independent row/column homogeneous identities; independent symbolic rank10 certificate is `check_universal_feature_rank.py/.json`. The author's125 rational-anchor geometry script was replayed and its nonzero35-dimensional and radially augmented minors passed. Thus this is not an extrapolation from a numerical sampled rank.

Replayed300 author positive-probe/geometry cases. Independent50 radial-rounding/query-masking expectation cases pass with estimator residual4.5e−18. No tilted-density bandit learning run is claimed by these tests.

I accept the new stochastic-response extension and radial physical-query construction at the specified EXACT sampling/second-moment oracle scope. The published regret theorem is credited as established machinery; the checked extension replaces its deterministic feedback by actual bounded unbiased physical feedback. Approximate/adaptive covariance, finite sampling/quadrature, cumulative numerical errors, gate precision, end-to-end three-role integration and total-resource advantage remain separate unclosed claims. The already accepted exact finite square-root-loss learner is not superseded as the implemented fallback.
