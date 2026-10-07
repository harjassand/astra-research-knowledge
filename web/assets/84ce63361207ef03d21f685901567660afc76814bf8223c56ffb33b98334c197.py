"""Finite coefficient sanity checks, not a theorem or novelty certification."""
from math import exp, lgamma, log
from pathlib import Path
import json

rows = []
for n in (64, 256, 1024, 4096, 16384):
    jvals = range(n // 2 + 1)
    exact_logs, quartic_logs = [], []
    for j in jvals:
        k = j + 0.5
        exact_logs.append(
            log(4 * k * k / (n + 1)) + lgamma(n + 2)
            - lgamma((n + 1) / 2 - k + 1)
            - lgamma((n + 1) / 2 + k + 1)
            + 2 * j * (j + 1) / n
        )
        r = k / n ** 0.75
        quartic_logs.append(log(r * r) - 4 * r ** 4 / 3)

    def normalize(logs):
        pivot = max(logs)
        masses = [exp(value - pivot) for value in logs]
        total = sum(masses)
        return [value / total for value in masses]

    q, p = normalize(exact_logs), normalize(quartic_logs)
    tv = 0.5 * sum(abs(x - y) for x, y in zip(q, p))
    mean_radius = sum(qj * (j + 0.5) / n ** 0.75 for j, qj in zip(jvals, q))
    rows.append({
        "N": n,
        "sector_TV_to_quartic_grid": tv,
        "sqrt_N_times_TV": n ** 0.5 * tv,
        "mean_scaled_Weyl_radius": mean_radius,
    })

result = {
    "scope": "Finite sanity check of critical spin-sector coefficient; not a proof or novelty check.",
    "results": rows,
}
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
