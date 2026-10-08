#!/usr/bin/env python3
"""Reconstruct Rule 166's one-run dynamics and audit the exact formulas.

Standard-library only.  This script is a finite-state check of a closed-form
birth--death reduction; it is not a model of a realized protein complex.
"""

from __future__ import annotations

import json
import math
from typing import Dict, Iterable, List


RULE = 166
ACTIVE = tuple(p for p in range(8) if ((RULE >> p) & 1) != ((p >> 1) & 1))


def bit(x: int, i: int) -> int:
    return (x >> i) & 1


def motif(x: int, i: int, n: int) -> int:
    return 4 * bit(x, (i - 1) % n) + 2 * bit(x, i) + bit(x, (i + 1) % n)


def outgoing_strong_drive(x: int, n: int) -> List[int]:
    return [x ^ (1 << i) for i in range(n) if motif(x, i, n) in ACTIVE]


def solve(a: List[List[float]], b: List[float]) -> List[float]:
    """Partial-pivot Gaussian elimination for small verification fixtures."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[pivot][col]) < 1e-14:
            raise ArithmeticError("singular transient generator")
        m[col], m[pivot] = m[pivot], m[col]
        scale = m[col][col]
        for j in range(col, n + 1):
            m[col][j] /= scale
        for row in range(n):
            if row == col:
                continue
            factor = m[row][col]
            for j in range(col, n + 1):
                m[row][j] -= factor * m[col][j]
    return [m[i][n] for i in range(n)]


def one_run_ctmc_check(n: int) -> dict:
    """Check the one-run CTMC mean time and fuel count by a direct solve."""
    if n < 3 or n % 2 != 1:
        raise ValueError("use odd N >= 3")
    majority = (n + 1) // 2
    safe = [sum(1 << ((start + j) % n) for j in range(length))
            for length in range(1, majority)
            for start in range(n)]
    # The run states above are unique before majority for odd N.
    index = {state: i for i, state in enumerate(safe)}
    if len(index) != n * (majority - 1):
        raise AssertionError("one-run state enumeration was not unique")
    m = len(safe)
    minus_q = [[0.0] * m for _ in range(m)]
    reward = [0.0] * m  # one fuel molecule is consumed per forward event
    for state in safe:
        i = index[state]
        edges = outgoing_strong_drive(state, n)
        for nxt in edges:
            minus_q[i][i] += 1.0
            reward[i] += 1.0
            if nxt in index:
                minus_q[i][index[nxt]] -= 1.0
    start = index[1]
    mean_time = solve(minus_q, [1.0] * m)[start]
    mean_fuel = solve(minus_q, reward)[start]
    expected_time_formula = 2**majority - majority - 1
    expected_fuel_formula = 2 ** (majority + 1) - 3 * majority - 1

    # Check that the full forward closure is exactly all cyclic 1-runs and 1^N.
    seen = {1}
    todo = [1]
    while todo:
        state = todo.pop()
        for nxt in outgoing_strong_drive(state, n):
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    full_run_count = n * (n - 1) + 1
    expected_closure = {((1 << length) - 1) << start
                        for length in range(1, n)
                        for start in range(n)
                        if start + length <= n}
    expected_closure |= {
        sum(1 << ((start + j) % n) for j in range(length))
        for length in range(1, n)
        for start in range(n)
        if start + length > n
    }
    expected_closure.add((1 << n) - 1)
    if seen != expected_closure or len(seen) != full_run_count:
        raise AssertionError(
            f"reachable closure mismatch: got {len(seen)}, expected {len(expected_closure)}"
        )

    if abs(mean_time - expected_time_formula) > 1e-8:
        raise AssertionError((n, mean_time, expected_time_formula))
    if abs(mean_fuel - expected_fuel_formula) > 1e-8:
        raise AssertionError((n, mean_fuel, expected_fuel_formula))
    return {
        "N": n,
        "majority_threshold_M": majority,
        "safe_one_run_states": len(safe),
        "full_forward_reachable_states_from_single_1": len(seen),
        "mean_time_from_single_1_to_wrong_majority_in_1_over_kcat": mean_time,
        "closed_form_mean_time": expected_time_formula,
        "expected_forward_fuel_equivalents_to_wrong_majority": mean_fuel,
        "closed_form_expected_fuel_equivalents": expected_fuel_formula,
        "status": "finite numerical generator check passed",
    }


def zero_run_ctmc_check(n: int) -> dict:
    """Check wrong-majority probability and return time for a 0-run in 1^N."""
    if n < 3 or n % 2 != 1:
        raise ValueError("use odd N >= 3")
    majority = (n + 1) // 2

    # Before either repair (z=0) or wrong majority (z=M), rates are 2c up, c down.
    interior = list(range(1, majority))
    ix = {z: i for i, z in enumerate(interior)}
    a = [[0.0] * len(interior) for _ in interior]
    for z in interior:
        i = ix[z]
        a[i][i] = 3.0
        if z - 1 in ix:
            a[i][ix[z - 1]] -= 1.0
        if z + 1 in ix:
            a[i][ix[z + 1]] -= 2.0
    rhs = [0.0] * len(interior)
    if majority > 1:
        rhs[ix[majority - 1]] = 2.0  # term from boundary value u_M=1
    prob = solve(a, rhs)[ix[1]]
    prob_formula = 1.0 / (2.0 * (1.0 - 2.0 ** (-majority)))

    # Mean time to return all the way to 1^N; z=N-1 has only one downward edge.
    states = list(range(1, n))
    jx = {z: i for i, z in enumerate(states)}
    b = [[0.0] * len(states) for _ in states]
    for z in states:
        i = jx[z]
        if z == n - 1:
            b[i][i] = 1.0
            b[i][jx[z - 1]] -= 1.0
        else:
            b[i][i] = 3.0
            if z - 1 in jx:
                b[i][jx[z - 1]] -= 1.0
            b[i][jx[z + 1]] -= 2.0
    mean_return = solve(b, [1.0] * len(states))[jx[1]]
    return_formula = 2 ** (n - 1) - 1
    if abs(prob - prob_formula) > 1e-10:
        raise AssertionError((n, prob, prob_formula))
    if abs(mean_return - return_formula) > 1e-8:
        raise AssertionError((n, mean_return, return_formula))
    return {
        "N": n,
        "majority_threshold_M": majority,
        "single_zero_wrong_majority_probability": prob,
        "closed_form_wrong_majority_probability": prob_formula,
        "mean_time_from_one_zero_to_all_one_in_1_over_kcat": mean_return,
        "closed_form_mean_repair_time": return_formula,
        "status": "finite numerical birth-death check passed",
    }


def main() -> None:
    a_values = [one_run_ctmc_check(n) for n in (3, 5, 7, 9, 11)]
    z_values = [zero_run_ctmc_check(n) for n in (3, 5, 7, 9, 11)]
    print(json.dumps({
        "rule": RULE,
        "active_enzyme_substrates": list(ACTIVE),
        "finite_drive_rates": {
            "forward": "q=c*exp(A)/(1+exp(A))",
            "reverse": "r=c/(1+exp(A))",
            "spontaneous": "s=k_spo per site, symmetric",
        },
        "closed_form_checks": a_values,
        "opposite_error_checks": z_values,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
