# A matching precision cost under continuous observation and adaptive control

30 October 2026. Root construction. Working proof; not yet received.

## 1. Why this question matters to the positive result

The acquired ensemble norm gives an all-future preparation certificate
without finite predictive closure. Its elementary statistical cost is
fourth order in the requested total-variation precision. A loose upper
bound alone cannot show whether that is a real price of the information
being acquired. This construction proves a matching worst-case physical-
time exponent at a specified, stronger continuous-observation interface.

It does not assert that every material has this cost. Adding a useful
readout or control port changes the statistical experiment. Nonregular
rates in latent models, filtering, relative entropy and binary testing are
established machinery; the source and controlled receiving task below are
constructed explicitly. No general n^(-1/4) phenomenon is claimed as new.

## 2. A reciprocal four-state generator menu

The hidden state is (a,b) in {+1,-1}^2. Only a is visible. The baseline mu
is uniform. In temperature/time units fixed once, define the symmetric
generator

    Q_theta = Pi-I+(theta/4)(a b^T+b a^T),          (1)

where Pi is the uniform averaging matrix and a,b are their four-component
Walsh vectors. For 0<=theta<=1/4 every off-diagonal rate is positive and
between 1/8 and 3/8. All generators have the same reversible uniform law.
Their rates and relaxation gap remain bounded away from zero.

Equivalently, from (a,b) the three possible native jumps have rates

    (a,b)->(a,-b)       1/4,
    (a,b)->(-a,b)       1/4,
    (a,b)->(-a,-b)      1/4-theta*a*b/2.              (2)

There is no slow hidden mixing obstruction. The unknown device has either
theta=0 or theta=epsilon>0. The experimenter may choose the baseline Q_0
or the actual active generator Q_theta at any predictable time, adaptively
using the entire visible history, every visible jump time, retained
controller records and independent random seeds. Switching makes no
unmodeled state kick. The experimenter may stop adaptively and may obtain
fresh warranted baseline preparations, including preparation conditioned on
a declared visible a. Those preparations have hidden b uniform conditional
on the complete prior; their cost is additional.

No sensor of b, native hidden-jump counter, bath transition mark, or an
operation that reveals b directly is supplied. The lower bound includes
all records available at the stated interface, rather than discarding
visible timing or a known controller selector. It is not a lower bound
against a different apparatus with additional access.

## 3. A one-time-unit preparation differs at first order in hidden state

Use input f=1+a, the actual uniform law conditioned on a=+1. Compare the
candidate exp(Q_theta) with the reference exp(Q_0). On the span of a,b,
Q_theta has matrix [-1,theta;theta,-1]; on ab it is -1. Thus the output
densities are exactly

    rho_theta=1+e^(-1)[cosh(theta)*a+sinh(theta)*b],
    rho_0    =1+e^(-1)*a.                           (3)

Their full-state total variation and squared echo distance are

    d_theta=(e^(-1)/2) sinh(theta),                 (4)
    D_theta=e^(-2)[(cosh(theta)-1)^2+sinh(theta)^2]
           =2e^(-2) cosh(theta)(cosh(theta)-1).      (5)

The derivation of (4) uses sinh(theta)>cosh(theta)-1 for theta>0 and
averages the four absolute density differences. Hence d_theta is order
theta, while the visible endpoint difference is only order theta^2.
A later actual swap of a and b followed by the ordinary a readout would
expose the first-order difference. Such a new later intervention is among
the receivers for which the state certificate is intended. Supplying that
swap already during calibration would change the lower-bound interface.

The exact three echo entries are

    K(theta,theta)=1+e^(-2)cosh(2theta),
    K(theta,0)    =1+e^(-2)cosh(theta),
    K(0,0)        =1+e^(-2).                        (6)

They give (5) without learning the four-state generator. In particular,
the positive procedure is available on this source at its declared cost.

## 4. Adaptive observation cannot expose a first-order visible signal

Under the theta=epsilon source let u_t in {0,1} select active versus
baseline and put q_t=epsilon*u_t. Let

    h_t=E_epsilon[b_t | complete visible/controller history through t].

Given a current visible a, the visible flip intensity is

    lambda_t=1/2-(q_t a_t h_t)/2.                   (7)

Between visible flips the exact conditional filter is

    dh/dt=-h/2+(q_t a/2)(1-h^2).                   (8)

The first term is the unobserved b-flip generator, and the second is the
Bayesian no-visible-jump update from its state-dependent intensity.
At a visible flip, using a immediately before the flip,

    h_after=q_t a_before/(1-q_t a_before h_before). (9)

Indeed the conditional numerator for the new b is q_t a_before/2,
and the event intensity is (1-q_t a_before h_before)/2. Both the pure
a flip and simultaneous a,b flip must be included; silently observing
which native jump occurred would be a stronger sensor.

Fresh qualified preparation starts with h=0. For 0<epsilon<=1/4 the
interval [-2epsilon,2epsilon] is invariant under every predictable control:
at +2epsilon the right side of (8) is at most -epsilon/2, and at
-2epsilon it is at least epsilon/2. Equation (9) has magnitude at most
epsilon/(1-2epsilon^2)<2epsilon. Baseline calls are the q=0 case; switching
is continuous in h, and any allowed fresh preparation resets h to zero.

Therefore, on **every visible history**, including rare ones,

    |h_t|<=2epsilon,
    |lambda_t-1/2|<=epsilon^2 u_t.                 (10)

Adaptive controls, rare visible-history selection and continuous sensing
cannot turn the hidden first-order discrepancy into a first-order visible
hazard at this menu. Failed selections and their elapsed time remain in
the record and budget.

## 5. Full recorded experiment has only fourth-order information rate

Under theta=0, visible a flips at constant rate lambda_0=1/2 regardless of
the controller. For a fixed controller, its own random seeds have the same
law under both sources; its commands are the same functions of the visible
history. The observed point-process likelihood therefore gives

    KL(P_epsilon^record || P_0^record)
      = E_epsilon integral [lambda log(lambda/lambda_0)
                            -lambda+lambda_0] dt
      <= 2 epsilon^4 E_epsilon T_active.            (11)

The inequality follows from log z<=z-1:
lambda log(lambda/lambda_0)-lambda+lambda_0
<= (lambda-lambda_0)^2/lambda_0, followed by (10).
T_active is total actual time using the unknown active generator, summed
over all specimens and attempts. Baseline waiting, preparation and sensing
costs only increase the full budget. Initial visible labels selected by
the qualified supplier have the same conditional law under both hypotheses
and add no distinguishing term. Their future feedback is already included.

The formula first holds at bounded stopping times. Truncation and the
bounded positive intensities extend the upper bound to an experiment with
finite expected active time. If that expectation is infinite, the claimed
lower bound is already satisfied. Controller postprocessing, storage and
declared calibration output cannot increase relative entropy.

## 6. Matching lower bound for a useful certificate

Suppose a certifier must accept an exactly matching preparation under
theta=0 with probability at least 1-alpha, and reject the theta=epsilon
source when its distance (4) exceeds the declared separated tolerance,
also with probability at least 1-alpha, where 0<alpha<1/2. Its decision
is a binary test. Relative-entropy data processing implies

    KL(P_epsilon^record || P_0^record)
       >= (1-2alpha) log((1-alpha)/alpha).           (12)

Combining (11) and (12),

    E_epsilon T_active
       >= [(1-2alpha) log((1-alpha)/alpha)]
                              /(2 epsilon^4).      (13)

Because d_epsilon is proportional to epsilon on (0,1/4], this is
Omega(d_epsilon^(-4) log(1/alpha)) in the small-alpha regime. The model-
free echo estimator has the same precision and confidence exponents at
bounded input B=2 and fixed word durations. It also pays preparation,
reading and restoration; (13) lower-bounds only the active native time.

The lower bound gives the conventional estimator the complete parametric
family, its exact filtering equations, continuous visible jump times,
adaptive generator switching, fresh qualified input preparations and any
computation. It is not a restriction to a particular moment estimator or
nonadaptive echo protocol. An algorithm that always refuses to certify
does not satisfy the useful null-acceptance condition.

## 7. What changes the law

If the extra a<->b swap/read port is made available during calibration,
the endpoint hidden mean e^(-1)sinh(epsilon) is directly observable after
one candidate execution. Ordinary bounded-variable estimation then tests
the two hypotheses in O(epsilon^(-2)log(1/alpha)) fresh executions. This
does not contradict (13); it changes the accessible experiment.

The target precision also matters. Certifying only the original visible
endpoint mean to tolerance delta is an ordinary delta^(-2) task. Requiring
qualification against every later common intervention asks for hidden-state
precision d, while this material exposes its effect on the original sensor
only at order d^2. That stronger objective is warranted for reusable
preparations whose future use is not fixed, and may be unnecessary for a
single declared observable task. The theorem is not a reason to impose
full-state qualification on every controller.

This example couples the positive completeness result to an explicit
physical information budget. It establishes an interface-specific worst
case, not a universal thermodynamic lower bound, a practical speedup or a
new generic theory of singular statistical estimation.
