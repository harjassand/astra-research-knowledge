"""Finite exact-arithmetic checks; these are not a substitute for the proof."""
from fractions import Fraction
from math import comb


def e_coefficients(n, magnetization, maximum):
    values = [Fraction(1)]
    if maximum:
        values.append(Fraction(magnetization))
    for degree in range(1, maximum):
        values.append(
            (magnetization * values[degree] - (n - degree + 1) * values[degree - 1])
            / (degree + 1)
        )
    return values


checks = 0
for n in range(1, 65):
    maximum = min(n, 8)
    values = {m: e_coefficients(n, m, maximum) for m in range(-n, n + 1, 2)}
    for degree in range(1, maximum + 1):
        raw = sum(
            Fraction(comb(n, count), 2**n) * values[2 * count - n][degree] ** 2
            for count in range(n + 1)
        )
        assert raw == comb(n, degree)
        schur_raw = Fraction(0)
        for spin_twice in range(n, -1, -2):
            count = (n - spin_twice) // 2
            multiplicity = comb(n, count) - (comb(n, count - 1) if count else 0)
            # White sector weight times normalized sector trace cancels irrep dimension.
            schur_raw += Fraction(multiplicity, 2**n) * sum(
                values[m][degree] ** 2 for m in range(-spin_twice, spin_twice + 1, 2)
            )
        assert schur_raw == raw
        checks += 2

coefficient = Fraction(108 * 131, 128) * Fraction(64, 63) ** 4
assert coefficient == Fraction(68681728, 583443)
assert coefficient < 128
checks += 2
print(f"PASS: {checks} exact normalization/constant checks, N=1..64, k<=8.")
