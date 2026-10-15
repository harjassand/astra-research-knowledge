#!/usr/bin/env python3
"""Independent finite graph checks for temporary clearance routing.

No third-party dependencies. These checks are fixtures, not a universal proof.
See REPORT.md for the proofs and physical limitations.
"""
import argparse
import itertools
import json
from collections import defaultdict, deque
from fractions import Fraction
from pathlib import Path


def adjacency(n, edges):
    a = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        a[u].append((v, i))
        a[v].append((u, i))
    return a


def connected(n, edges):
    a = adjacency(n, edges)
    seen = {0}
    stack = [0]
    while stack:
        for v, _ in a[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def odd_vertices(n, edges):
    d = [0] * n
    for u, v in edges:
        d[u] ^= 1
        d[v] ^= 1
    return {v for v, p in enumerate(d) if p}


def simple_paths(n, edges, s, t):
    a = adjacency(n, edges)
    out = []

    def visit(v, seen, path):
        if v == t:
            out.append(tuple(path))
            return
        for w, e in a[v]:
            if w not in seen:
                visit(w, seen | {w}, path + [e])

    visit(s, {s}, [])
    return out


def accessible_by_paths(n, edges, s, t):
    return {e for p in simple_paths(n, edges, s, t) for e in p}


def biconnected_blocks(n, edges):
    """Tarjan edge blocks; a bridge is a one-edge block."""
    a = adjacency(n, edges)
    disc = [-1] * n
    low = [0] * n
    stack = []
    blocks = []
    clock = 0

    def dfs(u, parent_edge):
        nonlocal clock
        disc[u] = low[u] = clock
        clock += 1
        for v, e in a[u]:
            if e == parent_edge:
                continue
            if disc[v] < 0:
                stack.append(e)
                dfs(v, e)
                low[u] = min(low[u], low[v])
                if low[v] >= disc[u]:
                    block = set()
                    while True:
                        j = stack.pop()
                        block.add(j)
                        if j == e:
                            break
                    blocks.append(block)
            elif disc[v] < disc[u]:
                stack.append(e)
                low[u] = min(low[u], disc[v])

    for v in range(n):
        if disc[v] < 0:
            dfs(v, -1)
    assert not stack
    return blocks


def accessible_by_block_tree(n, edges, s, t):
    blocks = biconnected_blocks(n, edges)
    tree = defaultdict(list)
    # Keep all original vertices in the incidence tree, including non-cut leaves.
    for b, block in enumerate(blocks):
        vertices = {v for e in block for v in edges[e]}
        for v in vertices:
            tree[("b", b)].append(("v", v))
            tree[("v", v)].append(("b", b))
    start, goal = ("v", s), ("v", t)
    parent = {start: None}
    queue = deque([start])
    while queue and goal not in parent:
        v = queue.popleft()
        for w in tree[v]:
            if w not in parent:
                parent[w] = v
                queue.append(w)
    if goal not in parent:
        return set()
    path_blocks = []
    v = goal
    while v is not None:
        if v[0] == "b":
            path_blocks.append(v[1])
        v = parent[v]
    return {e for b in path_blocks for e in blocks[b]}


def tree_t_join(n, edges, targets):
    """A T-join contained in an arbitrary spanning tree, in linear time."""
    a = adjacency(n, edges)
    parent = {0: None}
    parent_edge = {}
    order = [0]
    for u in order:
        for v, e in a[u]:
            if v not in parent:
                parent[v] = u
                parent_edge[v] = e
                order.append(v)
    assert len(order) == n
    need = [v in targets for v in range(n)]
    result = set()
    for v in reversed(order[1:]):
        if need[v]:
            result.add(parent_edge[v])
            need[parent[v]] ^= True
    assert not need[0]
    return result


def minimum_t_join_brute(n, edges, targets, weights=None):
    weights = weights or [1] * len(edges)
    best = None
    for mask in range(1 << len(edges)):
        selected = [e for e in range(len(edges)) if mask >> e & 1]
        cost = sum(weights[e] for e in selected)
        if best is not None and cost > best[0]:
            continue
        if odd_vertices(n, [edges[e] for e in selected]) == targets:
            key = (cost, selected)
            if best is None or key < best:
                best = key
    assert best is not None
    return set(best[1])


def euler_trail(n, edges, s):
    a = adjacency(n, edges)
    used = [False] * len(edges)
    vertices, incoming = [s], []
    out_vertices, out_edges = [], []
    while vertices:
        v = vertices[-1]
        while a[v] and used[a[v][-1][1]]:
            a[v].pop()
        if a[v]:
            w, e = a[v].pop()
            used[e] = True
            vertices.append(w)
            incoming.append(e)
        else:
            out_vertices.append(vertices.pop())
            if incoming:
                out_edges.append(incoming.pop())
    assert all(used)
    return list(reversed(out_vertices)), list(reversed(out_edges))


def route(n, edges, s, t, duplicate=None):
    targets = odd_vertices(n, edges) ^ {s, t}
    if duplicate is None:
        duplicate = tree_t_join(n, edges, targets)
    lanes = list(edges) + [edges[e] for e in sorted(duplicate)]
    originals = list(range(len(edges))) + sorted(duplicate)
    assert odd_vertices(n, lanes) == {s, t}
    vertices, lane_ids = euler_trail(n, lanes, s)
    assert vertices[0] == s and vertices[-1] == t
    assert len(lane_ids) == len(lanes)
    assert len(set(lane_ids)) == len(lanes)
    for i, e in enumerate(lane_ids):
        assert {vertices[i], vertices[i + 1]} == set(lanes[e])
    return {
        "targets": sorted(targets),
        "duplicated_edges": sorted(duplicate),
        "vertices": vertices,
        "lane_ids": lane_ids,
        "original_edge_ids": [originals[e] for e in lane_ids],
    }


def exact_pressures(n, edges, s, t):
    """Unit-resistance network, exact rational Dirichlet solution.

    Detached components receive zero pressure; they have zero edge flow.
    """
    a = adjacency(n, edges)
    seen = {s}
    queue = [s]
    for u in queue:
        for v, _ in a[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    if t not in seen:
        return None
    interior = [v for v in seen if v not in {s, t}]
    idx = {v: i for i, v in enumerate(interior)}
    m = len(interior)
    matrix = [[Fraction(0) for _ in range(m + 1)] for _ in range(m)]
    for u in interior:
        i = idx[u]
        matrix[i][i] = len(a[u])
        for v, _ in a[u]:
            if v == s:
                matrix[i][-1] += 1
            elif v in idx:
                matrix[i][idx[v]] -= 1
    for k in range(m):
        pivot = next(i for i in range(k, m) if matrix[i][k])
        matrix[k], matrix[pivot] = matrix[pivot], matrix[k]
        z = matrix[k][k]
        matrix[k] = [x / z for x in matrix[k]]
        for i in range(m):
            if i == k:
                continue
            z = matrix[i][k]
            matrix[i] = [x - z * y for x, y in zip(matrix[i], matrix[k])]
    p = [Fraction(0)] * n
    p[s] = Fraction(1)
    for v, i in idx.items():
        p[v] = matrix[i][-1]
    q = [p[u] - p[v] for u, v in edges]
    return p, q


def example(n, edges, names, s, t):
    duplicate = minimum_t_join_brute(n, edges, odd_vertices(n, edges) ^ {s, t})
    routed = route(n, edges, s, t, duplicate)
    p, q = exact_pressures(n, edges, s, t)
    return {
        "names": names,
        "edges": [[names[u], names[v]] for u, v in edges],
        "odd_vertices": [names[v] for v in sorted(odd_vertices(n, edges))],
        "steady_pressures": {names[v]: str(p[v]) for v in range(n)},
        "steady_edge_flows": [str(x) for x in q],
        "accessible_edge_ids": sorted(accessible_by_paths(n, edges, s, t)),
        "route": routed,
        "named_trail": [names[v] for v in routed["vertices"]],
    }


def exhaustive(max_n):
    counts = {}
    for n in range(2, max_n + 1):
        pairs = list(itertools.combinations(range(n), 2))
        count = 0
        paths = 0
        for mask in range(1 << len(pairs)):
            if mask.bit_count() < n - 1:
                continue
            edges = [p for e, p in enumerate(pairs) if mask >> e & 1]
            if not connected(n, edges):
                continue
            count += 1
            a = accessible_by_paths(n, edges, 0, n - 1)
            b = accessible_by_block_tree(n, edges, 0, n - 1)
            assert a == b, (n, edges, a, b)
            route(n, edges, 0, n - 1)
            paths += len(simple_paths(n, edges, 0, n - 1))
        counts[str(n)] = {"connected_labeled_graphs": count, "simple_st_paths": paths}
    return counts


def all_deletions_check(n=5):
    """For every graph on n fixed labels, union exact flowing edges over deletions.

    One exact solve per subgraph of K_n. A subset zeta transform unions the
    nonzero-flow witness masks over all possible deletion states of each graph.
    """
    pairs = list(itertools.combinations(range(n), 2))
    total = 1 << len(pairs)
    flowing = [0] * total
    solves = 0
    for mask in range(total):
        ids = [i for i in range(len(pairs)) if mask >> i & 1]
        edges = [pairs[i] for i in ids]
        result = exact_pressures(n, edges, 0, n - 1)
        if result is not None:
            solves += 1
            _, q = result
            flowing[mask] = sum(1 << ids[i] for i, x in enumerate(q) if x)
    for bit in range(len(pairs)):
        for mask in range(total):
            if mask >> bit & 1:
                flowing[mask] |= flowing[mask ^ (1 << bit)]
    for mask in range(total):
        ids = [i for i in range(len(pairs)) if mask >> i & 1]
        edges = [pairs[i] for i in ids]
        expected = sum(1 << ids[i] for i in accessible_by_paths(n, edges, 0, n - 1))
        assert flowing[mask] == expected, (mask, flowing[mask], expected)
    return {"n": n, "all_graph_masks": total, "exact_rational_solves": solves,
            "mismatches": 0, "resistances": "all edges 1; terminal pressures 1,0"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=6)
    parser.add_argument("--output", default="graph_certificate.json")
    args = parser.parse_args()
    result = {
        "scope": "finite internal fixture checks; no physical or novelty evidence",
        "universal_route_and_block_path_checks": exhaustive(args.max_n),
        "all_edge_deletion_flux_check": all_deletions_check(),
        "wheatstone": example(4, [(0, 1), (1, 3), (0, 2), (2, 3), (1, 2)],
                               ["A", "B", "C", "D"], 0, 3),
        "blind_branch": example(4, [(0, 1), (1, 2), (1, 3)],
                                 ["s", "v", "t", "cap"], 0, 2),
        "lollipop": example(5, [(0, 1), (1, 2), (1, 3), (3, 4), (4, 1)],
                              ["s", "v", "t", "b", "c"], 0, 2),
        "mismatches": 0,
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": args.output, "counts": result["universal_route_and_block_path_checks"],
                      "all_deletions": result["all_edge_deletion_flux_check"], "mismatches": 0}, indent=2))


if __name__ == "__main__":
    main()
