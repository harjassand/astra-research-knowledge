# Controller complexity and the cost of real experiments

29 October 2026. Root construction, sixth continuation. Mathematical
research unit; no device, historical-priority or major-discovery claim.
All preceding constructions remain unchanged.

## 1. Question and the predecessor that changed it

Can the number of real experiments needed to discover a useful
intervention be governed by controller complexity, even when the
physical system has arbitrary hidden memory?

A strong upper route already exists. Contextual Krichevsky--Trofimov
(KT) prediction is a special case of Cover--Ordentlich's universal
portfolios with side information. More decisively, Peshkin--Mukherjee
(COLT 2001), section 5.2, already turns minimax logarithmic-loss regret
into trajectory likelihood-ratio bounds and polynomial-horizon
reusable policy evaluation. That source invalidated the proposed
novelty of this round's initial coding-to-experiments bridge.

The retained construction makes the ordinary route explicit under
Astra's actual experimental, randomness and conditional-start
interfaces, then proves a matching worst-case **learning** lower
bound that allows fully adaptive per-device calibration. A lower
bound on domination alone would not answer the learning question.
For fixed finite-context randomized controllers with d probability
parameters, the worst-case experimental burden is of order T^(d/2),
up to logarithms and dimension-dependent constants. Latent dimension
and hidden mixing gaps do not enter. The lower construction's
historical novelty remains unresolved.

The consequential target is intervention discovery when a microscopic
description is unattainable. The result gives an existing route for
small controller classes and identifies a cost that an additional
operation must overcome in the unrestricted plant class. It does not
yet supply that new operation or establish a major new capability.

## 2. Actual interface

There are A>=2 actual operations and T operation calls per episode.
Before each call a supplied deterministic observable-memory map
computes c_t in {1,...,S} from the recorded past. It need not be a
sufficient physical state. The target class has all randomized rows
pi(a|c), with fresh sampling at each visit and d=S(A-1) real parameters.
The plant is an arbitrary causal kernel from its past and the actual
action to the next observation. Hidden memory, nonlinearities and
non-Markov observations are allowed. No reversibility, equilibrium,
finite predictive rank or hidden reset within an episode is assumed.

Each episode has the same warranted initial law, independently of
the other episodes. The statement may be conditioned on a fixed old
record and fixed unknown device parameter if this same independence
and initial-law contract actually holds conditionally. Arbitrary
repetition on a frozen specimen does not supply it. Preparation and
waiting costs are paid.

A specified recorded score R(h) lies in [0,1]. Finitely many declared
scores can be covered by a union bound. An arbitrary score invented
after inspecting the bank is not automatically covered.

Plant kernels conditional on the action must be common in calibration
and deployment. Equal-duration slots are one supplier. Variable
durations can instead be included in the common kernel and transcript,
but T then counts operations, not fixed physical time. Selector timing
that changes the specimen must be represented explicitly.

The service transcript includes actions, observations, count/context
updates and common-kernel apparatus outputs used in the score. It
does not identify literal private random keys across different
selectors. These keys have real generation, retention and erasure
costs, but the theorem concerns the declared marginal transcript.
If the requested joint law includes raw keys, the action-only
likelihood ratio below can fail. No unrecorded specimen-dependent
selection variable is permitted.

## 3. Executable universal experimental controller: established route

Reset integer counters n_ca to zero at each episode. In context c,
execute action a with probability

    q_t(a|h_<t) = (2 n_ca+1)/(2 n_c+A),  n_c=sum_a n_ca,

then increment its counter. These are rational probabilities, not
an infinite-precision Dirichlet draw. Finite-bit rejection sampling
of a finite integer distribution is one exact supplier. Its random
bit cost and variable selector time must be charged or isolated by
a real timing interface.

For a complete transcript define

    L_pi(h) = product_(c,a) pi(a|c)^n_ca,
    Q_sel(h) = product_c [Gamma(A/2)/Gamma(n_c+A/2)
                         product_a Gamma(n_ca+1/2)/Gamma(1/2)].

The chronological chain rule gives

    dP_pi/dP_Q(h) = W_pi(h) = L_pi(h)/Q_sel(h).             (1)

The actual causal plant factors cancel. This needs neither a Markov
observation model nor two futures from one hidden state. Counts
suffice to evaluate (1); this does not make the plant exchangeable.

The contextual KT bound inherited from universal coding/portfolios is

    W_pi(h) <= product_c 2(n_c+1)^((A-1)/2)
             <= C_T := 2^S(1+T/S)^(d/2).                 (2)

The last step is arithmetic-geometric mean. A path-dependent smaller
bound does not automatically justify replacing C_T in confidence
statements. For A=2,S=1, a constant action word has endpoint ratio
4^T/binom(2T,T), asymptotic to sqrt(pi T).

Since E_Q W_pi=1 and R is bounded,

    E_Q[(W_pi R)^2] <= C_T E_Q[W_pi R^2] <= C_T.           (3)

The variance bound is C_T, not C_T^2. This is ordinary importance
sampling, already present in the predecessor literature.

## 4. Finite-bank global learning, including selection on the bank

Take N independent episodes under Q and form

    Vhat(pi) = (1/N) sum_j W_pi(h_j) R(h_j).

For a grid G of M policies, let x=log(2M/beta). Bernstein's inequality
and a union bound give, with probability at least 1-beta,

    max_(pi in G) |Vhat(pi)-V(pi)| <= r_N,
    r_N = sqrt(2 C_T x/N)+2 C_T x/(3N).                   (4)

The linear term is a conservative valid inversion. This is a
simultaneous event, so the same bank can choose the policy. It is not
posterior validity for every realized transcript.

Use the row-simplex grid with denominator L. It has

    M = binom(L+A-1,A-1)^S.

Rounding down the first A-1 coordinates and putting the remainder
in the last gives a grid point pi' with
max_c TV(pi(.|c),pi'(.|c)) <= (A-1)/L. Couple the two controllers
until their first different action. Before then histories, contexts
and common conditional plant kernels agree, so

    TV(P_pi,P_pi') <= T(A-1)/L.                           (5)

If pihat maximizes the grid estimate, or is within gamma of its
maximum, the confidence event implies

    sup_pi V(pi)-V(pihat) <= 2 r_N+T(A-1)/L+gamma.         (6)

For 0<epsilon<=1, L>=4T(A-1)/epsilon and
N>=32 C_T log(2M/beta)/epsilon^2 suffice for epsilon regret when
gamma=0. For fixed A,S the resulting sample bound is

    N = O_(A,S)(T^(d/2)/epsilon^2
                [d log(T/epsilon)+log(1/beta)]).          (7)

The cost is N preparations, NT native calls, actual readings,
controller resets, random selection and offline computation.
Searching M candidates can be expensive: (7) is an experimental
bound, not efficient global optimization in all dimensions.

The fair comparator is stronger than uniform actions. An episode
mixture assigning half its mass to Q and half uniformly to the A^S
deterministic stationary controllers has domination at most
2 min(C_T,A^S) for a deterministic target and 2 C_T for an arbitrary
randomized target. The branch is an apparatus record; comparison
again concerns the stated marginal service. Randomized policies can
outperform all deterministic members of the same context class.

## 5. Matching lower bound for learning, not only for reweighting

This is root's proposed addition to the local research unit. Its
historical novelty has not been established. The proof uses the
standard adaptive change-of-measure method for finite-armed trials.

### Theorem

Fix A>=2,S>=1,d=S(A-1),T=Sn. For all sufficiently large n depending
only on A,S, there is a finite causal operation model with a warranted
episode reset and one terminal binary readout such that every
adaptive experimental procedure returning an epsilon-optimal target
policy with probability at least 1-beta on every model needs

    N >= c_(A,S) n^(d/2) epsilon^(-2)
                      log[1/(4 beta(1-beta))]             (8)

episodes, for 0<epsilon<=1/32 and 0<beta<=1/8.

The learner may use arbitrary history-dependent experimental actions,
force exact action counts, adapt across episodes, know the whole
hard family and use unlimited offline computation. Ordinary per-device
calibration is included. The claim concerns a worst-case family, not
every system or every score.

### Disjoint response regions

Schedule each context for n calls in S known blocks, with no informative
observation before the terminal readout. Track counts K_ca for
a=1,...,A-1; the last count follows from their sum.

Let r=ceil(sqrt(d n)). In each of the d tracked coordinates choose
integer centers in [ceil(n/(4A)),floor(n/(2A))], spaced by 2r+1.
For large n there are at least c sqrt(n) centers per coordinate,
where c>0 depends only on A,S. Every combination of centers defines
a box B_b of count vectors within r of its center in every coordinate.
These boxes are disjoint. Their number K satisfies

    K >= c'_(A,S) n^(d/2).

For box b set pi_b(a|c)=m_ca/n on the tracked coordinates and assign
the remainder to action A. The row probabilities are valid because
the tracked means sum to less than n/2. Under pi_b, each tracked
count has its specified mean and variance at most n/4. A union bound
and Chebyshev give

    P_pi_b(B_b) >= 1-d n/(4 r^2) >= 3/4.                 (9)

No independence of multinomial coordinates is needed for this bound.

### Finite executable family

The device has a fixed hidden parameter b in {1,...,K}. Native actions
increment the appropriate finite counters. The context schedule and
call counter are finite too. At the end of T calls a fresh binary
readout has mean

    1/2+Delta * 1{count vector belongs to B_b}.

Null device b=0 returns Bernoulli(1/2) on every word. A supplied reset
returns counters to zero and leaves b intact. Only reset, the action
menu and the terminal read are available. No extra probe or early
readout revealing b is granted. The terminal noise is independent
across trials. This is a finite physical-operation model, not a
laboratory-material claim.

On device b,

    V_b(pi)=1/2+Delta P_pi(B_b).

The best target value is at least 1/2+3Delta/4 by (9). Put
Delta=8epsilon<=1/4. An epsilon-optimal returned policy has
P_pi(B_b)>=5/8. No policy can put probability greater than 1/2 on
two disjoint boxes, so successful learning identifies b. This also
holds if the learner returns an episode-level mixture of target
policies, whose box probabilities still sum to at most one.

### Adaptive information bound

Let E_b mean that the returned policy identifies b by this rule.
The E_b are disjoint. Under the null law P_0, at least K/2 indices
have P_0(E_b)<=2/K<=1/2, taking n large enough that K>=4. Under the
alternative, success requires P_b(E_b)>=1-beta.

Let N_b count experimental episodes whose actual count vector lies
in B_b. The strongest learner can observe and force these counts.
Every episode hits at most one box. Chronological KL chain rule
cancels the learner's own action choices, including adaptive ones:

    KL(P_0 || P_b)
       = E_0 N_b * kl(1/2 || 1/2+Delta)
       <= (8/3) Delta^2 E_0 N_b.                         (10)

The last step uses -log(1-x)<=x/(1-x) with x=4Delta^2<=1/4.
Data processing to E_b for the selected K/2 indices gives

    KL(P_0 || P_b)
       >= kl(1/2 || 1-beta)
       = (1/2) log[1/(4 beta(1-beta))].                   (11)

Summing and using sum_b N_b<=N yields

    N >= (3K/(32 Delta^2)) log[1/(4 beta(1-beta))]
      = (3K/(2048 epsilon^2)) log[1/(4 beta(1-beta))].     (12)

This proves (8). Equations (7) and (8) match the horizon exponent
d/2 for fixed A,S up to the upper logarithm. Unlike a minimax
portfolio ratio, (8) is about learning a useful intervention from
noisy observations, and includes experimental controllers outside
the target class. Constants are not the destination.

## 6. Meaning and limitations of the exponent

For one repeated binary row, changing its probability by order
T^(-1/2) moves its mean action count by one sampling fluctuation.
An arbitrary device can attach different terminal responses to
order sqrt(T) separated count regions. With d row coordinates there
are order T^(d/2) such regions. The known KT controller covers them
in one experimental distribution. The hard device makes them an
identification problem that adaptive calibration cannot uniformly
avoid without an extra operation or additional structure.

The fixed controller can still be inadequate. Enlarging its context
architecture increases d and can make the bound useless. A small
parameter count alone is insufficient for arbitrary policy families:
one real number can encode exponentially many unrelated action words.
The row-simplex structure, evaluation complexity and physical records
must remain attached to the claim.

A fixed finite library of context architectures can be covered by
mixing their experimental laws with declared positive masses. Each
inherits its bound divided by its mixture mass, and a union budget
covers selection. This is a conventional mixture/model-selection
extension, not a learned proof that a context captures hidden state.
An infinite library needs an actual computable mixture supplier.

## 7. Conditional deployment and physical errors

Deployment chosen after the bank requires the same initial-law and
kernel contract conditional on retained calibration and old records.
A freshly prepared independent specimen is one supplier. Reusing
the last hidden state is not justified by (6). A fixed unknown device
parameter is allowed: prove coverage for each fixed parameter under
its conditional sampling law. Coverage is frequentist, not posterior
validity for every realized bank.

If target execution differs from its specified conditional kernel
by at most delta in TV per call, coupling adds at most T delta to
bounded-score error. For the acquisition bank, a TV error zeta in
the behavior transcript law can shift a weighted score by as much
as C_T zeta. Actual selector probabilities and common actual kernels
should therefore be used whenever warranted.

This theorem supplies neither actuators, isolation, timing, sensing,
score evaluation nor reset. An ordinary controller with the same
interfaces can use the same algorithm. There is no thermodynamic
saving or practical speedup claim. Unmeasured interventions need
actual acquisition; equilibrium weights do not specify their kinetics.

## 8. Useful failures

* Exposed key: record U~Uniform[0,1] and take a=1{U<p}. For different
  p,q there are regions of (U,a) that one law assigns zero and the
  other positive mass. The marginal action ratio does not compare
  the literal joint records. Actions/counts differ from raw keys.
* Frozen repetition: A=1 and a fixed hidden Bernoulli bit read on
  every repeat. Repeated reads do not concentrate around its
  ensemble mean. Independent preparation cannot be counted for free.
* Unfair comparator: uniform actions have worst ratio A^T, but an
  episode mixture of deterministic context policies has A^S on its
  subclass. The exponential comparison alone proves no new advantage.
* Full records: bounded-score learning does not reconstruct an
  arbitrary continuous or huge full record in total variation.
* Simulator substitution: replaying common noise through a known
  deterministic simulator is stronger access than actual trajectories.
  PEGASUS uses that stronger interface explicitly.
* Population identities and synthetic samples do not constitute an
  acquired apparatus precision budget.

## 9. Primary predecessors and research status

1. Cover and Ordentlich, Universal Portfolios with Side Information,
   IEEE TIT 42(2), 1996. https://doi.org/10.1109/18.485708
2. Ordentlich and Cover, The Cost of Achieving the Best Portfolio in
   Hindsight, Mathematics of Operations Research 23(4), 1998.
   https://isl.stanford.edu/people/cover/papers/hindsight.pdf
3. Peshkin and Mukherjee, Bounds on sample size for policy evaluation
   in Markov environments, COLT 2001, especially section 5.2.
   https://arxiv.org/pdf/cs/0105027
4. Kearns, Mansour and Ng, Approximate Planning in Large POMDPs via
   Reusable Trajectories, NeurIPS 1999.
   https://papers.neurips.cc/paper_files/paper/1999/hash/4f398cb9d6bc79ae567298335b51ba8a-Abstract.html
5. Ng and Jordan, PEGASUS: A Policy Search Method for Large MDPs and
   POMDPs, UAI 2000. https://arxiv.org/pdf/1301.3878

The upper route and coding-to-off-policy bridge are established.
The proposed local addition is the matching task-learning lower
construction and careful physical-interface interpretation. Historical
priority and a civilisation-changing new capability are not established.
The useful conventional foundation must not be relabeled as the
invention still being sought.
