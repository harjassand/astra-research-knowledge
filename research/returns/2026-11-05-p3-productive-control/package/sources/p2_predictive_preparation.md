---
title: "Predictive preparation without equilibration"
subtitle: "A finite operation for unknown passive linear environments"
author: "Research construction and execution record"
date: "5 November 2026"
geometry: margin=0.85in
fontsize: 10pt
colorlinks: true
linkcolor: MidnightBlue
urlcolor: MidnightBlue
toc: true
toc-depth: 1
numbersections: true
---

# Result and scientific status

An unknown passive linear environment can be prepared for prediction without preparing its hidden state, knowing its dimension, bounding its slowest relaxation time, or identifying its microscopic memory kernel. The preparation operation is a private random choice of when to begin. It turns a finite budget of possible visible motion into a finite, probabilistic guarantee for a complete experiment. A finite smooth probe then acquires the input-output response directly. The resulting table predicts every subsequently chosen input in a declared variation budget, on a common finite-horizon event.

This is an operational statement about a particular class and access model. It requires an actual local dissipation inequality, a bound on total initial stored energy, whole-plant linearity and time invariance, a controlled off mode, finite calibrated position metrology, and a private clock independent of the hidden initial state. A permanent spring supplies a known position-energy bound and the actuation interface. Predictions concern that permanently loaded plant. The operation does not certify these premises from a fitted trace.

There is also an obstruction with different quantifiers. The same one-exponential response kernel admits both a dissipative realization and a conservative realization containing delayed incoming disturbances. For the latter, no finite deterministic preparation deadline eliminates the worst-case future uncertainty, even with ideal local observations. Its exact uncertainty radius is computed below. Private random timing escapes that obstruction because the hidden initial state must be fixed before the random clock is drawn.

The endpoint is complete within its stated contracts: finite acquisition, retained-source preparation, finite force programs, a reusable predictor, and a finite robust planning operation. An example carries finite sensor reports through an exact rational predictor and an independently checked polynomial certificate. The simulated source is floating point, and no laboratory prototype is claimed. The theorem is dimension independent in its stated parameters; the total-energy bound can itself scale with hidden volume, and the worst-case waiting and precision costs can be large. Historical priority and a civilisation-changing practical advantage have not been established.

# Selection from independent constructions

The selection did not start by requiring a better fit to the previous Maxwell model. Three independent lines first attempted different complete endpoints.

| Construction | Completed consequence | Decision |
|:--|:--|:--|
| Composing acquired passive modules | A maximum-node trajectory bound for heterogeneous Maxwell modules connected by monotone pairwise springs; finite attachment and initialization; an exact boundary for arbitrary strongly convex coupling | Preserved as a companion. Its comparison principle is established machinery, and it stays inside the positive-memory family. |
| Acquisition for damped oscillatory spectra | A finite operation for sectorial modes with a supplied frequency-to-damping ratio; positive weights, phase-bearing filtered atoms, acquisition and nonlinear comparison | Preserved analytically. The spectral sector is substantive, and the large fitter was not executed. |
| Prediction despite arbitrary hidden preparation | An exact fixed-deadline indistinguishability theorem and minimax radius, followed by a private-random-time escape based on finite dissipation | Selected. It changes preparation and permits conservative, oscillatory and continuum environments without a spectral-sector premise. |

The bridge was built by eliminating an unnecessary operation. Instead of reconstructing a microscopic friction kernel and then releasing a trap, keep a calibrated spring attached, acquire the loaded port's step response, and use linear superposition. The backward requirement is a small free continuation during the future experiment. The forward physical resource is finite total visible dissipation. A private random clock joins these with explicit quantifiers. It does not assume that a short observation reveals the hidden state.

The prior passive bridge and all its opposite-ends constructions remain unchanged in the embedded warm archive. The present result broadens the hidden linear environment but does not replace the prior theorem for a known nonlinear visible law, or the acquired thermal simulator's stochastic feedback interface.

# Physical and mathematical contract

## Loaded port

Let a causal, well-posed LTI system have scalar input force $f$, observable displacement $x$, and velocity $v=\dot x$. It includes every hidden coordinate. There is a nonnegative storage $\mathcal E$ such that

$$
\mathcal E(t)-\mathcal E(s)
\le \int_s^t f(u)v(u)\,du-\Gamma\int_s^t v(u)^2\,du,
\qquad \mathcal E(t)\ge \frac{\mu x(t)^2}{2},
\quad \Gamma,\mu>0.                                      \tag{1}
$$

The zero state is an equilibrium of zero storage. Initial states are arbitrary within a supplied energy ball. Infinite-dimensional realizations are allowed only when dynamics, superposition and (1) are well posed. Displacement is absolutely continuous on finite intervals for the finite-energy inputs used here.

A concrete interface has an arbitrary linear passive bare plant, a calibrated local damper, and a permanent spring of stiffness $k>0$. Program its center as $q=f/k$. The spring force is $k(q-x)=f-kx$. The term $-kx$ belongs to the fixed loaded plant. Its storage $kx^2/2$ supplies $\mu=k$ even when the bare restoring law is unknown. A known extra bare stiffness can improve $\mu$. An optional known mass $M>0$ supplies storage at least $Mv^2/2$, hence finite velocity and damper-reaction bounds. Neither damping nor mass is inferred from bare passivity.

Electrical force-flow analogues obey the same theorem when their actual constitutive laws and storage bounds are supplied. This does not assert that every device has a free calibrated port.

## Access and supplied precision

The experiment controls the local center and observes finite position averages. It does not observe hidden modes, velocity, hidden energy, or bath preparation keys. It has a finite clock, private random bits, bounded-range digitization, and a meter with declared response, bias, noise and backaction. Every actual force includes tracking, calibration, timing and backaction errors in its ledger.

In the primary operation, off mode is a fixed passive center. Common nonzero off leakage is treated below. The unknown initial state is fixed before each private scheduling choice. A disturbance source that learns the choice and then places a pulse at that time is outside this information pattern.

Completing the square in (1) gives

$$
\mathcal E(t)\le\mathcal E(s)+\frac{1}{4\Gamma}\int_s^t f^2,
\qquad
\int_s^t v^2\le\frac{2\mathcal E(s)}{\Gamma}
                 +\frac{1}{\Gamma^2}\int_s^t f^2.           \tag{2}
$$

Every preparation, probe, delay with nonzero force, return ramp and physical reuse therefore has a computable energy update. For nominal force $f_0$ and an $L^2$ error allowance $q_f$,

$$\int f_{\rm actual}^2\le(\|f_0\|_2+q_f)^2.              \tag{3}$$

Storage inequalities and interconnection rules are established dissipativity theory [1]. Input-output data do not uniquely determine all internal storage or initial-state behavior. Here the physical inequality is supplied; it is not inferred from a response fit.

# A deterministic preparation boundary

## One response, two preparation classes

Set $\Gamma=1$ and use an overdamped visible coordinate with restoring coefficient $\mu>0$. The known memory kernel is $K(t)=B e^{-at}$, where $B,a>0$. A single dissipative Maxwell mode realizes it. A conservative realization uses

$$d\nu(\omega)=\frac{2Ba}{\pi(a^2+\omega^2)}\,d\omega,
\qquad\omega\ge0,$$

$$
\dot x=-\mu x-\int r_\omega\,d\nu+f,
\quad\dot r_\omega=\dot x-\omega p_\omega,
\quad\dot p_\omega=\omega r_\omega.
$$

Storage $\mu x^2/2+\tfrac12\int(r^2+p^2)d\nu$ obeys (1). Eliminating the bath gives $\dot x+\mu x+K*\dot x=f+g$. Its free initial-force history can be any real $g\in H^1(\mathbb R)$ with exact initial energy

$$E[g]=\frac{1}{4Ba}\int_{\mathbb R}(g'^2+a^2g^2)dt.       \tag{4}$$

For proof, use $\widehat g(\omega)=\int e^{-i\omega t}g(t)dt$. With $r=d\nu/d\omega$, take cosine and sine amplitudes $\operatorname{Re}\widehat g/(\pi r)$ and $-\operatorname{Im}\widehat g/(\pi r)$. Fourier inversion gives $g$; Plancherel gives (4). Translation preserves the energy.

A smooth pulse can be placed after any finite deadline $H$ at unchanged energy. Opposite pulses yield identical records before $H$ under common causal local controls. This includes continuous noiseless observation. A deterministic stopping rule terminating on the zero-free-force record is covered by placing the pulse after that stop. Randomized controls with a fixed deadline are covered too. Private randomized stopping has a different order of quantifiers.

Conservative extensions and the significance of preparation are established theory [2,3]. The result used here is the explicit finite-access ambiguity and attainable uncertainty calculation, not the existence of conservative dilation.

## Exact attainable uncertainty

Write $g'+ag=\sqrt{2Ba}\,w$, $g(H)=0$, for a future-only force. Equation (4) becomes $E[g]=\|w\|_2^2/2$, including its exponential continuation. The deviation transfer function is

$$\frac{X(s)}{W(s)}=\frac{\sqrt{2Ba}}{s^2+(a+\mu+B)s+a\mu}. \tag{5}$$

Let $h$ be its impulse response. Among energy-at-most-$E$ states consistent with the entire zero-free-force preparation record, the exact minimax path error on the next $T$ is

$$\boxed{R(E,T)=\sqrt{2E}\,\|h\|_{L^2(0,T)}.}              \tag{6}$$

Cauchy-Schwarz proves the upper bound for the nominal prediction. The opposite inputs $w(s)=\pm\sqrt{2E}\,h(T-s)/\|h\|_2$ attain separation $2R$ at $T$. A predictor errs by at least $R$ for one state. A randomized forecast has failure probability at least $1/2$ for one fixed state at each strict threshold below $R$.

For $r_\pm=((a+\mu+B)\pm\sqrt{(a+\mu+B)^2-4a\mu})/2$,

$$h(t)=\frac{\sqrt{2Ba}}{r_+-r_-}(e^{-r_-t}-e^{-r_+t}),
\qquad R(E,T)^2\longrightarrow\frac{2BE}{\mu(a+\mu+B)}.$$

No preceding wait $H$ occurs. Adding a known visible mass preserves the obstruction: replace (5)'s denominator by $(s+a)(Ms^2+s+\mu)+Bs$ and use the corresponding three-state Gramian. The complete proof includes the exact finite-$T$ integral and the energy interpretation of the indistinguishable states.

## Local realization and its size cost

A spring of stiffness $B$ attached to a lossless string of impedance $Z=B/a$ gives the same obstruction. For incoming endpoint wave velocity $v_{\rm in}$,

$$g'+ag=2Bv_{\rm in},\qquad E_{\rm incoming}=Z\int v_{\rm in}^2.$$

A packet arriving during $[H,H+T]$ initially occupies distances between $cH$ and $c(H+T)$ from the port. Local controls cannot reach it before arrival. A finite string long enough to avoid reflection realizes the finite-horizon witness. Its length, mass, tension, packet energy and spatial resolution are resources. The ideal infinite line gives the exact exponential response for all times; the finite line does not.

Finite oscillator approximants are also available. On duration $S$, cutoff $O(a\zeta^{-2})$ and $O(aS\zeta^{-3})$ modes give the stated normalized kernel/force tolerances without increasing initial energy. These are finite-noise approximations, not exact forever-invisible small systems. All constants and constructions are in the independent proof.

# Random timing as predictive preparation

## Finite quiet-window theorem

Fix an initial state with $\mathcal E(0)\le E$ before choosing a private index. Its common counterfactual off trajectory $x_0$ satisfies $\int_0^\infty\dot x_0^2\le E/\Gamma$. Partition time into $N$ disjoint enclosing slots $I_j$ of duration at most $D$, and put $Z_j=\sup_{s,t\in I_j}|x_0(s)-x_0(t)|$. Cauchy-Schwarz gives $Z_j^2\le D\int_{I_j}\dot x_0^2$. For uniform $J$,

$$\mathbb E Z_J^2\le\frac{ED}{\Gamma N},\qquad
\boxed{\Pr(Z_J>\delta)\le\frac{ED}{\Gamma N\delta^2}.}      \tag{7}$$

Choose the next power of two above $ED/(\Gamma\alpha\delta^2)$, or one if this is below one. The operation needs $\log_2N$ private bits, maximum wait plus slot $ND$, and mean selected start $(N-1)D/2$. The slot encloses meter clearing, baseline, the entire experiment, required computation latency and clock guards.

Converting an aggregate budget into a random selected-index bound has established analogues in randomized-iterate optimization [4]. The physical interface here includes a common counterfactual trajectory, the order of choices, metrology, backaction and subsequent all-input prediction.

The selected slot cannot generally be recognized as safe from its prefix. Equation (7) is not conditional on each realized index. It gives a high-probability operation for every fixed admissible initial state. No hidden state is reset and no equilibrium is asserted. The lemma needs only the dissipation budget; linearity is needed later for the reusable response predictor.

## Leakage, backaction and private randomness

For a common off error $|w_0|\le\xi_0$, (2) gives

$$\Pr(Z_J>\delta)\le\frac{2ED}{\Gamma N\delta^2}
+\frac{\xi_0^2D^2}{\Gamma^2\delta^2}.                       \tag{8}$$

Increasing $N$ cannot remove the second term. Off energy $\xi_0^2ND$ is separately charged. A constant bias $f_0$ is different: shifted storage $\mathcal E^\sharp=\mathcal E-f_0x+f_0^2/(2\mu)$ is nonnegative, with derivative at most $-\Gamma v^2$ in that fixed off mode and initial bound $(\sqrt E+|f_0|/\sqrt{2\mu})^2$. A fixed bias changes the energy bound and baseline. Arbitrary time-varying leakage creates (8)'s floor.

Only a common off trajectory independent of the index is averaged. A meter activated in the selected slot can exert index-dependent backaction; its force is separately priced by (11). A clock law within total variation $\beta$ of uniform adds $\beta$ to failure. Predictable pseudorandomness does not supply the theorem's private randomness.

# Acquiring the response without preparing the zero state

## Universal response bounds

Let $S$ be the zero-state position response to the mathematical unit force step, extended by zero before zero. It is a target, not an infinite-slew command. The shifted storage $\mathcal E-S+1/(2\mu)$ is nonnegative, starts at $1/(2\mu)$, and has derivative at most $-\Gamma S'^2$. Also $\mathcal E\le S$ and $\mathcal E\ge\mu S^2/2$. Hence

$$0\le S(t)\le\frac2\mu,\qquad
\int_0^\infty S'^2\le\frac1{2\Gamma\mu},                  \tag{9}$$

$$|S(t)-S(s)|\le\omega(|t-s|),\quad
\omega(u)=\sqrt{\frac{u}{2\Gamma\mu}}.                    \tag{10}$$

No hidden frequency or dimension appears. A known mass gives the conservative alternative $\omega(u)=2u/\sqrt{M\mu}$ because $MS'^2/2\le\mathcal E\le S\le2/\mu$. One can use the smaller modulus. For any zero-state force error $d$, (2) yields

$$\boxed{\|Rd\|_\infty\le\frac{\|d\|_2}{\sqrt{2\Gamma\mu}}.} \tag{11}$$

This prices finite control and backaction without a hidden bandwidth cutoff.

## Smooth probe, finite position records

Let $\phi(s)=10s^3-15s^4+6s^5$ on $[0,1]$, extended by zero and one. Its derivative is a positive normalized kernel $\rho_h(t)=\phi'(t/h)/h$ on $[0,h]$. In a selected quiet slot, take a baseline position box of width $b$, apply $A\phi(t/h)$, and hold through the last data box. Turn off with a separately counted smooth ramp.

The forced response is $A(\rho_h*S)$. The node-$t_i$ box uses $[t_i,t_i+b]$. On the quiet event, baseline subtraction gives nodal error $\delta/A+\omega(h)+\omega(b)$ before meter and force errors. The retained state is handled by superposition, with no physical zero-state preparation.

Each box has deterministic error at most $b_x$ and white readout density $\nu_x$, or an equivalent conditional sub-Gaussian contract. Separated baseline and data-box noise difference has variance proxy $2\nu_x/b$; different data boxes may be correlated. After $R$ repetitions, a union bound over $m$ nonzero averaged nodes gives noise at most

$$\eta_n=\frac1A\sqrt{\frac{4\nu_x\log(2m/\alpha_m)}{Rb}}.  \tag{12}$$

Bias $2b_x/A$ does not average away. For baseline-only backaction budget $q_b$ and later on-minus-off force discrepancy $q_p$, the nodal contribution is $(2q_b+q_p)/(A\sqrt{2\Gamma\mu})$. Timing allowance $\kappa_t$ costs $\omega(\kappa_t)$ for the sample; ramp-delivery errors belong to $q_p$.

Set the zero node to zero, clip other reports to $[0,2/\mu]$, and interpolate linearly with gap at most $\Delta$. Projection cannot enlarge error. With encoding allowance $\eta_{\rm enc}$,

$$\begin{split}
\|\widehat S-S\|_\infty\le\epsilon_S:={}&\delta/A+2b_x/A+\eta_n
+\frac{2q_b+q_p}{A\sqrt{2\Gamma\mu}}+\eta_{\rm enc}\\
&+\omega(h)+\omega(b)+\omega(\kappa_t)+\omega(\Delta).
\end{split}                                                \tag{13}$$

For Lipschitz constant $L_S$, the symmetric ramp and box have mean delays $h/2,b/2$, and interpolation costs $L_S\Delta/2$. The example uses these sharper constants.

## Retained repetitions

After each full probe and off-ramp, update energy using actual force and draw the next clock freshly. $S$ stays fixed while hidden state changes. Choose $N_r$ from its current energy bound so that $\mathbb E[Z_r^2\mid\mathrm{past}]\le\alpha_q\delta^2$. Jensen and Markov give

$$\Pr\left(R^{-1}\sum_{r=1}^R Z_r>\delta\right)\le\alpha_q. \tag{14}$$

This average controls the background at every averaged node, without requiring every repetition separately to be quiet. For imperfect off mode, meet both (8) and a per-cycle force-energy budget, preventing unpriced growth during long waits.

# The acquired arbitrary-input operation

After acquisition and preprocessing, perform fresh randomized preparation. Its selected slot includes the baseline and complete future horizon. Let $\widehat x_0$ be the baseline, $\delta_g$ the free-motion allowance, and $\eta_g$ its meter error. For a causal BV force extended by zero before launch, define $W_f=|f(0+)|+\operatorname{TV}_{(0,T]}(f)$. LTI superposition gives

$$Rf(t)=\int_{[0,t]}S(t-s)df(s).$$

The acquired predictor is $\widetilde x_f(t)=\widehat x_0+\int_{[0,t]}\widehat S(t-s)df(s)$. On the common calibration and preparation event,

$$\boxed{\|x_f-\widetilde x_f\|_\infty
\le\delta_g+\eta_g+W_f\epsilon_S
+\frac{2q_{bg}+q_f}{\sqrt{2\Gamma\mu}}+\epsilon_{\rm num}.} \tag{15}$$

Here $q_{bg}$ is baseline-only backaction, $q_f$ the later actual force discrepancy relative to the common off continuation, and $\epsilon_{\rm num}$ numerical execution error. Do not count a disturbance twice.

The event is simultaneous over all subsequently selected admitted preprogrammed inputs. A program may depend on acquired data and the fresh baseline if computation fits inside the slot. There is no union bound over programs. Counterfactual queries about this prepared hypothetical state reuse the event. Actual physical deployment changes state; another needs an energy update, fresh preparation and confidence allocation.

General future measurement-feedback policies require a separate closed-loop comparison and finite controller interface. The earlier thermal simulator has a different arbitrary-feedback encoded-record guarantee. If an intended force has jumps, deliver $f_a=\rho_a*f$ and add $W_f\omega(a)$ when comparing with the ideal unsmoothed command. If the query itself is smooth, evaluate it directly and add no ideal-jump error. An arbitrary BV function is not a computation oracle: its finite representation or validated evaluation procedure must be supplied.

# Complete physical resource law

## Waiting, exposure and precision

For target response error $\epsilon$, one sufficient general allocation is

$$h,b,\Delta,\kappa_t=O(\Gamma\mu\epsilon^2),\quad
\delta=O(A\epsilon),\quad
m=O\!\left(1+\frac{T}{\Gamma\mu\epsilon^2}\right),$$

$$R=O\!\left(1+\frac{\nu_x\log(2m/\alpha_m)}{A^2\Gamma\mu\epsilon^4}\right).
                                                               \tag{16}$$

Constants allocate every term in (13). These are sufficient scales, not optimized costs or matching lower bounds. With known mass, the Lipschitz modulus gives $m=O(1+TL_S/\epsilon)$ and $R=O(1+\nu_xL_S\log(2m/\alpha_m)/(A^2\epsilon^3))$.

For slot length $D$, exact off mode and quiet failure $\alpha_q$, the repetition-$r$ wait is of order $E_rD^2/(\Gamma\alpha_q A^2\epsilon^2)$, plus $D$. With probe force-energy $O(A^2D)$ and bounded other contributions,

$$\mathcal T_{\rm cal}=O\!\left(RD+
\frac{D^2}{\Gamma\alpha_q A^2\epsilon^2}
\left[RE_0+\frac{R^2A^2D}{\Gamma}\right]\right).             \tag{17}$$

Fresh deployment preparation separately costs $O(D_g+E_gD_g^2/(\Gamma\alpha_g\delta_g^2))$. There are $R(m+1)$ raw calibration boxes and one baseline per deployment. Unselected slots need no measurement. Averaging uses $O(m)$ encoded words; retaining all raw records is optional.

No hidden mode count, damping gap or inverse local rate appears. The energy bound remains supplied and can be extensive. Continuous unbudgeted heat input is not finite initial energy. Off leakage, fixed meter bias, clock error and sensor response create accuracy floors.

## Actuation and reaction

For a quintic ramp of increment $c$ over $h$,

$$\|\dot f\|_\infty=\frac{15|c|}{8h},\qquad
\|\ddot f\|_\infty=\frac{10\sqrt3|c|}{3h^2}.$$

Divide by $k$ for center speed and acceleration. For storage bound $E_{\max}$,

$$X_{\max}=\sqrt{2E_{\max}/\mu},\qquad F_{\rm spring}\le F+kX_{\max}.$$

Absolute moving-center work is at most $(F+kX_{\max})\operatorname{TV}(q)$, and peak power at most reaction times center speed. A calibration up/hold/off cycle has center travel $2A/k$. A known mass bounds damper reaction by $\Gamma\sqrt{2E_{\max}/M}$. These caps concern the fixture. They neither bound every hidden internal force nor infer unlimited material bandwidth from storage. The supplied LTI and dissipation laws must actually hold on the operating range.

At fixed speed and acceleration caps, reducing $h$ requires reducing $A$. Substituting that amplitude into (12), (16) and (17) worsens noise exposure and waiting. Arbitrary accuracy at fixed absolute hardware errors is not asserted. Actuator inertia, electronics, cooling and holding power depend on the apparatus. Idle power $P_{\rm idle}$ costs $P_{\rm idle}\mathcal T$ even when source input is zero.

## Installation, metrology and protection

The primary initial energy includes the permanent spring. If it must be installed, supply bare energy $E_b$, initial displacement bound $X_0$, and a finite stiffness ramp over $\tau_c$ with $k\tau_c<\Gamma$. The installation proof gives

$$D_x^2\le\frac{2X_0^2+2\tau_c E_b/\Gamma}{1-k\tau_c/\Gamma},
\qquad E_{\rm loaded}\le E_b+kD_x^2/2.$$

Reaction, parameter slew and work follow from this range. An initial displacement bound is not implied by bare passivity.

A positive finite sensor response of mean delay $\tau_m$ has bias at most $\sqrt{Q_v\tau_m}$ when its relevant velocity-energy budget is $Q_v$. With a velocity cap, the bias is at most $V_{\max}\tau_m$. Sensor history must be bounded or cleared for a finite time. Integration, ADC, gain and calibration errors belong to the deterministic allowance.

For $Q$ boxes of minimum width $b_{\min}$, a sufficient digitizer half-range is $X_{\max}+\sqrt{\nu_x/b_{\min}}\sqrt{2\log(2Q/\alpha_{\rm ov})}$ plus margins. Quantization uses finite bits; overflow is flagged and charged to confidence. Private entropy, clock drift, memory corruption and arithmetic reliability need their own hardware contracts. The passive experiment does not certify them. For example, a memory-retention design must keep its total error below its allocated failure probability for the entire physical wait, not just for the processor run time.

Exact gain identification can be avoided at the native input. If a fixed trap stiffness only satisfies $0<k_{\min}\le k_{\rm true}\le k_{\max}$, learn center-to-position response and use that same interface later. Its range is at most $2k_{\max}/k_{\min}$ and modulus $k_{\max}\sqrt{u/(2\Gamma k_{\min})}$. Fixed unknown gain cancels; drift after calibration changes the plant and does not cancel.

The result is a finite conditional operation. It does not manufacture arbitrarily precise sensors, energy bounds or dampers from unspecified materials. Those are declared physical access, whose costs must be supplied for a chosen apparatus.

# Finite prediction and robust planning

## Exact compilation

For rational response knots and a finite input made of quintic ramps, all convolution coefficients are rational. On a table interval, $\widehat S$ is linear; the ramp density is degree four. Their integral is piecewise polynomial of degree at most six. Breakpoints lie among input starts plus response knots and input starts plus ramp widths plus response knots. A finite sorted sweep compiles the whole path.

For $K$ input ramps and $m$ table intervals, a straightforward compiler takes polynomial rational arithmetic work and at most $O(Km)$ breakpoints. Prefix integrals of $u^r\widehat S(u)$ for $0\le r\le4$ allow each requested coefficient after preprocessing to be found with a table search and a constant number of rational operations. Bit lengths depend on the actual rational encoding; arithmetic is not counted as unit cost at unbounded precision.

The implemented independent verifier uses exact degree-five Boole quadrature on each clipped table interval. At seven rational points in every partition cell, it compares this convolution against the emitted degree-six polynomial. Together with the independently verified complete partition and exact continuity, these seven identities prove equality throughout each cell. This certifies the predictor as a function, not merely its sampled accuracy.

## Planning theorem

Choose rational nonoverlapping ramp starts $t_j$ and width $h$, and use

$$f_c(t)=\sum_{j=1}^K c_j\phi((t-t_j)/h).$$

Amplitude restrictions are linear prefix inequalities $|\sum_{i\le j}c_i|\le F$; variation is $\sum_j|c_j|\le V$. Individual coefficient caps give finite center slew and acceleration. Epigraph variables make variation linear. The predicted position is

$$\widehat x_c(t)=b+\sum_j A_j(t)c_j,\quad
A_j(t)=\int_0^h\rho_h(s)\widehat S(t-t_j-s)ds.$$

Let $\epsilon_*=\eta_0+V\epsilon_S+\eta_d$ be the earned uniform physical error, and let $L_{\widehat S}$ be the largest absolute slope of the acquired table. The predicted path has Lipschitz constant at most $VL_{\widehat S}$. For a planning grid of fill distance $d$, imposing

$$L+\epsilon_*+VL_{\widehat S}d\le\widehat x_c(t_i)
\le U-\epsilon_*-VL_{\widehat S}d                         \tag{18}$$

proves the actual continuous path lies in $[L,U]$ on the common event. Thus endpoint maximization is a finite rational LP. The margin uses the acquired table's slope, not an unobserved plant derivative.

The executed planner may use a floating optimizer to propose a vertex. It then reconstructs a rational feasible point, checks every inequality, and constructs nonnegative rational dual multipliers satisfying exact stationarity. Explicit variable boxes permit repairing rounded dual residuals. A separate verifier reconstructs coefficients by direct integration and checks feasibility and the exact primal-dual gap. The floating solver is not trusted as a certificate.

This is optimization within the declared finite basis and tightened polytope. Empty tightening does not prove impossibility of all safe physical controls. A plan optimal to tolerance $\epsilon_{\rm opt}$ is within $2L_J\epsilon_*+\epsilon_{\rm opt}$ of the best true value within that same polytope for a path objective of Lipschitz constant $L_J$. It is not a global optimal-control claim.

If planning depends on the new baseline, its worst-case latency must be included in $D$. A measured execution time is not such a proof. One may instead precompute the plan before drawing the fresh clock. The demonstrated physical query is preprogrammed; the optimizer on its saved baseline is a counterfactual planning example, not an unpriced second physical deployment.

# Joined execution

## One continuously retained source

The executed source is a 26-state passive oscillator fixture: an observed mass and spring and twelve hidden oscillator pairs with mixed damping, including undamped and very slow modes. One pair is dark to the measured port and retains energy. The initial state is generated once, before both clock draws. The source is retained through calibration, turnoff, the second wait, the query and its final turnoff. Only the sensor/integrator is reinitialized. The learner receives finite position reports, times and public bounds, with no source matrix, mode frequencies or hidden state.

The source and sensor evolution use floating ODE integration and matrix exponentials. Jumping over a long wait in simulation does not remove its physical occupancy cost. Independent reproducible PRNG streams emulate the separate private clock choices; this is not execution of a certified entropy source. Nonzero robust allowances are budgeted; their adversarial worst cases are not all simulated.

| Quantity | Declared or executed value |
|:--|--:|
| Observed mass, local drag, permanent stiffness | $M=\Gamma=k=1$ |
| Forecast horizon; initial total energy bound | $T=1$; $E_0=0.2$ |
| Probe amplitude; positive ramp duration | $A=1$; $h=0.02$ |
| Position box; table mesh | $b=0.005$; $\Delta=0.01$ |
| Sensor time constant; clearing time | $10^{-5}$; $0.0002$ |
| Absolute report/slot tolerance; waveform timing tolerance | $10^{-6}$; $10^{-8}$ |
| Calibration/deployment quiet tolerances | $0.02$; $0.04$ |
| Allowed quiet failures | $0.02$ each |
| Force discrepancy; selected-window backaction amplitude | $10^{-5}$; $10^{-6}$ |
| Deterministic position-box error; readout density | $10^{-4}$; $10^{-10}$ |
| Calibration slots; deployment slots | $32768$; $16384$ |
| Raw boxes; ADC resolution and range | $102$; 20 bits over $[-2,2]$ |
| Source resets; sensor resets | $0$; $2$ |
| Private random bits; timer width | $29$; $43$ bits |
| Actual total schedule; worst allowed schedule | $37154.426896$; $50390.748704$ |
| Raw ADC payload; acquired fraction payload | $2040$; $4271$ bits |

These are normalized units, not an experimentally optimized apparatus. For example, the calibration center has speed cap $93.75$ and acceleration cap about $14433.757$. A physically chosen scale must convert every force, length, time and energy consistently. The known fixture's reaction is bounded; an arbitrary hidden-force peak is not.

The query's rise has speed cap 30. Its shorter final return has speed cap 75, still covered by the calibration fixture's overall speed and acceleration capacities. The forecast guarantee ends before that separately charged return.

The exact nominal probe squared-force integral, including its full off-ramp, is $46231/46200$. With the permitted force error and backaction, the certified post-calibration energy is below $0.450174$ and is rounded upward to $0.5$ for the next preparation. The nominal source's actual energies are approximately $0.280010$ after calibration and $0.0808445$ immediately before deployment. Hidden energy remains; the operation has not equilibrated the source.

## Acquired predictor and confidence

The finite report gives

$$\epsilon_S=0.0562185,\qquad
\eta_{\rm readiness}=0.04070011,\qquad
\eta_{\rm delivery}=0.000008.$$

Thus all admitted smooth inputs with $W_f\le1$ have error at most

$$0.04070011+0.0562185+0.000008=0.09692661.$$

The declared joint physical event has probability at least $0.951998$, conditional on reliable controller, clock and metrology contracts. Its allocation includes both quiet events, both noise events and ADC overflow. Any additional hardware-failure allocation must be subtracted. This is an unconditional protocol guarantee over the private draws and meter noise, not a posterior confidence inferred from a quiet observed trace.

The actually simulated query is $0.8\phi(t/0.05)$, held through the horizon. It has $W_f=0.8$ and exact bound

$$\|x-\widetilde x\|_\infty\le0.08568291.$$

The compiler emitted 100 polynomial segments of degree at most six, using 585 active table-interval visits and 27,552 bits of coefficient integer payload. The independent verifier checked 700 rational identity points and 4,095 exact quadrature subintervals, plus partition completeness and continuity. Compilation and verification each took less than one second in this execution. These times are measurements, not a machine-independent worst-case guarantee. The source simulation took about 12.4 seconds of CPU wall time while its declared physical schedule remained over 37,000 time units.

The acquired table SHA-256 is `c1527bb91029dd3141a1b3583d4e8cd82c7f50b4b30473ed05ff37f16ad421ce`. The exact prediction path is separately hashed in the machine-readable receipt. Exact compilation proves that the numerical object implements the acquired formula. It does not turn floating source integration into a validated physical experiment.

![Finite response acquisition, retained-source prediction, and the full physical waiting bill. The source curves are floating diagnostics; the bands are conditional theorem bounds.](bridge/complete_operation.pdf){height=8.1in}

## Executed robust planning

The planner uses five possible ramps starting at $0,0.2,0.4,0.6,0.8$, each of width $0.05$. It imposes force and variation caps of one, increment cap $0.4$, and a desired path band $[-0.3,0.3]$. A 64-interval planning grid yields a 10-variable, 171-inequality rational LP. Its coefficient integers have maximum 106 bits in the recorded implementation.

The exact optimum uses two nonzero increments, approximately $0.376972$ and $0.4$, at times zero and $0.2$. The predicted endpoint is $0.1988623218$. The rational primal-dual gap is exactly zero. A separate checker reconstructs 325 response coefficients, checks all 171 inequalities, 171 nonnegative multipliers and ten stationarity equalities. A further polynomial verifier certifies the emitted whole prediction path. Using the actual variation gives physical error bound $0.0843883317$ and endpoint interval approximately $[0.114474,0.283251]$. Equation (18) gives the full-time safety band on the common physical event.

An offline parametric construction removes online LP search. Over baseline interval approximately $[-0.01643123,0.11114808]$, an affine primal formula and fixed dual remain exactly feasible and optimal. Checking both endpoints proves feasibility throughout; the duality gap is identically zero. Online work is two interval comparisons and ten rational multiply-add pairs, followed by finite command encoding. Fixed word bounds follow from the finite ADC and coefficient encodings, and actual hardware execution must fit the declared latency. Outside this one region the plan abstains. No conditional-on-acceptance confidence amplification is claimed.

There is a simpler integer implementation. For a fresh report $\beta=a/q$, form $R=3276800000000a$, $P=364210013027q$, $L=-53841850173q$ and $D=1045129658000q$. Accept $L\le R\le P$ and emit $c_0=(P-R)/D$, $c_1=2/5$. This takes four products by fixed integers of at most 42 bits, one subtraction and two comparisons. A $B$-bit report needs at most $B+43$-bit intermediates. Rounding to $p$ fractional bits adds a shift and integer division: schoolbook bit work $O((B+p+43)^2)$ and working bits $O(B+p+43)$. The rounding and waveform-loading errors enter the force allowance. Offline explicit optimization is established machinery [15]; this is its finite implementation at the newly acquired interface.

The planner includes a finite two-ramp post-horizon return, duration $0.1$, with its additional center travel and energy. It was executed computationally on the saved readiness record. This is not a second physical source deployment. A new actual deployment would use a fresh private preparation and the appropriate energy bound.

# Comparison with strong ordinary approaches

## What is reused

Step-response prediction and optimization are old, effective ideas. Dynamic Matrix Control already uses experimentally acquired step-response coefficients to predict and plan [6]. Identification without explicitly estimating initial state goes back at least to Pearson [5]. The response table and LP are therefore not the scientific claim.

Modern latent-system prediction already avoids full state-space identification, including spectral filtering [7]. Learning without a conventional mixing argument is also established [8]. Set-membership identification provides rigorous simulation bounds under its stated assumptions [9]. The result here should not be described as the first model-free predictor, the first method without mixing, or the first finite-data certificate.

Generalized-Langevin identification is a serious alternative. Bockius et al. construct a Markov model from measured correlations without explicitly reconstructing a memory kernel [10]. Lang and Lu study stable kernel estimation in weighted norms [11], and recent GLE perturbation results transfer kernel errors to stochastic dynamics under their contracts [12]. Such machinery can be more accurate, more efficient or support broader stochastic/nonlinear questions when its required data and preparation law are supplied.

## The exact added capability

The new comparison is at the initialization and access interface. For every finite-energy initial state of a supplied locally dissipative LTI port, the construction obtains a high-probability prepared input-output experiment with no hidden order, gap or frequency-sector bound. It admits conservative incoming-wave realizations that defeat fixed-deadline preparation despite a completely known elementary response kernel. Finite random timing, finite metrology and superposition close the gap through the final acquired prediction and robust program.

An equally informed ordinary practitioner can incorporate this preparation operation into a standard step-response controller. The advantage is not superior algebra after a response table is given. It is the additional theorem that makes the table and its initialization valid under the stated physical uncertainty. The proof does not show that the waiting bound is optimal or that this is the best experimental design for a particular apparatus.

## Accepted Astra baseline and previous bridge

The accepted N1688 acquired thermal simulator already treats a retained device without resets, unknown fixed gains, noisy readout and arbitrary bounded future feedback at its encoded pulse interface [13]. Its positive reciprocal thermal response and specially matched balanced pulse are substantive structure. It supplies a future record-law total-variation guarantee, which is stronger than this report's open-loop path claim in that direction.

The present theorem retains continuous and DC response and includes arbitrary passive oscillatory or conservative hidden linear dynamics under (1), but uses a finite-energy bound and private randomized starts. It does not produce a thermal path law, remove unbudgeted heat injection, or inherit N1688's arbitrary-feedback guarantee. The two operations have different premises and outputs.

The previous acquired passive bridge handles a known strongly convex nonlinear visible law coupled to positive Maxwell memory, including its finite initialization and numerical contracts [14]. The selected theorem removes that microscopic bath form and need for a known bare restoring law by keeping a permanent spring, but requires whole-plant LTI superposition. The nonlinear theorem remains useful and unchanged.

## Consequence and limits

There are three distinct resources: forced response, hidden initial-state behavior, and control over the start time. A low-order forced response need not imply a low-complexity or rapidly forgetful hidden preparation. Conversely, a large or nonrelaxing hidden environment need not prevent a finite prepared prediction when only a locally dissipating visible coordinate matters and private random scheduling is available.

This gives a broad sufficient operational law and an exact deterministic boundary. It does not characterize every observable environment. Nonlinear unknown laws, active hidden modes, uncontrolled nonstationarity, missing dissipation, unbounded initial energy and unknown access outside the declared port remain outside it. A small fitted model or strong convexity alone does not replace these conditions. The completed construction warrants studying this preparation resource; its present resource bounds do not establish practical transformative performance.

# Preserved companions and scope ledger

The package retains the network-composition theorem and its exact counterexample. Monotone pairwise springs preserve the stated maximum-node comparison for heterogeneous Maxwell modules. Arbitrary strong convexity is insufficient: with $n=s^2+1$ and $I\preceq H\preceq2I$, the explicit rank-one family has coordinate error $(s+7)/16$ at time $\log2$ under unit per-coordinate force uncertainty. This excludes a dimension-free maximum-coordinate law from strong convexity alone; it does not contradict Euclidean stability.

The finite-sector oscillatory companion remains at its supplied $|\omega|\le Q\lambda$ scope. Its filtering calculation tracks complex phase. A filtered atom can have negative real value at zero; positive microscopic weights do not make that filtered function an ordinary passive atom. The analytic acquisition and comparison construction is complete; only small diagnostics were executed.

A finite-horizon response lemma without coercivity is retained. Nonnegative storage and local dissipation give $\|S'\|_{L^2(0,L)}\le\sqrt L/\Gamma$, $0\le S(t)\le t/\Gamma$, and modulus $\sqrt{L|t-s|}/\Gamma$ on $[0,L]$. The permanent spring supplies a time-uniform range and hardware caps; it is not necessary for every finite-horizon estimate.

The previous complete archive is embedded byte-for-byte, with SHA-256

`98350f429ad0abff06f908b4bcaac9a14d0ea59e105760884a44d083fb7673e5`.

Its 5,423,526 bytes and nested earlier packages preserve the passive acquisition-to-prediction construction, opposite-ends attempts and failures, quantum results, rare-failure constructions and source receipts. No accepted theorem is reopened or strengthened. Half-diamond conventions, actual pure-port access, weak-action restrictions, classical-feedback/pathwise budgets, finite payload-memory results, and source forgetting versus output acquisition remain as stated. The homogeneous weak-stream receiver is not claimed solved.

# Evidence and reproducibility

The archive contains independent proofs, physical closure, source simulation, acquired table, exact predictor and verifier, planner and separate verifiers, parameter checks, diagnostic figures, receipts and preservation hashes. The reproduction guide distinguishes analytic theorems under contracts, exact finite arithmetic, and floating simulations. Sampled plots do not prove uniform bounds, and no interval-validated source or laboratory experiment is claimed.

The simulator accesses its matrix to generate data and diagnostics. The acquired predictor and planner do not. Their verifiers reconstruct identities from acquired data; physical assumptions are not inferred from those identities.

# Primary sources and accepted machinery

1. J. C. Willems, *Dissipative Dynamical Systems, Part I: General Theory*, 1972. [Primary paper](https://homes.esat.kuleuven.be/~sistawww/smc/jwillems/Articles/JournalArticles/1972.1.pdf). Storage inequalities, nonuniqueness and interconnection.

2. A. Figotin and J. H. Schenker, *Hamiltonian structure for dispersive and dissipative dynamical systems*. [Primary preprint](https://arxiv.org/abs/math-ph/0608003). Conservative extensions.

3. A. Mielke, M. A. Peletier and J. Zimmer, *Deriving a GENERIC system from a Hamiltonian system*, arXiv version 2; journal 2025. [Primary full text](https://arxiv.org/html/2404.09284v2). Preparation and hidden evolution, especially section 5.3.

4. S. Ghadimi and G. Lan, *Stochastic First- and Zeroth-Order Methods for Nonconvex Stochastic Programming*. [Primary preprint](https://arxiv.org/abs/1309.5549). Random-iterate selection from aggregate bounds.

5. A. E. Pearson, *Finite time interval linear system identification without initial state estimation*, Automatica 12 (1976), 577-587. [Publisher record](https://doi.org/10.1016/0005-1098(76)90039-X).

6. C. R. Cutler and B. L. Ramaker, *Dynamic Matrix Control - A Computer Control Algorithm*, 1980. [Primary paper](https://skoge.folk.ntnu.no/puublications_others/1980_Cutler-Ramaker_Dynamic-matrix-control_JACC1980.pdf).

7. E. Hazan, H. Lee, K. Singh, C. Zhang and Y. Zhang, *Spectral Filtering for General Linear Dynamical Systems*, NeurIPS 2018. [Primary paper](https://papers.nips.cc/paper_files/paper/2018/file/d6288499d0083cc34e60a077b7c4b3e1-Paper.pdf).

8. M. Simchowitz, H. Mania, S. Tu, M. I. Jordan and B. Recht, *Learning Without Mixing: Towards A Sharp Analysis of Linear System Identification*, COLT 2018. [Primary proceedings](https://proceedings.mlr.press/v75/simchowitz18a.html).

9. M. Lauricella and L. Fagiano, *Set Membership identification of linear models with guaranteed simulation accuracy*. [Primary preprint](https://arxiv.org/abs/2001.07628).

10. N. Bockius et al., *Model reduction techniques for the computation of extended Markov parameterizations for generalized Langevin equations*. [Primary preprint](https://arxiv.org/abs/2101.02657).

11. Q. Lang and J. Lu, *Learning Memory Kernels in Generalized Langevin Equations*. [Primary full text](https://arxiv.org/html/2402.11705v3).

12. Q. Lang and J. Lu, *Error Analysis of Generalized Langevin Equations with Approximated Memory Kernels*, 2025. [Primary full text](https://arxiv.org/html/2512.10256v1).

13. Astra Research N1688, *Acquired thermal feedback simulator*, accepted source, revision `626bf0fb5da19c8eb62964f0d7949bb19bc64799`. [Pinned source](https://github.com/harjassand/astra-research-knowledge/blob/626bf0fb5da19c8eb62964f0d7949bb19bc64799/research/2026-11-04-p2-acquired-thermal-feedback-simulator/source/p2/COMPLETE_VISIBLE_RESPONSE.txt).

14. *Acquiring a certified passive environment*, preceding completed construction. Preserved with proofs, programs, governing receipts and selection attempts. Its accepted passive-memory proof is pinned at the same revision. [Governing proof](https://github.com/harjassand/astra-research-knowledge/blob/626bf0fb5da19c8eb62964f0d7949bb19bc64799/research/returns/2026-11-05-p3-correlated-reliability/package/independent_routes/next3_first_principles/02_PASSIVE_MEMORY_PROOF.md).

15. A. Bemporad, M. Morari, V. Dua and E. N. Pistikopoulos, *The Explicit Linear Quadratic Regulator for Constrained Systems*, Automatica 38 (2002), 3-20. [Institutional primary record](https://old.control.ee.ethz.ch/publications/2002/12.html). Offline parametric optimization is established control machinery.

The public Astra corpus was also consulted at revision `3971cfa5513774bcc4aee30083ebe7bd2ab8d09b`. No historical novelty conclusion follows from an incomplete search. The claims here are the explicitly constructed operations and boundaries.
