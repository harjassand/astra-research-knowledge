# Learning intervention response without a hidden kinetic model

New construction, 25 October 2026 (Australia/Brisbane). Earlier cross-clock,
reaction-history and local-resolvent sources are preserved unchanged.

## 1. Question and information contract

The activity-ceiling obstruction is not repaired by estimating a maximum rate
from a finite endpoint record. Arbitrarily brief hidden excursions remain
possible. This construction instead acquires the response to a specified
class of interventions: competing irreversible captures, or persistent tags
whose first occurrence excludes a trajectory from the untagged-outcome count.

Let a native experiment have an arbitrary hidden, possibly non-Markovian path,
an almost surely finite stopping time tau, and a terminal native category
B in a finite alphabet. The stopping rule can be native completion or a fixed
experimental horizon with a distinct timeout category. The hidden state count,
generator, native reaction rates and native event record are not supplied.

There are r probe channels. Before the first probe hit, adding a nonnegative
dose vector c changes only the probe-hit intensity, to sum_j c_j b_j(t), where
b_j is a nonnegative predictable susceptibility along the native path.
The b_j may depend on the entire hidden history. Their values and their
absolute calibration are not supplied. The relative scaling by delivered dose
and the absence of other effects before the first hit ARE physical premises.
The added contacts are independently driven competing clocks conditional on
the potential native path (equivalently, independent exponential thresholds
on their integrated susceptibilities). This is part of the causal instrument
contract, not a consequence of observing a marginal contact intensity alone.
Each integrated susceptibility A_j=integral_0^tau b_j(t)dt is finite almost
surely; no upper bound or finite mean is assumed.

At acquisition the preparation is common across independently randomized dose
arms. The observed categories are the native outcome if no probe hit occurred,
and a distinct aggregate probe-hit category otherwise. A persistent hit tag is
sufficient: behavior after the first hit may be arbitrary because those
trajectories are excluded. If missed hits or category errors are possible,
their error contract must be supplied and paid in the probability intervals.
The executed prototype uses error-free categorical reporting.

This is not a general model of reversible inhibitors, saturation, allosteric
effects, changed native generators, or arbitrary treatment schedules. A probe
that binds reversibly and changes native kinetics before its first recorded
capture can violate the premise. Terminal times, if observed, are extra data
and may not be discarded in a comparison claiming the same information.

## 2. Exact obtaining of an interception kernel

Conditional on a complete native path, no probe hit has probability
exp(-c.A). Thus the native outcome subprobabilities are

    K_b(c) = E[1{B=b} exp(-c.A)] = integral exp(-c.a) mu_b(da),       (1)
    K_hit(c) = 1 - sum_b K_b(c),

where mu is the joint law of (B,A). This follows by independent exponential
threshold construction of the added capture clocks, or the usual killing /
Feynman-Kac identity. No independence between susceptibilities, terminal
categories, or different parts of the hidden history is used.

The acquired object is a set of possible JOINT measures mu_b. It is not a
claim to identify the native microscopic network or the physical rates b_j.
The integrated susceptibility has inverse-dose units. Calling it an exposure
TIME requires additional calibration of b_j.

Equation (1) is an established Laplace/frailty representation. The proposed
research contribution is an acquiring and obtaining operation around it:
data-acquired regularity, sound model-set decisions, actual positive finite
alternative processes, and explicit physical-interface failure tests.
Historical novelty is not established.

If a reference native CTMC is supplied for a CONTROL, with transient generator
Q, native absorbing rates R, entrance alpha and susceptibilities b_j(x), then

    K(c) = alpha [diag(sum_j c_j b_j)-Q]^{-1} R.                     (2)

This is an exact rational calculation for rational inputs. The main learner
does not receive Q, R, alpha's hidden coordinates or b_j.

## 3. Acquiring the regularity needed for reuse

Write L(h)=K_hit(h,...,h). For any nonnegative c,d with
||c-d||_infinity <= h,

    TV(K(c),K(d)) <= E[1-exp(-h sum_j A_j)] = L(h).                  (3)

Proof: couple the same (B,A) and one uniform survival threshold. Conditional
TV is |exp(-c.A)-exp(-d.A)|, bounded by
1-exp(-sum_j |c_j-d_j| A_j). Average and use the coordinate bound.
The result controls the whole native-outcome-plus-hit law, not only individual
coordinates. It has no hidden-state or outcome-count factor. Correlations are
retained, including in the weak mixed-probe experiment that measures L(h).

A weak challenge therefore directly measures a uniform continuity modulus
for the entire bounded-dose response family. It is not a bound on any native
reaction rate. No derivative, mean susceptibility or maximum susceptibility
needs to exist. Since each A_j is finite almost surely, dominated convergence
gives L(h)->0 as h decreases to zero.

### 3.1 Finite-data acquisition theorem

Fix a bounded dose cube [0,C]^r, target TV accuracy epsilon, and failure budget
delta. Test a dyadic sequence h_k=C*2^{-k} with independent repetitions and
summably allocated confidence budgets, using an upper confidence bound on the
binary hit probability L(h_k). Stop once that upper bound is below the chosen
modulus tolerance rho. Conditional on the common preparation and probe
contract, this stops after finitely many stages almost surely whenever all
A_j are finite almost surely, if sample errors decrease to zero. There is no
model-uniform upper bound on the required stage or number of experiments.

Measure the categorical output laws on a finite h_k-net of the dose cube,
with simultaneous TV error at most beta. Nearest-net prediction then has
uniform TV error at most rho+beta, on the acquired confidence event.
All further bounded losses/decisions may be evaluated on this same event.
The number of net points is exponential in r in general. This theorem proves
obtainability, not economical acquisition for a large number of channels.

If two coherent kernels fit every net law to TV beta and both satisfy the
acquired weak-probe bound rho, their distance over the whole cube is at most
2*beta+2*rho. A selected action for any loss in [0,1] then has regret at most
twice a uniform kernel-error bound. Extra representation slack is added
explicitly. Conditional predictions require a positive normalizer and amplify
error; they are not included free of charge.

### 3.2 Acquired tail bound

For S=sum_j A_j and any H>0,

    P(S>H) <= L(h)/(1-exp(-h H)).                                  (4)

Thus a weak challenge also acquires tightness of the response-relevant hidden
quantity. This is different from certifying a pointwise ceiling on kinetics.
Heavy-tailed susceptibility with infinite mean is admitted.

An instrument with a smallest realizable positive dose h_min may fail to
obtain a requested tolerance. Increasing numerical degree does not remove
this physical limitation. An atom at infinite susceptibility makes response
discontinuous at zero and prevents arbitrarily fine uniform acquisition.

## 4. Finite model sets without fitting a latent kinetic template

Set X_j=exp(-A_j), so X is in (0,1]^r. Dose experiments at integer coordinates
observe multivariate Hausdorff moments E[1{B=b} product_j X_j^{k_j}]. General
nonnegative doses observe continuous powers, using x^0=1 even at x=0.
The compact closure [0,1]^r includes infinite-susceptibility boundary models;
it is used only as a sound outer set. Weak-probe data control their mass.

The numerical outer compiler partitions [0,1]^r into rational boxes. It assigns
one nonnegative mass to each native-category/box pair, with total mass one.
For every data arm and box, coordinatewise monotonicity gives rigorous lower
and upper bounds on the power-product kernel. The resulting linear inequalities
are necessary for every underlying measure. Query bounds use the same lower
and upper cell values and rational LP dual certificates. These are outer
bounds at finite mesh. A single cell need not realize all its separately
allowed kernel endpoints. Vanishing mesh gives the sharp measure bounds for
each fixed finite family of continuous query functions by compactness.

The compiler does not turn a solver status into a proof. Numerical solvers
propose duals and sparse positive primal mixtures. Exact rational checks
include residual/box penalties and reject invalid reconstructions. Fractional
powers are enclosed by integer root tests. The retained files contain the
actual matrices, intervals, multipliers and positive mixtures.

The first executed cell relaxation gave unnecessarily broad query bounds,
including for nearby already-observed doses. Its checked operators and results
are retained. A joint Hausdorff moment representation was then added: with
base dose a and X_j=exp(-a A_j), each lattice dose a*k is one retained moment.
The compiler imposes all rectangular finite-difference positivity constraints
through the retained coordinate degrees. This shares each query value with its
actual data constraint instead of giving separate cell endpoints to the same
function. It remains an outer relaxation. Off-lattice weak challenges enter
through sound monotonicity and acquired-modulus inequalities, not invented
integer moments. No new observations are needed for this change of numerical
representation. The principal advance is the probe/inference interface and
obtaining theorem, not the chosen polynomial degree.

## 5. Positive finite conservative explanations

First suppose an atomic exposure explanation has weights w_i>=0 summing to one,
native categories b_i, and finite vectors a_i>=0. Its kernel is

    F_b(c) = sum_(i:b_i=b) w_i exp(-c.a_i).

For an integer n>=3, replace each atom by n native progression phases, each
advancing at rate n, with a probe-capture rate c.a_i in every phase. The last
native phase absorbs into b_i; capture absorbs into the hit category.
The hidden branch i is drawn at initialization with weight w_i. This is a
finite homogeneous conservative CTMC, with a probe-independent native
generator and probe-linear capture rates. It has kernel

    F_b^(n)(c) = sum_(i:b_i=b) w_i [1+c.a_i/n]^{-n}.                 (5)

For all nonnegative dose vectors, simultaneously,

    TV(F^(n)(c),F(c)) <= d_n
      = (2/n)(1-2/n)^(n-2) <= 2/n.                                (6)

Proof: for z>=0, let d=z-n*log(1+z/n). Then 0<=d<=z^2/(2n), and

    0 <= (1+z/n)^(-n)-exp(-z)
       <= (z^2/(2n))(1+z/n)^(-n).

The last expression is maximized at z=2n/(n-2), giving d_n. Each native
category gains nonnegative mass and the hit category loses their sum, so
whole-law TV is their total, at most d_n. No number-of-atoms, hidden states,
probe channels, maximum susceptibility or dose factor appears in this bound.
The globally uniform certificate is relative to the obtained atomic kernel;
it does not infer unknown responses at unlimited doses from finite data.

Finite exposure mixtures approximate arbitrary finite-A kernels uniformly on
bounded dose sets: truncate a tail of probability eta, discretize the compact
remaining exposure set, and use uniform continuity. Rational atoms and weights
are dense. Combining this with (6) gives finite conservative explanations
arbitrarily close on every bounded dose set. If data intervals have a strict
feasibility margin, enumerating finer rational exposure grids and increasing
n eventually obtains a model inside the ORIGINAL intervals. With no margin,
one can guarantee only declared approximation slack; boundary cases need not
terminate. This is not unique microscopic mechanism identification.

The phase construction above realizes outcome-only NATIVE-COMPLETION assays;
it does not preserve a separately supplied distribution of completion times.
For a FIXED readout horizon T, an atomic kernel has a different exact finite
assay realization: keep latent type (b_i,a_i) fixed, capture at rate c.a_i/T,
and read b_i at T if uncaptured. This is a conservative CTMC with an output
map, not a reconstructed physical product-formation pathway. If initial
product states, reaction ordering or intermediate readouts are additionally
specified, those constraints must be respected by a further construction.

The prototype also obtains phase mixtures directly by linear programming:
for fixed rational atoms and n, every kernel value in (5) is rational at a
rational dose. The actual weights and generators can therefore be checked
exactly. Phase states are mathematical explanatory memory, not experimentally
identified conformations. Terminal timing distributions are not certified by
an outcome-only fit.

## 6. Revealing failures and method controls

### 6.1 The fast-cascade ambiguity survives correctly

A direct completion that never exposes a trap has response 1. A serial
completion that exposes the trap for an Exp(M) residence has response
M/(M+c). On 0<=c<=C their difference is at most C/(M+C), tending to zero
without a bound on M. No finite-dose experiment can certify an atom of exactly
zero exposure against all arbitrarily short positive exposures. The new
operation learns interceptibility within a stated dose range, not an assumed
rate separation or proof of concerted chemistry.

### 6.2 Single-probe curves do not determine combination response

Two conservative finite models have an Exp(1) native completion clock.
Model P is half fully protected, half susceptible to both probes at unit rate.
Model A is half susceptible only to probe 1, half only to probe 2. Both have
the same response (1+1/(1+c))/2 on either single-probe axis, for EVERY dose.
At c=(1,1), model P gives 2/3 and model A gives 1/2. Joint challenge experiments
are necessary. A strong comparator receives those experiments and retains
the same correlations.

### 6.3 A valid-looking response curve does not establish probe innocence

Take native completion rate 1+c and probe rate c. Completion probability is
(1+c)/(1+2c). Every constant-dose value agrees with an innocent mixture:
half immune, half with native rate 1/2 and probe rate c. Thus even the ENTIRE
constant-dose curve cannot certify that native kinetics are unchanged.
For a unit-dose pulse lasting one time unit, followed by no probe, the two
models instead give 1-(1-exp(-3))/3 and 1-(1-exp(-3/2))/3. They differ.
The native-perturbation model violates the construction's contract; positive
moment tests can falsify some violations but cannot establish that contract.
Constant-dose data also do not acquire arbitrary time-order information.

Nor does a marginal contact intensity establish an added competing clock.
Consider an Exp(1) native completion event, tagged with probability c in [0,1].
The tag-event intensity while native completion is pending is c, and no earlier
perturbation occurs. Yet untagged completion has probability 1-c. An independent
competing clock of rate c would instead leave probability 1/(1+c). At c=1/2
these are 1/2 and 2/3. Marking pre-existing native events is therefore outside
the added-clock contract even when the marginal intensity agrees. This is an
exact analytic control; no new observations are generated for it.

### 6.4 Reuse of the previous positive realization as a method control

The previous obtained phase generator can be given a native completion exit
and probe susceptibilities. Equation (2) then checks the new compiler against
an actual retained positive operator. This uses existing code and operators;
it does not regenerate the earlier observations or recover missing files.

## 7. Scientific scope and antecedents

Laplace/frailty representations, Feynman-Kac killing, nonparametric mixture
inference, Hausdorff moment constraints, occupation-measure optimization and
Erlangization are prior scientific machinery. In particular, nonparametric
competing-risk/frailty identification already retains dependent latent risks;
it is not an independent-marginal baseline. Recent multivariate Erlang-mixture
work also proves constructive approximation results. The present proposed
capability is the obtained experimental-response family and data-acquired
regularity, with finite-data model sets and conservative alternative processes.
No architecture exclusivity, historical priority or matched performance
advantage is claimed.

The physical class motivating the construction is interception of reaction
completion by selective traps or irreversible footprinting. Established
enzyme processivity assays already use traps. Their interference must be
checked: trap binding can alter motor behavior, and a trap can incompletely
prevent rebinding. A published trap assay is not automatically an acquisition
of the contract in Section 1. Source-specific findings and executed results
are appended after their actual retrieval/calculation.

## 8. Allowing probe-induced changes after unrecorded contacts

The strict pure-capture premise can be weakened in a way that is directly
connected to a reporting instrument. Define a probe CONTACT as any interaction
that can change native dynamics or produce a persistent tag. Before the first
contact, the native law is unchanged and the total first-contact intensity is
sum_j c_j b_j(t). At the first contact, conditional on every prior history and
the contact type, a persistent tag is produced with probability at least
q>0. No assumption is made about dynamics after an untagged contact, including
native acceleration, coupled reactions, further contacts or changed completion
times. A tag overrides the terminal native category in the acquired record.
The actual experiment must still return a recorded category almost surely;
a finite-horizon timeout is one way to guarantee this. All added first-contact
clocks obey the independent competing-clock contract of Section 1.

This contract does not follow from marginal detection efficiency in a separate
calibration population. The coverage q must apply to the relevant FIRST
contacts, including contacts that could perturb the system. It can be an
instrument/design guarantee or an independently justified bound. Neither a
positive fitted kernel nor the present synthetic experiment acquires it.
Diffuse dose-dependent effects not covered by such contacts remain outside
the theorem.

Let K(c) be the ideal NO-CONTACT outcome law: its hit category stops at the
first contact, whether tagged or not. It still has representation (1). Let
D(c) be the ACTUAL recorded law, R(c)=D_hit(c), and H(c)=K_hit(c). Then

    q H(c) <= R(c) <= H(c),
    D_b(c) = K_b(c)+u_b(c),  u_b(c)>=0,
    sum_b u_b(c) = H(c)-R(c) <= (1-q)H(c),                         (7)
    TV(D(c),K(c)) = H(c)-R(c) <= [(1-q)/q] R(c).                    (8)

Proof: until the first contact, actual and ideal experiments can be coupled
exactly. No-contact trajectories contribute the same native category. A tagged
first contact is included in the observed tag category and occurs with
probability at least qH. Only an untagged first contact can add an untagged
native outcome that the ideal law would have killed. Subsequent behavior is
irrelevant to these inequalities. All native differences have one sign, so
the whole-law TV identity in (8) is exact.

Consequently a weak mixed-probe observation supplies

    H(h,...,h) <= R(h,...,h)/q,                                    (9)

which acquires the regularity/tightness of the ideal no-contact kernel even
when unrecorded contacts alter the native system. At any untested dose, the
actual native category is bounded by

    K_b(c) <= D_b(c) <= K_b(c)+(1-q)H(c).                          (10)

The residual width is material. The construction does not grant that arbitrary
native feedback after an untagged contact has been learned.
In particular, for ||c-d||_infinity<=h, the triangle inequality gives only

    TV(D(c),D(d)) <= H(h,...,h)+(1-q)[H(c)+H(d)].                  (11)

When empirical tag bounds are available, the R-based bound in (8) supplies
another valid upper bound on each disturbance term. Unlike the ideal kernel's
modulus, (11) need not tend to zero as d approaches a nonzero c when q<1.
A fixed imperfect contact contract
therefore does not inherit arbitrary-accuracy acquisition of the full ACTUAL
response family. It gives the ideal kernel and the explicitly bounded residual
outcome freedom. The q=1 finite-acquisition theorem is not silently extended
past this residual by increasing moment degree or repetitions.

Equations (7) are linear at every acquisition dose: introduce leakage variables
u_b>=0, constrain observed probabilities K_b+u_b to their acquired intervals,
and impose sum_b u_b <= (1-q)(1-sum_b K_b). Thus the unknown-contact extension
fits the retained moment programme without a hidden reaction template. The
programme provides sound bounds on an ideal no-contact kernel and actual
outcome envelopes. Free leakage variables at separate doses do NOT by themselves
constitute an obtained conservative marked process with common post-contact
kinetics. The explicit conservative explanations in Section 5 are for the
ideal kernel; in the q=1 execution they are also actual assay explanations.

### 8.1 Exact saturation control

The noninnocent example of Section 6.3 has a first probe-contact intensity 2c.
A contact is tagged with probability q=1/2 and otherwise immediately completes
the native reaction. Hence

    K_native(c)=1/(1+2c),
    D_native(c)=(1+c)/(1+2c),  R(c)=c/(1+2c).

Equation (8) is saturated at every c. At c=1, the actual native probability is
2/3, whereas the no-contact probability is 1/3. The contact-aware moment
programme admits the correct no-contact value; treating every untagged outcome
as unperturbed would be unjustified. This example is a finite conservative
reaction process, not just a positive record-likelihood construction.

## 9. Primary source conditions that changed the construction

Gyimesi, Sarlos, Derenyi and Kovacs, *Streamlined determination of processive run
length and mechanochemical coupling of nucleic acid motor activities*, Nucleic
Acids Research 38 (2010), e102, DOI 10.1093/nar/gkq014, was read through the
indexed primary full text. The section on the protein trap explicitly treats
heparin effects on processivity, generally through increased dissociation and
potentially altered translocation rates, and models trap-bound and trap-free
motor behavior. It therefore does not supply the pure-capture premise.
https://pmc.ncbi.nlm.nih.gov/articles/PMC2853143/

The related BLM translocation paper uses high-time-resolution nucleotide and
DNA-interaction observations and a quantitative mechanistic model:
https://doi.org/10.1093/nar/gkq145 . These are substantial experimental tools,
not an incumbent forced to use only independent endpoint marginals. The
present proposal receives outcome-only probe experiments and returns weaker,
robust response sets. It does not replace those measurements or claim to
identify BLM's native microscopic cycle. No heparin contact-coverage q was
acquired from these publications.

Abbring and van den Berg's primary mixed-proportional-hazard competing-risk
identification work explicitly retains dependent frailties and studies when
covariate variation identifies them. It is a close antecedent, with different
identification and observation contracts:
https://papers.tinbergen.nl/00066.pdf .

Sanguesa's uniform gamma/Erlang approximation work and Nguyen's 2026 constructive
multivariate Erlang-mixture approximation results rule out a claim that
positive phase approximation or latent-mixture representation is new here:
https://arxiv.org/pdf/1010.2066
https://arxiv.org/html/2603.18506v1 .

The new organizing candidate is acquisition of an operation-specific response
class and its regularity from interventions, with a local first-contact
reporting contract replacing a global native activity ceiling. It does not
establish historical priority for every constituent lemma or the combined
operation, and a conventional scientific programme can adopt it.

The Astra orientation was read at revision
8fe0ad7e53068f3e0da26f51705faeb2700a1d52. Previously read governing local-island
and cross-clock sources supply no probe noninterference, q-coverage, or native
preparation promise used here. No such premise is silently imported.

## 10. Compactness of scientific operations, not of the hidden world

For a declared dose cube C, define the operational distance between two joint
exposure/outcome laws by sup_(c in C) TV(K_mu(c),K_nu(c)). This is generally
much weaker than total variation of the hidden exposure laws themselves.
For any nonzero atom a, the deterministic law delta_a and the exposure law
a*S_n with S_n~Gamma(n,n) are mutually singular: S_n equals one with probability
zero. Their hidden-law TV distance is one at every finite n. Nevertheless,
their complete response kernels are at distance at most d_n from Section 5,
uniformly over every nonnegative dose. Approximation in the scientific
operation's metric is therefore possible even when the hidden distributions
are not close in a stronger metric.

This is why the representation is useful without being the microscopic truth.
It does not license a new measurement of A, a new reaction-history predicate,
or a different intervention outside the acquired family. Such operations can
distinguish the hidden alternatives and need new information.

Conversely, the relevant regularity cannot simply be assumed for free. For
deterministic susceptibilities A=M and A=2M, any fixed collection of strictly
positive doses bounded below by c_min has exponentially small response in both
worlds when M is large. At the unmeasured dose 1/M, their survival probabilities
are exp(-1) and exp(-2). Thus no fixed positive-dose resolution uniformly
acquires the whole response curve down to zero over the unrestricted class.
The weak-probe acquisition is an information operation, not a sharper numerical
constant. It discovers when the instrument has reached a sufficient resolution.

The finite acquisition theorem counts completed experiments. If native stopping
times have infinite mean, its expected elapsed laboratory time may be infinite,
even though each finite acquisition finishes almost surely. A fixed horizon
with an explicit timeout category bounds trial duration but changes the target
kernel. Probe dynamic range, minimum dose, mixing time, preparation and reporting
costs remain physical resources.

### Repeated use

On one simultaneous statistical confidence event, any number of later model-set
queries is sound without another statistical allocation. New observations need
an appropriate additional or time-uniform confidence construction. Reusing an
approximate positive kernel over N freshly prepared experiments is different:
if each admissible input law is approximated to TV epsilon, a sequential
coupling bounds the joint record error by min(1,N*epsilon), including dose choices
adaptive to earlier outcomes. This assumes the same acquisition/preparation
contract at each experiment. The theorem does not cover repeatedly perturbing
one continuing physical molecule with arbitrary feedback. Conditional record
queries require a normalizer bound and amplify error near rare events.

## 11. Executed acquisition, decision, failure and verification

The new synthetic acquisition fixes a five-state recurrent hidden transient
network, two native terminal categories and two capture channels. The entire
native network and all susceptibilities are withheld from the learner. Twelve
dose arms were fixed before execution: the 3x3 grid {0,1,2}^2 and weak mixed
doses (1/8,1/8), (1/32,1/32), (1/128,1/128). Each has 12,000 independent
categorical draws, seed 2026102503. These 144,000 draws are synthetic data,
not physical observations. Exact rational absorption laws drive integer
pseudorandom sampling. Event paths and terminal times are not generated.

The learner retains one simultaneous 95% Hoeffding family for the 36 categorical
probabilities. It has no source-network input. Query choices, numerical
representations and q-coverage hypotheses reuse that same confidence event;
they do not claim an additional statistical sample.

### Acquired regularity

The weakest mixed challenge produced 174 recorded hits in 12,000 trials. Its
outward upper probability is 0.03190737199264779. Under the pure-capture contract,
this certifies whole-outcome TV change <=0.0319074 whenever every dose changes
by at most 1/128. The same data give

    P(A_1+A_2 > 128) <= 0.06381474398529557,

using the rational bound 1-exp(-x)>=x/(1+x). This is a tail guarantee in
inverse-dose susceptibility units, not an acquired time or native rate bound.
Under q-coverage, the ideal-kernel modulus is inflated by at most 1/q.

The known-answer infinite-mean mixture in the control script has latent class
m of probability 2^(-m-1), native completion rate 4^(-m), and unit probe rate
per dose. It has finite susceptibility almost surely but infinite mean. Exact
finite-sum/tail enclosures give weak hit upper bounds about 0.25230 at dose
1/16 and 0.004419 at dose 1/65536. The regularity acquisition does not assume
the finite moment that this control violates.

### A decision at an unmeasured intervention

Under pure capture, the joint moment set bounds full-product probability at
the unmeasured combination (5/4,3/4) by approximately

    [0.24142925, 0.32112634].

Joint optimization over the SAME retained model set certifies that this
combination lowers full-product probability relative to every pure probe-1
dose in [0,2] by at least 0.01965585, and relative to every pure probe-2 dose
in [0,2] by at least 0.03688296. The extension from pure dose 2 to smaller
pure doses uses monotonicity of the ideal no-contact kernel. This is a
functional interception decision, not a claim of a unique biochemical pathway.

When arbitrary post-contact changes are allowed with first-contact reporting
coverage q>=0.99, the corresponding certified advantages are still positive,
at least 0.00758110 and 0.02471890. At q>=0.95, this computation does not
certify the decision: its lower bounds become negative. The coverage values
are CONDITIONAL instrument hypotheses, not estimates from these assay counts.
The executed source has q=1. It supplies no physical heparin or other probe
coverage calibration.

The selected measured combination (1,1) has full-product upper bound about
0.305825. A convexity-based lower bound on the optimum over every split of
total dose two is only about 0.172884, leaving a regret certificate about
0.132940. Thus a near-optimal dose allocation has NOT been established. The
certified dominance of an unmeasured mixture over pure probes is the stronger
decision currently justified.

### Positive explanations and numerical limitations

Two explicitly retained 32-phase mixtures, each with 11 hidden branches,
fit every ORIGINAL acquired probability interval exactly. They are actual
conservative processes with dose-independent native progression and dose-linear
capture rates, encoded by their weights, capture coefficients, phase rates and
terminal categories. Their full-product probabilities at the unmeasured
(1/2,3/2) are about 0.257076 and 0.346493. They demonstrate the obtaining
operation and compatibility with the declared confidence object; equal
likelihood or intrinsic information-theoretic indistinguishability is not
claimed. Their atom-to-phase whole-kernel certificate is d_32<0.009017 for all
nonnegative doses. Fitting the phase model itself to the acquired intervals
is checked directly and does not spend this representation error again.

The first cell-mass relaxation was sound but too loose for a useful continuum
decision; its first lower envelope was zero. The cell operators, results and
verification are preserved with the `_cells` suffix. The joint moment programme
is the current numerical representation. No claim of practical superiority
over nonparametric frailty likelihood, general moment/SDP, imprecise-process,
trajectory or tensor implementations has been measured. They receive all
crossed dose experiments and correlations used here.

### Verification and entry points

`interception_learning.py --verify` rebuilds the confidence object from counts,
checks 26 rational dual certificates, both exact positive-process primal fits,
and the convex continuum decision calculation. `--verify-contacts` checks ten
further rational certificates and an exact common-moment/primal witness for
the genuinely perturbing q=1/2 control. Its acquired no-contact probability at
unit dose is [1/3,2/3], containing the true 1/3; the actual recorded completion
probability is 2/3. The bound (8) is saturated.

`interception_reference.py --score` is separate reference-only scoring; all
source probabilities fall within the acquired confidence intervals and every
certified query contains the reference value. `--controls` checks the retained
old positive operator, the cascade, correlated-probe ambiguity, native-
perturbation counterexample, phase bound and infinite-mean example. The old
positive operator's base-clock law is recovered exactly. These are executed
finite checks, not independent proof review, physical validation or a benchmark
against the strongest incumbent implementation.

The original count file is protected against accidental regeneration by the
reference acquisition command. The proof and three new scripts use the existing
available `hidden_mechanism_occupation.py` and `local_resolvent_learning.py`.
The missing historical helpers remain missing and are not imported.
