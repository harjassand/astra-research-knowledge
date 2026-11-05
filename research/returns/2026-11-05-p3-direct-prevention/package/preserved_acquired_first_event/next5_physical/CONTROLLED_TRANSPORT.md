# Active forcing cannot supply a missing transport-tail certificate

## Status, chosen question, and earned consequence

**Question.** Can arbitrary causal mechanical forcing at the observed current's conjugate port replace an independently supplied relaxation, visibility, or model-completeness certificate when estimating a macroscopic equilibrium transport coefficient?

**Answer at the declared access.** No. Even positive-temperature, stable, passive linear mechanics with bounded mass eigenvalues admits an arbitrarily large Green–Kubo coefficient whose entire controlled observation record is arbitrarily close to that of a unit-mobility reference. The statement includes controllers using the complete noiseless current history, arbitrary classical computation, and locally finite adaptive stopping. It prices both time and squared-force effort.

The governing new bound is

\[
D_{\rm KL}(P_{a,M}^{\rm record}\Vert P_0^{\rm record})
\le a(1+T)+a^2ET^2,\qquad
\int_0^T u_t^2\,dt\le E,                              \tag{1}
\]

where \(K_{a,M}=M\), \(K_0=1\), \(0<a\le1/4\), and \(M\ge2\). For a peak-force bound \(|u_t|\le U\), this becomes

\[
D_{\rm KL}\le a(1+T)+U^2a^2T^3.                       \tag{2}
\]

The complementary positive construction earns the cubic active-visibility scale in (2): a single finite-slew trapezoid and two endpoint position measurements distinguish a **specified** alternative from the reference with error \(\delta\) when \(U^2a^2T^3\) is sufficiently large and \(aT\le1\). It can expose a specified weak mode much sooner than that mode relaxes. Detecting one specified mode does not certify that a still weaker, slower mode is absent.

This is a completed theoretical boundary and a conditional finite-interface diagnostic, not a universal transport predictor or a manufactured physical device. It is an independent companion to the acquired first-event work. Historical firstness against the general system-identification literature is not established.

## 1. Governing premises and relation to preserved work

The earlier passive result is preserved without edits:

- [Original passive transport theorem](../preserved_first_event/preserved_correlated_reliability/independent_routes/next3_observational/transport_no_go.md).
- [Earlier fixed-mechanics thermal-port construction](../preserved_first_event/next4_physical/01_FIXED_MECHANICS_THERMAL_PORT.md).

The passive construction already supplied the reversible two-coordinate family, its transport identity, exact passive path divergence, and the passive uniform-confidence and stopping obstructions. The present contribution is the **all-causal conjugate-force extension**, the hidden-coordinate comparison that removes an artificial inverse-slow-rate cost, the explicit active testing lower bound, and its finite-slew achieved scale.

The thermal-port work addressed a different question: indistinguishable baths under fixed observable mechanics. The present family changes the mechanics slightly, has one equilibrium temperature, and addresses statistical invisibility of an integrated response. It does not strengthen or replace the fixed-mechanics thermal claim.

We assume the stated Markov Langevin model is exact. The lower theorem grants an ideal continuous scalar-current observation and exact equilibrium velocity initialization. It supplies neither the hidden coordinate nor the generator. It does not cover interventions that directly prepare, measure, pin, or actuate the hidden coordinate; alteration of the mass matrix or friction; controlled bath temperatures; or a microscopic generator known independently. For a supplied exact generator, the target is an ordinary matrix inverse.

The positive diagnostic additionally assumes calibrated finite force, timing, and detector interfaces, a supplied equilibrium source, and the two candidate models. Their manufacture and calibration are premises, with separate costs. No assertion about a particular material follows from fitting its finite record to this model family.

## 2. Passive mechanics with a genuine conjugate force

Set the thermal energy and a reference fast relaxation rate to one. For

\[
a=\rho^2\in(0,1/4],\qquad
\lambda=\frac a{M-1},\quad M\ge2,
\]

define

\[
\Sigma=\begin{pmatrix}1&\rho\\ \rho&1\end{pmatrix},
\quad Q=\operatorname{diag}(1,\lambda),
\quad A=Q\Sigma^{-1},\quad c=\Sigma e_1 .
\]

The observed current is the first velocity \(J_t=e_1^TZ_t\), and the permitted force \(u_t\) acts as

\[
dZ_t=(-AZ_t+c\,u_t)\,dt+\sqrt{2Q}\,dW_t,\qquad
Z_0\sim N(0,\Sigma).                                  \tag{3}
\]

The force coupling \(c\) is derived from canonical mechanics; it is not an arbitrary hidden intervention. Let

\[
H(p)=\tfrac12p^T\Sigma p,\quad
\Gamma=\Sigma^{-1}Q\Sigma^{-1},\quad
dp=(-\Gamma\Sigma p+e_1u)\,dt+\sqrt{2\Gamma}\,dW,
\quad dq=\Sigma p\,dt .                               \tag{4}
\]

Then \(Z=\Sigma p\) gives (3), up to an orthogonal representation of the Brownian noise. The mechanical input work is

\[
W=\int u_t\,dq_{1,t}=\int u_tJ_t\,dt.
\]

The mass matrix is \(\Sigma^{-1}\), with eigenvalues in \([2/3,2]\). Friction is positive definite. The unforced velocity process satisfies

\[
A\Sigma=Q=\Sigma A^T,
\]

so it is stable, reversible, and has the stated invariant Gaussian law. Every rate is strictly positive. There is no active gain, negative damping, infinite mass, or truly nonergodic mode. No common positive lower bound on the slow friction or relaxation rate is assumed.

Position is a relative free coordinate; a stationary position law on the real line is unnecessary. A periodic coordinate with recorded winding gives the same local velocity and unwrapped-displacement operation. The positive readout below separately supplies a bounded initial-position fiducial.

At zero force,

\[
C(t)=E[J_tJ_0]=e_1^Te^{-At}\Sigma e_1,\qquad
K=\int_0^\infty C(t)\,dt
=e_1^T\Sigma Q^{-1}\Sigma e_1
=1+\frac a\lambda=M.                                 \tag{5}
\]

The same \(C(t)\) is the impulse response from conjugate force to mean velocity. Thus \(K\) is both the Green–Kubo integral and the steady zero-frequency mobility. The model is linear for the full applied-force range; this is a supplied constitutive assumption.

All alternatives have

\[
C(0)=1,\qquad C'(0+)=-1,\qquad [J]_t=2t.
\]

In particular, perfect continuous observation cannot distinguish them by instantaneous quadratic variation. The reference scalar process is

\[
dJ_t=(-J_t+u_t)\,dt+\sqrt2\,dW_t,\quad J_0\sim N(0,1),
\qquad K_0=1.                                        \tag{6}
\]

For every nonzero \(\rho\), the stable current response in (3) is a controllable and observable two-dimensional realization:

\[
\det[c,Ac]=-\rho,\qquad
\det\begin{pmatrix}e_1^T\\e_1^TA\end{pmatrix}
=-\frac{\rho}{1-a}.                                  \tag{7}
\]

These determinants approach zero. Qualitative controllability and observability alone do not supply a quantitative acquisition margin.

## 3. Access, controller, and record

A controller may use the entire current history, its integrated position, a common independent random seed, unlimited classical memory, and any causal computation. It outputs an adapted force. The controlled equations must be well posed and nonexplosive. Initially assume the pathwise budget

\[
\int_0^T u_t^2dt\le E.                                \tag{8}
\]

Peak and slew bounds may be added; they only restrict the controller class. The record may include force readback, positions, work, stopping flags, and every output calculated from the current and the controller seed. Independent detector noise, finite sampling, finite bit storage, or compression are additional common channels. The strongest record is already covered by observing the whole current path and seed.

The theorem is for this force port. A force applied directly to a hidden coordinate, or preparation of a hidden velocity, would be a different access model.

## 4. The controlled trajectory information bound

### 4.1 A reference extension that preserves the actual reference record

A direct comparison with an unforced hidden reference coordinate would charge the alternative's hidden forcing by \(aE/\lambda=(M-1)E\). That is an artifact of an unobserved comparison coordinate.

Instead extend the physical scalar reference (6) by the mathematical hidden process

\[
d\widetilde Z_t=(-Q\widetilde Z_t+c\,u_t)\,dt
                    +\sqrt{2Q}\,dW_t,
\qquad\widetilde Z_0\sim N(0,I).                        \tag{9}
\]

Its first coordinate is precisely (6); its second coordinate does not feed back into that first coordinate. Consequently its observable controlled record is the same fixed reference law for every \(a,\lambda\). The hidden force \(\rho u\) in (9) is **only a comparison extension**. It is not an additional physical resource granted to the experiment.

The full processes (3) and (9) now have identical input terms and diffusion. The common causal feedback cancels in their drift difference. Let

\[
B=Q^{1/2}(\Sigma^{-1}-I).
\]

The initial relative entropy is \(-\frac12\log(1-a)\). A same-diffusion change of drift, followed by data processing, gives

\[
D_{\rm KL}(P_{a,M}^{\rm record}\Vert P_0^{\rm record})
\le -\tfrac12\log(1-a)
  +\tfrac14E_{a,M}\int_0^T\|BZ_t\|^2dt.               \tag{10}
\]

For arbitrary admissible feedback, one may first stop the drift difference on bounded-state events, apply the exponential likelihood there, and then remove the stops. The finite energy bound below, nonexplosion, and lower semicontinuity give (10). This argument does not assume an unverified global Novikov condition for arbitrary observation durations.

### 4.2 Stationary and controlled parts

Using the same initial velocity and noise, write pathwise

\[
Z_t=Z_t^0+\int_0^t e^{-A(t-s)}c\,u_sds,                \tag{11}
\]

where \(Z^0\) is the stationary unforced process. The force may depend on \(Z^0\); independence is not used.

The stationary term satisfies

\[
E\|BZ_t^0\|^2
=\operatorname{tr}\{Q(\Sigma^{-1}-2I+\Sigma)\}
=\frac{(1+\lambda)a}{1-a}
\le\frac53a.                                         \tag{12}
\]

For the response kernel, reversibility gives

\[
Be^{-At}c=Q^{1/2}(I-\Sigma)e^{-A^Tt}e_1.
\]

Write \(w=e^{-A^Tt}e_1\). Since the diagonal semigroup entry is the corresponding diagonal entry of a symmetric positive contraction, \(0\le w_1\le1\). If

\[
d=\sqrt{(1-\lambda)^2+4a\lambda},\qquad
r_\pm=\frac{1+\lambda\pm d}{2(1-a)},
\]

then

\[
w_2=\frac{\rho}{d}(e^{-r_-t}-e^{-r_+t})
\le\frac{\rho}{1-\lambda}\le\frac43\rho.
\]

It follows that

\[
\|Be^{-At}c\|^2=a w_2^2+\lambda a w_1^2
\le\frac{16}{9}a^2+\lambda a
\le\frac{25}{9}a^2<4a^2.                              \tag{13}
\]

Cauchy–Schwarz and (8) yield

\[
\left\|\int_0^t Be^{-A(t-s)}c\,u_sds\right\|^2
\le4a^2tE.
\]

Apply \(\|x+y\|^2\le2\|x\|^2+2\|y\|^2\) in (11), integrate, and substitute in (10):

\[
D_{\rm KL}
\le\frac23a+\frac56aT+a^2ET^2
\le a(1+T)+a^2ET^2.                                  \tag{14}
\]

This proves (1). With \(E\le U^2T\), it proves (2). Random controller seeds can be conditioned on and averaged; the same bound holds.

Pinsker's inequality supplies

\[
\|P_{a,M}^{\rm record}-P_0^{\rm record}\|_{\rm TV}
\le\sqrt{\frac{a(1+T)+a^2ET^2}{2}}.                   \tag{15}
\]

For every finite \(T,E\), every \(M\ge2\), and every \(\varepsilon>0\), choosing sufficiently small positive \(a\) makes this at most \(\varepsilon\), while \(K=M\) exactly.

### 4.3 Repeated experiments and parallel access

For \(m\) independently initialized runs, possibly chosen adaptively from previous results, entropy conditions and adds. If run \(i\) has deterministic horizon bound \(T_i\) and pathwise effort bound \(E_i\), then

\[
D_{\rm KL}^{\rm joint}
\le a\!\left(m+\sum_iT_i\right)+a^2\sum_iE_iT_i^2.     \tag{16}
\]

Each additional exact equilibrium start is charged. A finite parallel array is covered by the same sum. Adaptive requests for new copies are covered after capping their count. There is no free unlimited ensemble in the no-go theorem or positive diagnostic.

## 5. Consequences for transport certification and testing

### 5.1 Uniform upper confidence must be infinite at the reference

Let \(V\in[0,\infty]\) be an upper confidence bound computed at finite \(T,E\), with

\[
P_\theta(K_\theta\le V)\ge1-\alpha
\]

uniformly over the reference and alternatives. For any fixed \(M\ge2\), (15) and coverage give \(P_0(V<M)\le\alpha+\varepsilon\). Send \(a\downarrow0\), then \(M\uparrow\infty\). Therefore

\[
\boxed{P_0(V=\infty)\ge1-\alpha.}                      \tag{17}
\]

Arbitrarily capable adaptive forcing cannot create a uniform finite upper certificate from this access and model class.

### 5.2 Adaptive stopping does not remove the missing premise

Suppose a protocol stops at \(\tau\), announces \(V_\tau\), and satisfies

\[
P_\theta(\tau<\infty,\ V_\tau<K_\theta)\le\alpha
\]

uniformly. Assume its force effort is almost surely finite on every finite interval. Localize to an event with \(\tau\le n\), \(V_\tau\le n\), and effort at most \(n\). Cap the controller at a slightly larger effort and set force to zero after it stops. An alternative with \(M>n\) and sufficiently small \(a\) has the same capped record up to arbitrarily small TV error. Thus each such localized event has reference probability at most \(\alpha\). Taking an increasing union yields

\[
\boxed{P_0(\tau<\infty,\ V_\tau<\infty)\le\alpha.}       \tag{18}
\]

The protocol may instead run forever or return an infinite interval. Divergent force effort in finite time falls outside the physical access and the theorem.

### 5.3 Exact model-order qualification

The fixed reference has minimal stable velocity-response order **one**. The alternatives have order **two**. Thus (17)–(18) apply to a class permitting the reference and arbitrarily weak second modes, for example a certified upper order bound of two. They must not be cited as a fixed-reference stopping impossibility for a class separately certified to have exact minimal order two.

Within the exact-order-two class, take one family with \(K=2\) and another with \(K=M\), both with the same small \(a>0\). Each controlled record approaches the same unit-OU reference. The triangle inequality then gives arbitrarily small distance between them at every fixed finite \(T,E\). Hence no **uniform fixed-budget** estimator separates these transports even within minimal order two. This does not rule out pointwise terminating sequential identification when exact minimal order two and the constitutive family are supplied.

### 5.4 An information lower bound for detecting a specified alternative

If a test distinguishes a specified alternative and reference with both errors at most \(\delta<1/2\), binary data processing gives

\[
D_{\rm KL}\ge
k_\delta=(1-2\delta)\log\frac{1-\delta}{\delta}.
\]

Consequently every causal peak-\(U\) controller must satisfy

\[
a(1+T)+U^2a^2T^3\ge k_\delta.                         \tag{19}
\]

When \(a(1+T)\le k_\delta/2\), this implies

\[
T\ge\left(\frac{k_\delta}{2U^2a^2}\right)^{1/3}.        \tag{20}
\]

The lower bound is not limited to deterministic, constant, or sinusoidal input.

## 6. A finite-slew pulse attains the active visibility scale

We now test the **declared pair** (3) and (6). The two candidate parameter sets are supplied, while their actual identity is unknown. This is a model test, not parameter learning over an unspecified family.

Take a trapezoidal force: ramp linearly from zero to \(U\) over \(h\), hold until \(T-h\), and ramp to zero over the last \(h\). It has peak \(U\), slew \(U/h\) almost everywhere, and exact effort

\[
E=U^2(T-4h/3).                                       \tag{21}
\]

No bound on the derivative of the slew is imposed; it is permitted to change at the corners. If that derivative is bounded too, round the corners and charge their uniform force error using Section 7.

Observe only

\[
D_T=q_1(T)-q_1(0)=\int_0^T J_tdt.
\]

Under either candidate, this is Gaussian for the nominal deterministic force.

### 6.1 Positive spectral weights and quantitative separation

The equilibrium covariance is

\[
C(t)=(1-w_-)e^{-r_+t}+w_-e^{-r_-t},\qquad
w_-=\frac{r_+-1}{r_+-r_-}.                            \tag{22}
\]

For \(0<\lambda\le a\le1/4\),

\[
a\le w_-\le2a,\qquad r_-\le\lambda\le a,\qquad
1\le r_+\le1+2a,\qquad r_+-r_-\ge1.                  \tag{23}
\]

To verify these constants, the characteristic polynomial is
\(f(r)=(1-a)r^2-(1+\lambda)r+\lambda\).
It obeys \(f(1)=-a\), \(f(\lambda)=-a\lambda^2\), and
\(f(1+2a)=a(1-2\lambda-4a^2)>0\).
The gap bound follows from \(d\ge1-\lambda\ge1-a\).
For the lower weight bound, rewrite it as
\((1-a)r_++ar_-\ge1\), which follows from
\((1-a)(r_++r_-)=1+\lambda\) and
\(\lambda\ge(1-2a)r_-\).
The upper weight bound then follows from \(r_+-1\le2a\) and gap at least one.

The mean spectral rate is one, so Jensen's inequality implies \(C(t)\ge e^{-t}\) for every \(t\). More explicitly,

\[
C(t)-e^{-t}
\ge a\{e^{-at}-(1+2t)e^{-t}\}.
\]

For \(4\le t\le1/(2a)\), the bracket is at least
\(e^{-1/2}-9e^{-4}>1/4\). Also \(C(t)\le e^{-t}+2a\).

Let \(\Delta m\) denote the alternative minus reference mean displacement. Positivity allows restriction of the response integral:

\[
\Delta m
=\int_0^T u(s)\int_0^{T-s}(C(v)-e^{-v})\,dv\,ds
\ge\frac{UaT^2}{64},                                \tag{24}
\]

provided

\[
T\ge\max(16,4h),\qquad aT\le1.                        \tag{25}
\]

Indeed, use \(s\in[h,T/2]\), where the force is \(U\), and \(v\in[4,T/2]\). Both intervals have length at least \(T/4\), and the covariance difference is at least \(a/4\).

Under either candidate,

\[
v_i(T)=\operatorname{Var}(D_T)
=2\int_0^T(T-t)C_i(t)\,dt
\le2T+2aT^2\le4T.                                    \tag{26}
\]

The midpoint-of-means test therefore has each error at most

\[
\boxed{\exp\!\left[-\frac{U^2a^2T^3}{131072}\right].}  \tag{27}
\]

For fixed target error and \(a\downarrow0\), this achieves
\(T=O(U^{-2/3}a^{-2/3})\), matching (20) in power when the ramp duration is subordinate. Constants are conservative; no full optimal-constant or all-regime minimax result is claimed.

The slow relaxation time is approximately \((M-1)/a\). Therefore a specified weak mode can be detected well before it relaxes. The experiment detects its response amplitude. It does not exclude smaller amplitudes with still longer relaxation times.

## 7. Finite receivers, timing, force accuracy, and mechanical work

The following finite interface suffices. It is a stated interface specification, not a derived microscopic detector or actuator.

### 7.1 Initialization and endpoint readout

At time \(-2d_t\), supply a velocity in its true equilibrium law and a position within \(q_{\max}\) of a fiducial. Apply no force before zero. The first position gate lies in \([-2d_t,0]\); the second lies in \([T,T+2d_t]\). A gate may average position with nonnegative normalized weights. Its timing and integration support are contained in those windows.

Each readout has independent zero-mean Gaussian detector error of variance \(\sigma^2\). The sum of the absolute endpoint bias bounds is \(b\). Quantization step \(\Delta\) contributes at most \(\Delta\) to their difference. Each receiver has finite analog range \([-L,L]\) about the fiducial and declares saturation. Gaussian detector errors are an explicit calibrated noise model; adversarial unbounded readout noise is not covered.

Suppose actual force is zero outside \([0,T]\), and throughout the pulse
\[
|u_{\rm actual}(t)-u(t)|\le e_F.
\]
This envelope may hold for causal force errors. Positivity of \(C_i\) bounds the resulting displacement deviation by
\[
d_F\le e_Fv_{\max}/2,\qquad v_{\max}=\max_i v_i(T).
\]
The remaining nominal displacement is the Gaussian variable above, so random force error need not preserve Gaussianity.

Let \(\mathcal I\) be the sum of the integrals of \(|J|\) over both endpoint windows. It bounds the timing/gate contribution to displacement error. Stationary current variance is one, and its controlled mean is bounded by
\((U+e_F)[1+2a(T+2d_t)]\) after the pulse. Thus

\[
E\mathcal I\le
2d_t\{2+(U+e_F)[1+2a(T+2d_t)]\}.                     \tag{28}
\]

For a timing allowance \(d_g>0\), Markov's inequality gives a failure probability
\[
\beta_g=\frac{2d_t\{2+(U+e_F)[1+2a(T+2d_t)]\}}{d_g}.  \tag{29}
\]

If the midpoint threshold is represented to error \(d_{\rm num}\), the bounded offset on the good event is
\[
d_*=\frac{e_Fv_{\max}}2+b+\Delta+d_g+d_{\rm num}.       \tag{30}
\]
The two independent detector noises add \(2\sigma^2\) to variance. If \(\Delta m/2>d_*\), each decision error is at most

\[
\beta_g+\beta_{\rm sat}
+\exp\!\left[
-\frac{(\Delta m/2-d_*)^2}{2(v_{\max}+2\sigma^2)}
\right].                                             \tag{31}
\]

One sufficient saturation bound is

\[
\beta_{\rm sat}\le4\exp\!\left[
-\frac{(L-m_{\max}-d_F-q_{\max}-d_g-b-\Delta)^2}
          {2(v_{\max}+2\sigma^2)}
\right],                                             \tag{32}
\]

when its numerator margin is positive. Here \(m_{\max}\) is the larger absolute nominal displacement mean. On the good timing event, the initial lead-in displacement and final gate displacement are both bounded by \(\mathcal I\). This is why a bounded initial position at the start of the lead-in suffices; an exactly known position at time zero is unnecessary.

### 7.2 Timing and analog waveform bill

A piecewise linear analog ramp with a hold segment supplies finite slew. A digital sequence of ideal instantaneous force jumps would not meet this interface. An actuator clock, analog ramp/hold precision, force readback calibration, and propagation delay must jointly establish the uniform force envelope.

For the explicit example, a sufficient allocation is a total phase-error envelope of \(5\times10^{-6}\) time units and analog force error at most \(5\times10^{-5}\): with nominal slew 10, their sum is at most \(e_F=10^{-4}\). The actual force port also guarantees slew at most 10.001; this derivative guarantee is additional to the amplitude-error envelope. Guarding the pulse outside \([0,T]\) is part of the supplied force-port interface. A timer with tick \(5\times10^{-6}\) needs 28 counter bits over \(T=800\), and services \(1.6\times10^8\) ticks. A counter does not establish timebase accuracy: the stated total phase envelope includes accumulated drift and synchronization error. Calibration of that envelope is a separate paid premise. A slew bound is not a hard spectral passband or a microscopic actuator construction.

Readout-gate timing has its separate \(d_t\) envelope. Two detector-service intervals of 0.01 and the gate windows give a conservative wall-time allowance \(T+4d_t+0.02\), excluding source and instrument preparation. The first conversion can run during the pulse.

### 7.3 Work and finite reserve

For the nominal deterministic nonnegative pulse,
\[
m_{W,i}=\int_0^T u(t)\int_0^t C_i(t-s)u(s)\,ds\,dt,
\qquad \operatorname{Var}(W_i)=2m_{W,i}.              \tag{33}
\]
This follows from the response kernel and the stationary covariance, and prices net mechanical work.

To cover a bounded causal force error and avoid relying on regenerative energy recovery, use cumulative absolute work. Since \(E|J^0|\le1\), a sufficient expectation bound is

\[
E\int_0^T|u_{\rm actual}J_{\rm actual}|dt
\le m_{W,i}+e_F|m_i|
+e_F(U+e_F)v_i/2+U(T-h)+e_FT.                        \tag{34}
\]

A mechanical work reserve \(B_W\), with depletion reported as an abort, adds at most the right side of (34) divided by \(B_W\) to the error probability. Couple the full-reserve and capped-reserve systems until depletion to justify this bound. The port must actually enforce the finite reserve or supply its depletion flag; the endpoint measurements alone do not monitor cumulative work.

Controller electronics, sensing, force-generation dissipation, source preparation, instrument calibration, and the physical bath are additional costs. Equations (21), (28)–(34) do not declare them free. Without the supplied calibrated interfaces, this file does not provide an instrument factory.

## 8. Executed finite instance and its bill

The analytic formulas and a directed-rounding certificate were executed for

\[
a=10^{-4},\quad M=1000,\quad
\lambda=10^{-4}/999,\quad U=10,\quad h=1,\quad T=800.
\]

The slow time is approximately \(9{,}990{,}000.0001\) time units. No SI interpretation is imposed; thermal energy and the fast relaxation rate are the chosen units.

| Quantity | Reference | Specified alternative |
|---|---:|---:|
| Transport coefficient | 1 | 1000 |
| Mean displacement | 7983.6787944 | 8301.6745727 |
| Displacement variance | 1598 | 1661.6789204 |
| Mean nominal mechanical work | 79793.0907784 | 82969.0629260 |
| Nominal Gaussian decision error, including meter noise | \(3.48543\times10^{-5}\) | \(4.80307\times10^{-5}\) |

The threshold is the finite decimal **8142.67668356**, within \(10^{-8}\) of the exact midpoint. The mean separation is between 317.99577828 and 317.99577830.

The finite interface uses per-reading noise \(\sigma=0.25\), quantization step 0.01, total endpoint bias 0.01, \(e_F=10^{-4}\), \(d_t=10^{-4}\), timing displacement allowance \(d_g=1\), position fiducial radius \(q_{\max}=1\), and analog range \([-12000,12000]\). Each position result requires 22 bits; two results require 44 bits, plus saturation/abort flags. The finer arithmetic threshold may be compiled once to the corresponding ADC comparison threshold.

The nominal squared-force effort is \(79{,}866.666667\), and including the force error it is at most \(79{,}868.264675\). Nominal peak force and slew are both 10; actual peak is at most 10.0001 and actual slew at most 10.001 under the interface contract. The finite meter/force error bound is less than **0.003273**. The conservative expected absolute-work upper bound, including the bounded force error, is less than 90,961. A reserve of \(10^8\) mechanical energy units adds less than 0.000910 to the failure budget. The complete stated bound, counting reserve abort, is less than **0.004183**. Electronics and other overhead are not included in that mechanical reserve.

The pulse and detector wall-time bound is **800.0204** time units. Native equilibrium velocity and bounded-position initialization are supplied. Generic relaxation preparation from an arbitrary velocity can scale with the roughly ten-million-unit slow time, and is not supplied by the 800-unit pulse. Copy manufacture and source equilibration are not simulated.

Grant the passive observer the full conservative 800.0204-unit wall time as noiseless continuous current observation. For the same pair, the original exact full-path divergence gives
\[
D_{\rm passive}\le0.02005252,\qquad
\mathrm{TV}\le0.100132.
\]
Every passive test then has maximum error at least **0.449934**. This is a same-source/time comparison with a deliberately added active force resource; it is not a claim that active and passive experiments have equal total cost.

At the same inclusive 800.0204-unit time and actual-force effort allowance, choose instead \(a=10^{-10}\), \(M=10^9\). Equation (15) gives record TV below **0.000201** for every causal force controller in the budget. The directed-rounding certificate includes the increased actual-force effort. This alternative is only a theoretical indistinguishability witness, not a generated physical specimen.

### What was executed

- [Audit program](audit_controlled_transport.py): symbolic Lyapunov, physical-noise, transport, controllability, observability, and stationary divergence identities; 240 sampled kernel inequalities; 80-digit pulse evaluation.
- [Audit output](audit_results.json): exact-model quantities and scope metadata.
- [Directed-rounding certificate](certify_endpoint.py): 100-significant-digit interval arithmetic. Ordinary operations round outward; correctly rounded Decimal exponential, logarithm, and square root are expanded to adjacent representable values. Under the documented arithmetic contract, this encloses the finite error bounds and checks the stated threshold, reserve, passive comparison, and hidden-alternative bound.
- [Certificate output](endpoint_certificate.json): all numerical enclosures.

The audit also generated 100,000 independent scalar Gaussian endpoint statistics per hypothesis, with seed 2026110505, then quantized them. It observed 1 and 6 misclassifications respectively. It quantizes the already-subtracted scalar statistic once; the two separate endpoint ADCs are covered by the deterministic quantization allowance in the certificate and were not simulated. These are synthetic draws of the exact-model endpoint statistic, not full SDE simulations, hardware trials, detector calibration, or evidence that the confidence guarantee holds for natural materials. The analytic argument and interval calculation govern the error claim.

The audit's measured execution time was about 0.22 seconds on this environment; that is classical arithmetic time, not experimental exposure or device manufacture. Runtime versions are in [execution_environment.json](execution_environment.json). The certificate uses finitely many operations on 100-digit numbers; its software arithmetic contract is explicit. No computer-assisted claim depends on the Monte Carlo error rate.

## 9. Comparison with strong applicable approaches

The result should not be compared with an artificially weak estimator.

**Finite input/output system identification.** Sarkar, Rakhlin, and Dahleh construct finite-data identification and data-dependent order selection for stable LTI systems with unknown latent order, learning the lower-order approximation supported by the data [1]. That is directly relevant machinery. A good finite-horizon or finite-data approximation does not by itself supply a uniform upper bound on an integrated zero-frequency response contributed by an unresolved weak pole. Equations (14)–(18) identify that specific endpoint obstruction within a passive mechanical family. They do not refute their finite-data approximation theorem or claim that model order must always be known in advance.

**Optimal active excitation.** Wagenmaker and Jamieson give finite-time and asymptotically optimal active input design under an energy constraint while observing the full state [2]. Our experiment sees only one current. Their stronger observation and quantitative identification task are not silently removed in this comparison. Equation (19) is specific to the declared conjugate-port/current interface.

**Learning without waiting for mixing.** Simchowitz and collaborators prove finite-time full-state learning bounds that avoid a generic mixing-time requirement [3]. The positive pulse here also demonstrates why “one must always wait for the slow relaxation time” is too strong. The negative result is about uniform upper certification of an unresolved integrated tail, not a universal inverse-gap lower bound for every parameter-learning problem.

**Modern transport estimators.** Frequency-domain correlation estimators address practical bias/variance and trajectory-length issues, while transient-subtraction methods use a perturbed initial ensemble together with a coupled equilibrium trajectory to reduce variance [4,5]. Those methods remain applicable where their model, initial-state, coupling, and error assumptions hold. A known microscopic generator or synchronously coupled trajectories is additional access beyond this current-and-force experiment. Our construction does not establish that they are inefficient, and it does not supply a cheaper universal replacement.

**Earlier Astra results.** The passive transport impossibility was already earned. The new substantive change is that adaptive feedback through the actual conjugate port cannot repair its missing uniform tail certificate at any finite force budget, while a specified mode admits a constructive active advantage. Broad active thermal-port nonidentifiability and thermal-pulse identification were also already present; this file does not rename them as new results.

The consequence is a precise boundary for an acquired transport claim: finite active current evidence can establish a particular mechanistic contrast, but an honest upper bound on unobserved DC transport still needs a supplied quantitative closure condition or stronger access. Qualitative stability, bounded masses, controllability, observability, excellent finite-data fit, and adaptive excitation are insufficient together.

## 10. Useful failed attempts and retained limits

1. **Direct hidden-coordinate comparison.** Comparing physical null and alternative with their different hidden input coefficients creates \(aE/\lambda\) in a full-path divergence. This does not prove observed distinguishability; it charges an unobserved response. The extension (9) fixes the comparison while preserving the actual null record.

2. **Reusing thermal-port ambiguity.** A fixed-mechanics bath construction would answer a different question and overlap accepted results. It was not presented as the new mechanism.

3. **Using qualitative minimality as a margin.** Equation (7) proves exact controllability and observability, but their determinants vanish. This is insufficient for uniform inference. The separate order-one/order-two stopping qualification is essential.

4. **Calling a specified-pair pulse a transport estimator.** The positive pulse assumes two known candidate responses and identifies their label. It cannot certify an arbitrary unknown relaxation rate or the absence of additional slow modes.

5. **Charging only pulse time.** Native equilibrium preparation may dominate by an inverse slow rate. The positive construction takes a source as supplied and explicitly leaves its manufacture, equilibration, calibration, and clock acquisition costs outside the pulse bill.

6. **Inferring precision from a digital counter.** A 28-bit timer stores the requested duration; it does not establish the total phase accuracy. That calibration is an independent supplied interface condition.

7. **Using Gaussian synthetic draws as physical execution.** The executed draws check the statistic and threshold path. They do not execute the bath, force mechanism, receiver, initial state, or source.

8. **Overstating the impossibility.** Full-state access, direct hidden actuation, known generator, a certified exact constitutive family with quantitative margins, a lower relaxation bound, or another proved tail envelope can change the conclusion. Arbitrarily small individual rates are allowed here; no statement says every real material has them.

## References and provenance

[1] Tuhin Sarkar, Alexander Rakhlin, Munther A. Dahleh, *Finite Time LTI System Identification*, Journal of Machine Learning Research 22 (2021), 1–61.
https://jmlr.org/papers/volume22/19-725/19-725.pdf

[2] Andrew Wagenmaker, Kevin Jamieson, *Active Learning for Identification of Linear Dynamical Systems*, COLT/PMLR 125 (2020).
https://proceedings.mlr.press/v125/wagenmaker20a/wagenmaker20a.pdf

[3] Max Simchowitz et al., *Learning Without Mixing: Towards a Sharp Analysis of Linear System Identification*, COLT/PMLR 75 (2018).
https://proceedings.mlr.press/v75/simchowitz18a/simchowitz18a.pdf

[4] Toraman, Fauconnier, Verstraelen, *STACIE* transport-estimation study, Journal of Chemical Information and Modeling 65(19) (2025), 10445–10464; DOI 10.1021/acs.jcim.5c01475.
https://pmc.ncbi.nlm.nih.gov/articles/PMC12529779/

[5] Pierre Monmarché, Renato Spacek, Gabriel Stoltz, *Transient subtraction: A control variate method for computing transport coefficients*, arXiv:2410.00212v3 (2025).
https://arxiv.org/abs/2410.00212v3

[6] Python Decimal arithmetic specification, including correctly rounded elementary functions and directed rounding:
https://docs.python.org/3/library/decimal.html

The original passive and thermal constructions were read directly from the preserved local source files above. The broader Astra public corpus at the previously retrieved revision fef3640a8b1dc5475674a006de417f652f3baf3c was consulted for prior active-port work; an incomplete code-search result is not treated as evidence of historical novelty. The exact earlier source URLs and qualifications remain in the preserved originals.

This directory is a new local research artifact. No prior source was edited and no external publication was made.
