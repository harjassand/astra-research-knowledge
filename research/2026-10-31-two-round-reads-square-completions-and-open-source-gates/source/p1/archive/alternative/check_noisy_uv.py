"""Finite independent checks of the all-noisy UV construction and comparator."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np


def grid(d):
    nodes = (-np.sqrt(3.0), 0.0, np.sqrt(3.0))
    weights = (1/6, 2/3, 1/6)
    for indices in product(range(3), repeat=d):
        yield (np.array([nodes[i] for i in indices]),
               np.prod([weights[i] for i in indices]))


def conditional_mse(y, s):
    m = len(y)
    alpha = 1 / (1 + s)
    ynorm = np.linalg.norm(y)
    w = y / ynorm if ynorm > 1e-10 else np.eye(m)[0]
    v_sqrt_cov = np.eye(m) + (np.sqrt(1-alpha)-1)*np.outer(w, w)
    answer = 0.0
    for values, weight in grid(2*m+1):
        z = np.sqrt(1+s)*values[-1]
        u = alpha*y + np.sqrt(1-alpha)*values[:m]
        v = alpha*w*z + v_sqrt_cov @ values[m:2*m]
        prediction = alpha**2 * ynorm * z / np.sqrt(m)
        answer += weight * (u@v / np.sqrt(m)-prediction)**2
    formula = (1-alpha)*(1+alpha**2*ynorm**2/m)
    return float(answer), float(formula)


def target_matrix(m):
    a = np.zeros((2*m, 2*m))
    a[:m, m:] = np.eye(m)/(2*np.sqrt(m))
    a[m:, :m] = np.eye(m)/(2*np.sqrt(m))
    return a


def fixed_gain(a, measurements, s):
    h = measurements.T @ measurements
    p = np.linalg.solve(h+s*np.eye(len(a)), h)
    return float(2*np.trace(a@p@a@p))


def main():
    rng = np.random.default_rng(20261030)
    out = dict(seed=20261030, conditional_quadrature_checks=0,
               rational_tangent_checks=0, fixed_design_bound_checks=0,
               fixed_optimum_attainment_checks=0,
               max_quadrature_absolute_error=0.0,
               max_attainment_absolute_error=0.0)
    for s in (F(1,100), F(1,5), F(1,1)):
        for t in (F(0), F(1,100), F(1,4), F(1), F(3,2), F(2), F(9)):
            lhs = 1/(s+1)**2 + (t-1)*2*s/(s+1)**3 - t*t/(s+t)**2
            rhs = s*(t-1)**2*(2*t+s-s*s)/((1+s)**3*(s+t)**2)
            assert lhs == rhs and rhs >= 0
            out["rational_tangent_checks"] += 1
    for m in (1,2,3):
        for s in (0.01,0.2,1.0):
            for y in (np.zeros(m), rng.normal(size=m), 3*rng.normal(size=m)):
                measured, formula = conditional_mse(y, s)
                error = abs(measured-formula)
                out["max_quadrature_absolute_error"] = max(
                    out["max_quadrature_absolute_error"], error)
                assert error < 1e-10*(1+formula)
                out["conditional_quadrature_checks"] += 1
    for m in (1,2,3,4,5):
        a = target_matrix(m)
        _, vectors = np.linalg.eigh(a)
        for s in (0.01,0.2,1.0):
            for q in range(1,2*m+1):
                bound = q / (2*m*(1+s)**2)
                for _ in range(3):
                    measurements = rng.normal(size=(q,2*m))
                    measurements /= np.linalg.norm(measurements,axis=1,keepdims=True)
                    gain = fixed_gain(a,measurements,s)
                    assert gain <= bound+1e-10
                    out["fixed_design_bound_checks"] += 1
                repeated = np.repeat(vectors[:, :1].T,q,axis=0)
                assert fixed_gain(a,repeated,s) <= bound+1e-10
                out["fixed_design_bound_checks"] += 1
                attained = fixed_gain(a,vectors[:, :q].T,s)
                error = abs(attained-bound)
                out["max_attainment_absolute_error"] = max(
                    out["max_attainment_absolute_error"], error)
                assert error < 1e-10
                out["fixed_optimum_attainment_checks"] += 1
    a = target_matrix(1)
    _, vectors = np.linalg.eigh(a)
    repeat = np.repeat(vectors[:, :1].T,2,axis=0)
    out["noise_2_scope_counterexample"] = dict(
        repeated_two_gain=fixed_gain(a,repeat,2.0),
        orthogonal_two_gain=fixed_gain(a,vectors.T,2.0))
    assert out["noise_2_scope_counterexample"]["repeated_two_gain"] > out[
        "noise_2_scope_counterexample"]["orthogonal_two_gain"]
    m,s=128,0.01
    alpha=1/(1+s)
    out["example"] = dict(m=m,noise_variance=s,adaptive_read_count=m+1,
                          adaptive_risk=1-alpha**2,
                          best_fixed_same_count_risk=1-(m+1)*alpha**2/(2*m),
                          fixed_matching_count=2*m)
    out["status"]="PASS"
    Path(__file__).with_name("check_noisy_uv_results.json").write_text(
        json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__ == "__main__":
    main()
