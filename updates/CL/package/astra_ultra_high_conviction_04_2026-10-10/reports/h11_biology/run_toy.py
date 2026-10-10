#!/usr/bin/env python3
"""Finite check for the sparse-Walsh panel and a viable-domain alias."""
from itertools import combinations
import json
import math
from pathlib import Path

import numpy as np

SEED = 20261010
N = 100
D = 2
SPARSITY = 2
DELTA = 0.05
TAU = 1 / (2 * SPARSITY)

# Draw actual genotype assays from the uniform binary cube.
rng = np.random.default_rng(SEED)
M = sum(math.comb(N, k) for k in range(D + 1))
m = math.ceil(2 * TAU**-2 * math.log(M * (M - 1) / DELTA))
z = rng.integers(0, 2, size=(m, N), dtype=np.int8) * 2 - 1

# Materialize the degree-at-most-two Walsh dictionary.
columns = [np.ones(m, dtype=np.int8)]
columns.extend(z[:, i] for i in range(N))
columns.extend(z[:, i] * z[:, j] for i, j in combinations(range(N), 2))
X = np.column_stack(columns).astype(np.float64)
A = X / math.sqrt(m)

# The realized maximum column coherence is the event used by the proof.
G = A.T @ A
np.fill_diagonal(G, 0.0)
coherence = float(np.max(np.abs(G)))

# A fixed, two-term exact phenotype; OMP should recover its support.
true_support = np.array([7, M - 17], dtype=np.int64)
true_coefficients = np.array([1.25, -0.75], dtype=np.float64)
y = A[:, true_support] @ true_coefficients
selected = []
residual = y.copy()
for _ in range(SPARSITY):
    corr = A.T @ residual
    corr[selected] = 0.0
    selected.append(int(np.argmax(np.abs(corr))))
    fitted, *_ = np.linalg.lstsq(A[:, selected], y, rcond=None)
    residual = y - A[:, selected] @ fitted

# Exact restricted-domain alias: V is WT plus every single mutant in three loci.
# Features 1 + z1*z2 and z1 + z2 are two-term models agreeing on all of V.
V = np.array([[1, 1, 1], [-1, 1, 1], [1, -1, 1], [1, 1, -1]], dtype=np.int8)
left = 1 + V[:, 0] * V[:, 1]
right = V[:, 0] + V[:, 1]
assert np.array_equal(left, right)
double_mutant = np.array([-1, -1, 1], dtype=np.int8)
left_unseen = int(1 + double_mutant[0] * double_mutant[1])
right_unseen = int(double_mutant[0] + double_mutant[1])
assert left_unseen != right_unseen

result = {
    "seed": SEED,
    "n": N,
    "degree": D,
    "sparsity": SPARSITY,
    "features": M,
    "delta": DELTA,
    "coherence_threshold": TAU,
    "assays": m,
    "realized_max_coherence": coherence,
    "coherence_event_passed": coherence < TAU,
    "true_support": true_support.tolist(),
    "omp_support": sorted(selected),
    "true_coefficients": true_coefficients.tolist(),
    "omp_coefficients_in_selected_order": fitted.tolist(),
    "omp_residual_norm": float(np.linalg.norm(residual)),
    "omp_exact_support_recovered": sorted(selected) == sorted(true_support.tolist()),
    "viable_domain": V.tolist(),
    "viable_left_values": left.tolist(),
    "viable_right_values": right.tolist(),
    "unseen_double_mutant": double_mutant.tolist(),
    "left_unseen_value": left_unseen,
    "right_unseen_value": right_unseen,
}
out_path = Path(__file__).with_name("toy_result.json")
out_path.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
