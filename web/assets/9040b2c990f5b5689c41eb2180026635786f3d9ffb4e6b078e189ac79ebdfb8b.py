#!/usr/bin/env python3
"""Exact rational diagnostics for the fixed-filter perfect-matching reduction.

This verifies finite instances; the general proof is in RESULT.txt. No floats,
external packages, random inputs, or arbitrary filter predicates are used.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, lcm
import json
from pathlib import Path


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def det(a):
    a = [[Q(x) for x in row] for row in a]
    n = len(a)
    ans = Q(1)
    for j in range(n):
        p = next((i for i in range(j, n) if a[i][j]), None)
        if p is None:
            return Q(0)
        if p != j:
            a[p], a[j] = a[j], a[p]
            ans = -ans
        pivot = a[j][j]
        ans *= pivot
        for i in range(j + 1, n):
            if a[i][j]:
                ratio = a[i][j] / pivot
                for s in range(j + 1, n):
                    a[i][s] -= ratio * a[j][s]
                a[i][j] = Q(0)
    return ans


def inverse(a):
    n = len(a)
    a = [[Q(x) for x in row] + eye(n)[i] for i, row in enumerate(a)]
    for j in range(n):
        p = next(i for i in range(j, n) if a[i][j])
        a[p], a[j] = a[j], a[p]
        pivot = a[j][j]
        a[j] = [x / pivot for x in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                ratio = a[i][j]
                a[i] = [x - ratio * y for x, y in zip(a[i], a[j])]
    return [row[n:] for row in a]


def mul(a, b):
    return [[sum((a[i][s] * b[s][j] for s in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def pm_count(m, edges):
    adj = [set() for _ in range(m)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    def recurse(vertices):
        if not vertices:
            return 1
        u = min(vertices)
        return sum(recurse(vertices - {u, v})
                   for v in adj[u] & vertices)
    return recurse(set(range(m)))


def pad(m, edges):
    """v is a leaf forcing uv; all extra edges are then unusable."""
    edges = list(edges)
    if len(edges) >= m:
        return m, edges, False
    assert edges and m % 2 == 0
    u, v = m, m + 1
    return m + 2, edges + [(u, v)] + [(u, w) for w in range(m)], True


def pair_instance(m, edges):
    m2, edges2, padded = pad(m, edges)
    e = len(edges2)
    d = e - m2
    n = e + d
    assert n == m2 + 2 * d and n % 2 == 0
    b = [[Q(0) for _ in range(n)] for _ in range(n)]
    c = [[Q(0) for _ in range(n)] for _ in range(n)]
    for j, (u, v) in enumerate(edges2):
        b[u][j] = 1
        c[v][j] = 1
    for j in range(d):
        b[m2 + 2 * j][e + j] = 1
        c[m2 + 2 * j + 1][e + j] = 1
    assert all(sum(b[i][j] for i in range(n)) == 1 for j in range(n))
    f = [next(i for i in range(n) if b[i][j]) for j in range(n)]
    period = lcm(*range(1, n + 1))
    for j in range(n):
        x = j
        for _ in range(n):
            x = f[x]
        y = x
        # Reduce an orbit modulo its period instead of iterating the huge lcm.
        seen, orbit = {}, []
        while y not in seen:
            seen[y] = len(orbit)
            orbit.append(y)
            y = f[y]
        assert seen[y] == 0 and period % len(orbit) == 0
    return b, c, dict(original_vertices=m, original_edges=len(edges),
                      vertices=m2, edges=e, dummies=d, n=n, k=n // 2,
                      padded=padded, functional_map=f)


def paired_weights(b, c, t):
    n = len(b)
    k = n // 2
    bt = [[b[i][j] + (t if i == j else 0) for j in range(n)] for i in range(n)]
    weights = {}
    for s in combinations(range(n), k):
        # Interleaved pair order changes determinant sign only.
        matrix = [[x for j in s for x in (bt[i][j], c[i][j])]
                  for i in range(n)]
        weights[s] = det(matrix) ** 2
    return weights, bt


def target_weights(a):
    n = len(a)
    return {s: det([[a[i][j] for j in range(n) if j not in s] for i in s]) ** 2
            for s in combinations(range(n), n // 2)}


def lagrange_at_zero(points):
    result = Q(0)
    for i, (x, y) in enumerate(points):
        ratio = Q(1)
        for j, (xx, _) in enumerate(points):
            if i != j:
                ratio *= -xx / (x - xx)
        result += y * ratio
    return result


def canonical_norm(a, k):
    h = mul(a, transpose(a))
    power = eye(len(a))
    traces = [Q(0)]
    for _ in range(k):
        power = mul(power, h)
        traces.append(sum((power[i][i] for i in range(len(a))), Q(0)))
    coefficients = [Q(1)]
    for j in range(1, k + 1):
        coefficients.append(sum(((-1) ** (i - 1) * coefficients[j - i] * traces[i]
                                 for i in range(1, j + 1)), Q(0)) / j)
    return coefficients[k]


def fmt(x):
    x = Q(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def pfaffian_estimator_check(blocks):
    n = 4 * blocks
    a = [[Q(0) for _ in range(n)] for _ in range(n)]
    for block in range(blocks):
        for j in range(4):
            a[4 * block + j][4 * block + (j + 1) % 4] = 1
    values = []
    for signs in product((-1, 1), repeat=n):
        skew = [[signs[i] * a[i][j] - signs[j] * a[j][i]
                 for j in range(n)] for i in range(n)]
        values.append(det(skew))
    mean = sum(values, Q(0)) / len(values)
    second = sum((x * x for x in values), Q(0)) / len(values)
    assert mean == sum(target_weights(a).values()) == 2 ** blocks
    assert second / mean ** 2 - 1 == 2 ** blocks - 1
    assert set(values) == {Q(0), Q(4 ** blocks)}
    return dict(blocks=blocks, n=n, signs_enumerated=len(values),
                mean=fmt(mean), second_moment=fmt(second),
                relative_variance=fmt(second / mean ** 2 - 1))


def check_case(name, m, edges):
    b, c, metadata = pair_instance(m, edges)
    n, k = metadata["n"], metadata["k"]
    base, _ = paired_weights(b, c, Q(0))
    count = pm_count(m, edges)
    assert all(x in (0, 1) for x in base.values())
    assert sum(base.values()) == count
    checked = 0
    for t in (Q(1, 2), Q(1, 3), Q(1, 16)):
        weights, bt = paired_weights(b, c, t)
        factor = det(bt) ** 2
        assert factor > 0
        a = transpose(mul(inverse(bt), c))
        target = target_weights(a)
        for s in weights:
            assert weights[s] == factor * target[s], (name, t, s)
            checked += 1
    points = []
    for j in range(n + 1):
        t = Q(1, j + 2)
        weights, bt = paired_weights(b, c, t)
        assert det(bt)
        points.append((t, sum(weights.values())))
    recovered = lagrange_at_zero(points)
    assert recovered == count
    q = n + (64 * k).bit_length()
    t = Q(1, 2 ** q)
    weights, bt = paired_weights(b, c, t)
    r = sum(weights.values())
    bound = 8 * k * 2 ** n * t
    actual_l1 = sum(abs(weights[s] - base[s]) for s in base)
    assert k * t <= Q(1, 2)
    assert actual_l1 <= bound < Q(1, 4)
    assert (r + Q(1, 2)).numerator // (r + Q(1, 2)).denominator == count
    factor = det(bt) ** 2
    a = transpose(mul(inverse(bt), c))
    target = target_weights(a)
    z = sum(target.values())
    assert factor * z == r
    denominator = lcm(*(x.denominator for row in a for x in row))
    integer_a = [[int(x * denominator) for x in row] for row in a]
    integer_z = sum(target_weights(integer_a).values())
    assert integer_z == denominator ** (2 * k) * z
    canonical = canonical_norm(a, k)
    assert canonical >= z > 0
    tv = None
    if count:
        tv = sum(abs(weights[s] / r - base[s] / count) for s in base) / 2
        assert tv <= bound / (1 - bound)
    return dict(name=name, **metadata, perfect_matchings=count,
                selected_subsets=comb(n, k), chart_weight_equalities=checked,
                interpolation_constant=fmt(recovered), dyadic_q=q,
                perturbation=fmt(t), perturbed_R=fmt(r),
                l1_error=fmt(actual_l1), l1_bound=fmt(bound),
                normalized_TV=None if tv is None else fmt(tv),
                integer_chart_denominator_bits=denominator.bit_length(),
                canonical_success_probability=fmt(z / canonical),
                expected_canonical_trials=fmt(canonical / z),
                max_chart_entry_numerator_bits=max(abs(x.numerator).bit_length() for row in a for x in row),
                max_chart_entry_denominator_bits=max(x.denominator.bit_length() for row in a for x in row))


def main():
    cases = [
        ("cycle4", 4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
        ("K4_with_forced_dummy_pairs", 4, list(combinations(range(4), 2))),
        ("path4_with_count_preserving_leaf_padding", 4, [(0, 1), (1, 2), (2, 3)]),
        ("star4_zero_perfect_matchings", 4, [(0, 1), (0, 2), (0, 3)]),
    ]
    results = [check_case(*case) for case in cases]
    certificate = dict(status="PASS", arithmetic="exact Python Fraction", cases=results,
                       total_chart_weight_equalities=sum(x["chart_weight_equalities"] for x in results),
                       pfaffian_estimator=[pfaffian_estimator_check(b) for b in (1, 2)],
                       scope="Finite diagnostics only; no external proof validation or novelty claim.")
    output = Path(__file__).with_name("check_reduction.json")
    output.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps(dict(status=certificate["status"],
                         cases=len(results), equalities=certificate["total_chart_weight_equalities"],
                         output=str(output))))


if __name__ == "__main__":
    main()
