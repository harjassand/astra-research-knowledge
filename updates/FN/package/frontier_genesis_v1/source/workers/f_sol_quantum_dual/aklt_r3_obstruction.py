#!/usr/bin/env python3
"""Rational six-site AKLT obstruction to a three-site local dual ansatz.

The matrix columns equal the span obtained by applying the spin-2 projector
on a pair inside each contiguous three-site block, tensored with the exact
outside Schmidt support of the periodic AKLT ground state. Everything is
restricted to total S_z=0, which contains the source S_z(0)|psi>.
"""

from itertools import product
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix


N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
R = 3
WORDS = list(product(range(3), repeat=N))
MAG = (1, 0, -1)
ZERO = [w for w in WORDS if sum(MAG[s] for s in w) == 0]
ZERO_INDEX = {w: i for i, w in enumerate(ZERO)}
INSIDE = list(product(range(3), repeat=R))
OUTSIDE = list(product(range(3), repeat=N - R))
OUTSIDE_INDEX = {w: i for i, w in enumerate(OUTSIDE)}

# An integer-gauge AKLT MPS; periodic traces agree with the standard
# A+=(sqrt(2/3)) sigma+, A0=-(1/sqrt(3)) sigmaz,
# A-=-(sqrt(2/3)) sigma- up to one common factor per site.
A = (
    sp.Matrix([[0, 2], [0, 0]]),
    sp.Matrix([[-1, 0], [0, 1]]),
    sp.Matrix([[0, 0], [-1, 0]]),
)


def amp(word):
    p = sp.eye(2)
    for s in word:
        p *= A[s]
    return sp.trace(p)


PSI = {w: amp(w) for w in ZERO}
B = sp.Matrix([MAG[w[0]] * PSI[w] for w in ZERO])
assert B != sp.zeros(len(ZERO), 1)
assert sum(PSI[w] * B[ZERO_INDEX[w]] for w in ZERO) == 0

# Projector onto pair total spin 2, all rational in the spin-z basis.
Q = {
    (0, 0): {(0, 0): sp.Integer(1)},
    (0, 1): {(0, 1): sp.Rational(1, 2), (1, 0): sp.Rational(1, 2)},
    (1, 0): {(0, 1): sp.Rational(1, 2), (1, 0): sp.Rational(1, 2)},
    (0, 2): {(0, 2): sp.Rational(1, 6), (1, 1): sp.Rational(1, 3), (2, 0): sp.Rational(1, 6)},
    (1, 1): {(0, 2): sp.Rational(1, 3), (1, 1): sp.Rational(2, 3), (2, 0): sp.Rational(1, 3)},
    (2, 0): {(0, 2): sp.Rational(1, 6), (1, 1): sp.Rational(1, 3), (2, 0): sp.Rational(1, 6)},
    (1, 2): {(1, 2): sp.Rational(1, 2), (2, 1): sp.Rational(1, 2)},
    (2, 1): {(1, 2): sp.Rational(1, 2), (2, 1): sp.Rational(1, 2)},
    (2, 2): {(2, 2): sp.Integer(1)},
}


def joined(block, outside, sites, other):
    word = [0] * N
    for j, s in zip(sites, block):
        word[j] = s
    for j, s in zip(other, outside):
        word[j] = s
    return tuple(word)


def columns_for_bond(j, start_offset=0):
    assert start_offset in (0, -1)
    sites = [(j + start_offset + t) % N for t in range(R)]
    other = [t for t in range(N) if t not in sites]
    pair_pos = -start_offset
    # Rows of the Schmidt reshaping span exactly the outside Schmidt support.
    rows = []
    for inside in INSIDE:
        rows.append(sp.Matrix([[PSI.get(joined(inside, outside, sites, other), 0)
                                for outside in OUTSIDE]]))
    env_basis = sp.Matrix.vstack(*rows).rowspace()
    assert len(env_basis) == 4
    cols = []
    for v in env_basis:
        nonzero = [OUTSIDE[t] for t, value in enumerate(v) if value]
        assert nonzero
        outside_mag = sum(MAG[s] for s in nonzero[0])
        assert all(sum(MAG[s] for s in w) == outside_mag for w in nonzero)
        for inside in INSIDE:
            if sum(MAG[s] for s in inside) != -outside_mag:
                continue
            col = sp.zeros(len(ZERO), 1)
            for out_pair, coeff in Q[inside[pair_pos:pair_pos + 2]].items():
                block_list = list(inside)
                block_list[pair_pos:pair_pos + 2] = out_pair
                block = tuple(block_list)
                for outside in nonzero:
                    word = joined(block, outside, sites, other)
                    col[ZERO_INDEX[word]] += coeff * v[OUTSIDE_INDEX[outside]]
            if col != sp.zeros(len(ZERO), 1):
                cols.append(col)
    return cols


def main():
    import json
    from pathlib import Path

    if N == 6:
        cols = [col for j in range(N) for col in columns_for_bond(j)]
        C = sp.Matrix.hstack(*cols)
        # Exact rational left-null witness for the narrow right-only ansatz.
        rank = DomainMatrix.from_Matrix(C).to_field().rank()
        augmented_rank = DomainMatrix.from_Matrix(C.row_join(B)).to_field().rank()
        assert augmented_rank == rank + 1
        left_null = DomainMatrix.from_Matrix(C.T).to_field().nullspace().to_Matrix()
        witness = next((left_null.row(i).T for i in range(left_null.rows)
                        if left_null.row(i).dot(B) != 0))
        den = sp.ilcm(*[value.q for value in witness])
        witness *= den
        gcd = sp.igcd(*[abs(int(value)) for value in witness if value])
        witness /= gcd
        assert C.T * witness == sp.zeros(C.cols, 1)
        assert witness.dot(B) != 0
        out = {
            "n": N, "block_size": R, "sz_zero_dimension": len(ZERO),
            "columns": C.cols, "rank": rank, "augmented_rank": augmented_rank,
            "witness_dot_source": str(witness.dot(B)),
            "witness_nonzero_entries": sum(bool(v) for v in witness),
            "witness_by_basis_word": {''.join('+' if s == 0 else '0' if s == 1 else '-' for s in w): str(witness[i])
                                      for i, w in enumerate(ZERO) if witness[i]},
        }
        path = Path(__file__).with_name('aklt_r3_obstruction.json')
        path.write_text(json.dumps(out, indent=2) + '\n')
        print(json.dumps({k: v for k, v in out.items() if k != 'witness_by_basis_word'}, indent=2))

    both_cols = [col for j in range(N)
                 for placement in (0, -1)
                 for col in columns_for_bond(j, placement)]
    both = sp.Matrix.hstack(*both_cols)
    both_rank = DomainMatrix.from_Matrix(both).to_field().rank()
    both_augmented_rank = DomainMatrix.from_Matrix(both.row_join(B)).to_field().rank()
    both_out = {
        "n": N, "block_size": R, "placements": ["right", "left"],
        "sz_zero_dimension": len(ZERO), "columns": both.cols,
        "rank": both_rank, "augmented_rank": both_augmented_rank,
        "source_exactly_feasible": both_rank == both_augmented_rank,
        "note": "Rank membership only; placement columns overlap within each physical bond, so their raw coefficient norm is not a dual upper bound.",
    }
    both_path = Path(__file__).with_name(f'aklt_r3_all_placements_n{N}.json')
    both_path.write_text(json.dumps(both_out, indent=2) + '\n')
    print(json.dumps(both_out, indent=2))


if __name__ == '__main__':
    main()
