#!/usr/bin/env python3
"""Exact finite diagnostics for a uniform Foster/truncation certificate."""
from fractions import Fraction
from itertools import product
from math import comb
import json
from pathlib import Path

BIRTH_MAX = 2
DEATH_MIN = 1


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def choose2(x):
    return x * (x - 1) // 2


def upper_drift(d, x):
    n = sum(x)
    return Fraction(2**n) * (
        d * BIRTH_MAX - Fraction(DEATH_MIN, 2) * sum(choose2(z) for z in x)
    )


def drift_cutoff(d):
    # Exact rational search for a sufficient total-count cutoff using
    # sum_i C(x_i,2) >= (n^2/d - n)/2.
    n = 0
    while True:
        lower_sum = Fraction(n * n, d) - n
        bracket = d * BIRTH_MAX - Fraction(DEATH_MIN, 4) * lower_sum
        if bracket <= -1:
            return n
        n += 1


def main():
    records = []
    diagnostic_count = 0
    for d in range(1, 5):
        nstar = drift_cutoff(d)
        conservative_B = d * BIRTH_MAX * 2 ** (nstar - 1)
        exact_B = Fraction(0)
        for n in range(nstar):
            for x in compositions(n, d):
                val = upper_drift(d, x)
                exact_B = max(exact_B, val)
        for n in range(nstar + 4):
            for x in compositions(n, d):
                val = upper_drift(d, x)
                assert val <= conservative_B
                if n >= nstar:
                    assert val <= -(2**n)
                diagnostic_count += 1
        records.append({
            "dimension": d,
            "recovery_count_cutoff_nstar": nstar,
            "coarse_global_upper_drift_B": conservative_B,
            "exact_B_on_pre_cutoff_states": str(exact_B),
            "states_checked": sum(comb(n + d - 1, d - 1) for n in range(nstar + 4)),
            "status": "PASS_EXACT_RATIONAL_FINITE_DIAGNOSTIC"
        })

    d = 2
    initial_total = 2
    horizon = 100
    epsilon = Fraction(1, 100)
    exact_B = 64
    numerator = 2**initial_total + exact_B * horizon
    cutoff = 0
    while Fraction(numerator, 2**cutoff) > epsilon:
        cutoff += 1
    exit_bound = Fraction(numerator, 2**cutoff)
    assert cutoff == 20
    assert exit_bound <= epsilon
    example = {
        "dimension": d,
        "initial_state": [1, 1],
        "horizon": horizon,
        "epsilon": str(epsilon),
        "exact_global_upper_drift_B": exact_B,
        "absorbing_cutoff_total_count_ge": cutoff,
        "finite_states_with_total_count_lt_cutoff": comb(cutoff + d - 1, d),
        "certified_exit_probability_upper_bound": str(exit_bound),
        "decimal_upper_bound_for_display_only": float(exit_bound),
        "status": "PASS_EXACT_RATIONAL_ARITHMETIC"
    }
    out = {
        "model": "d independent controlled species; 0->A_i rate in [1,2], 2A_i->A_i rate d_i*C(x_i,2), d_i in [1,4]",
        "lyapunov": "W(x)=2^(sum_i x_i)",
        "action_quantifier": "arbitrary predictable rates, including history-dependent randomized control",
        "diagnostic_scope": "finite exact checks corroborate the algebra; they do not replace the uniform proof",
        "diagnostic_count": diagnostic_count,
        "dimensions": records,
        "two_species_finite_horizon_example": example
    }
    path = Path(__file__).with_name("recovery_truncation_checks.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(path)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
