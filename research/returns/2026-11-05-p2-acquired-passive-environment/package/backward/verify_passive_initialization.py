"""Numerical diagnostics for the passive initialization/comparison derivations.

The inequalities are proved in the companion Markdown notes. This script tests
their fragile constants and signs on a nonquadratic fixture with frozen, very
slow, intermediate, and fast hidden modes. It is not physical acquisition and
does not turn floating-point integration into a formal trajectory certificate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from numpy.polynomial import Chebyshev, Polynomial
from scipy.integrate import quad, solve_ivp


OUT = Path(__file__).resolve().parent


def chebyshev_power_diagnostics():
    cases = []
    chi = 3 + 2 * math.sqrt(2)
    u = np.linspace(0.0, 1.0, 20001)
    for m in (1, 2, 5, 12, 20):
        for beta in (float(m), m + 0.37, 1.7 * m, 3.0 * m):
            c = max(1.0, beta / m)
            a0 = math.exp(
                math.lgamma(2 * beta + 1)
                - 2 * beta * math.log(2)
                - 2 * math.lgamma(beta + 1)
            )
            aa = [a0]
            ak = 2 * a0
            for k in range(1, m + 1):
                ak *= (beta - (k - 1)) / (beta + k)
                aa.append(ak)
            ch = Chebyshev(aa, domain=[0, 1])
            err = float(np.max(np.abs(ch(u) - u**beta)))
            bound = c * math.exp(-m / (c + 1))
            mono = ch.convert(kind=Polynomial)
            l1 = float(np.abs(mono.coef).sum())
            l1_bound = 3 * chi**m
            assert err <= bound + 1e-11
            assert l1 <= l1_bound * (1 + 1e-11)
            cases.append(
                dict(m=m, beta=beta, error=err, error_bound=bound,
                     coefficient_l1=l1, coefficient_l1_bound=l1_bound)
            )
    return {
        "cases": cases,
        "largest_error_to_bound_ratio": max(v["error"] / v["error_bound"] for v in cases),
        "largest_coefficient_ratio": max(v["coefficient_l1"] / v["coefficient_l1_bound"] for v in cases),
    }


def passive_fixture():
    mu = 1.1
    quartic = 0.2
    rates = np.array([0.0, 1e-9, 1e-4, 0.03, 0.2, 1.0, 7.0, 80.0])
    weights = np.array([0.35, 0.25, 0.2, 0.25, 0.3, 0.2, 0.25, 0.2])
    old_hidden = np.array([1.1, -0.4, 1.0, -0.8, 0.3, 0.6, -0.2, 0.5])
    B = float(weights.sum())
    initial_energy = float(0.5 * np.dot(weights, old_hidden**2))
    G = math.sqrt(2 * B * initial_energy)
    true_tv = float(np.dot(weights, np.abs(old_hidden)))
    delta = 0.0015
    omega = 0.71
    H = 250.3
    bin_length = 0.8
    T = 4.0
    eta = 0.0003
    sensor_offset = 0.0002

    def potential_prime(x):
        return mu * x + quartic * x**3

    def hold_position(t):
        return delta * np.sin(omega * t)

    def hold_velocity(t):
        return delta * omega * np.cos(omega * t)

    def hidden_during_hold(t):
        decay = np.exp(-rates * t)
        driven = (
            delta * rates
            * (rates * np.sin(omega * t) - omega * np.cos(omega * t) + omega * decay)
            / (rates**2 + omega**2)
        )
        return decay * old_hidden + driven

    def bath_force(t):
        return float(np.dot(weights, hidden_during_hold(t) - hold_position(t)))

    def applied_hold_force(t):
        return hold_velocity(t) + potential_prime(hold_position(t)) - bath_force(t)

    bin_true = quad(bath_force, H-bin_length, H, epsabs=1e-12, epsrel=1e-12)[0] / bin_length
    bin_balance = (
        (hold_position(H) - hold_position(H-bin_length)) / bin_length
        + quad(lambda t: potential_prime(hold_position(t)) - applied_hold_force(t),
               H-bin_length, H, epsabs=1e-12, epsrel=1e-12)[0] / bin_length
    )
    assert abs(bin_true - bin_balance) < 1e-11
    c = bin_balance + sensor_offset
    drift_bound = G * (bin_length + T) / (math.e * (H-bin_length))
    gamma = eta + 3 * B * delta + drift_bound
    state_after_hold = hidden_during_hold(H)
    x_initial = float(hold_position(H))
    future_grid = np.linspace(0, T, 10001)
    g_ref = np.exp(-np.outer(future_grid, rates)) @ (weights * state_after_hold)
    g_error = float(np.max(np.abs(g_ref - c)))
    assert g_error <= gamma

    # Retain a finite positive surrogate and compute an analytic kernel L1
    # upper bound by summing exact one-mode ordered exponential errors.
    hat_rates = rates * np.array([1, 1.0, 1.01, 0.995, 1.004, 0.996, 1.003, 0.998])
    def exp_integral(rate):
        return T if rate == 0 else -math.expm1(-rate * T) / rate
    zeta = float(sum(w * abs(exp_integral(r)-exp_integral(h))
                     for w, r, h in zip(weights, rates, hat_rates)))
    dense_l1 = quad(lambda t: abs(float(np.dot(weights, np.exp(-rates*t)-np.exp(-hat_rates*t)))),
                    0, T, epsabs=1e-12, epsrel=1e-10)[0]
    assert dense_l1 <= zeta + 1e-11

    queries = []
    for name, amplitude, feedback_gain in [
        ("zero_drive", 0.0, 0.0),
        ("dc_drive", 0.8, 0.0),
        ("smooth_drive", 0.8, 0.0),
        ("separate_lipschitz_feedback", 0.3, 0.35),
    ]:
        F = amplitude + abs(feedback_gain)
        def force(t, x):
            if name == "dc_drive":
                base = amplitude
            elif name == "zero_drive":
                base = 0.0
            else:
                base = amplitude * math.sin(2.2*t) * math.cos(0.7*t)
            return base + feedback_gain * math.tanh(x)

        def rhs_true(t, state):
            x, yy = state[0], state[1:]
            return np.r_[ -potential_prime(x) - np.dot(weights, x-yy) + force(t, x),
                           rates * (x-yy) ]

        def rhs_hat(t, state):
            x, yy = state[0], state[1:]
            return np.r_[ -potential_prime(x) - np.dot(weights, x-yy) + force(t, x) + c,
                           hat_rates * (x-yy) ]

        true = solve_ivp(rhs_true, (0,T), np.r_[x_initial, state_after_hold],
                         method="Radau", rtol=2e-10, atol=2e-12, dense_output=True)
        hat = solve_ivp(rhs_hat, (0,T), np.zeros(1+len(weights)),
                        method="Radau", rtol=2e-10, atol=2e-12, dense_output=True)
        assert true.success and hat.success
        tt = np.linspace(0,T,4001)
        xt = true.sol(tt)
        xh = hat.sol(tt)
        error = float(np.max(np.abs(xt[0]-xh[0])))
        D0 = abs(c) / mu
        D = max(D0, F/mu)
        local_L = mu + 3*quartic*(D0+D)**2
        Dv = F + (local_L + 2*B)*D
        model_vel = np.array([rhs_hat(t, xh[:,i])[0] for i,t in enumerate(tt)])
        actual_model_speed = float(np.max(np.abs(model_vel)))
        bound = max(delta, (zeta*Dv + gamma)/(mu-feedback_gain))
        assert actual_model_speed <= Dv + 1e-10
        assert error <= bound + 1e-8
        queries.append(dict(
            name=name, force_budget=F, feedback_gain=feedback_gain,
            model_speed=actual_model_speed, model_speed_bound=Dv,
            trajectory_error=error, trajectory_bound=bound,
        ))

    return {
        "mu": mu, "B": B, "rates": rates.tolist(), "weights": weights.tolist(),
        "initial_energy": initial_energy, "old_force_tv": true_tv, "old_force_tv_bound": G,
        "hold_time": H, "bin_length": bin_length, "deployment_horizon": T,
        "tracking_delta": delta, "physical_initial_coordinate": x_initial,
        "bin_force_direct": bin_true, "bin_force_balance": bin_balance,
        "measured_constant": c, "force_readout_error_budget": eta,
        "drift_bound": drift_bound, "future_initial_force_error": g_error,
        "future_initial_force_bound": gamma,
        "kernel_l1_numerical": dense_l1, "kernel_l1_analytic_upper_bound": zeta,
        "frozen_initial_force": float(weights[0]*old_hidden[0]),
        "frozen_hidden_retention": 1.0,
        "slowest_positive_retention_after_hold": math.exp(-rates[1]*H),
        "queries": queries,
    }


if __name__ == "__main__":
    results = {
        "status": "all numerical diagnostics passed; proofs are in the notes",
        "chebyshev_initial_force_continuation": chebyshev_power_diagnostics(),
        "nonlinear_passive_fixture": passive_fixture(),
    }
    target = OUT / "passive_verification_results.json"
    target.write_text(json.dumps(results, indent=2) + "\n")
    fixture = results["nonlinear_passive_fixture"]
    print(json.dumps({
        "status": results["status"],
        "result_file": str(target),
        "force_error": fixture["future_initial_force_error"],
        "force_bound": fixture["future_initial_force_bound"],
        "kernel_l1_upper_bound": fixture["kernel_l1_analytic_upper_bound"],
        "slow_mode_retention": fixture["slowest_positive_retention_after_hold"],
        "queries": fixture["queries"],
    }, indent=2))
