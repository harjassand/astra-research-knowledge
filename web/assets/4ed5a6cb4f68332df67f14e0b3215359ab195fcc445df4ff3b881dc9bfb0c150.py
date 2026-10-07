#!/usr/bin/env python3
"""Small reproducible checks for the N75 heat bound and PI/LSI gap.

This is diagnostic arithmetic only; it does not prove the heat-flow identities
or any KLS/LSI theorem.
"""
from math import exp, log


def truncated_exp(L: float):
    z = 1.0 - exp(-L)
    mean = (1.0 - (L + 1.0) * exp(-L)) / z
    second = (2.0 - (L * L + 2.0 * L + 2.0) * exp(-L)) / z
    variance = second - mean * mean

    a = 0.5 - 1.0 / L
    zq = (L / 2.0) * (1.0 - exp(-2.0))
    eq = (L / 2.0) * (1.0 - 3.0 * exp(-2.0)) / (1.0 - exp(-2.0))
    log_c2 = log(z / zq)
    entropy = log_c2 + 2.0 * a * eq
    dirichlet = a * a
    lsi_rho_sq_lower = entropy / (2.0 * dirichlet)
    return variance, entropy, dirichlet, lsi_rho_sq_lower


def plateau_bound(P0: float, covariance: float, s: float):
    # Integrate the differential majorant sigma^2 P0/(P0-t)^2.
    integrated = covariance * P0 * (1.0 / (P0 - s) - 1.0 / P0)
    claimed = covariance * s / (P0 - s)
    assert abs(integrated - claimed) <= 1e-12 * max(1.0, abs(claimed))
    return P0 + claimed


print("Heat-flow integrated majorant checks")
for P0, sigma2, s in [(1.0, 1e-2, 0.4), (2.5, 0.03, 1.0), (10.0, 1e-4, 9.0)]:
    print(f"P0={P0:g}, sigma2={sigma2:g}, s={s:g}, upper={plateau_bound(P0, sigma2, s):.12g}")

print("\nTruncated exponential LSI test functions")
print("L, variance, entropy, Dirichlet, lower_bound_on_rho_LS_squared")
for L in (16.0, 32.0, 64.0, 128.0, 256.0):
    var, ent, energy, rho2 = truncated_exp(L)
    print(f"{L:5.0f}, {var:.12g}, {ent:.12g}, {energy:.12g}, {rho2:.12g}")
    assert 0.9 < var < 1.1
    assert ent > 0 and rho2 > 0
