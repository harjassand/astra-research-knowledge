"""Exact finite checks of the odd-degree proof's coefficient interface.

The universal proof is in parity_six_hole_exchange.txt. No FPRAS or walk is run.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations
from functools import lru_cache
from math import isqrt
from pathlib import Path
import json


def polynomial_product(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def gaussian_product(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


@lru_cache(None)
def signed_permutations(n):
    return [(p, (-1) ** sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n)))
            for p in permutations(range(n))]


def determinant_gaussian(a):
    value = (0, 0)
    for p, sign in signed_permutations(len(a)):
        term = (sign, 0)
        for i, j in enumerate(p):
            term = gaussian_product(term, a[i][j])
        value = (value[0] + term[0], value[1] + term[1])
    return value


def partitions(a):
    n = len(a)
    out = [0] * (1 << n)
    for holes in range(1 << n):
        retained = [i for i in range(n) if not holes >> i & 1]
        if len(retained) % 2:
            continue
        for rows in combinations(retained, len(retained) // 2):
            cols = [j for j in retained if j not in rows]
            d = determinant_gaussian([[a[i][j] for j in cols] for i in rows])
            out[holes] += d[0] ** 2 + d[1] ** 2
    return out


def mask(items):
    return sum(1 << i for i in items)


def radical_check(lhs, terms):
    if lhs <= sum(terms):
        return
    scale = 10 ** 60
    hi = isqrt(lhs * scale * scale) + 1
    lo = sum(isqrt(v * scale * scale) for v in terms)
    assert hi <= lo, (lhs, terms)


def coefficient_fixture(f, n, S, T, a):
    D = S ^ T
    sites = [i for i in range(n) if D >> i & 1]
    J = [i for i in sites if i != a]
    m = len(sites)
    assert m > 0 and m % 2 == 0 and a in sites
    assert f[S] and f[T]
    weights = {j: Q(j + 2, j + 1) for j in J}
    W = Q(1)
    for w in weights.values():
        W *= w
    coefficients = [Q(0)] * m
    # Full twist by T, then zero outside D, then a=1 and x_j=w_j*z.
    for local in range(1 << m):
        U = mask(sites[k] for k in range(m) if local >> k & 1)
        if U.bit_count() % 2:
            continue
        c = f[T ^ U]
        degree, value = 0, Q(c)
        for j in J:
            if U >> j & 1:
                degree += 1
                value *= weights[j]
        coefficients[degree] += value
    A = [f[T ^ (1 << a) ^ (1 << j)] for j in J]
    B = [f[S ^ (1 << a) ^ (1 << j)] for j in J]
    assert coefficients[0] == f[T]
    assert coefficients[-1] == f[S] * W
    assert coefficients[1] == sum((v * weights[j] for v, j in zip(A, J)), Q(0))
    assert coefficients[-2] == W * sum((v / weights[j] for v, j in zip(B, J)), Q(0))
    margin = coefficients[1] * coefficients[-2] - coefficients[0] * coefficients[-1]
    assert margin >= 0
    terms = [x * y for x, y in zip(A, B)]
    radical_check(f[S] * f[T], terms)
    return {"n": n, "S": S, "T": T, "a": a, "difference_size": m,
            "common_occupied_core_size": n - (S | T).bit_count(),
            "common_hole_size": (S & T).bit_count(),
            "polynomial_coefficients": [str(c) for c in coefficients],
            "endpoint_minor_margin": str(margin),
            "exchange_left_product": f[S] * f[T],
            "exchange_right_products": terms}


def main():
    root_checks = []
    for pairs in range(5):
        p = [Q(3, 2), Q(1)]
        for j in range(pairs):
            p = polynomial_product(p, [Q(j + 2), Q(0 if j % 2 == 0 else 1), Q(1)])
        margin = p[1] * p[-2] - p[0] * p[-1]
        assert margin >= 0
        root_checks.append({"degree": len(p) - 1, "coefficients": [str(c) for c in p],
                            "endpoint_minor_margin": str(margin)})
    # Odd degree is necessary for the lemma: 1+z^2 has boundary imaginary roots.
    assert Q(0) * Q(0) - Q(1) * Q(1) == -1

    fixtures = []
    for n in [6, 8]:
        a = [[(0, 0) for _ in range(n)] for _ in range(n)]
        for i in range(0, n, 2):
            a[i][i + 1] = (1, 0)
        f = partitions(a)
        assert all(f[u] == int(all(bool(u >> i & 1) == bool(u >> (i + 1) & 1)
                                 for i in range(0, n, 2)))
                   for u in range(1 << n))
        S, T = mask([0, 1, 2, 3]), mask([4, 5])
        for site in range(6):
            r = coefficient_fixture(f, n, S, T, site)
            assert r['exchange_left_product'] == 1
            assert sum(r['exchange_right_products']) == 1
            assert r['endpoint_minor_margin'] == '0'
            fixtures.append(r)

    n = 8
    a = [[((17 * i + 7 * j + 3 * i * j) % 5 - 2,
           (3 * i + 11 * j + 5 * i * j) % 7 - 3) if i != j else (0, 0)
          for j in range(n)] for i in range(n)]
    f = partitions(a)
    # Six differences, a genuine shared occupied core, and all choices of a.
    S, T = mask([0, 1, 2, 3]), mask([4, 5])
    for site in range(6):
        fixtures.append(coefficient_fixture(f, n, S, T, site))
    # Shared HOLES require twisting the full T before the outside-zero step.
    S, T = mask([0, 1, 2, 3]), mask([2, 3, 6, 7])
    for site in [0, 1, 6, 7]:
        fixtures.append(coefficient_fixture(f, n, S, T, site))

    result = {"all_passed": True, "root_factor_fixtures": len(root_checks),
              "coefficient_index_fixtures": len(fixtures),
              "sharp_exchange_fixtures": 12,
              "complex_shared_occupied_core_fixtures": 6,
              "complex_shared_hole_fixtures": 4,
              "scope": "Finite exact arithmetic diagnostics; universal proof is in report; no FPRAS.",
              "root_checks": root_checks, "fixtures": fixtures}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('root_checks', 'fixtures')}))


if __name__ == '__main__':
    main()
