# Task-specific inverse learning with bounded receivers and persistent memory

30 October 2026. Root construction. The independent sparse-probe construction in `physical_mechanism/BOUNDED_SPARSE_PROBING_WITH_REAL_SATURATION.md` changed this attack: acquiring a complete boundary matrix is not compulsory. Sparse physical gradient pairs, real saturation and recorded guard flags can instead support task-specific learning. This requires a stronger physical supplier than the first exact-port theorem. No priority or practical speedup is asserted.

## 1. Capability and price

The capability is to solve a constrained regularized boundary inverse problem on one persistent passive medium while all commanded pulse norms, ADC rails and ADC output alphabets remain fixed. The controller receives bounded coefficient reports, including saturated reports. It need not learn the hidden dynamics or first acquire the complete boundary matrix.

The price is real zero-incident time between increasingly sparse active pairs. These windows export whatever energy the actual source releases through its fixed matched loads. They are not free calls, hidden resets, or evidence that the material equilibrates. No uniform decay time is required. The calibrated stochastic ADC mean is a substantive operation, and fixed unknown mean errors can leave an accuracy floor. Bounded amplitude does not supply arbitrarily fine actuator coefficients or arithmetic.

Ordinary stochastic optimization consumes the records. Full-matrix sparse acquisition, iterative feedback tuning and time-reversal adjoints remain constructive competitors. The new mechanism pursued here is the bounded task-specific source with its actual-record error budget.

## 2. The physical two-window decomposition

Let A:R^d -> R^m be fixed, unknown and contractive. A sufficient source has two contractive collocations on a common stored-energy space:

\[
x_1=T_Fx+B_Fa,\quad y=C_Fx+Aa,
\qquad x_2=T_Rx_1+B_Rv,\quad z=C_Rx_1+A^*v.          \tag{1}
\]

Its actual energy E=||x||^2 satisfies the incoming/outgoing balance. Internal dimension does not appear in the bounds. A distributed source needs its well-posed boundary energy identity. The matched mechanical and reciprocal packet suppliers give finite realizations; their terminations and signed coefficient ports are actual apparatus.

Before drawing the activity key, define

\[
\beta=C_Fx,\quad\chi_0=C_RT_Fx,\quad L=C_RB_F,
\qquad\|L\|\le1.
\]

The last bound also follows by emitting a zero-state forward pulse and zero in the second window: the second selected output cannot contain more energy than that pulse. With fresh activity bit B, actual paired reads are

\[
y=\beta+B\sigma Au,
\qquad z=\chi_0+B\sigma Lu+B\kappa\tau A^*\widehat r. \tag{2}
\]

Beta and chi_0 are fixed before B. The bounded current-round term L sigma u must not be treated as old memory independent of B. This is the extra connection: separate current-input affine ports do not imply (2) for arbitrary nonlinear hidden updates.

Inactive rounds execute the same two configurations and elapsed windows with zero incident commands. Loading and timing do not depend on measured amplitudes. Fixed replay latency can be included in the map and charged in calendar time; outcome-dependent delays cannot silently change chi_0 or L.

The task is

\[
F(u)=\tfrac12\|Au-b\|^2+\tfrac\lambda2\|u\|^2,
\quad u\in D\subseteq\{\|u\|\le U\},\quad\lambda>0,  \tag{3}
\]

with D closed convex. Put B_*=||b||. The object is an inverse waveform or decoded incremental response; an uncontrolled total warm field is a different task.

## 3. Bounded instruments and active operation

Each coordinate has an actual hard limiter and stochastic ADC Q_R satisfying

\[
E[Q_R(y)\mid\mathcal I_{\rm pre},y]=C_R(y),\quad |Q_R(y)|\le R,
\quad |Q_R(y)-C_R(y)|\le\Delta.                     \tag{4}
\]

C_R clips componentwise. Here I_pre includes the complete pre-read physical and instrument record, the current signs and commands, and earlier ADC randomizations. The current dither is freshly generated independently of that record and of the physical source. This is a fixed calibrated conditional channel, not merely a marginal mean after conditioning only on the numerical amplitude. A fixed L-level stochastic-rounding implementation has Delta=2R/(L-1), analogue one-step uniform dither and a fixed multilevel comparator. The companion proof gives the formula. Mean calibration, fixed loading and absence of sensor-randomization backaction are actual premises. No unbounded amplitude is first digitized and then clipped in software.

Let first/second rails and steps be R_y,R_z and Delta_y,Delta_z. Fix kappa>0 and write

\[
r_{\max}=R_y\sqrt m+B_*,\quad V=\kappa r_{\max},
\qquad S=U^2+V^2.                                  \tag{5}
\]

In round i choose u_i from the completed record. Draw an independent B_i with deterministic known probability p_i>0. If active, draw sigma_i, emit sigma_i u_i, read yhat_i, form rhat_i=sigma_i yhat_i-b, then draw fresh tau_i, emit kappa tau_i rhat_i and read zhat_i. Return

\[
g_i=\lambda u_i+\frac{B_i\tau_i}{p_i\kappa}\widehat z_i. \tag{6}
\]

On an inactive round both inputs are zero and g_i=lambda u_i. Every forward command has norm at most U; every replay has norm at most V. Receiver rails and alphabets stay fixed. The increasing importance weight 1/p_i is digital arithmetic, not an emitted amplitude. Its arithmetic precision and the forward command's coefficient accuracy are still actual costs.

## 4. Clipping bias and the physical occupation budget

First assume R_y>U and R_z>U+V. For a symmetric clipped read,

\[
D_R(h,c)=\tfrac12\{C_R(h+c)-C_R(h-c)\},
\]

each component has the sign of c and magnitude at most |c|. It equals c_j when |h_j|+|c_j|<=R. Hence

\[
\|D_R(h,c)-c\|\le\|c\|
\sum_j1_{\{|h_j|>R-\|c\|\}}.                       \tag{7}
\]

For the first sign c=Au, so first-read bias is at most U||beta||^2/(R_y-U)^2. Tau is averaged after rhat is known. Its actual background is chi_0+sigma Lu. Since ||Lu||<=U and ||kappa A^*rhat||<=V, second-read clipping is impossible unless some |chi_{0,j}|>R_z-U-V. Its divided-by-kappa bias is at most r_max||chi_0||^2/(R_z-U-V)^2.

With H_i the full pre-key physical history,

\[
h_i:=E[g_i\mid H_i]-\nabla F(u_i),\qquad
\|h_i\|\le K(\|\beta_i\|^2+\|\chi_{0,i}\|^2),
\]
\[
K=\max\left\{\frac U{(R_y-U)^2},
\frac{r_{\max}}{(R_z-U-V)^2}\right\}.               \tag{8}
\]

Importance weighting cancels the activity probability. It does not cancel clipping: h_i is a genuine conditional bias.

Add the two real passivity balances. Fresh signs give

\[
E\|y_i\|^2=E\|\beta_i\|^2+p_iE\|Au_i\|^2,
\]
\[
E\|z_i\|^2=E\|\chi_{0,i}\|^2+p_iE\|Lu_i\|^2
 +\kappa^2E[B_i\|A^*\widehat r_i\|^2].              \tag{9}
\]

Tau removes cross terms with the replay although rhat depends on the first sign and ADC. Sigma removes the chi_0--L u cross term. For E(x_0)<=E_0, telescoping proves

\[
\boxed{\sum_{i\le N}E(\|\beta_i\|^2+\|\chi_{0,i}\|^2)
\le E_0+S P_N,\qquad P_N=\sum_{i\le N}p_i.}         \tag{10}
\]

This bounds the occupation of large returning fields, not their instantaneous decay. No window is declared to start reset.

The naive estimate of the second field only on active rounds loses a factor 1/p and leaves a constant bound. Separating the bounded current-pair excitation before setting the second rail repairs that argument. The stronger two-window interface is essential.

## 5. Active records reveal a conservative clipping debit

A worst-case mean bias bound is useful for convergence but can be far too costly for a stopping rule. The ADC outputs can also produce guard flags without an unbounded readout or an extra analogue amplitude measurement.

Require R_y>2U+Delta_y and R_z>2(U+V)+Delta_z, and on each active pair set

\[
f^y_{ij}=1_{\{|\widehat y_{ij}|\ge R_y-2U-\Delta_y\}},
\quad
f^z_{ij}=1_{\{|\widehat z_{ij}|\ge R_z-2(U+V)-\Delta_z\}}.
                                                               \tag{11}
\]

If |beta_j|>R_y-U, every first-sign outcome has |y_j|>R_y-2U. Clipping at R_y and an ADC error at most Delta_y therefore force the first flag. If |chi_{0,j}|>R_z-U-V, every combination of current signs, first ADC and replay satisfies |z_j|>R_z-2(U+V), forcing the second flag. This includes first-pulse self-excitation. Flags may also fire conservatively when there is no clipping.

Define from actual active reports

\[
F_i^{\rm flag}=U\sum_{j=1}^m f^y_{ij}
 +r_{\max}\sum_{j=1}^d f^z_{ij},\qquad
C_F=Um+r_{\max}d.                                  \tag{12}
\]

Then 0<=F_i^flag<=C_F and, with no clipping event discarded,

\[
\|h_i\|\le f_i:=E[B_iF_i^{\rm flag}/p_i\mid H_i].    \tag{13}
\]

For deterministic nonnegative weights w_i and a fixed horizon N, put

\[
S_N^w=\sum_{i\le N}w_i,\quad
a_N=\max_{i\le N}(w_i/p_i),\quad
O_N=\sum_{i\le N}\frac{w_iB_iF_i^{\rm flag}}{p_i}.
\]

A bounded nonnegative-increment argument gives, with probability at least 1-delta_B,

\[
\sum_{i\le N}w_i f_i\le
D_N:=\frac{O_N+a_NC_F\log(1/\delta_B)}{1-e^{-1}}.   \tag{14}
\]

**Proof.** Let Z_i=w_iB_iF_i^flag/(p_i a_N C_F), so 0<=Z_i<=1. Convexity gives exp(-z)<=1-(1-e^{-1})z on [0,1]. Consequently

\[
\exp\left((1-e^{-1})\sum_{i\le t}E[Z_i\mid H_i]
 -\sum_{i\le t}Z_i\right)
\]

is a nonnegative supermartingale. Markov's inequality at N proves (14). The observed O_N and gradient record may be dependent; the later union bound does not require independence.

The audit reads only active pairs. The record-geometry role also constructed a different option: read bounded guard flags during inactive windows, which directly expose beta and chi_0 without current excitation. That can use weaker rail margins and more idle sensing. It is retained separately; neither receiver dominates without pricing time, sensing and range.

### Sufficient margins for the flags themselves to become rare

For a general completion statement, require the stronger fixed margins

\[
s_y=R_y-3U-2\Delta_y>0,\qquad
s_z=R_z-3(U+V)-2\Delta_z>0.                          \tag{15}
\]

An observed first flag then implies |beta_j|>=s_y, and a second implies |chi_{0,j}|>=s_z. This follows by undoing the at-most-Delta quantization error and then subtracting the bounded current contributions. Thus, on each active pair,

\[
F_i^{\rm flag}\le K_F(\|\beta_i\|^2+\|\chi_{0,i}\|^2),
\quad K_F=\max\{U/s_y^2,r_{\max}/s_z^2\}.           \tag{16}
\]

For w_i=i, freshness of B and (10) give

\[
E[O_N]\le K_FN(E_0+SP_N).                           \tag{17}
\]

One literal fixed choice is 33 output levels per coordinate, R_y=4U and R_z=4(U+V). Then Delta_y=U/4, Delta_z=(U+V)/4, s_y=U/2 and s_z=(U+V)/2. U>0 is assumed; U=0 is a trivial task. The finite alphabet has 33 levels, requiring six bits under a straightforward binary encoding. Its calibration is not free.

## 6. Finite confidence from the same bounded record

The gradient no longer has the exact symmetric-noise decomposition of the previous theorem. Use an ordinary bounded martingale bound and explicitly add the clipping debit.

Let M_i=g_i-E[g_i|H_i]. In any coordinate, the importance-weighted random part in (6) gives

\[
|w_iM_{ij}|\le \frac{2w_iR_z}{p_i\kappa},\qquad
E[(w_iM_{ij})^2\mid H_i]\le\frac{w_i^2R_z^2}{p_i\kappa^2}.
\]

Define deterministic horizon bounds

\[
c_N=2R_za_N/\kappa,\qquad
v_N=\frac{R_z^2}{\kappa^2}\sum_{i\le N}\frac{w_i^2}{p_i},
\quad \ell=\log(2d/\delta_M).
\]

Scalar martingale Bernstein bounds in both directions, followed by a union bound across d coordinates, yield with probability at least 1-delta_M

\[
\left\|\sum_{i\le N}w_iM_i\right\|
\le H_N:=\sqrt d\left(\sqrt{2v_N\ell}+
\frac{2c_N\ell}{3}\right).                         \tag{18}
\]

For completeness, the scalar ingredient follows from the Taylor bound
E exp(theta X)<=exp(theta^2 E[X^2]/[2(1-theta c/3)])
for a mean-zero |X|<=c and 0<theta<3/c, iterated conditionally. Chernoff optimization gives exp(-t^2/[2(v+ct/3)]). The threshold sqrt(2v ell)+2c ell/3 is a conservative solution, so (18) does not require independent rounds or an imported unproved vector inequality.

For the actual averages ubar_N=sum w_i u_i/S_N^w and gbar_N=sum w_i g_i/S_N^w, the quadratic gradient is affine. Therefore, on the intersection of (14) and (18),

\[
\boxed{\|\bar g_N-\nabla F(\bar u_N)\|
\le e_N:=\frac{H_N+D_N}{S_N^w}.}                    \tag{19}
\]

The failure probability is at most delta_M+delta_B. Only bounded ADC values, activity/sign keys, commands and guard flags enter the computed radius. No internal state or fitted A enters it. Known initial energy is needed for a priori cost and continued hardware validity, not for evaluating (19).

At predetermined checkpoints N_j=2^j, preallocate alpha_j=6alpha/[pi^2(j+1)^2] and take delta_M=delta_B=alpha_j/2. The union bound gives simultaneous coverage at all these checkpoints. One may stop at the first checkpoint where the declared precision is met; post-hoc reweighting of individual observations is not allowed.

As in the earlier exact-port proof, eta=1/(1+lambda) and

\[
\mathcal R_N=
\frac{\|\bar u_N-\Pi_D(\bar u_N-\eta\bar g_N)\|}{\eta\lambda}
 +\frac{e_N}{\lambda}                               \tag{20}
\]

bound ||ubar_N-u_*|| on this single simultaneous event. This handles an active constraint and an input selected from the same records. It is frequentist coverage, not a posterior probability conditional on an arbitrary selected rare record. It certifies this fixed incremental task, not all later interventions.

## 7. One continuing schedule and an ordinary optimizer

Choose p_i comparable to i^{-a}, 0<a<1. A literal dyadic schedule is

\[
p_i=2^{-\lceil a\log_2(i+1)\rceil},                 \tag{21}
\]

using a finite number of fresh fair bits. It obeys (i+1)^{-a}/2<=p_i<=(i+1)^{-a}. Use ordinary projected SGD

\[
u_{i+1}=\Pi_D\{u_i-\eta_i g_i\},\quad
\eta_i=2/[\lambda(i+1)],\quad w_i=i.                \tag{22}
\]

There is one persistent physical chronology. Statistical weights and the key schedule do not reinitialize it. Both windows of every inactive round still elapse.

Put J=dR_z^2/kappa^2. The gradient second moment satisfies

\[
E\|g_i\|^2\le2J/p_i+2\lambda^2U^2.
\]

The same weighted projection proof as before, now retaining h_i, gives

\[
E[F(\bar u_N)-F(u_*)]
\le\frac{4J\sum_{i\le N}p_i^{-1}+4\lambda^2NU^2}
 {\lambda N(N+1)}
 +\frac{4UK(E_0+SP_N)}{N+1}.                       \tag{23}
\]

It tends to zero for every 0<a<1. The two leading contributions have orders N^{a-1} and N^{-a}; a=1/2 balances this conservative expected-objective bound.

For same-record gradient precision, (18) divided by S_N^w has order N^{(a-1)/2} up to logarithms. The expected observed clipping debit divided by S_N^w is O(E_0/N+N^{-a}), by (17). Thus a=1/3 balances the task-facing gradient-accuracy scales. Expected active pairs then grow as N^{2/3}; real calendar windows are 2N. This is a time/probe tradeoff, not a practical superiority claim. Confidence constants and field/ADC dimensions may be large.

There is also an almost-sure completion statement under indefinite valid operation. From (8)--(10), the cumulative expected bias is O(N^{1-a}). Summation by parts gives sum_i E||h_i||/i<infinity. Also sum_i E||g_i||^2/i^2<infinity because a<1. The projected distance recurrence has summable bias and noise errors, so the ordinary almost-supermartingale argument gives u_i->u_* almost surely.

At dyadic checkpoints, (17) and Markov's inequality are summable for any fixed positive threshold on O_N/S_N^w; hence that quantity tends to zero almost surely. The deterministic audit offset a_N log(1/delta_B)/S_N^w is O(N^{a-1} log j), and the Bernstein term tends to zero. The weighted gradient error also tends to zero almost surely by applying the confidence construction at levels approaching zero. Consequently (20) eventually reaches every positive threshold at unbounded checkpoints. This is not a deterministic deadline, a bound on source lifetime, or permission to exceed a declared apparatus rating.

## 8. Physical scope, correction floors and useful failures

**The essential operation changed.** Full-range signed replay has been replaced by an actual hard limiter, bounded stochastic ADC, sparse fixed-clock operation and conservative guards. The ordinary full-matrix sparse learner can use the same finite instruments; a faster calibrated or rapidly relaxing device may make that conventional route preferable.

**Current excitation cannot be ignored.** Without the term B sigma L u, treating the second background as independent of B produces a false sparse-bias argument. The rail margins explicitly pay for this excitation. A nonlinear hidden source that reacts to the active key by releasing stored energy need not admit (2); it is outside this theorem even if it is passive.

**Sensing choices have different costs.** The active audit uses wider margins but needs no idle output readings. The complementary inactive audit reads real zero-input windows and can use narrower margins. Both retain all recorded saturation; neither discards inconvenient observations.

**Fixed ADC levels do not give free exact calibration.** If the first and second conditional mean contracts have uniformly bounded vector defects delta_y and delta_z, the gradient can have an extra bias at most delta_y+delta_z/kappa. A conservative certificate must add this quantity to e_N; its optimum-distance floor is divided by lambda. This statement retains the absolute ADC error intervals in (4); if those change, the guard thresholds must also be enlarged accordingly. Reference-waveform accuracy, actuation, finite arithmetic, timing and loading errors need their actual bounds as well. A varying A cannot be hidden in the old-field budget.

**Thermal and active fluxes are not free.** An ongoing energy injection adds to (10). If its expected cumulative energy is linear in N, the sparse clipping proof can leave a nonzero floor. Sensor noise covered by the calibrated bounded instrument differs from uncharged force noise driving the material. A known bath model or another receiver might solve a larger task, but it is not established here.

**External range requires a supplier.** General passivity controls L2 energy, not every instantaneous internal voltage. The fixed-wavepacket reciprocal coupler family in the complementary proof has a uniform external amplitude bound ||x_0||+3a sqrt(n) for every bounded incident sequence and arbitrary slow leakages. With a=max(U,V), it supplies a real bounded external-port family for this task. Its symmetric A uses the same physical port as its adjoint. Other media need their own front-end and waveform rating.

**The complete physical cycle remains priced.** Both active and idle windows, sensing where performed, fixed matched loads, source and receiver calibration, random-key generation, waveform storage, computation, communication, dissipation and eventual restoration are actual costs. No raw warm-field cancellation, work advantage or acquired end-to-end apparatus precision has been shown.

The closest ingredients and their actual read scopes remain in the two complementary source records: binary-sensor identification, dither, randomized adjoint ILC, physical inverse filtering, passivity and reset-free/mixing-free learning all have direct predecessors. The contribution sought here is the explicit combined operation and its task-specific confidence/energy argument. External priority remains unestablished.

### Binding ADC clarification from the focused challenge

The record-geometry role found that a marginal E[Q(z)|z] statement alone is insufficient. At A=0 and beta=chi_0=0, an instrument returning zhat=Delta_z tau has the displayed marginal mean zero and bounded error, yet adds gradient bias Delta_z/kappa without triggering a guard. The complete-history conditional channel in (4), with fresh independent dither, excludes this counterexample. The pre-correction source is preserved in `review_snapshots/`. The executed code already generated ADC dither from a separate fresh random stream; this wording correction is essential to the theorem's physical scope.
