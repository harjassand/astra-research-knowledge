# Exposed stopping times: a physical-state obstruction and strong predecessors

29 October 2026. Ordinary complementary proof. This obstruction is scoped to
one unknown symmetric flip family (and the proportional subfamily described
below). It is NOT a no-go for all controls of source B, all Bernoulli factories,
or classical random output generation.

## 1. Endpoint exactness does not imply strong preparation with its clock

Let a physical bit start at Y0=0. Every native call lasts t0>0 and flips it
with an unknown probability p in a nonempty open interval I contained in
(0,1). Native flip increments are independent conditional on p. An algorithm
sees endpoint labels, may use arbitrary independent external randomness, and
may decide whether to continue or stop. Its rules do not know p. It must
return the ACTUAL physical bit, not print a different classical sample.

There is no such rule with positive probability of finite termination for
which, simultaneously for every p in I, the stopped bit has a fixed
nondegenerate law rho and is independent of its exposed stopping count N:

    P_p(Y_N=b,N=n)=rho_b P_p(N=n),  b=0,1, every n.        (1)

Proof. Fix n. For every n-bit flip history x, let a_x in [0,1] be the probability
(over external randomness) that the algorithm stops exactly at n after seeing
that history. This coefficient includes the decisions not to stop earlier;
it does not depend on p. Write A_r for the sum of a_x over histories with
r flips. Then

    F_0(p)=P_p(N=n,Y_N=0)=sum_(r even) A_r p^r(1-p)^(n-r),
    F_1(p)=P_p(N=n,Y_N=1)=sum_(r odd)  A_r p^r(1-p)^(n-r).

Equation (1) requires rho_1 F_0=rho_0 F_1 on I, hence as a polynomial identity.
If any A_r is positive, take the smallest such r. Its side has a strictly
positive leading coefficient at order p^r near p=0; the opposite side has
strictly higher order because all its r have the opposite parity. This is
impossible since rho_0,rho_1>0. Therefore every A_r is zero. As this holds for
every finite n, the algorithm never terminates with positive probability. QED.

The use of p near zero is a polynomial-identity argument, not an additional
physical assumption that the device actually reaches zero flip probability.
A parameter-independent rule valid on ANY interval forces that identity.

## 2. Padding and finite calibration do not silently repair this theorem

The same proof permits nonnegative random physical padding that preserves Y.
For each fixed deadline t, at most floor(t/t0) native calls can have occurred.
The probabilities of {completion time<=t,Y=b} are finite sums of the same
nonnegative path terms, now with varying n. Their first nonzero power of p
again has parity b. Thus a nondegenerate stopped bit cannot be independent of
its full exposed completion time by adding such padding. This conclusion
assumes endpoint-only native information and a genuine positive lower bound
t0 on time per native call. Arbitrarily many zero-time calls are not allowed.

Finite parameter-independent calibration does not make p known exactly. If
its full finite record D is retained, every particular positive-probability
record has positive likelihood throughout I. Conditional on D, future native
increments are still Bernoulli(p), and the selected stopping algorithm is a
fixed parameter-independent rule. Consequently it cannot satisfy (1)
conditional on every D for all p. Finite-confidence approximate preparation is
possible and is constructed in the companion note.

The leading-order argument extends to a finite collection of controlled
native kernels with flip probabilities c_j p, c_j>0, under arbitrary
history-dependent operation choices: every finite path with r flips still
has a positive leading coefficient at order p^r. This includes source B's
modes 0 and 1 with p=p0 and c=(1,3). It does NOT apply to the full source-B
menu, since modes 2 and 3 have nonzero offsets in this parameterization.

The theorem does not obstruct printing an independent fair bit. It concerns
preparing the actual physical state. It also does not obstruct an exact target
endpoint with time discarded: independently choose the target and stop on
first hitting it, as in the companion construction. That target sample is
usually correlated with its completion time.

## 3. Primary predecessors already provide substantial leverage

### Unknown-chain exact sampling

Lovasz and Winkler, *Exact Mixing in an Unknown Markov Chain*, Electronic
Journal of Combinatorics 2(1), R15 (1995), DOI 10.37236/1209:
https://www.combinatorics.org/ojs/index.php/eljc/article/view/v2i1r15

The primary abstract gives an exact stopping rule for an unknown irreducible
finite chain, with expected stopping bounded polynomially in maximum mean
hitting time. This is a serious exact alternative to waiting for asymptotic
mixing. The abstract was read; the linked PDF viewer was available but one
mirror blocked a full-text fetch. The present explicit binary hitting proof
is self-contained and does not import unseen lemmas from that paper.

### Stationary versus strong stationary times

Aldous and Fill, *Reversible Markov Chains and Random Walks on Graphs*,
Chapter 9.1, author-hosted manuscript:
https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch9.S1.html

Read definitions (9.1)--(9.2), Theorem 9.1 and the target-distribution discussion
in Section 9.1.2. A strong stationary time requires independence of terminal
state and stopping time, whereas ordinary stationary stopping only specifies
the terminal marginal. Their filling construction addresses exact target
sampling when the required chain information is supplied. The distinction is
exactly why a terminal-only certificate does not automatically cover exposed
clocks or apparatus histories.

### Interruptibility with an unknown chain

Crank and Fill, *Interruptible exact sampling in the passive case*,
arXiv:math/0202136:
https://www.ams.jhu.edu/~fill/papers/passive.pdf
https://arxiv.org/abs/math/0202136

Read introduction and Section 3.2, especially the full record/interruptibility
definition. They prove general single-trajectory impossibility results for
interruptible exact stationary sampling from unknown finite chains, and give
positive algorithms when enough synchronized copies are available. Their
returned sample need not be the chain's actual state. Our short special proof
uses the stronger actual-state requirement even when the stationary target is
known to be uniform; it is not claimed as a new general sampling obstruction.

### Bernoulli factories

Nacu and Peres, *Fast simulation of new coins from old*, Annals of Applied
Probability 15 (2005), 93--115, DOI 10.1214/105051604000000549:
https://arxiv.org/pdf/math/0309222

Read introduction and Theorems 1--2. Real-analytic functions from a closed
parameter interval inside (0,1) to (0,1) admit coin factories with exponential
runtime tails. Rational corrections such as a strictly interior reciprocal
thinning probability therefore have powerful established machinery. The
method presumes conditional iid input coins and pays their random count.
Producing a classical corrected coin does not by itself set a physical bit,
restore the disturbed device or erase the factory's stopping transcript.

### Full-path likelihood and sensitivity

Dupuis, Katsoulakis, Pantazis and Plechac, *Path-space information bounds for
uncertainty quantification and sensitivity analysis of stochastic dynamics*,
SIAM/ASA Journal on Uncertainty Quantification 4 (2016):
https://arxiv.org/abs/1503.05136
https://doi.org/10.1137/15M1025645

The primary abstract and publisher description identify established
path-relative-entropy bounds; the supplement gathers standard discrete/continuous
Markov path formulas. The companion's elementary binary hazard likelihood
calculation is written out directly. No claim of inventing KL propagation or
sensitivity analysis is made.

## 4. Research implication

A claim that arbitrary frozen kinetics prevent exact useful control is false
at an ordinary stopping interface. A claim that a correct terminal distribution
also prepares its complete clock/history record is likewise false. The strong
ordinary comparator should be stated as exact variable-time physical endpoint
control, or as a calibrated positive marked model with an explicit finite-record
error. Both are already constructive here. Neither requires pretending that
retained bit count pays acquisition or that hidden equilibrium was prepared.
