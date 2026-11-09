# Exact categorical sample reuse

An exact sample-only coupling algorithm with controlled latency and near-optimal expected query scaling

9 November 2026

## Main conclusion

An actual stored categorical outcome can be updated to an exactly correct new marginal using only independent samples from the old and new distributions. The construction makes disagreement at most eta worse than a maximal coupling, uses O(d/eta) expected new samples, and has a distribution-uniform exponential query-count tail on the broader O(d/eta^2) scale.

Three complementary lower bounds explain the costs. A deterministic global call cap requires Omega(d/eta^2). Under an exponential-moment assumption, even a balanced binary instance requires a second moment of order at least eta^-3. A reduction to published tolerant-testing results requires worst-case expected calls Omega(d/[eta log d]+sqrt(d)/eta), up to the one supplied input sample. Thus the expected query order is within a logarithmic factor in alphabet size of optimal under this information contract.

The proofs have received independent analytic review. This is a mathematical research package, not an implemented sampler, a measured speedup, or a claim of historical novelty. The small-alphabet cost example below is deliberately included because the asymptotic result alone does not establish practical value.

## Information contract

- P and Q are fixed unknown distributions on an explicitly encoded, known finite alphabet [d].
- The supplied input is the actual X~P that the operation is intended to retain. It is not replaced by a conveniently generated pair.
- Each new call returns an independent exact draw from its named source, independent of X and the operation's fresh fair bits.
- The algorithm has equality tests on labels, exact integer arithmetic and fair bits. It does not receive probabilities, density ratios, a shared source seed or distribution-dependent advice.
- Conditional applications are valid only when, conditional on the declared history, these same assumptions hold. The new target cannot be chosen arbitrarily after inspecting X.
- The guarantee is Y~Q marginally. It does not say that Y is an independent Q draw conditional on X.

The old sample is supplied free in the query count. Actual source runtime and the cost of obtaining this initial sample must be included when appropriate to the application.

## Main quantitative theorem

For rational 0<eta<=1/2, set

    L = ceil(2/eta),
    K = ceil(2d(L-1)/eta),
    C = 1+2d(L-1),
    D = K+LC+2,
    B = 2D.

The locally capped construction has new source-query count N and returns Y satisfying

    Y ~ Q exactly,
    TV(P,Q) <= Pr(X != Y) <= TV(P,Q)+eta,
    E N <= C,
    Pr(N>mB) <= 2^-m,
    Pr(N>mB) <= (C/B) 2^(-(m-1)) for integer m>=1,
    E N^2 <= 2DC.

It uses at most C-1 expected fair bits and O(log d+log L+log K) auxiliary bits. Conservative expected local bit work is O(C[log d+log L+log K]), plus the source-oracle work. There is no probability-evaluation or compilation oracle.

The rational parameter is acquired by exact integer arithmetic. The work bounds depend on the numerical value 1/eta, not merely on the bit length used to encode eta. The d=1 deterministic case can simply retain X; the substantive lower bounds assume d>=2.

Each individual overlap factory is capped at K queries. The outer residual race is not capped. This distinction is essential to exactness. Forcing a global stop and adding an arbitrary fallback generally produces only an approximately Q-distributed output.

## What is new relative to the starting point

The starting Astra N1691 result already treated actual-sample reuse, characterized fixed-batch empirical coupling, and obtained sharp binary expected/hard-cap laws. This package supplies a finite-alphabet construction with an exact support-sensitive mean bill, a symmetric local-timeout repair, and categorical query and binary moment limitations. It does not improve N1691's sharper binary mean constant.

The organizing distinction is between expected acquisition cost, uniform latency and a deterministic hard cap. These are different resources. Rare expensive branches are compatible with a small mean, and the lower bounds show that demanding a mean-scale tail or a small exact hard cap is not a free upgrade.

## Reading order and dependencies

1. `proofs/PROOF.md`: the original finite-counter factory, exact joint law and exact mean identity.
2. `proofs/LOCAL_CAP_EXTENSION.md`: the preferred latency repair. It depends only on the original factory proof, not on the optional killed variant.
3. `proofs/EMPIRICAL_BATCH_CONVERSE.md` and `proofs/FIXED_ALLOCATION_COMPARISON.md`: the self-contained fixed-batch premise and moment calculation.
4. `proofs/HARD_CAP_AND_MOMENT_LOWER_BOUNDS.md`: the adaptive hard-cap reduction and binary stopped-score lower bound.
5. `proofs/TOLERANT_TESTING_LOWER_BOUND.md`: the expected-query lower bound. This imports the precisely stated published tolerant-testing theorem; its proof is not presented as a new distribution-testing result.
6. `PRIOR_APPLICATIONS_AND_COSTS.md`: strongest access-model comparisons, source versions, economics and limits.
7. `review/MATHEMATICAL_AUDIT.md`: independent mathematical findings and source bindings.
8. `PROVENANCE.json` and `MANIFEST.sha256`: source/export provenance and package integrity.

`proofs/KILLED_WALK_EXTENSION.md` is a valid optional alternative. It uses extra killing bits and is not needed for the main result. Frozen proof notes retain their original status/date language. The completed mathematical review and this summary provide the current status; no frozen theorem is silently enlarged.

The frozen notes' references to an earlier cost/response clarification and prior note are supplied here in the consolidated `PRIOR_APPLICATIONS_AND_COSTS.md`: actual conditional source costs and conditional response independence are mandatory. Those references do not add an omitted mathematical oracle or proof dependency.

The packet contains pseudocode and proofs, not production code or empirical validation. The verification helper checks only file hashes. It does not verify the mathematics.

## Costs that prevent a performance claim

At d=16 and eta=.01,

    L=200, K=636800, C=6369,
    D=1910602, B=3821204.

The expected call bound is 6,369; the conservative tail block is over 3.8 million calls. A fixed-batch competitor pays O(d/eta^2) calls with a deterministic cap and may be preferable for parallel or latency-sensitive work. The hard-cap lower bound is not a benchmark.

For equal uniform sources, a sufficient reuse-work comparison requires the cost of a changed downstream response to exceed about 6,866 times a source draw, before local processing costs. No actual workload with this verified ratio and the exact oracle contract has been acquired. Known probabilities, accessible common randomness or a consumer needing only one expectation can make stronger established methods preferable.

## Boundaries

The theorem does not cover arbitrary continuous distributions, approximate source oracles, non-independent oracle histories, arbitrary latent-state reuse, free probability access, or amortized many-output learning. The second-moment lower bound assumes an exponential moment; the expected-query lower bound does not. The expected-query lower bound is asymptotic for eta below an unspecified absolute constant, not a numerical lower bound at eta=.01. The logarithmic gap, sharp dimension dependence of moments and sharp latency constants remain open in this packet.

This is a reusable theoretical result with an explicit information and cost contract. Its practical usefulness and historical priority remain unestablished.
