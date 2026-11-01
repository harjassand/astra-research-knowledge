# Prospective jointly tagged acquisition: same observations, stronger retention

New, not yet independently reviewed. Earlier accepted sources/archives are
unchanged. This theorem isolates the coherent NEW joint sampler; it does not
silently reinterpret missing historical source-row tags or the older separately
normalized row-block/pooled fixture argument laws.

## T1. Interface, acquired partition, and outgoing event

Unknown stochastic actions A_a on n named states admit ordinary iid forward
calls (chosen source row, action, destination label). Discovery counts acquire
a partition of r blocks by the ordinary retained threshold-community proposal.
No correctness of the heuristic is assumed: the fixed partition is validated
on fresh observations. The initial law is explicitly uniform within blocks.
Let Z lift block functions, W average uniformly within each acquired block,
P=ZW, Q=I-P, H=I/n. Source sampling/provenance/independence and the fixed,
nonanticipating validation schedule are external premises, not file assertions.

A column confidence event acquired from old ordinary-law column samples bounds
max_j sum_i A_a[i,j]<=B for every action and column. Therefore the true pooled
next-state law p_g=(WA_a)[g,:] has max_j p_g(j)<=B/|g|, even for a partition
chosen after this column sample. Put kappa=B n/|g|.

For N iid pooled destinations with counts C_i, the retained reviewed statistic

 U = n/[N(N-1)] * [sum_i(C_i^2-C_i)
                    -sum_blocks h (C_h^2-C_h)/|h|]

has expectation v=n||p_g Q||_2^2 and variance
Var(U)<=4 kappa v/N + 2 kappa n/[N(N-1)]. This follows from the second-order
U-statistic variance identity, detailed in the dependency
`QUADRATIC_LEAKAGE_VALIDATION.md`, Q1--Q3; the exact code is
`quadratic_leakage.py`. For a=4 kappa/N, b=2 kappa n/[N(N-1)], base failure q,
Chebyshev and the quadratic inequality imply, with probability >=1-q,

 v <= max(0,U)+a/(2q)
      +sqrt((a/q)max(0,U)+a^2/(4q^2)+b/q).

The actual square root is rounded outward. An odd number of independent fixed
replicates followed by the median reduces failure to the explicitly computed
binomial tail; every replicate and failed round is paid. Taking max over the
rows/actions gives e>=max_(a,g)||WA_aQ[g,:]||_(H^-1). Fine pooled BLOCK counts
from the same observations produce stochastic B_a and simultaneous empirical-
Bernstein row L1 bound d. Correlation with U requires only a union bound, not
independent confidence events. No complement-norm probes are taken.

## T2. Source-row metadata costs no additional transition

A pooled draw is implemented by choosing a row uniformly in its source block,
then making an ordinary forward call. That chosen row is available information.
The method retains row->destination-BLOCK counts as well as the pooled
microscopic destination count. Both arise from the SAME destinations. The
extra sufficient statistics are O(m n r) counters; claiming a competitor must
buy new incoming-only samples would be unfair. The current file retains every
batch's row totals and joint block counts as well, for replay/storage costs.

Let N_(i,a) be a row's cumulative sampled count at a fixed prefix. All row
choices and hence N_(i,a) are drawn independently of outcomes. Conditional on
these counts and prior discovery, each fixed row has N_(i,a) iid outcomes.
Cross-row independence is unnecessary for the next argument. The algorithm
refuses if N_min=min_(i,a)N_(i,a)<2. Outcome-dependent row sampling/stopping is
not justified by this conditional argument.

## T3. Polynomial incoming scalar witness, with random unequal row counts

Write p_(i,a) for the true next-BLOCK law and pbar_(g,a) for its uniform block
average. We need only the scalar

 c=max_(a,i in g) TV(p_(i,a),pbar_(g,a)),

not simultaneous fine estimates of all row distributions. From empirical rows
hat p_(i,a), acquired coarse B_a, and N_min, compute

 tau=max_(a,i in g) TV(hat p_(i,a),B_a[g,:]),
 vB=max_(a,g) [bmax(1-bmax) if bmax>=1/2, else 1/4],
 vhat=min(1/4,vB+tau).

For every subset S of blocks, B_g(S)(1-B_g(S))<=v(B_g); the largest coordinate
is either inside or outside S. The function x(1-x) is 1-Lipschitz on [0,1],
so every empirical subset variance hat p_i(S)(1-hat p_i(S))<=vhat. Computing
tau and vhat costs O(m n r), NOT enumeration of 2^r subsets.

Conditional on the acquired partition and all outcome-independent row counts,
fix ONE true maximizing (a*,i*,g*,S*) for p_i(S)-pbar_g(S), with a fixed tie rule.
It exists and attains c. It is an analysis witness, never an oracle input.
Maurer--Pontil Theorem 4 for this fixed row/subset, failure zeta, gives

 p_i*(S*) <= hat p_i*(S*)
 +sqrt(2 K hat p_i*(S*)(1-hat p_i*(S*))/(N_i*-1))
 +7 K/[3(N_i*-1)], with K>=ln(2/zeta).

Use N_min<=N_i*, the variance envelope, and the simultaneous fine event
TV(pbar_g,B_g)<=d/2. Therefore

 c<=min(1,tau+sqrt_up(2 K vhat/(N_min-1))
                  +7 K/[3(N_min-1)]+d/2).                 (T3)

No union over rows/actions/subsets is needed for this scalar maximum. This is
not a claim that high-dimensional distribution estimation is dimension-free:
the observed maximum tau itself becomes large with sparse/high-rank data.
The witness is fixed before outcomes conditional on row counts, so neither
unknown maximizing row nor shared pooled/tagged data invalidates the argument.
There is no assertion for an adaptively chosen partition from this same batch.

## T4. Uniform future task certificate

For q=Qq, stochasticity of A_a,P gives
||QA_aq||_infty<=||A_aq||_infty+||PA_aq||_infty
              <=(1+e)||q||_infty,
using ||q||_H<=||q||_infty. Also, for 0<=f<=1,
||QA_a P f||_infty<=c. Set z_0=0, z_(j+1)=min(1,c+(1+e)z_j).
A backward induction with separately patched block-history child continuations
has residual at most z_j, and block-average error increases by at most
d/2+e z_j. Thus every [0,1] complete-record payoff, every block-observation
history controller, and a block-uniform initial law satisfy

 |true expectation-coarse expectation| <= E_L=L d/2+e sum_(j<L)z_j. (T4)

Equivalently the complete observed-record laws have TV<=E_L. Terminal leaf
payoffs are constant on the leaf's current block; different histories can have
different payoffs. A patched residual is still in range(Q), and its sup norm
is the maximum child residual; no branch-count factor or rare-history division
is concealed. Randomized controllers follow by convexity. Microscopic-state
policies are NOT covered. Fixed block->action table words are a special case;
row selection within blocks preserves the same c,e,d, useful for population
planning. Arbitrary N-fold transcript replacement still amplifies TV and is
not claimed. The population corollary uses weaker aggregate tasks explicitly.

## T5. Confidence and exact fixture join

The conservative schedule reserves: column delta/8; outgoing across all six
possible rounds 3delta/28; fine rows 3delta/14; incoming six scalar witnesses
delta/2. Total 53delta/56<delta. Only three rounds were actually generated. All
replicates within/outside selected prefixes are received and paid; a first-
admitted-prefix prospective comparison does not refund actual later work.
Independent fixed row choices precede outcomes; iid PRNG ideality is external.

The new sampler uses EXACTLY the original ordinary `_row_counts` ideal
multinomial argument law: first three binary64 branch probabilities, fourth
remaining mass. Dyadic group/neighbor probabilities and integer destination
labels join the statistics exactly. Old column/coarse evidence used this same
law; it supplies previously paid partition discovery/column validation. The
old separately normalized incoming/pooled outputs are NOT used as fresh row
or pooled evidence. `GENERATIVE_JOIN.md` and `check_joint_law.py` give the actual
source-law proof and exhaustive joint-law check; full regeneration reproduces
100,186,909 actually generated macro/reset labels and every saved count.

Current errors: .28283061844, .04719440917, .01097391423. The .05 request first
passes at prefix 1 (prospective 615,588,352 calls); .02 first passes prefix 2
(2,535,588,352); .01 refuses. Actual new experiment calls are 2,504,000,000,
in addition to the already performed 3,298,951,680 old acquisition calls and
old norm work. No incoming-only or norm-probe calls are newly required. Extra
row metadata uses 40,960 streaming counters (327,680 nominal uint64 bytes,
excluding Python overhead); the retained compressed joint transcript is
3,830,533 bytes. Exact arithmetic/serialized certificates are additional costs.

The algebra is elementary projection/TV theory plus standard empirical
Bernstein and collision-statistic confidence. Prior formulas and ordinary
planners are explicitly credited, not relabelled as new methods. The useful
acquisition ingredient is made available to every comparator. No historical
novelty or practical advantage is asserted. A rare exceptional microscopic
row can force c near 1 even if an L2 method succeeds; this is a portfolio
certificate, not a universal robust-representation theorem.

Primary sources: Maurer--Pontil (2009), Theorem 4,
https://arxiv.org/pdf/0907.3740 ; ordinary collision/L2 testing prior
Diakonikolas et al. (2016), https://arxiv.org/pdf/1611.03579 .
