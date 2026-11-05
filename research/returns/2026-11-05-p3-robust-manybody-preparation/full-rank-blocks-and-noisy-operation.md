# Preserving full rank and delivering through noisy apparatus

[Return guide](README.md) · [Complete supplied response](P3_NOISY_PREPARATION_CONSEQUENCE_20261105_RETURN.txt) · [Costs and boundaries](boundaries-factories-and-costs.md)

The established fixed-temperature 1D preparation method supplies mixtures of bounded contiguous pure blocks. The new step keeps its exact positive sums while replacing rank-deficient components by uniformly mixed blocks. Precompensation itself is established machinery; the earned addition is the uniform many-body margin and constructive compatible operation.

## Structural construction

For the source's local positive matrices and midpoint-cut operators, `G'_j<=G_j<=exp(7m)G'_j`. Choosing `F_j=G'_j/2` and `a=exp(-7m)/2` gives a full-rank remainder `Delta_j=G_j-F_j`, bounded between `G_j/2` and `(1-a)G_j`.

The normalized remainder has eigenvalues in `[1/2,1-a]`. Its sharp spectral projectors are softened by mixing with identity, using `s=a/2`. Adjusted nonnegative coefficients preserve both exact identities `G_j=sum_t E_(j,t)` and `Delta_j=sum_t b_(j,t) E_(j,t)`, while retaining a spectral floor and `b_(j,t)<=1-a/2`.

A first-cut expansion isolates bounded superblocks. Its remaining central perturbation is made small enough for a positive parity mixture of products of `(I +/- P/2)/2`, whose one-qubit minimum eigenvalue is `1/4`. Dressing preserves the selected cuts. Every final block therefore has a uniform condition-number bound. The supplied response contains the equations and proof outline; the [original detailed proof](package/research/comparators/robust_1d_block_opening.md) and [operation note](package/research/operation_and_consequences.md) are included.

The first-stage sampling law remains unchanged because each modified positive decomposition sums to the same original operator. Finite superblock labels retain neighbor-factorized weights and forward-backward sampling. Local relative Loewner approximation gives `O(N zeta)` normalized error with `zeta=O(epsilon/N)`, without an extensive dressing-condition-number multiplier. The report retains the inherited polynomial sampler's numerical-input convention; it does not claim near-linear performance or a new tight bit-complexity theorem for all inherited operations.

## Completed physical composition

The inherited apparatus commissions endpoint templates with noisy contrasts and protected simulation; protected computation samples the mixed blocks, inverts the acquired channel on each actual sampled block, synthesizes the resulting positive inputs, and exports through the real boundary at a prescribed time. Fresh ensemble labels and fine interface histories are erased or their correlated extension enters the declared output specification. Keeping fresh labels does not make every conditioned output Gibbs.

Inverting each sampled block avoids approximating a global inverse state. Source approximation error is not amplified by an extensive inverse norm. For actual product endpoint channels `K_i` and acquired channels `Khat_i`, forward comparison on an ordinary positive input gives

```
D(K(sigmahat),Khat(sigmahat))
    <= (1/2) sum_i ||K_i-Khat_i||_diamond.
```

The complete error budget charges source sampling, numerical work, physical execution, tree export, calibration, failure and target-description error. Each can decrease at fixed primitive noise below the supplied family threshold `p_*(beta,r)>0`, under the actual inherited stationary independent-Pauli/shared-component apparatus contract. The mathematical non-Pauli range theorem alone supplies no broader physical acquisition model.

For local target-term error `xi`, Gibbs-state error is bounded by `beta ||H-Hhat||<=beta N xi`; target precision is paid. Repeated calls, including adaptive digital targets within uniform parameter bounds, compose by their summed error budgets. Existing retained external records and references keep the inherited interface guarantee; fresh preparation labels obey the new output contract.

## Finite arithmetic and remaining control requirement

An explicitly expensive fallback computes the full digital Gibbs matrix and tensor inverse with certified finite arithmetic, then prepares it through the same physical compiler. Matrix and synthesis work are exponential in system size. Positive-semidefinite projection and renormalization allow requested-accuracy approximation instead of working at the exponentially tiny global eigenvalue floor. The source's final arithmetic audit reports that this closes finite-bit physical existence without an ideal real-arithmetic oracle. It does not improve the resource conclusion.

Full-rank bounded blocks alone do not remove growing quantum error correction: faulty partition selection, masks and couplers can create cross-block errors. Protected scheduling and routing remain in the completed operation. No new controller-free physical construction is inferred.

This is known-target preparation. It does not transport an unknown input, prepare a chosen purification or establish a noncommuting long-hold theorem.
