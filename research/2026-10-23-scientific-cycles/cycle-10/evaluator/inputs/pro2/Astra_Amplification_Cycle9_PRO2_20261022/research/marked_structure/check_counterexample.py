"""Exact bounded check of the K2,3 marked-terminal failure.

No producer imports and no old closure replay. The all-size marked-root
statements are proved in PROOF.md, not inferred from this one graph.
"""
from pathlib import Path
import json
import time
import resource


def main():
    start = time.perf_counter()
    n, a, b, marked = 5, 0, 1, 2
    mids = [2, 3, 4]
    edges = [(hub, v) for hub in [a, b] for v in mids]
    edge_set = {tuple(sorted(e)) for e in edges}
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    assert len(adj[marked]) == 2 and max(map(len, adj)) == 3
    candidates = sorted(set(range(n)) - adj[marked] - {marked})
    assert candidates == [3, 4]
    excluded = []
    for other in candidates:
        third = next(v for v in mids if v not in (marked, other))
        path = [marked, a, third, b, other]
        assert len(set(path)) == len(path)
        assert all(tuple(sorted(e)) in edge_set for e in zip(path, path[1:]))
        chords = [[u, v] for i, u in enumerate(path)
                  for v in path[i + 2:]
                  if tuple(sorted((u, v))) in edge_set]
        assert sorted(map(sorted, chords)) == sorted([[a, other], [b, marked]])
        excluded.append({"candidate_second_terminal": other,
                         "simple_noninduced_terminal_path": path,
                         "chords": chords})

    def connected_after(removed):
        allowed = set(range(n)) - {removed}
        seen, stack = {min(allowed)}, [min(allowed)]
        while stack:
            v = stack.pop()
            for w in adj[v] & (allowed - seen):
                seen.add(w)
                stack.append(w)
        return seen == allowed

    assert all(connected_after(v) for v in range(n))
    bags = [[a, b, mid] for mid in mids]
    assert all(any(u in bag and v in bag for bag in bags) for u, v in edges)
    for v in range(n):
        indices = [i for i, bag in enumerate(bags) if v in bag]
        assert indices == list(range(min(indices), max(indices) + 1))

    # H=G-marked is exactly the two-path module; P(path2(marked),H) is G.
    h_edges = [(hub, v) for hub in [a, b] for v in mids if v != marked]
    marked_path_edges = [(a, marked), (marked, b)]
    assert ({tuple(sorted(e)) for e in h_edges + marked_path_edges} == edge_set)
    result = {
        "schema": "astra-cycle9-marked-structure-counterexample/v1",
        "graph": {"n": n, "edges": sorted(edge_set),
                  "width_two_bags": bags, "bag_tree_edges": [[0, 1], [1, 2]]},
        "marked_degree_two_vertex": marked,
        "all_nonadjacent_terminal_candidates_excluded": excluded,
        "correct_marked_midpoint_representation": {
            "terminals": [a, b], "marked_path": [a, marked, b],
            "H_edges": sorted(tuple(sorted(e)) for e in h_edges),
            "H_terminal_loads": [2, 2],
            "H_expression": {"op": "P", "paths": [[a, 3, b], [a, 4, b]]}},
        "degree_three_terminal_example": {"marked": a, "other_terminal": b,
                                           "branches": [[a, v, b] for v in mids]},
        "passed": True,
        "wall_seconds_body": time.perf_counter() - start,
        "process_max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "scope": "One exact counterexample and its repaired representation; all-size statements are analytical."}
    Path(__file__).with_name("RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in
                      ["passed", "wall_seconds_body", "process_max_rss_kib"]}))


if __name__ == "__main__":
    main()
