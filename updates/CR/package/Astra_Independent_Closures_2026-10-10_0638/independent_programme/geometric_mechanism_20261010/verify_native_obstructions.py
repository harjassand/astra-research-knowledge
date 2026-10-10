"""Reproducible modest-CPU checks accompanying exact proofs.

The symbolic assertions are exact. Monte Carlo output is only an implementation
cross-check and is not the mathematical evidence for the stated inequalities.
Run: python verify_native_obstructions.py
"""
from pathlib import Path
import json
import math
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent
rng = np.random.default_rng(20261010)

# Exact random-scan block calculation; never interpreted as a full-sweep gap.
a, b, m = sp.symbols("a b m", positive=True)
r = m / (m + 2)
pf = (r - (r + 1) * b + (r + 1) * a - r) / 2
assert sp.simplify(pf - (m + 1) / (m + 2) * (a - b)) == 0

# Exact Stein identity for the rank-one tangential Gaussian kernel.
x, y, eps = sp.symbols("x y eps", real=True)
rho = sp.exp(-(x * x + y * y) / 2)
tau = sp.Matrix([[y * y, -x * y], [-x * y, x * x]])
for i, z in enumerate([x, y]):
    div = sum(sp.diff(rho * tau[i, j], w) for j, w in enumerate([x, y]))
    assert sp.simplify(div + z * rho) == 0
assert sp.simplify((sp.Matrix([2*x, 2*y]).T * tau * sp.Matrix([2*x, 2*y]))[0]) == 0

# Exact exponential test-function Rayleigh quotient.
alpha = sp.symbols("alpha", positive=True)
ratio = (1/(1-2*alpha)-1/(1-alpha)**2)/(alpha**2/(1-2*alpha))
assert sp.simplify(ratio - 1/(1-alpha)**2) == 0

out = {"seed": 20261010, "symbolic_assertions": 5,
       "status": "Exact symbolic identities passed; simulations are checks only.",
       "simplex": [], "block_ball": [], "stein_maxima": [], "square_clock": []}

for n in [1, 2, 4, 8, 16, 32, 64]:
    N = n + 1
    samples = 12000
    g = rng.normal(size=(samples, N))
    g -= g.mean(axis=1, keepdims=True)
    u = g / np.linalg.norm(g, axis=1, keepdims=True)
    l1 = np.abs(u).sum(axis=1)
    dir_rq = 2 / n * np.mean(1 / l1**2)
    lower, upper = 2 / (n*N), 6 / (N*(n+2))
    assert lower - 1e-12 <= dir_rq <= upper + 1e-12
    p = rng.exponential(size=(samples, N))
    p /= p.sum(axis=1, keepdims=True)
    plus = np.min(np.where(u < 0, p / np.where(u < 0, -u, 1), np.inf), axis=1)
    minus = np.min(np.where(u > 0, p / np.where(u > 0, u, 1), np.inf), axis=1)
    chord_variance = N*(N+1)*(plus+minus)**2/12
    predicted_variance = 2/l1**2
    out["simplex"].append({"dimension": n, "linear_rq_direction_mc": float(dir_rq),
        "exact_lower": lower, "exact_upper": upper,
        "n_squared_times_rq_mc": float(n*n*dir_rq),
        "mean_chord_variance_mc": float(chord_variance.mean()),
        "predicted_mean_chord_variance_mc": float(predicted_variance.mean())})

for m0 in [1, 2, 4, 16, 64, 256]:
    out["block_ball"].append({"dimension": 2*m0, "operator": "random-scan (P_X+P_Y)/2",
        "linear_rayleigh_quotient": 0.5, "quadratic_eigen_gap": 1/(m0+2),
        "quadratic_to_linear_ratio": 2/(m0+2)})

for n in [1, 2, 8, 32, 128, 512]:
    maxes = rng.exponential(size=(8000, n)).max(axis=1)
    hn = sum(1/k for k in range(1, n+1))
    hn2 = sum(1/(k*k) for k in range(1, n+1))
    out["stein_maxima"].append({"dimension": n, "norm_of_mean_tau_squared_exact": 2,
        "mean_norm_tau_exact": hn, "mean_norm_tau_mc": float(maxes.mean()),
        "mean_norm_tau_squared_exact": hn*hn+hn2,
        "mean_norm_tau_squared_mc": float(np.mean(maxes*maxes))})

# At direction (1,1)/sqrt(2), chop off projected distance epsilon from corners.
# The exact stationary truncated mean rate is 3 log(sqrt(2)/epsilon).
for e in [1e-1, 1e-2, 1e-4, 1e-8, 1e-16]:
    out["square_clock"].append({"corner_cutoff": e,
        "exact_truncated_stationary_rate": 3*math.log(math.sqrt(2)/e)})

out["padded_exponential_entropy"] = 0.5*math.log(2*math.pi)-0.5
out["exponential_poincare_lower_bound"] = 4
out["numpy_version"] = np.__version__
out["sympy_version"] = sp.__version__
target = ROOT / "native_checks.json"
target.write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps({"saved": str(target), "symbolic_assertions": out["symbolic_assertions"],
                  "simplex_dimension_64": out["simplex"][-1],
                  "status": out["status"]}, indent=2))
