# A reciprocal wave counter with finite native response

30 October 2026. Complementary constructive supplier. Ordinary passive wave-network machinery supplies a stronger comparison than chiral memory at the Gaussian heat/current objective. No invention of LC lines, Langevin fluctuation-dissipation, momentum reversal, or constrained transport is asserted. The exact ports, initialization, losses and output current are part of the result.

## 1. Actual operation and measured current

On the periodic N-site ring put `(Bv)_i=v_(i-1)-v_i`. The native visible field x is a signed harmonic density with zero sum, not a binary occupation. Its actual integrated branch current is `J(t)=int_0^t v(s)ds`. Introduce auxiliary storage q and momentum/flux p, with equations

\[
\begin{aligned}
dx&=Bv\,dt,\\
dq&=(g_Nv-aB^*p)dt,\\
dp&=aBq\,dt-B\Gamma B^*p\,dt+\sqrt2 B\sqrt\Gamma\,dV,\\
\tau dv&=-(B^*x+g_Nq)dt-Rv\,dt+f(t)dt+\sqrt{2R}\,dW.
\end{aligned}                                                    \tag{1}
\]

Here a,tau>0 are fixed, `kappa_N=g_N^2`, and R and Gamma are frozen diagonal reciprocal coefficients. Assume `0<r_-<=R_ii<=r_+` and `0<=Gamma_ii<=gamma_+`. Independent local bath innovations W,V are supplied at the same temperature, normalized to one. The auxiliary loss is explicitly **relative-momentum loss**, with matched gradient noise. Its sum is zero on every realization. A grounded friction on each p_i is a different operation and is analyzed in Section 10.

The full native stochastic impedance law in (1), including its response to the actual load `B^*x+g_N q`, is a supplied port. It does not follow from equilibrium weights or an arbitrary hidden jump-operation library. R and Gamma need not be numerically learned. Their future conditional laws and frozen status are actual premises.

The force f is a native physical force/voltage port with power `f^T v`; set f=0 for the unforced path theorem. All reaction forces affect the measured v. Every coupling has range one. Local frequencies and the current response time `tau/R_ii` remain bounded independently of N. No controller reads the bath noise or reacts at the collective event rate.

The chosen output is current in the **native ring**. The auxiliary momentum/flux is a separately specified apparatus channel. If an application instead measures native plus apparatus mass/charge displacement, that enlarged output must include the apparatus channel and is not suppressed by the theorem. A reciprocal transducer can exchange energy without transferring native particles into that channel. The native continuity law counts all native displacement.

## 2. Passivity, momentum reversal and initialization

Set

\[
E=\tfrac12(\|x\|^2+\|q\|^2+\|p\|^2+\tau\|v\|^2),
\qquad K=B\Gamma B^*.
\]

The conservative terms cancel exactly. Ito's formula gives

\[
\begin{aligned}
dE={}&[-v^TRv-p^TKp+f^Tv+\operatorname{tr}R/\tau
+\operatorname{tr}K]dt\\
&+v^T\sqrt{2R}\,dW+\sqrt2 p^TB\sqrt\Gamma\,dV.                 \tag{2}
\end{aligned}
\]

This identifies reciprocal energy transfer, the actual force work and the two matched dissipative baths. Each local thermal power is finite. The strictly positive native inertia/inductance tau is retained, rather than treating a white current as a finite-response apparatus.

At zero force the exact invariant law is

\[
\mu_N=\gamma_{\{\sum x=0\}}(dx)\otimes\gamma(dq)
\otimes\gamma(dp)\otimes N(0,\tau^{-1}I)(dv).                   \tag{3}
\]

The constant p mode is conserved and decoupled; it may have a warranted Gaussian or fixed initial law. Reversibility is under

\[
\Theta(x,q,p,v)=(x,q,-p,-v),                                  \tag{4}
\]

not identity reversal of every variable. The earlier ordinary-reversible counter theorem does not silently extend to this inertial phase space.

Initialization is paid. Either warrant (3), or prepare a deterministic nonflat visible profile `x(0)=x_N^0` and independent thermal q,p,v according to (3). The latter is the regular conditional Gaussian preparation at the given visible value. It is not implemented by retaining a measured thermal realization and then ignoring its record. For retained calibration D, a conditional conclusion requires the actual preparation and future innovations conditional on `(D,R,Gamma)`. An averaged preparation error does not provide a rare-record guarantee.

The displacement-unit counter is `z=q/g_N`; its variance is `1/kappa_N`. The normalized storage has unit variance and unit quadratic stiffness. A hardware realization may pay growing compliance/capacitance or a weak reciprocal tap, with its accuracy and range. Coordinate normalization does not decide that engineering trade. In particular, it does not imply divergent equilibrium energy: each normalized quadratic degree has mean energy one half.

## 3. Exact current counting and whole-horizon rare tails

Because `1^T B^*=0`, all native currents, including their reaction-force changes, obey

\[
\boxed{J_{\rm tot}(t)=\sum_iJ_i(t)
=g_N^{-1}\sum_i[q_i(t)-q_i(0)].}                              \tag{5}
\]

Local counters also transport: `dq=g dJ-aB^*p dt`. Thus the previous frozen coordinate `x-Bq/g` is no longer conserved. This distinction is necessary for nonflat relaxation.

Under (3), for every frozen admissible R,Gamma,

\[
\operatorname{Var}J_{\rm tot}(t)\le4N/\kappa_N.                 \tag{6}
\]

The same covariance bound holds with deterministic x_N^0 and independent thermal auxiliaries: Gaussian conditioning reduces the covariance of every linear path functional. If `||x_N^0||^2<=CN`, deterministic energy contraction bounds the mean total current by `C' N/g_N` at every time.

Put `S(t)=sum q_i(t)`. At equilibrium its variance is N, and `S'=g sum v` gives

\[
\mathbb E|S(t)-S(s)|^2\le(\kappa_N N/\tau)|t-s|^2.              \tag{7}
\]

For the sharper long-time modulus, the passive spectrum bound proved in Section 5 also gives `Var[J_tot(t)-J_tot(s)]<=(2N/r_-)|t-s|`. Cover `[0,N^2T]` at this canonical-metric resolution and integrate the square root of the log covering number up to the variance diameter. The Gaussian entropy bound yields

\[
\mathbb E\sup_{t\le N^2T}|J_{\rm tot}(t)-\mathbb EJ_{\rm tot}(t)|
\le C_T\sqrt{\frac N{\kappa_N}
\log(2+N^2\kappa_N)}.                                         \tag{8}
\]

Borell's Gaussian inequality, with variance at most `4N/kappa_N`, now proves that if `kappa_N N^2 -> infinity`, then for every delta>0,

\[
\lim_{N\to\infty}\frac1N\log\mathbb P\left(
\sup_{t\le T}|J_{\rm tot}(N^2t)|/N^2>\delta\right)=-\infty.      \tag{9}
\]

Both the mean bound and the expected supremum are negligible compared with N^2. This is a rare-history statement, not only a CLT, and is uniform over the frozen heterogeneous reciprocal coefficients in the stated port.

For homogeneous `R=rI`, the zero mode is the damped oscillator

\[
dQ_0=g V_0dt,\qquad
\tau dV_0=-gQ_0dt-rV_0dt+\sqrt{2r}\,dW_0,
\quad Q_0=N^{-1/2}\sum q_i.                                   \tag{10}
\]

With canonical initialization its covariance c solves `tau c''+r c'+kappa c=0`, `c(0)=1,c'(0)=0`, and

\[
\operatorname{Var}J_{\rm tot}(t)=2N[1-c(t)]/\kappa_N.            \tag{11}
\]

The centered circulation CLT is suppressed as a whole path when `kappa_N N^2 -> infinity`: (8) divided by `N^(3/2)` is bounded by a constant times `sqrt(log(2+L_N)/L_N)`, where `L_N=kappa_N N^2`. In the homogeneous nonflat preparation its mean is zero as well. The uncoupled native finite-tau ring instead has variance asymptotic to `2N^3T/r` on the diffusive horizon. A constant circulating load charges the storage and is blocked at long times; steady force response is not retained for free.

## 4. Homogeneous receiver: exact slow pole and every other residue

Assume `R=rI`, `Gamma=gamma I`, with unknown r in a fixed positive compact interval and `0<=gamma<=gamma_+`. The path theorem is conditional on that fixed r; mixing unknown r values need not give a Gaussian law. For a nonzero Fourier mode use `b=e^(ik)-1` up to orientation, `ell=|b|^2`, and the energy-normalized coordinates `(x,q,p,u)`, `u=sqrt(tau)v`. The drift G satisfies

\[
G+G^*=-2(r/\tau)e_ue_u^*-2\gamma\ell e_pe_p^*,\qquad
G^*=\Theta G\Theta.                                          \tag{12}
\]

In particular `||exp(tG)||<=1`. Direct elimination gives

\[
P(\lambda)=
(\tau\lambda^2+r\lambda+\ell)
(\lambda^2+\gamma\ell\lambda+a^2\ell)
+\kappa\lambda(\lambda+\gamma\ell).                           \tag{13}
\]

### The density pole is uniform in the tap/wavelength ratio

Writing `lambda=ell z` gives

\[
\ell^{-2}P(\ell z)=
(\tau\ell z^2+r z+1)[a^2+\ell(z^2+\gamma z)]
+\kappa z(z+\gamma).                                         \tag{14}
\]

At `(ell,kappa)=(0,0)` the root `z=-1/r` is simple with derivative `a^2r`. The uniform implicit-function theorem therefore supplies a real, simple, negative root

\[
\lambda_s=-\ell/r+O(\ell\kappa+\ell^2),                       \tag{15}
\]

whose decay coefficient remains bounded above and below by positive constants. All constants are uniform in bounded gamma and in the stated r interval. No relation `kappa << |k|` is needed.

For orientation, when gamma=0 and ell first tends to zero, the two long-wave diffusion coefficients solve `kappa D^2-a^2rD+a^2=0`. The slow coefficient is

\[
D_s=\frac{2}{r+\sqrt{r^2-4\kappa/a^2}}=1/r+O(\kappa).          \tag{16}
\]

The other coefficient grows as `a^2r/kappa`. It must not be discarded at a fixed kappa merely by calling it an inertial mode.

### Initial transients and all omitted poles

Choose the right eigenvector h with `h_x=1`. Exact formulas are

\[
v=\lambda_s/b,\quad
q=\frac{g\lambda_s(\lambda_s+\gamma\ell)}
{b(\lambda_s^2+\gamma\ell\lambda_s+a^2\ell)},\quad
p=\frac{a g\lambda_s}{\lambda_s^2+\gamma\ell\lambda_s+a^2\ell},
\quad u=\sqrt\tau v.                                        \tag{17}
\]

Consequently `q=O(g sqrt(ell))`, `p=O(g)`, and `u=O(sqrt(ell))`. Momentum reversal makes the left eigenvector `Theta h/(h^*Theta h)`, with

\[
h^*\Theta h=1+|q|^2-|p|^2-|u|^2=1+O(\kappa+\ell).              \tag{18}
\]

The exact spectral projection P_s therefore satisfies

\[
(P_s)_{xx}=1+O(\kappa+\ell),\qquad
\|(I-P_s)e_x\|+\|(I-P_s)^*e_x\|
\le C(\sqrt\kappa+\sqrt\ell).                                \tag{19}
\]

Since P_s commutes with the full contraction semigroup,

\[
|e_x^*e^{tG}(I-P_s)e_x|
=|e_x^*(I-P_s)e^{tG}(I-P_s)e_x|
\le C(\kappa+\ell),\quad t\ge0.                              \tag{20}
\]

This controls every other pole and initial transient even if their individual residues are poorly conditioned. It does not presume mixing of an auxiliary sector. For the stationary visible covariance C, (15)--(20) prove

\[
\boxed{\sup_{t\ge0}|C_{\ell,\kappa}(t)-e^{-\ell t/r}|
\le C(\kappa+\ell).}                                        \tag{21}
\]

The exponential comparison is uniform in time because `sup_(u>=0) u exp(-c u)` is finite. The small-ell, small-kappa neighborhood is essential; a finite-size parameter choice outside it can have a complex pole pair rather than this real slow pole. The same matrix entry is the visible mean propagator from an initial visible mode with zero auxiliary means, so (21) also controls nonflat relaxation.

## 5. Passive impedance gives the needed path increment bound

For a stationary Fourier mode, eliminating the reactive coordinates gives the native velocity impedance

\[
Z_k(\omega)=r+i\tau\omega+\frac\ell{i\omega}
+\kappa\frac{i\omega+\gamma\ell}
{a^2\ell-\omega^2+i\gamma\ell\omega}.                          \tag{22}
\]

The auxiliary real part is

\[
\operatorname{Re}Z_{\rm aux}
=\frac{\kappa\gamma a^2\ell^2}
{(a^2\ell-\omega^2)^2+\gamma^2\ell^2\omega^2}\ge0.              \tag{23}
\]

All dissipative ports are at the same temperature. Eliminating their independent noises gives the exact fluctuation-dissipation spectrum

\[
S_v(\omega)=2\operatorname{Re}(Z_k(\omega)^{-1})\le2/r.         \tag{24}
\]

For gamma=0 this reduces to `2r/|Z|^2`, with purely reactive auxiliary load. The singular lossless frequencies are interpreted by limits. Native inertia gives high-frequency decay proportional to `omega^-2`. The bath still uses classical white-voltage noise; the result is a finite response roll-off, not an exact hard frequency cutoff.

Parseval yields the uniform increment estimate

\[
\mathbb E|x_k(t)-x_k(s)|^2
=\ell\operatorname{Var}\int_s^t v_k(u)du
\le(2\ell/r)|t-s|.                                          \tag{25}
\]

This supplies tightness without incorrectly treating the error floor in (21) as a modulus of continuity. Conditioning the initial visible field only reduces the covariance of these increments.

For heterogeneous R,Gamma, the auxiliary transfer is still passive. Its native matrix impedance has `Re Z(omega)>=R`, and all baths give `S_v=2 Re Z^(-1)`. Writing `Z=H+iX` with H positive and X Hermitian proves

\[
S_v=2(H+XH^{-1}X)^{-1}\preceq2R^{-1}\preceq(2/r_-)I.           \tag{26}
\]

Thus passivity also provides a heterogeneous quadratic-form increment bound; it does not by itself identify an unchanged heterogeneous mean heat equation.

## 6. Whole density paths and nonflat initialization

Let rho_0 be a smooth periodic zero-mean profile and prepare `x_N^0` by sampling it, with the independent thermal auxiliaries from Section 2. Embed the empirical density as `rho_N(t)=N^(-1)sum_i x_i(N^2t) delta_(i/N)`, or use its standard trigonometric discrete-Fourier embedding.

If `kappa_N -> 0`, the mean converges to the nonflat native heat evolution

\[
\rho_t=r^{-1}\rho_{xx},\qquad \rho(0)=\rho_0.                 \tag{27}
\]

For a finite Fourier profile this is (21). General smooth profiles follow by energy contraction and a Fourier-tail approximation. The native unknown r is retained; a known new diffusion constant has not been programmed without calibration.

The centered fluctuation field `Y_N=sqrt(N)(rho_N-E rho_N)` has convergent fixed-mode/time covariances by (21). Under deterministic visible initialization, Gaussian conditioning subtracts the product of the two visible initial-response entries from the stationary covariance. Hence its limiting field is

\[
dY=r^{-1}\partial_x^2Ydt+\sqrt{2/r}\,\partial_xd\mathcal W,
\qquad Y(0)=0.                                               \tag{28}
\]

A stationary visible initializer instead gives the stationary OU field. The two claims have different preparation premises.

On the macroscopic clock (25) gives, for every integer Fourier label k,

\[
\mathbb E|\widehat Y_N(k,t)-\widehat Y_N(k,s)|^2
\le C k^2|t-s|.                                              \tag{29}
\]

Mode variances are bounded by one. Sum against `(1+k^2)^(-p')`, with `p'>3/2`, and use Gaussian moments of arbitrarily high order. Kolmogorov/GRR gives a uniform positive time-Holder norm in `H^(-p')`. Compact spatial embedding into `H^(-p)` for `p>p'` proves tightness in `C([0,T],H^(-p))`. Thus (28) is whole-path convergence for every `p>3/2`. No individual auxiliary relaxation time was silently set to zero.

## 7. Gaussian rare-history consequence at the same task

The density path LDP at speed N follows by a Gaussian argument stronger than the CLT statement alone. Finite-dimensional covariance operators converge to (28). The uniform Holder/Sobolev estimates give a common positive-probability norm ball for these Gaussian paths; the Gaussian Fernique inequality then gives a uniform exponential square moment in a norm with relatively compact balls in the weaker path topology. Scaling by `N^(-1/2)` proves exponential tightness at speed N. Finite-dimensional Gaussian LDPs and projective limits identify the rate with the OU Cameron--Martin norm. The deterministic mean limit is (27).

Define the integrated native-current field by discrete Fourier coefficients

\[
\widehat Q_N(k,t)=N^{-2}\sum_i e^{iki}J_i(N^2t).
\]

Exact native continuity gives, at every nonzero mode,

\[
\widehat\rho_N(k,t)-\widehat\rho_N(k,0)=N b_k\widehat Q_N(k,t),  \tag{30}
\]

with the fixed incidence orientation. Thus its nonconstant part is a deterministic discrete inverse gradient of the density change. The inverse-gradient maps converge in the same weak Fourier/Sobolev topology. The constant current mode is superexponentially zero by (9) when `kappa_N N^2 -> infinity`.

The joint density/integrated-current LDP is consequently

\[
I(\rho,j)=\frac r4\int_0^T\!\int_0^1
(j+r^{-1}\partial_x\rho)^2dxdt,                              \tag{31}
\]

on `rho_t+partial_x j=0`, `rho(0)=rho_0`, and `int j(t,x)dx=0` almost everywhere, and infinity otherwise. The observed current path is `Q(t)=int_0^t j(s)ds`. Finite action means the displayed residual is L2 in the weak PDE sense; it is the complete OU Cameron--Martin image, not only a smooth-history formula. Gaussian exponential tightness supplies goodness. This theorem does not include a complete microscopic apparatus/noise record.

For spatially constant harmonic mobility, constraining the constant current does not change the contracted density action. The conclusion is special to this interface, not a general density-dependent or heterogeneous assertion.

The two scales required for this same-task result are

\[
\boxed{\kappa_N\to0,\qquad N^2\kappa_N\to\infty.}             \tag{32}
\]

For example `kappa_N=1/log(N+1)` is allowed. There is no `kappa_N << N^-1` condition. Fixed bounded **conservative** auxiliary damping gamma is allowed. The finite response tau, native duration N^2T, weak-tap tolerances and initialization remain actual costs.

## 8. Heterogeneous kinetics: true projection rather than unchanged heat

The equilibrium and current identities hold for arbitrary frozen R,Gamma, but the homogeneous receiver is not transferred without proof. A uniform auxiliary force acting through `D=R^(-1)` produces the actual current-metric projection

\[
C_D=D-D\mathbf1(\mathbf1^TD\mathbf1)^{-1}\mathbf1^TD.           \tag{33}
\]

Usually `B C_D B^* != B D B^*`. The density-preserving algebraic projection `PDP`, `P=I-11^T/N`, is a different supplied port: `B P D P B^*=B D B^*`. Reciprocity alone does not provide it.

For example, `d(x)=1+epsilon sin(2pi x)` and `rho(x)=cos(2pi x)` have native Fick current of mean `pi epsilon`. A spatially uniform feedback force removes mean current by adding a term proportional to d(x), whose divergence changes the nonflat density equation. The appropriate target is the actual metric-projected/conditioned transport law. Root is constructing that more general receiver separately.

## 9. Literal ports and physical limits

Equation (1) is a reciprocal passive interconnection: unit visible and auxiliary energy stores; native inertias tau; a nearest-neighbor auxiliary LC/wave line of speed parameter a; actual reciprocal taps of ratio g_N; native resistive ports R; and relative-momentum damping ports Gamma. A local mechanical linkage or electrical transducer must supply both directions of each tap. Sensing a current and writing a number is not the reciprocal force port. Native resistance values may remain hidden because their dissipation and thermal noise are actual constitutive partners.

An electrical implementation using ideal transformer ratios is a port-model construction, not proof that an off-the-shelf transformer has the required low-frequency response as N grows. Low-frequency leakage, finite magnetizing inductance, parasitic modes, range and ratio accuracy must be paid. Alternatively, a large physical compliance/capacitance represents `z=q/g`; that changes component size/current budgets even though normalized stored thermal energy stays finite. A mechanical realization can pay geometric ratio/stroke constraints. No particular fabrication is certified here.

The conservative bath is an actual pair interaction: its equal/opposite forces and noise preserve total auxiliary momentum. Ordinary independent grounded dampers do not meet it. Likewise the topology of the auxiliary storage must preserve its total except for the g v taps. Leakage to an uncontrolled reservoir changes the exact counter.

All parameters are static during execution; no event clock, global synchronization, microscopic copying or hidden reset is used. Thermalizing the full connected system may still take a long time. Product auxiliary preparation or a warranted stationary baseline is a separate paid initializer. A nonflat visible profile needs its real preparation work. Fixed-probability calibration or preparation failures cannot be omitted in a speed-N rare-event claim.

## 10. Grounded-loss failure and force-response cost

Replace the conservative p bath by `dp=aBq dt-gamma_N p dt+sqrt(2gamma_N)dV`. This preserves the canonical law and the total-current counter, but its polynomial is

\[
(\tau\lambda^2+r\lambda+\ell)
(\lambda^2+\gamma_N\lambda+a^2\ell)
+\kappa_N\lambda(\lambda+\gamma_N)=0.                          \tag{34}
\]

For fixed positive gamma and `ell << kappa gamma`, the density pole is

\[
\lambda\sim-a^2\ell^2/(\kappa\gamma).                         \tag{35}
\]

Rare native circulation is still controlled, while nonflat relaxation becomes slow. Recovering ordinary heat at the fundamental mode requires the additional scale `kappa_N gamma_N N^2 -> 0`. Together with (32), this needs a vanishing grounded-loss budget. A reciprocal line with ordinary fixed loss in each inductor therefore does not supply the positive theorem. Structural conservative damping avoids this particular requirement and must be warranted physically.

A constant circulating force f=F1 ultimately yields zero native velocity and a stored mean q=F1/g, costing equilibrium energy `N F^2/(2kappa_N)`. The operation changes force response as it changes current noise. No passive precision improvement at unchanged DC response is asserted.

## 11. Primary comparison and status

Freitas, Delvenne and Esposito, *Stochastic and Quantum Thermodynamics of Driven RLC Networks*, PRX 10, 031005 (2020), [arXiv:1906.11233](https://arxiv.org/abs/1906.11233), explicitly derives charge/flux interconnection, momentum reversal, resistor noise and the need to retain inductive response when heat/noise matters. Sections II--IV and the regularization discussion were read during construction. Nyquist, *Thermal Agitation of Electric Charge in Conductors*, Phys. Rev. 32, 110 (1928), [DOI](https://doi.org/10.1103/PhysRev.32.110), is the original direct noise/impedance predecessor. Passive filtering and the fluctuation-dissipation relation are established machinery.

The constructed comparison is the exact current counter plus uniform residue/path control at a declared local finite-response port, and its loss/initialization/disorder boundary. It is not a new basic LC principle, a proof of a fabricated apparatus, or an implementation at every hidden operation interface. It can redirect the larger research target even when an ordinary network designer is the eventual supplier.
