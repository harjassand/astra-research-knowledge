# Passive hidden memory: completed stability theorem and unresolved acquisition endpoint

## Status

The completed result here is a deterministic, finite-horizon, a posteriori trajectory certificate for a nonlinear observed coordinate with a passive hidden bath. The broader physical endpoint—acquiring and executing a certified predictor on an arbitrary retained apparatus—was not completed. Closely related acquisition mechanisms already occur in Astra N1688. This route should not be ranked as a new civilisation-changing capability or as a completed experimental algorithm.

## Question and representation

Can an observed nonlinear coordinate be predicted accurately without equilibrating or identifying an arbitrarily slow hidden passive bath? Keep the derivative-memory representation rather than replacing its sign structure by an absolute-norm perturbation.

Let \(V:\mathbb R^d\to\mathbb R\) be differentiable and \(\mu\)-strongly convex. In the scalar-coupling form consider

\[
\dot x=-\nabla V(x)-\sum_i w_i(x-y_i)+f(t),\qquad
\dot y_i=\lambda_i(x-y_i),
\]

where \(w_i\ge0\), \(\lambda_i\ge0\), and \(B=\sum_iw_i<\infty\). Finite baths suffice for the proof; positive measures follow when the displayed integrals exist. With prepared initial values \(y_i(0)=x(0)\), elimination gives

\[
\dot x+\nabla V(x)+K*\dot x=f,\qquad K(t)=\sum_iw_i e^{-\lambda_i t}.
\]

For arbitrary initial values the right-hand side gains
\(g(t)=\sum_iw_i e^{-\lambda_i t}(y_i(0)-x(0))\).
No lower bound on \(\lambda_i\) is imposed. Zero rates are included.

## Theorem

Let \(x,\widehat x\in H^1(0,T;\mathbb R^d)\) start at the same observed coordinate. Suppose their equations can be subtracted to give

\[
\dot e+\nabla V(x)-\nabla V(\widehat x)+K*\dot e
=(\widehat K-K)*\dot{\widehat x}+\rho=:r,
\qquad e=x-\widehat x,
\]

where \(\rho\) includes initial-force mismatch, forcing mismatch, and numerical residual. Put

\[
R=\|K-\widehat K\|_{L^1(0,T)}\|\dot{\widehat x}\|_{L^2(0,T)}+\|\rho\|_{L^2(0,T)}.
\]

Then

\[
\|x-\widehat x\|_{L^2(0,T)}\le R/\mu,
\qquad
|x(T)-\widehat x(T)|\le R/\sqrt{2\mu}.
\]

The true kernel must have the stated passive positive-mixture form. The inequality itself does not require a passive surrogate, although a passive surrogate is useful for stable implementation. It contains no exponential-in-horizon factor, no bath spectral gap, and no damping-dominance or small-kernel condition. Its actual right-hand side can grow with the horizon and the drive, so it is not a universal horizon-independent prediction claim.

### Proof of the sign retained by derivative memory

For each \(\lambda>0\), solve \(\dot r_\lambda=\lambda(e-r_\lambda)\), \(r_\lambda(0)=0\), and set \(z_\lambda=e-r_\lambda\). Since \(e(0)=0\), \(z_\lambda=e^{-\lambda\cdot}*\dot e\). Therefore

\[
\int_0^T e\cdot z_\lambda\,dt
=\int_0^T|z_\lambda|^2\,dt+
\int_0^T r_\lambda\cdot\dot r_\lambda/\lambda\,dt
=\int_0^T|z_\lambda|^2\,dt+|r_\lambda(T)|^2/(2\lambda)\ge0.
\]

For \(\lambda=0\), \(z_0=e\), so the integral is \(\|e\|_2^2\). Multiplication by positive weights and summation proves \(\int e\cdot(K*\dot e)\ge0\). Taking the inner product of the error equation with \(e\), integrating, and using strong convexity gives

\[
\tfrac12|e(T)|^2+\mu\|e\|_2^2\le\|e\|_2\|r\|_2\le R\|e\|_2.
\]

The first bound follows immediately. Maximizing \(Ru-\mu u^2\) over \(u\ge0\) gives \(R^2/(4\mu)\), proving the endpoint bound. Young's convolution inequality supplies the displayed expression for \(R\).

The same proof permits matrix kernels \(K(t)=\sum_i a_i a_i^\top e^{-\lambda_i t}\), by applying the scalar identity to each projected error \(a_i^\top e\). No mode-wise diagonalization in the observed coordinates is needed.

## Initialization is paid separately

For initial offsets \(\delta y_i\), define \(E_0=\frac12\sum_iw_i|\delta y_i|^2\). Holding the observed coordinate fixed for a guard \(\tau\) leaves the force
\(g_\tau(t)=\sum_iw_i e^{-\lambda_i(\tau+t)}\delta y_i\).
Cauchy–Schwarz gives

\[
|g_\tau(t)|^2\le 2E_0 K(2(\tau+t)).
\]

Its time integral can enter \(\|\rho\|_2\). Arbitrarily slow modes can prevent a guard from making this small. The theorem does not erase initialization cost, and a supplied microscopic energy bound may itself scale with hidden volume.

## Proposed retained-apparatus measurement and its limit

If the latent initial state for a run is fixed before a fresh random sign \(s\in\{-1,1\}\), an ideal clamp to \(x=as\) produces a bath reaction of the form
\(F_s(t)=asK(t)-g(t)+\eta(t)\).
Then \(sF_s(t)/a\) has conditional mean \(K(t)\) when the sensor noise has the appropriate zero-mean conditional law. This cancels arbitrary history-dependent latent offsets in expectation; it does not require matching the hidden state between runs. If \(|g|\le G\) and the noise is conditionally \(\sigma\)-sub-Gaussian, the signed noise is sub-Gaussian with proxy \((G^2+\sigma^2)/a^2\), giving the usual logarithmic-confidence repeat cost for pointwise kernel estimates.

However, an instantaneous clamp requires ideal bandwidth, and the above ideal observation identity is not a proved finite-slew implementation. No finite-bandwidth apparatus, unknown gain calibration, stochastic initialization law, or thermal path simulator has been completed here. White-noise-driven sample paths are outside the \(H^1\) theorem as stated.

## Finite-data kernel certificate

Both true and fitted positive-mixture kernels are decreasing. On a uniform mesh of spacing at most \(h\), suppose sound node bounds give \(|K(t_j)-\widehat K(t_j)|\le\eta\), and each kernel starts at most \(B\). Monotonicity bounds the discrepancy between successive nodes by the sum of their downward variations. Summing rectangles yields the safe bound

\[
\|K-\widehat K\|_1\le 2hB+T\eta
\]

(up to the final truncated interval, already covered by the same estimate). Thus finite nodal confidence bands can certify the actual trajectory through the theorem without identifying microscopic rates. A tighter constant is possible but not needed. A nonnegative exponential dictionary can preserve passivity, but an end-to-end finite-precision fitting and execution implementation was not completed.

## Primary comparison and provenance

1. Lang and Lu, *Error Analysis of Generalized Langevin Equations with Approximated Memory Kernels*, [arXiv:2512.10256](https://arxiv.org/abs/2512.10256), [full text](https://arxiv.org/html/2512.10256v1), SIAM/ASA Journal on Uncertainty Quantification 14(3), 2026, [DOI:10.1137/26M1837290](https://epubs.siam.org/doi/10.1137/26M1837290). They already study strongly convex generalized Langevin equations, approximate kernels, and long-time trajectory error. Their weighted comparison conditions and synchronous stochastic treatment are stronger in several directions; this narrower deterministic derivative-memory certificate retains a positivity identity to avoid a smallness/damping-dominance condition. Broad novelty is not claimed.
2. Lang and Lu, *Learning Memory Kernels in Generalized Langevin Equations*, SIAM Journal on Mathematics of Data Science 8(1), 2026, [DOI:10.1137/24M1651101](https://epubs.siam.org/doi/10.1137/24M1651101), already develops kernel learning with regularized Prony representations.
3. Baczewski and Bond, *Numerical Integration of the Extended Variable Generalized Langevin Equation with a Positive Prony Representable Memory Kernel*, Journal of Chemical Physics 139, 044107 (2013), [DOI:10.1063/1.4815917](https://doi.org/10.1063/1.4815917), is an existing extended-state realization and execution comparator.
4. Astra N1069, N1607, and especially N1688 cover positive memory, slow-mode obstructions, and retained-device thermal acquisition. At revision `76f6a7ce78867b927680ba3b9cd5eb407ce61ccd`, N1688's [complete source](https://github.com/harjassand/astra-research-knowledge/blob/76f6a7ce78867b927680ba3b9cd5eb407ce61ccd/research/2026-11-04-p2-acquired-thermal-feedback-simulator/source/p2/COMPLETE_VISIBLE_RESPONSE.txt) already uses fresh random-sign response acquisition on a retained nonstationary apparatus and certifies an encoded future law under bounded causal feedback. Consequently the sign-cancellation/no-reset idea is not a new primitive relative to Astra.

## What is earned

An explicit passivity-based nonlinear error inequality, an initialization bound, and a finite nodal-to-integrated kernel certificate are proved. A new physical acquisition-and-execution capability, general thermal prediction, and historical originality are not established. The selected correlated-Gibbs static acquisition construction is the stronger route being implemented separately.
