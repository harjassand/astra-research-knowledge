#!/usr/bin/env python3
"""Exact finite checks for CONTROL_CONTINUITY_OBSTRUCTION.md."""

from fractions import Fraction as F
import json
from pathlib import Path


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return list(map(list, zip(*a)))


def correlation(a):
    f = [F(1), F(1), F(-1), F(-1)]
    return sum((f[i]*a[i][j]*f[j] for i in range(4) for j in range(4)), F(0))/4


def require(value, message):
    if not value:
        raise RuntimeError(message)


def main():
    p = [[F(1, 2) if i//2 == j//2 else F(0) for j in range(4)]
         for i in range(4)]
    b = [
        [F(3,4), 0, F(1,4), 0],
        [0, F(5,8), 0, F(3,8)],
        [F(1,4), 0, F(3,4), 0],
        [0, F(3,8), 0, F(5,8)],
    ]
    identity = [[F(i == j) for j in range(4)] for i in range(4)]
    for a in [p, b]:
        require(a == transpose(a), "kernel not reversible for uniform law")
        require(all(sum(row) == 1 for row in a), "kernel not stochastic")
        require(min(v for row in a for v in row) >= 0, "negative probability")
    require(mm(p, p) == p, "P not a projection")
    for label in range(2):
        f = [[F(i//2 == label)] for i in range(4)]
        require(mm(p, f) == f, "P does not fix sensor")
    no_insert = correlation(mm(b, b))
    positive_insert = correlation(mm(mm(b, p), b))
    gap = no_insert-positive_insert
    require(no_insert == F(5,32), "unpulsed correlation mismatch")
    require(positive_insert == F(9,64), "inserted correlation mismatch")
    require(gap == F(1,64), "gap mismatch")
    # K_a = P + z(I-P); exact affine correlation for all scalar z.
    for z in [F(0), F(1,3), F(1,2), F(1)]:
        a = [[p[i][j]+z*(identity[i][j]-p[i][j]) for j in range(4)]
             for i in range(4)]
        require(correlation(mm(mm(b,a),b)) == positive_insert+z*gap,
                "finite-rate interpolation failure")
    record = {
        "status": "all exact finite checks passed",
        "scope": "kernel algebra and observed protocol discontinuity",
        "unpulsed": str(no_insert),
        "positive_duration_insertion": str(positive_insert),
        "gap": str(gap),
        "approximating_correlation": "9/64 + exp(-M epsilon)/64",
        "generator_exit_rate_for_action_a": "M/2",
        "not_claimed": [
            "constant-control continuity implies common hidden continuity",
            "uniform approximation for all positive durations by one finite clock",
            "any native physical implementation"
        ]
    }
    output = Path(__file__).with_name("CONTROL_CONTINUITY_CHECKS.json")
    output.write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
