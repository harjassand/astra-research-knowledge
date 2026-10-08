#!/usr/bin/env python3
"""Exact rational checks for local-denominator mixed-face rays.

This finite diagnostic checks the exact 2-catalyst/2-substrate fixture in
REPORT.txt. The all-state D=m assertion is proved by the exponent/max-face
split in the report; this script checks the closed-form generator and the
D<m-1 falsifying ray only.
"""
from fractions import Fraction as F
from math import prod


def falling(n, k):
    if n < k:
        return 0
    return prod(range(n-k+1, n+1))


def propensity(x, source, rate):
    out = F(rate)
    for n, order in zip(x, source):
        out *= falling(n, order)
    return out


def fixture_reactions(m, extension_rate=1):
    z = (0, 0, 0, 0)
    a1 = (1, 0, 0, 0)
    a2 = (0, 1, 0, 0)
    a1b1 = (1, 0, 1, 0)
    a2b2 = (0, 1, 0, 1)
    tw_a1b1 = (2, 0, 1, 0)
    tw_a2b2 = (0, 2, 0, 1)
    a1mb2 = (1, 0, 0, m)
    a2mb2 = (0, 1, 0, m)
    return [
        (z, a1, 1), (a1, z, 1), (z, a2, 1), (a2, z, 1),
        (a1, a1b1, 1), (a1b1, a1, 1),
        (a2, a2b2, 1), (a2b2, a2, 1),
        (a1b1, tw_a1b1, 1), (tw_a1b1, a1b1, 1),
        (a2b2, tw_a2b2, 1), (tw_a2b2, a2b2, 1),
        (a1mb2, a2mb2, extension_rate),
        (a2mb2, a1mb2, extension_rate),
    ]


def potential(x, D):
    a1, a2, b1, b2 = x
    eps = F(1, 10)
    h1 = int(a1 == 0)
    h2 = int(a2 == 0)
    return (
        F(a1 + a2)
        + F(6, 5) ** b1 * (1 + eps * h1 / F((1 + b1) ** D))
        + F(11, 10) ** b2 * (1 + eps * h2 / F((1 + b2) ** D))
    )


def generator(x, D, m, extension_rate=1):
    value = F(0)
    vx = potential(x, D)
    for source, target, rate in fixture_reactions(m, extension_rate):
        intensity = propensity(x, source, rate)
        if intensity:
            y = tuple(n - s + t for n, s, t in zip(x, source, target))
            value += intensity * (potential(y, D) - vx)
    return value


def closed_form(n, D, m, extension_rate=1):
    eps = F(1, 10)
    return (
        F(1 + n) + F(6, 5) ** n / 5 - F(n, 6) * F(6, 5) ** n
        + eps * (1 + extension_rate * falling(n, m))
          * (F(6, 5) ** n - F(11, 10) ** n) / F((n + 1) ** D)
    )


def main():
    # Direct symbolic structure at x_n=(1,0,n,n): the catalyst source A1
    # loses B1 support and gains B2 support in the conversion pair.
    for D, m in ((2, 4), (4, 4)):
        for n in range(max(m, 4), 31):
            direct = generator((1, 0, n, n), D, m)
            formula = closed_form(n, D, m)
            assert direct == formula, (D, m, n, direct - formula)

    # The borderline D=m-1 is not all-rate safe: increasing both rates of
    # the reversible conversion to 10 makes the leading n*2^n coefficient
    # equal to eps*c - (1-1/R1)=1-1/6>0.
    for n in range(12, 31):
        direct = generator((1, 0, n, n), 3, 4, extension_rate=10)
        formula = closed_form(n, 3, 4, extension_rate=10)
        assert direct == formula and direct > 0, (n, direct, formula)

    # D=2,m=4 is a strict counterexample: every rate is positive rational,
    # the reverse transfer is disabled at x_n, and LV is positive for n>=11
    # in this tested range. The asymptotic in REPORT proves LV->+infinity.
    for n in range(11, 31):
        assert generator((1, 0, n, n), 2, 4) > 0, n

    # At the requested boundary D=m=4, this ray is negative for n>=12 in
    # the checked window; the asymptotic limit LV/(n (6/5)^n)=-1/6 is analytic.
    for n in range(12, 31):
        assert generator((1, 0, n, n), 4, 4) < 0, n

    print("PASS: exact generator identity for D=2,m=4 and D=m=4, n=4..30")
    print("PASS: D=2,m=4 gives LV>0 on n=11..30; asymptotic is +infinity")
    print("PASS: D=m=4 ray is negative on n=12..30; asymptotic ratio is -1/6")
    print("PASS: D=3,m=4 with reversible rate 10 gives LV>0 on n=12..30")
    print("Finite evidence only; the all-state local-denominator bound is in REPORT.txt")


if __name__ == "__main__":
    main()
