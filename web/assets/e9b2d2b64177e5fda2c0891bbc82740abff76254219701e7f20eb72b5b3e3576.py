#!/usr/bin/env python3
"""Exact qutrit hard-support probe scores and work moments for leaf 07.

Uses only the Python standard library. The integer W_{r,i} gives miss 1/W.
The Fraction calculation gives the exact accepted-probe energy distribution.
"""

from fractions import Fraction
from math import comb, log, sqrt


def score(r: int, i: int) -> int:
    """W_{r,i}=<D_{r,i}|A_+^{tensor r}|D_{r,i}>."""
    if not (0 <= i <= r):
        raise ValueError("require 0 <= i <= r")
    low = max(0, 2 * i - r)
    return 2 ** (r - i) * sum(
        comb(i, t) * comb(r - i, i - t) * 3**t
        for t in range(low, i + 1)
    )


def output_weights(r: int, i: int) -> list[Fraction]:
    """Unnormalized probabilities for output Dicke weight j in chi_{r,i}."""
    return [
        Fraction(comb(i, j) ** 2, 2 ** (i - j) * comb(r, j))
        for j in range(i + 1)
    ]


def best_score_at_budget(q: int) -> tuple[int, int, int]:
    """Return (W,r,i) maximizing the explicit one-type score at r+i=q."""
    candidates = [(score(q - i, i), q - i, i) for i in range(q // 2 + 1)]
    return max(candidates)


def main() -> None:
    root = (1 + sqrt(17)) / 2
    s_h = log(root)
    p_star = (7 - sqrt(17)) / 10
    alpha = (5 - sqrt(17)) / 10
    h_star = 1 + p_star
    work_per_site = 1 + alpha
    work_per_budget = work_per_site / h_star

    print(f"R={root:.15f} s_H={s_h:.15f}")
    print(f"p_star={p_star:.15f} h_star={h_star:.15f}")
    print(f"alpha_output={alpha:.15f} mean_energy_per_site={work_per_site:.15f}")
    print(f"asymptotic_mean_energy_per_Q={work_per_budget:.15f}")
    print("Q,r,i,W,miss,miss_exponent_per_Q,filter_success,expected_filter_trials,mean_energy")

    for q in (3, 4, 5, 6, 8, 10, 20, 50, 100, 200):
        w, r, i = best_score_at_budget(q)
        weights = output_weights(r, i)
        z = sum(weights, Fraction(0, 1))
        mean_j = sum((j * v for j, v in enumerate(weights)), Fraction(0, 1)) / z
        mean_energy = Fraction(r, 1) + mean_j
        filter_success = w / root**q
        print(
            f"{q},{r},{i},{w},{1/w:.12g},{log(w)/q:.12f},"
            f"{filter_success:.12g},{1/filter_success:.12g},{float(mean_energy):.12f}"
        )

    # Exact small witness at n=2,Q=3. Its matrix is
    # [[1/4,1/4],[1/4,1/2]], with eigenvalues (3 +/- sqrt(5))/8.
    p2 = (3 - sqrt(5)) / 8
    work_high_prob = (5 - sqrt(5)) / 10
    print(f"pair_miss={p2:.15f} pair_detection_success={1-p2:.15f}")
    print(f"pair_mean_energy={2+work_high_prob:.15f} pair_energy_variance=0.2")


if __name__ == "__main__":
    main()
