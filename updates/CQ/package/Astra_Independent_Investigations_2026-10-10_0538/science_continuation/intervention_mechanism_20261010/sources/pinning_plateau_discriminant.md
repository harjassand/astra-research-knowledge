# Quantitative plateau test for an occupancy-threshold bearing

2026-10-10. Analytical derivation only; no discovery or validation trajectories inspected. This test concerns a restricted fixed sinusoidal bearing model. It does not turn speed into a direct occupancy measurement.

## 1. Correct mean-speed formula

Let theta be rotor angle in radians, gamma rotational drag, tau the approximately speed-independent torque per active stator, N its integer count, and B the amplitude of the periodic resisting torque. At zero temperature:

    gamma dtheta/dt = N tau - B sin(q theta).

For positive N tau > B, the traversal time over one period L = 2 pi/q is

    t_period = gamma integral_0^L dtheta / [N tau - B sin(q theta)]
             = gamma L / sqrt[(N tau)^2 - B^2].

Thus mean angular speed is sqrt[(N tau)^2 - B^2]/gamma. In revolutions per second:

    v_N = A sqrt(N^2 - rho^2),
    A = tau/(2 pi gamma),   rho = B/tau.

The harmonic q cancels from mean speed. Below or at threshold N <= rho, deterministic long-time speed is zero. At finite temperature the strict threshold is rounded by activated creep, so zero here means below the experiment's finite-time resolution. The potential's peak-to-trough energy barrier is 2B/q; an energy barrier is not numerically the same as resisting torque B.

The independent, unpinned constant-torque model is v_N = A N. Both formulas presume an OFF plateau, negligible acceleration, constant drag, additive equal stator torques, and operation in a sufficiently flat single-stator torque-speed region.

## 2. A scale-free test with three consecutive moving plateaus

Suppose v_0, v_1, v_2 are successive plateaus due to single-unit additions. Their unknown absolute occupancies are m, m+1, m+2. Put y_j = v_j^2. Then

    y_j = A^2 j^2 + 2 A^2 m j + A^2(m^2 - rho^2).

Define D = y_2 - 2 y_1 + y_0. If D > 0, the exact model gives

    A^2   = D/2,
    m     = (y_1-y_0)/D - 1/2,
    rho^2 = m^2 - 2 y_0/D.

Therefore unknown gamma and tau do not prevent identification of the dimensionless barrier rho and unknown occupancy offset m *within this model*. The data identify A, not gamma and tau separately. The inferred m must be a positive integer; rho^2 must be nonnegative; and m > rho. If v_0 is truly the earliest possible moving state reached by single additions from a pinned state, additionally m-1 <= rho < m.

Three levels exactly determine the three continuous parameters, so an unconstrained exact fit alone is not evidence for the mechanism. Integer/range restrictions do test it. Four or more consecutive levels provide an additional check: every second difference of v_j^2 must equal the same 2A^2.

Equivalent simpler invariant:

    v_{j+2} - 2 v_{j+1} + v_j < 0 for any rho > 0;
    v_{j+2} - 2 v_{j+1} + v_j = 0 for rho = 0.

This follows from d^2 v/dN^2 = -A rho^2/(N^2-rho^2)^(3/2). Successive speed increments diminish as the motor moves away from depinning. A weak barrier or measurements far above threshold can make this curvature arbitrarily small. Positive speed curvature is inconsistent with either idealized model and suggests changed torque/drag, skipped levels, or another process.

## 3. Particularly useful hidden-first-stator bound

If the first two moving levels are exactly u and 2u, the washboard fit requires

    rho^2 = m^2 - (2m+1)/3,
    v_2/u = sqrt[(14m+13)/(2m+1)].

For m=1, rho=0 and v_2/u=3: ordinary first, second, and third active units.

If the threshold masks at least one whole active stator, m >= 2, then

    sqrt(7) < v_2/u <= sqrt(41/5) = 2.86356.

The closest hidden-occupancy alternative (m=2) therefore predicts at least a 4.55% shortfall from the third linear plateau 3u. The associated second speed increment is at most 0.86356 of the first increment. Two moving levels cannot discriminate: any integer m >= 2 has a suitable rho reproducing their ratio of two. The third level supplies the discriminant.

Do not apply this exact-ratio bound to noisy data as if v_1/v_0 were exactly two. Fit all three speeds jointly, allowing uncertainty in that ratio. A more general decision is to profile rho; if its upper confidence bound is below 1, the fixed sinusoidal barrier cannot mask a complete first active stator, although a weaker bearing barrier can still exist.

## 4. Sensible estimation with real traces

- Fit measured plateau speeds directly with their correlated uncertainties. Squaring noisy estimates adds a variance bias; the squared-speed formulas are diagnostic algebra, not necessarily the best estimator.
- Analyze within each motor/run, with its own A. Do not pool raw speeds across cells with different drag or PMF. Preserve motor-level clustering in uncertainty calculations.
- Compare the no-barrier m=1 model against discrete m>=2 models satisfying m-1 <= rho < m, using identical plateau selection and censoring. Use profile likelihood or simulation-calibrated comparisons; ordinary nested chi-square assumptions need not hold.
- Establish consecutiveness independently as far as possible. Missing a fast intermediate level, two nearly simultaneous arrivals, or a torque activation step invalidates the indexing. A selection procedure that favors equal spacings would make the test circular.
- Predefine plateau duration/stability requirements and all exclusions before applying to untouched cells. OFF epochs are short; near-threshold stochastic dwell cycles can bias estimated means.
- If angle is retained, repeatable phase-localized dwell slowing is a complementary bearing prediction. It is not unique: angle-dependent body drag and surface contacts must be distinguished from a molecular harmonic.

## 5. What can and cannot be rejected

With precise, consecutive levels close to u, 2u, 3u, the data can reject a **fixed, sinusoidal, effectively athermal threshold masking one or more equal active stators** without directly imaging occupancy. This rejection is conditional on the mechanical and indexing assumptions above. The experiment cannot decisively reject all occupancy-masking or hidden-activation mechanisms from mean plateaus alone.

One explicit counterexample shows the broader nonidentifiability. Let a motor have static friction large enough to pin N <= m-1, but after sliding begins let a constant kinetic resistance K=(m-1)tau oppose rotation. Then its successive moving speeds are

    v_{m+j} = [(m+j)tau-K]/(2 pi gamma) = A(j+1).

They are exactly u, 2u, 3u, ... although the first visible plateau contains m active stators. This is not the sinusoidal conservative-potential model; it demonstrates why rejecting that particular potential is not equivalent to rejecting mechanical masking. History-dependent barriers, changing stator torque, and physical occupancy versus conducting occupancy offer further alternatives.

Conversely, negative plateau curvature would support the restricted model's prediction but would not establish it: nonlinear torque-speed behavior, changing drag, and unequal active-unit torque can mimic it. Orthogonal occupancy imaging or independently calibrated torque and mobility is needed to identify molecular occupancy unambiguously.

## Prior-art position

The overdamped tilted-periodic-potential calculation is a standard mechanical model, not a proposed new law. Its application here is a targeted falsification strategy. [Rieu et al. 2026](https://www.nature.com/articles/s41467-026-74079-9) measured stator-independent bearing wells and heterogeneous dynamics, motivating a competing bearing explanation but also warning that a single stationary sinusoid may be too simple. [Ito et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8163892/) inferred active-unit changes from tethered-cell speed and discussed pinning when opposing torque arrested motion. [Wadhwa et al. 2022](https://www.nature.com/articles/s41467-022-33075-5) modeled physically distinct states with indistinguishable torque output. None of these references makes the present trace-only inference a direct stator count.
