"""Independent finite checks of H-tree geometry and its exact hook recurrence.

The theorem is analytic; this checks the easily mis-indexed construction and
recurrence rather than treating finite-size numerics as an asymptotic proof.
"""
from collections import deque
from functools import lru_cache
from itertools import permutations
import json
import math
from pathlib import Path


@lru_cache(None)
def tree(h):
    if h == 0:
        return frozenset({(0, 0)}), frozenset()
    length = 2 ** (h - 1)
    vertices = {(0, 0)}
    edges = set()

    def edge(a, b):
        assert abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
        vertices.update((a, b))
        edges.add(tuple(sorted((a, b))))

    for sx in (-1, 1):
        for t in range(length):
            edge((sx*t, 0), (sx*(t+1), 0))
        for sy in (-1, 1):
            for t in range(length):
                edge((sx*length, sy*t), (sx*length, sy*(t+1)))
    child_vertices, child_edges = tree(h - 1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            root = (sx*length, sy*length)
            translate = lambda v: (v[0] + root[0], v[1] + root[1])
            moved = {translate(v) for v in child_vertices}
            assert vertices & moved == {root}
            vertices.update(moved)
            edges.update(tuple(sorted((translate(a), translate(b))))
                         for a, b in child_edges)
    return frozenset(vertices), frozenset(edges)


def inspect(h):
    vertices, edges = tree(h)
    graph = {v: [] for v in vertices}
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    parent = {(0, 0): None}
    order = [(0, 0)]
    for v in order:
        for w in graph[v]:
            if w == parent[v]:
                continue
            assert w not in parent
            parent[w] = v
            order.append(w)
    assert set(order) == set(vertices)
    assert len(edges) == len(vertices) - 1 == 3*(4**h - 2**h)
    assert max(map(len, graph.values())) <= 3
    assert {v for v in vertices if v[0] == 0} == {(0, 0)}
    side = 2**(h+1) - 1
    assert side**2 == (4*len(vertices) - 1)//3
    assert max(max(abs(x), abs(y)) for x, y in vertices) == 2**h - 1
    subtree = {}
    for v in reversed(order):
        subtree[v] = 1 + sum(subtree[w] for w in graph[v] if parent.get(w) == v)
    hook = math.prod(subtree[v] for v in vertices if v != (0, 0))
    assert hook <= 16**len(edges)
    return {
        'h': h, 'vertices': len(vertices), 'edges': len(edges),
        'bounding_square_sites': side**2,
        'max_degree': max(map(len, graph.values())),
        'log2_hook_per_edge': math.log2(hook)/len(edges),
        'hook': hook, 'parent': parent,
    }


def main():
    records = []
    old_hook = 1
    old_n = 1
    for h in range(1, 7):
        record = inspect(h)
        length = 2**(h - 1)
        predicted = (old_hook**4
                     * math.prod(old_n + t for t in range(length))**4
                     * math.prod(2*old_n + 2*length - 1 + t
                                 for t in range(length))**2)
        assert predicted == record['hook']
        if h == 1:
            parent = record['parent']
            rest = [v for v in parent if v != (0, 0)]
            count = 0
            for order in permutations(rest):
                rank = {(0, 0): -1, **{v: i for i, v in enumerate(order)}}
                count += all(rank[parent[v]] < rank[v] for v in rest)
            assert count == math.factorial(len(rest)) // record['hook'] == 80
            record['enumerated_activation_orders'] = count
        old_hook, old_n = record.pop('hook'), record['vertices']
        record.pop('parent')
        record['all_assertions_passed'] = True
        records.append(record)
    receipt = {'checks': records,
               'scope': 'Finite geometry, exact subtree-product recurrence, and h=1 hook order count only.'}
    destination = Path(__file__).with_name('planar_geometry_verification.json')
    destination.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
