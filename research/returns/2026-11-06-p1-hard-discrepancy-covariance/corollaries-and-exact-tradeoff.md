# Deductions and an exact optimal covariance–discrepancy tradeoff

[Result guide](README.md) · [Construction and costs](construction-prior-art-and-costs.md) · [Complete response](P1_HARD_DISCREPANCY_COVARIANCE_20261106_RETURN.txt)

## Second moments under the same hard-bounded law

The covariance guarantee controls every positive-semidefinite quadratic loss and any fixed collection of later linear measurements. Averaging independent draws divides covariance by the number of draws. It does not establish Gaussian/Bernstein tails, negative dependence or convex-order domination.

Exact affine constraints `H(Z-x)=0` sharpen the bound by replacing `D_x` with its constrained projection

```
D_x-D_x H^T(H D_x H^T)^dagger H D_x.
```

This is the standard query-projection deduction from the joint law, not an additional new projection principle.

Matroid base-polytope edges have Hamming length two. The proposed corollary has exact means, hard discrepancy at most `2048` and covariance at most `512 D_x`, using independence-oracle greedy optimization without a representation or strong-base-orderability premise. Constants are conservative; applicable existing weighted matroid algorithms retain their stronger practical guarantees.

The credited adjacent-cell reduction for integral submodular base polyhedra places each integer-valued coordinate in its neighboring integer pair, preserves exact means and tight original constraints, and bounds covariance by `512 diag(p_j(1-p_j))`, `p=x-floor(x)`, with hard bound `2048`. The reduction's own oracle/value/bit-length costs are not waived.

## K4: compare against a globally optimal alternative

For the six edges of K4, set every mean to `1/2`. Each triangle measurement counts half its selected edges; column norm is `1/sqrt(2)`. There are four star and twelve Hamilton-path spanning trees.

| Exact-mean law | Maximum triangle discrepancy | Best relative covariance factor |
|---|---:|---:|
| Uniform over all 16 trees | `3/4` | `3/2` |
| Probability `1/10` per star, `1/20` per path | `3/4` | `6/5`, globally optimal |
| Uniform over 12 paths | `1/4` | `2`, optimal with the tighter hard bound |

The middle law has covariance `(3/10)I-(1/20)J`. Every exact-mean tree covariance has trace `3/2` and annihilates the all-ones vector, so its largest eigenvalue is at least `3/10`; the displayed law attains it. Below hard radius `3/4`, stars are forbidden and symmetry yields the optimal path law.

Thus the exact frontier is infeasible below `1/4`, factor two on `[1/4,3/4)`, and factor `6/5` at radii at least `3/4`. The same marginals can therefore conceal materially different joint hard/variance tradeoffs.

The source verifies these finite laws and certificates with exact rational arithmetic. This illustration is not execution of the enormous general algorithm, proof of a separate priority claim or evidence of practical large-instance advantage. Full standalone report/code/results remain pending transfer; the complete visible source is available now.
