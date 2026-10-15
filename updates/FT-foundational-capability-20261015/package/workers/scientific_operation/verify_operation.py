#!/usr/bin/env python3
"""Conditional optics fixtures. No laboratory measurement is generated here.

The optimizer sees only a two-power scalar loss oracle. A supplied random unitary
is used inside that oracle and for final validation; its acquisition is not free
experimental evidence. Run from any directory; output stays beside this script.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import platform
import time

import numpy as np


def rational_text(x):
    return f"{x.numerator}/{x.denominator}"


def cavity(k_external, k_background, k_target):
    denominator = (k_external + k_background + k_target) ** 2
    return {
        "total_absorption": 4 * k_external * (k_background + k_target) / denominator,
        "target_absorption": 4 * k_external * k_target / denominator,
        "background_absorption": 4 * k_external * k_background / denominator,
    }


def scalar_oracle_fixture(n=8, low_saturation=0.1, high_saturation=1.0, beta=0.01, seed=20261015):
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    unitary, _ = np.linalg.qr(raw)
    evaluations = 0

    def unpack(z):
        u = z[:n] + 1j * z[n:]
        return u / np.linalg.norm(u)

    def score(z):
        nonlocal evaluations
        evaluations += 1
        intensities = np.abs(unitary @ unpack(z)) ** 2
        # Two normalized total-loss measurements. The constant linear loss
        # cancels. Both interrogation powers are strictly positive.
        low_loss = beta * np.sum(intensities / (1 + low_saturation * intensities)) + 0.02
        high_loss = beta * np.sum(intensities / (1 + high_saturation * intensities)) + 0.02
        return float((low_loss - high_loss) / beta)

    z = rng.normal(size=2 * n)
    z /= np.linalg.norm(z)
    initial = score(z)
    trace = [initial]
    h = 1e-5
    iterations = 0
    for iterations in range(1, 501):
        gradient = np.empty(2 * n)
        for j in range(2 * n):
            delta = np.zeros(2 * n)
            delta[j] = h
            gradient[j] = (score(z + delta) - score(z - delta)) / (2 * h)
        gradient -= z * np.dot(z, gradient)
        if np.linalg.norm(gradient) < 1e-8:
            break
        step = 1.0
        current = trace[-1]
        accepted = False
        for _ in range(30):
            candidate = z + step * gradient
            candidate /= np.linalg.norm(candidate)
            value = score(candidate)
            if value > current:
                z = candidate
                trace.append(value)
                accepted = True
                break
            step *= 0.5
        if not accepted:
            break
    x = np.abs(unitary @ unpack(z)) ** 2
    optimum = 1 / (1 + low_saturation) - 1 / (1 + high_saturation)
    uniform = 1 / (1 + low_saturation / n) - 1 / (1 + high_saturation / n)
    convexity_quantity = (low_saturation * high_saturation) ** (1 / 3) * (
        low_saturation ** (1 / 3) + high_saturation ** (1 / 3)
    )
    return {
        "model_status": "SUPPLIED_IDEAL_UNITARY_SIMULATION_ONLY",
        "n": n,
        "low_saturation": low_saturation,
        "high_saturation": high_saturation,
        "convexity_sufficient_quantity": convexity_quantity,
        "beta": beta,
        "seed": seed,
        "unitary_error": float(np.linalg.norm(unitary.conj().T @ unitary - np.eye(n))),
        "initial_score_div_beta": initial,
        "final_score_div_beta": trace[-1],
        "proved_maximum_div_beta": optimum,
        "uniform_score_div_beta": uniform,
        "final_largest_intensity_fraction": float(np.max(x)),
        "iterations": iterations,
        "scalar_score_evaluations": evaluations,
        "two_power_exposures": 2 * evaluations,
        "final_intensities": [float(v) for v in x],
        "trace": trace,
    }


def main():
    start = time.perf_counter()
    before = cavity(F(1), F(2), F(0))
    after = cavity(F(1), F(2), F(1))
    assert after["total_absorption"] - before["total_absorption"] == -F(5, 36)
    assert after["target_absorption"] == F(1, 4)
    assert before["total_absorption"] == F(8, 9)
    # At background critical coupling, any positive target loss reduces total
    # absorption: A(t)=1-t^2/(2+t)^2. The first derivative at zero is zero.
    critical_t = F(1, 100)
    critical = cavity(F(1), F(1), critical_t)
    assert critical["total_absorption"] == 1 - critical_t**2 / (2 + critical_t)**2
    # Different delivered powers defeat a focus interpretation of the score.
    f = lambda x: x * x / (1 + x)
    diffuse_score = 2 * f(F(1, 2))
    weak_focus_score = f(F(1, 10))
    assert diffuse_score == F(1, 3)
    assert weak_focus_score == F(1, 110)
    fixtures = [scalar_oracle_fixture(n=n) for n in (8, 16)]
    for fixture in fixtures:
        assert fixture["unitary_error"] < 1e-12
        assert fixture["convexity_sufficient_quantity"] < 1
        assert fixture["final_score_div_beta"] <= fixture["proved_maximum_div_beta"] + 1e-12
        assert fixture["final_largest_intensity_fraction"] > 0.999
        assert all(b >= a for a, b in zip(fixture["trace"], fixture["trace"][1:]))
    result = {
        "status": "MODEL_FIXTURES_PASS_NO_PHYSICAL_OR_NOVELTY_CLAIM",
        "python": platform.python_version(),
        "numpy": np.__version__,
        "cavity_counterexample": {
            "external_rate": "1/1",
            "background_rate": "2/1",
            "target_rate_before": "0/1",
            "target_rate_after": "1/1",
            "before": {k: rational_text(v) for k, v in before.items()},
            "after": {k: rational_text(v) for k, v in after.items()},
            "total_absorption_change": "-5/36",
            "interpretation": "Adding target absorption decreases the total loss flag probability.",
        },
        "critical_coupling_counterexample": {
            "external_and_background_rates": "1/1",
            "total_absorption_function": "1 - t^2/(2+t)^2",
            "target_absorption_function": "4t/(2+t)^2",
            "total_first_derivative_at_zero": "0/1",
            "target_first_derivative_at_zero": "1/1",
        },
        "variable_delivery_counterexample": {
            "diffuse_intensities": ["1/2", "1/2", "0/1"],
            "focused_intensities": ["0/1", "0/1", "1/10"],
            "diffuse_deficit_div_beta": rational_text(diffuse_score),
            "weak_focused_deficit_div_beta": rational_text(weak_focus_score),
            "diffuse_to_focused_score_ratio": rational_text(diffuse_score / weak_focus_score),
        },
        "optimizer_fixtures": fixtures,
        "elapsed_seconds": time.perf_counter() - start,
        "physical_evidence": "NONE_EXECUTED",
        "priority": "UNKNOWN",
    }
    destination = Path(__file__).with_name("verification_results.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "optimizer_fixtures"}, indent=2))
    for fixture in fixtures:
        print(json.dumps({k: v for k, v in fixture.items() if k not in ("trace", "final_intensities")}, indent=2))


if __name__ == "__main__":
    main()
