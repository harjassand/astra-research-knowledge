"""Finite diagnostic for the stage-incidence identity; not a general proof."""
import itertools
import json
from collections import Counter
from pathlib import Path


def walks(edges, max_length, closed):
    adjacency = {}
    for u, v in edges:
        adjacency.setdefault(u, []).append(v)
        adjacency.setdefault(v, []).append(u)
    answer = []

    def extend(path):
        h = len(path) - 1
        if h:
            if not closed or (path[-1] == path[0] and h >= 3 and path[-2] != path[1]):
                answer.append(tuple(path))
        if h == max_length:
            return
        for next_vertex in adjacency[path[-1]]:
            if h and next_vertex == path[-2]:
                continue
            extend(path + [next_vertex])

    for start in adjacency:
        extend([start])
    return answer


def audit(system, iota):
    multiplicity = Counter()
    endpoints = Counter()
    for path, is_interval in system:
        for u, v in zip(path, path[1:]):
            multiplicity[tuple(sorted((u, v)))] += 1
        if is_interval:
            endpoints[path[0]] += 1
            endpoints[path[-1]] += 1
    incident = {}
    for (u, v), count in multiplicity.items():
        incident.setdefault(u, []).append(count)
        incident.setdefault(v, []).append(count)
    for vertex, counts in incident.items():
        assert 2 * max(counts) <= sum(counts) + endpoints[vertex]
    total_h = sum(multiplicity.values())
    stage_edges = []
    stage_vertices = []
    for stage in range(1, max(multiplicity.values()) + 1):
        active = [edge for edge, count in multiplicity.items() if count >= stage]
        vertices = set(itertools.chain.from_iterable(active))
        stage_edges.append(len(active))
        stage_vertices.append(len(vertices))
    assert sum(stage_edges) == total_h
    assert sum(stage_vertices) <= total_h + iota
    assert sum(v - e for v, e in zip(stage_vertices, stage_edges)) - iota <= 0


graphs = {
    "path4": [(0, 1), (1, 2), (2, 3)],
    "triangle": [(0, 1), (1, 2), (2, 0)],
    "square_diagonal": [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)],
    "K4": list(itertools.combinations(range(4), 2)),
    "lollipop": [(0, 1), (1, 2), (2, 3), (3, 1)],
}
results = {}
for name, edges in graphs.items():
    cycles = walks(edges, 6, True)
    intervals = walks(edges, 6, False)
    number = 0
    for path in cycles:
        audit([(path, False)], 0)
        number += 1
    for left, right in itertools.combinations_with_replacement(cycles, 2):
        audit([(left, False), (right, False)], 0)
        number += 1
    for path in intervals:
        audit([(path, True)], 1)
        number += 1
    for path in intervals:
        for cycle in cycles:
            audit([(path, True), (cycle, False)], 1)
            number += 1
    results[name] = {"closed_paths": len(cycles), "interval_paths": len(intervals), "systems": number}
payload = {"status": "no finite counterexample", "graphs": results, "total_systems": sum(r["systems"] for r in results.values()), "scope": "One or two cyclically immersed closed paths, or one immersed interval with zero or one closed path, individual length at most six, on listed loopless simple graphs. This does not certify the general theorem."}
destination = Path(__file__).with_name("incidence_diagnostic.json")
destination.write_text(json.dumps(payload, indent=2) + "\n")
print(json.dumps(payload, indent=2))
