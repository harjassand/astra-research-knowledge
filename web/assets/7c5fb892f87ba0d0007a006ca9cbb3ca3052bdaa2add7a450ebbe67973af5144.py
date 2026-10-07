"""Exact, bounded fixtures for the stable-parity prior-art audit.

This script checks finite identities and the stated cycle obstruction only; it
is not evidence for the universal stability/exchange proof or for an FPRAS.
"""
from itertools import combinations
import json


def det_int(matrix):
    if not matrix:
        return 1
    a = [list(map(int, row)) for row in matrix]
    n = len(a)
    sign = 1
    prev = 1
    for k in range(n - 1):
        pivot_row = next((i for i in range(k, n) if a[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % prev == 0
                a[i][j] = numerator // prev
            a[i][k] = 0
        prev = pivot
    return sign * a[-1][-1]


def hole_counts(F):
    n = len(F)
    out = [0] * (1 << n)
    for holes in range(1 << n):
        retained = [i for i in range(n) if not ((holes >> i) & 1)]
        if len(retained) % 2:
            continue
        k = len(retained) // 2
        for I in combinations(retained, k):
            Iset = set(I)
            J = [j for j in retained if j not in Iset]
            minor = [[F[i][j] for j in J] for i in I]
            out[holes] += det_int(minor) ** 2
    return out


def check_cycle(q):
    n = 2 * q
    F = [[0] * n for _ in range(n)]
    for i in range(n):
        F[i][(i + 1) % n] = 1
    supports = []
    for I in combinations(range(n), q):
        J = {(i + 1) % n for i in I}
        if len(set(I) & J) == 0:
            supports.append(sum(1 << i for i in I))
    expected = [sum(1 << i for i in range(n) if i % 2 == parity)
                for parity in (0, 1)]
    assert sorted(supports) == sorted(expected)
    return {"q": q, "n": n, "max_sector_support_count": len(supports),
            "supports": [format(x, f"0{n}b") for x in sorted(supports)],
            "necessary_fractional_lc_alpha": f"<=1/{q}",
            "sector_zero_aperture_threshold": f"pi/{q}"}


def check_sharp_exchange():
    n = 6
    F = [[0] * n for _ in range(n)]
    for i in (0, 2, 4):
        F[i][i + 1] = 1
    f = hole_counts(F)
    S = sum(1 << i for i in (0, 1, 2, 3))
    T = sum(1 << i for i in (4, 5))
    a = 0
    terms = []
    for j in range(n):
        if j != a and ((S ^ T) >> j) & 1:
            exchanged = 1 << a | 1 << j
            terms.append(f[S ^ exchanged] * f[T ^ exchanged])
    lhs_product = f[S] * f[T]
    assert lhs_product == 1
    assert terms == [1, 0, 0, 0, 0]
    return {"matrix": "F[0,1]=F[2,3]=F[4,5]=1; all other entries 0",
            "S": [0, 1, 2, 3], "T": [4, 5], "a": 0,
            "fS": f[S], "fT": f[T], "sqrt_product_lhs": 1,
            "exchange_products_in_j_order": terms,
            "sqrt_exchange_rhs": 1}


def main():
    result = {"cycle_obstructions": [check_cycle(q) for q in (2, 3, 4, 5)],
              "coefficient_one_sharpness": check_sharp_exchange(),
              "scope": "exact finite diagnostics only"}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
