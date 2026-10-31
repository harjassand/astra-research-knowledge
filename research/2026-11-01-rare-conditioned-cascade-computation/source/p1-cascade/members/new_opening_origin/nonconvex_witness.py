"""Exact rational witnesses against generic convex integration shortcuts.

Run directly.  No numerical CTMC approximations are used.  The simulator advances
piecewise-constant cumulative exposures and handles simultaneous events exactly.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
import math


@dataclass(frozen=True)
class Node:
    parents: tuple[int, ...]
    rates: tuple[F, ...]

    def rate(self, active: list[bool]) -> F:
        index = sum(int(active[j]) << k for k, j in enumerate(self.parents))
        return self.rates[index]


def event_times(nodes: list[Node], thresholds: tuple[F, ...]):
    n = len(nodes)
    active = [False] * n
    remaining = list(thresholds)
    times = [None] * n
    time = F(0)
    while not all(active):
        rates = [F(0) if active[i] else nodes[i].rate(active) for i in range(n)]
        waits = [remaining[i] / rates[i] for i in range(n) if rates[i] > 0]
        if not waits:
            return times
        dt = min(waits)
        time += dt
        for i in range(n):
            if not active[i]:
                remaining[i] -= rates[i] * dt
        new = [i for i in range(n) if not active[i] and remaining[i] == 0]
        assert new
        for i in new:
            active[i] = True
            times[i] = time
    return times


def build_family(m: int):
    assert m >= 1 and m & (m - 1) == 0
    nodes: list[Node] = []
    bags: list[tuple[int, ...]] = []
    bag_edges: list[tuple[int, int]] = []
    current = []
    owner = {}
    for j in range(m):
        a, b, c = 3 * j, 3 * j + 1, 3 * j + 2
        # c -> a is monotone feedback. It changes no pre-c firing time.
        nodes.extend([
            Node((c,), (F(1), F(2))),
            Node((), (F(1),)),
            Node((a, b), (F(0), F(1), F(1), F(1))),
        ])
        owner[c] = len(bags)
        bags.append((a, b, c))
        current.append(c)
    while len(current) > 1:
        next_level = []
        for left, right in zip(current[::2], current[1::2]):
            root = len(nodes)
            nodes.append(Node((left, right), (F(0), F(0), F(0), F(1))))
            bag_id = len(bags)
            bags.append((left, right, root))
            bag_edges.extend([(bag_id, owner[left]), (bag_id, owner[right])])
            owner[root] = bag_id
            next_level.append(root)
        current = next_level
    depth = m.bit_length() - 1
    gate_threshold = F(1, 8 * max(1, depth))
    witnesses = []
    for choices in product((0, 1), repeat=m):
        values = []
        for choice in choices:
            values.extend((F(1, 4), F(7, 4), F(1, 4)) if choice == 0
                          else (F(7, 4), F(1, 4), F(1, 4)))
        values.extend([gate_threshold] * (m - 1))
        witnesses.append(tuple(values))
    return nodes, current[0], bags, bag_edges, witnesses


def check_width_two(nodes, bags, edges):
    assert all(len(bag) <= 3 for bag in bags)
    assert len(edges) == len(bags) - 1
    adjacency = [set() for _ in bags]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    for i, node in enumerate(nodes):
        scope = {i, *node.parents}
        assert any(scope.issubset(bag) for bag in bags)
        occurrences = {j for j, bag in enumerate(bags) if i in bag}
        visited = set()
        stack = [next(iter(occurrences))]
        while stack:
            j = stack.pop()
            if j not in visited:
                visited.add(j)
                stack.extend((adjacency[j] & occurrences) - visited)
        assert visited == occurrences


def main():
    rows = []
    for m in (1, 2, 4):
        nodes, target, bags, edges, witnesses = build_family(m)
        check_width_two(nodes, bags, edges)
        successful_times = [event_times(nodes, w)[target] for w in witnesses]
        assert all(t is not None and t < 1 for t in successful_times)
        midpoint_times = []
        for u, v in combinations(witnesses, 2):
            midpoint = tuple((a + b) / 2 for a, b in zip(u, v))
            t = event_times(nodes, midpoint)[target]
            assert t is not None and t > 1
            midpoint_times.append(t)
        rows.append({
            "or_gadgets": m,
            "sites": len(nodes),
            "moral_treewidth_certificate": 2,
            "successful_witnesses": len(witnesses),
            "all_pair_midpoints_checked": len(midpoint_times),
            "latest_success_time": str(max(successful_times)),
            "earliest_midpoint_time": str(min(midpoint_times)),
            "cyclic_hazard_graph": True,
        })
    # Ordinary Exp-CDF uniformization also leaves a nonconvex success region.
    uniform_u = (0.1, 0.99, 0.5)
    uniform_v = (0.99, 0.1, 0.5)
    uniform_mid = tuple((a + b) / 2 for a, b in zip(uniform_u, uniform_v))
    def output_time_uniform(z):
        e = [-math.log1p(-x) for x in z]
        return min(e[0], e[1]) + e[2]
    uniform = {
        "point_u_time": output_time_uniform(uniform_u),
        "point_v_time": output_time_uniform(uniform_v),
        "midpoint_time": output_time_uniform(uniform_mid),
    }
    assert uniform["point_u_time"] < 1 < uniform["midpoint_time"]
    result = {"exact_rational_checks": rows, "cdf_uniformization_check": uniform}
    path = Path(__file__).with_name("nonconvex_witness_results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
