# One global fractional-factorial bulk certificate: no sector partition

Status: newly derived candidate, awaiting adversarial audit. This is NOT a recurrence theorem: a fixed-width union of coordinate boundary strips remains infinite in dimension≥2.

## 1. Finite killed-generator lemma
Let Q be a finite substochastic generator: off-diagonal rates k_ij≥0, diagonal Q_ii=−sum_(j≠i)k_ij−k_i0, with k_i0≥0. Assume every vertex has a directed path to a vertex with positive killing rate. For 0<alpha<1 put

    E_alpha(z)=sum_ij k_ij[z_i^(1−alpha) z_j^alpha−z_i]−sum_i k_i0 z_i,
    z_i≥0, sum_i z_i=1.

Claim: there exists alpha0>0 such that for every0<alpha<alpha0, E_alpha(z)<0 for every z on the closed simplex. For each such fixed alpha there is a uniform eta_alpha>0 with E_alpha≤−eta_alpha.

Proof. Positive individual edge terms are uniformly O(alpha). Indeed if z_j>z_i, write z_i=z_j t, t∈[0,1]; then

    z_i^(1−alpha)z_j^alpha−z_i
      =z_j(t^(1−alpha)−t)≤2alpha/e, alpha≤1/2,

by the mean-value theorem and max_(0<t≤1) t^(1−alpha)|log t|≤2/e. Suppose alpha_n→0 and E_(alpha_n)(z^n)≥0. Pass to z^n→z. The killing term and the O(alpha_n) positive-term bound force z_i=0 at every killed vertex. Let U={i:z_i>0}; U is nonempty. A path from U to killing has an edge i→j with i∈U,j∉U. Its negative contribution divided by alpha_n has magnitude

    k_ij z_i^n [1−exp(−alpha_n L_n)]/alpha_n,
    L_n=log(z_i^n/z_j^n)→infinity.

This tends to infinity: use 1−e^(−u)≥min(u/2,1−e^(−1)). If z_j^n=0, the conclusion is immediate. All positive contributions divided by alpha_n remain bounded. Contradiction. Continuity on the compact simplex supplies eta_alpha>0. No spectral gap, invariant distribution, or assumed Lyapunov function enters.

## 2. Simultaneous proper-subset contraction
Let the full finite complex graph be strongly connected, with at least two distinct complexes. For every nonempty proper subset U of complexes, restrict the graph to U and kill at edges leaving U. The lemma applies. There are finitely many U, so choose one fixed alpha>0 working for all of them.

Define the full graph functional

    H_alpha(z)=sum_(y→y') k_yy'[z_y^(1−alpha)z_y'^alpha−z_y],
    z≥0, sum_y z_y=1.

On the boundary of the simplex its nonzero support is a proper U, and H_alpha equals that killed functional: edges entering U from zero source contribute0, edges leaving U contribute−k z_y. Therefore H_alpha is uniformly strictly negative on the entire simplex boundary. By continuity it remains≤−eta in an open neighborhood of that boundary, for some eta>0.

Unlike coefficientwise face fugacity tests, this conclusion handles every proper support, including nonsimplicial faces and arbitrarily separated internal monomial scales. Numerical small-alpha thresholds can be enormous; no useful effective bound is claimed.

## 3. Exact factorial comparison
Take stochastic mass-action rates lambda_y→y'(x)=k_yy'(x)_y. Define ONE measure on the entire lattice:

    mu_alpha(x)=product_i (x_i!)^(−alpha).

Write a_y(x)=(x)_y and nu=y'−y. At coordinates larger than a fixed graph-dependent threshold, every incoming predecessor is valid and

    mu_alpha(x−nu) lambda_y→y'(x−nu)/mu_alpha(x)
      =k_yy' a_y(x)^(1−alpha) a_y'(x)^alpha [1+epsilon_yy'(x)],

where |epsilon_yy'(x)|≤C/min_i x_i uniformly. This follows from the exact factorial ratio

    [ ((x−nu)! (x−y)!)/(x! (x−y')!) ]^(1−alpha)

and finite-product estimates; factorials and products here are coordinatewise. The source and target exponents are in this order. This is not an asymptotic replacement at bounded counts.

Let A(x)=sum_y a_y(x), z_y=a_y/A. Weighted Young's inequality bounds a_y^(1−alpha)a_y'^alpha≤(1−alpha)a_y+alpha a_y', so summing all rate-weighted approximation errors gives≤C' A/min_i x_i. Consequently

    (L*mu_alpha)(x)/mu_alpha(x)
      ≤A(x)[H_alpha(z(x))+C'/min_i x_i].

## 4. Classwise escape forces the monomial vector toward the simplex boundary
Fix a stoichiometric affine class x0+S. Along any unbounded sequence in this class with all coordinates≥K (K larger than all source coordinates), z(x) cannot remain in a compact subset of the positive simplex.

Otherwise all ratios a_y/a_y' remain bounded above and below. Uniform finite-product estimates give

    log a_y=y·log x+O(1/K).

Thus (y−y')·log x stays bounded for every complex pair. Divide by max_i log x_i and take a subsequence. The limiting v≥0 has max_i v_i=1 and v∈S^perp (single linkage: all complex differences span S). Since v is now fixed, v·x=v·x0 for every point in the class. But a coordinate with v_i>0 diverges along the sequence, contradicting nonnegativity and this conservation law.

Hence outside a class-dependent finite set, z(x) lies in the boundary neighborhood from Section2.

## 5. Bulk conclusion and precise missing step
Choose fixed K large enough that C'/K≤eta/2 and all factorial estimates are valid. Then on every stoichiometric class there is a finite set F such that

    (L*mu_alpha)(x)≤−(eta/2) A(x) mu_alpha(x)<0

for x outside F with every coordinate≥K. The measure and its product with any fixed polynomial jump rate are summable; it has every exponential population moment.

This is a genuine all-dimensional bulk gluing result for one strongly connected linkage class: a single global measure replaces the family of local radial measures and their selector commutators. No angular partition is present.

It is NOT global recurrence. The infinite sets where one or more coordinates<K remain. Also, for multiple linkage classes, a high-rate linkage can remain internally comparable while another linkage supplies escape; the full proper-support killed argument then fails on a union of whole linkage classes. Neither issue is assumed away.
