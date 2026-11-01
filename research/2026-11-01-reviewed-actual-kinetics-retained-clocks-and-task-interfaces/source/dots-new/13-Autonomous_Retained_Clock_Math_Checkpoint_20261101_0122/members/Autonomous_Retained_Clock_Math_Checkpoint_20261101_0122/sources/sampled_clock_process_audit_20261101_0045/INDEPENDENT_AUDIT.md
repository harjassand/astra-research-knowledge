# Independent audit: actual slow vector to finite binary sampled path

Audit date: 2026-11-01. Auditor: `producer-workspace/audit_sampled_clock_process`.

Frozen target: `sampled_clock_process_pending_20261101/ROOT_VECTOR_TO_PATH_THEOREM.md`.
SHA-256: `d1eb7f96cd68e1c681baa4907f888265dbd16a233096d9a345a53003d53e4979`.
The target was read, not edited. This audit used local sources only, no external
retrieval, helper agents, or numerical evidence in place of proof.

## Verdict

**PASS: the conditional finite sampled-path KL and TV theorem.** Its actual-history
conditioning, deterministic-time density estimate, and constants are correct.
**PASS: the weaker-initial-L2 TV alternative.** A telescoping proof is supplied below.
**PASS: the reversible trial-to-vector bridge**, provided the trial is nonzero and
the stated spectral/inverse-form premises really hold for the actual full process.
The standard formalizations are `N>0`, `k>0`, and a Markov-process realization whose
transition operators are the displayed semigroup. These are implicit in the text,
not additional mixing or preparation conclusions.

**COST QUALIFICATION:** the O(n) event-computation statement is valid for a
fixed-size finite-state accumulator in a unit-cost arithmetic model. If “bounded
accumulator” means only bounded numerical range, that statement is not established
and should be narrowed. See Section 7.

**CONTROLLING COST CORRECTION, accepted by the root author during this audit:**
for J finite accumulator states, compilation/evaluation uses O(nJ) arithmetic
operations (assuming fixed-cost transitions), plus the separately accounted
exact-bit/numerical-error cost. O(n) means J fixed, not a universal claim for a
bounded real-valued statistic. This correction controls the cost reading of the
unchanged frozen target. The source probability theorem is separate from the
query algorithm.

**NOT APPROVED:** any unfinished global odd-trial/current construction, any
particular physical model, its source certificate, its rate, its initial
preparation, its arithmetic enclosures, or a physical realization. This is an
audit of a conditional theorem, not evidence that its premises have been earned
for concrete kinetics.

## 1. Density propagation requires no reversibility

Let `mu_t=nu P_t`. For every measurable set A,

    mu_t(A) = integral f0 P_t 1_A d pi
            <= R integral P_t 1_A d pi = R pi(A).

Thus `mu_t << pi` with density `f_t<=R`. This only uses positivity, invariance,
and the initial bound. It does not assert that the law conditioned on a label
history has bounded density. That generally false assertion is not needed.

Likewise, a Markov operator preserving pi is an L2(pi) contraction: Jensen gives
`|P_t g|^2 <= P_t |g|^2`, then invariance allows integration. Its Hilbert adjoint
is also an L2 contraction. Consequently `f_t=P_t^* f0` satisfies
`||f_t||_2<=||f0||_2<=sqrt(D)` under the weaker premise.

The actual process must satisfy the Markov conditional-expectation identity for
P_t. Knowing just its one-time marginals, or postulating a formal unrelated
semigroup, would not suffice.

## 2. Actual-history KL chain rule, including null histories

Write `Y_j=Z(X_{t_j})`, `H_j=(Y_0,...,Y_j)`, and
`a_i=P_{Delta_i}Z-r_i Z`. The process Markov property and tower property give,
for an actual-history version of the conditional probability,

    p_i(H_{i-1}) = P(Y_i=+1 | H_{i-1})
                = (1 + E[P_{Delta_i}Z(X_{t_{i-1}}) | H_{i-1}])/2.

The comparison conditional probability, evaluated on this same history, is

    q_i(H_{i-1}) = (1+r_i Y_{i-1})/2.

Since `Y_{i-1}` is measurable from the history,

    p_i-q_i = E[a_i(X_{t_{i-1}})/2 | H_{i-1}].

Let A denote the actual joint record law and B the comparison joint law. Their
initial label laws agree. Since `r_i<1`, every comparison transition is strictly
positive. Every record with positive A mass therefore has positive B mass,
including when some initial labels have zero mass under both laws. Conditional
p_i values on A-null histories are irrelevant. The finite-alphabet chain rule is

    KL(A || B) = sum_i E_A kl(Ber(p_i) || Ber(q_i)).

The expectation is under A, not under B. No history likelihood-ratio bound is
required. For `q in (0,1)`, applying `log u<=u-1` to the two Bernoulli outcomes gives

    kl(Ber(p) || Ber(q))
      <= (p-q)^2/[q(1-q)].

This remains valid for p=0 or p=1 by the usual zero-term convention. Here
`q_i(1-q_i)=(1-r_i^2)/4` is independent of the sign in the history. Conditional
Jensen and Section 1 imply

    E_A (p_i-q_i)^2
      <= (1/4) E_nu a_i(X_{t_{i-1}})^2
      <= (R/4) ||a_i||_2^2 <= R d_i^2/4.

Thus

    KL(A || B) <= R sum_i d_i^2/(1-r_i^2).

For `TV(P,Q)=sup_E |P(E)-Q(E)|=(1/2)||P-Q||_1`, Pinsker with natural logarithms
gives exactly the displayed root TV bound, capped by 1. Neither reset nor global
mixing has entered the argument.

## 3. Weaker L2 premise: rigorous actual-prefix telescoping

For each i form a hybrid record law that uses the actual conditional kernels for
the initial i transitions and comparison kernels thereafter. The initial label
law is common. The adjacent hybrids with i-1 and i actual transitions have the
same ACTUAL prefix law through i-1, differ only in their next Bernoulli kernel,
and share the same comparison suffix kernel. Kernel contraction of TV gives

    TV(adjacent hybrids) <= E_A |p_i(H_{i-1})-q_i(H_{i-1})|.

Triangle inequality, conditional Jensen for absolute value, Cauchy--Schwarz, and
the propagated L2 density bound imply

    TV(A,B)
      <= sum_i E_A |p_i-q_i|
      <= (1/2) sum_i integral f_{t_{i-1}} |a_i| d pi
      <= (sqrt(D)/2) sum_i ||a_i||_2
      <= (sqrt(D)/2) sum_i d_i.

This proof avoids any unsupported control of densities given entire histories.
The cap at 1 is valid. It does not establish a quadratic-in-d KL estimate.

### Counterexample: fixed initial L2 control cannot generally replace R in the KL estimate

Fix `0<r<1`, `0<delta<1`, and consider three states `b,+,-`. Put
`pi(b)=delta`, `pi(+) = pi(-)=(1-delta)/2`. State b is absorbing; on the other
two states use a symmetric continuous-time flip chain whose correlation after the
chosen deterministic interval is r. Define `Z(b)=Z(+)=+1`, `Z(-)=-1`.

Then `P_Delta Z=r Z` on the two-state component, whereas the error at b is `1-r`.
Consequently

    d^2=delta(1-r)^2.

Choose `nu(b)=sqrt(delta)`, `nu(-)=1-sqrt(delta)`, `nu(+)=0`. Its density obeys

    ||f0||_2^2
      = 1 + 2(1-sqrt(delta))^2/(1-delta)
      <= 3.

Given initial label +, the actual state is b, hence the next label is certainly
+ rather than having comparison probability `(1+r)/2`. Given initial label -,
the actual and comparison transition laws agree. Therefore the one-step path KL
is exactly

    sqrt(delta) log(2/(1+r)).

For fixed r this is order `sqrt(delta)`, while d^2 is order delta, so no finite
coefficient depending only on the uniform bound D=3 can supply the root's
quadratic KL claim in place of R. If all initial mass is instead at b, the path
error stays positive while d tends to zero: without any initial-density control,
an L2(pi) vector estimate alone gives no small-path-error guarantee.

## 4. Spectral moment to vector estimate

For a reversible Markov semigroup let `K>=0` be its self-adjoint generator.
Let psi be nonzero and in the energy form domain, with finite inverse form
`<psi,K^{-1}psi>`. Interpret the inverse form as the spectral integral, possibly
obtained by monotone zero-resolvent limits; finiteness excludes any spectral mass
of psi at lambda=0. No positive gap away from zero is inferred or needed.

With `N=||psi||_2^2>0`, let m be its normalized spectral measure. Then

    integral lambda dm = E(psi)/N <= k,
    integral (k/lambda) dm = k<psi,K^{-1}psi>/N <= 1+epsilon.

The nonzero trial and finiteness imply `k>0`. Spectral Cauchy--Schwarz implies
epsilon>=0. Apply the accepted scalar lemma to `X=lambda/k` and `s=kt` to obtain

    a <= C(t) <= a+epsilon,  a=exp(-kt).

The scalar lemma's proof in
`constant_spd_mfpt_20261031/TRIAL_RESOLVENT_TO_SURVIVAL_ROOT_V2.md` was also checked:
its Taylor remainder bound, both x ranges, and constants `1/e+4/e^2<1` are valid.
Only its elementary scalar lemma is used, not a killed-process-to-global-process
identification.

Self-adjointness and the semigroup property give

    ||P_t psi-a psi||_2^2/N = C(2t)-2a C(t)+a^2
                            <= (a^2+epsilon)-2a^2+a^2
                            = epsilon.

The negative coefficient of C(t) correctly uses its LOWER bound. Finally,

    P_t Z-a Z = P_t(Z-psi) + (P_t psi-a psi) + a(psi-Z),

so L2 contraction and the triangle inequality yield

    ||P_t Z-a Z||_2 <= sqrt(N epsilon)+(1+a)||Z-psi||_2.

This establishes exactly the root d_i receipt with `a=r_i`. It cannot be applied
to a nonreversible or time-dependent scalar correlation certificate without a
separate vector argument. In particular, merely knowing a scalar correlation
does not justify the identity `||P_t psi||_2^2=<psi,P_{2t}psi>` outside the
self-adjoint setting.

## 5. Full label, slab, deterministic times, and event scope

If psi and Z lie in [-1,1] and agree off a set S, then

    ||Z-psi||_2^2 = integral_S |Z-psi|^2 d pi <= 4 pi(S).

Thus eta<=2 sqrt(s) is valid. The proof needs a measurable binary label on ALL
states, including S. Deleting slab observations or waiting until the trajectory
leaves S changes the record and is not covered by this deterministic-time proof.

An exact two-state symmetric continuous-time chain is a simple reason adaptive
sampling is excluded: `P_t Z=e^{-2 lambda t}Z` with d=0 for every deterministic t,
but observing at the first jump forces the next label to be the opposite one.
The deterministic-time comparison transition with `r=e^{-2 lambda t}` does not
describe that adaptively selected observation. No error-free adaptive theorem
can be inferred from this root.

For every event E of the finite record, `|A(E)-B(E)|<=TV(A,B)`. For every
measurable function F of the record, its pushforward laws have no larger TV.
For a real-valued F, expectation error is at most
`(max F-min F) TV(A,B)`; no scale-free expectation-error assertion for arbitrary
functions follows. These are absolute-error, not relative rare-event guarantees.

The same continuing physical trajectory is permitted because each step uses its
actual conditional law. The root neither proves exact residence-time renewal nor
independence of waiting times. The singular `1/(1-r_i^2)` cost at short lags is
real in this bound. A finite n is part of the theorem; it does not directly give
uniform control of an indefinitely long or continuous-time record.

## 6. Preparation and actual-model boundaries

For exact `nu=pi(.|A)` with pi(A)>0, the density is `1_A/pi(A)`, so
`R=1/pi(A)` is correct. This is not a preparation algorithm. Trial, source current,
global inverse form, full binary label, deterministic intervals, actual rates,
model validity, and initial-density certificate remain receiving obligations.

If an implementation needs intervals for r_i or errors in numerical Q_i, these
must be separately enclosed and propagated. The exact-real theorem does not
silently certify a floating-point midpoint or its bit complexity.

## 7. Computational cost: precise supported form and obstruction

For an event recognized by a deterministic accumulator with B possible states,
augment the comparison label by its accumulator. If the update for each possible
next label is O(1), the forward dynamic program stores 2B probabilities and uses
O(nB) arithmetic operations and O(B) working space. Thus O(n) is correct for
fixed B. Arithmetic bit precision, input decoding, exponentials, and certificate
construction are separate costs.

Bounded numerical range alone is not sufficient. For iid fair comparison bits
`b_i=(Y_i+1)/2` (r_i=0), take nonnegative integer weights w_i and let

    S_j = (sum_{i<=j} w_i b_i)/(sum_i w_i).

Every partial accumulator lies in [0,1], yet the exact probability of
`S_n=T/(sum_i w_i)` is `2^{-n}` times the number of subsets whose integer weights
sum to T. Its attainable-state count can grow exponentially; bounded range
does not give a fixed-state dynamic program. General exact evaluation is the
standard counting subset-sum problem, so no universal cheap query conclusion is
justified by bounded range. The root already disclaims arbitrary predicates;
the additive-event sentence should likewise specify fixed finite state count.

Suggested non-mutating clarification for a later target revision:

    Computing a comparison-chain event recognized by a fixed-size finite-state
    accumulator costs O(n) arithmetic operations, provided updates are fixed-cost.
    For B accumulator states the standard bound is O(nB); bit complexity and
    numerical enclosures are separate. Bounded real-valued range alone is not enough.

## 8. Blockers and disposition

* Probability theorem: **no mathematical blocker** under its actual Markov,
  deterministic-time, initial-density, and actual L2-vector premises.
* Cost wording: **action** specify a fixed finite accumulator state count and
  arithmetic model; **target** root Scope and cost paragraph; **reason** bounded
  real range does not bound computational state count; **outcome** O(nB), or O(n)
  for fixed B, is rigorously supported. The frozen target remains unchanged.
* Concrete kinetics: **action** separately earn and independently audit the
  global trial/inverse-form/current and actual preparation receipts; **target**
  the author's unfinished concrete construction; **reason** this root is only a
  conditional interface; **outcome** not approved or rejected here, not inspected
  as a completed construction, and not silently promoted by this audit.

No external retrieval, helper work, permission escalation, denial, or retry was
needed for this audit.
