#!/usr/bin/env python3
"""Exact Fraction replay for the local-denominator nongeometric ray.

The fixture includes degree-two substrate-preserving catalyst channels,
including an active-B-dependent transfer whose propensity is unbounded.
The tested ray has A1=A3=0, so only A1 immigration and the reverse
deactivation channel activate the support correction.
"""
from fractions import Fraction as F
from math import prod

# Species order: A1, A3, B, C. A1 supports the active substrate B;
# C is isolated under the base support E={(A1,B)} and is fixed at 2.
ZERO = (0, 0, 0, 0)
REACTIONS = [
    (ZERO,       (1, 0, 0, 0), F(1)),
    ((1, 0, 0, 0), ZERO,       F(1)),
    (ZERO,       (0, 1, 0, 0), F(1)),
    ((0, 1, 0, 0), ZERO,       F(1)),
    ((1, 0, 0, 0), (1, 0, 1, 0), F(1)),  # A1 -> A1+B
    ((1, 0, 1, 0), (1, 0, 0, 0), F(1)),  # A1+B -> A1
    ((1, 0, 1, 0), (2, 0, 1, 0), F(1)),  # A1+B -> 2A1+B
    ((2, 0, 1, 0), (1, 0, 1, 0), F(1)),  # reverse
    ((1, 0, 0, 2), (0, 0, 0, 2), F(1)),  # A1+2C -> 2C
    ((0, 0, 0, 2), (1, 0, 0, 2), F(1)),  # reverse; C label is fixed
    ((1, 0, 2, 0), (0, 1, 2, 0), F(1)),  # degree-2 transfer
    ((0, 1, 2, 0), (1, 0, 2, 0), F(1)),
]

R = F(3, 2)
EPS = F(1)
D = 2
K = F(1)


def falling(n, k):
    if n < k:
        return 0
    return prod(range(n - k + 1, n + 1))


def propensity(x, source, rate):
    return rate * prod(falling(xi, yi) for xi, yi in zip(x, source))


def V(x):
    a1, a3, b, c = x
    A = a1 + a3
    h = int(a1 == 0)
    i0 = int(A == 0)
    return (F(1) + A + R**b * (1 + EPS * h / F((1 + b) ** D))
            + K * i0)


def LV(x):
    value = F(0)
    for source, target, rate in REACTIONS:
        intensity = propensity(x, source, rate)
        if intensity:
            y = tuple(xi + target_i - source_i
                      for xi, source_i, target_i in zip(x, source, target))
            value += intensity * (V(y) - V(x))
    return value


def total_rate(x):
    return sum(propensity(x, source, rate)
               for source, _target, rate in REACTIONS)


for n in range(0, 31):
    x = (0, 0, n, 2)
    expected = -3 * EPS * R**n / F((1 + n) ** D)
    assert LV(x) == expected, (n, LV(x), expected)

for n in (10, 20, 30):
    # High-rate support-preserving transfer is enabled at A1=1, A3=0.
    q = total_rate((1, 0, n, 2))
    assert q >= n * (n - 1)

print("PASS: exact LV ray identity for n=0..30")
print("LV(0,0,n,2) = -3*(3/2)^n/(1+n)^2")
print("PASS: total exit rate grows at least n(n-1) on the active transfer ray")
