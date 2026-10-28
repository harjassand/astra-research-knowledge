# Complete acquisition cost: positive flags and the unavoidable calibration rate

28 October 2026. Independent scoped review of the new rank-one cost theorem.
The positive-flag access and the previously reviewed energy certificates are
used at their stated scope. This document gives the new polynomial, sampling,
cost and testing arguments. It does not re-audit the earlier compiler.

## Finding

The proposed g^(-3) source-execution rate is valid, with the following precise
scope. For q primitives, total cost is O(q g^(-3) log(q/delta)); the q factor
may be absorbed only when q is fixed. The positive flag acquires a useful
inverse-dissipation upper bound and the same trials supply the more demanding
self-loop calibration. First-step rejection keeps expected primitive cost
per logical trial bounded. Reusing an exactly recognized reset state reduces
actual preparations to O(q g^(-2) log(q/delta)) in expectation.

The proposed lower constant 1/(8g^3) is valid for accuracy g/10 and error
probability at most 1/3, even when every state is observed. A small rescaling
of the alternative, given below, matches an arbitrary fixed constant in an
upper O(g) accuracy guarantee. These statements match the slow-scale
exponent; they do not establish optimal dependence on q or an optimal
tradeoff among preparations, observations and primitive steps.

## 1. Source and access contract

The upper construction needs a family of killed reversible Markov kernels
represented as selfadjoint contractions A_i in one common Hilbert space.
For a common reset state b, normalize ||b||=1 so that

    f_i(k)=<b,A_i^k b>

is the probability of returning to b after k repetitions. For ordinary
symmetric substochastic matrices, b is just the reset coordinate vector.
A common selfadjoint representation matters for arbitrary switched words;
separate reversibility measures with no common representation are not enough.

The learner can apply a chosen primitive, exactly and nonintrusively test
membership in the singleton state b at selected times, and prepare b after
a trial ends elsewhere. The process has the Markov restart property at b.
The latter requires the predicate to identify the actual reset state, not
merely a coarse set of potentially different hidden states. These are
additional physical access assumptions, not consequences of scalar endpoint
measurements.

For fixed known class constants c>0, C_d and C_Q, assume, for sufficiently
small known g>0,

    ||A_i||<=a_i<=1-cg<1,
    d_i=1-t_i<=C_d g,    t_i=<b,A_i b>,
    Q_i=<D_i,(I-A_i^2)^(-1)D_i><=C_Q g^2,
    D_i=(A_i-t_i)b.

The Q promise concerns the true Galerkin scalar t_i, not an estimated scalar.
The norm bound also implies d_i>=cg. No hidden dimension or rank is given
to the learner. The norm bound concerns the killed live-state operator,
not the absorbing transition operator with cemetery included.

## 2. A finite positive polynomial within a factor two

Put h=1-a^2, L=1/h and K=ceil(L). Since a>=t=1-d,

    cg<=h<=2 C_d g,
    Z=K+L=Theta(1/g).

The lower bound on Z uses both the norm warranty and the small departure
premise; a<=1-cg alone would not imply Z=Theta(1/g).

Define

    P_K(lambda)=sum_{k=0}^{K-1} lambda^(2k)+lambda^(2K)/h.

For |lambda|<=a, write x=1-lambda^2, so x>=h. Then

    (1-lambda^2) P_K(lambda)
      =1-lambda^(2K)+(x/h)lambda^(2K).

The ratio is at least one. Also x(1-x)^K<=1/(K+1): multiply the inequality
sum_{j=0}^K(1-x)^j >= (K+1)(1-x)^K by x. Therefore the ratio is at most

    1+1/[h(K+1)] < 2.

By the spectral theorem, the finite form

    F_K=sum_{k<K}<D,A^(2k)D>+<D,A^(2K)D>/h

satisfies Q<=F_K<=2Q. This is an all-spectrum proof, not an inference from
finite numerical examples.

## 3. The positive flag and its normalization

Choose k<K with probability 1/Z each, and k=K with probability L/Z.
Execute 2k+2 repetitions from b. The flag is one precisely when the state
is outside b after the first step, outside b after the penultimate step,
and inside b after the last step.

For the true t=A_bb, inclusion-exclusion and the Markov property give

    P(flag=1 | k)
      = f(2k+2)-2t f(2k+1)+t^2 f(2k)
      = <D,A^(2k)D>.

Selfadjointness supplies the last identification. The event is observed
directly and does not require knowing t. Cemetery is included in outside;
its probability contributes no return flags. Thus the mixture flag has

    p_flag=F_K/Z <= 2 C_Q C_d g^3.

A first-step self-loop makes the flag false for every label k. It can be
rejected immediately, before choosing a label. On departure, an independent
label is sampled and the remaining segment is executed. Deferring the label
does not change the flag law.

## 4. One set of trials acquires both premises

Use N=ceil(B g^(-3) ell) trials per primitive, where
ell=log(4q/delta) and B is a sufficiently large constant depending only on
the class constants. Let S count positive flags and X count first-step
departures. The same trials supply both observations; a union bound, not
independence between the counts, is used.

One simple, deliberately conservative valid upper confidence bound is

    p_upper=min(1, 2(S+ell)/N).

It fails with probability at most exp(-ell). Indeed
E exp(-S+Np_flag/2)<=1, since 1-exp(-1)>1/2.
For performance, the elementary mgf E 2^S<=[exp(p_flag)]^N shows

    S<=2N p_flag+2ell

except with probability exp(-ell). Hence on these events

    p_upper<=4p_flag+6ell/N=O(g^3),
    Q_upper=Z p_upper=O(g^2).

More efficient exact binomial or empirical Bernstein bounds can replace
this conservative choice without changing the rate.

For departure calibration, a valid known-variance-envelope radius is

    r_N=sqrt(2 C_d g ell/N)+2ell/(3N)=O(g^2).

Bernstein's bound gives |X/N-d|<=r_N except with probability at most
2 exp(-ell). This follows directly from the Bernoulli mgf and its usual
quadratic upper bound; it is not a constant-variance Hoeffding estimate.
Let that=1-X/N. On the same event,

    R=1-that^2=Theta(g).

For example, choose B large enough that r_N<=cg^2/2; then R>=cg/2 for
g<=1. A zero empirical departure count is outside this good event and does
not justify a dissipation certificate.

The four events per primitive fit the stated failure budget. The first
two prove a useful positive-form certificate and the other two control
the proposed model. They remain valid when b is reused between trials by
the Markov restart property.

## 5. Transfer to the proposed model and all words

The estimated defect is

    Dhat=(A-that)b = D+(t-that)b.

Minkowski in the inverse-dissipation norm gives the acquired bound

    Qhat <= [sqrt(Q_upper)+r_N/sqrt(1-a^2)]^2.

Here sqrt(Q_upper)=O(g), while
r_N/sqrt(1-a^2)=O(g^(3/2)). Therefore Qhat=O(g^2), and

    theta_i^2=Qhat_i/(1-that_i^2)=O(g).

The known reset Gram value is one. Taking the empirical self-loop value
as the model makes the observed weak-defect center zero; its uncertainty
is r_N. The reviewed noise normalization gives

    zeta_i=r_N/(1-that_i^2)=O(g).

The already reviewed signed energy theorem consequently certifies every
finite switched word with error

    2 max_i theta_i^2 + max_i zeta_i = O(g).

The returned midpoint is the product of the empirical scalar models.
Unknown hidden rank does not enter the acquisition or this guarantee.
This is a simultaneous all-word confidence statement on one good event,
not a claim of correctness conditional only on emitting a certificate.

## 6. Complete physical ledger and reset-state reuse

A logical trial costs one initial source application. Only first-step
departures incur up to 2K+1 additional applications. Therefore

    E[primitive applications per trial]
      <=1+d(2K+1)=O(1).

The exact mean for the specified mixture, when no other early rejection is
used, is

    1+d [K^2+L(2K+1)]/Z.

No hidden detection of cemetery is used: a departed trajectory that is
not visibly back at b is charged through its assigned horizon. Membership
observations cost at most one plus two per departure, so their expected
number is also bounded per trial.

After the terminal predicate identifies b, the next logical trial may
start from that same physical state. The strong Markov property supplies
the same fresh-trial distribution. No reset command is required. A trial
can end outside only if its first step departed, so actual preparations
are bounded by the initial preparation plus the number of departures.
Across all primitives this gives

    logical trials:                  O(q g^(-3) ell),
    expected primitive applications: O(q g^(-3) ell),
    membership observations:         O(q g^(-3) ell),
    expected actual preparations:    O(q g^(-2) ell), plus initialization.

These preparation counts are an achievable upper bound, not a proven
optimal preparation tradeoff. Earlier receipts charging one fresh reset
per trial remain conservative receipts; their recorded execution is not
retroactively changed.

The primitive and preparation bounds also hold with high probability on
the same bounded-departure-count event. Without such an event or a budget
cap, the deterministic worst-case source cost is O(q N/g), since every
trial could depart.

Mixture labels should be drawn only after departure. With ordinary bounded
encoding length for g and the warranted cap, expected controller randomness
is O(g log(1/g)) per trial. A simple exact alternative avoids awkward
rational sampling: choose K to be a power of two with K>=1/h, use tail
weight K, and normalizer 2K. Choose the tail with probability 1/2 and
otherwise a uniform label below K. The same factor-two spectral proof
holds, and the expected source cost retains its order.

This ledger counts source operations, preparations and membership reads
at specified unit costs. A preparation whose own physical cost diverges,
an increasingly difficult membership sensor, parameter-input bit complexity
or future word-evaluation work must still be charged separately. None is
acquired merely by quoting a number of trials.

## 7. Full-state lower bound, including adaptive trajectories

Consider a source with one live state b and an absorbing cemetery. One
source application from b survives with probability p; from cemetery it
has no unknown behavior. Let g=1/m, integer m>=4, and

    p0=1-g,    p1=1-g+g^2.

Both killed live-state operators satisfy the same cap a=1-g/2. Both have
zero true Galerkin residual, and departures remain Theta(g).

Give the learner full state observations, arbitrary adaptive trajectory
lengths, arbitrary resets, private randomness and almost-surely finite
stopping. Each informative application is exactly a Bernoulli survival
observation. Operations at cemetery and reset decisions add no information.
Using natural logarithms,

    KL(Bern(p0)||Bern(p1))
      <=g^4/[p1(1-p1)]
      <=16 g^3/9,

because p1>=3/4 and 1-p1=g(1-g)>=3g/4. The reversed KL obeys the same
coarse bound.

The adaptive finite-prefix KL chain rule therefore bounds transcript KL
by (16g^3/9) times expected source applications under the corresponding
hypothesis. Finite-prefix decision events converge at almost-sure stopping;
no optional-stopping shortcut is needed. Error at most 1/3 under both
hypotheses implies total variation at least 1/3, so Pinsker yields

    E_0[source applications] >=1/(8g^3),

and the same coarse lower bound under hypothesis 1. Infinite expected cost
is trivial. The lower bound counts source applications; it does not prove
a preparation lower bound.

At H=m, the power response gap obeys

    p1^H-p0^H
      >=H(p1-p0)p0^(H-1)
      =g(1-g)^(1/g-1)
      >g/3.

The last inequality follows from
(1+1/(m-1))^(m-1)<exp(1)<3.
Consequently an all-word predictor with absolute accuracy g/10 and success
probability >=2/3 under each source distinguishes the pair.

This is a lower bound for every allowed full-state algorithm on this known
pair, not only for short echoes or positive flags. A class with the diagonal
survival probability supplied exactly is a different, more informed task.

## 8. Matching the accuracy constant and an existing upper route

The displayed lower pair proves the g/10 task. An upper guarantee C_* g
with an unspecified or larger C_* is not literally the same task. This
constant mismatch can be repaired without changing the exponent.

For any fixed desired accuracy constant A, choose fixed beta>6A and

    p1=1-g+beta g^2,
    0<g<=min(1/4,1/(2beta)),    g=1/m.

The same cap 1-g/2 and zero residual hold. The target gap is >beta g/3>2Ag,
while per-informative-step KL is <=(8/3)beta^2 g^3. Hence accuracy Ag implies

    E[source applications] >=1/(12 beta^2 g^3).

This proves matching slow-scale order for any fixed upper accuracy constant
on a source class containing these alternatives. It does not imply the
same lower bound for a specially restricted class with no calibration
uncertainty.

An equally informed ordinary route matches the order on the one-live-state
family: estimate its survival coin with variance-aware precision O(g^2)
using O(g^(-3) log(1/delta)) primitive applications. Clip the estimate to the
known cap a=1-g/2. Then for every H,

    |phat^H-p^H| <=H |phat-p| a^(H-1)
                 <=2 |phat-p|/g.

Precision g^2/20 therefore suffices for uniform accuracy g/10. This is
ordinary rare-event calibration, with no residual acquisition needed.
For example, N=ceil(3200 g^(-3) log(2/delta)) makes the Bernstein radius
at most g^2/40+g^3/4800<g^2/20 for g<=1/4. The ordinary procedure can
also continue from b after survival and prepare b only after death, so
its expected preparation count is at most one plus gN.
For small failure probabilities, binary decision KL also supplies the
usual log(1/delta) lower factor. No claim of a new general statistical
principle or an improved q dependence is made.

## 9. What the renewal improvement can and cannot change

A renewal construction may acquire the true Galerkin residual with only
O(g^(-2)) trials. Those trials alone give self-loop calibration uncertainty
of order g^(3/2), not g^2. Although that may already keep the proposed
weighted residual of order g^2, its all-word correction uncertainty is
order sqrt(g), not order g.

Additional calibration restores the g^(-3) complete rate. The zero-residual
full-state lower family proves that this is not merely a weakness of the
chosen certificate. Faster residual acquisition can still improve constants,
preparation tradeoffs or tasks with a known diagonal; it cannot defeat
this source-action lower bound for the stated unknown-diagonal accuracy
task.

## 10. Executed exact receipt

calibration_cost_checks.py executed exact rational checks for six scales
g=1/4 through 1/128. Two symmetric substochastic source matrices at each
scale satisfy the advertised cap and Q<=2g^2. The checker verifies
Q<=F_K<=2Q, the mixture probability envelope, expected primitive and
membership costs, terminal-outside preparation bounds, and a concrete
variance-aware budget.

For the first source, the expected primitive cost per trial decreases from
about 2.94 at g=1/4 to about 2.51 at g=1/128; for the second it decreases
from about 4.88 to about 4.03. The flag probability divided by g^3 stays
bounded, near 0.53--0.62 in these checks. The script also verifies the
original lower pair at all six scales and the rescaled accuracy argument
at three scales.

CALIBRATION_COST_REVIEW_CHECKS.json is an algebraic receipt. Listed trial
counts are proposed statistical budgets, not executed trajectories.
The ordinary arguments above establish the all-scale and adaptive claims;
finite checks do not substitute for them.

The adaptive change-of-measure method is standard; see Kaufmann, Cappe and
Garivier, JMLR 17 (2016), Lemma 1 and Remark 2:
https://www.jmlr.org/papers/volume17/kaufman16a/kaufman16a.pdf
The source-specific polynomial flag, reuse protocol, confidence transfer
and complete-cost conclusion are distinguished from that antecedent.
