#!/usr/bin/env python3
"""Exact small CAR fixtures for bounded-body-order sector reconstruction.

Does not import producer/root code or change the frozen review receipt.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json
import math
import random

OUT = Path(__file__).resolve().parent


def subsets(n, q):
    return list(combinations(range(n), q))


def states(n, number):
    return [sum(1 << i for i in row) for row in subsets(n, number)]


def zero(d):
    return [[Q(0) for _ in range(d)] for _ in range(d)]


def identity(d, value=Q(1)):
    a = zero(d)
    for i in range(d):
        a[i][i] = value
    return a


def add(a, b, sign=1):
    return [[x+sign*y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def apply_monomial(state, creation, annihilation):
    sign = 1
    for j in annihilation:
        if not ((state >> j) & 1):
            return None
        sign *= (-1)**((state & ((1 << j)-1)).bit_count())
        state ^= 1 << j
    for i in reversed(creation):
        if (state >> i) & 1:
            return None
        sign *= (-1)**((state & ((1 << i)-1)).bit_count())
        state ^= 1 << i
    return state, sign


def lift(n, order, matrix, number):
    basis = states(n, number)
    inverse = {b: j for j, b in enumerate(basis)}
    modes = subsets(n, order)
    result = zero(len(basis))
    for col, b in enumerate(basis):
        for j, annihilation in enumerate(modes):
            if any(not ((b >> x) & 1) for x in annihilation):
                continue
            for i, creation in enumerate(modes):
                if not matrix[i][j]:
                    continue
                acted = apply_monomial(b, creation, annihilation)
                if acted is not None:
                    target, sign = acted
                    result[inverse[target]][col] += sign*matrix[i][j]
    return result


def reconstruction_fixture(n, p, seed):
    rng = random.Random(seed)
    coefficients = []
    for q in range(p+1):
        d = math.comb(n, q)
        u = zero(d)
        for i in range(d):
            for j in range(i+1):
                u[i][j] = u[j][i] = Q(rng.randrange(-5, 6), 7)
        coefficients.append(u)
    blocks = []
    for number in range(n+1):
        block = zero(math.comb(n, number))
        for q in range(min(number, p)+1):
            block = add(block, lift(n, q, coefficients[q], number))
        blocks.append(block)
    recovered = []
    for q in range(p+1):
        residual = blocks[q]
        for lower in range(q):
            residual = add(residual, lift(n, lower, recovered[lower], q), -1)
        assert residual == coefficients[q]
        recovered.append(residual)
    for number in range(n+1):
        rebuilt = zero(math.comb(n, number))
        for q in range(min(number, p)+1):
            rebuilt = add(rebuilt, lift(n, q, recovered[q], number))
        assert rebuilt == blocks[number]
    # Sharp lift norm: a q-body identity lifts to C(N,q) times identity.
    sharp = []
    for q in range(p+1):
        for number in range(q, n+1):
            assert lift(n, q, identity(math.comb(n, q)), number) == \
                   identity(math.comb(n, number), Q(math.comb(number, q)))
            sharp.append([q, number, math.comb(number, q)])
    # Exact noisy-sector recursion with identity input errors.
    deltas = [Q(1, 1000), Q(1, 700), Q(1, 1300), Q(1, 1700)][:p+1]
    noisy, radii, actual = [], [], []
    for q in range(p+1):
        residual = add(blocks[q], identity(math.comb(n, q), deltas[q]))
        for lower in range(q):
            residual = add(residual, lift(n, lower, noisy[lower], q), -1)
        noisy.append(residual)
        error = add(residual, coefficients[q], -1)
        scalar = error[0][0]
        assert error == identity(len(error), scalar)
        radius = deltas[q]+sum(Q(math.comb(q, lower))*radii[lower]
                              for lower in range(q))
        assert abs(scalar) <= radius
        radii.append(radius); actual.append(abs(scalar))
    lifted = []
    for number in range(n+1):
        err = zero(math.comb(n, number))
        for q in range(min(number, p)+1):
            err = add(err, lift(n, q, add(noisy[q], coefficients[q], -1), number))
        scalar = err[0][0]
        assert err == identity(len(err), scalar)
        radius = sum(Q(math.comb(number, q))*radii[q]
                     for q in range(min(number, p)+1))
        assert abs(scalar) <= radius
        lifted.append({"N": number, "actual_error": str(abs(scalar)),
                       "conservative_radius": str(radius)})
    return {"bath_modes": n, "body_order": p,
            "sector_dimensions": [math.comb(n, q) for q in range(p+1)],
            "all_reconstructed_coefficients_exact": True,
            "all_fock_sector_blocks_exact": True,
            "sharp_binomial_identity_fixtures": sharp,
            "input_sector_error_radii": list(map(str, deltas)),
            "recursive_coefficient_radii": list(map(str, radii)),
            "actual_coefficient_errors": list(map(str, actual)),
            "all_sector_error_bounds": lifted}


def main():
    result = {"status": "exact_finite_fixtures_not_external_validation",
              "producer_imports": False,
              "fixtures": [reconstruction_fixture(4, 2, 79013),
                           reconstruction_fixture(5, 3, 79014)]}
    (OUT/"addendum_results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"all_checks_passed": True, "exact_reconstruction_fixtures": 2,
                      "sharp_identity_lifts": sum(len(x["sharp_binomial_identity_fixtures"])
                                                 for x in result["fixtures"])}))


if __name__ == "__main__":
    main()
