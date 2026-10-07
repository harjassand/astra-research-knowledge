#!/usr/bin/env python3
"""Exact bit-precision bottleneck for a one-pair Metropolis kernel."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path


def det_fraction(a: list[list[Fraction]]) -> Fraction:
    n = len(a)
    if n == 0:
        return Fraction(1)
    m = [row[:] for row in a]
    sign = 1
    result = Fraction(1)
    for col in range(n):
        pivot_row = next((r for r in range(col, n) if m[r][col]), None)
        if pivot_row is None:
            return Fraction(0)
        if pivot_row != col:
            m[col], m[pivot_row] = m[pivot_row], m[col]
            sign = -sign
        pivot = m[col][col]
        result *= pivot
        for r in range(col + 1, n):
            factor = m[r][col] / pivot
            for c in range(col + 1, n):
                m[r][c] -= factor * m[col][c]
            m[r][col] = Fraction(0)
    return sign * result


def ring_matrix(n: int, delta: Fraction) -> list[list[Fraction]]:
    f = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        f[i][(i + 1) % n] = Fraction(1)
        f[i][(i - 1) % n] = delta
    return f


def exact_determinants(f: list[list[Fraction]]) -> tuple[list[tuple[int, ...]], dict[tuple[int, ...], Fraction]]:
    n = len(f)
    k = n // 2
    all_states = list(combinations(range(n), k))
    universe = set(range(n))
    dets: dict[tuple[int, ...], Fraction] = {}
    for state in all_states:
        complement = sorted(universe.difference(state))
        minor = [[f[i][j] for j in complement] for i in state]
        d = det_fraction(minor)
        if d:
            dets[state] = d
    return all_states, dets


def one_swap_kernel(
    all_states: list[tuple[int, ...]],
    dets: dict[tuple[int, ...], Fraction],
    exchange_radius: int,
) -> tuple[list[tuple[int, ...]], dict[tuple[int, ...], Fraction], list[list[Fraction]]]:
    support = list(dets)
    weights = {s: dets[s] ** 2 for s in support}
    k = len(support[0])
    from math import comb

    degree = comb(k, exchange_radius) ** 2
    q = [[Fraction(0) for _ in support] for _ in support]
    support_index = {s: i for i, s in enumerate(support)}
    for i, state in enumerate(support):
        state_set = set(state)
        outgoing = Fraction(0)
        for proposed in all_states:
            if proposed == state or len(state_set.difference(proposed)) != exchange_radius:
                continue
            j = support_index.get(proposed)
            if j is None:
                continue
            acceptance = min(Fraction(1), weights[proposed] / weights[state])
            q[i][j] = acceptance / degree
            outgoing += q[i][j]
        q[i][i] = 1 - outgoing
    z = sum(weights.values())
    for i, a in enumerate(support):
        for j, b in enumerate(support):
            assert weights[a] * q[i][j] == weights[b] * q[j][i]
    return support, weights, q


def pair_kernel(q: list[list[Fraction]]) -> list[list[Fraction]]:
    m = len(q)
    states = [(i, j) for i in range(m) for j in range(m)]
    index = {s: i for i, s in enumerate(states)}
    p = [[Fraction(0) for _ in states] for _ in states]
    for r, (i, j) in enumerate(states):
        for ii in range(m):
            p[r][index[(ii, j)]] += q[i][ii] / 3
        for jj in range(m):
            p[r][index[(i, jj)]] += q[j][jj] / 3
        p[r][index[(j, i)]] += Fraction(1, 3)
    return p


def dirichlet(p: list[list[Fraction]], mu: list[Fraction], values: list[Fraction]) -> Fraction:
    return sum(
        mu[i] * p[i][j] * (values[i] - values[j]) ** 2 / 2
        for i in range(len(p))
        for j in range(len(p))
    )


def connected(support: list[tuple[int, ...]]) -> bool:
    unseen = set(support)
    todo = [unseen.pop()]
    while todo:
        state = set(todo.pop())
        for other in list(unseen):
            if len(state.difference(other)) == 1:
                unseen.remove(other)
                todo.append(other)
    return not unseen


def run(b: int) -> dict[str, object]:
    n = 6
    delta = Fraction(1, 2**b)
    f = ring_matrix(n, delta)
    all_states, dets = exact_determinants(f)
    support = list(dets)
    weights = {s: dets[s] ** 2 for s in support}
    assert len(all_states) == 20
    assert len(support) == 14
    assert connected(support)

    even = {0, 2, 4}
    sign = [Fraction(1 if len(set(s) & even) >= 2 else -1) for s in support]
    z = sum(weights.values())
    pi = [weights[s] / z for s in support]
    mean = sum(p * x for p, x in zip(pi, sign))
    variance = sum(p * (x - mean) ** 2 for p, x in zip(pi, sign))
    assert mean == 0 and variance == 1
    expected_z = 2 * (1 + delta**3) ** 2 + 6 * delta**2 + 6 * delta**4
    assert z == expected_z

    kernel_results = {}
    pi_pair = [pi[i] * pi[j] for i in range(len(support)) for j in range(len(support))]
    values_pair = [sign[i] + sign[j] for i in range(len(support)) for j in range(len(support))]
    for radius in (1, 2):
        _, _, q = one_swap_kernel(all_states, dets, radius)
        one_energy = dirichlet(q, pi, sign)
        p_pair = pair_kernel(q)
        pair_energy = dirichlet(p_pair, pi_pair, values_pair)
        assert pair_energy == Fraction(2, 3) * one_energy
        cross_min = Fraction(0)
        cross_count = 0
        cross_weight_counts = {"delta2": 0, "delta4": 0}
        for i, a in enumerate(support):
            for j in range(i + 1, len(support)):
                c = support[j]
                if len(set(a).difference(c)) != radius or sign[i] == sign[j]:
                    continue
                cross_count += 1
                contribution = min(weights[a], weights[c])
                cross_min += contribution
                if contribution == delta**2:
                    cross_weight_counts["delta2"] += 1
                elif contribution == delta**4:
                    cross_weight_counts["delta4"] += 1
                else:
                    raise AssertionError((radius, a, c, contribution))
        degree = 3**2  # binom(3,radius)^2 for both radius 1 and 2.
        assert one_energy == Fraction(4) * cross_min / (degree * z)
        energy_constant_lower = 1 / pair_energy
        kernel_results[str(radius)] = {
            "candidate_neighbor_count": degree,
            "crossing_edges": cross_count,
            "crossing_min_weight_counts": cross_weight_counts,
            "crossing_min_weight_sum": {"numerator": str(cross_min.numerator), "denominator": str(cross_min.denominator)},
            "one_replica_rayleigh_quotient": {"numerator": str(one_energy.numerator), "denominator": str(one_energy.denominator)},
            "one_replica_gap_upper_bound": {"numerator": str(one_energy.numerator), "denominator": str(one_energy.denominator)},
            "two_replica_additive_energy": {"numerator": str(pair_energy.numerator), "denominator": str(pair_energy.denominator)},
            "two_replica_L_lower_bound": {"numerator": str(energy_constant_lower.numerator), "denominator": str(energy_constant_lower.denominator)},
        }
    assert kernel_results["1"]["crossing_edges"] == 18
    assert kernel_results["1"]["crossing_min_weight_counts"] == {"delta2": 3, "delta4": 15}
    assert kernel_results["1"]["crossing_min_weight_sum"] == {"numerator": str((3*delta**2+15*delta**4).numerator), "denominator": str((3*delta**2+15*delta**4).denominator)}
    assert kernel_results["2"]["crossing_edges"] == 24
    assert kernel_results["2"]["crossing_min_weight_counts"] == {"delta2": 12, "delta4": 12}
    assert kernel_results["2"]["crossing_min_weight_sum"] == {"numerator": str((12*delta**2+12*delta**4).numerator), "denominator": str((12*delta**2+12*delta**4).denominator)}
    assert Fraction(int(kernel_results["1"]["two_replica_L_lower_bound"]["numerator"]), int(kernel_results["1"]["two_replica_L_lower_bound"]["denominator"])) >= Fraction(1) / delta**2
    assert Fraction(int(kernel_results["2"]["two_replica_L_lower_bound"]["numerator"]), int(kernel_results["2"]["two_replica_L_lower_bound"]["denominator"])) >= Fraction(9, 20) / delta**2

    return {
        "delta": f"1/2^{b}",
        "delta_fraction": {"numerator": str(delta.numerator), "denominator": str(delta.denominator)},
        "input_bits_per_nonzero_entry": b + 1,
        "matrix_dimension": n,
        "candidate_configurations": len(all_states),
        "supported_configurations": len(support),
        "support_graph_connected_under_one_swap": True,
        "pair_state_count": len(support) ** 2,
        "partition_function": {"numerator": str(z.numerator), "denominator": str(z.denominator)},
        "kernel_by_exchange_radius": kernel_results,
        "simple_L1_lower_bound": f"1/delta^2 = {str((Fraction(1)/delta**2).numerator)}/{str((Fraction(1)/delta**2).denominator)}",
        "simple_L2_lower_bound": f"9/(20*delta^2) = {str((Fraction(9,20)/delta**2).numerator)}/{str((Fraction(9,20)/delta**2).denominator)}",
    }


def main() -> None:
    cases = [run(b) for b in range(1, 13)]
    out = {
        "status": "PASS",
        "arithmetic": "exact Fractions and exact rational Gaussian elimination",
        "matrix_family": "n=6; F[i,i+1]=1 and F[i,i-1]=delta cyclically",
        "kernel": "exactly t selected/unselected label swaps with Metropolis acceptance for t=1,2; pair kernel adds independent coordinate updates and whole-layer swap",
        "claim_scope": "exact n=6 input-bit bottleneck for these local MH kernels; no universal-kernel lower bound",
        "cases": cases,
    }
    target = Path(__file__).with_name("r1_ring_mh_bottleneck_result.json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
