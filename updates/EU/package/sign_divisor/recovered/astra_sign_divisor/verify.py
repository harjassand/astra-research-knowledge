#!/usr/bin/env python3
"""Finite diagnostics for ASTRA sign-divisor research, 2026-10-13.

These checks do not establish the general theorems or historical novelty.
Exact finite checks use integer bit masks, fractions and symbolic polynomials.
Floating-point spectral checks are explicitly reported as diagnostics.
Dependencies: Python 3.10+, numpy, sympy.
Run: python verify.py --output checks.json
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Iterable

import numpy as np
import sympy as sp


def rank_gf2(vectors: Iterable[int]) -> int:
    pivots: dict[int, int] = {}
    for value in vectors:
        if value < 0:
            raise ValueError("Binary vectors must be nonnegative masks")
        x = value
        while x:
            bit = x.bit_length() - 1
            if bit in pivots:
                x ^= pivots[bit]
            else:
                pivots[bit] = x
                break
    return len(pivots)


def span(vectors: Iterable[int]) -> frozenset[int]:
    values = {0}
    for v in vectors:
        values |= {x ^ v for x in tuple(values)}
    return frozenset(values)


def all_subspaces(n: int) -> list[frozenset[int]]:
    known = {frozenset({0})}
    frontier = list(known)
    while frontier:
        space = frontier.pop()
        for v in range(1, 1 << n):
            if v in space:
                continue
            enlarged = frozenset(set(space) | {x ^ v for x in space})
            if enlarged not in known:
                known.add(enlarged)
                frontier.append(enlarged)
    return sorted(known, key=lambda c: (len(c), sorted(c)))


def bases(code: frozenset[int]) -> list[tuple[int, ...]]:
    k = (len(code)).bit_length() - 1
    return [b for b in itertools.combinations(sorted(code - {0}), k)
            if rank_gf2(b) == k]


def loads(vectors: Iterable[int], n: int) -> tuple[int, ...]:
    vs = tuple(vectors)
    return tuple(sum((v >> i) & 1 for v in vs) for i in range(n))


def pareto_minimal(vectors: Iterable[tuple[int, ...]]) -> set[tuple[int, ...]]:
    unique = set(vectors)
    return {a for a in unique if not any(
        b != a and all(x <= y for x, y in zip(b, a)) for b in unique)}


def exact_small_code_checks() -> dict:
    code_count = family_count = 0
    for n in range(1, 5):
        for code in all_subspaces(n):
            code_count += 1
            bs = bases(code)
            k = int(math.log2(len(code)))
            basis_loads = [loads(b, n) for b in bs]
            if k:
                distance = min(v.bit_count() for v in code if v)
                assert min(map(sum, basis_loads)) >= distance * k
            else:
                distance = 0
            # Exhaust all possible sets of active factor masks for n <= 4.
            nonzero = sorted(code - {0})
            family_pareto = []
            for r in range(len(nonzero) + 1):
                for family in itertools.combinations(nonzero, r):
                    if rank_gf2(family) != k:
                        continue
                    family_count += 1
                    budget = loads(family, n)
                    # A basis can be extracted coordinatewise below the budget.
                    assert any(all(a <= b for a, b in zip(bl, budget))
                               for bl in basis_loads)
                    family_pareto.append(budget)
            assert pareto_minimal(family_pareto) == pareto_minimal(basis_loads)
    return {"status": "PASS", "binary_codes_checked": code_count,
            "spanning_factor_mask_families_checked": family_count,
            "scope": "All subspaces of F_2^n for 1 <= n <= 4; finite algebraic consequence only"}


def named_codes() -> dict:
    examples = {
        "even_parity_3": (3, [0b011, 0b101]),
        "simplex_7_3_4": (7, [0b1010101, 0b1100110, 0b1111000]),
        "hamming_7_4_3": (7, [0b0001111, 0b0110011, 0b1010101, 0b1111111]),
        "extended_hamming_8_4_4": (8, [0b00001111, 0b00110011, 0b01010101, 0b11111111]),
    }
    output = {}
    for name, (n, generator) in examples.items():
        code = span(generator)
        bs = bases(code)
        degree_vectors = [loads(b, n) for b in bs]
        best_total = min(map(sum, degree_vectors))
        best_max = min(map(max, degree_vectors))
        min_distance = min(x.bit_count() for x in code if x)
        assert len(code) == 1 << len(generator)
        # Monomial output signs are exactly the ordinary binary encoder.
        counts: dict[int, int] = {}
        for bits in itertools.product((0, 1), repeat=len(generator)):
            word = 0
            for u, row in zip(bits, generator):
                if u:
                    word ^= row
            counts[word] = counts.get(word, 0) + 1
        assert set(counts) == set(code) and set(counts.values()) == {1}
        output[name] = {"n": n, "k": len(generator), "minimum_distance": min_distance,
                        "minimum_total_degree": best_total,
                        "minimum_maximum_coordinate_degree": best_max,
                        "bases_enumerated": len(bs), "exact_uniform_encoding": "PASS"}
    return output


def symbolic_examples() -> dict:
    x, y = sp.symbols("x y")
    polynomials = [x * (x + y) * (1 + x*x + y*y),
                   y * (x + y), x*y]
    masks = [0b101, 0b110, 0b011]  # x, y, x+y; bit i is output i.
    # The first mask is x: outputs 0 and 2 = 101;
    # y: outputs 1 and 2 = 110; x+y: outputs 0 and 1 = 011.
    observed = set()
    for a, b in itertools.product(range(-5, 6), repeat=2):
        values = [p.subs({x: a, y: b}) for p in polynomials]
        if any(v == 0 for v in values):
            continue
        word = sum((int(bool(v < 0)) << i) for i, v in enumerate(values))
        observed.add(word)
    hull = span([w ^ next(iter(observed)) for w in observed])
    assert hull == span(masks)
    assert len(hull) == 4 and len(observed) == 3
    assert all(w.bit_count() % 2 == 0 for w in observed)
    # The parity product is globally nonnegative, not merely a formal square.
    parity_product = sp.factor(sp.prod(polynomials))
    expected = x*x*y*y*(x+y)**2*(1+x*x+y*y)
    assert sp.expand(parity_product - expected) == 0
    # A sign-definite irreducible factor must not create an independent sign bit.
    assert all((1 + a*a + b*b) > 0 for a, b in itertools.product(range(-5, 6), repeat=2))
    return {"status": "PASS", "polynomials": [str(p) for p in polynomials],
            "factor_masks": masks, "factor_mask_rank": rank_gf2(masks),
            "observed_support": sorted(observed), "affine_hull_size": len(hull),
            "warning": "Affine hull extraction does not recover full support or atom probabilities",
            "parity_product": str(parity_product)}


def balanced_slice_check() -> dict:
    n = 4
    vectors = [s for s in itertools.product((-1, 1), repeat=n) if sum(s) == 0]
    cov = [[Fraction(sum(s[i] * s[j] for s in vectors), len(vectors))
            for j in range(n)] for i in range(n)]
    assert all(cov[i][j] == Fraction(-1, 3) for i in range(n) for j in range(n) if i != j)
    K = sp.Matrix(n, n, lambda i, j: 1 if i == j else sp.Rational(-1, 2))
    eigen = K.eigenvals()
    assert eigen == {sp.Rational(-1, 2): 1, sp.Rational(3, 2): 3}
    # The pair moments alone have a three-component antithetic Gaussian mixture.
    matchings = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
    pair_counts = np.zeros((n, n), dtype=int)
    for matching in matchings:
        for a, b in matching:
            pair_counts[a, b] += 1
            pair_counts[b, a] += 1
    assert np.all(pair_counts + np.eye(n, dtype=int) == 1)
    return {"status": "PASS", "balanced_slice_size": len(vectors),
            "off_diagonal_sign_correlation": "-1/3", "inverse_sine_minimum_eigenvalue": "-1/2",
            "pair_marginals_antithetic_components": len(matchings),
            "scope": "Full-law mixture lower bounds must not be asserted for pair marginals alone"}


def hadamard(n: int) -> np.ndarray:
    if n < 1 or n & (n-1):
        raise ValueError("n must be a positive power of two")
    H = np.ones((1, 1), dtype=float)
    while len(H) < n:
        H = np.block([[H, H], [H, -H]])
    return H


def quantum_gluing_diagnostics() -> dict:
    r0 = 2 * math.asinh(1) / (3 * math.pi)
    r = 0.18
    rows = []
    for n in (4, 8, 16, 32):
        H = hadamard(n)
        S = H - np.diag(np.diag(H))
        t = r / (math.sqrt(n) + 1)
        T = np.kron(t*S, np.eye(3))
        K = np.eye(3*n) + np.sin((3*math.pi/2)*T)
        spectrum = np.linalg.eigvalsh(K)
        recovered = (2/(3*math.pi))*np.arcsin(np.clip(K, -1, 1))
        error = float(np.max(np.abs((recovered-T)[~np.eye(3*n, dtype=bool)])))
        assert float(np.linalg.norm(T, 2)) < r0
        assert spectrum[0] > 0 and error < 1e-14
        rows.append({"n_qubits": n, "correlation_operator_norm": float(np.linalg.norm(T, 2)),
                     "latent_minimum_eigenvalue": float(spectrum[0]),
                     "pair_correlation_recovery_error": error,
                     "absolute_edge_sum_per_axis": float((n-1)*t)})
    return {"status": "PASS_FLOATING_DIAGNOSTIC", "sufficient_radius": r0,
            "examples": rows, "warning": "Floating-point calculations are not PSD certificates"}


def robust_constants() -> dict:
    rows = []
    for delta in (0.1, 0.25, 0.5):
        for D in (1, 2, 4):
            for eta in (0.25, 0.5, 0.75):
                theta = math.pi * delta * eta*eta / (2*D)
                alpha_minus_one = math.tan(theta/2)**2
                log2_K = math.log2(2/eta) / alpha_minus_one
                upper = 16*D*D*math.log2(2/eta)/(math.pi**2*delta*delta*eta**4)
                assert log2_K <= upper * (1 + 1e-12)
                sigma = D*theta/(math.pi*delta)
                assert abs(sigma-eta*eta/2) < 1e-14
                # q^2 <= (eta/2)q + eta^2/2 has positive root eta.
                root = (eta/2 + math.sqrt(eta*eta/4 + 2*eta*eta))/2
                assert abs(root-eta) < 1e-14
                rows.append({"delta": delta, "degree": D, "eta": eta, "log2_K": log2_K})
    return {"status": "PASS", "parameter_checks": len(rows), "values": rows,
            "warning": "Bounds can be quantitatively vacuous at small n; no Monte Carlo theorem validation"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("checks.json"))
    args = parser.parse_args()
    results = {"date": "2026-10-13", "general_proof_status": "Human-readable derivations; no independent validation",
               "novelty_status": "Not established",
               "small_code_checks": exact_small_code_checks(),
               "named_codes": named_codes(), "symbolic_examples": symbolic_examples(),
               "balanced_slice": balanced_slice_check(),
               "quantum_gluing": quantum_gluing_diagnostics(),
               "robust_bound_constants": robust_constants()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "small_codes": results["small_code_checks"],
                      "named_codes": results["named_codes"],
                      "overall": "All diagnostic assertions passed"}, indent=2))


if __name__ == "__main__":
    main()
