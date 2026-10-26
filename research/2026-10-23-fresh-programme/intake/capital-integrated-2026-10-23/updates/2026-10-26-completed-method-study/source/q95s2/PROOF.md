# Stage 2: sequential stress and the strongest positive result obtained

All assumptions of stage 1 remain explicit. In particular the readout is scalar stress with known, common additive Gaussian noise density sigma>0, the specimen is linear and initially equilibrated, and controls have a finite strain bound. No physical measurements are made here.

## 1. Unbounded adaptive stopping cannot certify exact permanence

Let E be the permanent spring of modulus A and Mlambda the same-instantaneous-modulus Maxwell element for each lambda>0. Allow any bounded causal policy and a possibly unbounded stopping time tau. Suppose a declaration S of permanent solidity is made only at finite tau, and the procedure controls its false-solid probability uniformly:

\[
\sup_{\lambda>0}P_{M\lambda}(S,\tau<\infty)\le\alpha.
\]

Then

\[
P_E(S,\tau<\infty)\le\alpha.
\]

**Proof.** For each deterministic T, the event {S,tau<=T} is measurable in the finite record. Stage 1 supplies, for the same controller,

\[
\operatorname{TV}(P_E^{[0,T]},P_{M\lambda}^{[0,T]})
\le2\Phi\left(\frac{AU}{2\sigma}\sqrt{\int_0^T(1-e^{-\lambda t})^2dt}\right)-1\longrightarrow0.
\]

Consequently P_E(S,tau<=T)<=alpha by taking lambda down to zero. Increase T to infinity and use continuity from below. QED.

Thus a test that must terminate under the permanent spring cannot have both conditional classification errors below 1/2 uniformly over all positive Maxwell rates. Pointwise longer waits do not repair *uniformly valid finite-time confirmation of exact permanence*. This is a full-domain proof including arbitrary random stopping, not a bound inferred from the withheld simulations. It is a standard dense-null/testing obstruction in this physical model, not an asserted new general statistical principle. The quantitative witnesses in `SEQUENTIAL_WITNESSES.csv` illustrate the bound; they do not supply its quantifiers.

## 2. Positive mechanism: an honest upper confidence sequence for equilibrium stiffness

Use the ordinary step u=U. The full class is

\[
G(t)=g+\int_{(0,\infty)}e^{-\lambda t}d\mu(\lambda),
\quad g\ge0,\ \mu\ge0,\ g+\mu((0,\infty))=A.
\]

The readout satisfies dY_t=UG(t)dt+sigma dW_t. No lower relaxation rate or finite spectral representation is assumed. For a candidate g0, define S_t(g0)=(Ug0 t-Y_t)/sigma. Under the null g>=g0, G(t)>=g0 and S has nonpositive drift. For every q>=0,

\[
L_t^q(g_0)=\exp\{qS_t(g_0)-q^2t/2\}
\]

is a nonnegative supermartingale starting at one. This follows directly by Ito's formula: its finite-variation drift is qU(g0-G(t))/sigma times L, hence nonpositive. Bounded coefficients on compact intervals justify the standard localization argument.

Mix q over a half-normal density with precision rho>0. Completing the square gives

\[
E_t(g_0)=2\sqrt{\frac{\rho}{t+\rho}}
\exp\!\left\{\frac{S_t(g_0)^2}{2(t+\rho)}\right\}
\Phi\!\left(\frac{S_t(g_0)}{\sqrt{t+\rho}}\right).
\]

The positive mixture remains a supermartingale by Tonelli and conditional expectation. Ville's inequality therefore gives P_g(sup_t E_t(g)>=1/alpha)<=alpha. For t>0 this expression is strictly increasing in S: its integral representation has a strictly positive derivative. Let b_alpha(t) be its unique solution at level 1/alpha. Then

\[
\overline g_t=\min\left\{A,\inf_{0<s\le t}\frac{Y_s+\sigma b_\alpha(s)}{Us}\right\}
\]

clipped below at zero satisfies

\[
P_G(\forall t>0:\ g\le\overline g_t)\ge1-\alpha.
\]

There is no union over candidate g0: only the process evaluated at the true g is needed for inversion. This is conventional mixture confidence-sequence machinery, instantiated for a passive response bound. The normal-mixture method is established in [Howard et al., Annals of Statistics 2021, DOI 10.1214/20-AOS1991](https://doi.org/10.1214/20-AOS1991), [arXiv:1810.08240v9](https://arxiv.org/abs/1810.08240v9). It is not claimed as a new invention.

On the coverage event the upper bound decreases to g. Indeed G(t)->g by dominated convergence, its time average tends to g, W_t/t->0 almost surely, and b_alpha(t)/t->0. The last property follows from the displayed mixture formula, or by substituting C sqrt(t log t) for any sufficiently large fixed C. For every gamma>g the rule tau_gamma=inf{t: upper_g_t<gamma} is finite almost surely on this event. It certifies g<gamma with an error probability at most alpha. There is no uniform finite duration across the spectral class.

This is asymmetric information: the interval [0,upper_g_t] supplies no positive lower stiffness certificate. At g=0 it can eventually certify any *positive tolerance* gamma. It cannot certify exact g=0 at finite time, and it cannot establish a nonzero permanent stiffness. Those claims are not silently substituted for the original target.

## 3. Competent ordinary incumbents under the same observations

An ordinary method may discard early transient data. Fix deterministic restart times sj and weights wj summing to one. Apply the same mixture construction to (Ug0(t-sj)-(Yt-Ysj))/sigma for t>sj, with failure alpha wj. The minimum across these upper sequences has simultaneous coverage by the union bound. Each shifted response still satisfies G(s)>=g; no assumption of stationarity of the transient mean is used. This is the `restart_CS` incumbent.

For the finite prescribed readout grid, an additional strong ordinary comparator considers *every* interval between recorded times. There are M=n(n+1)/2 intervals. For each [sj,ti], its mean stress is at least Ug, and its noise is N(0,sigma^2/(ti-sj)). Therefore

\[
\overline g^{\rm grid}_{t_i}=
\min_{k\le i,\ j<k}\left\{
\frac{Y_{t_k}-Y_{t_j}}{U(t_k-t_j)}+
\frac{\sigma\Phi^{-1}(1-\alpha/M)}{U\sqrt{t_k-t_j}}
\right\}
\]

clipped into [0,A] covers g at all allowed readouts with probability at least 1-alpha. It can select a late window after inspecting the data without invalid coverage. It is valid for the declared finite observation interface; it does not claim continuum validity beyond that interface. All comparators receive identical Brownian increments, timestamps and noise calibration. Work, duration and strain are identical because they use the same single step. No spectrum, true rate, or equilibrium value is supplied to an inference method.

The cumulative candidate has no general efficiency advantage over these established methods. Restarting or selecting late windows can reduce transient bias dramatically. That conventional explanation is directly tested on new cases and retained whether it wins or loses.

## 4. Withholding and full-domain scope

`DESIGN.md` was written before `WITHHELD_CASES.json` and before any detector noise was generated. The fixed generator uses a new seed; none of its truth is used for tuning the bounds. Cases include 24 discrete nonnegative spectra, four continuous gamma spectra with analytic Laplace responses, three extremely slow modes, and a permanent spring. Every local observation is synthetic. The positive mechanism is valid for the entire finite positive-measure class by the above proof, including continuous spectra absent from the numerical grid. The simulation tests implementation and contrasts conventional procedures; coverage on 32 cases is not a proof of general validity.

## 5. What survives and what remains missing

The stage 1 finite-horizon obstruction survives the strongest sequential escape in Section 1. The positive construction supplies useful one-sided tolerance certificates without a relaxation cutoff, with honest optional stopping. Its statistical engine and stronger conventional variants are established. No new physical primitive, general advantage over conventional methods, or verified novel scientific advance is established.

The remaining operation for the original exact long-term target is a justified restriction excluding arbitrarily slow alternatives, or an independently supported observable that distinguishes them. Finite noisy mechanical histories alone do not supply it under this model. Model-dependent material fluctuation noise, nonlinear probes, and other detector channels are outside this proof; no universal impossibility across those unconstructed operations is claimed.
