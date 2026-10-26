# A stronger representation: exact conductance-contrast frontier

This is a mathematical relaxation of an ordinary self-cooling thermal switch, not a source measurement or a claim of a new device. Unlike an independent ideal clock, switching is driven by the reservoir's own temperature. All pre-release leakage is counted in the delivered waveform. A physical actuator's heat capacity, finite switching dynamics, mechanical hysteresis and actual conductance curve must be supplied before applying this model to a device.

## Model

A single source reservoir has constant heat capacity C, temperature rise T0 above a fixed bath, and initial energy E=C*T0. It cools through an autonomous memoryless conductance G(T), with

    0<g_min<=G(T)<=g_max,    K=g_max/g_min>1.

There is no subsequent input or independent clock. The normalized bath-flux distribution is the full released energy, including off-state leakage. Let its mean be m and variance V. Overall timescale rescaling does not change V/m^2.

Writing u=T/T0 and z=-log u, conservation says normalized released energy is -du. Therefore Z=-log U is an Exp(1) variable and the release-time random variable is

    t(Z),  t(z)=integral_0^z a(s)ds,
    a(s)=C/G(T0*exp(-s)).

Rescale time so a is in [1/K,1]. This is an exact representation of the model, not a stochastic material mechanism.

## The exact global optimum

Among every measurable conductance curve in the allowed range, the smallest squared coefficient of variation v=V/m^2 is the unique solution v in (0,1) of

    2[atanh(v)-v] = -log(1-1/K)-1/K.                     (1)

An attaining memoryless curve is a single threshold: G=g_min initially, then G=g_max after the reservoir cools to eta*T0, where

    eta=(1-v)/[(1+v)(1-1/K)].                           (2)

For continuous curves with no bound on slope this is an infimum, approached by steep smooth transitions. A real actuator with bounded transition width/dynamics may do worse. The theorem optimizes the mathematical conductance curve; it does not supply a physical curve that was not measured.

## Derivation for a threshold

Let d=-log eta, a=1 before d, a=1/K afterward, and r=1-1/K. Its survival function has off-state decay until d and on-state decay afterward. Direct integration gives

    m=1-eta+eta/K,
    E[t^2]=2[1-eta(1+d)+eta(d/K+1/K^2)].                (3)

Set y=r*eta. Then m=1-y and E[t^2]=2[1-y(1+1/K+log(r/y))]. Differentiating E[t^2]/m^2 with respect to y shows the unique stationary point satisfies

    1+1/K+log(r/y)=(3-y)/(1+y).                         (4)

The derivative of the left side minus right side is

    -(1-y)^2/[y(1+y)^2]<0.

It tends to positive infinity at y=0 and is negative at y=r, so the root is unique in the physical interval. At this point

    v=(1-y)/(1+y).

Substituting in (4) gives (1),(2). All endpoint cases have CV squared 1, so this is the unique threshold optimum.

## Global certificate over arbitrary admissible curves

Threshold optimality is not inferred from a numerical search. Let t_* be the candidate above, m_*=E[t_*(Z)], and R_*=E[t_*^2]/m_*^2=1+v. For a competitor t_a built from any a in [1/K,1], consider

    F(a)=E[t_*(Z)t_a(Z)]-R_* m_* E[t_a(Z)].

F is linear in a. Its functional coefficient at s is

    exp(-s){ E[t_*(Z)|Z>=s]-R_*m_* }.

The conditional expectation increases strictly with s. At the optimized threshold d, (4) implies

    E[t_*(Z)|Z>=d] = d+1/K = R_*m_*.

Thus the coefficient is negative below d and positive above d. The candidate a_*=1 below d and 1/K above d minimizes F pointwise over the entire admissible box. Since F(a_*)=0, every competitor has F(a)>=0. Cauchy--Schwarz then gives

    R_*m_* E[t_a] <= E[t_*t_a]
                   <= sqrt(E[t_*^2] E[t_a^2]),

and therefore E[t_a^2]/E[t_a]^2>=R_*. This proves the global claim for every measurable admissible conductance curve. No finite collection of numerical examples supplies this quantifier.

## Resource consequence and sensitivity

For large K,

    v ~ (3/4)^(1/3) K^(-2/3),
    CV ~ (3/4)^(1/6) K^(-1/3).

This follows by expanding both sides of (1): the left side is 2v^3/3+O(v^5), the right side is 1/(2K^2)+O(K^-3). Thus target CV=epsilon asymptotically needs K approximately sqrt(3)/(2 epsilon^3), a contrast cost rather than the linear-tree model's exponential capacity cost.

The threshold delay is t_d=(C/g_min) log(1/eta). Sensitivity to a small independent threshold-temperature error is

    |delta t_d|/t_d approximately
      |delta theta|/[theta*log(1/eta)].

Small pre-release leakage (eta close to one) makes this sensitivity severe. This law concerns threshold variation; the waveform's deterministic RMS width is distinct from run-to-run timing jitter.

## Source-supported operation and unsupplied bridge

Cold-closing zero-power switches are established by Dietrich, Euler and Thummes' primary manuscript https://arxiv.org/html/1307.6367v2 (DOI 10.1016/j.cryogenics.2013.11.004). Its near-100 K ON performance and near-220 K closure do not supply a local step G(T); the actuator belongs to a two-temperature assembly. These endpoint regimes are not combined here.

Ralphs et al.'s accepted manuscript record https://digitalcommons.usu.edu/sdl_pubs/298/ reports a tunable zero-power cold-closing switch. The full download was unavailable in this session, so its response curve and timing were not invented.

The actual remaining operation is a calibrated whole reservoir--switch--bath response delivering the required local conductance contrast and transition sharpness, including actuator storage and charging/reset costs. The theorem states the best any ideal curve could do; it is not evidence that a given component reaches it. The ordinary thermal-switch architecture may realize the same operation, so this calculation establishes no physical invention or novelty.

The mean delay is an output in this contrast frontier. Restoring dimensions, the optimum has mean (C/g_min)*(1-eta+eta/K). To specify a desired mean tau, the required ratio is C/g_min=tau/(1-eta+eta/K). This is not a free rescaling if absolute capacitance/conductance budgets are already fixed. No optimality at an independently fixed C, g_min, g_max and tau is claimed.

## Charging cannot be dropped from the operation

For the same ideal cold-closing switch, charging from bath temperature initially occurs through the ON conductance. A constant-power heater must satisfy P>g_max*theta to cross the opening threshold theta; otherwise its ON-state equilibrium is below threshold. With an ideal common opening/closing threshold, its pre-opening charging time is

    t_charge = -(C/g_max) log[1-g_max*theta/P].

This is a model-level lower barrier to loading the assumed initial state with that heater protocol. It does not claim every charging protocol has that peak-power requirement. Real threshold hysteresis and actuator storage would change the loading operation and must be included in a physical implementation. A large contrast does not make preparation/reset resources free.

## Conventional convex finite-curve comparator

For a log-temperature partition with finite intervals [l_i,u_i] and one final infinite interval, let phi_i(z) be the length of [0,z] inside interval i. A piecewise resistance curve has t(z)=sum a_i phi_i(z). Define b_i=E[phi_i(Z)] and M_ij=E[phi_i(Z)phi_j(Z)], Z~Exp(1). For ordered disjoint bins,

    b_i=exp(-l_i)-exp(-u_i),
    M_ij=(u_i-l_i)*b_j for i<j,
    M_ii=2 exp(-l_i)[1-(u_i-l_i+1)exp(-(u_i-l_i))].

For the final infinite bin use b=exp(-l), M_ii=2exp(-l). After normalizing x=a/E[t], the entire contrast-only design is the convex quadratic program

    minimize x^T M x,
    b^T x=1,    lambda<=x_i<=K*lambda,    lambda>=0.

The covariance Gram matrix M is positive semidefinite by construction. This includes arbitrary nonmonotone finite-bin curves, and receives no analytic threshold location. ordinary_curve_qp.py uses a fixed grid followed by refinement around its own detected transitions. The analytic full-function certificate above supplies an independent lower bound for every feasible QP value.
