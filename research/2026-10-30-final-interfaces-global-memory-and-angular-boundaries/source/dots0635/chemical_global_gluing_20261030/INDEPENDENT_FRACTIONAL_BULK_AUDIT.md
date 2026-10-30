# Independent adversarial audit: fractional-factorial bulk certificate

Reviewer: finite_phase_drift_challenge. 2026-10-30. Internal mathematical review only. No external novelty certification.

## Verdict

The stated all-dimensional, single-linkage, fixed-width-bulk adjoint inequality passes this review. I found no mathematical defect in the killed-generator lemma, its simultaneous proper-support application, the exact factorial ratio, or the classwise escape argument. It is NOT a global recurrence theorem: the excluded coordinate strips remain infinite, and multiple linkage classes are not covered.

## 1. Hard finite-dimensional lemma

The positive-term estimate is valid uniformly up to zero coordinates: for 0≤t≤1 and alpha≤1/2, t^(1−alpha)−t≤(2/e)alpha. If E_alpha_n(z^n)≥0 and alpha_n→0, the total killing contribution is at most C alpha_n, so every killed vertex has zero limit coordinate. The limiting positive support is nonempty. A path from that support to a killed vertex must first leave it across an edge i→j with z_i>0 and z_j=0. Along the sequence z_i^n stays bounded below and L_n=log(z_i^n/z_j^n)→infinity (zero denominator treated directly). The magnitude of this single negative term divided by alpha_n is bounded below by a fixed positive multiple of

    min(L_n/2,(1−e^(−1))/alpha_n),

which diverges. All positive terms divided by alpha_n remain bounded. Other negative terms cannot cancel this. This proves the contradiction for all sufficiently small alpha, not merely along a chosen subsequence.

For fixed alpha in (0,1), the functional is continuous on the CLOSED simplex because both powers are strictly positive. Strict negativity therefore has a uniform negative maximum. Finitely many nonempty proper subsets of a strongly connected graph admit one common alpha. On a boundary support the full functional agrees exactly with the killed-subset functional: incoming edges from zero sources contribute zero, and edges into zero targets contribute their full negative source term. Uniform boundary negativity and its neighborhood follow by compactness.

Useful identification, not a literature equivalence claim: putting p=1/alpha and u_i=z_i^alpha gives E_alpha(z)=sum_i u_i^(p−1)(Qu)_i. Thus the finite lemma is strict dissipativity of a transient substochastic generator in sufficiently large unweighted ell-p norm. No stationary distribution of Q has been presumed.

## 2. Exact factorial identity and orientation

For nu=y'−y the actual incoming factor, divided by mu_alpha(x), is exactly

    k (x!)^alpha ((x−nu)!)^(1−alpha)/(x−y')!.

The proposed mixed source/target factor is

    k (x)_y^(1−alpha)(x)_y'^alpha
      =k x! /[((x−y)!)^(1−alpha)((x−y')!)^alpha].

Their ratio is exactly

    [((x−nu)!(x−y)!)/(x!(x−y')!)]^(1−alpha),

as written in the manuscript. In each coordinate, the offsets of the two numerator factorials sum to the offsets of the two denominator factorials. Consequently the leading power of x_i cancels, leaving 1+O(1/x_i), uniformly for the finite reaction set and for counts above a fixed threshold. The source exponent is 1−alpha, the target exponent alpha; no reversal error occurs.

Weighted Young controls each mixed monomial by a linear combination of its source and target monomials. The finite rate sum therefore bounds all approximation errors by C'A/min_i x_i. Incoming predecessors and all source/target factorials are valid once the graph-dependent count threshold is imposed. No approximation at bounded counts is used.

## 3. Escape in a fixed stoichiometric lattice class

Suppose infinitely many class states with every coordinate≥K have normalized monomial vectors in a compact positive simplex subset. Passing to an unbounded sequence, all monomial ratios are uniformly bounded. The expansion log(x)_y=y·log x+O(1/K) has a uniform bound because the finite complex coordinates are fixed. Let M_n=max_i log x_i^n→infinity and pass to log x^n/M_n→v. Then v≥0, max v_i=1, and v annihilates every complex difference. For one linkage class those differences span the stoichiometric subspace S, hence v is a fixed element of S-perp.

Every state of the sequence consequently obeys v·x^n=v·x0. But any coordinate with v_i>0 diverges, contradicting this equality and nonnegativity. This excludes every compact interior simplex subset at sufficiently large class states. On the discrete lattice, the exceptional bounded set is finite. The result is class-dependent; no uniform finite set over all conservation classes has been obtained or needed.

## 4. Quantifier order and conclusion

Choose alpha from the finite graph/rates first; obtain the boundary neighborhood and its negative margin eta; then choose a single count cutoff K large enough for all factorial estimates and C'/K≤eta/2. Finally, for each fixed stoichiometric class choose its finite exception set F from the escape argument. This order is consistent and noncircular. The resulting strict adjoint inequality holds on that class outside F wherever all coordinates≥K.

The positive measure product_i(x_i!)^(−alpha) and its product with every fixed polynomial are summable, and all exponential population moments are finite. These facts do not extend the local sign to excluded boundary strips. No embedded-chain recurrence conclusion is licensed without an additional boundary argument.

## 5. Quick primary overlap check: do not claim novelty yet

Agazzi and Laurence, *Bulk stability of bimolecular stochastic chemical reaction networks*, arXiv:2610.31550v1, submitted October 22, 2026: https://arxiv.org/abs/2610.31550 and https://arxiv.org/pdf/2610.31550 . Its abstract/introduction concern planar bulk Lyapunov construction using compactification and local patching, with compatible boundary estimates still needed. This is directly relevant current context, but is not the stated arbitrary-dimensional single-linkage fractional-factorial adjoint certificate. No full priority comparison was performed.

Anderson, Cappelletti, Kim, *Stochastically modeled weakly reversible reaction networks with a single linkage class*, https://arxiv.org/abs/1904.08967 , explicitly imposes binary and pure-species-complex assumptions in its recurrence theorem and uses embedded chains/tier sequences. The present conservation/monomial escape argument is close in spirit to tier methods, so the derivation should not be advertised as unprecedented without a detailed source comparison.

Reviewed source SHA-256: `439964f8c9c5fa3dd8cc0c6166b450b52a4b51519476ad35e168d2d3ff11b1ba`.
