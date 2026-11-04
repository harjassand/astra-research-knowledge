# Finite passive current records cannot universally upper-certify transport

This independent [complete obstruction](package/independent_routes/next3_observational/transport_no_go.md) asks whether finite equilibrium-current observations can certify the entire Green–Kubo correlation integral without an externally supplied relaxation bound. It gives a two-dimensional passive reversible counterexample, fixed-window and adaptive-stopping confidence results, and a conditional tail bracket. It does not supply a universal transport predictor or claim a new physical mechanism in a particular material.

## A small hidden slow contribution with arbitrarily large area

Start stationarily in the stable reversible OU model `dZ=-Q_lambda Sigma_rho^-1 Z dt+sqrt(2Q_lambda)dW`, where `Sigma_rho=[[1,rho],[rho,1]]`, `Q_lambda=diag(1,lambda)`, `0<lambda<=1`, `|rho|<1`. Observe only `J=Z_1`, granting noiseless continuous recording, unlimited computation and finitely many exact equilibrium starts. The generator/hidden coordinate and a positive relaxation floor are not provided.

Every model has observed variance one, quadratic variation `2t` and initial correlation slope minus one. Yet its transport integral is exactly `K=1+rho^2/lambda`. Choosing `lambda=rho^2/(M-1)` gives arbitrary finite K=M while the finite current law approaches the same unit-OU reference as rho tends to zero. The process remains strictly ergodic and passive; no negative damping or nonstationarity is required.

For m runs of total duration B, with `u=rho^2`, full-path relative entropy is `-(m/2)log(1-u)+B(1+lambda)u/[4(1-u)]`. Projection onto current only reduces information, and Pinsker bounds observed TV. Matching the noise quadratic variation prevents ideal continuous observation from distinguishing the family instantly.

A uniformly covering upper confidence endpoint must be infinite under the reference with probability at least its promised coverage. An adaptive method with uniform false-upper-bound probability at most alpha can stop with a **finite** endpoint under the reference with probability at most alpha. Apparent plateaus, residuals or longer passive data do not manufacture the missing relaxation certificate. Pointwise consistency at growing duration and useful performance on a restricted class are not refuted.

The coefficient also has a supplied passive Langevin free-particle realization as diffusion/zero-frequency mobility. No isolated fixed-material many-body Hamiltonian realization is claimed. If the full exact generator is known, this two-dimensional coefficient is simply a matrix-inverse query; the theorem concerns the restricted passive-current experiment, not every known-generator computational technique.

## Conditional positive statement and evidence

If an independent premise supplies a reversible positive exponential spectral representation with floor `g>0`, then for partial integral R_T and nonzero residual correlation,

```text
C(T)^2/[-C'(T)] <= K-R_T <= C(T)/g.
```

The gap must be earned independently; the negative theorem prevents extracting a universal positive value from the same unrestricted finite passive record. Oscillatory/nonreversible correlations do not automatically have this representation. Zero residual is handled separately, not by `0/0`.

The [recorded matrix diagnostic](package/independent_routes/next3_observational/verification_results.json) chooses rho=.01, K=1000 and duration 100: tested covariance difference is below `.0001`, path-TV upper bound about `.0357089`, partial integral about `1.0098`, and remaining area about `998.9902`. These are checks of analytic formulas, not Monte Carlo discovery or observed material data. [Supplied figure](package/independent_routes/next3_observational/transport_counterexample.png), [original program](package/independent_routes/next3_observational/verify_transport.py).

Cepstral transport estimation, STACIE and intervention/coupled-trajectory control variates are strong compared methods with their own premises; the source does not claim they promise the universal certificate refuted here. Equilibrium starts were granted, even though preparing very slow modes can itself cost long physical time. No new Capital calculation, physical experiment or priority audit was performed. [Original package and provenance](SOURCES.json).
