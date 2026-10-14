#!/usr/bin/env python3
"""Exact independent checks of the fixed-total-mass CLIQUE reduction."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from hashlib import sha256
import json
import random
import time

from independent_audit import check_spd, invert, quad

BASE = Path(__file__).resolve().parent


def one_graph(n, edges):
    degree = [0] * n
    B = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, j in edges:
        B[i][j] = B[j][i] = F(1)
        degree[i] += 1
        degree[j] += 1
    for i in range(n):
        B[i][i] = F(n) - F(2, 3) * degree[i]
    eps = F(1, 256 * n ** 3)
    A = [[F(int(i == j)) - eps * B[i][j] for j in range(n)] for i in range(n)]
    G = invert(A)
    check_spd(A)
    check_spd(G)
    assert all(v >= 0 for row in G for v in row)
    assert all(A[i][j] <= 0 for i in range(n) for j in range(n) if i != j)
    killing = [sum(row, F(0)) for row in A]
    assert all(x > 0 for x in killing)
    assert killing == [1 - eps * (n + F(d, 3)) for d in degree]
    assert all(sum(row, F(0)) < 2 * n for row in B)
    C = F(n * n) + F(2 * len(edges), 3)
    assert C == sum((sum(row, F(0)) for row in B), F(0))
    tail_bound = F(16 * n ** 3) * eps ** 2 / (1 - 2 * n * eps)
    assert tail_bound / eps <= F(8, 127) < F(1, 4)
    edge_set = set(edges)
    rows = []
    count = 0
    for k in range(1, n):
        values = []
        base = F(n + 3 * k) + eps * (C + 3 * n * k)
        for S in combinations(range(n), k):
            selected = set(S)
            e = sum(i in selected and j in selected for i, j in edge_set)
            s = [F(1 + (i in selected)) for i in range(n)]
            assert sum(s) == n + k
            assert quad(B, s) == C + 3 * n * k + 2 * e
            q = quad(G, s)
            tail = q - base - 2 * eps * e
            assert 0 <= tail <= tail_bound
            values.append((q, e, S, tail))
            count += 1
        qstar, es, Sstar, tail = max(values)
        emax = max(e for _, e, _, _ in values)
        assert es == emax
        recovered = (qstar - base) // (2 * eps)
        assert recovered == emax
        # Use two signed admissible perturbations, each below eps/4.
        for error in (F(-1, 8), F(0), F(1, 8)):
            q_approx = qstar + error * eps
            recovered_approx = (q_approx - base + eps / 2) // (2 * eps)
            assert recovered_approx == emax
        clique_target = k * (k - 1) // 2
        decision_threshold = base + 2 * eps * clique_target - eps / 2
        assert (qstar > decision_threshold) == (emax == clique_target)
        rows.append({"n": n, "k": k, "edges": len(edges), "maximum_induced_edges": emax,
                     "exact_optimal_ratio": str(qstar / (n + k)),
                     "optimal_selected_vertices": list(Sstar),
                     "maximum_allowed_ratio_error": str(eps / (4 * (n + k))),
                     "tail_at_optimum": str(tail), "tail_bound": str(tail_bound)})
    return rows, count


def main():
    start = time.time()
    rows, graphs, vertices = [], 0, 0
    # Exhaustive labelled graphs up to four vertices, followed by seeded cases.
    for n in range(1, 5):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            edges = [pair for bit, pair in enumerate(pairs) if mask & (1 << bit)]
            r, count = one_graph(n, edges)
            rows.extend(r)
            graphs += 1
            vertices += count
    rng = random.Random(20261014)
    for n in range(5, 9):
        for case in range(8):
            edges = [pair for pair in combinations(range(n), 2) if rng.randrange(3) == 0]
            r, count = one_graph(n, edges)
            rows.extend(r)
            graphs += 1
            vertices += count
    report = {"status": "PASS", "scope": "finite exact checks of an independently derived reduction; not a proof-assistant proof",
              "graphs": graphs, "graph_k_instances": len(rows), "hypersimplex_vertices": vertices,
              "rational_precision_recovery_checks": 3 * len(rows),
              "elapsed_seconds": time.time() - start, "results": rows,
              "code_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}
    out = BASE / "CORRELATED_SOURCE_RESULTS.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "results"}, indent=2))


if __name__ == "__main__":
    main()
