"""Finite exact envelope/implementation checks; no empirical exact-law claim."""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import json
import platform
import resource
import time

import factory


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def main():
    started = time.perf_counter()
    n = factory.START
    bounds = [factory.coefficient_envelope(n, k) for k in range(n + 1)]
    assert min(a for a, b in bounds) >= 0
    assert max(b for a, b in bounds) <= 1
    # A global analytic bound validates later coefficients, rather than finite
    # checks purporting to establish an infinite family.
    m2, m3 = F(297, 8), F(891, 2)
    safe_error = m2 / (8 * n) + factory.radius(n)
    assert safe_error < F(2, 15)
    assert factory.RADIUS_CONSTANT == 2 * (m2 + m3)
    assert F(7, 8) * factory.RADIUS_CONSTANT >= m2 + m3
    expected = n + 12 * factory.RADIUS_CONSTANT / isqrt(n)
    assert expected == F(44351, 32)

    # Exercise exact hypergeometric elevation across plateaux and transition.
    checks = []
    for k in [0, 512, 683, 1024, 1365, 1707, 2048, 2389, 2731, 3584, 4096]:
        center_old = factory.elevated_center(n, 4 * n, k)
        center_new = factory.center(4 * n, k)
        difference = abs(center_new - center_old)
        allowance = factory.radius(n) - factory.radius(4 * n)
        assert difference <= allowance
        weights = factory.refinement_weights(n, 4 * n, k)
        checks.append({"new_heads": k, "absolute_center_change": difference,
                       "allowed_change": allowance, "weights": weights})

    # Path coverage is explicit deterministic diagnostic data. It is not sampled
    # evidence for the ideal distribution or the a.s. stopping theorem.
    path_checks = []
    for nominal_heads, decisions in [(683, [0]), (171, [1]), (683, [2, 0])]:
        draws = 0
        def coin():
            nonlocal draws
            value = (draws % n) < nominal_heads
            draws += 1
            return value
        remaining = iter(decisions)
        trace = []
        answer = factory.factory_coin(coin, choose=lambda weights: next(remaining), trace=trace)
        assert draws == (n if len(decisions) == 1 else 4 * n)
        assert len(trace) == len(decisions)
        path_checks.append({"prescribed_decisions": decisions, "calls": draws,
                            "answer": answer, "levels": [t["degree"] for t in trace]})

    # Initial stop/continue identity: all finite words have continuation mass 2e.
    assert all(b - a == 2 * factory.radius(n) for a, b in bounds)
    result = {
        "status": "EXPLICIT_ORDINARY_FACTORY_IMPLEMENTED; SCOPED_EXACT_CHECKS_PASS; GENERAL_PROOF_REQUIRES_REVIEW",
        "n0": n, "D": factory.RADIUS_CONSTANT,
        "derivative_bounds": {"M2": m2, "Lip_second_derivative": m3},
        "initial_coefficient_min": min(a for a, b in bounds),
        "initial_coefficient_max": max(b for a, b in bounds),
        "initial_max_deviation_bound": safe_error,
        "initial_continue_probability": 2 * factory.radius(n),
        "later_continue_probability": F(1, 8),
        "expected_cheap_calls": expected,
        "raw_calls": 0,
        "scope": "Already classical persistent X; unlimited iid cheap proxy stream; p(z=0) on fixed plateaux. No physical service acquired.",
        "fixed_plateau_tv_radius_sufficient": F(1, 12),
        "expected_total_bit_complexity": "NOT_FINITE_FOR_THE_NAIVE_FULL_EXACT_SUM_IMPLEMENTATION under interior p: per-level Omega(n^2) bit work and geometric level probability 8^(-j). This is an implementation obstruction, not a Bernoulli-factory impossibility.",
        "initial_coefficients_checked": n + 1,
        "selected_hypergeometric_refinements": checks,
        "deterministic_path_checks": path_checks,
        "runtime": {"python": platform.python_version(),
                    "wall_s": time.perf_counter() - started,
                    "peak_rss_bytes_macos": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
    }
    path = Path(__file__).resolve().parent / "factory_verification_results.json"
    path.write_text(json.dumps(encode(result), indent=2) + "\n")
    print(json.dumps(encode({"status": result["status"], "expected_cheap_calls": expected,
                            "initial_continue_probability": result["initial_continue_probability"],
                            "implementation_cost_limit": result["expected_total_bit_complexity"],
                            "runtime": result["runtime"]}), indent=2))


if __name__ == "__main__":
    main()
