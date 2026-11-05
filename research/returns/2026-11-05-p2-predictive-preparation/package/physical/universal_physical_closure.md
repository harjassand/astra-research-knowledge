# Finite physical closure for a randomized acquired passive response

## Status

This note supplies finite acquisition, actuation, metrology and reuse for the universal linear passive response programme. It preserves COMPOSITION_THEOREM.md unchanged. The independent randomized-initialization proof is in ../independent/RANDOMIZED_PREDICTIVE_INITIALIZATION.md.

The main realization keeps a calibrated spring/trap installed permanently. This eliminates release and removes the need to bound unknown bath velocity peaks. It predicts the permanently loaded plant. Prediction of an unloaded plant is not inferred from this operation.

There is no physical prototype in this note. It specifies finite operations and proves their guarantees. The physical model class and hardware contracts remain premises.

## 1. Plant, storage, and the permanent trap

The scalar force port has input f and observable position x, with v=xdot. The complete plant, including all hidden coordinates, is causal and linear time invariant. It has nonnegative storage E satisfying

\[
 E(t)-E(s)\le\int_s^t f(u)v(u)\,du-\int_s^t v(u)^2\,du,
 \qquad E(t)\ge\mu x(t)^2/2,\quad\mu>0.                       \tag{1}
\]

Local drag is calibrated and normalized to one. The initial state is fixed before each private scheduling choice, with a supplied energy bound E_0.

A mechanical realization has a known local damper, an arbitrary unknown linear passive bath, and a calibrated spring/trap of stiffness k>0. A known bare visible spring of stiffness mu_0>=0 may also be present. Keep the trap installed, put mu=mu_0+k, and program its center

\[
 q(t)=f(t)/k.
\]

The actual trap force is k(q-x)=f-kx. The -kx term is part of the fixed loaded plant; the additive term is the experimental input. No separate viscous-support actuator, instantaneous release, or coherent access to the bath is used.

Hidden order, frequencies, damping gap and equilibrium preparation are not assumed. The bath can include conservative modes, delays or a continuum if the well-posed LTI dynamics and storage law actually hold. The trap law, local drag, storage bound, linearity/time invariance and measurement contracts are supplied physical premises, not inferred from a fitted trace.

For any actual force program, completing the square in (1) yields

\[
 E_{\rm after}\le E_{\rm before}+\tfrac14\int f_{\rm actual}^2,
 \qquad
 \int v^2\le2E_{\rm before}+\int f_{\rm actual}^2.             \tag{2}
\]

All intentional forces, off-mode error, selected-window meter backaction and nonzero force during computational delays are included in this ledger.

## 2. Universal zero-state bounds

Let S be the zero-state position response to the ideal mathematical unit step. This is the acquisition target, not an instantaneous physical operation.

Under that input, E-S+1/(2mu) is nonnegative, starts at 1/(2mu), and has derivative at most -Sdot^2. Hence

\[
 0\le S(t)\le2/\mu,\qquad
 \int_0^\infty|\dot S(t)|^2\,dt\le1/(2\mu).                  \tag{3}
\]

With S(t)=0 for negative t,

\[
 |S(t)-S(s)|\le\omega(|t-s|),\qquad
 \omega(a)=\sqrt{a/(2\mu)}.                                 \tag{4}
\]

No translation or equilibrium preparation of the hidden bath was used.

For any zero-state force error d, (2) also gives

\[
 \|Rd\|_{\infty,[0,T]}\le\|d\|_{L^2(0,T)}/\sqrt{2\mu}.       \tag{5}
\]

This prices finite actuator errors and backaction without assuming a hidden bandwidth.

## 3. Random quiet windows, including imperfect off mode

Divide a common counterfactual off-mode trajectory into N disjoint slots, each of duration at most D and long enough for the baseline, all data/forecast times and clock guards. Choose the slot index J privately and uniformly. A power-of-two N requires exactly log2(N) unbiased private bits.

The off-mode force w_0 is bounded by xi_0 and follows a common causal law independent of J until intervention. The private index must not be revealed to a disturbance source or used to reprepare the hidden initial state. Shared exogenous randomness independent of J can be used to define this counterfactual law.

For slot I_j set Z_j=sup_{s,t in I_j}|x_off(s)-x_off(t)|. Then

\[
 Z_j^2\le D\int_{I_j}v_{\rm off}^2,\qquad
 \Pr[Z_J>\delta]\le
 \frac{2E_0D}{N\delta^2}+\frac{\xi_0^2D^2}{\delta^2}.         \tag{6}
\]

The second term is a real off-mode accuracy floor. Sufficient choices for failure alpha_q are

\[
 N\ge4E_0D/(\alpha_q\delta^2),\qquad
 \xi_0\le\delta\sqrt{\alpha_q/2}/D,                          \tag{7}
\]

with N rounded upward to a power of two. A genuinely passive exact off mode has the sharper E_0D/(N delta^2) probability.

Only the selected slot is measured. Worst-case occupancy is ND; expected selected start is at most (N-1)D/2 plus finite scheduling conventions.

The actual clock produces consecutive nonoverlapping enclosing slots with certified maximum duration D. All baseline and data boxes fit inside them with explicit guards. Uncertain report time contributes (4); force-program timing error contributes (5). Finite clock precision, maximum duration, counter bits and memory reliability are paid.

Pseudorandomness is not substituted for the private randomness in this information-theoretic claim. An index distribution beta away from uniform in total variation adds beta to failure. An arbitrary index-dependent force cannot be placed inside the common-path averaging argument.

## 4. Finite positive-ramp acquisition

Choose a positive normalized kernel supported on [0,h]:

\[
 k_h(t)=R'(t/h)/h,\qquad R(s)=10s^3-15s^4+6s^5.
\]

Its cumulative ramp is zero before zero and one after h. Apply f_probe(t)=A R(t/h), hold through the final data box, then turn off with a finite smooth reverse ramp. The zero-state response on the data interval is A S_h, where S_h=k_h*S and

\[
 \|S_h-S\|_\infty\le\omega(h).                              \tag{8}
\]

No deconvolution or kernel differentiation is required.

Use nodes t_j from zero through T with maximum gap Delta. In the selected slot, first read a position baseline over duration b. Start the force ramp after that box. For every nonzero node, read the position mean over [t_j,t_j+b] relative to the force start. Hold the force through T+b. A slot length D=T+2b plus clock guards suffices; it may also include the off-ramp if desired.

If X_0 and X_j are the true position means, on the selected quiet event,

\[
 |(X_j-X_0)/A-S(t_j)|\le\delta/A+\omega(h)+\omega(b).         \tag{9}
\]

This uses one retained device and requires no physical zero-state preparation.

Suppose a b-box mean has deterministic error at most b_x and conditionally sub-Gaussian noise with variance proxy v_x/b. The deterministic term includes calibration, finite integration, ADC and sensor-response effects. After R repetitions, simultaneous averaged nodal noise is at most

\[
 \frac1A\sqrt{\frac{4v_x\log(2M/\alpha_m)}{Rb}},              \tag{10}
\]

where M is the number of nonzero nodes. Later boxes may overlap; the union bound does not need independence among them. Conditional noise increments across actual readings or the equivalent metrology contract suffice. The deterministic difference error is 2b_x/A and is not reduced by repetition.

Selected-window meter backaction is charged separately. If its force during the baseline has L2 norm q_b, and the later actual probe minus the common off counterfactual has force discrepancy of L2 norm q_p, baseline subtraction costs at most

\[
 \eta_{\rm force}=(2q_b+q_p)/(A\sqrt{2\mu}).                 \tag{11}
\]

The factor two accounts for the baseline disturbance's effect on both baseline and forecast. With no baseline backaction, q_b=0. A uniform on/off discrepancy gives q_p <= (xi_1+xi_0)sqrt(T+b), plus separately bounded probe-time backaction.

Set the zero-time report to zero, clip remaining reports into [0,2/mu], and interpolate linearly. The clipping cannot increase error relative to S. With knot-time error kappa_t and finite encoding allowance eta_enc,

\[
\begin{split}
 \|S-\widehat S\|_\infty\le\epsilon_S:={}&
 \delta/A+2b_x/A+\eta_{\rm force}+\eta_{\rm enc}\\
 &+\frac1A\sqrt{\frac{4v_x\log(2M/\alpha_m)}{Rb}}\\
 &+\omega(h)+\omega(b)+\omega(\kappa_t)+\omega(\Delta).
\end{split}                                               \tag{12}
\]

The representation is a finite response table. A sufficient mesh has M=O(1+T/(mu epsilon_S^2)), with every other error separately allocated.

## 5. Repetitions without resets and their energy bill

After every repetition, finish the smooth off-ramp and update E using (2). Choose the next index freshly with the new energy bound. S is unchanged because the plant is time invariant, although its hidden state has changed.

One valid construction requires every repetition's quiet event and splits alpha_q across repetitions. A less wasteful construction averages the quiet error. Conditional on every preceding history, choose N_r and xi_0,r so that E[Z_r^2 | past] <= alpha_q delta^2. Jensen and Markov then give

\[
 \Pr\!\left[R^{-1}\sum_{r=1}^R Z_r>\delta\right]\le\alpha_q.   \tag{13}
\]

The same average bounds the retained background in every averaged node report. No independence of hidden states is used. The conditional readout-noise estimate (10) remains valid.

Allocate a per-cycle off input-energy budget P_off,r and require

\[
 \xi_{0,r}^2N_rD\le P_{\rm off,r}.                           \tag{14}
\]

First choose N_r from the current E_r, then choose off-mode precision to satisfy both (7) and (14). This prevents a conservative persistent off force from causing an unpriced multiplicative energy growth. With fixed per-cycle force-energy budgets, E_r grows at most linearly and the total waiting bill is the sum of energy-dependent N_rD.

There are R(M+1) position boxes. None is measured in the unselected slots. O(M) finite counters accumulate the reports; retaining every raw record is optional. Every cycle pays its random bits, sequencing, force ramps, noise exposure and energy update.

## 6. Fresh initialization and all-input prediction

After acquisition and any computation delay, update the energy ledger and choose a fresh quiet slot containing a baseline box and the entire forecast. Report its mean as xhat_0, with metrology error eta_g. On the selected event, the off counterfactual remains within delta_g+eta_g of that report throughout the future horizon.

For a nominal force f of bounded variation, extended by zero before launch, put

\[
 W_f=|f(0+)|+\operatorname{TV}_{(0,T]}f.
\]

LTI superposition gives

\[
 (Rf)(t)=f(0+)S(t)+\int_{(0,t]}S(t-s)\,df(s).                 \tag{15}
\]

Replacing S by its acquired table therefore produces error at most W_f epsilon_S. The same calibration/initialization event supports every later admissible preprogrammed force, including a choice made after calibration and the baseline. Computation performed after the baseline must fit inside the quiet slot, or the force program must be computed beforehand.

Counterfactual simulator queries reuse the table and do not consume extra confidence. Physically executing a force changes the plant state. Another physical deployment needs a new energy bound and a fresh selected window. General future measurement-feedback policies require a separately proved closed-loop comparison.

## 7. Finite actuation of BV inputs

A mathematical jump is not issued instantaneously. Deliver the positive smoothed force f_a=k_a*f, using the kernel in section 4 with width a. If |f|<=F, then |f_a|<=F and

\[
 \|\dot f_a\|_\infty\le15F/(4a).
\]

For the same quintic kernel, its derivative has total variation

\[
 \|k_a''\|_1=\frac{40\sqrt3}{3a^2},
\]

so

\[
 \|\ddot f_a\|_\infty\le \frac{40\sqrt3\,F}{3a^2}.            \tag{16}
\]

These follow from the exact extrema of R' and R'' and the zero endpoint derivatives. Consequently the permanent trap center has finite bounds

\[
 |q|\le F/k,\quad
 |\dot q|\le15F/(4ka),\quad
 |\ddot q|\le40\sqrt3 F/(3ka^2).                            \tag{17}
\]

More smoothness requirements are handled by a higher-order positive kernel with its derivative norms explicitly charged.

Since Rf_a=(S*k_a)*df, smoothing contributes at most

\[
 \|Rf_a-Rf\|_\infty\le W_f\omega(a).                         \tag{18}
\]

This is a consequence of the proved step modulus, not an assumption that the high-frequency bath is negligible.

Let q_f bound the L2 difference between actual delivered force and the requested smoothed force plus common off counterfactual, over the forecast. Let q_bg bound baseline-only backaction. If epsilon_num bounds actual numerical evaluation of the finite table formula, the completed operation has

\[
 \boxed{
 \|x_f-\widetilde q_f\|_\infty
 \le\delta_g+\eta_g
 +W_f[\epsilon_S+\omega(a)]
 +\frac{2q_{bg}+q_f}{\sqrt{2\mu}}
 +\epsilon_{\rm num}.}                                    \tag{19}
\]

Actual timing is measured from the start of the physical smoothed program. Clock/program errors appear in the declared finite budgets.

An arbitrary mathematical BV function is not a computation oracle. A supplied finite program must provide its finite representation or validated evaluations. Moving its variation measure onto a grid of mesh tau contributes at most W_f omega(tau), by the same argument as (18). A finite list of K force jumps gives a piecewise-linear table prediction with at most K(M+1) shifted knots. A direct sorted sweep costs O(KM log(KM)) arithmetic operations, with its output storage and rounding explicitly counted. Standard faster gridded convolution is an optional implementation.

## 8. Bounded physical control with the permanent trap

If E_max bounds the energy throughout a stage, then

\[
 |x|\le X_{\max}:=\sqrt{2E_{\max}/\mu}.
\]

The trap reaction is k(q-x). Its peak is bounded by

\[
 F+kX_{\max},                                               \tag{20}
\]

plus declared actuation allowances. This bound needs no peak velocity estimate. Absolute moving-center work is at most

\[
 (F+kX_{\max})\,\operatorname{TV}(q).
\]

For a smoothed BV program, TV(q)<=W_f/k, including the initial rise; any final return to zero contributes its own force variation and energy. Peak actuator power is bounded by reaction times the center-speed bound in (17).

Calibration positive ramp/hold/off has center travel 2A/k and finite displacement A/k. There is no displacement accumulating with hold duration. During a quiet phase the center is at zero, up to its calibrated error. A center error e_q contributes additive force k e_q to xi_0 or xi_1. A stiffness error has both a multiplicative visible term and a center term; bound its total force effect on the known position/center box and include it explicitly. The mass of the apparatus, control electronics and holding power retain their hardware-specific costs.

This physical realization predicts the permanently loaded plant. Removing the trap changes its response and is a separate operation. There is no release in the completed primary construction.

### Unknown bare visible law

The bare plant need not have a known restoring law. If it has nonnegative storage E_b and the known local velocity-dissipation inequality, a calibrated permanent spring k yields E=E_b+kx^2/2 and certified mu=k. A known additional bare stiffness can improve the coercivity constant, but is unnecessary. Whole-plant linearity, time invariance and passivity remain substantive premises.

### Installing the spring rather than assuming it already operates

If the spring already operates, the supplied initial E_0 must include its storage. Otherwise supply a bare-energy bound E_b0 and an initial position bound |x(0)|<=X_0 relative to its intended center. Ramp stiffness monotonically from zero to k over finite tau_c with k tau_c<1. Let D_x=sup_{[0,tau_c]}|x|. The time-dependent stored energy obeys

    Edot <= -v^2 + (kdot/2)x^2.

Thus int v^2 <= E_b0+(k/2)D_x^2 and

\[
 D_x^2\le\frac{2X_0^2+2\tau_c E_{b0}}{1-k\tau_c},\qquad
 E_{\rm loaded}\le E_{b0}+(k/2)D_x^2.                       \tag{21}
\]

The finite stiffness slew, peak reaction kD_x, stiffness-change work at most (k/2)D_x^2 and peak parameter power are explicit. An initial finite-box position measurement can supply X_0 only when its range/noise and the relevant prior motion-energy bound are paid. No unbounded position preparation is inferred from bare passivity.

### Scope of the known local damper

The main theorem assumes an actual calibrated velocity-dissipation inequality. An arbitrary passive device need not supply it. If the whole mass-spring-damper interface is engineered, the damper's reaction gamma v also needs a physical cap. An optional known inertial mass m with storage at least m v^2/2 yields |v|<=sqrt(2E_max/m) and closes this cap. The random-window and step-response proofs are unchanged. This is an additional realizable fixture, not a deduction of damping or inertia from passivity alone.

## 9. Finite measurement, clocks and digitization

Let Q be the total number of raw position boxes and b_min the shortest. The storage gives a finite mean range X_max. With white readout density v_x, choose ADC half-range

\[
 X_{\max}+\sqrt{v_x/b_{\min}}\sqrt{2\log(2Q/\alpha_{\rm ov})}
\]

plus deterministic margins. Quantization within its allocated bias has a finite bit count. Overflow is flagged and costs alpha_ov in the joint event.

Finite sensor response is not replaced by an exact point meter. If a positive sensor kernel has mean delay tau_m and its initial/history transient is bounded or cleared, a known total motion-energy budget Q_v gives delay bias at most sqrt(Q_v tau_m), by Cauchy--Schwarz and Jensen. A supplied velocity cap improves this to V_max tau_m. The bound must cover the relevant prehistory; initialization/clearing costs are explicit. Integration, calibration and digitization errors enter b_x and eta_g and are not averaged away.

An actual clock guard must ensure nonoverlapping physical candidate slots. Source evolution during a computation delay is charged through its actual off-mode force and energy bound. The permanent trap has a finite center program, and the decoder/table has finite classical precision and protection costs. No ideal field buffer, hidden-state measurement, velocity oracle, exact kernel sample or infinite-range digitizer is used.

## 10. Reuse and sufficient resource scales

After every actual physical force or final return ramp, update energy by (2). The table S remains valid for the same unchanged LTI loaded plant. Every new physical deployment gets a fresh predictive initialization. To guarantee a joint event over many deployments, allocate initialization failures across runs and pay the resulting larger slot count and force precision.

For fixed calibration amplitude A and target response error eps, one sufficient scale allocation is

    h,b,Delta,kappa_t = O(mu eps^2),
    delta = O(A eps),
    deterministic position error = O(A eps),
    R = O(1+v_x log(M/alpha_m)/(A^2 mu eps^4)),
    M = O(1+T/(mu eps^2)).

The quiet wait is N_rD with N_r from the current E_r and (7), or the averaged construction (13). With bounded per-cycle force-energy, total waiting is proportional to the sum of the growing E_r. The raw measurement count is R(M+1); finite averaging/clipping/interpolation is linear in this count apart from clock and word-length costs.

For fixed center speed and acceleration caps, decrease A along with h so the finite command fits. This worsens the noise, wait and precision bills. For fixed force-program variation, smoother delivery requires a wider filter and its explicit W_f omega(a) prediction error. Fixed nonzero off-force, clock, sensor or calibration errors impose floors. No arbitrary-accuracy statement at fixed absolute hardware errors is made.

No physical prototype or fully materialized random-clock experiment is claimed here. The result is a full finite conditional operation. Its strongest comparison is with ordinary experimental linear response and system identification under unknown initial conditions, prepared-bath GLE models, and randomized selection from a dissipation budget. The contribution to evaluate is their complete interface and quantifiers; neither Markov's inequality nor the Holder interpolation scale is claimed as a new mathematical principle.

## 11. Native-input corollary: exact stiffness identification is unnecessary

The constant trap stiffness need not be numerically identified exactly if the question is posed at the actual accessible input. Suppose a fixed linear trap is certified only within 0<k_min<=k_true<=k_max. Learn the response S_q from programmed trap-center displacement q to observed x, and later query the same center interface.

The storage dominates k_min x^2/2. For a mathematical unit center step the additive force is k_true, so

    0<=S_q<=2 k_max/k_min,
    int S_qdot^2 <= k_max^2/(2 k_min),
    |S_q(t)-S_q(s)| <= k_max sqrt(|t-s|/(2 k_min)).

All acquisition, smoothing and BV formulas apply with this modulus and center amplitudes/variations. A center-tracking error e_q costs at most k_max ||e_q||_2/sqrt(2 k_min). A known upper bound on total storage is updated with (k_max^2/4) int q_actual^2. Reaction is bounded by k_max(|q|+|x|).

An unknown fixed gain therefore cancels between calibration and deployment. A stiffness change after calibration does not cancel and must be treated as a changed plant or additional force uncertainty. This is a change of the input representation, not a promise to implement an exactly specified physical force without calibration.

## 12. Finite force-energy accounting convention

The energy inequalities use actual force. For an interval with known nominal force f_nom and an L2 delivery/backaction allowance q_err, a directly computable sufficient budget is

    P_actual <= (||f_nom||_2 + q_err)^2.

Disjoint quiet and intervention intervals can be summed. A quiet interval of duration ND contributes at most xi_0^2 ND. A positive probe held through T+b and switched off over h_off has nominal input energy at most A^2(T+b+h_off), since its amplitude never exceeds A. A final return to center zero changes the plant state and is included in this budget; it is not a hidden reset. For the native-center corollary multiply squared center-input budgets by k_max^2.
