# Passive memory: retained-device initialization and uniform nonlinear prediction

## Status and interface to the other constructions

This note closes the deterministic deployment and initialization portion of the acquired passive-memory programme. It is conditional on the forward acquisition returning a positive exponential model with a sound kernel certificate. It does **not** take physical samples of the unknown kernel as a primitive. The companion forward construction must supply those observations through its actual finite moving-trap protocol, with its own force, time, noise, tracking, and confidence costs.

The accepted P3 residual theorem is at `../PASSIVE_MEMORY_ACCEPTED_SOURCE.md`. Its derivative-memory energy identity is retained. The new steps here are a finite no-reset initialization procedure, a stronger uniform-in-time comparison bound in the scalar/isotropic case, a model velocity budget, explicit deployment quantifiers, and a finite-bin force readout. No historical novelty or experimental validation is claimed.

The earlier sparse-equilibrium attempt in this directory is unchanged.

## 1. Physical class and paid information

For clarity write the scalar system

\[
 \dot x=-V'(x)-\int(x-y_\lambda)\,d\nu(\lambda)+f,
 \qquad \dot y_\lambda=\lambda(x-y_\lambda).
\tag{1}
\]

Assume:

* \(V\) is known, \(\mu\)-strongly convex, and has locally Lipschitz derivative. The latter is a routine existence and numerical-evaluation condition; no global upper curvature bound is required for the stability theorem.
* \(\nu\) is an unknown nonnegative finite measure on \([0,\infty)\), with mass \(b_0\le B\). There is no bound on hidden order, no positive rate floor, and no finite rate ceiling.
* At the start of acquisition, the observed coordinate is known within the stated measurement accuracy, and an initial hidden energy budget is supplied:
  \(E_0=\tfrac12\int|y_\lambda(0)-x(0)|^2d\nu\le E_{\rm init}\).
* The calibration and its final transition to the hold remain within a certified observed-position envelope \(|x-x_r|\le A\). The hold then achieves \(|x-x_r|\le\delta\).
* Later forces have an explicit budget, such as \(|f(t)|\le F\) for a fixed total deployment horizon \(T\). The theorem is not a uniform claim over unbounded drives.

The mass bound, physical law, convexity, actuator/readout calibration, and initial-energy bound are supplied physical premises. A kernel fit alone does not establish them. The energy bound can scale with hidden volume.

The vector version holds for a common scalar kernel multiplying every coordinate, with \(V:\mathbb R^d\to\mathbb R\) strongly convex and Euclidean norms. The stronger maximum principle below is not asserted for general noncommuting matrix-valued kernels. The accepted \(L^2\) theorem has a broader positive matrix-kernel extension.

## 2. Hidden-state envelope after arbitrary bounded calibration

Let \(t_a\) be the end of calibration, including its final transition. The hidden field satisfies

\[
 y_\lambda(t_a)-x_r=e^{-\lambda t_a}(y_\lambda(0)-x(0))
 +e^{-\lambda t_a}(x(0)-x_r)
 +\lambda\int_0^{t_a}e^{-\lambda(t_a-s)}(x(s)-x_r)ds.
\]

Because the calibration envelope includes \(|x(0)-x_r|\le A\),

\[
 G_a:=\int|y_\lambda(t_a)-x_r|d\nu
 \le \sqrt{2BE_{\rm init}}+BA=:G.
\tag{2}
\]

This is a total-variation bound on the old signed force measure. It does not grow with the number or duration of calibration probes. It uses the bounded position envelope rather than pretending that the bath resets between probes.

Restart the clock at \(t_a\) and put \(d_\lambda=y_\lambda(t_a)-x_r\). During a hold define the old force

\[
 g_0(s)=\int e^{-\lambda s}d_\lambda\,d\nu.
\]

It obeys \(|g_0(s)|\le G\) and, for every \(s>0\),

\[
 |g_0'(s)|\le\int\lambda e^{-\lambda s}|d_\lambda|d\nu
 \le \frac{G}{e s}.
\tag{3}
\]

The proof only uses \(\sup_{\lambda\ge0}\lambda e^{-\lambda s}=1/(es)\). Frozen modes survive in \(g_0\), but their derivative is zero. This is a bound on variation, not a claim of equilibration.

## 3. Finite hold, finite-bin readout, and the 3Bδ term

Suppose \(|e(s)|:=|x(s)-x_r|\le\delta\) throughout a hold \([0,H]\). Choose a final measurement bin \([H-b,H]\), where \(0<b<H\).

The hidden field at the end of the hold is

\[
 y_\lambda(H)-x_r=e^{-\lambda H}d_\lambda+h_\lambda,
 \quad
 h_\lambda=\lambda\int_0^H e^{-\lambda(H-s)}e(s)ds,
 \quad |h_\lambda|\le\delta(1-e^{-\lambda H}).
\tag{4}
\]

Define the future force relative to the reference coordinate by

\[
 g_r(u)=\int e^{-\lambda u}(y_\lambda(H)-x_r)d\nu,
 \qquad 0\le u\le T.
\]

Then \(|g_r(u)-g_0(H+u)|\le B\delta\). The **actual** bath force during the hold is

\[
 m(s)=\int(y_\lambda(s)-x(s))d\nu
 =g_0(s)+\int\lambda\int_0^s e^{-\lambda(s-v)}e(v)dv\,d\nu-b_0e(s),
\]

so \(|m(s)-g_0(s)|\le2B\delta\). If a finite-bin readout returns \(c\) with

\[
 \left|c-\frac1b\int_{H-b}^H m(s)ds\right|\le\eta,
\tag{5}
\]

then every later time in the deployment window satisfies

\[
 \boxed{\quad |g_r(u)-c|\le
 \underbrace{\eta+3B\delta+
 \frac{G(b+T)}{e(H-b)}}_{\displaystyle\gamma},\qquad 0\le u\le T.\quad}
\tag{6}
\]

Indeed, the derivative bound (3) gives

\[
 |g_0(H+u)-g_0(s)|
 \le\frac Ge\log\frac{H+u}{s}
 \le\frac{G(b+T)}{e(H-b)}
\]

for every \(s\) in the bin. The remaining three units of \(B\delta\) are one from the hold-induced hidden offset and two from observing the actual bath force while the coordinate is imperfectly held.

This construction measures the surviving force. It neither deletes a frozen component nor assumes it has decayed.

The actual bin mean lies in the known interval \([-G-2B\delta,G+2B\delta]\). Projecting a noisy scalar estimate onto that interval cannot worsen (5). It therefore provides a deterministic bound \(|c|\le G+2B\delta\), including on bad sensor outcomes, without another measurement.

### 3.1 A physical finite-bin residual sensor

The balance law gives the exact identity

\[
 \frac1b\int_{H-b}^H m(s)ds
 =\frac{x(H)-x(H-b)}b
 +\frac1b\int_{H-b}^H[V'(x(s))-f(s)]ds.
\tag{7}
\]

Thus no instantaneous velocity or inaccessible kernel value needs to be measured. A sensor can combine two position readings, recorded applied force, and the known potential force.

For example, suppose endpoint position errors are at most \(\epsilon_x\), a reconstructed position curve over the bin has uniform error at most \(\epsilon_p\), the mean applied-force error is at most \(\eta_f\), and numerical quadrature error is at most \(\eta_Q\). If \(L_r\) bounds \(|V''|\) over the small measured position range, then

\[
 \eta\le \frac{2\epsilon_x}{b}+L_r\epsilon_p+\eta_f+\eta_Q.
\tag{8}
\]

A known modulus of continuity of \(V'\) can replace \(L_r\epsilon_p\). With a certified speed bound \(D_h\), linearly interpolating position samples at spacing \(h\) gives \(\epsilon_p\le\epsilon_x+D_hh/2\). This makes the observation finite. The known derivative or modulus is a computational resource, not something strong convexity alone provides as an upper bound.

If the mean force sensor has a conditionally sub-Gaussian error with variance proxy \(\sigma_f^2/b\), its random term in \(\eta_f\) can be set to
\(\sigma_f\sqrt{2\log(2/\alpha_g)/b}\). Endpoint and quadrature errors have their own finite budgets. A conditionally valid concentration bound and a union bound suffice; independence from the retained hidden state is not assumed.

### 3.2 Finite tracking is sufficient

An ideal hard clamp is unnecessary. A physical finite-stiffness trap at \(x_r\),

\[
 f=V'(x_r)-\kappa(x-x_r)+d(t),\qquad |d|\le d_*,
\]

can give the required tube. Let its starting coordinate error be at most \(A\ge\delta\), and let the old hidden-force total variation be at most \(G_0\). Provided \(\mu+\kappa\ge(G_0+d_*)/A\), the position stays within \(A\). The hidden-coordinate force is then at most \(G_0+BA\), and

\[
 |x(t)-x_r|\le A e^{-(\mu+\kappa)t}
 +\frac{G_0+BA+d_*}{\mu+\kappa}.
\]

Choose \(\mu+\kappa\ge2(G_0+BA+d_*)/\delta\), and wait at least
\(\log(2A/\delta)/(\mu+\kappa)\). The position enters the \(\delta\) tube; the same bounds maintain it thereafter. If a digital position error contributes \(d_*\le\kappa\epsilon_c+\eta_a\), the sufficient choices \(\epsilon_c\le\delta/4\) and \(\mu+\kappa\ge4(G_0+BA+\eta_a)/\delta\) give the same conclusion.

A finite moving-trap transition from the last calibration target can instead supply this entrance directly. Its duration, slew, maximum excursion, force, and actuator error belong to the forward resource account. Neither this argument nor the sensor presumes an instantaneous jump in the observed coordinate.

## 4. A passive predictor, including the measured constant force

Suppose the acquired model is

\[
 \widehat K(t)=\sum_{j=1}^n w_j e^{-\ell_jt},\qquad
 w_j\ge0,\quad \ell_j\ge0,\quad \sum_jw_j\le B,
 \qquad \|K-\widehat K\|_{L^1(0,T)}\le\zeta.
\tag{9}
\]

Initialize its observed coordinate and every auxiliary coordinate at \(x_r\):

\[
 \dot q=-V'(q)-\sum_jw_j(q-z_j)+f+c,
 \quad \dot z_j=\ell_j(q-z_j),\quad q(0)=z_j(0)=x_r.
\tag{10}
\]

The measured constant enters the shifted potential \(W(q)=V(q)-cq\), which remains \(\mu\)-strongly convex. Hence this is a passive model with input \(f\) and storage

\[
 \mathcal E=W(q)-\min W+\tfrac12\sum_jw_j(q-z_j)^2,
 \qquad
 \dot{\mathcal E}=-\dot q^2-\sum_jw_j\ell_j(q-z_j)^2+f\dot q.
\tag{11}
\]

Zero-rate modes are allowed. The constant measured force is not represented by a fictitious reset of the physical bath.

## 5. Rigorous maximum principle and nonlinear error certificate

Put \(J(t)=-K'(t)=\int\lambda e^{-\lambda t}d\nu\) for \(t>0\). Although \(J(0)\) need not be finite,

\[
 \int_0^T J(t)dt=b_0-K(T)\le B.
\]

Consequently \(J\in L^1(0,T)\), and the position-memory operator

\[
 P_K e=b_0e-J*e
\tag{12}
\]

is well defined. For an error with arbitrary initial value, \(P_Ke=K*\dot e+K(t)e(0)\).

### Comparison lemma

If an absolutely continuous scalar error satisfies

\[
 \dot e+a(t)e+P_Ke=r,
 \qquad a(t)\ge\mu>0,
\]

then

\[
 \boxed{\|e\|_{L^\infty(0,T)}\le
 \max\{|e(0)|,\|r\|_\infty/\mu\}.}
\tag{13}
\]

To prove this without assuming a differentiable attained maximum, take
\(M=\max\{|e(0)|,\|r\|_\infty/\mu\}\). The constant function \(M\) has
\(\dot M+aM+P_KM=[a(t)+K(t)]M\ge r(t)\).
For \(w=e-M\), variation of constants and positivity of \(J\) imply

\[
 w_+(t)\le\int_0^t\!\int_0^s J(s-u)w_+(u)du\,ds
 \le B\int_0^t w_+(u)du.
\]

Gronwall gives \(w_+=0\). Apply the same argument to \(-e\). This proof covers bounded measurable residuals, arbitrary finite horizons, and unbounded microscopic rates. In the isotropic vector case, the norm obeys the corresponding scalar differential inequality, so the same result holds.

### Applying the lemma to the physical state

Let deployment time zero be the end of the hold. The physical coordinate starts at \(x(0)=x_r+e_0\), with \(|e_0|\le\delta\), and the physical hidden state remains the actual \(y_\lambda(H)\). Its exact equation in reference-position form is

\[
 \dot x+V'(x)+P_K(x-x_r)=f+g_r.
\]

Subtract (10), and use \(q(0)=x_r\), so \(P_{\widehat K-K}(q-x_r)=(\widehat K-K)*\dot q\). Then

\[
 \dot e+[V'(x)-V'(q)]+P_Ke
 =(\widehat K-K)*\dot q+(g_r-c).
\tag{14}
\]

Strong convexity supplies the coefficient \(a(t)\ge\mu\). Young's convolution inequality therefore gives

\[
 \boxed{\quad
 \sup_{0\le t\le T}|x(t)-q(t)|
 \le\max\left\{\delta,\frac{\zeta\|\dot q\|_\infty+\gamma}{\mu}\right\}.
 \quad}
\tag{15}
\]

Thus the initial-coordinate mismatch can be paid by a maximum, rather than an additive triangle inequality. The weaker \(\delta+(\zeta\|\dot q\|_\infty+\gamma)/\mu\) is also safe.

If the numerical output has a certified position-equation residual \(\rho\), reconstructing its modal convolution from that output gives the same direct bound with its actual velocity and \(\gamma+\|\rho\|_\infty\). Alternatively, compare with the exact model first: the numerical trajectory differs from (10) by at most \(\|\rho\|_\infty/\mu\), so one may add this amount to (15) while using an a priori exact-model velocity bound. These two accounting choices must not be mixed.

### 5.1 Explicit uniform velocity budget

Let \(x_*\) solve \(V'(x_*)=c\), and define

\[
 D_0=|V'(x_r)-c|/\mu,\qquad
 D=\max\{D_0,F/\mu\}.
\]

Strong convexity gives \(|x_*-x_r|\le D_0\). The interval \([x_*-D,x_*+D]\) is invariant for the observed and all learned hidden coordinates in (10). At its upper boundary the potential force is at least \(\mu D\), while the memory force points inward and \(f\le F\); the lower boundary is analogous. Each hidden coordinate remains between earlier observed positions and its initial value.

If \(L\) bounds \(|V''|\) on the computable containing interval
\([x_r-(D_0+D),x_r+(D_0+D)]\), then

\[
 \boxed{\|\dot q\|_\infty\le D_v:=F+(L+2B)D.}
\tag{16}
\]

A direct bound on \(|V'(q)-c|\) over the same interval can replace \(LD\). No microscopic rate occurs in this budget. A rough root bracket suffices; exact solution for \(x_*\) is unnecessary.

There is no need to choose the kernel accuracy after observing \(c\). With the clipping convention above, use \(D_{0,\rm pre}=(|V'(x_r)|+G+2B\delta)/\mu\), \(D_{\rm pre}=\max\{D_{0,\rm pre},F/\mu\}\), and a potential derivative bound on \([x_r-D_{0,\rm pre}-D_{\rm pre},x_r+D_{0,\rm pre}+D_{\rm pre}]\). These give a pre-acquisition upper bound for (16).

### 5.2 The accepted L2 route, with initial-coordinate mismatch

For each rate let \(p_\lambda'=\lambda(e-p_\lambda)\), \(p_\lambda(0)=0\), and \(z_\lambda=e-p_\lambda\). Then \(P_Ke=\int z_\lambda d\nu\), and

\[
 \int_0^t e z_\lambda ds
 =\int_0^t z_\lambda^2ds+p_\lambda(t)^2/(2\lambda)\ge0
\]

for \(\lambda>0\); the zero-rate contribution is \(\int e^2\). Thus

\[
 \tfrac12|e(t)|^2+\mu\|e\|_{L^2(0,t)}^2
 \le\tfrac12\delta^2+R_t\|e\|_{L^2(0,t)},
\]

where \(R_t=\zeta\|\dot q\|_{L^2(0,t)}+\gamma\sqrt t\), plus any properly included residual norm. Consequently

\[
 |e(t)|\le\sqrt{\delta^2+R_t^2/(2\mu)},
 \quad
 \|e\|_{L^2(0,t)}\le
 \frac{R_t+\sqrt{R_t^2+2\mu\delta^2}}{2\mu}.
\tag{17}
\]

The model storage identity implies

\[
 \|\dot q\|_2^2\le |V'(x_r)-c|^2/\mu+\|f\|_2^2.
\tag{18}
\]

This route remains useful when only an energy budget on the drive is available. Unlike (15), its initialization term includes \(\sqrt T\).

## 6. One confidence event and later queries

Let \(\mathcal E_K\) be the acquisition event establishing (9), \(\mathcal E_g\) the finite-bin event (5), and \(\mathcal E_h\) any probabilistic tracking/readout event. Their intersection has probability at least \(1-\alpha_K-\alpha_g-\alpha_h\), by a union bound. No independence is required.

On that one event, equations (6), (15), and (16) hold **simultaneously for every** later bounded force history on the fixed horizon. The force may be chosen after inspecting the fitted model and acquisition data. An optimizer can issue any number of counterfactual force queries without spending another confidence probability. The same guarantee applies pathwise to a realized force generated adaptively from physical observations when that identical force is supplied to the predictor.

This does not automatically transfer the law or trajectory of an arbitrary separately simulated feedback controller. A discontinuous controller can change its action by order one after an arbitrarily small state error. For a bounded causal policy with sup-history Lipschitz gain \(\kappa<\mu\), the comparison proof instead gives

\[
 \sup_t|x(t)-q(t)|\le
 \max\left\{\delta,
 \frac{\zeta D_*+\gamma+\rho_*}{\mu-\kappa}\right\},
\tag{19}
\]

when the histories supplied before deployment agree. Here \(D_*\) is a certified maximum slope of the actual numerical path. For an exact model, take \(\rho_*=0\) and \(D_*=D_v\); for a direct numerical-residual argument, an a priori alternative is (16) recomputed with effective forcing bound \(F+\rho_*\). At a first global error maximum the policy discrepancy is at most \(\kappa\) times that maximum. The rigorous comparison follows the same positive-kernel argument. A memoryless one-sided Lipschitz/dissipativity bound is another sufficient condition.

For ordinary planning, if \(J(f,x)\) is \(L_J\)-Lipschitz in the trajectory sup norm, a model-optimal force within optimization tolerance \(\epsilon_{\rm opt}\) is within \(2L_J\epsilon+\epsilon_{\rm opt}\) of the true optimum over the admitted force class. A state constraint with Lipschitz constant \(L_c\) transfers if the model satisfies it with margin \(L_c\epsilon\).

### Restarts and actual history

A model queried from the original post-hold state needs no physical reset. For a later query initialized at the current physical coordinate, its memory must be replayed from the **actual** recorded past, not from an earlier hypothetical branch. For a pole \(\ell\), the update can use positions without differentiating noisy data:

\[
 \int_0^a e^{-\ell(a-s)}dx(s)
 =x(a)-e^{-\ell a}x(0)-\ell\int_0^a e^{-\ell(a-s)}x(s)ds.
\tag{20}
\]

A uniform position-record error \(\epsilon_p\) changes this quantity by at most \(2\epsilon_p\), independently of \(\ell\). The resulting force error is at most \(2B\epsilon_p\). The kernel error must cover all lags in the total physical past-plus-query horizon, and its residual charges the norm of the concatenated actual-past and proposed-future velocity.

If initialization is changed from \(x_r\) to the exact actual post-hold coordinate while the model starts with zero derivative-memory state, the initial force is \(g_r(u)-K(u)e_0\); the simple constant-force bound becomes \(\gamma+B\delta\). This is the valid 4Bδ alternative. The 3Bδ formula must not be reused after silently changing that initialization convention.

## 7. Explicit accuracy and physical costs

For a target trajectory tolerance \(\epsilon\), one safe allocation for an exact-model certificate is

\[
 \delta\le\min\{\epsilon,\mu\epsilon/(12B)\},\quad
 \eta\le\mu\epsilon/4,\quad
 H-b\ge\frac{4G(b+T)}{e\mu\epsilon},\quad
 \zeta D_v\le\mu\epsilon/4.
\tag{21}
\]

Then \(\gamma\le3\mu\epsilon/4\) and (15) gives error at most \(\epsilon\). Reserve an additional share if numerical execution or feedback amplification is included. If \(B=0\), omit the corresponding tracking restriction.

The final guard is finite but can be costly. A force-average noise target \(\eta\) requires \(b=O(\sigma_f^2\eta^{-2}\log(1/\alpha_g))\) under the stated sensor model. The hold then costs

\[
 H=O\!\left(b+\frac{G(b+T)}{\mu\epsilon}\right),
\]

in addition to acquisition and trap-entry time. Tracking stiffness scales as an inverse tracking tolerance. Sensor precision, sample count, actuator force, and control range are also paid. There is no claim that these costs are small in a particular laboratory. The construction removes a spectral-gap dependence; it does not remove dependence on initial energy, force budget, accuracy, or horizon.

For the finite trap, a simple force-amplitude bound during the hold is \(|V'(x_r)|+\kappa\delta+d_*\). Its squared-force integral is therefore at most \(H(|V'(x_r)|+\kappa\delta+d_*)^2\), plus the separately charged entrance transient. This is a force-resource bound, not a model of actuator electrical consumption. One can ensure \(H>b\) even in a zero-old-force case by choosing \(H=b+\max\{b,4G(b+T)/(e\mu\epsilon)\}\).

### The constant-bias hold scaling is necessary for this strategy

Even with exact knowledge of the old force, consider the one-mode function \(g(t)=G e^{-\lambda t}\). The best constant approximation on \([H,H+T]\) has sup error equal to half its total variation. Maximizing over \(\lambda\ge0\), attained at \(\lambda=\log(1+T/H)/T\), gives

\[
 \inf_c\sup_{H\le t\le H+T}|g(t)-c|
 \ge \frac G2\frac{T}{H+T}
 \left(\frac H{H+T}\right)^{H/T}
\]

for a worst-case admissible mode. As \(H/T\to\infty\), the right side is asymptotic to \(GT/(2eH)\). Thus a uniform constant-bias strategy requires \(H=\Omega(GT/\epsilon_g)\) at small force error \(\epsilon_g\). The derivative argument has the correct scale. This is not a lower bound against fitting the changing initial force, such as the alternative in `passive_extrapolation_companion.md`.

The kernel certificate is valid only on its acquired horizon. Extending deployment requires a new longer-horizon kernel certificate and a renewed initial-force variation budget, not a free extrapolation of the old statement.

## 8. Finite execution of the small model

For a piecewise linear numerical position with slope \(v\) on a step of length \(h\), each derivative-memory variable has the exact update

\[
 r_j(t+h)=e^{-\ell_jh}r_j(t)
 +\frac{1-e^{-\ell_jh}}{\ell_j}v,
\]

with the continuous zero-rate value \(r_j(t+h)=r_j(t)+hv\). This supports stable exponential updates even for fast poles. Interval evaluation of these filters, the known potential, and the supplied finite representation of the force produces a position-equation residual certificate. The comparison theorem then translates that residual into trajectory error.

The mathematical comparison covers measurable bounded inputs. A finite numerical implementation requires a finite representation, or a certified integration/evaluation oracle, for the requested input. It cannot evaluate an arbitrary unrepresented measurable function. No laboratory rate ceiling is assumed merely because the learned numerical representation has finitely many poles.

### Executed diagnostic

`verify_passive_initialization.py` tests the signs and constants on a scalar quartic potential with \(\mu=1.1\), total memory mass \(B=2\), and rates \(0,10^{-9},10^{-4},0.03,0.2,1,7,80\). The hold lasts \(250.3\), with tracking tube \(\delta=0.0015\), final bin length \(0.8\), and deployment horizon \(T=4\). The slowest positive mode retains \(0.9999997497\) of its initial value; the frozen mode retains all of it.

The finite-bin force identity agrees to numerical precision. The measured constant's worst future initial-force error is \(0.002829\), below the derived bound \(0.019222\). A positive perturbed kernel has an analytic atomwise \(L^1\) upper bound \(0.002266\). Zero drive, DC drive, smooth drive, and separately simulated Lipschitz feedback all satisfy their nonlinear trajectory bounds. The observed maximum trajectory error is \(0.001467\); conservative bounds range from \(0.022446\) to \(0.037823\).

The script also checks the companion Chebyshev approximation inequalities at integer and noninteger exponents. `passive_verification_results.json` records all outputs. These are numerical diagnostics of the proved bridge, not physical acquisition or formal verification of floating-point ODE integration.

## 9. Strong ordinary alternatives and honest scope

1. **Positive Prony embeddings and model reduction are established.** Baczewski and Bond (2013) already construct extended-variable integration for positive Prony kernels. Bockius et al. (2021) infer extended Markov models from velocity autocorrelation samples using a Prony variant and the positive real lemma. Finite exponential state realization itself is not a new operation.
2. **Kernel learning with error analysis is established.** Lang and Lu's *Learning Memory Kernels in Generalized Langevin Equations* (2026) uses regularized Prony correlation estimation followed by Sobolev-loss/RKHS kernel regression. Their *Error Analysis of Generalized Langevin Equations with Approximated Memory Kernels* (2026) gives stochastic trajectory perturbation results in weighted norms, including strongly convex potentials and more general kernels. Their equations and assumptions differ; this note does not claim to supersede their stochastic or long-time results.
3. **Nonzero-initial-state model reduction has its own literature.** Schröder and Voigt (2023) give balanced-truncation variants with a priori initial-value error bounds. Such methods can be much more efficient when a usable state-space realization and initial-state subspace are known. They must be compared on those resources, rather than treated as zero-initial-state methods only.
4. **Astra N1688 is a strong internal precursor.** Its accepted source at `../N1688_ACCEPTED_SOURCE.txt` already acquires a retained thermal apparatus through actual random-sign interventions and transfers full encoded-record laws to arbitrary bounded later causal feedback. Its matched charge-balanced high-pass interface excludes arbitrary DC tasks and unfiltered trajectories. The present endpoint earns a different conditional operation: unfiltered deterministic nonlinear position prediction, with a retained measured slow bias. It loses N1688's arbitrary-policy stochastic-TV guarantee and does not include thermal path simulation or unknown gain calibration.

The exact constitutive class remains restrictive: a known strongly convex observed potential coupled to an unknown positive relaxation bath. General metastable, active, inertial, nonreciprocal, oscillatory, or state-dependent memory systems are outside the proof. Broad physical identification and civilisation-level consequence remain unestablished. What is complete here is the deterministic no-reset bridge from an acquired kernel certificate and a finite force readout to reusable nonlinear trajectory bounds.

### Primary sources retrieved

* Quanjun Lang and Jianfeng Lu, *Error Analysis of Generalized Langevin Equations with Approximated Memory Kernels*: https://arxiv.org/html/2512.10256v1 and https://doi.org/10.1137/26M1837290 . The first-order model discussed in that paper is not the overdamped derivative-memory position equation used here; its Remark 1.1 explicitly distinguishes the overdamped limit.
* Quanjun Lang and Jianfeng Lu, *Learning Memory Kernels in Generalized Langevin Equations*: https://doi.org/10.1137/24M1651101 .
* Niklas Bockius, Jeanine Shea, Gerhard Jung, Friederike Schmid, Martin Hanke, *Model reduction techniques for the computation of extended Markov parameterizations for generalized Langevin equations*: https://arxiv.org/abs/2101.02657 and https://doi.org/10.1088/1361-648X/abe6df .
* Andrew D. Baczewski and Stephen D. Bond, *Numerical Integration of the Extended Variable Generalized Langevin Equation with a Positive Prony Representable Memory Kernel*: https://arxiv.org/abs/1304.6446 and https://doi.org/10.1063/1.4815917 .
* Christian Schröder and Matthias Voigt, *Balanced truncation model reduction with a priori error bounds for LTI systems with nonzero initial value*: https://doi.org/10.1016/j.cam.2022.114708 .

