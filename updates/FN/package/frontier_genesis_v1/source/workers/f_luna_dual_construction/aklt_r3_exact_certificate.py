"""Exact N=6 AKLT local-row dual and tangent-primal certificate.

The source generator is the campaign's rational R=3 AKLT span probe. This
script independently solves the row-norm-constrained completion, computes an
exact full-sector response reference, and verifies a tangent-space lower
bound. It is a finite exact diagnostic, not a scaling proof.
"""
from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix


HERE = Path(__file__).resolve().parent
N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
SOURCE = HERE.parent / "f_sol_quantum_dual" / "aklt_r3_obstruction.py"
sys.argv = [str(SOURCE), str(N)]
src = runpy.run_path(str(SOURCE))

zero_words = src["ZERO"]
index = src["ZERO_INDEX"]
psi_entries = src["PSI"]
mag = src["MAG"]
projector = src["Q"]
columns_for_bond = src["columns_for_bond"]
dim = len(zero_words)

psi = sp.Matrix([psi_entries[word] for word in zero_words])
source = sp.Matrix([mag[word[0]] * psi_entries[word] for word in zero_words])
norm_psi_sq = (psi.T * psi)[0]
assert (psi.T * source)[0] == 0

# Exact parent Hamiltonian restricted to total S_z=0.
hamiltonian = sp.zeros(dim, dim)
for bond in range(N):
    for col, word in enumerate(zero_words):
        for in_pair, outputs in projector.items():
            if (word[bond], word[(bond + 1) % N]) != in_pair:
                continue
            for out_pair, coeff in outputs.items():
                updated = list(word)
                updated[bond], updated[(bond + 1) % N] = out_pair
                updated = tuple(updated)
                if updated in index:
                    hamiltonian[index[updated], col] += coeff

# The full R=3 ansatz allows both placements of the spin-2 pair in each
# three-site window. Reduce each row to an independent basis, retaining its
# physical row Gram matrix so duplicate placements are charged correctly.
row_bases: list[sp.Matrix] = []
for bond in range(N):
    row_columns = []
    for placement in (0, -1):
        row_columns.extend(columns_for_bond(bond, placement))
    row_matrix = sp.Matrix.hstack(*row_columns)
    row_bases.append(sp.Matrix.hstack(*row_matrix.columnspace()))

dual_map = sp.Matrix.hstack(*row_bases)
gram = sp.zeros(dual_map.cols, dual_map.cols)
offset = 0
row_dimensions = []
for basis in row_bases:
    count = basis.cols
    gram[offset : offset + count, offset : offset + count] = basis.T * basis
    row_dimensions.append(count)
    offset += count
assert gram.det() != 0

# Minimum sum_j ||w_j||^2 over this restricted local-row ansatz.
normal = dual_map * gram.inv() * dual_map.T
lagrange = normal.gauss_jordan_solve(source)[0]
coefficients = gram.inv() * dual_map.T * lagrange
assert dual_map * coefficients == source
dual_energy = sp.factor((coefficients.T * gram * coefficients)[0] / norm_psi_sq)

# Exact response reference. The rank-one anchor removes the MPS ground vector;
# centered source orthogonality makes this equal to H^+ source.
anchored = hamiltonian + psi * psi.T
response_vector = anchored.inv() * source
chi = sp.factor((source.T * response_vector)[0] / norm_psi_sq)

# Primal variational lower bound optimized in span{S^z_j psi}.
tangent = sp.Matrix.hstack(*[
    sp.Matrix([mag[word[j]] * psi_entries[word] for word in zero_words])
    for j in range(N)
])
tangent_gram = tangent.T * hamiltonian * tangent
tangent_rhs = tangent.T * source
tangent_coefficients = tangent_gram.gauss_jordan_solve(tangent_rhs)[0]
primal_vector = tangent * tangent_coefficients
primal_lower = sp.factor(
    (2 * (source.T * primal_vector)[0]
     - (primal_vector.T * hamiltonian * primal_vector)[0]) / norm_psi_sq
)

assert primal_lower <= chi <= dual_energy
result = {
    "n": N,
    "hilbert_dimension_total_sz_0": dim,
    "mps_bond_dimension": 2,
    "block_size": 3,
    "placements_per_bond": ["left", "right"],
    "independent_local_row_dimensions": row_dimensions,
    "dual_map_rank": DomainMatrix.from_Matrix(dual_map).to_field().rank(),
    "feasible_exactly": True,
    "chi_exact": str(chi),
    "primal_lower_exact": str(primal_lower),
    "dual_upper_exact": str(dual_energy),
    "lower_le_chi_le_upper_exact": True,
    "upper_over_chi_exact": str(sp.factor(dual_energy / chi)),
    "upper_over_chi": float(dual_energy / chi),
    "interval_width_exact": str(sp.factor(dual_energy - primal_lower)),
    "interval_width": float(dual_energy - primal_lower),
    "scope": "finite exact AKLT diagnostic only; no all-N construction or scaling claim",
}
out = HERE / f"aklt_r3_exact_certificate_n{N}.json"
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
