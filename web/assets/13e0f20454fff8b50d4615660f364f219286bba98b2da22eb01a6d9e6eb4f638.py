"""Exact small checks for rejection from an unrestricted paired-minor k-DPP.

The theorem is proved in revisions/micro_rejection_obstruction.txt. This script
checks only finite determinant identities/support/marginals, not the theorem.
"""
from fractions import Fraction
from itertools import combinations
import json

EPS = Fraction(1, 4)


def det_q(M):
    M = [[Fraction(x) for x in row] for row in M]
    n = len(M)
    if n == 0:
        return Fraction(1)
    sign = 1
    result = Fraction(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if M[i][j]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != j:
            M[j], M[pivot] = M[pivot], M[j]
            sign *= -1
        p = M[j][j]
        result *= p
        for i in range(j + 1, n):
            if not M[i][j]:
                continue
            c = M[i][j] / p
            for t in range(j + 1, n):
                M[i][t] -= c * M[j][t]
            M[i][j] = 0
    return sign * result


def submatrix(A, rows, cols):
    return [[A[i][j] for j in cols] for i in rows]


def fixture(n):
    assert n % 2 == 0
    k = n // 2
    F = [[Fraction(int(j == (i + 1) % n)) + EPS * int(i == j)
          for j in range(n)] for i in range(n)]
    Isets = list(combinations(range(n), k))
    weights = {}
    row_marginal = [Fraction(0) for _ in range(n)]
    col_marginal = [Fraction(0) for _ in range(n)]
    total = Fraction(0)
    hard = Fraction(0)
    hard_support = []
    for I in Isets:
        for J in Isets:
            value = det_q(submatrix(F, I, J)) ** 2
            weights[(I, J)] = value
            total += value
            for i in I:
                row_marginal[i] += value
            for j in J:
                col_marginal[j] += value
            if set(I).isdisjoint(J):
                hard += value
                if value:
                    hard_support.append((I, J, value))
    gram = [[sum(F[r][i] * F[r][j] for r in range(n))
             for j in range(n)] for i in range(n)]
    e_k_gram = sum(det_q(submatrix(gram, J, J)) for J in Isets)
    assert total == e_k_gram
    assert all(m == total / 2 for m in row_marginal)
    assert all(m == total / 2 for m in col_marginal)
    expected = []
    for parity in (0, 1):
        I = tuple(i for i in range(n) if i % 2 == parity)
        J = tuple(i for i in range(n) if i % 2 != parity)
        expected.append((I, J, Fraction(1)))
    assert sorted(hard_support) == sorted(expected)
    assert hard == 2
    bound = Fraction(2, 1) / (Fraction(__import__('math').comb(n, k)) * (1 - EPS) ** n)
    assert Fraction(hard, total) <= bound
    return {
        "n": n,
        "k": k,
        "epsilon": "1/4",
        "matrix_nonzeros": 2 * n,
        "condition_number_upper_bound": "5/3",
        "unrestricted_partition_exact": str(total),
        "hard_disjoint_partition_exact": str(hard),
        "hard_probability_exact": str(Fraction(hard, total)),
        "hard_probability_upper_bound": str(bound),
        "row_marginals_all_equal_half": True,
        "column_marginals_all_equal_half": True,
        "hard_support_count": len(hard_support),
        "hard_supports": [[list(I), list(J), str(w)] for I, J, w in sorted(hard_support)],
        "scope": "exact finite rational diagnostics only"
    }


if __name__ == "__main__":
    print(json.dumps([fixture(n) for n in (4, 6, 8)], indent=2))
