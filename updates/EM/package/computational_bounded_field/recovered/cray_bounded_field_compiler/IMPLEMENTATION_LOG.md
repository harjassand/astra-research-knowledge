# Implementation record

The mathematical fixed-rank theorem and numerical programs have different scopes.

1. `verify_compiler.py`: 240 small random envelope fixtures and five rank-one full-mass fixtures passed. Base spins are enumerated; 90-digit arithmetic is not interval-certified.
2. `verify_discrete_mixture.py`: three complete three-spin output distributions passed their ideal-law bounds. Same arithmetic and enumeration limitations.
3. `verify_integral_layers.py`: four rank-one positive-volume-sum checks passed; interval lengths replace the unimplemented general convex-volume routine.
4. An initial non-exhaustive rank-one product-base implementation using only 90-digit mpmath interval probabilities completed cold K=1 and K=2^60 tests. Changing the moderate-coupling fixtures to K=1/n caused the full demonstration to exceed first a 45-second and then a 120-second execution cap. Those interrupted runs produced no completed new results file. A terminal streaming attempt was unavailable and did no scientific work.
5. The delivered `rank_one_product_compiler.py` uses a hybrid interval routine: SciPy log-CDF/difference calculations for standardized endpoints with magnitudes below 100 and separation above 1e-6; otherwise high-precision mpmath. Outer arithmetic remains at 90 decimal digits. This version completed the eight-spin check and the two 20-spin runs. Its result file and captured log match this delivered source. It is not a certified numerical implementation: there is no uniform end-to-end error proof for the hybrid routine or a precision scheduler covering arbitrary input bit lengths.

The core logical reduction is not benchmarked by these timings. The generic convex-volume engine and correlated-base sampler/annealer are not implemented here. Finite checks, implementation success, external mathematical correctness, historical priority and practical advantage remain separate claims.
