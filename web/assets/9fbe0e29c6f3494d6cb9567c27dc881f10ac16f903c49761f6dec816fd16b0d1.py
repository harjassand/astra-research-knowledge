#!/usr/bin/env python3
"""Exact effective conductance witness for two weighted cycle arrangements."""

from math import isclose


def cycle_conductance(m: int, eps: float, arrangement: str) -> float:
    """Conductance between opposite vertices of a cycle with 2m edges.

    Every vertex has degree two. The edge-weight multiset is m copies of 1
    and m copies of eps in both arrangements. Terminals split the cycle into
    two paths of m edges each.
    """
    if m < 4 or m % 2 or not 0 < eps < 1:
        raise ValueError("require even m >= 4 and 0 < eps < 1")

    if arrangement == "clustered":
        path_weights = ([1.0] * m, [eps] * m)
    elif arrangement == "balanced":
        half = m // 2
        mixed = [1.0] * half + [eps] * half
        path_weights = (mixed, mixed)
    else:
        raise ValueError("arrangement must be 'clustered' or 'balanced'")

    # Path conductances add because the two paths are in parallel.
    return sum(1.0 / sum(1.0 / g for g in path) for path in path_weights)


def main() -> None:
    m = 12
    print("epsilon,G_clustered,G_balanced,ratio,formula_ratio")
    for eps in (0.1, 0.01, 0.001):
        clustered = cycle_conductance(m, eps, "clustered")
        balanced = cycle_conductance(m, eps, "balanced")
        ratio = clustered / balanced
        formula_a = (1 + eps) / m
        formula_b = 4 * eps / (m * (1 + eps))
        formula_ratio = (1 + eps) ** 2 / (4 * eps)
        assert isclose(clustered, formula_a, rel_tol=1e-12)
        assert isclose(balanced, formula_b, rel_tol=1e-12)
        assert isclose(ratio, formula_ratio, rel_tol=1e-12)
        print(f"{eps},{clustered:.12g},{balanced:.12g},{ratio:.12g},{formula_ratio:.12g}")


if __name__ == "__main__":
    main()
