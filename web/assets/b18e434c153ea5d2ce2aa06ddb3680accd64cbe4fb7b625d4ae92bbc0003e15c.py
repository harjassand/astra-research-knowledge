#!/usr/bin/env python3
"""Exact polyhedral audit for the candidate Spin(9) EB support triangle.

This checks the ten extreme rays listed in SPIN9_SUPPORT_POLYTOPE.md. It
does not evaluate any star Hamiltonian or prove the quantum inequality.
"""

from __future__ import annotations

from itertools import combinations
from math import gcd

import sympy as sp


VERTICES = [
    sp.Matrix([1, 0, 0, 14]),
    sp.Matrix([0, 1, 7, 7]),
    sp.Matrix([1, 4, 4, 6]),
]
EXPECTED = {
    (0, 0): {
        (0, 0, 0, 1),
        (0, 0, 1, 1),
        (0, 2, 0, 1),
        (0, 7, 5, 6),
        (1, 0, 0, 0),
        (7, 0, 2, 1),
    },
    (0, 1): {
        (0, 0, 1, 0),
        (0, 0, 1, 1),
        (0, 1, 1, 0),
        (0, 7, 5, 6),
        (3, 0, 1, 0),
        (7, 0, 2, 1),
    },
    (0, 2): {
        (0, 1, 0, 0),
        (0, 1, 1, 0),
        (0, 2, 0, 1),
        (0, 7, 5, 6),
        (1, 0, 0, 0),
        (3, 0, 1, 0),
        (7, 0, 2, 1),
    },
}


def primitive_integer_ray(v: sp.Matrix) -> tuple[int, ...]:
    denominator_lcm = sp.ilcm(*(entry.q for entry in v))
    entries = [int(entry * denominator_lcm) for entry in v]
    common = 0
    for entry in entries:
        common = gcd(common, abs(entry))
    return tuple(entry // common for entry in entries)


def cone_rays(winner: int) -> set[tuple[int, ...]]:
    # Row constraints are alpha_j >= 0 and (v_winner-v_other)·alpha >= 0.
    rows = [sp.eye(4).row(j) for j in range(4)]
    rows.extend(
        (VERTICES[winner] - VERTICES[other]).T
        for other in range(3)
        if other != winner
    )
    rays: set[tuple[int, ...]] = set()
    # A pointed full-dimensional cone in R^4 has each extreme ray on at least
    # three independent active facets. Enumerate all rank-three triples.
    for active in combinations(range(len(rows)), 3):
        matrix = sp.Matrix.vstack(*(sp.Matrix(rows[index]) for index in active))
        if matrix.rank() != 3:
            continue
        kernel = matrix.nullspace()
        if len(kernel) != 1:
            continue
        candidate = kernel[0]
        if all((row * candidate)[0] >= 0 for row in rows):
            pass
        elif all((row * (-candidate))[0] >= 0 for row in rows):
            candidate = -candidate
        else:
            continue
        rays.add(primitive_integer_ray(candidate))
    return rays


def main() -> None:
    all_rays: set[tuple[int, ...]] = set()
    for winner in range(3):
        rays = cone_rays(winner)
        expected = EXPECTED[(0, winner)]
        if rays != expected:
            raise AssertionError(
                f"winner {winner}: got {sorted(rays)}, expected {sorted(expected)}"
            )
        for ray in rays:
            alpha = sp.Matrix(ray)
            values = [int((vertex.T * alpha)[0]) for vertex in VERTICES]
            if values[winner] != max(values):
                raise AssertionError((winner, ray, values))
        all_rays.update(rays)

    expected_union = set().union(*EXPECTED.values())
    if all_rays != expected_union or len(all_rays) != 10:
        raise AssertionError((sorted(all_rays), sorted(expected_union)))

    print("exact support-cone ray audit: PASS")
    for winner in range(3):
        print(f"L{winner} cone rays ({len(EXPECTED[(0, winner)])}):")
        for ray in sorted(EXPECTED[(0, winner)]):
            print(" ", ray)
    print(f"distinct union ({len(all_rays)}): {sorted(all_rays)}")
    print("scope: candidate support-polytope geometry only; no star PSD checks")


if __name__ == "__main__":
    main()
