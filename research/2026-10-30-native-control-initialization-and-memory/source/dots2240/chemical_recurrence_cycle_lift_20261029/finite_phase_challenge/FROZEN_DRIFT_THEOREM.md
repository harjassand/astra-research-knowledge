# Exact eventual sign of frozen finite-phase chemical drift

Independent reconstruction/challenge, 29 October 2026. This is a mathematical derivation, not an externally reviewed theorem or a proof of CTMC recurrence. The parent independently obtained the same argument before receiving this full note.

## Contract

There are finitely many modes j in {1,...,m}, exactly one occupied at a time, and one nonnegative unbounded count n. A complex is (j,a), a nonnegative integer. A reaction e:(j,a)->(k,b) changes the count by b-a and the mode to k, with mass-action rate k_e (n)_a. All k_e>0 are fixed. The finite graph on complexes is weakly reversible (each edge has a directed return path). The graph obtained by projecting reactions to modes is irreducible. Same-mode count-changing reactions are allowed; multiple complex linkage classes are allowed.

For real x greater than the largest source exponent, freeze the count and retain only the mode jumps. Let Q(x) be this finite irreducible generator, excluding same-mode reactions from Q. Let p(x) be its unique stationary probability row vector. Define the frozen averaged count drift

    m(x) = sum_e p_j(x) k_e (x)_a (b-a).

This is a finite algebraic object. It is not asserted to be the actual process's asymptotic drift along trajectories.

## Theorem

Exactly one of the following holds:

1. There are integer offsets beta_j such that every reaction satisfies b-a+beta_k-beta_j=0. Then n+beta_mode is an exact pathwise invariant, every actual communicating class has at most m states, and m(x)=0 identically.
2. There are an integer H and C>0, explicitly determined by finite polynomials, such that

       m(x) = -C x^H (1+O(1/x)).

   In particular m(x)<0 for every sufficiently large x. H can be negative. A finite rational threshold can be computed when the rates are rational.

## Proof

Let tau_j(x) be the Markov-chain tree polynomial, the sum of weights of all directed mode spanning trees oriented into j. For m=1 use tau_1=1. Each tree weight is a product of finite sums of k_e(x)_a. Every nonzero tree polynomial has positive leading coefficient: each factor has positive leading coefficient and summation cannot cancel a leading positive coefficient. Irreducibility guarantees tau_j>0 for sufficiently large x.

Set t_j=degree(tau_j), T=sum_j tau_j, D=degree(T)=max_j t_j, beta_j=t_j-D, and c_j=LC(tau_j)/LC(T)>0. Then

    p_j(x)=tau_j(x)/T(x)=c_j x^{beta_j}(1+O(1/x)).

Define the height of each complex by h(j,a)=a+beta_j, and the height change delta_e=h(k,b)-h(j,a). Stationarity of the finite mode chain gives the exact identity

    sum_e p_j(x) k_e(x)_a (beta_k-beta_j)=0.

Thus m(x)=sum_e p_j k_e(x)_a delta_e. Same-mode reactions contribute zero to the added term, so no reaction was lost.

If every delta_e=0, the exact jump of n+beta_mode is zero and conclusion 1 follows. Otherwise let H be the maximum source height of an edge with nonzero delta_e. Every such edge with source height H points strictly downward. To see this, suppose it points upward to height>H. A directed return path exists by weak reversibility. Along that path there must be a first downward crossing back to height<=H, giving a nonhorizontal edge whose source height is >H, contrary to the definition of H. At least one nonhorizontal edge has source height H, by definition. Consequently

    C = -sum_{e: source height H, delta_e !=0} k_e c_j delta_e >0.

Each term's leading order is x^{a+beta_j}=x^{h(source)}. The horizontal edges vanish exactly, not merely to leading order. Every remaining term outside the displayed sum has a strictly lower integer power. Hence m(x)=-C x^H(1+O(1/x)), proving conclusion 2.

This proof also shows the two alternatives are exhaustive. An independently given phase-offset invariant forces m=0 exactly by stationarity, so it cannot coexist with alternative 2.

## Exact finite threshold and costs

For rational rates compute the polynomial

    N(x)=sum_j tau_j(x) sum_{e out of j} k_e(x)_a(b-a),

so m=N/T. In alternative 2, N has degree d=D+H>=0 and leading coefficient -c<0. If d=0, N<0 everywhere. Otherwise let B be the sum of the absolute values of all lower-degree coefficients. For x>=1,

    N(x) <= -c x^d + B x^{d-1}.

Therefore the rational/integer choice

    X = max{largest source exponent + 1, 2, floor(B/c)+1}

guarantees m(x)<0 for all real x>=X. This is a sufficient threshold, not a sharp one. It can be astronomically large. All source exponents, rates, denominator clearing and polynomial coefficients are actually used, not supplied as oracles.

Enumerating trees is a finite exact algorithm with potentially exponential cost in m. Alternatively determinant minors give the same polynomials. Their degrees are at most (m-1) times the maximum source exponent; the numerator degree is at most m times that exponent. No efficient bound in the *binary encoding* of exponents is claimed: explicit falling-factorial expansion is at least linear in the numerical exponent, and coefficient bit lengths and the number of trees must be charged. Nothing here establishes a practical general recurrence algorithm.

## Sharp scope limitation

The theorem is about one unbounded coordinate plus finitely many modes. It does not reduce an arbitrary-dimensional stochastic reaction network to such a representation. Fixing conserved internal counts can create finitely many modes, but their number may grow with those supplied counts and become infinite in a general boundary stratum.

Negative frozen drift alone is not a CTMC recurrence theorem. In particular, a uniform mixing-time comparison, a proper actual-generator Lyapunov function, or an exact trace-process argument remains necessary. A naive x-dependent Poisson corrector is evaluated after x changes and introduces extra terms; when neutral fast reaction rates dominate the drift, those terms may be larger than the claimed negative margin. Neither finite symbolic screens nor this sign proof closes that issue.
