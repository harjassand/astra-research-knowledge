# Independent adversarial audit of the Pfaffian-moment learner

## Verdict and scope

The conditional learning theorem is mathematically supported. No counterexample or fatal gap was found in the derivative identity, uniform perturbation estimate, signed prefix formula, clipping argument, sample bound, or polynomial bit-runtime argument. The audit supplies independent derivations below rather than relying on the proposed proof's conclusions.

The initially supplied clipping bound was valid but unnecessarily loose. The stronger bound TV(Q,P)<=||q-P||_1/2 follows directly from domination and has been incorporated in the proof. The requested capped-coin clarification is now incorporated: probabilities zero and one are handled deterministically, and a positive-mass child is selected on a cap event. Neither the exact model promise nor novelty is certified by this review.

Reviewed final PROOF.md has SHA-256 35fff3eb5be9e986e33a01d7894d65392a597f2bb98c524d99f20ae3194d345d, including the capped-coin clarification and the exact evaluator for the capped law. Later substantive changes require separate review.

## 1. Derivative identity

Fix a matching M of r disjoint pairs and let U be its endpoints. In the defining Fourier polynomial, an upper-triangular variable A_ij occurs precisely in terms whose Pfaffian perfect matching includes edge (i,j). Differentiating with respect to all edges in M therefore deletes those weights and retains only such matchings.

The crossing parity of a retained matching splits into three parts: crossings within M, crossings within the residual matching, and crossings between those two matchings. For a fixed edge (i,j) and residual edge (l,h), the latter crossing indicator, modulo two, is

    1{i<l<j} + 1{i<h<j}.

Consequently all mixed crossing signs can be assigned independently to residual endpoints. Defining s_l=(-1)^(number of fixed edges enclosing l) and y_l=s_l x_l gives

    partial_M p_C(x)
      = sigma_M 2^(-2r) product_(i in U)x_i
          p_(C_(U complement))(y).

The normalization is 2^(-k)=2^(-2r)2^(-(k-2r)); there is no missing power of two. Removal of endpoints leaves the residual order unchanged. Crossing and nested fixed edges are both covered. Repeated differentiation in one edge, or differentiation in edges sharing an endpoint, gives zero.

Since the residual distribution is an actual marginal of P, its masses are nonnegative. The spin flip is a bijection, and the removed endpoints have 2^(2r) assignments. Thus the derivative's L1 norm is exactly one, including when P has zero-probability configurations. No positivity of perturbed matrices is used.

## 2. Uniform perturbation estimate

The exact multivariate Taylor expansion is indexed by matchings, not arbitrary edge multisets: the polynomial is multilinear and overlapping-edge derivatives vanish. Each nonempty matching contributes a signed measure of L1 norm at most product_(e in M)|Delta_e|. Hence

    ||p_(C+Delta)-p_C||_1
       <= sum_(M nonempty matching) product_(e in M)|Delta_e|
       <= product_e(1+|Delta_e|)-1
       <= exp(sum_e|Delta_e|)-1.

All derivatives are evaluated at the true C. In particular this does not assume the segment C+t Delta consists of valid laws, and it does not require the physical correlation set to be convex. The conclusion holds for every nonnegative probability law satisfying the stated Pfaffian-moment promise.

When both endpoints are true laws, the stated TV<=D corollary also follows: for 0<=D<=1, exp(D)-1<2D, and for D>=1 use TV<=1.

## 3. Prefix formula and signs

For even matrix size n, expanding Pf(J+B) by the subset S of vertices matched using B yields the shuffle sign

    (-1)^(sum_(i in S)i-|S|/2).

Every even principal Pfaffian of J is one: first-row expansion gives an alternating sum with an odd number of terms. With one-based D_ii=(-1)^i a_i and B=-DAD,

    Pf(B_S)=(-1)^(|S|/2+sum_(i in S)i)
              product_(i in S)a_i Pf(A_S).

The signs cancel exactly. Multiplication by 2^(-j) therefore gives the signed prefix mass. For odd j, the appended zero row/column eliminates all A-subsets involving the dummy. It changes only the matrix size, not the desired Fourier denominator 2^j. For j=0 the value is one. Summing over discarded spins justifies using a principal submatrix for each ordered prefix, including for a signed law.

## 4. Positive-flow clipping and the improved factor

At a reached prefix a, q(a)>0. Since its children sum to q(a), their positive parts have total R_a>=q(a)>0. The conditional probability of a positive child b is q(a,b)/R_a. Along a reachable leaf,

    Q(x)=q(x) product_(prefix a along x) q(a)/R_a <= q(x).

Unreachable leaves have Q(x)=0, so Q<=q_+ pointwise and sum Q=1. This alone gives the strongest factor required here. For every genuine probability P,

    (Q-P)_+ <= (q-P)_+

pointwise: on q<0 the left side is zero, while on q>=0 use Q<=q. Since q, Q and P have total mass one,

    TV(Q,P)=sum (Q-P)_+ <= sum (q-P)_+ = ||q-P||_1/2.

The factor 1/2 cannot be improved uniformly: if q is already a probability law, clipping leaves q unchanged, and equality holds for every distinct P. The argument requires neither computing the global negative mass nor normalizing q_+.

## 5. Sampling confidence and complexity

For each pair, X_i X_j lies in [-1,1]. Hoeffding gives failure probability at most 2 exp(-N h^2/2), so the union bound over m pairs yields exactly the stated sufficient N. Using the same independent full-spin samples for all pairs does not violate this calculation; independence is needed across samples, not across pair estimates.

With h=epsilon/(8m), the good training event implies D<=epsilon/8 and L1 error at most epsilon/4. The improved clipping lemma gives TV at most epsilon/8; retaining the proof's weaker epsilon/4 allocation is harmless. This is one high-probability statement about the learned law, not an extra failure probability for each generated output.

Each empirical matrix entry has denominator N. After multiplying a prefix matrix by N, its integer entries have magnitude at most 2N. For size 2r, its Pfaffian is a sum of (2r-1)!! products of r such integers. Its bit length is therefore O(r(log N+log r)). The 2^j normalization adds only O(j) bits.

Exact Pfaffian elimination with simultaneous row/column pivoting uses cubic arithmetic work. If a pivot row in the remaining matrix is zero, that remaining Pfaffian is zero. Otherwise choose a nonzero entry and continue. Reduced intermediate Schur entries are ratios of Pfaffian minors, which have polynomial bit length by the same product bound. Thus pivots arbitrarily close to zero do not invalidate polynomial exact bit complexity. Summing separate cubic evaluations over k depths gives O(k^4) rational operations; integer arithmetic costs remain polynomial. Training increments cost an additional O(log N) bit factor, still polynomial.

For a reduced nontrivial conditional coin a/b, rejection from ceil(log2 b) bits succeeds with probability b/2^ceil(log2 b)>1/2. Capping after R=ceil(log2(4k/epsilon))+1 rounds gives total cap probability at most k 2^(-R)<=epsilon/8, below the stated epsilon/4 allocation. Couple capped and uncapped outputs using identical randomness until a cap to obtain the TV bound.

The final implementation explicitly bypasses rejection for probabilities zero and one and selects a positive-mass child on cap exceedance. This preserves all reached-prefix invariants and removes the earlier ambiguity about a fixed fallback entering a zero-mass prefix.

The exact clipped law has the stated polynomial probability evaluator. The bounded-time capped law can also be evaluated: replace each ideal transition p by (1-f)p+f times the indicator of its deterministic fallback child, where f=(1-b/2^ceil(log2 b))^R. These are polynomial-bit rationals. Multiplying k transitions remains polynomial.

## 6. Detector-noise extension

Under independent detector signs with known means t_i, independence gives every observed moment as product_(i in S)t_i times the corresponding latent moment. The Pfaffian diagonal-congruence identity gives precisely the same factor, so the promise is preserved. Estimating observed pair moments to tau^2 h accuracy when |t_i|>=tau produces deconvolved pair error at most h. Hoeffding then adds the asserted tau^(-4) sample factor. Arbitrary nonphysical deconvolved estimates are allowed by the signed reconstruction.

Exact rational means and their encoding lengths must be part of the input, as stated. Unknown calibration, zero means, correlated errors, and temporally dependent samples are not covered. No such missing capability follows from the algebraic identity.

## 7. Source comparison and validity boundary

Primary sources independently checked support the stated comparison boundaries:

- Galashin and Pylyavskyy, https://arxiv.org/abs/1807.03282 , characterize boundary correlation matrices and recover parameters of reduced planar Ising networks. Exact inverse recovery is an established comparator, not an exponential baseline.
- Johnson et al., https://jmlr.csail.mit.edu/papers/v17/15-579.html , learn a planar Ising approximation on observed variables from pair correlations. A latent boundary marginal is not automatically a pairwise Ising model on those same variables.
- Daskalakis et al., https://proceedings.mlr.press/v336/daskalakis26a.html , give TV-estimation results for stated classes of observed Ising models. Their assumptions cannot silently be inherited by arbitrary hidden-bulk marginals.
- Edelman et al., https://arxiv.org/abs/2605.01202 , give exact Pfaffian point-process sampling from supplied kernels. This does not by itself establish the empirical-spin-moment learning and signed-repair theorem here.
- Nietner, https://arxiv.org/abs/2306.04731 , proves hardness for broader free-fermion measurement distributions. The classical spin-moment promise is different; the present proof does not overturn that hardness.
- DPP method-of-moments learning and TV learning also have established prior: https://proceedings.mlr.press/v70/urschel17a.html and https://proceedings.neurips.cc/paper/2020/file/964d1775b722eff11b8ecd9e9ed5bd9e-Paper.pdf . They are relevant priority comparators, but determinant inclusion moments are not identical to the promised spin-product Pfaffians without an explicit reduction.

This review establishes correctness under the exact probability-law contract. It does not establish priority, optimality, physical reconstruction, model certification, access to iid equilibrium data, efficient rare conditioning, general composability, or a transformative practical consequence. No theorem statement should imply those stronger outcomes.
