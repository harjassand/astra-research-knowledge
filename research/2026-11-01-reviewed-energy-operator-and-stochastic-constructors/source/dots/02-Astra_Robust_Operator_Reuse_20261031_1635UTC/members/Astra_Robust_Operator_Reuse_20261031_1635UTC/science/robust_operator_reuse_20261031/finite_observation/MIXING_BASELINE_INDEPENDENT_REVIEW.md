# Separate certified-forgetting comparator review

31 October 2026. Scoped mathematical and fixture-code PASS after full read:

- `MIXING_BASELINE.md`: SHA-256 `f610578cc1d8ee32c150d5e3d9c7dcfff534da5660c1edf913c2f26e4bdf122d`.
- `mixing_baseline.py`: `fd7e8eb15088068b2d349bbfae4ef5180276faa1f3705e3d95f44f23dc6b2918`.
- Frozen results: `mixing_baseline_results.json`, `9a73d4416d7c18a3740a1ecaf7c94c6fa30954adf7b05a5c7e041c76baf20366`.

The earlier imperfect-observation proof/code and its receipt are unchanged.

For stochastic C with C>=d*1*h^T, the difference of probability rows nu-h has zero total mass. Its reset term therefore vanishes, while stochastic R contracts row l1. Adding the checked drift h^T C-h^T proves the displayed affine recurrence. The independent probability-distance bound supplies the cap at 2. At d=1 the channel resets to h exactly and xi=0. No exact common invariant distribution is assumed.

Pairing with b gives ||b||_infinity D_l. Adding the already acquired stochastic-center observation transport gives ||b||_infinity(l eta_inf+D_l), and final scalar rounding is separately paid. Each length has its own checked rule; the code does not extrapolate the admitted interval to arbitrary longer words. Uniformity in every word permits the chronological/reverse observable convention used by the earlier replay API, since the entire set of words is bounded.

For fallback, initialization plus l rounded center applications contribute at most (l+1)q in infinity norm. Probability mu has l1 norm one; final output rounding adds q. Thus M*l*eta_inf+(l+2)q is a valid fallback bound. Both branches retain the same finite observations; center storage and any actual fallback compilation/products are not removed from the cost. This executable is a known-fixture comparator, not a newly hardened external verifier.

I independently reran the file in a separate temporary working directory. All 240 checks passed. The checked minorization is 9831/32768 and reference drift is 1/147456. Constant answering is admitted at every length from 16 through 30, while the shorter lengths use the paid full-center fallback. All 40 existing horizon-30 queries were answered with zero matrix-vector products and no fallback compilation. Symbol validation and reading the word still occur. Wall-clock timings are illustrative; they do not authenticate hardware or prove a universal asymptotic speedup.

This materially defeats the proposed reduced-recurrence online advantage on that particular long-word batch. It does NOT invalidate the previously proved two-sided leakage or mixed-norm certificate, nor establish that all task families can be answered by forgetting. The same hybrid is available to reduced and unreduced retained algorithms. Standard-method usability is not evidence that a proved formulation is mathematically empty, and this review makes no historical novelty judgment about the exact formulations. What remains unestablished is a general strongest-baseline computational advantage, not the soundness of the acquired certificates.
