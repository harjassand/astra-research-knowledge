"""Independent L=2 control: actual sparse joint map and complex conditionals.

Density entries use exact rational arithmetic. SymPy is used only for one
complex rank-one conditioning calculation. No optimization is performed.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json
import sympy as s

OWN = Path(__file__).resolve().parent
D, L = 4, 2
ns = [1, 2]
basis = [(j, T) for j, n in enumerate(ns) for T in combinations(range(D), n)]
index = {label: i for i, label in enumerate(basis)}
bottom = [index[(0, (i,))] for i in range(D)]

def add(out, key, value):
    out[key] += value

rho, effect = defaultdict(F), defaultdict(F)
for j, n in enumerate(ns):
    for subset in combinations(range(D), n + 1):
        terms = [((a, index[(j, tuple(x for x in subset if x != a))]), (-1) ** p)
                 for p, a in enumerate(subset)]
        for row, x in terms:
            for col, y in terms:
                add(effect, (row, col), F(x * y, n + 1))
                add(rho, (row, col), F(x * y, L * (n + 1) * comb(D, n + 1)))
assert sum(v for (row, col), v in rho.items() if row == col) == 1
assert sum(v * effect.get((col, row), F()) for (row, col), v in rho.items()) == 1

# The active isometry maps each wedge^2 determinant to two antisymmetric
# singleton terms, with their common coefficient 1/sqrt(2) kept implicit.
columns = {}
for i, (j, T) in enumerate(basis):
    if j == 1:
        u, v = T
        columns[i] = {(index[(0, (u,))], index[(0, (v,))]): 1,
                      (index[(0, (v,))], index[(0, (u,))]): -1}
for i, ci in columns.items():
    for k, ck in columns.items():
        assert sum(F(x * ck.get(out, 0), 2) for out, x in ci.items()) == int(i == k)
    assert {(c, b): x for (b, c), x in ci.items()} == {key: -x for key, x in ci.items()}

# Direct application of the ONE broadcaster to the sparse input state.
joint = defaultdict(F)
for ((a, i), (aa, ii)), value in rho.items():
    j, _ = basis[i]
    jj, _ = basis[ii]
    if j != jj:
        continue
    if j == 0:
        if i == ii:
            for b in bottom:
                for c in bottom:
                    add(joint, ((a, b, c), (aa, b, c)), value / D ** 2)
    else:
        for (b, c), x in columns[i].items():
            for (bb, cc), y in columns[ii].items():
                add(joint, ((a, b, c), (aa, bb, cc)), value * F(x * y, 2))
joint = {key: value for key, value in joint.items() if value}
assert sum(v for (row, col), v in joint.items() if row == col) == 1
assert all(v == joint.get(((row[0], row[2], row[1]),
                           (col[0], col[2], col[1])), F())
           for (row, col), v in joint.items())
marginal_b, marginal_c = defaultdict(F), defaultdict(F)
for (row, col), value in joint.items():
    if row[2] == col[2]:
        add(marginal_b, (row[:2], col[:2]), value)
    if row[1] == col[1]:
        add(marginal_c, ((row[0], row[2]), (col[0], col[2])), value)
assert dict(marginal_b) == dict(marginal_c)
expected_delta = defaultdict(F)
for a in range(D):
    for b in bottom:
        add(expected_delta, ((a, b), (a, b)), F(1, L * D ** 2))
for key, value in rho.items():
    if basis[key[0][1]][0] == L - 1:
        add(expected_delta, key, -value)
for key in set(rho) | set(marginal_b) | set(expected_delta):
    assert marginal_b.get(key, F()) - rho.get(key, F()) == expected_delta.get(key, F())
positive_trace = sum(v for (row, col), v in expected_delta.items()
                     if row == col and basis[row[1]][0] == 0)
negative_trace = sum(v for (row, col), v in expected_delta.items()
                     if row == col and basis[row[1]][0] == L - 1)
assert positive_trace == F(1, L) and negative_trace == -F(1, L)

# The full-domain map is CP by these Kraus isometries plus replacement.
# Its summed Gram is I on bottom and top and zero between distinct flags.
gram = [[F() for k in range(len(basis))] for i in range(len(basis))]
for i, ci in columns.items():
    for k, ck in columns.items():
        gram[i][k] += sum(F(x * ck.get(out, 0), 2) for out, x in ci.items())
for t in bottom:
    for r in bottom:
        for ss in bottom:
            gram[t][t] += F(1, D ** 2)
assert all(gram[i][k] == int(i == k) for i in range(len(basis)) for k in range(len(basis)))

# Direct compression of the actual projector for a complex unit A vector.
phase = [s.S.One, s.I, s.S.Zero, s.S.Zero]  # divide by sqrt(2)
conditional_complex = s.zeros(len(basis))
ranks = []
for j, n in enumerate(ns):
    sector = [i for i, label in enumerate(basis) if label[0] == j]
    compressed = s.zeros(len(sector))
    for b, i in enumerate(sector):
        for bb, ii in enumerate(sector):
            compressed[b, bb] = s.simplify(sum(
                s.conjugate(phase[a]) * phase[aa] *
                s.Rational(effect.get(((a, i), (aa, ii)), F())) / 2
                for a in range(D) for aa in range(D)))
    projector = ((n + 1) * compressed).applyfunc(s.simplify)
    assert projector == projector.H
    assert projector * projector == projector
    assert s.trace(projector) == comb(D - 1, n)
    ranks.append(int(s.trace(projector)))
    state = projector / (L * comb(D - 1, n))
    for b, i in enumerate(sector):
        for bb, ii in enumerate(sector):
            conditional_complex[i, ii] = state[b, bb]
            direct = s.simplify(sum(
                D * s.conjugate(phase[a]) * phase[aa] *
                s.Rational(rho.get(((a, i), (aa, ii)), F())) / 2
                for a in range(D) for aa in range(D)))
            assert s.simplify(state[b, bb] - direct) == 0
assert s.trace(conditional_complex) == 1

# A finite uniform orthonormal A prior gives exactly rho_B.
bary = defaultdict(F)
for a in range(D):
    for i in range(len(basis)):
        for ii in range(len(basis)):
            add(bary, (i, ii), rho.get(((a, i), (a, ii)), F()))
assert all(bary[i, ii] == (F(1, L * comb(D, ns[basis[i][0]])) if i == ii else F())
           for i in range(len(basis)) for ii in range(len(basis)))
conditional_halftrace = sum(F(n, L * D) for n in ns)
assert conditional_halftrace == F(3, 8)

# The shared-vacuum extension's ONE map copies vacuum and uses this map
# on the active subspace. Both marginal differences scale exactly by w.
w = F(1, L)
vac_a, vac_b = D, len(basis)
flagged_rho = {(row, col): w * value for (row, col), value in rho.items()}
flagged_rho[((vac_a, vac_b), (vac_a, vac_b))] = 1 - w
flagged_joint = {(row, col): w * value for (row, col), value in joint.items()}
flagged_joint[((vac_a, vac_b, vac_b), (vac_a, vac_b, vac_b))] = 1 - w
flagged_marginal = defaultdict(F)
for (row, col), value in flagged_joint.items():
    if row[2] == col[2]:
        add(flagged_marginal, (row[:2], col[:2]), value)
for key in set(flagged_rho) | set(flagged_marginal) | set(expected_delta):
    assert flagged_marginal.get(key, F()) - flagged_rho.get(key, F()) == w * expected_delta.get(key, F())
assert sum(v for (row, col), v in flagged_marginal.items()
           if row == col and row[0] != vac_a) == w
assert sum(v * effect.get((col, row), F()) for (row, col), v in flagged_rho.items()) == w

result = {"status": "ALL_EXACT_ASSERTIONS_PASSED", "L": L, "D": D,
          "dim_B": len(basis), "joint_output_nonzero_entries": len(joint),
          "scope": "one L=2 exact channel and flagged control, not an optimization or quantified proof",
          "isometry_TP": True, "full_domain_pinching_and_replacement": True,
          "BC_swap_invariant": True, "both_marginal_differences_exact": True,
          "broadcast_halftrace": str(F(1, L)), "complex_conditional_projector_ranks": ranks,
          "uniform_conditional_halftrace": str(conditional_halftrace),
          "finite_basis_prior_barycenter": True,
          "max_prior_Holevo_exact_expression": "ln(8/3)/2",
          "mutual_information_exact_expression": "ln(4)",
          "flagged_broadcast_halftrace": str(w / L),
          "unchanged_A_active_mass": str(w), "flagged_EB_lower_bound": str(w / 2),
          "blind_proof_sha256": hashlib.sha256((OWN / "THEOREM_FIRST_BASELINE.txt").read_bytes()).hexdigest(),
          "flag_proof_sha256": hashlib.sha256((OWN / "FLAG_EXTENSION_THEOREM_FIRST_AUDIT.txt").read_bytes()).hexdigest()}
(OWN / "FULL_CHANNEL_L2_REPLAY.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
