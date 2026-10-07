"""Bounded scalar-only evidence for the separate optimal-domain corollary.

This does not run an LP, a generic iid compiler, or an optimal-domain Gibbs
sampler. Existing practical code retains its frozen nonnegative delta1 scope.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import signal
import time

from axial_acquisition import exp_neg_dyadic, choose, sector_matrix
from filtered_sector import filtered_sector_columns, conditional_max_shift_probabilities


def endpoint_enclosure(accuracy):
    """Exact lower/upper rationals for delta*=4atanh(1/3)."""
    accuracy = F(accuracy)
    if accuracy <= 0:
        raise ValueError("positive rational absolute accuracy required")
    M, lower = 0, F(0)
    while True:
        lower += F(4, (2 * M + 1) * 3 ** (2 * M + 1))
        M += 1
        tail = F(4, (2 * M + 1) * 3 ** (2 * M + 1)) / F(8, 9)
        if tail <= accuracy:
            return lower, lower + tail, M


def general_shifted_grid(N, delta, h, bits):
    """Scalar fixture only; mathematical admitted domain supplied by promise."""
    delta, h = F(delta), F(h)
    H = max(F(0), -delta) * N / 4 + abs(h) * N / 2
    args = []
    for t in range(N + 1):
        m = F(2 * t - N, 2)
        args.append(H + delta * m * m / N - h * m)
    if min(args) < 0:
        raise AssertionError("exact exponent shift failed")
    return [exp_neg_dyadic(x, bits) for x in args], args


def main():
    def wall_limit(signum, frame):
        raise TimeoutError("declared20second extension-scalar wall cap exceeded")
    signal.signal(signal.SIGALRM, wall_limit)
    signal.alarm(20)
    started, assertions = time.perf_counter(), 0

    def check(condition):
        nonlocal assertions
        assertions += 1
        assert condition

    endpoint_records = []
    for N in [1, 2, 8, 64]:
        for accuracy_bits in [3, 20, 100]:
            eps = F(1, 1 << accuracy_bits)
            lo, hi, M = endpoint_enclosure(eps / (2 * N))
            check(hi - lo <= eps / (2 * N))
            # Separate much longer positive-series enclosure validates inclusion.
            fine_lo, fine_hi, fine_M = endpoint_enclosure(eps / (1024 * N))
            check(lo < fine_lo < fine_hi < hi)
            check(F(4, 3) <= lo < hi < F(7, 5))
            check(M <= accuracy_bits + N.bit_length() + 3)
            # The proof uses a<=eps/8 and T<=2a<=eps/4.
            check(N * (hi - lo) / 4 <= eps / 8)
            endpoint_records.append({"N": N, "epsilon_bits": accuracy_bits,
                                     "series_terms": M,
                                     "lower": str(lo), "upper": str(hi),
                                     "generator_range_upper": str(N * (hi - lo) / 4),
                                     "Gibbs_TV_upper": str(N * (hi - lo) / 2)})

    # This exact rational lies below the endpoint by a distinct fixed series.
    near_endpoint = F(138629, 100000)
    delta_lo, delta_hi, _ = endpoint_enclosure(F(1, 1 << 100))
    check(near_endpoint < delta_lo < delta_hi < 2)
    huge = F(1 << 256)
    cases = []
    for N in [1, 2, 8, 16, 64]:
        parameter_cases = [(-huge, huge), (-huge, -huge)]
        if N <= 16:
            parameter_cases += [(near_endpoint, F(1, 3)), (F(-1), F(0))]
        for delta, h in parameter_cases:
            bits = 2 * N + 32
            grid, args = general_shifted_grid(N, delta, h, bits)
            aligned = N if h >= 0 else 0
            check(args[aligned] == max(F(0), delta) * N / 4)
            check(min(args) >= 0 and max(grid) <= 1)
            check(grid[aligned] >= F(1, 1 << N))
            if delta < 0:
                check(grid[aligned] == 1)
            C, c, Z = filtered_sector_columns(N, grid)
            check(min(Z) >= F(1, 1 << (2 * N)))
            if delta < 0:
                check(min(Z) >= F(1, 1 << N))
            check((N + 1) * c[0] == sum(grid))
            check((N + 1) * c[0] >= F(1, 1 << N))
            for k in range(N + 1):
                check(sum(C[b][k] for b in range(len(C))) == 1)
                raw_sum = sum(F(choose(N - k, u), (k + 1) * (1 << (N - k)))
                              * sum(grid[u:u + k + 1]) for u in range(N - k + 1))
                check(raw_sum == Z[k])
            # Selected conditional fixtures keep a scalar denominator >=1 even
            # when the common grid has clipped zero slices. No iid backend run.
            conditional_ks = range(N + 1) if N <= 2 else sorted(set([0, 1, 2, N // 2, N]))
            for k in conditional_ks:
                conditional_us = range(N - k + 1) if N <= 2 else sorted(set([0, (N-k)//2, N-k]))
                for u in conditional_us:
                    p, meta = conditional_max_shift_probabilities(N, k, u, delta, h, F(1, 1024))
                    check(sum(p) == 1 and min(p) >= 0)
                    check(meta["normalizer_at_least_one"])
                    check(meta["scalar_bits"] <= 25)
            cases.append({"N": N, "delta": str(delta), "h": str(h),
                          "input_magnitude_bits": max(delta.numerator.bit_length(), h.numerator.bit_length()),
                          "precision_bits": bits,
                          "extremal_grid_value": str(grid[aligned]),
                          "clipped_zero_values": grid.count(F(0)),
                          "minimum_K_normalizer": str(min(Z))})

    result = {"status": "PASS", "assertions": assertions,
              "elapsed_seconds_shared_machine": time.perf_counter() - started,
              "wall_cap_seconds": 20,
              "endpoint_enclosures": endpoint_records,
              "scalar_domain_cases": cases,
              "scope": "exact acquired one-sided endpoint plus scalar/normalizer/conditional-input checks only",
              "optimal_domain_Gibbs_sampler_executed": False,
              "LP_or_generic_iid_backend_executed": False,
              "frozen_practical_domain": "nonnegative delta<=1 cases only",
              "hardware_preparation": "NOT_EXECUTED"}
    signal.alarm(0)
    Path(__file__).with_name("domain_extension_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "assertions": assertions,
                      "elapsed_seconds_shared_machine": result["elapsed_seconds_shared_machine"],
                      "scalar_cases": len(cases), "endpoint_cases": len(endpoint_records),
                      "scope": result["scope"]}, indent=2))


if __name__ == "__main__":
    main()
