#!/usr/bin/env python3
"""Sanity check: a positive two-hidden-state binary HMM, observed paths only."""
import itertools
import numpy as np

T = np.array([[0.82, 0.18], [0.27, 0.73]], dtype=float)
# Rows are hidden states; columns are emitted symbols 0 and 1.
E = np.array([[0.78, 0.22], [0.19, 0.81]], dtype=float)
# Solve the stationary equations together with normalization by least squares.
pi = np.linalg.lstsq(np.vstack([T.T - np.eye(2), np.ones(2)]), np.array([0.0, 0.0, 1.0]), rcond=None)[0]
assert np.allclose(pi @ T, pi)

A = [np.diag(E[:, x]) @ T for x in range(2)]
def f(word):
    z = pi.copy()
    for x in word:
        z = z @ A[x]
    return float(z @ np.ones(2))

def words(depth):
    return [w for h in range(depth + 1) for w in itertools.product(range(2), repeat=h)]

k = ell = 2
P = words(k)
S = words(ell)
H = np.array([[f(u + v) for v in S] for u in P])
sigma = np.linalg.svd(H, compute_uv=False)
rank = int(np.sum(sigma > 1e-10))
assert rank == 2, (rank, sigma)

# Simulate only emitted strings. The estimator below sees no hidden-state path.
rng = np.random.default_rng(20261008)
N = 100_000
L = k + ell
obs = []
for _ in range(N):
    state = int(rng.choice(2, p=pi))  # independent stationary reset
    x = []
    for _t in range(L):
        x.append(int(rng.choice(2, p=E[state])))
        state = int(rng.choice(2, p=T[state]))
    obs.append(tuple(x))

counts = {w: 0 for w in words(L)}
for path in obs:
    for h in range(L + 1):
        counts[path[:h]] += 1
fhat = {w: counts[w] / N for w in counts}
Hhat = np.array([[fhat[u + v] for v in S] for u in P])
max_word_error = max(abs(fhat[w] - f(w)) for w in counts)
print(f"alphabet=2, state cap=2, k=ell=2, L={L}, D_L={len(counts)}, N={N}")
print(f"population singular values={sigma}")
print(f"population rank={rank}; empirical singular values={np.linalg.svd(Hhat, compute_uv=False)}")
print(f"max raw-word frequency error={max_word_error:.6g}")
