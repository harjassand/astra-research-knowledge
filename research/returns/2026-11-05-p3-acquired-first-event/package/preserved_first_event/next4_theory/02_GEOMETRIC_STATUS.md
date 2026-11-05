# Finite-bit geometric clock execution

The module is written at `next4_execution/finite_geometric.py`.

API: `GeometricClockCompiler(r: Fraction, epsilon: Fraction)`; reuse
`compiler.sample(rng) -> (integer, metadata)` or `compiler.draw(rng) -> integer`.
Convenience API: `sample_geometric(r, epsilon, rng)`.

The implemented cap is exactly
`M = ceil(ceil(log2(1/epsilon)) / r)`.
Only O(log M) powers are stored. Each draw consumes a fixed number of uniform
bits and has at most `bit_length(M)^2` fixed-point multiplications.

All compiler arithmetic is integer/rational. No floating logarithm, inverse-r
iteration, or huge exact rational power occurs. The rational tail bound uses
`exp(-1) < 3/8`; grid and rounding errors consume at most epsilon/4 together.

Status: COMPLETE. All exact-distribution and enormous-index checks passed.

- `02_GEOMETRIC_PROOF.md`: full self-contained error and bit-complexity proof,
  root-integration instructions, executed evidence, and finite-compiler review.
- `02_GEOMETRIC_INSERT.tex`: ready-to-insert LaTeX proof for the root report.
- `02_GEOMETRIC_CHECKS.py`: independent verifier and execution script.
- `02_GEOMETRIC_CHECKS.json`: completed evidence.

Ten small exact finite-distribution audits passed. At epsilon = 2^-20,
1000 draws at r = 2^-100 took 1.0025 seconds with 128 uniform bits and
233 fixed-point bits per draw; 1000 draws at r = 10^-25 took 0.8478 seconds.
Two stress draws at r = 2^-1000 took 2.1551 seconds. Timings and PRNG
statistics are diagnostics, not the proof of the error bound.

For direct root integration pass epsilon_clock = epsilon_root/128. This
matches the existing report's cap and places the module's total error inside
its epsilon_root/64 allocation. The class is ready for the root's exact
Fraction qhat and a batch of 1000 draws.

No material fault was found in the current huge-clock subsection. The proof
now explicitly covers base rounding, possible nonmonotonic rounded
thresholds, integer endpoint conventions, exact operation bounds, and the
ideal-fair-bits model. In the marked Poisson branch an n <= k_U cap means
the unmarked count is truncated to M <= k_U-1.

The root report and the earlier completed fixed-law files are unchanged.
