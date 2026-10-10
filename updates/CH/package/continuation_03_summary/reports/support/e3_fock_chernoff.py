"""Floating-point diagnostic of an exact Fock-block Chernoff formula.

No capacity conclusion is certified by this script.  The analytic derivation
and rigorous tail formulas are in ../e3_closure.txt.  Run with plain Python
plus NumPy; no SciPy is required.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


def log_factorials(maximum):
    return np.array([math.lgamma(j + 1) for j in range(maximum + 1)])


def joint(n, delta, lost, eta, nu, logfac):
    gain = 1 + (1 - eta) * nu
    tau = eta / gain
    a = 1 - tau
    dd, ll = delta[:, None], lost[None, :]
    out = n + dd + np.zeros_like(ll)
    kk = dd + ll
    valid = (ll >= 0) & (ll <= n) & (kk >= 0) & (kk <= out)
    nml = np.maximum(0, n - ll)
    kval = np.maximum(0, kk)
    oval = np.maximum(0, out)
    lval = np.maximum(0, ll)
    logp = (
        logfac[n] - logfac[lval] - logfac[nml]
        + ll * math.log(a) + (n - ll) * math.log(tau)
        + logfac[oval] - logfac[kval] - logfac[nml]
        + kk * math.log(gain - 1) - (out + 1) * math.log(gain)
    )
    return np.where(valid, np.exp(np.where(valid, logp, -np.inf)), 0.0)


def moment_log_output(h, n, eta, nu):
    gain = 1 + (1 - eta) * nu
    tau = eta / gain
    den = gain - (gain - 1) * math.exp(h)
    if den <= 0:
        return float("inf")
    return -math.log(den) + n * math.log(1 - tau + tau * math.exp(h) / den)


def golden_minimum(fun, left, right, iterations=100):
    g = (math.sqrt(5) - 1) / 2
    a, b = left, right
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = fun(c), fun(d)
    for _ in range(iterations):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = fun(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = fun(d)
    return (a + b) / 2, min(fc, fd)


def chernoff_output_tail(boundary, n, eta, nu, upper):
    gain = 1 + (1 - eta) * nu
    if not upper and boundary < 0:
        return 0.0
    left, right = (0.0, math.log(gain / (gain - 1)) * (1 - 1e-12)) if upper else (-30.0, 0.0)
    _, value = golden_minimum(lambda h: moment_log_output(h, n, eta, nu) - h * boundary, left, right)
    return min(1.0, math.exp(value))


def binomial_tail(boundary, n, prob, upper):
    if (not upper and boundary < 0) or (upper and boundary > n):
        return 0.0
    left, right = (0.0, 30.0) if upper else (-30.0, 0.0)
    _, value = golden_minimum(
        lambda h: n * math.log(1 - prob + prob * math.exp(h)) - h * boundary,
        left, right,
    )
    return min(1.0, math.exp(value))


def calculation(n, eta, nu, radius=12.0):
    gain = 1 + (1 - eta) * nu
    tau = eta / gain
    loss = 1 - tau
    b = 1 - eta
    variance = eta * b * (2 * nu + 1)
    delta_mid = -b * n + gain - 1
    delta_radius = radius * math.sqrt(variance * n + gain * (gain - 1)) + 4
    lost_mid = loss * n
    lost_radius = radius * math.sqrt(loss * tau * n) + 4
    delta = np.arange(max(-n, math.floor(delta_mid - delta_radius)), math.ceil(delta_mid + delta_radius) + 1)
    lost = np.arange(max(0, math.floor(lost_mid - lost_radius)), min(n + 1, math.ceil(lost_mid + lost_radius)) + 1)
    logfac = log_factorials(2 * n + int(2 * delta_radius + 100))
    p = joint(n, delta, lost, eta, nu, logfac)
    q = joint(n + 1, delta, lost, eta, nu, logfac)
    q_same_output = joint(n + 1, delta - 1, lost, eta, nu, logfac)
    p_delta, q_delta = p.sum(axis=1), q.sum(axis=1)
    q_output = q_same_output.sum(axis=1)
    overlap_numerator = np.sqrt(p * q).sum(axis=1) ** 2
    good = (p_delta > 0) & (q_delta > 0)
    logpd, logqd = np.log(p_delta[good]), np.log(q_delta[good])
    logorientation = np.log(overlap_numerator[good]) - logpd - logqd
    good_b = (p_delta > 0) & (q_output > 0)
    logpout, logqout = np.log(p_delta[good_b]), np.log(q_output[good_b])

    def q_e(s):
        return float(np.exp(s * logpd + (1 - s) * logqd + logorientation).sum())

    def q_b(s):
        return float(np.exp(s * logpout + (1 - s) * logqout).sum())

    se, qe = golden_minimum(q_e, 0.0, 1.0)
    sb, qb = golden_minimum(q_b, 0.0, 1.0)
    qjoint_half = float(np.sqrt(p * q).sum())
    qclass_half = float(np.sqrt(p_delta * q_delta).sum())

    # A union bound on all omitted (l,delta) cells for each relevant law.
    tail_bounds = []
    for nn, ddshift in [(n, 0), (n + 1, 0), (n + 1, -1)]:
        outlo, outhi = nn + int(delta[0]) + ddshift, nn + int(delta[-1]) + ddshift
        tail_bounds.append(
            chernoff_output_tail(outlo - 1, nn, eta, nu, False)
            + chernoff_output_tail(outhi + 1, nn, eta, nu, True)
            + binomial_tail(int(lost[0]) - 1, nn, loss, False)
            + binomial_tail(int(lost[-1]) + 1, nn, loss, True)
        )
    return {
        "n": n, "eta": eta, "nu": nu,
        "n_C_B_float": -n * math.log(qb),
        "n_C_E_float": -n * math.log(qe),
        "s_B_float": sb, "s_E_float": se,
        "n_C_B_limit": eta / (8 * b * (2 * nu + 1)),
        "n_C_E_limit": b * (1 + 8 * nu * (nu + 1)) / (8 * eta * (2 * nu + 1)),
        "n_C_joint_half_float": -n * math.log(qjoint_half),
        "n_C_class_E_half_float": -n * math.log(qclass_half),
        "n_C_joint_limit": b * (2 * nu + 1) / (8 * eta),
        "n_C_class_E_limit": b / (8 * eta * (2 * nu + 1)),
        "largest_omission_probability_bound_float": max(tail_bounds),
        "mass_p_float": float(p.sum()), "mass_q_float": float(q.sum()),
    }


def main():
    results = [calculation(n, eta, 1.0) for eta in [0.75, 0.78, 0.8, 0.81] for n in [100, 400, 1600, 6400]]
    target = Path(__file__).with_name("e3_fock_chernoff_results.json")
    target.write_text(json.dumps({
        "status": "FLOATING_POINT_DIAGNOSTIC_NOT_A_CERTIFICATE",
        "nu1_asymptotic_threshold": math.sqrt(17) / (1 + math.sqrt(17)),
        "results": results,
    }, indent=2) + "\n")
    for result in results:
        print(json.dumps(result))


if __name__ == "__main__":
    main()
