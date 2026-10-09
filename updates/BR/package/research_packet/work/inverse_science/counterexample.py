"""Prior-mismatch sensing counterexample and exact finite audit accounting.
Standard-library-only, deterministic. No trained diffusion model is involved.
The diagonal Gaussian prior isolates posterior-variance acquisition itself.
"""
from itertools import combinations
from math import comb, log
import json
from pathlib import Path

n = 16
amplitude = 1.0
true_signal = [0.0] * (n - 1) + [amplitude]
prior_mean = [0.0] * n
prior_var = [1.0] * (n - 1) + [0.0]
measurements = []
for _ in range(n - 1):
    j = max(range(n), key=prior_var.__getitem__)
    y = true_signal[j]
    measurements.append((j, y))
    prior_mean[j] = y
    prior_var[j] = 0.0
sq_error = sum((x - xhat) ** 2 for x, xhat in zip(true_signal, prior_mean))
residual_sq = sum((prior_mean[j] - y) ** 2 for j, y in measurements)

# Enumerate all uniform distinct-coordinate audit designs for a frozen estimate.
# These are replacement audits from the entire n-coordinate family, so the
# accounting is transparent; re-measuring an already observed coordinate is wasted.
audit = []
for q in [1, 2, 4, 8, 12, 15, 16]:
    misses = sum(n - 1 not in subset for subset in combinations(range(n), q))
    total = comb(n, q)
    audit.append({"q": q, "misses": misses, "designs": total,
                  "miss_probability": misses / total,
                  "exact_miss_probability": 1 - q / n})

# Exact information-theoretic necessary budget, not a measured experiment.
delta = 0.05
sigma = 1.0
binary_kl = (1 - 2 * delta) * log((1 - delta) / delta)
energy_lower_bound = 2 * n * sigma**2 / amplitude**2 * binary_kl
out = {
    "status": "finite_counterexample_and_analytical_costs_only",
    "n": n, "queries": len(measurements),
    "queried_coordinates_zero_based": [j for j, _ in measurements],
    "learned_prior_posterior_trace": sum(prior_var),
    "observed_residual_squared": residual_sq,
    "actual_reconstruction_error_squared": sq_error,
    "uniform_coordinate_audit": audit,
    "unit_energy_noisy_detection_lower_bound": {
        "delta": delta, "sigma": sigma, "amplitude": amplitude,
        "binary_kl": binary_kl, "necessary_expected_energy": energy_lower_bound
    },
    "limitations": [
        "No realistic scan, diffusion model, or image dataset is evaluated.",
        "The Gaussian prior is deliberately misspecified to isolate the mechanism.",
        "Enumeration validates arithmetic only; the mathematical proof is in result.txt."
    ]
}
path = Path(__file__).with_name("counterexample_results.json")
path.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
