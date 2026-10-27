#!/usr/bin/env python3
"""Exact product-centroid acquisition, including cross-component quadratic glue."""
from pathlib import Path
from itertools import combinations
import json
import random
import time
from local_algebra_checks import fixture_field, random_invertible, anf_from_cubic
from local_algebra_acquisition import (ChainRing, acquire_product_chain_cubic,
                                      reconstructed_product_value, linear_apply)


def fixture(parameters, seed):
    rng = random.Random(seed)
    rings = [ChainRing(fixture_field(d).modulus, e) for d, e in parameters]
    n = sum(3*ring.m for ring in rings)
    mix = random_invertible(n, rng)
    translation = rng.getrandbits(n)
    coefficients = [rng.getrandbits(ring.m) | 1 for ring in rings]
    quadratic = [((1 << i) | (1 << j)) for i, j in combinations(range(n), 2)
                 if rng.randrange(5) == 0]
    quadratic.extend(1 << i for i in range(n) if rng.randrange(2))
    def evaluator(x):
        result = sum((x & mask) == mask for mask in quadratic) & 1
        x = linear_apply(mix, x) ^ translation
        offset = 0
        for ring, c in zip(rings, coefficients):
            mask = (1 << ring.m)-1
            a, b, z = [(x >> (offset+j*ring.m)) & mask for j in range(3)]
            result ^= ring.functional(ring.mul(c, ring.mul(a, ring.mul(b, z))))
            offset += 3*ring.m
        return result
    return anf_from_cubic(evaluator, n), n, evaluator


def main():
    cases = []
    for case, parameters in enumerate([[(1, 2), (2, 1)], [(1, 2), (1, 3)],
                                      [(1, 2), (2, 2), (1, 3)], [(2, 2), (3, 2)]]):
        start = time.perf_counter()
        poly, n, evaluator = fixture(parameters, 700200+case)
        acquired = acquire_product_chain_cubic(poly, n, verify_cubic_coefficients=True)
        recovered = sorted((part["d"], part["e"]) for part in acquired["components"])
        assert recovered == sorted(parameters)
        rng = random.Random(61104+case)
        points = list(range(1 << n)) if n <= 15 else [rng.getrandbits(n) for _ in range(2048)]
        for y in points:
            assert reconstructed_product_value(acquired, y) == evaluator(linear_apply(acquired["coordinate_columns"], y))
        component_for_bit = [None]*n
        for i, part in enumerate(acquired["components"]):
            component_for_bit[part["bit_offset"]:part["bit_offset"]+part["n"]] = [i]*part["n"]
        cross = 0
        for mask in acquired["quadratic_remainder"]:
            if mask.bit_count() == 2:
                indices = [i for i in range(n) if mask >> i & 1]
                cross += component_for_bit[indices[0]] != component_for_bit[indices[1]]
        assert cross > 0
        cases.append(dict(n=n, components=recovered, raw_anf_terms=len(poly),
                          retained_cross_quadratic_terms=cross, pointwise_checks=len(points),
                          exhaustive=n <= 15, elapsed_seconds=time.perf_counter()-start))
        print(json.dumps(cases[-1]), flush=True)
    result = dict(cases=cases, pointwise_checks=sum(c["pointwise_checks"] for c in cases),
                  warning="Cross-component quadratic terms are preserved; no independent-count factorization asserted.")
    Path(__file__).with_name("product_chain_results.json").write_text(json.dumps(result, indent=2)+"\n")


if __name__ == "__main__":
    main()
