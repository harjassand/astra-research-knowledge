# Operational transport: independent theorem and obstruction audit

Date: 23 October 2026. Native agent: /root/verification_primitive.

This is an independent mathematical audit of the construction in
[CONSTRUCTION.md](../CONSTRUCTION.md). The central theorem and the reversible
guard extension are valid with the conditions below. They warrant operations
on an explicitly represented distribution; they do not establish exact
membership in an unknown source class. Historical novelty and practical
advantage remain **UNKNOWN**. No external priority review was performed for
this bounded task.

The most consequential limits are:

1. The initial-state density bound must hold **conditional on the chosen
   program and past information**. State-based program selection can otherwise
   cause failure probability one while every action has tiny uniform error.
2. A new operation must preserve the reference measure, not merely remain
   inside its support.
3. An invariant fiber need not be a reachable orbit or a scientifically
   meaningful externally labeled level set.
4. A finite audit controls disagreement in measure. Exact conservation and
   unlimited-horizon correctness do not follow.
5. A strong retaining program/library learner can implement the same chart,
   sampler, fit, audit, and warrant composition. No separation from that
   baseline is established.

## 1. Access and version contract

Let S be a finite, explicitly represented nonempty subset of the raw state
space X, and let mu be uniform on S. A candidate encoder E is a proved
bijection from a finite sampling space onto S. Sampling that space uniformly
and evaluating E must actually be available and charged. A source query
returns the complete, exact successor F_a(x) for any requested x in S.

Each F_a:X -> X is a fixed deterministic function during the warrant's
lifetime. It may be noninvertible and may leave S. Each candidate
P_a:S -> S is a proved permutation. Candidates, source semantics, the chart,
the support S, and the comparison operation are bound to the audit.

This is a reset-and-read access model. A mathematical ability to name x does
not supply a physical ability to prepare it, observe the full state, suppress
an intervention, or repeat the same source law. Those are separate
requirements of an application. All source calls, preparations, failed fits,
training, program checks, arithmetic, and random-bit costs belong in the
end-to-end comparison.

Write

\[
 E_a=\{x\in S:F_a(x)\ne P_a(x)\},\qquad e_a=\mu(E_a).
\]

## 2. Fresh audits give a frequentist warrant

Fix a candidate and support using arbitrary prior information. Conditional
on that information, draw m fresh iid points from mu and compare the complete
source and candidate outputs. Accept only if every comparison agrees. Then

\[
 \Pr(\mathrm{PASS})=(1-e_a)^m.
\]

Therefore, for any 0<epsilon<1,

\[
 \Pr(\mathrm{PASS}\ \text{and}\ e_a>\epsilon)
 \le (1-\epsilon)^m \le \exp(-m\epsilon).                 \tag{1}
\]

The sufficient exact sample count is

\[
 m\ge\left\lceil\frac{\log\delta}{\log(1-\epsilon)}\right\rceil;
\]

the conservative count ceil(log(1/delta)/epsilon) also works. After m zero
failures, 1-delta^(1/m) is a one-sided upper confidence bound. This is a
frequentist false-warrant guarantee, not a posterior assertion that a fixed
source has probability delta of being bad after PASS. A source can have
positive error and fail the audit frequently; tolerant completeness is not
claimed.

Sampling without replacement only reduces the miss probability for a fixed
error set. A census certifies exact agreement on S. Fresh random indices
sampled with replacement may repeat; a deterministic source output already
cached at that index can be reused without another source call. Repeating a
chosen old index does not by itself create a fresh uniform audit sample.

### 2.1 Adaptive libraries

At stage s, the support, candidate, epsilon_s, sample size, and confidence
allocation delta_s may depend on all earlier information. The audit draws at
that stage must be fresh conditional on that information. If
sum_s delta_s <= delta almost surely, conditioning on the pre-audit history
and applying (1) gives

\[
 \Pr(\text{any false warrant is issued})\le\delta.          \tag{2}
\]

This handles adaptively requested actions, fibers, and observables. A finite
or countable later set of programs built deterministically from valid
warrants does not need another statistical union bound when the relevant
error-containment statements are uniform over those programs.

Repeatedly trying a one-sample audit until PASS without spending confidence
is invalid. For X={0,1}, candidate identity, and true F identically zero,
the error is 1/2. A one-sample audit passes with probability 1/2; after K
independent attempts it has passed with probability 1-2^(-K), tending to one.

An oracle that changes its source function after seeing audit inputs also
falls outside the contract.

## 3. The open-loop transport theorem

Let w=(a_1,...,a_T) be fixed before a fresh initial state is drawn. More
generally, conditional on all information used to choose w, suppose

\[
 \nu(x)\le\rho\mu(x)\quad\text{for every }x\in S.           \tag{3}
\]

Run the source path X and candidate path Z from the same initial state:

\[
 X_t=F_{a_t}(X_{t-1}),\qquad
 Z_t=P_{a_t}(Z_{t-1}),\qquad X_0=Z_0\sim\nu.
\]

Every candidate prefix is a permutation of S. Thus
Pr(Z_t=x)<=rho*mu(x) for every t. If the paths first disagree at step t,
then Z_(t-1) belongs to E_(a_t). Taking the union of these events under the
**unconditional candidate path**, rather than conditioning the true path on
previous agreement, gives

\[
 \Pr((X_0,\ldots,X_T)\ne(Z_0,\ldots,Z_T))
 \le\min\left(1,\rho\sum_{t=1}^T e_{a_t}\right).           \tag{4}
\]

On the common valid-warrant event in (2), e_a may be replaced by epsilon_a.
Nothing in this proof assumes that F_a preserves S or its measure.

The induced total variation distance of the complete path laws is bounded
by (4). In this deterministic setting, when the initial state is part of the
path, this same-start coupling actually realizes that path TV distance:
paths from different initial states cannot be confused, and at each initial
state the two deterministic paths either agree or do not. Terminal-state
TV can be smaller because paths may later merge.

Every [0,1]-valued measurable statistic of the complete finite path inherits
the same expectation error bound. This includes finite-horizon hitting
indicators and the state selected by a bounded stopping rule of that fixed
path. It does not prove a bound for an unbounded expected stopping time.

### 3.1 What is simultaneous

Once the deterministic masses e_a are bounded, (4) is true for all words,
all finite horizons, and all initial distributions satisfying (3). A later
word may be chosen from old audit results or previous completed rollouts.
The new initial state must still obey (3) conditional on that selection.

No confidence penalty is paid again merely for using a warrant. The
dynamical error budget is paid on every use. For several future rollouts,
a bound on the probability of any disagreement is obtained by summing their
per-rollout budgets and adding the common audit failure probability.
Selecting the first failed rollout does not turn the original per-rollout
guarantee into a guarantee for the selected rollout.

For a specified deterministic initial state, rho=|S| is always sufficient
and is often useless. A direct source execution of a known T-step trajectory
costs T source transitions and is an essential baseline for that task.

### 3.2 The additive budget is sharp

Let X=Z_N, P(x)=x+1 mod N, and let F equal P except F(0)=0, with N>=2.
For T<=N the complete paths disagree exactly for starting states
0,-1,...,-(T-1), so their error is T/N. The one-step error is 1/N.

Consequently, a product replacement
1-(1-1/N)^T can be too small. The bad events at successive candidate
prefixes can be disjoint, rather than independent.

### 3.3 Conditioning costs probability mass

A rare-event probability receives an absolute error guarantee from (4), not
a free relative error guarantee. If path laws have TV at most eta and both
assign a conditioning event A probability at least p>0, then their conditional
laws on A have TV at most min(1,eta/p).

For completeness, let alpha=P(A), beta=Q(A), and assume beta>=alpha.
The common unnormalized mass inside A is at least beta-eta. After
normalization its common mass is at least (beta-eta)/beta, proving the
stronger bound eta/max(alpha,beta). The safe eta/p statement follows.
Thus choosing a stopping event of tiny probability can restore a rare-mass
penalty even though the bounded stopping-time statistic itself was covered.

## 4. Feedback is a real obstruction

### 4.1 Failure in one step, even with a measure-preserving combined candidate

Let X=Z_N, N>=2. For every action a in X, let P_a be identity. Let F_a
equal identity except F_a(a)=a+1 mod N. Each uniform error is 1/N.
Choose action a=X_0 after seeing the uniformly distributed initial state.
The source and candidate disagree with probability one.

The combined candidate policy is still identity and preserves uniform
measure. Nevertheless its selected error set is the union of the errors
selected by the state. Neither max_a e_a nor an action-frequency-weighted
average of the e_a controls it.

### 4.2 Exact steering can concentrate a later rare error

On Z_N, retain every exact translation P_j(x)=F_j(x)=x+j. Also retain a risky
identity candidate whose source fails only at zero. After observing X_0,
choose translation j=-X_0, followed by the risky action. Failure is certain.
The word is fixed before the first transition, but was selected using its
initial state. Conditional on the selected translation, the initial law
has density N, not one.

Similarly, merely requiring a new candidate to remain in S is insufficient.
An exactly learned compressor P(x)=F(x)=0 followed by the risky identity
action stays in S but fails surely. The compressor does not preserve mu.

### 4.3 The correct feedback quantity

For a candidate policy, the first-error argument always leads to its
candidate occupation probability of the selected error relation:

\[
 \sum_t\Pr\{Z_{t-1}\in E_{A_t}\}.                          \tag{5}
\]

Statewise selection can change both the occupation distribution and which
error set is inspected. A fixed policy can be given its own error audit and
a proof that its candidate transition preserves mu. Per-action marginal
audits alone only bound the mass of a selected union by sum_a e_a.
Known density-amplification or conditional-error bounds can also repair (5),
but those are additional acquired or proved contracts.

## 5. Reversible guards are a valid restricted intervention compiler

Work in coordinates y in GF(2)^n, and let b be nonzero. Define

\[
 T_{b,f}(y)=y+b f(y),
\]

where f is Boolean. On each pair {y,y+b}, this map is a permutation if and
only if f(y+b)=f(y): it either fixes both points or swaps them. It is then
an involution.

Given a Boolean guard g, define h=fg. The guarded candidate

\[
 T_{b,h}(y)=y+b f(y)g(y)                                  \tag{6}
\]

is a permutation if and only if h(y+b)=h(y). The guard g itself need not
be invariant on pairs where f is zero.

The corresponding source intervention evaluates the same exact guard and
applies the original F_a only when g=1; otherwise it performs identity.
Its mismatch set is exactly

\[
 E_{a,g}=E_a\cap\{x:g(Rx)=1\}\subseteq E_a.                \tag{7}
\]

If (6) is structurally certified and preserves the intended fiber, (7)
transfers the old epsilon_a warrant. Every fixed sequence of such guarded
operations satisfies (4). This gives useful state-dependent interventions
whose candidate maps retain the sampling law.

The guard can be chosen after the original audit, even using its data:
the error containment is true simultaneously for every guard, so this
specific derivation does not overfit the audit. However, selecting WHICH
guarded operation to run from the fresh state is still feedback. Either
the combined candidate operation and its error containment must be
certified, or the earlier limitations apply.

A piecewise operation selecting among different source actions has errors
contained in their union; it does not automatically inherit just one
action's epsilon. A noisy guard, a changed chart, different source semantics,
or an unavailable physical no-op breaks (7) unless separately accounted for.

Every affine fiber y_0+B is preserved when b belongs to B. Checking
shift invariance by canonical polynomial expansion can be expensive;
constructing f and g from coordinates complementary to b supplies a cheaper
sufficient certificate. These computational costs are not free.

## 6. Acquired fibers and exact conditional sampling

The Boolean extension needs a proved chart R:X -> GF(2)^n, so here
|X|=2^n. An arbitrary finite X does not automatically have this form.

For a candidate action in coordinates, write its displacement in the
canonical multilinear Boolean algebraic normal form:

\[
 P_a^R(y)+y=\sum_{A\subseteq[n]} v_{a,A}\prod_{i\in A} y_i.
\]

Boolean monomials form a basis for Boolean functions. A parity c^T y is
invariant under all candidate actions if and only if
c^T v_(a,A)=0 for every a,A. Let B be the span of these coefficient vectors;
rows of a matrix C spanning B-perp are therefore exactly the common linear
parities of these maps.

For individual nontrivial shears the coefficient vectors are either zero
or the update direction b, so spanning the nonzero action directions gives
the same conclusion without expansion. If the retained library contains
only compositions of many shears, spanning every internal gate direction
is sufficient but can miss invariants created by net cancellations.
Completeness from polynomials requires canonical reduction modulo
y_i^2=y_i; raw formal coefficients need not expose all cancellations.

If rank(C)=k and Cy=beta is consistent, solve it over GF(2), obtaining a
particular y_beta and a basis N for ker(C). Then

\[
 z\mapsto R^{-1}(y_\beta+Nz),\quad z\in\mathrm{GF}(2)^{n-k} \tag{8}
\]

is a bijection onto the explicit fiber S_beta. Uniform independent bits z
therefore sample it exactly. Its ambient mass is 2^(-k); direct sampling
does not reject ambient states and has no inverse-mass factor.

The costs include elimination, basis storage, n-k fresh random bits,
coordinate arithmetic, R inverse, and actual source preparation. Standard
single-coordinate shears updating every independent direction often span
the entire space; then C has no rows and there is no nontrivial rare fiber.
A useful invariant is a result to acquire, not an automatic consequence
of using polynomial programs.

Each candidate permutation preserving S_beta restricts to a permutation
of it. Directly auditing with (8) and applying (4) gives a local guarantee
with error masses e_(a,beta), without assuming that true actions preserve
the fiber.

### 6.1 A fiber need not be an orbit

On GF(2)^2, the shear (y_1,y_2) -> (y_1+y_2,y_2) preserves y_2.
The fiber y_2=0 contains two separate fixed points. Neither can reach the
other. The correct term is an explicit invariant fiber containing a given
state. Reachability, ergodicity, or a hidden physical charge interpretation
requires additional evidence.

Reset access to every point in (8) can sample the entire fiber even when
the dynamics cannot traverse it. Natural trajectory access alone does not
provide that reset capability.

### 6.2 Where the rare-mass benefit comes from

Suppose S_beta has ambient mass p and a source differs from its candidate
on an epsilon fraction of that fiber, with no error elsewhere. An ambient
uniform zero-failure audit misses all errors with probability
(1-p*epsilon)^m. A direct fiber audit misses them with probability
(1-epsilon)^m.

The changed acquisition distribution removes the 1/p cost. No inference
from the same global observations can justify that removal for arbitrary
sources: until an error input is queried, the clean and corrupted sources
give the same transcript. The precise claim is conditional access to the
explicit raw subset, not recognition of a latent true-rank fiber.

Different future fibers require fresh local audits, a simultaneous
all-fiber argument, or valid transfers of existing warrants.

## 7. Acquiring a further action or observable

Let r be the fiber dimension in (8). For an unknown Boolean observable
H(z), query all z of Hamming weight at most e. There are

\[
 M_e(r)=\sum_{j=0}^{\min(e,r)}\binom rj
\]

such inputs. For each |A|<=e, Boolean Möbius inversion gives

\[
 c_A=\bigoplus_{D\subseteq A}H(1_D).
\]

The degree-at-most-e polynomial with these coefficients is the unique
candidate matching those fitting inputs. If the actual H has that degree,
it is recovered everywhere. Without that promise, this remains only a
candidate. For example H(z_1,z_2)=z_1*z_2 is zero at every point of weight
at most one; a degree-one fit returns zero and errs on one quarter of
the cube. A fresh local audit supplies the operational warrant.

Interpolating output coordinates of a new action does not by itself make
the map a permutation. For a safe shear, choose a nonzero direction b in
the fiber, take b as the first basis vector, and fit its control using only
the other r-1 coordinates. The resulting control is automatically invariant
under translation by b. Still audit the **complete raw successor** over
the whole fiber, including both values of the b coordinate. A source need
not actually move in direction b, satisfy the degree hypothesis, or remain
inside the fiber.

A fiber permutation can be extended by identity outside that fiber to give
a global permutation. This is a legitimate new library operation only
with the corresponding source-intervention semantics and fresh warrant.

For an audited Boolean terminal observable with local error epsilon_H,
the prediction disagreement bound becomes

\[
 \rho\left(\sum_t\epsilon_{a_t}+\epsilon_H\right).         \tag{9}
\]

For [0,1]-valued observables, a local L1 approximation guarantee replaces
epsilon_H. It must be acquired with its own sound statistical procedure;
Boolean exact-equality tests do not automatically supply real-valued
numerical precision.

The new source evaluations are genuinely new information. The chart,
invariants, and conditional sampler are executable consequences of retained
information. For fixed small e, M_e(r) can be manageable; if e grows with r,
it can be exponential. Output bit lengths, chart evaluation, symbolic
checks, audits, and failed candidate fits remain part of the cost.

## 8. Warrant transfer after representation changes

Changing a candidate after audit is invalid unless a transfer is proved.
For a new candidate P'_a on the same reference distribution,

\[
 e'_a\le e_a+\mu\{x:P'_a(x)\ne P_a(x)\}.                  \tag{10}
\]

The second term must be proved, computed, or freshly audited. Semantic
equivalence transfers the warrant exactly. Merely retaining the old epsilon
beside a changed program does not.

An overfit example is F=identity on N states. After seeing an audited set,
choose a new permutation fixing that set and deranging the unobserved
points whenever at least two remain. It has zero empirical error but may
have almost unit true error.

Restriction to a subset having fraction p of the old reference measure
only gives error at most min(1,epsilon/p). A mixture of audited disjoint
supports transfers with its actual mixture weights. Enlarging a support
without auditing the new portion allows arbitrary error there.

Adding an action which preserves an already audited fiber does not erase
old warrants. Adding a direction which merges fibers does not extend the
old local warrants to the enlarged domain. The support and reference
measure are part of each retained artifact, not incidental metadata.

## 9. Exact and approximate conservation are different contracts

Candidate parity preservation is exact. A sampled full-map equality
warrant implies that the source follows those parities with high probability
over the specified finite rollout, via (4). It does not establish exact
true-source conservation at every state.

Auditing only the invariant is insufficient. Let S={0,...,M-1} and add an
outside state bottom. Let F(0)=bottom and F(x)=0 for x in S other than zero.
The one-step conservation violation fraction is 1/M, but every initial
state leaves by step two. Full-map equality to an identity candidate would
have error one, so the correct audit detects the missing information.

A limited extension is possible if candidates are global permutations
but leak from S on a known local fraction ell_a. Starting with density rho
on S, the probability of either leaving S or disagreeing by T is at most
rho*sum_t(ell_(a_t)+epsilon_(a_t)). Use the unnormalized candidate process
until its first exit: each global permutation prefix retains the original
per-state mass cap rho/|S|. Normalizing on survival would discard the
necessary density control.

Metric-close transitions need a separate stability argument. Exact
finite-state equality and approximate state distance cannot be silently
substituted for one another.

## 10. Noisy audits need a conditional detection guarantee

Suppose the comparison has sensitivity at least eta>0 on every true
mismatch, conditional on the current input and all previous audit history.
Fresh audit inputs remain uniform conditional on that history. Then each
trial flags an error with conditional probability at least eta*e_a, and

\[
 \Pr(\text{zero flags})\le(1-\eta e_a)^m.                  \tag{11}
\]

The sample count therefore scales as log(1/delta)/(eta*epsilon).
False positive flags reduce power but do not invalidate this one-sided
bound. A known margin or sound detector is needed to derive such a
condition from noisy numerical observations.

Marginal sensitivity alone is not enough. Let every input be a mismatch,
and draw one common fair coin for the entire audit. On one outcome the
detector flags every mismatch; on the other it flags none. Each individual
trial has sensitivity 1/2, but the whole audit passes with probability 1/2
for every m, rather than 2^(-m). Unknown noise which always reports agreement
makes source error unidentifiable.

A different valid model is a stationary Markov source kernel K_a with fresh
transition randomness. Define
e_a=E_mu[1-K_a(x,{P_a(x)})]. Independent source-query outcomes allow the same
audit and first-error proof. This treats the stochastic transition law as
the target; it does not recover a hidden deterministic map from an
unidentified measurement channel.

## 11. Horizon-dependent acquisition has an information lower bound

This lower bound includes arbitrary adaptive chosen-state source queries,
not just uniform testing. Fix X=Z_N, N>=2, candidate cycle P(x)=x+1,
uniform initial state, and horizon 1<=T<=N. For each v define

\[
 F_v(x)=
 \begin{cases}v,&x=v,\\P(x),&x\ne v.\end{cases}
\]

The complete path error is exactly T/N, since its bad initial states are
v,v-1,...,v-(T-1), all distinct modulo N.

Consider any possibly randomized verifier which accepts the clean source P
with probability at least 1-alpha and accepts each F_v with probability
at most beta. Couple its run on P and F_v using the same random bits.
Unless the run on P queries v, every oracle answer and the final decision
are identical. Hence

\[
 \Pr_{F_v}(\mathrm{accept})
 \ge 1-\alpha-\Pr_P(\text{query }v),
\]

and therefore Pr_P(query v)>=1-alpha-beta. Summing over v gives

\[
 \mathbb E_P[\text{number of source calls}]
 \ge\mathbb E_P[\text{distinct queried states}]
 \ge(1-\alpha-\beta)N.                                  \tag{12}
\]

For 0<eta<=1/4 and N=floor(T/(2*eta)), N>=2 and T<=N, while
T/N>=2*eta>eta. All alternatives violate an eta path-error requirement.
Since N>=T/(4*eta), (12) is an Omega(T/eta) worst-case acquisition lower
bound whenever alpha+beta is bounded below one.

### 11.1 The obstruction persists for reversible true sources

Instead define Q_v by swapping the two values P(v) and P(v+1), indices
modulo N. Each Q_v is a permutation and differs from P exactly on
{v,v+1}. For 1<=T<N, the bad starting states are the cyclic interval

\[
 \{v-(T-1),\ldots,v,v+1\},
\]

of cardinality T+1. Its complete path error is (T+1)/N.

The verifier must query at least one of {v,v+1} with probability
at least 1-alpha-beta. One queried input x belongs to at most two such
sets, corresponding to v=x and v=x-1. Summing the coupled inequalities
therefore gives

\[
 \mathbb E_P[\text{source calls}]
 \ge (1-\alpha-\beta)N/2.                               \tag{13}
\]

The same choice N=floor(T/(2*eta)) has T<N for eta<=1/4.
Thus an Omega(T/eta) obstruction remains under true reversibility.

These are lower bounds for a complete-path or uniform-all-path-observable
warrant. They are not lower bounds for every selected terminal observable,
some of which may be trivial. They establish the horizon factor, not an
additional log(1/delta) factor. A census on a finite space can of course
remove statistical uncertainty entirely. Source queries used during earlier
training, resetting, or building retained tables are part of the same
transcript and are charged in (12)-(13).

## 12. What has been established

The sound reusable object is a bound artifact containing:

- A fixed support, exact conditional sampler, and candidate program version.
- A structural measure-preservation certificate.
- A source access/observation contract and an acquired disagreement warrant.
- A rule for permitted guards, compositions, and domain transfers.
- The conditional initial-density, finite horizon, and confidence budgets.

This interface supports later data acquisition on explicitly represented
fibers and a restricted family of state-dependent reversible interventions.
It leaves exact class recognition unresolved, as it must. It also cannot
make arbitrarily long compositions reliable from a fixed cheap audit:
(12)-(13) quantify that obstruction.

An equally informed retaining program learner can store and execute every
operation described here and therefore can tie it. A full-table cache,
a fixed raw-coordinate low-degree learner, or a learner denied conditional
reset access is a weaker comparison, not a universal baseline.

The remaining scientific applicability question is whether a real target
has a useful acquired chart, tractable nontrivial invariant fibers, source
preparation/readout access, and a downstream task whose cost exceeds this
complete acquisition bill. This proof does not answer that empirical
question.

## 13. Executable evidence and usage boundary

[PLAN.json](PLAN.json) specifies a bounded exact checker before execution.
It includes every three-state true-map pair for a fixed noncommuting
candidate pair, all short words and subset-uniform initial laws, all
two-bit reversible-guard controls, a nonlinear chart/fiber fixture, exact
cycle lower-bound counts, and the disclosed negative controls above.

The fixtures are exploratory proof checks with full prior exposure, not
independent evidence for practical superiority. Results and receipts are
recorded separately. No trajectories of a physical model, external oracle
measurements, or new agents are required. Exact serving model, token usage,
and monetary cost are not exposed to this agent and remain UNKNOWN.
