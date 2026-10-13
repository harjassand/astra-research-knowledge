#!/usr/bin/env python3
"""Exact Bernoulli-LR confidence/cap audit for robust matching validation.

This is a statistical-kernel benchmark. It consumes independent batch scores
Z in [0,1] through Y|Z ~ Bernoulli(Z); it does not simulate a comparator or
claim source execution. Every matching batch costs at most m^2 ordered query
requests. The endpoint Bernoulli laws are the proved worst-case means.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
import json
import math
from pathlib import Path


@dataclass(frozen=True)
class Parameters:
    degree: int
    epsilon: str
    m: int
    candidate_slots: int
    validation_budget: str


@dataclass(frozen=True)
class BatchBounds:
    c_m: str
    p_true_max: float
    p_false_min: float
    gap: float
    alpha_each: float
    hoeffding_batches: int
    cap_batches: int
    cap_tail_true: float
    cap_tail_false: float
    kl_true: float
    kl_false: float
    expected_upper_true: float
    expected_upper_false: float


def batch_mean_bounds(degree: int, epsilon: Fraction, m: int) -> tuple[Fraction, Fraction, Fraction]:
    if degree < 1 or m < 1 or epsilon < 0:
        raise ValueError("degree, m and epsilon are outside their allowed range")
    c_m = Fraction(math.comb(2 * m, m), 2 * (4**m))
    a = 2 * epsilon
    b = Fraction(1, 2**degree) - 2 * epsilon - c_m
    if not (0 <= a < b <= 1):
        raise ValueError(f"no validation gap: need 0 <= a < b <= 1, got a={a}, b={b}")
    return a, b, c_m


def _log_binomial_pmf(n: int, k: int, p: float) -> float:
    return (
        math.lgamma(n + 1)
        - math.lgamma(k + 1)
        - math.lgamma(n - k + 1)
        + k * math.log(p)
        + (n - k) * math.log1p(-p)
    )


def _sum_log_probs(log_values: list[float]) -> float:
    if not log_values:
        return 0.0
    top = max(log_values)
    return min(1.0, math.exp(top) * math.fsum(math.exp(v - top) for v in log_values))


def binomial_upper_tail(n: int, p: float, k_min: int) -> float:
    if k_min <= 0:
        return 1.0
    if k_min > n:
        return 0.0
    return _sum_log_probs([_log_binomial_pmf(n, k, p) for k in range(k_min, n + 1)])


def binomial_lower_tail(n: int, p: float, k_max: int) -> float:
    if k_max < 0:
        return 0.0
    if k_max >= n:
        return 1.0
    return _sum_log_probs([_log_binomial_pmf(n, k, p) for k in range(0, k_max + 1)])


def binomial_tail_fraction(n: int, p: Fraction, cutoff: int, upper: bool) -> Fraction:
    """Evaluate one Binomial tail exactly using integer recurrence."""
    if upper:
        if cutoff <= 0:
            return Fraction(1)
        if cutoff > n:
            return Fraction(0)
    else:
        if cutoff < 0:
            return Fraction(0)
        if cutoff >= n:
            return Fraction(1)

    q = p.denominator
    r = p.numerator
    term = (q - r) ** n
    total = 0
    for k in range(n + 1):
        if (upper and k >= cutoff) or (not upper and k <= cutoff):
            total += term
        if k < n:
            term = term * (n - k) * r // ((k + 1) * (q - r))
    return Fraction(total, q**n)


def log_lr_parameters(a: float | Fraction, b: float | Fraction) -> tuple[float, float, float, float]:
    """Return success increment u, failure increment w, KL(a||b), KL(b||a)."""
    a = float(a)
    b = float(b)
    if a == 0.0 or b == 1.0:
        raise ValueError("interior Bernoulli bounds required by this LR implementation")
    u = math.log(b / a)
    w = math.log((1.0 - b) / (1.0 - a))
    d0 = a * math.log(a / b) + (1.0 - a) * math.log((1.0 - a) / (1.0 - b))
    d1 = b * math.log(b / a) + (1.0 - b) * math.log((1.0 - b) / (1.0 - a))
    return u, w, d0, d1


def timeout_tail_bounds(
    n: int,
    a: Fraction,
    b: Fraction,
    alpha_true: Fraction,
    alpha_false: Fraction,
) -> tuple[Fraction, Fraction]:
    """Exact endpoint Binomial bounds on failing to hit either LR boundary by n."""
    u, w, _, _ = log_lr_parameters(a, b)
    span = u - w
    # Lower boundary is log(LR) <= -log(1/alpha_true).
    low = -math.log(1.0 / float(alpha_true))
    # Upper boundary is log(LR) >= log(1/alpha_false).
    high = math.log(1.0 / float(alpha_false))
    # Include one extra terminal count on each side. This is a conservative
    # guard for floating evaluation of the logarithmic integer cutoffs.
    k_true_min = math.floor((low - n * w) / span)  # superset of W_n > low
    k_false_max = math.ceil((high - n * w) / span)  # superset of W_n < high
    return (
        binomial_tail_fraction(n, a, k_true_min, upper=True),
        binomial_tail_fraction(n, b, k_false_max, upper=False),
    )


def exact_tail_cap(a: Fraction, b: Fraction, alpha: Fraction) -> tuple[int, Fraction, Fraction]:
    """Choose a deterministic cap whose exact tails pass alpha."""
    def passing(n: int) -> tuple[bool, Fraction, Fraction]:
        t_true, t_false = timeout_tail_bounds(n, a, b, alpha, alpha)
        return t_true <= alpha and t_false <= alpha, t_true, t_false

    low, high = 0, 1
    ok, tail_true, tail_false = passing(high)
    while not ok:
        low = high
        high *= 2
        ok, tail_true, tail_false = passing(high)

    # Keep high as a checked passing cap; the bisection is only an optimization.
    while high - low > 1:
        middle = (low + high) // 2
        ok, _, _ = passing(middle)
        if ok:
            high = middle
        else:
            low = middle
    ok, tail_true, tail_false = passing(high)
    if not ok:
        raise ArithmeticError("final exact binomial cap check failed")
    return high, tail_true, tail_false


def capped_lr_dp(n: int, p: float, a: float, b: float, alpha_true: float, alpha_false: float) -> dict[str, float]:
    """Exact-state recursion (floating probabilities) for a Bernoulli(p) score stream."""
    u, w, _, _ = log_lr_parameters(a, b)
    low = -math.log(1.0 / alpha_true)
    high = math.log(1.0 / alpha_false)
    alive: dict[int, float] = {0: 1.0}  # successes among the batches seen
    accept_candidate = 0.0
    reject_candidate = 0.0
    expected_batches = 0.0

    for t in range(n):
        expected_batches += math.fsum(alive.values())
        next_alive: defaultdict[int, float] = defaultdict(float)
        for successes, mass in alive.items():
            for y, py in ((0, 1.0 - p), (1, p)):
                if py == 0.0:
                    continue
                s2 = successes + y
                log_lr = (t + 1) * w + s2 * (u - w)
                next_mass = mass * py
                if log_lr >= high:
                    reject_candidate += next_mass
                elif log_lr <= low:
                    accept_candidate += next_mass
                else:
                    next_alive[s2] += next_mass
        alive = dict(next_alive)
        if not alive:
            break

    unknown = math.fsum(alive.values())
    return {
        "expected_batches": expected_batches,
        "accept_candidate": accept_candidate,
        "reject_candidate": reject_candidate,
        "unknown_at_cap": unknown,
        "mass_total": accept_candidate + reject_candidate + unknown,
    }


def benchmark(parameters: Parameters) -> dict[str, object]:
    eps_q = Fraction(parameters.epsilon)
    beta_q = Fraction(parameters.validation_budget)
    a_q, b_q, c_m = batch_mean_bounds(parameters.degree, eps_q, parameters.m)
    a, b = float(a_q), float(b_q)
    gap = b - a
    slots = parameters.candidate_slots
    # Three equal all-history ledgers: false acceptance, true rejection, timeout.
    alpha_q = beta_q / (3 * slots)
    alpha = float(alpha_q)
    fixed = math.ceil(2.0 * math.log(1.0 / alpha) / (gap * gap))
    n_cap, tail_true_q, tail_false_q = exact_tail_cap(a_q, b_q, alpha_q)
    tail_true, tail_false = float(tail_true_q), float(tail_false_q)
    u, w, kl_true, kl_false = log_lr_parameters(a, b)
    expected_upper_true = (math.log(1.0 / alpha) - w) / kl_true
    expected_upper_false = (math.log(1.0 / alpha) + u) / kl_false
    true_dp = capped_lr_dp(n_cap, a, a, b, alpha, alpha)
    false_dp = capped_lr_dp(n_cap, b, a, b, alpha, alpha)
    m2 = parameters.m * parameters.m

    bounds = BatchBounds(
        c_m=str(c_m),
        p_true_max=a,
        p_false_min=b,
        gap=gap,
        alpha_each=alpha,
        hoeffding_batches=fixed,
        cap_batches=n_cap,
        cap_tail_true=tail_true,
        cap_tail_false=tail_false,
        kl_true=kl_true,
        kl_false=kl_false,
        expected_upper_true=expected_upper_true,
        expected_upper_false=expected_upper_false,
    )
    return {
        "status": "exact_binomial_cap_and_finite_state_expected_stop_benchmark",
        "parameters": asdict(parameters),
        "bounds": asdict(bounds),
        "endpoint_dp": {
            "true_candidate_at_p_a": true_dp,
            "false_candidate_at_p_b": false_dp,
        },
        "logical_ordered_pair_request_bounds": {
            "per_batch_max": m2,
            "fixed_hoeffding_cap": fixed * m2,
            "sequential_hard_cap": n_cap * m2,
            "all_slots_fixed_hoeffding_cap": slots * fixed * m2,
            "all_slots_sequential_hard_cap": slots * n_cap * m2,
            "sequential_expected_true_endpoint": true_dp["expected_batches"] * m2,
            "sequential_expected_false_endpoint": false_dp["expected_batches"] * m2,
        },
        "ledger": {
            "number_of_potential_candidate_tests": slots,
            "false_accept_sum_bound": slots * alpha,
            "true_reject_sum_bound": slots * alpha,
            "cap_unknown_sum_bound": slots * alpha,
            "total_validation_failure_or_unknown_bound": min(
                1.0, 3.0 * slots * alpha
            ),
        },
        "limits": [
            "Endpoint score streams are the exact Bernoulli worst-case mean models, not simulated comparator batches.",
            "The matching batch itself still costs at most m^2 ordered pair requests; cache hits and unique source calls are separate.",
            "The result is conditional on a frozen candidate of admitted degree d, a correct prefix, fresh independent batch randomness, and a fixed comparator.",
        ],
    }


def main() -> None:
    params = Parameters(
        degree=2,
        epsilon="0.0331",
        m=11,
        candidate_slots=1000,
        validation_budget="0.05",
    )
    result = benchmark(params)
    out = Path(__file__).with_name("sequential_matching_receipt.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
