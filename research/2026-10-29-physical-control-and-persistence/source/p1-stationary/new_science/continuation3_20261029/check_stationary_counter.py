#!/usr/bin/env python3
"""Exact model checks of the integer counter, directed kernels and incumbent.

No apparatus acquisition. Every arithmetic comparison is rational; the
literal simulator makes policy decisions from weights, phase, and direction.
"""
from fractions import Fraction as F
from math import ceil
from pathlib import Path
import hashlib
import json
from check_reversible_excursion_compiler import (
    zeros, eye, mul, add, scale, row_times, normalize, reversible,
    make_reversible, controller as binary_controller, jsonable)

HERE = Path(__file__).resolve().parent


def inverse(a):
    n = len(a)
    aug = [row[:] + identity for row, identity in zip(a, eye(n))]
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col])
        aug[pivot], aug[col] = aug[col], aug[pivot]
        value = aug[col][col]
        aug[col] = [x / value for x in aug[col]]
        for i in range(n):
            if i != col:
                factor = aug[i][col]
                aug[i] = [x - factor * y for x, y in zip(aug[i], aug[col])]
    return [row[n:] for row in aug]


def compiled(p, weights, direction, wrong_phase=False):
    n = len(p)
    low, high = min(weights), max(weights)
    cap = (high + low - 1) // low
    k, occ = zeros(n), zeros(n)
    clock = [[[F(0)] * n for _ in range(cap + 1)] for _ in range(n)]
    for start in range(n):
        phase_count = high if wrong_phase else weights[start]
        active = {(start, phase): F(1, phase_count) for phase in range(phase_count)}
        for call in range(1, cap + 1):
            nxt = {}
            for (x, phase), mass in active.items():
                occ[start][x] += mass
                phase2 = (phase + direction * low) % high
                for y, prob in enumerate(p[x]):
                    pathmass = mass * prob
                    if phase2 < weights[y]:
                        k[start][y] += pathmass
                        clock[start][call][y] += pathmass
                    elif pathmass:
                        nxt[(y, phase2)] = nxt.get((y, phase2), F(0)) + pathmass
            active = nxt
        assert not active
        assert sum(k[start]) == 1
        assert sum(clock[start][0]) == 0
        assert sum(occ[start]) == sum(t * sum(clock[start][t]) for t in range(cap + 1))
    return k, occ, clock


def thinning(p, weights):
    """Exact ordinary independent Bernoulli marking, not finite truncation."""
    high = max(weights)
    accept = [F(w, high) for w in weights]
    fail = [[p[i][j] * (1 - accept[j]) for j in range(len(p))] for i in range(len(p))]
    accepted = [[p[i][j] * accept[j] for j in range(len(p))] for i in range(len(p))]
    occupation = inverse(add(eye(len(p)), scale(F(-1), fail)))
    return mul(occupation, accepted), occupation, fail


def directed(p, mu):
    q = [row[:] for row in p]
    for i in range(len(q)):
        f = F(1, 1024) / mu[i]
        q[i][(i + 1) % len(q)] += f
        q[i][i] -= f
    assert row_times(mu, q) == mu
    assert any(mu[i] * q[i][j] != mu[j] * q[j][i]
               for i in range(len(q)) for j in range(len(q)))
    assert all(min(row) >= 0 and sum(row) == 1 for row in q)
    return q


def flux_defect(k, nu):
    return max(abs(nu[i] * k[i][j] - nu[j] * k[j][i])
               for i in range(len(k)) for j in range(len(k)))


def main():
    p_rev, mu = make_reversible([1, 2, 3, 4], 19)
    p_dir = directed(p_rev, mu)
    weight_sets = [[1, 2, 4, 8], [2, 3, 5, 7], [3, 4, 6, 8],
                   [3, 3, 6, 9], [2, 2, 2, 2], [5, 6, 7, 8],
                   [2, 4, 6, 8], [1, 1, 4, 4]]
    cases = []
    for name, p in [("reversible", p_rev), ("directed_stationary", p_dir)]:
        for weights in weight_sets:
            z = sum(w * m for w, m in zip(weights, mu))
            nu = [w * m / z for w, m in zip(weights, mu)]
            cap = ceil(F(max(weights), min(weights)))
            plus, oplus, cplus = compiled(p, weights, +1)
            minus, ominus, cminus = compiled(p, weights, -1)
            for k, occ in [(plus, oplus), (minus, ominus)]:
                assert row_times(nu, k) == nu
                assert row_times(nu, occ) == [max(weights) * m / z for m in mu]
            sym = scale(F(1, 2), add(plus, minus))
            if name == "reversible":
                assert all(nu[i] * plus[i][j] == nu[j] * minus[j][i]
                           for i in range(4) for j in range(4))
                assert all(nu[i] * cplus[i][t][j] == nu[j] * cminus[j][t][i]
                           for i in range(4) for j in range(4) for t in range(cap + 1))
                reversible(sym, nu)
            ordinary, ordinary_occ, fail = thinning(p, weights)
            assert row_times(nu, ordinary) == nu
            assert row_times(nu, ordinary_occ) == row_times(nu, oplus)
            survivor = nu[:]
            for _ in range(cap):
                survivor = row_times(survivor, fail)
            tail = sum(survivor)
            if min(weights) != max(weights):
                assert tail > 0
            else:
                assert tail == 0
            cases.append({"source": name, "weights": weights,
                          "target": nu, "sharp_native_call_cap": cap,
                          "counter_stationary_mean_calls": F(max(weights)) / z,
                          "thinning_stationary_mean_calls": F(max(weights)) / z,
                          "thinning_probability_exceeding_counter_cap": tail,
                          "symmetrized_endpoint_flux_defect": flux_defect(sym, nu),
                          "one_direction_endpoint_flux_defect": flux_defect(plus, nu),
                          "counter_plus_kernel": plus,
                          "counter_minus_kernel": minus})
    # Literal reduction to the already independently checked excursion rule.
    p6, mu6 = make_reversible([1, 2, 3, 3, 2, 1], 7)
    for ncap in [1, 2, 4, 8]:
        k, occ, clock = compiled(p6, [1, 1, 1, ncap, ncap, ncap], +1)
        special, special_occ, special_clock = binary_controller(p6, [0, 1, 2], {ncap: F(1)})
        assert k == special and occ == special_occ and clock == special_clock
    # Wrong unconditional phase refresh is an actual failure, not a valid variant.
    p2 = [[F(3, 4), F(1, 4)], [F(1, 4), F(3, 4)]]
    wrong, _, _ = compiled(p2, [1, 4], +1, wrong_phase=True)
    intended = [F(1, 5), F(4, 5)]
    wrong_stationary = normalize([wrong[1][0], wrong[0][1]])
    assert row_times(intended, wrong) != intended
    result = {"scope": "Exact finite population-model checks; no physical measurements",
              "cases": cases,
              "native_reversible": p_rev, "native_directed": p_dir, "baseline": mu,
              "binary_reduction_cases": 4,
              "wrong_phase_counterexample": {
                  "weights": [1, 4], "p": F(1, 4), "kernel": wrong,
                  "intended": intended, "actual_stationary": wrong_stationary},
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    target = HERE / "STATIONARY_COUNTER_CHECKS.json"
    target.write_text(json.dumps(jsonable(result), indent=2) + "\n")
    print(json.dumps({"cases": len(cases), "binary_reductions": 4,
                      "status": "all exact assertions passed", "output": str(target)}))


if __name__ == "__main__":
    main()
