"""Exact finite diagnostics for the reduction; not a proof of NP-hardness."""
from fractions import Fraction as F
from itertools import product
from random import Random
import json


def subset_sums(weights):
    sums = {0}
    for weight in weights:
        sums |= {s + weight for s in sums}
    return sums


def construct(weights, t):
    assert sum(weights) % 2 == 0 and min(weights) > 0 and t >= 2
    B = sum(weights) // 2
    K = B + 1
    if (B + K) % t == 0:
        K += 1
    target = B + K
    assert target % t and K > B
    derived = [t * w for w in weights + [K, K]] + [target]
    total = (2 * t + 1) * target
    assert sum(derived) == total
    return derived, target, total


def direct_ratio(probabilities, endpoints):
    mean = sum(p * z for p, z in zip(probabilities, endpoints))
    return sum(p * z * z for p, z in zip(probabilities, endpoints)) / mean**2


def verify(weights, t, direct=False):
    derived, target, total = construct(weights, t)
    a = F(t, t + 1)
    C = F((2 * t + 1) ** 2, 4 * t * (t + 1))
    gap = F(1, 4 * t * (t + 1) ** 3 * target**2)
    threshold = C - gap / 2
    original_yes = sum(weights) // 2 in subset_sums(weights)
    masses = [F(y, total) for y in subset_sums(derived)]
    ratios = [(F(t*t) + (2*t + 1)*r)/(F(t) + r)**2 for r in masses]
    maximum = max(ratios)
    assert (maximum == C) == original_yes
    assert (maximum > threshold) == original_yes
    if not original_yes:
        assert maximum <= C - gap
    for r, ratio in zip(masses, ratios):
        assert C - ratio == ((2*t+1)*r-t)**2/(4*t*(t+1)*(t+r)**2)
    if direct:
        probabilities = [F(w, total) for w in derived]
        exhaustive = max(direct_ratio(probabilities, z)
                         for z in product([a, F(1)], repeat=len(derived)))
        assert exhaustive == maximum
    return original_yes, maximum, C, gap


def main():
    rng = Random(20261010)
    rows = []
    cases = [[1, 1], [1, 3], [1, 2, 3], [2, 2, 2], [1, 1, 1, 5],
             [2, 4, 6, 8], [3, 5, 7, 9]]
    for _ in range(120):
        w = [rng.randrange(1, 30) for _ in range(rng.randrange(2, 10))]
        if sum(w) % 2:
            w[-1] += 1
        cases.append(w)
    yes = no = 0
    for index, weights in enumerate(cases):
        for t in (2, 3, 9, 99):
            answer, maximum, C, gap = verify(weights, t, direct=index < 7)
            yes += answer
            no += not answer
            if index < 7:
                rows.append(dict(weights=weights, t=t, partition=answer,
                                 max_ratio=str(maximum), bound=str(C),
                                 guaranteed_no_gap=str(gap)))
    out = dict(status="PASS", reductions_checked=len(cases)*4,
               yes_instances=yes, no_instances=no,
               direct_corner_checks=7*4, examples=rows)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
