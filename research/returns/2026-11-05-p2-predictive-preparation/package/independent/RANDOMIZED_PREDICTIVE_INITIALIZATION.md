# Finite-energy randomized predictive initialization

## Status

This is an independent constructive complement to the fixed-deadline conservative
bath obstruction. It does not erase hidden state, equilibrate every mode, or
identify a microscopic state. It makes the free visible continuation nearly
constant over a selected finite window, with a paid probability and waiting cost.
For a linear plant, this supplies an initialization interface for every later
additive-force query through the same zero-state response operator.

The main mathematical step is an elementary energy averaging argument. The
scientific content to evaluate is its fully specified physical use and its
quantifiers, not a claim of discovering Markov's inequality or random-iterate
selection. The user-facing result must be compared with passivity, randomized
iterate methods, experimental linear response, and prepared-bath GLE theory.

## 1. Physical and mathematical premises

An autonomous physical plant has observable scalar coordinate x and velocity v.
It admits a nonnegative storage functional E with known initial upper bound E0.
During a quiet phase, the external force is zero and

    E(t) + integral_0^t v(s)^2 ds <= E0.                         (1)

The normalization is a known local viscous drag equal to one. With drag c>0,
replace E0 by E0/c throughout the motion bounds. Hidden dimension, frequencies,
mixing time, and existence of a bath spectral gap need not be known. Conservative
hidden reservoirs are allowed.

The coordinate is absolutely continuous and v belongs to L2 on finite intervals.
An initial state is fixed before the experiment's private random choice.
The environment does not observe that choice and then reprepare itself.

The device has a finite clock with start-time error at most kappa, a finite-box
position meter, and an additive-force actuator. The undriven trajectory up to
selection is independent of the private choice J. Meter backaction is absent,
or its seed-dependent contribution is bounded separately as described below.
The later force program and numerical predictor each have their own calibrated
execution budgets.

## 2. Exact finite-clock selection

Fix a forecast length L, position averaging duration b>0, energy-motion tolerance
delta>0, timing allowance kappa>=0, and integer N>=1. Put

    D = L+b+2kappa.

Choose J uniformly from {0,...,N-1} before waiting. A power-of-two N needs exactly
log2(N) unbiased private random bits; arbitrary N can use finite rejection with
its separately chosen tail bound.

Leave the plant unforced until the selected measurement and launch time. Program
the nominal launch at

    tau_nom = J D + b + kappa.

The actual launch tau_J differs by at most kappa. Thus the box measurement
[tau_J-b,tau_J] and the entire subsequent horizon [tau_J,tau_J+L] lie in

    I_J = [J D,(J+1)D].

Take the position-box mean m_J and let the reported value mhat_J obey
|mhat_J-m_J|<=eta on a declared metrology event. Start the desired later force
program at tau_J. No trap or instantaneous state reset is used.

For theoretical comparison, let x0 be the continuation that would occur if the
plant remained unforced. Up to tau_J this is exactly the actual trajectory.
For every s in [0,L] and every r in [tau_J-b,tau_J], Cauchy--Schwarz gives

    |x0(tau_J+s)-x0(r)|^2
       <= (L+b) integral_I_J |v0(t)|^2 dt.

Averaging r yields

    sup_0<=s<=L |x0(tau_J+s)-m_J|
       <= sqrt((L+b) integral_I_J |v0|^2).                       (2)

The I_j are disjoint. Equation (1) bounds the sum of their motion energies by E0.
Consequently, for every fixed admissible hidden initial state,

    P_J[sup_s |x0(tau_J+s)-mhat_J| > delta+eta]
       <= E0(L+b)/(N delta^2) + alpha_meter.                    (3)

This remains true if actual timing errors depend on the trajectory, provided the
same programmed error envelope holds: the bound uses the whole enclosing block.
The worst-case launch/forecast completion time is at most N D. The expected
launch time is at most (N-1)D/2+b+2kappa. There is only one selected position box.
The protocol does not need to observe or test the unselected blocks.

Choose

    N >= E0(L+b)/(alpha_init delta^2)

and round upward to a power of two. This is a complete finite stopping operation.

## 3. Prediction for all later additive inputs

Assume additionally that the physical plant is linear and time invariant at its
additive force port. Let R be its zero-state map from the force after launch to
the observed displacement. This response can be known or supplied by a separate
acquisition contract; it is not inferred from passivity alone.

For every force program f supported after launch, superposition gives

    x_f(tau_J+s) = x0(tau_J+s) + (R f)(s).

The predictor

    q_f(s) = mhat_J + (R f)(s)

therefore satisfies, on the one event in (3),

    sup_s |x_f(tau_J+s)-q_f(s)| <= delta+eta                     (4)

SIMULTANEOUSLY for every admissible future force program. The program may be
selected after the measured baseline and acquired response have been inspected.
No union bound over candidate future queries is required.

With an acquired response Rhat and an actual numerical output qtilde_f, add
the separately earned uniform errors of (R-Rhat)f, numerical execution, and
force delivery to the right side of (4). A later controller using future noisy
observations needs its own feedback stability/execution analysis; arbitrary
feedback is not supplied merely by this open-loop superposition statement.

The event concerns the unforced counterfactual continuation from the selected
state. It need not be physically realized. The same initial state supports many
counterfactual simulator queries, but physically executing a drive changes the
state. Reuse requires a new energy bound and a fresh random selection.

The distinction in quantifiers is essential:

    for every fixed admissible initial state,
    with probability at least 1-alpha over private selection/metrology,
    for every later admissible input, the prediction bound holds.

There is no single random seed that works for every adversarial initial state.
An adversary allowed to select the state after seeing the private seed can place
an incoming pulse at the selected launch and defeat this guarantee.

## 4. Meter and clock costs

For a position meter with deterministic mean bias epsilon_x and white noise
density v_x, its b-box mean has variance v_x/b. A sub-Gaussian tail gives

    eta = epsilon_x + sqrt(2 v_x log(2/alpha_meter)/b)
                    + epsilon_quant + epsilon_program.

Finite b trades metrology variance against D and the (L+b) factor in (3).
Parallel meter replication is an additional supplied resource, not assumed.

If the storage dominates mu(x-x_star)^2/2, then |x-x_star|<=sqrt(2E0/mu)
throughout a truly quiet phase. This supplies a finite ADC mean range; add the
chosen noise tail and quantization allowances and declare an overflow event.
The digitizer does not require infinite range or precision.

The random integer needs O(log N) classical bits. The clock's absolute accuracy,
maximum waiting duration, meter activity and device occupancy are paid resources.
No claim is made that an arbitrarily long unforced hold is experimentally cheap.

## 5. Nonzero quiet-phase forces and reuse

If the actual quiet phase has a residual force e(t) whose undriven continuation
is independent of the private choice J, passivity gives

    Edot <= e v-v^2 <= -v^2/2+e^2/2,
    integral_0^ND v^2 <= 2E0 + integral_0^ND e^2.                (5)

Replace E0 in (3) by this motion-energy budget. If |e|<=xi, the resulting bound is

    2E0(L+b)/(N delta^2) + xi^2 D(L+b)/delta^2.

The second term is an accuracy/confidence floor. Additional waiting alone does
not remove it. A more informative calibrated residual-force model may yield a
better bound, but it must be supplied.

After an actual experiment with force f and a known starting storage bound Epre,

    Epost <= Epre + (1/4) integral f^2,

because f v-v^2 <= f^2/4 pointwise. Measured work can improve this conservative
bound if its own finite metrology is certified. Fresh randomized initialization
then uses Epost. An arbitrary number of reuses does not have a fixed free cost.

If measurement or clock operation contributes a force specifically at the
selected window, its trajectory can depend on J. It cannot be hidden in the
averaging argument: each possible J would then select a different disturbance
trajectory. For the linear plant, a selected-window extra force e_J supported
over duration b+L and bounded by xi_J has a zero-state displacement at most
||e_J||_2/sqrt(2mu)<=xi_J sqrt((b+L)/(2mu)), when storage dominates mu x^2/2.
Its effect on both the baseline and forecast can be charged by twice this bound,
or calculated more sharply from the acquired response. This is a separate
error allowance, not divided by N. Thus finite nonzero backaction is permitted
only with its explicit effect included; the meter is not an energy-free oracle.

## 6. Known nonlinear visible force: a finite extension

Consider a scalar convolution plant

    xdot + V'(x) + K*xdot = f+g,

with known V', |K(t)|<=B, and a known local Lipschitz constant L_V on a certified
reachable interval. Let z(s) be its free continuation after launch, and suppose
the randomized event gives |z(s)-mhat|<=delta0 for all s<=T.

Subtract the free and driven trajectories. Their increment y starts at zero and
satisfies

    ydot + V'(z+y)-V'(z) + K*ydot = f.

Simulate yhat from zero with z replaced by mhat. Integrating the two equations
once and using y(0)=yhat(0)=0 gives

    |y-yhat|(t)
      <= integral_0^t (L_V+B)|y-yhat|(s) ds + 2L_V delta0 t.

Hence the actual q=mhat+yhat satisfies

    ||x-q||_infinity
      <= delta0 [1+2L_V T exp((L_V+B)T)].                       (6)

This conservative extension is finite and dimension independent, but can be
exponentially ill conditioned in horizon. The response-only acquisition of a
general nonlinear environment is not supplied by (6). The linear case (4) is
sharper and supports the complete acquired step-response construction.

## 7. Relation to deterministic impossibility and existing approaches

A passive conservative bath can hide an incoming force pulse until after any
fixed preparation deadline while retaining a bounded initial energy. Thus no
deterministic waiting law based only on energy can guarantee a quiet future
window for every initial state. The randomized theorem succeeds by selecting
among many disjoint candidate windows: a finite energy budget limits how many
can contain sufficiently large visible motion.

This is analogous to random-iterate guarantees from a bounded total descent or
dissipation budget. It should not be presented as a new probabilistic inequality.
The full physical consequence is that predictive initialization can be obtained
without hidden equilibration, a hidden-state reconstruction, or an assumption of
well-prepared bath modes, when the future zero-state response is acquired and the
randomized quantifiers are acceptable.

