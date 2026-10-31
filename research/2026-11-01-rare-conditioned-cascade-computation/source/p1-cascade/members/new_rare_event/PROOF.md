# Learning irreversible event dynamics and compiling rare conditioned paths

Research construction, 31 October 2026.  The root researcher owns the
acquisition theorem and overall synthesis.  This document proves the
execution, probability, and conditional-path bridge.  Historical priority
has not been established.  The accompanying program is a floating-point
implementation, not a finite-bit or interval proof.

## 1. Operation and legal information

There are n components, each initially in state 0 and able to change once
to state 1.  Write X(t) in {0,1}^n.  An unfailed component i changes at
rate lambda_i(x), where lambda_i is nonnegative, finite, and coordinatewise
nondecreasing in the other components.  Its own state is excluded from
the rate table because its only transition is 0 to 1.  Local dependence,
when available, means that lambda_i depends on a parent set P_i.  The
directed dependence graph can contain cycles.  There are at most n real
jumps, but there can be 2^n global states.

The event is E_T={X(T) in F}, where F is upward closed: x in F and y>=x
imply y in F.  Requiring a selected subset of components to have failed
is an important example and adds only unary factors to the computation.
The deadline T is positive.  Conditioning is asserted only when p=P(E_T)>0.

The acquisition output used in the theorem is a learned attractive local
model lambda_minus with the same state meaning and

    (1-zeta) lambda_i(x) <= lambda_minus_i(x) <= lambda_i(x),  0<=zeta<1,

simultaneously for all states and nodes.  Its scope should be a subset of
the true parent scope; this preserves the relevant graphical width.
The root's acquisition construction must earn this output through actual
component experiments and charge resets, clamping, elapsed time, finite
readout precision, and sampling.  This document does not assume a
committor, conditioned-path oracle, graph oracle, or full-state solver.

Two-sided local confidence intervals can be made one-sided and attractive
without a nonlinear optimizer.  If L_i(s)<=lambda_i(s) and
L_i(s)>=(1-zeta)lambda_i(s) for every local configuration, set

    lambda_minus_i(s) = max_{u<=s} L_i(u).

Attractiveness of the truth proves both bounds and monotonicity of this
closure.  The same operation cannot repair a scope that omitted an
influential parent; that is an acquisition obligation.

## 2. The acquired one-sided model preserves rare conditional laws

Let P and P_minus be the two path laws through a fixed deadline T.
The standard continuous-time path likelihood is

    dP_minus/dP(path)
      = product_over_jumps lambda_minus_i(X_before)/lambda_i(X_before)
        * exp( integral_0^T sum_alive_i
                    [lambda_i(X(t))-lambda_minus_i(X(t))] dt ).

The integral is nonnegative.  The path has at most n jumps.  Consequently

    dP_minus/dP >= c_rate := (1-zeta)^n.                       (2.1)

Ratios at a zero rate cause no problem: a zero-rate jump has P-probability
zero, and the two models have the same zero rates under the assumed
multiplicative bound.  This is a probability-law statement in exact
arithmetic; it is not an empirical certification of a Markov model.

A common-clock monotone coupling gives X_minus(t)<=X(t).  Indeed,
whenever the two corresponding components are both unfailed and the
states are ordered,

    lambda_minus_i(x_minus) <= lambda_i(x_minus) <= lambda_i(x).

Therefore p_minus=P_minus(E_T)<=p=P(E_T).  On conditioning (2.1),

    dP_minus(.|E_T)/dP(.|E_T)
       = (dP_minus/dP) * p/p_minus >= c_rate.

If Q'>=c Q as measures, Q'=cQ+(1-c)R for a probability measure R, and
TV(Q,Q')<=1-c.  Thus

    TV(P(.|E_T), P_minus(.|E_T)) <= 1-(1-zeta)^n <= n zeta.    (2.2)

The bound has no factor 1/p, no mixing-time premise, and no rate-ratio
factor.  It applies to the full fine-time path law through T, hence to
every later bounded path statistic.  For positive rates and observation
through completion of all n transitions, the same likelihood argument
applies to the entire completed path.  It does not extend automatically
to repair processes with unbounded jump counts or to nonmonotone events.

An equally useful probability bound follows from the same likelihood:

    c_rate p <= p_minus <= p.                                (2.3)

The lower inequality is obtained simply by integrating (2.1) on E_T.
No time-rescaling argument is needed for this acquisition step.

## 3. Deadline elasticity is bounded by the number of possible jumps

For any time-homogeneous pure-birth-on-subsets CTMC and upward-closed F,
not yet hit at time 0, condition on the finite ordered sequence of
components that change before F is first hit.  Conditional on such a
sequence, the holding times are independent exponentials with the total
exit rates along that sequence.  The probability of the sequence is
independent of these holding times.  Sequences of zero probability can
be discarded.  There are r<=n holding times on each successful sequence.

If S is a sum of r independent exponentials, then for 0<a<=1,

    P(S<=aT)
      = a^r integral_{sum u_j<=T} product_j b_j
                                   exp(-a sum_j b_j u_j) du
      >= a^r P(S<=T) >= a^n P(S<=T).

Mixing over the sequences proves

    p(aT) >= a^n p(T),                  0<a<=1.               (3.1)

The argument uses only time homogeneity and at most n irreversible jumps.
Attractiveness is needed below for the comparison with a held-interaction
process.  Formula (3.1) is a proof device, not an algorithm enumerating
the possible component orders.

## 4. Hold interactions during bins, with a pathwise time guarantee

Fix a bin width Delta>0.  At the beginning of every bin, read the failed
set.  During that bin each remaining component evolves independently at
the rate determined by this beginning-of-bin state.  A newly failed
component affects other components only from the next bin.  Call this
the held process.  A component still fails at a continuous time inside
its bin; only the propagation of that failure is delayed.

Construct both processes using independent unit exponential thresholds
e_1,...,e_n.  Component i fails when its cumulative hazard reaches e_i.
Let tau_i be its true failure time and tau_i^Delta its held failure time.
Attractiveness first gives tau_i<=tau_i^Delta by the standard first-crossing
argument.

For the upper bound, order the true failures so that i has rank k.
Assume inductively that every earlier component j, of rank l<k, satisfies
tau_j^Delta<=tau_j+l Delta.  For t<=tau_i, examine held time s=t+k Delta.
The beginning of its bin is at least s-Delta=t+(k-1)Delta.  If a component
j is already failed at true time t, it has rank l<k and

    tau_j^Delta <= tau_j+l Delta <= t+(k-1)Delta.

Thus, by held time s, all failures present at true time t have already
propagated.  If i has not failed earlier, its held rate at s is at least
its true rate at t.  Integrating on the shifted interval
[k Delta,tau_i+k Delta] gives cumulative hazard at least e_i.  Hence

    tau_i <= tau_i^Delta <= tau_i+k Delta <= tau_i+n Delta.   (4.1)

The proof remains valid when some rates are zero.  Infinite failure times
are interpreted in the extended sense.  The zero-probability ambiguity at
bin endpoints does not affect the path law.  No upper bound on a rate,
no ratio of fastest to slowest rate, and no assumed reaction coordinate
appears in (4.1).

For every upward-closed F, the corresponding driver events satisfy

    E_true(T-n Delta) subset E_held(T) subset E_true(T),       (4.2)

and also

    E_true(T) subset E_held(T+n Delta).                       (4.3)

Take Delta=T/N with N>n.  Equations (3.1) and (4.2) give

    c_grid p(T) <= p_held(T) <= p(T),
    c_grid := (1-n/N)^n >= 1-n^2/N.                          (4.4)

Therefore N>=n^2/epsilon suffices for relative probability error at most
epsilon.  This is independent of p(T) and of rate stiffness.  An absolute
coupling estimate of order rate_max*Delta would not give this result.

For a stronger computable enclosure at an actual model, keep Delta fixed
and compute both N-bin and (N+n)-bin held probabilities:

    p_held(T) <= p(T) <= p_held(T+n Delta).                  (4.5)

The right calculation has only n extra bins.  It can be much sharper than
the worst-case power bound and gives a refinement rule without evaluating
the true CTMC.  When lambda_minus is the acquired lower model, use
lambda_plus=lambda_minus/(1-zeta) for the upper calculation; this gives

    p_minus,held(T) <= p_true(T)
                   <= p_plus,held(T+n Delta).               (4.6)

Both bounding models are attractive.  When zeta=0, (4.6) reduces to (4.5).

## 5. A finite factor graph replaces the exponential state space

Let Z_i be the held failure bin: Z_i in {0,...,N-1}, with Z_i=N meaning
that i survives through T.  A parent j contributes to i's rate in bin m
exactly when Z_j<m.  For a particular assignment z, define

    a_i(m;z) = lambda_i( 1{z_j<m} : j in P_i ).

The joint probability of the assignment is exactly

    P(Z=z) = product_i f_i(z_i,z_{P_i}),

where, for z_i<N,

    f_i = exp(-Delta sum_{m=0}^{z_i-1} a_i(m;z))
          * [1-exp(-Delta a_i(z_i;z))],                      (5.1)

and for z_i=N,

    f_i = exp(-Delta sum_{m=0}^{N-1} a_i(m;z)).               (5.2)

Proof: at each bin, conditional on the beginning state, distinct unfailed
components have independent constant clocks.  Multiply all survival and
failure probabilities and regroup by component.  Cycles in the local
dependence graph are allowed because a same-bin failure is not propagated.
This proves normalization; it is not a loopy-BP approximation.

For the event that all i in S have failed, restrict z_i<N for each i in S.
This is a unary factor and does not increase graphical width.  A more
general upward-closed event requires its own supplied finite predicate or
factor representation, whose acquisition, evaluation, and added width
must be charged.  An arbitrary Boolean event is not declared cheap.

The primal graph connects all variables in each scope {i} union P_i.
Suppose an actual acquired elimination order has width w.  Ordinary
variable elimination computes the positive partition function in
O(n (N+1)^(w+1)) arithmetic operations up to local factor construction
costs.  A local table has degree d_i<=w.  Sorting parent bin changes lets
one evaluate a factor entry using O(d_i log d_i) work, rather than N work.
The implementation uses an equivalent vectorized sum over 2^d_i local
configurations.  Backward elimination tables yield an exact conditional
bin draw in O(n(N+1)) arithmetic per draw after preprocessing.

No supplied tree decomposition is necessary: a standard fixed-parameter
treewidth algorithm may be used and charged.  The implementation instead
constructs a min-fill order and reports its actual width; it does not
claim that this heuristic attains the optimum width.  Keeping an actual
order is a certificate of the width used by the computation.

With N=ceil(n^2/epsilon), this is a relative-error approximation scheme
polynomial in n and 1/epsilon for each fixed width w, independent of the
2^n state count and inverse event probability.  Its polynomial degree can
be large and the dense tables can be impractical; that is an explicit
cost, not a claim of universal large-system deployment.

## 6. Pull back the conditional bin draw to continuous drivers

A bin draw alone is not a total-variation approximation to the true
continuous path.  It is essential to reconstruct the exponential drivers
and run the undelayed dynamics.

Given a complete bin assignment z, let

    H_i = Delta sum_{m<z_i} a_i(m;z),
    r_i = a_i(z_i;z).

If z_i<N, the compatible unit exponential threshold lies in
[H_i,H_i+Delta r_i).  If z_i=N, it lies in [H_i,infinity).  Conditional on
z, these intervals are independent across i: the unconditional driver
density is product_i exp(-e_i), and a fixed assignment imposes exactly
these separate interval constraints.  Their masses are precisely (5.1)
and (5.2).

Thus, independently for each component, sample

    e_i = H_i - log(1-U_i [1-exp(-Delta r_i)])       if z_i<N,
    e_i = H_i + Exp(1)                             if z_i=N, (6.1)

with independent uniforms U_i.  This is exact conditional sampling of the
original drivers in the exact-real random-variable model.  A stored
finite-bit path has an atomic law and therefore has total variation one
from a nonatomic ideal continuous path law.  An implementation must instead
target a specified rounded-output law (the ideal-law bound transfers under
the same rounding map), or use a lazy random-bit representation of a real
path.  Approximate exponentials, logarithms, and categorical sampling then
need an error budget for that actual output contract.  The floating
prototype does not earn such a finite-bit total-variation guarantee.

Now simulate the undelayed CTMC from e_1,...,e_n.  It has at most n real
jumps and can be simulated directly from the learned local rates.  The
resulting fine-time path has the model's driver law conditioned on
E_held(T), rather than conditioned on E_true(T).  By (4.2), the first event
is a subset of the second.  The total variation of the two conditional
driver laws is exactly

    1 - p_held(T)/p(T) <= 1-c_grid.                         (6.2)

A deterministic map from drivers to paths cannot increase total
variation.  Consequently the returned continuous path is within
1-c_grid of the desired continuous event-conditioned model law.
This is a law guarantee, not merely a bound on a smooth observable or on
the locations of binned event times.  The driver pullback can change the
order of failures inside a bin; retaining the held times would lose this
argument.

The computable refinement certificate (4.5) also gives

    TV <= 1 - p_held(T)/p_held(T+n Delta).                  (6.3)

The implementation uses ordinary backward variable-elimination sampling,
formula (6.1), and direct cumulative-hazard event simulation.  It does not
compute or approximate a committor.

## 7. End-to-end consequences of one successful acquisition event

Let p_comp be the held probability under the acquired lower rates.  On
the acquisition event, uniformly over all later deadlines, selected target
subsets, and initial failed subsets to which the same learned table
applies,

    c_rate c_grid p_true <= p_comp <= p_true,               (7.1)

and the conditional-path algorithm satisfies

    TV(returned law, true law given E_T)
       <= (1-c_rate) + (1-c_grid)
       <= n zeta + n^2/N.                                 (7.2)

Taking zeta<=epsilon/(2n) and N>=2n^2/epsilon gives TV at most epsilon.
The same choices give a relative probability deficit at most epsilon,
since c_rate c_grid >= 1-n zeta-n^2/N.

Known static positive multipliers on each component's rates preserve
the relative learned bracket and attractiveness, so the same acquisition
event also supports these interventions.  Arbitrary time-dependent
control policies, repairs, nonmonotone event conditioning, or changes
that destroy local scope/attractiveness require additional arguments.

Future queries may be chosen adaptively from previous answers: all these
claims hold deterministically on the one fixed uniform acquisition event.
The arithmetic and sampling cost of each query remains charged.
The path-law bound is per fresh requested draw.  It is not a fixed total
variation bound for an arbitrarily long transcript of learned-model
samples: repeated samples can distinguish any persistent model error.
For a finite adaptive transcript, the standard sequential coupling bound
adds the per-call total-variation budgets.  Uniform probability bounds
and a lifetime joint-sampling-law bound have different quantifiers.
Conditional probability output alone does not solve arbitrary control
optimization.  The compiler supplies probability evaluation and path
sampling for the specified structurally feasible query class.

## 8. Strong existing routes and the actual candidate opening

This is a structured continuous-time Bayesian network (CTBN).  CTBN local
rates, learning from paths, importance sampling, and conditional trajectory
inference are established.  Fan, Xu and Shelton (JMLR 2010) give importance
sampling, filtering, and smoothing for broad CTBN evidence.  Sturlaugson
and Sheppard (UAI 2014) establish general inference hardness.  Neither fact
by itself certifies an efficient relative approximation in the present
irreversible attractive bounded-width regime.

Encoding progressive dynamics by infection/failure times and using local
factors is also established.  Du, Song, Gómez-Rodríguez and Zha
describe local infection-time factorization for continuous-time independent
cascades.  Braunstein and colleagues use static graphical representations
of progressive cascades for network reconstruction.  Junction-tree and
variable-elimination algorithms, their width dependence, and conditional
backtracking are standard.  These components should be adopted directly,
not claimed as inventions of this construction.

The candidate contribution investigated here is the composable bridge:

    acquired one-sided local experiments
      -> bounded-jump conditional-law domination
      -> rate-independent relative time discretization
      -> exact finite factor inference
      -> continuous conditional paths by driver pullback.

It is stronger than a routine absolute discretization bound: the accuracy
is relative to a possibly exponentially small event and controls the
conditioned fine-time path law.  The difficult representation must still
be acquired, and the physical intervention resources must be real.  A
literature search has not established priority for the relative
discretization/pullback combination.  Independent mathematical review and
a stronger equally informed comparator remain appropriate.

An ordinary direct event-time importance/rejection comparator was actually
implemented for the ten-node short-deadline vignette.  It draws independent
uniform failure times on [0,T]^n and weights the standard complete-path
density.  The bound T^n product_i max_x lambda_i(x) is a valid rejection
envelope.  On that fixture, 100,000 proposals estimated the probability
with 0.431% estimated relative standard error and 0.137% realized relative
error against the positive uniformization check; density evaluation took
about 0.026 seconds in that run.  The compiler's earlier preprocessing
took about 0.291 seconds and its actual relative deficit was 0.493%, with
a looser proved bound.  Rejection needs about 81.2 proposals per ideal
reactive sample on this fixture.  These are synthetic timing observations,
not hardware or physical-experiment costs.

Therefore the selected numerical vignette does not demonstrate practical
superiority over ordinary rare-event methods.  Its purpose is to check
the new execution and certification argument.  The theoretical claim is
the uniform bounded-width operation and its acquisition contract; direct
event-time importance sampling has no claimed polynomial relative-variance
bound for the entire model class.  The comparator and its result are
preserved as direct_event_time_baseline.py and direct_baseline_results.json.

Primary research consulted:

- Fan, Xu, Shelton, "Importance Sampling for Continuous Time Bayesian
  Networks", JMLR 11 (2010), 2115-2140:
  https://jmlr.org/papers/v11/fan10a.html
  https://www.cs.ucr.edu/~cshelton/papers/docs/ctbn-is.pdf
- Sturlaugson and Sheppard, "Inference Complexity in Continuous Time
  Bayesian Networks", UAI 2014:
  https://proceedings.mlr.press/r12/university14k.html
- "Scalable Influence Estimation in Continuous-Time Diffusion Networks":
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4704803/
- "Network reconstruction from infection cascades":
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6408341/
- Zwirglmaier and Straub, "A discretization procedure for rare events in
  Bayesian networks", Reliability Engineering & System Safety 153
  (2016), 96-109.  The stated method uses FORM approximations and a
  numerical discretization heuristic; it is a comparator, not the present
  theorem: https://doi.org/10.1016/j.ress.2016.04.008

Relevant Astra inherited source, read at pinned commit
cb87e72296824ae2a677ccd337025d02d20cbb0a:

    updates/FW-moving-heat-observable-20261015/package/derived/root/
    MARKED_CONDITIONAL_SAMPLER.md

Its N870 construction assumes a reference conditional path sampler and
local residual-rate access.  It explicitly separates its ideal exact law
from finite-bit implementation and unacquired physical rates.  The present
construction does not treat those interfaces as already earned.

## 9. Informative failures and scope limits

1. A generative finite-state kernel plus a minimum local probability already
   allows standard kernel estimation and positive forest/state-elimination
   calculations of rare hitting probabilities.  Merely rediscovering that
   endpoint is not the scientific destination.

2. A low-state-count hidden model need not be learnable from terminal-only
   observations.  An unknown length-L binary password has a deterministic
   machine with L+2 states, but each failed whole-word membership experiment
   eliminates at most one candidate.  Finding an accepting trajectory or
   distinguishing no accepting word from a uniformly hidden accepting word
   requires order 2^L experiments.  Revealing whether every prefix remains
   valid changes this to order L controlled tests.  Reset and low rank do
   not supply the missing informative observation.

3. Naive local quadrature of the continuous path density can have constants
   depending on rate_max*T, and arbitrary absolute error in p becomes
   useless when p is tiny.  The held process is chosen for its monotone
   pathwise coupling and normalized local factors, not because time bins
   alone cure rare-event inference.

4. Returning binned trajectories or held-process trajectories is not the
   claimed fine-time conditional sampler.  The exponential-driver pullback
   and undelayed replay are necessary.

5. Bounded degree does not imply bounded moral-graph treewidth.  Parent
   discovery that adds many false edges can destroy the promised
   computational gain even if it predicts local rates accurately.

6. Finite observed data cannot establish an unrestricted Markov,
   irreversibility, locality, or causal-clamp model.  These are scientific
   model assumptions.  Learned local coefficients and scopes are earned
   conditionally on them; their physical validity is a separate question.

7. Repair, inhibition, and late scheduled actions can invalidate the
   bounded-jump/time-elasticity coupling.  For example a process can have a
   sharp externally scheduled transition just before T; shrinking T need
   not preserve event probability by a power of the shrinkage factor.

8. Mathematical rarity independence does not eliminate local waiting-time,
   actuation, memory, width, or numerical-precision costs.  The supplied
   implementation demonstrates the construction on synthetic local rates;
   it is not physical rate acquisition or a hardware speed claim.

9. The n^2/N scaling is substantive for this particular held-interaction
   scheme.  Consider an activating chain: node 1 has constant rate lambda;
   each subsequent node has rate zero until its predecessor fails and rate
   lambda afterwards.  As lambda*T tends to zero, the true completion
   probability is asymptotic to (lambda*T)^n/n!, while the held completion
   probability is asymptotic to choose(N,n)(lambda*T/N)^n.  Their ratio tends
   to (N)_n/N^n, whose deficit is asymptotic to n(n-1)/(2N) when n^2/N is
   small.  Positive but sufficiently small pre-parent rates approximate
   this example if strict positivity is part of the acquisition model.

10. Attraction is necessary for the held-event comparison.  With two
    components, let both initial rates be M and let the remaining rate
    drop to delta after either fails.  For M*Delta large, the held model
    makes both fail in the first bin with probability almost one.  In the
    true model completion time is Exp(2M)+Exp(delta), whose probability by
    T is approximately delta*T when M*T is large and delta*T is small.
    Thus inhibition can invalidate a relative guarantee by an arbitrarily
    large factor even with only two components.
