"""Finite algebra diagnostics; the analytic sign-sector proof is independent."""
from pathlib import Path
import json
import numpy as np

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)

def kron_all(items):
    out = np.ones((1, 1), dtype=complex)
    for item in items:
        out = np.kron(out, item)
    return out

def clifford(k):
    n = max(1, k // 2)
    out = []
    for j in range(n):
        out.append(kron_all([Z] * j + [X] + [I2] * (n - j - 1)))
        out.append(kron_all([Z] * j + [Y] + [I2] * (n - j - 1)))
    out.append(kron_all([Z] * n))
    return out[:k]

def star(gens, weights):
    ident = np.eye(gens[0].shape[0])
    return sum(w * np.kron(g.T, np.kron(g, ident) + np.kron(ident, g))
               for g, w in zip(gens, weights))

results = []
rng = np.random.default_rng(191003)
for k in range(1, 8):
    gens = clifford(k)
    d = gens[0].shape[0]
    actual = np.max(np.abs(np.linalg.eigvalsh(star(gens, np.ones(k)))))
    bound = k + 1 if k % 2 else np.sqrt(k * (k + 2))
    weights = rng.uniform(0, 2, k)
    actual_w = np.max(np.abs(np.linalg.eigvalsh(star(gens, weights))))
    bound_w = weights.sum() + weights.max()
    row = {"k": k, "d": d, "norm": float(actual), "bound": float(bound),
           "weighted_norm": float(actual_w), "weighted_bound": float(bound_w),
           "pass": bool(actual <= bound + 1e-10 and actual_w <= bound_w + 1e-10)}
    results.append(row)
    print(json.dumps(row), flush=True)

Path(__file__).with_name("clifford_norm_diagnostics.json").write_text(
    json.dumps({"status": "finite_diagnostic_only", "seed": 191003,
                "rows": results}, indent=2) + "\n")
assert all(r["pass"] for r in results)
