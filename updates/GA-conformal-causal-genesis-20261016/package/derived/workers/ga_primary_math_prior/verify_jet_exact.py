"""Exact fixtures only; the analytic theorems require the written proofs."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import datetime
import json

BASE = Path(__file__).resolve().parent


def convolution(left, right, add_frequency):
    out = {}
    for k, v in left.items():
        for ell, w in right.items():
            key = add_frequency(k, ell)
            out[key] = out.get(key, F(0)) + v * w
    return out


h = {-2: F(1, 2), -1: F(1, 2), 1: F(1, 2), 2: F(1, 2)}
power = {0: F(1)}
moments = {}
for degree in range(1, 13):
    power = convolution(power, h, lambda k, ell: k + ell)
    moments[degree] = power.get(0, F(0))
assert moments[1] == 0 and moments[2] == 1 and moments[3] == F(3, 4)
assert all(moments[degree] > 0 for degree in range(2, 13))

carrier_cases = []
for r in [F(1, 2), F(1), F(3, 2), F(2), F(5)]:
    sigma, kappa = r + 1, r * (r + 2) / 3
    for n in [1, 2, 5, 11]:
        a, b, c, d = F(1, n), F(1), -sigma / n**2, -sigma / n
        q, determinant = sigma * a + d, a * d - b * c
        u_r = 2 * a * q - (r + 2) * a**2 + r * c**2 - 2 * b * c
        cubic = q * u_r - kappa * a * (a**2 + c**2)
        expected = -kappa / n**3 * (1 + sigma**2 / n**2)
        assert q == 0 and determinant == 0 and cubic == expected
        assert sigma * a**2 == a * q - b * c
        carrier_cases.append(
            {"r": str(r), "N": n, "q_coefficient": str(q),
             "determinant_coefficient": str(determinant),
             "C_r_h_cubed_coefficient": str(cubic),
             "mean_C_r": str(cubic * moments[3])}
        )

exponents = []
for s in [F(4), F(9, 2), F(5), F(11, 2), F(6)]:
    theta = 2 * (s - 3) / (s - 2)
    rate = (theta - 1) / 2
    balance = theta / 2 + (3 - theta) / s
    concentration = rate + (3 - theta) * (2 / s - F(1, 2))
    assert balance == 1 and concentration == 0
    exponents.append(
        {"s": str(s), "theta": str(theta), "Q_rate_after_division": str(rate),
         "norm_power": str(3 - theta), "holder_balance": str(balance),
         "critical_concentration_exponent": str(concentration)}
    )

dimensions = []
for degree in range(2, 13):
    tuples = [
        (i, j, k, degree - i - j - k)
        for i in range(degree + 1)
        for j in range(degree - i + 1)
        for k in range(degree - i - j + 1)
    ]
    excluded = [v for v in tuples if v[2] == 0 and v[3] == 0 and v[0] < 2]
    assert len(excluded) == 2 and len(tuples) == comb(degree + 3, 3)
    dimensions.append(
        {"degree": degree, "total": len(tuples),
         "excluded_first_two_jets": len(excluded),
         "selected_theta_1": len(tuples) - len(excluded)}
    )

# Exact Gaussian rationals as (real, imaginary) Fraction pairs.
ZERO, ONE = (F(0), F(0)), (F(1), F(0))


def add(z, w):
    return z[0] + w[0], z[1] + w[1]


def multiply(z, w):
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def polynomial_product(left, right):
    out = {}
    for k, v in left.items():
        for ell, w in right.items():
            key = (k[0] + ell[0], k[1] + ell[1])
            out[key] = add(out.get(key, ZERO), multiply(v, w))
    return out


cos_x = {(1, 0): (F(1, 2), F(0)), (-1, 0): (F(1, 2), F(0))}
sin_x = {(1, 0): (F(0), -F(1, 2)), (-1, 0): (F(0), F(1, 2))}
cos_y = {(0, 1): (F(1, 2), F(0)), (0, -1): (F(1, 2), F(0))}
sin_y = {(0, 1): (F(0), -F(1, 2)), (0, -1): (F(0), F(1, 2))}
entries = [cos_x, cos_y, polynomial_product(cos_x, sin_y),
           polynomial_product(sin_x, cos_y)]
assert all(entry.get((0, 0), ZERO) == ZERO for entry in entries)
covariance = []
for left in entries:
    row = []
    for right in entries:
        moment = polynomial_product(left, right).get((0, 0), ZERO)
        assert moment[1] == 0
        row.append(moment[0])
    covariance.append(row)
expected_diagonal = [F(1, 2), F(1, 2), F(1, 4), F(1, 4)]
assert covariance == [
    [expected_diagonal[i] if i == j else F(0) for j in range(4)]
    for i in range(4)
]


def evaluate_y_zero(entry, quarter_turns_x):
    unit_roots = [ONE, (F(0), F(1)), (-F(1), F(0)), (F(0), -F(1))]
    value = ZERO
    for (kx, _ky), coefficient in entry.items():
        value = add(value, multiply(coefficient, unit_roots[(kx * quarter_turns_x) % 4]))
    assert value[1] == 0
    return value[0]


slice_zero = [evaluate_y_zero(entry, 0) for entry in entries]
slice_quarter = [evaluate_y_zero(entry, 1) for entry in entries]
difference = [left - right for left, right in zip(slice_zero, slice_quarter)]
assert difference == [1, 0, 0, -1]
slice_determinant = difference[0] * difference[3] - difference[1] * difference[2]
assert slice_determinant == -1

receipt = {
    "date_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "PASS_SPECIFIED_EXACT_ALGEBRA_ONLY",
    "scope": (
        "Exact Fourier carrier moments, rank-one compatibility and target-cubic coefficients, "
        "exponent balances, polynomial dimensions, separated-subclass covariance and rank-two "
        "slice difference. Does not verify interpolation, Hodge, density, universal inequalities "
        "or historical priority."
    ),
    "moment_profile": "cos(z)+cos(2z)",
    "moments": {str(k): str(v) for k, v in moments.items()},
    "carrier_cases": carrier_cases,
    "exponents": exponents,
    "dimensions": dimensions,
    "separated_subclass_scope_blocker": {
        "f": "sin(x)+sin(y)", "g": "sin(x)*sin(y)",
        "covariance": [[str(v) for v in row] for row in covariance],
        "covariance_determinant": str(F(1, 2)**2 * F(1, 4)**2),
        "slice_y": "0", "slice_x": ["0", "pi/2"],
        "slice_matrices": [[str(v) for v in slice_zero], [str(v) for v in slice_quarter]],
        "difference_matrix": [
            [str(difference[0]), str(difference[1])],
            [str(difference[2]), str(difference[3])],
        ],
        "difference_determinant": str(slice_determinant),
        "logical_scope": (
            "Blocks triangular support and ordinary rank-one slice Jensen; "
            "does not establish nonlaminate status."
        ),
    },
}
(BASE / "JET_EXACT_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print("PASS: 20 carrier cases, 5 exponent cases, 11 dimensions, exact covariance and slice rank.")
