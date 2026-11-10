Canonical prefix lowering preserves deficiency
and pays a uniform stationary rate-error box when that deficiency is zero
11 November 2026 Brisbane

1. Exact construction and structural counts.

Fix a finite weakly reversible reaction TABLE R on d original species. The table here means the actual table that is being lowered; it need not be the unaugmented input graph if catalytic channels have already been added. Let C be its set of distinct complexes, n=|C|, l its number of linkage classes and r its stoichiometric rank. Its deficiency is Delta=n-l-r. Use stochastic mass action with propensity k_e (x)_(y_e), where (x)_y=product_i x_i!/(x_i-y_i)! and the value is zero when y is not enabled. Parallel and null labels are charged separately.

Choose one global order on original species. For every complex, use the prefixes of its canonically sorted molecule list. Identical prefix vectors are shared. Let P be the set of prefixes of order>=2, a=|P|, and h the number of original complexes of order>=2. Each p in P has ONE parent obtained by removing its last molecule. Introduce one auxiliary X_p. Represent order0 by0, order1 by the original species and order>=2 by X_p. Add reversible binding

 rep(parent_p)+S_i <-> X_p,

and replace every original conversion y->z by rep(y)->rep(z). The decoder D is identity on original species and sends X_p to p. All channels have at most two molecules on each side. Previous exact graph/class and nominal-balance proofs apply to this canonical prefix construction.

The fine complex vertices consist of:
 - n represented original complexes;
 - a-h auxiliary singletons not already represented original complexes;
 - a binary binding inputs rep(parent_p)+S_i.

These sets are disjoint. A binary input cannot equal a0/1-molecule representative. Different binary inputs have different decoded prefix vectors, so are distinct. Each auxiliary singleton is distinct. Thus n_f=n+2a-h.

If X_p represents an original complex, its reversible binding attaches one new leaf vertex to the represented original linkage class. Otherwise the pair of complex vertices X_p and rep(parent_p)+S_i is an additional linkage class. Occurrence of X_p as a SPECIES inside another binary input does not identify those complex vertices. Hence l_f=l+a-h. Every linkage class is weakly reversible.

The a binding reaction vectors lie in ker D and are linearly independent: order auxiliaries by encoded degree; the auxiliary block is triangular with unit diagonal. Since D is onto and there are d+a fine species, dim kerD=a, so these binding vectors span kerD. Fine conversion vectors project under D exactly to the original reaction vectors. Therefore r_f=a+r.

Consequently, EXACTLY,

 Delta_f=n_f-l_f-r_f=n-l-r=Delta.                            (1)

This is not a monotonicity theorem for every possible graph-faithful compiler. It is a proof for the stated canonical shared unique-parent lowering. It explains both an opportunity and a limitation: a deficiency-zero table stays deficiency zero, while merely lowering a positive-deficiency table does not remove its deficiency.

2. Fixed-complex-graph quantitative balance under rate errors.

Assume now Delta=0, and suppose nominal fine rates k_e have a positive complex-balanced activity vector c. For every independent fixed perturbation |k'_e/k_e-1|<=delta<=1/2, there is a complex-balanced c' satisfying

 max_i |log(c'_i/c_i)| <= B_R delta,                         (2)

where B_R is explicitly computable from the FIXED fine complex graph and integer complex matrix. It is independent of the population, class, small rate magnitudes, fast normalization and c. Here is the constructive proof; an unknown-error measurement or an exact-real oracle is not required by the compiler.

On each finite linkage class let tau_C be the directed matrix-tree sum rooted at complex C. All its terms have exactly n_l-1 rate factors, where n_l is that linkage's number of complexes. Multiplicative rate errors give

 (1-delta)^(n_l-1) <= tau'_C/tau_C <=(1+delta)^(n_l-1).

This tree is on FIXED COMPLEX VERTICES, not on the unbounded population state space. Hence b_C=log(tau'_C/tau_C) has |b_C|<=2(n_f-1)delta. No minimum tree weight or stationary population probability occurs.

Let Y be the fine species-by-complex matrix and U the complex-by-linkage indicator matrix. Deficiency zero says Y is injective on im I=ker U^T, where I is the graph incidence matrix. Therefore the linear map

 (z,alpha) -> Y^T z-U alpha

is onto R^(n_f). Indeed any vector orthogonal to its image belongs to kerY intersect kerU^T, which is zero. Compute a fixed rational right inverse once. If R_s is its species-row block, solve z=R_s b with the accompanying alpha. Then c'=c exp(z) satisfies

 (c')^C/c^C=(tau'_C/tau_C)exp(alpha_linkage(C)).

The linkage scale is free in the complex balance equation, so these are complex-balanced activities for the perturbed rates. Taking B_R=max(1,2(n_f-1)||R_s||_(infinity->infinity)) proves(2). For a singleton/null linkage the empty tree has value1 and the same argument applies. This is also a direct quantitative proof of the particular deficiency-zero balance consequence used here.

The compiler does NOT need to calculate b, c' or unknown k'. It only uses the fixed rational right-inverse norm bound B_R. Logarithms and tree sums in this argument are proof devices; they do not become free numerical input or runtime oracles.

3. Class-uniform population control from the canonical anchor.

Use the nominal prefix activities c_i=lambda_i for original species and c_p=theta lambda^p for auxiliaries, 0<theta<=1. Let Gamma_hat be the actual fine class of j(x0)=(x0,0). It is unchanged by positive rate perturbations, and is closed because the fine table is weakly reversible. Let mu be the nominal product-form law conditioned on that class. Its partition sum contains the exact zero-auxiliary anchor weight lambda^x0/x0!.

Writing N=|Z| and n0=|x0|, take the rational bound

 G=2+3 sum_i c_i+n0²+n0 sum_(original i)lambda_i^-1.

Summing the unnormalized factorial weights over all fine states gives

 E_mu exp(N) <=exp(G).                                     (3)

The numerator is at most exp(e sum c_i); the denominator is at least the anchor, and log(x0!)<=n0², -sum x0_i loglambda_i<=n0 sumlambda_i^-1. These bounds explain(3) without a rare-class oracle or state enumeration. G is polynomial numerically in W0=2+n0+sum_(original i)(lambda_i+lambda_i^-1)+epsilon^-1 for fixed R, with no theta reciprocal, because all prefix degrees are fixed. Here x0, positive lambda_i, theta and epsilon are finite binary inputs, lambda_i and theta are rational, and 0<epsilon<1. The earlier nominal static choice makes theta^-1 polynomial in W0 as well; that additional choice is needed when importing the earlier fine-rate reciprocal contract.

For 0<=t<=1/[4(G+1)] and any fixed integer j>=0, concavity of x^s and x^j<=j!s^-j exp(sx) give

 E_mu N^j exp(tN) <=2 j![4(G+1)]^j.                        (4)

For j=0 the same constant2 is harmless. This is a uniform exponentially weighted bound, not the unhelpful exp(G) prefactor applied directly to a rare initial state.

4. Perturbed stationary law, whole TV and ABSOLUTE first moments.

Complex balance gives the perturbed stationary candidate mu' on the SAME actual class. With z=log(c'/c) from(2), it is exactly the exponential tilt

 dmu'/dmu=exp(z dot Z)/E_mu exp(z dot Z).

Let t=B_R delta. Since |z dot Z|<=tN,

 A0:=E_mu |exp(z dot Z)-1| <=8t(G+1),
 A1:=E_mu N|exp(z dot Z)-1|<=64t(G+1)²,

provided t<=1/[4(G+1)]. If t<=1/[32(G+1)], the tilt normalizer lies in[3/4,5/4]. Using the weaker denominator bound1/2 yields the explicit estimates

 TV(mu',mu)<=16t(G+1),                                    (5)
 |E_mu'(D Z)_i-E_mu(D Z)_i|<=256 D_* t(G+1)²,               (6)
 E_mu' N^j<=4 j![4(G+1)]^j,                               (7)

where D_* is the maximum decoder entry, enlarged to at least1. Pushforward cannot increase TV. Equation(6) uses (DZ)_i<=D_*N; it is an absolute error, not a relative or normalized error. Equations(3)--(7) are uniform over every finite or infinite actual class containing the canonical initial state and every admitted fixed independent rate perturbation.

For example choose a rational delta no larger than

 min(1/2,1/[32B_R(G+1)], epsilon/[512D_*B_R(G+1)²]).

Then perturbed-vs-nominal stationary decoded TV and absolute first-moment errors are each at most epsilon/2. Combine with the already available nominal static theta choice at epsilon/2 to meet the full stationary epsilon contract. The tolerance reciprocal is polynomial numerically in W; the fixed-degree rational arithmetic and output bit lengths are polynomial in complete input length. No actual error coefficient, class normalizer or exact sampler is computed.

Every elementary positive-total-population jump is0->1,0->2 or1->2, so its total positive-growth intensity is at most linear in N. This supplies structural nonexplosion for the finite constant-rate table. With the inherited common normalization max_e k_e<=1, the perturbed coefficients are<=3/2, and (7) pays the stationary intensity of ALL fine/null/parallel firings by a fixed-R multiple of(G+1)². Common normalization changes physical time and its reciprocal must retain the earlier polynomial rate contract; stationarity alone does not pay that reciprocal. The normalizable product law is positive throughout the closed irreducible class, so the nonexplosive process is positive recurrent there with its unique stationary probability.

5. What this closes, and the essential remaining restrictions.

For ANY weakly reversible DEFICIENCY-ZERO TABLE that is lowered by this construction, the independently perturbed stationary part is now quantitative on ALL actual classes: recurrence, whole decoded TV, absolute decoded means, stationary populations and stationary all-firing intensity. Equation(1) also shows why simple prefix lowering cannot invoke this argument on a positive-deficiency table.

This does NOT establish the full P3 compiler even for every raw input structure of deficiency zero. The accepted polynomial mixing compiler may add catalytic pump/join channels BEFORE lowering, and that augmented table can have positive deficiency. Zero deficiency of the RAW input is not silently substituted for zero deficiency of the ACTUAL TABLE BEING LOWERED. Nor does stationary product form alone pay transient mixing time from the canonical input or total firings up to that mixing time. Combining with an existing polynomial nominal/finite-horizon construction is legitimate ONLY when it applies to this SAME resulting design with the same graph and rates. Those compatibility checks and the universal positive-deficiency operation remain unresolved.

This does not claim that every allowed compiler preserves deficiency, or a universal impossibility theorem. It also does not treat merely formal lattice classes as actual communicating classes. The nominal graph and conditioning are those of the exact physical prefix construction.

6. Governing source and original contribution binding.

Anderson--Craciun--Kurtz0803.3042v1, https://arxiv.org/pdf/0803.3042v1, Definitions2.2--2.4, Theorems3.1--3.3 and4.1--4.2 supply the established deficiency-zero/complex-balance and conditioned product-form foundations. The actual governing hypotheses were refreshed. Deficiency-zero product form itself is inherited primary machinery, not claimed new here. The exact canonical-prefix deficiency count, fixed-complex-tree/right-inverse UNIFORM error-to-activity comparison, and rare-class-independent tilted stationary law/resource estimates are the composition derived in this note. The zero-auxiliary anchor is reused from ROOT_INFINITE_CLASS_NOMINAL_BIMOLECULAR_ACCURACY_20261110.txt at its actual scope, not independently rediscovered. The nominal static accuracy and graph contracts are inherited from that construction; they are not a transient mixing theorem for this design.
