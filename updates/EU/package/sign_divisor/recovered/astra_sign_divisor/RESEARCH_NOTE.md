# Sign-divisor extraction, exact degree normal forms, and robust sampling obstructions

ASTRA Primitive Genesis — research record, 13 October 2026

## Status and scope

This record gives self-contained derivations of an exact structural theorem for polynomial-threshold generators, its coordinatewise degree-normal-form consequence, and a robust Gaussian-mixture sampling bound. The last result imports two established analytic inequalities, explicitly identified below. The arguments have not received independent mathematical review; the finite checks are diagnostics, not a proof of the general results. Historical novelty is not established. In particular, earlier work already proves code-sampling lower bounds for other restricted generator classes.

No resolution of unrestricted circuit lower bounds, general quantum marginal compatibility, Navier–Stokes regularity, or a comparably consequential foundational problem is claimed. The preserved advance is a complete description of exact parity invariants in the specified polynomial-sign representation, together with a quantified failure of low-degree mixtures and an exact alternative representation.

The labels “sign-divisor extraction” and “degree normal form” are descriptive names used in this record, not claims of historical priority.

## 1. Independent search and route selection

The initial search compared the following different obstructions. This was a screening of possible mechanisms, not an assertion of comprehensive mastery of all four literatures.

| Direction | Decisive objective | Obstruction exposed by the attempted mechanism |
|---|---|---|
| Fluid singularities | A coercive estimate controlling critical vortex stretching without assuming regularity | Repackaging strain and vorticity did not supply a new cancellation; the uncontrolled term remained. |
| Unrestricted Boolean circuits | An explicit superpolynomial lower bound compatible with arbitrary reuse of intermediate computations | Candidate local representation costs did not survive unrestricted gate composition. A restricted-model separation cannot be transferred for free. |
| High-dimensional concentration | Dimension-free concentration via a new operator or geometric flow | Current proof claims change the target landscape; a purportedly new attack must engage those claims rather than assume an old problem statement is still the frontier. |
| Quantum local-to-global consistency | An acquired positive global completion rather than an unproved compatibility premise | Gaussian-sign positive completions give a concrete inner class, but do not encompass all compatible marginals or entangled states. Exact algebraic support constraints expose a representation obstruction. |

The Gaussian pair-marginal construction is preserved in Appendix A. Its failure led to a question that could be answered completely: which exact binary constraints can polynomial-threshold latent generators satisfy, and what does that force their degree to be?

General local-density-matrix consistency has a QMA-complete promise formulation [4]. This is context, not an unconditional impossibility theorem for the constructive subclasses considered here.

## 2. Definitions

Write binary outputs in the field F_2. For a nonzero real polynomial p, define its output bit by

    bit_p(z) = 1 if p(z) < 0, and 0 otherwise.

Values on polynomial zero sets are immaterial under any latent law with a density that is strictly positive almost everywhere on R^m. Let

    F(z) = (bit_p1(z), ..., bit_pn(z)).

The support of F(Z) means its positive-probability atoms. Its affine hull is taken over F_2, not over R.

Constant coordinates are allowed and have degree zero. A coordinate polynomial that becomes identically zero after an affine pullback can be replaced by the appropriate constant according to the chosen zero convention.

An irreducible real polynomial is **sign-changing** if it takes both strictly positive and strictly negative real values. Nonconstant irreducible factors that do not change sign must not be treated as independent binary sign variables.

## 3. A local crossing lemma

**Lemma 1.** Let q be a sign-changing irreducible real polynomial. Let r_1,...,r_t be finitely many real irreducible polynomials, none associated to q. There exists a real smooth point of q=0 which lies on none of the zero sets r_j=0. At this point a small transverse segment crosses q=0 while the signs of all r_j stay unchanged.

**Proof.** Choose two points at which q has opposite signs. Use their connecting direction as the t coordinate and write the remaining coordinates as y. On the resulting line y=y_0, there are fixed endpoints t=a,b with opposite q signs. The same remains true on an open set of nearby parallel lines.

The polynomial q has positive degree in t. Its irreducibility and Gauss's lemma make it irreducible in R(y)[t]. In characteristic zero it is relatively prime to its t derivative. Hence the resultant of q and its t derivative is a nonzero rational function of y; clearing denominators gives a nonzero polynomial whose nonvanishing, together with that of the leading coefficient, guarantees that the specialized polynomial in t has only simple roots.

Similarly, for each r_j having positive t degree, the resultant of q and r_j is nonzero over R(y). If r_j is independent of t, simply exclude its zero set in y. Exclude the zeros of these finitely many nonzero polynomials and the denominators and leading coefficients used above. Their union has empty interior, so a nearby parallel line avoiding all of them exists.

The opposite endpoint signs force a real root on that line. The root is simple and is not a root of any r_j. Therefore the t derivative of q is nonzero there, and crossing the root changes precisely the sign of q among the listed distinct factors. For one variable, the same assertion follows directly from the fact that a sign-changing irreducible real univariate polynomial is linear. QED.

## 4. Sign-divisor extraction

Factor p_1,...,p_n over R and collect all distinct sign-changing irreducible factors q_1,...,q_s. For each factor define its incidence mask

    v_j = (ord_qj(p_i) mod 2)_(i=1,...,n) in F_2^n.

Masks equal to zero can be discarded. Let V be their binary linear span.

**Theorem 2 — exact affine-support extraction.** For any regular output c_0=F(z_0),

    aff_F2(supp(F(Z))) = c_0 + V.

Equivalently, a parity a dot F(Z) is almost surely constant if and only if a dot v_j=0 for every j. Its value is a dot c_0.

**Proof.** Even powers contribute no sign changes. Every non-sign-changing irreducible factor has a fixed sign away from its zero set, so those signs can be absorbed into a fixed binary offset b. Unique factorization yields

    F(z) = b + sum_j v_j 1{q_j(z)<0}   in F_2^n

away from the union of the zero sets. Consequently the support is contained in c_0+V.

For the reverse inclusion, apply Lemma 1 to q_j and every other distinct irreducible factor occurring in the p_i. On the two sides of the resulting crossing, the output vectors differ by exactly v_j. Both sides contain open sets, which have positive probability under the specified latent law. Thus each v_j lies in the linear span of differences of actual support points. This proves equality. The parity characterization is its binary orthogonality formulation. QED.

A compact way to describe the operation is

    partial_sgn(p) = (ord_q(p) mod 2)_(q sign-changing),
    partial_sgn(p r) = partial_sgn(p) + partial_sgn(r).

For a vector of output polynomials, the operation replaces all its exact parity constraints with the kernel of the transpose of a finite binary factor-mask matrix.

### What the operation does not recover

It recovers the affine hull of the support, not the support itself and not its probabilities. For example, take

    p_1=x(x+y),   p_2=y(x+y),   p_3=xy.

Their sign bits have even parity because their product is x^2 y^2 (x+y)^2. The factor masks span the entire two-dimensional even-parity code. Nevertheless only the outputs 000, 101 and 011 occur: 110 cannot occur because x and y having the same sign forces x+y to have that sign. Thus the affine hull has four points while the support has three.

This counterexample prevents an invalid escalation from “all parity invariants are extracted” to “all global compatibility constraints are solved.”

### Acquisition costs

Given a real factorization and the sign-changing classification of its factors, mask formation and kernel computation use finite binary linear algebra. No efficient general algorithm for obtaining those real-algebraic inputs is claimed here. In particular, deciding sign-changing behavior and finding an optimal code basis are not free computational primitives.

## 5. Exact coordinatewise degree normal form

Let C be a k-dimensional binary linear subspace of F_2^n, and let c+C be an affine translate. For a basis B=(b_1,...,b_k) of C, define its coordinate loads

    ell_i(B) = sum_j (b_j)_i.

**Theorem 3 — complete degree-budget characterization.** The uniform law on c+C can be generated by polynomial thresholds of coordinate degrees at most (d_1,...,d_n), using a Gaussian latent vector of any finite dimension, if and only if C has a basis B satisfying

    ell_i(B) <= d_i  for every i.

Whenever such a representation exists, it can be replaced by a generator whose coordinate polynomials are parity monomials, without increasing any coordinate degree.

**Proof: necessity.** Exact uniform generation has support c+C. Theorem 2 says the sign-changing factor masks span C. Select k independent masks b_1,...,b_k from them. Whenever (b_j)_i=1, the corresponding irreducible factor occurs to odd positive multiplicity in p_i and contributes at least one to its total degree. Therefore ell_i(B)<=deg(p_i)<=d_i.

**Proof: sufficiency.** Take independent standard Gaussians Y_1,...,Y_k and define

    ptilde_i(Y) = (-1)^(c_i) product_(j:(b_j)_i=1) Y_j.

An empty product is one. The sign bits of Y_j are independent fair bits, so the output is a uniformly random affine combination c+sum_j U_j b_j. It is uniform on c+C, and deg(ptilde_i)=ell_i(B). QED.

The structural necessity only uses full affine support; uniformity is needed for the stated replacement to preserve the entire target law.

### Exact optimization formulas

Define D_sum(C) to be the minimum total coordinate degree of an exact uniform polynomial-threshold generator, and D_max(C) its minimum possible largest coordinate degree. The theorem gives

    D_sum(C) = min_(B basis of C) sum_(b in B) wt(b),
    D_max(C) = min_(B basis of C) max_i ell_i(B).

These basis-cost expressions are consequences of the theorem. They are not claimed to be historically new combinatorial invariants merely because they receive notation here.

If every nonzero codeword has Hamming weight at least d, then

    sum_i deg(p_i) >= d k,
    max_i deg(p_i) >= d k/n.

In particular, for d>=delta n and k>=R n, the largest degree is at least delta R n.

### Exact mixture tradeoff

Suppose a mixture of L polynomial-threshold generators has exact uniform law on c+C. Let T_j be the sum of coordinate degrees in component j, and assume its weight is positive. Positivity of mixture weights forces each component to be supported inside c+C.

By Theorem 2 its affine-support direction space has a basis consisting of nonzero vectors of C. If its dimension is r_j, degree accounting gives d r_j<=T_j, so that component has at most 2^(T_j/d) support points. Covering all 2^k target points implies

    sum_(j=1,...,L) 2^(T_j/d) >= 2^k.

If every coordinate of every component has degree at most D and delta=d/n, then

    log_2 L + D/delta >= k.

In particular, affine Gaussian thresholds, D=1, need exponentially many mixture components for constant-rate, constant-relative-distance codes.

### Finite-bit implementation and the interpretation of degree

The canonical monomial generator does not require numerical Gaussian sampling: draw k independent fair bits and multiply a binary generator matrix by that bit vector. Dense evaluation needs O(nk) binary operations. Gaussian signs are just an equivalent mathematical representation. The normal form preserves coordinate degree budgets, not the original number of latent variables: it uses k independent signs, with k<=n. It does not assert a degree-preserving compilation within the original circuit architecture.

Thus these are degree and mixture-size lower bounds, not runtime lower bounds. A high-degree parity monomial can be evaluated efficiently. There is no implication here that P differs from NP, that such target laws are computationally hard to sample, or that unrestricted neural networks require exponential size.

## 6. Robust lower bound for approximate Gaussian-threshold mixtures

The exact factorization argument is not stable under small coefficient perturbations. To obtain an approximation result, replace algebraic extraction by a collision-packing argument.

Let S be a subset of {0,1}^n with pairwise Hamming distances at least delta n, where 0<delta<=1. Let P be supported on S and satisfy

    max_x P(x) <= 2^(-h).

Thus h is a lower bound on min-entropy. Suppose Q is a mixture of L laws generated by coordinatewise real polynomial thresholds of degree at most D, D>=1, applied to Gaussian latent vectors. Each component may use its own dimension, coefficients, mean and covariance. Singular Gaussians are included by affine pullback to their intrinsic latent space.

For 0<eta<1, define

    theta = pi delta eta^2/(2D),
    rho = cos(theta),
    a = (1-rho)/(1+rho) = tan^2(theta/2),
    K(D,delta,eta) = (2/eta)^[cot^2(pi delta eta^2/(4D))].

**Theorem 4 — robust packing bound.**

    TV(P,Q) >= 1 - eta - L K(D,delta,eta) 2^(-h).

No component is assumed to be supported on S. Arbitrary leakage outside the code is allowed.

### Imported inequalities

For a degree-D polynomial threshold f and correlated standard Gaussians G,G_rho with correlation rho=cos(theta), Kane's noise-sensitivity bound gives [1]

    Pr[f(G) != f(G_rho)] <= D theta/pi.

Gaussian hypercontractivity for the Ornstein–Uhlenbeck operator gives, for every measurable A [2],

    Pr[G in A, G_rho in A] <= gamma(A)^[2/(1+rho)].

Indeed this is ||P_sqrt(rho) 1_A||_2 <= ||1_A||_(1+rho), squared. Positivity of that same operator also gives the lower bound

    Pr[G in A, G_rho in A] >= gamma(A)^2,

because P_rho=P_sqrt(rho) P_sqrt(rho), and the squared L2 norm is at least the squared mean. These analytic facts are established tools, not inventions of this investigation.

### Proof of Theorem 4

Consider one component Q_j and write q_x=Q_j({x}). Let

    tau = 1/K = (eta/2)^(1/a),
    H_j = {x in S : q_x > tau},
    T_j = S minus H_j,
    q = Q_j(T_j).

There are at most K heavy atoms in H_j. Set A=F_j^(-1)(T_j). Operator positivity implies that the probability that both correlated outputs lie in T_j is at least q^2.

Split that joint event into equal and unequal output pairs. If they are unequal, their Hamming distance is at least delta n. Summing the degree-D noise bounds over the coordinates and applying Markov's inequality gives

    Pr[both outputs in T_j and unequal]
       <= D theta/(pi delta) = eta^2/2.

For equal outputs, hypercontractivity applied to each fiber F_j^(-1)({x}) gives

    sum_(x in T_j) Pr[F_j(G)=F_j(G_rho)=x]
       <= sum_(x in T_j) q_x^(1+a)
       <= q tau^a = q eta/2.

Therefore

    q^2 <= q eta/2 + eta^2/2.

The positive root of this quadratic is eta, so Q_j(T_j)<=eta.

Now let H be the union of the heavy sets over all L components. It contains at most LK target points, and every component assigns at most eta mass to S minus H. Consequently

    Q(S minus H) <= eta,
    P(S minus H) >= 1-LK 2^(-h).

Taking the difference on this single event proves the total-variation bound. QED.

### Consequences and constants

Using tan(x)>=x,

    log_2 K <= 16 D^2 log_2(2/eta)/(pi^2 delta^2 eta^4).

For fixed delta,D, targets with h>=Rn, and L=2^o(n), one can take eta=n^(-1/8). Then log_2 K=O(sqrt(n) log n)=o(n), so TV(P,Q) tends to one.

A simple finite inequality follows from eta=1/2. If TV(P,Q)<=1/4, then

    log_2 L + (512/pi^2) D^2/delta^2 >= h-2.

Thus for constant-rate, constant-relative-distance uniform codes and polynomially many components, degree Omega(sqrt(n)) is necessary for TV error at most 1/4. Constants in the displayed K can be very large; this is not a claim of useful numerical bounds at small block lengths.

### Relation to earlier sampling lower bounds

Lovett and Viola proved that small constant-depth Boolean circuits cannot sample uniform good codes even approximately, with total-variation distance tending to one [3]. Therefore neither “codes obstruct restricted samplers” nor “sampling lower bounds can approach maximal total variation” is new in itself.

The result proved here is specifically a Gaussian polynomial-threshold mixture statement with the explicit packing inequality above. Its novelty relative to all related literature is unestablished. The present audit inspected the Lovett–Viola abstract, not its full proof.

## 7. Counterexamples and unresolved boundary

### 7.1 Exact factor sharing is not a stable approximation invariant

Take p_1(x)=x and p_2(x)=x-epsilon with epsilon>0. They have no common irreducible factor. Nevertheless their sign bits disagree only when 0<x<epsilon, a standard-Gaussian event of probability Phi(epsilon)-1/2, which tends to zero.

Thus an argument asserting that a small parity defect forces literal shared factors is false. A robust theorem must use an approximate geometric object, not exact polynomial gcds.

### 7.2 The exact and approximate degree bounds do not match

For good codes the exact single-component result forces degree Omega(n). The approximation theorem, for polynomial mixtures and fixed TV error, forces only Omega(sqrt(n)). This record neither proves that a linear bound persists under approximation nor constructs a sublinear-degree approximate generator. The gap is a precise unresolved mathematical question of this investigation; no claim is made that its historical status was exhaustively settled by the search.

### 7.3 A mathematically distinct next attack

The candidate replacement is a Gaussian-weighted geometric description of sign boundaries. The exact theorem labels a shared irreducible hypersurface by the codeword of output bits that flip across it. Under approximation, nearby but distinct hypersurfaces can replace a shared factor, as the preceding counterexample shows.

A meaningful next result would have to quantify one of the following alternatives: either most of the probability-carrying boundaries of a near-code sampler admit approximately codeword-valued labels at controlled degree cost, or an explicit construction shows that approximate boundary matching permits lower-degree generation. Such a result must be derived from observable polynomial geometry and probability mass, not postulated as an unproved compatibility condition.

The present noise argument loses a square because the hypercontractive exponent differs from one by order theta^2, while the probability of a polynomial-sign change is controlled by order D theta. A geometric method would need additional structure beyond those two scalar inequalities to improve that loss. No such improvement is claimed here.

### 7.4 General targets remain outside the proved mechanism

The operation extracts binary linear constraints on support. It does not solve non-affine support feasibility, atom-weight synthesis, entangled quantum consistency, or unrestricted circuit complexity. A mechanism whose cost survives arbitrary composition and reuse is still missing for an unrestricted circuit lower bound. A globally positive completion extending beyond the Gaussian/separable inner class is still missing for the quantum route.

## 8. Prior Astra and repository audit

The investigation inspected the two repositories through the connected GitHub reader after initial independent screening. Searches for threshold, arcsine and hypercontractivity terms did not produce a matching construction, but the search index was not reliably complete. Empty search results are not evidence of historical absence.

Astra's complexity route and the scoped N26 positive-syndrome-locality card were inspected [6]. N26 concerns a normalized positive local syndrome-testing bound with a common auxiliary space; it is not the polynomial sign-factor extraction proved here. The card explicitly marks external correctness and priority unresolved. Only the retrieved card was inspected, not its full underlying proof package.

The OpenAI repository search surfaced current concentration and quantum-gap-related manuscript titles; it did not furnish a proof premise for Theorems 2–4. No exhaustive source or commit-history audit was completed. Accordingly the correct status is “derived here; historical novelty not established,” not “new to mathematics” or “independently validated.”

## 9. Reproducibility

`verify.py` runs deterministic finite diagnostics. The accompanying `checks.json` is the actual output from this investigation. It includes:

- All 90 binary linear subspaces in dimensions 1 through 4, and all 32,906 spanning subsets of their nonzero vectors. Coordinatewise basis extraction and its Pareto-degree consequence passed.
- Exhaustive basis optimization for four named small codes, with exact uniform parity encoding checks.
- A symbolic factor-mask example whose support has three points but affine hull has four.
- Exact rational/eigenvalue checks for the four-bit balanced-slice Gaussian-copula counterexample.
- Floating-point diagnostics for the pair-marginal construction below; these are explicitly not certified PSD computations.
- Twenty-seven checks of the robust-bound parameter algebra.

The finite checks do not establish the crossing lemma, the full analytic inequalities, the arbitrary-dimension conclusions, or novelty. Those require the proofs and source qualifications above.

## Appendix A. Initial quantum pair-marginal gluing construction

This appendix records the construction that motivated the representation investigation. Its scalar engine is the established Gaussian arcsine identity, not a newly invented probability law. Gaussian-threshold calibration and its global PSD restriction are discussed in [5].

Suppose n qubits have prescribed one-qubit states I/2 and desired pair states

    rho_ij = (I + sum_(a,b=1)^3 T_ij^(a,b) sigma_a tensor sigma_b)/4.

Assemble the pair coefficients in a real symmetric 3n by 3n matrix T with zero diagonal site blocks. Assume every entry has absolute value at most 1/3. Define, entrywise,

    K = I + sin^circ((3pi/2) T).

If K is positive semidefinite, sample G~N(0,K) and form unit Bloch vectors

    r_i = (sgn G_i1, sgn G_i2, sgn G_i3)/sqrt(3).

The state

    Omega = E [ tensor_(i=1)^n (I+r_i dot sigma)/2 ]

is fully separable and matches all prescribed pairs. Each coordinate has zero mean, and the Gaussian sign identity gives

    E[r_i^a r_j^b] = (2/(3pi)) arcsin(K_(ia,jb)) = T_ij^(a,b).

The entry bound ensures arcsin(sin((3pi/2)t))=(3pi/2)t. This is a sufficient completion certificate, not a characterization of all compatible pair marginals.

### A dimension-independent sufficient spectral radius

For a symmetric matrix T, its entrywise k-th power is a compression of T tensor ... tensor T under e_i -> e_i tensor ... tensor e_i. Hence

    ||T^circ k|| <= ||T||^k.

The power series and the triangle inequality imply

    ||sin^circ(cT)|| <= sinh(c||T||), c=3pi/2.

Therefore K is positive semidefinite whenever

    ||T|| <= 2 asinh(1)/(3pi),

approximately 0.187. The same norm bound implies the required entry bound. This is exact mathematics; the numerical examples in the code are only floating diagnostics.

For symmetric Sylvester Hadamard matrices H of size n, put S=H-diag(H) and

    T = [0.18/(sqrt(n)+1)] S tensor I_3.

Then ||T||<=0.18 while the absolute sum of the intersite coefficients in each axis row grows like sqrt(n). Thus the criterion is not merely a row-sum smallness condition.

### A compatible law that the single Gaussian-sign certificate misses

Let four signs be uniform over the six vectors with exactly two plus signs. Every distinct pair has correlation -1/3. A centered Gaussian-sign realization would require latent off-diagonal correlations sin(-pi/6)=-1/2. The resulting four-by-four correlation matrix has eigenvalue -1/2, so it is not positive semidefinite.

This does not prove that its pair marginals need large mixtures. In fact a mixture over the three perfect matchings, putting independent antithetic sign pairs on each matching, realizes those pair moments. It also realizes the full balanced four-bit law. More generally, pair data and full-law sampling must be distinguished throughout.

## References and reading scope

[1] Daniel M. Kane, *The Gaussian Surface Area and Noise Sensitivity of Degree-d Polynomials*, arXiv:0912.2709. https://arxiv.org/abs/0912.2709 . The noise-sensitivity proof was inspected in the PDF, including rendered pages. This supplies the degree-D Gaussian noise bound used in Theorem 4.

[2] Wei-Kuo Chen, Nikos Dafnis, Grigoris Paouris, *Improved Hölder and reverse Hölder inequalities for Gaussian random vectors*, arXiv:1306.2410. https://arxiv.org/abs/1306.2410 . The Ornstein–Uhlenbeck/hypercontractivity subsection was inspected in the HTML rendition during this investigation; the PDF statement was subsequently checked as well. Hypercontractivity is established prior mathematics, not attributed as a new result here.

[3] Shachar Lovett and Emanuele Viola, *Bounded-depth circuits cannot sample good codes*, ECCC TR10-115, 2010. https://eccc.weizmann.ac.il/report/2010/115/ . Abstract inspected; full proof not audited. Relevant prior sampling lower bound.

[4] Yi-Kai Liu, *Consistency of Local Density Matrices is QMA-complete*, arXiv:quant-ph/0604166. https://arxiv.org/abs/quant-ph/0604166 . Abstract and problem description inspected; used only for complexity context.

[5] *A Practical Guide to Simulating Correlated Binary Outcomes*, arXiv:2607.16801, July 2026. https://arxiv.org/abs/2607.16801 . Gaussian-threshold calibration and PSD limitations were inspected in the HTML version during the initial route exploration. Used for prior-art context, not as a premise for the elementary appendix proof.

[6] Astra Research Knowledge, scoped card N26-positive-syndrome-locality and complexity route. https://github.com/harjassand/astra-research-knowledge/blob/main/frontier/review_cards/N26-positive-syndrome-locality.txt and https://github.com/harjassand/astra-research-knowledge/blob/main/agent/topics/complexity.tsv . Scoped card inspected; external validity and priority retain its stated unresolved status.

[7] https://github.com/openai/math . Selective root and topic searches only; no exhaustive novelty audit and no imported mathematical premise for the principal theorems.

[8] Pierre Bizeul, Boaz Klartag, Joseph Lehec, *Presenting a proof of the Kannan-Lovasz-Simonovits conjecture*, arXiv:2610.05474, October 2026. https://arxiv.org/abs/2610.05474 . A current proof claim encountered during initial screening, not independently validated here and not used in any proof above.
