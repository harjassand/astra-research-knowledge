#!/usr/bin/env python3
"""Exact two-block tensor test against a whole-system complement update."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import sys

import r1_ring_mh_bottleneck as ring


def direct_block_matrix(delta: Fraction) -> list[list[Fraction]]:
    n = 12
    f = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for base in (0, 6):
        for i in range(base, base + 6):
            f[i][base + (i - base + 1) % 6] = 1
            f[i][base + (i - base - 1) % 6] = delta
    return f


def direct_states(f: list[list[Fraction]]) -> dict[tuple[int, ...], Fraction]:
    n = len(f)
    k = n // 2
    universe = set(range(n))
    out = {}
    for state in combinations(range(n), k):
        complement = sorted(universe.difference(state))
        minor = [[f[i][j] for j in complement] for i in state]
        det = ring.det_fraction(minor)
        if det:
            out[state] = det**2
    return out


def product_kernel(q6: list[list[Fraction]]) -> list[list[Fraction]]:
    m = len(q6)
    support = [(a, b) for a in range(m) for b in range(m)]
    index = {x: i for i, x in enumerate(support)}
    q = [[Fraction(0) for _ in support] for _ in support]
    for r, (a, b) in enumerate(support):
        q[r][r] += Fraction(1, 2)  # cross-block one-swaps reject
        for aa in range(m):
            q[r][index[(aa, b)]] += q6[a][aa] / 4
        for bb in range(m):
            q[r][index[(a, bb)]] += q6[b][bb] / 4
    return q


def complement_metropolis(
    local_support: list[tuple[int, ...]],
    local_weights: dict[tuple[int, ...], Fraction],
    q_global: list[list[Fraction]],
) -> list[list[Fraction]]:
    m = len(local_support)
    product_states = [(a, b) for a in range(m) for b in range(m)]
    index = {x: i for i, x in enumerate(product_states)}
    local_index = {x: i for i, x in enumerate(local_support)}
    q = [[Fraction(0) for _ in product_states] for _ in product_states]
    for r, (a, b) in enumerate(product_states):
        ca = tuple(i for i in range(6) if i not in set(local_support[a]))
        cb = tuple(i for i in range(6) if i not in set(local_support[b]))
        aa = local_index[ca]
        bb = local_index[cb]
        target = index[(aa, bb)]
        w0 = local_weights[local_support[a]] * local_weights[local_support[b]]
        w1 = local_weights[local_support[aa]] * local_weights[local_support[bb]]
        accept = min(Fraction(1), w1 / w0)
        q[r][target] += accept
        q[r][r] += 1 - accept
    return q


def mix(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[(x + y) / 2 for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def run(b: int) -> dict[str, object]:
    delta = Fraction(1, 2**b)
    f6 = ring.ring_matrix(6, delta)
    all6, dets6 = ring.exact_determinants(f6)
    support6, weights6, q6 = ring.one_swap_kernel(all6, dets6, 1)
    assert len(support6) == 14
    z6 = sum(weights6.values())

    f12 = direct_block_matrix(delta)
    direct12 = direct_states(f12)
    assert len(list(combinations(range(12), 6))) == 924
    assert len(direct12) == 196

    expected = {}
    for a in support6:
        for c in support6:
            state = tuple(sorted(a + tuple(i + 6 for i in c)))
            expected[state] = weights6[a] * weights6[c]
    assert direct12 == expected

    support = [(a, c) for a in support6 for c in support6]
    weights = {s: weights6[s[0]] * weights6[s[1]] for s in support}
    z = sum(weights.values())
    assert z == z6**2
    pi = [weights[s] / z for s in support]
    even = {0, 2, 4}
    local_sign = {a: Fraction(1 if len(set(a) & even) >= 2 else -1) for a in support6}
    h = [local_sign[a] * local_sign[c] for a, c in support]
    mean = sum(p * x for p, x in zip(pi, h))
    variance = sum(p * (x - mean) ** 2 for p, x in zip(pi, h))
    assert mean == 0 and variance == 1

    q_global = product_kernel(q6)
    q_complement = complement_metropolis(support6, weights6, q_global)
    # Whole-system complement is an involution; Metropolis is reversible.
    q = mix(q_global, q_complement)
    for i, s in enumerate(support):
        for j, t in enumerate(support):
            assert weights[s] * q[i][j] == weights[t] * q[j][i]
    one_energy = ring.dirichlet(q, pi, h)

    sign6 = [local_sign[s] for s in support6]
    pi6 = [weights6[s] / z6 for s in support6]
    e6 = ring.dirichlet(q6, pi6, sign6)
    assert one_energy == e6 / 4

    # The two-replica kernel updates A by Q, B by Q, or swaps A and B.
    # For H(A,B)=h(A)+h(B), the swap is invariant and the other two terms
    # contribute (1/3)E_Q(h) each.
    pair_energy = Fraction(2, 3) * one_energy
    l_lower = 1 / pair_energy
    expected_l = Fraction(27) * z6 / (2 * (3 * delta**2 + 15 * delta**4))
    assert l_lower == expected_l
    assert l_lower >= 4 / delta**2

    return {
        "delta": f"1/2^{b}",
        "matrix_dimension": 12,
        "candidate_configurations": 924,
        "supported_configurations": 196,
        "two_replica_supported_states": 196**2,
        "direct_full_determinant_factorization_checked": True,
        "product_partition_function": {"numerator": str(z.numerator), "denominator": str(z.denominator)},
        "one_block_partition_function": {"numerator": str(z6.numerator), "denominator": str(z6.denominator)},
        "variance_of_sign_product": 1,
        "one_block_local_energy": {"numerator": str(e6.numerator), "denominator": str(e6.denominator)},
        "one_replica_energy_after_global_one_swap_and_whole_complement": {"numerator": str(one_energy.numerator), "denominator": str(one_energy.denominator)},
        "two_replica_additive_energy": {"numerator": str(pair_energy.numerator), "denominator": str(pair_energy.denominator)},
        "required_energy_constant_lower_bound": {"numerator": str(l_lower.numerator), "denominator": str(l_lower.denominator)},
        "simple_lower_bound": f"4/delta^2 = {str((Fraction(4)/delta**2).numerator)}/{str((Fraction(4)/delta**2).denominator)}",
    }


def main() -> None:
    cases = [run(b) for b in range(1, 7)]
    result = {
        "status": "PASS",
        "arithmetic": "exact Fractions; direct determinants; no spectral floating point",
        "matrix_family": "F=diag(F_delta,F_delta), with F_delta the 6-cycle plus reverse edges delta",
        "one_replica_kernel": "one global selected/unselected swap with MH, or whole 12-label complement with MH, each probability 1/2",
        "pair_kernel": "update replica A, update replica B, or swap replica layers, each probability 1/3",
        "claim_scope": "tensor test of this specified whole-complement kernel; no universal-kernel lower bound",
        "cases": cases,
    }
    p = Path(__file__).with_name("r2_macro_complement_tensor_result.json")
    p.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
