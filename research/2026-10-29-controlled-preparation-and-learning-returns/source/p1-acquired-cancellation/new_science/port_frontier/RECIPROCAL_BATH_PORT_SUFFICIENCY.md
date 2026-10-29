# A reciprocal thermal port: acquired memory sufficient for every bounded history controller

29 October 2026. Complementary construction by the port-information agent.
Ordinary proof below; not yet an independent internal review. This is a
conditional native source class, not a claim that fitting a GLE certifies it.

## 1. Consequence and actual physical interface

One scalar mechanical port can support all-history controlled prediction without
observing the bath microstate, provided the bath is genuinely reciprocal, linear
and thermal, and the port has a specified independent white thermal channel.
The sufficient acquired object is the memory kernel together with the Gaussian
noise law it physically determines. It is stronger than a stationary marginal,
a single relaxation time, a fitted equilibrium correlation, or a retained bit.

The directly observed coordinates are q,p. The known external potential V is
C^1 with globally Lipschitz derivative, |V'(q)|<=v0+L|q|. The Gibbs law
nu_V(dq) M_tau(dp) is normalizable and has supplied finite second moment M0.
The native finite-dimensional bath has unobserved z in R^r:

    dq = p dt,
    dp = [-V'(q)-gamma p+C z+u_t]dt + sqrt(2 gamma tau)dW,
    dz = [-Lambda z-C^T p]dt + sqrt(2 tau Lambda)dB.          (1)

Here gamma,tau>0, Lambda is symmetric nonnegative, C is a row vector, and
W,B are independent Brownian motions. The usual positive-relaxation case has
Lambda>0. Temperature, force calibration, the additive port actuation, and this
reciprocal structure are native hypotheses. The controller is any common bounded
progressively measurable functional of the observed port history and its own
independent randomization, |u_t|<=B. It receives no hidden z or future bath noise.

The baseline canonical law is

    rho(dq dp dz) proportional to exp[-(V(q)+p^2/2+|z|^2/2)/tau].

Antisymmetric coupling between p and z preserves the energy; the dissipative
terms preserve their Maxwell factors. Under the physical parity (q,p,z)->(q,-p,z),
the conservative part changes sign and the dissipative part does not. Thus this
is a genuine equilibrium reciprocal thermal realization, not an arbitrary
nonreciprocal colored-force surrogate. The law factors in the shifted bath
coordinates z. A fresh baseline Gibbs preparation is a substantive resource.

## 2. Exact elimination and the sufficient physical record

Solving the last equation of (1) and substituting gives

    dp = [-V'(q)-gamma p-int_0^t K(t-s)p_s ds+u_t+xi_K(t)]dt
                                                    +sqrt(2gamma tau)dW,
    K(t)=C exp(-Lambda t) C^T.                              (2)

Under the stated equilibrium preparation, xi_K is centered stationary Gaussian,

    E[xi_K(t)xi_K(s)]=tau K(|t-s|),

and its entire path is independent of q0,p0 and W. This follows directly from
z0~N(0,tau I), independence of B,W, and the OU covariance. Neither elimination nor
the noise law depends on u, including nonlinear, adaptive history feedback.

Therefore the triple (V,K,tau), gamma, the initial port law and this preparation
contract determine the entire observed controlled law for every admitted u.
The hidden number r and its individual bath coordinates are unnecessary.
Different realizations C,Lambda with the same K are equivalent at this port.
This exact statement is standard harmonic/linear-bath GLE physics assembled at
the declared causal interface; it is not claimed as a new microscopic derivation.

Weak existence and uniqueness for bounded history feedback follow by Girsanov
from the Lipschitz Volterra equation without u, conditional on the independent
Gaussian forcing. Mathematical controls must be measurable; operational ones
also need actual sensing, descriptions, execution and precision.

## 3. Uniform full-path control certificate from an acquired approximation

Let K and J be two admitted kernels with K(0),J(0)<=kappa. Both models use the
SAME known V,gamma,tau, the same initial port law, and the same controller. Put

    delta_K = ||K-J||_(L1[0,T]),
    delta_noise = W2(Law(xi_K),Law(xi_J); L2[0,T]).

The Gaussian transport coupling is a proof device, not a proposed laboratory
operation or a controller with future-noise access. An optimal coupling of the
two complete forcing paths may be sampled in the mathematical initial sigma
field, independently of q0,p0 and W. The port controller still uses only its
declared causal observations.

For any bound P_T >= sup_(|u|<=B) E_K^u int_0^T p_t^2 dt,

    D(P_K^u || P_J^u)
       <= [delta_K^2 P_T + delta_noise^2]/(2 gamma tau),       (3)
    sup_u TV(P_K^u,P_J^u)
       <= min(1, sqrt(delta_K^2 P_T+delta_noise^2)
                                                   /(2sqrt(gamma tau))). (4)

These are FULL observed continuous-path laws, not just snapshots. Hence every
common causal sensor, acquired memory and eventual output obeys (4), regardless
of the final memory alphabet. Precision and acquisition costs are not erased.

### Proof

On the joint Gaussian-environment space, source and comparison drifts differ by

    a_t = -int_0^t (K-J)(t-s)p_s ds + xi_K(t)-xi_J(t).

The common control cancels, even if it is a discontinuous functional of all past
port readings. The known potential and direct damping also cancel. Conditional
Girsanov, followed by marginalization of the auxiliary environment, gives

    D(P_K^u||P_J^u) <= E int_0^T |a_t|^2dt/(4gamma tau).

Young's convolution inequality and (x+y)^2<=2x^2+2y^2 give (3). Infimize over
Gaussian forcing couplings. Pinsker gives (4).

To avoid an unproved global Novikov condition, stop on bounded state and forcing
energy sets. The stopped drift difference is bounded, so Girsanov is valid. The
hybrid comparison uses the J equation before the stopping time and the K equation
afterwards. Both satisfy a common linear-growth moment bound. Thus its exit
probability tends to zero, it converges to the J law, and relative-entropy lower
semicontinuity gives the displayed bound. Conditioning on each Gaussian
environment retains its original distribution; the Brownian channel is the only
changed random input. This argument does not assume the controller is Lipschitz.

A fully explicit conservative moment bound suffices. Define

    a_T = 1+L+gamma+kappa T,
    P_T = 4T exp(2a_T T)
          [2M0+(v0+B)^2 T^2+tau kappa T^2+8gamma tau T].       (5)

Indeed the integrated equation, |K(t)|<=kappa, and q_t=q0+int p imply

    sup_(t<=T)(|q_t|+|p_t|)
    <=exp(a_T T)[|q0|+|p0|+(v0+B)T+int_0^T|xi_K(t)|dt
                                      +sqrt(2gamma tau)sup_(t<=T)|W_t|].

Use (sum of four terms)^2<=4 sum of squares, E(|q0|+|p0|)^2<=2M0,
E(int|xi|)^2<=tau kappa T^2, and Doob E sup|W|^2<=4T.
Formula (5) is deliberately conservative, not an efficient long-time estimate.

## 4. A finite covariance record controls both terms

Suppose the WARRANTED bath spectrum lies in [0,Lambda_max] and K(0)<=kappa.
Then K(t)=int exp(-lambda t)mu(dlambda), mu>=0, mu(total)<=kappa,
and |K'|<=kappa Lambda_max. The candidate has the same promises. No lower
relaxation bound is needed for a fixed finite T; one is needed for reset claims
based on waiting. Zero-rate modes need a genuine thermal initial preparation.

Take T=mh and cells I_i=[ih,(i+1)h], i=0,...,m-1. Let A_K be the covariance
matrix of the cell averages h^-1 int_(I_i)xi_K(t)dt. Its entries are

    (A_K)_ij = tau h^-2 int_(I_i)int_(I_j) K(|t-s|)dt ds.

Assume a simultaneous acquired certificate

    max_ij |(A_K-A_J)_ij| <= tau delta.                       (6)

The ordinary piecewise-constant orthogonal projection Pi_h satisfies

    E||xi_K-Pi_h xi_K||_(L2)^2
       <= tau kappa Lambda_max T h/3,                        (7)

and the same for J. To see (7), write the projection residual in one cell as
(2h)^-1 int int E|xi(t)-xi(s)|^2 and use
E|xi(t)-xi(s)|^2<=2tau kappa Lambda_max|t-s| and
int_0^h int_0^h |t-s|dt ds=h^3/3.

Common-standard-Gaussian coupling of cell averages gives the finite matrix cost
sqrt(h)||A_K^(1/2)-A_J^(1/2)||_F. A self-contained conservative bound is

    ||A^(1/2)-D^(1/2)||_F <= 2 m^(1/4)||A-D||_F^(1/2).       (8)

For proof, regularize A,D by epsilon I. The square-root difference X solves
S_A X+X S_D=A-D, whence ||X||_F<=||A-D||_F/(2sqrt(epsilon)); each regularization
cost is at most sqrt(m epsilon). Optimize epsilon=||A-D||_F/(4sqrt(m)).
The exact Gaussian Bures transport cost can improve (8), but is not needed.

Triangle inequality, (6)--(8) yield the fully finite certificate

    delta_noise
      <= 2sqrt(tau kappa Lambda_max T h/3)
                          +2sqrt(tau T sqrt(m) delta),        (9)
    delta_K <= T[delta+4kappa Lambda_max h].                  (10)

For (10), compare each time to a nearby cell lag and each kernel to its cell
average. Each incurs at most 2kappa Lambda_max h. All constants are elementary.
Substitute (9)--(10) into (4). Arbitrarily fine continuous-path classification is
covered only because this record controls the stronger physical influence law.
This does not follow from baseline entropy or finite stored memory size.

## 5. Finite physical acquisition by clamping and integrated reaction readings

The required operation is to hold the mechanical port at fixed q (p=0), while
retaining the reciprocal bath and known white port thermostat. Under the genuine
baseline Gibbs preparation, the shifted z is already independent thermal. During
the clamp it obeys an autonomous stationary OU law. Holding q costs an actuator
and changes the native experiment; this is not ordinary passive q observation.

An ideal constraint does no displacement work, but its force capacity, control
bandwidth, dissipation, sensing and finite precision are NOT free. Imperfect clamp
motion changes the bath through -C^T p; its resulting error must be bounded.

Crucially, an instantaneous colored-force reading is NOT assumed. The measured
mean reaction over a cell, after subtracting the known constant V'(q), is

    R_i = h^-1 int_(I_i)xi_K(t)dt
                         +sqrt(2gamma tau) Delta W_i/h.       (11)

A sign change of all R_i is immaterial to covariance. Thus

    Cov(R_i,R_j) = (A_K)_ij + (2gamma tau/h) 1_(i=j).          (12)

The finite integrated impulse measurement has a known white-noise contribution;
it is subtracted at the covariance level, not pathwise or by inventing access to
the microscopic noise. This is the decisive preparation/measurement step.

An imperfect finite clamp can use an actually measured balance residual instead.
If a calibrated enclosure/servo plus metrology warrants
sup_(s<=T)|q_s-q0|<=epsilon_q, record the momentum endpoints and the integrals of
the known V'(q), gamma p and applied clamp force u_clamp. The computable residual

    [p_(i+1)-p_i+int_(I_i)(V'(q)+gamma p-u_clamp)dt]/h

equals (11) minus the cell average of K*p. Integration by parts gives

    (K*p)(t)=K(0)(q_t-q0)+int_0^t K'(t-s)(q_s-q0)ds,

so |K*p|<=2kappa epsilon_q, using complete monotonicity. Thus a finite-motion
clamp adds a bounded reading error; it does not need a pathwise measurement of
xi. Endpoint precision and quadrature errors of the balance terms must also be
included. If the displacement certificate can fail, its joint failure probability
is charged; trajectories must not be silently selected by successful confinement.
This constructs error propagation for an imperfect operation, not a claim that
an actual enclosure/servo or its force/work budget has been acquired.

Each R_i is centered Gaussian with variance at most

    v = tau(kappa+2gamma/h).

Use N=kr genuinely independent clamped preparations, k odd blocks of r trials.
For each pair i,j, Var(R_i R_j)<=2v^2. Chebyshev makes a block mean deviation
2sqrt(2)v/sqrt(r) have probability <=1/4. The median of blocks fails with
probability <=exp(-k/8). A union bound over m^2 entries gives an honest simultaneous
covariance uncertainty. Toeplitz stationarity can reduce the number of fitted
entries, but no independent within-path samples are assumed.

Finite sensor range and precision can be included explicitly. Clip each R_i to
[-R,R], without discarding the trial. For a Gaussian pair with variances <=v,

    |E(R_i R_j)-E(clip_R R_i clip_R R_j)|
                           <=2sqrt(3)v exp[-R^2/(4v)].        (13)

This follows from Cauchy--Schwarz, E R_i^2 R_j^2<=3v^2, and the Gaussian union
tail bound. For these CLIPPED products use Var<=3v^2 and block deviation
2sqrt(3)v/sqrt(r), rather than transferring the sharper untruncated variance
bound without proof. The same exp(-k/8) median failure bound holds.
Calibrated clipped-reading error <=epsilon_R contributes at most
2R epsilon_R+epsilon_R^2 to a product. Arithmetic and calibration errors in
2gamma tau/h are separate additions. Finite range R, resolution epsilon_R and
their bit count ceil(log2(2R/epsilon_R+1)) are paid. Exact Gaussian tails here
come from the warranted bath class, not a fitted normal histogram.

## 6. Positive finite fitting and execution

Choose a rate mesh lambda_l in [0,Lambda_max] and weights w_l>=0,
sum w_l<=kappa. The candidate J(t)=sum_l w_l exp(-lambda_l t) is a native thermal
kernel. For lag k the cell-averaged exponential feature is

    psi_lambda,0 = 2(lambda h-1+exp(-lambda h))/(lambda h)^2,
    psi_lambda,k = exp[-lambda(k-1)h]
                    [(1-exp(-lambda h))/(lambda h)]^2, k>=1,

with continuous value 1 at lambda=0. Thus fitting measured covariances with
simultaneous intervals is an ordinary linear program in nonnegative weights.
If the rate mesh has radius epsilon_lambda, moving each spectral mass to its
nearest rate changes every kernel/covariance feature by <=kappa T epsilon_lambda.
A feasible approximate source therefore exists at this tolerance. A returned
candidate's achieved residual, data uncertainty and certified coefficient
rounding supply delta in (6); no inference of hidden order is needed.

An equally informed existing GLE method can use this same record and positive
fit. An ordinary auxiliary OU solver realizes the candidate using z_l with
C_l=sqrt(w_l), Lambda_ll=lambda_l. Charge LP variables/constraints and precision,
Gaussian initialization, step size, simulation error, number of service rollouts,
and actual controller sensing/execution. The theorem itself is a law-level
certificate, not an executed end-to-end device or a runtime speedup.

For fixed native constants and finite T, the coarse displayed estimates can
reach output-TV epsilon with h=O(epsilon^2), delta=O(epsilon^3). The direct white
reaction variance makes N=O(epsilon^-10 log(m/alpha)) independent trials sufficient,
with m=O(epsilon^-2) cell readings per trial. This is a conservative existence
schedule, not an optimal complexity claim. Better GLE estimators may be much
stronger. If a separately calibrated colored-force sensor exists, it changes
the variance/cost contract; it is not assumed in (11).

Total acquisition includes N actual equilibrium preparations, N clamped runs of
length T, mN integrated readings, range/precision, source and instrument stability,
clamp imperfections and bath calibration. Calibration and service must have
genuinely independent initial baths, or their actual joint conditional law must
be modeled. Waiting or resetting only q,p does not regenerate hidden z.

## 7. Limits and strongest comparison

Lei, Baker and Li (PNAS 2016) already learn GLE kernels/noise from equilibrium
statistics and build auxiliary Markov realizations satisfying FDT. This is a
strong comparator, not an inferior curve fitter. General Mori--Zwanzig reduction
does not automatically give (2): Ayaz, Dalton and Netz (2022) derive nonlinear
memory and initial-state dependent, generally non-Gaussian random forces. Netz's
2023 all-orders driven projection similarly has non-Gaussian correction terms.
Muller et al. (2020) show how additional one-step linear perturbation experiments
can determine coarse second-order response; baseline FDT alone is insufficient.

The useful addition here is an explicit physical clamp/impulse contract plus a
uniform FULL-PATH, all-bounded-history control certificate in finite acquired
covariance errors, with hidden bath dimension eliminated. The native harmonic
influence law, Girsanov and Gaussian covariance fitting are known ingredients.
Historical novelty, favorable practical scaling, an actual bath specimen,
acquired physical resets and an executed native advantage are NOT established.

No theorem here repairs a completely general hidden diffusion from its baseline
output law. In particular the reversible finite-state similarity counterexample
developed independently by root and this agent exposes a missing multiplication
operation. Extending a fitted covariance law beyond the warranted reciprocal
linear bath would silently reintroduce that unresolved information problem.
