#!/usr/bin/env python3
"""Exact finite-copy neutral Moran calculation for mtDNA turnover.

This is a scoped mathematical model, not a biological simulator. It treats a
postmitotic cell as N exchangeable mtDNA copies with genotype-blind replacement.
"""
from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from typing import Any


def hit_probability_before_loss(initial_k: int, threshold_m: int) -> Fraction:
    """Exact neutral Moran probability to hit m before extinction at 0."""
    if threshold_m <= 0 or initial_k < 0 or initial_k > threshold_m:
        raise ValueError("require 0 <= initial_k <= threshold_m and m > 0")
    return Fraction(initial_k, threshold_m)


def neutral_moran_hit_by_time(
    *, population_size: int, initial_k: int, threshold_m: int,
    turnover_cycles_per_year: float, horizon_years: float,
) -> float:
    """Uniformized CTMC probability of hitting m by T under neutral turnover.

    One turnover cycle is N replacement attempts, so attempts form a Poisson
    process with mean N * turnover_cycles_per_year * horizon_years. A Moran
    attempt chooses a parent and a removed copy independently and uniformly.
    States 0 and m are absorbing for the threshold-hitting calculation.
    """
    n = population_size
    m = threshold_m
    k0 = initial_k
    rho = turnover_cycles_per_year
    horizon = horizon_years
    if n < 2 or not (0 <= k0 <= m <= n) or m == 0:
        raise ValueError("require N >= 2 and 0 <= k <= m <= N, m > 0")
    if rho < 0 or horizon < 0:
        raise ValueError("turnover and horizon must be nonnegative")
    if k0 == 0:
        return 0.0
    if k0 >= m or horizon == 0:
        return float(k0 >= m)
    mean_steps = n * rho * horizon
    if mean_steps == 0:
        return 0.0

    # Truncate only the Poisson tails (12 standard deviations); renormalize the
    # retained weights. For the finite examples below the omitted mass is tiny.
    radius = 12.0 * math.sqrt(mean_steps) + 20.0
    lo = max(0, int(mean_steps - radius))
    hi = int(mean_steps + radius) + 1
    mode = int(mean_steps)
    log_w_mode = -mean_steps + mode * math.log(mean_steps) - math.lgamma(mode + 1)
    weights: dict[int, float] = {mode: math.exp(log_w_mode)}
    for j in range(mode + 1, hi + 1):
        weights[j] = weights[j - 1] * mean_steps / j
    for j in range(mode - 1, lo - 1, -1):
        weights[j] = weights[j + 1] * (j + 1) / mean_steps
    weight_total = sum(weights.values())
    weights = {j: w / weight_total for j, w in weights.items()}

    dist = [0.0] * (m + 1)
    dist[k0] = 1.0
    hit_cdf = 0.0
    if 0 in weights:
        hit_cdf += weights[0] * dist[m]
    for step in range(1, hi + 1):
        nxt = [0.0] * (m + 1)
        nxt[0] += dist[0]
        nxt[m] += dist[m]
        for k in range(1, m):
            move = (k * (n - k)) / (n * n)
            mass = dist[k]
            nxt[k - 1] += move * mass
            nxt[k + 1] += move * mass
            nxt[k] += (1.0 - 2.0 * move) * mass
        dist = nxt
        if step in weights:
            hit_cdf += weights[step] * dist[m]
    return hit_cdf


def source_parameter_translation(
    *, copy_number: int = 750, genome_bp: int = 16_569,
    mutation_rate_per_bp_replication: float = 5.0e-8,
    turnover_cycles_per_year: tuple[float, float] = (6.5, 11.5),
    heteroplasmy_threshold: float = 0.8,
) -> dict[str, Any]:
    """Translate An et al. 2024 model inputs; keep biological caveats explicit."""
    n = copy_number
    m = math.ceil(n * heteroplasmy_threshold)
    mu_genome = mutation_rate_per_bp_replication * genome_bp
    rates = []
    for rho in turnover_cycles_per_year:
        origins = n * rho * mu_genome
        p_hit = 1.0 / m
        eventual_lineage_rate = origins * p_hit
        rates.append({
            "turnover_cycles_per_year": rho,
            "new_unique_variant_origins_per_cell_year_model_mean": origins,
            "single_neutral_origin_probability_to_reach_threshold": p_hit,
            "expected_origins_per_cell_year_that_eventually_reach_threshold": eventual_lineage_rate,
        })
    return {
        "population_size_mtDNA_copies": n,
        "genome_length_bp": genome_bp,
        "mutation_rate_per_bp_per_replication": mutation_rate_per_bp_replication,
        "poisson_mean_new_variants_per_replicated_genome": mu_genome,
        "mean_new_variants_per_homeostatic_turnover": n * mu_genome,
        "illustrative_heteroplasmy_threshold": heteroplasmy_threshold,
        "threshold_copy_count": m,
        "finite_N_copy_number_factor_N_over_m": n / m,
        "parameter_scenarios": rates,
        "identity": "N*rho*mu_genome/m = rho*mu_genome*(N/m), approaching rho*mu_genome/h as N grows",
        "status": "conditional model translation, not a biological disease-incidence estimate",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=None, help="optional JSON output path")
    args = parser.parse_args()
    finite = {
        "population_size": 100,
        "initial_mutant_copies": 10,
        "threshold_mutant_copies": 80,
        "threshold_fraction": 0.8,
        "horizon_years": 10,
        "turnover_scenarios_per_year": [0.5, 2.0],
        "eventual_hit_probability_before_loss": str(hit_probability_before_loss(10, 80)),
        "finite_horizon_hit_probabilities": [],
        "interpretation": "Same embedded neutral chain; higher turnover only advances its event clock.",
    }
    for rho in finite["turnover_scenarios_per_year"]:
        p = neutral_moran_hit_by_time(
            population_size=finite["population_size"],
            initial_k=finite["initial_mutant_copies"],
            threshold_m=finite["threshold_mutant_copies"],
            turnover_cycles_per_year=rho,
            horizon_years=finite["horizon_years"],
        )
        finite["finite_horizon_hit_probabilities"].append({
            "turnover_cycles_per_year": rho,
            "probability_threshold_reached_by_horizon": p,
        })
    result = {
        "finite_horizon_example": finite,
        "An_2024_source_parameter_translation": source_parameter_translation(),
        "counterexample_selective_clearance": {
            "statement": "For mutant replication fitness 1-s, s>0, the exact mean mutant-count drift per replacement attempt is negative at every interior k; increasing the event rate then accelerates purification rather than worsening load.",
            "drift_per_attempt": "-s*k*(N-k)/(N*(N-s*k))",
            "scope": "This is a contrasting Moran model, not fitted biology; it shows why genotype-blindness is a load-bearing premise.",
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(rendered + "\n")
    print(rendered)


if __name__ == "__main__":
    main()
