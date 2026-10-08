#!/usr/bin/env python3
"""Exact checks for the q=2 hidden renewal prefix counterexample.

This is a finite diagnostic, not an approximation algorithm. It enumerates
all span-at-most-4 pools for N=5 and compares the closed prefix formula with
direct sequential row-urn draws followed by the strict residual-gap test.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product
from math import comb, factorial
from pathlib import Path
import json


def enumerate_pools(N, q=2):
    """All q^2-coloured gap-count vectors with span at most N-1."""
    coords = [(i, d, g) for g in range(1, N)
              for i in range(q) for d in range(q)]
    current = {}
    pools = []

    def visit(j, remaining, span):
        if j == len(coords):
            pools.append((span, current.copy()))
            return
        i, d, g = coords[j]
        key = (i, d, g)
        for u in range(remaining // g + 1):
            if u:
                current[key] = u
            else:
                current.pop(key, None)
            visit(j + 1, remaining - u * g, span + u * g)
        current.pop(key, None)

    visit(0, N - 1, 0)
    return pools


def falling(x, k):
    if x < k:
        return 0
    return factorial(x) // factorial(x - k)


def hidden_path_formula(states, events, t, N, pools):
    """Marked-prefix formula, omitting common factor 1/(2 K_N)."""
    k = len(events)
    anchor = events[0]
    age = t - events[-1]
    observed = Counter(
        (states[j], states[j + 1], events[j + 1] - events[j])
        for j in range(k - 1)
    )
    row_uses = [sum(states[j] == i for j in range(k - 1))
                for i in range(2)]
    last = states[-1]
    parts = defaultdict(F)

    for span, pool in pools:
        if span > N - anchor:
            continue
        numerator = 1
        feasible = True
        for key, used in observed.items():
            numerator *= falling(pool.get(key, 0), used)
            if numerator == 0:
                feasible = False
                break
        if not feasible:
            continue

        row_totals = [sum(v for (i, _d, _g), v in pool.items() if i == h)
                      for h in range(2)]
        denominator = 1
        for i in range(2):
            denominator *= falling(row_totals[i], row_uses[i])
        if denominator == 0:
            continue

        base = F(numerator, denominator * (N - span))
        remaining_last_row = row_totals[last] - row_uses[last]
        if remaining_last_row == 0:
            parts["T=0"] += base
            if row_totals[1 - last] > row_uses[1 - last]:
                parts["T=0_other_row_unused"] += base
            continue

        used_tail = sum(v for (i, _d, g), v in observed.items()
                        if i == last and g > age)
        remaining_long = sum(v for (i, _d, g), v in pool.items()
                             if i == last and g > age) - used_tail
        if remaining_long:
            parts["T>0_tail_accepted"] += base * F(remaining_long,
                                                   remaining_last_row)
        else:
            # Record the pre-tail base mass to show what the strict test removes.
            parts["T>0_tail_rejected_base"] += base
    return parts


def hidden_path_direct(states, events, t, N, pools):
    """Directly multiply sequential row-draw probabilities and survival."""
    age = t - events[-1]
    parts = defaultdict(F)
    for span, pool in pools:
        if span > N - events[0]:
            continue
        remaining = pool.copy()
        probability = F(1)
        possible = True
        for j in range(len(events) - 1):
            source, destination = states[j], states[j + 1]
            gap = events[j + 1] - events[j]
            row_total = sum(v for (i, _d, _g), v in remaining.items()
                            if i == source)
            count = remaining.get((source, destination, gap), 0)
            if count == 0 or row_total == 0:
                possible = False
                break
            probability *= F(count, row_total)
            remaining[(source, destination, gap)] -= 1
        if not possible:
            continue

        last = states[-1]
        row_total = sum(v for (i, _d, _g), v in remaining.items()
                        if i == last)
        base = probability / (N - span)
        if row_total == 0:
            parts["T=0"] += base
            continue
        long_count = sum(v for (i, _d, g), v in remaining.items()
                         if i == last and g > age)
        if long_count:
            parts["T>0_tail_accepted"] += base * F(long_count, row_total)
        else:
            parts["T>0_tail_rejected_base"] += base
    return parts


def full_span_coefficients(word):
    m = len(word)
    A = [0] * (m + 1)
    Z = F(0)
    for states in product((0, 1), repeat=m + 1):
        counts = Counter((states[j], states[j + 1], word[j])
                         for j in range(m))
        numerator = 1
        for count in counts.values():
            numerator *= factorial(count)
        r0 = sum(states[j] == 0 for j in range(m))
        A[r0] += numerator
        Z += F(numerator, factorial(r0) * factorial(m - r0))
    B = [comb(m, r) * A[r] for r in range(m + 1)]
    return A, B, Z


def main():
    N, events, t = 5, (1, 2, 3), 4
    pools = enumerate_pools(N)
    assert len(pools) == 164
    code_types = len(pools) + 1  # separate all-zero option
    assert code_types == 165

    table = {}
    branch_000 = None
    for states in product((0, 1), repeat=3):
        f = hidden_path_formula(states, events, t, N, pools)
        d = hidden_path_direct(states, events, t, N, pools)
        # Both methods report disjoint T=0 and T>0 accepted contributions;
        # rejected-base mass is diagnostic and contributes zero.
        for key in ("T=0", "T>0_tail_accepted"):
            assert f[key] == d[key], (states, key, f, d)
        value = f["T=0"] + f["T>0_tail_accepted"]
        table["".join(map(str, states))] = value
        if states == (0, 0, 0):
            branch_000 = f

    expected = {
        "000": F(7), "001": F(8, 3),
        "010": F(61, 12), "011": F(61, 12),
        "100": F(61, 12), "101": F(61, 12),
        "110": F(8, 3), "111": F(7),
    }
    assert table == expected
    assert branch_000["T=0"] == F(19, 3)
    assert branch_000["T=0_other_row_unused"] == 6
    assert branch_000["T>0_tail_accepted"] == F(2, 3)
    assert branch_000["T>0_tail_rejected_base"] == 5

    # FKG positive-lattice inequality fails for 010 and 100.
    lhs = table["000"] * table["110"]
    rhs = table["010"] * table["100"]
    assert lhs == F(56, 3) and rhs == F(3721, 144) and lhs < rhs
    total_lambda = sum(table.values(), F(0))
    assert total_lambda == F(119, 3)
    q_mass = total_lambda / (2 * code_types)
    assert q_mass == F(119, 990)
    scaled_integer_mass = 2 * code_types * factorial(N) * q_mass
    assert scaled_integer_mass == 4760

    # Natural full-span magnetization polynomial is not log-concave.
    word = (1, 2, 2, 2, 2, 2, 2)
    A, B, Z = full_span_coefficients(word)
    assert A == [840, 1176, 588, 540, 540, 588, 1176, 840]
    assert B == [840, 8232, 12348, 18900, 18900, 12348, 8232, 840]
    assert B[2] ** 2 == 152473104
    assert B[1] * B[3] == 155584800
    assert B[2] ** 2 < B[1] * B[3]
    assert Z == 16

    # Distinct labels have a closed exact sum.
    distinct_word = (1, 2, 3, 4)
    _A, _B, distinct_Z = full_span_coefficients(distinct_word)
    m = len(distinct_word)
    closed_form = F(2 * comb(2 * m, m), factorial(m))
    assert distinct_Z == closed_form == F(35, 6)

    result = {
        "status": "PASS",
        "arithmetic": "exact Python integers and Fractions",
        "scope": "N=5, q=2, prefix 1110; all 164 pools and all 8 hidden paths",
        "pool_count": len(pools),
        "K_5_including_zero_option": code_types,
        "hidden_path_lambda_without_common_factor": {
            u: str(v) for u, v in table.items()
        },
        "formula_vs_direct_sequential_draws": "all 8 path contributions match",
        "path_000_branch_breakdown": {
            "T_eq_0_total": str(branch_000["T=0"]),
            "T_eq_0_with_other_row_unused": str(
                branch_000["T=0_other_row_unused"]
            ),
            "T_gt_0_tail_accepted": str(branch_000["T>0_tail_accepted"]),
            "T_gt_0_rejected_pre_tail_base": str(
                branch_000["T>0_tail_rejected_base"]
            ),
        },
        "projected_prefix_mass_Q5_1110": str(q_mass),
        "integer_scaled_mass_H5": int(scaled_integer_mass),
        "fkg_witness": {
            "x": "010", "y": "100", "meet": "000", "join": "110",
            "lhs_lambda_meet_times_join": str(lhs),
            "rhs_lambda_x_times_y": str(rhs),
            "positive_lattice_condition": "FAIL",
        },
        "full_span_log_concavity_word": list(word),
        "A_r": A,
        "binomial_weighted_coefficients_B_r": B,
        "B2_squared": B[2] ** 2,
        "B1_times_B3": B[1] * B[3],
        "Z_word": str(Z),
        "distinct_gap_control": {
            "word": list(distinct_word),
            "enumerated_Z": str(distinct_Z),
            "closed_form_Z": str(closed_form),
        },
        "not_claimed": [
            "no general FPRAS or approximation lower bound",
            "no proof that transformed FKG representations cannot exist",
            "finite checks are not an all-input algorithm",
        ],
    }
    path = Path(__file__).with_name("exact_check.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
