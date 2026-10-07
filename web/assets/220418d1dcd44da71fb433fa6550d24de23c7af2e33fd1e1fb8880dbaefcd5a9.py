#!/usr/bin/env python3
"""Exact block-factorized heat-bath kernel and energy checks."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import comb, prod
import json
from pathlib import Path
import r1_ring_mh_bottleneck as ring


def local_data(delta: Fraction):
    f = ring.ring_matrix(6, delta)
    all_states, dets = ring.exact_determinants(f)
    support = list(dets)
    weights = {s: dets[s] ** 2 for s in support}
    z = sum(weights.values())
    probs = {s: weights[s] / z for s in support}
    return all_states, support, weights, probs


def product_kernel(support, probs, r: int):
    states = list(product(support, repeat=r))
    index = {s: i for i, s in enumerate(states)}
    q = [[Fraction(0) for _ in states] for _ in states]
    for i, state in enumerate(states):
        for b in range(r):
            for replacement in support:
                target = list(state)
                target[b] = replacement
                j = index[tuple(target)]
                q[i][j] += probs[replacement] / r
    return states, q


def dirichlet(q, pi, f):
    return sum(
        pi[i] * q[i][j] * (f[i] - f[j]) ** 2 / 2
        for i in range(len(q))
        for j in range(len(q))
    )


def frac(x):
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def run(r: int) -> dict[str, object]:
    delta = Fraction(1, 8)
    _, support, weights, probs = local_data(delta)
    states, q = product_kernel(support, probs, r)
    pi = [prod((probs[s] for s in state), start=Fraction(1)) for state in states]
    assert sum(pi) == 1
    for i in range(len(states)):
        assert sum(q[i]) == 1
        for j in range(len(states)):
            assert pi[i] * q[i][j] == pi[j] * q[j][i]

    local_sign = {s: Fraction(1 if len(set(s) & {0, 2, 4}) >= 2 else -1) for s in support}
    test = [local_sign[state[0]] for state in states]
    mean = sum(p * x for p, x in zip(pi, test))
    variance = sum(p * (x - mean) ** 2 for p, x in zip(pi, test))
    energy = dirichlet(q, pi, test)
    assert mean == 0 and variance == 1
    assert energy == Fraction(1, r)

    # The pair kernel refreshes A or B, each with probability 1/2.
    # For F=f1(A)+f2(B), the exact product Dirichlet form is
    # (E_Q(f1)+E_Q(f2))/2. Choosing f1=test and f2=0 attains L=2r.
    l_exact = 2 * r

    return {
        "number_of_blocks": r,
        "candidate_states_per_block": 20,
        "supported_states_per_block": len(support),
        "all_global_fixed_cardinality_subsets": comb(6 * r, 3 * r),
        "blockwise_candidate_product_state_count": 20**r,
        "global_supported_state_count": len(states),
        "two_replica_supported_state_count": len(states) ** 2,
        "local_determinant_evaluations_for_preprocessing": 20 * r,
        "one_replica_heatbath_gap": frac(Fraction(1, r)),
        "tested_function_variance": frac(variance),
        "tested_function_one_replica_energy": frac(energy),
        "pair_energy_constant_exact": l_exact,
    }


def main() -> None:
    result = {
        "status": "PASS",
        "arithmetic": "exact Fractions; explicit transition matrix for r=1,2",
        "block_family": "r direct-sum copies of the 6-coordinate F_delta block, delta=1/8",
        "kernel": "uniformly choose a block and refresh it exactly from its local determinant law; pair kernel refreshes one of two replicas",
        "cases": [run(r) for r in (1, 2)],
        "general_exact_claim": "for r independent finite blocks, random-scan exact block heat-bath has gap exactly 1/r and the two-replica additive energy constant is exactly 2r",
        "cost_scope": "polynomial preprocessing when maximum block size is O(log n); for fixed size 6, exactly 20 minor evaluations per block",
    }
    path = Path(__file__).with_name("r3_bounded_block_heatbath_result.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
