"""Finite diagnostics for the rational quadratic-gate XXZ refinement.

These checks do not implement or certify the imported Chen--Liu FPRAS.
They check exact local log-concavity inequalities and small-matrix error
bounds for the independently derived symmetric-product schedule.
"""
from fractions import Fraction as F
import itertools
import json
import math
from pathlib import Path

import numpy as np


def p2(x):
    return 1 + x + x * x / 2


def edge_gate(alpha, gamma, h):
    lo = alpha - gamma
    mid = 3 * alpha + gamma
    hi = 5 * alpha - gamma
    vals = [p2(h * x) for x in (lo, mid, hi)]
    low, a, high = vals
    b = (high + low) / 2
    c = (high - low) / 2
    eigs = [a + b + c, a - b - c, -a + b - c, -a - b + c]
    assert lo >= 0 and lo <= mid <= hi
    assert min(eigs) >= 0 or max(eigs[1:]) <= 0
    assert eigs[0] >= 0 and all(x <= 0 for x in eigs[1:])
    return {"a": a, "b": b, "c": c, "eigenvalues": eigs}


def field_gate(b, c, h):
    r = b + abs(c)
    # A = [[r+c,b],[b,r-c]], F=I+hA+h^2 A^2/2.
    A00, A01, A11 = r + c, b, r - c
    v = 1 + h * A00 + h * h * (A00 * A00 + A01 * A01) / 2
    d = h * A01 + h * h * A01 * (A00 + A11) / 2
    u = 1 + h * A11 + h * h * (A11 * A11 + A01 * A01) / 2
    assert u > 0 and v > 0 and d >= 0 and u * v - d * d > 0
    return {"u": u, "v": v, "d": d, "det": u * v - d * d}


I2 = np.eye(2, dtype=float)
X = np.array([[0., 1.], [1., 0.]])
Y = np.array([[0., -1j], [1j, 0.]])
Z = np.diag([1., -1.]).astype(complex)


def embed(n, ops):
    out = np.ones((1, 1), dtype=complex)
    for v in range(n):
        out = np.kron(out, ops.get(v, I2))
    return np.real_if_close(out).real


def local_terms(n, case):
    terms = []
    # Include a triangle for n=3, plus one edge in the two-qubit fixtures.
    edges = list(itertools.combinations(range(n), 2))
    for j, (u, v) in enumerate(edges):
        alpha = [.5, 1., 1.25][(case + j) % 3]
        gamma = alpha * [-1., 0., 1.][(case + j) % 3]
        term = alpha * (embed(n, {u: X, v: X}) + embed(n, {u: Y, v: Y}))
        term += gamma * embed(n, {u: Z, v: Z})
        term += 3 * alpha * np.eye(2**n)
        terms.append(term)
    for v in range(n):
        b = [0., .25, .75][(case + v) % 3]
        c = [-.5, 0., .75][(case + 2 * v) % 3]
        r = b + abs(c)
        terms.append(b * embed(n, {v: X}) + c * embed(n, {v: Z}) + r * np.eye(2**n))
    return terms


def main():
    exact_edge_cases = 0
    exact_field_cases = 0
    for alpha in (F(1, 3), F(1), F(5, 4)):
        for ratio in (F(-1), F(-1, 2), F(0), F(1, 2), F(1)):
            for h in (F(1, 16), F(1, 3), F(2)):
                edge_gate(alpha, alpha * ratio, h)
                exact_edge_cases += 1
    for b in (F(0), F(1, 3), F(2)):
        for c in (F(-2, 3), F(0), F(5, 4)):
            for h in (F(1, 16), F(1, 3), F(2)):
                field_gate(b, c, h)
                exact_field_cases += 1

    numerical = []
    for case in range(24):
        n = 2 + case % 2
        terms = local_terms(n, case)
        D = sum(float(np.linalg.norm(a, 2)) for a in terms)
        beta = [.2, .7, 1.3][case % 3]
        eps = [.2, .05, .01, .005][case % 4]
        tau = beta * D
        m = math.ceil(max(1., 2 * tau, math.sqrt((43. / 15.) * tau**3 / eps)))
        h = beta / (2 * m)
        w = np.eye(2**n)
        sum_a = np.zeros_like(w)
        for a in terms:
            sum_a += a
            w = w @ (np.eye(2**n) + h * a + (h * h / 2) * (a @ a))
        B = w @ w.T
        vals, vecs = np.linalg.eigh(B)
        assert vals[0] >= 1. - 1e-9
        logB = (vecs * np.log(vals)) @ vecs.T
        err = float(np.linalg.norm(m * logB - beta * sum_a, 2))
        bound = (43. / 60.) * tau**3 / m**2
        assert err <= bound + 2e-7 * max(1., bound), (case, err, bound)
        assert err <= eps / 4 + 2e-7
        numerical.append({"case": case, "n": n, "beta": beta, "epsilon": eps,
                          "m": m, "tau": tau, "generator_error": err,
                          "proved_bound": bound, "target": eps / 4})

    old_exponents = {"partition_m_large_tau": "Theta(tau^2/epsilon)",
                     "partition_count_arithmetic_core": "O(p^12 tau^24 epsilon^-14) up to logarithms",
                     "partition_count_with_explicit_oracle": "O(p^13 tau^26 epsilon^-15) up to logarithms",
                     "constant_generator_budget_m": "Theta(tau^2)"}
    new_exponents = {"partition_m_large_tau": "Theta(tau^(3/2)/sqrt(epsilon))",
                     "partition_count_arithmetic_core": "O(p^12 tau^18 epsilon^-8) up to logarithms",
                     "partition_count_with_explicit_oracle": "O(p^13 tau^(39/2) epsilon^(-17/2)) up to logarithms",
                     "constant_generator_budget_m": "Theta(tau^(3/2))"}
    out = {
        "status": "PASS: finite local and small-matrix diagnostics only; imported FPRAS not run",
        "exact_edge_gate_cases": exact_edge_cases,
        "exact_field_gate_cases": exact_field_cases,
        "matrix_cases": len(numerical),
        "max_generator_error_over_proved_bound": max(x["generator_error"] / x["proved_bound"] for x in numerical),
        "max_generator_error_over_target": max(x["generator_error"] / x["target"] for x in numerical),
        "old_exponents": old_exponents,
        "new_exponents": new_exponents,
        "matrix_details": numerical,
    }
    path = Path(__file__).with_name("strang_xxz_cost_check.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "matrix_details"}, indent=2))


if __name__ == "__main__":
    main()
