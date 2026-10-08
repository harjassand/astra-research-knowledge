#!/usr/bin/env python3
"""Finite diagnostic for the proposed SU(3) wall-fiber eigenvalue bound.

The exact CPV block formulas and diagonal symmetrization are implemented by
the adjacent interpolating_fiber_check.ls_eigenvalues routine. This wrapper
recounts every tested block instead of hard-coding the number of blocks.
It checks only the bounded box 1<=b<=20, b<=a<=60 and p+q<=a; the
floating-point eigenvalue scan is falsification evidence, not a proof.
"""

from __future__ import annotations

import sympy as sp

from interpolating_fiber_check import ls_eigenvalues


def exact_selfdual_22_block() -> None:
    """Print the exact 3x3 CPV-index example obstructing diagonal Loewner bounds."""
    n, z = sp.symbols("n z", positive=True)
    diagonal_outer = (3 * n**2 + 6 * n + 1) / (2 * n**2)
    diagonal_middle = (2 * n**2 + 4 * n - 3) / (2 * n**2)
    edge = sp.sqrt((n - 1) * (n + 2) * (n + 3)) / (2 * n ** sp.Rational(3, 2))
    block = sp.Matrix(
        [
            [diagonal_outer, edge, 0],
            [edge, diagonal_middle, edge],
            [0, edge, diagonal_outer],
        ]
    )
    charpoly = sp.factor(block.charpoly(z).as_expr())
    expected = sp.factor(
        (2 * z * n**2 - 3 * n**2 - 6 * n - 1)
        * (
            4 * z**2 * n**4
            - 10 * z * n**4
            - 20 * z * n**3
            + 4 * z * n**2
            + 4 * n**4
            + 16 * n**3
            + 15 * n**2
            - 2 * n
            - 3
        )
        / (8 * n**6)
    )
    assert str(charpoly) == str(expected)
    x = sp.symbols("x", positive=True)
    central_potential = (
        1 + 2 * x - sp.Rational(3, 2) * x**2
        - sp.sqrt((1 - x) * (1 + 2 * x) * (1 + 3 * x))
    )
    expansion = sp.series(central_potential, x, 0, 6)
    print("exact (n,n), (2,2) charpoly:", charpoly)
    print("central CPV-row potential at j=1, x=1/n:", expansion)


def main() -> None:
    worst_ratio = float("inf")
    worst_case = None
    block_count = 0
    eigenvalue_tests = 0
    largest_dimension = 0

    for b in range(1, 21):
        for a in range(b, 61):
            eta = (a - b) / (a + b)
            for p in range(a + 1):
                for q in range(p, a - p + 1):
                    if (p + 2 * q) % 3:
                        continue
                    delta = (q - p) // 3
                    j_max = min((2 * p + q) // 3, b)
                    multiplicity = j_max - delta + 1
                    if multiplicity <= 0:
                        continue

                    eigenvalues, matrix_dimension = ls_eigenvalues(a, b, p, q)
                    if matrix_dimension != multiplicity:
                        raise AssertionError(
                            (a, b, p, q, matrix_dimension, multiplicity)
                        )
                    block_count += 1
                    largest_dimension = max(largest_dimension, matrix_dimension)
                    if len(eigenvalues) != multiplicity:
                        raise AssertionError((a, b, p, q, len(eigenvalues)))

                    spins = range(delta, delta + multiplicity)
                    for eigenvalue, j in zip(eigenvalues, spins):
                        if j == 0:
                            continue  # diagonal-block scalar slot is unconstrained
                        ratio = float(eigenvalue) / (j + eta * j * j)
                        eigenvalue_tests += 1
                        if ratio < worst_ratio:
                            worst_ratio = ratio
                            worst_case = (a, b, p, q, j, float(eigenvalue))

    print(f"truncated blocks checked: {block_count}")
    print(f"nonzero-spin eigenvalue comparisons: {eigenvalue_tests}")
    print(f"largest multiplicity tested: {largest_dimension}")
    print(f"minimum kappa/[j+eta*j^2]: {worst_ratio:.12g}")
    print(f"attained at (a,b,p,q,j,kappa): {worst_case}")
    print("No finite counterexample found; no uniform theorem inferred.")
    exact_selfdual_22_block()


if __name__ == "__main__":
    main()
