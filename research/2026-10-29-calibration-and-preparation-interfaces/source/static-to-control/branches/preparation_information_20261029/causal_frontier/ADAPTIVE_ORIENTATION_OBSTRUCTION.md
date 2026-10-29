# Finite adaptive experiments do not by themselves erase the orientation ambiguity

29 October 2026. Ordinary complementary proof. Independent review pending.

## 1. Exact declared interface

Fix a finite-state source with a baseline irreducible CTMC Q_0, stationary pi,
and deterministic readout g. It can be run under a library of controlled
generators Q_u and instantaneous classical instruments M_(a,y), where each
M_(a,y) is nonnegative and sum_y M_(a,y) is stochastic. Instruments include
visible-state preparations, measurements, feedback actions and declared
restart actions. A protocol can choose actions, waiting times and stopping
based on the full visible history and its own independent randomness.

Assume the instrument semantics specify this input/output interface but do
NOT independently certify an action on every latent physical coordinate,
a singleton microscopic reset, a parity pulse, a thermal bath refresh, or
another hidden constraint that excludes the extensions below.

Take a protocol with total continuous exposure at most T and an arbitrary
finite number of instantaneous instruments. Its source starts from the
baseline stationary preparation. This is a transcript experiment class,
not a claim that instruments have zero physical work, duration or hardware
cost. Real durations during which latent switching can occur belong in T.

## 2. Uniform adaptive coupling construction

Use the predecessor's 2n orientation model on (x,+/-), with + running Q_0,
- running Q_0*=D_pi^-1 Q_0^T D_pi, and independent switching rates

    + -> - : a=kappa epsilon,
    - -> + : b=kappa(1-epsilon).

Its baseline stationary law is pi times (1-epsilon,epsilon). Under control
u, run Q_u in + and any valid chosen generator in -, retaining the same
switching mechanism. The choice in - can be Q_u itself, or its stationary
adjoint when appropriate. Each instantaneous M_(a,y) acts on x and preserves
orientation, with the SAME conditional outcome rule in both orientations.
The observation g(x) is even under Theta(x,s)=(x,-s).

Couple the original source and lifted experiment using the same controller
randomness, the same initial x, the same + dynamics and instrument outcomes.
Conditional on starting in +, their complete transcripts agree until the
first + -> - switch. Because the visible histories agree up to that event,
all adaptive choices agree as well. The switch clock has constant intensity
a independently of those choices. Thus for EVERY allowed adaptive protocol,

    TV(P_lift^protocol,P_source^protocol)
       <= epsilon+(1-epsilon)(1-exp(-a T))
       <= epsilon+kappa epsilon T.                         (1)

The bound is uniform over the number, identity and adaptivity of the
instantaneous visible instruments. It includes full continuous readout,
all action/outcome transcripts and every bounded decision statistic.
For expected-exposure constraints the same coupling gives the looser
epsilon+a E[T] when that expected-time bound is valid for the coupled
no-switch target protocol. A fixed deterministic cap avoids any optional-
stopping bookkeeping.

If a nominal restart simply applies a specified x-preparation kernel,
it preserves sign and does not pay a new epsilon failure term. If the
contract genuinely supplies N independent whole-source stationary starts,
apply a product/conditional hybrid and pay at most N epsilon+a T_total.
This does not treat an observed restart as a hidden reset.

## 3. Baseline physical conclusion

The BASELINE lifted generator retains the predecessor's exact intrinsic
stationary reversal-divergence rate

    sigma_2n=kappa(1-2epsilon)^2,
    B=(1-2epsilon)log[(1-epsilon)/epsilon].                 (2)

For a fixed common microscopic baseline escape clock, append the hidden
toggle bit of the predecessor's 4n construction. Let
Lambda=max_x lambda_0(x)+c_0 and kappa<c_0. It preserves the observed baseline
path law exactly and yields

    sigma_4n <= kappa(1-2epsilon)^2/(1-kappa/c_0).           (3)

The controlled protocols can carry that additional hidden bit invisibly;
their coupling (1) is unchanged. The fixed common clock in (3) is a
BASELINE statement. If a finite controlled family is bounded uniformly,
one can instead choose Lambda larger than every controlled escape rate
and use invisible toggles action by action; no free bound is asserted for
unbounded interventions. Each physical action's full duration/precision
remains part of its actual implementation.

For any finite experiment budget and accuracy delta>0, choose epsilon
small enough and then kappa small enough to make all transcript TV errors
less than delta while making baseline sigma arbitrarily small. Standard
testing inequalities transfer immediately: an acceptance event with
probability p under the target has probability at least p-delta under the
low-sigma alternative. Therefore no uniformly valid finite-budget procedure
can certify a positive BASELINE intrinsic entropy lower bound solely from
that unrestricted visible intervention record.

This is stronger than a passive-record failure, but it is not a claim about
all physically possible control. The theorem's hidden-preserving instrument
extensions are admissible only when the declared physical semantics allow
them. Known microscopic reset, parity action, local detailed balance,
reservoir coupling, exact dimension or complete-rank upper bounds can exclude
these alternatives. A finite fitted predictor does not acquire those facts.

## 4. An exact common-invariant control refinement

Suppose every Q_u has the same stationary pi. Choose the - generator to be
Q_u*=D_pi^-1 Q_u^T D_pi. Then every frozen-control generator has the SAME
stationary orientation law, and its 2n intrinsic rate is exactly (2).
For any deterministic open-loop switching schedule, rho remains invariant
at all times. The internal forward/reverse likelihood ratios telescope
through the common pi; with the appropriately reversed externally supplied
schedule the total expected path KL is B+T sigma_2n. Thus rich open-loop
driving within this common-invariant family does not remove the boundary.

This does not assign the same entropy formula to feedback-controlled
protocols: reversing a feedback controller introduces its own record,
preparation and action-likelihood accounting. The adaptive transcript
coupling (1) remains valid, but its baseline inference consequence does not
silently become a full thermodynamic cost claim for the controller.

## 5. Reach and novelty scope

An acquired predictor can be entirely sufficient for every experiment in a
declared control library while failing to determine a physical property of
its realizations. Predictive equivalence and physical equivalence are
different equivalence relations. The active coupling makes the distinction
constructive at finite precision; it is not merely a warning that unobserved
variables might exist.

The proof is a straightforward coupling extension of the predecessor's
orientation theorem, whose adjoint-sign and odd-ring antecedents are already
credited there. No separate historical novelty is claimed. Its useful role
is to state the missing physical input precisely when importing operational
reset/predictive-core results into an entropy argument.

The positive companion OPERATIONAL_FORGETTING_ENTROPY_BRIDGE.md shows what
changes under an honest complete observable-rank/core contract with an
ACQUIRED passive forgetting certificate. In that class a latent orientation
that could influence arbitrarily late visible histories cannot be omitted
from the certified quotient. Its rare acquisition probability and poor
conditioning are real costs, not invisible state variables removed by
notation.
