#!/usr/bin/env python3
"""Exact small-instance check for the paired-determinant support reduction."""

from itertools import combinations, permutations
from random import Random

G = tuple[int, int]  # Gaussian integer a + b i
ZERO: G = (0, 0)
ONE: G = (1, 0)


def add(a: G, b: G) -> G:
    return (a[0] + b[0], a[1] + b[1])


def neg(a: G) -> G:
    return (-a[0], -a[1])


def mul(a: G, b: G) -> G:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def determinant(a: list[list[G]]) -> G:
    n = len(a)
    if n == 0:
        return ONE
    total = ZERO
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = ONE
        for i, j in enumerate(p):
            term = mul(term, a[i][j])
        total = add(total, term if inversions % 2 == 0 else neg(term))
    return total


def pfaffian(a: list[list[G]]) -> G:
    n = len(a)
    if n == 0:
        return ONE
    if n % 2:
        return ZERO
    total = ZERO
    for j in range(1, n):
        rest = [k for k in range(1, n) if k != j]
        minor = [[a[r][c] for c in rest] for r in rest]
        term = mul(a[0][j], pfaffian(minor))
        total = add(total, term if j % 2 == 1 else neg(term))
    return total


def skew_pair_matrix(f: list[list[G]]) -> list[list[G]]:
    n = len(f)
    a = [[ZERO for _ in range(2 * n)] for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            a[i][n + j] = f[i][j]
            a[n + j][i] = neg(f[i][j])
    return a


def nonzero_principal_pfaffian(a: list[list[G]], x: frozenset[int]) -> bool:
    if len(x) % 2:
        return False
    ids = sorted(x)
    return pfaffian([[a[i][j] for j in ids] for i in ids]) != ZERO


def at_most_one_per_site(x: frozenset[int], n: int) -> bool:
    return all(not (i in x and n + i in x) for i in range(n))


def support_from_minors(f: list[list[G]]) -> set[frozenset[int]]:
    n = len(f)
    support = set()
    for r_size in range(0, n + 1, 2):
        for r_tuple in combinations(range(n), r_size):
            r = frozenset(r_tuple)
            k = r_size // 2
            for i_tuple in combinations(r_tuple, k):
                i = frozenset(i_tuple)
                j = r - i
                minor = [[f[u][v] for v in sorted(j)] for u in sorted(i)]
                if determinant(minor) != ZERO:
                    support.add(r)
                    break
    return support


def common_feasible_support(f: list[list[G]]) -> set[frozenset[int]]:
    n = len(f)
    a = skew_pair_matrix(f)
    support = set()
    for mask in range(1 << (2 * n)):
        x = frozenset(i for i in range(2 * n) if mask & (1 << i))
        if not at_most_one_per_site(x, n) or not nonzero_principal_pfaffian(a, x):
            continue
        r = frozenset(i for i in range(n) if i in x or n + i in x)
        support.add(r)
    return support


def local_projection_check() -> None:
    # One three-vertex linear even delta-matroid gadget: s--u and s--v.
    c = [[ZERO for _ in range(3)] for _ in range(3)]
    c[0][1], c[1][0] = ONE, neg(ONE)
    c[0][2], c[2][0] = ONE, neg(ONE)
    projected = set()
    for mask in range(1 << 3):
        x = frozenset(i for i in range(3) if mask & (1 << i))
        if nonzero_principal_pfaffian(c, x):
            projected.add(frozenset(i - 1 for i in x if i in (1, 2)))
    assert projected == {frozenset(), frozenset({0}), frozenset({1})}


def main() -> None:
    local_projection_check()
    rng = Random(20261007)
    values = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1)]
    cases = 0
    for n, count in ((1, 8), (2, 16), (3, 24), (4, 24), (5, 8)):
        for case in range(count):
            if n == 2 and case < 16:
                bits = case
                f = [[((1, 0) if bits & (1 << (2 * i + j)) else ZERO)
                      for j in range(n)] for i in range(n)]
            else:
                f = [[rng.choice(values) for _ in range(n)] for _ in range(n)]
            direct = support_from_minors(f)
            intersection = common_feasible_support(f)
            assert direct == intersection, (n, case, direct, intersection)

            weights = [1 + ((3 * i + case) % 7) for i in range(n)]
            direct_opt = max(sum(weights[i] for i in r) for r in direct)
            intersection_opt = max(sum(weights[i] for i in r) for r in intersection)
            assert direct_opt == intersection_opt
            cases += 1

    # Omitting the at-most-one constraint creates a false positive even when
    # the projected site set has even size: F=I_2 has a nonsingular doubled
    # principal set, but every complementary off-diagonal 1x1 minor vanishes.
    f = [[ONE, ZERO], [ZERO, ONE]]
    a = skew_pair_matrix(f)
    doubled = frozenset({0, 2, 1, 3})
    assert nonzero_principal_pfaffian(a, doubled)
    assert frozenset({0, 1}) not in support_from_minors(f)
    assert frozenset({0, 1}) not in common_feasible_support(f)

    print(f"PASS: exact support and weighted-optimum equivalence on {cases} Gaussian-integer matrices")
    print("PASS: three-vertex gadget projects to {empty, {u}, {v}} per site")
    print("PASS: F=I_2 refutes the unconstrained principal-Pfaffian shortcut")


if __name__ == "__main__":
    main()
