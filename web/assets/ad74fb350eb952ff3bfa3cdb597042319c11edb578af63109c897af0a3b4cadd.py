"""Symbolic algebra checks for the analytic USp(2n) mixed-dual proof.

This verifies the displayed 2x2 block identities and support accounting.
It does not replace the representation-theoretic proof in
USp_fundamental_all_mixed_Q.md.
"""
from __future__ import annotations

import sympy as sp


d, a, b = sp.symbols("d a b", positive=True, real=True)
t = 1 / d
alpha = d**2 * (a + b) / 2
beta = d * (b - a) / 2
gamma = -2 * b
h = sp.expand(gamma + alpha * (1 + t) - beta)

# Matrix of the star on the output-antisymmetric contraction multiplicity
# space in the nonorthogonal basis (U_01-U_02, U_12).
H_minus = sp.Matrix(
    [
        [alpha * (1 - t) - beta + gamma, -alpha * t - beta],
        [-2 * beta, gamma],
    ]
)
gram = sp.Matrix([[2 * (1 - t), -2 * t], [-2 * t, 1]])
gap = sp.simplify(h * sp.eye(2) - H_minus)

assert sp.simplify(gram * H_minus - (gram * H_minus).T) == sp.zeros(2)
assert sp.simplify(gram.det() - 2 * (d - 2) * (d + 1) / d**2) == 0
assert sp.simplify(sp.trace(gap) - d * ((d + 4) * a + (d + 2) * b) / 2) == 0
assert sp.simplify(gap.det() - (
    d**2
    * ((d + 2) * a**2 + 2 * (d + 2) * a * b + (d - 2) * b**2)
    / 2
)) == 0

# The complement bound h - (gamma + 2|beta|) is checked in the two
# parameter regions b >= a and a >= b, without sampling.
gap_b_ge_a = sp.factor((h - gamma - 2 * beta))
gap_a_ge_b = sp.factor((h - gamma + 2 * beta))
assert sp.simplify(gap_b_ge_a - d * ((d + 4) * a + (d - 2) * b) / 2) == 0
assert sp.simplify(gap_a_ge_b - d * (d * a + (d + 2) * b) / 2) == 0

n_plus = d * (d + 1) / 2
n_minus = (d - 2) * (d + 1) / 2
eb_support = (a * n_plus + b * n_minus) / (d + 1)
assert sp.simplify(h - (a * n_plus + b * n_minus + eb_support)) == 0

print("PASS: Gram metric, antisymmetric trace/determinant, complement cases, and EB support identity")
