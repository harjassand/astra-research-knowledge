# Direct susceptibility acquisition: access model and resource accounting

## Status

Research derivations for a specified class of reciprocal passive linear systems. Chebyshev approximation, moment duality, and Gaussian change of measure are prior machinery. The proposed contribution is the combined uniform resource law and its physical realization within this access model, not the discovery that analytic extrapolation can be ill-conditioned. Priority for the combined theorem is not established by the literature search.

## 1. Model and target

Let

\[
\dot x=-Ax+bu,\quad y=b^Tx,\quad A=A^T,
\quad\mu I\preceq A\preceq\Lambda I,\quad\|b\|=1.
\]

Its impulse response and normalized static susceptibility are

\[
k_\nu(t)=\int_\mu^\Lambda e^{-\lambda t}d\nu(\lambda),
\qquad S(\nu)=\int_\mu^\Lambda\frac\mu\lambda d\nu(\lambda),
\]

where nu is a probability measure. The dimension and observable spectral weights are unknown. Every finitely supported measure has a diagonal realization with eigenvalues at the support points and components of b equal to square roots of the weights. The energy identity is

\[
\frac d{dt}\frac{\|x\|^2}{2}=-x^TAx+uy,
\]

so these are genuine passive stable systems.

A concrete deterministic circuit realization of nu=sum p_j delta_lambda_j is a series connection of parallel RC branches with Cj=1/pj and Rj=pj/lambda_j in the selected units. Branch impedance Rj/(1+s Rj Cj)=pj/(s+lambda_j), so a common input current and the total measured voltage realize the required response. With xj=sqrt(Cj) vj, the capacitor energy is exactly norm(x) squared divided by two. Every positive nonzero mass gives finite positive components. This realization does not remove intrinsic thermal noise; the theorem's additive sensor-noise premise must be justified separately before a thermal circuit experiment is claimed.

Each trial starts at a supplied zero state, lasts at most T, and observes

\[
dY_i(t)=y_i(t)dt+\sigma dW_i(t),\qquad y_i=k_\nu*u_i.
\]

The sensor noise is additive, Gaussian, and parameter independent, with known intensity sigma squared. Brownian noises are independent between trials. Inputs may be arbitrary predictable functions of all available observations and independent algorithmic randomness, including feedback within a trial and between trials. There is no restriction on classical computation or memory. Total squared-input effort is bounded almost surely by

\[
\sum_i\int_0^T|u_i|^2dt\le E,
\qquad\mathcal I=\frac{T^2E}{\sigma^2}.
\]

For reporting effort independently of the deadline, use

\[
\mathcal B=\frac E{\sigma^2\mu^2},\qquad
\mathcal I=(\mu T)^2\mathcal B.
\]

The compiler reports B. The exact Gaussian lower bound becomes B at least 4(1-2 alpha) squared divided by ((mu T) squared eta squared). This polynomial factor does not change the logarithmic asymptotic law.

E is an input-effort budget; it is not automatically the thermodynamic work, which is the integral of uy. Direct hidden-coordinate access, matrix-vector access to A, changes to A during acquisition, and parameter-dependent fluctuation statistics are outside this experiment class.

T is the largest age of an acquired transient, not total serial laboratory time. A single continuously reused plant whose old inputs remain observable for times exceeding T supplies a different resource.

## 2. Lower bound includes all causal inputs

Suppose two systems satisfy sup over t in [0,T] of |k0(t)-k1(t)| at most eta. Conditional on the same observation history, a causal algorithm uses the same input. The conditional observation drifts differ by (k0-k1)*u. Young's inequality gives

\[
\|(k_0-k_1)*u\|_{L^2[0,T]}
\le\|k_0-k_1\|_{L^1[0,T]}\|u\|_2
\le T\eta\|u\|_2.
\]

Gaussian change of measure therefore yields

\[
D_{\rm KL}(P_0\Vert P_1)
=\frac1{2\sigma^2}\mathbb E_0\sum_i\|(k_0-k_1)*u_i\|_2^2
\le\frac{\eta^2\mathcal I}{2}.
\]

A deterministic effort bound supplies the needed integrability. Bounded stopping and an adaptive trial count can be incorporated by stopping the observation process. This comparison does not assume linear estimation, fixed waveforms, or model reconstruction.

An estimate within epsilon of both possible targets, whose targets differ by more than 2 epsilon, supplies a binary test. If its failure probability is at most alpha under either hypothesis, Pinsker's inequality gives

\[
\mathcal I\ge\frac{4(1-2\alpha)^2}{\eta^2}.
\]

For success probability at least 3/4, this is I at least eta to the power minus two. The Bretagnolle--Huber bound also gives I at least 2 log(1/(4 alpha))/eta squared for alpha below 1/4. The companion approximation proof constructs finite positive moment-matched measures with exponentially small eta and separated susceptibilities.

A sharper exact confidence expression uses binary data processing: KL is at least kl(1-alpha,alpha)=(1-2alpha) log((1-alpha)/alpha). Thus

\[
\mathcal B\ge
\frac{2\,\operatorname{kl}(1-\alpha,\alpha)}{(\mu T)^2\eta^2}.
\]

## 3. Finite ramp and finite bin acquisition

Choose a ramp time tr<T, remaining observation time H=T-tr, and plateau U>0. Use any monotone ramp from zero to U completed by tr, and hold U thereafter. With a slew bound S and peak bound Umax, the linear ramp is permitted for

\[
t_r=T/2,\qquad U=\min\{U_{\max},ST/2\}.
\]

For t at least tr, integration by parts gives

\[
y(t)=U\int\lambda^{-1}[1-a_r(\lambda)e^{-\lambda(t-t_r)}]d\nu,
\quad
a_r(\lambda)=\frac1U\int_0^{t_r}e^{-\lambda(t_r-s)}du(s)\in[0,1].
\]

Thus no impulse or unbounded source slew is required. The detailed monotone ramp need not be reconstructed. A linear ramp has ar(lambda)=(1-exp(-lambda tr))/(lambda tr).

Choose degree m at least 1, n=m+1 bins, and bin duration h=H/n. Define

\[
z=e^{-\lambda h},\quad a=e^{-\Lambda h},\quad b=e^{-\mu h},
\quad v=\frac{2-a-b}{b-a}>1,
\]

with a=0 when Lambda is unbounded. Form the Chebyshev residual

\[
R_m(z)=\frac{T_m((2z-a-b)/(b-a))}{T_m(v)}
=\sum_{j=0}^mw_jz^j.
\]

The weights sum to Rm(1)=1. Record the n integrated bin averages

\[
\bar Y_j=\frac{Y(t_r+(j+1)h)-Y(t_r+jh)}h.
\]

Writing h_lambda=(1-z)/(lambda h), which lies in (0,1], their expectations satisfy

\[
\mathbb E\bar Y_j
=U\int\lambda^{-1}[1-a_r(\lambda)h_\lambda z^j]d\nu.
\]

Use the direct estimate

\[
\widehat S=\frac\mu U\sum_{j=0}^mw_j\bar Y_j.
\]

Its exact bias identity is

\[
\mathbb E\widehat S-S
=-\int\frac\mu\lambda a_r(\lambda)h_\lambda
 R_m(e^{-\lambda h})d\nu.
\]

Consequently the uniform certificate is

\[
|\mathbb E\widehat S-S|\le\rho_m,\qquad\rho_m=\frac1{T_m(v)}.
\]

This acquires the requested functional without recovering eigenvalues, spectral weights, hidden trajectories, or a fitted state-space model.

The final report also gives a separate thermal upper extension. For dx=(-Ax+bu)dt+sqrt(2 Theta A)dB from zero, with B independent of the sensor noise and Theta known, the output covariance is Theta[k(|t-v|)-k(t+v)]. Its absolute value is at most Theta, so the estimator variance gains at most (mu/U)^2 Theta A_m^2. Independent thermal trials add sufficient normalized effort O((Theta T/sigma^2) A_m^2 epsilon^-2 log(1/alpha)). At fixed Theta T/sigma^2 this leaves the upper exponent unchanged. It does not extend the main adaptive lower theorem to parameter-dependent fluctuation data.

## 4. Exact uncertainty and amplification bill

Independent Brownian increments give

\[
\operatorname{Var}(\widehat S)
=\frac{\mu^2\sigma^2}{U^2h}\sum_jw_j^2.
\]

All roots of Rm lie in [a,b], which is inside [0,1), so its monomial coefficients alternate in sign. Therefore its total absolute coefficient weight is exactly

\[
A_m=\sum_j|w_j|
=\frac{T_m((2+a+b)/(b-a))}{T_m((2-a-b)/(b-a))}.
\]

The ratio can be computed as a difference of log-cosh values. Its exact squared coefficient norm gives the actual noise variance; Am squared is a convenient upper bound.

Average R independent reset trials or independently prepared identical specimens. If rho_m is at most epsilon/2, a sufficient repetition count for failure probability at most alpha is

\[
R\ge\left\lceil
\frac{8\mu^2\sigma^2}{U^2h\epsilon^2}
\left(\sum_jw_j^2\right)\log\frac2\alpha
\right\rceil.
\]

Input effort per trial is at most U squared T. A linear ramp uses exactly U squared times (tr/3+H). Negative polynomial weights are classical postprocessing; the physical input remains bounded and monotone.

If necessary choose U no larger than sigma mu divided by sqrt(T), in addition to the peak and slew limits. Then the extra one trial from integer rounding contributes at most one to B. Smaller amplitude costs more repetitions without invalidating the bias certificate.

## 5. Degree bounds and joint parameter dependence

Write sH=mu H and kappa=Lambda/mu. Two elementary inequalities are

\[
\operatorname{arcosh}v
\ge\log\frac{\sqrt\kappa+1}{\sqrt\kappa-1}
\ge\frac2{\sqrt\kappa},
\qquad
\operatorname{arcosh}v\ge2\sqrt{\frac{s_H}{m+1}}.
\]

The first follows because (exp(x)-1)/(1-exp(-(kappa-1)x)) is at least 1/(kappa-1). For the second set a to zero, which decreases v, and use arcosh(2 exp(x)-1) at least 2 sqrt(x). This last inequality follows from cosh(2 sqrt(x)) at most 2 exp(x)-1, coefficient by coefficient in the power series.

Set L1=log(4/epsilon). Each branch in

\[
m=\left\lceil\min\left\{\frac{\sqrt\kappa L_1}{2},
\frac{L_1^2}{2s_H}\right\}\right\rceil
\]

individually gives rho_m at most epsilon/2. When Lambda is unbounded, retain only the second branch. Moreover, for sH at most 1,

\[
\log A_m\le m\left[\log8+\frac{s_H}{m+1}
+\log\left(1+\frac{m+1}{(\kappa-1)s_H}\right)\right].
\]

Using the appropriate degree branch yields

\[
\log A_m=O\!\left(
\sqrt\kappa L\log\left(1+\frac L{s_H\sqrt\kappa}\right)
\right),\qquad L=\log(1/\epsilon).
\]

The independently checked companion lower bound matches this exponent for kappa at least 16, mu T at most 1/64, epsilon at most 1/16, and fixed nontrivial confidence. The finite ramp H=T/2 changes this exponent only by universal constants. For fixed accuracy, the exponent is sqrt(kappa) log(1+1/(mu T sqrt(kappa))). It becomes proportional to 1/(mu T) in the broad-bandwidth regime; finite Lambda supplies the other branch.

### Exact rational compiler variant

For rational mu, Lambda, and h, replace the exponential interval by the enclosing rational interval

\[
a=\max\{0,1-\Lambda h\},\qquad b=\frac1{1+\mu h}.
\]

The inequalities exp(-Lambda h) at least a and exp(-mu h) at most b prove containment. The same polynomial then has exactly rational coefficients, exact rational bias certificate, exact rational coefficient norm, and exact rational squared coefficient norm. A slightly larger degree may be needed; the same asymptotic exponent holds because (1-b)/(1-a) is at least a constant times max{1/kappa,mu h} when mu h is small. This removes reliance on an uncertified floating-point evaluation of exponential endpoints.

## 6. Preparation and reuse

The formal model grants zero-state trials. It does not prove that every unknown plant can be reset rapidly through its measurement port. With only passive waiting, a previous state of norm at most B contracts to B exp(-mu t), so tolerance Breq costs at most

\[
t_{\rm reset}=\mu^{-1}\log(B/B_{\rm req}).
\]

If an actual reset circuit supplies damping gamma I on all coordinates, use mu+gamma instead, at the cost of those additional reset couplers. Such access must be stated, not silently supplied. Thermal process noise changes the reset and inference model.

An initial state bounded by norm B0 contributes at most (mu/U) Am B0 to the estimator's deterministic error. An optional robust upper construction removes its mean: choose a fresh fair sign after the initial state is set, drive the whole ramp/plateau with that sign, and multiply the final estimate by it. Any initial state independent of this fresh sign contributes zero conditional mean. Its bounded contribution has sub-Gaussian variance proxy ((mu/U) Am B0) squared; add this to the Gaussian variance in the repetition bill. This requires an actual initial-energy bound and fresh private signs. It does not justify applying the short-age lower bound to unrestricted long-time reuse of one continuously evolving plant.

R serial trials cost R acquisition periods plus actual reset periods. R simultaneous trials require R specimens, sensor channels, and their preparation hardware. Parameters must remain the same across repetitions. Short maximum trial age is not a claim of short total serial time or low hardware cost.

To allocate deterministic preparation error epsilon_p, passive waiting from a state bounded by B can use

\[
W\ge\mu^{-1}\left[\log\frac{\mu A_m B}{U\epsilon_p}\right]_+.
\]

The subsequent bounded input leaves a state norm at most B+U/mu, supplying a conservative bound for the next reset. Waiting can cost order log(Am)/mu and dominate T. Observations during that long reset would provide older transient data and are outside the short-age lower-bound contract.

## 7. Calibration, protection, and computation

For deterministic bin errors ej,

\[
|\Delta\widehat S|\le(\mu/U)A_m\max_j|e_j|.
\]

Thus bin-dependent drift, offsets, digitization errors, uncontrolled timing distortion, and unmodelled plant variation may require exponentially small tolerances. Repetition removes independent zero-mean noise, not unknown bias.

Structured uncertainties can cost less. A common amplitude calibration error induces common relative scaling. A common constant offset is multiplied by sum wj=1. Uncertainty in the detailed monotone ramp is already covered. A common constant clock-rate uncertainty can be covered by conservative exponential endpoints. Independent bin distortions need a separate error budget.

The bin rate is (m+1)/H. A fixed sensor bandwidth imposes an additional feasibility limit on T. Finite integrator settling and quantization must satisfy the preceding bias certificate. There is no claim of a fixed-hardware, arbitrarily short experiment.

Coefficient generation by the three-term recurrence costs O(m squared) arithmetic operations and O(m) stored coefficients. Working precision must include O(log Am+log(m/epsilon)) bits beyond signal dynamic range to certify cancellation. Each trial requires m+1 integrated samples and O(m) postprocessing. The estimates can be accumulated without storing trajectories. The exact rational compiler makes arithmetic and stopping certificates reviewable.

## 8. Comparison and attribution

Ordinary direct settling after a step needs time of order mu inverse times log(1/epsilon) for uniform bias epsilon. Short-horizon extrapolation replaces this waiting with the explicitly large precision/repetition bill. The lower bound applies to all permitted controls and algorithms, including full system identification, and the upper uses ordinary Chebyshev extrapolation. The conclusion is an optimal resource law, not a speed advantage over the best ordinary same-access method.

Closest primary sources:

1. H. J. Brown and Y. Grabovsky, *On feasibility of extrapolation of completely monotone functions*, arXiv:2401.15178v2; SIAM Journal on Mathematical Analysis 56(6), 7713--7747 (2024), DOI 10.1137/24M1652325. Their Theorem 2.1 gives the fixed-point asymptotic power exponent (2/pi) arcsin(1/x0) for relative L2 discrepancies. This already establishes severe extrapolation ill-conditioning. https://arxiv.org/html/2401.15178v2
2. J. K. Kraus, P. S. Vassilevski, L. T. Zikatanov, *Polynomial of best uniform approximation to x inverse and smoothing in two-level methods*, Computational Methods in Applied Mathematics 12(4), 448--468 (2012), arXiv:1002.1859. Exact reciprocal minimax approximation is prior work; their introduction traces it to Chebyshev. https://arxiv.org/pdf/1002.1859
3. G. Plonka and M. Tasche, *Fast computation of best approximation polynomials for the reciprocal function*, Numerical Algorithms (2026), DOI 10.1007/s11075-026-02364-1. Explicit relative/absolute approximation and stable recurrence formulas. https://link.springer.com/article/10.1007/s11075-026-02364-1
4. C. L. Epstein and J. Schotland, *The bad truth about Laplace's transform*, SIAM Review 50(3), 504--520 (2008), DOI 10.1137/060657273. Classical severe inverse-Laplace ill-conditioning. https://epubs.siam.org/doi/10.1137/060657273

The distinctions being established here are the finite-bandwidth crossover, uniform joint accuracy/horizon parameters, the static functional, arbitrary causal bounded-effort experimental control, and a finite ramp/integrated-readout attaining operation. These do not establish worldwide novelty on their own.
