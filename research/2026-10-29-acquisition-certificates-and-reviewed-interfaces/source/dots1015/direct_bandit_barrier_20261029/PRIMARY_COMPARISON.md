# Primary comparison: first-order bandits are established machinery

Read 2026-10-29: Chen-Yu Wei and Haipeng Luo, *More Adaptive Algorithms for Adversarial Bandits*, COLT/PMLR75 (2018), https://proceedings.mlr.press/v75/wei18a.html and governing PDF https://proceedings.mlr.press/v75/wei18a/wei18a.pdf .

Their introduction explicitly uses log-barrier regularization and credits Foster et al. (2016). Theorem10 gives a nonnegative-loss small-loss regret bound of order sqrt(K L_best logT)+K logT. Thus neither log-barrier bandits nor first-order improvement over basic EXP3 is new here. Their more adaptive controller is a strong conventional comparator, not an alternative we can ignore.

The present construction only supplies an explicit rational floor-normalization implementation and composes a simpler constant-factor first-order inequality with a candidate-relative quantum swap witness, rational SO(3) coverage, actual-history causal source assumptions and existing recovery-loss transfer. Historical novelty of that composition is unestablished. No optimality, best classical bandit constant or superiority to established adaptive methods is claimed.
