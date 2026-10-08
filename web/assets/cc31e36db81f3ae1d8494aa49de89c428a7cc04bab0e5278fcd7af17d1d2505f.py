#!/usr/bin/env python3
"""Exact finite checks for the rectangle-cover selective-output reduction.

This checks the indexing/tiling identity with classical integer products. It
does not implement or validate the OpenAI 9/4 matrix-multiplication kernel.
"""

from __future__ import annotations

import json
import random
from fractions import Fraction
from pathlib import Path


def matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    assert a and b and len(a[0]) == len(b)
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def tiled_rect(x: list[list[int]], y: list[list[int]], rows: list[int], cols: list[int], tile: int):
    """Compute X[rows,:]Y[:,cols] from padded tile-square products."""
    inner = len(y)
    assert inner == tile and len(x[0]) == tile
    out: dict[tuple[int, int], int] = {}
    for ri in range(0, len(rows), tile):
        rs = rows[ri : ri + tile]
        for cj in range(0, len(cols), tile):
            cs = cols[cj : cj + tile]
            aa = [x[r][:] for r in rs]
            bb = [[y[k][c] for c in cs] for k in range(tile)]
            aa += [[0] * tile for _ in range(tile - len(aa))]
            bb += []  # number of rows is already exactly tile
            for row in aa:
                row += [0] * (tile - len(row))
            for row in bb:
                row += [0] * (tile - len(row))
            cc = matmul(aa, bb)
            for i, r in enumerate(rs):
                for j, c in enumerate(cs):
                    out[r, c] = cc[i][j]
    return out


def full_product(x, y):
    return matmul(x, y)


def run() -> dict:
    rng = random.Random(20261008)
    n, d = 16, 2
    x = [[rng.randrange(-7, 8) for _ in range(d)] for _ in range(n)]
    y = [[rng.randrange(-7, 8) for _ in range(n)] for _ in range(d)]
    full = full_product(x, y)

    rectangles = [
        (list(range(0, 5)), list(range(0, 7))),
        (list(range(5, 12)), list(range(7, 15))),
        # Overlap one row and one column with the preceding rectangle.
        (list(range(11, 16)), list(range(14, 16))),
    ]
    residual = {(2, 15), (13, 2), (15, 0)}
    cover = {}
    tile_calls = 0
    for rows, cols in rectangles:
        tile_calls += ((len(rows) + d - 1) // d) * ((len(cols) + d - 1) // d)
        block = tiled_rect(x, y, rows, cols, d)
        for key, value in block.items():
            if key in cover:
                assert cover[key] == value
            cover[key] = value

    selected = dict(cover)
    for i, j in residual:
        assert (i, j) not in selected
        selected[i, j] = sum(x[i][k] * y[k][j] for k in range(d))

    assert all(selected[i, j] == full[i][j] for i, j in selected)

    # The component-rectangle recognition guard: the 3-edge path is not a
    # complete bipartite component and must not be treated as one rectangle.
    path_edges = {(0, 0), (0, 1), (1, 1)}
    left = {i for i, _ in path_edges}
    right = {j for _, j in path_edges}
    guard_rejects_path = len(path_edges) != len(left) * len(right)
    assert guard_rejects_path

    # Exact exponent arithmetic: 15/8 + (1/4)(1/4+1/8) = 63/32 < 2.
    exponent = Fraction(15, 8) + Fraction(1, 4) * (Fraction(1, 4) + Fraction(1, 8))
    assert exponent == Fraction(63, 32) and exponent < 2

    return {
        "status": "PASS_FINITE_INTERFACE_CHECK_ONLY",
        "seed": 20261008,
        "dimensions": {"N": n, "D": d},
        "rectangle_count": len(rectangles),
        "rectangle_cover_volume": sum(len(r) * len(c) for r, c in rectangles),
        "tile_calls_using_classical_reference": tile_calls,
        "residual_edges": len(residual),
        "unique_outputs_checked": len(selected),
        "all_outputs_equal_direct_integer_product": True,
        "overlap_deduplication_checked": True,
        "noncomplete_component_guard_rejects_path": guard_rejects_path,
        "exponent": str(exponent),
        "exponent_is_strictly_subquadratic": True,
        "limitations": [
            "Uses classical D-by-D products as the finite reference.",
            "Does not implement or validate the release's 9/4 kernel.",
            "Does not measure bit complexity, setup cost, or practical speed.",
        ],
    }


if __name__ == "__main__":
    result = run()
    out = Path(__file__).with_name("finite_check.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
