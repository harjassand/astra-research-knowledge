# Local reversible counters with prepared elastic memory

30 October 2026. Constructive complementary result. This is a harmonic continuous-current model, in the same mathematical class as root's Gaussian paired-current comparator. It is not a counterexample inside the bounded-occupation jump class of the locality theorem. It pays growing memory capacity and prepared long-wavelength memory susceptibility while keeping runtime interactions local and the dynamics reversible.

## 1. Result and objective actually achieved

There is a local reversible current bath with bounded memory coordinates z_i such that:

1. Its exact stationary visible law is the unit Gaussian on the zero-sum density subspace, for every finite N.
2. All physical currents, including constraint reactions, satisfy dz=dJ and dx=B dJ. Hence the complete total current is bounded by 2N b_N at every time.
3. With b_N=sqrt(N)[log(N+1)]^2=o(N), every fixed nonzero macroscopic circulation J_total/N^2 is eventually impossible.
4. On physical horizons N^2T, the entire stationary Gaussian density-fluctuation path converges to the ordinary diffusive Ornstein--Uhlenbeck field. The joint leading circulation CLT also remains ordinary.

The construction therefore preserves a meaningful complete **fluctuation path limit**, not the full finite-N density-path law or its speed-N large-deviation action. Its CLT circulation is not suppressed. The difference between typical path limits and rare-history laws is essential here.

No apparatus, finite-bandwidth bath, integer-particle realization, hidden-kinetics blindness, or preparation by the same nonergodic dynamics is claimed.

## 2. Actual local current operation and stationary initializer

On the N-site periodic ring, let

\[
(Bj)_i=j_{i-1}-j_i,\qquad L=B^TB.
\]

Let x lie in the zero-sum subspace H of R^N. These x_i are signed harmonic density/charge fluctuations, not occupancies. Put

\[
a_N=[\log(N+1)]^2,\qquad
H_N=\frac{L+N^{-2}I}{a_N},\qquad
K_N=H_N^{-1},\qquad b_N=\sqrt N\,a_N.                \tag{1}
\]

The memory precision matrix H_N is strictly positive and local: nearest-neighbor elastic couplings plus an on-site pinning term. Its inverse K_N is nonlocal and large. This prepared covariance is a real resource, not runtime long-range actuation.

The full state is (x,z) in H times [-b_N,b_N]^N. Its energy and specified stationary law are

\[
U_N(x,z)=\tfrac12\|x\|^2+\tfrac12z^TH_Nz,
\qquad
\mu_N^b(dx,dz)=\gamma_H(dx)\,
\frac{e^{-z^TH_Nz/2}\,1_{\{|z_i|\le b_N\}}dz}
{\int_{[-b_N,b_N]^N}e^{-z^TH_Nz/2}dz}.                \tag{2}
\]

Here gamma_H is the unit Gaussian on H. Initialize at this actual joint law. The visible marginal is exactly gamma_H and is independent of the memory at each stationary time. Preparing (2), including its long-wavelength correlations, is an explicit premise. The dynamics below conserves x-Bz and cannot generate every such mixture from an arbitrary fixed start by waiting.

For a fixed physical bath strength s>0, define the actual bond currents by

\[
\begin{aligned}
dJ&=-\frac s2(B^Tx+H_Nz)\,dt+\sqrt s\,dW-dR,\\
dx&=B\,dJ,\qquad dz=dJ. 
\end{aligned}                                       \tag{3}
\]

R_i=L_i^+-L_i^- is the usual box reflection: L_i^+ increases only when z_i=b_N and L_i^- only when z_i=-b_N. The sign in (3) pushes inward. The same reaction current -dR_i changes both z_i and the two endpoint density coordinates through B. It is not an unrecorded reset of the counter.

Every independent noise input acts on one physical bond and its colocated memory. The force on that bond uses its two endpoint densities and nearest-neighbor memory coordinates. All coefficients have bounded local operator norm; no coefficient proportional to a positive power of N is introduced. The on-site memory pinning becomes weak as N grows.

White noise and ideal conormal reflection are mathematical bath operations. They do not assert finite sensing bandwidth or a finite maximum instantaneous current. The per-bond quadratic-variation budget is exactly s dt. This is the appropriate continuous-current analogue of a fixed event-intensity budget; it is not the bounded-jump hypothesis of the separate exclusion theorem.

## 3. Reversibility, conserved hidden memory and full current accounting

For smooth f define the local directional derivative

\[
\mathcal D_i f=(Be_i)\cdot\nabla_x f+\partial_{z_i}f.
\]

Inside the box the generator is

\[
\mathcal L_Nf=\frac s2\sum_i
\{\mathcal D_i^2f-(\mathcal D_iU_N)\mathcal D_i f\}.    \tag{4}
\]

The boundary condition is conormal: \(\mathcal D_i f=0\) at z_i=plus or minus b_N. The reflection vector in the full (x,z) space is proportional to (Be_i,e_i), with inward sign. Integration by parts gives

\[
-\langle f,\mathcal L_Ng\rangle_{\mu_N^b}
=\frac s2\sum_i\langle\mathcal D_if,\mathcal D_ig\rangle_{\mu_N^b}.
                                                               \tag{5}
\]

Thus the process is reversible in (2). Conditional on the conserved vector

\[
w=x-Bz,                                             \tag{6}
\]

it is an ordinary reflected finite-dimensional Langevin diffusion on the box with strictly convex quadratic energy U_N(w+Bz,z). This gives a direct well-defined realization; no hidden-state mixing is required.

Equation (3), including every reflection current, implies

\[
J_i(t)=z_i(t)-z_i(0),\qquad
J_{\rm total}(t)=\sum_i[z_i(t)-z_i(0)],
\qquad |J_{\rm total}(t)|\le2Nb_N.                    \tag{7}
\]

Consequently

\[
\sup_{t\ge0}|J_{\rm total}(t)|/N^2
\le2a_N/\sqrt N\longrightarrow0.                    \tag{8}
\]

The counter is exact and local. The escape from a bounded-memory obstruction comes from the diverging b_N and its equilibrium susceptibility, not from omitted apparatus current, nonreversibility or an external global bit.

## 4. Unconfined reference: exact visible covariances

First remove the box and reflection. The process (3) with R=0 is a linear stationary Gaussian process under

\[
\mu_N^{\infty}=\gamma_H\otimes N(0,K_N).              \tag{9}
\]

For a nonzero spatial Fourier mode let

\[
\ell_k=4\sin^2(\pi k/N),\qquad
h_k=(\ell_k+N^{-2})/a_N.
\]

Use unitary Fourier coordinates, so the stationary variance of the visible mode x_hat(k) is one. Since w=x-Bz is conserved, its equation is

\[
d\widehat x_k=-\frac s2[(\ell_k+h_k)\widehat x_k
-h_k\widehat w_k]dt+\sqrt s\,\widehat B_k d\widehat W_k.
                                                               \tag{10}
\]

Under (9), x and z are independent, Var(z_hat(k))=1/h_k, and

\[
\operatorname{Var}(w_hat(k))=1+\ell_k/h_k.
\]

Gaussian conditioning therefore decomposes x_hat into its conserved conditional mean and a decaying fluctuation. Its exact stationary covariance is

\[
\boxed{C_{N,k}(t)=
\frac{h_k}{\ell_k+h_k}
+\frac{\ell_k}{\ell_k+h_k}
e^{-(s/2)(\ell_k+h_k)|t|}.}                           \tag{11}
\]

The nondecaying part is not omitted. It is the visible overlap with the frozen w. Since the smallest nonzero ell_k is of order N^-2,

\[
\sup_{k\ne0}\frac{h_k}{\ell_k}\le C/a_N\to0.          \tag{12}
\]

Thus the conserved overlap vanishes uniformly in mode. For each fixed nonzero integer k, on the macroscopic clock

\[
C_{N,k}(N^2t)\longrightarrow
\exp[-(s/2)(2\pi k)^2|t|].                            \tag{13}
\]

The right side is precisely the ordinary stationary diffusive Gaussian density covariance. No hypothetical copying experiment is used; the unconfined process is a proof reference whose coupling to the actual box process is established next.

## 5. The counter walls are not reached on the diffusive horizon

This is the required initialization and runtime estimate. Under (9),

\[
\operatorname{Var}(z_i)=\frac{a_N}{N}\sum_k
\frac1{\ell_k+N^{-2}}\le C_0a_NN.                    \tag{14}
\]

For example, sin(pi k/N)>=2k/N for k<=N/2 bounds the nonzero-mode sum by a constant times N^2; the zero mode contributes N^2 exactly. C_0 is independent of N.

Write the unconfined memory drift as

\[
v_i(t)=-(s/2)[B^Tx(t)+H_Nz(t)]_i.
\]

It is centered Gaussian at each stationary time, with

\[
\operatorname{Var}(v_i)
=\frac{s^2}{4}[2+(H_N)_{ii}]
=\frac{s^2}{4}[2+(2+N^{-2})/a_N]\le C_s.             \tag{15}
\]

Fix physical S_N=N^2T. On integer time points, Gaussian tails and a union bound over at most C_TN^3 site/time pairs give

\[
\mathbb P\left(\max_{i,j\le\lceil S_N\rceil}|z_i(j)|>b_N/2\right)
\le C_TN^3\exp[-b_N^2/(8C_0a_NN)].                  \tag{16}
\]

Between consecutive integers,

\[
z_i(t)-z_i(j)=\sqrt s[W_i(t)-W_i(j)]+\int_j^t v_i(u)du.
\]

The Brownian supremum has the usual Gaussian bound. For the drift, Jensen and stationarity give, for theta>0,

\[
\mathbb E\exp\left(\theta\int_j^{j+1}|v_i(u)|du\right)
\le\int_j^{j+1}\mathbb E e^{\theta|v_i(u)|}du
\le2e^{\theta^2C_s/2}.                              \tag{17}
\]

Optimizing theta bounds the probability that this integral exceeds b_N/4 by 2exp[-b_N^2/(32C_s)]. The Brownian contribution exceeding b_N/4 is bounded by 4exp[-b_N^2/(32s)]. Taking another site/time union bound yields

\[
\begin{aligned}
\mathbb P_{\mu_N^\infty}
\left(\max_{i,t\le N^2T}|z_i(t)|\ge b_N\right)
\le C_TN^3\bigl[&e^{-b_N^2/(8C_0a_NN)}
+e^{-b_N^2/(32C_s)}+e^{-b_N^2/(32s)}\bigr]\to0.
\end{aligned}                                       \tag{18}
\]

Indeed b_N^2/(a_NN)=a_N=[log(N+1)]^2. The polynomial prefactor is dominated. No temporal independence or mixing of z has been assumed.

The actual initial law (2) is exactly (9) conditioned on all memory coordinates lying in the box. Couple these initial states so that they agree whenever the unconfined draw lies in the box, and use the same driving Brownian motions. The two dynamics agree until the first unconfined boundary hit. Thus (18) bounds the total-variation distance between their complete visible path laws on [0,N^2T] by a quantity tending to zero. This comparison is to the **elastic unconfined reference**, not yet to ordinary diffusion.

The bound in (18) is only subexponential in N at its dominant scale. It is insufficient for transferring a speed-N action. No such transfer is claimed.

## 6. The whole density-fluctuation path limit is ordinary diffusion

Embed the visible field as

\[
Y_N(t)=N^{-1/2}\sum_i x_i(N^2t)\,\delta_{i/N}.         \tag{19}
\]

This is a signed fluctuation distribution with zero constant mode. Under the unconfined reference it is Gaussian. Formula (13), spatial Fourier orthogonality, and stationarity give convergence of all fixed Fourier/time finite-dimensional distributions to the stationary solution

\[
dY=(s/2)\partial_x^2Y\,dt+\sqrt s\,\partial_x d\mathcal W,
\qquad \langle Y,1\rangle=0.                          \tag{20}
\]

The initial field in (20) is unit spatial white noise with its constant mode removed. This is the ordinary Gaussian diffusion field.

For completeness, tightness is not inferred from covariance values at isolated times. From (11),

\[
\mathbb E|\widehat Y_N(k,t)-\widehat Y_N(k,u)|^2
\le sN^2\ell_k|t-u|\le C_sk^2|t-u|.                 \tag{21}
\]

The stationary mode variance is at most one, including the aliased discrete Fourier modes. For any p'>3/2, summing (21) against (1+k^2)^(-p') gives a uniform second-moment increment bound in H^(-p'). Gaussian fourth moments give a bound C|t-u|^2. Kolmogorov estimates, the uniform stationary Sobolev moment, and the compact embedding H^(-p') into H^(-p) for p>p' prove tightness in C([0,T],H^(-p)). Hence (19) converges as an entire path to (20), for every p>3/2 after choosing an intermediate p'.

The path coupling in Section 5 transfers this limit to the actual bounded-memory process. Its stationary visible marginal remains exactly gamma_H for each N, not merely asymptotically Gaussian.

This does not prove equality of the complete finite-N density-path law with ordinary diffusion. That stronger exact equality is supplied by root's all-to-all paired-current bath, at its different nonlocal port. Nor does the present convergence identify a full speed-N density large-deviation action.

## 7. Circulation at the CLT scale is deliberately not suppressed

For the unconfined reference, the constant memory mode is independent of all density modes. Let Z_0=N^-1/2 sum_i z_i. Since the density has zero sum,

\[
dZ_0=-\frac{s}{2a_NN^2}Z_0dt+\sqrt s\,dW_0,
\qquad \operatorname{Var}(Z_0)=a_NN^2.                \tag{22}
\]

The scaled total current is

\[
\frac{J_{\rm total}(N^2t)}{N^{3/2}}
=\frac{Z_0(N^2t)-Z_0(0)}N.                           \tag{23}
\]

Its stationary variance is exactly

\[
2a_N[1-e^{-st/(2a_N)}]\longrightarrow st.             \tag{24}
\]

The rescaled zero-mode equation has noise sqrt(s) and drift strength s/(2a_N). The initial mode divided by N has standard deviation sqrt(a_N), but its drift over a bounded macroscopic interval is O(a_N^-1/2) in L2. Thus (23) converges as a whole path to sqrt(s) Brownian motion. It is independent of the limiting density field. Section 5 transfers this joint limit to the bounded process.

There is no contradiction with (8): the hard current cap in CLT units is 2b_N/sqrt(N)=2a_N, which diverges. The buffer admits ordinary typical current fluctuations while excluding every fixed nonzero circulation at the larger N^2 scale.

For the ordinary reference bath C=sI, J_total(N^2T)/N^2 is exactly Gaussian with variance sT/N and speed-N rate q^2/(2sT). For the bounded local counter, it is supported in [-2a_N/sqrt(N),2a_N/sqrt(N)]. Its scalar speed-N rate is therefore zero at q=0 and infinite otherwise. Equality of the typical Gaussian fluctuation path limits does not preserve that rare-current action.

## 8. Memory susceptibility is the sharper resource

Root's exact-counter proof immediately admits the following refinement without changing its jump-process premises. Let X be its fundamental density Fourier mode, Z_k its memory mode, V_N=Var(X), and F=X-dZ_k. Stationarity and the reversible spectral inequality give

\[
\begin{aligned}
\|X_t-X_0\|_2
&\le\sqrt{2tD(F)}+2|d|\sqrt{\operatorname{Var}(Z_k)},\\
\frac{\mathbb E|X_t-X_0|^2}{V_N}
&\le\frac{4tD(F)}{V_N}
+\frac{8|d|^2\operatorname{Var}(Z_k)}{V_N}.            \tag{25}
\end{aligned}
\]

Since V_N is order N, |d| is order N^-1, and D(F) has the proved local-range bound, diffusive visible decorrelation with R_N=o(N) requires

\[
\operatorname{Var}(Z_k)\ \text{of order at least }N^3. \tag{26}
\]

If memory covariances obey the actual row-sum bound
\(\sup_i\sum_j|\operatorname{Cov}(z_i,z_j)|\le Cb_N^2\xi_N\),
then Var(Z_k)<=CN b_N^2 xi_N. A necessary resource condition is therefore

\[
b_N^2\xi_N\gtrsim N^2.                              \tag{27}
\]

Independent or uniformly short-correlated memory needs b_N of order N, not merely sqrt(N). The original worst-case bound Var(Z_k)<=N^2b_N^2 permits the smaller sqrt(N) threshold only with sufficiently coherent long-wavelength memory.

The present elastic memory explicitly pays that susceptibility. Before truncation,

\[
\operatorname{Var}(Z_k)=N\frac{a_N}{\ell_k+N^{-2}}
\asymp a_NN^3
\]

at the fundamental wave number. The box conditioning changes this by a negligible relative amount: its Gaussian tail probability is superpolynomially small, and Gaussian fourth moments control the removed second moment by Cauchy--Schwarz. The small conserved overlap in (11) is the same resource viewed dynamically.

## 9. Failure modes and scope of the evasion

The construction keeps reversibility, stationarity, local inverse covariance, local runtime current updates and complete current accounting. It changes the memory budget and, relative to root's exclusion theorem, uses signed harmonic variables with continuous currents. It therefore does not disprove the bounded-occupation locality theorem or demonstrate its sharpness within that jump class.

Its initializer is a prepared critical/soft memory field with a correlation scale of order N. Local runtime couplings do not make that initializer free. The same counter dynamics preserves w and cannot manufacture its required equilibrium mixture from arbitrary history. No ordinary memory reset is inserted during execution.

Growing capacity alone is not the full mechanism: uncorrelated local memories with b_N=o(N) still fail the susceptibility condition (27). The local elastic bath supplies the missing coherent storage. Conversely, wrapping a finite counter modulo its capacity would violate the exact eventwise counter law; the wrap contributes a large actual mismatch and cannot be ignored as a memory relabeling.

This alternative gives a genuine but weaker resource substitution: prepared long-wavelength memory and growing local capacity replace nonlocal runtime pairing for an ordinary density-fluctuation path limit plus a macroscopic current cap. It does not deliver the root one-bit gate's CLT-current suppression, its proposed full spatial action, exact finite-N ordinary density paths, or a practical apparatus.
