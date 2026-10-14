"""Independent exact checks for the acoustic-face obstruction audit.

This script imports no code from the supplied worker package.  It reconstructs
the two quartics from their displayed formulas, differentiates them directly,
and checks exact identities and finite lifted-barycenter laws.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


a, b, c, d, p, t, tau = sp.symbols("a b c d p t tau", real=True)
coords = (a, b, c, d)
u = a**2 + c**2
v = b**2 + d**2
w = a * b + c * d
q = a * d - b * c
Fstar = sp.expand(u**2 + v**2 + 4 * w**2 + sp.Rational(7, 2) * q**2 - sp.Rational(29, 10) * q * (u + v))
G = sp.expand(3 * (u + v - 2 * q) ** 2 + sp.Rational(35, 24) * u**2 + q**2 - sp.Rational(5, 2) * q * u)


def matrix_vars(M: sp.Matrix) -> dict[sp.Symbol, sp.Expr]:
    return {a: M[0, 0], b: M[0, 1], c: M[1, 0], d: M[1, 1]}


def matrix_flat(M: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([M[0, 0], M[0, 1], M[1, 0], M[1, 1]])


def rank_one(a_vec: sp.Matrix, b_vec: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([a_vec[0] * b_vec[0], a_vec[0] * b_vec[1], a_vec[1] * b_vec[0], a_vec[1] * b_vec[1]])


def second_derivative(expr: sp.Expr, at: sp.Matrix, direction: sp.Matrix) -> sp.Expr:
    hessian = sp.hessian(expr, coords).subs(matrix_vars(at))
    return sp.factor((direction.T * hessian * direction)[0])


# Reconstruct the acoustic polynomial by differentiating Fstar itself.  The
# rational Gram is the independently transcribed N794 certificate; positivity
# below is checked by an exact LDL factorization as well as the polynomial identity.
X = sp.Matrix(coords)
F_hessian = sp.hessian(Fstar, coords)
first_row_probe = sp.Matrix([p, t, 0, 0])
acoustic = sp.expand((first_row_probe.T * F_hessian * first_row_probe)[0])
z = sp.Matrix([p * a, p * b, p * c, p * d, t * a, t * b, t * c, t * d])
Q = sp.Matrix(
    [
        [12, 0, 0, sp.Rational(-87, 10), 0, sp.Rational(17, 2), sp.Rational(23, 5), 0],
        [0, 8, sp.Rational(29, 10), 0, sp.Rational(15, 2), 0, 0, sp.Rational(-6, 5)],
        [0, sp.Rational(29, 10), 4, 0, sp.Rational(6, 5), 0, 0, sp.Rational(14, 5)],
        [sp.Rational(-87, 10), 0, 0, 7, 0, sp.Rational(-23, 5), sp.Rational(-9, 5), 0],
        [0, sp.Rational(15, 2), sp.Rational(6, 5), 0, 8, 0, 0, sp.Rational(-29, 10)],
        [sp.Rational(17, 2), 0, 0, sp.Rational(-23, 5), 0, 12, sp.Rational(87, 10), 0],
        [sp.Rational(23, 5), 0, 0, sp.Rational(-9, 5), 0, sp.Rational(87, 10), 7, 0],
        [0, sp.Rational(-6, 5), sp.Rational(14, 5), 0, sp.Rational(-29, 10), 0, 0, 4],
    ]
)
assert sp.expand(acoustic - (z.T * Q * z)[0]) == 0
shifted = Q - sp.eye(8) / 16
L, D = shifted.LDLdecomposition(hermitian=False)
ldl_pivots = [sp.factor(D[i, i]) for i in range(8)]
assert L * D * L.T == shifted
assert all(x.is_Rational and x > 0 for x in ldl_pivots)

# SO(2) output invariance gives the same uniform estimate for every output
# vector after rotating it to e1; check a nontrivial exact instance of the
# chain-rule and singular-value constants at B0=diag(2,3).
B0 = sp.diag(2, 3)
a0 = sp.Matrix([1, 1])
b0 = sp.Matrix([1, 2])
S = sp.diag(sp.Rational(3, 5), sp.Rational(4, 5))  # Frobenius norm one; invertible
X0 = B0 * S
probe_b = S.T * b0
ell_value = second_derivative(Fstar, X0, rank_one(a0, probe_b))
ell_lower = sp.Rational(1, 16) * sp.Rational(2) ** 2 * (a0.dot(a0)) * (probe_b.dot(probe_b))
assert ell_value >= ell_lower
lambda_value = sum(
    second_derivative(Fstar, X0, rank_one(a0, S.T * ej))
    for ej in (sp.Matrix([1, 0]), sp.Matrix([0, 1]))
)
lambda_lower = sp.Rational(1, 16) * sp.Rational(2) ** 2 * a0.dot(a0)
assert lambda_value >= lambda_lower

# The normalized invertible orbit can approach its rank-one zero set while
# the sum-probe lower bound stays fixed.  This is the mechanism used in the
# compactness argument, checked on exact rational Pythagorean parameters.
orbit_sequence = []
for n in (2, 3, 10):
    x = sp.Rational(n * n - 1, n * n + 1)
    y = sp.Rational(2 * n, n * n + 1)
    Sn = sp.diag(x, y)
    assert sp.trace(Sn.T * Sn) == 1 and sp.det(Sn) != 0
    null_probe_norm_sq = (Sn.T * sp.Matrix([0, 1])).dot(Sn.T * sp.Matrix([0, 1]))
    orbit_sequence.append({"n": n, "distance_probe_norm_sq": str(null_probe_norm_sq), "lambda_lower": "1/16"})

# Rank-one limiting atoms are ordinary convex functions.  This concrete
# normalized boundary transform makes the restricted profile explicit.
S_boundary = sp.Matrix([[sp.Rational(3, 5), sp.Rational(4, 5)], [0, 0]])
boundary_expr = sp.factor(Fstar.subs(matrix_vars(sp.Matrix([[a, b], [c, d]]) * S_boundary), simultaneous=True))
boundary_constant = sp.Rational(3, 5) ** 4 + 4 * sp.Rational(3, 5) ** 2 * sp.Rational(4, 5) ** 2 + sp.Rational(4, 5) ** 4
assert sp.expand(boundary_expr - boundary_constant * (a**2 + c**2) ** 2) == 0
boundary_hessian_in_z = sp.hessian(boundary_constant * (a**2 + c**2) ** 2, (a, c))
assert sp.expand(boundary_hessian_in_z[0, 0] - boundary_constant * (12 * a**2 + 4 * c**2)) == 0
assert sp.expand(boundary_hessian_in_z.det() - 48 * boundary_constant**2 * (a**2 + c**2) ** 2) == 0

# Exact target null probe and the determinant-balanced finite law.
I = sp.eye(2)
J = sp.diag(1, -1)
G_line = sp.factor(G.subs({a: 1, b: tau, c: 0, d: 1}))
assert sp.expand(G_line - (3 * tau**4 - sp.Rational(1, 24))) == 0
assert sp.diff(G_line, tau, 2).subs(tau, 0) == 0
assert G.subs(matrix_vars(I)) == -sp.Rational(1, 24)
assert G.subs(matrix_vars(J)) == sp.Rational(1271, 24)

G_law = [
    (36 * I, sp.Rational(1, 2 * 1297)),
    (-36 * I, sp.Rational(1, 2 * 1297)),
    (J, sp.Rational(1296, 2 * 1297)),
    (-J, sp.Rational(1296, 2 * 1297)),
]
G_mean_A = sum((weight * M for M, weight in G_law), sp.zeros(2))
G_mean_det = sum((weight * M.det() for M, weight in G_law), sp.Integer(0))
G_mean_energy = sum((weight * G.subs(matrix_vars(M)) for M, weight in G_law), sp.Integer(0))
assert G_mean_A == sp.zeros(2) and G_mean_det == 0
assert G_mean_energy == -sp.Rational(1350, 1297)

# Assumption stress test: if invertibility of B0 (or nonzero probe vectors)
# is dropped, the N794 Fstar law itself is a counterexample to the weakened
# implication.  This is not a counterexample to the stated theorem.
Fstar_law = [
    (7 * I, sp.Rational(1, 100)),
    (-7 * I, sp.Rational(1, 100)),
    (J, sp.Rational(49, 100)),
    (-J, sp.Rational(49, 100)),
]
Fstar_mean_A = sum((weight * M for M, weight in Fstar_law), sp.zeros(2))
Fstar_mean_det = sum((weight * M.det() for M, weight in Fstar_law), sp.Integer(0))
Fstar_mean_energy = sum((weight * Fstar.subs(matrix_vars(M)) for M, weight in Fstar_law), sp.Integer(0))
assert Fstar_mean_A == sp.zeros(2) and Fstar_mean_det == 0
assert Fstar_mean_energy == -sp.Rational(833, 250)
zero_background_probe = second_derivative(Fstar, sp.zeros(2), rank_one(sp.Matrix([1, 0]), sp.Matrix([0, 1])))
assert zero_background_probe == 0

out = {
    "status": "PASS",
    "source_verifier_independent_checks": {
        "Fstar_acoustic_gram_identity": True,
        "shifted_exact_ldl_pivots": [str(x) for x in ldl_pivots],
        "Fstar_strict_constant": "1/16",
    },
    "general_proof_stress_checks": {
        "B0_invertible_exact_ell": str(ell_value),
        "B0_invertible_exact_ell_lower_bound": str(ell_lower),
        "B0_invertible_exact_lambda": str(lambda_value),
        "B0_invertible_exact_lambda_lower_bound": str(lambda_lower),
        "normalized_invertible_orbit_sequence": orbit_sequence,
        "boundary_rank1_convex_profile_constant": str(boundary_constant),
    },
    "target_witness": {
        "G_line": str(G_line),
        "G_I": str(G.subs(matrix_vars(I))),
        "G_J": str(G.subs(matrix_vars(J))),
        "mean_A": str(G_mean_A),
        "mean_det": str(G_mean_det),
        "mean_G": str(G_mean_energy),
    },
    "assumption_boundary_test": {
        "Fstar_mean_A": str(Fstar_mean_A),
        "Fstar_mean_det": str(Fstar_mean_det),
        "Fstar_mean_energy": str(Fstar_mean_energy),
        "D2Fstar_at_zero_rank1_probe": str(zero_background_probe),
        "interpretation": "Counterexample only after dropping invertible B0; the stated theorem is unaffected.",
    },
}
out_path = Path(__file__).with_name("independent_acoustic_face_checks.json")
out_path.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
