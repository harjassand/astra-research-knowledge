#!/usr/bin/env python3
"""Exact rational replay of the two-round correlated-input falsifier."""

from fractions import Fraction as F
from itertools import product

BITS = (0, 1)


def mu(x, y):
    return F(3, 8) if x == y else F(1, 8)


def event(x1, x2):
    return x1 == x2


def live_table(x1, y1):
    # Conditional selected table for answers A1=X2, B1=Y2.
    raw = {}
    denom = F(0)
    for x2, y2 in product(BITS, repeat=2):
        weight = mu(x1, y1) * mu(x2, y2) * F(event(x1, x2))
        denom += weight
        pair = (x2, y2)
        raw[pair] = raw.get(pair, F(0)) + weight
    assert denom == mu(x1, y1) * F(1, 2)
    return {pair: mass / denom for pair, mass in raw.items() if mass}


def proposed_factorization(x1):
    # S10 sees X2=x1 and therefore A1=x1. S11 averages Y2 under its
    # original marginal, which is uniform.
    return {(x1, 0): F(1, 2), (x1, 1): F(1, 2)}


for x1, y1 in product(BITS, repeat=2):
    actual = live_table(x1, y1)
    predicted = proposed_factorization(x1)
    assert actual == {(x1, x1): F(3, 4),
                      (x1, 1 - x1): F(1, 4)}
    assert predicted == {(x1, 0): F(1, 2),
                         (x1, 1): F(1, 2)}
    # The Bob-answer TV distance is 1/4 for every supported (x1,y1).
    assert sum(abs(actual.get((x1, b), F(0))
                   - predicted.get((x1, b), F(0))) for b in BITS) / 2 \
        == F(1, 4)

# Selection biases the residual Bob question conditional on Alice's current
# bit: uniform before selection, 3/4 toward x1 afterwards.
def original_y2_marginal(y2):
    # Round 2 is independent of (X1,Y1), and Y is uniform under mu.
    return sum(mu(x2, y2) for x2 in BITS)


for x1 in BITS:
    assert original_y2_marginal(0) == F(1, 2)
    assert original_y2_marginal(1) == F(1, 2)
    selected_same = live_table(x1, 0).get((x1, x1), F(0))
    assert selected_same == F(3, 4)

print("pointwise success p_(x1,x2) = 1[x2=x1], overall p = 1/2")
print("for each x1,y1: actual answer table = (a=x1,b=x1):3/4, "
      "(a=x1,b=1-x1):1/4")
print("proposed S10/S11 table = (a=x1,b=0):1/2, "
      "(a=x1,b=1):1/2")
print("exact total-variation discrepancy on Bob answer = 1/4")
