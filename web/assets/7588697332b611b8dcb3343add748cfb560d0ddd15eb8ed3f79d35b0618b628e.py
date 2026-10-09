"""Exact finite diagnostics for identities used in v1/v2, not a solver implementation."""
from fractions import Fraction as F
from itertools import combinations
from math import prod
import json
from pathlib import Path

DIM = 3
ZERO = (0,) * DIM

def add(*polys):
    out = {}
    for poly in polys:
        for powers, value in poly.items():
            out[powers] = out.get(powers, F(0)) + value
    return {powers: value for powers, value in out.items() if value}

def scale(poly, scalar):
    return {powers: value * scalar for powers, value in poly.items() if value * scalar}

def mul(*polys):
    out = {ZERO: F(1)}
    for poly in polys:
        updated = {}
        for powers, value in out.items():
            for others, coefficient in poly.items():
                key = tuple(a + b for a, b in zip(powers, others))
                updated[key] = updated.get(key, F(0)) + value * coefficient
        out = updated
    return out

def linear(vector):
    return {tuple(int(i == j) for i in range(DIM)): coefficient
            for j, coefficient in enumerate(vector) if coefficient}

def gauss_moment(power):
    if power % 2:
        return 0
    return prod(range(1, power, 2))

def expectation(poly):
    return sum((value * prod(gauss_moment(p) for p in powers)
                for powers, value in poly.items()), F(0))

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(((-1) ** j * matrix[0][j] * determinant(
        [[row[k] for k in range(len(matrix)) if k != j] for row in matrix[1:]])
        for j in range(len(matrix))), F(0))

def psd(matrix):
    for size in range(1, DIM + 1):
        for subset in combinations(range(DIM), size):
            if determinant([[matrix[i][j] for j in subset] for i in subset]) < 0:
                return False
    return True

def eye_difference(bound, matrix):
    return [[(bound if i == j else F(0)) - matrix[i][j]
             for j in range(DIM)] for i in range(DIM)]

signal = [F(1), F(0), F(0)]
U = linear(signal)
design = [linear([F(int(i == j)) for i in range(DIM)]) for j in range(DIM)]
cases = [
    ("at_truth", [F(0), F(0), F(0)]),
    ("parallel_out", [F(1, 9), F(0), F(0)]),
    ("parallel_in", [F(-1, 9), F(0), F(0)]),
    ("orthogonal", [F(0), F(1, 9), F(0)]),
    ("rational_oblique", [F(1, 15), F(4, 45), F(0)]),
]
records = []
for name, displacement in cases:
    candidate = [a + b for a, b in zip(signal, displacement)]
    W = linear(candidate)
    residual = add(mul(W, W), scale(mul(U, U), -1))
    grad_poly = [mul(residual, W, coordinate) for coordinate in design]
    observed_mean = [expectation(poly) for poly in grad_poly]
    norm_squared = sum(c * c for c in candidate)
    expected_mean = [(3 * norm_squared - 1) * c - 2 * candidate[0] * s
                     for c, s in zip(candidate, signal)]
    assert observed_mean == expected_mean
    e_squared = sum(e * e for e in displacement)
    assert e_squared <= F(1, 81)
    hessian = [[((3 * norm_squared - 1) if i == j else F(0))
                + 6 * candidate[i] * candidate[j] - 2 * signal[i] * signal[j]
                for j in range(DIM)] for i in range(DIM)]
    assert psd([[hessian[i][j] - (F(4, 3) if i == j else F(0))
                 for j in range(DIM)] for i in range(DIM)])
    assert psd(eye_difference(F(11), hessian))
    for sigma in [F(0), F(1), F(10)]:
        covariance = [[expectation(mul(grad_poly[i], grad_poly[j]))
                       - observed_mean[i] * observed_mean[j]
                       + sigma * sigma * ((norm_squared if i == j else F(0))
                                          + 2 * candidate[i] * candidate[j])
                       for j in range(DIM)] for i in range(DIM)]
        bound = 1300 * e_squared + 4 * sigma * sigma
        assert psd(eye_difference(bound, covariance))
        records.append({"case": name, "sigma": str(sigma),
                        "gradient_identity": True, "local_hessian_bounds": True,
                        "covariance_bound_v2_4_1": True,
                        "covariance_trace": str(sum(covariance[i][i] for i in range(DIM)))})

for sigma in [F(0), F(1), F(10)]:
    raw = [[expectation(mul(U, U, U, U, design[i], design[j]))
            + (sigma * sigma if i == j else F(0))
            for j in range(DIM)] for i in range(DIM)]
    expected = [[((3 + sigma * sigma) if i == j else F(0))
                 + 12 * signal[i] * signal[j] for j in range(DIM)] for i in range(DIM)]
    assert raw == expected

result = {"scope": "Exact rational Gaussian moment checks at 5 fixed local points; no robust PCA or covering SDP was implemented.",
          "cases_passed": len(records), "records": records,
          "raw_second_moment_identity": True,
          "status": "finite-tested diagnostics only, not verification of uniform theorems"}
Path(__file__).with_name("exact_checks_output_v1.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"cases_passed": len(records), "raw_second_moment_identity": True,
                  "output": "exact_checks_output_v1.json"}))
