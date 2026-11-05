#!/usr/bin/env python3
"""Exact dyadic Pauli-algebra checks of the all-n cascade continuity law.

No dense state matrices or numerical optimization are used. All coefficients
in the tested identities are Gaussian integers divided by powers of two.
"""
import json
from pathlib import Path


def add(*terms):
    result = {}
    for scale, operator in terms:
        for string, value in operator.items():
            result[string] = result.get(string, 0) + scale*value
    return {key: value for key, value in result.items() if value}


def multiply(left, right):
    result = {}
    for a, x in left.items():
        for b, y in right.items():
            phase = x*y
            string = []
            for u, v in zip(a, b):
                if u == 0:
                    string.append(v)
                elif v == 0:
                    string.append(u)
                elif u == v:
                    string.append(0)
                else:
                    string.append(6-u-v)
                    phase *= 1j if (u, v) in [(1, 2), (2, 3), (3, 1)] else -1j
            key = tuple(string)
            result[key] = result.get(key, 0) + phase
    return {key: value for key, value in result.items() if value}


def comm(left, right):
    return add((1, multiply(left, right)), (-1, multiply(right, left)))


def epsilon(a, b, c):
    if len({a, b, c}) < 3:
        return 0
    return 1 if (a, b, c) in [(1, 2, 3), (2, 3, 1), (3, 1, 2)] else -1


def string(n, entries):
    result = [0]*n
    for position, value in entries.items():
        result[position] = value
    return {tuple(result): 1}


def dot(n, i, j):
    return add(*[(1, string(n, {i: a, j: a})) for a in range(1, 4)])


def charges(n):
    y = [{}, {}, {}]
    chirality = {}
    for i in range(n):
        for j in range(i+1, n):
            for a in range(1, 4):
                for b in range(1, 4):
                    for c in range(1, 4):
                        e = epsilon(a, b, c)
                        if e:
                            y[a-1] = add((1, y[a-1]), (e, string(n, {i: b, j: c})))
                            for k in range(j+1, n):
                                chirality = add((1, chirality), (e, string(n, {i: a, j: b, k: c})))
    return y, chirality


def adjoint_generator(x, y, chirality):
    return add(*[(-1/32, comm(item, comm(item, x))) for item in y],
               (-1j/8, comm(chirality, x)))


def norm2(x):
    return float(sum(abs(v)**2 for v in x.values()))


def main():
    results = []
    for n in range(2, 7):
        y, chirality = charges(n)
        h = add(*[(1, dot(n, j, j+1)) for j in range(n-1)])
        for j in range(n-1):
            actual = adjoint_generator(dot(n, j, j+1), y, chirality)
            target = add((-1, dot(n, j, j+1)),
                         *[(1, dot(n, i, j)) for i in range(j)],
                         *[(-1, dot(n, i, j+1)) for i in range(j)])
            assert not add((1, actual), (-1, target))
        boundary = add(*[(-1, dot(n, i, n-1)) for i in range(n-1)])
        assert not add((1, adjoint_generator(h, y, chirality)), (-1, boundary))
        commutator_norm = 0.
        for a in range(1, 4):
            target = add((4j, string(n, {0: a})), (-4j, string(n, {n-1: a})))
            actual = comm(y[a-1], h)
            assert not add((1, actual), (-1, target))
            commutator_norm += norm2(actual)
        assert commutator_norm == 96
        assert norm2(h) == 3*(n-1)
        remote_pair = adjoint_generator(dot(n, 0, n-1), y, chirality)
        high_weight = {key: value for key, value in remote_pair.items()
                       if sum(a != 0 for a in key) > 2}
        results.append(dict(n=n, adjacent_identities=n-1,
                            continuity_exact=True,
                            Yangian_boundary_commutator_exact=True,
                            H_norm_squared=norm2(h),
                            H_Dirichlet_loss=commutator_norm/32,
                            remote_pair_higher_weight_norm_squared=norm2(high_weight),
                            remote_pair_max_weight=max(sum(a != 0 for a in key) for key in remote_pair)))
    Path(__file__).with_name('cascade_continuity_checks.json').write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
