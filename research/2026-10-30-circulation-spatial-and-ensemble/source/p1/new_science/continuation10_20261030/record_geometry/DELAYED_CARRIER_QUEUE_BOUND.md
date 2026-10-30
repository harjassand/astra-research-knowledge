# A causal delayed carrier queue bound

**Status.** Proved scalar tracking lemma for the root composite-conductor path map, followed by two distinct actual suppliers. It does not infer an actuator, detector, or reliable communication channel from equilibrium data.

## 1. Conditional physical interface

Use fixed-length physical sampling periods. Let \(K_N\leq C_TN^2\). A corrected scalar error starts at \(X_0=0\) and satisfies

\[
X_{k+1}-X_k=b_k-c_ku_k+M_{k+1}-M_k,
\quad |b_k|\leq b_0,
\quad0<\nu_N^-\leq c_k\leq\nu_N^+,
\quad|u_k|\leq1.
\tag{1}
\]

Integrated random drifts are permitted when these bounds hold pathwise; the unknown drifts need not be estimated. The command is selected from past observations and held over the period. Use a decision filtration \(\mathcal F_k\) containing all previous innovations and all information used to select the command, but not an unread fresh source coordinate for period \(k\). The actual conditional experiment warrants, uniformly in allowed hidden parameters and controls,

\[
E[e^{\theta(M_{k+1}-M_k)}\mid\mathcal F_k]
\leq e^{CN\theta^2},\qquad |\theta|\leq1.
\tag{2}
\]

This is a conditional martingale-noise interface, not a conclusion from a marginal equilibrium distribution. Bounded-jump processes with conditional intensity \(O(N)\), and the finite-duration Gaussian supplier below, satisfy it. For the latter, revealing the newly prepared Gaussian coordinate before selecting the force would invalidate the interface; a mathematical filtration containing that already generated coordinate at time \(k\) would likewise not make its contribution a new martingale increment.

The true measured error is \(E_k\). It can differ from \(X_k\) by an analytically bounded endpoint correction. A command used at step \(k\) is based on a sample index in \([\max(0,k-D_N),k]\). Outside a deadband \([-L_N,L_N]\), it is the sign of the received observation \(\widehat E_s\); inside it is zero. A finite ramp may combine old commands convexly if all contributing samples have age at most \(D_N\). Thus when all such samples have the same sign beyond the deadband, the actual command has that sign and unit magnitude. Initial startup is included in the age bound.

Assume a whole-horizon observation guarantee

\[
\Pr\{\max_{\text{samples used}}|\widehat E_s-X_s|>\eta_N\}
\leq p_N.
\tag{3}
\]

It includes sensing, endpoint correction, quantization, sample-time uncertainty and communication failure. The sample schedule can be adapted; causality and these actual bounds are the relevant facts.

## 2. Tracking theorem

Suppose

\[
\nu_N^-\to\infty,\quad \nu_N^+D_N=o(N^2),
\quad \eta_N+L_N=o(N^2),\quad
\limsup_NN^{-1}\log p_N=-\infty.
\tag{4}
\]

Then for every \(\epsilon>0\),

\[
\limsup_N\frac1N\log
\Pr\{\max_{k\leq K_N}|X_k|>\epsilon N^2\}=-\infty.
\tag{5}
\]

For sufficiently large \(N\), a quantitative version is

\[
\begin{split}
\Pr\{\max_{k\leq K_N}|X_k|>\epsilon N^2\}
\leq p_N
&+C_\epsilon(K_N+1)
\exp\left[-\frac{c_\epsilon N^4}{N(D_N+1)+N^2}\right]\\
&+C_\epsilon(K_N+1)
\exp[-c_\epsilon N^2\min\{\nu_N^-/N,1\}].
\end{split}
\tag{6}
\]

In the intended regime \(\nu_N^-=o(N)\), the last exponent has order \(-\nu_N^-N\). Two different servos need not have matching mobilities.

## 3. Proof

The exponential-compensator inequality from (2) gives

\[
\Pr\{\max_{0\leq j\leq h}|M_{a+j}-M_a|>x\mid\mathcal F_a\}
\leq2\exp\left[-\frac{c x^2}{Nh+x}\right].
\tag{7}
\]

Indeed use \(\exp[\theta(M_{a+j}-M_a)-CN\theta^2j]\), the nonnegative-supermartingale maximal inequality, and \(\theta\) equal to the smaller of a fixed constant and \(x/(2CNh)\). Apply the same argument to the negative tail. Independent increments are unnecessary.

Set \(A=\epsilon N^2\). Cover the horizon by overlapping blocks of length \(2(D_N+1)\). Every pair of sample times at distance at most \(D_N+1\) lies in one block. By (7), except on an event of probability at most

\[
C(K_N+1)\exp\left[-\frac{cA^2}{N(D_N+1)+A}\right],
\tag{8}
\]

all martingale differences over these short windows are at most \(A/8\) in absolute value. Fixed constants absorb the difference between a block's maximum from its start and its two-point oscillation.

For sufficiently large \(N\), (4) gives

\[
(b_0+\nu_N^+)D_N\leq A/8,
\quad \eta_N+L_N\leq A/16,
\quad b_0+\nu_N^+\leq A/16.
\tag{9}
\]

Until the first failure of (3) or the short-window bound, \(X_k>A/2\) implies that every sample entering the current command has \(X_s>A/4\). Every received value is therefore positive beyond the deadband, and \(u_k=1\). Similarly \(X_k<-A/2\) implies \(u_k=-1\). This is a statement about information already available by step \(k\); no martingale is conditioned on a future good event.

Eventually \(\nu_N^-\geq2b_0\). Choose

\[
\theta_N=\min\{1/2,\nu_N^-/(8CN)\}.
\tag{10}
\]

While \(X_k>A/2\) and before a bad event, (1)--(2) imply

\[
E[e^{\theta_N(X_{k+1}-X_k)}\mid\mathcal F_k]
\leq e^{-\theta_N(\nu_N^--b_0)+CN\theta_N^2}\leq1.
\tag{11}
\]

Stop this supermartingale at level \(A\), return below \(A/2\), the first bad event, or the horizon. On the good short-window event, a new entrance above \(A/2\) starts no higher than \(3A/4\), by the one-step window bound and (9). From such an entrance, the probability of reaching \(A\) first is at most

\[
e^{-\theta_N A/4}.
\tag{12}
\]

Apply optional stopping at each stopping-time entrance and sum over at most \(K_N+1\) entrances. Repeat for \(-X\), then add the observation and window-failure probabilities. This proves (6). Since \(\nu_N^+\geq\nu_N^-\to\infty\), (4) implies \(D_N=o(N^2)\); each exponent in (6), divided by \(N\), therefore diverges. Polynomial factors do not affect (5).

An initial \(|X_0|=o(N^2)\), outside a superexponentially rare event if needed, is harmless. The same proof permits a controller that is initially unarmed and starts the valid schedule after an \(o(N^2)\) trigger is crossed, provided startup is included in \(D_N\). The probability of arming is irrelevant to this tracking conclusion.

## 4. Background and two independent scalar servos

Let \(B_1(t),B_2(t)\) be the total true signed background displacements of two isolated conductors. A sufficient actual background interface is

\[
B_1(t)-B_2(t)=\int_0^t b_sds+M^{\rm bg}(t),
\qquad |b_s|\leq b_0,
\tag{13}
\]

with bounded jumps and total conditional jump intensity \(O(N)\). The condition is uniform after any retained record over the allowed controls. It permits persistent hidden memory without a finite hidden model or a mixing bound.

A simple example is homogeneous exclusion on each ring with a bounded common reciprocal kinetic prefactor: total unforced drift is zero because \(\sum_i(\eta_i-\eta_{i+1})=0\). A bounded field of order \(1/N\) adds only \(O(1)\) total drift. Arbitrary bond-dependent reciprocal rates do not by themselves imply (13). The actual background must warrant this interface or a proved substitute.

Following the root's two-servo construction, write

\[
D=B_1-B_2,\qquad E_1=A_1+D/2,
\qquad E_2=A_2-D/2,
\tag{14}
\]

where \(A_a\) is the actual auxiliary displacement on ring \(a\). Each scalar input \(\pm D/2\) has bounded drift and bounded-jump noise with intensity \(O(N)\). Different actuator gains, particle numbers, clocks, hidden parameters and noise strengths are allowed when each scalar obeys its own instance of (1)--(4).

When both true errors are superexponentially \(o(N^2)\), exact physical-current identities give

\[
B_1+A_1=(B_1+B_2)/2+E_1,
\quad B_2+A_2=(B_1+B_2)/2+E_2,
\tag{15}
\]

\[
A_1+A_2=E_1+E_2,\qquad
A_1-A_2=-D+E_1-E_2.
\tag{16}
\]

Thus the actual auxiliary-current record is retained. Actual added charges supply the counterflow. No old branch current is discarded or renamed. The unbiased comparison has the same added lanes with forces set to zero. Root's separate path-map theorem supplies the spatial current and density consequences; they are not inferred here from an unproved path law.

## 5. Finite-duration interacting supplier

Use `FINITE_DURATION_INTERACTING_CARRIER_PORT.md`, with true auxiliary displacement \(A=J\), period \(p_*\), and fresh aggregate \(Y_k\sim N(0,R_N)\). For \(Z_k=\pm D(kp_*)/2\), define

\[
E_k=A(kp_*)+Z_k,\qquad
X_k=E_k+[P_k-P_0]/g.
\tag{17}
\]

Apply \(F_k=-a_Nu_k\). Its exact current cell is

\[
X_{k+1}-X_k
=-\frac{R_N\beta^2a_N}{2}u_k
-\beta Y_k+(Z_{k+1}-Z_k).
\tag{18}
\]

Hence \(\nu_N^- =\nu_N^+=R_N\beta^2a_N/2\). Isolation and the fresh-source filtration give (2) for the combined background and auxiliary noise when \(R_N=O(N)\). If their noise is not independent, the joint conditional exponential bound itself must be supplied; it cannot be inferred merely from marginal bounds without a conditional argument. Conditional Cauchy--Schwarz supplies such a bound from uniform conditional exponential bounds for both increments.

The physical detector reads \(E\), not \(X\). Its momentum correction enters (3). The supplier's explicit Gaussian maximum bound makes this correction superexponentially smaller than \(N^2\) for \(R_N=o(N)\), \(R_Na_N=o(N^2)\). For example \(\eta_N=N^{3/2}\) is sufficient when its deterministic force term is smaller: the endpoint-tail exponent is of order \(N^3/R_N\). Otherwise select a larger \(o(N^2)\) envelope. The explicit within-period solution and a bounded-jump background maximal bound extend tracking to every physical time.

The simultaneous regime is

\[
a_N\to0,\quad R_Na_N\to\infty,\quad R_N/N\to0,
\quad R_Na_ND_N=o(N^2).
\tag{19}
\]

In particular \(D_N=O(N)\) is allowed. Unknown force-conserving relative interactions remain present. The two lanes need not have equal \(g,b,R_N\), or equal physical periods; apply the scalar bound at each lane's own period boundaries and extend to physical time.

## 6. Separate bounded-rate independent-walker supplier

A conventional alternative has \(R_N\) actual unit charges on separate \(N\)-site circular tracks, or on an explicitly supplied noninteracting shared lane. Separate tracks cost \(O(NR_N)\) track hardware. The unbiased reference contains the same tracks and charges.

At the current state of carrier \(l\), the actual two intensities are

\[
c_l(t,\mathcal H_t)e^{F(t)/2},\qquad
c_l(t,\mathcal H_t)e^{-F(t)/2},
\qquad 0<c_-\leq c_l\leq c_+<\infty.
\tag{20}
\]

The same unknown prefactor multiplies both directions at the current state, and the force really acts as displayed. This is stronger than knowing unbiased equilibrium weights. The prefactor can retain hidden causal memory if (20) remains the complete conditional-intensity description; a constant unknown per-track clock is a simple example. Generic reciprocal edge conductances have unequal outgoing rates and do not automatically satisfy this contract.

With \(F=-a_Nu\), an inward unit command supplies per-unit-time drift between

\[
\nu_N^-=2R_Nc_-\sinh(a_N/2),\qquad
\nu_N^+=2R_Nc_+\sinh(a_N/2),
\tag{21}
\]

and total jump intensity is at most \(2R_Nc_+\cosh(a_N/2)\). The unit-jump martingale gives (2). There is no momentum correction. Unknown clocks need not be estimated, matched or reset. A supplied bounded external load of order \(1/N\) contributes only \(O(R_N/N)\) additional drift, absorbed in (1). Regime (19) applies.

A shared **exclusion** lane is not interchangeable: in a contiguous \(R_N\)-particle cluster only two edges are active, so capacity is \(O(a_N)\), rather than \(O(R_Na_N)\). Such configurations cannot be discarded solely from \(R_N/N\to0\); their probabilities need not be superexponential at speed \(N\). Independence, noninteraction, or the force-conserving finite-duration supplier is a real requirement.

## 7. Conditional records, costs and predecessor scope

An arbitrary old record or data-selected controller is allowed only if the displayed initial, future-noise and operation bounds remain valid under the conditioning. A fixed calibration failure probability cannot support an unconditional speed-\(N\) rare-event guarantee. It must be conditioned upon explicitly, or its whole-horizon failure must be included in \(p_N\) satisfying (4).

The theorem prices delay through \(\nu_N^+D_N\), capacity through \(\nu_N^-\), and actual noise through (2). It does not price detector energy, fabrication, logical reliability, fresh Gaussian preparation, injection or refrigeration. Those are actual resources declared in the companion interface. Brandes (2010) and Wagner et al. (2017), cited there, directly precede current-error feedback and shot-noise suppression. This queue estimate is a resource-qualified supplier for the composite-conductor path task, not a claim to invent current regulation.
