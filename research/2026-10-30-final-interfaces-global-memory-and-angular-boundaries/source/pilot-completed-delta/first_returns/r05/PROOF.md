# Finite-ADC learning by reducing drive energy, with a uniform task certificate

## Scientific result and scope

For a calibrated passive input/output port, a fixed finite-horizon incremental
map can be identified, with an explicit finite confidence ceiling, from one
persistent specimen using only forward experiments and a finite-level ADC.
Unknown memory is allowed to depend on every earlier command; no relaxation
rate, mixing time, reset, adjoint or inactive waiting window is required.
The mechanism is ordinary randomized system identification with reduced probe
energy and a record-based correction for clipping. It is not an advantage
over an equally informed ordinary identifier: that identifier can run precisely
this construction.

The distinguishing mathematical content is the joint bridge:

* clipping attenuates a fresh-sign scalar contrast by an amount controlled by
  its conditional saturation probability;
* actual retained saturation flags and squared finite-ADC reports give an
  anytime confidence set even for arbitrary causal additive memory;
* pathwise passive port energy provides a finite, rate-independent ceiling
  for this record certificate when probe energy is sufficiently small;
* one certified operator supplies a uniform certificate for all later bounded
  ridge-control tasks, including tasks selected from the acquired record.

The last two statements require the actual energy and actuator/readout
calibrations below. Mere abstract conditional passivity of an unspecified
readout is not silently upgraded to this stronger port contract. These are
mathematical and simulated results, with no physical apparatus qualification
or established priority claim.

## Model and operations

All norms are Euclidean or induced spectral norms. Commands and measured
waveform coefficients are in calibrated energy coordinates. There is a fixed
unknown real matrix A of size m by d, and for window i

    y_i = A u_i + w_i.

The old field w_i is measurable before the fresh sign for window i is drawn.
It can contain arbitrary persistent hidden state. A known entry bound is
|A_kj| <= L. A natural realization is the loaded passive scattering port

    x_{i+1} = R x_i + B u_i,
    y_i     = C_state x_i + A u_i,

whose whole block matrix is a contraction in these energy coordinates.
Then for every realized command sequence and horizon T,

    sum_{i<=T} ||y_i||^2 <= E0 + sum_{i<=T} ||u_i||^2.             (P)

E0 is a warranted initial stored-energy upper bound, including dark modes.
No bound on the dimension, decay rate or mixing of the state is needed.
Finite waveform windows can be used; A then denotes that finite waveform
map. This does not identify an infinite-horizon/DC gain by extrapolation.

Cycle deterministically through input columns j. In each window use

    u_i = r s_i e_j,       P(s_i=+1 | complete pre-sign history)=1/2.

The sensor has fixed range [-C,C], a finite grid of M levels and spacing
Delta=2C/(M-1). It reports q_ik and the true overrange flag

    W_ik = 1{|y_ik| > C}.

Fresh dither gives the complete conditional contract

    E[q_ik | pre-read history, current sign, command, y_i]
        = clip_C(y_ik),
    |q_ik - clip_C(y_ik)| <= Delta.

This operation does not require a prior high-precision digitization of y:
for a scalar analog y, add U*Delta with U uniform on [0,1), floor on the
shifted threshold ladder, and clamp to the M output levels. Two calibrated
analog endpoint comparators produce the overrange flag before dither.
The random dither must be fresh conditional on the complete history. Merely
marginally unbiased ADC errors do not suffice. All saturated reports remain
in the record and in every estimate.

## Fresh-sign clipping identity

Fix a column j, one output coordinate k, and write a=A_kj. Define

    z_i = s_i q_ik/r,
    mu_i = E[z_i | complete pre-sign history].

Conditional on history, w=w_ik is fixed, so

    mu_i = [clip_C(w+ra)-clip_C(w-ra)]/(2r).                     (1)

Clipping is monotone and 1-Lipschitz. Consequently mu_i=a*theta_i
for some theta_i in [0,1]. If neither sign clips then theta_i=1.
Let p_i=E[W_ik | pre-sign history]. If a nonzero attenuation occurs,
at least one of the two signs clips, so p_i>=1/2. Thus

    0 <= 1-theta_i <= 2 p_i.                                  (2)

This is valid for positive and negative a, every w and every r,C>0.
No assumption that memory is independent of earlier signs is used.
At a=0 the contrast is zero and theta_i can be set to one.

In particular, a fresh sign alone does NOT make a clipped report unbiased.
It cancels the additive old field before clipping, while the clipped
contrast estimates an attenuated slope.

## A confidence set from the acquired record

There are J=md scalar slopes. Choose total failure probability delta,
predeclare K positive numbers

    eta_l = (r/(2C))*2^{-l},        l=0,...,K-1,

and put H=C/r, c=1-exp(-1),

    ell   = log(4 K J/delta),
    ell_W = log(2 J/delta).

For a column with n observations, the controller retains only

    n,  Z=sum z_i,  V=sum z_i^2,  W=sum W_ik.

Set

    a_raw = Z/n,
    t = min_l {eta_l V + ell/eta_l}/n,
    Q_up = (W+ell_W)/c,
    beta = min(1, 2 Q_up/n).                                  (3)

These are all device information. They do not use w, hidden energy, a
population loss or an audited error.

### Martingale proof of the mean bound

For |x|<=1/2, exp(x-x^2)<=1+x. Since |eta_l z_i|<=1/2,

    E exp(eta_l(z_i-mu_i)-eta_l^2 z_i^2 | history) <= 1.

The same holds with -eta_l. The products are nonnegative
supermartingales starting at one. Ville's inequality, unioned over the two
signs, K values and J slopes, gives, simultaneously for every sample count,

    |a_raw - (sum mu_i)/n| <= t                               (4)

except on a set of probability at most delta/2.

### Martingale proof of the warning bound

For any Bernoulli W_i with conditional mean p_i,

    E exp(c p_i - W_i | history)
      = exp(c p_i) (1-c p_i) <= 1.

Ville's inequality and a union over the J slopes give

    sum p_i <= (W+ell_W)/c                                   (5)

simultaneously in time, outside another set of probability delta/2.
The signs may be independent while the p_i depend arbitrarily on all past
experiments. Neither proof applies an IID concentration theorem to the
observed warm fields.

Combining (1)--(5), on one event of probability at least 1-delta, every true
entry belongs at every time to

    I = { a in [-L,L] : a*theta in [a_raw-t,a_raw+t]
                           for some theta in [1-beta,1] }.   (6)

This is an interval. For beta<1 and v_-=a_raw-t, v_+=a_raw+t,
its lower endpoint before intersection with [-L,L] is v_- if v_->=0 and
v_-/(1-beta) otherwise. The upper endpoint is v_+ if v_+<=0 and
v_+/(1-beta) otherwise. At beta=1, use the limiting intervals; an interval
for the mean containing zero permits any a in [-L,L].

Take Ahat as the matrix of interval midpoints and Rbox as the nonnegative
matrix of half-widths. Then

    ||Ahat-A|| <= ||Rbox|| =: epsilon_A.                      (7)

Indeed |(Ahat-A)x| <= Rbox|x| coordinatewise. The norm ||Rbox|| is the exact
largest spectral norm of the symmetric rectangular error box; using its
Frobenius norm would be a valid but looser bound. The rectangle may contain
nonpassive matrices, which only makes this certificate conservative.

The confidence event is joint in time, so stopping from (7) is legitimate.
An empty interval is not silently discarded: the executable reports a
calibration inconsistency or confidence failure. Saturation is never
treated as an excuse to delete a data point.

## A finite ceiling without a relaxation rate

Here the calibrated pathwise port contract (P), rather than just the
mean energy contract in the supplied source, is used explicitly.
Suppose every column has N observations, so T=dN. Every actual overrange
flag consumes at least C^2 of measured port energy. Therefore, pathwise,

    sum_{j,k} W_kj <= (E0+dN r^2)/C^2.                        (8)

Likewise |q-clip(y)|<=Delta gives

    sum_{j,k} V_kj
       <= 2E0/r^2 + 2dN + 2mdN Delta^2/r^2 =: U.             (9)

No observation or prediction of a last warning is needed. Warnings may
continue indefinitely at fixed r; it is their fraction that is controlled.

If the grid covers the optimizing eta, specifically

    U <= ell H^2 4^K,

then t_kj <= 3 sqrt(ell V_kj)/N + 2H ell/N. The factor three covers a
factor-two grid approximation; the second term covers the upper endpoint
eta_0. Each interval half-width is at most t_kj+L beta_kj. The triangle
inequality for Frobenius norms, (8), (9), and ||W_matrix||_F<=sum W imply

 epsilon_A <= G(N,r)

 G(N,r) = 3 sqrt(ell U)/N + 2C ell sqrt(md)/(rN)
          + [2L/(cN)] [(E0+dN r^2)/C^2 + sqrt(md) ell_W].      (10)

The ceiling is deterministic for the physical record. Its interpretation
as distance to the true operator has the same single failure allocation
delta as the anytime certificate. There is no additional Markov loss,
unknown mixing constant or uncharged waiting time.

As N grows with fixed r, this ceiling tends to 2Ld r^2/(c C^2).
For every prescribed positive epsilon_A, choose r small enough to put
that floor below epsilon_A and then choose a finite N. The leading
nonasymptotic terms are

    O(sqrt(d ell/N) + Delta sqrt(md ell)/(r sqrt(N))
      + sqrt(E0 ell)/(rN) + C ell sqrt(md)/(rN)
      + Ld r^2/C^2 + LE0/(NC^2)).

Taking r^2 proportional to the requested operator error gives the usual
sampling term proportional to epsilon_A^{-2}, a finite-ADC term
proportional to Delta^2 epsilon_A^{-3}, and smaller initial-energy terms,
with dimension and confidence constants as displayed in (10). These are
upper bounds, not optimality or lower-bound claims. The per-window command
amplitude and analog calibration become more demanding as r shrinks.

The executable also minimizes (10) over a declared radius grid using only
calibrations, before instantiating the population model. For m=d=2,
E0<=100, C=.8, M=257, L=1, delta=.01, lambda=.5 and ||b||<=.4, it selects
r=.054. The rounded ceiling is 71,680 forward windows and 209.01888
normalized input-energy units for a uniform task radius below .15. This
ceiling applies to the whole stated passive-port class, not only the
simulated decay rates. It is not a total apparatus work or wall-time bill.

## A uniform certificate for all later ridge tasks

For lambda>0 define

    K_lambda(A) = (A^T A+lambda I)^{-1} A^T,
    u_star(A,b) = K_lambda(A)b.

The following global perturbation bound avoids paying a large gradient
norm coefficient:

    ||K_lambda(A)-K_lambda(B)|| <= ||A-B||/lambda.             (11)

To prove it, let alpha=sqrt(lambda) and form the real block matrix

              [ alpha I_d    A^T    ]
    M(A)  =   [   -A       alpha I_m].

Its off-diagonal part is skew-symmetric, so its smallest singular value
is at least alpha. The top-right block of M(A)^{-1} is -K_lambda(A).
The inverse identity gives

    ||M(A)^{-1}-M(B)^{-1}||
        <= ||M(A)^{-1}|| ||M(A)-M(B)|| ||M(B)^{-1}||
        <= ||A-B||/lambda.

Taking a block proves (11). Its constant is sharp near A=B=0, so this
global bound is not claiming a hidden improvement in ridge conditioning.

Thus the controller's output map b -> K_lambda(Ahat)b has, simultaneously
for every b with ||b||<=B0, the acquired certificate

    ||u_hat(b)-u_star(A,b)|| <= B0 epsilon_A/lambda.            (12)

The b can be selected after examining the entire learning record. No new
experiments are needed to justify each task. Numerical linear algebra and
command execution still cost resources. The standard singular-value bound
||K_lambda(A)||<=1/(2 sqrt(lambda)) ensures the unconstrained optima for
both A and Ahat satisfy the command limit whenever

    B0/(2 sqrt(lambda)) <= command_radius.

That is the scope used in the executable. If the command constraint binds,
(12) is not asserted for constrained optima; one can instead use a
variational-inequality perturbation bound with its larger constants.
This certifies the optimizer of the incremental-map objective. It does not
bound a later total warm output A u+w or prepare a prescribed hidden state.

## First failed attack and the changed mechanism

The scalar lossless plant

    x_{i+1} = -.1 x_i + sqrt(.99) u_i,
    y_i     = sqrt(.99) x_i + .1 u_i,
    x_1=0,

satisfies x_{i+1}^2+y_i^2=x_i^2+u_i^2 exactly. It has true incremental
gain a=.1, and no external bath or initial energy. With u_i=.5 s_i,
|x_i|<=sqrt(.99)*.5/.9. For i>=2,

    |sqrt(.99)x_i| >= .99*.5*(1-.1/.9) = .44,

so |y_i|>=.39>.2 for either current sign. A sensor with C=.2 therefore
clips every read after the first. Its output depends on the old field's
sign and not the new input sign; the conditional contrast is zero.
This is an actual passive indistinguishability of the CURRENT two signed
measurements after clipping, not a claim that all possible experiments
on two different unknown plants are indistinguishable.

Executed with 257 levels and 65,536 windows, it retained 65,535 saturated
reports and the ordinary correlation estimate was .00047150, despite the
true gain .1. Its confidence set correctly remained uninformative.
Keeping the same plant, ADC and random streams, but reducing r to .02,
gave zero saturated reports, estimate .10110140, and operator radius
.02349169. Input energy fell from 16,384 to 26.2144 normalized units.
These are separate matched simulated runs, each with one initialization
and no subsequent hidden-state resets. They are not physical experiments.

The failure changes the experiment rather than only its optimizer:
command-generated memory can replenish clipping forever, so duty-cycle
randomization is replaced here by low-energy dense forward probes.
The sensor resolution cost of those smaller probes is explicitly present
in (9), (10), and in all acquired reports.

## Executed multimode construction and ordinary comparator

The executable uses an orthogonal scattering colligation with two visible
rates .98 and .9999, nonidentical input/output rotations and a dark state
whose energy 9 never decays. Its true initial stored energy is 89; the
design uses only the warranted upper bound 100. True rates, states and A
are never arguments to the controller certificate. The maximum per-step
floating-point energy-balance residual is recorded separately as an audit.

The r=.12 run stopped from its own finite-ADC record at 5,120 physical
forward windows, 5,120 vector reads and 10,240 scalar reports. All 28
saturated scalar reports were retained. It used 73.728 normalized incident
energy units, zero adjoint calls, zero waiting windows and zero resets after
initialization. The joint anytime operator radius was .18181313; (12)
gave .14545050 for every later ||b||<=.4 at lambda=.5. This beats the
zero-experiment radius .28284272 under the same task norm and command bound.
The calibrated ceiling design r=.054 stopped at 10,240 windows with 27
saturated scalar reports, all retained. It used 10,240 vector reads, 20,480
scalar reports and 29.85984 normalized incident-energy units. Its operator
radius was .17650974 and its uniform ridge-command distance radius was
.14120779. Its audited single-task error .00499834 and uniform task error
.00502771 are separately labeled model information, never controller
inputs. No resets, adjoint calls or zero-input waiting windows were used.

Every window also needs one fresh sign, m dither values, one commanded
waveform, one vector ADC conversion and m overrange flags. A 257-level
report needs nine binary bits plus its flag; these readout operations are
not treated as free. The online sufficient statistics use O(md+d) stored
numbers, with O(m) arithmetic per window. At each declared 512-sample
checkpoint, forming all intervals is O(Kmd); the matrix norm and ridge
factorization cost ordinary numerical linear algebra. A cached ridge
factorization allows later tasks in O(md+d^2) arithmetic. The raw records
are also preserved here; the sufficient-statistic controller does not need
them for continuing operation. Counts are physical-window costs, not
measured seconds: a fixed window duration and actual converter/controller
latencies must be supplied for a complete wall-time or work bill.

An instrument-record replay reconstructs both stopping certificates with
zero numerical difference, without population matrix or state inputs.
A separate finite diagnostic used 256 independent simulated trajectories
covering four fast, oscillatory and very slow rate pairs. Across 16 declared
checkpoints per trajectory there were zero interval misses; all 256 met
the .15 target by 14,336 windows. The proof, not those finite successes,
supports the confidence statement. A further 1,000-matrix-pair check
exercised (11), including a scalar example approaching its sharp constant.
These checks are reproducible in verify_scientific_claims.py and retained
in VERIFICATION.json.

The strongest ordinary alternative is precisely an equally informed
forward system identifier. Before clipping correction, a_raw is its usual
orthogonal-design least-squares/correlation estimate. It can use the same
conditional dither, saturation counters, confidence intervals and ridge
map. It therefore matches all the performance claimed here. Physical
adjoint iterative learning can use different experiment/dimension tradeoffs;
the present method pays a number of forward windows proportional to input
dimension and may be unattractive for very large waveform spaces or a
single task. No speedup or cost dominance over an optimized ordinary
competitor is established.

The recovered P1 execution cannot be treated as a matched benchmark: its
governing programs and fixture are not locally available. The new model is
not a rerun of P1. Its zero-command comparison is valid within this model;
cross-model numerical cost comparisons would not be valid.

## Remaining central obligation

The mathematics provides a finite, record-verifiable operation under the
stated port model. The unresolved physical obligation is to realize and
calibrate that energy-normalized fixed linear port with sign-reliable small
commands, conditionally fresh finite ADC dither and honest overrange flags
over the required lifetime, and to beat the best ordinary architecture
after apparatus, recording and control costs are charged.

If there is unaccounted bath injection J_T, replace E0+Tr^2 in (8), (9)
by E0+Tr^2+J_T. Persistent energy injection can leave a nonzero clipping
floor. If an actuator error kappa is correlated with the commanded sign,
the inferred slope can shift by order ||A|| kappa/r. A systematic ADC mean
error epsilon_ADC can similarly shift it by epsilon_ADC/r. Arbitrarily
small probes are therefore not a free physical precision operation.
State-dependent incremental gain, nonlinear command response, unknown port
gain and arbitrary sensor memory violate premises rather than becoming
automatically covered by the old-field budget.

## Governing sources read

* The supplied FACTS.txt and both recovered P1 visible-text files in
  ../../cases/physical/. The separately linked P1 proof/program attachments
  were unavailable and were not read or imported.
* L. Aarnoudse and T. Oomen, "Model-Free Learning for Massive MIMO Systems:
  Stochastic Approximation Adjoint Iterative Learning Control," IEEE Control
  Systems Letters 5(6), 1946--1951 (2021), DOI 10.1109/LCSYS.2020.3046169.
  The retrieved publisher PDF supplies the direct comparison: physical
  adjoint experiments, SISO time reversal, randomized MIMO adjoint gradients
  and stochastic approximation precede this work.
  https://pure.tue.nl/ws/files/193833656/Model_Free_Learning_for_Massive_MIMO_Systems_Stochastic_Approximation_Adjoint_Iterative_Learning_Control.pdf

External priority was not established. These sources motivate the scope;
the new proof above does not invoke an unavailable source theorem.
