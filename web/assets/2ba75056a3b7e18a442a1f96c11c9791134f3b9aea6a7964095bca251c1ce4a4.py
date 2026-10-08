#!/usr/bin/env python3
"""Exact bounded checks for Sections 6--7 of regular_su_m/RESULT.txt.

Uses only Python's standard library and Fraction arithmetic.  This is a
finite diagnostic, not a proof of the uniform statements in the report.
"""

from fractions import Fraction as F
from itertools import product, permutations


def rows_from_dynkin(a):
    m = len(a) + 1
    return [sum(a[i:]) for i in range(m - 1)] + [0]


def centered(values):
    mean = F(sum(values), len(values))
    return [F(v) - mean for v in values]


def determinant(matrix):
    a = [[F(x) for x in row] for row in matrix]
    n = len(a)
    out = F(1)
    for k in range(n):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            out = -out
        x = a[k][k]
        out *= x
        for i in range(k + 1, n):
            if not a[i][k]:
                continue
            factor = a[i][k] / x
            for j in range(k + 1, n):
                a[i][j] -= factor * a[k][j]
            a[i][k] = F(0)
    return out


def partition_dimension(a):
    m = len(a) + 1
    d = F(1)
    for i in range(m):
        for j in range(i + 1, m):
            numerator = sum(a[i:j]) + (j - i)
            d *= F(numerator, j - i)
    assert d.denominator == 1
    return d.numerator


def casimir_from_dynkin(a):
    m = len(a) + 1
    ell = rows_from_dynkin(a)
    linear = sum(
        ell[i] * (ell[i] + m + 1 - 2 * (i + 1))
        for i in range(m)
    )
    return (F(linear) - F(sum(ell) ** 2, m)) / 2


def parity(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def alternant_adjoint_multiplicity(a):
    """Coefficient of chi_lambda in chi_lambda * chi_ad via alternants."""
    m = len(a) + 1
    lam = centered(rows_from_dynkin(a))
    rho = [F(m + 1 - 2 * (i + 1), 2) for i in range(m)]
    alpha = [lam[i] + rho[i] for i in range(m)]
    total = 0
    for perm in permutations(range(m)):
        delta = [alpha[perm[i]] - alpha[i] for i in range(m)]
        if all(x == 0 for x in delta):
            total += (m - 1) * parity(perm)  # zero-weight multiplicity
        elif delta.count(F(1)) == 1 and delta.count(F(-1)) == 1 and all(
            x in (F(-1), F(0), F(1)) for x in delta
        ):
            total += parity(perm)  # one root weight
    return total


def check_fundamental_pieri(a):
    """All m one-box additions are valid and distinct modulo trace."""
    m = len(a) + 1
    ell = rows_from_dynkin(a)
    su_weights = []
    for i in range(m):
        added = ell[:]
        added[i] += 1
        assert all(added[j] >= added[j + 1] for j in range(m - 1))
        su_weights.append(centered(added))
    assert len(set(tuple(w) for w in su_weights)) == m


def check_vandermonde_and_dimension(a, N):
    m = len(a) + 1
    p = m - 1
    ell = rows_from_dynkin(a)
    eta = [x / (2 * N) for x in centered(ell)]
    H = [
        [
            2 * (
                sum(eta[i] ** (s + t + 2) for i in range(m))
                - sum(eta[i] ** (s + 1) for i in range(m))
                * sum(eta[i] ** (t + 1) for i in range(m)) / m
            )
            for t in range(p)
        ]
        for s in range(p)
    ]
    det_h = determinant(H)
    vandermonde = F(2**p, m)
    for i in range(m):
        for j in range(i + 1, m):
            vandermonde *= (eta[i] - eta[j]) ** 2
    assert det_h == vandermonde and det_h > 0
    for k in range(1, p + 1):
        assert determinant([row[:k] for row in H[:k]]) > 0

    c = F(min(a), N)
    determinant_floor = F(2**p, m) * (c / 2) ** (m * (m - 1))
    assert det_h >= determinant_floor

    # Exact dimension formula and the report's (C N + 1)^M bound,
    # choosing the pointwise C=max_i a_i/N for this diagnostic.
    d = partition_dimension(a)
    C = F(max(a), N)
    M = m * (m - 1) // 2
    assert d <= (C * N + 1) ** M

    # Check the elementary trace bound with b=max_i |eta_i|, which is
    # stronger than substituting the report's coarser uniform b.
    b = max(abs(x) for x in eta)
    trace_h = sum(H[s][s] for s in range(p))
    trace_cap = 2 * m * sum(b ** (2 * s) for s in range(1, p + 1))
    assert trace_h <= trace_cap
    return det_h, d


def main():
    regular_cases = 0
    determinant_cases = 0
    dimension_cases = 0
    for m in range(2, 9):
        for a in product((1, 2, 3), repeat=m - 1):
            check_fundamental_pieri(a)
            regular_cases += 1
            for N in range(1, 6):
                check_vandermonde_and_dimension(a, N)
                determinant_cases += 1
                dimension_cases += 1

    alternant_cases = 0
    for m in range(2, 8):
        for a in product((1, 2), repeat=m - 1):
            observed = alternant_adjoint_multiplicity(a)
            assert observed == m - 1, (m, a, observed)
            alternant_cases += 1

    casimir_cases = 0
    minimum_by_m = {}
    for m in range(2, 9):
        values = []
        for a in product(range(6), repeat=m - 1):
            if not any(a):
                continue
            value = casimir_from_dynkin(a)
            assert value >= F(m * m - 1, 2 * m), (m, a, value)
            if value == F(m * m - 1, 2 * m):
                assert a in tuple(
                    tuple(1 if i == j else 0 for i in range(m - 1))
                    for j in (0, m - 2)
                ), (m, a)
            values.append(value)
            casimir_cases += 1
        minimum_by_m[m] = min(values)
        assert minimum_by_m[m] == F(m * m - 1, 2 * m)

    print("exact checks passed")
    print(f"regular label vectors m=2..8, a_i in {{1,2,3}}: {regular_cases}")
    print(f"Vandermonde/determinant/trace/dimension checks, N=1..5: {determinant_cases}")
    print(f"Weyl alternant adjoint multiplicity, m=2..7, a_i in {{1,2}}: {alternant_cases}")
    print(f"Casimir vectors m=2..8, a_i in {{0,...,5}} excluding zero: {casimir_cases}")
    print("minimum Casimir by m:", ", ".join(f"m={m}: {v}" for m, v in minimum_by_m.items()))


if __name__ == "__main__":
    main()
