"""Certified finite-horizon rare-event probability for a run automaton.

The implementation is a small, explicit-state model checker.  Its purpose is
to make the representation and arithmetic costs visible, not to claim a new
rare-event sampling method.
"""
from __future__ import annotations

import json
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


def ceil_div(a: int, b: int) -> int:
    return (a + b - 1) // b


def interval_matmul(a_lo, a_hi, b_lo, b_hi, scale: int):
    """Entrywise enclosure for products of nonnegative interval matrices."""
    n = len(a_lo)
    out_lo = [[0] * n for _ in range(n)]
    out_hi = [[0] * n for _ in range(n)]
    for i in range(n):
        alo, ahi = a_lo[i], a_hi[i]
        olo, ohi = out_lo[i], out_hi[i]
        for k in range(n):
            al, ah = alo[k], ahi[k]
            if al == 0 and ah == 0:
                continue
            blo, bhi = b_lo[k], b_hi[k]
            for j in range(n):
                if al and blo[j]:
                    olo[j] += al * blo[j]
                if ah and bhi[j]:
                    ohi[j] += ah * bhi[j]
    for i in range(n):
        for j in range(n):
            out_lo[i][j] //= scale
            out_hi[i][j] = ceil_div(out_hi[i][j], scale)
    return out_lo, out_hi


def interval_matrix_power(lo, hi, exponent: int, scale: int):
    """Binary power with outward-rounded fixed-point interval arithmetic."""
    n = len(lo)
    result_lo = [[int(i == j) * scale for j in range(n)] for i in range(n)]
    result_hi = [row[:] for row in result_lo]
    base_lo, base_hi = [row[:] for row in lo], [row[:] for row in hi]
    multiplications = 0
    e = exponent
    while e:
        if e & 1:
            result_lo, result_hi = interval_matmul(
                result_lo, result_hi, base_lo, base_hi, scale
            )
            multiplications += 1
        e >>= 1
        if e:
            base_lo, base_hi = interval_matmul(
                base_lo, base_hi, base_lo, base_hi, scale
            )
            multiplications += 1
    return result_lo, result_hi, multiplications


def run_automaton_matrix(k: int, bits: int, precision_bits: int):
    """Build the DFA for k consecutive heads and enclose its reachability."""
    assert k >= 1 and bits >= 0 and precision_bits >= 2
    states = k + 1  # trailing-head counts 0..k-1, plus absorbing hit state
    scale = 1 << precision_bits
    lo = [[0] * states for _ in range(states)]
    hi = [[0] * states for _ in range(states)]
    half = scale // 2
    for j in range(k):
        # Tail resets the suffix automaton to state zero.
        lo[j][0] = hi[j][0] = half
        # Head either extends the run or reaches the absorbing target.
        lo[j][j + 1] = hi[j][j + 1] = half
    lo[k][k] = hi[k][k] = scale

    start = time.perf_counter()
    p_lo, p_hi, n_mult = interval_matrix_power(lo, hi, 1 << bits, scale)
    elapsed = time.perf_counter() - start
    lower, upper = p_lo[0][k], p_hi[0][k]
    assert lower <= upper
    return {
        "k": k,
        "horizon_bits": bits,
        "horizon": str(1 << bits),
        "states_including_absorber": states,
        "transition_entries_supplied": 2 * k + 1,
        "fixed_point_precision_bits": precision_bits,
        "matrix_multiplications": n_mult,
        "dense_scalar_product_upper_bound": n_mult * states**3,
        "elapsed_seconds": elapsed,
        "probability_lower": str(Fraction(lower, scale)),
        "probability_upper": str(Fraction(upper, scale)),
        "relative_interval_width": str(Fraction(upper - lower, lower)) if lower else None,
        "decimal_lower": decimal_fraction(Fraction(lower, scale)),
        "decimal_upper": decimal_fraction(Fraction(upper, scale)),
        "interval_is_nonempty": lower > 0,
    }


def decimal_fraction(x: Fraction, digits: int = 35) -> str:
    with localcontext() as ctx:
        ctx.prec = digits
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def exact_run_probability(k: int, horizon: int) -> Fraction:
    """Exact small-fixture probability via the standard run-count recurrence."""
    alive = [0] * k
    alive[0] = 1
    hit = 0
    for _ in range(horizon):
        new = [0] * k
        new[0] = sum(alive)  # next bit is tail
        for j in range(k - 1):
            new[j + 1] = alive[j]  # next bit is head
        hit = 2 * hit + alive[k - 1]
        alive = new
    return Fraction(hit, 1 << horizon)


def exact_regenerative_probability(k: int, horizon: int) -> Fraction:
    """Renewal decomposition at each tail, evaluated with exact rationals.

    The first excursion either contains k heads in its first k bits
    (probability 2^-k), or its first tail occurs on bit ell <= k
    (probability 2^-ell), regenerating the same process with horizon reduced
    by ell.
    """
    f = [Fraction(0)] * (horizon + 1)
    for t in range(k, horizon + 1):
        value = Fraction(1, 1 << k)
        # A failed excursion may also end in a tail on bit k; that outcome
        # has probability 2^-k and regenerates at the same boundary.
        for ell in range(1, min(k, t) + 1):
            value += Fraction(1, 1 << ell) * f[t - ell]
        f[t] = value
    return f[horizon]


def exact_small_interval_check(k: int = 9, horizon: int = 257, precision_bits: int = 80):
    states = k + 1
    scale = 1 << precision_bits
    lo = [[0] * states for _ in range(states)]
    hi = [[0] * states for _ in range(states)]
    half = scale // 2
    for j in range(k):
        lo[j][0] = hi[j][0] = half
        lo[j][j + 1] = hi[j][j + 1] = half
    lo[k][k] = hi[k][k] = scale
    pl, pu, mults = interval_matrix_power(lo, hi, horizon, scale)
    exact = exact_run_probability(k, horizon)
    regenerative = exact_regenerative_probability(k, horizon)
    assert exact == regenerative
    lower, upper = Fraction(pl[0][k], scale), Fraction(pu[0][k], scale)
    assert lower <= exact <= upper
    return {
        "k": k,
        "horizon": horizon,
        "precision_bits": precision_bits,
        "matrix_multiplications": mults,
        "exact_probability": str(exact),
        "regenerative_recurrence_probability": str(regenerative),
        "interval_lower": str(lower),
        "interval_upper": str(upper),
        "contains_exact_recurrence": True,
    }


def main():
    # A run of 48 heads in 2^20 fair bits has probability around 2^-29.
    toy = run_automaton_matrix(k=48, bits=20, precision_bits=128)
    assert toy["interval_is_nonempty"]
    assert Fraction(toy["probability_upper"]) <= Fraction(toy["probability_lower"]) * Fraction(10001, 10000)
    report = {
        "scope": "finite fair-bit program; target is k consecutive heads by a fixed horizon",
        "toy": toy,
        "exact_fixture": exact_small_interval_check(),
        "representation_acquisition": {
            "supplied_program": "fair-bit loop with a run-length target predicate",
            "target_compilation": "run-length automaton, O(k) states/transitions",
            "nonzero_transition_entries": toy["transition_entries_supplied"],
            "stochastic_measurements": 0,
        },
        "naive_relative_mc_baseline": {
            "relative_standard_error": "0.1",
            "trajectory_count_order": "100/p independent full trajectories",
            "trajectory_count_approx": str(int(100 / float(Fraction(toy["probability_lower"])))),
            "fair_bit_draws_approx": str(int((1 << 20) * 100 / float(Fraction(toy["probability_lower"])))),
        },
        "disclaimer": "matrix powering and run recurrences are standard finite-state model checking; this is not a novelty claim",
    }
    out = Path(__file__).with_name("RESULTS.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
