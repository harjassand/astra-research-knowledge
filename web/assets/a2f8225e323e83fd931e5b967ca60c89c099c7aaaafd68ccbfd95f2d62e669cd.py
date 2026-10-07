"""Deterministic finite diagnostic for canonical-sector log-concavity.

Uses n=8 sector matrices only. This is numerical evidence, not a theorem,
not a counterexample certificate, and not an FPRAS execution.
"""
import json
import math
from pathlib import Path
import numpy as np


def logsumexp(values):
    m = float(max(values))
    return m + math.log(sum(math.exp(float(x) - m) for x in values))


def sector_logs(n, edges, alpha, gamma, beta, fields):
    logs = []
    for particle_count in range(n + 1):
        masks = [s for s in range(1 << n) if s.bit_count() == particle_count]
        index = {s: i for i, s in enumerate(masks)}
        H = np.zeros((len(masks), len(masks)))
        for a, s in enumerate(masks):
            z = [1 - 2 * ((s >> i) & 1) for i in range(n)]
            H[a, a] = sum(fields[i] * z[i] for i in range(n))
            for (i, j), aa, gg in zip(edges, alpha, gamma):
                H[a, a] += gg * z[i] * z[j]
                if ((s >> i) & 1) != ((s >> j) & 1):
                    H[a, index[s ^ (1 << i) ^ (1 << j)]] += 2 * aa
        logs.append(logsumexp(beta * np.linalg.eigvalsh(H)))
    return logs


def main():
    rng = np.random.default_rng(777)
    n = 8
    all_edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    densities = [0.15, 0.4, 0.8, 1.0]
    ratios = [-1, -0.9, -0.5, 0, 0.5, 0.9, 1]
    alpha_choices = [0.1, 1, 5]
    field_choices = [-5, -2, -1, 0, 1, 2, 5]
    betas = [0.1, 1, 10, 100]
    count = 0
    minimum = float("inf")
    min_case = None
    violation = None
    instances = 1000
    for trial in range(instances):
        density = float(rng.choice(densities))
        edges = [e for e in all_edges if rng.random() < density]
        if not edges:
            continue
        alpha = rng.choice(alpha_choices, size=len(edges))
        gamma = alpha * rng.choice(ratios, size=len(edges))
        fields = rng.choice(field_choices, size=n)
        for beta in betas:
            L = sector_logs(n, edges, alpha, gamma, beta, fields)
            for m in range(1, n):
                margin = 2 * L[m] - L[m - 1] - L[m + 1]
                count += 1
                if margin < minimum:
                    minimum = float(margin)
                    min_case = {
                        "trial": trial,
                        "density_parameter": density,
                        "beta": beta,
                        "sector": m,
                        "edges": edges,
                        "alpha": alpha.tolist(),
                        "gamma": gamma.tolist(),
                        "fields": fields.tolist(),
                    }
                if margin < -1e-7 and violation is None:
                    violation = {"margin": float(margin), **min_case}
    result = {
        "status": "FINITE_NUMERICAL_DIAGNOSTIC_ONLY",
        "seed": 777,
        "n": n,
        "instances": instances,
        "densities": densities,
        "beta_values": betas,
        "alpha_values": alpha_choices,
        "gamma_over_alpha_values": ratios,
        "field_values": field_choices,
        "checks": count,
        "minimum_log_concavity_margin": minimum,
        "minimum_case": min_case,
        "violation_below_minus_1e-7": violation,
        "scope": "float eigensolver, finite n only; no proof and no canonical algorithm",
    }
    target = Path(__file__).with_name("canonical_sector_search.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
