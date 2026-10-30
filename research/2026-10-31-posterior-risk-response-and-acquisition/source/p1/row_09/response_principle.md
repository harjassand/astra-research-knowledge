# A response-cone principle for reusable inference

## Status and scope

This is an independent mathematical derivation, not a claim of bibliographic novelty. The all-evidence bound below is the familiar relationship between a projective density-ratio diameter and total variation, expressed as a reuse certificate. The main additional result developed here is an exact reduction from an entire finitely generated evidence cone to mixtures of at most two rays. The proofs do not rely on a decomposition oracle.

Public retrieval did not succeed: the web-search service returned empty errors, and one permitted Firecrawl search returned an insufficient-credit error. No blocked full-text source was retried. Consequently no external paper was read for this note, and priority of the two-ray observation is unverified.

The claim is about future updates inside a specified likelihood/model class. An adaptive choice of a permitted update is safe; an update outside the class is not automatically covered. All construction, data acquisition, approximation, and maintenance costs remain payable.

## 1. Compile a response, not just today's answer

Let P be the current measure on a possibly enormous hidden state X. Let Y be a finite target with q outcomes. Suppose permitted cumulative likelihoods have the form

    L_c(x) = sum_j c_j ell_j(x),    c_j >= 0,

for fixed nonnegative functions ell_1,...,ell_K. The word cumulative matters: if evidence arrives multiplicatively, its product must remain in this cone for this representation to remain valid.

Define the nonnegative response matrix

    R[y,j] = E_P[1{Y=y} ell_j(X)],
    b_j = sum_y R[y,j] > 0.

Then the posterior target distribution under any allowed update is exactly

    p(c) = R c / (b^T c).

This includes model changes to an outside factor whenever their effects on the fixed module are nonnegative combinations of the same interface functions. It does not include arbitrary changes to the fixed module itself.

The table R is a representation specification, not an algorithm: a useful implementation must construct it from the actual model and pay that cost. Below are both a concrete chain construction and lower bounds on when the representation cannot be small.

Let S be a nonnegative approximate response matrix with positive column masses d_j. Write

    nu_j = R[:,j]/b_j,
    nu_tilde_j = S[:,j]/d_j,
    r_j = d_j/b_j.

The approximate posterior is p_tilde(c) = S c/(d^T c).

## 2. Two-ray theorem: an exact restricted-update certificate

**Theorem.** For any norm on target vectors,

    sup_{c>=0,c!=0} ||p(c)-p_tilde(c)||

is attained by a c having at most two nonzero entries. The same assertion holds for any continuous jointly convex loss of the pair of posterior vectors. In particular, it holds for total variation and for absolute error in any fixed bounded scalar posterior expectation.

**Proof.** Normalize the coefficients by the true evidence masses:

    w_j = b_j c_j/(b^T c),  sum_j w_j=1,
    s = sum_j r_j w_j.

The two posteriors become

    p = sum_j w_j nu_j,
    p_tilde = sum_j w_j (r_j/s) nu_tilde_j.

For a fixed s, both are affine functions of w on the polytope

    W_s = {w>=0 : 1^T w=1, r^T w=s}.

A convex function on this compact polytope attains a maximum at a vertex. Every vertex has at most two nonzero coordinates: a point with three positive coordinates admits a nonzero perturbation supported on those coordinates that preserves both equality constraints, so it is not a vertex. Starting from a global maximizer and replacing it by such a vertex of its W_s cannot reduce the loss. This proves the claim. If all r_j are equal, one equality is redundant and one ray suffices. QED.

This is a deterministic statement. If the response-table certificate holds on a simultaneous confidence event, it also holds on that same event for arbitrarily many queries chosen adaptively from earlier answers. There is no extra union bound over the number of future queries.

### Individual-ray checks can miss the entire error

Take R=I_2 and S=diag(a,1), with a>1. The posterior is exactly right on each individual ray: both give the corresponding point mass. A mixture nevertheless changes the posterior mixing weights. The worst TV error is

    (sqrt(a)-1)/(sqrt(a)+1),

attained when the true mixture puts mass 1/(1+sqrt(a)) on the first ray. Thus a certificate checking only conditional posteriors at basis evidence values is insufficient unless it also controls their normalizations.

### Exact O(K^2) scalar certificate

For a fixed scalar target h, let mu_j=E_{nu_j}h and eta_j=E_{nu_tilde_j}h. On rays i,j, with true mixture weight t on i, the signed error is

    D_ij(t) = mu_j + t(mu_i-mu_j)
              - [r_j eta_j+t(r_i eta_i-r_j eta_j)]
                /[r_j+t(r_i-r_j)],  0<=t<=1.

Its derivative is

    D_ij'(t) = (mu_i-mu_j)
               - r_i r_j(eta_i-eta_j)
                 /[r_j+t(r_i-r_j)]^2.

If r_i=r_j, D is affine. Otherwise, in addition to endpoints, there is at most one interior stationary point, obtained from

    s_* = sqrt(r_i r_j (eta_i-eta_j)/(mu_i-mu_j)),
    t_* = (s_*-r_j)/(r_i-r_j),

when the ratio is positive and 0<t_*<1. Evaluating these candidates for every pair gives the exact uniform absolute error in O(K^2) arithmetic after the scalar responses have been constructed. Degenerate zero differences are handled by their affine or monotone limits.

For full finite-target TV, each pair is also exactly tractable: after multiplying by the positive affine denominator, each coordinate error is quadratic in t. There are at most 2q sign-change roots. On each intervening interval, the TV numerator is a fixed quadratic, so its possible stationary points are obtained from a quadratic equation. Sorting the roots and updating coefficient sums gives O(q log q) work per pair in exact real arithmetic; interval root isolation can provide numerical certificates.

### An informative special case

If every ray's conditional target distribution is exactly preserved, nu_tilde_j=nu_j, then

    sup_c TV(p(c),p_tilde(c))
      = max_{i,j} TV(nu_i,nu_j)
        tanh(|log(r_i/r_j)|/4).

On a two-ray mixture, the only error is a change in mixture weight, multiplied by the distance between the two component distributions. Optimizing that scalar weight gives the formula. The two-ray theorem makes it globally exact.

This shows why a large normalization error can be harmless when it occurs between indistinguishable target responses. A generic density-ratio certificate can be unnecessarily strict for a restricted target.

## 3. Constructive and optimal coarsening with exact masses

Suppose b_j is kept exactly and nu_j is replaced by a representative nu_bar_{g(j)}. Then all r_j=1, so

    sup_c TV(p(c),p_bar(c))
      = max_j TV(nu_j,nu_bar_{g(j)}).

The upper bound is convexity of TV under mixing; equality is attained by choosing a single ray. Thus clustering the normalized response columns is exactly the correct coarsening objective for uniform posterior accuracy, provided the evidence masses are preserved.

For a single scalar target with values mu_j, the least number of representatives achieving uniform error epsilon is obtained constructively: sort the mu_j; begin at the smallest uncovered value v; group all values through v+2 epsilon; choose the midpoint; repeat. This is the optimal interval-covering rule. Its cost is O(K log K), after the responses have been acquired and computed.

For a q-outcome target and a fixed budget of r representatives, farthest-first clustering in TV provides the usual factor-two bound on the optimal maximum radius. It costs O(Krq) using explicit columns and needs no nonnegative-factorization oracle.

The runtime claim must remain workload-specific. Keeping masses and assignments costs O(K); representatives cost O(rq). A dense new c still costs Omega(K) just to read. With s changed coefficients, compressed group masses can be maintained in O(s), followed by O(rq) work to materialize the posterior. The equally equipped uncompressed method can maintain Rc directly in O(sq). For one fixed scalar target, the exact baseline already has O(s) updates, so clustering gives no asymptotic update advantage. Compression is useful for storage, many-output responses, or large batches of coefficient changes; it is not a universal speedup.

## 4. The all-evidence certificate, with its sharp limitation

Let P and Q be equivalent probability measures, with r=dQ/dP and essential bounds 0<m<=r<=M<infinity. For an arbitrary nonnegative likelihood L with positive evidence, denote the reweighted measures P_L,Q_L. Then

    sup_L TV(P_L,Q_L)
      = (sqrt(M)-sqrt(m))/(sqrt(M)+sqrt(m))
      = tanh(osc(log r)/4).

Here the supremum is approached by concentrating L near essential ratio extrema if they are not attained.

To prove the upper bound, view r as a random variable under P_L, let s=E_{P_L}r, and write

    TV(P_L,Q_L)=E_{P_L}|r-s|/(2s).

Among distributions on [m,M] with fixed mean s, convexity of |r-s| makes the endpoint mixture extremal. Optimizing its mean gives s=sqrt(mM), and the displayed expression follows. The endpoint mixture also proves sharpness.

For a positive module response psi and its approximation psi_tilde, any future outside factor multiplies both responses identically. The same ratio remains psi_tilde/psi, so this bound certifies every allowed external change, however adaptively selected. If several fixed modules are replaced and module a has log-ratio oscillation Delta_a, their joint oscillation is at most sum_a Delta_a, giving TV at most tanh(sum_a Delta_a/4).

**Counterexample to additive approximation.** Let

    P=(1-delta, delta(1-eta), delta eta),
    Q=(1-delta, delta eta, delta(1-eta)),

with 0<eta<1/2. Their base TV is delta(1-2eta), arbitrarily small as delta goes to zero. Evidence selecting the last two states gives posterior TV 1-2eta, arbitrarily close to one. A small additive error for the original distribution does not survive arbitrary future rare evidence.

The full-posterior projective certificate can be stronger than necessary for a fixed observable or restricted evidence cone. Sections 2 and 3 state the sharper target-specific alternatives.

## 5. What multiplicative update closure really costs

Suppose Omega is finite and the allowed evidence generators are positive functions g_1,...,g_k. Permit arbitrary finite products of them, representing accumulated evidence. Let A be the unital algebra they generate.

Partition Omega by equal generator signatures:

    x~x' iff (g_1(x),...,g_k(x))=(g_1(x'),...,g_k(x')).

**Algebra theorem.** A is exactly the set of functions constant on these partition cells. Consequently its dimension is the number of distinct signatures. Exact expectations of all future evidence products require, and are determined by, the mass of each cell. For a fixed target h one additionally needs the h-weighted mass of each cell; for a finite target Y one needs the cell-by-target joint masses.

**Proof.** Every polynomial in the generators is constant on each cell. Conversely, fix one signature. For every other signature, choose a coordinate in which it differs. A product of affine functions of these chosen coordinates can be scaled to equal one at the fixed signature and zero at every other signature. Thus every cell indicator belongs to A. QED.

Few update parameters do not imply a small exact response. A single positive generator g with N distinct values gives an N-dimensional algebra. More strongly, take the fixed scalar target h=g and repeated evidence L_t=g^t. The posterior answers are

    q_t = E[g^(t+1)]/E[g^t].

Starting from E[g^0]=1, q_0,...,q_{N-2} recover the first N-1 moments. A Vandermonde system then recovers all N cell masses. Thus an exact reusable summary for one scalar target and one repeatedly applied update generator can determine the entire original distribution. This forbids a low-dimensional continuous exact summary in the ordinary finite-precision model; it does not appeal to pathological encodings of many real numbers in one real number.

### A finite-bit lower bound for approximate adaptive reuse

Let Omega={(j,b):1<=j<=d,b in {0,1}}. For s in {-1,+1}^d set

    P_s(j,0)=(1+s_j alpha)/(2d),
    P_s(j,1)=(1-s_j alpha)/(2d),  0<alpha<1.

Use the single target h(j,b)=1{b=0} and evidence ray ell_j=1{first coordinate=j}. The posterior answer is (1+s_j alpha)/2. Uniform error smaller than alpha/2 on these d rays reveals every bit of s.

Any summary of B bits that is the only retained information about P_s and succeeds simultaneously for every allowed query with probability at least 1-delta must satisfy

    B >= d + log_2(1-delta).

For a fixed random seed, B bits allow at most 2^B decoded sign vectors. Averaging over uniform s and any random seed bounds success by 2^(B-d), proving the inequality. Retaining the original input merely retains the information whose storage and access costs must then be counted.

## 6. A fully constructed mechanism: dynamic finite-state chains

Take a path model with q states and explicit nonnegative transfer matrices A_1,...,A_n. Its normalizer is

    Z = l^T A_1 ... A_n r.

A balanced binary tree stores the product for every interval represented by a node. This is an explicit construction from the input matrices, not a supplied decomposition.

Costs with ordinary dense matrix multiplication:

* Read/acquire the specified input matrices: Theta(n q^2) scalar entries.
* Build all interval products: O(n q^3) arithmetic, O(n q^2) storage.
* Replace one local matrix: read its q^2 entries and recompute O(log n) ancestors, costing O(q^3 log n).
* Replace s matrices in a batch: update their union of ancestor paths, O(q^3 s[1+log(n/s)]) work for 1<=s<=n.
* Change only endpoint evidence l,r: O(q^2), with no internal recomputation.

For q fixed, this genuinely changes repeated local-update inference from linear-in-n recomputation to logarithmic update work after a paid linear build. A target at a fixed internal position is handled by interval products on either side; a bounded number of target insertions can be queried with O(log n) product-tree operations. If only k predetermined locations can change, static intervals can be compiled once and a tree over those locations has O(log k) update depth.

For the strongest fair comparison, ordinary variable elimination, incremental message passing, or a product-form plug-in estimator equipped with these same interval products obtains exactly the same complexity. There is no estimator-level separation. The reusable mathematical resource is low interface dimension and local change, and the data structure exploits it.

A fresh scalar normalizer can be computed by forward matrix-vector multiplication in O(n q^2), which is cheaper than building the full product tree when q is large and there are few queries. The tree construction is worthwhile only when its extra construction/storage cost is amortized by the actual update workload. For broad updates, the algorithm can choose a fresh forward pass instead of claiming that a tree is always better.

If matrices are learned from samples, sampling and uncertainty certification are extra costs. Exact compilation of an empirical product measure does not by itself certify the true model. A simultaneous interval or concentration certificate on the required finite responses is needed before making a statistical guarantee.

### An exact evidence-safe coarsening witness

Consider a binary symmetric chain X_0,...,X_n in {-1,+1}, with uniform initial state and transition factors

    P(X_i=y | X_{i-1}=x)=(1+rho_i x y)/2, |rho_i|<1.

For an internal target X_m, set

    a=product_{i<=m} rho_i,
    b=product_{i>m} rho_i.

For endpoints s,t,

    E[X_m | X_0=s,X_n=t]=(a s+b t)/(1+a b s t).

Any arbitrary nonnegative future evidence/model factor on the two endpoints mixes these four conditional responses. Therefore the constant probability estimate P(X_m=+1)=1/2 has the exact uniform error

    (|a|+|b|)/(2(1+|a b|)).

This is the optimal one-representative approximation, since the four conditional means have symmetric extrema. The certificate is valid even for hard, rare, adaptively selected endpoint evidence. Its construction costs O(n) products; once the displayed bound is below tolerance, no further endpoint-specific inference is required for this target. Local transition edits can maintain a,b by the same product-tree mechanism.

This is a constructed instance of response coarsening from decay of boundary influence. An equally informed incremental method can use the same certificate, so again the claim concerns reusable structure, not a monopoly for a new named estimator.

## 7. Maintenance and statistical qualifications

1. A local factor edit invalidates precisely the cached products depending on that factor. Creating a nonlocal edge can increase interface width and invalidate the chain guarantee entirely.
2. An evidence function outside the declared cone requires a new response column, a new basis, or recomputation. Multiplicative evidence may enlarge the required algebra.
3. Simultaneous response intervals for a fixed finite dictionary protect all later adaptive choices in that dictionary. A new data-dependent dictionary does not inherit a fixed-dictionary concentration statement automatically.
4. If response probabilities R[y,j] are enclosed in simultaneous intervals, posterior coordinate intervals can be formed monotonically: use the lower numerator and upper complementary mass for the lower bound, and vice versa for the upper bound. This includes numerical and acquisition uncertainty and is uniform in c>=0.
5. Exact evidence masses are a material part of mass-preserving coarsening. If they are approximate, use the two-ray certificate or an explicit ratio bound; checking the conditional responses alone is insufficient.
6. A decision can be certified only when its margin exceeds the resulting posterior-error bound. Otherwise the representation must be refined or additional evidence acquired.

## Assessment

The strongest reusable statement here is not 'all inference becomes cheap after preprocessing.' It is: a response operator can be certified uniformly for an explicit update cone; its target-specific worst-case normalization error is a two-ray problem; and its exact and approximate compression requirements are governed by distinguishability of responses and closure of the update algebra. Concrete low-width models supply the construction, and all equally equipped algorithms may exploit it. Unrestricted future updates can require retaining essentially the whole original measure.
