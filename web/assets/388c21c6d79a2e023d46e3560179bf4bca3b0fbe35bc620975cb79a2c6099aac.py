#!/usr/bin/env python3
"""Finite-data reflected-word dissipation certificate (stdlib only).

The training split chooses a bounded scalar feature of a reflected half-window
word. The independent validation split gives a one-sided empirical-Bernstein
upper confidence bound for its reflected product mean. A negative upper bound
is converted to an entropy-production-rate lower bound by the midpoint lemma
recorded in v1.txt.

The simulator is a three-state CTMC ring with rates a clockwise and b
counterclockwise, observed only through Y=1{X=0}. Independent windows are
sampled exactly from the stationary two-sided path law by drawing X_0 uniformly
and then drawing the past under Q* and future under Q, conditionally
independently. This is finite simulation evidence, not empirical validation.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter
from fractions import Fraction
from typing import Sequence


def transition_matrix(t: float, a: float, b: float) -> list[list[float]]:
    """Row-stochastic exp(tQ) for the 3-cycle, states 0,1,2."""
    decay = math.exp(-1.5 * (a + b) * t)
    phase = math.sqrt(3.0) * (a - b) * t / 2.0
    phases = (0.0, -2.0 * math.pi / 3.0, 2.0 * math.pi / 3.0)
    return [
        [
            (1.0 + 2.0 * decay * math.cos(phase + phases[(j - i) % 3])) / 3.0
            for j in range(3)
        ]
        for i in range(3)
    ]


def categorical(rng: random.Random, probabilities: Sequence[float]) -> int:
    u = rng.random()
    total = 0.0
    for j, probability in enumerate(probabilities):
        total += probability
        if u <= total:
            return j
    return len(probabilities) - 1


def draw_word(rng: random.Random, start: int, times: Sequence[float], a: float, b: float) -> tuple[int, ...]:
    state = start
    previous = 0.0
    bits: list[int] = []
    for time in times:
        matrix = transition_matrix(time - previous, a, b)
        state = categorical(rng, matrix[state])
        bits.append(int(state == 0))
        previous = time
    return tuple(bits)


def word_id(bits: Sequence[int]) -> int:
    value = 0
    for bit in bits:
        value = 2 * value + int(bit)
    return value


def sample_reflected_pair(
    rng: random.Random, times: Sequence[float], a: float, b: float
) -> tuple[int, int]:
    """Return (past word, future word), with times measured outward from 0."""
    center = rng.randrange(3)  # pi is uniform on the ring.
    past = draw_word(rng, center, times, b, a)  # Q* reverses the cycle rates.
    future = draw_word(rng, center, times, a, b)
    return word_id(past), word_id(future)


def jacobi_min_eigenvector(matrix: Sequence[Sequence[float]]) -> tuple[float, list[float]]:
    """Small symmetric eigensolver; adequate for the 4x4 example table."""
    n = len(matrix)
    a = [list(row) for row in matrix]
    v = [[float(i == j) for j in range(n)] for i in range(n)]
    for _ in range(200 * n * n):
        p, q = max(
            ((i, j) for i in range(n) for j in range(i + 1, n)),
            key=lambda ij: abs(a[ij[0]][ij[1]]),
            default=(0, 0),
        )
        if p == q or abs(a[p][q]) < 1e-14:
            break
        tau = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
        if tau == 0.0:
            tangent = 1.0
        else:
            tangent = math.copysign(1.0, tau) / (abs(tau) + math.sqrt(1.0 + tau * tau))
        cosine = 1.0 / math.sqrt(1.0 + tangent * tangent)
        sine = tangent * cosine
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        a[p][p] = app - tangent * apq
        a[q][q] = aqq + tangent * apq
        a[p][q] = a[q][p] = 0.0
        for k in range(n):
            if k not in (p, q):
                akp, akq = a[k][p], a[k][q]
                a[k][p] = a[p][k] = cosine * akp - sine * akq
                a[k][q] = a[q][k] = sine * akp + cosine * akq
            vkp, vkq = v[k][p], v[k][q]
            v[k][p] = cosine * vkp - sine * vkq
            v[k][q] = sine * vkp + cosine * vkq
    index = min(range(n), key=lambda j: a[j][j])
    return a[index][index], [v[k][index] for k in range(n)]


def train_feature(
    pairs: Sequence[tuple[int, int]], alphabet_size: int
) -> tuple[list[Fraction], Fraction, Fraction]:
    """Find a negative reflected-word direction, then train its common offset.

    The returned f table is fixed before validation. Its range is returned as
    R. A negative training score is required; otherwise the routine fails.
    """
    n = len(pairs)
    counts = [[0] * alphabet_size for _ in range(alphabet_size)]
    row = [0] * alphabet_size
    col = [0] * alphabet_size
    for u, v in pairs:
        counts[u][v] += 1
        row[u] += 1
        col[v] += 1
    empirical = [[counts[i][j] / n for j in range(alphabet_size)] for i in range(alphabet_size)]
    sym = [[(empirical[i][j] + empirical[j][i]) / 2.0 for j in range(alphabet_size)] for i in range(alphabet_size)]
    _, z = jacobi_min_eigenvector(sym)

    # Treat each returned binary float coefficient as its exact rational value.
    # Compute the training-optimal common offset exactly so the final witness
    # has a certified finite range and exact rational validation scores.
    zq = [Fraction.from_float(value) for value in z]
    mean_u = sum(Fraction(row[j], n) * zq[j] for j in range(alphabet_size))
    mean_v = sum(Fraction(col[j], n) * zq[j] for j in range(alphabet_size))
    offset = (mean_u + mean_v) / 2
    f = [zq[j] - offset for j in range(alphabet_size)]
    span = max(f) - min(f)
    if span <= 0:
        raise RuntimeError("training returned a constant feature")
    train_mean = sum((f[u] * f[v] for u, v in pairs), Fraction(0)) / n
    if train_mean >= 0:
        raise RuntimeError("training did not find a negative reflected score")
    return f, span, train_mean


def population_word_table(times: Sequence[float], a: float, b: float) -> list[list[float]]:
    """Exact finite-dimensional formula for the ring's reflected table."""
    alphabet_size = 2 ** len(times)

    def conditional_words(rate_cw: float, rate_ccw: float) -> list[list[float]]:
        distributions = []
        for start in range(3):
            row = [0.0] * alphabet_size
            for word in range(alphabet_size):
                bits = tuple((word >> (len(times) - 1 - j)) & 1 for j in range(len(times)))
                state_probabilities = [0.0] * 3
                state_probabilities[start] = 1.0
                previous = 0.0
                for time, bit in zip(times, bits):
                    matrix = transition_matrix(time - previous, rate_cw, rate_ccw)
                    next_probabilities = [0.0] * 3
                    for x in range(3):
                        for y in range(3):
                            if int(y == 0) == bit:
                                next_probabilities[y] += state_probabilities[x] * matrix[x][y]
                    state_probabilities = next_probabilities
                    previous = time
                row[word] = sum(state_probabilities)
            distributions.append(row)
        return distributions

    future = conditional_words(a, b)
    past = conditional_words(b, a)
    return [
        [sum(past[i][u] * future[i][v] for i in range(3)) / 3.0 for v in range(alphabet_size)]
        for u in range(alphabet_size)
    ]


def ceil_sqrt_fraction(value: Fraction, decimal_places: int = 15) -> Fraction:
    """Rational upper bound for sqrt(value), rounded upward by integer math."""
    if value < 0:
        raise ValueError("square root input must be nonnegative")
    scale = 10**decimal_places
    numerator = value.numerator * scale * scale
    quotient = (numerator + value.denominator - 1) // value.denominator
    root = math.isqrt(quotient)
    if root * root < quotient:
        root += 1
    return Fraction(root, scale)


def exact_validation_bound(
    pairs: Sequence[tuple[int, int]],
    f: Sequence[Fraction],
    span: Fraction,
    alpha: Fraction,
    family_size: int = 1,
) -> dict[str, object]:
    """Exact rational score/variance; conservative rational Bernstein radius.

    For X=f(U)f(V)/span^2, the training offset lies in the feature range, so
    |X|<=1. The log factor L is an integer chosen with 2**L >= 2K/alpha, hence
    exp(L)>=2**L>=2K/alpha and L>=ln(2K/alpha). The square root is rounded up
    using integer arithmetic. Thus the reported upper endpoint is conservative.
    """
    n = len(pairs)
    if n < 2:
        raise ValueError("at least two validation windows are required")
    scale = span * span
    score_by_pair = {(u, v): f[u] * f[v] / scale for u, v in set(pairs)}
    if any(abs(score) > 1 for score in score_by_pair.values()):
        raise RuntimeError("normalised score exceeded [-1,1]")
    counts = Counter(pairs)
    mean = sum((counts[pair] * score for pair, score in score_by_pair.items()), Fraction(0)) / n
    variance = sum(
        (counts[pair] * (score - mean) ** 2 for pair, score in score_by_pair.items()),
        Fraction(0),
    ) / (n - 1)
    ratio = Fraction(2 * family_size, 1) / alpha
    log_upper = 0
    while Fraction(2**log_upper, 1) < ratio:
        log_upper += 1
    square_root = ceil_sqrt_fraction(Fraction(2 * log_upper, n) * variance)
    radius = square_root + Fraction(14 * log_upper, 3 * (n - 1))
    upper_mean = mean + radius
    gap = max(Fraction(0), -upper_mean)
    return {
        "validation_mean_exact": f"{mean.numerator}/{mean.denominator}",
        "validation_variance_exact": f"{variance.numerator}/{variance.denominator}",
        "log_factor_upper_integer": log_upper,
        "log_factor_argument": f"2K/alpha = {ratio.numerator}/{ratio.denominator}",
        "confidence_radius_exact_upper": f"{radius.numerator}/{radius.denominator}",
        "upper_confidence_endpoint_exact_upper": f"{upper_mean.numerator}/{upper_mean.denominator}",
        "gap_lower_exact": f"{gap.numerator}/{gap.denominator}",
        "gap_lower_decimal": float(gap),
        "confidence_radius_decimal_upper": float(radius),
        "upper_confidence_endpoint_decimal_upper": float(upper_mean),
        "ep_rate_lower_exact_nats_per_time": None,
        "alpha_exact": f"{alpha.numerator}/{alpha.denominator}",
        "family_size": family_size,
    }


def run_example(
    seed: int = 20261009,
    n_train: int = 10000,
    n_validation: int = 250000,
    a: float = 1.0,
    b: float = 0.01,
    times: Sequence[float] = (0.01, 0.31),
    alpha: float = 0.05,
) -> dict[str, object]:
    rng = random.Random(seed)
    train_pairs = [sample_reflected_pair(rng, times, a, b) for _ in range(n_train)]
    validation_pairs = [sample_reflected_pair(rng, times, a, b) for _ in range(n_validation)]
    alphabet_size = 2 ** len(times)
    f, span, train_score = train_feature(train_pairs, alphabet_size)
    exact_alpha = Fraction(str(alpha))
    confidence = exact_validation_bound(validation_pairs, f, span, exact_alpha)
    total_span_fraction = 2 * Fraction(str(max(times)))
    gap_num, gap_den = map(int, confidence["gap_lower_exact"].split("/"))
    exact_gap = Fraction(gap_num, gap_den)
    exact_sigma_lower = 16 * exact_gap / total_span_fraction
    confidence["ep_rate_lower_exact_nats_per_time"] = f"{exact_sigma_lower.numerator}/{exact_sigma_lower.denominator}"
    sigma_lower = float(exact_sigma_lower)
    delta_lower = float(exact_gap)
    total_span = float(total_span_fraction)
    normalized_train_score = float(train_score / (span * span))
    normalized_witness = [float(value) for value in f]
    val_mean = float(confidence["validation_mean_exact"].split("/")[0]) / float(confidence["validation_mean_exact"].split("/")[1])
    val_variance = float(confidence["validation_variance_exact"].split("/")[0]) / float(confidence["validation_variance_exact"].split("/")[1])
    radius = float(confidence["confidence_radius_decimal_upper"])
    upper_mean = float(confidence["upper_confidence_endpoint_decimal_upper"])

    table = population_word_table(times, a, b)
    marginal_u = [sum(table[u]) for u in range(alphabet_size)]
    marginal_v = [sum(table[u][v] for u in range(alphabet_size)) for v in range(alphabet_size)]
    population_score = sum(
        table[u][v] * f[u] * f[v] / (span * span)
        for u in range(alphabet_size)
        for v in range(alphabet_size)
    )
    centered = [
        [table[u][v] - marginal_u[u] * marginal_v[v] for v in range(alphabet_size)]
        for u in range(alphabet_size)
    ]
    min_eig_table, _ = jacobi_min_eigenvector(
        [[(table[i][j] + table[j][i]) / 2.0 for j in range(alphabet_size)] for i in range(alphabet_size)]
    )
    min_eig, eigvec = jacobi_min_eigenvector(
        [[(centered[i][j] + centered[j][i]) / 2.0 for j in range(alphabet_size)] for i in range(alphabet_size)]
    )
    eig_span = max(eigvec) - min(eigvec)
    population_spectral_score = min_eig / (eig_span * eig_span)
    t = total_span
    covariance = (2.0 / 9.0) * math.exp(-1.5 * (a + b) * t) * math.cos(math.sqrt(3.0) * (a - b) * t / 2.0)
    hidden_sigma = (a - b) * math.log(a / b)
    best_one_time = optimize_one_time_bound(a, b)
    learned_population_bound = max(0.0, -population_score) * 16.0 / total_span
    population_asymmetry = max(
        abs(table[u][v] - table[v][u])
        for u in range(alphabet_size)
        for v in range(alphabet_size)
    )

    return {
        "claim_status": "finite-tested simulation only",
        "seed": seed,
        "rates_clockwise_counterclockwise": [a, b],
        "times_outward": list(times),
        "total_window_span": total_span,
        "training_windows": n_train,
        "validation_windows": n_validation,
        "independent_stationary_windows_required": True,
        "hidden_state_count_used_by_inference": None,
        "mixing_time_used_by_inference": None,
        "word_alphabet_size": alphabet_size,
        "witness_values_by_word_id": normalized_witness,
        "witness_values_exact_binary_rational": [f"{value.numerator}/{value.denominator}" for value in f],
        "witness_range": float(span),
        "witness_range_exact": f"{span.numerator}/{span.denominator}",
        "training_normalized_score": normalized_train_score,
        "validation_normalized_score": val_mean,
        "validation_sample_variance": val_variance,
        "confidence_alpha": alpha,
        "empirical_bernstein_radius": radius,
        "upper_confidence_bound_on_score": upper_mean,
        "lower_confidence_bound_on_reflected_gap": delta_lower,
        "ep_rate_lower_bound_nats_per_time": sigma_lower,
        "exact_validation_certificate": confidence,
        "population_score_for_learned_feature": population_score,
        "population_midpoint_ep_bound_for_learned_feature_nats_per_time": learned_population_bound,
        "population_spectral_negative_score_normalized": population_spectral_score,
        "population_reflected_table_min_eigenvalue": min_eig_table,
        "population_reflected_word_table": table,
        "population_reflected_word_table_max_asymmetry": population_asymmetry,
        "population_two_time_covariance_at_total_span": covariance,
        "best_one_time_midpoint_bound_on_grid_nats_per_time": best_one_time[0],
        "best_one_time_lag_on_grid": best_one_time[1],
        "exact_hidden_ep_rate_nats_per_time": hidden_sigma,
        "observed_path_reversal_kl_rate": 0.0,
        "apparent_two_state_markov_ep_rate": 0.0,
        "limitations": [
            "Simulation uses the known ring only to generate data; inference uses observed binary words.",
            "Confidence coverage is for independent stationary windows; no single-trajectory mixing bound is assumed.",
            "The zero observed reversal KL is established by the rate-swapping state permutation, not estimated from finite samples.",
            "The training eigensolver is floating point; its coefficients are frozen as exact binary rationals, and training/validation scores, ranges, variances, and the reported confidence endpoint are recomputed exactly.",
            "The generator uses floating-point transition probabilities; this finite run is simulation evidence, not an experiment or exact population proof."
        ]
    }


def optimize_one_time_bound(a: float, b: float) -> tuple[float, float]:
    lam = 1.5 * (a + b)
    omega = math.sqrt(3.0) * (a - b) / 2.0
    best = (0.0, 0.0)
    for k in range(1, 200001):
        t = k / 20000.0
        negative_cov = -(2.0 / 9.0) * math.exp(-lam * t) * math.cos(omega * t)
        if negative_cov > 0.0:
            bound = 16.0 * negative_cov / t
            if bound > best[0]:
                best = (bound, t)
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261009)
    parser.add_argument("--train", type=int, default=10000)
    parser.add_argument("--validation", type=int, default=250000)
    parser.add_argument("--a", type=float, default=1.0)
    parser.add_argument("--b", type=float, default=0.01)
    parser.add_argument("--s1", type=float, default=0.01)
    parser.add_argument("--s2", type=float, default=0.31)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    result = run_example(
        seed=args.seed,
        n_train=args.train,
        n_validation=args.validation,
        a=args.a,
        b=args.b,
        times=(args.s1, args.s2),
        alpha=args.alpha,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    print(rendered)


if __name__ == "__main__":
    main()
