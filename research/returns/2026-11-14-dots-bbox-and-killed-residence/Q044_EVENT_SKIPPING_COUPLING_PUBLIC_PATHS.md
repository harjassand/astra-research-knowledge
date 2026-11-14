# Exact shared-heatbath event skipping for hard-source decisions

This is classical continuous-time event skipping, not a new sampling principle. It removes null proposal work, not a physical metastable barrier or a proven runtime obstacle.

For fixed ordered configurations X≤Y, let k_l≤k_u be their numbers of plus nearest neighbors at sitei. The native heatbath redraw probability is

p(k)=1/[1+exp(−(16k−32+.04))]

atθ4,φ.02. A common rate-one clock and uniformU set the lower spin toplus ifU≤p_l and upper toplus ifU≤p_u. Thus the nonnull site rates and event branches are:

| Current pair | New pair | Unconditional event rate |
|---|---|---|
| -- | ++ | p_l |
| -- | -+ | p_u−p_l |
| ++ | -+ | p_u−p_l |
| ++ | -- | 1−p_u |
| -+ | ++ | p_l |
| -+ | -- | 1−p_u |

The respective total nonnull rates are p_u,1−p_l,p_l+1−p_u. Missing probability is a null redraw and may be skipped exactly. In particular a discrepancy with k_l0,k_u4 can have extremely small resolving rate; this construction does not certify fast coalescence.

Group sites by(current pair,k_l,k_u): at most3×15=45 classes. If classj hasN_j sites and per-site nonnull r_j, total holding rateΛ=sum N_j r_j. Choose class with probabilityN_jr_j/Λ, a uniform site in that class, and one branch in the table normalized by r_j. This is exactly the shared native heatbath generator with nulls removed. Its physical holding time isExp(Λ). Each event changes only sitei; update class membership and neighbor counts fori and its four neighbors. Plus counts and discrepancy count give O(1) boundary/coalescence tests. Initial class construction costsO(n), not free; bucket storage and swap-delete index updates costO(n) memory andO(1) work per affected site.

For a capacity Bernoulli decision, holding times need not be generated: the exact jump ordering determines absorption. To estimate physical duration, sum1/Λ along the jump path as an unbiased Rao–Blackwell holding-time reward, or draw actual exponentials. The waiting times are accounted for, not set tozero. Mathematical exactness uses true logistic probabilities; a floating implementation is only approximate unless it supplies rigorous categorical/branch comparisons. Finite rational exponential enclosures and lazy bits can implement the probabilities without a fixed precision cap.

Stop with outcome difference0 immediately when configurations coalesce. Before either boundary is hit, both configurations evolve by the table. Once one chain's absorption outcome is known, do NOT keep redrawing it as an active chain. Continue the other by its original single-chain rates until its own a/B outcome is known, or use the monotonicity implications that force equal outcomes. Single-chain event skipping uses10 classes(current spin,k). Hard sourcea is the actual all-minus state; targetB is the unchanged majority set. No reservoir clock is introduced or approximated.

This enables an exact original-clock implementation, but useful wall-clock and event-count bounds for the R200 energy-edge distribution still need proof or measured pilots. The transfer W/C*<exp20 is not a bound on these event counts.
