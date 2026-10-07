#!/usr/bin/env python3
"""Exact, scoped arithmetic checks for the jump-safety appendix.

The analytic proofs in jump_safety.md and jump_safety_appendix.tex carry
the universal quantifiers. These finite checks preserve rational arithmetic,
including insufficient-reactant cases, and evaluate the certified horizon.
No long-horizon trajectory simulation or external theorem validation occurs.
"""

from fractions import Fraction as F
from itertools import product
from math import ceil, exp, factorial, prod
from pathlib import Path
import json
import random
import time


START = time.perf_counter()


def falling(n, q):
    if n < q:
        return 0
    return prod(range(n - q + 1, n + 1))


def monomial(x, y):
    return prod((v ** q for v, q in zip(x, y)), start=F(1))


def propensity(n, y, volume):
    return F(prod(falling(v, q) for v, q in zip(n, y)), volume ** sum(y))


def error_bound(upper, y):
    result = F(0)
    for j, q in enumerate(y):
        if q >= 2:
            term = F(q * (q - 1), 2) * upper[j] ** (q - 1)
            term *= prod((upper[l] ** y[l] for l in range(len(y)) if l != j),
                         start=F(1))
            result += term
    return result


factorial_checks = 0
insufficient_checks = 0
for volume in range(1, 21):
    for upper in (F(1, 2), F(3, 4), F(1), F(3, 2), F(2)):
        for count in range((upper * volume).numerator // (upper * volume).denominator + 1):
            for degree in range(9):
                x = (F(count, volume),)
                y = (degree,)
                phi = propensity((count,), y, volume)
                deficit = monomial(x, y) - phi
                assert 0 <= deficit <= error_bound((upper,), y) / volume
                positive_part = prod((max(F(count - q, volume), 0)
                                      for q in range(degree)), start=F(1))
                assert phi == positive_part
                factorial_checks += 1
                insufficient_checks += int(count < degree)

rng = random.Random(20261007)
for _ in range(5000):
    d = rng.randrange(1, 5)
    volume = rng.randrange(1, 65)
    upper = tuple(rng.choice((F(1, 2), F(3, 4), F(1), F(3, 2), F(2)))
                  for _ in range(d))
    count = tuple(rng.randrange(int(u * volume) + 1) for u in upper)
    y = tuple(rng.randrange(7) for _ in range(d))
    x = tuple(F(n, volume) for n in count)
    deficit = monomial(x, y) - propensity(count, y, volume)
    assert 0 <= deficit <= error_bound(upper, y) / volume
    factorial_checks += 1
    insufficient_checks += int(any(n < q for n, q in zip(count, y)))

theta = F(12, 25)
exp_upper = 1 + theta + theta ** 2 / (2 * (1 - theta / 3))
assert exp_upper == F(283, 175)
ratio_lower = F(529, 324)
assert exp_upper < ratio_lower
assert exp(float(theta)) < float(exp_upper)
for j in range(2, 101):
    assert factorial(j) >= 2 * 3 ** (j - 2)

assert F(3, 4) ** 2 - 4 * F(1, 4) ** 2 == F(5, 16)
assert F(23, 32) ** 2 - 4 * F(9, 32) ** 2 == F(205, 1024)
assert theta / 32 == F(3, 200)
assert theta / 4 == F(3, 25)
assert 2 * F(5, 2) * (exp_upper - 1) == F(108, 35)

volumes = list(range(2, 130, 2)) + [256, 512, 1000, 3000, 5000]
rate_corners = list(product((1, 4), repeat=2))
activity_checks = 0
facet_generator_checks = 0
for volume in volumes:
    assert F(volume // 2, volume) - F(1, 4) == F(1, 4)
    for j in range(ceil(F(volume, 4)), int(F(3 * volume, 4)) + 1):
        x = F(j, volume)
        y = 1 - x
        base_death = F(falling(j, 2), volume ** 2)
        base_birth = F(falling(volume - j, 2), volume ** 2)
        for k_a, k_b in rate_corners:
            death = k_a * base_death
            birth = k_b * base_birth
            assert birth + death <= F(5, 2)
            activity_checks += 1
            if x <= F(9, 32):
                assert birth >= exp_upper * death
                # q=e^theta upper: exact rational sufficient generator bound.
                assert birth * (1 / exp_upper - 1) + death * (exp_upper - 1) <= 0
                facet_generator_checks += 1
            if x >= F(23, 32):
                assert death >= exp_upper * birth
                assert death * (1 / exp_upper - 1) + birth * (exp_upper - 1) <= 0
                facet_generator_checks += 1

# Generic conservative certificate for the same example, independently of
# the sharper birth/death-ratio certificate above.
generic = {
    "D": F(6),
    "J": F(1),
    "B": F(9, 2),
    "Lambda": F(9, 2),
    "gamma": F(205, 1024),
}
generic["V0"] = ceil(2 * generic["D"] / generic["gamma"])
generic["theta"] = min(1 / generic["J"], generic["gamma"] / (6 * generic["B"]))
generic["c_star"] = generic["theta"] / 32
assert generic["V0"] == 60
assert generic["theta"] == F(205, 27648)
assert generic["c_star"] == F(205, 884736)

horizons = []
for volume in (1000, 2000, 3000, 5000, 10000):
    horizon = exp(3 * volume / 400)
    initial_term = 2 * exp(-3 * volume / 25)
    turnover_term = (108 / 35) * volume * exp(-3 * volume / 400)
    horizons.append({
        "V": volume,
        "time_unit": "units of the assumed reaction-rate bounds",
        "T": horizon,
        "certified_exit_bound_raw": initial_term + turnover_term,
        "probability_bound_capped_at_one": min(1, initial_term + turnover_term),
        "expected_candidate_events_upper": (5 / 2) * volume * horizon,
        "simulation_performed": False,
    })
v3000 = next(row for row in horizons if row["V"] == 3000)
assert v3000["certified_exit_bound_raw"] < 1.57e-6

# Extinction limitation example: A+B -> 2A at k=2, A -> B at k=1.
# An exact positive death rate from every j>0 and a finite state space make
# 0 accessible from every state; the proof of almost-sure absorption is
# analytic, not estimated by this finite check.
extinction_checks = 0
for volume in (6, 16, 100, 3000):
    for j in range(volume + 1):
        birth = F(2 * j * (volume - j), volume)
        death = F(j)
        assert birth >= 0 and death >= 0
        assert (birth == death == 0) if j == 0 else death > 0
        extinction_checks += 1
assert F(1, 4) * (1 - 2 * F(1, 4)) == F(1, 8)
assert -F(3, 4) * (1 - 2 * F(3, 4)) == F(3, 8)

result = {
    "status": "PASS: finite exact arithmetic only; universal theorem is proved in the appendix",
    "factorial_correction_checks": factorial_checks,
    "insufficient_reactant_checks": insufficient_checks,
    "count_activity_checks_at_rate_corners": activity_checks,
    "exact_collar_generator_checks_at_rate_corners": facet_generator_checks,
    "even_volumes_checked": volumes,
    "rational_exp_upper": str(exp_upper),
    "rational_birth_death_ratio_lower": str(ratio_lower),
    "generic_example_certificate": {k: str(v) for k, v in generic.items()},
    "optimized_certificate": {
        "theta": str(theta),
        "collar": "1/32",
        "initial_facet_gap": "1/4",
        "Lambda": "5/2",
        "exit_bound": "2 exp(-3V/25) + (108/35) V T exp(-3V/200)",
        "horizon": "exp(3V/400)",
    },
    "numerical_horizon_evaluations": horizons,
    "extinction_example_rate_checks": extinction_checks,
    "scope_limit": "No long-horizon simulation, recurrence test, release replay or external novelty validation.",
    "wall_seconds": time.perf_counter() - START,
}
destination = Path(__file__).with_suffix(".json")
destination.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
