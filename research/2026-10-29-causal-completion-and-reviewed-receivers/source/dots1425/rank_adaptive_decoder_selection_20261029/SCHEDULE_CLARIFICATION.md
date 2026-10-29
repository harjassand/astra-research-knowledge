# Finite schedule clarification
2026-10-29. Additive clarification to GOVERNING_v1.md; the original file is preserved.

For the implemented theorem, choose b_j to be the **least nonnegative integer** such that 2^(-b_j) <= delta_j. Rational integer comparisons implement this rule. In particular b_j=ceil(log2(1/delta))+j+1, so b_j=O(j+log(1/delta)). The soundness bounds remain true for any larger integer, but the stated polynomial expected query-cost conclusion is asserted only for this least-integer schedule (or another explicitly linearly bounded schedule), not for arbitrarily oversized b_j. The existing check_selection.py already uses the least-integer rule.

No other claim is changed. Candidate physical runtime and query cost remain separate.
