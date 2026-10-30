"""Finite numerical evidence for the hard-control Gaussian sensing theorem.

Prior geometry: unequal-dimensional Grassmann quantization, Dai/Rider/Liu.
This script tests formulas and a replay fixture, not historical novelty.
"""

import json
import math
import time
import numpy as np
from scipy.integrate import quad
from scipy.special import betainc, betaincinv, gammaln


def cap_bounds(m, q, bits):
    assert isinstance(bits, int) and bits >= 0
    assert 0 <= q <= m
    if q == 0:
        return {"lower": 1.0, "random_code_upper": 1.0}
    if q == m:
        return {"lower": 0.0, "random_code_upper": 0.0}
    a, b = (m - q) / 2.0, q / 2.0
    if bits == 0:
        return {"lower": (m - q) / m, "random_code_upper": (m - q) / m}
    n = math.ldexp(1.0, bits)
    cutoff = float(betaincinv(a, b, 1.0 / n))
    lower = n * a / (a + b) * float(betainc(a + 1, b, cutoff))

    def survival(x):
        f = float(betainc(a, b, x))
        if f <= 0:
            return 1.0
        if f >= 1:
            return 0.0
        exponent = n * math.log1p(-f)
        return math.exp(exponent) if exponent > -745 else 0.0

    quantiles = [1e-5, 1e-3, 0.1, 1.0, 3.0, 10.0, 30.0]
    points = sorted(set(float(betaincinv(a, b, t / n))
                        for t in quantiles if t < n))
    upper, error = quad(survival, 0.0, 1.0, points=points,
                        epsabs=1e-11, epsrel=1e-10, limit=250)
    assert lower <= upper + 1e-9
    assert upper <= (m - q) / m + 1e-9
    return {"lower": lower, "random_code_upper": upper,
            "cap_cutoff": cutoff, "quadrature_reported_absolute_error": error}


def analytic_special_cases():
    checks = []
    for bits in (0, 1, 2, 4, 6, 8):
        n = 2 ** bits
        for m in (3, 4, 8, 16):
            a = (m - 2) / 2
            actual = cap_bounds(m, 2, bits)
            low = a / (a + 1) * n ** (-1 / a)
            up = math.exp(gammaln(n + 1) + gammaln(1 + 1 / a)
                          - gammaln(n + 1 + 1 / a))
            assert abs(actual["lower"] - low) < 2e-10
            assert abs(actual["random_code_upper"] - up) < 2e-10
            checks.append({"m": m, "q": 2, "B": bits, "valid": True})
        actual = cap_bounds(2, 1, bits)
        exact = 0.5 - n * math.sin(math.pi / n) / (2 * math.pi)
        assert abs(actual["lower"] - exact) < 2e-10
        actual3 = cap_bounds(3, 1, bits)
        assert abs(actual3["lower"] - (1 / n - 1 / (3 * n * n))) < 2e-10
        assert abs(actual3["random_code_upper"] - 2 / (n + 2)) < 2e-10
    return {"q2_cases": checks, "circle_exact_optimum_cases": 6,
            "m3_q1_beta_closed_form_cases": 6, "all_passed": True}


def interleaved_fixture(samples=120000, seed=77741):
    """B=1,q=2,m=4. Second candidate directions depend on first V readout.

    First read is V0. Based on it, actuator has two orthogonal directions
    rotated within the remaining 3-space. Controller picks one by a bit.
    Bayes prediction uses U and both exact readings. Replay enumerates the
    two choices using V alone; actual span must be one of those choices.
    """
    rng = np.random.default_rng(seed)
    u, v = rng.normal(size=(2, samples, 4))
    y = v[:, 0]
    theta = np.arctan(y)
    cs, sn = np.cos(theta), np.sin(theta)
    # a0=(0,cos(theta),sin(theta),0), a1=(0,0,0,1).
    ua0 = cs * u[:, 1] + sn * u[:, 2]
    ua1 = u[:, 3]
    bit = ua1 * ua1 > ua0 * ua0
    va0 = cs * v[:, 1] + sn * v[:, 2]
    va1 = v[:, 3]
    uc = np.where(bit, ua1, ua0)
    z = np.where(bit, va1, va0)
    prediction = (u[:, 0] * y + uc * z) / 2
    target = np.sum(u * v, axis=1) / 2
    conditional_error = (np.sum(u * u, axis=1) - u[:, 0] ** 2 - uc ** 2) / 4
    replay_min = (np.sum(u * u, axis=1) - u[:, 0] ** 2
                  - np.maximum(ua0 ** 2, ua1 ** 2)) / 4
    assert np.max(np.abs(conditional_error - replay_min)) < 1e-12
    exact_risk = 1 - (2 + 2 / math.pi) / 4
    empirical = np.mean((target - prediction) ** 2)
    standard_error = np.std((target - prediction) ** 2, ddof=1) / math.sqrt(samples)
    assert abs(empirical - exact_risk) <= 6 * standard_error
    # An ordinary fixed 2-plane codebook with disjoint coordinate planes is
    # optimal here: its distortion 1/4 equals the beta-cap lower bound.
    best_fixed_codebook_risk = 0.25
    assert abs(cap_bounds(4, 2, 1)["lower"] - best_fixed_codebook_risk) < 1e-12
    return {"m": 4, "q": 2, "B": 1, "samples": samples,
            "genuine_readout_dependent_directions": True,
            "actual_span_equals_a_replayed_span": True,
            "exact_fixture_risk": exact_risk,
            "empirical_MSE": float(empirical),
            "MSE_standard_error": float(standard_error),
            "mean_conditional_risk": float(np.mean(conditional_error)),
            "optimal_noninteractive_codebook_risk": best_fixed_codebook_risk,
            "scope": "One seeded diagnostic; the interactive equivalence is proved separately."}


def tables():
    rows = []
    for m, q in ((16, 1), (16, 4), (128, 1), (128, 8), (128, 32)):
        for bits in (0, 8, 32, 64, 128, 256, 512):
            item = {"m": m, "q": q, "B": bits, **cap_bounds(m, q, bits)}
            rows.append(item)
    m, s = 128, 0.01
    alpha2 = 1 / (1 + s) ** 2
    noisy = []
    for bits in (0, 32, 64, 127, 128, 256, 420, 512):
        bounds = cap_bounds(m, 1, bits)
        noisy.append({"m": m, "total_linear_reads": m + 1,
                      "noise_variance_each_read": s, "B": bits,
                      "optimal_risk_lower": 1 - alpha2 + alpha2 * bounds["lower"],
                      "random_code_risk_upper": 1 - alpha2 + alpha2 * bounds["random_code_upper"]})
    sign_risk = (1 - 1 / m) * (1 - 2 / math.pi)
    return {"finite_cap_sandwiches": rows, "noisy_one_read_control": noisy,
            "sign_code": {"m": m, "B": m - 1, "q": 1,
                          "exact_noiseless_risk": sign_risk,
                          "exact_equal_noise_risk": 1 - alpha2 + alpha2 * sign_risk},
            "resource_scope": "Random code upper bounds are not efficient codebook implementations; no exponential codebook is built."}


if __name__ == "__main__":
    start = time.perf_counter()
    result = {"special_case_checks": analytic_special_cases(),
              "interactive_replay_fixture": interleaved_fixture(),
              **tables()}
    result["wall_seconds"] = time.perf_counter() - start
    print(json.dumps(result, indent=2))
