#!/usr/bin/env python3
"""Exact small integer checks of the owned phase estimator; no timing benchmark."""
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def det(a):
    a = [[Fraction(v) for v in row] for row in a]
    out = Fraction(1)
    for i in range(len(a)):
        j = next((j for j in range(i, len(a)) if a[j][i]), None)
        if j is None:
            return Fraction(0)
        if j != i:
            a[i], a[j] = a[j], a[i]
            out = -out
        pivot = a[i][i]
        out *= pivot
        for j in range(i + 1, len(a)):
            ratio = a[j][i] / pivot
            for k in range(i + 1, len(a)):
                a[j][k] -= ratio * a[i][k]
    return out


def pf(a):
    if not a:
        return 1
    return sum((-1) ** (j + 1) * a[0][j] *
               pf([[a[s][t] for t in range(1, len(a)) if t != j]
                   for s in range(1, len(a)) if s != j])
               for j in range(1, len(a)))


def audit(f):
    n = len(f)
    k = n // 2
    coeff = {}
    target = Fraction(0)
    for s in combinations(range(n), k):
        t = [i for i in range(n) if i not in s]
        target += det([[f[i][j] for j in t] for i in s]) ** 2
        columns = []
        for i in s:
            columns += [[int(j == i) for j in range(n)], f[i]]
        coeff[s] = det([[columns[j][i] for j in range(n)] for i in range(n)])
    assert sum(v * v for v in coeff.values()) == target
    sums = [0, 0]
    roots = (1, -1, 1j, -1j)
    for z in product(roots, repeat=n):
        m = [[z[i] * f[i][j] - z[j] * f[j][i] for j in range(n)] for i in range(n)]
        value = pf(m)
        expansion = sum(complex(c) * product_phase(z, s) for s, c in coeff.items())
        assert value == expansion
        # All operations here are integer real/imaginary arithmetic within
        # binary64's exact range for these tiny fixtures; verify that explicitly.
        assert value.real == int(value.real) and value.imag == int(value.imag)
        x = int(value.real) ** 2 + int(value.imag) ** 2
        sums[0] += x
        sums[1] += x * x
    mean, second = (Fraction(x, 4 ** n) for x in sums)
    assert mean == target
    return {'n': n, 'phase_points': 4 ** n, 'normalizer': str(target),
            'phase_mean': str(mean), 'phase_second_moment': str(second),
            'relative_variance': str(second / mean ** 2 - 1)}


def product_phase(z, s):
    out = 1
    for i in s:
        out *= z[i]
    return out


def main():
    records = []
    for blocks in (1, 2, 3):
        n = 2 * blocks
        f = [[int(i ^ 1 == j) for j in range(n)] for i in range(n)]
        r = audit(f)
        assert Fraction(r['phase_second_moment']) == 6 ** blocks
        assert Fraction(r['normalizer']) == 2 ** blocks
        assert Fraction(r['relative_variance']) == Fraction(3, 2) ** blocks - 1
        r['fixture'] = 'independent_swap_blocks'
        records.append(r)
    f = [[0, 1, 2, -1], [2, 0, -1, 1], [1, -2, 0, 2], [-1, 1, 1, 0]]
    r = audit(f)
    r['fixture'] = 'coupled_integer_matrix'
    records.append(r)
    output = {'scope': 'FINITE_EXACT_IDENTITY_AND_VARIANCE_CHECK', 'records': records}
    path = Path(__file__).with_name('PHASE_IDENTITY_CHECK.json')
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
