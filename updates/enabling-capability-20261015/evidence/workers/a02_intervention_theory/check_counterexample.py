#!/usr/bin/env python3
"""Exact nonlinear calibration obstruction and bounded synthetic replay.

Only Python's standard library is required. This is a mathematical audit;
the generated traces are not measurements of a physical specimen.
"""

from fractions import Fraction as F
import json
import math
from pathlib import Path
import random
import time


PSI = [F(0), F(4888, 2039), F(-27951, 2039), F(83314, 2039),
       F(-97020, 2039), F(38808, 2039)]


def multiply(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return out


def integrate_unit(p):
    return sum((c / (i + 1) for i, c in enumerate(p)), F(0))


def evaluate(p, x):
    y = 0
    for c in reversed(p):
        y = y * x + c
    return y


PSI_FLOAT = list(map(float, PSI))


def psi(x):
    return evaluate(PSI_FLOAT, x)


def inverse_psi(y):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if psi(mid) < y:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def exact_checks():
    # Let u=(2x-1)^2. psi'(x) = A(u-v)^2 + minimum.
    a, v, minimum = F(24255, 4078), F(89, 210), F(34469, 81560)
    u = [F(1), F(-4), F(4)]
    umv = u.copy()
    umv[0] -= v
    complete_square = [a * c for c in multiply(umv, umv)]
    complete_square[0] += minimum
    derivative = [(i + 1) * PSI[i + 1] for i in range(len(PSI) - 1)]
    assert complete_square == derivative
    assert minimum > 0 and 0 < v < 1
    assert evaluate(PSI, F(0)) == 0
    assert evaluate(PSI, F(1)) == 1
    assert integrate_unit(PSI) == F(1, 2)
    assert integrate_unit(multiply(PSI, PSI)) == F(1, 3)
    target_a = F(1, 4)
    target_b = evaluate(PSI, target_a)
    assert target_b == F(55777, 260992)
    return {
        "status": "EXACT_RATIONAL_IDENTITIES_PASS",
        "coefficients_ascending": list(map(str, PSI)),
        "endpoints": ["0", "1"],
        "reference_mean_both_models": "1/2",
        "reference_second_moment_both_models": "1/3",
        "reference_variance_both_models": "1/12",
        "derivative_global_minimum": str(minimum),
        "target_a": str(target_a),
        "target_b": str(target_b),
        "target_b_decimal": float(target_b),
        "absolute_target_separation": float(target_a - target_b),
        "relative_target_separation": float((target_a - target_b) / target_a),
        "two_model_minimax_absolute_error_lower_bound": float((target_a - target_b) / 2),
    }


def adaptive_replay(n=2000, seed=20261015):
    rng = random.Random(seed)
    previous_a = previous_b = 0.5
    max_error = 0.0
    commands_equal = True
    for i in range(n):
        # Periodic reference command delivers Uniform[0,1] in model A.
        command_a = 0 if i % 7 == 0 else (1 if previous_a < 0.5 else -1)
        command_b = 0 if i % 7 == 0 else (1 if previous_b < 0.5 else -1)
        commands_equal &= command_a == command_b
        assert command_a == command_b
        delivered_a = rng.betavariate(1 + command_a / 2, 1 - command_a / 2)
        delivered_b = psi(delivered_a)
        assay_noise = rng.gauss(0, 0.03)
        previous_a = delivered_a + assay_noise
        previous_b = inverse_psi(delivered_b) + assay_noise
        max_error = max(max_error, abs(previous_a - previous_b))
    assert max_error < 1e-11
    return {
        "status": "SYNTHETIC_COUPLED_REPLAY_PASS",
        "trials": n,
        "seed": seed,
        "assay_noise_standard_deviation": 0.03,
        "identical_adaptive_commands": commands_equal,
        "maximum_floating_point_output_discrepancy": max_error,
        "interpretation": "Numerical illustration of an exact equality in law, not empirical evidence for a physical intervention.",
    }


def uniform_cdf(x, lo, hi):
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))


def sharp_interval_witness(theta):
    """Positive-density moment-matched law with F(theta)=1/4.

    Uses uniform bumps for an elementary numerical witness. THEORY.txt
    gives the smooth-bump version, with the same moment algebra.
    """
    assert 0 < theta < 2 / 3
    p, mu, m2 = 0.25, 0.5, 1 / 3
    gap = 2 / 3 - theta
    low_mean = min(theta / 8, gap * gap / 64, 0.01)
    diffuse_weight = low_mean / 100
    low_weight = (p - diffuse_weight * theta) / (1 - diffuse_weight)
    high_mean = (mu - low_weight * low_mean) / (1 - low_weight)
    residual = m2 - low_weight * low_mean**2 - (1 - low_weight) * high_mean**2
    provisional_s = math.sqrt(residual / (1 - low_weight))
    halfwidth = min(low_mean / 4, (theta - low_mean) / 4,
                    (high_mean - provisional_s - theta) / 4,
                    (1 - high_mean - provisional_s) / 4)
    assert halfwidth > 0
    split = math.sqrt((residual - halfwidth**2 / 3) / (1 - low_weight))
    centers = [low_mean, high_mean - split, high_mean + split]
    component_weights = [low_weight, (1 - low_weight) / 2, (1 - low_weight) / 2]
    assert 0 < centers[0] - halfwidth < centers[0] + halfwidth < theta
    assert theta < centers[1] - halfwidth < centers[2] + halfwidth < 1
    mean = diffuse_weight / 2 + (1 - diffuse_weight) * sum(
        w * c for w, c in zip(component_weights, centers))
    second = diffuse_weight / 3 + (1 - diffuse_weight) * sum(
        w * (c*c + halfwidth**2 / 3) for w, c in zip(component_weights, centers))
    cdf_at_theta = diffuse_weight * theta + (1 - diffuse_weight) * sum(
        w * uniform_cdf(theta, c - halfwidth, c + halfwidth)
        for w, c in zip(component_weights, centers))
    assert abs(mean - mu) < 1e-14
    assert abs(second - m2) < 1e-14
    assert abs(cdf_at_theta - p) < 1e-14
    return {
        "theta": theta,
        "mean": mean,
        "second_moment": second,
        "cdf_at_theta": cdf_at_theta,
        "strictly_positive_density_lower_bound": diffuse_weight,
        "uniform_bump_centers": centers,
        "uniform_bump_halfwidth": halfwidth,
        "component_weights_before_diffuse_mixture": component_weights,
    }


def main():
    start = time.perf_counter()
    results = {
        "status": "MATHEMATICAL_OBSTRUCTION_REPLAYED_NO_PHYSICAL_CAPABILITY_CLAIM",
        "exact_polynomial": exact_checks(),
        "adaptive_replay": adaptive_replay(),
        "sharp_interval_closure": [0, 2 / 3],
        "sharp_interval_witnesses": [sharp_interval_witness(t)
            for t in (0.001, 0.01, 0.1, 0.25, 0.5, 0.6, 0.65, 0.666)],
        "inference_tokens": "UNKNOWN",
        "inference_cost": "UNKNOWN",
        "inference_energy": "UNKNOWN",
        "measured_physical_specimens": 0,
    }
    results["executed_code_wall_seconds"] = time.perf_counter() - start
    output = Path(__file__).with_name("results.json")
    output.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"output": str(output), "status": results["status"],
                      "target_b": results["exact_polynomial"]["target_b_decimal"],
                      "wall_seconds": results["executed_code_wall_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
