#!/usr/bin/env python3
"""Finite algebra checks for the conditional two-gate relay model.

This script checks identities in the written model and reproduces its explicit
counterexample/reliability numbers. It does not fit or simulate Drosophila.
All force variables are dimensionless unless independently calibrated.
"""

from __future__ import annotations

import json
import math


def margin(o: float, i: float, b: float, theta: float, *, m0: float,
           gamma: float, k: float, alpha: float, beta: float) -> float:
    m = m0 + gamma * o * i / (k + i)
    return alpha * m * math.sin(theta) - beta * b


def integrin_derivative(o: float, i: float, theta: float, *, gamma: float,
                        k: float, alpha: float, beta: float) -> float:
    return alpha * gamma * o * k * math.sin(theta) / (k + i) ** 2 - beta


def critical_cluster(i: float, theta: float, *, gamma: float, k: float,
                     alpha: float, beta: float) -> float:
    return beta * (k + i) ** 2 / (alpha * gamma * k * math.sin(theta))


def optimal_integrin(o: float, theta: float, *, gamma: float, k: float,
                     alpha: float, beta: float) -> float:
    return max(0.0, math.sqrt(alpha * gamma * o * k * math.sin(theta) / beta) - k)


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def normal_quantile(p: float) -> float:
    if not 0.0 < p < 1.0:
        raise ValueError("p must be strictly between 0 and 1")
    lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if normal_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def reliability_threshold(n: int, epsilon: float) -> float:
    return normal_quantile((1.0 - epsilon) ** (1.0 / n))


def main() -> None:
    # Same means; distinct weakest-cell outcomes in the named serial model.
    uniform = [(1.2, 1.0), (1.2, 1.0)]
    heterogeneous = [(2.2, 0.5), (0.2, 1.5)]
    force_reserves = {
        "uniform": [m - b for m, b in uniform],
        "heterogeneous": [m - b for m, b in heterogeneous],
    }
    assert math.isclose(sum(m for m, _ in uniform) / 2, 1.2)
    assert math.isclose(sum(m for m, _ in heterogeneous) / 2, 1.2)
    assert math.isclose(sum(b for _, b in uniform) / 2, 1.0)
    assert math.isclose(sum(b for _, b in heterogeneous) / 2, 1.0)
    assert min(force_reserves["uniform"]) > 0
    assert min(force_reserves["heterogeneous"]) < 0

    # Verify the derivative sign boundary for one arbitrary dimensionless
    # parameter tuple; these values are algebra fixtures, not biological fits.
    pars = dict(gamma=2.0, k=0.7, alpha=1.3, beta=0.4)
    theta = 0.8
    i = 0.9
    oc = critical_cluster(i, theta, **pars)
    deriv_below = integrin_derivative(0.99 * oc, i, theta, **pars)
    deriv_above = integrin_derivative(1.01 * oc, i, theta, **pars)
    assert deriv_below < 0 < deriv_above
    i_star = optimal_integrin(2.0 * oc, theta, **pars)
    # Interior optimum: derivative is zero at I_star.
    assert i_star > 0
    assert abs(integrin_derivative(2.0 * oc, i_star, theta, **pars)) < 1e-12

    reliability = {}
    for n in (7, 20):
        z = reliability_threshold(n, 0.05)
        p_n = normal_cdf(z) ** n
        assert abs(p_n - 0.95) < 1e-12
        reliability[str(n)] = {"z_required": z, "joint_success": p_n}

    # Verify the conditional fold formulas at a point on the analytic curve.
    y = 0.4
    beta_fold = (1 + y * y) ** 2 / (2 * y)
    h_fold = y * (1 - y * y) / 2
    rhs = h_fold + beta_fold * y * y / (1 + y * y) - y
    derivative = 2 * beta_fold * y / (1 + y * y) ** 2 - 1
    assert abs(rhs) < 1e-14
    assert abs(derivative) < 1e-14

    print(json.dumps({
        "scope": "finite algebra checks only; no biological parameter fitting",
        "mean_matched_reserves": force_reserves,
        "integrin_sign_switch": {
            "critical_cluster_fixture": oc,
            "d_delta_dI_below": deriv_below,
            "d_delta_dI_above": deriv_above,
            "interior_optimum_fixture": i_star,
        },
        "iid_normal_reliability": reliability,
        "hill_fold_fixture": {"y": y, "beta": beta_fold, "h": h_fold},
        "checks": "PASS",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
