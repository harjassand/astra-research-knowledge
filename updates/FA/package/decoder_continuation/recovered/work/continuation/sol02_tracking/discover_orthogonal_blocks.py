#!/usr/bin/env python3
"""Exact discovery and well-scaled rational coordinates for orthogonal blocks."""
from __future__ import annotations
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def exact_components(vectors):
    parent = list(range(len(vectors)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i, v in enumerate(vectors):
        for j in range(i):
            if dot(v, vectors[j]) != 0:
                parent[find(i)] = find(j)
    groups = {}
    for i, v in enumerate(vectors):
        if dot(v, v):
            groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def rational_orthogonal_basis(vectors, indices):
    basis = []
    for index in indices:
        u = list(vectors[index])
        for b in basis:
            coefficient = dot(u, b) / dot(b, b)
            u = [x-coefficient*y for x, y in zip(u, b)]
        norm2 = dot(u, u)
        if norm2 == 0:
            continue
        # A power-of-two scaling gives norm^2 in [1,4) exactly, without sqrt.
        scale = F(1)
        while norm2 * scale * scale < 1:
            scale *= 2
        while norm2 * scale * scale >= 4:
            scale /= 2
        basis.append(tuple(scale*x for x in u))
    assert all(1 <= dot(b, b) < 4 for b in basis)
    assert all(dot(basis[i], basis[j]) == 0 for i in range(len(basis)) for j in range(i))
    return basis


def nearest_integer(x):
    y = x + F(1, 2)
    return y.numerator // y.denominator


def main():
    # Rational orthogonal Hadamard rotation: every nonzero pulse is dense in
    # the original coordinates, but there are two orthogonal rank-two blocks.
    hadamard = [tuple(F(value, 2) for value in row) for row in
                [(1,1,1,1), (1,-1,1,-1), (1,1,-1,-1), (1,-1,-1,1)]]
    columns = list(zip(*hadamard))
    local = [(F(1),F(0)), (F(3,5),F(4,5)), (F(0),F(1)), (F(4,5),F(-3,5))]
    vectors = []
    for p in range(len(local)):
        for block in range(2):
            w = local[p]
            vectors.append(tuple(w[0]*columns[2*block][i]+w[1]*columns[2*block+1][i] for i in range(4)))
    assert all(dot(v, v) == 1 for v in vectors)
    assert all(all(value != 0 for value in v) for v in vectors)
    groups = exact_components(vectors)
    bases = [rational_orthogonal_basis(vectors, group) for group in groups]
    assert sorted(map(len, bases)) == [2, 2]
    assert all(dot(vectors[i], vectors[j]) == 0 for g, group in enumerate(groups)
               for other in groups[g+1:] for i in group for j in other)
    components = []
    for group, basis in zip(groups, bases):
        n, rank = len(group), len(basis)
        mden = 16*n*rank
        rounded = []
        for index in group:
            v = vectors[index]
            coordinates = [dot(v, b)/dot(b, b) for b in basis]
            reconstructed = tuple(sum((c*b[i] for c, b in zip(coordinates, basis)), F(0)) for i in range(4))
            assert reconstructed == v
            z = [nearest_integer(mden*c) for c in coordinates]
            approx = tuple(sum((F(c, mden+rank)*b[i] for c, b in zip(z, basis)), F(0)) for i in range(4))
            error = tuple(a-b for a, b in zip(approx, v))
            assert dot(approx, approx) <= 1
            assert dot(error, error) <= F(2*rank, mden)**2
            assert dot(error, error) <= F(1, 8*n)**2
            rounded.append({"input_index": index, "coordinates": list(map(str, coordinates)),
                            "integer_numerators": z, "coefficient_denominator": mden+rank,
                            "physical_approx_norm_squared": str(dot(approx, approx)),
                            "physical_error_norm_squared": str(dot(error, error))})
        components.append({"input_indices": group, "rank": rank,
                           "basis": [list(map(str, b)) for b in basis],
                           "basis_norm_squared": [str(dot(b,b)) for b in basis],
                           "rounding_M": mden, "rounding": rounded})
    receipt = {
        "status": "PASS",
        "evidence_status": "exact Fraction graph, orthogonalization, coordinate reconstruction and rounding checks",
        "dimension": 4,
        "supplied_directions": [list(map(str,v)) for v in vectors],
        "all_original_directions_dense": True,
        "coordinate_support_graph_component_size": 4,
        "orthogonality_graph_components": components,
        "all_cross_component_dot_products_exact_zero": True,
        "all_component_ranks_at_most": 2,
        "source_existence_theorem_used_by_this_test": False,
        "general_controller_synthesis_used_by_this_test": False,
        "scope": "algorithmic discovery/rounding witness; does not close arbitrary high-rank components",
    }
    (HERE / "orthogonal_block_discovery_receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
