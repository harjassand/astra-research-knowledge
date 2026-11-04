# One finite relative certificate for every equilibrium-safe failure deadline

This independent companion supplies the finite-confidence and finite-arithmetic closure that was **unfinished in the preceding return**. The [complete new proof](package/next2_reliability/PROOF.md) and [calibration/physical extension](package/next2_reliability/CALIBRATION_AND_PHYSICAL_SCOPE.md) now construct one finite certificate for the whole first-failure CDF. The [old sensitivity theorem](../2026-11-05-p3-deferred-calibration/reliability-cdf-sensitivity.md) and its dated unfinished notes remain unchanged as historical artifacts; they are not retroactively labelled complete.

## Precise computational theorem

The main all-terminal model has a known connected undirected graph, rational product invariant law, `0<p=pi(failure)<=1/2`, and a succinct reversible generator comprising supplied local tables and an operating refresh backbone. More generally it needs costed ordinary updates/predicate evaluation, an exit-rate upper bound and positive full-gap lower bound. Start from the **deliberately prepared** `pi(.|safe)` law, with its own physical setup costs. Product rejection has computational acceptance at least one half; physical preparation is not thereby free.

Given rational accuracy/confidence, one finite randomized preprocessing constructs intervals containing the CDF at **every positive rational deadline**, simultaneously on an event of probability at least `1-delta`, each with endpoint ratio at most `1+epsilon`. Work is polynomial in succinct input bit length, numerical inverse gap `g^-1`, inverse accuracy and log inverse confidence, including every priced static counting call. It has no inverse **global** failure-probability or mean-lifetime trajectory factor. Binary-deadline queries use finite polynomial bit work in certificate/query size, with no new stochastic path or counting call.

Static all-terminal unreliability estimation and contracted/deleted-prefix conditional sampling are imported published FPRAS machinery, **not a free arbitrary-predicate oracle or newly implemented generic Karger algorithm**. Other predicates require the same explicit static access at their actual cost. Genuine Poisson uniformization of the continuous generator preserves deadline laws. A distinct theorem treats actual positive-semidefinite reversible fixed-tick endpoint kernels; the two clocks are not interchanged through a mean-matching surrogate.

## Three finite time regimes and a complete representation

Tiny deadlines use a relative linear approximation from stationary boundary flux, so no infinite grid accumulates at zero. Intermediate deadlines use a bounded boundary-Palm forced-crossing observable, or bounded safe-start simulation when failure is common enough. Past a finite gap-scale horizon, a short reverse no-return experiment estimates the isolated slow mode; a proved **relative** spectral remainder covers every later deadline.

With uniformized time u, slow killed rate lambda and fast spectral mass r_fast, the supplied refinement gives `lambda>=g[p+(1-p)r_fast]` and relative failure-function remainder at most `2/(g u)` around `1-exp(-lambda u)`. It concerns failure probability, not relative precision of a tiny late survival tail.

All operations are finite: conditional finite Poisson tables use integer weights, omitted tails become mean bias, static/sampler errors and rounding are allocated, and rejection/random-bit/path caps contribute to confidence. Outward rational Taylor/repeated-squaring queries cover extremely small exponential arguments and huge deadlines. [Implemented query primitives](package/next2_reliability/finite_arithmetic.py) do not imply the entire generic preprocessing was run.

## Changing invariant law and actual physical uncertainty

The continuous companion extends common-law sensitivity. For killed conductances L0,L1 and diagonal invariant masses M0,M1 satisfying log bands alpha and Delta,

```text
exp(-alpha)L0 <= L1 <= exp(alpha)L0,
exp(-Delta)M0 <= M1 <= exp(Delta)M0
 => exp[-(alpha+2Delta)]F0(t) <= F1(t)
    <= exp(alpha+2Delta)F0(t).
```

It compares the corresponding equilibrium-safe initial laws and includes mass change plus safe normalization. Under the accepted P2 product-energy, refresh and unknown-support bands, the acquired continuous CDF log-radius is `3Delta+b+log(1+rho)`. Auxiliary conductances are explicitly reversible under fitted weights; true reverse rates are not reused under incompatible masses. The old common-invariant discrete/continuous sensitivity results keep their original assumptions; this changing-law conclusion is not silently exported to arbitrary fixed starts or endpoint kernels without its premises.

Local rare rate/weight estimation still pays actual local exposure; a direct energy meter helps only if its access/error are supplied. Unknown-support bands retain positive upper intervals for observed-zero channels, declared reach, model completeness and the native operational backbone. A computational saving in global rarity does not discover hidden common causes or make local calibration free.

Conditional implementation-error transfer is for the stated equilibrium-safe regime. In continuous time, an arbitrary small initialization mass already in failure dominates sufficiently early probabilities. Physical all-positive-time relative accuracy therefore needs exact or multiplicatively controlled safe initialization, or a minimum deadline. Fixed ticks and uncertain tick duration also require actual wall-clock treatment. The [all-working point-query extension](all-working-point-query.md) has a different scope and does not inherit these physical guarantees automatically.

## What was actually executed

The [recorded diagnostic](package/next2_reliability/results.json) and [original program](package/next2_reliability/diagnostic.py) use 24 parallel components, local failure probability `.1`, paired/single heat-bath refreshes and `pi(B)=1e-24`. They executed **2,926,345 ordinary kernel draws**, with 12,000 trials per sampled observable. A 25-state symmetry quotient gives a better conventional exact-state solver for this example, used as the reference.

Short paths supplied intervals near `1e-25`; a reverse window of length 448 yielded a killed-rate interval containing the numerical reference. At deadline `u=1e24`, the sample-derived interval `[.3630580878,.4013993353]` contains reference `.3760929816`. A 646-bit rational deadline was queried without simulating its duration. Exact rational forced-path checks through four updates, eleven outward-arithmetic cases, a finite-grid ratio check and a changing-mass floating diagnostic are recorded. High-precision eigensystem reference values are not machine-certified enclosures.

These are **not** the generic whole-curve preprocessing or a demonstrated all-deadline certificate from only three sampled middle deadlines. Generic Karger counting was not executed. The literal conservative generic allocation on this diagnostic exceeds `1.21e15` bounded trials and `6.21e19` path updates, before static/factory/calibration work; those resource counts were calculated, not run. [Complete diagnostic and resource limitations](package/next2_reliability/README.md).

Static FPRAS, regenerative transient-unreliability methods, reversible spectral approximation and explicit state solvers are strong prior comparators, credited in the supplied proofs. No historical firstness, broad practical superiority or civilisation-scale implementation is established. The new theorem/proof is completed at its stated scope; software execution and physical acquisition retain the limits above. No new Capital audit or scientific replay occurred. [Original package and provenance](SOURCES.json).
