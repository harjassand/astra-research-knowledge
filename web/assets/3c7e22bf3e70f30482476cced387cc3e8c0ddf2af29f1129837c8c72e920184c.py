#!/usr/bin/env python3
"""Check constants for the exact heterogeneous half-space profile in v1.txt."""

from math import pi


R = 1.001
BETA = 1.51
EPS = 0.01

lambda_u = 105 * pi / 256
u_l2_sq = 32 / 35
hessian_u = u_l2_sq * (lambda_u - BETA)
lambda2_lower = pi / (2 * R)
inverse_gap_lower = min(BETA - lambda_u, lambda2_lower - BETA)
inverse_norm_upper = 1 / inverse_gap_lower

g_l2_sq_over_eps2_kappa2 = 18 * ((R**5 - 1) / 5 - (R**3 - 1) / 3)
inverse_correction_over_eps2_kappa = (
    inverse_norm_upper * g_l2_sq_over_eps2_kappa2
)
s_upper_over_eps2_kappa = hessian_u + inverse_correction_over_eps2_kappa

# On |x|<=1 the dimensionless direct-effect coefficient divided by eps*kappa
# is beta*(1-x^2)^(3/2) - 3/2 + 3*x^2. For this beta<2 it is increasing in
# x^2, so its minimum is beta-3/2. Outside, it increases from 3/2.
a_min_over_eps_kappa = BETA - 1.5
a_max_over_eps_kappa = max(1.5, 3 * R**2 - 1.5)

print(f"lambda_U/kappa upper for lambda_1: {lambda_u:.12f}")
print(f"lambda_2/kappa lower:             {lambda2_lower:.12f}")
print(f"beta:                              {BETA:.12f}")
print(f"inverse spectral gap upper:        {inverse_norm_upper:.12f}/kappa")
print(f"h[eps U]/(eps^2 kappa):            {hessian_u:.12f}")
print(f"||g||^2/(eps^2 kappa^2):            {g_l2_sq_over_eps2_kappa2:.12g}")
print(f"<g,H^-1g> upper/(eps^2 kappa):      {inverse_correction_over_eps2_kappa:.12g}")
print(f"<c,H^-1c> upper/(eps^2 kappa):      {s_upper_over_eps2_kappa:.12f}")
print(f"a_min/(eps kappa):                  {a_min_over_eps_kappa:.12f}")
print(f"a_max/(eps kappa):                  {a_max_over_eps_kappa:.12f}")
print(f"a_max/b for eps={EPS}:               {EPS*a_max_over_eps_kappa/BETA:.12f}")
print(f"max W*:                             {EPS:.12f}")

assert lambda_u < BETA < lambda2_lower
assert s_upper_over_eps2_kappa < 0
assert a_min_over_eps_kappa > 0
assert EPS * a_max_over_eps_kappa < BETA
assert EPS < 1
