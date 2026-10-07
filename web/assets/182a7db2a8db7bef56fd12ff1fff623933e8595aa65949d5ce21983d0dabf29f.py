"""Exact finite diagnostic of the derived generating identity, not a proof."""

from fractions import Fraction
from math import factorial


def row_squared_norm(n: int, i: int) -> Fraction:
    return sum(
        (
            Fraction(
                factorial(n - j) * factorial(i),
                factorial(n - i)
                * factorial(j)
                * factorial(i - j) ** 2
                * 2 ** (i - j),
            )
            for j in range(i + 1)
        ),
        start=Fraction(0),
    )


coefficients = []
for energy in range(31):
    coefficients.append(
        sum(
            (
                2**n * row_squared_norm(n, energy - n)
                for n in range((energy + 1) // 2, energy + 1)
            ),
            start=Fraction(0),
        )
    )

assert coefficients[:4] == [1, 2, 7, 16]
for energy in range(3, len(coefficients)):
    assert coefficients[energy] == (
        2 * coefficients[energy - 1]
        + 3 * coefficients[energy - 2]
        - 4 * coefficients[energy - 3]
    )

print("Exact rational coefficient recurrence diagnostic passed for Q=0,...,30.")
