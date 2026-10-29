# One-way failure outputs and exact residual weights

28 October 2026. Clarifies DILUTE_SOURCE_COROLLARY_v1.md without changing its frozen bytes.

## Local failure, not unavailable reverse communication

“Other outcomes output a fixed failure state” means a total local output operation, not an instruction requiring Bob to notify Alice. On Bob's sector/dimension rejection he discards or replaces **his** output with a fixed K-dimensional state. Alice retains her already produced K-dimensional register, possibly correlated with external systems. This joint output need not be a fixed product state; its infidelity is simply at most one, which is all the rejection bound uses. Alice's own dimension or residual rejection can be sent forward to Bob. All outcomes retain a common K by K output interface. Nothing requires a backwards message or a common success flag known to Alice.

## Why residual probabilities are exact

For the iid purified source, simultaneous permutation covariance survives conditioning on local Schur sector labels and the environmental irrep label: their central projectors commute with permutations. After tracing Bob, environment, and non-Specht factors, Alice's conditional operator on her irreducible Specht space V_lambda commutes with p_lambda(g) for every g. Schur's lemma therefore makes it a scalar multiple of the identity. This holds for each such subnormalized branch and for sums of selected environmental labels. Hence any rank-K code block has mass exactly K/d_lambda times the branch mass, independently of the chosen random encoder; the residual block has relative mass q=(d_lambda mod K)/d_lambda<K/d_lambda. The proof is not substituting a Haar-average weight for an actual weight.

If selected mass is zero, no packing bound is required. On positive selected mass and the accepted Bob dimension event, the common-prefix argument ensures d_lambda>=K. For complete blocks, the same covariance makes physical reference weights independent of the encoder draw, as required by the governing mean transfer. Branch probabilities sum to one; no uniform per-branch success probability is asserted.
