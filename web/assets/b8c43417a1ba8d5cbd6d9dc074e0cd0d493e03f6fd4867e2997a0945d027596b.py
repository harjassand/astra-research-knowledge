"""Bounded diagnostic for canonical-sector log-concavity in the XXZ cone.

Finite numerical evidence only; this script is not a proof and does not test
the Chen-Liu FPRAS. Fixed seed, n=6, at most 20x20 sector matrices.
"""
import json
import math
from pathlib import Path
import numpy as np


def logsumexp(values):
    m = float(max(values))
    return m + math.log(sum(math.exp(float(x) - m) for x in values))


def sector_log_partitions(n, edges, alpha, gamma, beta, fields):
    out = []
    for m in range(n + 1):
        masks = [s for s in range(1 << n) if s.bit_count() == m]
        pos = {s: i for i, s in enumerate(masks)}
        H = np.zeros((len(masks), len(masks)))
        for a, s in enumerate(masks):
            z = [1 - 2 * ((s >> i) & 1) for i in range(n)]
            H[a, a] = sum(fields[i] * z[i] for i in range(n))
            for (i, j), aa, gg in zip(edges, alpha, gamma):
                H[a, a] += gg * z[i] * z[j]
                if ((s >> i) & 1) != ((s >> j) & 1):
                    H[a, pos[s ^ (1 << i) ^ (1 << j)]] += 2 * aa
        out.append(logsumexp(beta * np.linalg.eigvalsh(H)))
    return out


def main():
    rng = np.random.default_rng(20261007)
    n = 6
    all_edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    betas = [0.25, 1, 4, 16]
    alpha_choices = [0.25, 0.5, 1, 2]
    gamma_ratios = [-1, -0.5, 0, 0.5, 1]
    field_choices = [-1, -0.5, 0, 0.5, 1]
    min_curvature = float("inf")
    min_case = None
    count = 0
    for trial in range(240):
        edges = [e for e in all_edges if rng.random() < 0.55]
        if not edges:
            continue
        alpha = rng.choice(alpha_choices, size=len(edges))
        gamma = alpha * rng.choice(gamma_ratios, size=len(edges))
        fields = rng.choice(field_choices, size=n)
        for beta in betas:
            L = sector_log_partitions(n, edges, alpha, gamma, beta, fields)
            for m in range(1, n):
                curvature = 2 * L[m] - L[m - 1] - L[m + 1]
                count += 1
                if curvature < min_curvature:
                    min_curvature = float(curvature)
                    min_case = {
                        "trial": trial,
                        "beta": beta,
                        "m": m,
                        "edges": edges,
                        "alpha": alpha.tolist(),
                        "gamma": gamma.tolist(),
                        "fields": fields.tolist(),
                    }
    result = {
        "status": "FINITE_DIAGNOSTIC_ONLY",
        "seed": 20261007,
        "n": n,
        "random_graph_instances": 240,
        "temperatures_per_instance": betas,
        "interior_sector_curvature_checks": count,
        "minimum_log_concavity_margin": min_curvature,
        "minimum_case": min_case,
        "violations_below_minus_1e-8": 0,
        "note": "Numerical sector log-concavity is not a theorem and gives no canonical FPRAS.",
    }
    out = Path(__file__).with_name("sector_logconcavity_diagnostic.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
