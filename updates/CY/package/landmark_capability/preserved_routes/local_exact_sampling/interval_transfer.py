"""Exact one-site sampler for a positive transfer matrix on the infinite line.

The mathematical sampler assumes ``bit()`` returns independent fair bits.
The optional seeded demo is only a repeatable execution example; Python's
PRNG is not a mathematical source of iid randomness.
"""

from fractions import Fraction
from random import Random
from typing import Callable, Sequence


def _row_times_matrix(row: Sequence[int], matrix: Sequence[Sequence[int]]) -> list[int]:
    q = len(row)
    return [sum(row[i] * matrix[i][j] for i in range(q)) for j in range(q)]


def _matrix_times_column(matrix: Sequence[Sequence[int]], column: Sequence[int]) -> list[int]:
    q = len(column)
    return [sum(matrix[i][j] * column[j] for j in range(q)) for i in range(q)]


def sample_site(
    matrix: Sequence[Sequence[int]], bit: Callable[[], int]
) -> tuple[int, int]:
    """Return an exact sample of X_0 and the number of fair bits consumed.

    ``matrix`` must be square with strictly positive integer entries. It is
    the edge-weight matrix in the finite-volume law
    prod_i matrix[x_i][x_(i+1)] on [-n,n], with free boundary weights.
    """
    q = len(matrix)
    if q == 0 or any(len(row) != q for row in matrix):
        raise ValueError("matrix must be nonempty and square")
    if any(value <= 0 for row in matrix for value in row):
        raise ValueError("all transfer weights must be positive integers")
    if q == 1:
        return 0, 0

    minimum = min(value for row in matrix for value in row)
    maximum = max(value for row in matrix for value in row)
    kappa_minus_one = Fraction(maximum - minimum, minimum)
    rho = Fraction(maximum - minimum, maximum + minimum)

    left = [1] * q
    right = [1] * q
    prefix = 0

    n = 0
    while True:
        n += 1
        next_bit = bit()
        if next_bit not in (0, 1):
            raise ValueError("bit source must return 0 or 1")
        prefix = (prefix << 1) | next_bit
        left = _row_times_matrix(left, matrix)
        right = _matrix_times_column(matrix, right)

        weights = [left[a] * right[a] for a in range(q)]
        total = sum(weights)
        epsilon = min(Fraction(1), kappa_minus_one * rho ** (n - 1))

        cdf_lows: list[Fraction] = []
        cdf_highs: list[Fraction] = []
        cumulative = Fraction(0)
        for weight in weights[:-1]:
            cumulative += Fraction(weight, total)
            cdf_lows.append(max(Fraction(0), cumulative - epsilon))
            cdf_highs.append(min(Fraction(1), cumulative + epsilon))

        uniform_low = Fraction(prefix, 1 << n)
        uniform_high = Fraction(prefix + 1, 1 << n)
        for symbol in range(q):
            lower_is_certain = symbol == 0 or uniform_low >= cdf_highs[symbol - 1]
            upper_is_certain = symbol == q - 1 or uniform_high <= cdf_lows[symbol]
            if lower_is_certain and upper_is_certain:
                return symbol, n

def demo(seed: int = 20261010, draws: int = 12) -> list[tuple[int, int]]:
    """Run a repeatable example for T=[[5,2],[2,3]]."""
    rng = Random(seed)
    matrix = [[5, 2], [2, 3]]
    return [sample_site(matrix, lambda: rng.getrandbits(1)) for _ in range(draws)]


if __name__ == "__main__":
    for result in demo():
        print(result)
