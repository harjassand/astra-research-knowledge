# Certified decision bounds for source-model thermal avalanches

This is an independently written computational extension of the published model, not physical material validation or a priority claim. This bound implementation does not import or run upstream code; the separate source-acquisition provenance records an earlier upstream-function execution. Source model and exact static representation: `../failure_source_benchmark/ASSESSMENT.md`.

## Proven bound and why the first bound was inadequate

Use the established internal-time population K(u), extinction time U*=T_1, and psi(k)=exp(-F/(kT)). Originally feasible counts are those k with |A_k|>=k, A_k={i:s_i>F/k}. Their minimum and maximum are k_min and n0. Every positive population lies between them, proving psi(k_min)U*<=tau<=psi(n0)U*. The resulting simple early-failure upper bound is valid but very loose: at n400,f0=.175,T=.15,t=.1 it is approximately 1.30e-15, much worse than the informed Poisson bound 8.59e-45.

A stronger bound is available for every fixed m:

    tau = integral psi(K(u)) du >= psi(m) T_m,
    P(tau<=t) <= P(T_m<=t/psi(m)) = P(K(t/psi(m))<m).

The equality holds up to continuous clock boundaries. Any selected m gives a rigorous bound; no optimizer certification is necessary. We used the smallest maximizer of |A_m|-m+1, a deterministic strength-only choice. For the .175/.15 fixtures these are m43(n100),m166(n400); for grid midpoint .15/.1 they are m37,m142. A floating-point scan independently found m43 and m166 minimizing the one-level bound at each tested deadline for the .175/.15 fixtures. This is a bound on the failure probability in the stated model, not an evaluation of that probability or a relative-accuracy certificate for it.

## Positive boundary DP

Sort strengths decreasingly s_1>=...>=s_n. At fixed u let independent B_i=1{E_i>u} with probability p_i=exp(-exp(-s_i/T)u). Write C_j=sum_{i<=j}B_i. The event K(u)<m is exactly that, for every prefix j, either C_j<m or s_j*C_j<=F. Indeed a violating prefix witnesses at least C_j eligible survivors; conversely any feasible survivor count >=m has a violating eligible prefix.

Starting with suffix value h_n(c)=1, move backward through j=n,...,1. Gate g_j(c)=h_j(c) if c<m or s_j*c<=F, zero otherwise, and set

    h_(j-1)(c) = (1-p_j)g_j(c) + p_j*g_j(c+1).

The answer is h_0(0). This uses only nonnegative products and sums, O(n²) work and O(n) memory. No subtraction of a near-one final probability occurs. Computation of 1-p uses -expm1(-lambda*u).

## Strong informed comparator

Failure requires at least r*=max_k(|A_k|-k+1)_+ actual thermal triggers. To see this, deletion must reduce every |A_k| below k, requiring at least that many deletions. Deleting the r* strongest fibers simultaneously satisfies all nested constraints. Mechanical closure does not alter existence of stable subsets, so the same minimum applies to actual thermal-trigger sets despite intervening avalanches.

For any stable k, the maximum possible total physical hazard R(k) is exp(F/(kT)) times the sum of the k largest lambda_i among A_k (the k weakest eligible strengths). Thus a simple comparator is Poisson(Rmax*t)>=r*, Rmax=max R(k).

We additionally implemented the stronger state-informed pure-birth comparator used in this analysis. After ell thermal triggers, any surviving k satisfies:

- k<=n0-ell;
- |A_k|-k<=ell, because a mechanically removed fiber has strength <=F/k and cannot be in current A_k;
- k>=k_min(ell)=max{k:|A_k|-ell>=k}, since deleting the ell strongest fibers minimizes every eligible-prefix count and thus minimizes closure size.

Set R_ell=max R(k) over this restricted set; at ell=0 use only k=n0. Coupling each conditional waiting time to Exp(R_ell) proves that P(tau<=t) is bounded above by the CDF of the sum of independent Exp(R_ell), ell=0,...,r*-1. This comparator is substantially stronger than the broad Rmax Poisson bound and is the primary baseline below. Positive uniformization computes its CDF with a geometric bound on the remaining Poisson mass.

## Arithmetic and reproducibility

`certify.py`, `trigger_baseline.py`, `midpoint.py` are independently written. Strengths are the exact binary64 values returned by NumPy RandomState(0). Loads and temperatures use exact rationals: .175=7/40,.15=3/20,.1=1/10. All boundary products/comparisons use Python Fraction exactly. All probabilities, exponential evaluations, and DP arithmetic use mpmath interval arithmetic at 70 decimal digits. Factorials use exact integers. Uniformization truncates after r*+599 terms and adds a geometric remainder upper bound. The certificate trusts the installed interval arithmetic implementation, Python integer arithmetic and the model assumptions; it is not proof-assistant verification.

The JSON intervals enclose the computed *bound quantity*. Their lower endpoints are NOT lower bounds on the physical failure probability. Their upper endpoints are the certified model upper bounds. `physical_failure_upper_interval` in the JSON refers to this distinction. Uniformization result intervals enclose the finite sum plus remainder upper bound, not necessarily the exact comparator CDF at their lower endpoints.

`check.py` tested 162 small cases (n2..10, all m, three random strength fixtures) against exhaustive Bernoulli subset enumeration: largest absolute ordinary-floating discrepancy 8.89e-16. The analytic event equivalence and recurrence, not that numerical test, justify the method.

## Selected results (rounded upward for readable upper bounds)

Fixture f0=.175,T=.15:

| n | t | Boundary physical upper | Restricted pure-birth upper |
|---|---|---|---|
|100|.01|1.05304e-30|1.83787e-29|
|100|.1|3.53226e-14|5.25474e-13|
|400|.01|3.95438e-119|1.70487e-110|
|400|.1|6.67234e-54|8.49280e-46|
|400|.3|7.68305e-26|6.18936e-19|

Midpoint f0=.15,T=.1:

| n | t | Boundary physical upper | Restricted pure-birth upper |
|---|---|---|---|
|100|.01|1.13263e-50|9.24482e-47|
|100|.1|5.98029e-28|4.08868e-24|
|400|.01|1.19944e-200|1.86059e-175|
|400|.1|1.14594e-110|4.48222e-86|
|400|.3|1.72375e-69|2.99655e-46|

One boundary computation took approximately .04–.06 seconds at n100 and .58–.66 seconds at n400 for .175/.15 on this machine. Positive restricted pure-birth uniformization took approximately .10 and .42–.49 seconds respectively. These are single Python implementation timings excluding setup and m search, not optimized algorithmic performance claims. The boundary method is therefore comparable in measured cost and much sharper in these fixtures. Its absolute tail arithmetic remains reliable well below ordinary-Monte-Carlo reach; this does not establish tightness against the actual tail.

## Prior art and limits

Minimum cut sets, coherent-system monotonicity, Poisson-binomial recursion, Bernoulli boundary crossing and uniformization are classical tools. This work adapts those tools to the exact thermal-avalanche clock representation. No general novelty claim is supported by this limited literature check.

Relevant primary research includes Hong, “On computing the distribution function for the Poisson binomial distribution,” https://www.sciencedirect.com/science/article/pii/S0167947312003568; “Exactly computing the tail of the Poisson-Binomial Distribution,” https://arxiv.org/abs/2004.07429 (emphasizes severe relative errors in tiny tails and uses exponential shifting); and “Evaluation of reliability bounds by set covering models,” https://www.sciencedirect.com/science/article/abs/pii/S0167715202003462 (minimal cut/path set reliability bounds). These establish relevant classical context, not priority of this model-specific construction. A comprehensive model-specific literature review remains open.

Only two published parameter pairs and seed0 strengths were tested, not the complete published grid, deposited trajectories, measured material data or a rigorous benchmark of every alternative estimator. More informative bounds could combine multiple levels of the positive lifetime functional, but that has not been implemented here.

## Hypothetical coupled-strength uncertainty

No physical measurements or calibrated uncertainty region were supplied. As an illustrative robustness calculation only, suppose each input strength lies in [max(0,s_i-eta),s_i+eta], with eta=.005 or .01 in the model's dimensionless strength units.

Couple different strengths using the same independent X_i~Exp(1). Their internal clocks are E_i=X_i exp(s_i/T). Increasing any strengths simultaneously increases the corresponding clocks and enlarges every eligibility set A_k={i:s_i>F/k}. Therefore the maximal feasible K(u) increases pointwise at every u. Since psi(k) is increasing, tau=integral psi(K(u))du increases pathwise. Failure probability is consequently largest at the all-lower-strength corner of the box. This handles the coupled change in thermal rates and avalanche thresholds; changing just one would be incorrect.

At n400 and t=.1, exact-rational lower-corner inputs and the same 70-digit interval DP yield:

| f0,T | eta=0 | eta=.005 | eta=.01 |
|---|---|---|---|
|.15,.1|1.14594e-110|3.54381e-107|1.58996e-103|
|.175,.15|6.67234e-54|2.75931e-51|1.07696e-48|

Every entry is rounded upward and is a uniform upper bound throughout its hypothetical strength box. The selected m is recomputed at each lower corner using the same smallest-maximal-deficit rule. Files `strength_uncertainty.py` and `strength_uncertainty_results.json` contain the implementation and full intervals. The tail scale persists under these illustrative coordinatewise perturbations, while numerical values change by several orders of magnitude. This robustness check does not establish an empirical confidence region or physical predictive accuracy.
