# A recorded actuator-noise law is a complete intervention record

29 October 2026. Complementary construction by the causal-noise frontier.
Ordinary proof below; no independent review is claimed in this file. This is
not a claim that thermal noise has been measured or that a white-noise actuator
has been built. Girsanov reweighting and likelihood-ratio policy evaluation are
existing methods. The useful comparison is the exact physical information they
require, including a necessity statement for the complete response family.

## 1. The physical port and its actual acquisition

Let Z be any warranted, weakly well-posed hidden diffusion and Y its reported
observation process, including whatever common sensor randomness is needed.
An r-dimensional calibrated port adds force through a known matrix J(Z):

    dZ = b(Z) dt + Sigma(Z) dW + sqrt(2 kappa) J(Z) dV,
    kappa > 0.                                                   (1)

Here (W,V) is a joint Brownian motion, with independent components and future
increments independent of the initial full state. J may depend on hidden state:
it only has to be the SAME physical port for the added noise and the subsequent
force. The stated native interpretation is an additive momentum port, where J
is a constant coordinate injection. The hidden drift and hidden dimension need
not be identified. The law of initial hidden state is part of the preparation.

The genuinely acquired record is the JOINT law of (Y,V) during reference runs
of (1). V is either an actually measured native bath innovation, or an external
independent randomized actuator whose command realization is recorded. Knowing
the distribution of V without its pairing to Y is insufficient. An inferred
innovation of the visible marginal is not automatically this physical V.

If an external noise is used, (1) is the noise-AUGMENTED plant. The theorem does
not identify controls of the original plant with that noise removed.

Admissible controls u_t are bounded, predictable functions of the available Y
history and common independent controller initialization. They do not use a
hidden state or an unrecorded action channel. Assume |u_t| <= B. The controlled
physical experiment replaces the last term of (1) by

    J(Z) u_t dt + sqrt(2 kappa) J(Z) dV^u.                       (2)

The other dynamics, preparation and sensing are unchanged. This is a declared
operation, not a conclusion drawn from passive observations.

## 2. Exact sufficiency for the whole bounded feedback family

Set theta_t = u_t / sqrt(2 kappa), K=B^2 T/(2 kappa), and define

    L_u(Y,V) = exp{ integral theta_t . dV_t
                          - (1/2) integral |theta_t|^2 dt }.   (3)

All stochastic integrals are Ito integrals. Boundedness implies Novikov and
E L_u=1. Girsanov makes V^u=V-integral theta dt a Brownian motion under
dP^u=L_u dP. The unshifted W remains Brownian jointly with V^u, since the vector
change of drift shifts only V. Substitution into (1) yields exactly (2).
The initial full-state law is unchanged because the exponential has conditional
mean one given the initial sigma field. Weak uniqueness identifies this changed
measure with the specified physical experiment.

Therefore, for every bounded measurable functional f of the complete reported
path,

    E^u f(Y) = E[ f(Y) L_u(Y,V) ].                              (4)

One acquired joint law serves EVERY admitted feedback, without observing or
fitting the hidden dynamics. The word "one" describes a reusable population
record; finite data and numerical precision remain charged separately.

If a consequence also includes the actual actuator noise recorded in the
controlled experiment, the correct formula is

    E^u f(Y,V^u) = E[ f(Y,V-integral theta(Y)dt) L_u(Y,V) ].      (5)

It is incorrect to identify the unshifted coordinate V on the right with the
controlled innovation V^u. Controls using V^u as feedback require a separate
causal transformation/well-posedness construction and are not included here.

## 3. Necessity: the noise pairing is precisely the missing population object

Take two reference laws P and Q of (Y,V) with the SAME Y marginal and the SAME
standard Brownian V marginal. Suppose they have identical Y laws under every
bounded deterministic open-loop port force, including every finite step force.
Then their JOINT (Y,V) laws are equal.

Proof. For every bounded measurable f(Y) and every deterministic step function
h in L2([0,T];R^r), equality of controlled output laws says

    E_P[f(Y) exp{integral h.dV - ||h||_2^2/2}]
      = E_Q[f(Y) exp{integral h.dV - ||h||_2^2/2}].              (6)

No single amplitude ceiling is needed beyond an open neighborhood of zero for
each finite-dimensional family. If a fixed B>0 is imposed, scaling all members
of any finite list of step functions into that neighborhood suffices below.

For an event A of Y, define finite measures on Wiener space
mu_P(A,dv)=P(Y in A,V in dv) and mu_Q analogously. Both are dominated by Wiener
measure with densities in [0,1]. Their density difference is in L2(Wiener).
The stochastic exponentials of deterministic step functions are total in that
L2 space: on each finite Gaussian increment vector, their Laplace transforms
determine all Hermite coefficients, and these finite increment sigma fields
generate Wiener space. Equivalently, the finite-dimensional signed Laplace
transform vanishes on an open neighborhood and analytically everywhere; the
Gaussian domination supplies its entire exponential moments. Thus (6) implies
mu_P(A,.)=mu_Q(A,.). Rectangles generate the product sigma field, proving the
claim for standard Borel Y.

Consequently the family of ALL open-loop response laws and the paired-noise
joint law carry exactly the same population discrimination information once
the baseline Y law is fixed. The theorem does not say either representation
can be acquired cheaply. It explains why matching passive Y, including its
entire stationary time law, cannot substitute for the missing pairing.

A convenient reduced object is the regular conditional law I(dv|y) of V given
the COMPLETE visible path. Then

    dP_Y^u/dP_Y (y) = integral L_u(y,v) I(dv|y).                (7)

I is an offline conditional record, not itself a causal forward simulator.
Converting it to a generative controlled model or efficiently sampling a rare
weighted consequence is an additional computational task.

## 4. A finite controller family has a finite path record

For predictable reported-history features phi_1,...,phi_m taking values in
R^r, consider u_alpha(t)=sum alpha_j phi_j(t,Y). Restrict alpha to a declared
set where |u_alpha|<=B. Define

    S_j = (1/sqrt(2 kappa)) integral phi_j . dV,
    H_jk = (1/(2 kappa)) integral phi_j . phi_k dt.              (8)

Then L_alpha=exp(alpha.S-alpha^T H alpha/2). The JOINT record (Y,S,H) supplies
every bounded consequence for every alpha in this controller family. H is a
functional of Y when the features and clocks are fully specified. No scalar
entropy value or separately measured S marginal supplies this joint record.

For snapshot-held features, phi_j is fixed on each interval from the charged
earlier reports, and S,H are finite sums of recorded V increments and known
time intervals. This eliminates an ideal Ito-integration step FOR THAT CONTROL
CLASS. It does not make white-noise physical implementation or exact Gaussian
random numbers free. A real colored/quantized command source defines a different
reference channel and must use that channel's actual likelihood ratio.

For a known family and a fixed queried alpha, (8) can be accumulated online;
record dimension m+m(m+1)/2 does not count the acquisition resolution, dynamic
range, temporary state or number of reference trials.

## 5. Complete statistical and preparation cost, with a strong comparator

The second moment is bounded by

    E L_u^2 <= exp(K),  K=B^2 T/(2 kappa).                     (9)

Indeed L_u^2 is the stochastic exponential for 2theta times
exp(integral |theta|^2), and the latter is at most exp(K). For |f|<=1,
the ordinary importance-sampling estimator based on N genuinely independent
reference preparations has mean-square error at most exp(K)/N. Chebyshev gives
failure <=exp(K)/(N epsilon^2); a median of independent block averages yields
N=O(exp(K) epsilon^-2 log(1/delta)) for a FIXED query. A finite predeclared set
of M queries pays a log(M/delta) confidence factor using the same sample set.
An unrestricted adaptively chosen controller requires uniform class control or
fresh evaluation data. It is not licensed by a pointwise bound.

The bound is attained for the likelihood's second moment for deterministic
constant full-amplitude forcing: E L_u^2=exp(K). This establishes the variance
of this route, not a minimax lower bound against every learning method. Direct
execution of one chosen controller can be much cheaper when allowed. A fitted
hidden model or a standard system-identification method may also be superior
when useful structure is warranted. Ordinary Girsanov or randomized-policy
importance sampling is the equally informed comparator and executes this
construction; no speedup over it is claimed.

Acquisition requires N actual independent initial preparations, duration NT,
the complete charged Y record required by phi/f, the synchronized physical
actuator record, calibration of kappa and the port J, and arithmetic/range
control for scores and weights. Waiting in one trajectory does not give N
independent preparations without a separate warranted mixing argument.

## 6. Why decreasing the added noise is not free

For a directly thermalized momentum port, adding independent actuator noise
changes its observed quadratic variation. If the original local noise covariance
is D and the added covariance is 2 kappa I, continuous momentum paths have
quadratic variation (D+2 kappa I)t rather than Dt. Thus the corresponding full
continuous-path laws are singular for every kappa>0. No likelihood reweighting
removes the added bath at that scope. Finite-resolution consequences may converge
as kappa decreases under additional continuity estimates, but (9) then grows
as exp(B^2 T/(2 kappa)). The intended consequence must select the tradeoff.

The augmented actuator noise need not be a thermal bath. Its work, friction and
entropy interpretation are separate physical questions. This note claims only
causal prediction under the declared perturbation channel.

## 7. Relation to existing primary work

Schäfer and Keller, *Implementation of Girsanov Reweighting in OpenMM and
Deeptime*, J. Phys. Chem. B 128 (2024), 6014--6027, DOI
10.1021/acs.jpcb.4c01702, explicitly record random numbers and force differences
at integrator resolution. Their method is exact for its stochastic numerical
channel and already reuses reference paths for changed dynamics. Integrator
absolute continuity is substantive; a continuous Girsanov formula cannot simply
be pasted onto every splitting method.

Warren and Allen, *Malliavin Weight Sampling: A Practical Guide*, Entropy 16
(2014), 221--232, arXiv:1312.7480, constructs auxiliary score records for response
derivatives in stochastic simulation. Equations (3), (8) retain that known
likelihood-score structure; the present note's emphasis is complete response
equivalence and the native acquisition gate under partial observation.

Tennenholtz, Shalit and Mannor, AAAI 2020, DOI 10.1609/aaai.v34i06.6590, studies
off-policy evaluation when the behavior policy depends on unobserved state.
Its confounding obstruction must not be imported into our known independent
randomized-actuator contract. Conversely, a behavior policy inferred only from
visible marginals does not satisfy our contract.

No historical novelty claim is made for (3)--(5), finite score compression,
or importance sampling. The necessity result and explicit operation comparison
are proposed useful structural statements pending independent review.
