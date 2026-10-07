"""Bounded exact checks for functional_digraph_dp.py (no floating point)."""
import itertools
import json
import random
from fractions import Fraction as Q
from pathlib import Path

from functional_digraph_dp import count_poly, brute_poly


def det(A):
    A = [[Q(x) for x in row] for row in A]
    n = len(A)
    if n == 0:
        return Q(1)
    ans = Q(1)
    sign = 1
    for col in range(n):
        pivot = next((r for r in range(col, n) if A[r][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            A[col], A[pivot] = A[pivot], A[col]
            sign *= -1
        value = A[col][col]
        ans *= value
        for r in range(col + 1, n):
            if A[r][col]:
                factor = A[r][col] / value
                for c in range(col + 1, n):
                    A[r][c] -= factor * A[col][c]
                A[r][col] = 0
    return sign * ans


def direct_matrix_poly(p, f, t, row_fixed=None, col_fixed=None):
    n = len(p)
    row_fixed = {} if row_fixed is None else row_fixed
    col_fixed = {} if col_fixed is None else col_fixed
    F = [[Q(0) for _ in range(n)] for _ in range(n)]
    w = [Q(0)] * n
    for i, j in enumerate(p):
        if j is not None:
            F[i][j] = f[i]
            w[i] = f[i] * f[i]
    out = [Q(0)] * (n + 1)
    for mask in range(1 << n):
        I = [i for i in range(n) if mask >> i & 1]
        if any(((mask >> i) & 1) != bit for i, bit in row_fixed.items()):
            continue
        J_multiset = [p[i] for i in I]
        if any(j is None for j in J_multiset) or len(set(J_multiset)) != len(J_multiset):
            continue
        J = sorted(J_multiset)
        if any((j in J) != bool(bit) for j, bit in col_fixed.items()):
            continue
        minor = det([[F[i][j] for j in J] for i in I])
        weight = minor * minor
        for j in set(I).intersection(J):
            weight *= t[j]
        out[len(I)] += weight
    return out


def random_instance(rng, n):
    p = [None if rng.randrange(7) == 0 else rng.randrange(n) for _ in range(n)]
    f = [Q(rng.choice([-5, -3, -2, -1, 1, 2, 3, 5]), rng.choice([1, 2, 3]))
         if p[i] is not None else Q(0) for i in range(n)]
    t = [Q(rng.randrange(0, 7), rng.choice([1, 2, 3, 4])) for _ in range(n)]
    return p, f, t, [x * x for x in f]


def run_checks():
    rng = random.Random(7301907)
    cases = prefix_queries = minor_checks = 0
    for n in range(1, 9):
        for _ in range(20):
            p, f, t, w = random_instance(rng, n)
            got = count_poly(p, w, t)
            direct = direct_matrix_poly(p, f, t)
            assert got == direct == brute_poly(p, w, t)
            cases += 1
            for _q in range(3):
                row_fixed = {i: rng.randrange(2) for i in range(n) if rng.randrange(4) == 0}
                col_fixed = {j: rng.randrange(2) for j in range(n) if rng.randrange(4) == 0}
                got = count_poly(p, w, t, row_fixed, col_fixed)
                direct = direct_matrix_poly(p, f, t, row_fixed, col_fixed)
                assert got == direct == brute_poly(p, w, t, row_fixed, col_fixed)
                prefix_queries += 1
            for mask in range(1 << n):
                I = [i for i in range(n) if mask >> i & 1]
                if any(p[i] is None for i in I):
                    continue
                cols = [p[i] for i in I]
                if len(set(cols)) != len(cols):
                    continue
                J = sorted(cols)
                M = [[Q(0) for _ in range(n)] for _ in range(n)]
                for i, j in enumerate(p):
                    if j is not None:
                        M[i][j] = f[i]
                got_minor = det([[M[i][j] for j in J] for i in I])
                expected = Q(1)
                for i in I:
                    expected *= f[i]
                assert got_minor * got_minor == expected * expected
                minor_checks += 1

    # A strict extension of the cycle-only permutation case: two directed
    # self-cycles with in-trees, repeated image columns, and nontrivial weights.
    p = [1, 1, 1, 2, 2, 5, None]
    f = [Q(1), Q(2), Q(-1, 2), Q(3), Q(-2), Q(5, 3), Q(0)]
    w = [x * x for x in f]
    t = [Q(0), Q(2), Q(1, 3), Q(3, 2), Q(1), Q(4), Q(2)]
    assert len({v for v in p if v is not None}) < sum(v is not None for v in p)
    assert count_poly(p, w, t) == direct_matrix_poly(p, f, t)
    assert count_poly(p, w, t) == brute_poly(p, w, t)
    return {"exact_random_functional_matrices": cases,
            "exact_row_and_column_prefix_queries": prefix_queries,
            "nonzero_minor_identities": minor_checks,
            "strict_extension_fixture_coefficients": [str(x) for x in count_poly(p, w, t)],
            "all_pass": True}


if __name__ == "__main__":
    result = run_checks()
    out = Path(__file__).with_name("functional_digraph_checks_result.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
