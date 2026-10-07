"""Arithmetic diagnostics for report.md; not a proof of the theorem."""
import json
from pathlib import Path

import numpy as np
import sympy as sp


r = sp.symbols("r", positive=True)
m, u = sp.symbols("m u", real=True)
F_m, F_u = sp.sqrt(r * r + m * m), sp.sqrt(r * r + u * u)
regret = F_m - F_u - (m - u) * u / F_u
chord = F_m / 2 * (
    (r / F_m - r / F_u) ** 2 + (m / F_m - u / F_u) ** 2
)
score_plus = -(r * r + u) / F_u
score_derivative = r * r * (u - 1) / (r * r + u * u) ** sp.Rational(3, 2)

assert sp.simplify(regret - chord) == 0
assert sp.simplify(sp.diff(score_plus, u) - score_derivative) == 0
assert sp.simplify(score_plus.subs(u, -1) - score_plus.subs(u, 1)
                   - 2 / sp.sqrt(1 + r * r)) == 0

# Calibrated-score appendix: inverse derivative and exact r=1 losses.
v, p, q = sp.symbols("v p q", real=True)
posterior_inverse = (1 + sp.tanh(r * sp.atanh(v))) / 2
posterior_inverse_derivative = (
    r / (2 * (1 - v * v) * sp.cosh(r * sp.atanh(v)) ** 2)
)
assert sp.simplify(sp.diff(posterior_inverse, v)
                   - posterior_inverse_derivative) == 0
F_brier = (q - sp.Rational(1, 2)) ** 2
loss_zero_brier = sp.Rational(1, 4) - F_brier + q * (2 * q - 1)
loss_one_brier = sp.Rational(1, 4) - F_brier - (1 - q) * (2 * q - 1)
assert sp.simplify(loss_zero_brier - q * q) == 0
assert sp.simplify(loss_one_brier - (1 - q) ** 2) == 0

nodes, weights = np.polynomial.hermite.hermgauss(200)
gaussian_nodes, gaussian_weights = np.sqrt(2) * nodes, weights / np.sqrt(np.pi)
gaussian_entropy = 0.5 * np.log(2 * np.pi * np.e)
entropy_lower = gaussian_entropy - 1 - 1.5 * np.log(2)
rows = []
for signal in [1.0, 0.5, 0.1, 0.01, 1e-4, 1e-8]:
    x = gaussian_nodes
    t = np.tanh(signal * x)
    log_cosh = np.logaddexp(signal * x, -signal * x) - np.log(2)
    log_derivative = -2 * log_cosh - 1.5 * np.log1p((t / signal) ** 2)
    entropy = gaussian_entropy + float(gaussian_weights @ log_derivative)
    kappa = 4 * np.exp(signal * signal / 2) / np.sqrt(1 + signal * signal)
    assert entropy >= entropy_lower - 1e-10
    assert kappa <= 2 * np.sqrt(2 * np.e) + 1e-12
    rows.append({"r": signal, "entropy_quadrature": entropy, "kappa": kappa})

constant_nats = 1.25 + 2.25 * np.log(2)
calibrated_constant_nats = 1.25 + np.log(2)
query_margin = 0.5 * np.log(128) - calibrated_constant_nats
result = {
    "symbolic_chord_identity": True,
    "symbolic_loss_derivative": True,
    "symbolic_loss_oscillation": True,
    "uniform_entropy_lower_nats": entropy_lower,
    "additive_constant_nats_per_coordinate": constant_nats,
    "additive_constant_bits_per_coordinate": constant_nats / np.log(2),
    "epsilon_over_r_sufficient_for_quarter_log_lower": np.exp(-4 * constant_nats),
    "scalar_quadratures": rows,
    "calibrated_inverse_derivative_symbolic": True,
    "calibrated_r_equals_one_brier_losses_symbolic": True,
    "calibrated_constant_nats_per_coordinate": calibrated_constant_nats,
    "calibrated_constant_bits_per_coordinate": calibrated_constant_nats / np.log(2),
    "query_r_equals_128_epsilon_nats_per_coordinate": query_margin,
    "scope": "symbolic algebra and scalar quadrature only; theorem is in report.md",
}
Path(__file__).with_name("checks.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
