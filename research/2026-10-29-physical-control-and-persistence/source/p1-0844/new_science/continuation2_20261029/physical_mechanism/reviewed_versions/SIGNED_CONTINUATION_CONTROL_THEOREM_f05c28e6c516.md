# A signed continuation witness for physical control

29 October 2026. Astra P1, same continuing research role.

## 1. Question and result

Can measurement, feedback, calibration, postselection, or faster switching
replace the opposing hidden responses used by the acquired cancellation
construction? A useful comparison must allow all of those ordinary routes,
not only open-loop words.

The main result here is a sufficient obstruction to exact physical control.
An analytic family of stochastic dynamics can have a nonphysical parameter
value at which all jump rates reverse sign. At that value every trajectory
ending in the opposite part of a bipartite state graph has negative weight;
every trajectory ending in the original part has positive weight. A controller
using physical trajectories and independent randomness combines these weights
positively. Analytic continuation therefore forbids a nontrivial, parameter-
independent terminal transition within a deterministic physical deadline.
It also forbids a nondegenerate exact target conditional on heralded completion
by that deadline. The negative rates are a mathematical witness, never an
available physical intervention.

For the preserved source B this applies to arbitrary continuous observation,
nonanticipating switching among all four generators, and stopping before any
fixed physical deadline. It is stronger than the earlier finite-word
exclusion. It does not exclude approximate control, a parameter actually
known to the controller, or exact endpoint control with an unbounded random
completion time. Those alternatives are constructed below and in the
complementary notes.

Combining this obstruction with the preserved source A gives an operational
separation: sources with identical complete isolated-operation baseline path
laws differ in whether useful stochastic gates can be physically completed
exactly at a fixed time, even after the excluded source is granted feedback
and switching. Actual cross-operation acquisition distinguishes their relative
responses. This is a scoped mathematical capability separation, not an
apparatus demonstration or a claim of historical priority.

## 2. Physical interface and what is being controlled

Let the actual observable state take values in a finite set X. A fixed
two-colouring sigma:X->{-1,+1} makes every allowed jump cross the colouring.
The current physical state, not a remembered earlier state or an arbitrary
controller-generated output bit, is the terminal output.

A hidden parameter h remains fixed during the operation. It belongs to a
real interval I with nonempty interior. A finite menu of actual generators
has off-diagonal rates q_j(x,y;h). Each physical rate is strictly positive on
its specified allowed edge and zero on other edges. All allowed edges cross
sigma. Diagonal entries are minus the row sum. A zero-rate hold may optionally
be supplied as a separate actual control; its availability is not presumed.

The controller may have unlimited computation, independent random seeds,
continuous access to the visible jump path, a clock, and arbitrary memory of
that path. It chooses a predictable menu index, switches at arbitrary times,
and declares a stopping time tau. No direct measurement of h is supplied.
The rule is the same measurable function of its observations and independent
seed for every h. Predictability excludes choosing a control retrospectively
on the basis of the current jump before it has occurred.

The theorem concerns a physically specified, nonexplosive controlled process.
Finite state and a finite menu with bounded rates on I suffice. State-changing
actuators outside the specified menu, microscopic copies, extra probes of h,
or state relabellings that change the requested output are new resources.
Apparatus records that remain available can only strengthen the requirement
of autonomy: a failure already for the endpoint or endpoint-plus-clock
cannot be repaired by retaining more records.

At the start of the episode, x is fixed. Write O for final states with the
opposite colour and E for final states with the original colour. A desired
stochastic gate has Pr_h(O)=c, the same c>0 for all h. A nondegenerate reset
or gate has 0<c<1. Dependence on the specified starting state is permitted;
the theorem is applied to each starting row separately.

## 3. Analytic witness hypothesis

There is a connected complex open set D containing I and a real witness h_*
outside the physical interval, such that every allowed rate extends
holomorphically to D. At h_* every nonzero allowed rate is strictly negative.
The finite menu implies a uniform bound on the moduli of these extensions on
each compact subset of D. Zero controls remain zero.

The witness need not be close to I and is not a physically attainable state.
Its role is analogous to evaluating a polynomial outside the interval where
it represents probabilities. The claimed conclusion is conditional on this
actual analytic rate family. Finite measurements alone do not establish that
family, its exact analytic identity, or its continuation.

## 4. Stopped likelihood lemma

Fix a deterministic deadline T<infinity. Consider any stopping rule tau<=T
and an event A measurable from the stopped visible path and controller seed.
Its physical probability P_h(A) has a holomorphic extension to D.

Proof. Choose a reference process with a constant positive rate rho on every
allowed directed edge and use the identical controller seed, history rule,
and stopping functional. The reference ignores the selected control when
generating its jumps. It has finite total rate at most R=(|X|-1)rho. A
reference path with jumps (x_{i-1},x_i) at times t_i has the stopped likelihood

    L_z = exp[integral_0^tau {r_ref(X_s)-r_{a_s}(X_s;z)} ds]
          product_{t_i<=tau} q_{a_{t_i-}}(x_{i-1},x_i;z)/rho.

Terms with an edge disabled by the selected control have zero likelihood.
Here r denotes total outgoing rate. Standard stopped likelihood identities
give P_h(A)=E_ref[1_A L_h] for physical h. One can also obtain this identity
directly by multiplying survival probabilities and jump densities on each
stopped path cylinder and then monotone approximation.

For a compact K contained in D, choose Q bounding all |q_j(x,y;z)| on K.
The modulus of L_z is at most

    exp[(R+(|X|-1)Q)T] max(1,Q/rho)^{N_T}.

The reference jump count N_T is dominated by Poisson(R T). The displayed
envelope is integrable, uniformly on K. For a fixed reference path, L_z is
holomorphic: the path and its selected controls do not change with z.
Integrating the holomorphic functions using that envelope proves the lemma,
for example by Morera's theorem and dominated Fubini. The same argument
covers unbounded numbers of switches, provided the stated predictable
controlled intensity process is well-defined. It does not require a bound
on the number of physical jumps or label reads.

At h_*, the exponential is strictly positive and each nonzero jump factor
is negative. Bipartiteness gives

    sign L_{h_*} = (-1)^{N_tau} = sigma(x) sigma(X_tau)

on every nonzero-likelihood path. All paths with positive physical
likelihood have nonzero witness likelihood, because the same allowed edges
are strictly nonzero at h_*. Disabled-edge reference paths have zero
likelihood at both. Consequently an opposite-colour event of positive
physical probability has strictly negative continued probability; a
same-colour event of positive physical probability has strictly positive
continued probability.

## 5. Main theorem: bounded physical time and heralding

### 5.1 Total bounded-time operation

No admissible operation with tau<=T almost surely for every physical h can
have P_h(O)=c>0 for every h in I.

Indeed, F(z)=E_ref[1_O L_z] is holomorphic. If F(h)=c on I, the identity
theorem gives F(h_*)=c. The path-sign lemma gives F(h_*)<=0, a contradiction.
The same conclusion holds if equality is known on any parameter support
with an accumulation point inside D. A finite parameter set is insufficient.

### 5.2 Bounded-time heralded operation

Allow an operation to succeed only on an event A. On other trajectories it
may report failure. Suppose it completes or fails by T and has positive
success probability at at least one physical parameter. There is no fixed
c in (0,1) such that

    P_h(A and O) = c P_h(A)

for all h in I.

Let F(z)=P_z(A and O) and E(z)=P_z(A and same colour). The proposed identity
is (1-c)F-cE=0. Both functions extend holomorphically. At the witness,
F<=0 and E>=0, and at least one inequality is strict. Therefore
(1-c)F(h_*)-cE(h_*)<0, contradicting the identity theorem.

Heralding a deterministic target is not excluded: stopping at the first
flip before a deadline and reporting success then gives c=1 on successful
trials. The obstruction concerns an exact nondegenerate distribution among
the successfully prepared physical outputs. Randomly choosing a target
before a deadline does not remove success bias between those targets.

### 5.3 Exposed completion time

Suppose an operation stops almost surely in a finite but unbounded time and
has an exact nondegenerate endpoint law c for every h. It cannot also obey

    P_h(O, tau in B) = c P_h(tau in B)

for every measurable time set B and every h. Otherwise take B=[0,T] for a
finite T with positive completion probability. The interrupted protocol,
successful only when it has completed by T, contradicts Section 5.2.

This also covers any exposed completion clock C>=tau formed by genuine
nonnegative padding independent of the unknown parameter except through
allowed observations: success {C<=T} is a bounded-time event. Padding that
itself moves the physical state must be included as an actual allowed
control. A known instantaneous flip, replacement sample, or unrelated
actuator is outside the declared menu.

The conclusion is not that no exact terminal sample exists. It is that
the clock cannot be statistically separable from that sample throughout
the unknown-parameter family. If timing is retained, a reference must
model this joint record rather than silently discard it.

## 6. Source B: the actual continuation is explicit

Use the preserved hidden H in [-1,1], frozen for the whole process, and the
four symmetric binary endpoint flips p_j(h)=u_j+b_j h:

| j | u_j | b_j |
|---|---|---|
|0|1/10|1/20|
|1|3/10|3/20|
|2|1/4|1/10|
|3|7/20|1/10|

The actual continuous-time generator in mode j has symmetric flip rate

    q_j(h) = -log[1-2(u_j+b_j h)]/(2 t0).

Every mode held for time t0 has exactly the stated endpoint probability.
For all physical h the rates are positive and uniformly bounded by
log(10)/(2t0). All q_j are holomorphic on Re z<4/3 using the logarithm with
positive-real-part argument. The witness h_*=-4 gives

    p_j(-4)=(-1/10,-3/10,-3/20,-1/20),

so 1-2p_j(-4)>1 and all four q_j(-4)<0. The binary state graph is bipartite.
All hypotheses of the continuous-time theorem are therefore checked.

Source B cannot synthesize any nonzero, H-independent probability of changing
its actual bit within any fixed deterministic physical deadline, using only
these generators, observation, feedback, switching, and independent random
bits. It cannot even herald a nondegenerate exact H-independent final bit by
that deadline. An exact endpoint factory with unbounded completion time
must leave a parameter-dependent output-clock relation.

This excludes arbitrary positive durations and path-dependent switching;
it is not merely the old integer-word argument. It does not grant access
to the negative-rate witness. Unknown device kinetics are exactly those
of this specified family, not arbitrary reversible generators inferred
from their equilibrium alone.

## 7. Elementary endpoint version and a quantitative bound

For a program with at most L fixed-duration calls, a terminal path with d
calls and r flips has probability equal to a nonnegative controller weight
times a product of d affine factors. Its highest coefficient has sign
(-1)^(d-r). For terminal opposite parity r is odd. All maximal-length
opposite paths contribute the same sign to the top coefficient. Hence any
nonzero opposite probability is a nonconstant polynomial. For a heralded
target, the top coefficients of (1-c)F-cE have the same sign at the maximal
accepted depth; they cannot cancel. This is an independent proof of the
finite-call case, including arbitrary history-dependent choice and stopping.

The signed continuation gives a quantitative, conservative consequence.
Let f be the opposite endpoint probability of a total program with at most
L calls, and let delta=sup_{h in [-1,1]}|f(h)-c|, c>0. At h=-7/2 all
p_j(h)<=0, so f(-7/2)<=0. A degree-L polynomial r satisfies the Chebyshev
outside-interval inequality

    |r(x)| <= |T_L(x)| max_{[-1,1]} |r|,  |x|>1.

Applying it to r=f-c gives

    delta >= c / T_L(7/2).

For completeness, the Chebyshev inequality follows by contradiction from
alternation: if |r(x_*)|>|T_L(x_*)| ||r||_infinity, subtract a multiple of
T_L matching r(x_*). At its L+1 alternating extrema the difference has
alternating signs, hence L roots inside [-1,1], plus the root x_* outside,
contradicting degree <=L. Limits handle equality or zero values.

This lower bound is exponentially small and is not claimed sharp. It
establishes a positive uniform error floor for each finite call budget.
It must not be compared directly to an average calibration error without
the corresponding change of norm and parameter distribution.

## 8. Calibration and the retained information boundary

The no-go concerns a common control rule across the uncertain family. If h
is actually revealed, that premise disappears. A controller can choose
h-dependent mixing weights and sometimes implement the desired row in one
or two calls. Finite calibration can approximate that route very well.

After any finite endpoint calibration record D with positive probability,
every h in I still has positive likelihood in source B. Condition on D:
the selected future control rule is a fixed rule across that entire support.
The theorem therefore still excludes an exact future row independent of H
and arbitrary further retained old information, even if the rule depends
on D. Continuous-path finite calibration likewise has equivalent positive
likelihoods at the physical parameters, with the usual almost-everywhere
conditioning qualification.

This statement must not be strengthened to forbid Bayesian predictive
balancing relative to one chosen posterior. A marginal law averaged over
that posterior is a different target. The previous exact cancellation
theorem protects all old information, even H itself; it requires the
pointwise row property considered here. An exposed primitive key may also
be retained in a data-conditioned positive reference, without claiming
that its law is independent of H. The complementary comparator uses that
strong and legitimate alternative.

## 9. Positive side: acquired response orientation changes capability

The preserved source A replaces the second and fourth slopes by negative
ones. It implements the two exact fixed-duration calls

    A = (3/4)T0 + (1/4)T1,       flip probability 3/20,
    B = (1/2)T2 + (1/2)T3,       flip probability 3/10.

Those selectors use a fixed finite number of fresh fair random bits. All
branches have the same actual call duration t0. The compiled endpoint law
ignores H exactly. The complete compiled endpoint/action record is Markov
under arbitrary subsequent feedback and arbitrary old history, as proved
in the unchanged predecessor. Keys and native within-call paths must be
unavailable to that service, and their production, recording, withholding,
and possible erasure are real apparatus requirements and costs.

Each isolated raw mode, including its whole continuous-time baseline path,
has exactly the same law in A and B under uniform H, by h->-h for the modes
whose slope changes. Their cross-operation return laws differ. Thus separate
complete characterizations miss an operational capability which actual
cross experiments detect. The sign witness proves this separation survives
all bounded-time control in B, not just a specified finite menu of words.

Population cross-response Grams identify alignment and cancellation at the
declared interface. Finite confidence intervals do not prove exact zero,
exact rank, analytic continuation, or an infinite-support latent model.
The exact separation is a theorem about the explicitly given physical
families; it is not an assertion that finite data certify either family
without structural premises.

## 10. A scalable controlled network, with the added controls explicit

To move beyond an isolated bit, construct a ring of d>=3 binary sites. Each
site has an actual addressed copy of the four source-A generators; its own
H_i is frozen, and the joint H vector may be arbitrarily correlated. A call
acts only on the selected site. This addressability and isolation of other
sites are additional actual controls in this network construction, not
consequences of single-bit equilibrium data. Noninvasive neighbour reads
and a controller implementing the stated finite tables are also supplied.

Let the desired conditional probability that site i is 1 be 3/8 when both
neighbours are 0, 1/2 when they disagree, and 5/8 when both are 1. These are
the zero-field Ising ring heat-bath probabilities with

    beta J = (1/4) log(5/3).

Use the lazy heat-bath update with refresh probability s=9/20. Given the
current site value y, set p to its conditional probability of value 1 and
choose the desired flip probability

    alpha = (9/20)[p if y=0, otherwise 1-p].

It is one of 27/160, 9/40, 9/32. Randomize between the compiled A and B calls
with B probability r=(alpha-3/20)/(3/20), respectively 1/8,1/2,7/8.
Three fresh fair bits select this branch; two more implement its raw-mode
mixture. A fixed allocation of five bits suffices, including unused-bit
padding in the randomizer. The raw physical call always lasts t0. A fixed
controller latency is an explicit implementation premise; no unbounded
rejection sampler is hidden in the exact probabilities.

The resulting physical one-site operation is exactly

    (11/20) identity + (9/20) heat-bath update

on the visible ring, for every H vector. This equality is an identity of
the actual local transition kernel, not a claim that an identity actuator
was used. The native positive flip probabilities and feedback achieve it.
Random-scan or deterministic-scan composition gives the corresponding
standard Gibbs dynamics, with its usual statistical-mechanical target.
Every compiled record, including visible neighbour observations and site
choices, has the ideal controlled network law. The selectors within the
local call and microscopic trajectories retain their earlier scope.

The executable four-site rational check verifies the primitive cancellation,
the full 16-state transition matrix, detailed balance, and the target measure.
The same algebra applies to any ring size. This supplies an exact local
stochastic update on an exponentially large visible configuration space
while frozen hidden disorder remains. It does not establish fast mixing,
an advantage over conventional Gibbs software, hardware feasibility, or
hard-problem acceleration. General Gibbs specifications require reachable
row probabilities and actual randomizers for them; they are not silently
included in this fixed-five-bit construction.

## 11. Strong ordinary routes and limits of the new conclusion

The comparison is deliberately constructive.

1. **Per-device calibration.** Repeated visible flip increments on the same
   frozen H can estimate the probabilities directly. The complementary
   construction uses modes 0 and 3 to reach the same 3/20 and 3/10 targets
   by mixtures of T0 and T3 squared, with a simultaneous, uniform-in-H
   confidence bound. Its positive reference keeps calibration, exposed
   word keys, intermediate reads, and durations. The old record can be
   arbitrary. The guarantee concerns approximate data-conditioned laws,
   so it respects this exact no-go.
2. **Waiting.** In source B, mode 3 has centered multiplier in [1/10,1/2].
   L repeats prepare the bit within 2^(-L-1) of uniform pointwise in H and
   initial bit. Against the reference retaining the same old (H,Z), this
   joint preparation error transfers to any common later physical channel.
   It does not erase a record of the preparation itself. If an actual
   identity branch is available, its mixture with the long mode-3 call
   approximates useful stochastic gates cheaply; the companion note gives
   marked-record and cost bounds. Neither identity holding nor common-time
   padding is supplied by invariance.
3. **Random completion.** Choose an independent target bit with the desired
   probability, and observe mode 3 until that target is reached. This is
   exact endpoint control for every H. It has finite expected cost and an
   exponential tail, but no deterministic worst-case deadline. Timing and
   internal records carry the dependence excluded in Section 5.3.
4. **Returned-trial acquisition.** Where an actual H-preserving return gives
   fresh trials on one specimen, the complementary multiscale certificate
   improves the generic squared-defect acquisition exponent from v^-2 to
   v^-1 up to logarithms. Its recorded conservative constants are still
   enormous. Repeated specimens, return operations, and conditional
   freshness are added resources; the earlier two-call data do not gain
   that exponent merely by being reanalysed.

The finite-data result is not exact population cancellation. Per-device
information is not free. The positive-flux repair remains a comparison
kernel, not a new available actuator. The original full operation language
and its finite-error theorem remain unchanged. No accepted N675 dependency
is reopened or used without its own interface.

## 12. What this result contributes and does not yet settle

Polynomial transcript representations, Bernoulli factories, adaptive Markov
control, Gibbs updates, and impossibility of passive interruptible exact
sampling have close established predecessors. The candidate contribution
is the signed analytic continuation witness for controlled physical terminal
states, its continuous-time feedback and heralding scope, and its use with
the acquired cross-response construction to prove a strict operational
separation. See SOURCES_AND_FAILED_ATTACKS.md for the primary comparison.

This makes relative hidden-response orientation a resource with a precise
consequence: in the exhibited family it enables exact bounded-latency
stochastic physical transitions which arbitrary bounded-time sensing and
feedback cannot replace. Approximate operations may already be inexpensive
by ordinary routes. Which real materials supply opposing responses, how
to certify them at finite precision, and whether any application benefits
after full apparatus costs remain open. The theorem is not labelled a
civilisation-scale breakthrough.
