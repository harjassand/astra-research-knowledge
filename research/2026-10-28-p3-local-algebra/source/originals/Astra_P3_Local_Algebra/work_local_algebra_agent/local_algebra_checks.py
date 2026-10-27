#!/usr/bin/env python3
"""Executed exact validation of raw chain-algebra and free-module acquisition."""
from itertools import combinations
from pathlib import Path
import json
import random
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"work_program_next_agent"))
from field_acquisition_audit import fixture_field
from local_algebra_acquisition import (ChainRing, acquire_raw_chain_cubic,
                                      acquire_chain_algebra, reconstructed_value,
                                      linear_apply, solve, span)


def random_invertible(n, rng):
    columns = [1 << i for i in range(n)]
    for _ in range(12*n):
        i, j = rng.sample(range(n), 2)
        columns[i] ^= columns[j]
    assert len(span(columns)) == n
    return columns


def anf_from_cubic(evaluator, n):
    values = {0: evaluator(0)}
    poly = set([0]) if values[0] else set()
    for degree in range(1, 4):
        for indices in combinations(range(n), degree):
            mask = sum(1 << i for i in indices)
            values[mask] = evaluator(mask)
            coefficient = 0
            sub = mask
            while True:
                coefficient ^= values[sub]
                if not sub:
                    break
                sub = (sub-1) & mask
            if coefficient:
                poly.add(mask)
    return poly


def fixture(d, e, b, seed):
    rng = random.Random(seed)
    ring = ChainRing(fixture_field(d).modulus, e)
    m, n = d*e, b*d*e
    mask = (1 << m)-1
    mix = random_invertible(n, rng)
    translation = rng.getrandbits(n)
    triples = {(0, 1, 2): rng.getrandbits(m) | 1}
    if b == 5:
        triples[0, 3, 4] = rng.getrandbits(m) | 1
    elif b != 3:
        raise ValueError("test uses known radical-free three-form families")
    quadratic = []
    for i, j in combinations(range(n), 2):
        if rng.randrange(9) == 0:
            quadratic.append((1 << i) | (1 << j))
    quadratic.extend(1 << i for i in range(n) if rng.randrange(2))
    if rng.randrange(2):
        quadratic.append(0)

    def evaluator(x):
        original = x
        x = linear_apply(mix, x) ^ translation
        blocks = [(x >> (m*i)) & mask for i in range(b)]
        result = 0
        for (i, j, k), c in triples.items():
            result ^= ring.mul(c, ring.mul(blocks[i], ring.mul(blocks[j], blocks[k])))
        return ring.functional(result) ^ (sum((original & term) == term for term in quadratic) & 1)
    return anf_from_cubic(evaluator, n), n, evaluator


def regular_operators(m, mul):
    return [[mul(1 << i, 1 << j) for j in range(m)] for i in range(m)]


def negative_checks():
    failures = []
    # Local, non-chain algebra F2[u,v]/(u,v)^2.
    def nonchain_mul(a, b):
        return ((a & 1)*(b & 1)) ^ (((a & 1)*((b >> 1) & 3) ^
                                   (b & 1)*((a >> 1) & 3)) << 1)
    examples = [("nonchain_radical", regular_operators(3, nonchain_mul), 3)]
    # Reduced product F2 x F2; both primitive idempotents survive.
    examples.append(("product_requires_split", regular_operators(2, lambda a, b: a & b), 2))
    # Faithful but nonfree module A + F2^2 for A=F2[pi]/pi^2.
    # Dimension divisibility holds, so the Jordan-length test is necessary.
    examples.append(("faithful_nonfree_module", [[1, 2, 4, 8], [2, 0, 0, 0]], 4))
    for label, algebra, n in examples:
        try:
            acquire_chain_algebra(algebra, n)
        except ValueError as exc:
            failures.append(dict(case=label, rejection=str(exc)))
        else:
            raise AssertionError("invalid class accepted: "+label)
    return failures


def main():
    records = []
    total_points = 0
    for index, (d, e, b) in enumerate([(1, 2, 3), (2, 2, 3), (1, 4, 3),
                                      (2, 3, 3), (3, 2, 3), (2, 4, 3),
                                      (3, 3, 3), (1, 3, 5), (2, 2, 5)]):
        start = time.perf_counter()
        poly, n, evaluator = fixture(d, e, b, 197700+index)
        acquired = acquire_raw_chain_cubic(poly, n, verify_cubic_coefficients=True)
        assert (acquired["d"], acquired["e"], acquired["module_dimension"]) == (d, e, b)
        rng = random.Random(554000+index)
        points = list(range(1 << n)) if n <= 15 else [rng.getrandbits(n) for _ in range(1024)]
        for y in points:
            assert reconstructed_value(acquired, y) == evaluator(linear_apply(acquired["coordinate_columns"], y))
        total_points += len(points)
        records.append(dict(n=n, field_degree=d, chain_length=e, module_dimension=b,
                            raw_anf_terms=len(poly), field_modulus=acquired["h"],
                            algebra_dimension=acquired["algebra_dimension"],
                            quadratic_remainder_terms=len(acquired["quadratic_remainder"]),
                            pointwise_checks=len(points), exhaustive=n <= 15,
                            elapsed_seconds=time.perf_counter()-start))
        print(json.dumps(records[-1]), flush=True)
    result = dict(accepted_raw_cases=records, pointwise_checks=total_points,
                  negative_cases=negative_checks(),
                  execution_scope="Raw representation acquisition; no asymptotic counting backend.")
    Path(__file__).with_name("local_algebra_results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(dict(total_cases=len(records), pointwise_checks=total_points)), flush=True)


if __name__ == "__main__":
    main()
