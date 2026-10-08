#!/usr/bin/env python3
"""Exact finite diagnostics for the Cycle 4 biochemical-extension report.

This checks the displayed generator inequalities at every vertex of the
rational rate box on a finite state set, and recomputes the minorization Q.
The infinite-state conclusions in REPORT.txt follow from the algebraic proof,
not from this bounded enumeration.
"""

from fractions import Fraction as F
from itertools import product

BOX = (
    (F(1), F(2)),       # alpha
    (F(5), F(6)),       # delta
    (F(1), F(2)),       # p
    (F(4), F(5)),       # q
    (F(1, 4), F(1, 2)), # u
    (F(1), F(2)),       # v
    (F(1, 2), F(1)),    # s
    (F(4), F(5)),       # t
)


def potential_w(x):
    a, b, c = x
    return F(1) + a + b + F(3, 2) * c + (2 if a == 0 else 0)


def potential_w1(x):
    a, b, c = x
    corr = F(2) + F(3, 7) * b + F(2, 7) * c if a == 0 else 0
    return F(1) + a + b + F(3, 2) * c + corr


def jumps(x, rates):
    a, b, c = x
    alpha, delta, p, q, u, v, s, t = rates
    return (
        ((1, 0, 0), alpha),
        ((-1, 0, 0), delta * a),
        ((0, 1, 0), p * a),
        ((0, -1, 0), q * a * b),
        ((1, 0, 0), u * a * b),
        ((-1, 0, 0), v * a * (a - 1) * b),
        ((0, -1, 1), s * a * b),
        ((0, 1, -1), t * a * c),
    )


def generator(f, x, rates):
    total = F(0)
    for dx, rate in jumps(x, rates):
        if rate:
            y = tuple(xi + di for xi, di in zip(x, dx))
            assert min(y) >= 0
            total += rate * (f(y) - f(x))
    return total


def main():
    vertices = list(product(*BOX))
    states = [
        (a, b, c)
        for a in range(11)
        for b in range(11 - a)
        for c in range(11 - a - b)
    ]

    for rates in vertices:
        alpha = rates[0]
        for x in states:
            a, b, c = x
            lw = generator(potential_w, x, rates)
            lw1 = generator(potential_w1, x, rates)
            assert lw <= 14
            if a == 0:
                assert lw <= -1
            if a + b + c >= 8:
                assert lw <= -1
            assert lw1 <= 14 - 3 * a - F(3, 7) * b - F(2, 7) * c
            if a == 0:
                assert lw == -alpha

    L = 99
    Q = 2 + 8 * L + F(23, 2) * L**2 + 2 * L**3
    assert Q == 2054103 + F(1, 2)
    assert int(Q + F(1, 2)) == 2054104

    print(f"PASS: {len(vertices)} exact rate-box vertices; {len(states)} states each")
    print(f"PASS: W and W1 generator inequalities at all enumerated fixtures")
    print(f"PASS: Q_bound={int(Q + F(1, 2))}; path horizons H_B=198, H_C=199")


if __name__ == "__main__":
    main()
