#!/usr/bin/env python3
"""Scoped exact replay of the newly retrieved N507 construction.

This independently checks the finite algebra feeding the all-word CP mechanism
and the rigid-frame fixed-lag obstruction. It does not replay the seven-time
raw-word witness coefficients or constitute a proof of the closure theorem.
"""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SEED = HERE / "sources" / "ASTRA_N507_EXACT_SEED.json"


def matrix(x):
    return [[F(v) for v in row] for row in x]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    bt = transpose(b)
    return [[sum((u * v for u, v in zip(row, col)), F(0))
             for col in bt] for row in a]


def scale(a, c):
    return [[c * v for v in row] for row in a]


def rank(a):
    b = [row[:] for row in a]
    pivot = 0
    for col in range(len(b[0])):
        found = next((i for i in range(pivot, len(b)) if b[i][col]), None)
        if found is None:
            continue
        b[pivot], b[found] = b[found], b[pivot]
        value = b[pivot][col]
        b[pivot] = [x / value for x in b[pivot]]
        for i in range(pivot + 1, len(b)):
            value = b[i][col]
            if value:
                b[i] = [x - value * y for x, y in zip(b[i], b[pivot])]
        pivot += 1
        if pivot == len(b):
            break
    return pivot


def determinant(a):
    b = [row[:] for row in a]
    answer = F(1)
    for col in range(len(b)):
        found = next((i for i in range(col, len(b)) if b[i][col]), None)
        if found is None:
            return F(0)
        if found != col:
            b[col], b[found] = b[found], b[col]
            answer = -answer
        value = b[col][col]
        answer *= value
        b[col] = [x / value for x in b[col]]
        for i in range(col + 1, len(b)):
            value = b[i][col]
            if value:
                b[i] = [x - value * y for x, y in zip(b[i], b[col])]
    return answer


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    seed_bytes = SEED.read_bytes()
    seed = json.loads(seed_bytes)
    q, h, m, ell = map(matrix, [seed["Q"], seed["H"], seed["M"], seed["L"]])
    points, planar_z = map(matrix, [seed["points"], seed["farkas_z"]])
    require(len(q) == 10 and len(h[0]) == 8, "wrong seed dimensions")
    require(all(sum(row) == 0 for row in q), "row-sum failure")
    require(all(sum(col) == 0 for col in transpose(q)), "uniform stationarity failure")
    require(all(q[i][j] >= 0 for i in range(10) for j in range(10) if i != j),
            "negative off-diagonal rate")
    seen = {0}
    for _ in range(10):
        seen |= {j for i in seen for j in range(10) if i != j and q[i][j] > 0}
    require(len(seen) == 10, "not irreducible")
    require(all((q[i][j] > 0) == (q[j][i] > 0)
                for i in range(10) for j in range(10) if i != j),
            "unpaired edge support")
    require(q != transpose(q), "target unexpectedly reversible")
    require(rank(h) == 8, "observable basis rank failure")
    require(m == scale(mm(transpose(h), h), F(1, 10)), "Gram failure")
    qh = mm(q, h)
    require(qh == mm(h, ell), "forward invariance failure")
    require(mm(m, ell) == mm(transpose(ell), m), "restriction not selfadjoint")
    adjoint_h = mm(transpose(q), h)
    require(adjoint_h != qh, "claimed adjoint leakage absent")
    require(all(dot(v, v) == 1 for v in points), "vertices not on unit circle")
    require(len(set(tuple(v) for v in points)) == 5, "duplicate vertex")
    vandermonde = [[F(1), x, y, x*x, x*y] for x, y in points]
    det = determinant(vandermonde)
    require(det == F(seed["five_point_moment_determinant"]) and det != 0,
            "rigid weight moment determinant failure")

    field = []
    for v, z in zip(points, planar_z):
        field.append([F(0), *z, *([dot(v, z)] * 5)])
    field += [[F(0)] * 8 for _ in range(5)]
    pairings = {}
    for i in range(10):
        for j in range(i + 1, 10):
            pairings[f"{i},{j}"] = dot(
                [a-b for a, b in zip(field[i], field[j])],
                [a-b for a, b in zip(h[i], h[j])])
    require(min(pairings.values()) >= 0, "nonmonotone full field")
    internal_pairings = [pairings[f"{i},{j}"]
                         for i in range(5) for j in range(i+1, 5)]
    require(min(internal_pairings) > 0, "internal strict monotonicity failure")
    derivative = -sum((dot(z, dh) for z, dh in zip(field, qh)), F(0)) / 10
    require(2 * derivative == F(seed["farkas_drift_pairing"]), "drift mismatch")
    gamma = -derivative
    require(gamma > F(59, 10000), "insufficient exact drift margin")
    q_norm = max(sum(abs(v) for v in row) for row in q)
    beta = sum((sum(abs(v) for v in row) for row in field), F(0)) / 10
    require(q_norm <= 2 and beta <= 2, "Taylor norm cap failure")
    require(max(abs(v) for row in h for v in row) <= 1, "feature cap failure")
    lag = F(1, 1000)
    remainder = 4 * lag * lag / (1 - 2*lag)
    upper = -gamma * lag + remainder
    require(upper < -F(1968761, 10**12), "fixed-lag sign margin failure")

    # Output-block multiplication preserves the claimed observable basis.
    labels = [0]*5 + list(range(1, 6))
    for label in range(6):
        output_h = [[v if labels[i] == label else F(0) for v in row]
                    for i, row in enumerate(h)]
        joined = [row + other for row, other in zip(h, output_h)]
        require(rank(joined) == 8, "observation projection leaves feature space")

    record = {
        "status": "all scoped exact checks passed",
        "seed_sha256": hashlib.sha256(seed_bytes).hexdigest(),
        "arithmetic": "Python standard-library Fraction; no floating sign decisions",
        "dimensions": {"hidden": 10, "observed": 6, "feature_rank": 8},
        "finite_checks": [
            "stationary rational CTMC with uniform mass, irreducibility and paired support",
            "nonreversibility, QH=HL, M=H^T H/10, ML=L^T M",
            "adjoint leakage and invariant observation projections",
            "unit-circle rigidity points and invertible five-moment matrix",
            "full monotone field and strictly negative required reversible drift",
            "analytic Taylor remainder certifies a negative fixed rational lag"
        ],
        "minimum_internal_monotonicity": str(min(internal_pairings)),
        "gamma": str(gamma),
        "gamma_decimal": float(gamma),
        "Q_infinity_norm": str(q_norm),
        "beta": str(beta),
        "lag": str(lag),
        "fixed_lag_upper_bound": str(upper),
        "fixed_lag_upper_bound_decimal": float(upper),
        "not_checked_by_this_script": [
            "universal closure argument, which is a mathematical proof",
            "seven-time raw observation witness coefficients and sampling calculation",
            "historical priority, external validation, or any native physical system"
        ]
    }
    output = HERE / "N507_BRIDGE_CHECKS.json"
    output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
