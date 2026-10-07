#!/usr/bin/env python3
"""Exact small diagnostics for the N76 falling-factorial potential.

This is a fixture, not a proof of a general recurrence statement.  It checks
the potential ratios and event-clock moment for A <-> 2A, and the flat
potential increments on the high-rate exchange class A <-> B.
"""
from fractions import Fraction
from math import factorial


def ff(n: int, r: int) -> int:
    if n < r:
        return 0
    out = 1
    for j in range(r):
        out *= n - j
    return out


def fnum_1d(n: int) -> int:
    """exp(F(n)) for complexes A and 2A, with unavailable complexes omitted."""
    candidates = []
    if n >= 1:
        candidates.append(factorial(n - 1))
    if n >= 2:
        candidates.append(factorial(n - 2))
    return min(candidates) if candidates else 1


def a_to_2a(n: int, kp: Fraction, km: Fraction):
    edges = []
    if n >= 1:
        edges.append((kp * n, n + 1))
    if n >= 2:
        edges.append((km * n * (n - 1), n - 1))
    return edges


def event_moment_1d(n: int, kp: Fraction, km: Fraction) -> Fraction:
    edges = a_to_2a(n, kp, km)
    total = sum((rate for rate, _ in edges), Fraction(0))
    return sum((rate * Fraction(fnum_1d(m), fnum_1d(n))
                for rate, m in edges), Fraction(0)) / total


def fnum_exchange(a: int, b: int) -> int:
    """exp(F(a,b)) for complexes A and B, omitting disabled sources."""
    candidates = []
    if a >= 1:
        candidates.append(factorial(a - 1) * factorial(b))
    if b >= 1:
        candidates.append(factorial(a) * factorial(b - 1))
    if not candidates:
        return factorial(a) * factorial(b)
    return min(candidates)


def main() -> None:
    kp = km = Fraction(1)
    print("A <-> 2A; exact event moment and N76 bound C=2")
    for n in range(3, 9):
        print(f"n={n}: F-ratio birth={Fraction(fnum_1d(n + 1), fnum_1d(n))}, "
              f"death={Fraction(fnum_1d(n - 1), fnum_1d(n))}, "
              f"E[exp(delta F)]={event_moment_1d(n, kp, km)}")

    print("A <-> B; diagonal states have exactly zero F increment")
    for n in range(2, 9):
        old = fnum_exchange(n, n)
        left = fnum_exchange(n - 1, n + 1)
        right = fnum_exchange(n + 1, n - 1)
        print(f"n={n}: exp(delta F A->B)={Fraction(left, old)}, "
              f"exp(delta F B->A)={Fraction(right, old)}")


if __name__ == "__main__":
    main()
