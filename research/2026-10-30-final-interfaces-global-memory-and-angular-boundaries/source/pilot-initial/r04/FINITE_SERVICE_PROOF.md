# Passive memory, finite sensor range, and a finite service horizon

The consequential question pursued here is whether a controller can guarantee a
useful answer before its service horizon when a passive specimen has unknown
memory and the controller sees a bounded ADC. Two conclusions are established:

1. There are explicit lossless, reciprocal physical instances whose bounded
   records are identical throughout a prescribed horizon, although their task
   optima attain the two opposite extremes of the zero-experiment guarantee.
   Initial stored energy and hidden delay length pay for this obstruction.
2. Under a stated scattering-passivity contract, ordinary fresh-sign regression
   has an explicit finite-confidence deadline with a fixed finite-level ADC.
   Reducing drive amplitude is sufficient; no relaxation model, reset, or
   declaration of a last warning is used. Sparse ordinary probing provides a
   competing resource tradeoff. This is a certificate construction for an
   ordinary method, not an established advantage over ordinary control.

These are mathematical results with executed simulations. No apparatus was
built or qualified. External priority is unestablished.

## 1. Exact interface and assumptions

For the positive theorem, one fixed-duration scalar interrogation has

\[
 y_t=a u_t+h_t,\qquad |a|\leq1.                                      \tag{1}
\]

The unknown scalar incremental gain a is fixed. The old field h_t is determined
before the fresh current sign. It may depend arbitrarily on the entire past,
the unknown internal state, and previous measurements and commands. No state
dimension, stability margin, mixing rate, or decay law is supplied.

Use normalized traveling-wave amplitudes, so the following **pathwise
scattering-passivity** inequality holds at every finite prefix:

\[
 \sum_{t\leq n}y_t^2\leq E_0+\sum_{t\leq n}u_t^2.                    \tag{2}
\]

E_0 is a warranted bound on the initial stored energy, including dark energy.
There is no unaccounted bath or apparatus energy supplied to the specimen.
The normalization and the pathwise inequality are explicit additional scope:
the recovered source's conditional old-energy inequality alone is not silently
being promoted to (2) for an arbitrary mechanical displacement sensor.

The observation is a finite-level ADC Q_t and a saturation flag. With R>0 and
L>=2 levels, let Delta=2R/(L-1). The calibrated measurement contract is

\[
 |Q_t|\leq R,\quad
 \mathbb E[Q_t\mid\mathcal H_t,\sigma_t,u_t,y_t]=C_R(y_t),\quad
 \mathbb E[(Q_t-C_R(y_t))^2\mid\mathcal H_t,\sigma_t,u_t,y_t]
 \leq\Delta^2/4,                                                    \tag{3}
\]

where C_R is clipping to [-R,R]. Fresh stochastic rounding between the two
adjacent ADC levels realizes this mathematical contract. Every clipped sample
is retained. Marginally unbiased rounding is insufficient. Neither full raw y_t
nor h_t nor the current internal energy is supplied to the controller.

The scalar task is

\[
 F_a(u)=\tfrac12(au-b)^2+\tfrac\lambda2u^2,
 \qquad u^*(a)=\frac{ab}{a^2+\lambda}.                               \tag{4}
\]

The unconstrained optimum is feasible whenever the command radius is at least
|b|/(2 sqrt(lambda)). All executed tasks use b=.4, lambda=.5, and command radius
.7. Therefore returning zero gives the deterministic radius .2828427125 over
all a. The simulations do not use true a to construct their certificates.

## 2. First attack and its exact physical failure

A natural attack is synchronous sign modulation: apply fresh signed inputs and
demodulate the outputs. Before clipping, E[sigma*y/eta | history]=a. Clipping
destroys this identity. This is not merely a loose concentration bound.

Consider a lossless delay line of L packets, coupled to a measured scalar port
by the reciprocal orthogonal scattering matrix

\[
 \begin{pmatrix}y_t\\w_t\end{pmatrix}
 =\begin{pmatrix}a&c\\c&-a\end{pmatrix}
  \begin{pmatrix}u_t\\x_{t,1}\end{pmatrix},
 \quad c=\sqrt{1-a^2},\qquad
 x_{t+1}=(x_{t,2},\ldots,x_{t,L},w_t).                               \tag{5}
\]

It obeys exactly

\[
 y_t^2+\|x_{t+1}\|^2=u_t^2+\|x_t\|^2.                              \tag{6}
\]

This is a passive static coupler plus a propagation delay, not an oracle that
chooses its state after seeing the input. Its zero-state transfer function is
(a+z^{-L})/(1+a z^{-L}), which has unit modulus on the unit circle. The
incremental current-packet response is a. Its scalar adjoint response is also
a; granting that operation does not distinguish the instances below.

Fix a service horizon T, a command bound U, ADC range R, and 0<a_0<1. Choose
L=T, h>R+a_0 U, and prepare **both** instances with x_{1,j}=h/sqrt(1-a_0^2).
The two gains are a=+a_0 and a=-a_0. Their initial energy is the same:

\[
 E_{\rm mask}=T\frac{h^2}{1-a_0^2}.                                \tag{7}
\]

No updated packet reaches the measured head in the first T windows. Thus for
every admissible input sequence, including every adaptive randomized policy,

\[
 y_t^+=h+a_0u_t>R,\qquad y_t^-=h-a_0u_t>R,\qquad t\leq T.           \tag{8}
\]

The ADC value is +R and the warning is true in both worlds at every window.
Conditioned on the same internal controller randomness, all controller records
are identical, including the input energy bill, commands, signs, known
rounding coins, and warning flags. Waiting and zero-input calls also consume
delay packets and count toward T. Reusing signs, using fresh signs, ordinary
active-index updates, forward/adjoint iteration, or a sophisticated estimator
cannot recover information absent from this record.

For bounded pre-ADC dither of magnitude at most D, choose
h>R+D+a_0 U; the same obstruction holds. An unbounded-range threshold,
unsaturated analog channel, or accurate output-energy meter changes the
allowed observation and is not covered by this exact transcript equality.

If 0<lambda<1, choose a_0=sqrt(lambda). The two task optima are

\[
 u^*_\pm=\pm r_0,\qquad r_0=\frac{|b|}{2\sqrt\lambda}.              \tag{9}
\]

Every deterministic command has worst-case error at least r_0. More generally,
suppose an algorithm returns (u_hat,r_hat) with coverage at least 1-delta on
each instance. Since their transcript laws coincide, the probability that its
interval covers both optima is at least 1-2delta. Hence

\[
 \Pr\{r_{\rm hat}<r_0\}\leq2\delta.                                \tag{10}
\]

This is an explicit finite-service minimax obstruction. It does not assert
that a fixed E_0 hides arbitrarily many windows. Taking h down toward its
threshold gives the sufficient masking resource condition

\[
 T< E_0\frac{1-a_0^2}{(R+a_0U)^2}.                                 \tag{11}
\]

Hidden delay dimension L=T and stored energy (7) are paid resources of the
counterexample. It is not a hardness result for known low-order models.

The executed twins use T=L=1024, U=.7, R=1, a_0=sqrt(.5),
h=1.5049747468, and E_mask=4638.61552865. Their complete ADC values and warning
flags coincide under a feedback-dependent excitation policy. Their raw outputs
differ by as much as .98959047. The optima are +/- .2828427125. Maximum observed
numerical energy-balance discrepancy is below 1.7e-11. Equation (8), not that
single numerical policy, proves indistinguishability for every allowed policy.

## 3. Changed mechanism: reduce drive dose, retain bounded observations

Choose a fixed 0<eta<R, apply u_t=eta*sigma_t at every window, and draw each
sigma_t as a fresh independent symmetric sign before reading. Define the
ordinary signed regression estimate

\[
 \widehat a_N=\frac1{N\eta}\sum_{t=1}^N\sigma_tQ_t.                  \tag{12}
\]

The mechanism is simple ordinary identification. The substantive construction
is its finite-horizon confidence set under unknown persistent memory and
saturation. It does not require adjoint access.

**Theorem.** Under (1)-(3), let

\[
 K_N=2E_0+4N\eta^2,\qquad x=\log(2/\delta),
 \qquad\beta_N=\frac{K_N}{N(R-\eta)^2},                              \tag{13}
\]

\[
 \nu_N=
 \frac{\sqrt{2(K_N+N\Delta^2/4)x}}{N\eta}
 +\frac{2(R+\eta)x}{3N\eta}.                                        \tag{14}
\]

With probability at least 1-delta there is a tau in
[max(0,1-beta_N),1] for which

\[
 |\widehat a_N-a\tau|\leq\nu_N.                                    \tag{15}
\]

In particular, |a_hat-a|<=nu_N+beta_N. All constants use only the declared
physical/instrument contracts and experiment budget.

*Proof.* First, a pathwise old-field energy bound follows without observing the
old field. From h_t=y_t-a*u_t, (2), |a|<=1, and (v-w)^2<=2v^2+2w^2,

\[
 H_N:=\sum h_t^2\leq2\sum y_t^2+2\sum u_t^2
 \leq2E_0+4N\eta^2=K_N.                                             \tag{16}
\]

Second, condition on the complete pre-sign state and history. Fresh rounding
and the fresh sign give

\[
 m_t:=\mathbb E[\sigma_tQ_t/\eta\mid\mathcal H_t]
 =\frac{C_R(h_t+a\eta)-C_R(h_t-a\eta)}{2\eta}
 =a\theta_t,\qquad0\leq\theta_t\leq1.                              \tag{17}
\]

Clipping is monotone and 1-Lipschitz; if |h_t|<=R-eta neither possible sign
clips. Therefore

\[
 1-\theta_t\leq\mathbf1\{|h_t|>R-\eta\}
 \leq h_t^2/(R-\eta)^2.                                             \tag{18}
\]

For a=0, m_t=0 and theta_t may be set to 1. Averaging (18) and using (16) gives
the stated tau interval. The counterfactual second sign in (17) is used only
in the proof; no duplicate-state experiment or second simultaneous specimen
is assumed.

Third, set X_t=sigma_t Q_t/eta and D_t=X_t-m_t. Its increment obeys
|D_t|<=R/eta+1. Projection to [-R,R] cannot increase distance from the point
sigma_t a eta, because that point lies inside [-R,R]. Consequently

\[
 \mathbb E[(X_t-a)^2\mid\mathcal H_t]
 \leq(h_t^2+\Delta^2/4)/\eta^2,
\]

and variance is no larger than squared distance from any fixed center. Thus

\[
 V_N:=\sum\mathbb E[D_t^2\mid\mathcal H_t]
 \leq(K_N+N\Delta^2/4)/\eta^2.                                      \tag{19}
\]

The two-sided bounded-martingale Bernstein/Freedman inequality gives, with
probability at least 1-delta,

\[
 |\sum D_t|\leq\sqrt{2V_{\max}x}+\tfrac23(R/\eta+1)x.               \tag{20}
\]

The deliberately conservative 2/3 linear term follows by substituting this
threshold in exp[-s^2/(2(V_max+c*s/3))]. Equations (17)-(20) prove (15).
Neither independent h_t nor mixing is used. QED.

For beta_N<1, the exact interval inversion used in the code is as follows.
Let l=a_hat-nu_N, v=a_hat+nu_N, and tau_0=1-beta_N. The lower endpoint is
l/tau_0 if l<0, otherwise l. The upper endpoint is v/tau_0 if v>0, otherwise v.
Intersect with [-1,1]. An empty numerical interval triggers the safe full
interval [-1,1]. This rule preserves coverage.

Map that gain interval through (4). Its extreme task commands occur at its
endpoints and any included points +/-sqrt(lambda). Return the midpoint of the
resulting command interval, with half its width as the distance radius. This
is the exact minimax command for that scalar uncertainty interval.

## 4. An explicit service deadline and its resource bill

For 0<epsilon_a<=1, set eta=R*sqrt(epsilon_a)/8, provided that amplitude lies
within the warranted probe-command limit. A sufficient deterministic window
budget for |a_hat-a|<=epsilon_a with confidence 1-delta is the ceiling of the
largest of

\[
 \frac{32E_0}{R^2\epsilon_a},\quad
 \frac{128\sqrt{E_0x}}{R\epsilon_a^{3/2}},\quad
 \frac{512x}{\epsilon_a^2},\quad
 \frac{2048(\Delta/R)^2x}{\epsilon_a^3},\quad
 \frac{64x}{\epsilon_a^{3/2}}.                                     \tag{21}
\]

To verify (21), use R-eta>=R/2. The two terms of beta_N are at most epsilon_a/4
each. Split the square root in (14) into its E_0, drive-energy and quantization
terms. The resulting four noise terms are
2sqrt(E_0*x)/(N eta), sqrt(8x/N), Delta*sqrt(x/2)/(eta sqrt(N)), and
R*x/(N eta). Each is at most epsilon_a/8 under (21).

If the allowed probe amplitude U is smaller, choose
eta=min(U,R*sqrt(epsilon_a)/8). Keep the first and third terms in (21), and
replace its second, fourth and fifth terms by, respectively,
16*sqrt(E_0*x)/(eta*epsilon_a),
32*Delta^2*x/(eta^2*epsilon_a^2), and 8*R*x/(eta*epsilon_a).
This keeps the enabling actuator limit explicit.

For the scalar task, |d u*(a)/da|<=|b|/lambda. Clipping a_hat to [-1,1] cannot
increase its error. Choosing epsilon_a=lambda*epsilon_u/|b| therefore gives a
known fixed-budget task guarantee, provided the amplitude and hardware service
time needed for (21) are supplied. This is a finite-confidence deadline, not
a deterministic error guarantee for every random trajectory or a known last
warning time. It is not claimed minimax optimal.

Its cost is N physical windows, N scalar reads, incident specimen energy
N*eta^2, N fresh signs, N fresh rounding choices, and O(N) digital arithmetic.
The ADC has L fixed output levels. If a window takes t_w, readout takes t_r,
and switching/control takes t_c, a serial implementation costs at most
N*(t_w+t_r+t_c), only when those duration bounds are warranted. They are not
measured here. Electronics power, calorimeter work, initial preparation work,
actuator resolution, and instrument calibration are not supplied by the
normalized scattering-energy bill.

An additive actuator amplitude uncertainty e_act and a conditional sensor-mean
error e_sensor can introduce a gain error of order
(e_act+e_sensor)/eta. Thus small eta demands finer calibrated absolute
precision. The executable result assumes exact commands and (3); it does not
qualify real tolerances. More precisely, independent non-anticipating input
errors bounded by e_act and a port gain bound one contribute at most
e_act/eta to the direct demodulation error; extra input energy and memory must
also be charged in (16). No calibration floor is assumed away as a physical
fact.

If a bath contributes known cumulative energy J_N, replace K_N by
2E_0+4N eta^2+2J_N. A linear-in-time J_N can prevent this bound from shrinking.
If E_0 or J_N is unbounded, the saturation construction can defeat every
specified finite horizon. A continuously powered bath is not passive stored
energy supplied for free.

## 5. Multichannel restricted extension

For a fixed contractive A:R^d -> R^m satisfying
y_t=A u_t+h_t and the vector version of (2), make N preassigned coordinate
probes per input direction, M=dN total. Set u_t=eta*sigma_t*e_j on direction j
and form each entry estimate from its corresponding reads. Use independent
conditionally calibrated ADC rounding for each measured coordinate.

The same proof, with

\[
 K=2E_0+4dN\eta^2,\quad x=\log(2md/\delta),
 \quad\beta=K/[N(R-\eta)^2],
\]

and nu given by (14) with that K and x, gives simultaneous entry errors
at most e=beta+nu with probability at least 1-delta. For each entry, its
counterfactual scalar signal is A_lj*eta, bounded by eta, and the sum of its
old-field energies is bounded by the total K. The union bound is over md
entries. This proves the extension without a hidden-state identification.

Project the estimated matrix in Frobenius norm onto the closed convex set of
operators of norm at most one (cap its singular values at one). Projection is
nonexpansive, so the projected matrix A_hat obeys
||A_hat-A||_op <= sqrt(md)*e. On a command ball of radius U, strong convexity
and the two optimization variational inequalities give

\[
 \|u^*(\widehat A)-u^*(A)\|
 \leq\frac{(2U+\|b\|)\sqrt{md}\,e}{\lambda}.                       \tag{22}
\]

This explicit, possibly conservative bound counts dN windows and mdN scalar
reads. The multichannel extension is a proved restricted result; the execution
here is scalar. Neither this bound nor the scalar simulation establishes a
useful high-dimensional or large-scale device.

## 6. Strong ordinary alternatives and an executed sparse comparator

The dense construction **is** ordinary signed system identification. An
ordinary method given the same records can perform exactly (12) and the same
confidence computation. A performance separation from ordinary control cannot
follow from this construction.

A more economical ordinary readout design activates independently with
constant probability p and uses amplitude U_s<R when active. Inactive windows
still advance the same plant, with input zero. Let B_t be the fresh activity,
M=sum B_t its observed count, and
S=sum B_t*sigma_t*Q_t. Normalize by M*U_s, as an active-index learner does.

For a complete finite-confidence sparse certificate, reserve delta/2 for a
binomial count bound. With z=log(2/delta), let

\[
 M_{\max}=\min\{N,\lceil Np+\sqrt{2Np z}+2z/3\rceil\},\qquad
 K=2E_0+4M_{\max}U_s^2.                                             \tag{23}
\]

On the count event, the pathwise old energy is at most K. The drift of
B_t*(sigma_t Q_t-a U_s) has cumulative magnitude at most
p*|a|*U_s*K/(R-U_s)^2. Its conditional variance sum is at most
p*(K+N*Delta^2/4), by the projection argument in (19). Its centered increments
are bounded by R+2U_s. Freedman with x=log(4/delta) gives

\[
 \beta_s=\frac{pK}{M(R-U_s)^2},\qquad
 \nu_s=\frac{\sqrt{2p(K+N\Delta^2/4)x}+2(R+2U_s)x/3}{M U_s}.         \tag{24}
\]

Use the same attenuation interval inversion. Return the full interval if
M=0 or the count exceeds M_max. The total per-task failure allocation is at
most delta. The Freedman bound is used jointly with V<=V_max, so conditioning
on the future count event is not assumed to preserve a martingale.

Setting p*U_s^2=eta^2 matches **expected** incident energy to dense probing.
The actual count and energy remain reported; they are not silently equated.
The leading noise terms have similar scaling. Larger sparse amplitudes worsen
the clipping margin but reduce reads. This is a resource tradeoff rather than
an inherent dense-probe capability advantage. No global optimality is claimed
for U_s=.25 used in the concrete comparator.

The physical-adjoint alternative is established prior art: Aarnoudse and Oomen,
*Model-Free Learning for Massive MIMO Systems: Stochastic Approximation
Adjoint Iterative Learning Control* (IEEE Control Systems Letters 2021),
[publisher PDF at TU/e](https://pure.tue.nl/ws/files/193833656/Model_Free_Learning_for_Massive_MIMO_Systems_Stochastic_Approximation_Adjoint_Iterative_Learning_Control.pdf),
Theorem 1 and Algorithm 1. It constructs an unbiased physical-adjoint gradient
using randomized channel mixing and a dedicated experiment. It is not being
credited to this tranche. The primary
[Simchowitz et al. COLT 2018 proceedings abstract](https://proceedings.mlr.press/v75/simchowitz18a.html)
already establishes nearly minimax ordinary least-squares identification from
a single trajectory without mixing-time analysis. Only that published abstract
was read here; it does not by itself settle priority for the specific clipped,
energy-bounded service result above. Neither “no reset,” “randomized adjoint,”
nor “no mixing” is a new claim here.

## 7. Executed discrimination and its limits

Run `python3 passive_service_experiment.py` from any directory. It writes only
RESULTS.json beside itself. All code, results and this proof are in the
assigned research directory. The implementation uses no inherited unattached
programs, true-gain inputs to certificate construction, producer state, or
other experimental contexts.

For all four main scalar sources, the declared E_0 is 64 including an unchanged
dark energy of 9. The parameters are N=16384, R=1, L=257, delta=.01 **per
task**, lambda=.5, b=.4. A public-constants-only search selected
eta=.05493693737. Dense incident energy is 49.44801117 in normalized units.
Equations (13)-(14) give beta=.02226378285 and nu=.06944338179. The simple
gain error radius is .09170716464; the generic scalar task bound is therefore
.07336573171, already smaller than the zero-experiment .2828427125. The actual
record-dependent interval inversion is sharper:

| Gain (audit only) | Delay windows | Dense certified task radius | Dense true error (audit only) | Dense saturated reads | Sparse certified task radius | Sparse reads |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| .01 | 1 | .05623181 | .01410268 | 1 | .08320987 | 790 |
| .3 | 1 | .03346482 | .00053833 | 2 | .04932163 | 795 |
| -.6 | 127 | .00467086 | .00091586 | 6 | .00896216 | 792 |
| .95 | 32768 | .00466630 | .00038822 | 0 | .00567984 | 816 |

Dense probing reads every one of the 16384 windows. Sparse probing uses the
same number of calendar/physical windows, U_s=.25, p=.04828907341, and the
same expected incident energy 49.44801117. Actual sparse incident energies
are 49.375, 49.6875, 49.5 and 51.0. Both designs use one initial specimen state,
zero resets, a fixed 257-level ADC, and retain all saturated reads. All eight
certificates cover in their executed runs. These are individually 99 percent
mathematical statements under the exact contracts, not a joint 99 percent
coverage statement for eight selected tasks.

The long-delay source still has stored energy 65.87582088 after dense learning;
its dark energy also remains. Thus the execution does not obtain its result by
emptying the specimen. Numerical energy residuals in the primary positive
runs are below 1.5e-11. A separate 128-trial, N=4096, gain .3, delay 7 simulation
had zero observed coverage failures; it is only a finite diagnostic. The
analytic probability guarantee rests on the proof. One hundred thousand
random clipping-secant checks had only about 1e-12 floating-point discrepancy.

The central unresolved physical obligation is to supply (2)-(3), a warranted
E_0, command/readout precision at the selected eta, and a finite complete
apparatus work/time bill in a relevant platform. The central unresolved
information-theoretic obligation is a sharp rate/precision tradeoff: (11) is a
real obstruction and (21) is a sufficient upper bound, but they do not match.
Known dither records, adaptive thresholds, or stronger ordinary set-membership
methods might improve the upper bound and must be included before claiming an
optimal principle or a practical advantage. The failed saturation attack and
the useful restricted finite-service result are both preserved at this scope.
