#!/usr/bin/env python3
"""Exact reversible kernel where b=0 works but the all-a,b claim fails."""
from fractions import Fraction as Q
from itertools import product
import json

states = tuple(product((0, 1), repeat=2))
mu = {z: Q(1, 4) for z in states}

def theta(z):
    x, y = z
    return (1 - y, 1 - x)

def swap(z):
    x, y = z
    return (y, x)

def dirichlet(phi):
    return sum(mu[z] * (phi(z) - phi(theta(z))) ** 2 for z in states) / 2

def variance_binary(f):
    mean = (f[0] + f[1]) / 2
    return sum((f[x] - mean) ** 2 for x in (0, 1)) / 2

restricted_checks = 0
for a0, a1 in product(range(-3, 4), repeat=2):
    f = {0: Q(a0), 1: Q(a1)}
    local = dirichlet(lambda z: f[z[0]])
    var = variance_binary(f)
    assert local == var
    restricted_checks += 1

f1 = {0: Q(0), 1: Q(1)}
f2 = {0: Q(0), 1: Q(-1)}
additive = lambda z: f1[z[0]] + f2[z[1]]
companion_energy = dirichlet(additive)
companion_variance = variance_binary(f1)
assert companion_energy == 0
assert companion_variance == Q(1, 4)

# Testing only the diagonal choice f1=f2 also misses a zero-energy direction.
same_function_energy = sum(
    mu[z] * (Q(z[0] + z[1]) - Q(sum(swap(z)))) ** 2 / 2
    for z in states
)
assert same_function_energy == 0

result = {
    "status": "PASS_EXACT_RATIONAL_ARITHMETIC",
    "kernel": "(x,y) -> (1-y,1-x), deterministic involution on uniform {0,1}^2",
    "restricted_b_zero_assignments_checked": restricted_checks,
    "restricted_identity": "E_K(a(X)) = Var(a(X)) for every a on {0,1}",
    "companion_functions": {"f1": ["0", "1"], "f2": ["0", "-1"]},
    "all_additive_energy": str(companion_energy),
    "target_variance": str(companion_variance),
    "swap_same_function_energy": str(same_function_energy),
    "swap_same_function_variance": str(Q(1, 4)),
    "conclusion": "A bound tested only with b=0 does not imply the required all-a,b inequality."
}
print(json.dumps(result, indent=2))
