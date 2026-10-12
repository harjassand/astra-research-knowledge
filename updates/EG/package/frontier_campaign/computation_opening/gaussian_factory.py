#!/usr/bin/env python3
"""Bounded-vector mean -> approximately Gaussian sample.

This is a floating-point diagnostic implementation of a real-arithmetic
theorem, reconstructed as a specialization of first-order rejection
sampling (FORS). It does not certify continuous-law TV for machine floats.

The oracle returns independent vectors X with ||X||_2 <= radius. Its mean
is never evaluated or supplied to the sampler. The returned sample law in
the ideal real-arithmetic model is within epsilon TV of N(E[X], I_d).

Run the small diagnostics with:
    python3 gaussian_factory.py --diagnostics --samples 1000

NumPy is only needed for quadrature diagnostics; the sampler uses stdlib.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import math
import random
import time
from typing import Callable, Sequence


@dataclass
class Cost:
    oracle_calls: int = 0
    proposals: int = 0
    factors: int = 0


def factor_count(radius: float, epsilon: float) -> int:
    """Choose m with m >= R^2 and 10*m*exp(-m/(8*R^2)) <= epsilon.

    Search is on the decreasing branch m >= 8 R^2. It does not query X.
    """
    if not (math.isfinite(radius) and radius >= 0):
        raise ValueError("radius must be finite and nonnegative")
    if not (0 < epsilon < 1):
        raise ValueError("epsilon must lie in (0, 1)")
    if radius == 0:
        return 0
    r2 = radius * radius
    if not math.isfinite(r2):
        raise ValueError("radius squared is outside floating-point range")
    log_epsilon = math.log(epsilon)

    def valid(m: int) -> bool:
        return math.log(10) + math.log(m) - m / (8 * r2) <= log_epsilon

    lower = max(1, math.ceil(8 * r2))
    if valid(lower):
        return lower
    upper = lower
    while not valid(upper):
        upper *= 2
    while upper - lower > 1:
        middle = (upper + lower) // 2
        if valid(middle):
            upper = middle
        else:
            lower = middle
    return upper


def poisson_two(rng: random.Random) -> int:
    threshold = math.exp(-2.0)
    product = 1.0
    count = 0
    while product > threshold:
        product *= rng.random()
        count += 1
    return count - 1


def gaussian_from_mean(
    oracle: Callable[[], Sequence[float]],
    dimension: int,
    radius: float,
    epsilon: float,
    *,
    rng: random.Random | None = None,
    cost: Cost | None = None,
) -> list[float]:
    """Generate a diagnostic sample without evaluating the oracle mean.

    Oracle independence and the radius bound are interface promises.
    Dimension and the observed norm are checked on each acquisition.
    """
    if dimension < 1:
        raise ValueError("dimension must be positive")
    rng = random.Random() if rng is None else rng
    cost = Cost() if cost is None else cost
    m = factor_count(radius, epsilon)
    if m == 0:
        return [rng.gauss(0.0, 1.0) for _ in range(dimension)]
    scale = 1.0 / math.sqrt(m)
    output = [0.0] * dimension
    for _ in range(m):
        while True:
            cost.proposals += 1
            y = [rng.gauss(0.0, scale) for _ in range(dimension)]
            j = poisson_two(rng)
            acceptance = 1.0
            for _ in range(j):
                x = tuple(oracle())
                cost.oracle_calls += 1
                if len(x) != dimension:
                    raise ValueError("oracle returned the wrong dimension")
                if math.hypot(*x) > radius * (1 + 1e-12):
                    raise ValueError("observed oracle sample exceeds radius")
                w = math.fsum(a * b for a, b in zip(y, x))
                clipped = max(-1.0, min(1.0, w))
                acceptance *= (1.0 + clipped) / 2.0
            if rng.random() < acceptance:
                for k in range(dimension):
                    output[k] += y[k]
                cost.factors += 1
                break
    return output


def normal_cdf(z: float) -> float:
    return 0.5 * math.erfc(-z / math.sqrt(2.0))


def empirical_ks(samples: list[float], mean: float) -> float:
    ordered = sorted(samples)
    n = len(ordered)
    return max(
        max(abs(normal_cdf(x - mean) - i / n),
            abs((i + 1) / n - normal_cdf(x - mean)))
        for i, x in enumerate(ordered)
    )


def quadrature(points: list[float], probs: list[float], m: int) -> dict:
    """Approximate one-factor TV on a standardized [-12-|a|,12+|a|] grid.

    This independently evaluates the factory's exact ideal density. It is
    a numerical diagnostic, not a rigorous quadrature enclosure.
    """
    import numpy as np

    mean = math.fsum(x * p for x, p in zip(points, probs))
    a = mean / math.sqrt(m)
    limit = 12.0 + abs(a)
    s = np.linspace(-limit, limit, 200_001)
    base = np.exp(-s * s / 2) / math.sqrt(2 * math.pi)
    clipped_tilt = sum(
        p * np.clip(s * x / math.sqrt(m), -1, 1)
        for x, p in zip(points, probs)
    )
    unnormalized = base * np.exp(clipped_tilt)
    zhat = float(np.trapezoid(unnormalized, s))
    factory_density = unnormalized / zhat
    target_density = np.exp(-((s - a) ** 2) / 2) / math.sqrt(2 * math.pi)
    tv = float(np.trapezoid(abs(factory_density - target_density), s) / 2)
    return {
        "factor_tv_quadrature": tv,
        "m_times_factor_tv_quadrature": m * tv,
        "factor_acceptance_quadrature": zhat / math.e,
        "expected_calls_per_factor_quadrature": 2 * math.e / zhat,
        "quadrature_grid_points": len(s),
        "quadrature_standardized_limit": limit,
    }


def diagnostics(n: int, epsilon: float, seed: int) -> dict:
    cases = [
        ("symmetric_boundary", [-1.0, 1.0], [0.5, 0.5]),
        ("skew_boundary", [-1.0, 1.0], [0.1, 0.9]),
        ("rare_positive_spike", [0.0, 1.0], [0.999, 0.001]),
        ("deterministic_boundary", [1.0], [1.0]),
    ]
    rows = []
    for index, (name, points, probs) in enumerate(cases):
        radius = max(abs(x) for x in points)
        mean = math.fsum(x * p for x, p in zip(points, probs))
        m = factor_count(radius, epsilon)
        acquisition_rng = random.Random(seed + 2 * index)
        sampler_rng = random.Random(seed + 2 * index + 1)

        def oracle() -> tuple[float]:
            u = acquisition_rng.random()
            cumulative = 0.0
            for x, p in zip(points, probs):
                cumulative += p
                if u < cumulative:
                    return (x,)
            return (points[-1],)

        cost = Cost()
        start = time.perf_counter()
        samples = [gaussian_from_mean(
            oracle, 1, radius, epsilon, rng=sampler_rng, cost=cost,
        )[0] for _ in range(n)]
        elapsed = time.perf_counter() - start
        sample_mean = math.fsum(samples) / n
        sample_variance = math.fsum((x - sample_mean) ** 2 for x in samples) / (n - 1)
        row = {
            "case": name,
            "oracle_points": points,
            "oracle_probabilities": probs,
            "target_mean_for_diagnostic_only": mean,
            "target_variance": 1,
            "epsilon": epsilon,
            "factors_m": m,
            "analytic_total_tv_bound": 10 * m * math.exp(-m / (8 * radius * radius)),
            "samples": n,
            "sample_mean": sample_mean,
            "sample_variance": sample_variance,
            "empirical_ks_to_target": empirical_ks(samples, mean),
            "cost": asdict(cost),
            "calls_per_output": cost.oracle_calls / n,
            "calls_per_factor": cost.oracle_calls / (n * m),
            "elapsed_seconds": elapsed,
        }
        row.update(quadrature(points, probs, m))
        row["quadrature_factor_ladder"] = [
            {"m": ladder_m, **quadrature(points, probs, ladder_m)}
            for ladder_m in sorted({1, 2, 4, 8, 16, 32, m})
        ]
        rows.append(row)
    return {
        "status": "FINITE_DIAGNOSTICS_ONLY_KNOWN_FORS_COROLLARY",
        "seed": seed,
        "notes": [
            "Sampler receives no oracle mean; target mean is used only after sampling.",
            "Empirical KS is not a full-law TV certificate.",
            "Quadrature uses the independently reconstructed ideal factor density.",
            "Float output has finite support and is not continuous-law TV certified.",
            "These are acquired oracle samples, not physical validation.",
        ],
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diagnostics", action="store_true")
    parser.add_argument("--samples", type=int, default=1000)
    parser.add_argument("--epsilon", type=float, default=0.01)
    parser.add_argument("--seed", type=int, default=20261012)
    args = parser.parse_args()
    if not args.diagnostics:
        parser.error("use --diagnostics, or import gaussian_from_mean")
    if args.samples < 2:
        parser.error("--samples must be at least 2")
    print(json.dumps(diagnostics(args.samples, args.epsilon, args.seed), indent=2))


if __name__ == "__main__":
    main()
