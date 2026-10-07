#!/usr/bin/env python3
"""Exact finite audits for local additive energy versus pair/global mixing."""
from fractions import Fraction as Q
from itertools import product
import json

STATES = tuple(product((0, 1), repeat=2))
UNIFORM_PAIR = {z: Q(1, 4) for z in STATES}


def parity_kernel(z):
    parity = sum(z) % 2
    targets = [w for w in STATES if sum(w) % 2 == parity]
    return {w: Q(1, len(targets)) for w in targets}


def dirichlet(mu, kernel, value):
    total = Q(0)
    for z, pz in mu.items():
        for w, qzw in kernel(z).items():
            total += pz * qzw * (value(z) - value(w)) ** 2
    return total / 2


def variance(values, weights):
    mean = sum(weights[x] * values[x] for x in weights)
    return sum(weights[x] * (values[x] - mean) ** 2 for x in weights)


def product_heatbath_kernel(pi):
    return lambda _z: {
        (x, y): pi[x] * pi[y]
        for x in (0, 1)
        for y in (0, 1)
    }


# Exact check of every two-point f1,f2 with values in {-2,...,2}.
# This finite grid corroborates the algebraic identity E=(a^2+b^2)/4.
checked = 0
for u0, u1, v0, v1 in product(range(-2, 3), repeat=4):
    f1 = {0: Q(u0), 1: Q(u1)}
    f2 = {0: Q(v0), 1: Q(v1)}
    additive = {(x, y): f1[x] + f2[y] for x, y in STATES}
    e = dirichlet(UNIFORM_PAIR, parity_kernel, additive.__getitem__)
    var_f1 = variance(f1, {0: Q(1, 2), 1: Q(1, 2)})
    assert var_f1 <= e
    slope1, slope2 = Q(u1 - u0), Q(v1 - v0)
    assert e == (slope1 * slope1 + slope2 * slope2) / 4
    checked += 1

# The full pair chain has a nonconstant invariant: parity.
parity_observable = {z: Q(1 if sum(z) % 2 == 0 else -1) for z in STATES}
pair_var = variance(parity_observable, UNIFORM_PAIR)
pair_energy = dirichlet(UNIFORM_PAIR, parity_kernel, parity_observable.__getitem__)
assert pair_var == 1 and pair_energy == 0

# Endpoint-wise all-functions local inequality, but exponentially bad direct
# importance overlap for pi0 -> pi1 on a two-state space.
m = 12
eps = Q(1, 2**m)
pi0 = {0: 1 - eps, 1: eps}
pi1 = {0: eps, 1: 1 - eps}
local_checks = 0
for a0, a1, b0, b1 in product(range(-2, 3), repeat=4):
    f1 = {0: Q(a0), 1: Q(a1)}
    f2 = {0: Q(b0), 1: Q(b1)}
    additive = {(x, y): f1[x] + f2[y] for x, y in STATES}
    for pi in (pi0, pi1):
        pair_mu = {(x, y): pi[x] * pi[y] for x, y in STATES}
        energy = dirichlet(pair_mu, product_heatbath_kernel(pi), additive.__getitem__)
        assert variance(f1, pi) <= energy
        assert energy == variance(f1, pi) + variance(f2, pi)
        local_checks += 1

weights = {x: pi1[x] / pi0[x] for x in (0, 1)}
mean_weight = sum(pi0[x] * weights[x] for x in (0, 1))
second_moment = sum(pi0[x] * weights[x] ** 2 for x in (0, 1))
relative_variance = second_moment / mean_weight**2 - 1
closed_form = (1 - 2 * eps) ** 2 / (eps * (1 - eps))
max_ratio = max(pi1[x] / pi0[x] for x in (0, 1))
assert mean_weight == 1
assert relative_variance == closed_form
assert max_ratio == (1 - eps) / eps

result = {
    "status": "PASS_EXACT_RATIONAL_ARITHMETIC",
    "parity_kernel_additive_function_assignments_checked": checked,
    "parity_kernel_local_constant": "1",
    "parity_kernel_local_energy_identity": "(slope_f1^2+slope_f2^2)/4",
    "parity_kernel_full_pair_invariant_variance": str(pair_var),
    "parity_kernel_full_pair_invariant_dirichlet": str(pair_energy),
    "heatbath_endpoint_additive_assignments_checked": local_checks,
    "importance_example_m": m,
    "importance_example_pi0": [str(pi0[0]), str(pi0[1])],
    "importance_example_pi1": [str(pi1[0]), str(pi1[1])],
    "importance_ratio_mean": str(mean_weight),
    "importance_ratio_relative_variance": str(relative_variance),
    "importance_ratio_relative_variance_decimal": float(relative_variance),
    "largest_likelihood_ratio": str(max_ratio),
    "scope": "Exact examples, not a proof for determinant-weighted kernels."
}
print(json.dumps(result, indent=2))
