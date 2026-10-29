# Resource and finite-precision qualification for the proposed compiler

This closes the parameter interfaces in the proposed proof; independent whole
review is pending. None of the formal budgets is advertised as practical.

## 1. One polynomial, not a recursion in the horizon

Use A,x,tau,d',D,gamma0,zeta,N,M,theta_geo,eta exactly as in FRESH_SPANNERS5.
Every cut uses the SAME bounds. For A>=1000 and0<tau<=1/(100A):

    d'>=x^-2, zeta>=x^-50, gamma0>=x^-4,
    N<=x^61, M<=x^1200, theta_geo>=x^-112,
    eta>=x^-1400.                                    (1)

Here D<=x^41 since ceil(x^40)<=2x^40<=x^41. Also100(r+1)<=A and
100T<=A, and tau>=x^-1. These inequalities immediately give zeta>=x^-46;
the weaker x^-50 leaves room. A N/zeta<=x^112 implies M<=x^1121<=x^1200.
Then theta_geo>=x^-112 and the second term of eta is at least x^-1376.
The first term is at least x^-51. This proves(1).

N also pays the population sample-compression event: r/gamma0<=x^5 and
log(1/d')<=2log x, so the predecessor's already generous
(r/gamma0)^10 log(1/d') is below x^60. Alternatively substitute into the explicit
union bound(r+1)N^r exp[-gamma0(N-r)]; the negative exponent dominates because
gamma0(N-r)>=x^56/2 whereas its logarithmic competitor is at most O(x^2).

M=(A N/zeta)^10 dominates the full-L1 row-sketch Hoeffding/net bound. For coefficient
boxes[-4,4]^N the envelope is<=8N² and the sup-norm Lipschitz constant<=2N².
A zeta/(100N²) net has logarithm<=N log(1+800N²/zeta). The needed sample count
is bounded by a constant times N^7 zeta^-3 plus the confidence term; the stated
power10 exceeds it because A>=1000. Uniform row proximity in the sketch fails
with probability<=N M eta/theta_geo<=d'/100.

The global teacher event fails with probability<=2 T N Delta/eta². If
Delta<=x^-4096, (1) bounds this by2x^-1235 (or a still smaller bound), below the
allocated confidence. Equivalently it is much stronger than the explicit
d'eta²/(100TN) condition. No term tau^-T enters this probability calculation.

## 2. D pays the asymmetric projection events

The full density floor is delta_L=theta_floor a^L, theta_floor=tau/[4(r+1)]
and a=tau/(2O). Let K=(r+1)C/a+2. On all cuts

    B=log(K/(theta_floor a^T))<=A log x.

A coefficient sup-net for the clipped-gradient class has dimension at most
2(r+1)+O(r+1), if all child families are included together. The larger family
only adds a polynomial factor; it does not need a child sampling measure. Its
envelope is2S C B. The Lipschitz constant contains1/delta_L, but only its LOG
appears in the net size. Since T<=A, that log is O(A log x). The Hoeffding/net
sample bound is conservatively below x^24, including confidence and constant
factors; D=ceil(x^40) exceeds it.

For negative mass, the envelope is S C and coefficient Lipschitz constant S².
The desired error v=a tau has inverse<=x^4. Its analogous sample bound is below
x^24 too. Use half the allotted errors for the exact-data concentration and leave
the remaining halves for arithmetic. Multiplying these bounds by fixed constants
still lies below x^40 at x>=1000.

For feature-positive proxies, Section3 of FRESH_SPANNERS gives expected bad
P-prefix mass<=gamma0+4D r zeta/tau<=d'tau/20. Markov therefore bounds the chance
that its actual bad mass exceeds tau by d'/20. This is conditional on the acquired
basis, with a NEW independent feature sample. Across cuts and the other events,
the failure budget is below delta. Generated-history dependence is covered by
uniform coefficient events; it is not an additional union over exponentially
many prefixes.

## 3. No spectral conditioning oracle

In geometry, the unknown true-row sketch has rank<=r and the computed sketch is
within the stated known norm perturbation. Singular values above twice that
perturbation can be retained; those below can be discarded at paid L1 error.
If a singular value lies on a proposed threshold, choose a threshold gap among
r+1 levels between2 and4 times the perturbation, at spacing polynomially small
relative to it. Approximate SVD to that precision identifies a valid gap. The
smallest retained singular value then has a KNOWN lower bound. Pivot construction
and volume-doubling take polynomially many steps in its logarithm. Relaxing the
swap/stop thresholds by fixed factors pays finite arithmetic without deciding
equality of unknown real singular values. Constants in zeta/100 leave this room.

This is ordinary robust-spanner machinery with its actual hypotheses supplied;
it is not a new exact-rank oracle or free inverse of a target singular value.

## 4. Probability precision and teacher support

Every sketch measure includes a uniform future, so its density is at least
1/((N+1)O^L) in geometry and1/((r+1)O^L) in projection. Thus cached ratios can be
evaluated to any required accuracy with an absolute probability request having
only O(L log O) additional bits. Products of next-token probabilities have
absolute error bounded by the sum of their individual errors.

All raw basis prefixes are P-sampled and have positive Q probability when Delta
is finite. If the Q interface only supports positive-probability histories,
there is still no need for a zero-prefix query: child rows with next probability
below c_cut are replaced by the known uniform conditional, retaining their next
token mass. Heavy children have a certified positive probability and may be
queried. Choose c_cut<=tau a delta_min/[1000 S C O], where
delta_min=theta_floor a^T. The resulting full restriction error is at most
2S C O c_cut; after division by p_hat>=a and clipping the log its effect is at
most O(S C O c_cut/(a delta_min))<=tau/100. This is a precision bill, not a
division of conditional teacher error at each depth.

A queried future product can stop before an unsupported extension once its
partial product is below its required absolute tolerance. Otherwise refinement
certifies a positive partial product before requesting the next conditional.
At a true zero, the former event settles at the known tolerance; at a value above
tolerance, the latter settles. Only polynomially many precision bits are needed.
No unacquired total conditional P oracle or Q sample from an impossible history
is thereby granted.

Finite conditional-sampling accuracy, if the primitive is not exact, is allocated
across the known polynomial number of feature draws by coupling/union bound. Its
requested error and ACTUAL service cost must be charged. It is not automatically
obtained from a pointwise probability response at no computational cost.

## 5. Finite cached arrays and convex inference

Take all density/marginal cache errors small enough that their propagated error
through division by the known mixture floors and clipped logs is<=tau/100 per
step. A sufficient accuracy is a fixed polynomial in tau,a,delta_min, the mixture
floor,1/D,1/N,1/M and1/(S C O T). Its BIT LENGTH is polynomial in
T log(O/a), log(1/tau),logN,logM,logD. Absolute errors may be exponentially small
in T; their bit requirement is not exponential in T.

Store normalized rational next-token rows, so their row sums are exactly1.
Their discrepancy from the underlying teacher rows is included in the preceding
restriction/log budget. Use empirical feature lower constraint2tau with arithmetic
slack: the true padded proxy is>=3tau, while every accepted coefficient state has
true feature density>=tau. Uniform coefficients give empirical value1 and known
Slater slack. Coefficient sums are imposed exactly; the virtual full density's
mass is therefore1 even when off-feature entries are signed.

The empirical generalized-KL objective's Hessian is bounded by a polynomial in
S and1/tau, and its gradient by a polynomial in S,B. Linear minimization over
the rational coefficient polytope is an ordinary polynomial-size LP. Short-step
Frank--Wolfe decreases the objective by at least a polynomial multiple of the
squared dual gap; its bounded objective range therefore permits a polynomial
iteration bound to a certified first-order gap<=tau. Log evaluations at paid
precision and a conservative gap tolerance suffice. This is a constructive
convex inference operation, not an unspecified nonlinear global-fit oracle.

The model stores only the finite feature strings/arrays, next-token rows,
parameters and inference algorithm. The full teacher row densities in the proof
are virtual mathematical witnesses, NEVER post-compilation evaluation resources.
Rational categorical token probabilities can be sampled exactly in finite expected
bit time, or with a bounded randomness budget and a separately allocated TV error.

## 6. Current status

These are detailed derivations of the access/precision/resource gates, not a claim
that an installed SVD/convex package has been validated at the formal astronomical
sample schedule. Root/peer whole challenge is still needed before accepting the
proposed full theorem. Practical compiler implementation, usefulness at moderate
Delta, and advantage against the best equally informed conventional learner remain
separate. No physical/native world-model acquisition is claimed.
