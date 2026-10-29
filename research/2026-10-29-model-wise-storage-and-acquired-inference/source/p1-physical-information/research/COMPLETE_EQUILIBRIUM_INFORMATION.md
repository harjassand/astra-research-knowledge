# Complete finite witnesses for robust hidden dissipation

29 October 2026. Root construction, developed alongside the independent
metric-tree characterization in `history_realization`. The central
question is which finite observations can rule out every hidden equilibrium
explanation when microscopic states and clocks are not bounded.

The result concerns stationary, finite-alphabet, memoryless observations
of finite all-even CTMCs. A physical entropy interpretation requires the
corresponding local detailed balance and physically correct reversal.
Unknown odd parity is a different model class, treated in the native-event
completion theorem. No microscopic branching or parity operation is
assumed available.

## 1. Consequence and exact boundary

Let E be the rational-cylinder closure of stationary finite reversible
CTMC observation laws. The complete metric-tree compatibility hierarchy
characterizes E. Consequently, a stationary observed law p is outside E
if and only if some finite observed word statistic F obeys

    E_r F >= 0 for every r in E,       E_p F = -gamma < 0.       (1)

The statistic is bounded and depends on finitely many rational times in
one interval [0,T]. Write L=max F-min F>0. For any finite all-even CTMC
whose observed law is p, its stationary entropy rate satisfies

    sigma >= 8 gamma^2/(T L^2).                              (2)

This is a complete family for detecting a strictly positive ROBUST entropy
floor. It is not a tight numerical entropy estimator. Existing geometric
or network-optimization bounds may be much stronger on particular data.

More precisely, take the lower envelope of entropy rates over all finite
all-even CTMC observation laws in each cylinder neighborhood U of p, then
take the supremum over U. This robust envelope is zero exactly on E. If
p is in E, zero-entropy finite models approximate every finite observation
list. If p is outside E, a strict witness remains strict in a neighborhood
and (2) supplies a positive common bound there.

This does not identify the infimum over models reproducing every detail
of p EXACTLY. The exact/approximate distinction is essential: the native
event construction provides an explicit infinite-versus-finite example.

## 2. A direct compact moment construction for the tree bridge

The accompanying metric-tree note gives a colored version of Aldous's
classical infinite-degree tree representation. The following direct
moment proof supplies a second route through its main representation
obligation, avoiding a choice of infinite branch labels.

Suppose a compatible probability table q_T is given for every finite
unrooted tree with positive rational edge lengths. Compatibility means
isomorphism invariance, leaf marginalization, edge subdivision with length
addition, and agreement with the supplied observed path tables.

Enumerate finite rooted metric-tree patterns T in which any subset of
vertices is assigned observation labels. A vertex may be unobserved.
Let T*U denote disjoint copies glued only at their roots, with inconsistent
root labels interpreted as the zero pattern. Let 1 be the unobserved
one-vertex pattern. Let ell(T) be the probability of the pattern obtained
by summing unused labels in q_T.

Construct a countable tree by attaching infinitely many disjoint copies
of every pattern's underlying rooted tree to a common root. Only roots
are identified. The tables q define a law on this countable tree:
any finite vertex set is contained in a finite connected subtree, and
leaf deletion makes the construction consistent. Marginalizing extra
unobserved vertices defines the same cylinder law regardless of the
chosen connected subtree.

For each T, the indicators of its labeled event in its successive copies
are exchangeable. The empirical averages therefore converge almost surely
to a variable M_T in [0,1]. All limits can be taken simultaneously because
the pattern set is countable. For any finite list of patterns,

    E product_k M_Tk = ell(T_1*...*T_k).                       (3)

To verify (3), expand products of empirical averages. Terms using distinct
copies have the displayed tree probability by isomorphism invariance.
Coincident-copy terms for a repeated pattern have bounded magnitude and
vanishing relative count. Dominated convergence finishes the argument.

Associative root gluing gives

    E[(M_T M_U-M_(T*U))^2]=0.                                (4)

Indeed the three terms in this squared expression are probabilities of
the same four-pattern glued tree. Thus M_T M_U=M_(T*U) almost surely,
including the zero convention. Also M_1=1, the one-vertex label variables
M_a are mutually exclusive indicators, and their sum is one.

Let mu be the law of the countable vector X=(M_T)_T on its compact closed
support in [0,1]^N. All countably many continuous equalities above hold on
that support. Set f_T(x)=x_T. Their linear span B is a unital multiplication
algebra and generates the state sigma-field. It is dense in L2(mu), by
Stone-Weierstrass followed by the density of continuous functions (or the
bounded monotone-class theorem). The sensor is the deterministic label
selected by the indicators f_a.

For a positive rational edge length c, make the analogous countable bush
at each endpoint of an edge of length c. Let its two empirical feature
vectors be X and X'. Leaf marginalization gives both the marginal mu;
root interchange gives a symmetric joint law nu_c. Disintegration on the
compact standard Borel state space defines a reversible Markov kernel K_c.

For rooted patterns U,T,

    <f_U,K_c f_T> = probability of U and T joined by c
                 = <f_U,f_(edge_c T)>.                        (5)

Here edge_c T is T with a new unobserved root, joined to the old root by
an edge c. The second equality follows from (3) by gluing U to that new
root. Density gives K_c f_T=f_(edge_c T). Recursively deleting a leaf and
using multiplication therefore shows that these kernels and the sensor
generate every original finite tree table q_T.

Subdivide a connecting edge of length s+t between arbitrary rooted
patterns U,T. The table identity gives

    <f_U,K_(s+t) f_T> = <f_U,K_s K_t f_T>.

Density now gives one semigroup, K_(s+t)=K_s K_t. Each K_t is selfadjoint
and K_t=K_(t/2)^2 is positive semidefinite. Unique positive roots yield
K_q=K_1^q for positive rational q. These are the crucial dynamical
compatibility conditions missing from separate positive factorizations
of reflected histories.

The remaining semigroup and finite approximation steps are as in the
accompanying note. Briefly, Poissonize K_delta with generator
(K_delta-I)/delta, then compress onto increasing finite partitions that
refine the sensor. The finite generators are reversible, have escape
rates at most 1/delta, and approximate every finite positive-time word
probability. Rates and state counts are not bounded uniformly.

Conversely every finite reversible CTMC generates the required tree
tables by independent conditional propagation along edges; compactness
passes those tables to cylinder limits. This proves the closure criterion.

If observed paths are stochastically continuous, the support projection
P=lim_(t down to 0) K_t fixes the sensor indicators. P is a positive
stationary orthogonal projection, so its bounded range is closed under
products. It contains every K_t image and hence every rooted-pattern
function. Density forces P=I. This yields an exact strongly continuous
standard-Borel reversible semigroup, without a finite-state, finite-rate
or regular-hidden-path conclusion.

This proof uses classical exchangeability, moment representation and
Markov-kernel disintegration. Aldous's uncolored representation is an
explicit antecedent. The assembled metric subdivision, finite CTMC closure
and inference statement are the contribution under investigation;
historical priority has not been established.

## 3. Why a finite observable inequality must exist

All finite tree tables lie in a compact product of finite simplices. Each
consistency equation involves finitely many entries. The full extension
exists if and only if every finite subsystem is feasible, by compactness.
Each finite subsystem is an ordinary linear feasibility problem.

If p fails the hierarchy, a finite subsystem has a Farkas separation
certificate. Its only supplied inputs are finitely many observed path
probabilities; structural matrix entries are rational. Strict separation
allows a certificate with rational coefficients. If the inputs involve
several time grids, shift them by stationarity into a common [0,T] and
take the union of their rational times. Each original probability is a
marginal of that larger word table. The dual inequality is exactly the
expectation of one bounded statistic F on this common grid, as in (1).

Finite separation alone follows already from closed convexity. The tree
contribution is an explicit complete family of finite LP/dual certificates,
without choosing a hidden-state count or a hidden rate parametrization.

Finite reversible models may be reducible because mixtures are allowed.
This does not change the closure if irreducibility is required: add an
epsilon-rate refresh to the stationary law. The new generator stays
reversible and becomes irreducible on positive-weight states. Coupling
until the first refresh bounds path TV change on [0,T] by 1-exp(-epsilon T).
Finite positive mixtures and their stationary weights are actual model
resources, not acquired initial preparations.

## 4. Entropy controls distance to the equilibrium class

Let Q be an all-even finite CTMC with strictly positive stationary law pi
on its supported states. Put Q*_(xy)=pi_y q_yx/pi_x and

    A=(Q+Q*)/2.

A is reversible for pi and has exactly Q's escape rates, since Q* does.
Take both stationary processes with the same initial pi. Their complete
path divergence on [0,T] is

    D(P_Q || P_A)=T sum_{x<y} B(f_xy,f_yx),
    B(f,g)=f log[2f/(f+g)]+g log[2g/(f+g)],                (6)
    f_xy=pi_x q_xy.

The usual conventions handle zero fluxes; if sigma is infinite the bounds
below are automatic. Otherwise reciprocal support holds. The all-even
stationary entropy rate is

    sigma=sum_{x<y}(f_xy-f_yx)log(f_xy/f_yx).

For f,g>0,

    B(f,g) <= (f-g)log(f/g)/4.                             (7)

One direct proof writes f+g=s and d=(f-g)/s. Both sides are even in d.
After division by s the difference, for d>=0, has derivative

    [d/(1-d^2)-atanh(d)]/2 >= 0,

and is zero at d=0. The nonnegativity follows by differentiating the
bracket. Thus

    D(P_Q || P_A) <= T sigma/4.                           (8)

Equation (7) uses an UNAVERAGED scalar flux-pair bracket. For normalized
probability distributions, the conventionally averaged Jensen-Shannon
divergence has the corresponding sharp local bound Jeffreys/8. These
normalizations must not be interchanged.

Observation and finite-time sampling contract KL. The observed law of A
belongs to E. If F has range L and violates (1) by gamma, the expectation
gap between Q and A is at least gamma. With TV defined as half the L1
distance, |E_Q F-E_A F| <= L TV. Pinsker and (8) give

    gamma <= L sqrt(T sigma/8),

which proves (2). No hidden dimension, spectral gap, clock bound or mixing
time appears in this valid inequality. Their absence is not a claim that
the needed observations can be obtained free of those resources.

### Reusing the stronger time-symmetric transfer

For any pointwise reversal-even statistic F, the previously developed
geometric path comparison gives the stronger linear bound below. When
the observed target itself is time-reversal symmetric, an arbitrary
separator can be symmetrized on the union of its grid and reflection:
the target and every equilibrium mean are unchanged, and the range does
not increase. This proves completeness of even separators on that subclass.
To use the bound operationally, simply construct an even statistic and
validate its mean; no empirical certification of the entire target's
time-reversal symmetry is required.

    sigma >= 4 gamma/(T L).                              (9)

For completeness, let p,p* be the full path densities under Q,Q*, and a
the path density under A. Because Q and Q* have the same escape clocks,
the arithmetic/geometric mean inequality on every jump gives a>=sqrt(p p*)
pointwise. Also (p+p*)/2>=sqrt(p p*). Hence

    TV((P_Q+P_Q*)/2,P_A) <= 1-integral sqrt(p p*).

The scalar inequality (u-v)log(u/v)>=4(sqrt(u)-sqrt(v))^2, integrated on
path space, bounds this last deficit by T sigma/4. A symmetric statistic
has the same expectation under Q and (Q+Q*)/2 as PATH LAWS, proving (9).
This path mixture is not the Markov law of the arithmetic generator A;
the pointwise comparison is what connects them. The transfer mechanism
and its coefficient are reusable prior Astra capital, not a new numerical
bound claimed for this branch.

## 5. A convex information-distance form

For a finite observation grid G in [0,T], let p_G be its joint word law.
Let C_m(G) be any finite tree-hierarchy relaxation projected onto the
grid's word table. Include that grid as a path table and leave every OTHER
path table and every unobserved extension table variable. Do not fix other
paths to target statistics: that could exclude the comparison equilibrium
model and invalidate the bound. Every equilibrium grid law is in C_m(G).
Then (8) and data processing give

    sigma >= (4/T) min_{r in C_m(G)} D(p_G || r).          (10)

The right side is an ordinary convex optimization problem, not a new
optimization primitive. Rational Farkas witnesses plus Pinsker recover
(2). Enlarging finite subsystems tightens the admissible polytope. With
fixed G and an exhaustive hierarchy, their intersection is exactly the
projection of E onto G by compactness; KL lower semicontinuity then gives
convergence of the minima to the information distance from that set.

Taking all finite grids and levels is complete for positive detection:
if p is outside E, some finite grid and finite level have a positive
value. This does not make (10) the optimal numerical entropy bound, nor
does it give a finite acceptance certificate when p is in E.

## 6. Acquisition, certification and reuse

The preceding claims are about exact probability laws. A direct finite
acquisition contract for one witness is N independent preparations of
the same stationary source, each observed at its specified grid during
T native time units. With scores in an interval of length L, Hoeffding's
one-sided radius is

    epsilon_N = L sqrt(log(1/alpha)/(2N)).

If the empirical score is fbar, set gamma_cert=max(0,-fbar-epsilon_N).
With probability at least 1-alpha, (2) is valid with gamma_cert, and (9)
is valid for an algebraically reversal-even statistic. Repeated or
data-selected witnesses require independent held-out validation or a
simultaneous confidence construction. A confidence region for p_G can
also be inserted directly into (10), minimizing jointly over admissible
data laws and over r; joint convexity preserves the ordinary convex form
when that confidence region is convex.

A countable enumeration of valid rational dual certificates can be
dovetailed: revisit each witness j at stages m>=j with N_m=2^m independent
validation records and failure budget alpha*2^-j/[m(m+1)], for j>=1.
Every fixed witness is revisited infinitely often and its confidence
radius tends to zero. The budgets sum to at most alpha. This eventually
detects every fixed strict separation, with valid simultaneous coverage.
For a fixed grid, one valid confidence region already covers every
hierarchy level m, so choosing a level after seeing that region requires
no additional level penalty. Choosing grids or repeatedly updating the
data region still requires simultaneous coverage or held-out validation.
There is no source-uniform finite level,
runtime or sample bound. The number of possible words and tree tables
can grow severely; enumeration is a completeness argument, not a practical
default. Existing model fits and established correlation or CP witnesses
should be used when they solve the task more cheaply.

The direct contract consumes N actual stationary preparations and N T
native observation time, plus all observations, storage, arithmetic and
timing precision. If samples instead come from one long trajectory,
dependence needs an acquired or justified mixing bound; stationarity alone
does not make them independent. Known sensor/timing TV error eta costs at
most L eta in the witness margin. Tree branches are mathematical extension
variables, not cloning operations, samples or available hidden-state resets.

Reuse is genuine but limited: acquired word records can test further
statistics measurable on the same grids, with valid simultaneous inference.
They do not supply new interventions, branch experiments, exact short-time
zeros or a prepared hidden simulator.

## 7. Comparison and limits

Time reversal of the observed word law can be perfectly symmetric while
metric-tree compatibility fails. Current Astra N507 supplies such a case
even after a common CP factorization for every reflected-history table.
Its preserved source and internal review are the antecedent; this note
does not claim a new counterexample or reclassify it as external validation.
The complete hierarchy must reject that law at a finite level, but neither
the first rejecting level nor a computational advantage has been found.

Known hidden-network optimization already uses time-symmetric statistics
and can give stronger numerical bounds. The new scientific issue is a
complete convex characterization across UNBOUNDED hidden dimension and
rates, and its implication for finite observable entropy witnesses. The
tree-representation ingredient, KL contraction, additive reversibilization,
Pinsker and convex programming are established machinery. Their use here
does not supply a native physical realization or establish historical
priority of the combined principle.

If hidden parity is unrestricted, many all-even witnesses cease to apply.
For the resolved regenerative event interface, the separate completion
theorem gives the exact robust floor J instead. Thus an entropy claim
needs both the actual acquired law and the physical class of admissible
explanations. A finite-state assumption, known reversal, clock ceiling or
controlled perturbation contract is additional information, not a result
of fitting the same passive record more accurately.
