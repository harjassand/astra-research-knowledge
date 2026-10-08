"""Exact small-grid audit of the coherent Racah band inequality.

This is a finite algebra check only. The all-spin proof is the ratio and
alternating-series argument in ../sol_classicality/COHERENT_RACAH_LIFT.txt.
"""

from fractions import Fraction
from math import factorial

from sympy import Rational
from sympy.physics.wigner import wigner_6j


def term(n: int, ell: int, r: int) -> Fraction:
    return Fraction(
        (n + 1) * factorial(n - r) * factorial(ell + r) ** 2,
        factorial(n + r + 1) * factorial(ell - r) ** 2 * factorial(r) ** 2,
    )


def coherent_mu(n: int, ell: int) -> Fraction:
    value = Fraction(1)
    for r in range(ell):
        value *= Fraction(n - r, n + r + 2)
    return value


def main() -> None:
    cases = 0
    band_cases = 0
    for n in range(1, 25):
        j = Rational(n, 2)
        for ell in range(1, n + 1):
            L = ell * (ell + 1)
            N = n * (n + 2)
            x = Fraction(L * L, N)
            terms = [term(n, ell, r) for r in range(ell + 1)]
            eta_series = sum(((-1) ** r) * t for r, t in enumerate(terms))
            eta_value = (-1) ** n * (n + 1) * wigner_6j(j, j, ell, j, j, ell)
            numerator, denominator = eta_value.as_numer_denom()
            eta_6j = Fraction(int(numerator), int(denominator))
            assert eta_series == eta_6j, (n, ell, eta_series, eta_6j)

            for r in range(ell):
                ratio = terms[r + 1] / terms[r]
                assert ratio <= x / ((r + 1) ** 2), (n, ell, r, ratio, x)

            if x <= 3:
                mu = coherent_mu(n, ell)
                gap = 1 - eta_series
                delta = 1 - mu
                assert gap >= x - x * x / 4, (n, ell, gap, x)
                assert gap >= Fraction(3, 4) * delta * delta, (
                    n,
                    ell,
                    gap,
                    delta,
                )
                if 1 <= x <= 3:
                    assert eta_series <= Fraction(1, 4), (n, ell, eta_series)
                band_cases += 1
            cases += 1

    print(f"PASS: exact Racah-series, ratio, and widened-band checks: {cases} modes")
    print(f"PASS: C=9 coherent comparison algebra conditions checked: {band_cases} band modes")
    print("FINITE-EVIDENCE only; the proof for all spins is the analytic argument in COHERENT_RACAH_LIFT.txt.")


if __name__ == "__main__":
    main()
