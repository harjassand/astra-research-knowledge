#!/usr/bin/env python3
"""Small exact checks for the c01_l10 pair-volume/DPP transfer audit."""
from fractions import Fraction
from itertools import combinations


def det_fraction(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    n = len(a)
    if n == 0:
        return Fraction(1)
    sign = 1
    ans = Fraction(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j] != 0), None)
        if pivot is None:
            return Fraction(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            sign = -sign
        p = a[j][j]
        ans *= p
        for i in range(j + 1, n):
            factor = a[i][j] / p
            for k in range(j + 1, n):
                a[i][k] -= factor * a[j][k]
            a[i][j] = 0
    return sign * ans


def gram_minor_weight(columns, subset):
    m = [[columns[j][i] for j in subset] for i in range(len(columns[0]))]
    return det_fraction(m) ** 2


def cyclic_check(n):
    # F[i,i+1 mod n]=1, V=[I,F^T], with columns ordered e_0,...,e_{n-1},
    # f_0,...,f_{n-1}; f_i is the standard basis vector e_(i+1 mod n).
    cols = []
    for i in range(n):
        cols.append(tuple(int(i == r) for r in range(n)))
    for i in range(n):
        cols.append(tuple(int((i + 1) % n == r) for r in range(n)))

    total = sum(gram_minor_weight(cols, S)
                for S in combinations(range(2 * n), n))
    q = n // 2
    paired = []
    for sites in combinations(range(n), q):
        subset = tuple(sorted(tuple(sites) + tuple(n + i for i in sites)))
        paired.append((sites, gram_minor_weight(cols, subset)))
    target = sum(weight for _, weight in paired)
    support = [sites for sites, weight in paired if weight]
    assert total == 2 ** n
    assert target == 2
    assert len(support) == 2
    assert {tuple(sorted(sites)) for sites in support} == {
        tuple(range(0, n, 2)), tuple(range(1, n, 2))
    }
    return total, target, Fraction(target, total), support


def near_identity_two_partition_check(eps):
    # F=[[1,eps],[eps,1]], V=[I,F^T]. The two global partition quotas select
    # one e-column and one f-column; the target additionally requires i=j.
    columns = [
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(1), eps),
        (eps, Fraction(1)),
    ]
    weights = {}
    for i in range(2):
        for j in range(2):
            weights[i, j] = gram_minor_weight(columns, (i, 2 + j))
    paired = weights[0, 0] + weights[1, 1]
    all_two_partition = sum(weights.values())
    assert weights == {
        (0, 0): eps ** 2, (0, 1): Fraction(1),
        (1, 0): Fraction(1), (1, 1): eps ** 2,
    }
    assert paired == 2 * eps ** 2
    assert all_two_partition == 2 + 2 * eps ** 2
    probability = paired / all_two_partition
    assert probability == eps ** 2 / (1 + eps ** 2)
    return weights, paired, all_two_partition, probability


def balanced_field_check(eps, a1, b1, a2, b2):
    # Rational positive diagonal column fields. Equal d_i=a_i*b_i preserve
    # the target's two paired-state weights; AM-GM implies cross mass >= 2d.
    assert all(x > 0 for x in (a1, b1, a2, b2))
    d1, d2 = a1 * b1, a2 * b2
    assert d1 == d2
    target = eps ** 2 * (a1 * b1 + a2 * b2)
    cross = a1 * b2 + a2 * b1
    assert cross >= 2 * d1
    probability = target / (target + cross)
    assert probability <= eps ** 2 / (1 + eps ** 2)
    return target, cross, probability


def main():
    for n in (4, 6, 8):
        total, target, p, support = cyclic_check(n)
        print(f"cycle n={n}: all={total}, paired={target}, p={p}, support={support}")

    eps = Fraction(1, 8)
    weights, paired, all_two_partition, p = near_identity_two_partition_check(eps)
    print(f"F_eps weights={weights}; paired={paired}; two_partition={all_two_partition}; p={p}")

    target, cross, p = balanced_field_check(
        eps, Fraction(2), Fraction(3), Fraction(1, 2), Fraction(12)
    )
    print(f"balanced fields target={target}; cross={cross}; p={p}")


if __name__ == "__main__":
    main()
