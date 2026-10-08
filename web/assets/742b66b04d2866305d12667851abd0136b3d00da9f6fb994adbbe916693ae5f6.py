#!/usr/bin/env python3
"""Exact finite checks for the Cycle 2 weakly reversible escape-path audit."""

from fractions import Fraction


# Reaction order:
# 0: 2A+C -> 4A+B+C
# 1: 4A+B+C -> 6A+4B+C
# 2: 6A+4B+C -> 3A+C
# 3: 3A+C -> 2A+C, rate constant 2
# 4: 3C -> 4C
# 5: 4C -> 3C
DELTAS = ((2, 1, 0), (2, 3, 0), (-3, -4, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1))


def falling(n, m):
    if n < m:
        return 0
    out = 1
    for j in range(m):
        out *= n - j
    return out


def rates(x):
    a, b, c = x
    return (
        falling(a, 2) * c,
        falling(a, 4) * b * c,
        falling(a, 6) * falling(b, 4) * c,
        2 * falling(a, 3) * c,
        falling(c, 3),
        falling(c, 4),
    )


def fire(x, reaction):
    assert rates(x)[reaction] > 0, (x, reaction, rates(x))
    return tuple(v + dv for v, dv in zip(x, DELTAS[reaction]))


def explicit_path_to(a_target, b_target, c_target):
    """Construct a path from (2,0,3) to any (a>=2,b>=0,c>=3)."""
    assert a_target >= 2 and b_target >= 0 and c_target >= 3
    x = (2, 0, 3)
    for _ in range(c_target - 3):
        x = fire(x, 4)
    for _ in range(b_target):
        x = fire(x, 0)

    if x[0] < a_target:
        loops = (a_target - x[0] + 4) // 5
        for _ in range(loops):
            for _ in range(4):
                x = fire(x, 0)
            x = fire(x, 2)
    while x[0] > a_target:
        x = fire(x, 3)
    assert x == (a_target, b_target, c_target), x
    return x


def main():
    for a in range(2, 20):
        for b in range(0, 12):
            for c in range(3, 9):
                assert explicit_path_to(a, b, c) == (a, b, c)

    for n in range(3, 60):
        base = (n, 0, 3)
        r = rates(base)
        assert r[1] == 0 and r[2] == 0 and r[5] == 0
        p_continue = Fraction(r[0], sum(r))
        assert p_continue == Fraction((n * (n - 1)), (n * (n - 1)) * (2 * n - 3) + 2)
        assert p_continue <= Fraction(1, 2 * n - 3)

        u = (n + 2, 1, 3)
        v = (n + 4, 4, 3)
        assert fire(base, 0) == u
        assert fire(u, 1) == v
        assert fire(v, 2) == (n + 1, 0, 3)
        q0, q1, q2 = sum(rates(base)), sum(rates(u)), sum(rates(v))
        assert q0 >= 6 * falling(n, 3)
        assert q1 >= 3 * falling(n + 2, 4)
        assert q2 >= 72 * falling(n + 4, 6)

    print("exact checks passed: full-rank candidate class paths, intended three-step increments, base-state escape probability bound, and physical-rate lower bounds")


if __name__ == "__main__":
    main()
