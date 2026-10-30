# Independent general backward-product receiving review

30 October 2026. Frozen source SHA256 71c149ec5983a07b3f6eb2985051990c6bac6e3a6e8580dae7a2f632b70411f5, copied to `product_sources/ROOT_GENERAL_BACKWARD_PRODUCT.md`.

**Verdict: accept GBP as a local receiving theorem under the explicitly stated generator allocation, own-coordinate backward-function, collateral-safety and adverse-participation hypotheses.** No new raw acquisition or stopped/global theorem follows automatically.

Put u=T-t. For an allocated i-event, all collateral factors decrease or stay constant, while every factor is positive. Its actual after-product is therefore at most the product obtained by changing only coordinate i. Summing the allocated event intensities gives L_i F<=F(Q_i f_i)/f_i. This remains true even when the designated coordinate's own transition worsens its factor: multiplication by smaller positive collateral factors can only reduce the whole after-product. No independence assertion is involved.

The time derivative is

    partial_t f_i = a exp(-beta_i u)(partial_u v_i-beta_i v_i),
    Q_i f_i = -a exp(-beta_i u) Q_i v_i.

Thus partial_u v_i<=Q_i v_i has exactly the required sign, and their sum is at most -beta_i a p_i. Summing over i proves the stated negative product drift. History dependence in Q_i is harmless only because this inequality is imposed pointwise and uniformly against each allowed actual allocated generator.

For a batch J, f_i>=1-a and every after-factor is at most one. Telescoping product(1+z_i)-1 with z_i=a p_i/f_i gives the factor C_k=(1-a)^(-(k-1)). On summing intensities, coordinate i contributes at most C_k b_i z_i. Choosing beta_i=C_k b_i cancels each coordinate term separately, so heterogeneity creates no missing maximum or multiplicity factor. Take k>=1; if there are no adverse events, b_i=0 and any such k is harmless.

Extra safe events have nonpositive product increments for every u in the declared horizon. The bounded-test Dynkin/localization hypothesis then gives the supermartingale expectation inequality. At u=0, the exact target-indicator boundary values produce F(T)=(1-a)^(number of targets), proving GBP. For random initial states, read GBP conditionally on the initial retained history/state, or average its right-hand product; a random unaveraged right side is not an unconditional numerical bound.

The allocation condition is essential: subgenerator intensities must sum to no more than actual event intensities, without crediting a shared progress event repeatedly. Safe collateral updates are allowed, but safety must hold for ALL backward horizons, not merely the terminal target or a rank surrogate. The note correctly preserves these requirements.

Likewise, the functions depend only on u and the respective own coordinate. If a common environment is inserted into v_i, its generator/time contribution must be computed separately; GBP grants no cancellation for such additional dependence. The same caveat applies to changing the acquired test during the path. Regularity/domain conditions sufficient for the stated Dynkin limit remain assumptions, not consequences of bounded values alone.

The conclusion is the single displayed product-transform domination and its legitimate Chernoff consequences. It is not endpoint independence, negative association, coordinatewise stochastic domination by independent Bernoulli variables, or a source of participation bounds from mean occupation. Variable population, seed repair, kill rewards, physical-clock conversion and whole recurrence remain separate obligations. No counterexample was found inside this exact contract.
