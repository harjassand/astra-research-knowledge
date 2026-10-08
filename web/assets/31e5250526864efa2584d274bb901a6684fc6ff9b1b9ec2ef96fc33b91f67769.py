"""Finite d=3 check of the complete-MUB deletion formulas in CYCLE2_REPORT.md.

This verifies one explicit instance only; the prime-power family proof is algebraic.
"""
import numpy as np


def complete_mub_prime(p):
    omega = np.exp(2j * np.pi / p)
    shift = np.zeros((p, p), dtype=complex)
    for k in range(p):
        shift[(k + 1) % p, k] = 1
    phase = np.diag([omega**k for k in range(p)])
    bases = [np.eye(p, dtype=complex)]
    for a in range(p):
        _, vectors = np.linalg.eig(shift @ np.linalg.matrix_power(phase, a))
        vectors = vectors / np.linalg.norm(vectors, axis=0, keepdims=True)
        bases.append(vectors)
    return bases


d = 3
bases = complete_mub_prime(d)
projectors = [np.outer(b[:, k], b[:, k].conj()) for b in bases for k in range(d)]
m0 = len(projectors)
N = d * (d + 1) // 2
P_sym = np.zeros((d * d, d * d), dtype=complex)
for i in range(d):
    for j in range(d):
        P_sym[i * d + j, i * d + j] += 0.5
        P_sym[i * d + j, j * d + i] += 0.5
F0 = P_sym / N
Ffull = sum(np.kron(P, P) for P in projectors) / m0
w = bases[0][:, 0]
P_w = np.outer(w, w.conj())
kept = projectors[1:]
Fprime = sum(np.kron(P, P) for P in kept) / (m0 - 1)

# Quartic maximum witness: x is orthogonal to the deleted basis vector.
x = bases[0][:, 1]
qprime_x = sum(abs(np.vdot(b[:, k], x)) ** 4 for b in bases for k in range(d) if not np.allclose(b[:, k], w))

# Lower-constant witness (the source formula minimizes this over orthogonal u,v).
e = bases[0][:, 1]
u, v = (w + e) / np.sqrt(2), (w - e) / np.sqrt(2)
full_lower_sq = sum(np.real(np.vdot(u, P @ v)) ** 2 for P in projectors)
removed_sq = np.real(np.vdot(u, P_w @ v)) ** 2
kept_lower_sq = full_lower_sq - removed_sq

# Real span of Hermitian measurement projectors; rank d^2 means informationally complete.
coords = np.stack([np.concatenate([P.real.ravel(), P.imag.ravel()]) for P in kept])
span_rank = np.linalg.matrix_rank(coords, tol=1e-9)
expected_sq_error = (1 - 1 / N) / (m0 - 1) ** 2
actual_sq_error = np.linalg.norm(Fprime - F0, "fro") ** 2

print(f"d={d}, m_full={m0}, m_deleted={m0-1}")
print(f"full_moment_max_abs_error={np.max(np.abs(Ffull-F0)):.3e}")
print(f"deleted_moment_sq_error={actual_sq_error:.12g}, formula={expected_sq_error:.12g}")
print(f"deleted_relative_moment_error={np.linalg.norm(Fprime-F0,'fro')/np.linalg.norm(F0,'fro'):.12g}")
print(f"qprime_witness={qprime_x:.12g} (theoretical max 2)")
print(f"lower_full={full_lower_sq:.12g}, removed={removed_sq:.12g}, kept_witness={kept_lower_sq:.12g}")
print(f"retained_Hermitian_span_rank={span_rank}, expected={d*d}")

assert np.max(np.abs(Ffull - F0)) < 1e-12
assert abs(actual_sq_error - expected_sq_error) < 1e-12
assert abs(qprime_x - 2) < 1e-12
assert abs(full_lower_sq - 0.5) < 1e-12
assert abs(removed_sq - 0.25) < 1e-12
assert abs(kept_lower_sq - 0.25) < 1e-12
assert span_rank == d * d
