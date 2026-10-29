# Complete perturbative quartic oracle with a fixed resultant template

2026-10-29 — theoretical construction, receiving review requested. The universal template below has NOT been implemented. This does not supersede the executed SOS/grid controller or claim practical speed.

## Contract
Input: rational homogeneous quartic f in four variables, rational epsilon>0. Output: exactly rational unit quaternion q and rational lower bound l satisfying l<=min_{S3} f<=f(q)<=l+epsilon. The construction uses a fixed, input-independent universal resultant polynomial and derivatives as an enormous precomputed template. It terminates almost surely, not for every infinite random-bit tape. Its expected arithmetic bit cost is polynomial in input bit length plus log(1/epsilon), with fixed potentially astronomical constants. This is a mathematical algorithm, not an executed runtime result.

## Fixed polynomial assets and degrees
Write Q=sum q_i². Let U be the universal resultant of four cubics H_i in four variables, with their80 coefficients independent. It is a fixed integer polynomial, degree27 in each block, total108. It can be constructed once by finite symbolic elimination; the actual template is not supplied in this package.

For a quartic F, substitute H_i=(partial_i F)/4−lambda Qq_i, obtaining R_F(lambda). Primary dependencies: Sodomaco arXiv:1802.10173v2, Def1.2, Thm1.3/3.8 and Prop3.11, and Cartwright–Sturmfels arXiv:1004.4953, Thm5.5. Generically R has40 distinct roots. In R=sum c_j lambda^j, c_j has quartic-coefficient degree108−j. Therefore c40 has degree68, and Disc_lambda(R) has degree6864: its coefficient total degree is78 and index-weighted degree1560.

Let B(F) be the ternary resultant at q0=0 of partial_0 F, q1 partial_2 F−q2 partial_1 F, and q1 partial_3 F−q3 partial_1 F. Its degrees3,4,4 give coefficient degree40. Its nonvanishing suffices to exclude every boundary eigenray, although its zeros may include extraneous obstructions. The exact three-chart witness check_resultant_boundary_witness.py proves B is not identically zero on quartics. Thus P(F)=c40 Disc(R) B is a nonzero polynomial of degree at most6972. The factors need not share the same witness: their product is nonzero in the integral polynomial ring.

## Why simple resultant roots determine the ray
At any common projective root q of H, the universal resultant vanishes identically on the affine coefficient subspace H_i(q)=0. Its gradient in coefficient block i must therefore equal beta_i times the cubic-monomial evaluation vector at q. A simple lambda-root gives a nonzero universal gradient by the chain rule. If two rays were common zeros, a nonzero block would be proportional to the cubic Veronese vectors of both; injectivity of the Veronese map forces the rays equal. This also rules out positive-dimensional fibers. No reducedness claim is required.

R not identically zero also excludes a common isotropic ray: Q(q)=0 would imply grad F(q)=0 and hence a common zero for every lambda. Consequently each lambda-root gives one nonisotropic eigenray. If lambda is real and B!=0, uniqueness and conjugation make its q0=1 representative real. Conversely every sphere stationary ray gives a real R root and its objective is lambda by Euler's identity. Therefore the least REAL root of R is the sphere minimum of F.

## Global coordinate extraction without a separating z projection
Differentiate U in its80 independent cubic coefficients BEFORE restricting to quartic gradients. Let A_i(lambda) be the derivative for q0³ in block i and B_ij(lambda) the derivative for q0²qj. At every root, some A_i is nonzero because q0!=0. Thus gcd(R,A_0,...,A_3)=1. Extended Euclid gives b_i with sum b_i A_i=1 modulo R. Set X_j=sum b_i B_ij modulo R. At every root, X_j(lambda)=qj/q0. These polynomials have degree<40 after reduction. This construction does not require a radical critical ideal or an assumed SDP extraction.

## Uniform finite perturbation law
Let N=16384. Independently for each of35 coefficients draw k uniformly from{0,...,N−1} with14 bits and add

    epsilon*(2k−N+1)/(140*(N−1)).

The coefficient l1 perturbation b is at mostepsilon/4, hence |F−f|<=b on S3. Polynomial zero counting, after affine translation and scaling, bounds Pr[P(F)=0]<=6972/16384<1/2 for EVERY input f. Reject exactly when P(F)=0 and try fresh bits. The expected attempt count is less than2; an infinite sequence of rejected trials is a probability-zero nonterminating tape, not a pointwise finite-execution guarantee. A declared retry cap K gives failure probability at most(6972/16384)^K; capped failure returns no oracle output. It is NOT a neutral controller event or a free readiness claim.

For a good trial, isolate the least real R root and evaluate X_j with exact rational intervals. Construct an exactly rational unit quaternion by stereographic projection, refining until F(q)−l_F<=epsilon/2. Return l=l_F−b and evaluate f(q) exactly. Then f(q)−l<=epsilon/2+2b<=epsilon. Complete checking may directly enforce the requested final gap.

## Bit-cost justification at fixed-template scope
The universal U and its derivatives have fixed finite term counts/degrees. Evaluation on rational inputs therefore takes a fixed number of polynomial-bit arithmetic operations. R has degree40 and derivative polynomials have degree at most107 in lambda; extended Euclid uses fixed-degree polynomial arithmetic, with polynomial coefficient heights. Clearing denominators produces integer polynomials of polynomial bit height. A squarefree integer polynomial of fixed degree has root separation2^{-O(height)}: use |Disc|>=1, the leading coefficient, and Cauchy bounds on all other root differences. Sturm isolation and rational refinement therefore take polynomially many bit operations in height plus required precision. Coordinate-polynomial evaluation and positive-real normalization have polynomial precision requirements. These facts give expected polynomial bit cost, not a useful numerical constant or a measured implementation.

## Boundaries
The executed code instead uses critical Groebner/FGLM shape and exact intervals; no equivalence of its favorable runtime with the template algorithm is claimed. Its fixed-z shape success is an additional condition not controlled by P unless the template coordinate extractor is implemented. The completed rational-grid oracle remains the actual all-input fallback. Current-control secrecy still requires a deterministic padded execution bound or a separate timing-isolation assumption. Neither random retries nor solver latency may be hidden in an uncharged oracle. Historical novelty is not asserted for generic polynomial optimization or resultants; the potential contribution is their precise finite contract inside the existing unknown-noise controller.

## Optional total finite completion
A capped version can always invoke the already-completed exact original-f grid fallback instead of aborting. If W_net is an explicit upper bound on its total bit operations, including rational arithmetic, choosing K>=ceil(log2 W_net) bounds expected fallback work by1 because every attempt fails with probability<1/2. The existing stereographic grid has log W_net polynomial in input/accuracy bits, so this totalization retains expected polynomial bit cost. This paragraph is a mathematical composition rule; no numeric W_net, cap implementation, or paid wall-clock bound is supplied here. Worst-case padding still pays the large grid cost.
