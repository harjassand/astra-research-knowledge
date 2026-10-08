#!/usr/bin/env python3
"""Independent exact ray/tie check for the three Spin(9) support cones.

This checks cone geometry only. It does not build or test the star matrices.
Each cone is given by alpha>=0 and two exact score-difference inequalities.
For a full-dimensional pointed cone in R^4, an extreme ray is the nullspace
of at least three independent active facet normals; exhaustive triples find
all such rays. The script also records all winning-score ties on every ray.
"""

from __future__ import annotations

from itertools import combinations
from math import gcd

import sympy as sp


VERTICES = (
    sp.Matrix([1, 0, 0, 14]),
    sp.Matrix([0, 1, 7, 7]),
    sp.Matrix([1, 4, 4, 6]),
)


def primitive_ray(v: sp.Matrix) -> tuple[int, ...]:
    denominator = sp.ilcm(*(entry.q for entry in v))
    values = [int(entry * denominator) for entry in v]
    common = 0
    for value in values:
        common = gcd(common, abs(value))
    return tuple(value // common for value in values)


def cone_constraints(winner: int) -> list[sp.Matrix]:
    constraints = [sp.eye(4).row(j) for j in range(4)]
    constraints.extend(
        (VERTICES[winner] - VERTICES[other]).T
        for other in range(3)
        if other != winner
    )
    return constraints


def enumerate_cone(winner: int) -> set[tuple[int, ...]]:
    rows = cone_constraints(winner)
    rays: set[tuple[int, ...]] = set()
    for chosen in combinations(range(len(rows)), 3):
        active = sp.Matrix.vstack(*(sp.Matrix(rows[j]) for j in chosen))
        if active.rank() != 3:
            continue
        kernel = active.nullspace()
        if len(kernel) != 1:
            continue
        vector = kernel[0]
        if all((row * vector)[0] >= 0 for row in rows):
            pass
        elif all((row * (-vector))[0] >= 0 for row in rows):
            vector = -vector
        else:
            continue
        ray = primitive_ray(vector)
        # A ray on a pointed cone's boundary must have active-normal rank 3.
        active_at_ray = [row for row in rows if (row * sp.Matrix(ray))[0] == 0]
        if sp.Matrix.vstack(*active_at_ray).rank() < 3:
            raise AssertionError((winner, ray, "not extreme"))
        rays.add(ray)
    return rays


def main() -> None:
    expected = (
        {
            (0, 0, 0, 1),
            (0, 0, 1, 1),
            (0, 2, 0, 1),
            (0, 7, 5, 6),
            (1, 0, 0, 0),
            (7, 0, 2, 1),
        },
        {
            (0, 0, 1, 0),
            (0, 0, 1, 1),
            (0, 1, 1, 0),
            (0, 7, 5, 6),
            (3, 0, 1, 0),
            (7, 0, 2, 1),
        },
        {
            (0, 1, 0, 0),
            (0, 1, 1, 0),
            (0, 2, 0, 1),
            (0, 7, 5, 6),
            (1, 0, 0, 0),
            (3, 0, 1, 0),
            (7, 0, 2, 1),
        },
    )

    union: set[tuple[int, ...]] = set()
    strict_witnesses = ((1, 1, 1, 2), (1, 1, 2, 1), (1, 2, 1, 1))
    for winner in range(3):
        witness = sp.Matrix(strict_witnesses[winner])
        witness_values = tuple(int((vertex.T * witness)[0]) for vertex in VERTICES)
        assert all(value > 0 for value in witness)
        assert witness_values[winner] > max(
            witness_values[j] for j in range(3) if j != winner
        )
        rays = enumerate_cone(winner)
        assert rays == expected[winner], (winner, sorted(rays), sorted(expected[winner]))
        for ray in rays:
            alpha = sp.Matrix(ray)
            values = tuple(int((vertex.T * alpha)[0]) for vertex in VERTICES)
            assert values[winner] == max(values)
            ties = tuple(i for i, value in enumerate(values) if value == max(values))
            print(f"L{winner} cone ray {ray}: values={values}; tie set={ties}")
        union.update(rays)

    assert len(union) == 10
    print("independent exact extreme-ray and tie audit: PASS (10-ray union)")


if __name__ == "__main__":
    main()
