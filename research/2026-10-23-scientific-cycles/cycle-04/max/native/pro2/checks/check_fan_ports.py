#!/usr/bin/env python3
"""Exact local-port identities and a replicated-fan cancellation witness.

This check supplements the proof in notes/fan_port_lemma.md.  No eigensolver,
approximate arithmetic, original benchmark, or all-design inference is used.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import resource
import time


def graph_and_seed(copies):
    # Vertices 0=a, 1=u, 2=v. Each attached fan has a three-vertex path.
    colors = [0, 1, 2]
    edges = {(0, 1), (0, 2), (1, 2)}
    fans = [(0, (1, 2))]
    selected = {1: [], 2: []}
    for apex, palette in ((1, (2, 3, 4)), (2, (1, 3, 4))):
        for _ in range(copies):
            path = tuple(range(len(colors), len(colors) + 3))
            colors.extend(palette)
            fans.append((apex, path))
            selected[apex].append(path[0])
            edges.update((apex, v) for v in path)
            edges.update(zip(path, path[1:]))
    return colors, edges, fans, selected


def action(colors, coefficients):
    result = [[F(0) for _ in range(5)] for _ in colors]
    for (i, j), value in coefficients.items():
        result[i][colors[j]] += value
        if i != j:
            result[j][colors[i]] += value
    return result


def check(copies):
    colors, edges, fans, selected = graph_and_seed(copies)
    n = len(colors)
    assert n == 3 + 6 * copies
    assert len(edges) == 3 + 10 * copies
    assert all(0 <= c < 5 for c in colors)  # Each query row is exactly e_c.
    d = {(1, 2): F(1)}
    for apex in (1, 2):
        d.update({(apex, v): F(-1, copies) for v in selected[apex]})
    assert all(ij in edges for ij in d)
    y = action(colors, d)
    assert all(t == 0 for t in y[0] + y[1] + y[2])
    expected = {(v, colors[apex]): F(-1, copies)
                for apex in (1, 2) for v in selected[apex]}
    assert {(i, j): t for i, row in enumerate(y) for j, t in enumerate(row)
            if t} == expected
    norm2 = sum(t*t for row in y for t in row)
    assert norm2 == F(2, copies)
    # ||D||_2 >= |e_u^T D e_v| = 1, so ratio^2 >= copies/2.
    ratio2 = 1 / norm2
    assert ratio2 == F(copies, 2)

    # Independently check exact diagonal/spoke isolation on a nontrivial
    # fully populated supported input.  No apex action is used for a spoke.
    full_d = {(i, i): F(3*i - 7, 11) for i in range(n)}
    full_d.update({ij: F(5*k - 9, 13) for k, ij in enumerate(sorted(edges))})
    full_y = action(colors, full_d)
    assert all(full_y[i][colors[i]] == full_d[i, i] for i in range(n))
    for apex, path in fans:
        for v in path:
            assert full_y[v][colors[apex]] == full_d[min(apex,v), max(apex,v)]
    canonical = json.dumps({"copies": copies, "colors": colors,
                            "edges": sorted(edges),
                            "coefficients": [[i, j, t.numerator, t.denominator]
                                             for (i,j), t in sorted(d.items())]},
                           separators=(",", ":")).encode()
    return {"copies": copies, "vertices": n, "graph_edges": len(edges),
            "nonzero_undirected_coefficients": len(d),
            "row_norm_squared": "1", "action_norm_squared": str(norm2),
            "operator_norm_lower": "1", "inverse_ratio_squared_lower": str(ratio2),
            "fixture_sha256": hashlib.sha256(canonical).hexdigest(),
            "diagonal_and_spoke_isolation": "passed", "status": "passed"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    start, cpu = time.perf_counter(), time.process_time()
    cases = [check(n) for n in (1, 16, 256)]
    result = {"schema": "astra.local_fan_ports.v1", "cases": cases,
              "body_wall_seconds": time.perf_counter()-start,
              "body_cpu_seconds": time.process_time()-cpu,
              "max_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
              "claim_scope": "specified recursive orthogonal port design only",
              "universal_proof": "notes/fan_port_lemma.md"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
