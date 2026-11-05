# Fixed ordered-fault-tuple tests

Recorded before either statistical production run. Deterministic arithmetic/unit tests, including exact-versus-certified-CDF comparisons, are not used to select a favorable parameter or stopping rule.

## Fixed models and parameters

Use the already frozen distance-13/13-round and distance-21/21-round circuit graphs at exact physical model p=1/1000, the same selected detector basis plus L0, and the same integer-cost minimum-weight decoder. This does not claim hardware reliability.

The ordered-fault cover uses N=64, capped internal gap distance D=64, exact uncapped boundary distances, dyadic graph probabilities with denominator2^64, rational H-grid2^-56, and the verified conversion-TV expansion. No change after seeing trial counts is permitted within these tests.

## Fixed counts and questions

- d13: exactly20,000 trials, seed202611051913, individual99.9% outward confidence interval. Compare precision and complete costs with the already frozen100,000-trial path-cover operation on the same model.
- d21: exactly10,000 trials, seed202611052921, individual99.9% outward confidence interval. Retain the earlier question Pf≤10^-12 per21-round block; do not choose a different target from the result.
- Both use the certified floating-CDF selection with exact fallback. A disagreement in deterministic tests or audit is a blocker, not grounds for silently changing or discarding sampled outcomes.
- Allow at most20minutes for each fixed statistical run and2GiB resident memory. If a budget is exceeded, preserve the partial record and report the blocker. Do not turn a partial or optional-stopped count into the fixed-shot interval.

The source law and all table arithmetic must pass independent review before production begins. Freeze implementation, input, table and dependency hashes at launch. Record all proposal outcomes, decoder calls, requested random bits, CDF fast/fallback counts, full process time and peak memory. Existing producer and floating-build work must be charged separately rather than treating saved-table loading as the entire setup.

An exact smaller normalizer proves greater expected acceptance per trial on the same rounded target law. It does not prove faster execution, solve arbitrary-code witness overlap, or defeat optimized prior splitting/subset-sampling methods. The repetition-line exponential obstruction remains part of the scope.
