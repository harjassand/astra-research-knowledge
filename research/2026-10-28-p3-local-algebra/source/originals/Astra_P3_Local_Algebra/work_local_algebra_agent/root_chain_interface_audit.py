#!/usr/bin/env python3
"""Independent checks of the root implementation's actual ring interfaces."""
from pathlib import Path
from itertools import product
import sys
import json
import random
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"work_chain_root"))
from acquired_chain_counter import (factor_chain_cubic as root_factor,
    square_adjoint, fit_ordinary_cubic, ring_polynomial, ring_pow)
from chain_cubic_hensel_audit import forms_product, polynomial_value
from local_algebra_checks import fixture_field, random_invertible, anf_from_cubic
from local_algebra_acquisition import ChainRing, acquire_chain, linear_apply


def make_poly(ring, rng):
    forms = [[int(i == j) for j in range(3)] for i in range(3)]
    for _ in range(24):
        i, j = rng.sample(range(3), 2)
        c = rng.getrandbits(ring.m)
        forms[i] = [x ^ ring.mul(c, y) for x, y in zip(forms[i], forms[j])]
    unit = rng.getrandbits(ring.m) | 1
    poly = {alpha: ring.mul(unit, c) for alpha, c in forms_product(ring, forms).items()}
    for alpha in product(range(3), repeat=3):
        if sum(alpha) <= 2:
            c = rng.getrandbits(ring.m)
            if c:
                poly[alpha] = c
    return poly


def main():
    rng = random.Random(202610271144)
    factor_records = []
    for d, e in [(3, 2), (3, 3), (4, 2), (5, 4), (8, 6)]:
        ring = ChainRing(fixture_field(d).modulus, e)
        for repetition in range(6):
            original = make_poly(ring, rng)
            transformed, columns, certificate = root_factor(ring, original)
            assert {alpha for alpha in transformed if sum(alpha) == 3} == {(1, 1, 1)}
            for _ in range(64):
                point = [rng.getrandbits(ring.m) for _ in range(3)]
                old = [0, 0, 0]
                for i in range(3):
                    for j in range(3):
                        old[i] ^= ring.mul(columns[j][i], point[j])
                assert polynomial_value(ring, original, old) == polynomial_value(ring, transformed, point)
            factor_records.append(dict(d=d, e=e, repetition=repetition, point_checks=64,
                                       full_coefficient_identity=certificate["full_coefficient_identity"]))
    square_records = []
    for d, e in [(1, 3), (2, 3), (3, 2), (3, 3), (4, 2)]:
        ring = ChainRing(fixture_field(d).modulus, e)
        checks = 0
        for _ in range(12):
            c = rng.getrandbits(ring.m)
            a = square_adjoint(ring, c)
            for x in range(1 << ring.m):
                assert ring.functional(ring.mul(c, ring.mul(x, x))) == ring.functional(ring.mul(a, x))
                checks += 1
        square_records.append(dict(d=d, e=e, identities=checks))
    fits = []
    for d, e in [(3, 2), (3, 3), (4, 2)]:
        ring = ChainRing(fixture_field(d).modulus, e)
        n = 3*ring.m
        original = make_poly(ring, rng)
        mix = random_invertible(n, rng)
        shift = rng.getrandbits(n)
        def scalar(x):
            y = linear_apply(mix, x) ^ shift
            point = [(y >> (ring.m*i)) & ((1 << ring.m)-1) for i in range(3)]
            return ring.functional(polynomial_value(ring, original, point))
        raw = anf_from_cubic(scalar, n)
        acquired = acquire_chain(raw, n, verify_cubic_coefficients=True)
        fitted, certificate = fit_ordinary_cubic(acquired)
        recovered_ring = ChainRing(acquired["h"], acquired["e"])
        for _ in range(1024):
            y = rng.getrandbits(n)
            point = [(y >> (ring.m*i)) & ((1 << ring.m)-1) for i in range(3)]
            assert recovered_ring.functional(ring_polynomial(recovered_ring, fitted, point)) == scalar(
                linear_apply(acquired["coordinate_columns"], y))
        root_factor(recovered_ring, fitted)
        fits.append(dict(d=d, e=e, n=n, raw_anf_terms=len(raw), pointwise_checks=1024,
                         full_cubic_coefficients=True, fit_rank=certificate["binary_fit_rank"]))
    ring = ChainRing(fixture_field(3).modulus, 2)
    c, x = 1 << ring.d, 1
    correct = ring.functional(ring.mul(c, ring.mul(x, x)))
    false_field_rule = ring.functional(ring.mul(ring_pow(ring, c, 1 << (ring.d-1)), x))
    assert correct == 1 and false_field_rule == 0
    result = dict(root_factor_cases=factor_records, root_square_adjoint=square_records,
                  raw_fits=fits, failed_naive_field_square_rule=dict(
                      field_degree=3, chain_length=2, coefficient=c, input=x,
                      correct=correct, false_field_rule=false_field_rule),
                  scope="Independent exact interface checks; no performance comparison.")
    Path(__file__).with_name("root_chain_interface_results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(dict(factor_cases=len(factor_records), factor_points=64*len(factor_records),
                         square_identities=sum(x["identities"] for x in square_records),
                         raw_fit_cases=len(fits), raw_fit_points=3072)), flush=True)


if __name__ == "__main__":
    main()
