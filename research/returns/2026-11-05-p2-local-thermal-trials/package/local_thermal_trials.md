---
title: "Local causal trials without global equilibration"
subtitle: "A finite thermal preparation and measurement construction"
author: "Research construction and independent companion results"
date: "5 November 2026"
fontsize: 10pt
geometry: margin=0.8in
colorlinks: true
toc: true
toc-depth: 2
---

# Completed result and its meaning

The strongest completed construction is a **local causal-trial operation on a
retained nonlinear thermal apparatus**. A fresh local Langevin thermostat,
finite excess relative entropy and a private physical clock can supply a known
random momentum ensemble approximately independent of the contemporaneous
hidden environment and old classical reference. A finite pointer instrument
implements the required measurement with explicitly related imprecision,
backaction, initialization, timing, range and control costs.

The operation does not identify the hidden dynamics, acquire a response table,
restore the hidden equilibrium ensemble, or supply an arbitrary momentum
overwrite. It makes a specified local randomized experiment scientifically
interpretable despite unknown hidden dynamics. The hidden distribution shared
by the trial arms is whatever the passive waiting and measurement window
produces. An ordinary bounded weighted score is preferable when the subsequent
experiment does not use an arm label.

The completed theorem is conditional science within the stated classical
Hamiltonian/Langevin and instrument contracts. Its mathematical mechanism uses
established conditional entropy and Gaussian logarithmic Sobolev machinery.
Historical priority, a laboratory demonstration and civilisation-scale impact
are not established. The consequence earned here is the complete
reference-sensitive physical instrument and its separation from global mixing.

# 1. Physical and information resources

Write the full physical state as $S=(p,z)$, where $z$ contains the coordinate
$x$ conjugate to $p$ and every hidden degree of freedom. Assume a well-posed
Hamiltonian baseline with

\[
H(p,z)=\frac{p^2}{2M}+V(z),\qquad
\pi(dp,dz)=G_\sigma(dp)\pi_z(dz),\qquad \sigma^2=M/\beta.
\]

Here $G_\sigma$ is the centered Gaussian of variance $\sigma^2$ and $\pi$ is a
normalizable invariant probability law. The conservative dynamics preserves
phase volume and $H$. An actual local thermostat acts as

\[
dx=\frac pMdt,\qquad
dp=F(S)dt-\gamma pdt+\sqrt{2\gamma\sigma^2}\,dW_t,
\quad \gamma>0.
\]

Additional invariant dissipative channels are allowed if they cannot increase
relative entropy. Hidden nonlinear interactions and an unknown finite hidden
dimension are allowed. An infinite-dimensional extension requires the same
well-defined invariant measure and entropy identities; it is not granted merely
by writing infinitely many coordinates. Momentum-dependent interactions that
destroy the displayed factorization are outside this statement.

Let $R$ be all pre-existing retained classical information. Supply the bound

\[
D(\rho_{SR}\Vert\pi\otimes\rho_R)\le D_0<\infty. \tag{1}
\]

This includes both physical nonequilibrium free energy and shared information:

\[
D(\rho_{SR}\Vert\pi\rho_R)
=D(\rho_S\Vert\pi)+I(S:R).
\]

It is not a total-energy bound. Continuous equilibrium thermal input is allowed.
$D_0$ can be extensive, so absence of a separate dimension factor is not a
claim that a highly excited large apparatus is cheap. A quiet local trace does
not certify (1). A preparation protocol, supplied ensemble contract or other
valid thermodynamic bound must supply it. An exact reference copy of continuous
microscopic data can make it infinite. Future thermostat noise is fresh and
unobserved, independent of the initial source and reference.

The deployment observer has local measurement and receiver controls, a private
timer and initialized receiver memory. A momentum-reset actuator, hidden-state
access and a response model are not supplied. Known temperature, friction,
mass, meter gains, force/moment bounds and a finite validity range are substantive
calibration resources. The operation does not infer them without exposure.

# 2. The local replacement theorem

Define the mathematical replacement $C$ to retain the joint $(z,R)$ marginal
and draw $p$ independently from $G_\sigma$. Put

\[
J(t)=D(\rho_{SR,t}\Vert C\rho_{SR,t}).
\]

**Theorem.** Under the preceding contracts,

\[
\int_0^\infty J(t)\,dt\le\frac{D_0}{2\gamma}. \tag{2}
\]

If $T$ is an independent private trigger with density $g(t)\le C_g$, then,
with $\operatorname{TV}=\tfrac12\|P-Q\|_1$,

\[
\operatorname{TV}\!\left(
\mathcal L(T,S_T,R),\;G_\sigma\otimes\mathcal L(T,z_T,R)
\right)
\le \sqrt{\frac{C_gD_0}{4\gamma}}. \tag{3}
\]

This includes the actual time and the full hidden/reference state. It is an
average guarantee over private timing and old history, not a guarantee
conditioned on every exceptional clock value or posterior.

**Proof.** Let $h_t=d\rho_{SR,t}/d(\pi\rho_R)$ and
$I_p(t)=\mathbb E|\partial_p\log h_t|^2$. Integration by parts gives
$-D'(t)\ge\gamma\sigma^2 I_p(t)$: the conservative generator contributes zero
and the thermostat contributes its Dirichlet form. Conditional on each
$(z,R)$, Gaussian logarithmic Sobolev gives
$J(t)\le\sigma^2 I_p(t)/2$. Integration proves (2). Applying the entropy chain
rule to the time-labeled laws gives relative entropy at most
$C_gD_0/(2\gamma)$; Pinsker's inequality proves (3). Finite-entropy initial
laws use the integrated entropy identity and its standard approximation form.
No spatial logarithmic Sobolev constant or global mixing estimate is used.

A useful deduction is the exact decomposition

\[
J(t)=D(\rho_{p,t}\Vert G_\sigma)+I(p_t:z_t,R). \tag{4}
\]

Local dissipation therefore budgets both local nonthermal shape and hidden
confounding. A system can fail to approach its full equilibrium while still
supplying the local resource in (3).

# 3. Finite private timing

Use an isolated Poisson arrival clock of calibrated rate $r$. Accept the first
arrival before a finite deadline $H$; otherwise report timeout. Conditional on
arrival, its density is bounded by

\[
C_g=\frac r{1-e^{-rH}},\qquad
\Pr(\mathrm{timeout})=e^{-rH}=\alpha_c.
\]

For thermal error allocation $\delta_{\rm th}$, sufficient choices are

\[
r=\frac{4\gamma(1-\alpha_c)\delta_{\rm th}^2}{D_0},\qquad
H=\frac{D_0\log(1/\alpha_c)}
{4\gamma(1-\alpha_c)\delta_{\rm th}^2}. \tag{5}
\]

Expected clock occupancy including timeout is $(1-\alpha_c)/r$. Fixed finite
meter duration and independent latency shift or convolve the clock density
without increasing its cap. Fine event time need not be digitized. A bounded
clock-law discrepancy adds its own TV allowance. The $D_0=0$ case is already
locally ready and does not require division by zero in (5).

A finite-intensity coherent optical pulse with photon counting is one
candidate clock architecture under its actual Poisson/detector contract.
Detection efficiency $\eta_d$ requires photon flux $r/\eta_d$ and nominal
optical energy $\hbar\omega rH/\eta_d$. Laser, detector, watchdog and controller
standby power over $H$ are additional. Dark counts, afterpulsing, latency,
thermal coupling and any information leak into the specimen require calibration.
This is an explicit timing resource, not a claim that every photon detector
automatically meets it.

An arbitrary finite point grid does not follow from (2), because an integrable
quantity may concentrate at the grid times. A digital clock needs an additional
time-regularity proof or actual independent continuous dither. At timeout the
protocol aborts; it does not launch at that atom and reuse (3).

# 4. From local readiness to a causal trial

Choose a known odd Lipschitz score $s:\mathbb R\to[-1,1]$, and assign

\[
\Pr(A=a\mid p)=\frac{1+a s(p)}2,\qquad
q_a(dp)=G_\sigma(dp)[1+a s(p)],\quad a\in\{-1,+1\}.
\]

Under exact replacement, $A$ is fair and independent of $(z,R,T)$, while
$p\mid A=a$ has law $q_a$ independently of those variables. Thus the marked
joint law is exactly the law of first choosing a fair arm and then preparing
its known momentum distribution while preserving the passive hidden marginal.
All runs are used. Marking and every common subsequent experiment are
stochastic channels, so (3) transfers to their complete joint law without a
future-horizon multiplier.

The sinusoidal choice $s(p)=\sin(p/\sigma)$ gives

\[
\mathbb E_{q_\pm}p=\pm\sigma e^{-1/2},\qquad
\mathbb E_{q_\pm}p^2=\sigma^2.
\]

For the same Lipschitz constant, clipped-linear
$s(p)=\operatorname{clip}(p/\sigma,-1,1)$ gives the larger mean
$\pm\sigma[2\Phi(1)-1]\approx\pm0.682689\sigma$, with the same kinetic second
moment. It is implementable by finite arithmetic and comparisons. This is a
useful ordinary improvement, not the central consequence.

The output is a randomized arm, not deterministic control of momentum. For an
externally requested arm, accept with the corresponding probability; ideal
success is $1/2$, and conditioning increases an unconditional TV error
$\epsilon$ to at most $2\epsilon$. Failures consume their actual time and
resources. For general rare accepted targets the acceptance probability must
be paid. Since $q_a/G_\sigma\le2$, labeling itself cannot accelerate the
production of a rare outcome.

Fine current preparation readings are excluded from the prepared output.
They are correlated with $p$ and cannot simultaneously be treated as an
independent old reference. Keep the arm, old reference, declared clock record
and future reports. Temporary readings must be genuinely erased or isolated.
They cannot control later timing through a hidden data-dependent latency.

# 5. The finite meter and its physical backaction

Take two identical weighted position windows of duration $b$, separated by
$\ell$, and set $t_*=\ell+b$. The estimator is
$\widehat p=M(Y_1-Y_0)/\ell$. The exact noiseless expression is a positive
normalized average of momentum over the window. Use the momentum at its END
as the logical intervention variable. The trigger for that endpoint remains
bounded-density by the fixed time shift.

Supply local moments $\mathbb E p^2\le P_*^2$ and
$\mathbb E|F-\gamma p|^2\le B_*^2$. For an unbounded coordinate, supply
$\mathbb E x^2\le X_*^2$ or an appropriate range contract. For example,
Gaussian kinetic structure and (1) imply

\[
P_*^2=4\sigma^2[D_0+(\log2)/2].
\]

A bounded local conservative force gives $B_*\le F_*+\gamma P_*$. A local
equilibrium exponential force moment gives another entropy-variational bound.
These are metrology premises; factorization alone does not bound an arbitrary
force or an unbounded position.

Finite sensor error $e_x$ per position window and white detector density
$\nu_x$ give the sufficient mean error

\[
e_p\le B_*t_*+\sqrt{2\gamma\sigma^2t_*}
+\frac{2Me_x}{\ell}
+M\sqrt{\frac{2\nu_x}{b\ell^2}}. \tag{6}
\]

Sensor clearing, integration, ADC, timing and response lag enter these terms
or a separate overflow allowance. A mark with Lipschitz constant $L_a$ changes
the joint law by at most $L_a e_p$. No independence of meter error and later
trajectory is assumed. A native momentum-box readout can avoid differentiation
where the actual port supplies it, with its own loading/noise contract.

## 5.1 Explicit bounded pointer interaction

For each window initialize a fresh canonical pointer $(Q,P)$ with mass $m_d$
and centered variances $v_Q,v_P$. Use the smooth Hann weight

\[
w(t)=\frac{1-\cos(2\pi t/b)}b,\qquad 0\le t\le b,
\]

and the bounded interaction

\[
H_{\rm int}(t)=-G w(t)\chi_x(x)\chi_P(P). \tag{7}
\]

The smooth saturations equal the identity on declared finite ranges and obey
$|\chi'|\le1$, $|\chi_x|\le X_{\rm cap}$ and $|\chi_P|\le P_{\rm cap}$.
The pointer is free during the window. On the good range event,

\[
Q(b)=Q_0+\frac{bP_0}{m_d}-G\int_0^b w(t)x(t)dt,
\]

so measuring the detached pointer gives a position average with error

\[
e_x\le\frac{\sqrt{v_Q}}G
+\frac{b\sqrt{v_P}}{m_dG}+\frac{e_{\rm read}}G. \tag{8}
\]

Pointer momentum is constant. Its source disturbance is only in the noisy
momentum direction: $u=Gw\chi_x'\chi_P$. For two pointers,

\[
\mathbb E\int u^2dt\le\frac{3G^2v_P}b=:J_u,
\quad
\delta_{\rm back}\le\sqrt{\frac{J_u}{8\gamma\sigma^2}}. \tag{9}
\]

The latter is a full-path Girsanov/Pinsker comparison, including hidden state
and old reference, under the stated absolute-continuity conditions. Saturated
pointer momentum also gives a pathwise action bound. A small displacement
perturbation alone would not supply this arbitrary-hidden-state TV guarantee.

All controls in (7) are finite:

\[
|H_{\rm int}|_{\max}\le\frac{2GX_{\rm cap}P_{\rm cap}}b,
\quad |u|_{\max}\le\frac{2GP_{\rm cap}}b,
\quad |\dot g|_{\max}\le\frac{2\pi G}{b^2}.
\]

Hann switching work per box is at most
$4GX_{\rm cap}P_{\rm cap}/b$, in addition to driver and reset costs. On the
passive comparison path, source-range failure is at most
$[2X_*^2+2t_*^2P_*^2/M^2]/X_0^2$. Gaussian pointer tails and a finite $Q$-ADC
range add their explicit allowances. Compare the saturated-meter path to the
passive path first, then evaluate the same readout functional; this avoids
charging a second backaction comparison just for overflow. A rotor requires
a separately earned angular chart/encoder; (7) is a real-coordinate meter.

## 5.2 Pointer initialization and physical limits

While isolated from the source, a known harmonic pointer with
$k_d=\theta_d/v_Q$, $m_d=v_P/\theta_d$ and a calibrated local bath of thermal
energy $\theta_d$ has the target Gaussian covariance
$\Sigma=\operatorname{diag}(v_Q,v_P)$. For its known drift matrix $A_d$, put
$\rho(t)=\|\Sigma^{-1/2}e^{A_dt}\Sigma^{1/2}\|$. If the initial pointer,
including correlations with any old reference, has normalized second moment
$E_d$, its reset joint TV is at most $\rho(t)\sqrt{E_d+1}/2$ when
$\rho\le1/2$. At critical damping,
$\rho(t)\le2e^{-\omega_dt/2}$, giving the finite reset time

\[
t_{\rm reset}\ge\frac2{\omega_d}\log\frac2{\rho_*},\quad
\rho_* =\min\{1/2,2\delta_d/\sqrt{E_d+1}\}. \tag{10}
\]

This follows from the exact Gaussian transition covariance and entropy
convexity, not a free fresh-pointer assumption. Use actual available damping
if critical damping is unavailable. Trap release follows a finite known
schedule; propagate the covariance through it before using (8)--(9).
Refrigeration, trap preparation, initial energy, reset heat, readout and ramp
work are actual additional costs. The proof supplies bath-contact time, not a
refrigerator operating for free at a thermodynamic lower bound.

Imprecision and backaction are linked by (8)--(9). A quantum pointer must
satisfy $v_Qv_P\ge\hbar^2/4$, and a classical realization needs a comfortably
larger phase-space scale. Fixed hardware therefore has an error floor. The
classical theorem cannot be continued to arbitrarily small error through
quantum or finite-bandwidth limits. The accessible bounded canonical coupling
in (7) is an engineered meter resource; a named off-the-shelf probe is not
assumed to provide it automatically.

# 6. Complete error and resource law

For a finite $L$-bit Bernoulli coin and a finite numerical mark, conditional
on the declared clock-success branch,

\[
\epsilon_{\rm one}\le
\sqrt{\frac{C_gD_0}{4\gamma}}+L_a e_p
+\delta_{\rm back}+\eta_{\rm overflow}+\eta_{\rm clock}
+\eta_{\rm num}+2^{-L}+\eta_{\rm init}+\eta_{\rm cal}. \tag{11}
\]

The last terms are actual initialization and calibrated law-error allowances,
not presumed zero. Timeout is heralded separately. The ideal hidden marginal
is the passive waiting/window marginal evolved from the actual pretrial state;
it is not silently changed to the backacted meter-end marginal.

With $b\asymp\ell$, the Brownian term in (6) suggests
$b=O(\epsilon_m^2/\gamma)$ for a momentum-mark error $\epsilon_m$, subject
also to $B_*b/\sigma=O(\epsilon_m)$. A sufficient position accuracy is
$e_x=O(\sigma b\epsilon_m/M)$. For white position noise a sufficient density is
$\nu_x=O(\sigma^2 b^3\epsilon_m^2/M^2)$, hence the severe
$O(\epsilon_m^8)$ dependence after the Brownian time choice. The pointer
implementation replaces an arbitrary independent noise budget by the actual
tradeoff (8)--(9). These are sufficient scalings, not minimax metrology laws.

Per trial the source remains occupied for at most $H+t_*+$ finite latency,
future experiment duration and any nonoverlapped reset. The clock waiting is
$O(D_0\log(1/\alpha_c)/(\gamma\delta_{\rm th}^2))$. Temporary receiver memory
can be logarithmic in ADC range, target rounding and clock range. Clipped
marking uses $O(B^2)$ elementary bit work at $B$-bit precision with ordinary
arithmetic, plus the actual sensing/clock/output processing. A ticking
watchdog pays every tick; asynchronous timing does not erase standby power.

Receiver memory has its own finite initialization, retention and reset
contracts. For example, thermally activated bits with idle rate bounded by
$\nu_m e^{-E_b/(k_BT_m)}$ can keep $b_m$ bits over a finite duration $H_m$ at
failure $\delta_m$ with
$E_b\ge k_BT_m\max\{0,\log(b_m\nu_mH_m/\delta_m)\}$. A known isolated
two-state reset with energy bias $\Delta$ and relaxation rate $\kappa_m$
uses $\Delta\ge k_BT_m\log(2b_m/\delta_r)$ and
$t_r\ge\kappa_m^{-1}\log(2b_m/\delta_r)$. Raising the unwanted-state energy
costs at most $b_m\Delta$ positive work in that model; switching and driver
costs add. This is a finite-device upper-cost contract, not an assertion that
Landauer's lower bound is attained in finite time.

# 7. Evaluation and reuse

If the future channel ignores the arm, the causal contrast for a bounded
outcome is exactly

\[
\tau=\mathbb E_{q_+}Y-\mathbb E_{q_-}Y
=2\mathbb E[s(p)Y]. \tag{12}
\]

This ordinary weighted estimator removes the coin and has variance no larger
than $2AY$; the difference is $4\mathbb E[(1-s^2)Y^2]$. A finite private
weight cache must be withheld from the common future controller. After outcome
measurement, retain a quantized score and erase or isolate the cache. The
companion proves an explicit bias budget with $O(\log(1/\epsilon))$ weight and
score bits. If the arm selects a later physical action, use the actual arm
instrument instead.

For reuse, let $R_j$ be all actually retained records. Appending a $b$-bit report
adds $I(S:Y\mid R_j)\le b\log2$ to the joint entropy budget. Momentum-force
action contributes a conservative
$\mathbb E\int u^2dt/(2\gamma\sigma^2)$; Girsanov improves the coefficient to
$1/4$ at a fixed or source-independent endpoint. A state-dependent stopping
time does not inherit the stationary-endpoint argument. Pad to a fixed deadline
or use a separate proved bound. Work is not substituted for force-squared
action for arbitrary feedback.

An actual-history Markov-kernel hybrid gives total campaign TV at most
$\sum_j\epsilon_j$. It applies entropy only on actual histories, not an
unproved ideal-history budget. With $n$ rounds, total path error $\epsilon$,
and budgets $D_j$, comparable per-round errors give a waiting bill of order
$n^2\sum_jD_j\log(n/\alpha)/(\gamma\epsilon^2)$, which can be very large.

For a scalar causal estimate rather than a complete path-law comparison, set
$X_j=2A_jY_j\in[-2,2]$. Let $\tau_j$ be the ideal contrast for the current
actual pretrial history and its passive-window hidden law. If the one-round
TV errors have average bounds $\epsilon_j$, Markov plus a bounded martingale
inequality gives, with probability at least $1-\alpha-\eta$,

\[
\left|\frac1n\sum_jX_j-\frac1n\sum_j\tau_j\right|
\le\sqrt{\frac{8\log(2/\alpha)}n}
+\frac4\eta\frac1n\sum_j\epsilon_j. \tag{13}
\]

This is a current-environment causal contrast, not an iid or stationary
population estimate. Average joint entropy is not a uniform bound on each rare
history. Retained finite reports, imperfect reset residues, actuation and
future outcome exposure all remain paid.

# 8. A concrete separation from global mixing

Consider two coupled rotors with

\[
U(q,y)=B\sin^2y+g[1-\cos(q-y)],
\]

momenta $p,r$, masses $M,m$, and a thermostat only on $p$. The local force has
magnitude at most $g$, independently of $B$. Let the initial source be Gibbs
conditioned on the left hidden well, and shift $p$ by $a\sigma R$ with a fair
retained sign $R$. Then

\[
D_0=\log2+a^2/2,\qquad
\left\|\frac{d\rho_0}{d(\pi\rho_R)}\right\|_2^2=2e^{a^2}.
\]

Writing $b=\beta B$ and
$Z_y=2\pi e^{-b/2}I_0(b/2)$, the exact stationary outward crossing flux is

\[
\lambda_B=\frac{2e^{-b}}{Z_y\sqrt{2\pi\beta m}}.
\]

A crossing-count bound and Cauchy--Schwarz change of initial measure imply

\[
\operatorname{TV}(\rho_t,\pi)
\ge\frac12-\sqrt{2e^{a^2}\lambda_Bt}.
\]

Thus global TV is at least $1/4$ through

\[
t_B=\frac{Z_y\sqrt{2\pi\beta m}\,e^{\beta B}}{64e^{a^2}}
=\Theta\!\left(\frac{e^{\beta B}}{\sqrt B}\right). \tag{14}
\]

The local clock bound has no $B$ dependence. At unit $\beta,m,\gamma,a$, the
clean uniform-clock one-percent local bound is $2982.87$, while $\beta B=30$
gives $t_B=1.00518\times10^{11}$. These are formula evaluations before meter
and timing implementation allowances, not measured laboratory times.

Initialization is a real source resource. The exact conditioned ensemble is
not supplied by waiting cheaply for global equilibrium. A broader narrow-well
density family of width $O(B^{-1/2})$ has constant KL and requires finite-density
loading control, $O(\log B)$ command bits and hidden factory access. Its factory
cost is separate from deployment access. An angular encoder is also required
for rotor readout. Equation (14) proves a separation of operations; it does
not prove an exponential advantage over the best equally informed local method.

# 9. A boundary for continuous nonthermal driving

For ongoing forcing $u$ in the noisy momentum direction,

\[
\frac1T\int_0^T J(t)dt
\le\frac{D_0}{\gamma T}
+\frac{\mathbb E\int_0^T u^2dt}{2\gamma^2\sigma^2T}. \tag{15}
\]

This follows from entropy balance and Young's inequality. A driven free rotor
with constant torque $u$ has stationary momentum
$N(u/\gamma,\sigma^2)$ and exactly
$J=u^2/(2\gamma^2\sigma^2)$. Its distance from the desired Maxwell marginal is
$2\Phi(|u|/(2\gamma\sigma))-1$ at every independent trigger time. A marking-only
all-runs instrument leaves that marginal unchanged. Longer waiting cannot
remove this floor. A real actuator cancelling the drive changes the interface.
Continuous equilibrium heat and persistent nonthermal work are different
resources.

# 10. Independent companions, execution and limits

The decision constructor proved an exact Blackwell ordering for known ordered
LTI binary experiments and an unknown-initial-state annihilator attaining the
$\lambda^{-2/3}$ compliance-decision scale. Numerical annihilation residual was
$2.61\times10^{-10}$ and the forcing identity relative error
$6.60\times10^{-13}$. This is a completed structured decision, without a claim
of advantage over equally informed matched testing.

The preparation-uncertainty constructor proved an exact conservative-completion
Gram kernel and finite-record minimax radius. At the inherited acquired table
precision, its sufficient short-box radius $4.8732$ is worse than the energy
radius $1$; it correctly falls back. The theorem remains valid, but that
numerical point is not a useful new predictor.

Gaussian-integral checks verify the arm means, equal kinetic energies and the
weighted-score variance identity. Sinusoidal and clipped-linear arm information
is respectively $0.26175224$ and $0.33389329$ nats at unit scale. The rotor
programme evaluates the exact flux comparison. These are analytic/floating
checks, not a laboratory execution or proof by simulation. The separate finite receiver illustration now executes 100,000 independently
initialized linear-source trials, including smooth pointer/source dynamics,
32-bit position ADCs, a clipped-linear probability, a 24-bit coin and a finite
future outcome. It produced 99,070 clock successes, 930 timeouts and no ADC
overflows. Its derived conditional joint error allocation is 0.0467644 before
unexecuted hardware discrepancies: 0.03 thermal, 0.01 pointer backaction,
0.00676438 metrology, plus coin and range terms. The maximum physical clock
wait per attempt is 1292.14 and the expected clock occupancy is 277.778 in the
chosen units; meter duration is 0.0002. The source retained strong hidden/reference
correlation (sample normalized score 0.8985), while the arm/hidden score was
0.00274 with Monte Carlo standard error 0.00428. Actual and ideal causal scores
were 0.14125 and 0.14265, with standard errors about 0.00447 each. These checks
do not certify full total variation.

The simulation samples long Gaussian transitions numerically; it does not
physically skip waiting. Serial clock occupancy for its 100,000 attempts would
have expectation 27,777,778 time units, before initialization and outcome work.
Cold pointers, source factory, clock privacy, finite release/reset, calibration,
physical entropy bits and quantum/classical validity were not experimentally
executed. The main nonlinear theorem stands independently of this linear
illustration and does not acquire its premises from those samples.

The earlier complete predictive-preparation archive is preserved byte-for-byte,
including nested earlier results. This thermal theorem does not generalize the
finite-total-energy loaded LTI theorem by deleting its assumptions. The nonlinear
positive-relaxation bridge and the acquired thermal feedback simulator remain
separate operations. The earlier quantum results retain their purifiers,
environment access, memory and half-diamond conventions. No unresolved weak
partial-SWAP receiver is resolved here.

\newpage

# 11. Sources and strongest comparisons

The closest entropy machinery is Vladimirov's conditional momentum decomposition
[1], Desvillettes--Villani's velocity-dissipation analysis [2], and Gaussian
logarithmic Sobolev/hypocoercivity. Recent global kinetic results [3,4] use
additional spatial assumptions. The contribution claimed here is the finite
clock/reference/meter/instrument construction built from that machinery.

Andersen reset [5] is faster if actual independent momentum overwrite exists.
Isoconfigurational simulation [6] has stronger microscopic preparation access.
Ordinary random force trials are already causal but target a different input
law. Weighted change of measure is incorporated whenever it is the stronger
estimator. Measurement-noise constraints [7] and the finite classical thermal
range [8] remain substantive. No rare-event or universal algorithmic speedup is
inferred from these comparisons.

1. I. G. Vladimirov (2023), *Position-momentum conditioning, relative entropy
   decomposition and convergence to equilibrium in stochastic Hamiltonian
   systems*. <https://arxiv.org/abs/2312.09475>.
2. L. Desvillettes and C. Villani (2001), *On the trend to global equilibrium in
   spatially inhomogeneous entropy-dissipating systems: The linear Fokker-Planck
   equation*, CPAM 54, 1--42. DOI: 10.1002/1097-0312(200101)54:1<1::AID-CPA1>3.0.CO;2-Q.
3. J. Lu (2026), *A sharp hypocoercive entropy decay estimate for underdamped
   Langevin dynamics*. <https://arxiv.org/abs/2605.01933>.
4. B. Li and J. Lu (2026), *Space-Time Log-Sobolev Inequality and Hypocoercive
   Hypercontractivity for Underdamped Langevin Dynamics*.
   <https://arxiv.org/abs/2605.25083>.
5. H. C. Andersen (1980), *Molecular dynamics simulations at constant pressure
   and/or temperature*, JCP 72, 2384--2393. <https://doi.org/10.1063/1.439486>.
6. A. Widmer-Cooper, P. Harrowell and H. Fynewever (2004), *How Reproducible Are
   Dynamic Heterogeneities in a Supercooled Liquid?*, PRL 93, 135701.
   <https://doi.org/10.1103/PhysRevLett.93.135701>.
7. A. A. Clerk et al. (2010), *Introduction to quantum noise, measurement, and
   amplification*, RMP 82, 1155. <https://arxiv.org/abs/0810.4729>.
8. H. Nyquist (1928), *Thermal Agitation of Electric Charge in Conductors*,
   Physical Review 32, 110. <https://doi.org/10.1103/PhysRev.32.110>.
9. S. Lee, M. Ramil and I. Seo, *Eyring-Kramers Law for the Underdamped Langevin
   Process*. <https://arxiv.org/abs/2503.12610>. Context for metastability;
   (14) uses its own direct flux proof, not an imported asymptotic rate law.
10. Governing Astra predictive-preparation package, pinned revision 552a3c6:
    [complete public governing source](https://github.com/harjassand/astra-research-knowledge/blob/552a3c6f898e1d20529ed68ccd53b6ebee339a76/research/returns/2026-11-05-p2-predictive-preparation/README.md).
    Full revision identity is retained in the source receipt.
11. Accepted acquired thermal simulator N1688, pinned revision 626bf0f:
    [complete accepted source](https://github.com/harjassand/astra-research-knowledge/blob/626bf0fb5da19c8eb62964f0d7949bb19bc64799/research/2026-11-04-p2-acquired-thermal-feedback-simulator/source/p2/COMPLETE_VISIBLE_RESPONSE.txt).


The reproducible archive contains full subsidiary proofs, execution receipts,
source comparisons, preservation hashes and the unchanged earlier package.
