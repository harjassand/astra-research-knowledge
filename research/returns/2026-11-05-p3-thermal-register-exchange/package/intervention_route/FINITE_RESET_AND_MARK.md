# Finite-time reset and exact soft marking without learning the hidden force

## Result and scope

This is a constructive answer to a concrete missing operation in P2's intervention-stream opening. For its calibrated harmonic hidden-force family, a finite active local instrument can implement a fresh kinetic Gaussian replacement, jointly with the prescribed sine arm and the final loaded physical state, without learning the hidden sector and without waiting for the slow mode to mix. The implementation uses finite signed position-pointer couplings, a finite pointer rotation, a fresh Gaussian actuator, and a finite controllable force pulse. It retains the source's original hidden configuration and old reference in the target law.

The target is the finite-time loaded channel `K_T C`, not an instantaneous momentum-only canonical swap. Here `C` replaces the initial momentum by an independent thermal Gaussian while preserving the initial position, conserved hidden sector, and old reference; `K_T` is ordinary source evolution for the declared execution time, with an explicit independent meter-backaction term. The useful arm is marked from the replaced momentum. All source dynamics after completion therefore agree with the declared ideal intervention, for every initial source/reference law, provided the relevant hardware preparations are independent. Arbitrary future adaptive experiments can be appended by data processing.

This does **not** invalidate P2's accepted entropy/waiting upper bound or its independent-trigger lower bound. It supplies an active competitor outside the latter's restricted policy class. Nor is it a universal nonlinear reset: known linear transfer coefficients, a constant hidden force during the operation, additive Gaussian Markov bath noise, fresh controllable pointer modes, and mechanical force access are substantive premises. No bridge to the Gibbs-network or quantum-memory classes is asserted.

The generic idea of Gaussian measurement followed by feedback is established machinery. Milburn and Shrapnel's *Classical and Quantum Causal Interventions* (2018), Sections 4–5 and Appendix A, already treat measurement/control kernels, Gaussian momentum measurements, conditional impulses, apparatus entropy, discarded records, noise, and work. The missing operation addressed here is a **finite-window instrument whose measurement error is independent of the complete retained endpoint**, followed by an exact hidden/reference-preserving reset and arm channel. An abstract instantaneous measurement or an MSE estimate alone does not provide that interface.

Primary comparison: https://pmc.ncbi.nlm.nih.gov/articles/PMC7513211/ ; DOI https://doi.org/10.3390/e20090687 . The original P2 comparison already credits this paper. The present construction should not be advertised as the discovery of feedback cooling, Gaussian preparation, or thermodynamic intervention costs.

## 1. Source and required joint law

Let `S=(x,p)^T`, `B=(0,1)^T`, and

\[
A=\begin{pmatrix}0&1/M\\-k&-\gamma\end{pmatrix},
\qquad k=M\lambda\nu,\qquad \nu=\gamma-\lambda,
\qquad0<\lambda\le\gamma/2.
\]

During the operation,

\[
dS_t=(AS_t+BfZ+Bu_t)dt+
B\sqrt{2\gamma\sigma^2}\,dW_t.
\]

The hidden variable `Z` is conserved during the operation. Its value and the joint law of `(x_0,p_0,Z,R)` can be unknown and non-Gaussian. `R` contains arbitrary old classical reference data. The coefficients `M,k,gamma,sigma` and the force-coupling calibration are supplied or acquired with stated errors. The constant force amplitude itself need not be learned: the pulse cancels every constant force, with any moment or range envelope needed for resource certification retained separately. The new Brownian increments and fresh prepared apparatus are independent of this initial joint law. For P2's fixture, `f=kd`.

The target first draws

\[
\zeta\sim N(0,\sigma^2),\qquad
\zeta\perp(x_0,p_0,Z,R),
\]

replaces `p_0` by `zeta`, and later supplies a binary arm with

\[
a(\zeta)=\frac{1+\eta\sin(\zeta/\sigma)}2,
\qquad0<\eta<1.
\]

The desired endpoint is the source evolved under the specified loaded channel `K_T`. The arm is withheld until the fixed completion time `T`. Intermediate continuous meter values and bath trajectories are not retained as experiment outputs. The controller is isolated and reset or discarded into a declared sink before it can influence another trial.

## 2. Exact task-specific marking through Gaussian imprecision

Suppose a meter supplies `Y=u+E`, where `E~N(0,v)` is independent of `(u,S_final,R)` (or satisfies the equivalent conditional independence for each fixed prehistory). Then

\[
b_v(Y)=\frac{1+\eta e^{v/(2\sigma^2)}\sin(Y/\sigma)}2
\]

implements the exact arm instrument `a(u)`, jointly with the retained final state, whenever

\[
v\le2\sigma^2\log(1/\eta).
\]

Indeed, Gaussian convolution attenuates the sine by `exp[-v/(2 sigma^2)]`; the displayed amplitude compensates it. This is a task-specific garbling of the noisy observation, an elementary instance of Blackwell's comparison-of-experiments framework. It does not recover an arbitrary exact real value from a noisy observation.

The bound is sharp for a single Gaussian observation and all real `u`. Every randomized classical output has some measurable success probability `b(y)` in `[0,1]`. If Gaussian convolution of `b` equals `a`, its unique bounded solution is the displayed `b_v`. To see uniqueness directly, the difference of two bounded solutions has zero Gaussian convolution. Multiplying it by `exp[-y^2/(2v)]` gives an integrable function whose bilateral Laplace transform vanishes on the real line. That transform is entire, so its Fourier transform vanishes as well, and the difference is zero almost everywhere. If the amplitude exceeds one, the unique solution is not probability-valued.

This sharp bound concerns the specified interface. It is not a lower bound against multiple observations, different physical meters, or different finite-window controls.

Crucially, marginal unbiased marking is insufficient. If `E` also perturbs or reveals the retained source endpoint, the joint instrument need not be correct. The next construction earns the required independence physically.

## 3. A finite signed pointer pulse with independent endpoint error

### 3.1 Pulse design by a Hermite polynomial

Fix a meter duration `H>0`. Construct the unique polynomial `phi` of degree at most 13 satisfying

\[
\phi(0)=\phi'(0)=\phi''(0)=0,\quad
\phi'''(0)=1,\quad \phi''''(0)=0,
\]

\[
\phi^{(5)}(0)=\lambda^2+\nu^2,\quad
\phi^{(6)}(0)=0,\quad
\phi^{(j)}(H)=0\quad(0\le j\le6).
\]

Set

\[
h=D(D+\lambda)(D+\nu)\phi,
\qquad
g=M D(D^2-\lambda^2)(D^2-\nu^2)\phi.
\]

Equivalently,

\[
g=M(h''-\gamma h'+\lambda\nu h).
\]

The endpoint conditions imply

\[
h(0)=1,\quad h'(0)=\gamma,\quad
h(H)=h'(H)=0,
\quad g(0)=g'(0)=g(H)=g'(H)=0.
\]

The coupling thus has finite peak and slew and is continuously differentiable when joined to zero outside its window.

Three integrations by parts give

\[
\int_0^H h(s)\,ds=
\int_0^H h(s)e^{\lambda s}\,ds=
\int_0^H h(s)e^{\nu s}\,ds=0.
\]

At the critical case `lambda=nu`, differentiating the repeated-root identity also gives
`integral s h(s) exp(lambda s) ds=0`, exactly the additional condition needed for the Jordan-block response. The construction remains regular as `lambda` tends to zero. Five integrations by parts likewise give

\[
\int_0^H g(s)e^{as}\,ds=M a,
\qquad a\in\{0,\lambda,\nu,-\lambda,-\nu\}.
\]

These identities follow algebraically; numerical quadrature below checks their implementation, not their validity. The actual coefficients can be compiled directly from `gamma` and `k/M`, since `lambda^2+nu^2=gamma^2-2k/M` and `lambda^2 nu^2=(k/M)^2`; extracting nearly coincident eigenvalues is unnecessary. The same real polynomial construction also works for an underdamped harmonic well, with conjugate roots and the corresponding sine/cosine endpoint kernels. Its short-window costs then depend on the supplied oscillator-frequency scale as well as `gamma`; the uniform soft-mode statement above concerns P2's overdamped family.

### 3.2 Signal and endpoint independence

Let `x_free(t)` be the source position with the pointer force omitted but the same source initial condition and Brownian path. Duhamel's formula and the adjoint Green equation give

\[
\int_0^H g(t)x_{\rm free}(t)dt
=p_0+\sqrt{2\gamma\sigma^2}\int_0^H h(s)dW_s.
\]

The coefficient of `x_0` is `M[-h'(0)+gamma h(0)]=0`. The coefficient of the unknown constant force `fZ` is `integral h=0`. The coefficient of `p_0` is `h(0)=1`. Thus the pulse cancels both the unknown initial position and the unknown force, without estimating either.

Call the bath-noise integral `E_b`. Its covariance with the final two-dimensional source innovation is

\[
\operatorname{Cov}(E_b,N_H)
=2\gamma\sigma^2\int_0^H h(s)\,[e^{A(H-s)}B]^Tds=0.
\]

For distinct roots, the two endpoint kernels are linear combinations of `exp(lambda s)` and `exp(nu s)`; for the repeated root they are combinations of `exp(lambda s)` and `s exp(lambda s)`. The pulse identities therefore establish zero covariance in every case. Joint Gaussianity makes `E_b` independent of `N_H`. It is already independent of every initial source/reference variable.

This is the central finite-window operation: a generic noisy derivative estimator does not have this property.

### 3.3 Canonical pointer realization and self-backaction removal

Use a fresh canonical pointer `(Q,P)` with independent centered Gaussian initial coordinates of variances `v_Q,v_P`. During the pulse it is free with finite mass `m_d`, and apply

\[
H_{\rm int}(t)=-G g(t)xP.
\]

The pointer momentum is constant and the source receives the force `G g(t)P`. Write

\[
c_g=\int_0^H h(s)g(s)ds,
\qquad C=H/m_d-G^2 c_g.
\]

The exact pointer endpoint is

\[
Q_H=Q_0+C P-G(p_0+E_b).
\]

After detachment, read or route the quadrature `Q_H-C P`. Then

\[
Y=-\frac{Q_H-C P}{G}=p_0+E,
\qquad E=E_b-Q_0/G,
\]

\[
v=\operatorname{Var}(E)
=2\gamma\sigma^2\int_0^H h(s)^2ds+v_Q/G^2.
\]

`E` is independent of `(S_0,Z,R,P,N_H)`, hence of the full loaded source endpoint `S_H` jointly with the old reference and hidden sector. Fresh bath evolution during later detached-pointer operations preserves that independence.

A correlated Gaussian pointer is also allowed. Replace `Q_0` by its Gaussian residual `Q_0-Cov(Q_0,P)P/v_P`, add the known regression coefficient to `C`, and use the corresponding Schur-complement variance.

No instantaneous momentum-only canonical swap is used. Such a swap with `x'=x,p'=P` would violate the source Poisson bracket. The present meter deliberately has a finite, explicitly retained source-backaction channel.

### 3.4 The pulse can meet any fixed soft-mark noise threshold

In scaled coordinates `r=t/H`, write `phi(t)=H^3 Phi(r)`. The 14 Hermite coefficients of `Phi` depend polynomially on `H^2(lambda^2+nu^2)` and remain bounded for bounded `gamma H`, uniformly over `0<=lambda<=gamma/2`. Consequently

\[
\int h^2=O(H),\quad
\|g\|_\infty=O(M/H^2),\quad
\|g'\|_\infty=O(M/H^3),\quad
\int g^2=O(M^2/H^3).
\]

As `H` decreases, the scaled `h` approaches

\[
h_0(r)=(1-r)^4[1+4r+10r^2+20r^3
-7315r^4+27104r^5-24024r^6].
\]

The exact constants are

\[
\int_0^1h_0^2dr=\frac{41440}{46189}\simeq0.8971833,
\qquad
\int_0^1(h_0'')^2dr=\frac{48384000}{2431}\simeq19902.9206.
\]

Thus the bath part of the meter variance is asymptotic to
`1.7943666 gamma sigma^2 H`. A finite `H` and finite pointer variance can meet any strictly positive prescribed noise allowance. Faster operation requires larger finite coupling, slew, force action, and suitable pointer preparation; none of these is free.

## 4. Exact reset and exact arm, using finite feedforward

The following is a general Gaussian interface lemma.

Suppose a finite loaded source channel has the representation

\[
S_T^{\rm base}=e^{AT}S_0+F_T Z+N_T,
\]

and the meter supplies `Y=p_0+E` with `E~N(0,v)` independent of `(S_0,Z,R,N_T)`. Assume a controlled finite force can add any displacement proportional to `d=e^{AT}B` at the endpoint. If `v<sigma^2`, draw an independent fresh Gaussian

\[
\xi\sim N(0,\tau^2),\qquad \tau^2=\sigma^2-v,
\]

and add the endpoint displacement `d(xi-Y)`. Then

\[
S_T=e^{AT}(x_0,\zeta)^T+F_TZ+N_T,
\qquad \zeta=\xi-E\sim N(0,\sigma^2),
\]

with `zeta` independent of `(x_0,p_0,Z,R,N_T)`. This is exactly `K_T C`, including every old hidden/reference correlation.

For the arm, use the fresh actuator coordinate alone:

\[
b(\xi)=\frac12\left[1+
\eta\exp\!\left(\frac{v}{2\tau^2}\right)
\sin\!\left(\frac{\sigma\xi}{\tau^2}\right)\right].
\]

Since

\[
\xi\mid\zeta\sim
N\!\left(\frac{\tau^2}{\sigma^2}\zeta,
\frac{v\tau^2}{\sigma^2}\right),
\]

the conditional arm probability is exactly `a(zeta)`. This is a valid randomized decision precisely when

\[
\eta e^{v/[2(\sigma^2-v)]}\le1,
\quad\text{equivalently}\quad
v\le\frac{2\log(1/\eta)}{1+2\log(1/\eta)}\sigma^2.
\]

The latter bound is sharp even if the arm algorithm may use both available numerical records `(Y,xi)`, when the required equality holds for every initial momentum and its retained reference. To prove this, condition on `zeta,p_0`, and put `d=p_0-zeta`. Then `Y=xi+d`. For every `d`, the success function `b_d(q)=b(q+d,q)` must have the same Gaussian convolution, namely `a(zeta)`, under the displayed conditional law of `xi`. Gaussian convolution is injective, so every `b_d` is the same unique corrected sine function. If its amplitude exceeds one, no randomized postprocessing of these two records succeeds. Equality of the final loaded source/arm law imposes the same condition: convolution by its independent Gaussian source noise is injective along the nonzero endpoint direction `e^{AT}B`. This is an interface-specific impossibility result, not a bound on machines with additional meters, observations or actuators.

Because `N_T` is independent of both `xi` and `E`, the equality is an equality of the complete joint law `(S_T,Z,R,arm)`, not just an equality of the marginal momentum or the marginal arm frequency.

### 4.1 A smooth finite mechanical force implements the displacement

Let the detached pointer rotation take time `D`, and then use a force window of length `L`, so `T=H+D+L`. Put `s=0` at the start of this last window and let `w(s)=sin^2(pi s/L)`. Define

\[
W_w=\int_0^L w(s)e^{A(L-s)}BB^Te^{A^T(L-s)}ds.
\]

The pair `(A,B)` is controllable, so `W_w` is positive definite for every `L>0`. The continuously differentiable finite waveform

\[
f(s)=w(s)B^Te^{A^T(L-s)}W_w^{-1}e^{AT}B
\]

has zero value and slope at both endpoints. Apply

\[
u(s)=f(s)(\xi-Y).
\]

Direct integration gives `integral e^{A(L-s)}Bu(s)ds=d(xi-Y)`, as required. Its expected squared-force action is

\[
\mathbb E\int_0^L u^2 ds
=\kappa_f[\mathbb E(p_0^2)+\sigma^2],
\qquad \kappa_f=\int_0^L f(s)^2ds.
\]

The simplification follows because `xi-Y=zeta-p_0` and the refreshed `zeta` is independent of the complete old source state. It requires only a finite kinetic second moment, not a Gaussian prior or inference of `Z`.

### 4.2 Analog implementation avoids a free perfect digital measurement

The fine value `Y` need not be digitized. A detached finite harmonic rotation converts the known meter quadrature into an actuator momentum, up to a known scalar. For a simple plateau of frequency `Omega`,

\[
P_\theta=P\cos\theta-m_d\Omega Q_H\sin\theta.
\]

Choose its direction so that `a_d P_theta=-(Q_H-C P)/G=Y`. Equivalently, `cot(theta)=C m_d Omega`, with the appropriate positive scale `a_d`. Finite smooth trap ramps can be included in the known two-dimensional symplectic transfer matrix; varying the plateau phase covers every quadrature direction. Their duration and work are paid.

After rotation, release the actuator's position trap. Its momentum remains constant under its finite free kinetic Hamiltonian and a source coupling proportional to `x P_theta`. A second fresh free actuator momentum supplies `xi`. The two mechanical interactions

\[
H_{\rm feed}(s)=-x f(s)(\xi-Y)
\]

therefore supply the exact force above while their controlling momenta remain constant. This is a finite classical Hamiltonian realization of the linear feedforward; it is not an ideal impulse, a momentum-only canonical swap, or an unpriced exact ADC.

Only the final bounded arm probability needs classical coin logic. A further independent Gaussian error in reading `xi` can itself be compensated, provided the remaining probability margin permits it. Finite quantization and coin bits are separately charged below.

## 5. Explicit loaded channel and useful endpoint

The source effect of the measurement pulse has a particularly simple endpoint form:

\[
G P\int_0^H e^{A(T-s)}Bg(s)ds
=-GM e^{AT}AB\,P.
\]

Indeed, `g` acts as `M` times differentiation at zero on the two-dimensional exponential response space. Therefore

\[
N_T=-GM e^{AT}AB P+
\sqrt{2\gamma\sigma^2}\int_0^T e^{A(T-s)}B\,dW_s.
\]

Its covariance is completely explicit:

\[
\Sigma_T=G^2v_P M^2e^{AT}ABB^TA^Te^{A^TT}
+2\gamma\sigma^2\int_0^T e^{As}BB^Te^{A^Ts}ds.
\]

In particular, shrinking the meter window raises its transient force action but does not force its final source-backaction covariance to diverge. This distinction must not be mistaken for free transient control.

The resulting intervention has a concrete observable output. It gives equiprobable arms and

\[
\mathbb E[p_T\mid\mathrm{arm}=1]
-\mathbb E[p_T\mid\mathrm{arm}=0]
=2\eta\sigma e^{-1/2}[e^{AT}]_{pp}.
\]

All old source, hidden-sector, and reference terms, as well as the loaded noise, are independent of the arm. For `0<T<2/gamma`, the response coefficient is strictly positive for every `0<lambda<=gamma/2`. More specifically,

\[
[e^{AT}]_{pp}\ge
e^{-\gamma T/2}(1-\gamma T/2)
\quad (0\le T\le2/\gamma).
\]

To check the bound, write the coefficient as
`exp(-y)[cosh(ry)-sinh(ry)/r]`, with `y=gamma T/2` and `r=(nu-lambda)/gamma`; its even-power expansion is at least `exp(-y)(1-y)` when `0<=y<=1`. The critical case is the continuous limit `r=0`.

Thus a small fixed execution time retains a fixed useful arm-linked kinetic response even as the hidden relaxation time `1/lambda` diverges. It has not obtained this result by parking the useful system indefinitely or learning the hidden force sign.

## 6. Physical costs, finite range, reuse, and uncertainty

### 6.1 The actual cost vector

For each trial the ledger includes the source execution time `T`; pointer and actuator preparation and disposal; finite trap ramps and quadrature rotation; the two source coupling waveforms; peak force, coupling and slew; source and pointer aperture; actual mechanical work; finite readout/coin computation; and isolation and reset before reuse.

The meter force action is

\[
\mathcal A_m=G^2v_P\int_0^H g^2dt,
\]

and the feedforward action is the formula in Section 4.1. These are force-action resources, not automatically thermodynamic work. For couplings that vanish at their endpoints, the net switching work equals the mechanical force work `integral u p/M dt`. Hence

\[
\mathbb E|W|\le
\sqrt{\mathbb E\int u^2dt}\,
\sqrt{\mathbb E\int (p/M)^2dt}.
\]

The source momentum second moments during the finite linear protocol are computable from its transfer matrices and declared initial moment bounds. Restoring pointer traps and resetting the resulting information-bearing controllers require their additional actual work and heat disposal. A relative-entropy free-energy quantity is only an accounting lower bound unless a physical reset construction is supplied.

The accepted finite-pointer companion already supplies an explicit isolated harmonic Langevin reset. From a pointer with normalized second moment `E_d`, choosing contraction `rho` gives joint pointer/reference TV at most `rho sqrt(E_d+1)/2`. Critical damping supplies `rho<=2 exp(-omega_d t/2)`, so per-use reset accuracy `delta` costs a finite contact time `O(omega_d^-1 log[(E_d+1)/delta])`, in addition to the actual thermal resource, trap operations, damping hardware, and disposal. Reusing that construction is an earned interface; it is not a blank register assumption.

### 6.2 Finite bounded Hamiltonians

The algebra above uses bilinear `xP` interactions. To make their interaction energies globally bounded, replace them by smooth saturations `chi_x(x) chi_P(P)` that equal `xP` on a declared finite operating box, have derivatives bounded by one, and have bounded magnitude. On the event that the raw linear source and pointer path stay inside the box, the saturated and raw evolutions coincide exactly. A coupling-until-first-exit argument therefore bounds their entire output-law TV by the charged exit probability.

For a single pulse, finite peak interaction energy is at most
`G ||g||_infty X_cap P_cap`, finite peak force is at most
`G ||g||_infty P_cap`, and absolute switching work has the pathwise bound
`G X_cap P_cap integral |g'|`. The analogous formulas apply to each feedforward actuator. These conservative capacity bounds are distinct from the smaller possible net-work bill.

Moment bounds give a fully finite, though potentially large, aperture. For Gaussian initial data in the harmonic hard family, Gaussian path tails permit apertures growing as `sqrt(log(n/delta))` at fixed physical variances. For arbitrary initial laws with only second moments, Markov bounds require larger apertures and must be retained rather than silently replaced by Gaussian tails.

As in P2's hard family, the original source position width and displacement grow as `lambda^-1/2`. This spatial range remains a physical resource. Peak coupling energy capacity and transient free-pointer travel can inherit that dependence even where endpoint kinetic variances, source force action, and source net-work bounds remain finite. The construction does not establish a fixed-range result by letting `lambda` vanish.

### 6.3 Precision, classical validity, and useful disturbance

Let `v_m=v_Q/G^2` be the pointer-position contribution to the meter variance. Then

\[
v_m\mathcal A_m=v_Qv_P\int g^2.
\]

A quantum-valid apparatus cannot violate `v_Qv_P>=hbar^2/4`; a genuinely classical pointer needs phase-space spreads safely above that scale. Consequently small meter variance and arbitrarily small source force action cannot be obtained simultaneously at fixed hardware and action scale. The finite classical construction is meaningful only when the selected resources lie inside the classical regime. This is a compatibility condition, not a derived quantum extension of the classical source theorem.

The declared endpoint is loaded. If the objective instead requires agreement with the completely unmetered source path, the additional force path can be compared by the accepted Girsanov bound, and its force action must enter the campaign discrepancy. Fixed nonzero load cannot be declared harmless for every unmodified physical task. Here the useful endpoint is explicitly the loaded response calculated in Section 5.

### 6.4 Campaign composition and finite implementation

In the ideal calibrated Gaussian-interface model, each reset-and-mark kernel is exact conditional on any past history. Consequently an arbitrarily long adaptive campaign of such operations has **zero replacement/marking discrepancy**, with a linear number of fixed-duration source operations. There is no `n v` imprecision term. The kinetic moment cost can vary with the actual experiment; it is `sum_j kappa_f(E p_{0,j}^2+sigma^2)`, not automatically a constant times `n` without a supplied moment ledger.

For finite preparation, saturation and control errors, a conservative hybrid argument gives whole-campaign TV at most the sum of the per-operation kernel errors. The Gaussian pointer/actuator resets therefore use per-operation accuracy `O(epsilon/n)`, yielding `O(n log(n/epsilon))` serial bath-contact time when their post-use energy moments are uniformly bounded. Parallel preparation trades clock time for a larger apparatus inventory.

A quantization error `delta_xi` in the fresh-actuator readout changes the arm probability by at most
`[eta exp(v/(2tau^2)) sigma/(2tau^2)] delta_xi`; finite coin precision contributes its own uniform probability error. With a strict arm margin, chain-rule KL gives a sum of squared per-trial probability errors, so `O(epsilon/sqrt(n))` accuracy suffices for these binary-only errors. The required number of readout/coin bits is logarithmic in `n/epsilon`, with an additional range term. Analog feedback avoids a free exact digitization of the source meter value.

Coefficients, covariance, pulse gain, and analog rotations must be calibrated. If a common scalar meter-variance estimate differs by `Delta v`, the compensated probability changes smoothly; it is not immune to calibration error. More generally the finite linear source/controller gives explicit mean and covariance matrices smooth in all finite parameters. On a compact certified parameter neighborhood with nondegenerate endpoint covariance and a strict probability margin, conditional Gaussian KL supplies a computable bound of the form

\[
D_{\rm campaign}\le C\|\Delta\theta\|^2
\sum_j(1+\mathbb E\|S_{0,j}\|^2+\mathbb E Z_j^2)
\]

plus the separately paid preparation, clipping, numerical and coin terms. This follows by conditioning on the arbitrary initial state and comparing the finite Gaussian endpoint extensions; it does not compare singular continuous path laws with different diffusion constants. The constant is determined by the displayed transfer matrices and covariance eigenvalue bounds.

Thus a learned-parameter capability must acquire a certificate at the precision required by the desired campaign length and pay its actual Fisher information, laboratory time, forcing, and metrology costs. The exact known-coefficient theorem is already a valid counterexample to a universal intervention lower bound based solely on the hidden-force inference time. It is not an automatic theorem that arbitrary unknown nonlinear plants can be acquired or controlled at the same cost.

## 7. Numerical certificate and interpretation

`finite_reset.py` builds the degree-13 Hermite pulse, verifies all moment conditions and endpoint-noise orthogonality, computes the smooth controllability-Gramian force, and checks the conditional sine integral. It uses 65-digit arithmetic. The saved output covers `lambda=0.2`, the critical case `lambda=0.5`, and the soft case `lambda=10^-8`, all with `M=gamma=sigma=1`, `H=0.05`, detached delay `0.05`, force window `0.1`, `eta=0.5`, `G=1`, `v_Q=0.1`, and `v_P=10^-10`.

For `lambda=0.2`, the meter variance is approximately `0.1897204`, the fresh actuator variance is `0.8102796`, and the compensated arm amplitude is `0.5620996`, leaving a probability margin approximately `0.21895`. The useful final momentum arm contrast is approximately `0.494886`. The feedforward force-action coefficient is approximately `561.617` per unit of `E p_0^2+sigma^2`; the meter action is approximately `0.015923`. The selected pulse's coupling peak is roughly `1.05e5` and slew roughly `2.83e7` in these normalized units. Those large finite constants are part of the example, not hidden behind the asymptotic statement.

A second operating point trades a longer useful delay for substantially lower force resources. With `H=0.2`, detached delay `0.05`, `L=0.5`, and `v_P=10^-8`, the total execution time is `0.75`, the meter variance is approximately `0.459007`, the corrected arm amplitude is approximately `0.764204`, and the useful momentum contrast is approximately `0.269813`. The feedforward action coefficient falls to approximately `38.0529`, while the meter action is approximately `0.0248911`, coupling peak approximately `6578.67`, and slew approximately `442194`. These are concrete feasible points in a resource tradeoff, not an asserted optimal design.

Across all four cases, the algebraic endpoint identities have numerical residuals below `2*10^-54`; this checks implementation and signs. It is not an experimental validation, an acquisition procedure for a real material, or a claim that the selected normalized hardware numbers are attractive. The main scientific conclusion is the exact channel construction and its resource boundary: **a hidden slow force can obstruct inference while a known finite linear interface still permits a complete local reset and useful arm experiment without learning that force**.

## 8. What remains and what this changes in the question selection

The P2 question should not seek a universal quadratic campaign lower bound from the harmonic hidden-force witness alone. This witness admits the finite active construction above when the declared local linear controls and fresh pointer resources are available. Its independent-trigger lower bound and whole-campaign entropy upper bound remain correct at their original scopes.

The strongest equally informed method pursuing the same intervention can use this controller too. In particular, a model-based predictor supplied the same calibrated linear coefficients can compute the reset kernel and the useful arm contrast without learning the hidden sign. This result is an active-operation bypass of a passive waiting bottleneck, not a method-exclusive separation between direct decisions and every possible predictor. An absolute forecast of the hidden sector is a different task and retains its own inference cost.

The strongest next lower-bound question would have to specify the actuator class, force-action/energy/space/precision budgets, and useful endpoint tightly enough to exclude or price this route. Conversely a broad positive capability would have to construct the endpoint-independent measurement and reachable compensation interfaces in a nonlinear or constrained apparatus, rather than extrapolate this harmonic solution. Merely asking for more generality earns no further conclusion. The present note supplies the decisive attaining operation for the actual calibrated hidden-force class and leaves its full cost vector visible.
