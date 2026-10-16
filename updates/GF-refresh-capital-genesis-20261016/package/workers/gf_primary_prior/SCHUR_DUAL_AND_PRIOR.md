# Exact Schur certificates and the closest optimization predecessors

16 October 2026. Self-contained reconstruction. Generic convex duality, sparse regression, rank-one quadratic optimization, and feature screening are established. The independent-generator all-subset separation in root/SINGLETON_SCHUR_CERTIFICATE.md is a separate source-relative derivation. Its historical priority is UNKNOWN. No numerical optimization or acquired code was executed for this note.

## 1. An attained exact dual, including singular matrices

Let B be any finite Hermitian positive semidefinite K-by-K matrix, a>=0, and d any complex K-vector. The complex l1 norm is sum_j |z_j|. Define

    L(z)=2 Re(d* z)-a z*Bz,       ||z||_1<=1,
    U(v)=a v*Bv+2||d-aBv||_infinity,       v arbitrary.

Then

    max_(||z||_1<=1) L(z) = min_v U(v).                    (D1)

Both extrema are attained. This remains true when B is singular, a=0, d=0, or the optimum lies in the interior. No pseudoinverse, Slater limit, positive definiteness, or assertion of a unique optimizer is required.

Proof. For all z,v,

    a v*Bv+2 Re[(d-aBv)*z]-L(z)
       =a(v-z)*B(v-z)>=0.

The complex l1 support function is

    max_(||z||_1<=1) Re(r*z)=||r||_infinity.

Indeed Holder gives the upper bound, and a unit vector at a maximum-magnitude coordinate, with phase aligned with that coordinate of r, attains it. This proves weak duality L(z)<=U(v).

Compactness of the l1 ball and continuity give a primal maximizer z0. Differentiable concave optimality on the underlying real vector space gives

    Re[(d-aBz0)*(z-z0)]<=0       for every ||z||_1<=1.

Writing r0=d-aBz0, the support-function identity implies

    Re(r0*z0)=||r0||_infinity.

Consequently U(z0)=L(z0). Thus v=z0 is a dual minimizer and (D1) follows, including every degenerate case stated above. This proof establishes dual attainment directly; it does not infer it from an unbounded dual feasible set. End proof.

For the supplied Schur problem, a=pq, d=hc, and the endpoint value is Q+the value in (D1). If z is feasible and v arbitrary, the computable gap

    G(z,v)=a v*Bv+2||hc-aBv||_infinity
            -2h Re(c*z)+a z*Bz >=0                      (D2)

certifies the value to an interval of width G. Solver status is unnecessary. An equality certificate consists of feasible z and v with G=0. The simplest exact choice is v=z satisfying the following KKT test.

Let r=hc-aBz and lambda=||r||_infinity. For every nonzero coordinate require

    r_j=lambda z_j/|z_j|,

and require |r_j|<=lambda at zero coordinates, together with

    lambda(1-||z||_1)=0.

These conditions are necessary and sufficient. When lambda=0 all coordinates of r vanish, so an interior optimizer is covered. A violated zero-coordinate inequality supplies a feasible improving direction after reallocating l1 mass. Multiple primal/dual optimizers, null directions, and zero weights do not invalidate the certificate. Finite exact arithmetic must establish comparisons/equalities; rounded residuals alone are not exact certificates.

## 2. The generic problem is constrained least squares

For a>0 and d in Ran(B), put A=sqrt(a) B^(1/2) and y=B^(+1/2)d/sqrt(a). Completing the square gives

    L(z)=d*B^+d/a-||Az-y||_2^2.

Thus the general Schur optimizer is a complex l1-constrained least-squares problem. On real coefficients it is the constrained Lasso form; complex coefficients become real two-coordinate groups with Euclidean group norms. The usual residual-correlation KKT test and primal-dual gaps therefore have established sparse-regression antecedents. For a Schur correlation matrix C=[[1,c*],[c,B]]>=0, positivity implies c in Ran(B), so this representation applies whenever a>0. Formula (D1) itself does not need that range condition.

A more informative representation uses the independent-generator input without forming a dense square root. Let independent X_j in {-1,1} have E X_j=eta_j and let X_S=product_(j in S) X_j. Then

    E[X_S X_T]=product_(j in S xor T)eta_j=B_ST,
    E[X_S]=product_(j in S)eta_j=c_S.

For Z(X)=sum_(nonempty S) z_S X_S,

    2h Re(c*z)-a z*Bz
       =h^2/a-a E|Z(X)-h/a|^2.                         (D3)

The full problem is therefore regression of a constant against all nonempty parity features on a biased product cube, with a bound on the Fourier coefficient l1 norm. This is an exact algebraic identification, not a new statistical theorem or a promise of an efficient general solver. The input has m bias parameters but 2^m-1 possible coefficients. Explicit data over all cube vertices is also exponential. A generic dense Lasso implementation does not supply an implicit polynomial algorithm for this representation.

## 3. Closest primary predecessors actually read

### Single-index portfolios: close to the singleton solve

Elton, Gruber, Padberg, Simple Criteria for Optimal Portfolio Selection (1976), author-hosted PDF, pp. 1347-1348, equations (5)-(9), and Appendices A-C, pp. 1355-1356:

https://pages.stern.nyu.edu/~eelton/papers/76-dec.pdf

The primary scan was rendered and equations were read visually; adjacent OCR is only a navigation aid. The paper derives an active-prefix cutoff and positive weights for single-index covariance, a diagonal-plus-rank-one matrix. Its KKT proof orders assets by excess return divided by factor loading. The paper optimizes a return/standard-deviation ratio with a riskless asset; it is not literally the supplied fixed-risk-aversion simplex problem.

The exact mathematical overlap is the normal equation. For the singleton restriction, B_single=diag(1-eta_j^2)+eta eta^T. On active coordinates, the simplex KKT equation is

    (1-eta_j^2)v_j=(t-s)eta_j-mu,
    s=eta dot v.

Thus a common threshold in eta determines the active prefix, and two scalar equations determine t-s and mu. This is the same diagonal-plus-one-factor elimination and cutoff mechanism, with the budget multiplier supplying a common return shift. Generic rank-one elimination, sorting, and KKT sufficiency should not be claimed as new.

### Rank-one proximal optimization: useful, but preserve its complexity qualifiers

Becker and Fadili, A quasi-Newton proximal splitting method (2012), Theorem 7, Corollary 9, Proposition 10, Table 1:

https://proceedings.neurips.cc/paper_files/paper/2012/file/e034fb6b66aacc1d48f445ddfb08da98-Paper.pdf

The proof reduces diagonal-plus-rank-one proximal maps to a scalar root. For separable piecewise-affine proximal maps the root is obtained exactly by sorting breakpoints. Table 1 explicitly lists the canonical simplex and l1 ball as NONSEPARABLE semismooth-Newton cases. Therefore this source does not, by itself, prove O(m log m) exact complexity for the entire singleton simplex problem. It is a close antecedent for the rank-one/proximal mechanism, not a license to erase that distinction.

### Omitted-feature certification and exponentially large pattern families

Nakagawa et al., Safe Pattern Pruning (2016), Theorem 2 and its proof in Section 3.3, Lemmas 4-7:

https://arxiv.org/abs/1602.04548

The proof bounds residual correlations for all descendants of a pattern, uses a primal-dual gap ball, and prunes an entire subtree only when no coefficient there can be active. The observed pattern features have an antimonotonic occurrence structure. Biased parity features take signed values and do not automatically satisfy that occurrence ordering. Explicitly expanding parities into positive itemset indicators can increase representation size exponentially. This paper does not directly give the root residual-prefix formula or its complexity.

Le Morvan and Vert, WHInter (2018), equations (3)-(5), Section 2.2, Theorem 3.1:

https://proceedings.mlr.press/v80/morvan18a.html

The source makes the central incumbent explicit: solve on a working set and check all omitted residual correlations; stop only when no violation remains. It uses branch pruning and maximum-inner-product search for two-way binary interactions. It does not state the all-order product-kernel maximum used in the present certificate. Ndiaye et al., Gap Safe Screening Rules (2017), Theorem 3, Proposition 5 and Theorem 6, supplies the general residual/KKT and certified-gap framework:

https://jmlr.org/papers/v18/16-577.html

## 4. What the root certificate adds relative to these inspected sources

The source-relative step is the exact maximum over exponentially many omitted PARITY features. For the water-filled singleton vector, its residual on every subset is a product of eta values times a low-degree reciprocal sum. Under the proved active-threshold condition, coordinate monotonicity shows that the worst negative residual at each cardinality occurs on a sorted prefix. Inactive factors cannot increase its magnitude. Hence one sorted prefix scan evaluates the FULL infinity norm used in (D2), rather than a sampled gradient or a conservative screening bound.

This proves an exact-value region and an exact global bracket for that candidate with implicit tensor input. It does not solve every constrained Schur instance. General portfolio/Lasso/screening tools explain the singleton and certificate architecture; the special subset-separation algebra still needs the supplied proof. No historical-priority claim follows from not finding the exact formula in this bounded primary search. An equally informed classical optimizer can adopt the same separation result.

## 5. Scope

The Schur variational formula, privacy, fixed schedules, causal embedding, actual full-joint node channel, and endpoint instruments remain receiving premises. Computational certificates cannot qualify those physical assumptions. Generic sparse-regression duality does not prove a quantum-memory lifetime. No full optimizer, physical device, scalable operation, or scientific performance advantage was acquired here.
