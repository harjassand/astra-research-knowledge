# Independent audit: optimal Poisson exposure certificate

Date: 2026-10-16. Status: analytic verification of the parent-supplied optimization, under the exact admissible-control domain below. External correctness and historical priority unreviewed. This concerns a sufficient upper-bound certificate, not the true physical error probability.

## 1. Contract and Poisson certificate

Let a parent have fixed duration `tau>0`, deterministic nonnegative norm-bound profile `j(t)` with finite action `a=integral j(t)dt`, and deterministic locally integrable nonnegative full-pinch intensity `lambda(t)` with finite exposure `Lambda=integral lambda(t)dt`. Conditional on geometry, these profiles must not read the private Poisson cut histories, quantum state, or latent syndrome outcomes. Cuts are an independent inhomogeneous Poisson process. The entry/exit and support conditions in `AUDIT_POISSON_PINCH.md` remain necessary.

For a fixed cut partition, the block deletion/union bound is `sum_B (integral_B j)^2`. Averaging gives exactly the scalar certificate

\[
 p_{\rm uncapped}[j,\lambda]
 =\int_0^\tau\int_0^\tau
 j(t)j(s)\exp\!\left[-\left|\int_s^t\lambda(v)dv\right|\right]dt\,ds.
 \tag{1}
\]

This identity is the probability of no Poisson cut between each pair of action elements. There is no bath correlation factor. The parent effect is at most `min(1,p_uncapped) I`; a sharper analysis may average the cap pattern by pattern. The optimization below addresses the uncapped energy. For several independent parent cut processes, their uniform conditional scalar certificates multiply.

## 2. Pushforward proof, including zero-intensity intervals

Put `r(t)=integral_0^t lambda`, a nondecreasing absolutely continuous map into `[0,Lambda]`. Let the finite positive measure `nu` be the pushforward of `j(t)dt` under `r`. Its total mass is `a`, including any atoms caused by plateaus where `lambda=0` but `j>0`. A change of variables in the measure sense, requiring no inverse of `r` or division by `lambda`, gives

\[
 p_{\rm uncapped}=E(\nu)
 =\int_{[0,\Lambda]}\int_{[0,\Lambda]}e^{-|u-v|}\,d\nu(u)d\nu(v).
 \tag{2}
\]

Thus zero `lambda` or zero `j` intervals do not invalidate the reduction. Exposure spent while `j=0` can create holes in the support of `nu`, and can prevent equality in the optimum below. Idle intervals where both are zero are harmless. The lower bound remains valid even if the pushforward occupies only a proper subset of the exposure interval.

## 3. Exact measure optimum

For `Lambda>=0`, define

\[
 c=\frac{a}{\Lambda+2},\qquad
 \nu_*=c\left(\mathbf1_{[0,\Lambda]}du+\delta_0+\delta_\Lambda\right).
 \tag{3}
\]

At `Lambda=0` the Lebesgue part has mass zero and the two coincident endpoint atoms give `nu_*=a delta_0`, as required. Its mass is `a`. For every `u` in `[0,Lambda]`,

\[
 \int e^{-|u-v|}d\nu_*(v)
 =c\big[(2-e^{-u}-e^{-(\Lambda-u)})+e^{-u}+e^{-(\Lambda-u)}\big]
 =2c.
 \tag{4}
\]

The kernel has Fourier transform `2/(1+omega^2)`. For every finite real signed compactly supported measure `sigma`,

\[
 E(\sigma)=\frac1{2\pi}\int_{\mathbb R}
 \frac{2}{1+\omega^2}|\widehat\sigma(\omega)|^2d\omega\ge0,
 \tag{5}
\]

with equality only for `sigma=0`. Fourier inversion and Fubini apply because the spectral density is integrable and `sigma` has finite variation. For any other admissible positive measure `nu` of mass `a`, set `sigma=nu-nu_*`; its mass is zero, so the constant potential (4) kills the cross term. Hence

\[
 E(\nu)=E(\nu_*)+E(\sigma)
 \ge \boxed{\frac{2a^2}{\Lambda+2}}.
 \tag{6}
\]

For `a>0` the measure minimizer is unique. If `a=0`, every control has zero certificate, and uniqueness of a physical schedule is neither claimed nor needed. This is a lower bound on the best value of THIS UPPER-BOUND FUNCTIONAL. It is not a lower bound on actual quantum error.

The exact boundary mass in (3) is material. A uniform action density in exposure coordinates without the endpoint atoms has a nonconstant potential and is not the measure optimum.

## 4. Finite, explicit control attaining the optimum

For constant `j(t)=a/tau`, finite `Lambda>0`, choose

\[
 \lambda(t)=\begin{cases}
 0,&0\le t<\tau/(\Lambda+2),\\
 (\Lambda+2)/\tau,&\tau/(\Lambda+2)<t<\tau-\tau/(\Lambda+2),\\
 0,&\tau-\tau/(\Lambda+2)<t\le\tau.
 \end{cases}
 \tag{7}
\]

The middle interval has length `tau Lambda/(Lambda+2)` and exposure exactly `Lambda`. The first and final plateaus push action `a/(Lambda+2)` onto the two endpoint atoms. In the middle, `j/lambda=a/(Lambda+2)`, giving exactly the constant Lebesgue density. Thus (7) realizes (3) without infinite rates, singular intensity, or instantaneous action. For `Lambda=0`, simply set `lambda=0` throughout; the minimum is `a^2`.

If the intensity is capped at `lambda_max`, the constant-action construction is feasible iff `lambda_max tau >= Lambda+2` for `Lambda>0`. Merely satisfying the weaker exposure feasibility `lambda_max tau>=Lambda` does not ensure that the certificate optimum can be reached. The two nonzero-action plateaus need time. This cap condition is sufficient for the explicit constant-action schedule and necessary for that constant-action pushforward target: its endpoint atoms fix the plateau durations, leaving at most `tau Lambda/(Lambda+2)` for the interior exposure.

If BOTH action and intensity profiles are freely designed with upper bounds `j<=J_max` and `lambda<=lambda_max`, a piecewise realization of the same target is available whenever

\[
 \frac{2a}{(\Lambda+2)J_{\max}}+
 \frac{\Lambda}{\min\{\lambda_{\max},J_{\max}(\Lambda+2)/a\}}
 \le\tau,
 \tag{8}
\]

for positive `a,Lambda,J_max,lambda_max`: use endpoint plateaus at `J_max` and a middle segment with `j=c lambda`. The extra minimum in (8) is essential if the chosen intensity would force `j=c lambda>J_max`. Idle time with both profiles zero can fill any surplus. A looser claim using `2c/J_max+Lambda/lambda_max` alone would omit this interior action cap when `c lambda_max>J_max`.

These schedules presume the physical norm envelope is actually controllable. If `j(t)` is acquired fixed noise rather than a design variable, optimization over arbitrary `j` is not an authorized physical inference. Likewise reserved duration, exact endpoint operations, support, reset, and control costs remain charged.

For comparison, constant action AND constant intensity give `p/a^2=2(Lambda-1+exp(-Lambda))/Lambda^2`. This is strictly above `2/(Lambda+2)` when `Lambda>0`: the difference has numerator `Lambda-2+(Lambda+2)exp(-Lambda)`, whose derivative is `1-(Lambda+1)exp(-Lambda)>0`. Thus shaping the intensity can strictly improve this certificate while preserving action, total exposure and duration, provided the cap permits (7). At `Lambda=2`, the three certificate coefficients are `(1+exp(-2))/2` for constant intensity, `1/2` for the optimal Poisson schedule, and `1/3` for two ideal deterministic cuts. None is an actual measured error probability.

## 5. Deterministic exact cuts are a stronger ideal comparator

With exactly `N` ideal full pinches at prescribed times, let the `N+1` intervening blocks have actions `a_k>=0`, `sum a_k=a`. The same deletion/union certificate is

\[
 \sum_{k=0}^N a_k^2\ge\frac{a^2}{N+1},
 \tag{9}
\]

with equality when all actions are equal. Constant action uses equally spaced cuts. For any integrable nonnegative profile with no action atoms, cuts at equal cumulative-action quantiles also attain equality; flat action stretches do not matter.

At equal expected Poisson count `Lambda=N`,

\[
 \frac{a^2}{N+1}<\frac{2a^2}{N+2}\qquad(N>0,a>0).
\]

Therefore the optimized Poisson certificate does not improve on a matched ideal exact deterministic-cut resource. It has a different scheduling/damping interface. Poisson counts are unbounded even at fixed expectation; a hard-count or finite-duration-control budget needs separate analysis. This comparator does not establish which physical architecture is cheaper or feasible.

## 6. Adversarial verdict

The pushforward optimum, endpoint-atom optimizer, explicit constant-action schedule, and deterministic-cut comparison are mathematically correct under the stated domain. The exact endpoint operations, full-group pinching, independent fresh reservoir process, deterministic profiles, finite exposure, and unchanged geometry are substantive assumptions. Adaptive intensity tied to latent outcomes, arbitrary noisy detectors, discarded reservoirs that return, or replacement by generic multi-generator damping require a new argument.

The optimization is internally verified analytic capital. External correctness, historical novelty, hardware qualification, practical rates, and a physical memory advantage remain UNKNOWN.
