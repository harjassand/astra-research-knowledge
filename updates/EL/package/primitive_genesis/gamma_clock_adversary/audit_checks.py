#!/usr/bin/env python3
"""Independent arithmetic and numerical sanity checks for the clock audit.

The discrete reference sampler uses rational arithmetic. Its law is exact under
an ideal independent fair-bit source; random.Random is a reproducible PRNG here.
Gamma outputs and all Monte Carlo comparisons use floating point and are not a
certified exact-continuous implementation.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from fractions import Fraction as F
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent


class Bits:
    def __init__(self, seed: int):
        self.rng = random.Random(seed)
        self.poisson_trials = 0
        self.expcoin_rounds = 0

    def coin(self, p: F) -> bool:
        assert 0 <= p <= 1
        return self.rng.randrange(p.denominator) < p.numerator

    def expcoin(self, x: F) -> bool:
        """Bernoulli(exp(-x)), 0 <= x <= 1, by alternating rational bounds."""
        assert 0 <= x <= 1
        if x == 0:
            return True
        lower, upper, partial, term = F(0), F(1), F(1), F(1)
        prefix = 0
        for j in range(1, 100000):
            self.expcoin_rounds += 1
            prefix = 2 * prefix + self.rng.getrandbits(1)
            term *= x / j
            partial += term if j % 2 == 0 else -term
            if j % 2:
                lower = partial
            else:
                upper = partial
            u_low, u_high = F(prefix, 1 << j), F(prefix + 1, 1 << j)
            if u_high <= lower:
                return True
            if u_low >= upper:
                return False
        raise RuntimeError("Only a diagnostic guard; not part of the algorithm")

    def poisson_small(self, x: F) -> int:
        assert 0 <= x <= 1
        while True:
            self.poisson_trials += 1
            r = 0
            while self.rng.getrandbits(1):
                r += 1
            p = (2 * x) ** r / (2 * math.factorial(r))
            assert 0 <= p <= 1
            if self.coin(p) and self.expcoin(x):
                return r

    def poisson(self, mu: F) -> int:
        assert mu >= 0
        if mu == 0:
            return 0
        chunks = (mu.numerator + mu.denominator - 1) // mu.denominator
        return sum(self.poisson_small(mu / chunks) for _ in range(chunks))


def endpoints(n: int, k: int, o: int, g: int) -> tuple[int, int]:
    assert n >= o >= 0 and k >= 1 and g >= 0
    return math.comb(n, o), math.comb(n + (k - 1) * g, o)


def correction(bits: Bits, n: int, k: int, o: int, g: int) -> tuple[int, int, int]:
    a, b = endpoints(n, k, o, g)
    delta = b - a
    if delta == 0:
        return 0, 0, 0
    count = bits.poisson(F(k * delta, a))
    total = 0
    proposed_jump_total = 0
    for _ in range(count):
        i = bits.rng.randrange(k)
        rate = math.comb(n + i * g, o)
        r = 1
        while bits.coin(F(delta, b)):
            r += 1
        proposed_jump_total += r
        # The 1/r thinning coin can be placed before the power thinning coins.
        if bits.rng.randrange(r) != 0:
            continue
        if all(bits.coin(F(b - rate, delta)) for _ in range(r)):
            total += r
    return total, count, proposed_jump_total


def geometric_coefficients(qs: list[F], degree: int) -> list[F]:
    coeffs = [F(1)] + [F(0)] * degree
    for q in qs:
        out = [F(0)] * (degree + 1)
        for j in range(degree + 1):
            for r in range(j + 1):
                out[j] += coeffs[j - r] * (1 - q) * q**r
        coeffs = out
    return coeffs


def poisson_coefficients(qs: list[F], degree: int) -> list[F]:
    coeffs = [math.prod(1 - q for q in qs)]
    for j in range(1, degree + 1):
        coeffs.append(sum(sum(q**r for q in qs) * coeffs[j - r]
                          for r in range(1, j + 1)) / j)
    return coeffs


def exact_checks() -> dict:
    fixtures = [[F(0)], [F(1, 3), F(0)], [F(1, 2)] * 4,
                [F(1, 7), F(2, 5), F(9, 10), F(0)]]
    for n in [3, 7, 20, 100]:
        for o in [0, 1, 2, 3]:
            for g in [0, 1, 3]:
                for k in [1, 2, 5]:
                    a, b = endpoints(n, k, o, g)
                    fixtures.append([1 - F(math.comb(n + i * g, o), b)
                                     for i in range(k)])
    checked_coefficients = 0
    for qs in fixtures:
        degree = 12
        left = geometric_coefficients(qs, degree)
        right = poisson_coefficients(qs, degree)
        assert left == right
        checked_coefficients += degree + 1
        mean_n = sum(q / (1 - q) for q in qs)
        var_n = sum(q / (1 - q) ** 2 for q in qs)
        # Scale b=1. These are independent direct-sum moment calculations.
        assert len(qs) + mean_n == sum(1 / (1 - q) for q in qs)
        assert len(qs) + mean_n + var_n == sum(1 / (1 - q) ** 2 for q in qs)
    bound_fixtures = 0
    for n in [10, 100, 10000, 10**8, 10**16]:
        for o in [1, 2, 3, 7]:
            for g in [0, 1, 4]:
                for k in [1, math.isqrt(n), 2 * math.isqrt(n)]:
                    a, b = endpoints(n, k, o, g)
                    q = F(b - a, b)
                    alpha = F(o * g * (k - 1), n - o + 1)
                    assert q <= alpha
                    if alpha <= F(1, 2):
                        assert F(k * (b - a), a) <= 2 * k * alpha
                    bound_fixtures += 1
    return {"fixtures": len(fixtures), "exact_coefficients": checked_coefficients,
            "rate_bound_fixtures": bound_fixtures, "passed": True}


def discrete_checks() -> list[dict]:
    bits = Bits(2026101201)
    samples = 4000
    results = []
    for n in [100, 10000, 10**6, 10**8]:
        k, o, g = math.isqrt(n), 2, 1
        a, b = endpoints(n, k, o, g)
        mu = k * (b - a) / a
        triples = np.array([correction(bits, n, k, o, g) for _ in range(samples)])
        rates = [math.comb(n + i * g, o) for i in range(k)]
        exact_mean = sum((b - rate) / rate for rate in rates)
        exact_var = sum(b * (b - rate) / rate**2 for rate in rates)
        mean_z = ((float(triples[:, 0].mean()) - exact_mean)
                  / math.sqrt(exact_var / samples))
        assert abs(mean_z) < 6
        assert abs(float(triples[:, 1].mean()) - mu) < 6 * math.sqrt(mu / samples)
        results.append({"n": n, "k": k, "samples": samples,
                        "rational_envelope_mean_candidates": mu,
                        "sample_mean_candidates": float(triples[:, 1].mean()),
                        "sample_mean_proposed_jump_sum": float(triples[:, 2].mean()),
                        "target_mean_N": exact_mean,
                        "sample_mean_N": float(triples[:, 0].mean()),
                        "mean_N_standard_errors": mean_z})
    return results


def expm1_minus_x(x: float) -> float:
    if abs(x) > 0.01:
        return math.expm1(x) - x
    term = x * x / 2
    total = term
    for j in range(3, 1000):
        term *= x / j
        total += term
        if abs(term) <= 1e-17 * abs(total):
            return total
    return total


def gamma_envelope(rng: random.Random, shape: int) -> tuple[float, int]:
    root_shape = math.sqrt(shape)
    trials = 0
    while True:
        trials += 1
        component = rng.randrange(5)
        if component < 2:
            z = -1 - 2 * (-math.log1p(-rng.random()))
            log_envelope = (z + 1) / 2
        elif component < 4:
            z = 2 * rng.random() - 1
            log_envelope = 0.0
        else:
            z = 1 + (-math.log1p(-rng.random()))
            log_envelope = -(z - 1)
        threshold = shape * expm1_minus_x(z / root_shape) + log_envelope
        assert threshold >= -1e-11
        if -math.log1p(-rng.random()) >= threshold:
            return shape * math.exp(z / root_shape), trials


def gamma_checks() -> list[dict]:
    rng = random.Random(2026101202)
    samples = 20000
    results = []
    for m in [1, 2, 10, 10000, 10**8]:
        xs, trial_counts = [], []
        for _ in range(samples):
            x, trials = gamma_envelope(rng, m)
            xs.append((x - m) / math.sqrt(m))
            trial_counts.append(trials)
        xs = np.array(xs)
        mean_z = float(xs.mean()) * math.sqrt(samples)
        variance = float(xs.var())
        assert abs(mean_z) < 6
        assert abs(variance - 1) < 0.12
        assert float(np.mean(trial_counts)) < 2.1
        results.append({"shape": m, "samples": samples,
                        "standardized_mean_standard_errors": mean_z,
                        "standardized_variance": variance,
                        "mean_proposals": float(np.mean(trial_counts)),
                        "uniform_expected_proposal_bound": 5 / math.sqrt(2 * math.pi)})
    return results


def numerical_correction(rng: np.random.Generator, rates: np.ndarray) -> int:
    a, b = float(rates.min()), float(rates.max())
    if a == b:
        return 0
    delta = b - a
    q = delta / b
    count = rng.poisson(len(rates) * delta / a)
    total = 0
    for _ in range(count):
        i = int(rng.integers(len(rates)))
        r = int(rng.geometric(1 - q))
        if rng.random() < ((b - rates[i]) / delta) ** r / r:
            total += r
    return total


def ks_distance(a: np.ndarray, b: np.ndarray) -> float:
    a, b = np.sort(a), np.sort(b)
    grid = np.sort(np.concatenate((a, b)))
    return float(np.max(np.abs(np.searchsorted(a, grid, side="right") / len(a)
                               - np.searchsorted(b, grid, side="right") / len(b))))


def direct_sum_comparisons() -> list[dict]:
    rng = np.random.default_rng(2026101203)
    samples = 30000
    results = []
    for n, k, o, g in [(100, 10, 2, 1), (10000, 100, 3, 2), (30, 5, 2, 0)]:
        rates = np.array([math.comb(n + i * g, o) for i in range(k)], dtype=float)
        b = float(rates.max())
        scales = b / rates
        direct = rng.exponential(scales, size=(samples, k)).sum(axis=1)
        correction_n = np.array([numerical_correction(rng, rates) for _ in range(samples)])
        mixture = rng.gamma(k + correction_n, 1.0)
        mean = float(scales.sum())
        variance = float((scales**2).sum())
        mean_z = (float(mixture.mean()) - mean) / math.sqrt(variance / samples)
        variance_se = math.sqrt((6 * float((scales**4).sum()) + 2 * variance**2) / samples)
        variance_z = (float(mixture.var()) - variance) / variance_se
        ks = ks_distance(direct, mixture)
        assert abs(mean_z) < 6 and abs(variance_z) < 6 and ks < 0.025
        results.append({"n": n, "k": k, "order": o, "generativity": g,
                        "samples_per_method": samples, "scale": "b times timestamp",
                        "mixture_mean_standard_errors": mean_z,
                        "mixture_variance_standard_errors": variance_z,
                        "two_sample_KS_distance": ks})
    return results


def main() -> None:
    result = {
        "scope": "Arithmetic proof checks and reproducible Monte Carlo sanity, not a certified exact-continuous implementation",
        "exact_arithmetic": exact_checks(),
        "rational_discrete_reference": discrete_checks(),
        "gamma_reference": gamma_checks(),
        "direct_exponential_sum_baseline": direct_sum_comparisons(),
    }
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (ROOT / "audit_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
