# Guarded assignment update — continuation of structured sampling

This is a scoped continuation of [DA: Strong structured-constraint sampling](../../../DA/README.md), not a separate research programme. The exact 480-line source report is preserved in [RESEARCH_REPORT.md](RESEARCH_REPORT.md). The DA source package remains unchanged; [updates/DA/CONTINUATIONS.md](../../../DA/CONTINUATIONS.md) supplies an additive route to this continuation.

## Assignment target and guarded update

The reported target is a quadratically weighted permutation law

    μ(π) ∝ exp(hᵀz(π) + ½‖Bz(π)‖²),

with exact one-per-row and one-per-column constraints. The factor B may be explicitly supplied or explicitly constructed, with its evaluation and storage costs charged. A Gaussian auxiliary update uses Y | z ∼ N(Bz,I); it redraws the assignment from the linear weighted-permutation law only when Y lies in a certified convex field region D, and otherwise holds at the current state. In exact real arithmetic, the report claims the original μ is stationary. A finite run is approximate, with its total-variation error controlled through the gap.

Repeatedly redrawing Y until it enters D is biased; the report gives a four-row example with stationary total-variation error about 0.194676. The hold step is the correction that preserves μ.

## Certificate, sampler and end-to-end costs

For a positive n×n weight matrix W with max(W)/min(W) ≤ R, the internal covariance lemma claims

    Cov(Z) ≼ [2R²(1+R²)/n] I.

Set K=BᵀB, choose κ ≥ ‖K‖op and d ≥ max_e K_ee, and compute

    M ≥ max_(e,π) |h_e + (Kz(π))_e|.

The report says each cell-wise extremum can be computed by a linear assignment optimization; a cheaper sufficient bound is max_e (|h_e| + Σ_i max_j |K_(e,(i,j))|). Choose L > M and define D = {y : ‖h+Bᵀy‖∞ ≤ L}, R = exp(2L),

    δ = 2n² exp(−(L−M)²/(2d)),   θ = 2R²(1+R²)κ/n.

When δ, θ < 1, the report's Gaussian-tail and restricted-covariance argument gives gap γ ≥ (1−δ)(1−θ). This certificate requires covariance control only in D, unlike the all-field premise used in the earlier DA families.

Each accepted auxiliary field requires an explicit weighted-permutation draw. The implementation uses Huber–Law nesting rejection, not an exact permanent or conditional-marginal oracle. The report derives expected arithmetic cost per inner draw

    O(R n² log(n+2) + A_R n^((R²+3)/2)),

with explicit conservative A_R. For fixed L ≤ 1/3, R ≤ exp(2/3) and the exponent is at most 3.396834. Matrix scaling and the van der Waerden lower bound are imported ingredients. The report separately charges certificate computation, Gaussian generation, factor operations, initialization and precision; a stored generic rank-r factor costs O(rn²) space, and the simple generic bound for M costs O(rn⁴) arithmetic. The Fourier construction evaluates Bz in O(n²) and Bᵀy in O(n² log n), with O(n²) storage instead of materializing K.

Initialization is explicit as well. If no affordable weighted-assignment draw is supplied, compute a permutation π* maximizing the linear score hᵀz; the report bounds μ(π*) below by exp(−nκ/2)/n!. With ε the requested error and γ the displayed gap bound, it gives

    t = ceil([nκ/4 + ½ log(n!) + log(1/(2ε))] / [−log(1−γ)]).

For bounded initial field the implemented weighted-core initialization removes the ½ log(n!) term. Fixed bounded L is a genuine restriction of the uniform polynomial inner-draw guarantee.

## Demonstrated class, baselines, and limits

The report gives a Fourier factor family for primes n ≥ 7 with n ≡ 3 mod 4, rank 2(n−1), and mode strength κ=√n/64. Its stated bounds have δ ≤ 2n² exp(−c√n) and θ=O(n^−1/2), so the analytical certificate admits growing rank and interaction strength. This is a theorem/application construction, not a claim of advantage over every sampler.

The source reports matrix-free runs at sizes 131 and 523. It also gives a matched comparison where transposition Metropolis was faster in all four reported generic cases:

| n / rank | Guarded sampler | Transpositions |
|---|---:|---:|
| 32 / 4 | 11,535 | 196,500 |
| 64 / 4 | 2,994 | 96,312 |
| 128 / 8 | 562 | 31,287 |
| 128 / 32 | 454 | 3,211 |

The values are source-reported estimated effective samples per second, not convergence certificates or evidence of speedup. The executed numerical code is floating-point; the real-arithmetic gap is not a certificate for its exact executed distribution. The larger matrix-free runs lack a matched baseline.

Scope remains restricted to the stated assignment/permutation interface and certified inputs. Arbitrary forbidden-edge patterns, unrestricted fields or interactions, three-dimensional matching, arbitrary intersections of hard constraints, and worst-case quadratic-assignment optimization are not covered. A polynomial approximate-counting consequence is reported from charged annealing but is not implemented. Ordinary weighted-permanent approximation is established prior work and is not claimed as new. Independent proof reconstruction, formal verification, external correctness, and historical novelty remain unresolved.

The report links a full proof, evidence-and-limits file, and reproducible handoff ZIP. Those artifacts were not found locally and were not reconstructed. Exact source references and their availability status are in the intake manifest.
