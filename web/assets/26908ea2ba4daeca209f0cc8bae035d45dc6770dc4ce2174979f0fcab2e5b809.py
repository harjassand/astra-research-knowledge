"""Small exact diagnostics for the c01_l08 parity cost audit.

Uses only Python's standard library. These checks illustrate the rational
acceptance and refresh bit bounds; they are not a mixing or FPRAS test.
"""

from fractions import Fraction
from itertools import combinations
import json
import math


def det2(a, b, c, d):
    return a * d - b * c


def submatrix_det2(matrix, rows, cols):
    a, b = (matrix[rows[0]][cols[0]], matrix[rows[0]][cols[1]])
    c, d = (matrix[rows[1]][cols[0]], matrix[rows[1]][cols[1]])
    return det2(a, b, c, d)


def dyadic_acceptance(p, bits):
    """Down-round p to a bounded-time coin using exactly `bits` fair bits."""
    p = Fraction(p)
    scale = 1 << bits
    threshold = (p.numerator * scale) // p.denominator
    return Fraction(threshold, scale)


def modulo_tv_bound(modulus, bits):
    """Exact TV distance from x mod modulus for uniform x in [0,2**bits)."""
    size = 1 << bits
    q, rem = divmod(size, modulus)
    probs = [Fraction(q + (i < rem), size) for i in range(modulus)]
    return sum(abs(p - Fraction(1, modulus)) for p in probs) / 2


def main():
    # The four-site determinant reassignment from the inherited report.
    for L in range(1, 20):
        delta = Fraction(1, 1 << L)
        F = [
            [0, delta, 1, 0],
            [delta, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0],
        ]
        good_1 = submatrix_det2(F, (0, 1), (2, 3))
        good_2 = submatrix_det2(F, (2, 3), (0, 1))
        reassigned_1 = submatrix_det2(F, (0, 2), (1, 3))
        reassigned_2 = submatrix_det2(F, (1, 3), (0, 2))
        ratio = (reassigned_1 * reassigned_2) ** 2 / (good_1 * good_2) ** 2
        assert good_1 == good_2 == 1
        assert reassigned_1 == reassigned_2 == delta
        assert ratio == Fraction(1, 1 << (4 * L))

    # Every dyadic acceptance approximation has one-sided error < 2**(-k).
    acceptance_cases = 0
    for denominator in range(1, 41):
        for numerator in range(denominator + 1):
            p = Fraction(numerator, denominator)
            for bits in range(1, 9):
                rounded = dyadic_acceptance(p, bits)
                assert 0 <= p - rounded < Fraction(1, 1 << bits)
                acceptance_cases += 1

    # A recursive matching sampler with modulo choices has fixed cost and a
    # summable explicit bias; this checks the per-choice exact TV expression.
    matching_choice_cases = []
    for q in range(1, 32, 2):
        bits = math.ceil(math.log2(q)) + 8
        tv = modulo_tv_bound(q, bits)
        assert tv <= Fraction(q, 1 << bits)
        matching_choice_cases.append({"choices": q, "bits": bits, "tv": str(tv)})

    # Example refresh precision: r=8, M=36 lines, R=2**3, eta=2**-10.
    # K is chosen so 2**(-K) 2**M r**r R**(2r) <= eta.
    r, M, log2_R, log2_inv_eta = 8, 36, 3, 10
    K = M + math.ceil(r * math.log2(r)) + 2 * r * log2_R + log2_inv_eta
    assert K == 118
    assert K >= M + r * math.log2(r) + 2 * r * log2_R + log2_inv_eta

    print(json.dumps({
        "delta_reassignment": "exact ratio 2^(-4L), L=1..19",
        "dyadic_acceptance_checks": acceptance_cases,
        "modulo_matching_choice_examples": matching_choice_cases,
        "refresh_example": {
            "dimension_r": r,
            "line_count_M": M,
            "max_coordinate_R": "2^3",
            "refresh_tv_budget": "2^-10",
            "epsilon": "2^-118",
            "epsilon_encoding_bits": 119,
        },
        "scope": "exact arithmetic diagnostics only; no mixing or sampler validation",
    }, indent=2))


if __name__ == "__main__":
    main()
