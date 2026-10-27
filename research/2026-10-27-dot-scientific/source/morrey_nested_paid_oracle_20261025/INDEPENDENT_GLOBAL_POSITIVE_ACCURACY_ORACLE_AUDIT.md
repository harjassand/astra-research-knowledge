# Independent global positive-accuracy paid-oracle audit

**PASS under the stated computable Lipschitz input model.** The proof gives a terminating positive-accuracy lower/upper oracle in principle, without a practical rate or an exact-membership decision. A separate concrete tent majorant is actually verified below; general arbitrary-accuracy numerical outputs have not been obtained merely by proving the algorithm exists.

Reviewed `CERTIFIED_GLOBAL_POSITIVE_ACCURACY_ORACLE.md`, the audited nested-helper/WOS note, and Section 4 of `OBTAINED_NEW_HELPER_ORACLE_RESPONSE.md` with `certify_tent_global_majorant.py`. Exact receipt replay and independent coefficient/margin arithmetic pass.

## 1. Actual value function and smoothing

The proof correctly relies on the previously audited elliptope value theorem, not a formal HJB regularity assumption. The finite boundary-tree value is bounded, null-concave and separately concave in coordinate directions. Interior local Lipschitz continuity follows. Boundary mean/q rigidity makes all limiting boundary-root posteriors point masses; compactness gives the needed uniform concentration, hence continuity on the entire compact elliptope and equality V_f=f on its boundary.

For lambda<1, composing with lambda z extends the function to lambda^-1 E, which contains a neighborhood of E because zero is interior and E is convex. A sufficiently small positive convolution preserves concavity along every null direction. Uniform continuity of V_f on E gives uniform approximation on E. No differentiability of V_f up to the original boundary is assumed.

The density argument need not provide a computable modulus for V_f. Its role is existential completeness of a subsequent effective enumeration whose individual certificates are verified independently.

## 2. Strictification and rational polynomial approximation

All signs and constants check. From |U-V_f|<=epsilon/8, delta=epsilon/48, and |z|^2<=3,

`Q=U-delta|z|^2+epsilon/4`

has boundary slack at least epsilon/16, null Hessian at most -2delta on unit null vectors, and Q(0)<=V_f(0)+3epsilon/8.

A cutoff supported in the open smooth-extension neighborhood can equal one near E; extending by zero gives a smooth function on a surrounding cube. C² polynomial approximation there, followed by sufficiently small rational coefficient perturbation, gives simultaneous value error epsilon/32 and Hessian operator error delta on E. The resulting P has boundary slack epsilon/32, strict null margin delta, and

`V_f(0)<=P(0)<=V_f(0)+13epsilon/32<V_f(0)+epsilon`.

The lower inequality is actual null-tree Jensen and weak closure. No unproved global physical polynomial extension is needed for this paid-oracle upper bound on E.

## 3. Finite verification is effective and complete for strict certificates

Inside the coefficient cube, F>=0 plus the automatic 2x2 principal-minor inequalities is exactly correlation-matrix PSD. Thus the stated rational semialgebraic quantification is over precisely E and the compact unit null cone. Real-closed-field quantifier elimination decides each Hessian test in finite time. The argument does not confuse an incomplete numerical SOS search with a decision procedure.

The source phase map covers the whole compact boundary, including edge and vertex degeneracies. On a uniform torus grid, nearest phase errors are at most pi/N in each variable; its coefficient Lipschitz estimate gives image covering radius at most sqrt(6)pi/N<10/N. The proposed gradient bound from rational polynomial coefficients bounds the Euclidean gradient by first bounding its l1 norm on the cube.

Certified point evaluations and the known Lipschitz constant therefore make the finite boundary-net acceptance test valid. Every polynomial with a strict boundary margin eventually passes some net and precision. Exact cosine nodes can be evaluated as computable reals; their interval and reward-evaluation errors are included rather than silently using rounded points. A known computable modulus could replace the Lipschitz bound, but only the detailed Lipschitz version is audited here.

Enumerating polynomials, positive rational margins, net sizes, and precisions fairly avoids blocking on a candidate whose boundary gap is zero. Accepted values P(0) are genuine unrestricted upper bounds, and their running minimum converges to V_f(0).

## 4. Paid lower search and termination

The previously audited dyadic-helper families are dense in the paid boundary closure. Their finite-state transition data are rational, their Brownian macro rewards have deterministic certified intervals, and every feasible policy is complete with one absorbing macro. Exact rational LP optimization of lower reward enclosures yields a genuinely specified paid policy and a valid lower objective bound. Increasing k while shrinking macro reward errors produces lower bounds tending to V_f(0).

The finite occupation LP is bounded; no unaccounted nonabsorbing circulation can produce artificial objective value, because every ordinary action has positive quadratic activity. History-dependent approximating trees are allowed and cannot exceed the finite optimal Markov value.

Fairly dovetailing lower and upper searches eventually gives B-A<epsilon for every positive rational epsilon. Both bounds have actual receiving interpretations: the lower output is the true Brownian-completed policy, not its sphere-quadrature surrogate, and the upper output is an accepted rational polynomial, not a proposed numerical fit. This yields termination without knowing a modulus of convergence in k or a smoothing parameter for V_f.

The theorem is not an executed arbitrary-accuracy optimization run. It also gives no finite decision when epsilon=0, no certificate of source membership from the absence of a found gap, and no useful complexity claim.

## 5. Obtained concrete global tent upper bound

For R=1/5600 and n=(3/5,-1,4/5), exact expansion gives

`P=(R/4)n^T C(z)n=R/2-(3R/10)u-(2R/5)v+(6R/25)w`.

PSD makes P nonnegative on all E. At z*=(-3/5,-4/5,0), P=R. Its squared Euclidean gradient is `(769/2500)R^2<1`. Thus in the tent support P(z)>=R-|z-z*|=f(z), and outside P>=0=f. Being affine, P is globally null-concave. Every complete paid law has expected reward at most P(0)=1/11200. This is an actually obtained full-oracle upper certificate, not merely a finite-control estimate.

With delta=R/400, the rational quadratic `U=P+4delta-delta|z|^2` has boundary slack at least delta and Hessian -2delta I. Its value at zero is 51R/100=51/560000. The exact verifier passes. The affine bound is sharper, while the quadratic explicitly exemplifies the strict polynomial enumeration class.

Combined with the independently audited four-leaf AC response, these are genuine evaluated lower/upper bounds for this reward. They are not asserted tight. The actual source expectation is below 2R^3, far below the global upper bound, so no source-separating gap is present.

## 6. Remaining scientific interface

An obtained inequality E_mu f>P(0) for one verified majorant would be a true global source-separating gap. Conversely the lower oracle can provide constructive paid responses. The existence of this positive-accuracy algorithm supplies neither result for the unresolved full-source question by itself. Source convergence, exact membership, a Morrey counterexample, and a Hellinger update for an unspecified reward remain unproved.
