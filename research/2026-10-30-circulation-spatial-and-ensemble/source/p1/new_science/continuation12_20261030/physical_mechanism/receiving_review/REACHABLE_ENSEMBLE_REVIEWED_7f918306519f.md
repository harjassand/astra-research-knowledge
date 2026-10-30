# Reachable hidden ensembles: an acquired metric and an executable witness

30 October 2026. Root construction. Working theorem, not yet internally
received. Earlier proofs and all binding corrections remain unchanged.

## 1. Consequence selected

Can an unknown dissipative material experimentally qualify a replacement
preparation for **all later uses of its physical state**, even when no finite
predictive representation closes? Can failure of that qualification produce
an actual distinguishing experiment rather than an unobserved latent norm?

The intended addition is a physical acquisition/learning receiver. Inner
products, reversible-chain identities, kernel witnesses and total-variation
contraction are established mathematics. The chronological adjoint-word
acquisition is inherited from Astra's `ADJOINT_WORD_ACQUISITION_AND_EXPANSION.md`.
The present receiver uses it on preparation densities, rather than projecting
future features onto a finite space. No historical novelty is inferred from
the proof or from a failed search.

## 2. Actual interface

Let (X,mu) be a probability space representing the complete physical state
needed by every later operation in the comparison. X may be infinite and may
include frozen hidden memory. A noninvasive visible label Y is supplied.
The apparatus can execute a finite menu of fixed-call Markov kernels P_j,
each self-adjoint on L2(mu). Their transition laws and hidden kinetic
coefficients need not be known. Calls, switching and future source freshness
are actual physical operations; their costs are not supplied by the algebra.

A calibration trial starts from a warranted mu preparation. A deployment
trial starts from f mu, where 0<=f=f(Y)<=B, integral f dmu=1, and that
preparation is actually available. One supplier is rejection from independent
mu preparations with acceptance f(Y)/B. Its mean number of baseline
preparations is B. Its failed preparations, sensing, random bits and records
are real costs. Rejection does not make a baseline preparation available.

For a chronological word w=(j_1,...,j_L), let

    P_w=P_(j_1)...P_(j_L),       rho_w=P_w^* f.

Thus rho_w mu is the actual output law. The adjoint word is the reversed
list of the same *forward stochastic calls*. Fresh noise is used in every
call. It does not undo a trajectory or replay an old reservoir. All rho_w
are nonnegative densities, and 0<=rho_w<=B because common-mu adjoints are
Markov contractions. The state includes any residual apparatus memory on
which the later consumer can act. If that memory is omitted, the theorem
only covers the included subsystem and the actual conditional interface.

Words here are open-loop fixed-call preparations. An adaptive instrument
with a retained transcript is a different object; its joint scope is treated
separately. A fixed call can have deterministic duration. A random-duration
call does not discard an accessible clock side record for free.

## 3. Three chronological echoes measure full hidden density error

For two words u,v, define

    K(u,v)=<rho_u,rho_v>_mu
          =<f,P_u P_v^* f>_mu.                         (1)

An actual calibration experiment starts in mu, reads f(Y_0), executes u
and then the reversed word v with fresh operation noise, reads f(Y_end),
and reports their product. Its expectation is exactly K(u,v). The report
lies in [0,B^2]. No hidden state or pair of futures from one state is read.

Consequently

    D(u,v)=K(u,u)+K(v,v)-2K(u,v)
          =||rho_u-rho_v||_L2(mu)^2.                   (2)

The nonnegative population quantity is the true density error on the full
state X. It is not a residual in a guessed finite feature space, a visible
endpoint discrepancy, or a model-based extrapolation. A negative empirical
estimate is a sampling error and is not certified zero.

The same identity allows distinct known bounded visible inputs f,g:

    <P_u^* f,P_v^* g>=<f,P_u P_v^* g>.                 (3)

It therefore applies to a finite supplied input family or a target created
from a different known visible preparation. Each normalization and preparation
must be warranted at its actual interface.

## 4. Every later state-dependent experiment is controlled

Let C be any common Markov kernel from X to a standard measurable complete
later record space. C may incorporate a new physical intervention, arbitrary
adaptive decisions, future randomization and an arbitrarily long well-defined
history. It need not belong to the acquired menu or have known kinetics.
Both compared preparations must feed the same C, with the same conditional
future apparatus law. Then

    TV((rho_u mu)C,(rho_v mu)C)
       <= TV(rho_u mu,rho_v mu)
       <= (1/2) sqrt(D(u,v)).                         (4)

Proof: Markov-kernel contraction followed by Cauchy--Schwarz against the
probability mu. The conclusion is uniform over every such C. There is no
observation-depth factor, spectral gap, hidden mixing time, state-count
bound or finite predictive closure assumption. The acquisition words still
cost their full execution duration; this is not a horizon-independent total
cost claim. The conclusion compares preparations on the same state space,
not two unrelated devices whose latent coordinates have never been matched.

An outside receiver that acts on an omitted private selector, clock record,
retired reservoir or correlated calibration state violates the displayed
common-kernel premise. Those records must either be included and qualified
jointly, or their actual isolation/reset operation must be stated and priced.

## 5. The difference supplies its own physical witness

In the common-input case put delta=rho_u-rho_v. Starting from an unknown
candidate state x, execute the following real test:

* choose a fresh fair bit J;
* if J=0, run the reversed word u and return 1 with probability f(Y_end)/B;
* if J=1, run the reversed word v and return 1 with probability
  1-f(Y_end)/B.

Its conditional probability of 1 is

    phi(x)=1/2+delta(x)/(2B),                           (5)

which belongs to [0,1]. The actual test has probability difference

    Pr_u{1}-Pr_v{1}=D(u,v)/(2B).                       (6)

Thus a nonzero echo distance has an executable distinguishing continuation
using only the same forward calls and visible label access. The tester uses
fresh trajectories and does not estimate delta(x) on a microscopic state.
Its choice bit and terminal randomization are actual classical operations.

If d_menu is the supremum of probability differences over available future
experiments, the result gives

    D(u,v)/(2B) <= d_menu(u,v)
                <= TV(rho_u mu,rho_v mu)
                <= sqrt(D(u,v))/2.                   (7)

In particular D=0 is equivalent to equality of the full hidden ensembles
and also to operational indistinguishability within the adjoint-closed menu,
**restricted to these reachable ensembles**. This is a constructive
reachability/observability duality. It does not make every arbitrary hidden
initial state observable. A frozen variable with a different initial law,
unaffected by every available operation and label, is an immediate
counterexample outside the supplied reachable family.

For distinct inputs f,g bounded by B, use the appropriate endpoint function
on each witness branch. The same equations hold with delta=P_u^*f-P_v^*g.

## 6. Finite experimental confidence and adaptive selection

Suppose M candidate words and one reference word are fixed before validation.
Acquire the M diagonal terms, M cross terms and one reference diagonal.
For n independently warranted trials per entry, Hoeffding and a union bound
give simultaneous entry error at most

    r_n=B^2 sqrt(log(2(2M+1)/alpha)/(2n))               (8)

with probability at least 1-alpha. On that event every candidate satisfies

    |D_hat(w,t)-D(w,t)|<=4r_n,
    TV_later(w,t)<=min{1, (1/2)sqrt(max{0,D_hat+4r_n})}.
                                                            (9)

Any data-selected candidate is covered by this same event. One may instead
select using arbitrary pilot experiments and validate its three entries on
fresh trials; then M=1 in the validation bound. The candidate is fixed
conditionally on the pilot record. A replayed hidden microscopic state is
not an independent trial. Actual conditional baseline preparation and device
stability are required; finite confidence does not establish those suppliers.

To certify a total-variation tolerance epsilon near an exact match using
this elementary estimator takes O(B^4 epsilon^(-4) log(M/alpha)) trials per
entry, plus their full preparation/word/readout costs. This is an upper
bound for the stated acquisition, not an optimality theorem. Common
equilibrium avoids endpoint-weight growth; it does not remove the precision
or preparation bill. A known centered visible input can reduce variance
without changing the receiving theorem.

Deployment follows a fresh warranted conditional input preparation. Then
the same retained calibration record can be attached to both laws, with a
reference initialized at the corresponding reference output law. On the
simultaneous success event its selected conditional state error is bounded
as above. Unconditional record-and-output error pays the failure probability
as well. Persistent calibration memory in X requires the actual joint
initializer; a good visible fit does not provide one.

## 7. Learned substitutions and limits of the contribution

An ordinary optimizer can minimize an acquired upper confidence bound on
D, subject to actual word cost, or choose the cheapest validated candidate.
It needs no hidden transition matrix, learned force law, microscopic
trajectory adjoint or finite predictive state. The physical witness supplies
an automatic finite-amplitude discriminating experiment when a candidate
fails. The optimization method is ordinary and receives the same echo access.

This makes a learned replacement preparation qualified for later uses not
enumerated during learning. It does not give universal controllability,
promise a cheap replacement exists, certify the physical resource ledger
from a retained bit count, or prove a practical speedup. Calibration costs
are amortized only over the actual number of later executions. New target
ensembles outside the source's reachable family need their own preparation
or representation. Exact population zero and finite-data confidence remain
different statements.
