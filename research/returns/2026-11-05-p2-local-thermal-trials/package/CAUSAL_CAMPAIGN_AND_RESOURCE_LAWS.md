# Causal campaigns and the resource that persistent driving consumes

This subsidiary derivation uses total variation equal to one half of L1.
All references and records here are classical. The earlier quantum
half-diamond conventions remain separate.

## 1. A budget for local distribution error and hidden confounding

For S=(p,z), pi=G_sigma(dp)pi_z(dz), and old reference R, the chain rule gives

    J(t)=D(rho_pzR(t)||G_sigma x rho_zR(t))
        =D(rho_p(t)||G_sigma)+I(p_t:z_t,R).

The unforced local Langevin thermostat therefore implies

    integral_0^infinity [D(rho_p(t)||G_sigma)+I(p_t:z_t,R)]dt
       <=D_0/(2 gamma).

This is not a bound on total thermal heat, total microscopic energy, hidden
dimension, or global equilibration. D_0 itself can be extensive. It includes
reference information. The proof combines the chain rule, conditional Gaussian
log-Sobolev inequality and actual entropy dissipation; those are established
ingredients, not historical-priority claims.

## 2. Causal target of a reused source

Let H_i contain all available history before round i's fresh independent
trigger. Starting from the ACTUAL pretrial joint state, the ideal comparison passively
evolves through the clock and meter window, keeps that passive-window joint
hidden-state and clock marginal, replaces p by a fresh Maxwell draw, and
assigns balanced arms q_a=G_sigma(1+a s), a in {-1,+1}, for an odd bounded
Lipschitz s. Meter delay and the subsequent programme belong to the specified
intervention. The hidden marginal need not be Gibbs and can vary across rounds. It is the
passive comparison marginal, not the actual backacted meter-end marginal.
Changing the target to the latter costs an additional backaction TV term.

For outcome Y_i in [0,1], define

    tau_i(H_i)=E_ideal[Y_i|A_i=+1,H_i]
               -E_ideal[Y_i|A_i=-1,H_i].

The expectations average over the fresh clock and current hidden law. They may
include a specified arm-dependent future programme. This is a conditional
causal contrast, not an iid-specimen or identical-configuration experiment.

Suppose the actual conditional trial law differs from this ideal law by
e_i(H_i) in TV, with E[e_i(H_i)]<=epsilon_i. An average history-inclusive
entropy certificate does not give a uniform bound on every rare history.
Set X_i=2A_iY_i in [-2,2]. Then

    |E_actual[X_i|H_i]-tau_i(H_i)|<=4e_i(H_i).

The martingale differences X_i-E[X_i|H_i] have conditional range at most four.
Conditional Hoeffding and Markov inequalities give, for alpha,eta in (0,1),
with probability at least 1-alpha-eta,

    |tau_hat-tau_bar|
      <=sqrt[8 log(2/alpha)/n]+4 epsilon_bar/eta,             (1)
    tau_hat=n^(-1)sum_i X_i,
    tau_bar=n^(-1)sum_i tau_i(H_i),
    epsilon_bar=n^(-1)sum_i epsilon_i.

Indeed the martingale tail is at most 2exp(-n u^2/8), while
P(n^(-1)sum_i e_i>epsilon_bar/eta)<=eta. If a separate per-history bound
e_i<=epsilon_i is supplied, the 1/eta and eta failure allocation disappear.
Finite outcome quantization adds its explicit error. Full-campaign instrument
TV also obeys sum_i epsilon_i by the actual-history Markov-kernel hybrid.
Allocating per-round error proportional to 1/n can make that stronger target's
waiting bill much larger than the bounded-observable guarantee (1).

## 3. Timeout and selection

The clock has an explicit timeout branch. A campaign may abort on any timeout;
for n attempted rounds its total timeout probability is at most n alpha_c if
each fresh clock has that conditional failure probability. On success the
actual density cap is r/(1-alpha_c), already charged by the single-trial
theorem. A forced launch at a timeout atom is not covered. The source evolves
until the declared abort. An alternative keeps every flag and defines the
target as that flagged experiment. Conditioning a full campaign on successes
can divide its TV bound by the success probability. Formula (1) concerns the
declared successful-trial kernels, with the timeout event accounted for as
an additional failure. It does not license source-dependent postselection.

## 4. Reuse ledger

Appending a finite report Y changes the reference-inclusive entropy by exactly
I(S:Y|R), at most H(Y). A b-bit report costs at most b log 2 nats. A discarded
temporary meter record is absent from the claimed retained interface, but its
physical reset and any backaction remain charged.

A predictable force u in the thermostatted momentum direction has the safe
entropy-balance restart cost

    D_after<=D_before+E integral u^2dt/(2 gamma sigma^2).

For a deterministic or source-independent duration, path Girsanov against an
uncontrolled stationary process can improve the coefficient to 1/4. A finite
pathwise action bound supplies Novikov integrability. State-dependent stopping
does not inherit that endpoint argument: a stopped stationary process need not
have stationary endpoint law. Arbitrary feedback drift is charged by action,
not silently replaced by beta times mechanical work. A separately justified
Hamiltonian-work ledger can be used with its own information charge.

For per-round action J_u and b retained bits, a safe budget is

    D_i<=D_0+(i-1)c,
    c=J_u/(2 gamma sigma^2)+b log 2.

At thermal error epsilon_th and timeout alpha_c choose

    r_i=4 gamma(1-alpha_c)epsilon_th^2/D_i,
    H_i=D_i log(1/alpha_c)/[4 gamma(1-alpha_c)epsilon_th^2].

The worst-case sum of clock occupancies is

    log(1/alpha_c)/[4 gamma(1-alpha_c)epsilon_th^2]
       *[nD_0+c n(n-1)/2].                                 (2)

This conservative quadratic campaign bill is part of the capability, not an
optimality claim. Additional proved entropy decay can improve it. Future
experiment durations, metrology, latency, initialization, actuation, outcome
readout, memory retention and reset add to (2).

## 5. Persistent nonthermal forcing leaves a floor

For ongoing momentum force u, the entropy balance and Young inequality give

    D'<=-(gamma sigma^2/2)I_p+E[u^2]/(2 gamma sigma^2)
       <=-gamma J+E[u^2]/(2 gamma sigma^2).

Thus

    (1/T)integral_0^T J(t)dt
      <=D_0/(gamma T)
        +E integral_0^T u^2dt/(2 gamma^2 sigma^2 T).          (3)

A uniform trigger has joint TV at most the square root of one half of the
right side. Persistent mean-square force leaves a nonvanishing guarantee.
Equilibrium thermal noise is already paired with friction and introduces no
such excess-entropy source term.

The floor is attained by a continuously driven free rotor:

    dp=(u-gamma p)dt+sqrt(2 gamma sigma^2)dW,
    dq=(p/M)dt, with q on a circle.

Its stationary law has q uniform and p~N(u/gamma,sigma^2). Then
J=u^2/(2 gamma^2 sigma^2), attaining the constant term in (3), and

    TV(N(u/gamma,sigma^2),G_sigma)
      =2Phi(|u|/(2 gamma sigma))-1.

Every marking-only all-trials instrument leaves this momentum marginal
unchanged, so its joint error from balanced target arms with Maxwell mixture
is at least this amount. An actual actuator cancelling u changes the interface
and is not ruled out. This distinguishes equilibrium heat from persistent
nonthermal work without claiming a no-go for stronger control access.

## 6. Finite receiver memory and computation

The programme needs a timeout state, two ADC registers (or one native p-box
average), an arithmetic accumulator, a coin/weight register and declared
outputs. At B-bit precision, clipped-linear marking uses fixed-latency integer
arithmetic and comparisons, O(B^2) bit work with schoolbook arithmetic and
O(B) temporary bits. A sinusoid instead needs a proved finite approximation.
Fixed latency prevents a discarded fine record from changing the future start
time through data-dependent computation. After preparation, the future policy
uses only old history, clock and arm unless a larger interface is analysed.
The weighted estimator has a separate private cache which the common future
policy must ignore.

One explicit classical storage model has b_m bits, attempt frequency nu_m and
idle flip rate at most nu_m exp[-E_bar/(k_B T_m)]. A finite retention duration
H_m and total error delta_m are supported by

    E_bar>=k_B T_m max(0,log(b_m nu_m H_m/delta_m)).

This is a declared memory-device model, not a universal barrier law. For reset,
suppose a controllable two-state contact has downward rate >=k_m and upward
rate ratio exp[-E_gap/(k_B T_m)]. From any initial bit, its reset error is at
most exp[-E_gap/(k_B T_m)]+exp[-k_m t_reset]. Therefore

    E_gap=k_B T_m log(2b_m/delta_reset),
    t_reset=k_m^(-1)log(2b_m/delta_reset)

suffice for all bits by a union bound. Raising the unwanted logical state's
energy costs at most E_gap positive work per bit in this two-state model.
Opening/closing the reset contact and barriers have additional actual costs:
charge b_m(E_gap+2E_gate), controller energy and the reset occupancy. This is
a finite upper-cost model; the Landauer lower bound alone would not suffice.
These contacts are on the receiver memory, not hidden source variables.
Reset apparatus is isolated from the specimen; leakage belongs in backaction.

The asynchronous Poisson detector need not perform a digital operation each
source timestep. If the chosen watchdog uses periodic tick h_clk, however,
its H/h_clk updates and standby power are counted. O(B^2) assignment work
does not erase physical clock occupancy, sensor standby energy, outcome work
or memory protection throughout the waiting interval.
