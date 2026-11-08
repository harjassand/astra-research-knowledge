# Time-adaptive cluster cutoff and the remaining evaluator boundary

> Release-copy note: this historical proof/review snapshot has presentation-only edits recorded in SOURCE_PROVENANCE.json. Mathematical content is unchanged. Current status and superseded steps are identified in START_HERE.md and DEPENDENCY_MAP.md at the package root.

8 November 2026. This is resource accounting for the repaired connected-activity construction, not a new all-time polynomial algorithm. The underlying activity proof and its explicit two-body scope are in FIRST_DISCOVERY_PROOF.md and SPATIAL_RESPONSE_CANDIDATE.md.

## 1. Use the decay actually earned at the supplied time

The activity proof supports any integer b>=8 satisfying its scalar contract, not just b=8. Write tau=gamma T and rho=h/gamma, with fixed physical degree Delta. For a candidate b define

    c=200(b+4),
    r=max(4096,4096(b+7),128(c+3))+ceil(12rho Delta tau).

The sufficient condition is

    tau>=4+2ceil(log_2 r)+32(c+4).

At the actual supplied time, search monotonically over the admissible b values, with exact rational arithmetic. This never changes the physical time. The search takes logarithmically many scalar tests in an elementary upper bound b<=tau/6400.

If |w(C)|<=exp(-b|V(C)|), the cluster expansion can use an exponential tail weight

    kappa=b-7.

Indeed the KP sum for modified absolute activities |w(C)|exp(kappa|V(C)|), with a(C)=|V(C)|, is at most

    |V(C')| sum_(v>=2)[64 exp(-(b-kappa-1))]^v
      = |V(C')| sum_(v>=2)(64e^-6)^v < |V(C')|.

Therefore the tail beyond total cluster size m is at most n exp(-kappa m). For L=log(10n/delta_log), choose m=ceil(L/kappa), with a minimum bookkeeping size of1. The b=8 evaluator is recovered when kappa=1.

## 2. Improved upper bound, still not polynomial uniformly in time

For each fixed rho and Delta, once tau exceeds a constant threshold, one can choose b=Theta(tau) and r=O_{rho,Delta}(tau). For example b=floor(tau/12800)-4 leaves approximately half of tau for the logarithmic and constant terms in the scalar condition; direct checking determines whether this particular choice qualifies.

The cutoff is then

    m=O(1+L/tau),

and dense activity evaluation uses physical patches of size at most

    r^2 m=O_{rho,Delta}(tau^2+tau L).

Including the previously paid enumeration, action and finite-bit factors gives an upper bound of the form

    poly(paid inputs and actions) exp[O_{rho,Delta}(tau^2+tau L)].

This improves the prior fixed-b resource estimate exp[O(tau^2 L)]. It does not turn the exponent into O(L) for unbounded tau. At tau=Theta(L), it remains exp[O(L^2)], and at tau=sqrt(L) it remains exp[O(L^(3/2))]. Those are costs of this dense evaluator, not lower bounds on other algorithms.

The familiar global entropy-mixing shortcut gives output TV at most sqrt(n log2/2) exp(-tau). Thus sufficiently late times need only uniform output. Combining that shortcut with the adaptive evaluator provides, conditional on the repaired activity theorem, a quasipolynomial upper bound throughout the qualifying time regime. It leaves early times below the noise-accumulation contract uncovered and does not supply a uniform polynomial B sampler.

The action/error dependence resembles established two-dimensional local-observable simulation bounds in McDonough et al. The comparison is a prior boundary, not an import of their local-observable theorem as a full-output sampler. The present bottleneck remains certified logarithms for rare full-output prefixes.

## 3. Exact scalar checks and limits of the evidence

check_adaptive_cost.py and adaptive_cost_results.json use exact integers/rationals. For rho=1,Delta=5 and tau=2^17,...,2^24, they find the largest qualifying integer b and verify that b+1 fails. They compare the resulting dense physical-site budget to the old b=8 budget. The test parameter L=8tau is supplied directly; no system with n exponential in L is instantiated.

At tau=131072, the checked maximum is b=16, so kappa=9 and r=8376704. These constants are far beyond practical simulation. The calculation does not show a speedup on any actual physical experiment and does not justify omitting arithmetic costs from the original evaluator.

## 4. The concrete missing operation

To obtain a time-uniform polynomial result from this route at fixed rho, it is enough, but not established, to replace dense evaluation of each signed connected activity by a certified method with total cost polynomial in n and1/epsilon uniformly for tau below the global mixing cutoff. It must pay the interface-subset cancellation, local normalization, and log-marginal accuracy for every prefix.

In the difficult scaling interval, the present bound allows patches of order tau L physical qubits. Neither the small magnitude of their activities nor their positive underlying switched probabilities makes those quantum evolutions classically easy to evaluate. Large signed cancellations are already present in the exact four-qubit checks. Restarting the last short time interval from a product input is invalid because the earlier state is correlated.

A compressed operator/trajectory representation with certified relative or logarithmic accuracy, or an exact compositional rule retaining the needed correlated input, would address the actual missing operation. No such generic representation is proved here. The bounds above make the cost target sharper without presenting this unresolved step as routine.
