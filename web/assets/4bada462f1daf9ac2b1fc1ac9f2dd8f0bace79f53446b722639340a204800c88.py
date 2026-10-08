#!/usr/bin/env python3
"""Exact finite checks for the low-rank principal-Cartan cap ramp."""

from fractions import Fraction


def shell(q: int) -> int:
    return ((q + 2) ** 2) // 4


def volume(r: int) -> int:
    return sum(shell(q) for q in range(r + 1))


def c_one(a: int, b: int, q: int) -> Fraction:
    return sum(
        (Fraction(a + b) - p) * shell(p) for p in range(q)
    )


def c13(a: int, b: int, q: int) -> Fraction:
    return sum(
        (Fraction(a + b) - p) * shell(p)
        for p in range(q - 1)
        if p % 2 == q % 2
    )


def gt_shells(a: int, b: int) -> dict[int, int]:
    counts: dict[int, int] = {}
    for x in range(a + 1):
        for y in range(b + 1):
            for z in range(a - x + y + 1):
                q = 2 * x + y + z
                counts[q] = counts.get(q, 0) + 1
    return counts


def check_pair(a: int, b: int) -> int:
    m = min(a, b)
    counts = gt_shells(a, b)
    for q in range(m + 1):
        assert counts.get(q, 0) == shell(q)

    for q in range(1, m + 1):
        assert c_one(a, b, q) <= 5 * m * q**3
    for q in range(2, m + 2):
        assert c13(a, b, q) <= c_one(a, b, q - 1)

    r_max = (2 * m) // 3
    for r in range(1, r_max + 1):
        profile = lambda q: max(Fraction(0), Fraction(r - q, r))
        norm2 = sum(
            shell(q) * profile(q) ** 2 for q in range(r)
        )
        e1 = sum(
            c_one(a, b, q) * (profile(q - 1) - profile(q)) ** 2
            for q in range(1, r + 1)
        )
        e_long = sum(
            c13(a, b, q) * (profile(q - 2) - profile(q)) ** 2
            for q in range(2, r + 2)
        )
        assert norm2 >= Fraction(r**3, 384)
        assert e1 <= 5 * m * r**2
        assert e_long <= 20 * m * r**2
        assert e1 + e_long <= 25 * m * r**2

    d = (a + 1) * (b + 1) * (a + b + 2) // 2
    return d


def main() -> None:
    cases = [(16, 16), (16, 32), (32, 16), (32, 32), (64, 128)]
    for a, b in cases:
        d = check_pair(a, b)
        print(f"(a,b)=({a},{b}) d={d}: exact low-cap checks passed")


if __name__ == "__main__":
    main()
