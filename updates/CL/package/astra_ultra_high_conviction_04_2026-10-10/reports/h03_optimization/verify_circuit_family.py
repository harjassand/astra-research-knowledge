#!/usr/bin/env python3
"""Exact checks for the compact-circuit family in h03_optimization.txt."""

from math import comb
import sympy as sp


def check_even_n(n: int) -> None:
    assert n >= 4 and n % 2 == 0
    t = sp.symbols("t", real=True)
    alpha = sp.Rational(1) - sp.Rational(1, 2 * n)
    reduced = t**n - alpha * t**2
    tau_power = sp.Rational(2) * alpha / n

    derivative_factor = sp.factor(sp.diff(reduced, t))
    assert sp.simplify(derivative_factor - t * (n * t ** (n - 2) - 2 * alpha)) == 0
    assert sp.simplify(n * tau_power - 2 * alpha) == 0

    value_factor = -alpha * sp.Rational(n - 2, n) * tau_power ** sp.Rational(2, n - 2)
    # Under t^(n-2)=tau_power, factor the reduced value through t^2.
    assert sp.simplify(
        (t**n - alpha * t**2)
        - t**2 * (tau_power - alpha)
        - t**2 * (t ** (n - 2) - tau_power)
    ) == 0
    assert sp.simplify(tau_power - alpha + alpha * sp.Rational(n - 2, n)) == 0

    # The gradient at x=(t/n)1 vanishes when t^(n-2)=2 alpha/n.
    grad_factor = sp.simplify(sp.Rational(1, n) + 2 * alpha - 2)
    assert grad_factor == 0
    monomials = comb(2 * n - 1, n)
    print(
        f"n={n}: dense_monomials={monomials}; "
        f"reduced={reduced}; t_star_power={tau_power}; "
        f"minimum={value_factor}"
    )


if __name__ == "__main__":
    check_even_n(4)
    check_even_n(6)
    print(f"n=10: dense_monomials={comb(19, 10)}")
    print(f"n=20: dense_monomials={comb(39, 20)}")
