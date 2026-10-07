#!/usr/bin/env python3
"""Exact small Cartan/Grassmann splitter spectra from actual partial trace.

For d=4,5 and k=2,m=1, realize V_{2 omega_2} as the kernel of
 wedge: Sym^2(wedge^2 C^d) -> wedge^4 C^d. This script constructs the exact
orthogonal projector using rational entries, forms the actual partial-trace
Petz map, and checks its action on highest-weight operators against the
candidate Grassmann Berezin-spectrum ratios in c04_s02/revisions.

This is an exact finite diagnostic for two representations, not a proof of
the general spectrum or the Dirichlet comparison.
"""
from __future__ import annotations

import itertools
import json
import time
from math import comb
from pathlib import Path

import sympy as sp


def zero_matrix(a: sp.MatrixBase) -> bool:
    # Every matrix entry in this rational projector audit is already a
    # SymPy integer/rational, so direct exact zero testing avoids costly
    # general-purpose simplification on the 225-by-225 ambient matrices.
    return all(x == 0 for x in a)


def sign_to_sort(xs: tuple[int, ...]) -> int:
    inversions = sum(xs[i] > xs[j] for i in range(len(xs)) for j in range(i + 1, len(xs)))
    return -1 if inversions % 2 else 1


def exterior_generator(pairs: list[tuple[int, int]], a: int, b: int) -> sp.Matrix:
    lookup = {pair: i for i, pair in enumerate(pairs)}
    result = sp.MutableSparseMatrix(len(pairs), len(pairs), {})
    for col, (i, j) in enumerate(pairs):
        for x, y in ((a, j), (i, a)):
            if ((i == b and (x, y) == (a, j)) or (j == b and (x, y) == (i, a))):
                if x == y:
                    continue
                sign = 1 if x < y else -1
                result[lookup[tuple(sorted((x, y)))], col] += sign
    return result


def mu(m: int, d: int, lam: tuple[int, int]) -> sp.Rational:
    value = sp.Rational(1)
    for j, width in enumerate(lam):
        for t in range(width):
            value *= sp.Rational(m + j - t, m + d - j + t)
    return sp.simplify(value)


def weyl_dimension(weight: tuple[int, ...]) -> sp.Integer:
    d = len(weight)
    value = sp.Rational(1)
    for i in range(d):
        for j in range(i + 1, d):
            value *= sp.Rational(weight[i] - weight[j] + j - i, j - i)
    assert value.q == 1
    return sp.Integer(value)


def build(d: int) -> dict:
    q = comb(d, 2)
    pairs = [(i, j) for i in range(d) for j in range(i + 1, d)]
    tensor_dim = q * q
    swap = sp.MutableSparseMatrix(tensor_dim, tensor_dim, {})
    for i in range(q):
        for j in range(q):
            swap[i * q + j, j * q + i] = 1
    symmetric = (sp.SparseMatrix.eye(tensor_dim) + swap) / 2

    four_sets = list(itertools.combinations(range(d), 4))
    pair_id = {pair: i for i, pair in enumerate(pairs)}
    wedge = sp.MutableSparseMatrix(len(four_sets), tensor_dim, {})
    four_id = {subset: i for i, subset in enumerate(four_sets)}
    for a, pair_a in enumerate(pairs):
        for b, pair_b in enumerate(pairs):
            joined = pair_a + pair_b
            if len(set(joined)) != 4:
                continue
            wedge[four_id[tuple(sorted(joined))], a * q + b] = sign_to_sort(joined)
    assert zero_matrix(wedge * symmetric - wedge)
    gram_inverse = (wedge * wedge.T).inv()
    row_projector = wedge.T * gram_inverse * wedge
    projector = symmetric - row_projector
    dim_domain = q * (q + 1) // 2 - comb(d, 4)  # dim V_{2 omega_2}
    assert projector.rank() == dim_domain
    assert zero_matrix(projector * projector - projector)

    generators = {
        (a, b): exterior_generator(pairs, a, b)
        for a in range(d) for b in range(d) if a != b
    }

    for (a, b), ew in generators.items():
        action = sp.kronecker_product(ew, sp.SparseMatrix.eye(q)) + sp.kronecker_product(sp.SparseMatrix.eye(q), ew)
        assert zero_matrix(action * projector - projector * action * projector), (d, a, b, "Cartan space not invariant")

    def induced(a: int, b: int) -> sp.Matrix:
        ew = generators[(a, b)]
        action = sp.kronecker_product(ew, sp.SparseMatrix.eye(q)) + sp.kronecker_product(sp.SparseMatrix.eye(q), ew)
        result = projector * action * projector
        assert zero_matrix(result * projector - result)
        return result

    u = induced(0, d - 1)
    v = induced(1, d - 2)
    a = induced(0, d - 2)
    b = induced(1, d - 1)
    minor = u * v - a * b
    highest = {
        (0, 0): projector,
        (1, 0): u,
        (1, 1): minor,
        (2, 0): u ** 2,
        (2, 1): u * minor,
        (2, 2): minor ** 2,
    }
    ratios = {lam: sp.simplify(mu(1, d, lam) / mu(2, d, lam)) for lam in highest}

    simple_raising = [induced(i, i + 1) for i in range(d - 1)]
    cartan = []
    for i in range(d - 1):
        diagonal_w = sp.diag(*[int(i in pair) - int(i + 1 in pair) for pair in pairs])
        diagonal_action = sp.kronecker_product(sp.SparseMatrix(diagonal_w), sp.SparseMatrix.eye(q)) + sp.kronecker_product(sp.SparseMatrix.eye(q), sp.SparseMatrix(diagonal_w))
        cartan.append(projector * diagonal_action * projector)
    weight_data = {}
    dimension_sum = 0
    for lam, operator in highest.items():
        weight = (lam[0], lam[1]) + (0,) * (d - 4) + (-lam[1], -lam[0])
        assert len(weight) == d
        for raise_op in simple_raising:
            assert zero_matrix(raise_op * operator - operator * raise_op), (d, lam, "not highest")
        for i in range(d - 1):
            h_i = cartan[i]
            assert zero_matrix(h_i * operator - operator * h_i - (weight[i] - weight[i + 1]) * operator), (d, lam, "weight mismatch")
        dimension = weyl_dimension(weight)
        dimension_sum += int(dimension)
        weight_data[str(lam)] = {"highest_weight": list(weight), "Weyl_dimension": int(dimension)}
    dim_s = q

    def partial_trace_second(x: sp.MatrixBase) -> sp.Matrix:
        return sp.MutableSparseMatrix(q, q, {
            (i, k): sum(x[i * q + j, k * q + j] for j in range(q))
            for i in range(q) for k in range(q)
            if any(x[i * q + j, k * q + j] != 0 for j in range(q))
        })

    def phi(x: sp.MatrixBase) -> sp.Matrix:
        t = partial_trace_second(x)
        return sp.Rational(dim_s, dim_domain) * projector * sp.kronecker_product(t, sp.SparseMatrix.eye(q)) * projector

    assert zero_matrix(phi(projector) - projector)
    assert dimension_sum == dim_domain * dim_domain
    observed = {}
    for lam, operator in highest.items():
        assert not zero_matrix(operator), f"zero highest vector for {lam}"
        assert zero_matrix(phi(operator) - ratios[lam] * operator), (d, lam)
        observed[str(lam)] = str(ratios[lam])

    return {
        "d": d,
        "k": 2,
        "m": 1,
        "dim_output": dim_s,
        "dim_domain": dim_domain,
        "wedge4_dimension": len(four_sets),
        "checks": {
            "exact_rational_projector": True,
            "projector_rank_and_idempotence": True,
            "Cartan_space_invariant_under_all_matrix_units": True,
            "reference_preservation_Phi(P)=P": True,
            "all_six_highest_weight_vectors_nonzero": True,
            "highest_weight_annihilation_and_weights": weight_data,
            "Weyl_dimensions_sum_to_full_End_dimension": dimension_sum,
            "actual_Petz_channel_matches_candidate_ratios": observed,
        },
    }


def main() -> None:
    started = time.perf_counter()
    cases = [build(d) for d in (4, 5)]
    result = {
        "status": "PASS_EXACT_RATIONAL",
        "cases": cases,
        "runtime_seconds": round(time.perf_counter() - started, 6),
        "scope": "Exact finite representation checks for d=4,5; not a general Grassmann spectrum proof or EB theorem.",
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
