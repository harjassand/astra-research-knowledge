# Joint equilibrium density/current fluctuations with a programmed harmonic mode

30 October 2026. Authored constructive proof in the existing complementary Astra P1 role. This theorem is separate from the nonlinear LDP: it is not obtained by differentiating a rate function. Independent receiving review of this additional file remains pending.

## 1. Actual interface and theorem

On the even ring use the actual rates `r_i=c(1+alpha_N u delta_i)`, `c=s/2`, `delta_i=eta_i-eta_(i+1)`, `u=sigma p(eta)`. Native active exchanges flip `u`. An independent fresh Poisson clock flips `sigma` at physical rate `gamma_N`. Assume

\[
0\le\alpha_N\le1,\quad\alpha_N\to\alpha,
\qquad\gamma_N\to\infty,\quad\gamma_N/N\to0.
\tag{1}
\]

Initialize at the actual uniform canonical occupancy law with `M_N/N=m_N -> m in (0,1)`, times a fair sign. This stationary law is denoted by `mu_N`. Its preparation is a premise. The endpoint `alpha=1` is permitted here; native ellipticity is not needed.

Define the actual fluctuation density and integrated current on physical time `N^2t` by

\[
Y_t^N(G)=N^{-1/2}\sum_iG_i(\eta_i(N^2t)-m_N),
\qquad\mathcal W_t^N(H)=N^{-3/2}\sum_iH_iJ_i(N^2t).
\tag{2}
\]

For smooth periodic `H`, let `bar H=int H` and let `F_H` be the zero-mean periodic antiderivative of `H-bar H`.

**Theorem.** On each fixed horizon,

\[
(Y^N,\mathcal W^N)\Longrightarrow(Y,\mathcal W),
\qquad\mathcal W_t(H)=\bar H B_t+Y_t(F_H)-Y_0(F_H).
\tag{3}
\]

The density field is the ordinary stationary conservative Ornstein–Uhlenbeck field:

\[
dY_t(G)=cY_t(G'')dt+dZ_t(G),\qquad
d\langle Z(G),Z(K)\rangle_t=s\chi(m)\langle G',K'\rangle dt,
\tag{4}
\]

\[
\mathbb E[Y_0(G)Y_0(K)]=\chi(m)[\langle G,K\rangle-\bar G\bar K].
\tag{5}
\]

The Brownian motion `B` is independent of the complete density field and has covariance `s chi(m)(1-alpha^2)(t wedge s)`. A safe field topology is `D([0,T],H^{-5} x H^{-5})`, with continuous limits. In particular, finite lists of smooth test processes converge jointly functionally.

Equivalently, the current has Gaussian innovation representation

\[
\mathcal W_t(H)=c\int_0^tY_v(H')dv+\mathcal M_t(H),
\tag{6}
\]

\[
d\langle\mathcal M(H),\mathcal M(K)\rangle_t
=s\chi(m)\left[\int HK-\alpha^2\int H\int K\right]dt.
\tag{7}
\]

The controlled bit changes exactly the spatially constant current-noise mode at a flat equilibrium. Density sees only the spatial derivative of this noise and retains its ordinary OU law. At `alpha=1` the harmonic current vanishes while the density fluctuations remain unchanged. Nonconstant weighted integrated currents in (3) are generally not Brownian motions.

## 2. Canonical activity cancellation

Write `a_i=delta_i^2`, `A=sum a_i`. Under the canonical law,

\[
\mathbb E a_i=2m_N(1-m_N)N/(N-1).
\tag{8}
\]

Every pair of disjoint bonds has the same covariance `v_N=O(1/N)`, by the four-site hypergeometric probabilities. Overlapping covariances are bounded and there are only finitely many per bond. Hence

\[
\operatorname{Var}\Big(\sum_iw_i a_i\Big)
\le C_m\Big[\sum_iw_i^2+N^{-1}(\sum_iw_i)^2\Big].
\tag{9}
\]

For coefficients summing to zero, the second term disappears after subtracting the overlapping pairs from the full constant-covariance double sum. Thus `Var(sum_i Delta G_i a_i)=O_G(1/N)`, where `Delta G_i=G_(i+1)-G_i`, and `Var(A/N)=O(1/N)`. Stationarity and Jensen transfer these estimates to time integrals without any temporal mixing premise.

## 3. Density defect: an inverse-energy bound

The exact density Dynkin equation is

\[
Y_t^N(G)=Y_0^N(G)+c\int_0^tY_v^N(\Delta_NG)dv
+\int_0^t R_N^Gdv+Z_t^N(G),
\quad
R_N^G=c\alpha_N N^{3/2}u\sum_i\Delta G_i a_i.
\tag{10}
\]

Here `Delta_N` is the discrete Laplacian. The coefficient sum telescopes, so (9) gives `||R_N^G||_2^2<=C_G N^2`. This source is odd in `sigma`. Minus the complete macroscopic generator, denoted `A_N`, dominates the sign-clock form. On odd functions that form has operator `2N^2 gamma_N`. The inverse-energy variational bound is therefore

\[
\|R_N^G\|_{-1,A_N}^2
\le\frac{\|R_N^G\|_2^2}{2N^2\gamma_N}
\le C_G/\gamma_N.
\tag{11}
\]

The stationary reversible maximal inequality gives

\[
\mathbb E\sup_{t\le T}\left|\int_0^tR_N^Gdv\right|^2
\le CT\|R_N^G\|_{-1,A_N}^2\to0.
\tag{12}
\]

This finite-chain inequality can be proved by solving `A_N h=R_N^G`, adding forward and reversed Dynkin martingales so the endpoints cancel, and applying Doob's inequality. Their bracket means are `2T<h,A_N h>`. With a positive sign clock the nontrivial particle sector is connected even at `alpha_N=1`, since the clock makes either required native orientation available. Thus the mean-zero Poisson solution exists. The general inverse-energy/additive-functional framework is classical Kipnis–Varadhan theory.

The canonical cancellation is load bearing: a pointwise sum-of-absolute-values estimate would lose a power of `N`. Equation (11) is not a statement for arbitrary rare nonuniform density profiles.

## 4. Joint brackets and tightness

The density martingale jump is `delta_i Delta G_i/sqrt N`, and

\[
\frac d{dt}\langle Z^N(G),Z^N(K)\rangle_t
=cN\sum_i\Delta G_i\Delta K_i(a_i+\alpha_Nu\delta_i).
\tag{13}
\]

The activity part converges after integration to `s chi(m) int G'K'` by (9). Discrete summation by parts gives the deterministic bound

\[
\left|N\sum_i\Delta G_i\Delta K_i\delta_i\right|\le C_{G,K}/N,
\tag{14}
\]

so the phase contribution vanishes.

Let `M` be the exact total-current martingale with native increments `delta_i-alpha_Nu`, and put `B_t^N=M(N^2t)/N^{3/2}`. Its bracket and cross bracket are exactly

\[
\frac d{dt}\langle B^N\rangle_t=c(1-\alpha_N^2)A/N,
\qquad
\frac d{dt}\langle Z^N(G),B^N\rangle_t
=c(1-\alpha_N^2)\sum_i\Delta G_i a_i.
\tag{15}
\]

The first converges to `s chi(m)(1-alpha^2)` after integration; the second has zero mean and variance `O(1/N)`. Bounded brackets and finite time grids give uniform convergence of these bracket processes. All jumps vanish. The vector martingale functional CLT gives the displayed Gaussian innovations, jointly with time-zero variables and independent of their limiting sigma-field. The ordinary canonical sampling-without-replacement CLT gives (5), equivalently by conditioning the iid Bernoulli CLT on the total and using its local limit theorem. Equation (12) identifies the unique OU solution, and the zero cross bracket makes the harmonic Brownian motion independent of that field.

For field tightness, a Fourier test of frequency `k` obeys, by (10), stationarity, and (12),

\[
\mathbb E\sup_{t\le T}|Y_t^N(e_k)|^2
\le C_T(1+k^4+k^2/\gamma_N).
\tag{16}
\]

The same upper derivative bounds hold beyond the lattice frequency. Summation with `H^{-3}` weights gives bounded expected supremum norm, providing compact containment in `H^{-4}`. Finite-coordinate tightness follows from (10), the bounded drift second moment, martingale bounds, and the vanishing source remainder. Jumps vanish. The weaker stated `H^{-5}` topology is consequently safe.

## 5. Actual total current and exact spatial reconstruction

The physical path identity is

\[
J(t)=M(t)+\frac{\alpha_N}{2}(u_0-u_t)
-\alpha_N C_\gamma(t)-\alpha_N\gamma_N\int_0^t u_vdv.
\tag{17}
\]

The compensated clock martingale has bracket `gamma_N t`; after division by `N^{3/2}` its maximal squared norm is `O(gamma_N/N)`. The last term, in macroscopic units, has source `alpha_N gamma_N sqrt N u`, whose inverse-clock energy is at most `alpha_N^2 gamma_N/(2N)`. The same maximal estimate as (12) applies. The endpoint is bounded. Therefore

\[
\mathbb E\sup_{t\le T}|J(N^2t)/N^{3/2}-B_t^N|^2\to0.
\tag{18}
\]

For all other spatial current modes use exact conservation, `eta_i(t)-eta_i(0)=J_(i-1)(t)-J_i(t)`. Choose the zero-mean discrete antiderivative `F_H^N` satisfying `N(F_(i+1)^N-F_i^N)=H_i-bar H_N`. On every actual path,

\[
\mathcal W_t^N(H)=\bar H_N J(N^2t)/N^{3/2}
+Y_t^N(F_H^N)-Y_0^N(F_H^N).
\tag{19}
\]

Discrete antiderivatives converge with their required derivative bounds; the previous variance and maximal estimates make their vanishing test errors negligible. This proves (3). Fourier division on nonzero modes and (18) give the stated current-field convergence. No ratio `A_H/A` or trace-clock identification is required.

An explicit finite-time observable covariance follows. With `F=F_H`, `G=F_K`,

\[
\begin{aligned}
\operatorname{Cov}(\mathcal W_t(H),\mathcal W_s(K))
={}&s\chi(m)(1-\alpha^2)(t\wedge s)\bar H\bar K\\
&+\chi(m)\langle F,[e^{c|t-s|\Delta}-e^{ct\Delta}-e^{cs\Delta}+I]G\rangle.
\end{aligned}
\tag{20}
\]

Mean-zero weighted current covariances are independent of `alpha`; constant-current covariances carry exactly its programmed factor.

## 6. Information scope, cost, and predecessors

An initial density bounded by a fixed constant against `mu_N` transfers all small `L2` and probability errors. The martingale receiver then holds provided its actual initial fluctuation field has the stated limit. Canonical visible occupancy with a fixed recorded `sigma`, or with a fixed recorded `u`, has density two and the same initial field, so these are explicit valid extensions. Retaining a complete occupancy record typically costs exponentially more and is not covered by this observation. Conditional use requires the corresponding actual initial law and the complete declared future native-and-clock conditional generator.

The endpoint `alpha=1` is covered by this stationary proof. The zero-external-clock fluctuation receiver is not: (11) has no meaning at `gamma_N=0`. The theorem is finite-horizon and asymptotic in volume, not a uniform-in-infinite-time or full-record approximation. It contains no finite-data acquisition statement.

The stationary native event count over `N^2T` is order `N^3`; the external clock adds mean `gamma_N N^2T` events. Atomic shared-bit coupling, initialization, sensing, actuation and control bandwidth remain real suppliers and costs.

Primary machinery: Kipnis–Varadhan, [Central limit theorem for additive functionals of reversible Markov processes and applications to simple exclusions](https://doi.org/10.1007/BF01210789), 1986, and the [1985 primary announcement](https://www.numdam.org/article/AST_1985__132__65_0.pdf). Forward/backward decomposition and ordinary exclusion OU limits are established methods; their specific finite-chain use is displayed above.

There is no broad priority claim for noise engineering while retaining diffusion. Relevant physical predecessors include Hexner–Levine, [Noise, diffusion, and hyperuniformity](https://arxiv.org/abs/1611.02386), and Morningstar–O'Dea–Richter, [Hydrodynamics in long-range interacting systems with center-of-mass conservation](https://arxiv.org/abs/2304.12354). The scoped construction here is the actual joint limit (3) and its programmable rank-one current innovation at the stated initializer and paid clock window. Priority for that assembled family is unresolved.
