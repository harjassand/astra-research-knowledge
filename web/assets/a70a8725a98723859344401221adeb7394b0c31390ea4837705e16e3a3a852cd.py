"""Exact arithmetic audit of a finite-state catalytic diffusion/CTMC witness.

This is a small derivation checker, not an empirical experiment or a proof about
any real catalyst. Run with Python 3 from the repository root.
"""

from fractions import Fraction
from itertools import product
from math import comb


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def outer(a, b):
    return tuple(tuple(x * y for y in b) for x in a)


def add_matrices(a, b):
    return tuple(tuple(x + y for x, y in zip(row_a, row_b)) for row_a, row_b in zip(a, b))


def scale_matrix(c, a):
    return tuple(tuple(c * x for x in row) for row in a)


def multinomial_errors(n, rates_a, rates_b):
    total_a = sum(rates_a)
    total_b = sum(rates_b)
    err_a = Fraction(0)
    err_b = Fraction(0)
    tie_a = Fraction(0)
    tie_b = Fraction(0)

    # Four-category count vectors. Likelihood comparison is exact integer
    # arithmetic because both distributions have denominator 6 per trial.
    for c0 in range(n + 1):
        for c1 in range(n - c0 + 1):
            for c2 in range(n - c0 - c1 + 1):
                c3 = n - c0 - c1 - c2
                counts = (c0, c1, c2, c3)
                multinomial = comb(n, c0) * comb(n - c0, c1) * comb(n - c0 - c1, c2)
                wa = multinomial
                wb = multinomial
                for count, ra, rb in zip(counts, rates_a, rates_b):
                    wa *= ra**count
                    wb *= rb**count
                pa = Fraction(wa, total_a**n)
                pb = Fraction(wb, total_b**n)
                if wa > wb:
                    # Choose A; B is misclassified.
                    err_b += pb
                elif wa < wb:
                    # Choose B; A is misclassified.
                    err_a += pa
                else:
                    tie_a += pa
                    tie_b += pb
    return err_a + tie_a / 2, err_b + tie_b / 2


def main():
    # Species coordinates are (C,E,S,P); nu_k = b + k*u, k=1,...,4.
    b = (-1, 1, 4, 0)
    u = (0, 0, -1, 1)
    yields = tuple(range(1, 5))
    nu = tuple(add(b, scale(k, u)) for k in yields)
    rates_a = (1, 1, 4, 0)
    rates_b = (0, 4, 1, 1)

    moments_a = tuple(sum(r * k**j for k, r in zip(yields, rates_a)) for j in range(4))
    moments_b = tuple(sum(r * k**j for k, r in zip(yields, rates_b)) for j in range(4))
    assert moments_a == (6, 15, 41, 117)
    assert moments_b == (6, 15, 41, 123)
    assert moments_a[:3] == moments_b[:3]
    assert moments_b[3] - moments_a[3] == 6
    mean_yield = Fraction(moments_a[1], moments_a[0])
    second_yield = Fraction(moments_a[2], moments_a[0])
    third_cumulants = tuple(
        Fraction(m3, moments_a[0])
        - 3 * mean_yield * second_yield
        + 2 * mean_yield**3
        for m3 in (moments_a[3], moments_b[3])
    )
    assert mean_yield == Fraction(5, 2)
    assert second_yield - mean_yield**2 == Fraction(7, 12)
    assert third_cumulants == (Fraction(-1, 2), Fraction(1, 2))

    drift_a = tuple(sum(rates_a[k] * nu[k][i] for k in range(4)) for i in range(4))
    drift_b = tuple(sum(rates_b[k] * nu[k][i] for k in range(4)) for i in range(4))
    assert drift_a == drift_b == (-6, 6, 9, 15)

    cov_a = ((0, 0, 0, 0),) * 4
    cov_b = ((0, 0, 0, 0),) * 4
    for k in range(4):
        cov_a = add_matrices(cov_a, scale_matrix(rates_a[k], outer(nu[k], nu[k])))
        cov_b = add_matrices(cov_b, scale_matrix(rates_b[k], outer(nu[k], nu[k])))
    assert cov_a == cov_b == (
        (6, -6, -9, -15),
        (-6, 6, 9, 15),
        (-9, 9, 17, 19),
        (-15, 15, 19, 41),
    )

    # Exact optimal likelihood-ratio errors for the one-turnover yield labels.
    p_a = tuple(Fraction(r, sum(rates_a)) for r in rates_a)
    p_b = tuple(Fraction(r, sum(rates_b)) for r in rates_b)
    assert p_a == (Fraction(1, 6), Fraction(1, 6), Fraction(4, 6), Fraction(0))
    assert p_b == (Fraction(0), Fraction(4, 6), Fraction(1, 6), Fraction(1, 6))

    err4 = multinomial_errors(4, rates_a, rates_b)
    err5 = multinomial_errors(5, rates_a, rates_b)
    assert err5 == (Fraction(181, 7776), Fraction(181, 7776))
    assert sum(err5) == Fraction(181, 3888)
    assert sum(err4) == Fraction(65, 648)

    print("yield labels:", yields)
    print("moments A:", moments_a)
    print("moments B:", moments_b)
    print("conditional yield third cumulants A/B:", third_cumulants)
    print("common drift coefficient:", drift_a)
    print("common covariance coefficient:", cov_a)
    print("outcome probabilities A:", p_a)
    print("outcome probabilities B:", p_b)
    print("4-trial randomized LR errors:", err4, "sum:", sum(err4))
    print("5-trial LR errors:", err5, "sum:", sum(err5))


if __name__ == "__main__":
    main()
