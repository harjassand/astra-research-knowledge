# Output-specific certification of a thermal response

## Result

For a Hermitian observable with a positive finite-temperature transition measure, the requested scalar response is a linear functional of that measure. The closest prior method already certifies arbitrary such functionals from noisy Euclidean correlations and positivity: Mutzel and Tilloy, [arXiv:2606.09791v1](https://arxiv.org/abs/2606.09791). Their method covers this target after a simple change of spectral measure. The useful task here is therefore a response-specific cost and identifiability audit, not a new general spectral-certification method.

I derive the exact confidence-set and dual-certificate form, add the justified double-commutator sum rule, and give an explicit equal-information construction. At beta=1 and eta=1 (below the first Matsubara frequency 2 pi), two positive thermal measures match six Euclidean correlators, the exact first sum rule, and even the static response, while their target chi differ by 0.03389784. Thus the first moment plus a static calibration do not identify this finite-eta response. A calibrated finite-duration exponential-drive intervention then gives a conditional interval that separates this pair, with its duration, readout count, and systematic bounds charged. The numerical acquisition is a reproducible simulated Gaussian readout, not a physical or Monte Carlo acquisition.

## Model and exact input/output contract

Let H have eigenvalues E_n, let p_n=exp(-beta E_n)/Z, and let A be Hermitian. For each positive transition Delta=E_m-E_n, m>n, define

\[
d\mu_{\beta,A}(\Delta)=\sum_{m>n}(p_n-p_m)|A_{nm}|^2\,\delta_{E_m-E_n}(d\Delta),\qquad \mu\ge0.
\]

Assume the connected Euclidean correlator has no unremoved elastic/zero-frequency term. Such a term must be separately measured or bounded; it does not enter the commutator response below. For 0<=tau<=beta,

\[
C_\beta(\tau)=\int_0^\infty
\frac{e^{-\tau\Delta}+e^{-(\beta-\tau)\Delta}}
     {1-e^{-\beta\Delta}}\,d\mu(\Delta),
\qquad
\chi_{\beta,A}(i\eta)=\int_0^\infty
\frac{2\Delta}{\Delta^2+\eta^2}\,d\mu(\Delta),\quad \eta>0.
\]

The exact first moment is

\[
M_1=2\int_0^\infty\Delta\,d\mu(\Delta)
=\langle[A,[H,A]]\rangle_\beta.
\]

For A=q and H=p^2/2+V(q), this is the operator identity M1=1, independent of beta. For general A it is a thermal expectation and is not free; it needs an exact operator reduction or its own acquisition and uncertainty. A multiplicative calibration A_meas=gA changes C, chi and M1 by g^2.

Set rho(dDelta)=mu(dDelta)/(1-exp(-beta Delta)). Then the Euclidean kernel is the one used by Mutzel–Tilloy,

\[
C_\beta(\tau)=\int (e^{-\tau\Delta}+e^{-(\beta-\tau)\Delta})\,d\rho,
\]

and the target and sum-rule kernels are respectively

\[
G_\eta(\Delta)=\frac{2\Delta(1-e^{-\beta\Delta})}{\Delta^2+\eta^2},
\qquad
M_1=\int 2\Delta(1-e^{-\beta\Delta})\,d\rho.
\]

Thus the target is exactly a positive-measure linear functional of the same Euclidean data. No full spectral reconstruction is mathematically needed.

## Closest comparator and scope

Mutzel and Tilloy's v1 paper formulates min/max bounds for arbitrary linear functionals of a positive spectral measure subject to a covariance-based confidence region for Euclidean data. It derives a dual positivity certificate and finite SDP relaxations using rigorous kernel envelopes; every feasible dual point is a valid bound, and the relaxation converges as the envelope partition is refined. The article demonstrates this on actual two-dimensional lattice phi^4 Monte Carlo data. Our G_eta is one such functional. The exact M1 constraint can be added as an equality row in the moment problem (or as a zero-width data constraint), while its unbounded-frequency tail is controlled explicitly below. Mutzel–Tilloy's own discussion also points to direct real-time functional bounds as established work. I claim no novelty for positivity-based functional bounds, duality, or direct response measurement.

Their paper's worked output was a smeared spectral density for a lattice model, not this sub-Matsubara response. This report does not replay their Monte Carlo data or implementation. The specialization, matched ambiguity construction, and control-cost calculation below are new work in this worker directory, with correctness and priority scoped to the evidence stated here.

## Reliable finite-data interval and dual certificates

Let k_j(Delta) be the Euclidean kernels at acquired times tau_j, let y be their sample means, and let Sigma and F be a calibrated confidence ellipsoid. With extra acquired moments m_r(Delta) in intervals [l_r,u_r], define the feasible set

\[
\mathcal F(y)=\left\{\rho\ge0:
(K\rho-y)^T\Sigma^{-1}(K\rho-y)\le F,
\quad l_r\le\langle m_r,\rho\rangle\le u_r\right\}.
\]

The output-specific interval is [inf_{rho in F}<G_eta,rho>, sup_{rho in F}<G_eta,rho>]. This is the sharp interval under exactly the declared confidence set, positivity, and moment information; it does not choose a preferred spectrum. If the confidence set covers the acquired means with probability 1-alpha, this interval covers chi with at least that probability. Autocorrelation, covariance estimation, thermalization, and lattice/continuum systematics must be included in that confidence region or as separate additive errors.

For exact moments m_r rho=s_r, a convenient dual certificate is any coefficient vector a and lambda satisfying, for every Delta>0,

\[
\sum_j a_j k_j(\Delta)+\sum_r\lambda_r m_r(\Delta)\le G_\eta(\Delta).
\]

It certifies

\[
\chi(i\eta)\ge a^Ty+\lambda^Ts-\sqrt{F\,a^T\Sigma a}.
\]

Reversing the pointwise inequality gives the upper certificate

\[
\chi(i\eta)\le a^Ty+\lambda^Ts+\sqrt{F\,a^T\Sigma a}.
\]

These follow by integrating the pointwise inequality against rho and extremizing a^T K rho over the ellipsoid. Each feasible certificate is reliable without an optimal solve. Optimizing over certificates gives the exact endpoints when strong duality holds; otherwise it still gives safe outer bounds. An uncertain sum rule is another noisy row, not an exact lambda term.

For a finite implementation, use the Mutzel–Tilloy dual envelope construction on [0,Omega], splitting around the nonconvex part of G_eta or using piecewise-constant interval enclosures. The sum rule supplies a simple rigorous tail:

\[
0\le\chi_{\Delta>\Omega}(i\eta)
\le\frac{M_1}{\Omega^2+\eta^2},\qquad
\int_{\Delta>\Omega} k_j\,d\rho
\le M_1\sup_{\Delta\ge\Omega}
\frac{e^{-\tau_j\Delta}+e^{-(\beta-\tau_j)\Delta}}
     {2\Delta(1-e^{-\beta\Delta})}.
\]

The ratio in the second expression decreases for tau in [0,beta/2], so its supremum is its value at Omega. Low-frequency kernels in the rho convention are finite; no spectral gap is required for this tail argument. The universal moment-only scale is 0<=chi<=M1/eta^2, which becomes weak as eta decreases. For eta>0, G_eta vanishes quadratically at Delta=0 in the rho convention; normalization, beta, and the zero-mode subtraction therefore matter.

## Equal-information obstruction

The following is a rigorous construction for finite Euclidean-time rows, finitely many power moments, and an optional static-response row; it does not apply if the acquired rows already include the target itself. Let phi_1,...,phi_q be these rows and let g=G_eta. For eta>0, g is not in their linear span: at large Delta, Euclidean kernels decay exponentially except the tau=0 kernel, which tends to one; positive power moments grow polynomially; and static/negative power moments contribute only finitely many inverse powers. But g=2/Delta-2 eta^2/Delta^3+2 eta^4/Delta^5-... has an infinite inverse-power tail. No finite combination of those rows can equal it. Hence g,phi_1,...,phi_q are linearly independent functions. There exist q+1 positive frequencies whose evaluation matrix has full rank. A nonzero vector v in the null space of the q measurement rows then obeys <g,v> !=0.

Choose positive base weights b_i with 2 sum_i Delta_i b_i=M1. For sufficiently small d>0, the measures

\[
\mu_\pm=\sum_i(b_i\pm d v_i)\,\delta_{\Delta_i}
\]

are both positive, match every declared finite Euclidean mean, power moment, and static-response row exactly, and differ in target by 2d|<g,v>|. These are finite-dimensional thermal response measures: take H=diag(0,Delta_1,...,Delta_{q+1}) and an observable with only ground-to-excited entries, setting |A_0i|^2=w_i Z/(1-e^{-beta Delta_i}). Then its thermal positive transition weight at Delta_i is exactly w_i. This proof does not use a hidden sampler or eigensystem as an algorithm input.

The concrete instance uses beta=1, eta=1, tau={0,1/12,2/12,3/12,4/12,5/12}, exact M1=1, and an exact static-response row chi(0)=int 2/Delta dmu. The common support is {0.07,0.16,1.9,5.3,9,15,21.5,28.5,40}; the ambiguity persists even if this support grid is supplied and only its weights are hidden. A null vector is defined by v_9=1 and v_{1:8}=-A_{1:8}^{-1}A_9, with rows A=(k_0,...,k_5,2Delta,2/Delta). A 60-digit interval determinant encloses det(A_{1:8}) strictly below zero; interval Cramer bounds verify all weights remain positive at d=10^-6 and enclose the target gap away from zero. The exact construction matches all eight constraints by A v=0. The checker is `equal_information_witness.py`; decimal weights and interval receipts are in `RESULTS.json`.

The finite-data benchmark has common Euclidean means (at the six listed times) 27.1004409445, 27.0729097522, 27.0574652074, 27.0471079113, 27.0402408533, 27.0362806669; common static response 27.0530611582; and targets 0.2321723594 versus 0.2660701994. The gap is 0.0338978400. Additive Gaussian Euclidean noise of standard deviation 0.02, and static-response noise of standard deviation 0.05, have exactly the same observation law under the two measures because their means and noise law match. No estimator using only these inputs can identify which target is correct. Any interval with coverage 1-alpha for each system must have width at least the gap with probability at least 1-2alpha under their common data law.

The recorded noisy vector is in `noisy_euclidean.csv`. This is a simulated Gaussian acquisition generated from the common mean, not a physical experiment or raw MCMC configurations. The impossibility is about the declared finite summary/noise interface. It does not claim that the full raw Monte Carlo path distributions for the constructed pair are identical.

## Calibrated intervention and paid cost

The retarded response is R(t)=2 int sin(Delta t) dmu, and

\[
\chi(i\eta)=\int_0^\infty e^{-\eta t}R(t)\,dt.
\]

An exponential source f(s)=f_0 e^{eta s}, started at s=-T and read at s=0, has linear-response output f_0 chi_T with chi_T=int_0^T e^{-eta t}R(t)dt. A central difference between +f_0 and -f_0 cancels even powers. Since coth(beta Delta/2)>=1, the measured Euclidean C_beta(0) gives M_0=2 int dmu<=2 C_beta(0). Thus

\[
|\chi-\chi_T|\le M_0 e^{-\eta T}/\eta
\le2U_0e^{-\eta T}/\eta,
\]

where U_0 is an upper confidence bound for C_beta(0). To allocate tail error eps_tail choose

\[
T\ge\eta^{-1}\log\!\left(\frac{2U_0}{\eta\,\epsilon_{tail}}\right).
\]

For independent readouts of A with per-shot standard deviation sigma_A and n preparations per sign, the central-difference statistical radius at normal quantile z is

\[
\epsilon_{stat}=\frac{z\sigma_A}{\sqrt{2n}|f_0|},\qquad
n\ge\frac{z^2\sigma_A^2}{2f_0^2\epsilon_{stat}^2}.
\]

The finite-field bias needs a certified bound B_3 on the third derivative of the filtered expectation: eps_nl<=B_3 f_0^2/6. If this bound is absent, the nonlinear systematic is UNKNOWN. Gain, force calibration, envelope-shape, and timing errors must be added. The sum rule gives |R'(t)|<=M1, so a time-grid version of the same intervention with spacing h has left-rule error at most M1 h/eta; with an upper confidence bound M1_hi, set h<=eta eps_quad/M1_hi. This makes the resolution and number of time settings grow as eta falls. The continuous exponential drive avoids that numerical quadrature but still requires physical control over duration T and the same linear-response calibration.

This is an output-specific measurement of the desired resolvent, so it can remove the Euclidean-only ambiguity; it is not a free transition sampler and does not reconstruct a spectrum. Its control/readout is the dominant new acquisition. A numerical response certificate is valid only if the thermal state, drive transfer function, observable gain, field strength, timing, readout variance, nonlinear remainder, and statistical coverage have receipts. Discretizing a lattice in Euclidean time also adds its actual transfer-matrix kernel and continuum-extrapolation error; the continuum formulas above must not be silently applied to finite-a data.

In the synthetic demonstration, eta=1 is 0.1592 of the first Matsubara value 2 pi. The exponential-drive horizon is T=12.0; n=10,000 per sign; f0=0.1; per-readout sigma_A=0.02; relative observable-gain and force-calibration bounds are 0.3% and 0.2%. The Euclidean-derived tail radius is 0.000334, the statistical radius is 0.003643, and declared calibration, nonlinearity, and waveform radii are 0.001874, 0.000500, and 0.000543. The resulting interval is [0.226721,0.240508], containing the plus response and excluding the minus response. With the simulated Gaussian readings, a union bound gives at least 98.83% joint coverage for the statistical and C_beta(0) intervals, conditional on the explicitly declared deterministic systematic limits. These calibration limits are benchmark assumptions, not claims about an available instrument.

The eta dependence is material: T grows as eta^-1 log(1/(eta eps_tail)); the impulse-grid alternative has h=O(eta eps_quad/M1), and uniform per-time precision delta=O(eta eps_meas) requires shot count O(sigma_R^2/(eta^2 eps_meas^2)) per setting. The direct ramp's shot count instead follows the per-shot response variance and f0; its elapsed control duration still grows as eta^-1. No noise, mixing, state-preparation, or field-calibration cost is hidden in these expressions.

## N724/N725 applicability and remaining limits

At pinned Astra capital HEAD 4c47df1fda950e27e48295689dd642194bfac046, N724 is a source-derived, unreviewed scalar noisy-Laplace-query result targeting the return-probability trajectory of an unknown probability measure on [0,1]. N725 is a separate source-derived, unreviewed fixed-input full-quantum-snapshot result; its states are not Gibbs states and its target is a real-time return amplitude. Their exact access interfaces do not imply a minimax lower bound for this one thermal response functional. Both independent-review gates remain open; no result from either is used as a premise here. The complete source notes, gates, and notices were read and are listed in `INPUTS.json`.

The executed result is a proof of finite-information non-identifiability plus a response-measurement cost model. It is not a new general continuation algorithm, an optimal eta-dependent minimax theorem, physical validation, a universal gap assumption, or an implementation benchmark against Mutzel–Tilloy. The Euclidean-only optimal interval still requires solving the exact data-constrained positive-measure problem for a real covariance set; the source code in this directory does not implement that SDP. External correctness and historical priority remain open.
