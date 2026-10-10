# Native capability and mechanisms, before source comparison

2026-10-10. Exploratory independent construction. No originality claim established.

## Missing real-world operation

Given an electrical network, injection vector, branch limits, and a simultaneous-failure budget k, produce an independently checkable certificate that every set of at most k failed branches leaves all surviving flows within their limits. Return UNKNOWN rather than an unsupported safety claim when the certificate fails. The intended computational benefit is replacing combinatorially many post-failure solves by a single network factorization plus a polynomial-size certificate. This is DC/resistive linear-network safety, not full AC/transient or probabilistic safety.

## Three independently developed mechanisms

1. **Fault-budgeted return-current enclosure (selected).** Express outage compensation as a principal-submatrix resolvent of the network transfer projector. Enclose every possible failed-edge compensation simultaneously using only the largest k-1 interaction terms in each row. Refine a symmetric absolute enclosure into signed intervals, then bound each surviving edge with only its k largest potentially harmful incoming terms. The new candidate operation is a uniform certificate over an entire fault budget, with explicitly checkable row inequalities. Factorization, dense transfer acquisition, conditioning, and verification are charged below. Promising leverage: the row budget has size k-1 for a failed edge but k for a surviving edge; it accounts for a fault using one of its own budget slots and need not enumerate subsets. On a complete graph the elementary contraction test reaches the exact non-islanding threshold k <= n-2. Main risk: independent rowwise choices destroy the common-subset and reciprocity constraints, causing false UNKNOWNs.

2. **Exact nonlinear training-data removal by stored weight-response jets (stopped).** For stationarity F(w,a)=sum_i a_i grad ell_i(w)+lambda w=0, implicit differentiation gives dw/da_j=-H^-1 grad ell_j. A finite jet could transport the optimum along deletion of one or many a_j values. But the r-th jet has d times binomial(n+r-1,r) entries before structural compression, and a unit deletion need not lie inside its convergence radius. In one dimension, F(w,a)=w^2+a-c has square-root branch points at a=c; finite derivative storage cannot establish the endpoint branch without additional global information. Storing only local Hessian/gradient information cannot certify finite deletion transport: two smooth strongly convex objectives can have identical derivatives of every finite retained order at the original optimum but different optima after deletion. The proposed storage has not removed the original nonlinear solve. No implementation pursued.

3. **Cheap trajectory verification by a random generating-function identity (stopped).** For linear dynamics x_(t+1)=A x_t, define X(z)=sum_(t=0)^T x_t z^t; then (I-zA)X(z)=x_0-z^(T+1)A x_T. A verifier can check a supplied trajectory's random evaluation with one matrix action after acquiring X(z), which still costs reading the trajectory or trusting an unverified digest. For nonlinear polynomial dynamics x_(t+1)=f(x_t), sum z^t f(x_t) cannot in general be computed from X(z): multiplication becomes convolution and loses diagonal time matching. A random linear checksum of componentwise squares is not determined by a checksum of the states; choosing x=(1,-1) versus x=(0,0) already shows the kernel obstruction at z=1. Recovering the required diagonal products requires extra moment data, whose verification restores the native work or a general interactive-proof protocol. No new cheap native verifier results. No implementation pursued.

## Selected mechanism: exact algebra

Use a connected undirected graph with n vertices and m oriented edges, positive rational conductances/susceptances w_i, balanced rational injections p, and rational power-flow limits c_i. Ground one vertex. Let a_i be the reduced incidence column and b_i=sqrt(w_i) a_i. Define K=sum_i b_i b_i^T, Q=B^T K^-1 B, and g=B^T K^-1 p. Q is an orthogonal projector. Physical baseline branch flow is f_i=sqrt(w_i)g_i.

For an outage set S, K_S=K-B_S B_S^T. If I-Q_SS is positive definite, compensation x_S=(I-Q_SS)^-1 g_S gives surviving standardized flows g'_e=g_e+Q_eS x_S. There is no need to obtain any new injections or measured data for this linear calculation.

A positive weight vector v and rho<1 satisfying, for every i,

  sum of the largest k-1 values |Q_ij| v_j, j != i <= rho (1-Q_ii) v_i

certify that every I-Q_SS, |S|<=k, is nonsingular (and positive definite). Every diagonal Q_ii must be <1. The proof is a weighted infinity-norm contraction of D_S^-1(Q_SS-diag Q_SS), with D_i=1-Q_ii; since the symmetric I-Q_SS is positive semidefinite, nonsingularity implies positive definiteness.

Define a=max_i |g_i|/((1-Q_ii)v_i). Then u_i=a v_i/(1-rho) encloses |x_i| for every outage set containing i. This is a polynomial-time sufficient connectivity and compensation certificate, not a necessary criterion. It is exact for k=1 if instead one uses u_i=|g_i|/(1-Q_ii).

## Signed refinement

Start with L_i=-u_i, U_i=u_i. An enclosure is a supersolution when

  (1-Q_ii) U_i >= g_i + Top_(k-1)(max(Q_ij L_j,Q_ij U_j,0):j != i)
  (1-Q_ii) L_i <= g_i - Top_(k-1)(max(-Q_ij L_j,-Q_ij U_j,0):j != i)

and L_i<=U_i. Top_r sums r largest nonnegative values; Top_0=0. Replacing the endpoints by the right-hand sides divided by (1-Q_ii) yields narrower enclosing intervals and another supersolution in exact arithmetic. Soundness follows either by weighted contraction and interval iteration, or from the comparison solution of each fixed subset. A finite number of iterations suffices for any desired valid, though possibly loose, certificate. A noncontractive case is UNKNOWN unless a separate soundness proof is supplied.

For each surviving edge e, define

  upper_e = g_e + Top_k(max(Q_ej L_j,Q_ej U_j,0):j != e)
  lower_e = g_e - Top_k(max(-Q_ej L_j,-Q_ej U_j,0):j != e).

Every outage set of size <=k that leaves e intact obeys lower_e <= g'_e <= upper_e. Certify safety only when these limits lie in [-c_e/sqrt(w_e),c_e/sqrt(w_e)]. The optional signed iteration preserves the source signs; it is not merely a norm estimate.

## Operational costs and limitations

Native inputs: graph, all positive edge weights, injections, all limits, integer k. Native outputs: SAFE plus explicit transfer/inverse and enclosure certificate, or UNKNOWN. A failed enclosure alone is not a dangerous contingency. An exhaustive validation harness may report actual witnesses but is not part of the polynomial certification operation.

Compute K, factor K, solve m incidence right-hand sides, and form all m^2 entries of Q. Dense upper bounds are O(n^3+n^2 m+n m^2) time and O(n^2+m^2) storage. Sparse factorization can improve actual costs but is not assumed. Each interval iteration costs O(m^2) with rowwise selection. For a fixed v, certificate verification is O(m^2), in addition to checking the network solve/inverse used to derive Q. Exact rational weights can avoid square roots by using the unnormalized transfer T_ij=w_i a_i^T K^-1 a_j and physical flows; similarity scaling gives the same spectrum and corresponding row formulas. Rational arithmetic bit growth is additional, not free.

Certificates produced in floating point need outward-rounding/interval verification or exact rational reconstruction and verification. A small residual is not a safety certificate. Small 1-Q_ii, rho near 1, ill-conditioned K, tiny flow slack, and dense Q can make the method slow, numerically delicate, or uninformative. It assumes a fixed injection vector and does not model balancing actions, islands, AC voltages, protection, dynamics, or uncertainty not present in the inputs.

## Complete graph sanity check

For unit-weight K_n, Q_ii=2/n, |Q_ij|=1/n for incident distinct edges, and Q_ij=0 otherwise. With v=1 and k<=n-1, rho=(k-1)/(n-2). Thus rho<1 exactly when k<=n-2, the largest fault budget below its edge connectivity n-1. This proves a nontrivial broad family where the rowwise relaxation does not lose the connectivity threshold. It says nothing by itself about thermal-bound tightness.

## Later correction and closure

The initial 160-step weak-cut enclosure was not an intrinsic huge-flow obstruction. The interval update was initialized with a badly inflated global contraction envelope and converged slowly near rho=1. An explicit polynomial LP produces the interval supersolution directly. At epsilon=1/1000, the exact endpoints U_i=2001/500 for every edge, L_i=-2001/500 for the 12 internal edges, L_i=0 for the four links already give flow bound 4. `exact_weak_cut.py` verifies every defining inequality with fractions. More importantly, the elementary universal bound |f_e| <= sum_v max(p_v,0) is also 4, so this repair establishes no useful improvement on this family. The original 1848 number is retained in results.json and must never be presented as intrinsic conservatism of the optimum interval enclosure.

The mechanism is closed after an exact weighted-K5 example proves that its required common signed-interval supersolution need not exist even when every permitted contingency satisfies explicit nontrivial capacities with rational slack. This does NOT say no finite box contains all actual solutions; the family is finite and such a box plainly exists. It says this particular interval-invariance relaxation cannot certify one.
