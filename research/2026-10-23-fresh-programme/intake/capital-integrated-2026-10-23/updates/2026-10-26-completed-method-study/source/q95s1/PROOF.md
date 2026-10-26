# Bounded interrogation of a hidden relaxation mode

This is the governing construction made in Q95. It is a self-contained mathematical result in a declared observation model. Priority over the literature is **not established**. The general use of Gaussian degradation and comparison of experiments is established; see [Blackwell (1953)](https://doi.org/10.1214/aoms/1177729032) and the explicit adaptive-collapse construction in [Song, arXiv:2608.22905v1, Section 2, Theorem 2.1](https://arxiv.org/html/2608.22905v1#S2). The latter concerns menus of experiments, not this constitutive-law application.

## 1. Exact finite observation theorem

There are two known candidate causal linear systems, indexed by theta in {+1,-1}. At readout i,

\[
Y_i=(F_\theta u)_i+s_i\xi_i,\qquad \xi_i\stackrel{iid}{\sim}N(0,1),\ s_i>0.
\]

The matrices F+ and F- are lower triangular. Before observing Yi, a possibly randomized controller chooses ui from previous observations, with |ui| <= U. Its randomization is independent of theta and of the sensor noise. In particular there is no same-readout algebraic feedback. The complete record includes actions and observations.

Assume the contrast matrix K=F+ - F- is entrywise nonnegative. Let u*=U times the all-ones vector and bi=(Ku*)i. A single fixed u* experiment Blackwell-dominates every such bounded causal policy, for this fixed pair of known systems. Consequently it has at most the Bayes risk of any policy, for every prior and every decision loss for which the risks exist.

**Proof.** Center each observation Xi from the fixed experiment by its known midpoint m*i=((F+ + F-)u*)i/2. Its conditional law is theta bi/2 + si xi. Recursively simulate the proposed controller. Its controls through i are known from the previously simulated record. Set

\[
m_i=((F_++F_-)u)_i/2,\quad \delta_i=(Ku)_i,\quad
a_i=\begin{cases}\delta_i/b_i&b_i>0,\\0&b_i=0.\end{cases}
\]

Because K >= 0 and |uj| <= U, |delta_i| <= bi, so |ai| <= 1. Output

\[
\widetilde Y_i=m_i+a_iX_i+s_i\sqrt{1-a_i^2}\,\zeta_i,
\]

with fresh independent standard normals zeta_i. Conditional on the simulated past, Xi is independent of that past. This output has mean mi+theta delta_i/2=(Ftheta u)i and variance si squared. When bi=0, the entire relevant row of K is zero, so delta_i=0 too. Induction gives exactly the law of the proposed experiment, including its controls. The simulation kernel does not depend on theta. Apply any proposed terminal decision to this simulated record. This establishes the risk comparison directly. QED.

This is stronger than comparing Fisher information or KL divergence. It is also restricted to a binary pair with a common known noise law; a different garbling for each member of a composite family would not prove a composite Blackwell order.

## 2. Continuous readout and a positive contrast kernel

The corresponding continuous model is

\[
dY_t=y_\theta(u)_t\,dt+\sigma\,dW_t,\quad 0\le t\le T.
\]

Controls are bounded predictable processes and policies must give well-posed causal observation/control equations. Finite-latency sampled controllers satisfy the intended condition. Both systems start from the same known zero state. If their output difference is

\[
\delta_t(u)=\int_0^t k(t,s)u_s\,ds,\qquad k(t,s)\ge0,
\]

then b(t)=U integral_0^t k(t,s) ds bounds |delta_t(u)|, and u*=U attains b(t) simultaneously at every time. The fixed experiment again dominates any such controller.

For completeness the causal garbling is explicit. Write m_t(u)=(y+(u)t+y-(u)t)/2 and center/standardize the fixed readout to obtain dX_t=theta b(t)/(2 sigma) dt+dW_t. With a_t=delta_t(u)/b(t), or zero if b(t)=0, simulate

\[
d\widetilde Y_t=m_t(u)dt+\sigma\{a_t dX_t+\sqrt{1-a_t^2}\,dB_t\}.
\]

The new noise is a continuous martingale with quadratic variation t and hence a Brownian motion. Its drift is m_t(u)+theta delta_t(u)/2. Bounded predictable coefficients make the stochastic integrals valid. This produces the target law without using theta. The finite theorem avoids any stochastic-equation issues for an executable sampled implementation.

## 3. A physically admissible ambiguous component

Use strain u and stress y. Compare:

* E: a spring of modulus A, yE=A u.
* Mlambda: a Maxwell element with spring modulus A and dashpot viscosity eta=A/lambda. Let z'=lambda(u-z), z(0)=0; yM=A(u-z).

These are conventional components, not a proposed new material. A Maxwell element is a series spring and dashpot. Its stored energy is A(u-z)^2/2 and

\[
\frac{dE}{dt}=y_M\dot u-\frac{y_M^2}{\eta}.
\]

The second term is nonnegative dissipation. An elastic spring has dE/dt=yE u'. Thus both candidates are passive. Strain jumps can be interpreted by their exact finite energy change, or by smooth ramp limits.

They have the same instantaneous modulus A but equilibrium relaxation moduli A and 0. Their stress contrast is

\[
y_E-y_M=A\lambda\int_0^t e^{-\lambda(t-s)}u_s\,ds.
\]

Its kernel has one sign, so the preceding result applies. A common known passive background may be added to both and subtracted from the observations. Granting it known only helps discrimination. An unknown background cannot improve the lower bound, but the exact attaining test then need not remain available.

For a step u=U, b(t)=AU(1-exp(-lambda t)). For bins of length h, put a=exp(-lambda h), r=(1-a)/(lambda h). Bin-averaged stress gives

\[
K_{ii}=A(1-r),\qquad
K_{ij}=Ar(1-a)a^{i-j-1}\quad(j<i).
\]

All entries are nonnegative. The bin-averaged sensor has si=sigma/sqrt(h). This is exactly the matrix used by `experiment.py`; the independently implemented state recurrence checks it.

## 4. Exact best classification risk and acquisition time

For a deterministic waveform and Gaussian observations with common covariance, the optimum equal-prior classifier is the likelihood-ratio test. For the step experiment define

\[
D^2=\frac{A^2U^2}{\sigma^2}I(\lambda,T),\qquad
I(\lambda,T)=\int_0^T(1-e^{-\lambda t})^2dt
=T-\frac{2(1-e^{-\lambda T})}{\lambda}
+\frac{1-e^{-2\lambda T}}{2\lambda}.
\]

The matched-filter sufficient statistic has distributions N(+D/2,1) and N(-D/2,1). Therefore the equal-prior Bayes error and the smallest possible maximum of the two conditional errors are both

\[
p_*(\lambda,T)=\Phi(-D/2).
\]

The domination theorem makes this the optimum over **all** admissible bounded feedback policies, not only deterministic waveforms. The sampled formula replaces D squared with sum bi squared / si squared. Bin averaging discards a small amount of within-bin information; its risk approaches the continuous bound as h goes to zero.

For lambda T small,

\[
I(\lambda,T)=\lambda^2T^3/3+O(\lambda^3T^4).
\]

At target conditional error alpha < 1/2, the small-rate minimum duration is

\[
T_\alpha\sim\left[\frac{12\sigma^2\{\Phi^{-1}(1-\alpha)\}^2}
{A^2U^2\lambda^2}\right]^{1/3}.
\]

This is an important distinction from asserting that one must wait a full relaxation time: independent white-noise averaging permits T proportional to lambda^(-2/3) in the slow-mode regime, but the required duration remains unbounded as lambda tends to zero. The exact scalar root is computed in `detection_duration.csv`.

For bounded deterministic stress error epsilon, any waveform satisfies

\[
\sup_{t\le T}|y_E-y_M|\le AU(1-e^{-\lambda T}).
\]

If this is <= 2 epsilon, a common observation history exists: recursively use the midpoint response and allocate opposite errors to the two models. Extra readouts do not remove a common bounded calibration error. This statement is about adversarial bounded error, not independent random noise. The separating duration threshold is -log(1-2 epsilon/(AU))/lambda when 2 epsilon < AU.

## 5. A positive conditional operation for an entire spectral family

Suppose an **independent** rate floor ell>0 has already been established. Compare the permanent spring with the family

\[
G_\mu(t)=\int_{[\ell,\infty)}e^{-\lambda t}\,d\mu(\lambda),
\qquad \mu\ge0,\quad \mu([\ell,\infty))=A.
\]

No number of components, upper rate limit, or smooth spectral density is required. Under the step, each such alternative has stress decrement delta_mu(t) >= b_ell(t)=AU(1-exp(-ell t)). Let

\[
R=\sigma^{-2}\int_0^T b_\ell(t)\{dY_t-AUdt\},\qquad
D_\ell^2=\sigma^{-2}\int_0^T b_\ell(t)^2dt.
\]

Reject the permanent spring if R < -D_ell squared / 2. Under the spring, R is N(0,D_ell squared). Under any alternative its mean is -sigma^(-2) integral b_ell delta_mu <= -D_ell squared and its variance is unchanged. Thus both error types are at most Phi(-D_ell/2). Equality holds at the single least-favorable Maxwell element mu=A delta_ell.

Conversely, that least-favorable pair is part of the family. Section 4 prevents any adaptive controller from giving it a smaller maximum error. Therefore this simple test is **exactly minimax optimal over the whole spectral family and all bounded feedback policies**. The argument does not assert a common composite garbling: only the least-favorable binary pair is needed for the lower bound.

The rate-floor hypothesis is the missing operation, not an invention supplied by this theorem. It cannot be certified uniformly from the same finite experiment by taking a best-fit finite Prony spectrum and reading off its smallest fitted rate.

## 6. Without a rate floor, finite data have no uniform equilibrium-modulus value

Consider the full passive class

\[
\mathcal C_A=\left\{G(t)=g+\int_{(0,\infty)}e^{-\lambda t}d\mu(\lambda):
g\ge0,\ \mu\ge0,\ g+\mu((0,\infty))=A\right\}.
\]

The target equilibrium modulus is g in [0,A]. For every finite T, U and positive sigma, under the stated experiment class,

\[
\inf_{\text{policy},\widehat g}\sup_{G\in\mathcal C_A}
\mathbb E_G(\widehat g-g)^2=A^2/4.
\]

**Proof.** The constant estimator A/2 supplies the upper bound. For any fixed bounded policy, compare E with Mlambda. The step experiment dominates its binary observation law. The total variation distance of the two step laws is 2 Phi(D/2)-1, tending to zero as lambda tends to zero. Total variation contracts under the parameter-independent garbling, so the controlled laws also approach each other. Clip any estimator to [0,A], which cannot increase squared error. Its risks R_E and R_Mlambda obey

\[
\begin{aligned}
R_E+R_{M\lambda}
&\ge \mathbb E_E[(\widehat g-A)^2+\widehat g^2]
-A^2\operatorname{TV}(P_E,P_{M\lambda})\\
&\ge A^2/2-A^2\operatorname{TV}(P_E,P_{M\lambda}).
\end{aligned}
\]

The supremum risk is at least half this sum. Take lambda to zero and then the infimum over policies and estimators. QED.

This is a uniform minimax statement, not the claim that data are useless for each fixed material. Under an independently justified rate floor, finite-dimensional model, distributional prior, or other structure, data can be highly informative. With exact noiseless continuum data, analytic uniqueness is a different mathematical problem.

## 7. A stronger physical bridge considered: temperature acceleration

Even grant an ideal, known and compatible acceleration law lambda(t)=lambda_0 a(t), with 0 <= a(t) <= a_max, no thermal damage or expansion ambiguity, and free thermal control. Then

\[
z(t)=\int_0^t\lambda(s)e^{-\int_s^t\lambda(r)dr}u(s)ds,
\qquad |Az(t)|\le AU\{1-e^{-\lambda_0 a_{max}t}\}.
\]

Choosing a(t)=a_max and u=U attains this envelope. The same comparison and minimax obstruction hold with lambda replaced by lambda_0 a_max. A finite acceleration factor helps but does not create a rate floor. In real materials the common shift law itself requires independent compatibility evidence; [Fesko and Tschoegl (1971)](https://doi.org/10.1002/polc.5070350106) already explains why a single temperature shift need not work in multicomponent materials. This idealized extension is an impossibility argument, not a demonstrated thermal protocol.

## 8. Essential boundary: passivity alone is insufficient

Take ordinary passive RC filters H0(s)=1/(s+1), H1(s)=2/(s+2). Their impulse contrast is exp(-t)-2 exp(-2t), which changes sign. Under a unit step, the contrast is exp(-2t)-exp(-t), with total squared integral 1/12 over infinite time. A bounded sinusoid at omega=sqrt(2) instead has persistent contrast amplitude 1/3, so its accumulated squared contrast grows asymptotically like T/18. In the executable T=60 comparison it exceeds the step contrast by approximately 39 times.

Both filters are passive circuit operations; this prevents the invalid extrapolation from 'passive' to 'a step always wins.' A single parameter shared across a material's channels, correlated or model-dependent noise, extra detectors, unbounded strain, nonlinear activation, and apparatus dynamics also require separate treatment.

## Resource and physical scope

The comparison fixes one initially equilibrated specimen, horizon T, peak strain U, sensor noise density and readout interface. A full interval uses the same readout count. It permits arbitrary waveform complexity and gives initial preparation and computation free, favoring the proposed active bridge. It does not impose an additional tight work or slew-rate budget. `waveform_comparison.csv` reports strain-squared exposure, exact jump work, dissipation, and final stored energy under each model. Strain-squared exposure is not mechanical work. Unloading, reset, temperature sweeps, instrument calibration and material validation are not performed. No source measurement is represented by any locally generated number.
