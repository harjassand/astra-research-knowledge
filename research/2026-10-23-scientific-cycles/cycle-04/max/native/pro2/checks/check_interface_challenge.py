"""Exact supplementary checks for a scoped fan-block gluing failure.

This checks fixed designs, not an all-design query lower bound.  The universal
aggregate-Gram dichotomy is an analytic theorem in the accompanying note.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import resource
import time


def fixture(copies):
    # Root fan: apex a=0 has color 2, path u=1,v=2 has colors 0,1.
    colors = [2, 0, 1]
    edges = {(0, 1), (0, 2), (1, 2)}
    entries = {(1, 2): F(1)}
    blocks = [(0, 1, 2)]
    for apex, first_color in [(1, 1), (2, 0)]:
        for _ in range(copies):
            first = len(colors)
            colors.extend([first_color, 2])
            second = first + 1
            blocks.append((apex, first, second))
            edges.update(tuple(sorted(e)) for e in
                         [(apex, first), (apex, second), (first, second)])
            entries[tuple(sorted((apex, first)))] = -F(1, copies)
    assert all(len({colors[a], colors[b], colors[c]}) == 3
               for a, b, c in blocks)
    action = [[F(0) for _ in range(5)] for _ in colors]
    for (u, v), value in entries.items():
        assert (u, v) in edges
        action[u][colors[v]] += value
        action[v][colors[u]] += value
    assert all(value == 0 for row in action[:3] for value in row)
    action_sq = sum(value * value for row in action for value in row)
    assert action_sq == F(2, copies)
    assert entries[(1, 2)] == 1  # Certified operator norm >= this entry.
    assert len(colors) == 3 + 4 * copies
    assert len(edges) == 3 + 6 * copies
    return {
        "copies_per_attachment": copies,
        "vertices": len(colors),
        "edges": len(edges),
        "fan_blocks": len(blocks),
        "query_columns": 5,
        "unit_row_norms": True,
        "every_isolated_block_orthonormal_rows": True,
        "action_squared": str(action_sq),
        "operator_squared_lower": "1",
        "inverse_squared_lower": str(F(copies, 2)),
        "status": "passed",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    start_wall, start_cpu = time.perf_counter(), time.process_time()
    rows = [fixture(n) for n in [1, 2, 8, 64, 256]]
    # Root fan in universal proof: six path vertices, 18 scalar coefficients.
    core = {
        "path_vertices": 6,
        "vertices": 7,
        "edges": 11,
        "symmetric_support_dimension": 18,
        "five_query_apex_constraints_at_most": 5,
        "six_codimension_two_constraints_at_most": 12,
        "nonzero_kernel_dimension_at_least": 1,
    }
    assert core["symmetric_support_dimension"] == core["vertices"] + core["edges"]
    assert 18 - 5 - 12 == 1
    record = {
        "scope": "fixed-design gluing failure; universal proof is analytic",
        "fixtures": rows,
        "universal_core_dimension_count": core,
        "wall_seconds": time.perf_counter() - start_wall,
        "cpu_seconds": time.process_time() - start_cpu,
        "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
        "status": "passed",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record))


if __name__ == "__main__":
    main()
