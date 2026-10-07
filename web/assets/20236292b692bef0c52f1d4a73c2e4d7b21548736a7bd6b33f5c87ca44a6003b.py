#!/usr/bin/env python3
"""Exact bounded fixtures for a hard-parity local-walk obstruction.

The general theorem is proved in INITIAL.txt. This script does not test an
asymptotic mixing theorem or run an FPRAS. Only Python standard-library
integers and Fractions are used for acceptance assertions.
"""

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


def det_int(a):
    a = [list(row) for row in a]
    n = len(a)
    if not n:
        return 1
    sign, old = 1, 1
    for k in range(n - 1):
        if not a[k][k]:
            pivot = next((j for j in range(k + 1, n) if a[j][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = a[i][j] * p - a[i][k] * a[k][j]
                assert num % old == 0
                a[i][j] = num // old
            a[i][k] = 0
        old = p
    return sign * a[-1][-1]


def minor(a, rows, cols):
    return det_int([[a[i][j] for j in cols] for i in rows])


def fraction_record(x):
    return {
        "exact": str(x),
        "decimal_diagnostic": float(x),
        "numerator_bits": x.numerator.bit_length(),
        "denominator_bits": x.denominator.bit_length(),
    }


def fixture(n, precision):
    q = n // 2
    assert n >= 4 and not n % 2 and precision >= n + 2
    sites = set(range(n))
    p = [[int(j == (i + 1) % n) for j in range(n)] for i in range(n)]
    c = [[0 if i == j else (i + 1) ** j for j in range(n)] for i in range(n)]
    m = n ** (n - 1)
    h = math.factorial(n) * (1 + m) ** n
    denominator = (1 << precision) * h
    integer_f = [[denominator * p[i][j] + c[i][j]
                  for j in range(n)] for i in range(n)]
    amp_denominator = denominator ** q
    a = Fraction(1, 1 << precision)
    bound_r = Fraction(1 << n, 1 << (2 * precision))
    even = tuple(range(0, n, 2))
    odd = tuple(range(1, n, 2))
    endpoints = {even, odd}
    weights = {}
    endpoint_count = 0
    for chosen in itertools.combinations(range(n), q):
        other = tuple(sorted(sites - set(chosen)))
        # The generalized Vandermonde perturbation has every such minor nonzero.
        assert minor(c, chosen, other) != 0
        unperturbed = minor(p, chosen, other)
        assert (unperturbed != 0) == (chosen in endpoints)
        endpoint_count += int(unperturbed != 0)
        amplitude = Fraction(minor(integer_f, chosen, other), amp_denominator)
        assert amplitude != 0
        if chosen in endpoints:
            assert abs(amplitude - unperturbed) <= a
        else:
            assert abs(amplitude) <= a
        weights[chosen] = amplitude * amplitude
    assert endpoint_count == 2
    z = sum(weights.values(), Fraction())
    w_even, w_odd = weights[even], weights[odd]
    bridge = z - w_even - w_odd
    assert bridge <= bound_r
    pi_even, pi_odd, pi_bridge = w_even / z, w_odd / z, bridge / z
    assert pi_even >= Fraction(1, 3) and pi_odd >= Fraction(1, 3)
    assert pi_bridge <= bound_r
    universal_gap_bound = pi_bridge / (pi_even * (1 - pi_even))
    assert universal_gap_bound <= 9 * bound_r
    # Uniform one-pair proposal plus Metropolis acceptance is irreducible,
    # since every q-set has positive weight. Its exact endpoint exit flow is
    # also recorded, but the theorem bounds every stationary local kernel.
    even_set = set(even)
    proposal_exit = Fraction()
    for x in even:
        for y in sorted(sites - even_set):
            neighbor = tuple(sorted((even_set - {x}) | {y}))
            proposal_exit += min(Fraction(1), weights[neighbor] / w_even) / (q * q)
    metropolis_gap_upper = proposal_exit / (1 - pi_even)
    assert proposal_exit <= bridge / w_even
    assert metropolis_gap_upper <= universal_gap_bound
    norm_perturbation_bound = Fraction(n * m, denominator)
    assert norm_perturbation_bound <= a
    condition_upper = (1 + norm_perturbation_bound) / (1 - norm_perturbation_bound)
    assert condition_upper <= Fraction(65, 63)
    endpoint_sum = w_even + w_odd
    relative_count_omission = bridge / z
    assert relative_count_omission <= bound_r
    return {
        "n": n, "q": q, "precision_L": precision,
        "states": len(weights), "all_weights_positive": True,
        "unperturbed_nonzero_states": endpoint_count,
        "unit_activities": True, "F_diagonal_zero": True,
        "all_F_offdiagonals_positive": True,
        "entry_common_denominator_bits": denominator.bit_length(),
        "condition_number_upper": fraction_record(condition_upper),
        "stationary_bridge_mass": fraction_record(pi_bridge),
        "bridge_weight_bound_2n4minusL": fraction_record(bound_r),
        "universal_reversible_gap_upper": fraction_record(universal_gap_bound),
        "metropolis_endpoint_exit_probability": fraction_record(proposal_exit),
        "metropolis_gap_upper": fraction_record(metropolis_gap_upper),
        "endpoint_approximation_relative_error": fraction_record(relative_count_omission),
        "endpoint_sum_bits": {
            "numerator": endpoint_sum.numerator.bit_length(),
            "denominator": endpoint_sum.denominator.bit_length(),
        },
        "universal_mixing_lower_1_over_4": (1 << (2 * precision - n)) // 32,
    }


def main():
    cases = [fixture(n, precision) for n in (4, 6, 8, 10)
             for precision in (n + 2, n + 10, n + 24)]
    result = {
        "scope": "Exact finite rational bookkeeping; no general mixing run or FPRAS",
        "cases": len(cases), "all_assertions_passed": True,
        "total_q_set_minors": sum(x["states"] for x in cases),
        "fixtures": cases,
    }
    output = Path(__file__).with_name("full_support_barrier_checks.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "fixtures"}))


if __name__ == "__main__":
    main()
