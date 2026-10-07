"""Finite arithmetic diagnostic; the proof and scope are in AUDIT.md."""
from fractions import Fraction
from math import isqrt


def rotation_entry(numerator, denominator, bits):
    scaled_ratio = (numerator << (2 * bits)) // denominator
    return Fraction(isqrt(scaled_ratio), 1 << bits)


cases = 0
for denominator_bits in (1, 7, 50, 500, 2000):
    h = (1 << denominator_bits) + 1
    for denominator in (1, h, h * h):
        for numerator in sorted({0, 1, denominator // 2, denominator - 1, denominator}):
            if not 0 <= numerator <= denominator:
                continue
            for bits in (1, 7, 50, 500):
                a = rotation_entry(numerator, denominator, bits)
                r = Fraction(numerator, denominator)
                assert a * a <= r
                # Exact squared comparisons establish 0<=sqrt(r)-a<2^-bits.
                assert (a + Fraction(1, 1 << bits)) ** 2 > r
                cases += 1

print(f"PASS: {cases} exact rational endpoint/tiny-mass rotation checks")
