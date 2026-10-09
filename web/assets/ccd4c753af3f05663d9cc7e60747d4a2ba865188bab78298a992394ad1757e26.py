#!/usr/bin/env python3
"""Finite exact checks for the order-5 Latin square in v1.txt.

The exhaustive search checks whether the displayed Latin square is isotopic
to the unique group of order 5, Z_5.  Isotopy means that there are symbol,
row, and column permutations alpha,beta,gamma with
alpha(L(x,y)) = beta(x)+gamma(y) (mod 5) for all x,y.
"""

from itertools import permutations


LATIN = (
    (2, 0, 3, 1, 4),
    (3, 1, 4, 0, 2),
    (4, 2, 0, 3, 1),
    (1, 3, 2, 4, 0),
    (0, 4, 1, 2, 3),
)
Q = 5
PERMUTATIONS = tuple(permutations(range(Q)))


def verify_latin_square():
    universe = set(range(Q))
    assert all(set(row) == universe for row in LATIN)
    assert all({LATIN[row][column] for row in range(Q)} == universe for column in range(Q))
    diagonal = tuple(LATIN[i][i] for i in range(Q))
    assert set(diagonal) == universe
    return diagonal


def is_z5_isotope():
    for alpha in PERMUTATIONS:
        for beta in PERMUTATIONS:
            for gamma in PERMUTATIONS:
                if all(
                    alpha[LATIN[x][y]] == (beta[x] + gamma[y]) % Q
                    for x in range(Q)
                    for y in range(Q)
                ):
                    return True, (alpha, beta, gamma)
    return False, None


if __name__ == "__main__":
    print("diagonal transversal:", verify_latin_square())
    isotope, witness = is_z5_isotope()
    print("Z5-isotopic:", isotope)
    if witness is not None:
        print("isotopy permutations:", witness)
