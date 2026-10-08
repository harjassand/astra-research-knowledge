#!/usr/bin/env python3
"""Finite exact check of the shared local Fisher spectrum used in the note.

This checks only the sensor-algebra fixture. The analytic RAC and query
lower bounds are proved in proof.txt and are not numerically tested here.
"""

from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path


def bernoulli_score_fisher(d: int, r: Fraction) -> list[list[Fraction]]:
    points = list(product((-1, 1), repeat=d))
    scores = [[r * x[i] for i in range(d)] for x in points]
    return [
        [sum(row[i] * row[j] for row in scores) / len(points) for j in range(d)]
        for i in range(d)
    ]


def main() -> None:
    r = Fraction(1, 2)
    expected = r * r
    rows = []
    for d in range(1, 9):
        got = bernoulli_score_fisher(d, r)
        target = [
            [expected if i == j else Fraction(0) for j in range(d)]
            for i in range(d)
        ]
        assert got == target
        rows.append({"dimension": d, "bernoulli_fisher": str(got[0][0]),
                     "gaussian_fisher_diagonal": str(expected),
                     "off_diagonal_zero": True})

    ratio = 1 / 4
    h2 = -ratio * math.log2(ratio) - (1 - ratio) * math.log2(1 - ratio)
    result = {
        "status": "finite_exact_spectrum_fixture_only",
        "parameter_r": str(r),
        "bernoulli_and_gaussian_local_fisher_eigenvalue": str(expected),
        "tested_dimensions": rows,
        "rac_lower_bits_per_mode_at_eps_over_r_1_4": 1 - h2,
        "note": "Does not prove the archive lower bound or Gaussian candidate rate.",
    }
    out = Path(__file__).with_name("spectrum_fixture.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
