"""Finite diagnostic: SVD-gauge operators can be signed for a valid HMM.

This is a reproducibility check, not a proof of the general theorem. Requires numpy.
"""
from itertools import product
import json
import numpy as np

P = np.array([[4 / 5, 1 / 5], [3 / 10, 7 / 10]], dtype=float)
pi = np.array([3 / 5, 2 / 5], dtype=float)
M = {0: np.diag([1.0, 0.0]) @ P, 1: np.diag([0.0, 1.0]) @ P}
ones = np.ones(2)
words = [(), (0,), (1,)]


def prob(word):
    row = pi.copy()
    for a in word:
        row = row @ M[a]
    return float(row @ ones)


H = np.array([[prob(u + v) for v in words] for u in words])
Ha = {
    a: np.array([[prob(u + (a,) + v) for v in words] for u in words])
    for a in (0, 1)
}

U, singular, Vt = np.linalg.svd(H, full_matrices=False)
rank = 2
U_r = U[:, :rank]
V_r = Vt[:rank, :].T
singular_r = singular[:rank]
B = U_r @ np.diag(singular_r)
B_plus = np.linalg.pinv(B)
alpha = H[0, :] @ V_r
beta = B_plus @ H[:, 0]
A = {a: B_plus @ Ha[a] @ V_r for a in (0, 1)}

max_prediction_error = 0.0
for length in range(7):
    for word in product((0, 1), repeat=length):
        predicted = alpha.copy()
        for a in word:
            predicted = predicted @ A[a]
        predicted = float(predicted @ beta)
        max_prediction_error = max(max_prediction_error, abs(predicted - prob(word)))

result = {
    "stationary_distribution_check": (pi @ P).tolist(),
    "H": H.tolist(),
    "singular_values": singular.tolist(),
    "selected_rank": rank,
    "A0": A[0].tolist(),
    "A1": A[1].tolist(),
    "min_A1_entry": float(A[1].min()),
    "alpha_beta": float(alpha @ beta),
    "normalization_residual_l2": float(np.linalg.norm((A[0] + A[1]) @ beta - beta)),
    "max_prediction_error_lengths_0_to_6": max_prediction_error,
    "status": "FINITE_NUMERICAL_DIAGNOSTIC_ONLY",
}
print(json.dumps(result, indent=2))
assert np.linalg.matrix_rank(H, tol=1e-10) == 2
assert A[1].min() < -1e-3
assert max_prediction_error < 1e-10
assert abs(float(alpha @ beta) - 1.0) < 1e-10
assert np.linalg.norm((A[0] + A[1]) @ beta - beta) < 1e-10

