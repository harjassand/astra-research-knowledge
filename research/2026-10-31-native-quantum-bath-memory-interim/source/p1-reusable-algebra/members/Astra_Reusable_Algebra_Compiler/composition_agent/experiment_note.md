# Numerical evidence and limitations

## Exact proof versus floating point

The theorem is an exact algebraic statement. These experiments use double-precision numerical rank decisions: cyclic residual singular values below 1e-9 are discarded, algebra-basis residuals below 1e-8 are discarded, and center/rank clustering uses 1e-7. The observed small residuals do not certify exact algebra closure or guarantee arbitrary future program accuracy.

The independent exact rational prototype is `../planning_agent/check_cyclic_exact.py`. It implements raw word vectors and their Gram metric and verifies intertwining with Fraction arithmetic.

## Four-block trace experiment

Files: `hybrid_trace_four_blocks.py`, `hybrid_trace_four_blocks_results.json`.

The target comprises two full-rank noncommuting real symmetric generators on N=528 coordinates. A dense random orthogonal transform hides four simple blocks with r=(1,2,3,4) and m=(2,3,80,70). The learner receives only generator-vector actions and Gaussian probes. It constructs the compressed algebra, solves for its center, diagonalizes a generic central element, and infers r from the restricted algebra dimension and s from the compressed block size. Hidden labels are used only by the independent scoring routine.

All 120 runs (24 independent probe trials for each q) inferred algebra dimension30 and center dimension4. The table reports the exact worst relative error over the positive cone of this target algebra, evaluated numerically with ground truth. It is not a finite test set of chosen programs.

| q | Learned dimension R | Matvec calls | Median raw-probe error | Median hybrid error | Raw failures above10% | Hybrid failures above10% |
|---:|---:|---:|---:|---:|---:|---:|
|1|30|60|94.77%|70.27%|24/24|24/24|
|2|58|116|71.82%|53.38%|24/24|20/24|
|4|108|216|53.30%|4.22%|24/24|2/24|
|8|208|416|42.19%|3.07%|24/24|0/24|
|16|408|816|33.15%|2.27%|24/24|0/24|

At q=8, the largest hybrid error among24 trials was6.38%; at q=16 it was4.85%. The largest final closure residual across all runs was7.05e-11. The two small-multiplicity blocks become exactly resolved once q>=4, while two large blocks remain unresolved even at q=16. The known total dimension therefore does not trivially determine the two remaining multiplicities.

The raw estimator uses Gaussian probes (often grouped with Hutchinson-style trace estimators), not Rademacher probes. Its worst positive-cone error is computed from the empirical density projected orthogonally into the learned matrix algebra, compared to the true tracial density. For the hybrid functional, the worst error is exactly max_alpha |mhat_alpha/m_alpha-1|. These computations allow an adversarial positive program, as required by the uniform theorem.

Reported setup times in the JSON include closure, algebra-basis construction, center extraction, and trace-functional construction. They are useful for reproducibility but do not establish a wall-time advantage against optimized conventional competitors. Probe generation, target construction, and independent scoring are outside those setup timers; no end-to-end timing claim is made.

## A numerical failure that was repaired

The initial one-vector-at-a-time residual normalization can amplify numerical leakage. On the same fixed four-block target and the same eight probes, it returned the entire ambient dimension528, making1056 matvec calls. A batched frontier SVD returned the correct208-dimensional cyclic representation with416 calls. The two final residuals were approximately1.37e-15 and2.30e-12 respectively. A smaller residual alone therefore does not imply a more useful learned representation: the full ambient space is trivially invariant.

This comparison is preserved in `closure_comparison.json`. Batched frontier SVD processes every accepted basis vector exactly once under every generator, retaining the theoretical sR matrix-vector count; it merely decides which residual directions to accept jointly. It repairs this example but is not a general robustness theorem.

## Correction to the preliminary three-block experiment

The earlier `hybrid_trace_demo.py` and `hybrid_trace_results.json` used r=(1,2,3),m=(2,3,80),N=248. Once the two small blocks resolve, only one multiplicity remains unknown. The known dimension sum m_alpha r_alpha=N then determines that multiplicity exactly. The unmodified hybrid formula's remaining stochastic error in that preliminary example was avoidable. The four-block experiment above was introduced to remove this issue, while the original records remain available.

## What has and has not been established

The experiments check that inferred composition structure can support a uniformly accurate trace functional and that the saturation correction matters. They expose low-q failures and a numerical rank-discovery failure. They do not establish scientific novelty, accuracy under generic approximate algebra closure, superiority to optimized simultaneous block diagonalization, or an end-to-end break-even point on realistic workloads.
