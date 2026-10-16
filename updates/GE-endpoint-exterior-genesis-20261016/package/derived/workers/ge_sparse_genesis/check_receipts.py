"""Independent integer-only witness checker; does not import the proposer."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import json
import math
import time


def independently_build_killed(n, edges, rates):
    states = list(combinations(range(n), 2))
    lookup = {p: j for j, p in enumerate(states)}
    result = [dict() for _ in states]
    for e, r in zip(edges, rates):
        if F(r).denominator != 1 or r < 0:
            raise ValueError("noninteger or negative rate")
        a, b = sorted(e)
        for i, p in enumerate(states):
            occupied = (a in p) + (b in p)
            if occupied == 2:
                result[i][i] = result[i].get(i, 0) + 2 * r
            elif occupied == 1:
                moving, target = (a, b) if a in p else (b, a)
                other = p[1] if p[0] == moving else p[0]
                j = lookup[tuple(sorted((target, other)))]
                result[i][i] = result[i].get(i, 0) + r
                result[i][j] = result[i].get(j, 0) - r
    return result, [lookup[tuple(sorted(e))] for e in edges]


def check(data):
    begin = time.perf_counter()
    g = data["graph"]
    n, edges = g["n"], g["edges"]
    k, s, p = data["shape"], data["shift"], data["precision_bits"]
    assert k >= 2 and isinstance(s, int) and s > 0 and p >= 1
    assert data["horizon_exact"] == "1"
    assert len(data["dyadic_solve_witnesses"]) == len(data["residual_receipts"]) == 2
    all_lower, all_upper = [], []
    total_residuals = 0
    max_error = F(0)
    for rates, history, receipts in zip([g["original_rates"], g["comparison_rates"]], data["dyadic_solve_witnesses"], data["residual_receipts"]):
        h, ei = independently_build_killed(n, edges, rates)
        assert len(history) == len(receipts) == k - 1
        q = 1 << p
        prev = [q] * len(h)
        error = F(0)
        lower, upper = [], []
        for j, (v, receipt) in enumerate(zip(history, receipts), 1):
            assert len(v) == len(h) and all(isinstance(x, int) for x in v)
            residual = 0
            for i, row in enumerate(h):
                residual = max(residual, abs(s * prev[i] - s * v[i] - sum(w * v[z] for z, w in row.items())))
            assert receipt["power"] == j
            assert receipt["residual_numerator"] == residual
            assert receipt["grid_denominator_bits"] == p
            error += F(residual, s * q)
            assert error == F(receipt["accumulated_error_exact"])
            lower.append([max(F(0), F(v[e], q) - error) for e in ei])
            upper.append([min(F(1), F(v[e], q) + error) for e in ei])
            assert all(0 <= a <= b <= 1 for a, b in zip(lower[-1], upper[-1]))
            prev = v
            total_residuals += 1
            max_error = max(max_error, error)
        all_lower.append(lower)
        all_upper.append(upper)
    m = data["gamma_cdf_taylor_terms"]
    assert m >= k - 1
    # Independent direct factorial formula, not the proposer's recurrence.
    lower_exp = sum((F(s ** i, math.factorial(i)) for i in range(m + 1)), F(0))
    tail_poly = sum((F(s ** i, math.factorial(i)) for i in range(k)), F(0))
    gl = 1 - tail_poly / lower_exp
    assert gl > 0 and gl == F(data["gamma_cdf_lower_exact"])
    delta = [abs(a - b) for a, b in zip(g["original_rates"], g["comparison_rates"])]
    lower = F(0)
    upper = F(0)
    for j in range(k - 1):
        lower += sum(d * a * b for d, a, b in zip(delta, all_lower[0][j], all_lower[1][k - 2 - j]))
        upper += sum(d * a * b for d, a, b in zip(delta, all_upper[0][j], all_upper[1][k - 2 - j]))
    lower /= k - 1
    upper /= k - 1
    bound = upper / gl
    assert lower == F(data["averaged_b_lower_exact"])
    assert upper == F(data["averaged_b_upper_exact"])
    assert bound == F(data["Duhamel_upper_exact"])
    assert data["finite_generator_certified"] == (bound <= F(data["tolerance_exact"]))
    return dict(checked=True, pair_states=n * (n - 1) // 2, exact_shifted_residuals=total_residuals,
                bound_exact=str(bound), bound_float=float(bound),
                maximum_accumulated_action_error_exact=str(max_error),
                checker_seconds=time.perf_counter() - begin)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("receipt", type=Path)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    result = check(json.loads(a.receipt.read_text()))
    if a.output:
        a.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
