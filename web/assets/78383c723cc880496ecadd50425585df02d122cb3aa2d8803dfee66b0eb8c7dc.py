"""Finite floating checks for the qutrit vacuum-detector example.

The note energy.md contains the proofs. These checks are not an asymptotic proof
or an interval certificate. Requires only Python and numpy.
"""
import json
import math
from pathlib import Path

import numpy as np


def golden_max(f, lo, hi, iterations=150):
    r = (math.sqrt(5) - 1) / 2
    x1, x2 = hi - r * (hi - lo), lo + r * (hi - lo)
    f1, f2 = f(x1), f(x2)
    for _ in range(iterations):
        if f1 < f2:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + r * (hi - lo)
            f2 = f(x2)
        else:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - r * (hi - lo)
            f1 = f(x1)
    x = (lo + hi) / 2
    return x, f(x)


def logsumexp(x):
    a = float(np.max(x))
    return a + math.log(float(np.exp(x - a).sum()))


A = np.array([[2.0, 1.0], [1.0, 2.0]])
H = np.diag([1.0, 4.0])
alpha = (5 + math.sqrt(13)) / 4
ratio = alpha - 2
psi = np.array([1.0, ratio]) / math.sqrt(1 + ratio**2)
mean_a = float(psi @ A @ psi)
mean_h = float(psi @ H @ psi)
U = np.array([[1.0, 1.0], [-1.0, 1.0]]) / math.sqrt(2)
u, v = U.T @ psi
p = float(v * v)
E = U @ np.diag(np.exp(-np.array([1.0, 3.0]))) @ U.T


def product_exponent(theta, strength=1.0):
    survival = math.exp(-2 * strength) * (
        math.cosh(strength) - math.sinh(strength) * math.sin(2 * theta)
    )
    energy = 1 + 3 * math.sin(theta)**2
    return -math.log(survival) / energy


# Full scan brackets each local maximum. The strict gap itself is proved in the
# note by the equality cases of Jensen and the generalized Rayleigh quotient.
grid = np.linspace(0, math.pi / 2, 20001)
vals = np.array([product_exponent(float(t)) for t in grid])
local = [i for i in range(1, len(grid) - 1)
         if vals[i] >= vals[i-1] and vals[i] >= vals[i+1]]
solutions = [golden_max(product_exponent, float(grid[i-1]), float(grid[i+1]))
             for i in local]
solutions += [(0.0, product_exponent(0.0)),
              (math.pi/2, product_exponent(math.pi/2))]
theta_star, beta = max(solutions, key=lambda x: x[1])


def projected_block(m):
    delta = 0.25 * m**(-0.25)
    cutoff = max(0, math.ceil(m * (p - delta)))
    k = np.arange(m + 1)
    log_probs = np.array([
        math.lgamma(m + 1) - math.lgamma(int(j) + 1)
        - math.lgamma(m - int(j) + 1)
        + (m - int(j)) * math.log(1-p) + int(j) * math.log(p)
        for j in k
    ])
    log_z = logsumexp(log_probs[cutoff:])
    c = np.zeros(m + 1)
    c[cutoff:] = np.exp(0.5 * (log_probs[cutoff:] - log_z))
    energy = 2.5*m - 3*float(np.sum(
        c[:-1] * c[1:] * np.sqrt((k[:-1]+1)*(m-k[:-1]))))
    log_survival = logsumexp(
        log_probs[cutoff:] - (m + 2*k[cutoff:])) - log_z
    return {
        "m": m,
        "delta": delta,
        "cutoff": cutoff,
        "projection_success": math.exp(log_z),
        "cost_per_cell": energy/m,
        "minus_log_survival_per_energy": -log_survival/energy,
        "beats_fully_separable_bound": -log_survival/energy > beta,
        "jensen_converse_slack": alpha*energy + log_survival,
        "cutoff_survival_bound_slack": -log_survival - (m+2*cutoff),
    }


weak = []
for t in [1.0, 0.3, 0.1, 0.03, 0.01]:
    g = np.array([product_exponent(float(th), t) for th in grid])
    i = int(np.argmax(g))
    _, b = golden_max(lambda th: product_exponent(th, t),
                      float(grid[max(0, i-1)]), float(grid[min(len(grid)-1, i+1)]))
    weak.append({"strength": t, "regularized": t*alpha,
                 "product": b, "gap_over_t_squared": (t*alpha-b)/t**2})

result = {
    "scope": "Finite floating checks, not interval or asymptotic certification",
    "A": A.tolist(), "H": H.tolist(), "E": E.tolist(),
    "alpha_exact": "(5+sqrt(13))/4", "alpha": alpha,
    "generalized_eigenvector": psi.tolist(),
    "a": mean_a, "h": mean_h, "p_A_eigenvalue_3": p,
    "product_maximizer_angle": theta_star, "beta_numeric": beta,
    "relative_exponent_gain": alpha/beta-1,
    "weak_strength_checks": weak,
    "blocks": [projected_block(m) for m in
               [16, 64, 256, 1024, 4096, 16384, 65536]],
}

assert abs(mean_a / mean_h - alpha) < 1e-12
assert alpha > beta + 0.05
assert np.linalg.norm(A @ psi - alpha * H @ psi) < 1e-12
for block in result["blocks"]:
    assert block["jensen_converse_slack"] > -1e-7
    assert block["cutoff_survival_bound_slack"] > -1e-7
assert result["blocks"][-1]["beats_fully_separable_bound"]

path = Path(__file__).with_name("energy_probe.json")
path.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
