#!/usr/bin/env python3
"""Exact SU(3) sector replay for the full-space P_27 factor-two candidate.

The orbit-channel eigenvalue formula is proved in
regular_su3_unrestricted_eb.txt. This script checks its exact seed projection
norm inputs and the exact marginal spectrum; it is finite algebraic evidence,
not a substitute for the Schur-orthogonality proof.
"""
import importlib.util
from pathlib import Path
import sympy as sp

source = Path(__file__).parents[1] / "cycle4" / "multiplicity_blocks_check.py"
spec = importlib.util.spec_from_file_location("multiplicity_blocks", source)
mb = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mb)

d = 8
psi = sp.Matrix([1, sp.I, 0, 0, 0, 0, 0, 0]) / sp.sqrt(2)
P = psi * psi.conjugate().T
v = sp.Matrix(64, 1, list(P))
vt = sp.Matrix(64, 1, list(P.T))

sectors = [
    ("1", mb.P1, 1, sp.Rational(1, 1)),
    ("8s", mb.Ps, 8, sp.Rational(1, 5)),
    ("8a", mb.Pa, 8, sp.Rational(1, 3)),
    ("10+10bar", mb.P10, 20, sp.Rational(1, 15)),
    ("27", mb.P27, 27, sp.Rational(7, 135)),
]

norms = {}
for name, projector, dimension, expected_mu in sectors:
    euclidean = sp.simplify((v.conjugate().T * projector * v)[0])
    euclidean_transpose = sp.simplify((vt.conjugate().T * projector * vt)[0])
    assert euclidean == euclidean_transpose
    tau_norm = sp.simplify(euclidean / d)
    mu = sp.simplify(d**2 * tau_norm / dimension)
    assert mu == expected_mu, (name, tau_norm, mu, expected_mu)
    norms[name] = (tau_norm, mu)

# Exact marginal superoperator eigenvalues from P_27 compression.
K = mb.marginal_superoperator(mb.P27, 27)
actual = K.eigenvals()
expected = {
    sp.Integer(1): 1,
    sp.Rational(14, 25): 8,
    sp.Rational(2, 3): 8,
    sp.Rational(28, 75): 20,
    sp.Rational(218, 675): 27,
}
assert actual == expected, actual

ratios = {
    "8s": sp.Rational(20, 11),
    "8a": sp.Integer(2),
    "10+10bar": sp.Rational(70, 47),
    "27": sp.Rational(640, 457),
}
lambda_by_sector = {
    "8s": sp.Rational(14, 25),
    "8a": sp.Rational(2, 3),
    "10+10bar": sp.Rational(28, 75),
    "27": sp.Rational(218, 675),
}
for name, ratio in ratios.items():
    _, mu = norms[name]
    assert sp.simplify((1 - mu) / (1 - lambda_by_sector[name])) == ratio
    assert ratio <= 2
assert ratios["8a"] == 2

# Multiplicity-space matrix is checked independently by the original script.
assert mb.mode_block(mb.P27, 27) == sp.diag(sp.Rational(14, 25), sp.Rational(2, 3))

print({
    "marginal_spectrum": {str(k): v for k, v in actual.items()},
    "seed_projection_norms_tau": {k: str(v[0]) for k, v in norms.items()},
    "orbit_EB_multipliers": {k: str(v[1]) for k, v in norms.items()},
    "maximum_deficit_ratio": "2",
    "status": "exact sector inputs passed",
})
