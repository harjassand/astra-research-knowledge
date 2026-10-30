"""Exact order-four moving-bath expansion for H_M=Z_M/2.

All series use alpha=delta/2, so Gaussian-integer derivative coefficients
remain exact despite the factor 1/2 in the bath Hamiltonian.
"""

from fractions import Fraction
from math import factorial
from exact_word_check import (
    PROFILE, HANDLES, polynomial_mul, series_mul, gauss_add,
)


def exponential_derivatives(generator, degree):
    out = [{"III": (1, 0)}]
    for _ in range(degree):
        out.append(polynomial_mul(generator, out[-1]))
    return out


def coefficient_in_delta(derivative, degree, denominator=1):
    scale = denominator * 2**degree * factorial(degree)
    return {p: (Fraction(z[0], scale), Fraction(z[1], scale))
            for p, z in derivative.items()}


def main():
    degree = 4
    sums = [{} for _ in range(degree + 1)]
    for a in (-1, 1):
        for b in (-1, 1):
            signs = {"A": a, "B": b, "C": a*b}
            word = [{"III": (1, 0)}] + [{} for _ in range(degree)]
            for h, orientation in PROFILE:
                generator = {"IIZ": (0, -1),
                             HANDLES[h]: (0, -2*orientation*signs[h])}
                pulse = exponential_derivatives(generator, degree)
                word = series_mul(pulse, word, degree)
            # Remove exact forward free bath exp(-i 10 alpha Z_M).
            inverse_bath = exponential_derivatives({"IIZ": (0, 10)}, degree)
            word = series_mul(inverse_bath, word, degree)
            assert word[1] == {}
            assert word[2] == {"XIY": (0, 40*a), "IXX": (0, -32*b)}
            for k, term in enumerate(word):
                for p, z in term.items():
                    sums[k][p] = gauss_add(sums[k].get(p, (0, 0)), z)
            print(f"signs ({a:+d},{b:+d},{a*b:+d}): delta^2 coefficient = "
                  f"i {5*a:+d} XIY + i {-4*b:+d} IXX")
    sums = [{p: z for p, z in term.items() if z != (0, 0)} for term in sums]
    assert sums[1] == {}
    assert sums[2] == {}
    assert sums[3] == {"IIZ": (0, 1536), "ZXI": (0, -768)}
    assert sums[4] == {"III": (-31488, 0)}
    for k in (2, 3, 4):
        print(f"E[U] coefficient of delta^{k}: "
              f"{coefficient_in_delta(sums[k], k, denominator=4)}")
    print("Exact averaged-channel order-four remainder after the useful/bath cubic unitary:")
    print("  delta^4 [25(Ad_XIY-Id) + 16(Ad_IXX-Id)].")
    print("Normalized Choi trace-norm leading coefficient = 2*(25+16) = 82.")
    print("This is a lower-bound diagnostic for this loop, not an all-policy lower bound.")


if __name__ == "__main__":
    main()
