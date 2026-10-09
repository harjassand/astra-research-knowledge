#!/usr/bin/env python3
"""Evaluate the explicit full-tangent coercivity bound in N25 v1."""
from math import pi

R = 1.001
BETA = 1.51

lambda_u = 105 * pi / 256
alpha0 = BETA - lambda_u
delta0 = pi / (2 * R) - BETA
edge_g2 = 18 * ((R**5 - 1) / 5 - (R**3 - 1) / 3)
d0_profile = (32 / 35) * alpha0 - edge_g2 / min(alpha0, delta0)

# ||c||_2^2/(eps^2*kappa^2), integrating its exact inside and outside formulas.
c2 = (
    32 * BETA**2 / 35
    - 3 * BETA * pi / 4
    + 21 / 10
    + 2 * (9 * (R**5 - 1) / 5 - 3 * (R**3 - 1) + 9 * (R - 1) / 4)
)
theta = alpha0 * d0_profile / c2
eta_over_kappa = alpha0 * d0_profile * delta0 / c2

print(f"alpha0:                    {alpha0:.12f}")
print(f"delta0:                    {delta0:.12f}")
print(f"profile gap d0:            {d0_profile:.12f}")
print(f"C2:                        {c2:.12f}")
print(f"theta:                     {theta:.12f}")
print(f"eta/kappa:                 {eta_over_kappa:.12f}")

assert alpha0 > 0 and delta0 > 0 and d0_profile > 0
assert c2 > 0 and 0 < theta < 1 and eta_over_kappa > 0.00419
