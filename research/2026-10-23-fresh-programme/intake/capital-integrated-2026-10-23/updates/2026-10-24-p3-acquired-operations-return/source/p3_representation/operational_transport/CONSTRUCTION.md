# Acquire operations, then warrant their transport

Private P3 working construction, 23 October 2026. This is a finite-state theory
and an executable research route, not a general law of intelligence. Historical
novelty and practical advantage are UNKNOWN. The pinned N780 acquisition and
recognition arguments are used at revision
`0451552424b4679fa9a73faf5849ea5a4af21cf6`.

## 1. The change of question

N780 can acquire a hidden triangular rank decoder under a class promise, but
an arbitrary comparator cannot cheaply be recognized as belonging to that class.
We do not remove that obstruction. Instead, an acquired decoder is treated as
an executable candidate coordinate chart. Its bijectivity is proved from its
triangular program and invertible basis, independently of rank agreement.

The scientific operation to warrant is an actual transition of a resettable
finite-state source, expressed in that chart. A chart can be wrong about the
comparison order and still be useful for this separate task. This does NOT
permit reinterpreting its fibers as true, inaccessible rank fibers.

The proposed cumulative chain is:

1. Acquire a chart R from comparisons, including all acquisition costs.
2. Acquire previously unknown transition programs in R coordinates from
   chosen-state source evaluations.
3. Derive conserved coordinates and exact conditional samplers from the
   acquired programs, retaining their syntactic domain of use.
4. Use the sampler to acquire a NEW transition or observable on a selected
   fiber; its source evaluations are fresh information, not simulated evidence.
5. Audit the new operation on that explicit fiber, and compose it with the
   already warranted library, with an explicit error and horizon budget.

The key guarantee concerns distributions maintained by the CANDIDATE program.
It does not assume the unknown source maintains those distributions.

## 2. Exact access contract

Let X be a finite set. A fixed candidate program supplies a bijection
E:Z -> S onto an explicitly defined subset S of X. Initially Z={0,1}^n and
S=X; later Z can be a smaller Boolean cube parametrizing a learned fiber.
Uniform random bits and E give an exact sampler mu=Unif(S). The inverse is
defined and checked on S; it need not be total on X.

For each named action a, a resettable source answers the full state F_a(x) at
any chosen x in S. F_a:X -> X is deterministic and fixed during the warrant's
lifetime. It need not be a permutation or obey a learned degree bound. An exact
full-state readout and legal reset are stronger access than N780 comparisons.
They are not supplied by a static decoder or by a physical experiment in
general. Simulator execution, reset, transmission, precision, and failures
are charged. Here states are finite bit strings, so no real-number oracle is
being idealized.

Candidate maps P_a:S -> S are proved permutations by their executable form.
The version bindings of E, P_a, and F_a must remain fixed after their audit.
Later guards and compositions covered by the algebra below may be constructed
without a new audit; a newly fitted source action needs its own fresh audit.

## 3. Operation audit, without class recognition

For a fixed action define

    e_a = mu{x : F_a(x) != P_a(x)}.

Draw m_a fresh independent uniform points of S, compare complete true and
predicted successor states, and return PASS only when all agree. For any
epsilon_a in (0,1) and delta_a in (0,1), choose m_a so that

    (1-epsilon_a)^m_a <= delta_a.

Then

    Pr[PASS_a and e_a > epsilon_a] <= delta_a.                 (1)

Proof: for every fixed bad source/candidate pair, pass probability is
(1-e_a)^m_a. This remains valid conditional on all earlier training and candidate
selection, because the audit draws are fresh. It is not the posterior assertion
Pr[e_a>epsilon_a | PASS_a] <= delta_a. There is no tolerant completeness claim:
an approximately correct candidate with positive error can be rejected.

Across adaptively acquired candidates and fibers, allocate summable delta_a
budgets and condition on each pre-audit history. The probability of issuing any
false warrant is bounded by their sum. Full output comparisons can be cached
only when the source is deterministic; reusing an earlier sampled input does
not create a new independent sample, although iid sampling with replacement
can legitimately revisit points. Fresh candidate selection after looking at
an audit invalidates the old warrant unless a separate uniform argument applies.

## 4. Composition theorem

On the simultaneous valid-warrant event, fix a word a_1,...,a_T independently
of a fresh initial draw X_0. Suppose its distribution nu is bounded by rho*mu
pointwise. Couple actual and candidate paths from the same X_0. Since every
candidate prefix is a permutation of S, each candidate state distribution is
also bounded by rho*mu. If the paths first separate at step t, the candidate
state just before t lies in the action's mismatch set. Thus

    Pr[path disagreement by T] <= min(1, rho * sum_t epsilon_{a_t}).  (2)

No true-source measure-preservation assumption was used. In particular the
actual source may leave S on a mismatch. Equation (2) bounds total variation
of the complete paths under this coupling, and therefore the expectation gap
of EVERY bounded [0,1] path statistic. It covers hitting indicators and bounded
stopping-time statistics of the fixed finite word, as well as final readouts.
It does not bound an unbounded mean first-passage time, long-time mixing,
stationarity, or relative error of an exponentially rare event.

The good audit event is about deterministic source/candidate mismatch masses;
therefore (2) holds simultaneously for all later finite words, observables,
and initial laws satisfying the bound. A later task can be selected using all
previous data, provided the new initial draw obeys the stated conditional law.
The confidence budget is paid once per warrant; the path-error bound grows
with uses. A product bound 1-prod(1-epsilon_a) is NOT justified by marginal
uniform mismatch rates alone. A cyclic candidate shift with disjoint preimages
of a one-point mismatch attains the additive bound for short enough words.

Arbitrary state feedback is not covered: if P_a is identity for every a in X,
and F_a differs from it only at state a, every e_a=1/|X|, but selecting a=X_0
causes certain failure. An arbitrary choice of a word after seeing its initial
state needs a new conditional density or balanced-program argument.

## 5. An acquired, syntax-checkable family

Use Boolean coordinates y in F_2^n. A polynomial shear is

    T_{b,f}(y) = y + b f(y),

where b is a nonzero bit vector and f is a Boolean polynomial satisfying

    f(y+b) = f(y) for all y.                                 (3)

All arithmetic here is over F_2. Equation (3) makes T an involution: applying
it twice cancels the same b. It is a permutation without a source promise.
The identity map is represented separately by f=0.

To learn a candidate from a raw action, query

    D(y) = R(F_a(R^-1(y))) + y

on all points of weight at most d. There are M_d(n)=sum_{j=0}^d binom(n,j)
such points. Boolean Möbius inversion yields the degree-at-most-d vector ANF
interpolant. If every nonzero coefficient is the same vector b, its supports
define f. Check (3) by exact ANF substitution, at cost charged explicitly.
Otherwise return UNKNOWN. A syntactically accepted candidate is an involution
even if the arbitrary source violates the degree/shear hypothesis.

Under the supplied promise that D is a degree-at-most-d shear, this procedure
recovers it exactly. Without that promise, low-weight interpolation provides
only a candidate; equation (1) supplies the subsequent approximate warrant.
Neither a degree promise nor oracle membership is inferred from finite fit.

The operation is ordinary Boolean interpolation plus a reversibility check,
not a newly claimed learning algorithm. For a known nonzero b, degree-d
controls on n-1 complementary coordinates already give 2^M_d(n-1) possible
actions. Each query returns only one unknown bit (whether b is applied), so
worst-case exact identification needs at least M_d(n-1) queries. Our query
count is within the ratio M_d(n)/M_d(n-1), tending to one for fixed d, but this
is not a global optimality theorem for joint chart-and-action acquisition.

## 6. Learn conserved coordinates, then acquire something further

Let B be the span of all nonzero acquired action directions and let rank(B)=r.
Compute an independent basis B_1,...,B_r by exact Gaussian elimination. Let
the rows of H span B's orthogonal complement. Then H y is invariant under
every candidate action. These are precisely its COMMON LINEAR invariants:
for a nonzero control f, h*T(y)=h*y requires h*b=0.

For an explicit y_0, the fiber is

    S_{y_0} = { R^-1(y_0 + sum_i t_i B_i) : t in F_2^r }.     (4)

The map in (4) is a proved bijection from r independent bits to that fiber.
Its ambient mass is 2^{r-n}. It is an invariant fiber, NOT necessarily an
orbit: conditional controls may leave fixed points or smaller components.
Uniform measure on the whole fiber is stationary for each candidate permutation
even when the candidate dynamics is not ergodic on it.

A new task may now choose a fiber and request a previously unknown raw
observable or action there. Degree-e interpolation in the t coordinates needs
M_e(r) chosen source evaluations. A new action whose observed outputs leave
the fiber is rejected. An accepted candidate must preserve the fiber AND its
uniform measure; a syntactically proved local shear suffices. It can join the
fiber-specific library only after its own independent source audit.

The new action/observable provides new source information. The sampler and
the conserved coordinates are new executable consequences of earlier acquired
programs, not new physical observations. All earlier source and audit data
remain available to a strong retaining baseline.

Audits on (4) cost according to epsilon and confidence, without an inverse
ambient-mass factor. This is not a violation of N780's rare-prefix recognition
lower bound: the target is exactly the explicit raw subset (4), not a claimed
unknown true-rank fiber. If the intended scientific target instead refers to
an external energy, rank, or charge label, its equality with (4) is a SEPARATE
semantic obligation. No such equality follows merely from the learned program.

Global audits cannot be reused as equally strong rare-fiber audits: e_a may be
entirely concentrated on one fiber. A source action that exactly matches on
the training points but fails on an untested rare fiber is a required negative
control. Coarsening fibers after adding a new direction also requires new
audits or a valid mixture of existing domain-specific warrants.

## 7. A limited but useful form of feedback

Let g(y) be any exact Boolean guard and let h(y)=f(y)g(y). If

    h(y+b)=h(y),                                             (5)

the guarded candidate y -> y+b h(y) is again an involution. Its source
implementation applies F_a only when g(y)=1 and otherwise does nothing.
Its mismatch set is a subset of the base action's mismatch set. Consequently
the old epsilon warrant remains valid, and any fixed word of such guarded
operations satisfies (2). The guard can be chosen AFTER the audit because
the subset statement is uniform over guards. The exact structural test (5)
and guard computation are charged.

This permits genuinely state-dependent interventions while preserving the
sampling law needed by the proof. It is not a guarantee for arbitrary policies.
Product programs formed from these operations can be retained and reused;
their computational cost and the sum of inherited error budgets remain visible.

## 8. What the comparison must and must not claim

The strongest retaining learner can execute exactly this chart acquisition,
Boolean interpolation, linear algebra, conditional sampling, and audit. It
therefore ties. No advantage over all program/library learners is claimed.
An ordinary full-table cache cannot predict every unvisited state, but beating
that weaker baseline would not establish a research advance. A raw-coordinate
degree-d learner is also a limited ablation because nonlinear chart conjugacy
can increase degree; its failure is not an impossibility theorem for raw data.

The useful target is a proved END-TO-END acquisition-and-use contract, including
recognition costs, for a restricted family. The substantive question is whether
the learned invariants and conditional experiments matter in a real scientific
model whose access is obtainable. A source-defined classical plaquette dynamics
is a prospective application test; its known linear-algebra/sampling algorithm
must remain the tailored baseline. Authored obfuscations or a finite benchmark
cannot establish practical advantage, foundational novelty, or general
cumulative intelligence.

## 9. Resource and evidence obligations

Charge the decoder's comparison inputs/outputs, every source transition and
observable call, reset and source generation, all failed candidates, polynomial
interpolation, symbolic reversibility, GF(2) elimination, candidate inference,
fresh randomness, audits, and confirmation validation. No subscription or
credit audit is part of this investigation. Finite bit arithmetic avoids
unpriced real precision; actual arbitrary-size integer and program costs are
still recorded.

The code `acquired_chart.py` is an independent N780 implementation with a
global query cap. On every completed binary transcript it produces a proved
bijective chart; its receipt explicitly leaves true-rank agreement UNKNOWN
without the source promise. Root-authored development cases are exposed. A
separate independent fixture and a frozen protocol must precede transfer claims.
