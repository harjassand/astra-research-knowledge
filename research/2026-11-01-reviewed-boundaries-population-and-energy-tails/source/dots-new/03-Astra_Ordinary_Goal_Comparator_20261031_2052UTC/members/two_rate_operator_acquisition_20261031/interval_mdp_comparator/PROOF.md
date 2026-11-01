# An ordinary goal-directed baseline defeats the previous sufficient ledger

This is a **separate comparator**, not a replacement theorem or a new learning
algorithm. All earlier reviewed sources and archives remain unchanged. The
current finite-state example does not establish a consequential advantage of
our operator certificate. This comparator is goal-specific; it does not replace
the earlier uniform compatible-goal/operator certificate.

## 1. Task and actual information interface

The fixed public task is the pinned 4096-state, two-action, 24-step source,
initially uniform on its public initial support, with terminal reward the public
indicator b of G. Initial support is disjoint from G. Source access returns
sampled destination labels for named current labels/actions; block membership
is an acquired retained lookup. The learner is not given hidden groups, edge
lists, a useful decomposition, transition probabilities, or optimal values.
The same ordinary coarse-count community proposal acquires four blocks. All
pilot and incoming row-count batches used below were taken after that proposal.
The reused counts are exact recorded integers, not new observations. Direct
source implementation access appears only in the **source-side adapter audit**,
not in the planner or hazard estimator.

The deployed policy is an ordinary 24-by-4 action table with a 4096-entry block
lookup. It can run in an explicit-state simulator that returns the next label;
there is no claim of a physical sensor or hidden-state implementation. Each
step costs a source transition, label update, block lookup and policy lookup.

## 2. Confidence radius and fixed prefixes

For N iid Bernoulli trials and count c, put

    v(c)=c(N-c)/(N(N-1)),
    R(c,N,K)=min(1, sqrt_up(2 v(c) K/N) + 7K/[3(N-1)]).

`sqrt_up` is the retained exact dyadic upper square root with 40 fractional bits.
Maurer–Pontil (2009), Theorem 4, implies the one-sided upper/lower bounds at
failure probability zeta whenever K >= log(2/zeta). For two-sided receiving use
K >= log(4/zeta). We use K=(7/10) ceil(log2 x) >= ln x; ln 2 < 7/10 follows,
for example, from the positive Taylor lower sum for exp(7/10)>2.

Six possible acquisition prefixes are budgeted before data, though this saved
trace stops after the third. At prefix t the row half-batch size is 512*2^t,
with the fixed replicate count prescribed by the original confidence schedule.
Each action and microscopic row has the same total N, including the pilot and
both halves of all previous replicates. The three observed totals are 13312,
39936, 93184. Optional stopping among these fixed prefixes is handled by the
six-event union bound, not by pretending the selected prefix was fixed in
advance. Unequal or outcome-dependent unbudgeted row sample counts are outside
this theorem. A stored file cannot authenticate iid sampling or timing.

## 3. Standard interval-MDP candidate generation

At every fixed prefix, simultaneous per-row/action/block confidence intervals
are obtained with K=(7/10)ceil(log2(4 m n r * 6/(delta/2))). Take each block's
minimum lower endpoint and maximum upper endpoint over microscopic rows. Add
the source-transport reserve eta=10^-9 outward before clipping to [0,1].
Intersect a row's intervals with the probability simplex.

For an arbitrary value vector, its maximum/minimum over this interval simplex
is computed by filling probability from the lower endpoints in descending/
ascending value order. An exchange argument proves optimality: mass assigned
to a lower-value unsaturated coordinate while a better coordinate has capacity
can be moved to improve the objective. Finite-horizon optimistic and pessimistic
Bellman recurrences then give an upper bound on every microscopic/history
policy and a lower bound for the chosen pessimistic block-Markov table. Induct
on remaining time, using the interval inclusion of the true row and convexity
for randomized/history-dependent action selection. No inherited spectral
contraction or posterior block distribution is assumed.

This is conventional bounded-parameter MDP reasoning, not a new planner. It
alone is weaker on this trace: after fresh policy evaluation its final regret
bound is about .069282921, above .0565. It is retained as a genuine failed
comparison, not silently removed.

## 4. Maximum-hazard certificate: no unnecessary row union

For every microscopic state i outside G and action a, let p_(i,a) be the
probability of entering G in one step under the row-count observation law.
Let p_max be their maximum, and fix a deterministic maximizing pair (i*,a*)
before observations. Write C_max=max_(i outside G,a) C_(i,a). Define

    U_N(c)=1                           if 2c>N,
           min(1,c/N+R(c,N,K))         otherwise.

This function is monotone in integer c: c(N-c) is nondecreasing up to N/2,
upper square-root rounding preserves order, and the remaining branch is 1.
Thus U_N(C_max) >= U_N(C_(i*,a*)). The *single fixed maximizing row's*
empirical-Bernstein event gives p_max <= U_N(C_max). No union over n or m is
needed. This does not produce simultaneous individual row intervals, and it
does not permit selecting a different goal after seeing the samples. Across
six prefixes allocate delta/2 total, hence K=(7/10)ceil(log2(2*6/(delta/2)))=21/2.
Different rows need not be mutually independent for this maximum argument;
each fixed row's N samples must satisfy the iid hypothesis.

Let h=min(1,U_N(C_max)+eta) bound the *target* source's maximum entry hazard.
For every microscopic/history-dependent randomized policy, conditional on no
previous hit and any positive-probability history, the next hit probability is
at most h. Therefore P(no hit by L)>= (1-h)^L, by induction without dividing by
any particular rare history's probability. Terminal membership implies some
hit, so every allowed policy has value at most H=1-(1-h)^L. This upper bound
allows more information and control than the earlier block-history theorem;
it is a comparator upper bound, not an implemented microscopic controller.

## 5. Fresh chosen-policy evaluation and receiving

At each of the three attempts the interval table is fixed before an independent
250000-episode batch. Each episode really executes all 24 ordinary forward
transitions in the vectorized source adapter. There are 18,000,000 simulated
transitions, not an endpoint binomial shortcut. Endpoint bits are retained and
counted. With delta/6 per batch, all three policy-value lower bounds hold with
failure <=delta/2. The proposed policy may depend on past data; conditioning
on those data leaves the fresh evaluation argument valid.

On the joint hazard/evaluation event (total failure <=delta), regret of the
chosen table against *all* microscopic/history policies is <=max(0,H-V_lower).
The reported method is this fixed hazard/evaluation combination. It does not
take an unbudgeted minimum with the separate interval certificate. The
probability statement is false-admission control under the sampling protocol,
not posterior confidence conditional on PASS or a claim that deterministic
mock seeds prove independence.

The receiver binds the external public-task digest, horizon, alphabet,
confidence and requested regret; reproduces count coverage, equal N, exact
radii, endpoint count/byte/hash, arithmetic and cost totals; and the full check
independently reruns the candidate generator and all 18 million transitions
without modifying originals. These are scientific typed-API checks, not a
provenance attestation or unrestricted hostile-JSON parser.

## 6. Numerical source transport is paid, not silently ignored

The historical aggregate row-count simulator passed normalized binary64
probability vectors to a multinomial sampler. The new forward adapter uses
integer branch probabilities (95998,4000,1,1)/100000, with uniform degree-16,
1024-state group, and 2048-state reset selections. These laws must not simply
be asserted identical.

`check_source_transport.py` captures all 8192 historical row probability
arguments from the **unchanged pinned** source implementation, treating the
last multinomial probability as the remaining mass. It converts binary64
values to exact rationals and compares them with exact target block masses
computed source-side from the integer-branch law. Every L1 difference is
<=eta; the observed maximum is approximately 1.903e-16. This exact finite audit
justifies the fixed eta reserve for this fixture. The policy/estimator never
receives the private wiring. It does not establish correctness of a physical
source, floating-point PRNG law, or independence: ideal iid argument-law
semantics remain explicit premises for both simulated interfaces. The
historical scalar-alias overflow in this audit was repaired by conversion to
Python integers; failed bytes are preserved, not treated as a passing audit.

## 7. Results, costs, and limitations

At prefixes 0/1/2 the goal-hazard regret bounds are approximately
.1296167091, .0763331303, .0564322326. Only prefix 2 passes the externally
requested .0565. The last value is smaller than the prior reviewed block-history
bound .0565053039. Its prospective ledger is:

- 31,588,352 original column/coarse proposal calls (even unneeded columns kept);
- 763,363,328 pilot/incoming row calls, including both failed prefixes;
- 18,000,000 actually simulated fresh evaluation transitions;
- total **812,951,680** calls versus the earlier **3,298,951,680** sufficient
  acquisition ledger, with no outgoing microstate batches or spectral probes.

This is a prospective algorithm comparison on retained data. The original
experiment still paid the full 3.299 billion logical calls and its prior norm
work; no refund is claimed. Old aggregate count generation represented billions
of logical calls, not individually executed billions. Current fresh evaluations
and their replay do individually simulate 18 million transitions each.

Each prefix's two-sided interval DP charges 2 L m r^2=1536 scalar products plus
sorting/additions/comparisons and exact rational bit growth. Three attempts
are retained. Stored outcome bits total 93750 bytes; policies, block map, public
initial/reward interface, retained count files, exact certificate JSON and
source-side simulator memory are additional, not a 12-byte complete machine.
The replay JSON records storage and actual maximum exact rational component
bits; it is not a unit-cost-real arithmetic claim. The source has an explicit
O(n*degree) private simulator state, separately from the learner's lookup/table.

No important real application, new sampling exponent, universal planner,
historical novelty, or practical advantage is demonstrated. Goal selection,
one-step reachability structure and the broad bound on *ever* hitting G make
this baseline useful here. Other goals may make it vacuous. That is not grounds
to redesign the toy to evade it. The earlier certificates remain valid capital
for their wider task language; this example does not establish their necessity.

## Primary sources and exact scope of attribution

- Maurer–Pontil (2009), Theorem 4, empirical Bernstein bound:
  https://arxiv.org/pdf/0907.3740 . The radius is theirs; the elementary
  monotone-maximum specialization is proved above, without a novelty claim.
- Givan–Leach–Dean (2000), *Bounded-parameter Markov Decision Processes*:
  https://engineering.purdue.edu/~givan/papers/bmdp99.pdf . The primary paper
  explicitly treats aggregate-state interval transitions and optimistic/
  pessimistic planning. Our finite-horizon proof is supplied above; we do not
  claim its interval planner is new. The Brown mirror returned 404; no bypass.
