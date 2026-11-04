# All-deadline relative first-failure CDF sensitivity

This separate completed classical companion proves a uniform sensitivity theorem, its shared-backbone calibration corollary and a finite-implementation precision law. Read the [complete derivation](package/independent_routes/reliability/COMPLETED_RESULTS.txt). The proposed efficient whole-CDF computation was [explicitly unfinished at this return](package/independent_routes/reliability/UNFINISHED_COMPUTATIONAL_EXTENSION.txt). The subsequent [new finite all-deadline certificate](../2026-11-05-p3-passive-calibration/reliability-curve-certificate.md) now closes that computational construction under its own stated premises and costs. This page retains the earlier completed sensitivity result and its history. The quantum calibration audit is not automatically assigned to this independent route.

## Positive killed-operator comparison

For positive definite self-adjoint `K0,K1` with `exp(-eta)K0<=K1<=exp(eta)K0`, define `h_i(t)=<v,[I-exp(-tK_i)]v>`. Then the same `exp(+-eta)` sandwich holds for every real `t>0` simultaneously. In discrete time, if both `K_i<=I`, the analogous statement holds for `<v,[I-(I-K_i)^j]v>` at every integer `j>=1`. Noncommuting endpoints are allowed. The uniform exponent is sharp at discrete deadline one and in the continuous short-time limit; this does not assert sharpness for every particular model/deadline.

The proof uses the geometric path `K_s=K0^(1/2)(K0^(-1/2)K1K0^(-1/2))^s K0^(1/2)`, which satisfies `-eta K_s<=dot K_s<=eta K_s`. In the discrete case it stays a positive contraction by the weighted arithmetic-geometric bound. Differentiating the failure function and applying an energy identity bounds its log derivative by eta. The path need not itself be a Markov generator. One deterministic inequality covers all deadlines; no union bound over infinitely many queries appears.

## Exact reliability interpretation and calibrated uncertainty

Take finite irreducible reversible chains/generators with the **same invariant law pi, same failure set B, and deliberately prepared equilibrium-conditioned safe start** `nu=pi(.|A)`, `A=B^c`. The CDF is the quadratic killed-operator expression divided by `pi(A)`. Discrete endpoint kernels must have nonnegative spectrum, for example be lazy, at the same actual physical tick duration. Continuous-time generators need no laziness condition.

If a single simultaneous event gives `|E_true-E_fit|<=rho E_fit`, `0<=rho<1`, then at every deadline,

```text
(1-rho) F_fit <= F_true <= F_fit/(1-rho).
```

When both forms contain the **same positive operating backbone E0** and `|E_true-E_fit|<=rho E0`, their mutual comparison instead gives the sharper

```text
F_fit/(1+rho) <= F_true <= (1+rho)F_fit,
```

for any `rho>=0`. This is the recommended constant for the [accepted P2 unknown-local-port construction](../2026-11-05-p2-unknown-local-ports/README.md). Its prepared collision acquisition, positive bands for zero observations, product invariant law, declared bounded reach, native refresh, calibration confidence and full physical service costs remain governing conditions.

The relative uncertainty has no extra factor of deadline, lifetime, inverse failure probability or state count **for this common-invariant form comparison**. It controls failure CDF, not relative error in the tiny late survival tail. It is not a theorem for arbitrary fixed-point/all-working starts or uncertain pi. In discrete time, reconstructed generator rows alone do not supply a stochastic lazy kernel; actual row constraints and null ticks must be earned and charged. `Q=(P-I)/T` preserves a mean after clock conversion but **does not preserve the CDF**.

If a separate computation supplied simultaneous fitted intervals `[L,U]`, the shared-backbone result would expand them to `[L/(1+rho),min(1,(1+rho)U)]`, with endpoint-width multiplier `(1+rho)^2`. This conditional transfer does not complete the missing full-CDF computation.

## Separate finite physical precision theorem

Let the ideal lazy chain have certified gap `g>0` and stationary failure mass `p>0`. An actual process may be nonreversible and history-dependent, provided **every admitted conditional next-step law** is within total variation v of the ideal kernel and initial law is within delta of nu. Stopped maximal coupling gives

```text
|F_actual(j)-F_ideal(j)| <= delta+v E_nu[min(j,tau_B)],
|F_actual(j)/F_ideal(j)-1| <= (delta+v)/(g p),  j>=1.
```

Thus a uniform relative implementation claim still requires absolute errors of order `epsilon g p`. A two-state heat-bath example with `F(1)=g p` proves that this precision dependence is necessary in general. A stationary average error or good one-bit marginals do not provide the conditional contract. The strong stable-basis independent/nonbackacting verified-write model can suppress errors with checks logarithmic in inverse p, but writes, retries, sensor assumptions, protected storage, reset and padded service remain real costs; systematic floors and omitted mechanisms are not cured.

For continuous time, exact initialization and discrepancy intensity v give relative error at most `v/(gamma p)`. Arbitrary initial total-variation error can put an immediate failure atom in B while the ideal CDF tends to zero, so it cannot give an all-positive-time relative bound. Exact safe initialization or a stronger multiplicative initial-law guarantee is required. The discrete theorem begins at deadline one intentionally.

Classical spectral mixtures, reversible rare-event approximations and form perturbation have strong existing predecessors credited in the full proof. Historical priority and a new practical capability are not established. No physical experiment, new Capital audit or scientific program rerun occurred. The [route status](package/independent_routes/reliability/STATUS.txt) and [unfinished extension](package/independent_routes/reliability/UNFINISHED_COMPUTATIONAL_EXTENSION.txt) preserve the computational obligations at that earlier return; the new completion is linked above. [Original package and hashes](SOURCES.json).
