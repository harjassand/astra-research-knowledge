"""Independent exact checks for the frozen c10_s03 INITIAL counterexample.

This is a fresh, small checker written by c10_l08. It does not import or
execute c10_s03 code. The proof of positive recurrence is the detailed-balance
identity plus the stopped first-moment non-explosion argument in the audit.
"""

from fractions import Fraction as F
from itertools import product
from math import factorial
import json
from pathlib import Path


def falling(x, y):
    out = 1
    for a, b in zip(x, y):
        if a < b:
            return 0
        for v in range(a - b + 1, a + 1):
            out *= v
    return out


def weight(x):
    a, b = x
    return F(1, factorial(a) * factorial(b))


# All rates are one. Each edge is paired with its listed reverse edge.
channels = [
    ((0, 0), (1, 0)), ((1, 0), (0, 0)),
    ((0, 0), (0, 1)), ((0, 1), (0, 0)),
    ((1, 0), (1, 1)), ((1, 1), (1, 0)),
    ((0, 1), (1, 1)), ((1, 1), (0, 1)),
]
reverse = {(y, yp): (yp, y) for y, yp in channels}

db_checks = 0
for a, b in product(range(8), repeat=2):
    x = (a, b)
    for y, yp in channels:
        fwd = falling(x, y)
        if fwd == 0:
            continue
        target = tuple(x[i] + yp[i] - y[i] for i in range(2))
        ry, ryp = reverse[(y, yp)]
        rev = falling(target, ry)
        assert target == tuple(x[i] + yp[i] - y[i] for i in range(2))
        assert weight(x) * fwd == weight(target) * rev, (x, y, yp)
        db_checks += 1

# The exact generator drift of N=A+B, derived from the eight channels.
drift_checks = 0
for a, b in product(range(25), repeat=2):
    x = (a, b)
    drift = sum(
        F(falling(x, y) * sum(yp[i] - y[i] for i in range(2)))
        for y, yp in channels
    )
    assert drift == 2 - 2 * a * b
    assert drift <= 2
    drift_checks += 1

# In the INITIAL one-step class, a species cannot be assigned to S because
# there are no 2A or 2B source reactions. With S empty, these are the two
# required strict source inequalities; their left sides sum to zero.
coeff_A, coeff_B = (-1, 1), (1, -1)
sum_coeff = tuple(coeff_A[i] + coeff_B[i] for i in range(2))
assert sum_coeff == (0, 0)

result = {
    "origin": "c10_s03 frozen INITIAL counterexample; independently recoded by c10_l08",
    "unnormalized_stationary_weight": "1/(a! b!)",
    "local_detailed_balance_checks": db_checks,
    "exact_generator_drift": "L(A+B)=2-2ab",
    "nonexplosion_drift_bound_checks": drift_checks,
    "strict_affine_source_constraints": {
        "A_source_coefficients": coeff_A,
        "B_source_coefficients": coeff_B,
        "sum_coefficients": sum_coeff,
        "simultaneous_le_minus_one_feasible": False,
    },
    "status": "PASS",
    "scope": "finite checks diagnose indexing; detailed-balance and drift identities are symbolic",
}
out = Path(__file__).with_name("c10_s03_baseline_audit_checks.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
