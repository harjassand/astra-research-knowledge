"""Execute independent exact-distribution and enormous-index clock checks.

Run from any directory with Python 3.10+.  Only the standard library is used.
Exact rational target powers are deliberately restricted to small audit cases;
the sampler itself never computes them.  Large-case PRNG statistics are
diagnostics, while exact finite-distribution assertions and the proof provide
the accuracy guarantee.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import json
import math
from pathlib import Path
import platform
import random
import sys
import time


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "next4_execution"))
from finite_geometric import GeometricClockCompiler, sample_geometric, _ceil_log2_ratio


class CountingRandom(random.Random):
    def __init__(self, seed: int):
        self.bit_calls = 0
        self.bits_requested = 0
        super().__init__(seed)

    def getrandbits(self, k: int) -> int:
        self.bit_calls += 1
        self.bits_requested += k
        return super().getrandbits(k)


def fraction_record(value: Fraction) -> dict:
    result = {
        "decimal_approximation": float(value),
        "numerator_bits": value.numerator.bit_length(),
        "denominator_bits": value.denominator.bit_length(),
    }
    if max(value.numerator.bit_length(), value.denominator.bit_length()) <= 12000:
        result["exact_rational"] = str(value)
    else:
        result["numerator_hex"] = hex(value.numerator)
        result["denominator_hex"] = hex(value.denominator)
    return result


def exact_binary_tree_masses(clock: GeometricClockCompiler) -> list[Fraction]:
    """Count every B-bit input by exact decision-tree interval propagation.

    This visits at most O(M) leaves only in the small reference audit.  It
    neither enumerates the 2**B random-bit strings nor changes the sampler.
    """
    number_uniforms = 1 << clock.uniform_bits
    cell_scale = 1 << (clock.fixed_point_bits - clock.uniform_bits)
    counts = [0] * (clock.k_max + 1)
    pending = [(0, clock.k_max, 0, number_uniforms)]
    while pending:
        lower, upper, first_uniform, after_uniform = pending.pop()
        if first_uniform >= after_uniform:
            continue
        if lower == upper:
            counts[lower] += after_uniform - first_uniform
            # Both ends of every nonempty leaf interval must execute to it.
            assert clock._draw_from_uniform_integer(first_uniform)[0] == lower
            assert clock._draw_from_uniform_integer(after_uniform - 1)[0] == lower
            continue
        middle = (lower + upper) // 2
        threshold = clock.scale - clock.fixed_point_survival(middle + 1)
        split = (threshold + cell_scale - 1) // cell_scale
        pending.append((lower, middle, first_uniform, min(after_uniform, split)))
        pending.append((middle + 1, upper, max(first_uniform, split), after_uniform))
    assert sum(counts) == number_uniforms
    return [Fraction(count, number_uniforms) for count in counts]


def audit_small_case(r: Fraction, epsilon: Fraction, exhaustive_bits: bool = False) -> dict:
    clock = GeometricClockCompiler(r, epsilon)
    implemented = exact_binary_tree_masses(clock)
    q = 1 - r
    q_power = Fraction(1)
    target = []
    worst_power_error_ratio = Fraction(0)
    for k in range(clock.k_max + 1):
        target.append(r * q_power)
        q_power *= q
        n = k + 1
        if n <= clock.k_max:
            approximation = Fraction(clock.fixed_point_survival(n), clock.scale)
            error = q_power - approximation
            envelope = Fraction(2 * n, clock.scale)
            assert 0 <= error <= envelope
            worst_power_error_ratio = max(worst_power_error_ratio, error / envelope)

    exact_tail = q_power
    capped_target = target.copy()
    capped_target[-1] += exact_tail
    numeric_tv = sum(abs(a - b) for a, b in zip(implemented, capped_target)) / 2
    total_tv = (sum(abs(a - b) for a, b in zip(implemented, target)) + exact_tail) / 2
    assert sum(target) + exact_tail == 1
    assert sum(capped_target) == 1
    assert exact_tail <= clock.tail_tv_bound
    assert numeric_tv <= clock.uniform_tv_bound + clock.power_tv_bound
    assert total_tv <= clock.total_tv_bound <= epsilon

    rng = CountingRandom(20261105)
    for _ in range(100):
        value, metadata = clock.sample(rng)
        assert 0 <= value <= clock.k_max
        assert metadata["actual_cdf_evaluations"] <= clock.index_bits
        assert metadata["actual_fixed_point_multiplications"] <= clock.index_bits**2
        assert metadata["actual_exponent_bit_steps"] <= clock.index_bits**2
        assert metadata["actual_random_bits"] == clock.uniform_bits
    assert rng.bit_calls == (0 if r == 1 else 100)
    assert rng.bits_requested == 100 * clock.uniform_bits

    grid_inputs_checked = 0
    if exhaustive_bits:
        assert clock.uniform_bits <= 16
        counts = Counter()
        for uniform_integer in range(1 << clock.uniform_bits):
            value, metadata = clock._draw_from_uniform_integer(uniform_integer)
            counts[value] += 1
            assert metadata["actual_cdf_evaluations"] <= clock.index_bits
            assert metadata["actual_fixed_point_multiplications"] <= clock.index_bits**2
            assert metadata["actual_exponent_bit_steps"] <= clock.index_bits**2
        grid_inputs_checked = 1 << clock.uniform_bits
        assert all(
            Fraction(counts[k], grid_inputs_checked) == implemented[k]
            for k in range(clock.k_max + 1)
        )

    return {
        "r": str(r),
        "epsilon": str(epsilon),
        "certificate": clock.certificate(),
        "exact_target_tail": fraction_record(exact_tail),
        "exact_numeric_total_variation": fraction_record(numeric_tv),
        "exact_full_total_variation": fraction_record(total_tv),
        "max_power_error_fraction_of_proved_envelope": fraction_record(worst_power_error_ratio),
        "exact_power_exponents_checked": clock.k_max,
        "uniform_grid_inputs_exhaustively_checked": grid_inputs_checked,
        "all_exact_assertions_passed": True,
    }


def geometric_cdf_diagnostic(k: int, r: Fraction) -> float:
    if k < 0:
        return 0.0
    probability = float(r)
    log_ratio = math.log1p(-probability) / probability
    # Multiplying the exact fraction first avoids converting the huge k alone.
    exponent = float(r * (k + 1)) * log_ratio
    return -math.expm1(exponent)


def audit_large_case(r: Fraction, epsilon: Fraction, number_draws: int, seed: int) -> dict:
    start = time.perf_counter()
    clock = GeometricClockCompiler(r, epsilon)
    compilation_seconds = time.perf_counter() - start
    rng = CountingRandom(seed)
    values = []
    maximum_queries = maximum_multiplies = maximum_bit_steps = 0
    start = time.perf_counter()
    for _ in range(number_draws):
        value, metadata = clock.sample(rng)
        values.append(value)
        assert 0 <= value <= clock.k_max
        maximum_queries = max(maximum_queries, metadata["actual_cdf_evaluations"])
        maximum_multiplies = max(maximum_multiplies, metadata["actual_fixed_point_multiplications"])
        maximum_bit_steps = max(maximum_bit_steps, metadata["actual_exponent_bit_steps"])
        assert metadata["actual_random_bits"] == clock.uniform_bits
    execution_seconds = time.perf_counter() - start
    assert maximum_queries <= clock.index_bits
    assert maximum_multiplies <= clock.index_bits**2
    assert maximum_bit_steps <= clock.index_bits**2
    assert rng.bit_calls == number_draws
    assert rng.bits_requested == number_draws * clock.uniform_bits

    frequencies = Counter(values)
    accumulated = 0
    ks_distance = 0.0
    for value, count in sorted(frequencies.items()):
        ks_distance = max(
            ks_distance,
            abs(accumulated / number_draws - geometric_cdf_diagnostic(value - 1, r)),
        )
        accumulated += count
        ks_distance = max(
            ks_distance,
            abs(accumulated / number_draws - geometric_cdf_diagnostic(value, r)),
        )
    scaled_mean = float(r * Fraction(sum(values), number_draws))
    if number_draws >= 1000:
        # Reproducible broad regression checks; not a proof of a TV guarantee.
        assert ks_distance < 0.09
        assert abs(scaled_mean - float(1 - r)) < 0.15

    return {
        "r": str(r),
        "epsilon": str(epsilon),
        "draws": number_draws,
        "seed": seed,
        "randomness": "seeded Python random.Random subclass; diagnostic only",
        "certificate": clock.certificate(),
        "compile_seconds": compilation_seconds,
        "draw_seconds": execution_seconds,
        "first_ten_values": [str(v) for v in values[:10]],
        "minimum_value": str(min(values)),
        "maximum_value": str(max(values)),
        "cap_hits": sum(v == clock.k_max for v in values),
        "max_actual_cdf_evaluations": maximum_queries,
        "max_actual_fixed_point_multiplications": maximum_multiplies,
        "max_actual_exponent_bit_steps": maximum_bit_steps,
        "random_calls": rng.bit_calls,
        "random_bits_requested": rng.bits_requested,
        "scaled_sample_mean_rK": scaled_mean,
        "empirical_cdf_distance_diagnostic": ks_distance,
        "all_resource_assertions_passed": True,
    }


def audit_edge_cases() -> dict:
    logarithm_cases = 0
    for numerator in range(1, 41):
        for denominator in range(1, 41):
            result = _ceil_log2_ratio(numerator, denominator)
            upper = Fraction(1 << result) if result >= 0 else Fraction(1, 1 << -result)
            assert upper / 2 < Fraction(numerator, denominator) <= upper
            logarithm_cases += 1
    rejected = 0
    for r, epsilon in [
        (Fraction(0), Fraction(1, 2)),
        (Fraction(-1, 3), Fraction(1, 2)),
        (Fraction(4, 3), Fraction(1, 2)),
        (Fraction(1, 2), Fraction(0)),
        (Fraction(1, 2), Fraction(1)),
        (0.1, Fraction(1, 2)),
    ]:
        try:
            GeometricClockCompiler(r, epsilon)
        except (TypeError, ValueError):
            rejected += 1
        else:
            raise AssertionError("An invalid input was accepted.")
    first_rng = random.Random(123456)
    second_rng = random.Random(123456)
    r, epsilon = Fraction(2, 17), Fraction(1, 128)
    convenient = sample_geometric(r, epsilon, first_rng)
    cached = GeometricClockCompiler(r, epsilon).sample(second_rng)
    assert convenient == cached
    return {
        "exact_logarithm_cases": logarithm_cases,
        "invalid_inputs_rejected": rejected,
        "cached_and_convenience_api_agree": True,
    }


def main() -> None:
    started = time.perf_counter()
    small_specs = [
        (Fraction(1), Fraction(1, 8), True),
        (Fraction(1, 2), Fraction(1, 8), True),
        (Fraction(1, 3), Fraction(1, 32), False),
        (Fraction(2, 7), Fraction(1, 64), False),
        (Fraction(1, 10), Fraction(1, 64), False),
        (Fraction(1, 100), Fraction(1, 16), False),
        (Fraction(19, 20), Fraction(1, 1024), False),
        (Fraction(1, 64), Fraction(3, 10), False),
        (Fraction(3, 17), Fraction(999, 1000), True),
        (Fraction(1, 257), Fraction(1, 8), False),
    ]
    result = {
        "status": "running",
        "python": platform.python_version(),
        "claim_boundary": (
            "Exact arithmetic audits and the written coupling proof certify error bounds; "
            "large-case seeded-PRNG statistics are execution diagnostics only."
        ),
        "edge_checks": audit_edge_cases(),
        "small_exact_distribution_checks": [audit_small_case(*s) for s in small_specs],
        "large_index_checks": [
            audit_large_case(Fraction(1, 1 << 100), Fraction(1, 1 << 20), 1000, 20261105),
            audit_large_case(Fraction(1, 10**25), Fraction(1, 1 << 20), 1000, 20261106),
            audit_large_case(Fraction(1, 1 << 1000), Fraction(1, 1 << 20), 2, 20261107),
        ],
    }
    result["status"] = "all_checks_passed"
    result["execution_seconds"] = time.perf_counter() - started
    output = ROOT / "next4_theory" / "02_GEOMETRIC_CHECKS.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "small_exact_cases": len(result["small_exact_distribution_checks"]),
        "large_draws": [case["draws"] for case in result["large_index_checks"]],
        "large_compile_seconds": [case["compile_seconds"] for case in result["large_index_checks"]],
        "large_draw_seconds": [case["draw_seconds"] for case in result["large_index_checks"]],
        "large_uniform_bits": [case["certificate"]["uniform_bits"] for case in result["large_index_checks"]],
        "large_fixed_point_bits": [case["certificate"]["fixed_point_bits"] for case in result["large_index_checks"]],
        "large_cdf_diagnostics": [case["empirical_cdf_distance_diagnostic"] for case in result["large_index_checks"]],
        "output": str(output),
    }, indent=2))


if __name__ == "__main__":
    main()
