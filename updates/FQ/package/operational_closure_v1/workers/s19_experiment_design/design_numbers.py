"""Reproduce the finite-sample design numbers in REPORT.md; no experimental data."""

from math import ceil, log, sqrt

alpha_q = 0.025
sensitivity = 0.99
for bad_fraction in (0.05, 0.01, 0.001):
    assays = ceil(log(alpha_q) / log(1 - sensitivity * bad_fraction))
    print(f"q*={bad_fraction:g}: m={assays}")

alpha_c = 0.025
n_pairs = 64
margin_over_B = sqrt(2 * log(1 / alpha_c) / n_pairs)
print(f"n={n_pairs}: causal margin/B={margin_over_B:.6f}")
