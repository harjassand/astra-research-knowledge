#!/usr/bin/env python3
"""Exact population checks, not calibration data or a hardware experiment.

Endpoint output is always parity of the physical increments actually used.
Unused suffixes in exhaustive enumeration are only probability bookkeeping.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb, log, exp, lgamma, tanh
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def trim(p):
    p = list(map(F, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(a, b):
    return trim([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def scale(a, c):
    return trim([c * x for x in a])


def mul_p(a):
    return trim([0, *a])


def mul_s(a):
    return add(a, scale(mul_p(a), -1))


def from_word_counts(counts, n):
    out = [F(0)] * (n + 1)
    for k, c in enumerate(counts):
        for j in range(n - k + 1):
            out[k + j] += c * comb(n - k, j) * (-1) ** j
    return trim(out)


def fast_high(bits):
    for t, b in enumerate(bits, 1):
        if b:
            return t, 1
    return len(bits), 0


def fast_low(bits, residual_horizon):
    if not bits[0]:
        return 1, 0
    for t in range(2, residual_horizon + 2):
        if bits[t - 1]:
            return t, 0
    return 1 + residual_horizon, 1


def slow_program(bits, first_horizon):
    first_seen = False
    for t, b in enumerate(bits, 1):
        if b:
            if first_seen:
                return t, 0
            first_seen = True
        if not first_seen and t == first_horizon:
            return t, 0
    return len(bits), int(first_seen)


def enumerate_program(n, fn, seeds):
    success = [F(0)] * (n + 1)
    cost = [F(0)] * (n + 1)
    total_paths = 0
    for bits in product((0, 1), repeat=n):
        k = sum(bits)
        for seed, seed_prob in seeds:
            used, output = fn(bits, seed)
            assert 1 <= used <= n
            assert output == sum(bits[:used]) % 2
            success[k] += seed_prob * output
            cost[k] += seed_prob * used
            total_paths += 1
    return from_word_counts(success, n), from_word_counts(cost, n), total_paths


@lru_cache(None)
def all_stop_trees(remaining):
    if remaining == 0:
        return (None,)
    smaller = all_stop_trees(remaining - 1)
    return (None,) + tuple((a, b) for a in smaller for b in smaller)


def tree_success(tree, parity):
    if tree is None:
        return (F(parity),)
    return add(mul_s(tree_success(tree[0], parity)),
               mul_p(tree_success(tree[1], 1 - parity)))


def zero_path_length(tree):
    return 0 if tree is None else 1 + zero_path_length(tree[0])


def exact_program_checks():
    rows, paths = [], 0
    for n in range(1, 11):
        high, hc, nh = enumerate_program(n, lambda bits, unused: fast_high(bits), [(None, F(1))])
        low, lc, nl = enumerate_program(n, fast_low, [(j, F(1, n)) for j in range(n)])
        a = trim([0] + [F((-1) ** (j + 1) * comb(n, j)) for j in range(1, n + 1)])
        assert high == a and scale(low, n) == a
        assert hc == trim(a[1:])
        assert lc == add((F(2),), scale(trim(a[1:]), F(-1, n)))
        slow_count = 0
        for m in range(1, n + 1):
            slow, _, nc = enumerate_program(n, slow_program, [(m, F(1))])
            expected = trim([0] + [F(m * comb(n - 1, j) * (-1) ** j) for j in range(n)])
            assert slow == expected
            slow_count += nc
        paths += nh + nl + slow_count
        for r in (F(1), F(n), F(n + 1, 2)):
            if n == 1:
                fitted_low = low
            else:
                w = (F(n) / r - 1) / (n - 1)
                assert 0 <= w <= 1
                fitted_low = add(scale(high, w), scale(low, 1 - w))
            assert high == scale(fitted_low, r)
        rows.append({"cap": n, "high_first_coefficient": str(high[1]),
                     "low_first_coefficient": str(low[1]), "all_identities": True})
    deterministic = []
    for n in range(1, 5):
        subtrees, families, policy_count = all_stop_trees(n - 1), {}, 0
        for a in subtrees:
            for b in subtrees:
                tree = (a, b)
                poly = tree_success(tree, 0)
                derivative = poly[1]
                assert derivative == zero_path_length(tree) and 1 <= derivative <= n
                families.setdefault(scale(poly, 1 / derivative), []).append(derivative)
                policy_count += 1
        largest = max(max(xs) / min(xs) for xs in families.values())
        assert largest == n
        deterministic.append({"cap": n, "policies": policy_count,
                              "max_exact_ratio": str(largest)})
    return {"polynomial_checks": rows, "literal_path_seed_cases": paths,
            "all_deterministic_small_policies": deterministic}


def dyadic_slopes(r, cap):
    assert F(1) <= r <= cap
    if r == cap:
        return F(cap), F(1), 0
    u, v, bits, denominator = r.numerator, r.denominator, 0, 1
    while True:
        k = (denominator + v - 1) // v
        high, low = F(u * k, denominator), F(v * k, denominator)
        if high <= cap:
            assert 1 <= low <= high <= cap and high / low == r
            return high, low, bits
        bits, denominator = bits + 1, 2 * denominator


def selector_checks():
    rows = []
    for r, cap in [(F(3, 2), 2), (F(1001, 1000), 2), (F(1999, 1000), 2),
                   (F(7, 3), 3), (F(8), 8)]:
        high, low, bits = dyadic_slopes(r, cap)
        for slope in (high, low):
            m = slope.numerator // slope.denominator
            part = slope - m
            assert 0 <= part < 1 and (part * 2 ** bits).denominator == 1
            assert 1 <= m <= cap and (not part or m + 1 <= cap)
        rows.append({"ratio": str(r), "cap": cap, "bits": bits,
                     "high_slope": str(high), "low_slope": str(low)})
    return rows


def gibbs_fixture():
    d = 4
    states = list(product((-1, 1), repeat=d))
    ix = {x: i for i, x in enumerate(states)}
    edges = [(i, j) for i in range(d) for j in range(i)]
    weights = [4 ** sum(x[i] == x[j] for i, j in edges) for x in states]
    z, ps = sum(weights), (F(1, 20), F(1, 8), F(1, 4), F(9, 20))
    pi = [F(w, z) for w in weights]
    matrix = [[F(0) for _ in states] for _ in states]
    local, max_cap = [], 0
    for xi, x in enumerate(states):
        for site in range(d):
            alignment = x[site] * sum(x[j] for j in range(d) if j != site)
            cap = 2 ** (2 * abs(alignment))
            a = 1 - (1 - ps[site]) ** cap
            flip = a / cap if alignment > 0 else a
            y = list(x)
            y[site] *= -1
            yi = ix[tuple(y)]
            matrix[xi][yi] += flip / d
            matrix[xi][xi] += (1 - flip) / d
            cost = 2 - a / (cap * ps[site]) if alignment > 0 else a / ps[site]
            assert 1 <= cost <= cap
            local.append((xi, site, yi, cap, flip, cost))
            max_cap = max(max_cap, cap)
    for row in matrix:
        assert sum(row) == 1 and all(p >= 0 for p in row)
    for i in range(len(states)):
        for j in range(len(states)):
            assert pi[i] * matrix[i][j] == pi[j] * matrix[j][i]
    assert [sum(pi[i] * matrix[i][j] for i in range(len(states))) for j in range(len(states))] == pi
    assert all(matrix[i][i] > 0 for i in range(len(states)))
    cost = sum(pi[xi] * c / d for xi, _, _, _, _, c in local)
    assert 1 <= cost <= 2
    (HERE / "SHARP_GIBBS_EXACT_KERNEL.json").write_text(json.dumps({
        "states": states, "native_p": list(map(str, ps)), "target_weights": weights,
        "partition_sum_integer_weights": z, "target": list(map(str, pi)),
        "kernel": [[str(p) for p in row] for row in matrix],
        "local_rows": [{"state": states[xi], "site": i, "end_state": states[yi],
                        "cap": n, "flip_probability": str(f), "expected_calls": str(c)}
                       for xi, i, yi, n, f, c in local]}, indent=2) + "\n")
    return {"graph": "K4", "beta_times_J": "log(2)", "states": 16,
            "local_rows": len(local), "detailed_balance_pairs": 256,
            "max_native_cap": max_cap, "max_residual_selector_bits": max_cap.bit_length() - 1,
            "uniform_site_selector_bits": 2, "stationary_mean_calls": str(cost),
            "stationary_mean_calls_float": float(cost),
            "target_all_aligned_mass": str(pi[0] + pi[-1]),
            "full_physical_time_stationarity_claim": False}


def sector_counterexample():
    plus, old_h = (F(1, 4), F(3, 4)), (F(1, 2), F(1, 2))
    factors = tuple(1 + 2 * p for p in plus)
    total = sum(w * z for w, z in zip(old_h, factors))
    new_h = tuple(w * z / total for w, z in zip(old_h, factors))
    new_plus = tuple(3 * p / z for p, z in zip(plus, factors))
    formal = sum(w * p for w, p in zip(new_h, new_plus))
    achieved = sum(w * p for w, p in zip(old_h, new_plus))
    assert new_h == (F(3, 8), F(5, 8)) and new_plus == (F(1, 2), F(9, 10))
    assert formal == F(3, 4) and achieved == F(7, 10)
    return {"original_hidden": list(map(str, old_h)), "baseline_plus_given_hidden": list(map(str, plus)),
            "tilted_hidden": list(map(str, new_h)), "tilted_plus_given_hidden": list(map(str, new_plus)),
            "formal_visible_plus": str(formal), "conserved_sector_visible_equilibrium": str(achieved)}


def curie_weiss(n, beta, h):
    ms = [(2 * k - n) / n for k in range(n + 1)]
    base = [lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1) +
            n * beta * m * m / 2 for k, m in enumerate(ms)]
    def mean_logz(logweights):
        peak = max(logweights)
        weights = [exp(w - peak) for w in logweights]
        z = sum(weights)
        return sum(m * w for m, w in zip(ms, weights)) / z, peak + log(z)
    m0, z0 = mean_logz(base)
    m, z = mean_logz([v + n * h * x for v, x in zip(base, ms)])
    assert abs(m0) < 1e-12
    return {"sites": n, "field": h, "row_TV_bound": h / 2,
            "target_mean": m0, "perturbed_mean": m,
            "pressure_difference": (z - z0) / n, "KL_per_site": h * m - (z - z0) / n}


def phase_tables():
    beta, lo, hi = 2.0, 0.5, 1.0
    for _ in range(100):
        m = (lo + hi) / 2
        if tanh(beta * m) > m:
            lo = m
        else:
            hi = m
    m = (lo + hi) / 2
    return {"scope": "Floating population illustration; asymptotic theorem is analytic",
            "beta": beta, "positive_phase": m, "limit_for_h_1_over_n": m * tanh(m),
            "h_1_over_n": [curie_weiss(n, beta, 1 / n) for n in (20, 50, 100, 200, 500, 1000, 2000)],
            "h_1_over_sqrt_n": [curie_weiss(n, beta, n ** -0.5) for n in (20, 50, 100, 200, 500, 1000, 2000)]}


def main():
    report = {"scope": "Exact ideal-model population checks, not acquired data or hardware",
              "program_checks": exact_program_checks(), "finite_bit_selectors": selector_checks(),
              "gibbs_fixture": gibbs_fixture(), "sector_obstruction": sector_counterexample(),
              "phase_sensitivity": phase_tables()}
    report["sha256"] = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                        for name in ("check_sharp_finite_call.py", "SHARP_GIBBS_EXACT_KERNEL.json")}
    output = HERE / "SHARP_FINITE_CALL_CHECKS.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"path_seed_cases": report["program_checks"]["literal_path_seed_cases"],
                      "gibbs_fixture": report["gibbs_fixture"],
                      "sector_obstruction": report["sector_obstruction"],
                      "phase_limit": report["phase_sensitivity"]["limit_for_h_1_over_n"],
                      "result": str(output)}, indent=2))


if __name__ == "__main__":
    main()
