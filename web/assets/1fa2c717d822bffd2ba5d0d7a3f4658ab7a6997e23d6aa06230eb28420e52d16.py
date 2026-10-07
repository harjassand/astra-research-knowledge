#!/usr/bin/env python3
"""Independent bounded rational checks of the c10_s01 witness fixture."""

from fractions import Fraction


def v(a: int, b: int, c: int) -> Fraction:
    return 3 * a + 5 * c + (1 + Fraction(1, a + c + 1)) * b


def generator_v(a: int, b: int, c: int) -> Fraction:
    # Root immigration/death, A-catalyzed B birth/death, and
    # C-catalyzed B birth/death at the rates in frozen c10_s01 INITIAL.
    terms = [
        (Fraction(1), v(a + 1, b, c) - v(a, b, c)),
        (Fraction(a), v(a - 1, b, c) - v(a, b, c)) if a else (Fraction(0), Fraction(0)),
        (Fraction(1), v(a, b, c + 1) - v(a, b, c)),
        (Fraction(c), v(a, b, c - 1) - v(a, b, c)) if c else (Fraction(0), Fraction(0)),
        (Fraction(a), v(a, b + 1, c) - v(a, b, c)),
        (Fraction(a * b), v(a, b - 1, c) - v(a, b, c)) if a and b else (Fraction(0), Fraction(0)),
        (Fraction(2 * c), v(a, b + 1, c) - v(a, b, c)),
        (Fraction(b * c), v(a, b - 1, c) - v(a, b, c)) if b and c else (Fraction(0), Fraction(0)),
    ]
    return sum(rate * delta for rate, delta in terms)


def main() -> None:
    states = 0
    all_catalysts_zero = 0
    for a in range(9):
        for b in range(9):
            for c in range(9):
                drift = generator_v(a, b, c)
                rhs = Fraction(8) - Fraction(1, 5) * v(a, b, c)
                assert drift <= rhs, (a, b, c, drift, rhs)
                if a + c == 0:
                    # Exact boundary formula in the report gives LV=8-b.
                    assert drift == 8 - b
                    all_catalysts_zero += 1
                states += 1
    print(
        "PASS",
        {
            "states_checked": states,
            "zero_parent_states_checked": all_catalysts_zero,
            "certificate": "V=3A+5C+(1+1/(A+C+1))B, C=8, lambda=1/5",
            "status": "finite exact diagnostic; all-state result uses the source inequalities",
        },
    )


if __name__ == "__main__":
    main()
