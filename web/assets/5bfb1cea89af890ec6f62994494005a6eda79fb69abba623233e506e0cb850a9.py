"""Exact Fraction checks for the SU(m) symmetric-carrier mode formulas.

This is a finite diagnostic only; the derivations and claim boundaries are in
su_m_symcarrier.txt.  It checks the source factorial 6j normalization against
the proposed 4F3 channel eigenvalue, the k=1 Casimir formula, ranks, and the
candidate degree recurrence on a small exact grid.
"""
from fractions import Fraction
from math import comb, factorial, prod


def poch(a, r):
    return prod((a + s for s in range(r)), start=1)


def eta(m, n, k, ell):
    return sum(
        (
            Fraction(
                poch(-k, r)
                * poch(k + m - 1, r)
                * poch(-ell, r)
                * poch(ell + m - 1, r),
                poch(m - 1, r)
                * poch(-n, r)
                * poch(n + m, r)
                * factorial(r),
            )
            for r in range(min(k, ell) + 1)
        ),
        Fraction(0),
    )


def source_raw(m, n, k, ell):
    prefactor = Fraction(
        factorial(k) ** 2
        * factorial(ell) ** 2
        * factorial(n - k)
        * factorial(n - ell)
        * factorial(m - 1)
        * factorial(m - 2),
        factorial(n + k + m - 1) * factorial(n + ell + m - 1),
    )
    total = Fraction(0)
    for z in range(max(k, ell), min(n, k + ell) + 1):
        denominator = (
            factorial(z - k) ** 2
            * factorial(z - ell) ** 2
            * factorial(n - z)
            * factorial(k + ell - z)
            * factorial(k + ell + m - 2 - z)
        )
        total += Fraction((-1) ** z * factorial(n + m - 1 + z), denominator)
    return prefactor * total


def dimension(m, n):
    return comb(n + m - 1, m - 1)


def rank(m, k):
    return Fraction(2 * k + m - 1, m - 1) * comb(k + m - 2, m - 2) ** 2


checks = 0
recurrence_checks = 0
casimir_checks = 0
for m in range(2, 7):
    for n in range(1, 8):
        assert sum(rank(m, k) for k in range(n + 1)) == dimension(m, n) ** 2
        for k in range(n + 1):
            for ell in range(n + 1):
                # Source convention: eta = (-1)^(k+ell) d_n times raw 6j.
                assert eta(m, n, k, ell) == (
                    (-1) ** (k + ell) * dimension(m, n) * source_raw(m, n, k, ell)
                )
                checks += 1

                # The adjoint/Casimir calculation is independent of the
                # higher-mode Racah sum.
                eta1 = Fraction(1) - Fraction(
                    m * ell * (ell + m - 1),
                    n * (m - 1) * (n + m),
                )
                assert eta(m, n, 1, ell) == eta1
                casimir_checks += 1

                # Coefficient-level form of the candidate Racah degree
                # recurrence, tested exactly on the same finite grid.
                def coeff(degree, r):
                    if r < 0 or r > min(degree, n):
                        return Fraction(0)
                    return Fraction(
                        poch(-degree, r) * poch(degree + m - 1, r),
                        poch(m - 1, r)
                        * poch(-n, r)
                        * poch(n + m, r)
                        * factorial(r),
                    )

                B = (
                    Fraction(
                        (k + m - 1) ** 2 * (n - k) * (n + k + m),
                        (2 * k + m - 1) * (2 * k + m),
                    )
                    if k < n
                    else Fraction(0)
                )
                D = (
                    Fraction(
                        k**2 * (n + 1 - k) * (n + k + m - 1),
                        (2 * k + m - 2) * (2 * k + m - 1),
                    )
                    if k > 0
                    else Fraction(0)
                )
                lhs = B * (coeff(k + 1, 0) - coeff(k, 0))
                lhs += D * (coeff(k - 1, 0) - coeff(k, 0))
                # Check all polynomial coefficients, not just r=0.
                for r in range(n + 1):
                    lhs = B * (coeff(k + 1, r) - coeff(k, r))
                    lhs += D * (coeff(k - 1, r) - coeff(k, r))
                    rhs = coeff(k, r - 1) - r * (r + m - 1) * coeff(k, r)
                    assert lhs == rhs
                    recurrence_checks += 1

print(
    f"exact checks passed: source/4F3={checks}, "
    f"Casimir k=1={casimir_checks}, coefficient recurrence={recurrence_checks}"
)
