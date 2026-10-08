#!/usr/bin/env python3
"""Exact Fraction replay for the multi-catalyst support-switch ray."""
from fractions import Fraction


R = Fraction(3, 2)
EPS = Fraction(1, 10)
K = Fraction(2)


def fall(n, k):
    out = 1
    for z in range(k):
        out *= max(0, n - z)
    return out


def V(x, D):
    a, c, b = x
    h = int(a == 0)
    I0 = int(a + c == 0)
    return (Fraction(1 + a + c)
            + R**b * (1 + EPS * h / (1 + b)**D)
            + K * I0)


def generator(x, D):
    a, c, b = x
    channels = [
        ((1, 0, 0), Fraction(1)),              # 0 -> A
        ((-1, 0, 0), Fraction(a)),             # A -> 0
        ((0, 1, 0), Fraction(1)),              # 0 -> C
        ((0, -1, 0), Fraction(c)),             # C -> 0
        ((0, 0, 1), Fraction(a)),              # A -> A+B
        ((0, 0, -1), Fraction(a*b)),           # A+B -> A
        ((1, 0, 0), Fraction(a*b)),            # A+B -> 2A+B
        ((-1, 0, 0), Fraction(fall(a, 2)*b)),  # 2A+B -> A+B
        ((-1, 0, 0), Fraction(a*c)),           # A+C -> C
        ((1, 0, 0), Fraction(c)),              # C -> A+C
    ]
    total = Fraction(0)
    for (da, dc, db), rate in channels:
        if rate == 0:
            continue
        y = (a + da, c + dc, b + db)
        assert min(y) >= 0
        total += rate * (V(y, D) - V(x, D))
    return total


def formula(n, D):
    M = n**(D + 2)
    d = 1 - 1/R
    return (Fraction(1 - M)
            + (R - 1) * R**n
            - d * n * R**n
            + n
            + EPS * (1 + M) * R**n / (1 + n)**D)


for D in range(5):
    for n in range(2, 13):
        x = (1, n**(D + 2), n)
        assert generator(x, D) == formula(n, D), (D, n)
    # At this checked point the exponential has overtaken the polynomial
    # catalyst-death term for every tested D.
    n = 60
    x = (1, n**(D + 2), n)
    assert generator(x, D) > 0, (D, generator(x, D))

print("PASS: exact reaction-list generator equals (1) for D=0,...,4 and n=2,...,12")
print("PASS: LV>0 on each checked ray endpoint (n=60)")
print("Analytic limit: LV/(n^2 R^n) -> epsilon=1/10 for every fixed D>=0")
print("Scope: the local potential fails outside source-order-one grammar; no recurrence claim")
