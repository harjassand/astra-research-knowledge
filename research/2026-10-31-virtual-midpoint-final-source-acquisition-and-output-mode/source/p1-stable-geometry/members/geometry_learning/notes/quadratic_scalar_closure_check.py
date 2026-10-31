#!/usr/bin/env python3
"""Proof diagnostics for quadratic scalar closure; not an acquisition oracle."""

from fractions import Fraction
import json
from math import comb
from pathlib import Path

import numpy as np


def norm(matrix):
    return float(np.linalg.norm(matrix, 2))


def product(matrices):
    result = np.eye(matrices[0].shape[0])
    for matrix in matrices:
        result = matrix @ result
    return result


def bounds(matrices, p, f, g):
    q = np.eye(p.shape[0]) - p
    a = [norm(q @ matrix @ p) for matrix in matrices]
    b = [norm(p @ matrix @ q) for matrix in matrices]
    pairs = sum(a[i]*b[j] for i in range(len(a)) for j in range(i+1, len(a)))
    full = product(matrices)
    reduced = product([p @ matrix @ p for matrix in matrices])
    operator_error = norm(p @ full @ p - reduced)
    alpha, beta = float(np.linalg.norm(q @ f)), float(np.linalg.norm(q @ g))
    pf, pg = float(np.linalg.norm(p @ f)), float(np.linalg.norm(p @ g))
    scalar_bound = pf*pg*pairs + beta*pf*sum(a) + alpha*pg*sum(b) + alpha*beta
    scalar_error = abs(float(g @ full @ f - (p @ g) @ reduced @ (p @ f)))
    return {
        "operator_error": operator_error,
        "operator_bound": pairs,
        "scalar_error": scalar_error,
        "scalar_bound_with_projection_debts": scalar_bound,
    }


def exact_markov_checks():
    rows = []
    for horizon in [2, 3, 5, 20, 100]:
        for denominator in [100, 10_000, 1_000_000]:
            e = Fraction(1, denominator)
            true = (1+(1-2*e)**horizon)/2
            compressed = (1-e)**horizon
            error = true-compressed
            upper = comb(horizon, 2)*e**2
            lower = upper*(1-e)**(horizon-2)
            assert lower <= error <= upper
            if horizon == 2:
                assert error == upper
            rows.append({
                "horizon": horizon,
                "e_denominator": denominator,
                "exact_rational_inequalities_passed": True,
                "error_over_quadratic_upper": float(error/upper),
                "lower_over_upper": float(lower/upper),
            })
    return rows


def limitation_checks():
    p = np.diag([1.0, 0.0])
    f = np.array([1.0, 0.0])
    e = 0.125
    t1 = np.array([[0.0, 0.0], [e, 0.0]])
    t2 = np.array([[0.0, 1.0], [0.0, 0.0]])
    one_sided = bounds([t1, t2], p, f, f)
    assert one_sided["operator_error"] == e
    assert one_sided["operator_bound"] == e
    assert one_sided["operator_error"] > e**2

    symmetric = np.array([[0.0, e], [e, 0.0]])
    outside_readout = bounds([symmetric], p, f, np.array([0.0, 1.0]))
    assert outside_readout["operator_error"] == 0.0
    assert outside_readout["scalar_error"] == e
    assert outside_readout["scalar_bound_with_projection_debts"] == e

    xi = Fraction(1, 1000)
    fit = []
    for horizon in [1, 10, 100]:
        error = 1-(1-xi)**horizon
        assert error <= horizon*xi
        fit.append({
            "horizon": horizon,
            "fit_error_over_linear_upper": float(error/(horizon*xi)),
        })
    return {
        "forward_only_counterexample": one_sided,
        "readout_outside_subspace": outside_readout,
        "in_span_fit_error_is_first_order": fit,
    }


def random_checks():
    rng = np.random.default_rng(127301)
    maximum_operator_ratio = 0.0
    maximum_scalar_ratio = 0.0
    trials = 240
    self_adjoint_count = 0
    for trial in range(trials):
        dimension = int(rng.integers(2, 9))
        rank = int(rng.integers(1, dimension))
        horizon = int(rng.integers(1, 11))
        basis, _ = np.linalg.qr(rng.normal(size=(dimension, dimension)))
        p = basis[:, :rank] @ basis[:, :rank].T
        matrices = []
        self_adjoint = trial % 2 == 0
        self_adjoint_count += self_adjoint
        for _ in range(horizon):
            matrix = rng.normal(size=(dimension, dimension))
            if self_adjoint:
                matrix = (matrix+matrix.T)/2
            matrix /= max(1.0, norm(matrix))
            matrices.append(matrix)
        f, g = rng.normal(size=dimension), rng.normal(size=dimension)
        f /= np.linalg.norm(f)
        g /= np.linalg.norm(g)
        result = bounds(matrices, p, f, g)
        assert result["operator_error"] <= result["operator_bound"]+1e-12
        assert result["scalar_error"] <= result["scalar_bound_with_projection_debts"]+1e-12
        if result["operator_bound"] > 1e-12:
            maximum_operator_ratio = max(maximum_operator_ratio, result["operator_error"]/result["operator_bound"])
        if result["scalar_bound_with_projection_debts"] > 1e-12:
            maximum_scalar_ratio = max(maximum_scalar_ratio, result["scalar_error"]/result["scalar_bound_with_projection_debts"])
    return {
        "trials": trials,
        "self_adjoint_trials": self_adjoint_count,
        "all_operator_and_boundary_checks_passed": True,
        "max_operator_error_over_bound": maximum_operator_ratio,
        "max_scalar_error_over_boundary_bound": maximum_scalar_ratio,
        "arithmetic": "float64 diagnostics; proof independent of tests",
    }


if __name__ == "__main__":
    result = {
        "status": "all_diagnostics_passed",
        "exact_markov_sharpness": exact_markov_checks(),
        "preserved_limitations": limitation_checks(),
        "matrix_checks": random_checks(),
    }
    output = Path(__file__).with_name("quadratic_scalar_closure_results.json")
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
