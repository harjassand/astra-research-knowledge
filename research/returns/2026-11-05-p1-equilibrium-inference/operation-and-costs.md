# Attaining finite experiment, exact compiler and full costs

This page explains the operation attaining the [equilibrium-inference law](README.md). The [physical derivation](package/passive_programme/physical_operation.md), [main report](package/equilibrium_inference_20261105.pdf), [exact compiler](package/passive_programme/response_compiler.py) and [default certificate](package/passive_programme/response_certificate.json) are supplied unchanged. Capital did not execute them.

## Finite ramp and integrated observations

Raise a scalar input monotonically from zero to a plateau U during T/2, hold it for T/2, integrate the output over m+1 equal bins of width `h=T/[2(m+1)]`, and apply signed classical weights. Choosing `U<=min(U_max,V_max T/2)` respects finite peak and slew limits. No impulse, instantaneous jump, spectrum fitting or hidden-state access is needed.

After the ramp, every modal transient has an extra factor `a_r(lambda)` between zero and one. For `a=exp(-Lambda h)`, `b=exp(-mu h)`, define

```text
R_m(z)=T_m((2z-a-b)/(b-a)) / T_m((2-a-b)/(b-a))
      =sum_j w_j z^j,     R_m(1)=1.
S_hat=(mu/U) sum_j w_j Ybar_j.
```

Here T_m is the Chebyshev polynomial. Bin integration contributes another factor `(1-exp(-lambda h))/(lambda h)` between zero and one. The exact bias is minus the integral of `mu/lambda * a_r(lambda)` times that bin factor and `R_m(exp(-lambda h))`. Its magnitude is bounded by the reciprocal denominator `1/T_m((2-a-b)/(b-a))`. Thus the same weights preserve the static term and suppress every allowed transient.

The required degree is of order `min(sqrt(kappa)L,L^2/s)` for the theorem's accuracy range. Statistical and systematic amplification are paid:

```text
Var(S_hat)=mu^2 sigma^2/(U^2 h) * sum_j w_j^2,
A_m=sum_j |w_j|
   =T_m((2+a+b)/(b-a)) / T_m((2-a-b)/(b-a)).
Arbitrary bin error <=delta adds at most (mu/U) A_m delta.
```

Independent repetitions reduce random sensor noise, but cannot average away arbitrary systematic bin errors. The compiler uses exact rational arithmetic and the enclosing interval `a=max(0,1-Lambda h)`, `b=1/(1+mu h)`. It certifies its own bias, weight normalization, amplification, squared norm, repetition count and error allocation. That enclosure can enlarge finite costs; a software degree limit is not an impossibility theorem. Exact compiler arithmetic does not certify the hardware or a separately synthesized lower-witness plant.

## Supplied executed evidence

The [compiler checks](package/passive_programme/compiler_checks.json), [moment witnesses](package/passive_programme/moment_witness_checks.json), [saved-witness reload](package/passive_programme/saved_witness_checks.json), and [independent grid](package/passive_programme/audit_grid.json) record actual source-side computations: 12 exact recipes, 60 positive finite spectra of dimensions 1 through 128, separate finite-ramp/bin integration checks, four moment-matched hard families and 120 scalar challenges. They support implementation consistency; the analytical argument carries the theorem. No physical trials were performed.

For `mu=1, Lambda=16, T=0.1, epsilon=1/16, U=sigma=1`, confidence 0.95, the rational compiler gives degree 10, 11 bins, bias bound 0.0122397272, amplification about `2.48e18`, sufficient repetitions about `1.37e43`, and permitted arbitrary digitization error per bin about `6.30e-21` under its allocation. T=0.1 is outside the narrower asymptotic theorem range, while this exact finite certificate remains valid. These are sufficient costs of this estimator, not evaluated optimal costs or an executed laboratory experiment. The separate ideal-step numerical witness check uses different endpoints and allocation; its counts are not interchangeable with the ramp compiler's.

One saved hard pair has kappa=4096, s=1/2048 and 68 support points across the pair, static-response gap about 0.1270833585, and an analytical whole-interval impulse-difference bound of `1.636e-73`. Smaller sampled differences do not replace that uniform bound. The supplied [crossover figure](package/passive_programme/resource_crossover.png) plots the theoretical scale, not numerically evaluated optimal effort or known leading constants.

## Reset, reuse, work and control remain paid

Known positive finite spectra admit a deterministic series connection of parallel RC branches with `C_j=1/p_j`, `R_j=p_j/lambda_j`. Positive finite circuit realizability does not establish manufacturability to the precision demanded by a hard pair.

Zero-state trials are granted in the main information interface. From an initial-state norm bound B, passive reset for W leaves at most `B exp(-mu W)` and estimator contamination at most `(mu/U) A_m B exp(-mu W)`. To allocate epsilon_p, a sufficient wait is

```text
W >= (1/mu) [log(mu A_m B/(U epsilon_p))]_+.
```

Reset can take much longer than T. Reading a long reset trace supplies older-response information and changes the lower-bound interface. Serial repetitions pay every reset and interrogation; parallel repetitions pay identically prepared copies and measurement channels. A private-sign construction for bounded unknown initial states is a separate upper result, not a matching lower theorem for unrestricted continuous reuse. Retained-loaded-plant preparation from earlier Astra work is not a free reset theorem for this experiment.

Detector bandwidth must resolve m+1 integrated bins in T/2. The coefficient recurrence takes O(m^2) arithmetic operations, with growing rational bit lengths and cancellation precision also paid. Squared-drive effort is not port work. Calibration, normalization, clock drift, saturation, nonlinearities, protection from systematic error and total wall time remain distinct costs. Constant offset is less amplified because weights sum to one; general bin-dependent bias remains severe.

## Thermal extension has an upper guarantee only

For the additional zero-start plant `dx=(-Ax+bu)dt+sqrt(2 Theta A)dB_t`, with thermal noise independent of sensor noise, output covariance is `Theta[k_nu(|t-v|)-k_nu(t+v)]`. The estimator's extra variance is at most `(mu/U)^2 Theta A_m^2`. Independent repetition adds sufficient normalized effort of order

```text
(Theta T/sigma^2) A_m^2 epsilon^-2 log(1/alpha).
```

The upper exponent is retained at a fixed thermal-to-sensor ratio. The final internal review explicitly added this factor. The adaptive sensor-noise lower theorem does not automatically extend: parameter-dependent fluctuations can themselves reveal unknown response information, and some equilibrium variances can encode the static target directly. Preparation and fluctuation law must be specified before any physical claim.
