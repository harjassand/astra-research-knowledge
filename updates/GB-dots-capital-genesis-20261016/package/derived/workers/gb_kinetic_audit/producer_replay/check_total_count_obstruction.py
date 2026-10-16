#!/usr/bin/env python3
"""Exact actual-instance obstruction for arbitrary time-dependent S-only envelopes.

This is NOT simulation or a solution of the physical eight-site probability.
It constructs a finite adversarial row abstraction forced on any S-only
supercaloric envelope, checks its coefficients from actual elementary jumps,
and uses exact rational tridiagonal solves for its finite-deadline certificate.
No third-party libraries, downloads, or upstream executable code are used.
"""
from __future__ import annotations

import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction as F
from math import factorial
from pathlib import Path
from time import perf_counter

HERE = Path(__file__).resolve().parent
LO, HI, INITIAL, ALPHA = 16, 499, 400, 100
D = F("8.2207")
EDGES = [(0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (6, 7),
         (0, 4), (1, 5), (2, 6), (3, 7)]
DIRECTED = [(i, j) for i, j in EDGES for i, j in [(i, j), (j, i)]]


def birth(n):
    return F("2.676") * n * (n - 1) + F("108.102")


def death(n):
    return F("0.040") * n * (n - 1) * (n - 2) + F("37.881") * n


def representative(s):
    if s <= 121:
        # One count 16, all other counts at most 15. The corner containing
        # 16 is physical site 0; sites 1 and 4 determine diffusion success.
        rest, x = s - 16, [16]
        for _ in range(7):
            v = min(rest, 15)
            x.append(v)
            rest -= v
        assert rest == 0
    else:
        # No cap or target transition: at least one count is 100.
        k, r = divmod(s, 100)
        x = [100] * k + [r] + [0] * (7 - k)
    assert len(x) == 8 and sum(x) == s and 15 < max(x) <= 100
    return tuple(x)


def transitions(x):
    for i, n in enumerate(x):
        y = list(x)
        y[i] += 1
        yield tuple(y), birth(n)
        if n:
            y = list(x)
            y[i] -= 1
            yield tuple(y), death(n)
    for i, j in DIRECTED:
        if x[i]:
            y = list(x)
            y[i] -= 1
            y[j] += 1
            yield tuple(y), D * x[i]


def row_from_actual_jumps(s):
    x = representative(s)
    coeff = {"up": F(0), "down": F(0), "success": F(0), "same": F(0)}
    for y, rate in transitions(x):
        assert max(y) <= 162, "Representatives have no actual overflow."
        if max(y) <= 15:
            coeff["success"] += rate
        else:
            ds = sum(y) - s
            assert ds in (-1, 0, 1)
            coeff[{-1: "down", 0: "same", 1: "up"}[ds]] += rate
    b = sum(map(birth, x), F(0))
    a = sum(map(death, x), F(0))
    if s <= 121:
        target_diff = D * 16 * sum(x[j] <= 14 for i, j in DIRECTED if i == 0)
        kappa = death(16) + target_diff
        down = a - death(16)
    else:
        kappa, down = F(0), a
    assert coeff["up"] == b
    assert coeff["down"] == down
    assert coeff["success"] == kappa
    if s == LO:
        assert down == 0
    return b, down, kappa


def exact_tridiagonal(lower, diag, upper, rhs):
    """Thomas elimination with exact fractions, and complete residual replay."""
    c, z, pivots = [], [], []
    for i in range(len(diag)):
        pivot = diag[i] - (lower[i] * c[i - 1] if i else 0)
        assert pivot > 0
        pivots.append(pivot)
        c.append(upper[i] / pivot)
        z.append((rhs[i] - (lower[i] * z[i - 1] if i else 0)) / pivot)
    v = [F(0)] * len(diag)
    v[-1] = z[-1]
    for i in range(len(diag) - 2, -1, -1):
        v[i] = z[i] - c[i] * v[i + 1]
    for i in range(len(diag)):
        actual = diag[i] * v[i]
        if i:
            actual += lower[i] * v[i - 1]
        if i + 1 < len(diag):
            actual += upper[i] * v[i + 1]
        assert actual == rhs[i]
    return v, pivots


def descriptive(v):
    with localcontext() as ctx:
        ctx.prec = 45
        return str(Decimal(v.numerator) / Decimal(v.denominator))


def main():
    start = perf_counter()
    states = list(range(LO, HI + 1))
    rows = [row_from_actual_jumps(s) for s in states]
    lower = [-d for _, d, _ in rows]
    upper = [-b for b, _, _ in rows]
    # S=500 is artificial failure. Its actual continuation value is >=0.
    upper[-1] = F(0)
    diag0 = [b + d + k for b, d, k in rows]
    rhs_fail = [F(0)] * len(states)
    rhs_fail[-1] = rows[-1][0]
    failure, pf_pivots = exact_tridiagonal(lower, diag0, upper, rhs_fail)
    assert all(0 < v < 1 for v in failure)

    diag_alpha = [v - ALPHA for v in diag0]
    rhs_moment = [k for _, _, k in rows]
    rhs_moment[-1] += rows[-1][0]
    moment, m_pivots = exact_tridiagonal(lower, diag_alpha, upper, rhs_moment)
    assert all(v > 1 for v in moment)
    idx = INITIAL - LO
    # This is an all-state positive exponential-clock certificate, not a
    # numerical eigensolve or an assumed existence of an exponential moment.
    assert moment[idx] < 100
    assert failure[idx] < F(1, 10**18)
    # One positive Taylor term is enough to give an exact elementary bound.
    exp_lower = F(ALPHA ** ALPHA, factorial(ALPHA))
    assert exp_lower > 10**42
    deadline_failure_upper = F(1, 10**18) + F(1, 10**40)
    assert failure[idx] + moment[idx] / exp_lower < deadline_failure_upper

    code_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "status": "EXACT_BOUNDED_OBSTRUCTION_PASSED",
        "physical_probability_acquired": False,
        "cap": 162,
        "deadline": "1",
        "initial_physical_state": [50] * 8,
        "initial_total": INITIAL,
        "abstraction_domain": [LO, HI],
        "abstraction_states": len(states),
        "artificial_failure_total": HI + 1,
        "exponential_clock_alpha": ALPHA,
        "exact_actual_generator_rows_checked": len(states),
        "exact_full_linear_equations_checked": 2 * len(states),
        "all_elimination_pivots_positive": True,
        "all_failure_values_strictly_between_zero_and_one": True,
        "all_moment_certificate_values_strictly_above_one": True,
        "initial_failure_probability_descriptive": descriptive(failure[idx]),
        "initial_exponential_clock_certificate_descriptive": descriptive(moment[idx]),
        "initial_failure_probability_strict_upper": "1/10^18",
        "initial_exponential_clock_certificate_strict_upper": "100",
        "exp100_exact_taylor_term_strict_lower": "10^42",
        "finite_deadline_failure_strict_upper": "1/10^18 + 1/10^40",
        "all_S_only_supercaloric_envelope_initial_strict_lower":
            "1 - 1/10^18 - 1/10^40",
        "scope": "Arbitrary time-dependent nonlinear total-count continuation envelope; actual target prescribed one, cap overflow zero, terminal continuation nonnegative. This is NOT a lower bound on the physical target probability.",
        "script_sha256": code_hash,
        "wall_seconds_descriptive": perf_counter() - start,
    }
    (HERE / "total_count_obstruction_result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
