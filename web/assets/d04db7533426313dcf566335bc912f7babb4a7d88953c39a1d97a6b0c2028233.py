"""Finite check of the d=2 MUB projective-2-design inverse formula.

This checks an exact identity already known from projective-design frame theory;
it is not a proof and is not a novel algorithm.
"""
import numpy as np

d = 2
s = 1 / np.sqrt(2)
# Columns are normalized vectors in the Pauli X, Y, and Z bases.
bases = [
    np.array([[1, 1], [1, -1]], dtype=complex) * s,
    np.array([[1, 1], [1j, -1j]], dtype=complex) * s,
    np.eye(2, dtype=complex),
]
Acols = np.concatenate(bases, axis=1)
projectors = [np.outer(Acols[:, j], Acols[:, j].conj()) for j in range(6)]
x = np.array([0.37 + 0.21j, -0.43 + 0.78j])
y = np.array([abs(np.vdot(Acols[:, j], x)) ** 2 for j in range(6)])
S = sum(yj * Pj for yj, Pj in zip(y, projectors))
Xhat = (d * (d + 1) / len(y)) * S - (d / len(y)) * np.trace(S) * np.eye(d)
X = np.outer(x, x.conj())
T = sum(np.kron(Pj, Pj) for Pj in projectors)
I4 = np.eye(d * d)
F = np.zeros((d * d, d * d), dtype=complex)
for i in range(d):
    for j in range(d):
        F[i * d + j, j * d + i] = 1
Ttarget = len(y) / (d * (d + 1)) * (I4 + F)
print(f"reconstruction_max_abs_error={np.max(np.abs(Xhat - X)):.3e}")
print(f"moment_identity_max_abs_error={np.max(np.abs(T - Ttarget)):.3e}")
print(f"sum_intensities_error={abs(y.sum() - (d + 1) * np.vdot(x, x).real):.3e}")
print(f"theorem_constants L={np.sqrt(len(y)/(2*d*(d+1))):.12g} U={np.sqrt(2*len(y)/(d*(d+1))):.12g} beta=2")
