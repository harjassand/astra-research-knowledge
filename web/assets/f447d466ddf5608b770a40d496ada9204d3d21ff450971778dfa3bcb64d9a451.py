#!/usr/bin/env python3
"""Small numerical audit for the finite-jet archive counterexample.

The proof uses 3-point Gauss-Legendre quadrature on each coordinate, which is
exact through degree 5. This script checks the m=2, K=3 instance: moments
through K+2, Fisher-metric derivatives through order K, positivity, and the
archive lower-bound scaling for the continuous experiment.
"""

from itertools import product
from math import factorial, log2, sqrt
import json


NODES = [-sqrt(3.0 / 5.0), 0.0, sqrt(3.0 / 5.0)]
WEIGHTS = [5.0 / 18.0, 4.0 / 9.0, 5.0 / 18.0]  # normalized for Unif[-1,1]
M = 2
K = 3
MOMENT_DEGREE = K + 2
TAU = 1.0 / (4.0 * sqrt(M))


def continuous_1d(power):
    return 0.0 if power % 2 else 1.0 / (power + 1)


def discrete_1d(power):
    return sum(w * x**power for x, w in zip(NODES, WEIGHTS))


def moment(exponents, one_d):
    out = 1.0
    for exponent in exponents:
        out *= one_d(exponent)
    return out


def multiindices(m, max_total):
    return [a for a in product(range(max_total + 1), repeat=m) if sum(a) <= max_total]


moment_error = 0.0
for alpha in multiindices(M, MOMENT_DEGREE):
    moment_error = max(
        moment_error,
        abs(moment(alpha, continuous_1d) - moment(alpha, discrete_1d)),
    )


fisher_jet_error = 0.0
fisher_jet_count = 0
for i in range(M):
    for j in range(M):
        for alpha in multiindices(M, K):
            q = sum(alpha)
            exponents = list(alpha)
            exponents[i] += 1
            exponents[j] += 1
            derivative_factor = (
                (-1) ** q
                * factorial(q)
                / __import__("math").prod(factorial(a) for a in alpha)
                * TAU ** (q + 2)
            )
            f_cont = derivative_factor * moment(exponents, continuous_1d)
            f_disc = derivative_factor * moment(exponents, discrete_1d)
            fisher_jet_error = max(fisher_jet_error, abs(f_cont - f_disc))
            fisher_jet_count += 1


amari_error = 0.0
amari_count = 0
for order in range(1, K + 3):
    for indices in product(range(M), repeat=order):
        exponents = [indices.count(i) for i in range(M)]
        c_cont = TAU**order * moment(exponents, continuous_1d)
        c_disc = TAU**order * moment(exponents, discrete_1d)
        amari_error = max(amari_error, abs(c_cont - c_disc))
        amari_count += 1


# Uniform positivity follows analytically from tau * ||v||_2 * ||x||_2 <= 1/4.
# This finite grid checks the endpoint of that bound for the discrete support.
max_tau_dot_on_atoms = max(
    TAU * sqrt(x0 * x0 + x1 * x1)
    for x0, x1 in product(NODES, repeat=M)
)
positivity_lower = 1.0 - 0.25
positivity_upper = 1.0 + 0.25

atom_count = len(NODES) ** M
epsilons = [1e-3, 1e-6, 1e-9]
continuous_lower_bits = {
    str(eps): (M / 2.0) * log2(TAU / (2.0 * 3.141592653589793 * 2.718281828459045 * eps))
    for eps in epsilons
}

result = {
    "m": M,
    "K": K,
    "gauss_nodes_per_coordinate": len(NODES),
    "finite_support_atom_count": atom_count,
    "continuous_fisher_at_zero": (TAU**2) / 3.0,
    "max_moment_error_degree_le_K_plus_2": moment_error,
    "fisher_jet_derivatives_checked": fisher_jet_count,
    "max_fisher_jet_error_order_le_K": fisher_jet_error,
    "amari_tensor_entries_checked_through_order": K + 2,
    "amari_tensor_entries_checked": amari_count,
    "max_amari_tensor_error": amari_error,
    "tau_times_unit_ball_dot_bound": TAU * sqrt(M),
    "max_tau_dot_over_finite_support_and_unit_parameter_ball": max_tau_dot_on_atoms,
    "density_range_uniform_bound": [positivity_lower, positivity_upper],
    "continuous_quantum_archive_lower_bits": continuous_lower_bits,
    "finite_archive_exact_bits": log2(atom_count),
    "status": "finite numerical moment/jet audit only; theorem follows from Gauss exactness and the written entropy proof",
}

assert moment_error < 1e-14
assert fisher_jet_error < 1e-14
assert amari_error < 1e-14
assert abs(TAU * sqrt(M) - 0.25) < 1e-15
assert max_tau_dot_on_atoms <= 0.25
assert atom_count == 9
assert list(continuous_lower_bits.values())[1] > log2(atom_count)

print(json.dumps(result, indent=2, sort_keys=True))
