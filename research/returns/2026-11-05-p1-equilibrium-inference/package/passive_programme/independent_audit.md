# Independent in-session audit

Date: 5 November 2026. Reviewer: the independent quantum-construction agent in this session. This is an internal mathematical review and finite numerical challenge, not external peer review, formal proof verification, a priority determination, or a physical experiment.

## Material reviewed

- `bandwidth_accuracy_theorem.md`: normalized positive spectral class, direct bin estimator, reciprocal-approximation dual witness, joint parameter choices and claimed logarithmic minimax exponent.
- `physical_operation.md`: arbitrary predictable force inputs, adaptive trials, Gaussian readout, monotone ramp, finite bin integration, variance, preparation, reuse and calibration.
- `response_compiler.py`: exact rational enclosing interval, Chebyshev recurrence, weight normalization/amplification identities, stopping test, Gaussian repetition bound and error allocations. The reviewer read this code; the separate numerical challenge described below does not use its coefficient compiler.

## Mathematical findings

No counterexample or central proof gap was found under the stated domain: normalized spectral mass one, known positive lower rate, known finite upper rate or the unbounded upper-rate class, kappa at least 16, normalized horizon at most 1/64, and absolute susceptibility error at most 1/16.

1. The classical reciprocal minimax error and alternation dual produce genuine positive probability measures with matching moments. The Lagrange leading-coefficient weights have the requisite alternating signs and zero moments. The explicit phase-node formula agrees with the exact degree-zero endpoints and degree-one interior extremum x=sqrt(K). The general formula remains a claimed classical-approximation consequence; this review is not a new proof of its source theorem.
2. The choices K=min(kappa,[L0/(8e tau)]^2) and m=floor(sqrt(K)L0/4) keep K at least 16 in the declared range, give a target gap greater than 4 epsilon, and make the exponential Taylor-remainder base at most one half. The capped-bandwidth lower bound stays uniform: the function sqrt(kappa)L log(1+L/(tau sqrt(kappa))) increases to L^2/tau, so the capped construction covers every larger bandwidth.
3. For arbitrary causal control, the two models use the same input functional on the same observed path. Young's inequality bounds the squared drift discrepancy by eta^2 T^2 times force effort. The almost-sure total effort bound supplies integrability for the Gaussian change-of-measure argument. Feedback, nonlinear inference and adaptive trial counts therefore do not evade the stated two-point lower bound. Bounded stopping/localization is needed when presenting unbounded trial-count policies.
4. A monotone ramp followed by a plateau yields exactly the static susceptibility minus a positive modal filter times exp(-lambda t). Bin integration adds another filter in [0,1]. The polynomial's normalization R(1)=1 therefore targets the static functional directly, with the stated uniform residual bound. Negative weights occur in classical postprocessing only.
5. The finite-bandwidth and unbounded-bandwidth degree inequalities are correct for the exact exponential interval. The positive roots give the exact l1 coefficient identity. Their growth yields the claimed crossover tau sqrt(kappa) of order log(1/epsilon).
6. The rational interval used by the compiler is genuinely enclosing. It can require a larger degree than the exact exponential interval. The compiler explicitly verifies its own rational bias certificate, so it does not rely on transferring the exact-endpoint degree constant unchanged. Its normalization and amplification assertions use exact Fraction arithmetic. Its Gaussian tail bound uses a conservative logarithm upper bound and is valid.

## Independent finite challenge actually executed

`audit_grid.py` uses 100-decimal-digit mpmath scalar formulas rather than constructing monomial coefficients. It checked 120 combinations:

- normalized horizons 1/64, 10^-3, 10^-6, 10^-10;
- bandwidth ratios 16, 100, 10^4, 10^8, 10^20 and infinity;
- absolute errors 1/16, 10^-3, exp(-30), exp(-100), exp(-1000).

Every exact-endpoint degree choice met the advertised epsilon/2 bias bound. Every lower construction had K at least 16, m+1 at least two, susceptibility gap greater than 4 epsilon, and Taylor base at most one half. Over this finite grid, the minimum gap/(4 epsilon) was 2.00000000525; the minimum negative log kernel-bound divided by the claimed exponent was approximately 0.00199214; the maximum logarithmic precision-cost bound divided by that exponent was approximately 2.24668. Results are in `audit_grid.json`.

These numbers test consistency across disparate regimes. They are not universal constants, an interval certificate, or a substitute for the analytic proof. The asymptotic argument, not the grid, supports the theorem.

## Scope and interpretation cautions

- Coupling normalization means ||b||_2^2=1. The lower rate, upper rate and normalization are supplied calibration/prior information. Their uncertainty creates systematic error; it is not removed by averaging.
- T bounds the maximum age of a freshly acquired response. It is not a bound on total serial laboratory time. A continuously evolving plant retaining earlier excitations can supply information from ages greater than T and is outside the lower-bound interface.
- Rapid exact zero-state preparation is not derived for an arbitrary unknown scalar-port plant. The formal interface grants those trials. A reusable physical apparatus must pay a real reset mechanism, passive waiting, or independently prepared specimens.
- The private-sign extension for bounded initial states is valid as a separate upper construction, including martingale concentration when initial states depend on previous signs but not the fresh current sign. It does not automatically extend the matching lower bound to unrestricted continuous reuse.
- Noise must be parameter independent additive Gaussian sensor noise for the effort theorem. Equilibrium thermal fluctuations, hidden-coordinate observations, controllable changes to A, or a fixed known low model order can change the inference problem substantially.
- The resource is squared force effort, not automatically thermodynamic work. Peak force, slew, bin bandwidth, reset hardware, wall time and protection from systematic drift remain separately charged.
- Hard finite spectra exist mathematically, but approximate root finding and highly cancelling moment weights need controlled precision. Floating-point moment residuals do not alone establish the small uniform kernel discrepancy. The analytic Taylor bound supplies that certificate once the exact moment construction is specified; physical realization/calibration requires additional tolerances. The compiler's rational upper certificate does not by itself certify a numerically synthesized lower-witness plant.
- The result is a completed resource law in a declared experiment class. Ordinary Chebyshev extrapolation attains its exponent; there is no established advantage over the best same-access ordinary method. The close Brown--Grabovsky result and classical reciprocal approximation must remain attributed. Worldwide novelty and civilisation-changing impact have not been established by this review.

## Final thermal-extension review

The physical-construction agent separately checked the report's additional zero-start thermal model dx=(-Ax+bu)dt+sqrt(2 Theta A)dB, with B independent of the sensor Brownian noise. Its output covariance is exactly Theta[k(|t-v|)-k(t+v)], bounded in magnitude by Theta. Finite-bin averaging and signed weights therefore add variance at most (mu/U)^2 Theta A_m^2. Independent repetitions add sufficient normalized effort of order (Theta T/sigma^2) A_m^2 epsilon^-2 log(1/alpha). The report explicitly fixes or retains this noise ratio before comparing exponents. This is an upper construction only; parameter-dependent thermal covariance is not covered by the main adaptive lower theorem.

The same review checked the normalization log(1+B_star)=Theta(Phi) and the optional amplitude cap U<=sigma mu/sqrt(T), which makes a rounded extra trial cost at most one normalized effort unit. No additional physical experiment or external review is implied.
