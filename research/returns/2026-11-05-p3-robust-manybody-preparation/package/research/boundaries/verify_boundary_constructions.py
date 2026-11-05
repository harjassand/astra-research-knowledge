#!/usr/bin/env python3
"""Deterministic mathematical checks; no physical experiment or model fitting.

Checks actual-output convex geometry, exact finite-binomial affine coins,
positive Bernstein races, and terminal-depolarizer dimer optima.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from itertools import product
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.stats import binom


HERE = Path(__file__).resolve().parent


def geometry_checks():
    rng = np.random.default_rng(20261105)
    v0 = np.array([[1, -1, 0, 0, 0, 0],
                   [0, 0, 1, -1, 0, 0],
                   [0, 0, 0, 0, 1, -1]], dtype=float)
    b = v0.T / 2
    u = np.ones(6) / 6
    delta, radius = 1 / 32, 1 / 2
    min_weight, max_residual, max_norm_excess = 1., 0., 0.
    for _ in range(500):
        directions = rng.normal(size=(3, 6))
        directions /= np.linalg.norm(directions, axis=0)
        v = (1 - delta / 2) * v0 + (delta / 2) * directions
        assert np.max(np.linalg.norm(v - v0, axis=0)) <= delta + 1e-14
        max_norm_excess = max(max_norm_excess,
                              float(np.max(np.linalg.norm(v, axis=0)) - 1))
        a = v @ b
        for j in range(6):
            w0 = radius * np.eye(6)[j] + (1 - radius) * u
            target = radius * v0[:, j]
            w = w0 + b @ np.linalg.solve(a, target - v @ w0)
            min_weight = min(min_weight, float(np.min(w)))
            max_residual = max(max_residual,
                               float(np.linalg.norm(v @ w - target)),
                               float(abs(np.sum(w) - 1)))
    certified_weight_floor = ((1 - radius) / 6
                              - delta / (2 * (1 - math.sqrt(3) * delta)))
    assert min_weight >= certified_weight_floor - 1e-12
    assert max_residual < 1e-12

    amplitude_damping = []
    for gamma in [0, .1, .25, .4, .49, .5, .6]:
        a = np.diag([math.sqrt(1 - gamma), math.sqrt(1 - gamma), 1 - gamma])
        t = np.array([0., 0., gamma])
        v = a @ v0 + t[:, None]
        all_radii = []
        for j in range(6):
            # Variables are the six weights and the attainable axis radius.
            equality = np.zeros((4, 7))
            equality[:3, :6] = v
            equality[:3, 6] = -v0[:, j]
            equality[3, :6] = 1
            target = np.array([0., 0., 0., 1.])
            objective = np.array([0.] * 6 + [-1.])
            result = linprog(objective, A_eq=equality, b_eq=target,
                             bounds=[(0, None)] * 7, method="highs")
            all_radii.append(float(result.x[-1]) if result.success else None)
        actual = min(all_radii) if all(x is not None for x in all_radii) else None
        if gamma <= .5:
            assert abs(actual - (1 - 2 * gamma)) < 1e-9
        else:
            assert actual is None
        amplitude_damping.append({"gamma": gamma, "common_radius_lp": actual,
                                  "axis_radii": all_radii})
    return {"random_factories": 500, "radius": radius, "delta": delta,
            "certified_min_weight": certified_weight_floor,
            "observed_min_weight": min_weight,
            "max_linear_residual": max_residual,
            "max_bloch_norm_excess": max_norm_excess,
            "amplitude_damping": amplitude_damping}


def clipped_affine_probability(p, n, slope=5., intercept=-4.25):
    k = np.arange(n + 1, dtype=float)
    pmf = binom.pmf(k, n, p)
    return float(np.dot(pmf, np.clip(slope * k / n + intercept, 0, 1)))


def scalar_race_checks():
    radius, outer_a, outer_b = .5, .7, 1.1
    c = outer_b * (1 + radius)
    a0 = outer_a / c
    corners = []
    for k1, k2 in product([0, 1], repeat=2):
        m1 = outer_a + (outer_b - outer_a) * k1
        m2 = outer_a + (outer_b - outer_a) * k2
        corners.append({"corner": [k1, k2],
                        "plus_coefficient": m2 + radius * m1,
                        "minus_coefficient": m2 - radius * m1})
    assert min(row[sign + "_coefficient"] for row in corners
               for sign in ["plus", "minus"]) > 0

    affine_table = []
    for n in [20, 40, 80, 160, 320, 640, 1280]:
        worst = 0.
        for p in np.linspace(.9, 1, 101):
            actual = clipped_affine_probability(p, n)
            true = 5 * p - 4.25
            worst = max(worst, abs(actual - true))
        bound = 8.5 * math.exp(-n / 200)
        assert worst <= bound + 1e-12
        affine_table.append({"n": n, "grid_max_exact_binomial_bias": worst,
                             "certified_bias_bound": min(1., bound)})

    outputs, total_error = 1000, 1e-3
    per_error = total_error / outputs
    attempts = math.ceil(math.log(per_error / 2) / math.log(1 - a0))
    n = math.ceil(200 * math.log(8.5 * 4 * attempts / per_error))
    eta = 8.5 * math.exp(-n / 200)
    declared_bound = (1 - a0) ** attempts + 2 * attempts * eta
    assert declared_bound <= per_error
    rows = []
    for contrast, kappa in product([.95, .975, 1.], repeat=2):
        m1, m2 = contrast * kappa, contrast * kappa * kappa
        assert min(m1, m2) >= .8
        z1 = clipped_affine_probability((1 + m1) / 2, n)
        z2 = clipped_affine_probability((1 + m2) / 2, n)
        approximate_m1 = outer_a + (outer_b - outer_a) * z1
        approximate_m2 = outer_a + (outer_b - outer_a) * z2
        accepted_plus = (approximate_m2 + radius * approximate_m1) / (2 * approximate_m2)
        acceptance = approximate_m2 / c
        # On deadline choose minus, so the plus mass loses its tail.
        output_plus = accepted_plus * (1 - (1 - acceptance) ** attempts)
        ideal_plus = (m2 + radius * m1) / (2 * m2)
        label_error = abs(output_plus - ideal_plus)
        output_radius = kappa * (2 * output_plus - 1)
        # Trace distance for same-axis qubits is half their Bloch separation.
        state_error = abs(output_radius - radius) / 2
        assert label_error <= declared_bound + 1e-11
        assert state_error <= label_error + 1e-12
        assert abs(kappa * (2 * ideal_plus - 1) - radius) < 1e-14
        rows.append({"meter_contrast": contrast, "kappa": kappa,
                     "ideal_plus_probability": ideal_plus,
                     "finite_plus_probability": output_plus,
                     "label_total_variation": label_error,
                     "delivered_qubit_trace_distance": state_error})
    return {"outer_mean_box": [outer_a, outer_b], "target_radius": radius,
            "bernstein_corners": corners, "acceptance_lower_bound": a0,
            "affine_coin_bias_table": affine_table,
            "finite_demonstration": {
                "outputs": outputs, "total_error_budget": total_error,
                "per_output_error_bound": declared_bound,
                "race_attempt_cap": attempts, "assays_per_affine_coin": n,
                "assays_per_output_deadline": 2 * attempts * n,
                "warning": "Constants are large; no practical advantage is asserted.",
                "parameter_checks": rows}}


def falling(n, k):
    result = 1
    for i in range(k):
        result *= n - i
    return result


def bernstein_coefficients(polynomial, degree):
    coeffs = {}
    for k in product(range(degree + 1), repeat=2):
        value = Fraction(0)
        for alpha, coefficient in polynomial.items():
            factor = Fraction(1)
            for ki, ai in zip(k, alpha):
                factor *= Fraction(falling(ki, ai), falling(degree, ai))
            value += coefficient * factor
        coeffs[k] = value
    return coeffs


def polynomial_value(polynomial, z):
    return sum(float(a) * z[0] ** alpha[0] * z[1] ** alpha[1]
               for alpha, a in polynomial.items())


def positive_bernstein_checks():
    polys = [
        {(0, 0): Fraction(3, 10), (1, 0): Fraction(-1),
         (2, 0): Fraction(1), (0, 1): Fraction(1, 5),
         (0, 2): Fraction(-1, 5)},
        {(0, 0): Fraction(11, 10), (1, 0): Fraction(-2),
         (0, 1): Fraction(-2), (2, 0): Fraction(1),
         (1, 1): Fraction(2), (0, 2): Fraction(1)},
        {(0, 0): Fraction(1, 5), (1, 1): Fraction(3, 10)},
    ]
    # Respectively .05+(z1-.5)^2+.2*z2*(1-z2),
    # .1+(z1+z2-1)^2, and .2+.3*z1*z2.
    declared_minima = [.05, .1, .2]
    for degree in range(2, 101):
        coefficients = [bernstein_coefficients(p, degree) for p in polys]
        if min(c for table in coefficients for c in table.values()) > 0:
            break
    else:
        raise AssertionError("No positive elevation found")
    constant_c = max(float(c) for table in coefficients for c in table.values())
    max_identity_error, max_coefficient_bound_excess = 0., 0.
    coefficient_floors = []
    for poly, table in zip(polys, coefficients):
        cp = .5 * sum(float(abs(a)) * sum(ai * (ai - 1) for ai in alpha)
                      for alpha, a in poly.items())
        for k, coefficient in table.items():
            value = polynomial_value(poly, (k[0] / degree, k[1] / degree))
            max_coefficient_bound_excess = max(max_coefficient_bound_excess,
                                               abs(float(coefficient) - value) - cp / degree)
        coefficient_floors.append(float(min(table.values())))
    for z in product(np.linspace(0, 1, 13), repeat=2):
        marginal0 = binom.pmf(np.arange(degree + 1), degree, z[0])
        marginal1 = binom.pmf(np.arange(degree + 1), degree, z[1])
        actual_masses = []
        ideal_values = []
        for poly, table in zip(polys, coefficients):
            mean_c = sum(float(c) * marginal0[k[0]] * marginal1[k[1]]
                         for k, c in table.items())
            true_p = polynomial_value(poly, z)
            max_identity_error = max(max_identity_error, abs(mean_c - true_p))
            actual_masses.append(mean_c / (3 * constant_c))
            ideal_values.append(true_p)
        actual_law = np.array(actual_masses) / sum(actual_masses)
        ideal_law = np.array(ideal_values) / sum(ideal_values)
        assert np.max(np.abs(actual_law - ideal_law)) < 1e-12
    assert max_identity_error < 1e-12
    assert max_coefficient_bound_excess < 1e-12
    return {"first_strictly_positive_tensor_degree": degree,
            "number_of_coefficients": len(polys) * (degree + 1) ** 2,
            "minimum_coefficients": coefficient_floors,
            "maximum_coefficient": constant_c,
            "certified_acceptance_lower_bound": sum(declared_minima) / (3 * constant_c),
            "max_bernstein_identity_error": max_identity_error,
            "max_coefficient_bound_excess": max_coefficient_bound_excess}


def trace_distance(a, b):
    return float(np.sum(np.abs(np.linalg.eigvalsh(a - b))) / 2)


def terminal_depolarize(state, contraction):
    tensor = state.reshape(2, 2, 2, 2)
    rho_a = np.einsum("ijkj->ik", tensor)
    rho_b = np.einsum("ijil->jl", tensor)
    eye2 = np.eye(2) / 2
    return (contraction ** 2 * state
            + contraction * (1 - contraction)
            * (np.kron(rho_a, eye2) + np.kron(eye2, rho_b))
            + (1 - contraction) ** 2 * np.eye(4) / 4)


def dimer_checks():
    rng = np.random.default_rng(731)
    singlet = np.array([0, 1, -1, 0], dtype=complex) / math.sqrt(2)
    psi = np.outer(singlet, singlet.conj())
    eye4 = np.eye(4) / 4
    rho = lambda t: (1 - t) * eye4 + t * psi
    rows, min_random_gap, max_attainment_error = [], float("inf"), 0.
    for contraction, target_t in product([0., .2, .5, .8, 1.], [0., .1, .4, .7, 1.]):
        floor = .75 * max(0., target_t - contraction ** 2)
        input_s = min(1., target_t / contraction ** 2) if contraction else 0.
        result = terminal_depolarize(rho(input_s), contraction)
        actual = trace_distance(rho(target_t), result)
        max_attainment_error = max(max_attainment_error, abs(actual - floor))
        assert abs(actual - floor) < 1e-12
        for _ in range(100):
            g = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
            state = g @ g.conj().T
            state /= np.trace(state)
            gap = trace_distance(rho(target_t), terminal_depolarize(state, contraction)) - floor
            min_random_gap = min(min_random_gap, gap)
            assert gap > -1e-12
        rows.append({"lambda": contraction, "target_t": target_t,
                     "attaining_preimage_s": input_s,
                     "certified_floor": floor, "attained_distance": actual})
    ppt_rows = []
    for t in [0., 1 / 3, .4, .8, 1.]:
        partial_transpose = rho(t).reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)
        min_eigenvalue = float(np.linalg.eigvalsh(partial_transpose)[0])
        assert abs(min_eigenvalue - (1 - 3 * t) / 4) < 1e-12
        ppt_rows.append({"t": t, "partial_transpose_min_eigenvalue": min_eigenvalue})
    return {"attainment_grid": rows, "max_attainment_error": max_attainment_error,
            "random_state_trials": 2500, "minimum_random_gap_above_floor": min_random_gap,
            "separability_threshold_check": ppt_rows,
            "caution": "The analytic twirling proof establishes optimality; random trials are only sanity checks."}


def main():
    result = {"purpose": "Deterministic checks of finite mathematical constructions",
              "geometry": geometry_checks(),
              "scalar_race": scalar_race_checks(),
              "positive_bernstein": positive_bernstein_checks(),
              "dimer": dimer_checks()}
    output = HERE / "verification_results.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    compact = {
        "output": str(output),
        "geometry_max_residual": result["geometry"]["max_linear_residual"],
        "geometry_min_weight": result["geometry"]["observed_min_weight"],
        "bernstein_degree": result["positive_bernstein"]["first_strictly_positive_tensor_degree"],
        "bernstein_max_identity_error": result["positive_bernstein"]["max_bernstein_identity_error"],
        "scalar_per_output_error_bound": result["scalar_race"]["finite_demonstration"]["per_output_error_bound"],
        "scalar_assays_per_output": result["scalar_race"]["finite_demonstration"]["assays_per_output_deadline"],
        "dimer_attainment_error": result["dimer"]["max_attainment_error"],
    }
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
