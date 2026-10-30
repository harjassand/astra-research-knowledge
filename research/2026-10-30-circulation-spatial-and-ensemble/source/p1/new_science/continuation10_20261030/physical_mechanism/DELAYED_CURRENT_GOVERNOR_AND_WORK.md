# Delayed ordinary current feedback: vanishing carrier density, rare-current tracking, and the actual work distinction

Status: constructive ordinary comparator, developed in the existing physical-mechanism role. No priority claim. Root owns the full joint density/current path-map receiver; this note supplies a controller, a hidden-dynamics-independent equilibrium estimate, and an exact work comparison. All older work is preserved.

## 1. Result and what changes the comparison

Let an untouched stationary reversible native conductor have total jump activity at most `C N`, with an antisymmetric counted increment of magnitude at most one per jump. Its microscopic state, including frozen classes and evolving hidden variables, need not be reconstructed or mixed. Supply `R_N` additional **real** independently controlled carriers, with

\[
1\ll K_N\ll R_N\ll N.
\tag{1}
\]

Every native and auxiliary signed displacement is counted in the composite conductor. A delayed, clipped, linear feedback law with gain `g_N=K_N/N^2` suppresses the composite integrated-current error on the physical interval `[0,N^2T]`:

\[
\lim_{N\to\infty}\frac1N\log\Pr\left\{
\sup_{t\le N^2T}|J_{\rm native}(t)+J_{\rm aux}(t)|>
\varepsilon N^2\right\}=-\infty.
\tag{2}
\]

For the equilibrium initial law, its **expected carrier affinity heat** is

\[
\mathbb E W_{\rm aux}=O(K_NN/R_N)=o(N).
\tag{3}
\]

The actual affinity cap tends to zero. The controller tolerates a complete communication/control epoch of order `N`; the proof also allows a conservative digital epoch of order `N log N` if `K_N log N/N -> 0`.

By contrast, any controller at the same calibrated auxiliary port which must supply a sustained nonzero mean counter-current over time `N^2T` pays

\[
\mathbb E W_{\rm aux}=\Omega(N^2/R_N).
\tag{4}
\]

The distinction is between equilibrium fluctuation suppression and sustained mean transport. Equation (4) is not a lower bound on the expected cost in (3). Neither equation prices sensing, communication, clocking, carrier preparation, field drivers, control memory, or erasure. No total-apparatus energy advantage is established.

## 2. The ordinary predecessor is already a current governor

Brandes, *Feedback Control of Quantum Transport*, PRL **105**, 060602 (2010), explicitly drives transport rates from the accumulated count error `I_0 t-n`. For the elementary model it obtains variance `(1-exp(-2 g Gamma t))/(2g)`: cumulative-error feedback freezes transferred-charge fluctuations. Its actual primary PDF was read, including Eqs. (1)–(6): <https://arxiv.org/pdf/1005.0018>, DOI <https://doi.org/10.1103/PhysRevLett.105.060602>.

Wagner et al., *Strong suppression of shot noise in a feedback-controlled single-electron transistor*, Nature Nanotechnology **12**, 218–222 (2017), implement a sampled electronic loop, integrated charge counting, finite feedback windows, gate corrections and saturation at the limits of the usable rate range. Their Eq. (1) accumulates interval count errors into the control voltage; the measured count variance saturates. Primary text read through the feedback protocol and bandwidth discussion: <https://arxiv.org/pdf/1602.05466>, DOI <https://doi.org/10.1038/nnano.2016.225>. These experiments do not supply the isolated additional-carrier geometry below, but they defeat any claim that sampled current-error stabilization or finite response is a new principle.

Fricke et al., *Quantized current source with mesoscopic feedback*, PRB **83**, 193306 (2011), use two series pumps and an intermediate island. Accumulated mismatch changes the island potential and locks the second pump to the first. The actual primary text and charge-balance explanation were read: <https://d-nb.info/1211836061/34>, DOI <https://doi.org/10.1103/PhysRevB.83.193306>. This is a stronger actual autonomous comparator when series reconnection and feedback onto the native source are permitted; it does not preserve the isolated native dynamics at the port in this note.

Brandes, *Feedback between interacting transport channels*, PRE **91**, 052149 (2015), already develops passive/autonomous interaction-based feedback, bidirectional rates, local propagation, and separate interaction-energy and transport-heat terms. Sections II and IV were read: <https://arxiv.org/pdf/1503.03672>, DOI <https://doi.org/10.1103/PhysRevE.91.052149>. Its channel-relative stabilization and local feedback propagation are close precedents. Its finite-channel collective mode remains a distinct issue from making a selected **composite** current superexponentially small with additional controlled carriers.

The possible addition here is the explicit many-body scaling and work/interface comparison: leave an arbitrary reciprocal native process untouched, count the additional carrier motion honestly, and exploit the large separation between the communication scale, the relaxation scale of the controller, and the diffusive observation horizon. The governing feedback idea is ordinary.

## 3. Actual auxiliary port and its heat

Take `R=R_N` independent charges on homogeneous `N`-site rings. One separate track per charge is an explicit supplier, costing `O(NR)` track cells. A noninteracting gas in a shared lane is another, stronger supplied physical primitive; a generic exclusion lane is not equivalent, because clustering can remove its uniform drift capacity. Carrier positions can start arbitrarily. Their signed step counts start at zero by defining a new observation interval; no positional reset or microscopic copy is used.

For a spatially uniform dimensionless affinity `f` per signed step, each carrier has rates

\[
q_+(f)=c e^{f/2},\qquad q_-(f)=c e^{-f/2},\qquad c>0.
\tag{5}
\]

The symmetric prefactor `c` is a calibrated supplier parameter. The only required rate-control port in (5) is the affinity; no independent barrier or activity control is silently added. The total drift and activity are

\[
u(f)=2cR\sinh(f/2),\qquad a(f)=2cR\cosh(f/2).
\tag{6}
\]

The command realizing aggregate drift `u` is

\[
f(u)=2\operatorname{arsinh}\frac{u}{2cR}.
\tag{7}
\]

With the step work convention `k_B T=1`, the physical affinity work is the stochastic integral

\[
W_{\rm aux}=\int f_t\,dJ_{\rm aux}(t).
\tag{8}
\]

For predictable feedback, compensated counting gives exactly

\[
\mathbb E W_{\rm aux}
=\mathbb E\int H_R(u_t)dt,
\quad H_R(u)=2u\operatorname{arsinh}\frac{u}{2cR}.
\tag{9}
\]

Here `H_R` is nonnegative, even, convex, and

\[
H_R(u)\le\frac{u^2}{cR},\qquad
H_R(u)=\frac{u^2}{cR}(1+o(1))\quad\hbox{uniformly for }|u|/R\to0.
\tag{10}
\]

The rings are homogeneous and have no varying conservative internal energy in this supplier. Equation (8) therefore measures the affinity work delivered to carrier motion, whose mean is dissipated to its thermal bath. Work needed to generate or switch the field, power the detectors and processor, communicate, or initialize the device is additional. A negative realization of (8) is possible; only the stated expected identity is nonnegative.

All auxiliary motion is real and counted. This construction is not an estimator subtracting a signal from the reported native current. The actual native carriers are not held, returned, redirected, or assigned transformed displacement.

## 4. Delayed controller and stable response kernel

Let `T_N=N^2 T`. Choose an epoch length `Delta_N` satisfying

\[
\Delta_N\ge c_0N,\qquad
h_N:=g_N\Delta_N\to0,\qquad
g_N=K_N/N^2.
\tag{11}
\]

For a supplied `O(N)` local communication loop, take `Delta_N=C N`. If a literal fixed-bit-rate implementation is preferred, a simple store-and-forward sum and broadcast of `O(log N)`-bit counters is covered by `Delta_N=C N log(2+N)` and the additional choice `K_N log N/N ->0`. The latter avoids treating a growing digital word as a free constant-time message.

Define

\[
X(t)=J_{\rm native}(t)+J_{\rm aux}(t),\qquad X_m=X(m\Delta_N),
\quad X_{-1}=X_0=0.
\tag{12}
\]

During epoch `m`, use the previous completed measurement:

\[
u_m=-\operatorname{clip}(g_N X_{m-1},-K_N,K_N),\qquad
f_m=f(u_m).
\tag{13}
\]

The whole epoch is available to aggregate the newer measurement and distribute the next command. There is no instantaneous global event-by-event update. Local sensors must still count the actual native and auxiliary displacements; the costs and error contract of those sensors remain part of the apparatus.

The maximum force is

\[
a_N=2\operatorname{arsinh}\frac{K_N}{2cR_N}
\sim\frac{K_N}{cR_N}\to0,
\quad R_N a_N\sim K_N/c\to\infty.
\tag{14}
\]

All carrier jump rates stay bounded, and total auxiliary activity is at most `C R_N`.

The affinity in (14) is **per unit step**. A whole turn around an `N`-site track has cycle affinity `N a_N=O(NK_N/R_N)`, which generally grows. Thus weak local forcing is not a bounded-total-loop-electromotive-force claim. A fixed total-loop affinity would instead give per-step affinity `O(1/N)` and aggregate drift capacity `O(R_N/N)`, insufficient for this construction. Distributed local drive or the growing total-loop voltage range is an actual extra-carrier control resource.

Before the clipping threshold is reached, the exact recursion is

\[
X_{m+1}=X_m-h_N X_{m-1}+\zeta_m,
\quad
\zeta_m=J_{\rm native}((m+1)\Delta_N)-J_{\rm native}(m\Delta_N)
+M_{\rm aux}((m+1)\Delta_N)-M_{\rm aux}(m\Delta_N),
\tag{15}
\]

where `M_aux=J_aux-int u dt` is the actual compensated auxiliary current.

For `0<h<1/8`, the two roots are

\[
r_\pm=(1\pm\sqrt{1-4h})/2.
\tag{16}
\]

They obey `0<r_-<r_+<1`, `r_+<=1-h`, and `r_+-r_->1/sqrt(2)`. The impulse coefficients

\[
G_j=\frac{r_+^{j+1}-r_-^{j+1}}{r_+-r_-},\qquad j\ge0,
\tag{17}
\]

have `G_0=1`, `G_1=1`, and satisfy the recursion in (15). They give

\[
0\le G_j\le C(1-h)^j,\qquad
\sum_{j\ge0}G_j^2\le C/h,\qquad
\sum_{j\ge0}G_j=1/h.
\tag{18}
\]

For a sample at epoch `m`, its response to the native and auxiliary increments is therefore a deterministic piecewise-constant current filter `w_m`, with

\[
\|w_m\|_\infty\le C,\qquad
\int w_m(s)^2 ds\le C\Delta_N/h_N=C/g_N.
\tag{19}
\]

The non-martingale native drift has not been discarded. It is treated by the next reversible-path estimate.

## 5. A native-current bound which needs no hidden mixing

Let the native full-state jump generator be reversible in a warranted probability law `mu_N`, with total exit rate at most `C N`. Let `d(x,y)=-d(y,x)` and `|d|<=1` be the current increment. Frozen classes can be handled conditional on each class; the constants are uniform. The full state space need not be finite.

For real `xi`, the current-tilted generator is

\[
(L_\xi f)(x)=\int q(x,dy)[e^{\xi d(x,y)}f(y)-f(x)].
\tag{20}
\]

Reversibility makes its Hermitian part have off-diagonal weights `q cosh(xi d)`. Applying `2ab<=a^2+b^2`, or completing its symmetric Dirichlet form, gives

\[
\operatorname{Re}\langle f,L_\xi f\rangle_{\mu_N}
\le C N(\cosh|\xi|-1)\|f\|_2^2.
\tag{21}
\]

The same estimate applied successively to a nonautonomous tilted propagator yields, for every bounded deterministic filter `w`,

\[
\mathbb E_{\mu_N}\exp\left\{\theta\int w(s)dJ_{\rm native}(s)\right\}
\le\exp\left\{CN\int[\cosh(\theta w(s))-1]ds\right\}.
\tag{22}
\]

In particular, for `|theta| ||w||_infty<=1`,

\[
\log\mathbb E_{\mu_N}e^{\theta\int w dJ_{\rm native}}
\le C'N\theta^2\int w^2ds.
\tag{23}
\]

This is a path-current estimate, not an assertion that the native current itself is a martingale. It does not use a spectral gap, predictive-state rank, rate reconstruction, or a hidden-state reset.

Since the native system is untouched, it is legitimate **in the proof** to condition on its complete path. The independent auxiliary random clocks then retain their compensated-martingale property, with bounded intensity even though their rates depend causally on the observed native path. For the deterministic filter in (19), a bounded-jump exponential martingale gives, also after any stopping time,

\[
\log\mathbb E\left[e^{\theta\int w_m dM_{\rm aux}^{\rm stopped}}
\mid\hbox{native path}\right]\le C R_N\theta^2/g_N
\quad (|\theta|\le c).
\tag{24}
\]

No microscopic future is provided to the real controller by this conditioning argument.

## 6. Whole-horizon tracking, including clipping

Let `tau` be the first epoch index at which `|X_m|>=N^2`. Up to that epoch the actual recursion is linear. Define a surrogate linear recursion with the full untouched native path and the auxiliary martingale stopped at `tau Delta_N`. It agrees with the actual process up to and including `tau`. Combining (19), (23), and (24) gives the surrogate sample estimate

\[
\log\mathbb E e^{\theta\widetilde X_m}
\le C(N+R_N)\theta^2/g_N\le C'N\theta^2/g_N.
\tag{25}
\]

For a threshold `epsilon N^2`, choose `theta` proportional to `epsilon K_N/N`. This tends to zero and is admissible. The bound becomes

\[
\Pr\{|\widetilde X_m|>\epsilon N^2\}
\le 2e^{-c\epsilon^2 K_NN}.
\tag{26}
\]

A union over the `O(N^2/Delta_N)` epoch samples shows that cap activation itself has probability `exp[-c K_NN+O(log N)]`. The same first-exit argument at any smaller fixed threshold proves the sampled version of (2). The stopped surrogate is only a proof device; its behavior after the first exit is irrelevant.

For completeness, control between samples does not require monitoring every event centrally. On a stationary reversible native path on a block of duration `Delta_N`, write its forward and reversed current martingales as `M_f` and `M_b`. With the antisymmetric current convention,

\[
2J_{\rm native}(0,t)=M_f(t)-[M_b(\Delta_N)-M_b(\Delta_N-t)].
\tag{27}
\]

Both martingales have jumps of magnitude at most one and quadratic variation rate at most `C N`. A bounded-jump martingale inequality therefore yields

\[
\Pr\left\{\sup_{t\le\Delta_N}|J_{\rm native}(0,t)|>a\right\}
\le C\exp\left[-c\frac{a^2}{N\Delta_N+a}\right].
\tag{28}
\]

The same estimate holds for the auxiliary martingale with `N` replaced by `R_N`. The deterministic within-block auxiliary drift is at most `K_N Delta_N=o(N^2)`. For `Delta_N=O(N)` or `O(N log N)` and `a=epsilon N^2`, the exponent in (28), divided by `N`, diverges. Taking a union over blocks proves (2).

The proof extends the tracking bound to native initial laws with density ceiling `dnu_N/dmu_N <= exp(C_0 N)` by paying this factor in the native-path probability estimates. It does **not** extend the low expected-work conclusion below to arbitrary such initial laws. A nonflat or loaded initial condition can generate a mean current that requires sustained correction.

## 7. Equilibrium expected heat

The same filtered-current estimates give

\[
\mathbb E[|X_m|^2\mathbf1_{m<\tau}]
\le\mathbb E|\widetilde X_m|^2\le C N/g_N.
\tag{29}
\]

One can obtain this directly by differentiating (25) at zero; the native filter has zero mean by stationary reversibility, and the stopped auxiliary martingale has conditional mean zero given the native path.

Before cap activation, (10) and (29) imply

\[
\begin{aligned}
\mathbb E W_{\rm aux}^{\rm before\ cap}
&\le\frac{g_N^2}{cR_N}\sum_m\Delta_N\,
\mathbb E[|X_{m-1}|^2\mathbf1_{m-1<\tau}]\\
&\le C\frac{g_N^2}{R_N}(N^2T)\frac{N}{g_N}
=C_T\frac{K_NN}{R_N}.
\end{aligned}
\tag{30}
\]

This notation refers to the expected compensator contribution in (9), avoiding a false pathwise nonnegativity claim about stochastic heat. After the first cap activation the total compensator heat is bounded by `C N^2 K_N^2/R_N`. Its expectation is at most this bound times the superexponentially small cap-activation probability. Equation (3) follows.

For example, `R_N=N^(2/3)`, `K_N=N^(1/3)` permits epochs of either `O(N)` or `O(N log N)`, affinity cap `O(N^(-1/3))`, and expected carrier heat `O(N^(2/3))`. This is an asymptotic mathematical resource example, not a demonstrated physical apparatus.

The conditional relative entropy of the controlled auxiliary counting law against its zero-affinity law is also finite and satisfies

\[
D(P_{\rm controlled}\Vert P_{\rm zero\ affinity})
=\mathbb E\int\left[\frac{f_tu_t}{2}-2cR_N(\cosh(f_t/2)-1)\right]dt
\le\frac12\mathbb E W_{\rm aux}.
\tag{31}
\]

The native path law is identical on both sides. Equation (31) is an ordinary jump-process likelihood identity; it is not an information-erasure cost. Subextensive relative entropy does not force equal rare-event rate functions: exponentially rare records can be strongly changed while contributing negligibly to this average divergence.

## 8. Sustained counter-current has a different unavoidable bill

For any predictable feedback at the same affinity-only port, let `t_*=N^2T` and `j_* = E J_aux(t_*)`. Convexity of `H_R` and (9) yield the exact inequality

\[
\mathbb E W_{\rm aux}
\ge t_* H_R(j_*/t_*)
=2j_*\operatorname{arsinh}\frac{j_*}{2cR_Nt_*}.
\tag{32}
\]

When `j_*/t_* -> v !=0`, this is

\[
\mathbb E W_{\rm aux}\ge(1-o(1))\frac{v^2N^2T}{cR_N}.
\tag{33}
\]

A constant affinity realizing drift `v` attains the lower bound on mean heat. Knowledge of the native kinetics, a more informed waveform, or a different feedback algorithm cannot lower this bound without changing the auxiliary mobility or other supplied resources. A loaded native conductor with sustained mean current and a target that cancels it lies in this regime.

Equation (32) must **not** be applied after conditioning on a future rare event: the compensated-current martingale need not have mean zero under that conditioning. If the apparatus is required to track a prescribed load with high probability, the corresponding sustained-mean lower bound applies. For a rare spontaneous native trajectory in the equilibrium deployment, conditional heat, control-action cost, and mean deployed heat are different quantities. The current theorem proves (3), not a uniform subextensive-work guarantee on every rare record.

## 9. Precision, records and actual apparatus costs

Suppose an epoch counter read has deterministic error at most `eta_N`. Before clipping, this adds a disturbance of size at most `h_N eta_N` to the recurrence. By (18), the resulting counter bias is at most `C eta_N`. Thus tracking survives if `eta_N=o(N^2)`. To retain the same expected-heat order as (30), it is sufficient to require

\[
\eta_N^2=O(N^3/K_N).
\tag{34}
\]

More explicitly the compensator-heat estimate acquires an additive term `O(K_N^2 eta_N^2/(R_N N^2))`. Actual missed-event errors must satisfy a supplied error probability contract; a fixed unexplained detector failure probability does not establish a speed-`N` superexponential statement. A deterministic finite counter/quantization error and a certified sensor-error event are separate matters.

Typical equilibrium aggregate commands are only of order `sqrt(K_N/N)`, so the typical per-carrier affinity is of order `sqrt(K_N/N)/R_N`. Fixed force resolution need not resolve this scale. The theorem uses a calibrated command port or a precision budget that improves with `N`. Polynomial choices in (1) need only logarithmically many ideal digital bits to describe the scales, but the corresponding analogue generation, noise and reliability are real physical requirements.

All controller commands, delayed reads, and auxiliary displacement records may be retained. This is not a construction based on hiding a random selector. For the equilibrium heat bound conditional on an old record `D` and frozen class `h`, the actual native starting law must be the warranted `mu_(N,h)` conditional on `(D,h)`, or an explicitly justified equivalent. Unconditional equilibrium does not imply that premise after arbitrary retained calibration. If uniform conditional premises hold, averaging over `(D,h)` preserves the result. The unconditional probability estimate is not a guarantee after arbitrary rare postselection of controller records.

An implementation has at least the following unpriced resources:

* `R_N` actual carriers and their initial preparation; independent tracks cost `O(NR_N)` cells.
* Native and auxiliary displacement sensing. The native total microscopic event count can be `O(N^3)` over this horizon even though commands update only `O(N)` times.
* A local communication network, finite-speed aggregation and broadcast, clock synchronization, and storage of signed counts. The `O(N log N)` option above is a conservative fixed-bit-rate schedule.
* A homogeneous affinity port for every auxiliary track, calibrated response, finite field precision and field-switching work.
* Controller memory, the desired retained record, and any eventual erasure. Retaining the record does not pay the acquisition or communication cost.

Counting only one cut current is insufficient in a general nonflat ring program: total signed displacement differs from `N` times a cut count by an endpoint polarization term which can itself be `O(N^2)`. The required sensor measures the stated aggregate or also supplies that polarization correction. No free microscopic current readout is inferred from label access.

A capacitor coupled reciprocally to the **total** accumulated current may provide an autonomous governor, but its reciprocal force generally acts on the native carriers as well. Leaving the native law unchanged while acting only on the auxiliary carriers requires the actual directional sensing/feedback interface above, or a separately proved supplier. The passive series-pump predecessor does not silently supply this asymmetric port.

## 10. Consequence for selection

Ordinary sampled feedback already provides the current-error control mechanism once genuine auxiliary carrier, sensing, communication and affinity ports are granted. A strong comparison must therefore use that implementation, including its weak linear regime, instead of comparing only to constant bang-bang forcing.

The constructive result is the simultaneous window `1<<K_N<<R_N<<N`: the auxiliary density vanishes, the native path is untouched, the composite-current tracking error is superexponentially small at speed `N`, and equilibrium **carrier** heat can be subextensive. The loaded mean-current task has a different exact cost lower bound. Whether the complete apparatus improves a useful task depends on paid sensing, local communication, real extra-carrier geometry, and the actual full-path receiver; none is replaced by the heat estimate.
