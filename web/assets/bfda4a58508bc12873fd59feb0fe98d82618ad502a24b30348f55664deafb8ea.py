"""Exact single designed control; not the general comparator compiler.

Input is B=(2/5)B_copy+(3/5)B_symmetric_clone on d=2.
SymPy rational arithmetic only. Enumerates 144 records at depth ONE;
no claim of enumerating the general polynomial-depth alphabet.
"""
import hashlib
import itertools
import json
from pathlib import Path

import sympy as s

F = s.Rational
I2 = s.eye(2)
Z = s.diag(1, -1)
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -s.I], [s.I, 0]])
q = F(2, 5)
W = [
    s.Matrix([[1, 0], [0, 0], [0, 0], [0, 0]]),
    s.Matrix([[0, 0], [0, 0], [0, 0], [0, 1]]),
    s.Matrix([[1, 0], [0, F(1, 2)], [0, F(1, 2)], [0, 0]]),
    s.Matrix([[0, 0], [F(1, 2), 0], [F(1, 2), 0], [0, 1]]),
]
u = [s.Matrix(v) for v in ([1, 0], [0, 1], [1, 1], [1, -1], [1, s.I], [1, -s.I])]
f = [F(1, 3), F(1, 3)] + [F(1, 6)] * 4
leaf = [f[z] * u[z] * u[z].H for z in range(6)]


def B(A):
    return sum((q * w * A * w.H for w in W), s.zeros(4))


def tr_right(A):
    return s.Matrix(2, 2, lambda i, j: sum(A[2 * i + k, 2 * j + k] for k in range(2)))


def tr_left(A):
    return s.Matrix(2, 2, lambda i, j: sum(A[2 * k + i, 2 * k + j] for k in range(2)))


def pull(branches, A, C):
    return s.simplify(sum((q * W[j].H * s.kronecker_product(A, C) * W[j] for j in branches), s.zeros(2)))


def partial(h):
    # Variables are left leaf, internal Kraus branch, right leaf.
    zl, j, zr = h
    A = I2 if zl is None else leaf[zl]
    C = I2 if zr is None else leaf[zr]
    return pull(range(4) if j is None else [j], A, C)


assert sum((q * w.H * w for w in W), s.zeros(2)) == I2
assert sum(leaf, s.zeros(2)) == I2
for A in [I2, X, Y, Z]:
    assert tr_left(B(A)) == tr_right(B(A))
assert tr_right(B(I2)) == I2
assert tr_right(B(X)) == F(2, 5) * X
assert tr_right(B(Y)) == F(2, 5) * Y
assert tr_right(B(Z)) == F(4, 5) * Z
choi_columns = [s.Matrix([w[alpha, i] for i in range(2) for alpha in range(4)]) for w in W]
choi = sum((q * v * v.H for v in choi_columns), s.zeros(8))
assert choi.is_positive_semidefinite is True

records = list(itertools.product(range(6), range(4), range(6)))
effect = {}
posterior = {}
probability = {}
for zl, j, zr in records:
    row = s.kronecker_product(u[zl].H, u[zr].H) * W[j]
    M = s.simplify(q * f[zl] * f[zr] * row.H * row)
    assert s.simplify(M - partial((zl, j, zr))) == s.zeros(2)
    assert M.det() == 0
    assert M.is_positive_semidefinite is True
    effect[zl, j, zr] = M
    p = s.trace(M) / 2
    probability[zl, j, zr] = p
    if p:
        pi = s.simplify(M / s.trace(M))
        assert s.simplify(pi * pi - pi) == s.zeros(2) and s.trace(pi) == 1
        posterior[zl, j, zr] = pi

assert s.simplify(sum(effect.values(), s.zeros(2)) - I2) == s.zeros(2)
assert sum(probability.values()) == 1
assert s.simplify(sum((probability[w] * pi for w, pi in posterior.items()), s.zeros(2)) - I2 / 2) == s.zeros(2)

# All partial prefixes in the chosen interleaving must equal the direct
# sum of fine event effects; this checks correlated conditional sampling.
prefix_count = 0
for length in range(4):
    for prefix in itertools.product(*([range(6), range(4), range(6)][:length])):
        h = tuple(prefix) + (None,) * (3 - length)
        direct = sum((effect[w] for w in records if w[:length] == prefix), s.zeros(2))
        assert s.simplify(partial(h) - direct) == s.zeros(2)
        if length < 3:
            domain = [6, 4, 6][length]
            assert s.simplify(sum((partial(tuple(prefix) + (v,) + (None,) * (2 - length)) for v in range(domain)), s.zeros(2)) - direct) == s.zeros(2)
        prefix_count += 1


def Psi(A):
    return s.simplify(sum((effect[w] * s.trace(pi * A) for w, pi in posterior.items()), s.zeros(2)))


basis = [I2, X, Y, Z]
supermatrix = s.Matrix(4, 4, lambda i, j: s.simplify(s.trace(basis[i] * Psi(basis[j])) / 2))
assert supermatrix == supermatrix.T
assert Psi(I2) == I2
assert supermatrix.is_positive_semidefinite is True
assert (s.eye(4) - supermatrix).is_positive_semidefinite is True
target = s.diag(1, 4 * F(2, 5) - 3, 4 * F(2, 5) - 3, 4 * F(4, 5) - 3)
certificate = s.simplify(supermatrix - target)
assert certificate.is_positive_semidefinite is True

# Coarse all-X+ record mixes the two copy directions and is not rank one.
mixed_coarse = partial((2, None, 2))
assert mixed_coarse.rank() == 2

rho = B(I2 / 2)
Czz = s.trace(rho * s.kronecker_product(Z, Z))
assert Czz == F(3, 5)
leaf_z_estimate = [3, -3, 0, 0, 0, 0]
Nm = sum(probability[w] * (F(5, 8) * (leaf_z_estimate[w[0]] + leaf_z_estimate[w[2]])) ** 2 for w in records)
assert Nm == F(45, 16)
assert Nm == (3 + Czz) / (2 * F(4, 5) ** 2)
assert Nm != 3 / (2 * F(4, 5) ** 2)

result = {
    "status": "EXACT_DESIGNED_CONTROL_PASS",
    "scope": "One legal d=2 depth-one control, not a general compiler or finite-depth theorem validation",
    "input": {
        "d": 2, "copy_weight": "2/5", "symmetric_clone_weight": "3/5",
        "unnormalized_joint_Choi_input_then_output": str(choi),
        "branch_q": "2/5", "branch_W": [str(w) for w in W],
        "leaf_rows": [str(a.H) for a in u], "leaf_f": [str(c) for c in f],
        "depth": 1, "sampling_variable_order": ["left_leaf", "Kraus_branch", "right_leaf"],
    },
    "records": len(records),
    "nonzero_records": len(posterior),
    "partial_prefixes_checked": prefix_count,
    "Phi_I_X_Y_Z_eigenvalues": ["1", "2/5", "2/5", "4/5"],
    "reference_sibling_Czz": str(Czz),
    "exact_estimator_covariance_z": str(Nm),
    "incorrect_independent_sibling_covariance_z": str(3 / (2 * F(4, 5) ** 2)),
    "fine_canonical_supermatrix_I_X_Y_Z": str(supermatrix),
    "C4_exact_full_order_certificate": str(certificate),
    "coarse_Xplus_Xplus_effect": str(mixed_coarse),
    "coarse_Xplus_Xplus_rank": mixed_coarse.rank(),
    "enumeration": "Only 144 records in this designed depth-one diagnostic; general algorithm uses conditional sampling",
    "factorization_scope": "Displayed rational Gram factors are used; a general Choi-to-LDL compiler is not implemented by this diagnostic",
}
result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
out = Path(__file__).with_name("EXACT_CORRELATED_CONTROL.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
