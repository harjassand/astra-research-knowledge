# Receiving review: untuned partial thermal carrier

**Original actual input:** `UNTUNED_PARTIAL_THERMAL_CARRIER.md`, SHA256 `b37e49509e6fc5e3eb0436f330c24159770be73ebb405f6705670d790ee3eb00`.

**Binding correction:** `UNTUNED_CARRIER_ARMING_SCOPE_CORRECTION.md`, SHA256 `97c9d2d0e6d4627677c55c2bf51d47521b1897ea4a1d6515ab185379549ad6cd`.

Exact snapshots of both inputs are preserved in this directory under their names with `REVIEWED_` and their first twelve hash characters. Neither root input was edited by this role.

**Verdict: accepted as original plus correction.** The exact current cell, mobility/noise relation, compact uniform stability, Gaussian-reference endpoint estimate and conditional absolute-work bound were reconstructed independently. The correction closes the one substantive scope omission found during the actual-file review.

## 1. Exact physical cell and response

Integrating the transport segment and the free bath segment gives the displayed M, d, ell and d0. Force acts through both segments, and all carrier displacement is counted. Partial rotation produces the next state noise, not a direct innovation in the current cell before that rotation. The unread source is independent of the information selecting the fixed force.

The determinant is `(1−cos(theta))(1+r)`. Inverting the two-by-two matrix yields the displayed k, with

\[
k_Y=-\frac{2/g+b\cot(\theta/2)}{1+r},\qquad
\mu=\frac{1-r}{2(1+r)}[2/g+b\cot(\theta/2)]^2,
\qquad \sigma^2=2\mu.
\]

On the actual compact positive-angle class, mu and its reciprocal have uniform finite bounds. No tuned quarter angle, full refresh or identified kinetic coefficient is used by the sign controller. The positive branch is load-bearing: the preserved `theta=3pi/2, g=1, b=2, r=0` example is stable but has `Delta A=Delta P` and zero sustained mobility.

## 2. Stability and the actual observed error

The two-step observation matrix has determinant `−sin(theta)` and squared Frobenius norm at most two. This verifies

\[
\|M^2\|^2\leq1-(1-r^2)\sin^2\theta/2<1
\]

uniformly on the stated compact class. The thermal covariance identity `MM^T+nn^T=I` is exact. Starting from the supplied aggregate Gaussian preparation, the unforced reference recursion remains Gaussian with covariance RI; its temporal correlations are retained. Under any adapted bounded force, the forced convolution is bounded pathwise by CRa. The actual feedback-controlled state is not incorrectly assumed Gaussian.

These facts give the claimed endpoint and within-period maximum estimate. The detector reads true A, while the unmeasured state corrector is controlled analytically. The prior scalar queue applies using uniform gain/noise bounds. The local sensing energy envelope remains a separate actual requirement. Fixed unknown common parameters within one lane are covered; arbitrary per-carrier mismatch or pulse jitter is not silently included.

## 3. Actual work and the repaired arming premise

Actual work is the integral of F times the actual aggregate velocity P. The reference-plus-forced decomposition bounds its magnitude on armed histories. The deterministic forced part contributes a factor proportional to `Ra p_arm`; the Gaussian maximum contributes `sqrt(R log N) sqrt(p_arm)` by Cauchy--Schwarz. This proves equation (14) without dropping force/state correlations or replacing true displacement by corrected displacement. It does not imply exact work nonnegativity for arbitrary finite-memory feedback, and the draft explicitly avoids that claim.

The original Section 5 did not explicitly restrict the nonlinear target for its rare-arming probability. I supplied the allowed target `phi(t,h)=v t`, v nonzero: despite an unforced native martingale, the auxiliary target grows to order N² and the apparatus arms with probability tending to one. This leaves tracking intact but defeats the rare-arming premise.

The actual correction now imports all needed assumptions: `phi(t,0)=0` for every time; an actual unforced native aggregate martingale; actual zero force before the trigger; and the smaller whole-horizon observation/evaluation error `o(N^(3/2) log N)` with superexponential failure. With bounded spatial derivatives, the first condition gives `|Z_N|<=C|B|`. Native and corrected-auxiliary maximal inequalities then prove the stated arming probability, and (14) gives vanishing expected absolute net force work. The stronger energy/clock/source bill remains unpaid by this particular work statistic.

No further mathematical correction was found. The root's new ODE execution was reported to this role but was not independently rerun or certified here; this receipt is based on the actual written equations and their analytic reconstruction. No additional optional tests or agents were used.
