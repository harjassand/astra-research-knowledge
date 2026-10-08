#!/usr/bin/env python3
"""Exhaustively check the routed-pair edge-load bound used in cycle 7.

For each pair on a cubic torus, route coordinates in order 0,1,2 using a
shortest signed coordinate arc (ties go in the positive direction). The proof
uses the analytic bound max directed-edge load <= L**4; this script checks it
for small L and records the exact maxima.
"""
from collections import Counter
from itertools import product
import json
import sys


def displacement_steps(x: int, y: int, L: int) -> list[int]:
    d = (y - x) % L
    if d <= L // 2:
        return [1] * d
    return [-1] * (L - d)


def torus_load(L: int) -> dict:
    vertices = list(product(range(L), repeat=3))
    load: Counter[tuple[tuple[int, int, int], int, int]] = Counter()
    max_length = 0
    for x in vertices:
        for y in vertices:
            if x == y:
                continue
            pos = list(x)
            seen = {tuple(pos)}
            length = 0
            for axis in range(3):
                for sign in displacement_steps(pos[axis], y[axis], L):
                    edge_start = tuple(pos)
                    load[(edge_start, axis, sign)] += 1
                    pos[axis] = (pos[axis] + sign) % L
                    site = tuple(pos)
                    if site in seen:
                        raise AssertionError((L, x, y, site))
                    seen.add(site)
                    length += 1
            if tuple(pos) != y:
                raise AssertionError((L, x, y, tuple(pos)))
            max_length = max(max_length, length)
    max_load = max(load.values())
    return {
        "L": L,
        "volume": L**3,
        "ordered_pairs": L**3 * (L**3 - 1),
        "max_path_length": max_length,
        "analytic_path_length_bound": 3 * L // 2,
        "max_directed_edge_load": max_load,
        "analytic_load_bound": L**4,
        "load_bound_pass": max_load <= L**4,
        "path_length_bound_pass": max_length <= 3 * L / 2,
    }


def main() -> None:
    sizes = [int(x) for x in sys.argv[1:]] or [4, 6, 8]
    if any(L < 4 or L % 2 for L in sizes):
        raise SystemExit("use even torus sizes L>=4")
    rows = [torus_load(L) for L in sizes]
    if not all(row["load_bound_pass"] and row["path_length_bound_pass"] for row in rows):
        raise SystemExit(json.dumps(rows, indent=2))
    print(json.dumps({"rows": rows, "status": "PASS"}, indent=2))


if __name__ == "__main__":
    main()
