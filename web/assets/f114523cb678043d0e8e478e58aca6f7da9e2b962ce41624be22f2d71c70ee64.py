"""Scoped algebra checks for the scout's constructive local embedding lemma.

The all-graph claim rests on the written proof, not this finite enumeration.
No source scripts, graph packages, optimizers, or theorem provers are used.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import math
import time


def vertex_colors(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    colors = []
    for u in range(n):
        forbidden = {colors[v] for v in adj[u] if v < u}
        c = 0
        while c in forbidden:
            c += 1
        colors.append(c)
    return colors, adj


def edge_conflict(e, f, adj):
    return bool(set(e) & set(f)) or any(v in adj[u] for u in e for v in f)


def strong_colors(edges, adj):
    colors = []
    for i, e in enumerate(edges):
        forbidden = {colors[j] for j in range(i) if edge_conflict(e, edges[j], adj)}
        c = 0
        while c in forbidden:
            c += 1
        colors.append(c)
    return colors


def build(n, edges, sq_lengths, override_edge_colors=None):
    vcolors, adj = vertex_colors(n, edges)
    ecolors = strong_colors(edges, adj) if override_edge_colors is None else override_edge_colors
    c = (min(sq_lengths) + max(sq_lengths)) / 4
    q = [c - length / 2 for length in sq_lengths]
    residuals = [c for _ in range(n)]
    sparse = [dict() for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        residuals[u] -= abs(q[i])
        residuals[v] -= abs(q[i])
        # Tuple (sign, squared amplitude, identity) is an exact radical term.
        sparse[u][("edge", ecolors[i])] = (1 if q[i] >= 0 else -1, abs(q[i]), i)
        sparse[v][("edge", ecolors[i])] = (1, abs(q[i]), i)
    for u in range(n):
        assert residuals[u] >= 0
        sparse[u][("private", vcolors[u])] = (1, residuals[u], -1)
    return c, q, residuals, sparse, ecolors, vcolors


def check(n, edges, sq_lengths):
    c, q, residuals, sparse, ecolors, vcolors = build(n, edges, sq_lengths)
    degree = [0] * n
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    delta = max(degree)
    dimension = (max(ecolors) + 1) + (max(vcolors) + 1)
    assert dimension <= 2 * delta * delta - delta + 2
    for u in range(n):
        assert sum(t[1] for t in sparse[u].values()) == c
    for i, (u, v) in enumerate(edges):
        shared = sparse[u].keys() & sparse[v].keys()
        assert shared == {("edge", ecolors[i])}
        left, right = sparse[u][("edge", ecolors[i])], sparse[v][("edge", ecolors[i])]
        assert left[2] == right[2] == i
        inner_product = left[0] * right[0] * left[1]
        assert inner_product == q[i]
        assert 2 * c - 2 * inner_product == sq_lengths[i]
    return dimension, min(residuals)


def main():
    started = time.perf_counter()
    graph_count = 0
    instances = 0
    edge_checks = 0
    max_dimension = 0
    zero_residual_cases = 0
    for n in range(2, 7):
        possible = list(combinations(range(n), 2))
        for mask in range(1, 1 << len(possible)):
            edges = [e for i, e in enumerate(possible) if mask & (1 << i)]
            degree = [0] * n
            for u, v in edges:
                degree[u] += 1
                degree[v] += 1
            delta = max(degree)
            if delta > 3:
                continue
            graph_count += 1
            upper = F(delta + 1, delta - 1) if delta >= 2 else F(2)
            patterns = [
                [F(1) for _ in edges],
                [F(1) if i % 2 == 0 else upper for i in range(len(edges))],
                [F(1) + (upper - 1) * F((3 * i + n) % 7, 6) for i in range(len(edges))],
            ]
            for pattern in patterns:
                dim, residual = check(n, edges, pattern)
                instances += 1
                edge_checks += len(edges)
                max_dimension = max(max_dimension, dim)
                zero_residual_cases += residual == 0

    # Ordinary proper edge coloring fails: opposite C4 edges share coordinates.
    edges = [(0, 1), (1, 2), (2, 3), (0, 3)]
    sq_lengths = [F(1), F(2), F(1), F(2)]
    c, q, residuals, sparse, *_ = build(4, edges, sq_lengths, [0, 1, 0, 1])
    output = []
    for coords in sparse:
        output.append({key: sign * math.sqrt(float(amp)) for key, (sign, amp, _) in coords.items()})
    measured = sum((output[0].get(key, 0) - output[1].get(key, 0)) ** 2
                   for key in output[0].keys() | output[1].keys())
    assert abs(measured - .5) < 1e-12 and measured != 1

    result = {
        "scope": "All labelled simple graphs on 2..6 vertices with maximum degree <=3; three deterministic squared-length patterns per graph",
        "graphs": graph_count, "instances": instances,
        "exact_edge_checks": edge_checks, "max_observed_dimension": max_dimension,
        "zero_residual_instances": zero_residual_cases,
        "ordinary_edge_coloring_control": {"target_squared_length": 1, "observed_squared_length": measured, "expected_failure": True},
        "elapsed_seconds": time.perf_counter() - started,
        "universal_proof": "work/scouts/topology_geometry.md",
        "status": "finite construction checks pass; no novelty or full-open-problem certificate",
    }
    path = Path(__file__).with_name("topology_geometry_checks.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
