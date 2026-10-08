#!/usr/bin/env python3
"""Exact checks for actionwise CLE-equivalent offspring laws."""

from fractions import Fraction as F
from itertools import product
from math import ceil, comb, log

nu1 = [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]
nu2 = [F(1, 16), F(9, 16), F(3, 16), F(3, 16)]
nu2_rev = list(reversed(nu2))
laws = {"nu1": nu1, "nu2": nu2, "nu2_rev": nu2_rev}


def moments(pmf):
    mean = sum(F(k) * p for k, p in enumerate(pmf))
    second = sum(F(k * k) * p for k, p in enumerate(pmf))
    return mean, second, second - mean**2


def delta_moments(pmf):
    # Reaction: one R parent is replaced by K R and 3-K U daughters.
    d = [(F(k - 1), F(3 - k)) for k in range(4)]
    mean = tuple(sum(pmf[k] * d[k][i] for k in range(4)) for i in range(2))
    second = tuple(
        tuple(sum(pmf[k] * d[k][i] * d[k][j] for k in range(4)) for j in range(2))
        for i in range(2)
    )
    return mean, second


def slot_vector_prob(pmf, bits):
    k = sum(bits)
    return pmf[k] / comb(3, k)


def observed_vector_prob(pmf, observed, sensitivity, false_positive):
    total = F(0)
    for latent in product((0, 1), repeat=3):
        p_latent = slot_vector_prob(pmf, latent)
        if not p_latent:
            continue
        p_obs = F(1)
        for truth, report in zip(latent, observed):
            q = sensitivity if truth else false_positive
            p_obs *= q if report else 1 - q
        total += p_latent * p_obs
    return total


for name, pmf in laws.items():
    assert sum(pmf) == 1
    assert moments(pmf) == (F(3, 2), F(3), F(3, 4))
    assert delta_moments(pmf) == ((F(1, 2), F(3, 2)), ((F(1), F(0)), (F(0), F(3))))

# Pairwise daughter fate moments match: each slot has mean 1/2 and
# each pair has joint R probability E[K(K-1)]/(3*2)=1/4.
for pmf in laws.values():
    mean, second, _ = moments(pmf)
    factorial2 = second - mean
    assert mean / 3 == F(1, 2)
    assert factorial2 / 6 == F(1, 4)

world_plus = {"A": nu1, "B": nu2}
world_minus = {"A": nu1, "B": nu2_rev}
for action in ("A", "B"):
    for world in (world_plus, world_minus):
        assert delta_moments(world[action]) == delta_moments(nu1)

safe = lambda pmf: pmf[3]
unsafe = lambda pmf: 1 - pmf[3]
assert safe(world_plus["A"]) == F(1, 8)
assert safe(world_plus["B"]) == F(3, 16)
assert safe(world_minus["A"]) == F(1, 8)
assert safe(world_minus["B"]) == F(1, 16)
assert unsafe(world_plus["A"]) == F(7, 8)
assert unsafe(world_plus["B"]) == F(13, 16)
assert unsafe(world_minus["A"]) == F(7, 8)
assert unsafe(world_minus["B"]) == F(15, 16)

sens_plus, fp_plus = F(9, 10), F(1, 10)
sens_minus, fp_minus = F(1, 10), F(9, 10)
for action in ("A", "B"):
    for observed in product((0, 1), repeat=3):
        assert observed_vector_prob(world_plus[action], observed, sens_plus, fp_plus) == observed_vector_prob(
            world_minus[action], observed, sens_minus, fp_minus
        )

G1 = lambda z: (1 + z) ** 3 / 8
G2 = lambda z: (1 + 9 * z + 3 * z**2 + 3 * z**3) / 16
G2r = lambda z: (3 + 3 * z + 9 * z**2 + z**3) / 16
s2 = {"nu1": 1 - G1(G1(F(0))), "nu2": 1 - G2(G2(F(0))), "nu2_rev": 1 - G2r(G2r(F(0)))}
assert s2["nu1"] == F(3367, 4096)
assert s2["nu2"] == F(59085, 65536)
assert s2["nu2_rev"] == F(49621, 65536)

delta = F(1, 16)
alpha = 0.05
n_direct = ceil(log(1 / alpha) / float(delta**2))
kappa = F(4, 5)
w0 = -F(1, 8)
w1 = F(9, 8)
score_width = max(w0**3, w0**2 * w1, w0 * w1**2, w1**3) - min(
    w0**3, w0**2 * w1, w0 * w1**2, w1**3
)
n_noisy = ceil(log(1 / alpha) * float(score_width**2 / delta**2))
assert score_width == F(405, 256)
assert n_direct == 767
assert n_noisy == 1920

print({
    "shared_EK_EK2_VarK": tuple(str(x) for x in moments(nu1)),
    "shared_delta_mean_and_second_moment": tuple(
        tuple(str(x) for x in row) if isinstance(row, tuple) else str(row)
        for row in delta_moments(nu1)
    ),
    "safe_reach_plus_A_B": (str(safe(world_plus["A"])), str(safe(world_plus["B"]))),
    "safe_reach_minus_A_B": (str(safe(world_minus["A"])), str(safe(world_minus["B"]))),
    "two_generation_survival": {k: str(v) for k, v in s2.items()},
    "ranking_n_per_action_direct_gap_1_16_alpha_0.05": n_direct,
    "ranking_n_per_action_calibrated_reporter_unbiased_score": n_noisy,
    "status": "internal exact finite diagnostic; no biological validation",
})
