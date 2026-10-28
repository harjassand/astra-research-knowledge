# Finite experiments can certify operation composition without identifying the hidden source

Scientific note for Capital. 29 October 2026, Brisbane.

## Result and research decision

Two complementary constructions now acquire reusable operation models from
finite experiments on infinite hidden sources. The first certifies arbitrary
boundary transport using actual preparable boundary states and observed
irreversible loss. The new construction removes exact state recognition for
the narrower total-survival task, using a common reversible preparation and
coarse live/absorbed reports. It certifies a two-state approximation to a
countably infinite source with no strict global gap and infinite mean lifetime.

The static scalar machinery from P1 remains useful inside this larger question.
Static response acquisition alone does not capture how operations compose.
The new target is the information needed to certify future compositions
against the actual source, with acquisition, preparation, measurement accuracy,
execution and reuse all explicitly accounted for.

This is a substantive conditional construction, not a claim that the
civilisation-scale objective has been reached. It uses established Gram
realization, model reduction, energy estimates and renewal algebra. The
specific addition is a finite observable procedure supplying either local
physical residual forms or an experimentally acquired switching-tail bound
and mixed-word cover. These support simultaneous future-program guarantees
without a hidden-rank promise. The distinction matters: on the new source,
the centered inverse forms themselves diverge, while uniform absolute
survival prediction is still finitely certifiable.

## Why composition required a different representation

An exact Clifford construction gives two positive-operation sources with
identical frozen-mixture response families and identical scalar words through
length four, but a fifth-order word differs by 243/16384. Thus richer static
response data need not contain operation-order information. The branch also
constructs finite word dictionaries that recover the relevant composition
exactly when exact observations are supplied. This is a representational
separation, not a finite-noise autonomous discovery theorem.

The first new compiler acquired Gram, insertion and physical residual matrices
through reciprocal scalar words. It used the actual signed primal-dual
correction, whose remainder pairs two physical defects. That gave useful
uniform bounds without identifying the hidden source. Known GNS/LGST,
ResDMD and primal-dual model-reduction methods already supply much of the
mathematical machinery; precision and unknown-source access remain distinct.

A tempting stronger criterion failed: making each primitive defect small
relative to its model increment did not prevent nearly unit output error
after composition. The exact counterfamily survives removal of exact fixed
modes and admits a quantum-channel embedding. Primitive-relative smallness
was therefore abandoned as the controlling quantity.

The successful stronger quantity is physical inverse dissipation of the
defect. For a selfadjoint contraction A, representation V and proposed map T,

    D=AV-VT,    Q=D*(I-A^2)^(-1)D.

The inverse denotes a quadratic form on the relevant columns, with an actual
range condition. Its finiteness must be established; a pseudoinverse cannot
silently remove a bad component. If Q is dominated by theta^2 times the
computational dissipation I-T*T, the signed all-word remainder is bounded
by 2 theta^2. A general forward/dual theorem gives 2 theta_f theta_b.
The classical Julia-operator energy identity proves it; scoped examples show
that its factor two is sharp under the stated general assumptions.

The first finite acquisition of Q used reciprocal echoes and a strict source
norm cap to close an unmeasured tail. At g=.001, the refined bound was
.001069081794 instead of about one for the earlier unweighted certificate,
but it explicitly required raw ADC error 1e-14. That precision was a premise,
not acquired by counting 37 scalar readings.

## Positive observations supply the missing physical form

For a classical symmetric killed Markov source, prepare a genuine boundary
state, execute one primitive repeatedly, and observe the first boundary
return, irreversible absorption, or a finite censor time H. The experiment
counts an unresolved living excursion as a possible eventual return. It
therefore needs no estimate of the slowest hidden relaxation time.

Partition the source into finite boundary and arbitrary hidden coordinates:

    A=[T C*; C B],  D=[0;C].

Let K_+ be the sum of first-return matrices, K_- their parity-signed sum,
and E the even-return sum. Define H_+=I-T-K_+ and H_-=I+T-K_-.
Classical renewal and Schur identities give

    M=V*(I-A^2)^(-1)V=(H_+^(-1)+H_-^(-1))/2,
    Q=E+(K_+H_+^(-1)K_+ + K_-H_-^(-1)K_-)/2.

Observed absorption supplies positive finite lower bounds on both Schur
sectors. Upper bounds on return-or-live-censored and even-return-or-live-censored
events bound Q. The same local M transfers the form certificate from the
unknown true boundary kernel to its estimated matrix. This is the step that
replaces the global inverse factor 1/(1-a^2).

Abel regularization proves the formulas and actual form domains even when
the full source norm is exactly one and the global inverse is unbounded.
No hidden transition matrix, hidden dimension or tail distribution enters
the learner. The ordinary proof, exact finite checks and implementation-input
isolation are separately preserved and internally reviewed.

## Executed infinite-source construction

The source has three visible preparable states and two noncommuting actions.
Every visible state is connected to a fast hidden state and infinitely many
slow hidden states. Slow holding probabilities approach one, and every slow
state is reachable. The source norm is exactly one; every live state still
has positive loss. This is not an unreachable invariant block added to a
finite model.

The learner receives two million trials per action/start pair, six pairs
total. It stops at a boundary return, observed loss, or H=32. Integer random
transitions and an untruncated geometric sampler execute the countable source.
Only the allowed categories and counts leave the private source backend.

The acquired point model has absolute error at most .0399059846 for every
finite word and every unit boundary input/output vector. For nonnegative
boundary inputs and outputs, familiar positive interval propagation around
the true Galerkin model is stronger. Its physical dynamic remainder is
.001112504539; its complete word interval also includes parameter uncertainty.

For transport from boundary 0 to 2, compare ten action-0 operations followed
by ten action-1 operations with the reversed block order. Neither word is
used in acquisition. The stronger same-data route certifies

    difference in transport probability in [.1080212656,.1337115038].

The corrected point-model route independently resolves the same ordering.
The joint probability of a false used interval or certificate is below .001.
This covers all future words on one simultaneous event, including words chosen
after examining the acquisition data. It does not cover arbitrary feedback
policies conditioned on intermediate outcomes within a new run.

## Complete cost and the stronger existing routes

| Resource | Reusable acquisition | Direct test of the two named words |
|---|---:|---:|
| Logical trials | 12,000,000 | 20,000 |
| Primitive applications | 12,036,469 | 400,000 |
| Categorical observations | 12,036,469 | 20,000 |
| Physical preparations | 1,758,723 | 13,715 reported; 13,717 independently bounded |

The direct test uses the exact same infinite source and access interface and
certifies a difference in [.0867624766,.1476625420]. It is substantially cheaper
for this one comparison. The reusable certificate earns value only when many
subsequent programs need evaluation or when its simultaneous scope matters.
No universal speedup is claimed. Future finite-dimensional evaluations still
pay arithmetic and numerical-precision costs, and finding an optimal word
can remain difficult.

The same-data positive Galerkin comparator wins the finite-program inference
comparison. That is a useful adoption of the newly acquired physical form,
not evidence that the form was unnecessary. Existing methods supplied with
the same data and assumptions are entitled to use it. Stronger information,
such as complete hidden-state observations, can justify still other methods.

Earlier positive fixed-horizon flags were also compared with first-return
renewal acquisition. Renewal can reduce some preparation costs while adding
source time and observations. After correcting logical trials versus actual
resets, no unconditional winner remained. A known endpoint can be reused only
when it specifies the actual preparation state; this correction materially
reduces several earlier preparation ledgers.

## What the asymptotic cost theorem actually says

In a rank-one slow-scale family, boundary departure is Theta(g), finite
observed absorption is Omega(g), and return-or-live-censored probability is
O(g^2). The local form can be acquired with no strict global gap. A complete
O(g) all-word error requires O(q g^-3 log(q/delta)) source applications and
observations, and O(q g^-2 log(q/delta)) expected preparations under valid
boundary reuse. The constants and q dependence are explicit class resources.

This exponent cannot be removed by improving only residual acquisition.
Even a fully observed one-live-state survival source with zero residual
requires Omega(g^-3) primitive applications to distinguish retained rates
separated by order g^2 at the accuracy relevant to horizons of order 1/g.
Adaptive resets and stopping do not evade the transcript-information bound.
Ordinary variance-aware coin estimation matches the exponent on that family.

A countably infinite reachable example has norm exactly one at every g.
Its weighted certificate is O(g), while the old unweighted second-order
certificate remains at least 1/4 even with exact model and residual data.
At g=1/1024 the exact algebra gives weighted bound .000356342922 and
unweighted bound approximately .25. These are mathematical certificates;
the statistical acquisition budgets at these scales were not executed.

This comparison is deliberately precise: the original unweighted compiler
already avoided a strict hidden source gap. The new result removes that
premise from the more informative weighted acquisition and proves useful
separation on a family where its relevance is visible.

## Instrument precision and the boundary failure

Allowing the live/absorbed detector to err with conditional probability eta
per report contributes at most H eta to the relevant trial-event uncertainty,
while exact boundary labels and preparation remain. Recomputing the saved
counts with eta=1e-6 preserves the transport difference in
[.1063510236,.1353817458] and gives uniform point-model bound .0451712088.
At eta=1e-4 the tested difference interval crosses zero. The sensor warranty
has not been acquired by this analysis.

The next attempted extension, replacing exact boundary states by a coarse
cell and a reproducible initial distribution, fails. Two strictly contracting
two-state sources have identical coarse first-return laws for every acquisition
budget, yet later responses differ by more than .48. The observed cell hides
within-cell state redistribution; leaving-cell flags miss that residual.

An actual conditional resampling operation imposes exact finite closure even
for noncommuting original primitives. It also changes the program, incurs
refresh operations, and can destroy valuable protected populations. This is
a legitimate established alternative, not an inference about unchanged source
dynamics. The surviving research obligation is to acquire within-cell memory
or construct a physically warranted regeneration interface. A coarse positive
report cannot be relabeled as an exact reset.

The next source-preserving construction now detects that missing memory.
Uninterrupted two-step survival probes certify a positive two-word Hankel
determinant, but cost 63,499,098 source steps and 32 million preparations.
A separate, equally informed procedure pays for a short pilot and chooses
31-step blocks. It certifies the same need for memory using 522,817 source
steps, 18,847 coarse reports and 12,048 preparations. The observed determinant
interval is [.04617706029,.15682885293]. Thus changing experimental word length
can replace an onerous small-moment precision demand with explicitly paid
physical evolution. This acquires a missing representation direction, not a
complete finite-state model. COARSE_MEMORY_ACQUISITION.md preserves both
executions and an order-1/g known-pair information lower bound.

## Continuing past the boundary failure

The memory witness did not complete coarse-interface prediction. A strong
existing method first removed an unnecessary burden: ordinary DKW empirical
survival estimation certifies every repetition length of one operation without
identifying a hidden model. On the two-microstate slow example, 4,000 fresh
lifetimes, censored at a fixed finite cap, cost 62,181,306 source applications
and reports and gave an all-length error band of 1/32 at failure below .001.
That is a different task from merely detecting a second memory direction.

The next exact counterexample preserves every individual-action lifetime law
while changing mixed responses. Two symmetric two-state sources differ only
by a hidden swap in one primitive. AB survival is 15/64 versus 9/64, and
the AAB-minus-ABA ordering difference changes from -1/256 to 5/256. Thus
even perfect marginal lifetime data do not provide composition information.

A useful transfer remains. Suppose positivity-preserving selfadjoint actions
share a positive unit preparation vector v with A_i v<=v. Every reachable
word vector stays in the order interval [0,v]. A pure survival observation
therefore acquires an entire order-interval norm:

    sup_(|x|<=v) ||A_i^m x||^2 = ||A_i^m v||^2=f(i^(2m)).

The elementary spectral inequality 1-lambda^(2m)<=m(1-lambda^2) turns an
observed upper s>=max_i f(i^(2m)) into the common energy bound

    ||A_wv||^2 <= z_h=s+(1-1/m)^h(1-s),  h=|w|.

Split a scalar response into two reversed halves to obtain survival <=z_h
for EVERY word of length 2h. Individual eventual absorption then gives a
finite uniform switching cutoff at any fixed absolute accuracy, without
requiring finite hidden dimension, a strict norm gap or a finite mean lifetime.
The common order relation is a premise, not inferred from lifetime counts.
This is an observable specialization of established weak-Poincare theory.

Mixed-word acquisition supplies the information missing from the marginals.
At a prefix whose measured survival upper is <=epsilon, every longer
continuation also has survival <=epsilon. A complete finite tree of such
terminal prefixes, with confident intervals at all retained branches,
certifies all words. Familiar prefix estimation provides the representation;
the new tail acquisition supplies a finite cutoff for the source class.

The executed source has a fast two-state block and countably many slower
copies, all assigned positive preparation mass. Their holding probabilities
approach one. Every source operator has norm exactly one, and mean lifetime
is infinite, although eventual absorption holds. Pure-curve acquisition
costs 34,356 applications/reports and 16,384 fresh preparations. It acquires
m=4, s=.039498905686 and a length-26 all-switching survival upper below 1/16.

A separate balanced set of control tapes costs 1,051,824 applications/reports
and 524,288 fresh preparations. Its observations are shared across prefixes
using full preassigned denominators, with earlier deaths correctly counted
as zeros. The resulting complete cover has 84 nodes and closes by length 7.
All costs, including the pure curves, are paid:

| New coarse construction | Complete executed cost |
|---|---:|
| Primitive applications | 1,086,180 |
| Live/absorbed reports | 1,086,180 |
| Fresh preparations | 540,672 |
| All-word absolute survival error | 1/16 |
| Joint false-certificate upper | .001 |

Ordinary moment realization then proposes two positive substochastic matrices
from the same counts. The finite cover verifies both every retained-word
error and every terminal-prefix model survival. Since actual and model
survival decrease under a suffix, this certifies the two-state candidate
for EVERY word with error <=.062335817204, without additional source queries.
This closes an approximate coarse-model obligation. It does not identify the
physical source, bound its rank, or certify conditional survivor states or
lifetime moments. In particular, the fitted model's finite mean is compatible
with its approximation guarantee for a source whose true mean is infinite.

The new source also shows why inverse dissipation is not a universal target:
for finite word features and strictly stable computational maps, its centered
inverse residual forms diverge. An arbitrarily rare slow prepared component
can make those forms arbitrarily large while changing every observable word
probability by at most its small mass. A separate coupling theorem proves
that generic finite-confidence upper acquisition of those forms is impossible
over that unrestricted coarse class. Uniform prediction is a different,
less sensitive objective and remains possible.

COARSE_SWITCHING_THEORY.md provides ordinary proofs, exact costs and the
independent new reviews. The same-data old boxed scalar-echo certificate is
vacuous on these counts; that is not a lower bound against optimized convex
moment methods. The strongest adopted existing route is the ordinary positive
realization, now equipped with the finite acquired cover.

## The next attack resolves the generic cost question

Before relying on that new pipeline's bill, the continuation executed the
stronger familiar adaptive prefix comparator on the identical source and
interface. It uses independent fresh batches, selects the next word from
earlier results, and spends delta/[j(j+1)] confidence at visit j. At a prefix
whose upper survival is <=2epsilon, it predicts half that upper for every
extension. This preserves the same absolute-error target while ending branches
earlier than zero prediction.

The run obtained a 38-node cover, maximum depth five, with all-word error
1/16. It cost 458,449 source applications/reports and 255,220 preparations,
versus 1,086,180 and 540,672 for the balanced pipeline including its lifetime
phase. Each independent procedure has its own failure bound <=.001. This
adaptive predictor does not automatically certify the same two-state matrix
model, and its small terminal floor has no relative-tail or lifetime-mean
guarantee. For the shared absolute-survival task it is the best executed
route. ADAPTIVE_COARSE_COMPARISON.md records the fair comparison.

This particular emitted finite cover needs no lifetime pilot. The acquired
common energy profile supplies a class-level termination theorem, while
the instance certificate follows from actual prefix bounds. That theoretical
addition must not be credited with an operational saving produced by ordinary
adaptive estimation.

The exponential prefix obligation is not just an inefficient implementation.
A new hidden-coloring family has only four symmetric nonnegative controls,
one shared uniform preparation, and a supplied strict source norm cap
1-1/(20d). Every individual-action lifetime law is identical across its
hypotheses. A mixed word of length <=3d+2 reveals a particular hidden relation
with survival gap at least 1/5. There are 2^d-1 possible relations.

The ordinary adaptive-transcript proof shows that a reusable predictor with
all-word error <=1/16 and unconditional success >=2/3 must use at least
(2^d-1)/6 expected informative preparations and primitive applications.
Independent loss and destructive color tests limit each prepared trajectory
to a constant expected number of candidate relations. Fresh preparations
cannot retain the same hidden coloring. The proof allows adaptive controls,
stopping and resets; it grants full knowledge of the source family and gap.

A fully family-informed scan of the mixed witness words matches the
exponential acquisition scale up to polynomial and logarithmic factors.
Its preparation, source-time, report and future arithmetic costs are explicit.
The lower bound concerns successful reusable prediction; a certificate that
may abstain forever is not compelled to spend that cost. The enormous hidden
state space and exact access assumptions are stated in
COARSE_INTERFACE_LIMIT.md. This is a genuine limit of the coarse interface,
not a claim that existing convex or model-learning methods are weak.

The constructive response is an intrinsic context bound. If C_epsilon is
the size of a complete small-survival prefix cover, fresh adaptive estimation
can acquire an all-word predictor with preparation cost
O(C_epsilon epsilon^-2 log(C_epsilon/delta)), and source work also charging
the sum of context depths. Summable conditional confidence spending proves
almost-sure termination and bounds unconditional expected cost, including
rare confidence failures. The midpoint-terminal version obtains C_epsilon;
the zero-terminal version uses C_(epsilon/2). This is familiar prefix
estimation with a complete conditional cost theorem, not a universal shortcut.

These paired results change the agenda. Inverse dissipation is one useful
certificate, not a universal target. Output-sensitive certification can work
when it diverges. Efficient discovery of a small sufficient family of joint
contexts, or a physically justified operation exposing that information,
is now the load-bearing problem. The assignment's larger scientific mission
is not established by the present conditional constructions.

## Position relative to primary work

The closest existing ingredients include robust GNS and gate-set tomography;
Residual DMD and nonintrusive error estimation; boundary-wave Galerkin models;
dissipation perturbation and Julia dilation; switched-system reduction;
primal-dual corrected outputs; stochastic complementation and censored-chain
bounds; and exact or approximate Markov aggregation. The continuation also
inspects the March 2026 TrustKoopman methodology and July 2026 adversarial
Koopman learning results. SOURCE_NOTES.md and scoped branch comparisons give
the primary sources and access distinctions.

The candidate addition is the complete finite native acquisition and reuse
contract: local source forms at a genuine boundary, and common survival
profiles plus joint word coverage under a coarse interface. Estimated-model
transfer, complete costs, same-data competitors and explicit failed extensions
are part of that claim. Current weak-Poincare work already supplies the
functional-inequality mechanism, and current verified spectral learning
already handles important infinite-dimensional no-gap regimes. No novelty
claim rests on ignoring those capabilities.

Reliable composition can be controlled by acquired observable certificates
even when global hidden complexity is unbounded. Which certificate is useful
depends on the task metric and physical access; inverse dissipation is not
always finite or necessary. The remaining central obstruction is efficient
acquisition of joint contexts. A complete finite tree may grow exponentially.
The next strong method needs an experimentally checkable closure condition or
an additional physical operation that reveals joint information. A small
fitted model, by itself, does not supply that missing guarantee.
