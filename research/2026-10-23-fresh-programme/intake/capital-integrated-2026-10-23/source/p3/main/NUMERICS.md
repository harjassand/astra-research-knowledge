# Numerical contract and limits

The exact-model theorems and the numerical implementation are distinct.
The written proofs are human-readable derivations with exact diagnostic
checks, not proof-assistant verification. The statistical statement assumes
independent random draws from the specified dyadic proposal. Executed draws
use NumPy PCG64; hardware randomness and the PRNG are not formally verified.

## 1. Acquiring finite-bit bounds

Both compilers use integers representing a dyadic grid with **80 fractional
bits**, not growing exact rational trajectories. Lower recurrences round
down and upper recurrences round up. Their coefficient fractions in the
executed cases are exact dyadics. Integer magnitude can grow with the
horizon; the secant cubic has intermediate products of roughly three times
the grid bit length. Thus this is not a claim of unit-cost arithmetic on an
arbitrary-horizon 80-bit machine.

The derivative compiler uses O(Td) ring arithmetic and storage. The actual
secant implementation reuses one spatial impulse because the ring is
translation invariant; scoring every shifted impulse costs O(Td^2), with
O(Td) output storage. It does not enumerate histories. General nonhomogeneous
matrices, time-varying scores, and reachable cubes have larger costs described
in verification/SECANT_AUDIT.md. Those general costs must not be replaced
silently by the optimized ring cost.

At derivative criticality, outward rounding may create a positive plateau.
We certify the actual rounded sequence. We do not substitute its ideal
harmonic asymptotic into a floating certificate. An exact eight-bit
counterexample to that substitution is retained in the audit.

## 2. Proposal and certificate arithmetic

Proposals are rounded to **32-bit dyadic** Bernoulli probabilities, clipped
strictly inside (0,1). Simulation draws integers in [0,2^32) and compares with
the recorded numerator. Likelihood ratios use that same sampled probability.
The moment factor is recomputed for the actual grid point, so nearest-grid
rounding need not preserve the theoretical optimizer.

The endpoints logistic(logit(p)+ell/u) and endpoint risk calculations use
100-digit Decimal interval operations. In these cases the input fractions
have terminating decimal expansions shorter than this precision. Decimal
exp and ln are correctly rounded to their working precision; the code widens
their results by a full last-place unit. Addition, multiplication, division,
complement and accumulation round outward. The interval formula for odds
loses a little dependency information but remains an enclosure.

Extremely small probabilities are retained in log form. There is no need to
materialize a binary64 probability such as the scale case near 10^-324.

## 3. State and log-weight arithmetic

The simulator uses binary64 and clips states to the independently proved
invariant cube [-1,1]^d. Under round-to-nearest IEEE arithmetic, no overflow,
and the executed dyadic coefficients, a conservative per-coordinate local
state-map error is eta = 64 * 2^-53. This is deliberately much larger than
the operation-count bound: the neighbor average has absolute error below a
few units of roundoff, its two cubic multiplications remain on a bounded
domain, and the dyadic coefficient products and final additions add only a
few more. Clipping cannot enlarge the distance from the exact invariant state.
Subnormal arithmetic, if encountered, contributes negligible absolute error
relative to this allowance. The implementation has not been audited at the
instruction or library-kernel level.

For lambda=rho+3kappa<1, state error is <=eta/(1-lambda). At lambda=1 it is
<=t*eta at time t. The score allowance is respectively

    T * ||b||_1 * eta/(1-lambda)
    ||b||_1 * eta*T*(T+1)/2.

The code adds conservative gamma bounds for coordinate dot products and
time summation. Specifically, with u=2^-53, B=sum_j b_j, and L the largest
absolute log likelihood increment, it charges

    T * gamma_(8d) * (B+dL) + gamma_(8T) * T * (B+dL),
    gamma_n = n*u/(1-n*u).

Likelihood logarithms are evaluated with Decimal precision 100, converted
to binary64, and their conversion error is accumulated by choosing the
larger error of the two bit outcomes at each coordinate. The scoring offset
and the tested coefficients are exact dyadics. A further 1e-12 allowance is
included. The mean is aggregated using 60-digit Decimal exp and log in a
scaled representation; an additional 1e-35 aggregation allowance is stated.
The final high-precision confidence audit adds another 1e-12 for the displayed
log point. These are arithmetic-model allowances, not empirical fits.

The original result JSON displays binary64 confidence arithmetic. Its tiny
last-digit rounding is not used as an exact upper-bound assertion. The
separate audit_confidence.py uses the full preserved Decimal certificates,
outward exponentiation and a widened square root to check every advertised
5% target. All ten advertised target runs passed, with numerical allowances
included. The original source and result files remain unmodified.

## 4. Finite-sample meaning

For exact independent weights W with E W=Z and E W^2/Z^2<=K, Chebyshev gives

    Pr(|mean(W)/Z-1| > epsilon) <= (K-1)/(n*epsilon^2).

This is a finite-sample statement, not an estimated asymptotic standard
error. With a uniform computed log-weight error tau, the upper relative
error of the computed mean on that event is at most

    exp(tau)*(1+epsilon)-1.

The lower relative error is smaller for nonnegative epsilon. A 5% confidence
set for Z is obtained by inverting the event:

    [computed_mean/1.05, computed_mean/0.95].

The machine-readable audit records conservative Decimal endpoints. Without
the arithmetic and independence assumptions, retain the exact-model theorem
and label the simulation diagnostic. None of these confidence statements
account for misspecified physics or uncertainty in model coefficients.

## 5. Timing qualifications

Original certificate_seconds computes four proposals and their certificates
together. It is charged in full to each displayed per-method total. This is
conservative for a standalone optimized method. The separately computed
mean-path proposal certificate was not timed in its per-method subtotal;
the enclosing 120.051-second job receipt includes it. The particle method's
total_seconds is its own sampling/setup routine, not the same subtotal as
the iid methods. Do not rank those subtotals as a controlled speed benchmark.

The additional linear-baseline experiment runs one new stream to 182,528
paths and uses a predetermined 41,984-path prefix for the tighter certificate.
The prefix sampling time is proportional allocation, explicitly labeled,
not a separately measured run. Both aggregation costs are actually measured.
These caveats do not change the certified path-count comparison or the
observed failure of minimax to beat the elementary tilt in variance.

Official arithmetic API reference: https://docs.python.org/3.12/library/decimal.html (Decimal exp, ln, and context rounding). The executed runtime was Python 3.12.14; the currently served documentation identifies 3.12.15.
