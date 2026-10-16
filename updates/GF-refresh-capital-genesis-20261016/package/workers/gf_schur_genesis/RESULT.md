# Unequal Schur kernels: exact global screening and sparse separation

16 October 2026. Conditional mathematics from the supplied Schur endpoint optimization. Novelty, external verification, and physical capability UNKNOWN.

The strongest concrete result here is an exact **active-generator screen**. If a candidate uses labels on a retained generator set A, its complete residual factors as

```
g_(s_A,s_E)=eta_E^(s_E) g^A_(s_A),
||g_bad_full||_infinity=max(||g_bad_A||_infinity, mu_E |g^A_empty|),
mu_E=max excluded multiplier magnitude.
```

Thus a retained optimizer with l1 KKT multiplier lambda remains globally exact if and only if `mu_E |g^A_empty|<=lambda`. A violation gives an explicit improving excluded singleton direction. This tests all exponentially many excluded sector variables together; it is a product-kernel specialization of established KKT/safe-screening logic.

An exact constrained family has `p=q=10/21`, strong magnitudes `4/5,3/4`, and

```
v_(1,2,12)=(19/34,36/85,-3/170),
F=1109/1190.
```

Any number of extra unequal multipliers of magnitude at most `91/392` leave that exact optimum unchanged. The negative pair coefficient is essential. A 64-generator receipt uses 64 distinct positive magnitudes and certifies the full answer by 19 residual evaluations, without constructing the `2^64-1`-variable problem. At the threshold the certificate is exact; beyond it the candidate's exact gap becomes positive. This is a proved arbitrary-m family plus bounded algebra checks, not finite extrapolation.

A complementary **exact sparse residual oracle** works for arbitrary unequal magnitudes, and arbitrary complex sparse coefficients. For N support labels, group generator positions by their N support bits. There are `g<=min(m,2^N)` groups. Convexity of the residual modulus squared in each log group-product proves that the global bad-label maximum is attained among at most

```
2^g-1+g 2^(g-1)
```

compressed sectors. A singleton anchor is required to exclude the good sector correctly. Zero and unit boundaries follow by continuity; the implementation never divides by a multiplier.

This oracle plus a self-contained Frank--Wolfe argument constructs an epsilon certificate for every unequal product kernel after at most `40alpha/epsilon+O(1)` sparse updates, `alpha=pq`. Its worst-case cost is doubly exponential in alpha/epsilon but polynomial in m at fixed precision. This is a parameter-dependent construction, **not an FPTAS or a demonstrated practical generic speedup**. For sufficiently small-support candidates, and for the exact active-generator screen, its cost can be useful. The source's O(m), width-alpha bracket remains the preferred first stopping test.

`check_exact.py` passed 70 exact compressed-versus-full residual tests with rational real/complex coefficients, eight phase-gauge identities, the good-label exclusion test, screen boundaries, the 64-generator exact family, and two exact approximation runs at epsilon=alpha/16. Those runs stopped after 10 and 9 updates with at most three support labels. These are bounded implementation receipts, not runtime benchmarks.

The derivation is in `PROOF.md`; exact fractions are in `results.json`; source/hash/execution receipts accompany it. Acquired third-party fulltexts are confined to `acquired_excluded_from_publication`. No worktree/original files, Git state, installs, outreach, or child agents were used.
