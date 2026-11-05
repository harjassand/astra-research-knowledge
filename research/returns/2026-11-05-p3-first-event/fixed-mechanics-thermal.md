# Fixed reciprocal mechanics can hide heat from an active mechanical port

The independent [complete construction](package/next4_physical/01_FIXED_MECHANICS_THERMAL_PORT.md) specializes an [existing Astra active-port nonidentifiability result](../2026-11-05-p2-tracial-acquisition/active-port-nonidentifiability.md). It fixes reciprocal mechanics, unit mobility, bath directions, force/observation port and rates, while changing only two reservoir temperatures. It is a stricter explicit realization within that physical class, not a new useful engine or a stronger general nonidentifiability theorem.

In dimensionless units take `A=diag(1,3)`, `c=(1,1)/sqrt(2)`, `v=(1,-1)/sqrt(2)`, covariance `Sigma_s=A^-1+s vv^T` and diffusion `D_s=(A Sigma_s+Sigma_s A)/2`, for `0<=s<4+2sqrt(5)`. The stationary native model is

```text
dX=(-AX+c u)dt+sqrt(2D_s)dW, Y=c^T X,
X_0~N(0,Sigma_s).
```

The force is physically conjugate to Y. Both internal directions are controllable and observable, and relaxation rates remain 1 and 3. The measured native covariance is `[exp(-|t|)+exp(-3|t|)/3]/2`; the impulse-response kernel is `[exp(-t)+exp(-3t)]/2`. Both are independent of s.

The exact path equation `Y=Y^0+g*u` therefore gives the same complete force/observation transcript under every well-posed causal controller, including finite force/slew limits, adaptive stopping, digitization, detector postprocessing and unlimited classical memory. Deterministic state observability does not identify hidden stochastic bath covariance through this incomplete port.

At s=0 the baths are at equilibrium. At s=4 their fixed-direction temperatures are `5-2sqrt(5)` and `5+2sqrt(5)`, with heat current **4/5** and entropy production **16/5**, yet the accessible mechanical record is unchanged. Maintaining the reservoirs is not free, and identical port work statistics do not grant extractable work at an unavailable load.

A trusted reset of the **full hidden covariance** or an added thermal port breaks the equivalence; these are additional acquired physical resources. Native stationary initialization and ideal white Markov baths are explicit premises. A finite microscopic reservoir, replenishment apparatus or ultraviolet cutoff is not constructed. An unbounded-entropy limit needs one bath temperature tending to zero and does not imply unbounded heat power.

[Audit results](package/next4_physical/audit_results.json) corroborate the exact model identities; they are producer mathematical diagnostics, not device measurements or a new Capital run. Brownian gyrators and prior Astra adaptive-port examples remain credited. The distinct [thermal-pulse identification result](../2026-11-05-p2-causal-payload-memory/thermal-pulse-identification.md) uses an additional calibrated physical port, so its positive acquisition claim is not contradicted. [Complete original package and provenance](SOURCES.json).
