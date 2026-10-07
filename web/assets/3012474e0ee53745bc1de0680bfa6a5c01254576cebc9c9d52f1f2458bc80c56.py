"""Exact arithmetic checks for the instrument-square obstruction.

The proof in INITIAL.txt is analytic. This script checks its dimension formulas
and the strict separation between the symmetric-cloner depolarizing parameter
and the necessary instrument-square bound using rational arithmetic only.
"""
from fractions import Fraction

for d in range(2, 101):
    m = d * d - 1
    r = Fraction(d - 1, m)
    assert r == Fraction(1, d + 1)

    clone = Fraction(d + 2, 2 * (d + 1))
    instrument_bound = ((1 + r) / 2) ** 2
    gap = clone - instrument_bound
    assert gap == Fraction(d * (d + 2), 4 * (d + 1) ** 2)
    assert gap > 0

    noise = Fraction(1, 2 * (d + 1))
    assert clone + d * noise == 1  # trace-preserving depolarizing marginal

assert Fraction(2, 3) == Fraction(2 + 2, 2 * (2 + 1))
assert Fraction(4, 9) == Fraction(2 + 2, 2 * (2 + 1)) ** 2
assert Fraction(1, 2) - Fraction(4, 9) == Fraction(1, 18)

# The qubit lambda=1/2 contradiction can also be checked without radicals:
# 19/3 - 2*sqrt(2) > 3 iff 10/3 > 2*sqrt(2), iff 100 > 72.
assert 100 > 72

print("exact checks passed for d=2..100")
print("qubit instrument bound = 4/9; selfcompatible lambda=1/2 gap = 1/18")
