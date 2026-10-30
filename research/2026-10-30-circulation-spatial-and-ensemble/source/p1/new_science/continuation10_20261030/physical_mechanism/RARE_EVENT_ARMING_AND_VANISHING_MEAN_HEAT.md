# Rare-event arming: an ordinary governor can change a rare-current law with vanishing mean carrier heat

30 October 2026. Stronger constructive comparator following `DELAYED_CURRENT_GOVERNOR_AND_WORK.md`. The added-carrier, sensing and communication interfaces are unchanged. No new feedback-control principle is claimed. This result concerns expected **carrier affinity heat**, not total apparatus energy, and does not remove the sustained-mean-current lower bound.

## 1. The stronger opportunity

The always-active weak linear controller already gives mean carrier heat `O(K_N N/R_N)=o(N)`. It is unnecessarily active for the asymptotic objective: an equilibrium native current ordinarily fluctuates on scale `N^(3/2)` over time `N^2`, while the protected macroscopic displacement has scale `N^2`.

Leave the auxiliary drive exactly off until an intermediate threshold is reached, then permanently enable the delayed clipped linear controller. With

\[
b_N=N^{3/2}\log(2+N),\qquad
1\ll K_N\ll R_N\ll N,
\tag{1}
\]

this ordinary event-triggered policy satisfies, for every fixed `epsilon,T>0`,

\[
\lim_{N\to\infty}\frac1N\log\Pr\{\sup_{t\le N^2T}|X(t)|>
\epsilon N^2\}=-\infty,
\tag{2}
\]

while

\[
\mathbb E W_{\rm aux}
\le C_T\frac{N^2K_N^2}{R_N}
\exp[-c_T\log^2(2+N)]
=o(N^{-p})\quad\hbox{for every fixed }p>0.
\tag{3}
\]

Here `X=J_native+J_aux`, and **all actual carrier displacements are included**. The native process is untouched. Sensing, counter storage, communication and clocks run during the unarmed period and retain their real costs. Equation (3) therefore establishes no vanishing-total-energy apparatus.

This is stronger than merely correcting the mistaken assertion that equilibrium control must pay the loaded `Omega(N^2/R_N)` bill. With the present macroscopic objective and these ports, there is no positive asymptotic lower bound on *mean equilibrium carrier-drive heat* alone. Rare-record control and mean deployed heat are intrinsically different resource questions.

## 2. Supplied process and actual rule

Use the exact physical supplier and assumptions in the companion note:

* An untouched native stationary reversible full-state jump process, total activity at most `C N`, antisymmetric counted increments bounded by one. Frozen hidden classes and evolving microscopic memory are permitted. The actual stationary initial law is warranted conditional on any retained old record for which a conditional claim is made.
* `R_N` real independent auxiliary carriers, each with calibrated rates `c exp(plus or minus f/2)` and an actual zero-affinity setting. Separate tracks cost `O(NR_N)` cells; generic interacting exclusion carriers do not silently supply this interface.
* Local counts and a complete delayed aggregation/broadcast epoch `Delta_N=C N` or `C N log(2+N)`. In the latter case require `K_N log N/N ->0`. All apparatus and signal-error assumptions in the companion note remain in force.

Set `g_N=K_N/N^2`, and `X_m=X(m Delta_N)`. Let

\[
\sigma=\inf\{m\ge1:|X_m|\ge b_N\}.
\tag{4}
\]

The first threshold-crossing measurement has timestamp `sigma Delta_N`. Its command may begin only at the start of epoch `sigma+1`, after the full communication delay. Until then `f=0`. From epoch `sigma+1` onward the drive is permanently armed and obeys

\[
u_m=-\operatorname{clip}(g_N X_{m-1},-K_N,K_N),\qquad
f_m=2\operatorname{arsinh}\frac{u_m}{2cR_N}.
\tag{5}
\]

There is no repeated microscopic reset, no exposure of a future native trajectory to the controller, and no requirement that the native state be equilibrium after the trigger. The latter point is load-bearing: the stopping event certainly changes the native conditional state. The proof handles it without substituting an unwarranted conditional equilibrium law.

## 3. Arming is rare under the actual equilibrium deployment

Before arming, the actual process agrees with the supplied zero-drive reference, by coupling its independent primitive clocks. Its first-threshold event consequently has exactly the corresponding zero-drive first-threshold probability.

On the entire interval `T_N=N^2T`, the forward/backward martingale decomposition for a reversible antisymmetric native current gives

\[
\Pr\{\sup_{t\le T_N}|J_{\rm native}(t)|>a\}
\le C\exp\left[-c\frac{a^2}{N T_N+a}\right].
\tag{6}
\]

The zero-affinity auxiliary current is a martingale with activity `2cR_N`; the same inequality holds with `N` replaced by `R_N`. Apply the union bound with `a=b_N/2`. Then

\[
\Pr\{\sigma\Delta_N\le T_N\}
\le C_T e^{-c_T\log^2(2+N)}.
\tag{7}
\]

Only this arming-probability estimate uses the unconditioned equilibrium deployment. An initial density bound of order `exp(CN)` would ruin (7), unlike the superexponential tracking estimate. Thus it does not supply the low mean heat conclusion for arbitrary nonflat or loaded starts.

## 4. Arming overshoot remains below the macroscopic scale

Let `ell_N=1` or `log(2+N)` according to the communication schedule. For any deterministic block of length `Delta_N=O(N ell_N)`, the native-current maximal inequality and the bounded-activity auxiliary martingale give

\[
\Pr\{\hbox{a native or auxiliary martingale block increment exceeds }b_N\}
\le C\exp[-c N\log^2(2+N)/\ell_N].
\tag{8}
\]

At activation the drive is still zero during both blocks relevant to the first detected crossing. Except on the event in (8),

\[
|X_\sigma|\le2b_N,\qquad |X_{\sigma+1}|\le3b_N.
\tag{9}
\]

A union over the `O(N^2/Delta_N)` possible blocks preserves a superexponential bound at speed `N`: `log^2 N/ell_N -> infinity`. The delay therefore introduces an `o(N^2)` initial error, with a superexponentially small exception.

This uses the actual local delay, rather than assuming that the threshold sensor can switch the whole ring instantly.

## 5. Tracking after the random trigger without a conditional-equilibrium substitution

Fix a possible trigger index `k`. From epoch `k+1` onward, before the clipping threshold `N^2`, the controller obeys

\[
X_{m+1}=X_m-h_NX_{m-1}+\zeta_m,
\qquad h_N=g_N\Delta_N.
\tag{10}
\]

The two roots and impulse coefficients are those in the companion note. The homogeneous solution from the two initial values `(X_k,X_(k+1))` has absolute value at most `C(|X_k|+|X_(k+1)|)` for all later epochs. On (9) it is therefore `O(b_N)=o(N^2)`.

The remaining solution at a later deterministic epoch `m` is a deterministic weighted integral of native current increments after `(k+1)Delta_N`, plus the analogously filtered auxiliary martingale. The filter has uniformly bounded amplitude and squared integral `O(1/g_N)`. To handle clipping, stop the auxiliary martingale at the first clipped-region exit and extend only the mathematical linear surrogate. It agrees with the actual process up to the exit.

For this **fixed pair** `(k,m)`, the untouched native stationary path law obeys the tilted-generator estimate, and the auxiliary martingale obeys its conditional exponential bound given the full native path. Hence the noise term `Z_(k,m)` satisfies

\[
\Pr\{|Z_{k,m}|>\epsilon N^2\}
\le2e^{-c\epsilon^2K_NN}.
\tag{11}
\]

We do not claim (11) after conditioning on `sigma=k`. Instead the event

`{sigma=k, initial values satisfy (9), actual later error exceeds epsilon N^2}`

is contained, up to the first exit, in the unconditioned noise event in (11), with a slightly smaller fixed `epsilon` for all large `N`. A union over possible `(k,m)` costs only a polynomial factor. This is why no post-trigger native initializer, hidden-state reset, or false stationarity assumption is needed.

Clipping is handled by the same first-exit inclusion. Between sample times, native and auxiliary martingale block increments at threshold `epsilon N^2` have superexponentially small probability, while the deterministic controlled increment is at most

\[
K_N\Delta_N=o(N^2).
\tag{12}
\]

Before the trigger all samples are below `b_N`, and (8) controls its unobserved overshoot. Combining these facts proves the complete-horizon bound (2).

The same tracking argument continues to work under an initial native density ceiling `exp(CN)` by paying the factor in the unconditioned native-path bounds. The low arming probability and mean heat conclusion do not survive that extension without a separate input estimate.

## 6. Heat proof and its precise meaning

The exact heat compensator is

\[
\mathbb E W_{\rm aux}=\mathbb E\int H_{R_N}(u_t)dt,
\quad H_R(u)=2u\operatorname{arsinh}\frac{u}{2cR}.
\tag{13}
\]

It is identically zero before arming and at most `K_N^2/(cR_N)` per unit time afterward. Consequently,

\[
\mathbb E W_{\rm aux}
\le\frac{N^2T K_N^2}{cR_N}\Pr\{\sigma\Delta_N\le N^2T\}.
\tag{14}
\]

Equation (7) proves (3). This is a bound on the expected stochastic heat through its nonnegative compensator. It does not assert a deterministic bound on every realization of the jump heat, and it does not condition a compensated martingale on the future trigger event.

Because `K_N<R_N<N` eventually, the prefactor in (14) is polynomial. A constant force cap or polynomially costly actuator on armed histories would give the same qualitative mean conclusion. The exact vanishing per-step cap in (5) keeps the earlier local-rate resource contract intact.

The whole-ring cycle affinity remains `N` times the per-step affinity and need not be bounded. A fixed total-loop electromotive-force port is not a supplier. Replacing a delivered drive by a recorded subtraction is also not a supplier.

## 7. Two useful boundaries

**Martingale-native extension.** If the aggregate native current is a bounded-jump martingale with activity `O(N)` for every state, the same proof holds for arbitrary native initial laws: use its forward martingale bound directly in (6) and in the deterministic filtered-current estimate. Homogeneous symmetric exclusion on a periodic ring supplies this property, since its instantaneous total signed drift is `c sum_i(eta_i-eta_(i+1))=0`. Thus the vanishing-mean-drive conclusion can coexist with useful nonflat density relaxation in that actual model. This is a direct algebraic corollary; it does not assign the property to unknown heterogeneous native clocks.

**Sustained mean transport.** For the same auxiliary rates, every causal controller still satisfies

\[
\mathbb E W_{\rm aux}\ge t H_{R_N}(\mathbb E J_{\rm aux}(t)/t).
\tag{15}
\]

If a mean counter-current of order one must persist over `t=N^2T`, this is `Omega(N^2/R_N)`. Arming then typically occurs and (7) is not applicable. It is incorrect to transfer the vanishing equilibrium average to that different load, or to a guarantee of small work on every rare record.

## 8. Consequence for the research comparison

Brandes's accumulated-error governor, its sampled experimental implementations, and ordinary event-triggered control already motivate this policy; the cited primary predecessor discussion is in the companion note. The new calculation does not turn the governor into a new basic principle.

What it establishes for this task is sharper: a physical extra-carrier feedback port can reshape a speed-`N` current law while dissipating negligible **mean carrier drive heat** on the equilibrium or martingale-native deployment. It does so by being inactive on nearly all ordinary histories and acting on a narrowing but still microscopic error window before a finite macroscopic excursion develops. The meaningful resource comparison must retain the continuously running detector/network and the work distribution on the controlled rare histories, rather than using mean carrier heat alone as an impossibility argument or a complete efficiency certificate.

## 9. Receiving audit: synchronous snapshots and finite communication

The main proof uses `X_m` at a common physical timestamp. Merely collecting the latest value of each local counter in sequence does **not** supply that variable. A slow sweep can mix counter times over `O(N)` and the crude absolute error is then `O(N^2)`, already the protected scale. No telescoping identity erases that error.

An explicit sufficient implementation is as follows. Each local sensor keeps a cumulative signed counter for its assigned physical jumps, and latches a named epoch value into a buffer. Buffers are collected and summed afterward, then the command is broadcast for a scheduled future activation. Collection may be asynchronous; the latched timestamps, rather than the message-arrival times, determine the measured current. Clock synchronization and its error budget are actual apparatus resources. Initial and continuing synchronization do not follow merely from the existence of a communication network.

The proof tolerates a concrete finite-clock contract. Suppose every latch is within `delta_N<=C log(2+N)` of its named epoch, and local command activation is within the same error of its scheduled epoch. Keep `Delta_N=O(N)` or `O(N log N)` large enough for collection and advance broadcast. The timestamp error in the sum of all signed counters is bounded in absolute value by the total number of physical jumps in the common window of length `2 delta_N`. Since native plus auxiliary activity is `O(N)`, this count is Poisson-dominated with mean `O(N log N)`, even under feedback. Taking

\[
\eta_N=N\log^3(2+N)=o(b_N)
\tag{16}
\]

and union-bounding all read epochs gives a snapshot-error probability smaller than `exp[-c N log^2 N]` for all large `N`. A separate deterministic counter quantization error `o(b_N)` is also allowed. Thus false early arming due to these timing errors remains much rarer than the bound (7).

Before clipping, a read error at most `eta_N` perturbs the linear recursion by at most `h_N eta_N`. The impulse sum `sum_j G_j=1/h_N` bounds its accumulated counter effect by `eta_N`. Scheduled activation skew changes the actual drift only during boundary windows. With bounded local commanded rates, their integrated disturbance per epoch is at most `C K_N delta_N`, producing total response at most

\[
C\eta_N+C\frac{K_N\delta_N}{h_N}
=C\eta_N+C\frac{\delta_N N^2}{\Delta_N}
=o(N^2).
\tag{17}
\]

For the stated skew and epoch schedules it is even `o(b_N)`. Hence the first-exit and random-trigger arguments remain valid with slightly enlarged small thresholds. The actual local clocks may be imperfect; their common-time approximation must satisfy this paid contract. Arbitrary staggered readout or arrival-triggered activation with spread comparable to a full epoch is not covered by (17).

If each carrier's uniform scalar drive simply switches at its own slightly staggered time, the quadratic heat identity remains valid carrier by carrier. If a force is implemented by separately timed spatial field cells, there can instead be short spatially nonuniform force intervals. The always-active quadratic work estimate must not be transferred to those intervals without a further calculation. The rare-arming conclusion is more robust: with per-step force bounded by `a_N=O(K_N/R_N)` and auxiliary activity `O(R_N)`,

\[
\mathbb E\left[\sum_{\text{auxiliary jumps}}|f_e(t)\Delta J_e|\right]
\le C N^2 K_N\,\Pr\{\hbox{arming or a false-arm error}\}
\longrightarrow0.
\tag{18}
\]

This uses the absolute physical hop work and its predictable compensator, so it does not require cancellations of a force-switching correlation. The prefactor is still polynomial and the arming probability has the bound (7), plus the smaller timing-error probability. Field switching, sensing and network energy remain outside (18).

This timing-robustness extension is for the bounded-rate extra-carrier supplier. It is **not** an error theorem for the interacting finite-cell mechanical supplier: nonsynchronous gyroscopic stages can destroy its exact center-of-mass cancellation, and its actual pulse-map error must be supplied separately. The work note for that supplier uses its declared exact common schedule.
