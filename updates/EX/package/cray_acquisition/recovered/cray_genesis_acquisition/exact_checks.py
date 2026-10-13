#!/usr/bin/env python3
"""Exact-rational tests of response-cell certificates.

These tests are finite diagnostics, not a formal verification of the general
proof. SymPy rational arithmetic avoids floating-point ambiguities in the
reported identities and inequalities. No external data are used.
"""
from __future__ import annotations
import json
import random
from pathlib import Path
from typing import Sequence
import sympy as sp

Q = sp.Rational


def incidence(n: int, edges: Sequence[tuple[int, int]]) -> sp.Matrix:
    H = sp.zeros(n, len(edges))
    for e, (u, v) in enumerate(edges):
        H[u, e] = 1
        H[v, e] = -1
    return H


def harmonic(H: sp.Matrix, coeffs: list[sp.Rational],
             boundary: dict[int, sp.Rational]) -> tuple[sp.Matrix, sp.Rational]:
    n = H.rows
    L = H * sp.diag(*coeffs) * H.T
    h = sp.zeros(n, 1)
    for i, v in boundary.items():
        h[i] = v
    interior = [i for i in range(n) if i not in boundary]
    if interior:
        rhs = -(L * h).extract(interior, [0])
        hI = L.extract(interior, interior).inv() * rhs
        for i, value in zip(interior, hI):
            h[i] = value
    return h, (h.T * L * h)[0]


def components(nodes: list[int], edges: list[tuple[int, int]]) -> list[list[int]]:
    adj = {i: set() for i in nodes}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    unseen, out = set(nodes), []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        stack, comp = [start], []
        while stack:
            v = stack.pop()
            comp.append(v)
            new = adj[v] & unseen
            unseen.difference_update(new)
            stack.extend(new)
        out.append(sorted(comp))
    return out


def cell_pair(edges: list[tuple[int, int]], c0: list[sp.Rational],
              c: list[sp.Rational], h0: sp.Matrix, K: list[int],
              terminals: set[int]) -> tuple[sp.Rational, sp.Rational, sp.Rational]:
    n = h0.rows
    nodes = sorted({v for e in K for v in edges[e]})
    nodeidx = {v: i for i, v in enumerate(nodes)}
    localedges = [(nodeidx[edges[e][0]], nodeidx[edges[e][1]]) for e in K]
    HK = incidence(len(nodes), localedges)
    hbase = h0.extract(nodes, [0])
    drop = HK.T * hbase
    E0 = (drop.T * sp.diag(*(c0[e] for e in K)) * drop)[0]
    if E0 == 0:
        return Q(0), Q(0), Q(0)
    outside = {v for e in set(range(len(edges))) - set(K) for v in edges[e]}
    boundary_nodes = (outside | terminals) & set(nodes)
    boundary = {nodeidx[v]: h0[v] for v in boundary_nodes}
    _, DK = harmonic(HK, [c[e] for e in K], boundary)
    fbase = sp.diag(*(c0[e] for e in K)) * drop
    b = HK * fbase
    LK = HK * sp.diag(*(c[e] for e in K)) * HK.T
    z = sp.zeros(len(nodes), 1)
    for comp in components(list(range(len(nodes))), localedges):
        assert sum(b[i] for i in comp) == 0
        free = comp[1:]
        if free:
            zfree = LK.extract(free, free).inv() * b.extract(free, [0])
            for i, value in zip(free, zfree):
                z[i] = value
    NK = (b.T * z)[0]
    assert LK * z == b
    assert (hbase.T * b)[0] == E0
    return E0, DK, NK


def run(seed: int = 13102026, cases: int = 32) -> dict:
    rng = random.Random(seed)
    checks = 0
    records = []
    for case in range(cases):
        n = rng.randrange(4, 9)
        edges = [(i, i + 1) for i in range(n - 1)]
        extras = [(i, j) for i in range(n) for j in range(i + 2, n)]
        rng.shuffle(extras)
        edges += extras[:rng.randrange(min(6, len(extras)) + 1)]
        rng.shuffle(edges)
        m = len(edges)
        c0 = [Q(rng.randrange(1, 8), rng.randrange(1, 5)) for _ in edges]
        ratios = [Q(rng.randrange(1, 9), rng.randrange(1, 6)) for _ in edges]
        c = [x * r for x, r in zip(c0, ratios)]
        H = incidence(n, edges)
        h0, C0 = harmonic(H, c0, {0: Q(1), n - 1: Q(0)})
        _, C = harmonic(H, c, {0: Q(1), n - 1: Q(0)})
        a, b = min(ratios), max(ratios)
        R = b / a
        parts = [[e] for e in range(m)]
        last_upper, last_lower, last_gap = None, None, None
        steps = []
        while True:
            triples = [cell_pair(edges, c0, c, h0, K, {0, n-1}) for K in parts]
            assert sum(t[0] for t in triples) == C0
            checks += 1
            total_D = sum(t[1] for t in triples)
            total_N = sum(t[2] for t in triples)
            upper, lower = total_D, C0**2 / total_N
            A, B = total_D / C0, total_N / C0
            gap = A * B - 1
            assert lower <= C <= upper
            assert gap >= 0
            checks += 2
            varU, varV = Q(0), Q(0)
            for E0, D, N in triples:
                if E0 == 0:
                    assert D == 0 and N == 0
                    checks += 1
                    continue
                u, v, w = D / E0, N / E0, E0 / C0
                assert D * N >= E0**2
                assert a <= u <= b
                assert 1/b <= v <= 1/a
                assert u * v >= 1
                varU += w * (u - A)**2
                varV += w * (v - B)**2
                checks += 4
            assert varU / A**2 <= R * gap
            assert varV / B**2 <= R * gap
            checks += 2
            if last_upper is not None:
                assert upper <= last_upper
                assert lower >= last_lower
                assert gap <= last_gap
                checks += 3
            steps.append({'cells': len(parts), 'upper_over_C': float(upper/C),
                          'lower_over_C': float(lower/C), 'intrinsic_gap': float(gap)})
            last_upper, last_lower, last_gap = upper, lower, gap
            if len(parts) == 1:
                assert upper == lower == C
                checks += 1
                break
            parts = [sum(parts[i:i+2], []) for i in range(0, len(parts), 2)]
        records.append({'case': case, 'vertices': n, 'edges': m, 'partitions': steps})
    # A balanced diamond contains an exactly zero-reference-work transverse edge.
    edges = [(0, 1), (1, 3), (0, 2), (2, 3), (1, 2)]
    H = incidence(4, edges)
    c0 = [Q(1)] * 5
    h0, C0 = harmonic(H, c0, {0: Q(1), 3: Q(0)})
    c = [Q(1, 2), Q(2), Q(2), Q(1, 2), Q(10)**12]
    zero = cell_pair(edges, c0, c, h0, [4], {0, 3})
    assert zero == (0, 0, 0)
    triples = [cell_pair(edges, c0, c, h0, [e], {0, 3}) for e in range(5)]
    _, C = harmonic(H, c, {0: Q(1), 3: Q(0)})
    upper = sum(t[1] for t in triples)
    lower = C0**2 / sum(t[2] for t in triples)
    assert lower <= C <= upper
    checks += 2
    return {'status': 'all finite exact-rational assertions passed; not a general formal proof',
            'seed': seed, 'random_graph_cases': cases, 'assertions_counted': checks,
            'zero_work_edge_test': 'passed with target transverse conductance 10^12',
            'records': records, 'sympy_version': sp.__version__}


if __name__ == '__main__':
    result = run()
    dest = Path(__file__).with_name('exact_results.json')
    dest.write_text(json.dumps(result, indent=2))
    print(json.dumps({k:v for k,v in result.items() if k != 'records'}, indent=2))
