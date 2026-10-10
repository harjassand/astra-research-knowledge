#!/usr/bin/env python3
"""Exact threshold-compressed empirical ABC for a pathwise monotone epidemic."""
from __future__ import annotations
import json
import math
import random
import time
from collections import deque

NODES = 100
EDGE_PROB = 0.06
K = 513
BETA_MAX = 0.8
N_TAPES = 128
BETA_TRUE = 0.22
ABC_EPSILON = 3
BASE_SEED = 20261010


def make_graph(n: int, p: float, seed: int):
    rng = random.Random(seed)
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
    degree = [0] * n
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    root = max(range(n), key=lambda u: degree[u])
    return edges, root, degree


def make_tape(m: int, seed: int):
    rng = random.Random(seed)
    return [rng.random() for _ in range(m)]


def outbreak_size(edges, root: int, tape, beta: float, n: int, counter: dict):
    """SIR final size on a static graph: each edge transmits iff U_e <= beta."""
    adj = [[] for _ in range(n)]
    for (u, v), u_e in zip(edges, tape):
        counter["edge_checks"] += 1
        if u_e <= beta:
            adj[u].append(v)
            adj[v].append(u)
    seen = {root}
    queue = deque([root])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return len(seen)


def first_true_monotone(predicate, K_grid: int, evaluate):
    """First true grid index in {0,...,K_grid}; K_grid is an implicit true sentinel."""
    lo, hi = 0, K_grid
    calls = 0
    while lo < hi:
        mid = (lo + hi) // 2
        # Since lo < hi and hi <= K_grid, mid is always a real grid index.
        assert mid < K_grid
        calls += 1
        if predicate(evaluate(mid)):
            hi = mid
        else:
            lo = mid + 1
    return lo, calls


def dense_counts(edges, root, tapes, grid, low, high):
    counts = [0] * len(grid)
    counter = {"calls": 0, "edge_checks": 0}
    for tape in tapes:
        for j, beta in enumerate(grid):
            counter["calls"] += 1
            size = outbreak_size(edges, root, tape, beta, NODES, counter)
            if low <= size <= high:
                counts[j] += 1
    return counts, counter


def compressed_counts(edges, root, tapes, grid, low, high):
    counts = [0] * len(grid)
    counter = {"calls": 0, "edge_checks": 0, "max_calls_per_tape": 0,
               "max_calls_per_boundary": 0}
    max_boundary_calls = 0
    for tape in tapes:
        cache = {}

        def evaluate(j):
            if j not in cache:
                counter["calls"] += 1
                cache[j] = outbreak_size(edges, root, tape, grid[j], NODES, counter)
            return cache[j]

        left, left_calls = first_true_monotone(lambda size: size >= low, len(grid), evaluate)
        right, right_calls = first_true_monotone(lambda size: size > high, len(grid), evaluate)
        counter["max_calls_per_tape"] = max(counter["max_calls_per_tape"], len(cache))
        max_boundary_calls = max(max_boundary_calls, left_calls, right_calls)
        # Under pathwise monotonicity, ABC acceptance is exactly this half-open interval.
        if left < right:
            for j in range(left, right):
                counts[j] += 1
    counter["max_calls_per_boundary"] = max_boundary_calls
    return counts, counter


def normalize(counts):
    total = sum(counts)
    if total == 0:
        return None
    return [c / total for c in counts]


def first_mismatch(a, b):
    return next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), None)


def adversarial_nonmonotone_test():
    k = 101
    values = [1 if 20 <= j <= 30 else 0 for j in range(k)]
    low = high = 1
    dense = [int(low <= x <= high) for x in values]
    calls = 0

    def evaluate(j):
        nonlocal calls
        calls += 1
        return values[j]

    left, _ = first_true_monotone(lambda x: x >= low, k, evaluate)
    right, _ = first_true_monotone(lambda x: x > high, k, evaluate)
    compressed = [int(left <= j < right) for j in range(k)]
    return {
        "grid_points": k,
        "true_acceptance_indices": [j for j, x in enumerate(dense) if x],
        "compressed_interval": [left, right],
        "first_mismatch_index": first_mismatch(dense, compressed),
        "dense_accepted_points": sum(dense),
        "compressed_accepted_points": sum(compressed),
        "threshold_queries": calls,
        "result": "FAIL_CLOSED_CONTRACT_REQUIRED",
    }


def main():
    t0 = time.perf_counter()
    edges, root, degree = make_graph(NODES, EDGE_PROB, BASE_SEED)
    m = len(edges)
    grid = [BETA_MAX * j / (K - 1) for j in range(K)]
    tapes = [make_tape(m, BASE_SEED + 1 + r) for r in range(N_TAPES)]
    obs_tape = make_tape(m, BASE_SEED + 999999)
    obs_counter = {"edge_checks": 0}
    observed = outbreak_size(edges, root, obs_tape, BETA_TRUE, NODES, obs_counter)
    low = max(1, observed - ABC_EPSILON)
    high = observed + ABC_EPSILON

    td = time.perf_counter()
    dense, dense_cost = dense_counts(edges, root, tapes, grid, low, high)
    dense_seconds = time.perf_counter() - td
    tc = time.perf_counter()
    compressed, compressed_cost = compressed_counts(edges, root, tapes, grid, low, high)
    compressed_seconds = time.perf_counter() - tc

    assert dense == compressed
    assert dense_cost["calls"] == N_TAPES * K
    assert compressed_cost["calls"] <= 2 * N_TAPES * math.ceil(math.log2(K + 1))
    assert compressed_cost["max_calls_per_boundary"] <= math.ceil(math.log2(K + 1))
    assert sum(dense) > 0, "ABC event unexpectedly has zero support; adjust fixed experiment design."

    result = {
        "experiment": "paired-grid Monte Carlo versus threshold inversion, exact empirical ABC curve",
        "seed": BASE_SEED,
        "graph": {"nodes": NODES, "edges": m, "edge_probability": EDGE_PROB,
                  "index_case": root, "index_case_degree": degree[root]},
        "inference": {"grid_points": K, "beta_range": [0.0, BETA_MAX],
                      "tapes": N_TAPES, "observed_outbreak": observed,
                      "abc_epsilon": ABC_EPSILON, "accepted_size_interval": [low, high],
                      "nonzero_grid_points": sum(c > 0 for c in dense),
                      "total_grid_acceptances": sum(dense)},
        "dense": {**dense_cost, "seconds": round(dense_seconds, 6)},
        "threshold_inversion": {**compressed_cost, "seconds": round(compressed_seconds, 6)},
        "cost_comparison": {
            "call_reduction_factor": round(dense_cost["calls"] / compressed_cost["calls"], 4),
            "edge_check_reduction_factor": round(dense_cost["edge_checks"] / compressed_cost["edge_checks"], 4),
            "exact_count_vectors_equal": dense == compressed,
            "exact_posterior_vectors_equal": normalize(dense) == normalize(compressed),
            "tape_generation_uniforms_each_method": N_TAPES * m,
            "observation_simulation_edge_checks_each_method": obs_counter["edge_checks"],
            "theoretical_call_upper_bound": 2 * N_TAPES * math.ceil(math.log2(K + 1)),
        },
        "adversarial_nonmonotone": adversarial_nonmonotone_test(),
        "total_seconds": round(time.perf_counter() - t0, 6),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
