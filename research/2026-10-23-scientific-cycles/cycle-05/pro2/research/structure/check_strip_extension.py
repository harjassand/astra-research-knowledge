"""Bounded exact diagnostic for the new boundary extension, not an old replay."""
import json
import argparse
import resource
import time
from pathlib import Path
from itertools import combinations
from strip_extension import (PAIRS, TRANSITIONS, extend_strip, square_edges,
                             reduce_long_strips, extend_reduced_coloring)


def components(vertices, edges, colors):
    vertices = list(vertices)
    edges = list(edges)
    assert all(colors[u] != colors[v] for u, v in edges)
    result = []
    for pair in combinations(range(4), 2):
        selected = {v for v in vertices if colors[v] in pair}
        adj = {v: [] for v in selected}
        for u, v in edges:
            if u in selected and v in selected:
                adj[u].append(v); adj[v].append(u)
        while selected:
            root = min(selected)
            stack = [root]; seen = {root}; selected.remove(root)
            total_degree = 0
            while stack:
                u = stack.pop(); total_degree += len(adj[u])
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v); selected.remove(v); stack.append(v)
            assert total_degree == 2 * (len(seen) - 1), "bichromatic cycle"
            result.append((pair, seen))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('RESULT.json'))
    args = parser.parse_args()
    wall, cpu = time.perf_counter(), time.process_time()
    records = []
    for (left, right), word in sorted(TRANSITIONS.items()):
        whole = left + word
        assert len(word) == 6 and whole[-2:] == right
        assert all(len(set(whole[i:i+3])) == 3 for i in range(6))
        records.append({"start": left, "end": right, "appended": word})
    assert len(records) == 144
    maximum = 0
    tests = 0
    # All end states, all nine core-length residues.  Proof covers unbounded n.
    for n in range(30, 39):
        edges = square_edges(n)
        for left in PAIRS:
            for right in PAIRS:
                word = extend_strip(n, left, right)
                cc = components(range(n), edges, dict(enumerate(word)))
                maximum = max(maximum, max(map(lambda t: len(t[1]), cc)))
                assert all(len(vs) <= 16 for pair, vs in cc)
                assert all(not(vs & {0, 1} and vs & {n-2, n-1}) for pair, vs in cc)
                tests += 1
    # New receiving fixture: two long triangle strips joined through a square.
    # The square has vertices 0,1,61,60; strip1 starts 0,1 and strip2 starts60,61.
    n1, n2 = 60, 39
    order1 = list(range(n1))
    order2 = list(range(n1, n1+n2))
    edges = square_edges(n1) + [(n1+i, n1+j) for i, j in square_edges(n2)]
    edges += [(0, 60), (1, 61)]
    vertices = list(range(n1+n2))
    kept, reduced_edges, orders = reduce_long_strips(vertices, edges)
    assert len(orders) == 2 and len(kept) == 8
    colors = {0: 0, 1: 1, 58: 2, 59: 3, 60: 2, 61: 3, 97: 0, 98: 2}
    before = components(kept, reduced_edges, colors)
    k = max(len(vs) for _, vs in before)
    final = extend_reduced_coloring(colors, orders)
    after = components(vertices, edges, final)
    k_after = max(len(vs) for _, vs in after)
    assert k_after <= 65*k
    fixture = {"vertices": vertices, "edges": edges, "reduced_vertices": kept,
               "reduced_edges": reduced_edges, "strip_orders": orders,
               "reduced_colors": sorted(colors.items()), "colors": sorted(final.items()),
               "reduced_max_component": k, "extended_max_component": k_after}
    report = {"status": "PASS", "exact_transition_count": 144,
              "end_pair_and_core_residue_tests": tests,
              "maximum_component_observed": maximum, "fixture": fixture,
              "transition_certificate": records,
              "scope": "finite exact diagnostics; all-size extension proof is PROOF.md",
              "body_wall_seconds": time.perf_counter()-wall,
              "body_cpu_seconds": time.process_time()-cpu,
              "maxrss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024}
    path = args.output
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('fixture','transition_certificate')}, indent=2))


if __name__ == '__main__':
    main()
