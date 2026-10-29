# Finite rational quadrature kernel — v3 DRAFT
2026-10-29. Proposed constructive closure of the exact-sampler assumption. Independent review PENDING. This is a finite-computability claim, expressly NOT a polynomial-time, practical-latency or laboratory implementation claim. The accepted/oracle-relative v2 remains unchanged.

## Central distinction
Do not approximate a continuous law in total variation by a discrete grid. Instead choose a finite rational law Q with suitable first/second moments and leverage support, and use its EXACT rational second moment in the estimator. This restores conditional unbiasedness exactly. Only the analysis retains the continuous exponential density as a potential.

## Fixed rational geometry
Take v2's finite rational rotation net and the radial polytope K=conv{phi(C)/2,phi(C)}. Work in35 rational linearly independent feature coordinates, with the exact anchor certificate establishing full-dimensionality. All vertices are rational. Compute a rational halfspace representation by finite facet enumeration. A full-dimensional anchor simplex is explicit; its barycenter c and facet inequalities provide a positive rational r such that the Euclidean ball B(c,r) lies in K. For a simplex facet a·x<=b, use r<= (b-a·c)/sum_j|a_j|. Since every loss ell has values in[0,1] on K, ||ell||2<=1/r (a deliberately loose bound).

Let T>=2, gamma=4 ceil(log2(10dT)), eta=1/(32d gamma²), d=35. Both gamma and eta are rational/integer constants. All subsequent estimator states will be rational.

## Each round: finite, certified construction
Given rational cumulative estimator g, define the auxiliary continuous density
 p(x)=exp(-eta g·x)/integral_K exp(-eta g·u)du.
It is only a mathematical potential, not a distribution we must physically sample.

1. Compute interval enclosures for its second moment S=E_p xx^T by deterministic interval Riemann integration over a rational bounding box, classifying boxes as inside/outside/boundary relative to K. The unnormalized integrand is an exponential of a rational linear form; rational upper/lower approximations to exp are computable. Refine until a rational positive-definite matrix W is certified to satisfy .99 S<=W<=1.01 S in PSD order. One sufficient stopping rule: a rigorous operator error bound ||S-W||<=1/(101 Tr(W^-1)), with W positive definite. Since S is positive definite, this eventually succeeds.

2. Define the rational ellipsoid-clipped body
 G={x in K: x^T W^-1 x <=(3/2)d gamma²}.
It contains the standard region {x:x^T S^-1 x<=d gamma²} and is contained in {x:x^T S^-1 x<=2d gamma²}. Thus its excluded p-mass is at most d exp(1-gamma), and its conditional second moment S_G is at least (3/4)(1-d exp(1-gamma))S. The latter follows by applying the primary truncation covariance comparison to the smaller standard region, then using positivity of the extra integral. For the stated gamma and T, this is greater than .7S.

3. Construct a finite RATIONAL probability law Q supported on rational centers of boxes wholly contained in the interior of G. Assign rational positive approximations to exp(-eta g·center) times box volume, and normalize exactly. Refine the box mesh and exponential precision until both certificates hold:
   (a) M=E_Q xx^T satisfies M-(50/99)W positive semidefinite (strict positive definite certification is also allowed);
   (b) ||E_Q x-E_(p|G) x||2 <= r/(4T²), certified using componentwise interval integration bounds for the conditional mean.
All moments of Q itself are rational and are computed EXACTLY. For (b), componentwise errors <=r/(4dT²) are sufficient. Because the quadrature laws converge weakly with their first/second moments to p|G, and S_G>.7S while W<=1.01S, (a) has strict slack; (b) is achieved by refinement. No unknown environmental loss vector is used by these tests.

4. BEFORE fresh current randomization, compute alpha(x)=Tr(x)/3 and solve the finite rational vertex-decomposition LP for EVERY support point x of Q. Reweight its radial endpoint coefficients to obtain a distribution over genuine rotations with mean phi(C)=x/alpha(x). Flatten all these rational conditional laws into one joint rational law on (x,C). Precompute its cumulative integer weights and all required control descriptions, so no candidate-dependent LP or compilation follows the draw. Sample the joint pair, carry out the actual Bell-sign probe, and report Z=alpha(x)Y (or the masked alpha Y in the multiedge protocol). Update with
 ghat=Z M^-1 x.
The inverse is exact rational matrix inversion, not an approximate inverse of S. All updated quantities remain rational; random bits implement rational sampling with finite expected bit count.

## Why every construction step terminates
K is a full-dimensional rational polytope. Its boundary has Lebesgue measure zero. The extra boundary of G is a nonconstant positive-definite quadratic level surface and also has measure zero. Interior rational boxes exhaust G up to this null boundary. The exponential and all required first/second-moment integrands are continuous and bounded on the compact bounding box. Upper/lower interval Riemann sums therefore converge, and rational exponential approximations can be tightened arbitrarily. Positive normalizing integrals permit certified division.

Whole-box inclusion in K is decided by its rational facet inequalities; inclusion in the ellipsoid follows by checking the quadratic at the box vertices, since a convex quadratic attains its maximum over a box at a vertex. Outside and boundary boxes can be conservatively bounded and subdivided; positive-distance exterior boxes are eventually separated. This is enough for convergent enclosures, not a claim of fast convex integration. The PSD tests use exact rational algebra plus the certified interval errors. Positive S and the strict moment margin prove eventual finite stopping at every round. For a fixed finite T, each deterministic construction terminates on every finitely specified action/feedback history. Rational coin sampling terminates almost surely with finite expected bit count. The depth-T action/feedback tree has finite branching at each node, so the randomized controller is a finite almost-sure computation; this is not a uniform polynomial runtime bound.

No polynomial bound on this number, on coefficient bit sizes, or on practical walltime is asserted. They may be astronomical. The explicit integration procedure closes a computability/existence obligation only.

## Exact stochastic estimator and modified potential bound
Conditional on x, unbiased physical rounding and the shot imply E[Z|history,x]=ell·x, 0<=Z<=1, Z²<=Z. Consequently, using the ACTUAL Q covariance,
 E[ghat|history]=M^-1 E_Q[x x^T]ell=ell.
There is no covariance-approximation bias.

Condition(a) and W>=.99S imply M>=S/2. Every support point is in G, hence x^T S^-1 x<=2d gamma². Therefore
 ghat^T S ghat=Z² x^T M^-1 S M^-1 x
 <=2Z² x^T M^-1 x <=4Z² x^T S^-1 x <=8d gamma² Z².
The primary log-concave exponential-moment lemma, applied only to the auxiliary p, then bounds the potential stability term by16d eta gamma² Z². The step-size condition eta<=1/(sqrt(800d)gamma) holds for the chosen eta, since eta²*8d gamma²<=1/100.

To relate actual expected loss ell·E_Qx to potential loss ell·E_px, split through p|G. Their truncation difference is at most the excluded mass, because ell·x is in[0,1]. The quadrature mean error contributes at most1/(4T²) by the inradius dual bound. With the chosen gamma, total per-round discrepancy is at most1/T². Summing contributes at most1 for T>=2. The remaining potential/comparator-volume argument is unchanged, and the estimator is exactly unbiased. Using a conservative additive4,
 X-L* <=16d eta gamma² X + d logT/eta +4
        =X/2+32d²gamma²logT+4,
so X<=2L*+64d²gamma²logT+8.
For the radial physical response, actual cumulative failure is at most2X. With the epsilon grid comparator L*<=1.5T epsilon²,
 E sum_t q_t(C_t) <=6T epsilon²+128d²gamma²logT+16.
This is still O(log³T) expected source loss when epsilon<=T^-1/2, now with a specified finite rational sampling/update mechanism. The m-edge masked version follows identically with the corresponding m/p_edge factor. There is no high-probability readiness claim or integrated physical gate-error budget in this draft.

## Finite coin cap and private timing
For a deterministic cap on fresh random-bit work, write the PRECOMPUTED joint probabilities as integer weights n_j/D with a common denominator. Draw b=ceil(log2 D) bits per attempt (D=1 is deterministic), accept the integer if it is below D, and use the stored cumulative weights. Each attempt succeeds with probability D/2^b>=1/2. The number of rejected attempts is independent of the eventual joint outcome. A fixed cap R therefore introduces a neutral abort probability at most2^-R without changing the distribution of the current joint outcome conditional on success.

For at most mT controller draws choose R with mT2^-R<=delta_sample. Use a full fixed-length bit budget and padded lookup/control schedule; precomputation is completed before these fresh draws. This makes abort/timing independent of the current selected candidate. The abort occurs before a source interaction. A coupling to the uncapped process bounds the additional whole-protocol abort probability by delta_sample. Do NOT claim that conditioning globally on no abort leaves every past-history distribution unchanged; future history-dependent denominators can bias that global conditioning. The safe claim is the coupling/additive abort allowance. Hierarchical capped sampling of x and then C with x-dependent denominators would not supply this guarantee.

All arithmetic parameters are computable exactly: ceil(log2(10dT)) is obtained from integer bit length, not a floating logarithm test. This cap bounds random-bit work, not the deterministic adaptive quadrature runtime. Timing isolation/padding and trusted finite-action controls remain explicit physical requirements.

## Zero-response caching and fixed-resolution scope
With fixed horizon parameters and predictor m=0, a zero physical or masked response gives ghat=0 exactly. The cumulative estimator, auxiliary density and deterministic quadrature certificates then remain unchanged. Cache Q, M^-1 and its certificates until the next positive response. Each positive response has Z>=1/2 in the unmasked case, or on a selected learning event, so the expected number of necessary rebuilds is at most twice the expected reported cumulative loss, plus initial construction. This can avoid rebuilding on every source call. It does not bound the cost of even one rebuild or establish practical runtime.

A fixed epsilon net can replace the horizon-refined net when only a fixed error tolerance is sought. The theorem then has the nonzero average-risk floor6epsilon²; it must not be advertised as readiness approaching one at fixed resolution.

## What is and is not closed
If independently validated, this replaces exact continuous sampling and exact continuous covariance oracles by a finite albeit potentially unworkable interval-quadrature controller. It does NOT establish polynomial classical complexity, manageable memory, practical turnaround, or source-noise stability during long computation. It retains the common-algebra/private-setting promise and ideal or separately error-budgeted physical probe operations. No finite35-dimensional controller has yet been executed end-to-end in this package. The currently supplied checks cover the physical loss formula, finite rational feature geometry and (pending) small-dimensional quadrature diagnostics, not a practical large controller.
