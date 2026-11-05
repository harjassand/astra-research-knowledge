# Ordered binary experiments and a direct compliance decision

## 1. Exact comparison of complete causal experiments

Let two known causal LTI input/output operators have zero-state impulse responses `g_0,g_1`, locally integrable on `[0,H]`. Suppose

\[
d(t)=g_1(t)-g_0(t)\geq0\quad\text{a.e.}
\]

The scalar input is selected causally, using earlier measurements and private randomness. The physical constraint is a known nonnegative envelope

\[
|f(t)|\leq u_*(t).
\]

The observations are

\[
dY_t=(g_\theta*f)(t)dt+\sqrt\nu\,dW_t,
\qquad \theta\in\{0,1\},\quad \nu>0.
\]

The admissible policy class consists of policies for which this feedback experiment is well posed and causally simulable. This includes finite instruments, sampled feedback and regular continuous feedback. The reference contrast is assumed square integrable, as it is for every finite bounded-force experiment below. An assertion about arbitrary pathological measurable feedback is unnecessary.

Define

\[
\Delta_*(t)=(d*u_*)(t),\qquad
I_*(H)=\frac1\nu\int_0^H\Delta_*(t)^2dt.
\]

**Theorem 1.** The open-loop experiment `f=u_*` Blackwell-dominates every admissible causal policy satisfying the envelope. In particular, the smallest possible worst-hypothesis error, allowing all such input policies, all measurements of the supplied readout, all private randomness and all stopping rules bounded by `H`, is exactly

\[
\boxed{p_*(H)=\Phi\!\left(-\frac{\sqrt{I_*(H)}}2\right).}
\]

Here `Phi` is the standard normal CDF. Blackwell domination means that a parameter-independent randomized map of the reference experiment reproduces the complete joint law of another experiment, including its chosen inputs and decision. It is stronger than a Fisher-information comparison.

### Proof

For the input selected along any realized target observation history, compute both candidate deterministic outputs `x_0,x_1` using that same realized input. Positivity gives

\[
|x_1(t)-x_0(t)|=|(d*f)(t)|\leq(d*u_*)(t)=\Delta_*(t).
\]

Center and normalize the reference open-loop observation. It has the form

\[
dX_t=(2\theta-1)A(t)dt+dB_t,
\qquad A(t)=\frac{\Delta_*(t)}{2\sqrt\nu}.
\]

To generate a target observation, use an independent Brownian motion `B'` and the target policy's private randomness. At each time compute the target candidate states from the generated past, and set

\[
m_t=\frac{x_0(t)+x_1(t)}2,
\quad a_t=\frac{x_1(t)-x_0(t)}{2\sqrt\nu},
\quad r_t=\frac{a_t}{A(t)}.
\]

Set `r_t=0` wherever `A(t)=0`; then also `a_t=0`. The inequality above gives `|r_t|<=1`. Generate

\[
dZ_t=r_t\,dX_t+\sqrt{1-r_t^2}\,dB'_t,
\qquad dY_t=m_tdt+\sqrt\nu\,dZ_t.
\]

This construction is causal and does not use the true hypothesis. Under either hypothesis its drift is exactly `x_theta(t)`. Its noise is a continuous martingale with quadratic variation `nu dt`; the two Brownian sources have zero cross variation. Levy's characterization and the assumed well-posedness give exactly the target observation law. The target input, randomization, stopping rule and decision can consequently all be reproduced.

For the reference experiment, the log-likelihood statistic is normal with means `-I_*/2,+I_*/2` and variance `I_*`. Threshold zero gives equal errors `Phi(-sqrt(I_*)/2)`. It is Bayes optimal under equal priors, hence minimax because its two errors agree. Blackwell domination proves optimality over the full causal policy class. QED.

### Conditions that cannot be removed from this statement

The models and their initial state are known in this theorem. The input constraint is pointwise, not merely a total-energy constraint. The difference impulse response has one sign. The metrology is a declared Gaussian readout channel with known noise density, independent of the input and plant. No intrinsic thermal process noise is included. General input design under different constraints can prefer oscillatory, impulsive or adaptive inputs. The theorem does not assert otherwise.

## 2. A passive material pair with a discontinuous long-run answer

Normalize the local viscous drag to one. Let `mu,B>0` be known spring constants. The accessible displacement is `x`, the force is `f`, and an internal stress is `y`:

\[
\dot x=-\mu x-y+f,
\qquad \dot y=B\dot x-\lambda y.
\]

There are two hypotheses: `lambda=0` (frozen internal strain) and a specified `lambda>0` (a Maxwell relaxation channel). The model has storage

\[
\mathcal E=\frac\mu2x^2+\frac{y^2}{2B},
\quad
\dot{\mathcal E}=f\dot x-\dot x^2-\frac\lambda B y^2.
\]

It is passive, and the local force/position port is the only observation/actuation port during the experiment. This is a structured manufactured or otherwise certified material family, not a promise that every hidden environmental mechanism belongs to it.

Write `kappa=mu+B`. From zero initial state,

\[
G_0(s)=\frac1{s+\kappa},\qquad
G_\lambda(s)=\frac{s+\lambda}{s^2+(\kappa+\lambda)s+\mu\lambda}.
\]

Thus

\[
D_\lambda(s)=G_\lambda(s)-G_0(s)
=\frac{\lambda B}{(s+\kappa)(s+r_-)(s+r_+)},
\]

where

\[
r_\pm=\frac{\kappa+\lambda\pm
\sqrt{(\kappa+\lambda)^2-4\mu\lambda}}2>0.
\]

Its difference impulse response is

\[
d_\lambda=\lambda B\,
e^{-\kappa\cdot}*e^{-r_-\cdot}*e^{-r_+\cdot}\geq0.
\]

The zero-state DC compliances nevertheless differ by a constant:

\[
G_0(0)=\frac1\kappa,
\qquad G_\lambda(0)=\frac1\mu,
\qquad G_\lambda(0)-G_0(0)=\frac B{\mu\kappa}.
\]

Let

\[
C_\lambda(t)=\int_0^t d_\lambda(s)ds.
\]

Under `|f|<=F`, Theorem 1 gives the exact optimal error

\[
\boxed{p_*(H)=\Phi\left(-\frac F{2\sqrt\nu}
\sqrt{\int_0^H C_\lambda(t)^2dt}\right).}
\]

The ordinary maximal step load and a matched linear statistic attain this error. Neither feedback nor a privately randomized start/stopping time bounded by `H` can improve it.

## 3. Uniform information bounds and three regimes

Assume `0<lambda<=kappa` and put `rho=mu lambda/kappa`. The roots obey

\[
\kappa\leq r_+\leq2\kappa,
\qquad \rho/2\leq r_-\leq\rho.
\]

For `m_a(t)=min(t,1/a)`, direct integration over a simplex gives

\[
C_\lambda(t)=\lambda B
\int_{u,v,w\geq0,\ u+v+w\leq t}
e^{-\kappa u-r_-v-r_+w}\,du\,dv\,dw.
\]

Bounding this simplex above by the cube `[0,t]^3` and below by `[0,t/3]^3`, and using

\[
\frac{1-e^{-at/3}}a\geq\frac14\min(t,1/a),
\]

proves

\[
\frac{\lambda B}{128}m_\kappa(t)^2m_\rho(t)
\leq C_\lambda(t)
\leq2\lambda Bm_\kappa(t)^2m_\rho(t).
\]

Consequently, with absolute positive constants (for example `2^-21` and `4`),

\[
\boxed{I(H)\asymp
\frac{F^2\lambda^2B^2}{\nu}\,
H\min(H,\kappa^{-1})^4\min(H,\rho^{-1})^2.}
\]

More precisely:

\[
I(H)\sim\begin{cases}
F^2\lambda^2B^2H^7/(252\nu),&H\downarrow0,\\
F^2\lambda^2B^2H^3/(3\nu\kappa^4),
&\lambda\downarrow0,\ \kappa H\to\infty,\ \rho H\to0,\\
F^2B^2H/(\nu\mu^2\kappa^2),&H\to\infty\text{ at fixed }\lambda>0.
\end{cases}
\]

The middle limit follows because the two fast exponential filters have reached their integrals while the slow exponential is uniformly close to one on any fixed fractional terminal part of the interval. The elementary bounds above dominate the remaining part, so squaring and integrating is justified.

For fixed confidence `alpha in (0,1/2)` and fixed other parameters, let `z_alpha=Phi^-1(1-alpha)`. The exact optimal decision deadline therefore satisfies

\[
\boxed{H_\alpha\sim
\left(\frac{12\nu\kappa^4z_\alpha^2}
{F^2B^2\lambda^2}\right)^{1/3}.}
\]

Its slow relaxation time is `1/r_- ~ kappa/(mu lambda)`. The decision arrives parametrically earlier, but its time still diverges as `lambda^(-2/3)`.

An especially simple uniform obstruction is

\[
d_\lambda(t)\leq\lambda B/\kappa^2,
\quad C_\lambda(t)\leq\lambda Bt/\kappa^2,
\quad
I(H)\leq\frac{F^2\lambda^2B^2H^3}{3\nu\kappa^4}.
\]

Indeed `e^(-r_-.)*e^(-r_+.) <=1/r_+<=1/kappa`, after which the third convolution gives the first inequality. This bound holds for every positive `lambda`, since `r_+>=kappa` always. The KL divergence of any adaptive experiment is at most `I(H)/2`, either by the garbling theorem or directly by Girsanov. Thus no finite deadline works uniformly over every positive relaxation rate, despite the constant DC-compliance separation. This conclusion already holds with perfect initial readiness.

## 4. Composite decision without identifying the rate

With zero initial state the same operation solves

\[
H_0:\lambda=0,
\qquad H_1:\lambda\geq\lambda_{\min}>0.
\]

For any nonnegative nondecreasing input, `x_lambda(t)` is nondecreasing in `lambda`. To prove this, write `v=xdot` and `z=Bx-y`. The equations for `(v,y)` are cooperative under input `fdot>=0`, so `v,y>=0`. The equations for `(x,z)` are

\[
\dot x=-\kappa x+z+f,
\qquad \dot z=\lambda(Bx-z).
\]

Their parameter derivatives `(q,w)=(partial_lambda x,partial_lambda z)` satisfy

\[
\dot q=-\kappa q+w,
\qquad \dot w=\lambda Bq-\lambda w+y,
\]

with zero initial state. This is again cooperative with nonnegative forcing, so `q>=0`. Step inputs follow by a smooth monotone approximation.

The matched statistic for `lambda_min` has nonnegative weight. Every larger-rate alternative therefore has at least its alternative mean, with the same sensor variance. Its worst alternative is exactly `lambda_min`. The simple-pair lower bound is contained in the composite family, so the same formula for the optimal worst-case error is exact, using `C_lambda_min`. No estimation of the actual rate is required.

## 5. Finite actuation and readout

### Smooth forces

Let `phi(s)=10s^3-15s^4+6s^5` on `[0,1]`, with constant zero/one extensions, and use `f_h(t)=F phi(t/h)`. This has

\[
|\dot f_h|\leq15F/(8h),\qquad
|\ddot f_h|\leq10\sqrt3F/(3h^2).
\]

The contrast is a positive average of delayed step contrasts. For `t>=h`,

\[
FC_\lambda(t-h)\leq\Delta_h(t)\leq FC_\lambda(t).
\]

Its information at `H` is consequently at least the ideal-step information at `H-h`. A fixed finite ramp time therefore preserves the small-rate scaling. The exact Blackwell theorem also applies to the declared envelope `u_*=f_h`. It does not assert that this particular quintic ramp is optimal among all force waveforms sharing only derivative caps.

### Finitely many box integrals

Read `N` nonoverlapping integrals over intervals `I_j` of lengths `b_j`:

\[
Y_j=\int_{I_j}x(t)dt+\sqrt\nu\,[W(t_j)-W(t_{j-1})].
\]

Let `bar Delta_j` be the known average contrast on interval `I_j`. The finite sufficient statistic has information

\[
I_N=\nu^{-1}\sum_j b_j\bar\Delta_j^2,
\]

and exact equal errors `Phi(-sqrt(I_N)/2)`. The means are computed from the two explicitly supplied two-state equations, not from an acquired response table. Because the contrast is Lipschitz with constant `L=F lambda B/kappa^2`,

\[
0\leq I-I_N\leq L^2H b_{\max}^2/(12\nu).
\]

For equal bins in the intermediate regime, `N=O(eta^(-1/2))` retains a fraction `1-eta` of the information, with constants uniform as `lambda` tends to zero. Only one running weighted accumulator is necessary; keeping all bins is optional.

### Error budget and actual physical resources

The zero-state theorem is not a free-reset theorem. One may supply a factory-prepared strain state with energy at most `E_init`. Its contribution to position is bounded for all later times by

\[
|x_{\rm init}(t)|\leq\sqrt{2E_{\rm init}/\mu}.
\]

This follows from passivity of the homogeneous error dynamics. Preparing such a state is an explicit resource. For example, *if* actual reset contacts on the two strain coordinates are provided with a certified storage contraction `E(t)<=E_factory exp(-2r t)`, the preparation time is at least the chosen sufficient value `log(E_factory/E_init)/(2r)` and the contacts, dissipated stored energy and their control precision are paid. These contacts are additional physical access; the theorem does not infer their existence from the accessible force/position port.

For a genuinely finite alternative with no reset contacts, see Section 6.

Under a monotone force from zero, `0<=x<=F/mu`, `y>=0`, and `0<=xdot<=F`. A stable positive sensor filter of known mean delay `tau_s` therefore contributes position bias at most `F tau_s`, after its separately charged clearing. A bounded force error `delta_f` contributes at most `delta_f/mu`, because the force-position impulse response is nonnegative and its integral is at most `1/mu`. Add these to preparation bias, model-calibration bias, ADC error, coefficient-rounding error and clock/integration error. A pointwise total error `e` yields normalized matched-statistic bias at most

\[
\frac e\nu\sum_jb_j|\bar\Delta_j|.
\]

It is sufficient to budget this below a selected fraction of the nominal half-mean separation `I_N/2`. For a simpler terminal-bin test of duration `b`, average contrast `bar Delta>0`, and mean error `e<=bar Delta/4`, each error is at most

\[
\exp[-b\bar\Delta^2/(32\nu)]
\]

plus the separately allocated sensor-overflow probability. This one-bin operation has the same intermediate `lambda^2 H^3` information order.

The finite ADC range must include `F/mu+sqrt(2E_init/mu)` and the chosen Gaussian overflow margin, for example `sqrt(nu/b_j) sqrt(2 log(2N/alpha_overflow))` for a measured average. A quantization step `q` costs `q/2` in its deterministic error allocation. Exponential coefficients and thresholds can be enclosed to the required accuracy using ordinary interval arithmetic; an arithmetic operation with unbounded precision is not treated as free. The physical `mu,B`, drag and sensor-noise calibration must meet the specified output error contract. They are certified supplied structural parameters here, not learned without exposure. If this calibration is not available, this package has not solved its acquisition. Any physical meter backaction must be included in the certified force-error allowance or in a separately analysed noise model; the mathematical readout channel does not supply an unpriced noninvasive apparatus.

At the small-rate decision horizon, the response contrast has scale `lambda H`, hence `lambda^(1/3)` when other constants are fixed. Residual *unknown* systematic position bias must shrink on that scale. The simple prepared-state implementation correspondingly needs `E_init=O(lambda^(2/3))`, force calibration error `O(lambda^(1/3))`, and ADC resolution `O(lambda^(1/3))`. The ADC bit count grows logarithmically in `1/lambda`, while acquiring its noise and bias contract is a physical cost. If the crude unmodelled-lag bound above is used, its delay must also shrink on this scale. A known fixed sensor filter can instead be included in the two candidate means, or a delayed terminal window can be used; a vanishing sensor delay is not a necessary law. The exact time advantage is not a promise for one fixed hardware platform with a nonzero unknown systematic error floor.

The experiment occupies one specimen and one meter for `H`, plus force ramp, clearing and any declared reset times. Its force-squared action is at most `F^2H`. This is different from mechanical work. During monotone loading from zero,

\[
W=\int f\,dx\leq F x(H)\leq F^2/\mu.
\]

An actuator/controller's idle power still costs `P_idle H`; no inference-time or occupancy cost is hidden by the bounded mechanical work. The return ramp and preparation needed for reuse are additional, finite operations. A fresh specimen is not a free reset. Fixed-rate digital integration costs `O(H/b)` samples and arithmetic, constant running classical memory, and its sensor/controller energy for the full interval. At fixed target fractional information loss the mathematical integrated-readout statistic needs only the constant number of bins described above.

## 6. Removing an unknown initial state in the observation

This independent operation is for the simple binary pair `lambda=0` versus a specified positive `lambda`. It does not assume readiness and does not automatically solve a continuum of unknown rates.

For the frozen model, the output generated by an arbitrary initial state lies in

\[
\mathcal S_0=\operatorname{span}\{1,e^{-\kappa t}\}.
\]

For the relaxing model it lies in

\[
\mathcal S_1=\operatorname{span}\{e^{-r_-t},e^{-r_+t}\}.
\]

A constant force alone has its entire forced-response contrast inside `S_0+S_1`; simply fitting that trace with arbitrary initial states can erase the decision. A force reversal creates the required new information.

Define the fourth-order polynomial

\[
P(s)=s(s+\kappa)(s+r_-)(s+r_+)
=s^4+(2\kappa+\lambda)s^3
+[\kappa^2+(\kappa+\mu)\lambda]s^2+\kappa\mu\lambda s.
\]

Let `psi(t)=phi_8(t/H)` on `[0,H]`, where

\[
\phi_8(u)=256u^4(1-u)^4.
\]

It and its first three derivatives vanish at the endpoints. Put

\[
w(t)=P(-\partial_t)\psi(t).
\]

Then `integral w(t) h(t) dt=0` for every `h in S_0+S_1`, by four integrations by parts. No initial-state estimate is needed. Moreover, because `P(s)D_lambda(s)=lambda B s`, every finite-variation force satisfies exactly

\[
\int_0^H w(t)[x_\lambda^f(t)-x_0^f(t)]dt
=\lambda B\int_0^H\psi(t)\,df(t).
\]

The identity holds distributionally for piecewise constant force. The vanishing endpoint derivatives remove its initial jump and all homogeneous boundary terms.

Use `f=F` on the first half and `f=-F` on the second half. Since `psi(H/2)=1`, the two weighted means differ by `-2 lambda B F`, independently of both unknown initial states. The scalar observation `S=integral w dY` has variance `nu integral w^2 dt`. Subtract the known midpoint of the two forced means and threshold at zero. Its two errors are exactly

\[
\Phi\left(-\frac{\lambda BF}{\sqrt{\nu\int_0^H w(t)^2dt}}\right).
\]

This is a complete arbitrary-initial-state decision, not a readiness certificate.

For a bounded physical weight, use `q(t)=H^2 w(t)/kappa^2`; scaling does not change the test. With `eta=1/(kappa H)` and `rho=mu lambda/kappa`,

\[
q(Hu)=\eta^2\phi_8^{(4)}(u)
-(2+\lambda/\kappa)\eta\phi_8^{(3)}(u)
+[1+(\kappa+\mu)\lambda/\kappa^2]\phi_8''(u)
-\rho H\phi_8'(u).
\]

In the early-creep limit `kappa H -> infinity`, `rho H ->0`, this approaches `phi_8''`. Since

\[
J_2=\int_0^1[\phi_8''(u)]^2du=\frac{1572864}{5005},
\]

the decision deadline for error `alpha` obeys

\[
\boxed{H_{\alpha,\rm nuisance}\sim
\left(\frac{\nu\kappa^4J_2z_\alpha^2}
{F^2B^2\lambda^2}\right)^{1/3}.}
\]

The zero-state lower bound is also a lower bound when arbitrary initial states are allowed. The unknown-state operation therefore matches the optimal `lambda^(-2/3)` scale. Its asymptotic time constant is `(J_2/12)^(1/3)`, about `2.97`, times the ideal known-state optimum. This is an attained factor, not a claim that the polynomial weight is the optimal unknown-state receiver.

### Finite force and metrology implementation

Smooth the initial increase over `[0,h]` and the force reversal over `[H/2-h/2,H/2+h/2]`, using monotone quintic ramps, with `h<=H/8`. On the reversal interval `psi>=81/256`, while on the initial ramp `psi<=phi_8(1/8)<0.037`. Hence

\[
\left|\int\psi\,df\right|
\geq 2F(81/256)-0.037F>0.595F.
\]

The signal remains a fixed positive fraction of `lambda B F`; all force peaks, slopes and curvatures are finite. A fixed ramp duration has the same small-rate asymptotic constant as the ideal reversal, because `h/H ->0`.

The weight `q` is an explicitly known polynomial of degree at most seven. Its amplitude and first derivative are bounded by absolute constants and an absolute constant divided by `H`, respectively, whenever `kappa H>=1`, `rho H<=1`, and `lambda<=kappa`. It can be applied by a calibrated electronic multiplier/integrator or a finite digital weighted sum. This requires one running classical accumulator and a clock, not hidden-state access.

For a digital implementation, let `X` bound the actual position magnitude. Initial energy `E` and force `|f|<=F` give the uniform bound

\[
X\leq\sqrt{2E/\mu}+F/\mu.
\]

The homogeneous part is bounded by its decreasing storage, while the forced part has a nonnegative impulse response with integral at most `1/mu`. Approximate `q` uniformly by `q_N` with error `delta_q`; the weighted mean error is at most `delta_q XH`, and the RMS noise difference is at most `sqrt(nu H) delta_q`. The nominal weighted signal is `2 lambda BF H^2/kappa^2` for the ideal reversal. For example,

\[
\delta_q\leq c\frac{\lambda BF H}{\kappa^2 X}
\]

for a chosen small constant `c` controls the drift error. Piecewise-constant quadrature gives `delta_q<=C/N`; piecewise-linear quadrature gives `delta_q<=C/N^2`. At `H` proportional to `lambda^(-2/3)` with bounded `E`, the respective sufficient counts scale as `lambda^(-1/3)` and `lambda^(-1/6)`. The number of readings or waveform intervals and their accuracy are therefore explicitly charged. A fixed hardware sample rate instead gives `O(H/b)` processing and easily satisfies these conditions asymptotically at bounded `E`. A physical finite-range ADC must include `X` and its allocated noise tail. No unbounded-amplitude initial state is silently admitted by finite hardware.

Coefficient/parameter uncertainty produces an additional weight error, multiplied by the same `XH` bound, and an error in the known forced mean. Consequently the required precision improves only logarithmically in inverse target error in *bit count*, but acquiring that calibration is a supplied metrological task, not inferred from formal differentiation. The Gaussian sensor law is a sensor contract; a different colored or intrinsic-noise law requires its actual covariance and a new analysis. The operation works for every initial state within the declared range, so it can be reused without hidden equilibration provided its current state remains inside that paid range. A conservative per-run update is `E_next<=E+F^2H/4`, obtained from `f xdot-xdot^2<=f^2/4`; a declared return ramp adds its force-squared action divided by four to this bound. Force return, actuator idle energy and data acquisition over each entire experiment are still charged.

## 7. Relation to predictive preparation and ordinary methods

The known-state lower bound rules out a rate-independent inference of infinite-time compliance even after perfect preparation. Preparation supplies an initial-state resource, not arbitrarily long-time information.

If one applies a generic energy/dissipation quiet-window preparation to this decision, the required local displacement error in the early-creep regime is proportional to `F lambda B H/kappa^2`. Its sufficient waiting bill can therefore grow like `E kappa^4/(alpha F^2 B^2 lambda^2)` under the corresponding normalized dissipation contract. That is the cost of that sufficient construction. It is **not** a lower bound on all initial-state-independent decisions: Section 6 is an explicit counterexample to that interpretation.

Known-model matched testing, deterministic waveform design and elimination of a finite-dimensional initial-state nuisance are strong existing ordinary methods. The operation in this note has no exponential advantage over an equally informed application of them. It earns a clean exact boundary and a closed direct-decision example. It does not earn identification of arbitrary hidden dimension, proof of a complete failure family, unlimited-time material classification, a new thermodynamic resource, or a universal speedup from random timing.
