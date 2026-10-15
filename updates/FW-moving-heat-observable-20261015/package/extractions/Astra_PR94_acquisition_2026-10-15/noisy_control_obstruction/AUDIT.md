# Independent audit of the noisy diagonal-control construction

## Verdict

The exact construction, common calibrated ports, dissipation estimate, polynomial resource accounting, adaptive randomized bounded-noise lower bound, and Gaussian corollary pass independent algebraic review. This is an audit of the supplied mathematical construction, not a literature-priority or fabrication claim. The generic-locus extension also passes after inspecting ../N854_SOURCE_PROOF.txt and reproducing its rational witnesses. The original large-port embedding below has been superseded by the stronger small-port embedding audited next.

## Authoritative update: small-port embedding

The revised construction uses

B_small = [[epsilon,0,0],[-beta,A,0],[-epsilon alpha,-epsilon gamma^T,epsilon]],
b=epsilon e_source, c=e_detector, and standard internal-coordinate P.

Solving gives source coordinate y0=1 and output z=alpha+gamma^T x=F_s exactly. For arbitrary real (y0,x,z), define the same stage recursion with initial value y0. Direct telescoping now gives

x^T A x-y0 beta^T x = epsilon/2 [y_m^2-y0^2+sum_i(y_i-y_{i-1})^2].

Consequently

(y0,x,z)^T B_small(y0,x,z)
 = epsilon/2 [y0^2+z^2+(y_m-z)^2+sum_i(y_i-y_{i-1})^2].

At zero stages x_i=y0+sum_{j<=i}d_j, and at one stages x_i=-d_i, where d_i=y_i-y_{i-1}. Therefore ||x||^2<=2m y0^2+2m^2||d||^2. The full vector norm squared is at most 2(m+1)^2[y0^2+z^2+||d||^2]. This proves sym(B_small)>=kappa I with kappa=epsilon/[4(m+1)^2]. Nonnegative controls preserve it.

Every baseline entry has magnitude at most epsilon, so ||B_small||<=epsilon(m+2). On [0,1]^m the full controlled norm is at most 1+epsilon(m+2)=O(1); inverse norm and condition number are O(m^4). Source norm is epsilon<=1, detector norm is 1, and actuator norm is 1. Constant output contrast therefore requires no amplified source or detector. The inverse-polynomial dissipation floor remains an explicit resource.

A common scaling lambda=1/kappa=4m^2(m+1)^2, with B'=lambda B_small and P',b',c'=sqrt(lambda) times their original values, gives dissipation at least I. Controlled norm and condition number are O(m^4), ||P'||=||c'||=2m(m+1), and ||b'||=2(m+1)/m=O(1). Again all coefficient bit lengths are O(log m). This stronger embedding replaces the large-port resource bounds below.

The independent numerical script now tests this small-port construction, both homogeneous and nonhomogeneous energy identities, and its scaled transfer. The older large-port construction remains algebraically valid and is retained below only as historical audit context.

## Original large-port embedding: independent algebra

For a bit string s, empty products equal one. Direct formulas, independent of the producer's coefficient-update implementation, are

- A_ii = epsilon;
- A_ij = -epsilon (1-2s_j) product_{j<k<i}s_k for j<i;
- beta_i = epsilon product_{k<i}s_k;
- alpha = product_k s_k;
- gamma_j = (1-2s_j) product_{k>j}s_k.

These give the exact recurrence and F_s = alpha + gamma^T(A+diag(u))^{-1}beta. With homogeneous initial value y_0=0, x_i=y_i at zero stages and x_i=y_{i-1}-y_i at one stages. Consequently

x^T A x = epsilon sum_i(y_i^2-y_i y_{i-1})
          = epsilon/2 [y_m^2 + sum_i(y_i-y_{i-1})^2].

Writing d_i=y_i-y_{i-1}, each x_i is either -d_i or a partial sum of the d_j. Thus ||x|| <= m||d||, proving sym(A)>=delta I, delta=epsilon/(2m^2).

For the producer's common-port block B, a quadratic form has cross terms -z beta^T x -w gamma^T x-alpha zw. The first pair costs at most delta||x||^2/2+(||beta||^2 z^2+||gamma||^2 w^2)/delta, and the last costs at most (z^2+w^2)/2. D=4m/delta+2 therefore proves sym(B+P diag(u)P^T)>=delta I/2.

Solving the source row gives z=1, the middle rows give x=(A+diag(u))^{-1}beta, and the output row gives D w=alpha+gamma^T x. Common b=D e_first and c=D e_last yield exactly F_s, with no external feedthrough or uncharged output offset.

## Original large-port resource accounting (superseded)

For epsilon=m^{-2}, D=8m^5+2. Uniformly on the cube: matrix norm O(m^5), inverse norm O(m^4), condition number O(m^9), ||b||=||c||=O(m^5), and ||P||=1. The common rescaling lambda=4m^4, B'=lambda B, P'=sqrt(lambda)P, b'=sqrt(lambda)b, c'=sqrt(lambda)c preserves F_s, gives symmetric part at least I, matrix norm O(m^9), inverse norm at most 1, port norms O(m^7), and actuator norm 2m^2. Since sqrt(lambda)=2m^2, all coefficients have O(log m)-bit rational/integer descriptions.

Ports are polynomially large, not free. Unit-normalizing both ports reduces contrast by the square of their common norm; retaining the lower bound requires matching inverse-polynomial noise. The construction does not prove constant contrast with all ports and actuator strengths bounded independently of m.

## Adaptive randomized bounded-noise proof

Let N=2^m. Pointwise sum_s F_s(u)=1. For each plant fix the admissible oracle returning zero if F_s(u)<=eta, otherwise F_s(u). For any fixed random seed, each query on the zero-answer path exposes at most 1/eta labels. At most Q/eta labels can ever depart from that path. The final zero-path control meets F_s(u)>=tau for at most 1/tau labels. Averaging seeds and a uniform plant label yields

success <= (Q/eta+1/tau)/N,
Q >= eta(pN-1/tau).

This is a fixed per-plant noise oracle, independent of random seeds and future queries, and covers arbitrary adaptive interior controls. Q is a worst-case query cap.

For distinct labels choose a label r that has a zero where the other has a one. At u=r the other response is zero, whereas F_r(r)>=(1+epsilon)^{-m}>=1/2. Hence pairwise sup-distance is at least 1/2. A single output predictor can fit at most one label with uniform error strictly less than 1/4. Direct counting therefore proves Q>=eta(pN-1), without a zero plant and without requiring p>1/2.

## Independent Gaussian-noise proof

For independent Gaussian noise of variance sigma^2, introduce a fictitious transcript law P0 whose observations have mean zero. The adaptive KL chain rule under P0 gives

sum_s KL(P0||Ps) = E_0 sum_{t,s} F_s(u_t)^2/(2 sigma^2)
                 <= Q/(2 sigma^2),

because sum_s F_s(u)^2<=1. Include the algorithm's random seed in the transcript. Under P0, mean success over labels is at most K/N, with K=4 for threshold 1/4 and K=1 for the prediction packing. Pinsker and Jensen give

success <= K/N + sqrt(Q/(4 sigma^2 N)).

Thus Q >= 4 sigma^2 N(max{p-K/N,0})^2. The reference P0 need not be a member of the plant family.

## Exact-oracle distinction

Choose distinct primes p_i and a single rational control u_i=epsilon/p_i. Then

F_s(u) = product_{s_i=0}p_i / product_i(p_i+1).

The exact response identifies every bit by prime divisibility. First-m-prime controls and the exact rational response have polynomial bit lengths, O(m log m) for the latter. Exponentially small absolute noise tolerance is therefore not the same claim as exponentially many precision bits. The finite-noise lower bounds do not contradict exact identifiability.

## Perturbation stability, conditional genericity

For unscaled B, if ||E_s||<=h<=delta/4, perturbed dissipation is at least delta/4. The resolvent identity gives uniformly

|F_tilde_s-F_s| <= 8D^2 h/delta^2.

For bounded noise, choose this output deviation t<eta/2. Returning zero wherever the base F_s<=eta/2 is still admissible for the perturbed plant, while at most 2/eta labels/query escape. Pairwise separation remains at least 1/2-2t. This proves a robust neighborhood statement. A genericity conclusion additionally needs a proof that the particular required good locus is dense while P,b,c remain fixed.

For Gaussian noise, setting uniform output deviation zeta<=2^{-m}=1/N gives sum_s F_tilde_s(u)^2<=2+2N zeta^2<=4. The same KL argument then gives success<=K/N+sqrt(Q/(sigma^2 N)), with K determined by the surviving control-threshold or prediction-packing property. This preserves an exponential lower bound with a constant loss. A merely inverse-polynomial perturbation does not automatically preserve this Gaussian information bound.

## Scope and numerical checks

All full controlled matrices are nonsingular on the cube by strict accretivity. The original construction can have zero w coordinates; the completed generic-perturbation audit below explicitly removes that exclusion. Reciprocity/symmetry is not proved. Plant dimension is m+2 and the hidden family has only m bits; the lower bound concerns noisy acquisition, not parameter count, computation, or average-case prediction under a fixed control distribution.

The separate audit_check.py uses closed-form coefficient products, checks the full common-port matrix and the scaled transfer, verifies the homogeneous energy identity, the partition of unity, optimum contrast, and pairwise-vertex separation. It exhausts all labels for m=1,...,8; pairwise checks run through m=6. Its deterministic results are in AUDIT_CHECK_RESULTS.txt. Maximum observed transfer error for the revised small-port construction was 1.55e-15, and all full-matrix coercivity ratios exceeded the proved lower bound. Numerical checks support but do not replace the proof.

## Completed N854 generic-locus audit

Inspected the actual source ../laplace_primary_acquisition/../N854_SOURCE_PROOF.txt, sections 2.1-2.3. The generic bad conditions are O(m^2) singleton/pair reconstruction denominators, pair-root separations, and constant-many candidate-response separation tests per selected triple, plus nonzero w coordinates. Each involves only a fixed-size collection of reduced coefficients and a constant number of rational operations. Extracted inverse entries have adjugate/determinant degrees O(m), so every cleared bad condition has degree O(m) in physical matrix entries and their product has degree O(m^3). This is an existence/bit-complexity statement, not an efficient robust genericity-certification algorithm.

The source's four triple responses were independently recomputed with exact Fraction arithmetic and match all four reported fractions. Scaling H and a by 1/t3 transports the witness from amplitude 1 to any positive t3, including 1/2. Singleton and pair reconstruction denominators have elementary diagonal witnesses for distinct positive t1,t2; pair-root separations can be made nonzero by an arbitrarily small directed off-diagonal perturbation. All finite bad sets are therefore proper.

With distinct source/detector coordinates and fixed internal P, the extracted H,w,v,f0 occupy disjoint entries of the inverse matrix, up to nonzero constants. Coordinate extraction restricted to invertible matrices is a submersion with open image. It need not be globally surjective onto every arbitrary specified block; open image is sufficient. The reduced gauge map on w_i!=0 is also a submersion. Nonzero reduced bad polynomials thus have nonzero pullbacks and cannot fill any open accretive ball.

A full-entry rational perturbation grid with K greater than the total bad-polynomial degree cannot be entirely zero. Entry spacing rho/(nK) bounds operator perturbation by rho. For the constant-margin small-port version, choosing rho<=min(1/2,zeta/(2||b'|| ||c'||)) gives uniform response deviation zeta. Since ||b'|| ||c'|| is polynomial and K is polynomial, zeta=O(2^{-m}) needs only O(m+log m) coefficient bits. The bounded-noise and Gaussian perturbation bounds above then apply. No quantitative separation from exceptional sets is asserted, and no contradiction of the source's exact generic theorem follows.
