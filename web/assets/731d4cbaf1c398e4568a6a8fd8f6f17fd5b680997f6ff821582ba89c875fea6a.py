#!/usr/bin/env python3
"""Exact Fraction replay for the weighted-PM-to-fixed-Z AP reduction.

This checks finite identities and the stated perturbation/weight-approximation
bounds. It is evidence for the construction, not a proof of the uniform claim.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
import json


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


def pm_weight(m, edges):
    adj = [[] for _ in range(m)]
    for e, (u, v, w) in enumerate(edges):
        adj[u].append((v, e, Q(w)))
        adj[v].append((u, e, Q(w)))

    def rec(mask):
        if mask == 0:
            return Q(1)
        u = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << u)
        ans = Q(0)
        for v, e, w in adj[u]:
            if rest & (1 << v):
                ans += w * rec(rest ^ (1 << v))
        return ans

    return rec((1 << m) - 1)


def pad(m, edges):
    edges = [(u, v, Q(w)) for u, v, w in edges if Q(w) > 0]
    if len(edges) >= m:
        return m, edges, False
    assert m % 2 == 0 and m > 0
    u, v = m, m + 1
    # The leaf v forces uv. The u--old-vertex edges are positive but unusable.
    return m + 2, edges + [(u, v, Q(1))] + [(u, w, Q(1)) for w in range(m)], True


def dyadic_sqrt_floor(x, s):
    x = Q(x)
    t2 = (x.numerator << (2 * s)) // x.denominator
    return Q(isqrt(t2), 1 << s)


def paired_weights(b, c, t):
    n = len(b)
    k = n // 2
    bt = [[b[i][j] + (t if i == j else 0) for j in range(n)] for i in range(n)]
    values = {}
    for selected in combinations(range(n), k):
        mat = [[x for j in selected for x in (bt[i][j], c[i][j])]
               for i in range(n)]
        values[selected] = det(mat) ** 2
    return values, bt


def target_weights(a):
    n = len(a)
    return {s: det([[a[i][j] for j in range(n) if j not in s] for i in s]) ** 2
            for s in combinations(range(n), n // 2)}


def ceil_log2_fraction(x):
    x = Q(x)
    q = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    while Q(2) ** q < x:
        q += 1
    while q and Q(2) ** (q - 1) >= x:
        q -= 1
    return q


def make_chart(m, edges, rho=Q(1, 8)):
    m, edges, padded = pad(m, edges)
    E = len(edges)
    D = E - m
    n = E + D
    assert D >= 0 and n == m + 2 * D and n % 2 == 0
    k = n // 2
    r = m // 2
    M = max(w for _, _, w in edges)
    p = [w / M for _, _, w in edges]
    pmin = min(p)
    eta = rho / (64 * r)
    # Since sqrt(pmin) >= pmin, this precision gives
    # 2^-s <= eta*sqrt(pmin)/4.
    s = ceil_log2_fraction(4 / (eta * pmin))
    q = [dyadic_sqrt_floor(x, s) for x in p]

    b = [[Q(0) for _ in range(n)] for _ in range(n)]
    c = [[Q(0) for _ in range(n)] for _ in range(n)]
    for j, (u, v, _) in enumerate(edges):
        b[u][j] = 1
        c[v][j] = q[j]
    for j in range(D):
        b[m + 2 * j][E + j] = 1
        c[m + 2 * j + 1][E + j] = 1

    # eps is chosen so 8*r*2^n*eps <= rho*pmin^r/32.
    qeps = ceil_log2_fraction(Q(256 * k * (2 ** n), 1) / (rho * pmin ** r))
    eps = Q(1, 1 << qeps)
    return b, c, dict(m=m, edges=E, dummies=D, n=n, k=k, matching_edges=r, padded=padded,
                      scale= M, p=p, pmin=pmin, eta=eta, sqrt_bits=s,
                      q=q, eps_bits=qeps, eps=eps, rho=rho)


def fmt(x):
    x = Q(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def check_case(name, m, edges):
    source = pm_weight(m, edges)
    b, c, meta = make_chart(m, edges)
    n, k = meta["n"], meta["k"]
    base, _ = paired_weights(b, c, Q(0))
    matching_edges = meta["matching_edges"]
    normalized_source = source / meta["scale"] ** matching_edges
    approx_source = sum(base.values(), Q(0))
    # Every edge activity square is a lower approximation to its normalized
    # weight, with relative error at most 2*eta; a k-edge matching compounds it.
    approx_error = abs(approx_source - normalized_source)
    assert approx_source <= normalized_source
    assert approx_error <= 2 * matching_edges * meta["eta"] * normalized_source

    weights, bt = paired_weights(b, c, meta["eps"])
    factor = det(bt) ** 2
    assert factor > 0
    a = transpose(mul(inverse(bt), c))
    chart_values = target_weights(a)
    equalities = 0
    for sset, value in weights.items():
        assert value == factor * chart_values[sset]
        equalities += 1
    r_eps = sum(weights.values(), Q(0))
    z = sum(chart_values.values(), Q(0))
    assert factor * z == r_eps
    actual_l1 = sum((abs(weights[sset] - base[sset]) for sset in base), Q(0))
    perturbation_bound = 8 * k * (2 ** n) * meta["eps"]
    assert actual_l1 <= perturbation_bound
    assert perturbation_bound <= meta["rho"] * meta["pmin"] ** matching_edges / 32
    if source > 0:
        assert meta["pmin"] ** matching_edges <= normalized_source
        assert abs(r_eps - normalized_source) <= (meta["rho"] / 16) * normalized_source
    return dict(name=name, original_vertices=m, input_edges=len(edges),
                positive_source=source > 0, **{
                    key: (fmt(val) if isinstance(val, Q) else val)
                    for key, val in meta.items()
                    if key not in ("p", "q")
                },
                positive_edge_activities=len(meta["p"]),
                max_activity_denominator_bits=max(x.denominator.bit_length() for x in meta["q"]),
                sqrt_approx_error=fmt(approx_error),
                source_normalized=fmt(normalized_source),
                base_chart_sum=fmt(approx_source),
                perturbed_R=fmt(r_eps), z=fmt(z), chart_scale=fmt(factor),
                chart_equalities=equalities,
                perturbation_l1=fmt(actual_l1),
                perturbation_bound=fmt(perturbation_bound),
                perturbation_to_source=fmt(abs(r_eps-normalized_source)) if source else None,
                max_chart_numerator_bits=max(abs(x.numerator).bit_length() for row in a for x in row),
                max_chart_denominator_bits=max(x.denominator.bit_length() for row in a for x in row))


def main():
    cases = [
        ("weighted_cycle4_non_square", 4,
         [(0, 1, Q(1)), (1, 2, Q(2, 3)), (2, 3, Q(1, 3)), (3, 0, Q(5, 7))]),
        ("weighted_K4_with_dummies", 4,
         [(u, v, 2 * Q(w)) for (u, v), w in zip(combinations(range(4), 2),
                                                (1, Q(2, 5), Q(3, 7), Q(4, 9), Q(1, 6), Q(7, 10)))]),
        ("zero_source_star", 4,
         [(0, 1, Q(1)), (0, 2, Q(1, 2)), (0, 3, Q(1, 3))]),
    ]
    reports = [check_case(*case) for case in cases]
    result = dict(status="PASS", arithmetic="exact Python Fraction",
                  source="small weighted general-graph perfect-matching partition functions",
                  cases=reports,
                  scope="Finite identity and error-bound checks only; no external proof validation or novelty claim.")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
