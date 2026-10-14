#!/usr/bin/env python3
"""Exact AKLT N=6 susceptibility interval from primal and local dual witnesses.

The local dual uses the union of left and right three-site placements for each
physical bond. Each bond's overlapping placement columns are merged into one
subspace and its orthogonal projector before minimizing the dual norm.
"""

import json
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import aklt_r3_obstruction as ak

assert ak.N == 6
D = len(ak.ZERO)
psi = sp.Matrix([ak.PSI[word] for word in ak.ZERO])
norm = psi.dot(psi)
b = ak.B


def rational_solution(matrix: sp.Matrix, rhs: sp.Matrix) -> sp.Matrix:
    aug = matrix.row_join(rhs)
    reduced, pivots = DomainMatrix.from_Matrix(aug).to_field().rref()
    assert matrix.cols not in pivots
    r = reduced.to_Matrix()
    out = sp.zeros(matrix.cols, 1)
    for row, col in enumerate(pivots):
        out[col] = r[row, matrix.cols]
    assert matrix * out == rhs
    return out


def bond_projector(j: int) -> sp.Matrix:
    k = (j + 1) % ak.N
    p = sp.zeros(D)
    for word, col in ak.ZERO_INDEX.items():
        for pair, coeff in ak.Q[(word[j], word[k])].items():
            changed = list(word)
            changed[j], changed[k] = pair
            p[ak.ZERO_INDEX[tuple(changed)], col] += coeff
    assert p * p == p
    return p


def main() -> None:
    bonds = [bond_projector(j) for j in range(ak.N)]
    h = sum(bonds, sp.zeros(D))
    assert h * psi == sp.zeros(D, 1)

    local_projectors = []
    local_ranks = []
    for j in range(ak.N):
        columns = [col for offset in (0, -1)
                   for col in ak.columns_for_bond(j, offset)]
        raw = sp.Matrix.hstack(*columns)
        _, pivots = DomainMatrix.from_Matrix(raw).to_field().rref()
        basis = raw[:, list(pivots)]
        local_ranks.append(basis.cols)
        projection = basis * (basis.T * basis).inv() * basis.T
        assert projection * projection == projection
        assert bonds[j] * projection == projection
        local_projectors.append(projection)

    q = sum(local_projectors, sp.zeros(D))
    y = rational_solution(q, b)
    w = [projection * y for projection in local_projectors]
    assert sum(w, sp.zeros(D, 1)) == b
    upper = sum(wj.dot(wj) for wj in w) / norm
    assert upper == b.dot(y) / norm

    # Six-step Galerkin/Krylov primal lower witness.
    vectors = []
    v = b
    for _ in range(6):
        vectors.append(v)
        v = h * v
    gram = sp.Matrix([[vi.dot(h * vj) for vj in vectors]
                      for vi in vectors])
    rhs = sp.Matrix([b.dot(vi) for vi in vectors])
    coeff = gram.inv() * rhs
    x = sum((coeff[i] * vectors[i] for i in range(len(vectors))),
            sp.zeros(D, 1))
    lower = (2 * b.dot(x) - x.dot(h * x)) / norm
    assert lower == rhs.dot(coeff) / norm
    primal_residual = b - h * x
    residual_squared = primal_residual.dot(primal_residual) / norm
    gap = sum((wj - bonds[j] * x).dot(wj - bonds[j] * x)
              for j, wj in enumerate(w)) / norm
    assert gap == upper - lower

    out = {
        "model": "periodic spin-1 AKLT, six sites, exact MPS ground state",
        "source": "b=S_z(0)|psi>, with <psi|b>=0",
        "physical_hilbert_dimension": 3**ak.N,
        "sz_zero_dimension": D,
        "local_block_size": 3,
        "local_placements_per_bond": 2,
        "local_dual_ranks_by_bond": local_ranks,
        "source_in_exact_dual_span": True,
        "primal_krylov_steps": len(vectors),
        "lower_exact": str(lower),
        "primal_residual_squared_exact": str(residual_squared),
        "primal_residual_squared_decimal": str(sp.N(residual_squared, 16)),
        "residual_gap_upper_if_gamma_at_least_one_tenth_exact": str(lower + 10 * residual_squared),
        "residual_gap_upper_if_gamma_at_least_one_tenth_decimal": str(sp.N(lower + 10 * residual_squared, 16)),
        "gap_lower_bound_needed_to_beat_local_dual_exact": str(residual_squared / (upper - lower)),
        "upper_exact": str(upper),
        "gap_exact": str(gap),
        "lower_decimal": str(sp.N(lower, 16)),
        "upper_decimal": str(sp.N(upper, 16)),
        "relative_interval_width_over_lower": str(sp.N(gap / lower, 8)),
        "exact_zero_checks": {
            "H_ground": True,
            "dual_sum_minus_b": True,
            "duality_gap_identity": True,
            "local_bond_projector_action": True,
        },
        "status": "finite exact certificate; no all-N theorem, physical acquisition, or comparative advantage",
    }
    path = Path(__file__).with_name('aklt_n6_certified_interval.json')
    path.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
