#!/usr/bin/env python3
"""Floating-point checks of the analytically derived Bargmann dark vector.

This checks finite coefficient identities and convergence of a square norm.
It does not prove injectivity, noninjectivity beyond the stated analytic domain,
entropy continuity, or a quantum-capacity claim.
"""
import cmath
import json
import math

eta = 0.75
nu = 1.0
rho = 0.3
G = 1.0 + (1.0 - eta) * nu
a = 1.0 - eta / G
c = math.sqrt(eta) / G
d = math.sqrt((G - 1.0) / G)
t = -math.sqrt(a) * d / c
alpha = 1.0 - t * t
lam = c / d + math.sqrt(a) * t
R = lam * lam / alpha
C = lam * d


def psi(n):
    return math.sqrt(1.0 - rho) * rho ** (n / 2.0) * cmath.exp(
        1j * (0.731 * n * n + 0.119 * n * n * n)
    )


def signed_power(z, n):
    return z ** n


def dark_coefficient(l, k):
    # In normalized Bargmann monomials x^l y^k/sqrt(l! k!).
    n = k - l + 1
    if n < 0:
        return 0.0j
    fac = math.exp(
        0.5 * (math.lgamma(l + 1) + math.lgamma(k + 1) - math.lgamma(n + 1))
    )
    first = 0.0
    second = 0.0
    if l >= 1:
        first = lam ** n * signed_power(t, l - 1) / math.factorial(l - 1)
    if n >= 1:
        second = (
            -math.sqrt(a)
            * n
            * lam ** (n - 1)
            * signed_power(t, l)
            / math.factorial(l)
        )
    return psi(n) * fac * (first + second)


def kraus_amplitude(n, l, k):
    if l > n or k < 0:
        return 0.0
    m = n - l + k
    log_combinatorial = 0.5 * (
        math.lgamma(n + 1)
        - math.lgamma(l + 1)
        - math.lgamma(n - l + 1)
        + math.lgamma(m + 1)
        - math.lgamma(k + 1)
        - math.lgamma(n - l + 1)
    )
    return (
        math.exp(log_combinatorial)
        * a ** (l / 2.0)
        * c ** (n - l)
        * d ** k
        / math.sqrt(G)
    )


M = (1.0 - rho) / (1.0 - rho * R)
Mp = (1.0 - rho) * rho / (1.0 - rho * R) ** 2
norm_exact = M / alpha ** 2 + 4.0 * a * Mp / alpha
vacuum_image_norm_exact = (a / G) * (1.0 - rho) * rho / (1.0 - rho * C * C) ** 2
norm_checks = []
for cutoff in (8, 16, 32, 64):
    norm_cut = sum(
        abs(dark_coefficient(l, k)) ** 2
        for l in range(cutoff + 1)
        for k in range(2 * cutoff + 1)
    )
    norm_checks.append(
        {"loss_cutoff": cutoff, "amp_cutoff": 2 * cutoff,
         "norm_squared": norm_cut, "missing_norm_squared": norm_exact - norm_cut}
    )

residuals = []
for m in range(31):
    # For each fixed m only n=0,...,m+1 and l=0,...,n contribute:
    # dark_coefficient(l,k) vanishes when k-l+1<0.
    z = sum(
        psi(n)
        * kraus_amplitude(n, l, m - n + l)
        * dark_coefficient(l, m - n + l)
        for n in range(m + 2)
        for l in range(n + 1)
        if m - n + l >= 0
    )
    residuals.append(abs(z))

result = {
    "status": "floating_point_diagnostic_only",
    "parameters": {"eta": eta, "nu": nu, "rho": rho,
                   "G": G, "a": a, "c": c, "d": d,
                   "t": t, "alpha": alpha, "lambda": lam, "R": R, "C": C},
    "exact_formula_evaluated_float": {
        "dark_norm_squared": norm_exact,
        "vacuum_image_norm_squared": vacuum_image_norm_exact,
        "vacuum_leakage_lower_bound": vacuum_image_norm_exact / norm_exact,
    },
    "norm_cutoffs": norm_checks,
    "max_fixed_coefficient_kernel_residual_m_0_to_30": max(residuals),
    "fixed_coefficient_kernel_residuals": residuals,
}
print(json.dumps(result, indent=2))
