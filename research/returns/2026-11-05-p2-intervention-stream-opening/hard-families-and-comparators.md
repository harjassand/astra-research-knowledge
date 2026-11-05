# Physical hard families, stronger comparators and the remaining question

The [campaign opening](README.md) supplies an attained upper bound, not a universal lower bound. Its [complete source capture](P2_OPPORTUNITY_OPENING_20261105_RETURN.txt) preserves the following physical examples and ways a better protocol might bypass them. No ZIP or executable-check bundle was supplied in this return.

## A harmonic system saturates the integrated local bound

For harmonic Langevin dynamics with mass M, friction gamma, temperature variance `sigma^2=M/beta`, choose `0<lambda<=gamma/2` and `k=M lambda(gamma-lambda)`. Conditional on a retained fair reference R=±1, start at Gibbs covariance with mean `R(d,-M lambda d)` and

```text
d^2=2D0/(beta M lambda gamma).
D(t)=D0 exp(-2lambda t),
J(t)=(D0 lambda/gamma)exp(-2lambda t),
integral_0^infinity J(t)dt=D0/(2 gamma).
```

This exactly saturates the accepted entropy-dissipation bound. The source reports symbolic checks of the slow eigenmode, covariance and entropy identities.

For any independent trigger with expected time at most tau, selecting `lambda=min(1/(2tau),gamma/(2D0))`, with tau>=1/gamma, gives replacement TV at least `0.2135 min(1,sqrt(D0/(gamma tau)))`. Thus the one-shot inverse-square waiting law is sharp up to constants for independent timing and state-preserving marking that retains every attempt.

This is not a lower bound against every measurement, selection or actuator protocol. As lambda shrinks, stiffness decreases and both thermal position width and displacement grow as lambda^-1/2. Excess preparation energy remains D0/beta, but spatial range is a growing resource. The family does not prove the same bound for fixed minimum stiffness and fixed range.

## Hidden slow force: inference is not intervention

A harder example has an unobserved conserved sector Z=±1 and

```text
H_Z(x,p)=p^2/(2M)+k(x-Zd)^2/2.
```

Initially, `x|Z` has the same centered law in both sectors while `p|Z` has mean ZM lambda d and variance sigma^2. Then the mean position is `Zd(1-exp(-lambda t))`, mean momentum is `ZM lambda d exp(-lambda t)`, and the same local entropy law holds with Z hidden.

Even granting the entire continuously observed local path, sector distinguishability is

```text
KL(P_+^t||P_-^t)=4D0 lambda/gamma
 +2D0 lambda(1-lambda/gamma)^2 t.
```

Finite noisy readout cannot carry more information. A small order-sqrt(lambda) momentum shift persists for order 1/lambda while its sign is learned at order-lambda information rate. This is an inference bound. A protocol might remove the unwanted dependence without learning Z, so it is not yet an intervention lower bound. Exact conservation and growing range are premises; a finite barrier needs a paid barrier and sector-change guarantee over the actual horizon.

## Existing methods can beat the easiest bound

Stationary OU momentum sampled at interval Delta has record KL from independent thermal samples equal to `-(n-1)log(1-exp(-2gamma Delta))/2`. Choosing spacing of order `gamma^-1 log(n/epsilon^2)` gives whole-record TV epsilon in order `n gamma^-1 log(n/epsilon^2)` time. Marking inherits that comparison. This is a passive-record benchmark, not a result for every adaptive campaign with additional hidden records, but it defeats a claim that quadratic cost is necessary for every apparatus.

If a conditional shifted Gaussian and its reference sign are known, calibrated rejection can reweight on |p|<=L to truncated G_sigma with envelope `M_L=exp(|m|L/sigma^2+m^2/(2sigma^2))`. In the symmetric displaced-Gaussian fixture, equal acceptance probabilities preserve the relevant hidden/reference marginal on acceptance. For small shifts this can be far cheaper than inverse-square waiting. Its success is fixture-specific; general selection can change the hidden population and must pay failed attempts.

Strong stationary times also challenge restriction to exogenous timing. Their observation and structural requirements, and whether they preserve the needed contemporary hidden marginal, matter. The source credits Miclo and earlier strong-time machinery rather than claiming such adaptive competitors absent. Any reset synthesizable with the permitted hardware must likewise be admitted and priced.

Physical measurement/control theories and information-flow thermodynamics already account for causal interventions and memory costs. The proposed contribution must be an attainable access-sensitive resource law, not the broad assertion that interventions have thermodynamic cost. A finite-memory-bath route was explored but not selected as a stronger achieved operation; established generalized-Langevin machinery remains a comparator.

## What remains open

A full resolution needs either a physically priced protocol that beats the amortized construction while preserving its hidden/reference target, or a matching lower bound surviving observation-dependent timing, calibrated rejection, feedback and available reset. Fixed apparatus resources, growing range/cooling/bandwidth, useful response time and accessible observable consequences must all appear in the comparison.

A reliable intervention stream does not by itself guarantee persistent policy learning: irreversible hidden memory can still require a recovery or causal-memory premise. The current opening constructs a campaign upper bound and a concrete hard mechanism. It leaves optimal campaign cost, general intervention lower bounds and the foundational consequence under investigation.
