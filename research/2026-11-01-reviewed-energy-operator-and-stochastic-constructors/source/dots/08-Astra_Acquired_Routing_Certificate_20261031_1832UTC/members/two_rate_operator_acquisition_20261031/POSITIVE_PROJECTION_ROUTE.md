# A stronger ordinary aggregation route: positivity replaces global geometry

Working derivation, not independently reviewed. This is not a claim to invent
state aggregation, conditional expectation, stratified sampling or dual-output
residual products. It is a stronger comparator and possible implementation of
the same precision-allocation ingredient. It avoids the global-gap penalty of
the first Hilbert-metric construction when an acquired positive projection is
available. No useful partition is supplied: a proposal must be learned and
every displayed certificate checked, or acquisition is inconclusive.

## 1. Uniform scalar certificate without an invariant measure

Let Z indicate a partition into r nonempty blocks and let W average uniformly
within each block. Then WZ=I, P=ZW is a stochastic projection, and

    ||P||_infinity=||Z||_infinity=||W||_infinity=1,
    q=||I-P||_infinity <=2.

Require b=Z u and ell^T=ell^T P. The latter is checked, not approximated
without payment. Suppose all true A_a are stochastic. Let K_a=W A_a Z and
let a stored stochastic r-by-r B_a satisfy ||K_a-B_a||_infinity<=d. Define

    e_in >= max_a ||(I-P) A_a P||_infinity,
    e_out >= max_a ||P A_a (I-P)||_infinity,
    alpha >= max_a ||(I-P) A_a (I-P)||_infinity.

Put t_0=0 and t_(j+1)=min(q,alpha*t_j+e_in). For every word of length l,

    |ell^T A_w b - ell^T Z B_w u|
       <= ||ell||_1 ||b||_infinity [l*d + e_out sum_(j<l) t_j].       (P1)

Here words are in column-matrix application order, so A_w=A_(a_l)...A_(a_1).
Chronological Markov action lists are reversed at this API; the all-word
guarantee covers either convention after that explicit conversion.

Proof: the full trajectory is sup-norm bounded by ||b||_infinity; its Q part
is at most q times this bound and obeys the displayed recurrence. The P-part
error is propagated by Z B W, which is stochastic on the retained space;
each step adds at most d||b||_infinity plus e_out times the Q-state bound.
Finally ell^T Q=0. This is the same two-sided mechanism, now with a positive
projection and its natural Banach norm. No common stationary distribution,
global mean-zero contraction, Gram square root or scalar stabilization is
needed. A small COMPLEMENT norm alpha is still important for useful long-word
quadratic accuracy; positivity alone does not supply it.

If alpha<1 and e_in,e_out=O(theta), the compression term is at most
||ell||_1||b||_infinity theta^2*l/(1-alpha), up to the checked constants.
Any finite batch confidence event establishing these quantities supports all
later adaptive word queries of bounded length, not state-feedback planning.

## 2. Qualitative complement certification need not have fine precision

A full coarse spectral event ||A-C||_2<=t gives ||A-C||_infinity<=sqrt(n)t.
For the acquired P, deterministically and simultaneously for all proposals,

    alpha <= max ||Q C Q||_infinity + q^2 sqrt(n)t.                   (P2)

This only needs to establish a constant alpha<1. It need not be driven down
to the accuracy required of the two cross blocks. Coarse observations used
for clustering can therefore be reused for this certificate. Paid failed
partitions and spectral batches remain in the ledger.

## 3. Fresh stratified cross-block validation

After locking the partition, take N independent transitions from EVERY named
row of EACH generator. Let C be the row empirical frequency matrix. Define

    R=A Z,       Rhat=C Z,          (n-by-r block transition probabilities)
    T=W A,       That=W C.          (r-by-n averaged original transitions)

For a distribution on k labels and N independent draws, the elementary
subset Hoeffding bound is

    Pr(||phat-p||_1 > x) <= 2^(k+1) exp(-N*x^2/2).                 (P3)

It follows from ||phat-p||_1=2 max_S |phat(S)-p(S)| and union over subsets.
The same bound holds for independent non-identically distributed draws when
p denotes their mean. Consequently, conditional on the locked partition,

    max_(a,i) ||Rhat_a(i,:)-R_a(i,:)||_1 <= tau_R,
    max_a ||That_a(g,:)-T_a(g,:)||_1 <= tau_T(g),

with failure allocation delta_R+delta_T, where sufficient rational squared
radii are

    tau_R^2 >= 2 K_R/N,
    tau_T(g)^2 >= 2 K_T/(|block_g| N),
    K_R >= ln(2^(r+1) m n/delta_R),
    K_T >= ln(2^(n+1) m r/delta_T).

Use ceiling base-two logarithms conservatively. No exponential subset loop is
executed: only its logarithmic count appears in the schedule. Every block
average uses |block_g|N independent samples with equal weights, so this is not
an assumption of identical unknown rows or exact lumpability.

Because W has disjoint positive supports,

    ||Q A P||_infinity = ||R-Z W R||_infinity,
    ||P A Q||_infinity = ||T-(T Z)W||_infinity.

Thus acquire e_in from the empirical first norm plus q*tau_R and e_out from
the second norm plus q*max_g tau_T(g). The SAME stratified row batches support
both statements by a union bound, without needing independence between them.
For balanced acquired blocks, N=O((r+log(mn/delta))/theta^2) suffices for
both radii O(theta). Total validation draws are O(m n r/theta^2), up to logs
and actual block imbalance. The full empirical n-by-n count table is still
stored/processed unless an explicitly paid streaming alternative is used.

## 4. Fine stochastic block model

For each block g and generator, take N_f fresh samples: choose a row uniformly
inside g and observe its next-state BLOCK. This is exactly a draw from row g
of K=WAZ, even without lumpability. Empirical block frequencies B are already
stochastic, so they are stable in the sup norm without a fitted H.

By (P3), simultaneous row error <=zeta follows from

    N_f >= 2 K_f/zeta^2,
    K_f >= ln(2^(r+1) m r/delta_f).

Total fine source calls are m r N_f. Their count/bit/update costs, exact source
row selection and retained lookup table are paid. Rational empirical blocks
have one common denominator N_f. Finite-grid matvec rounding adds at most
one half-grid unit per step in sup norm, because B is stochastic. With
rounded initialization and final scalar output, a simple execution bound is
||ell||_1 (L+1)2^(-p-1)+2^(-p-1).

The conditional source profile is therefore qualitative partition/complement
acquisition plus approximately

    m n r L / epsilon       cross-block validation,
    m r(r+log(...)) L^2 / epsilon^2     fine block acquisition,

when task norms, complement gap and block balance are bounded and the true
cross-block defects lie below the admission budget. This is NOT a minimax
theorem or a guarantee that clustering finds such a partition. It may be a
better ordinary method than the preceding Hilbert frontend on partitionable
tasks. Standard aggregation, goal-oriented, orthogonal-learning and retained
Monte Carlo comparators must all receive this certificate and these data.

## 5. Limits that remain substantive

Many useful task spaces are not ranges of positive projections. Then forcing
a partition can require almost n blocks; the general Hilbert route still has
a different domain. Highly imbalanced blocks inflate the validation radius.
If the complement does not contract, the capped recurrence remains valid but
can lose the quadratic long-word gain. If b or ell is not compatible with the
partition, exact inclusion may force fine partitioning; any approximate
inclusion needs a separately charged boundary term. These are checkable
structural limitations, not general impossibility claims for retained learning.

There is also an exact scope boundary. If a stochastic projection P is
H-self-adjoint for a positive diagonal H, then it is a conditional-expectation
projection onto a partition (with H-conditional weights). Indeed detailed
balance makes the positive-support graph undirected, so it decomposes into
closed irreducible components. In each component, irreducibility makes the
eigenvalue 1 simple, while idempotence restricts every eigenvalue to 0 or 1.
Thus each block has rank one and identical rows equal to the normalized H
weights. Consequently Pb=b forces b to be constant on each block. If all
entries of b differ, any such positive orthogonal projection containing b has
full rank. This elementary classification is standard Markov/projection
structure, not a claimed new theorem. It explains why the positive route
cannot simply replace all signed low-dimensional spaces. Approximate task
inclusion is possible only with separately paid first-order boundary errors.
