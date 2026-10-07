#!/usr/bin/env python3
"""Exact additive-energy block matrices for two binary pair kernels."""
from fractions import Fraction as Q
from itertools import product
import json

states = tuple(product((0, 1), repeat=2))
mu = {z: Q(1, 4) for z in states}

def theta(z):
    x, y = z
    return (1 - y, 1 - x)

def parity_kernel(z):
    p = sum(z) % 2
    targets = [w for w in states if sum(w) % 2 == p]
    return {w: Q(1, len(targets)) for w in targets}

def involution_kernel(z):
    return {theta(z): Q(1)}

def dirichlet(kernel, alpha, beta):
    def phi(z):
        x, y = z
        return alpha * Q(2 * x - 1) + beta * Q(2 * y - 1)
    value = Q(0)
    for z in states:
        for w, p in kernel(z).items():
            value += mu[z] * p * (phi(z) - phi(w)) ** 2 / 2
    return value

def block_matrix(kernel):
    A = dirichlet(kernel, Q(1), Q(0))
    C = dirichlet(kernel, Q(0), Q(1))
    both = dirichlet(kernel, Q(1), Q(1))
    B = (both - A - C) / 2
    return A, B, C

results = {}
for name, kernel in (("companion_cancellation", involution_kernel),
                      ("parity_heatbath", parity_kernel)):
    A, B, C = block_matrix(kernel)
    assert C > 0
    schur = A - B * B / C
    results[name] = {
        "A": str(A), "B": str(B), "C": str(C),
        "schur_A_minus_BCinvB": str(schur)
    }

assert results["companion_cancellation"]["A"] == "1"
assert results["companion_cancellation"]["B"] == "1"
assert results["companion_cancellation"]["schur_A_minus_BCinvB"] == "0"
assert results["parity_heatbath"]["A"] == "1"
assert results["parity_heatbath"]["B"] == "0"
assert results["parity_heatbath"]["schur_A_minus_BCinvB"] == "1"

print(json.dumps({
    "status": "PASS_EXACT_RATIONAL_ARITHMETIC",
    "centered_basis": "u(x)=2x-1, v(y)=2y-1",
    "matrices": results,
    "interpretation": "All-a,b coercivity is the Schur complement; positive Schur complement still does not control non-additive pair modes."
}, indent=2))
