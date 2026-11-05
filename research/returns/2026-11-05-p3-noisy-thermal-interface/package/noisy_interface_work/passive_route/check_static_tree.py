"""Finite checks for the static classical history-regeneration operation.

This checks the actual three-gate voter and the decisive coupling witness.
It does not instantiate the BDL code or replace the analytic LS induction.
"""

from fractions import Fraction
from itertools import product
import json


def maj(x):
    return int(sum(x) >= 2)


def voter(x, fault):
    a, b, c = x
    b ^= a
    a ^= fault[0]
    b ^= fault[1]
    c ^= a
    a ^= fault[2]
    c ^= fault[3]
    a ^= b & c
    a ^= fault[4]
    b ^= fault[5]
    c ^= fault[6]
    return a


inputs = list(product((0, 1), repeat=3))
faults = list(product((0, 1), repeat=7))
no_fault_checks = 0
covariance_checks = 0
for x in inputs:
    assert voter(x, (0,) * 7) == maj(x)
    no_fault_checks += 1
    for f in faults:
        assert voter(tuple(t ^ 1 for t in x), f) == voter(x, f) ^ 1
        covariance_checks += 1

witness_checks = 0
for x in inputs:
    for y in inputs:
        if maj(x) != maj(y):
            disagreement = [x[i] ^ y[i] for i in range(3)]
            union_error = [x[i] | y[i] for i in range(3)]
            assert any(
                disagreement[i] and union_error[j]
                for i in range(3)
                for j in range(3)
                if i != j
            )
        witness_checks += 1


def reference_next(u, p, edge):
    z = edge + (1 - 2 * edge) * u
    result = Fraction(0)
    for x in inputs:
        px = z ** sum(x) * (1 - z) ** (3 - sum(x))
        for f in faults:
            pf = p ** sum(f) * (1 - p) ** (7 - sum(f))
            result += px * pf * voter(x, f)
    return result


p = Fraction(1, 1000)
edge = Fraction(1, 1000)
macro_fault = 1 - (1 - p) ** 7
assert macro_fault < Fraction(1, 100)
ubar = Fraction(1, 50)
alpha = 3 * macro_fault + 6 * (ubar + edge)
assert macro_fault + 3 * (ubar + edge) ** 2 <= ubar
assert alpha < 1

u = Fraction(0)
trajectory = []
for depth in range(1, 6):
    # Exact fractions become huge under repeated degree-three composition.
    # The first two steps are exact; thereafter preserve 12 decimal digits.
    u = reference_next(u, p, edge)
    trajectory.append({
        "depth": depth,
        "reference_error": float(u),
        "memory_bound_q_001": float(Fraction(1, 100) * alpha ** depth),
        "leaves": 3 ** depth,
    })
    if depth >= 2:
        u = Fraction(round(float(u) * 10**12), 10**12)

print(json.dumps({
    "ideal_voter_truth_table_checks": no_fault_checks,
    "faultwise_complement_covariance_checks": covariance_checks,
    "majority_disagreement_witness_checks": witness_checks,
    "elementary_output_flip_probability": float(p),
    "wire_flip_probability": float(edge),
    "macro_fault_probability_bound": float(macro_fault),
    "coupling_contraction_bound": float(alpha),
    "reference_trajectory": trajectory,
}, indent=2))
