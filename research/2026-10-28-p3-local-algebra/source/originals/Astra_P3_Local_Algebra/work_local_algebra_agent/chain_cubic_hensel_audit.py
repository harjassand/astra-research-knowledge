#!/usr/bin/env python3
"""Independent characteristic-two chain-ring cubic uniqueness/factor audit.

The actual factor acquisition uses residue-field factorization and one
seven-dimensional correction at each nilpotent layer. It does not enumerate
field or ring elements. Enumeration appears only in finite identity checks.
"""
from itertools import product, combinations
from pathlib import Path
import json
import random
from local_algebra_checks import fixture_field
from local_algebra_acquisition import ChainRing, linear_apply, kernel_columns
from field_descent import factor_cubic
from field_kloosterman import gf_pow


def poly_multiply(ring, a, b):
    out = {}
    for alpha, c in a.items():
        for beta, d in b.items():
            gamma = tuple(x+y for x, y in zip(alpha, beta))
            out[gamma] = out.get(gamma, 0) ^ ring.mul(c, d)
    return {e: c for e, c in out.items() if c}


def forms_product(ring, forms):
    poly = {(0, 0, 0): 1}
    for form in forms:
        linear = {tuple(int(i == j) for i in range(3)): c
                  for j, c in enumerate(form) if c}
        poly = poly_multiply(ring, poly, linear)
    return poly


def substitute(ring, poly, columns):
    linears = [{tuple(int(i == j) for i in range(3)): columns[j][k]
                for j in range(3) if columns[j][k]} for k in range(3)]
    out = {}
    for exponent, coefficient in poly.items():
        term = {(0, 0, 0): coefficient}
        for i, power in enumerate(exponent):
            for _ in range(power):
                term = poly_multiply(ring, term, linears[i])
        for alpha, c in term.items():
            out[alpha] = out.get(alpha, 0) ^ c
    return {alpha: c for alpha, c in out.items() if c}


def factor_chain_cubic(ring, polynomial):
    if ring.d < 3:
        raise ValueError("seven-probe residue factorization requires d>=3")
    if not polynomial or any(sum(alpha) != 3 for alpha in polynomial):
        raise ValueError("requires an ordinary homogeneous cubic")
    residue = {alpha: c & ring.mask for alpha, c in polynomial.items() if c & ring.mask}
    balanced, columns, factor_data = factor_cubic(residue, ring.h)
    lam = balanced[(1, 1, 1)]
    inv = gf_pow(lam, (1 << ring.d)-2, ring.h)
    transformed = substitute(ring, polynomial, columns)
    target = {alpha: ring.mul(c, inv) for alpha, c in transformed.items()}
    forms = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    labels = {(1, 1, 1): (0, 0), (0, 2, 1): (0, 1), (0, 1, 2): (0, 2),
              (2, 0, 1): (1, 0), (1, 0, 2): (1, 2),
              (2, 1, 0): (2, 0), (1, 2, 0): (2, 1)}
    for layer in range(1, ring.e):
        current = forms_product(ring, forms)
        error = {alpha: target.get(alpha, 0) ^ current.get(alpha, 0)
                 for alpha in set(target) | set(current)}
        lowmask = (1 << (ring.d*layer))-1
        if any(c & lowmask for c in error.values()):
            raise AssertionError("previous factor layers changed")
        for alpha, c in error.items():
            coefficient = (c >> (ring.d*layer)) & ring.mask
            if not coefficient:
                continue
            if alpha not in labels:
                raise ValueError("nonliftable pure-cube error at layer "+str(layer))
            i, j = labels[alpha]
            forms[i][j] ^= coefficient << (ring.d*layer)
    if forms_product(ring, forms) != target:
        raise AssertionError("Hensel factorization did not reconstruct the target")
    normals = factor_data["normals"]
    original_forms = []
    for form in forms:
        row = []
        for j in range(3):
            c = 0
            for k in range(3):
                c ^= ring.mul(form[k], normals[k][j])
            row.append(c)
        original_forms.append(row)
    acquired = {alpha: ring.mul(lam, c) for alpha, c in forms_product(ring, original_forms).items()}
    if acquired != polynomial:
        raise AssertionError("returned factorization fails in original coordinates")
    return dict(multiplier=lam, forms=original_forms, nilpotent_layers=ring.e-1,
                correction_dimension=7)


def polynomial_value(ring, poly, point):
    value = 0
    for alpha, c in poly.items():
        term = c
        for x, power in zip(point, alpha):
            for _ in range(power):
                term = ring.mul(term, x)
        value ^= term
    return value


def uniqueness_check(d, e):
    ring = ChainRing(fixture_field(d).modulus, e)
    n = 3*ring.m
    inputs = [0]
    inputs.extend(sum(1 << i for i in indices)
                  for weight in range(1, 4) for indices in combinations(range(n), weight))
    exponents = sorted(alpha for alpha in product(range(4), repeat=3) if sum(alpha) <= 3)
    gram = ring.gram()
    columns = []
    for alpha in exponents:
        block = [0]*ring.m
        for row, x in enumerate(inputs):
            values = [(x >> (ring.m*j)) & ((1 << ring.m)-1) for j in range(3)]
            value = polynomial_value(ring, {alpha: 1}, values)
            traces = linear_apply(gram, value)
            for j in range(ring.m):
                if traces >> j & 1:
                    block[j] |= 1 << row
        columns.extend(block)
    relations = kernel_columns(columns)
    cubic_mask = sum(1 << (i*ring.m+j) for i, alpha in enumerate(exponents)
                     if sum(alpha) == 3 for j in range(ring.m))
    cubic_aliases = sum(bool(relation & cubic_mask) for relation in relations)
    assert bool(cubic_aliases) == (d < 3)
    return dict(d=d, e=e, n=n, evaluation_rows=len(inputs), coefficient_columns=len(columns),
                relation_dimension=len(relations), cubic_alias_relations=cubic_aliases)


def main():
    rng = random.Random(202610270909)
    cases = []
    points = 0
    for d, e in [(3, 2), (3, 3), (4, 2), (4, 4), (5, 3), (8, 4)]:
        ring = ChainRing(fixture_field(d).modulus, e)
        for repeat in range(12):
            forms = [[int(i == j) for j in range(3)] for i in range(3)]
            for _ in range(24):
                i, j = rng.sample(range(3), 2)
                c = rng.getrandbits(ring.m)
                forms[i] = [x ^ ring.mul(c, y) for x, y in zip(forms[i], forms[j])]
            lam = rng.getrandbits(ring.m) | 1
            cubic = {alpha: ring.mul(lam, c) for alpha, c in forms_product(ring, forms).items()}
            acquired = factor_chain_cubic(ring, cubic)
            reconstructed = {alpha: ring.mul(acquired["multiplier"], c)
                             for alpha, c in forms_product(ring, acquired["forms"]).items()}
            assert reconstructed == cubic
            for _ in range(24):
                point = [rng.getrandbits(ring.m) for _ in range(3)]
                assert polynomial_value(ring, reconstructed, point) == polynomial_value(ring, cubic, point)
                points += 1
            cases.append(dict(d=d, e=e, repetition=repeat, exact_coefficient_identity=True))
    negatives = []
    for d, e, layer in [(3, 2, 1), (3, 3, 1), (3, 3, 2), (4, 4, 3)]:
        ring = ChainRing(fixture_field(d).modulus, e)
        bad = {(1, 1, 1): 1, (3, 0, 0): 1 << (d*layer)}
        try:
            factor_chain_cubic(ring, bad)
        except ValueError as exc:
            negatives.append(dict(d=d, e=e, layer=layer, rejection=str(exc)))
        else:
            raise AssertionError("a nonliftable split residue was accepted")
    uniqueness = [uniqueness_check(d, e) for d, e in [(1, 2), (2, 2), (3, 2), (3, 3), (4, 2)]]
    result = dict(factor_cases=cases, pointwise_checks=points, negative_cases=negatives,
                  homogeneous_uniqueness=uniqueness,
                  scope="Exact acquisition and identities only; no point-counting claim.")
    Path(__file__).with_name("chain_cubic_hensel_results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(dict(factor_cases=len(cases), pointwise_checks=points,
                         negative_cases=len(negatives), uniqueness=uniqueness)), flush=True)


if __name__ == "__main__":
    main()
