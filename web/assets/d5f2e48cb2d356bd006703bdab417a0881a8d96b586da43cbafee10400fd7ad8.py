"""Exact finite ledgers supporting frontier_geometry.md.

These checks are not proofs of any release theorem or of a universal bound.
They verify the graph distances used in the analytic diamond construction
and the exact numerical matrix printed in the Gepner manuscript.
"""

from fractions import Fraction as Q
from heapq import heappop, heappush
from pathlib import Path
import json
import time


def diamond(k):
    edges = [(0, 1, Q(1))]
    next_vertex = 2
    anti = []
    for level in range(1, k + 1):
        new_edges, layer = [], []
        for u, v, length in edges:
            a, b = next_vertex, next_vertex + 1
            next_vertex += 2
            half = length / 2
            new_edges.extend([(u, a, half), (a, v, half),
                              (u, b, half), (b, v, half)])
            layer.append((a, b, length))
        anti.append(layer)
        edges = new_edges
    graph = [[] for _ in range(next_vertex)]
    for u, v, length in edges:
        graph[u].append((v, length))
        graph[v].append((u, length))
    return graph, edges, anti


def distance(graph, source, target):
    dist = {source: Q(0)}
    queue = [(Q(0), source)]
    while queue:
        cost, v = heappop(queue)
        if cost != dist[v]:
            continue
        if v == target:
            return cost
        for w, length in graph[v]:
            candidate = cost + length
            if w not in dist or candidate < dist[w]:
                dist[w] = candidate
                heappush(queue, (candidate, w))
    raise AssertionError("disconnected graph")


def mul(a, b):
    return [[sum(a[i][s] * b[s][j] for s in range(4))
             for j in range(4)] for i in range(4)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def det(a):
    a = [row[:] for row in a]
    answer = Q(1)
    for i in range(4):
        pivot = next((j for j in range(i, 4) if a[j][i]), None)
        if pivot is None:
            return Q(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            answer = -answer
        pivot_value = a[i][i]
        answer *= pivot_value
        for j in range(i + 1, 4):
            scale = a[j][i] / pivot_value
            a[j] = [x - scale * y for x, y in zip(a[j], a[i])]
    return answer


def main():
    started = time.perf_counter()
    result = {"scope": "Finite exact graph and numerical-algebra ledgers only",
              "diamond": []}
    for k in range(1, 6):
        graph, edges, anti = diamond(k)
        assert len(graph) == 2 * (4 ** k + 2) // 3
        assert len(edges) == 4 ** k
        assert distance(graph, 0, 1) == 1
        assert sum(length * length for _, _, length in edges) == 1
        witnesses = 1
        for j, layer in enumerate(anti, 1):
            assert len(layer) == 4 ** (j - 1)
            assert sum(length * length for _, _, length in layer) == 1
            for u, v, length in layer:
                assert length == Q(1, 2 ** (j - 1))
                assert distance(graph, u, v) == length
                witnesses += 1
        result["diamond"].append({"level": k, "vertices": len(graph),
                                  "final_edges": len(edges),
                                  "exact_distance_checks": witnesses,
                                  "final_squared_edge_length_sum": "1",
                                  "each_anti_layer_squared_length_sum": "1"})
    M = [[Q(-4), Q(-20, 3), Q(-5), Q(-5)],
         [Q(1), Q(1), Q(0), Q(0)],
         [Q(1, 2), Q(1), Q(1), Q(0)],
         [Q(1, 6), Q(1, 2), Q(1), Q(1)]]
    I = [[Q(i == j) for j in range(4)] for i in range(4)]
    powers = [I]
    for _ in range(5):
        powers.append(mul(powers[-1], M))
    assert powers[5] == I
    assert all(sum(powers[h][i][j] for h in range(5)) == 0
               for i in range(4) for j in range(4))
    J = [[Q(0), Q(25, 6), Q(0), Q(5)],
         [Q(-25, 6), Q(0), Q(-5), Q(0)],
         [Q(0), Q(5), Q(0), Q(0)],
         [Q(-5), Q(0), Q(0), Q(0)]]
    assert det(J) == 625
    assert mul(mul(transpose(M), J), M) == J
    line_classes = [[Q(1), Q(t), Q(t*t, 2), Q(t*t*t, 6)]
                    for t in range(4)]
    assert det(line_classes) == 1
    result["gepner_numeric"] = {
        "M_fifth_power_identity": True,
        "cyclotomic_polynomial_annihilates_M": True,
        "Euler_form_preserved": True,
        "Euler_form_determinant": "625",
        "four_line_class_determinant": "1",
        "categorical_grid_support_or_HN_claim_verified": False}
    result["body_seconds"] = time.perf_counter() - started
    result["status"] = "PASS"
    output = Path(__file__).with_name("frontier_geometry_checks.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
