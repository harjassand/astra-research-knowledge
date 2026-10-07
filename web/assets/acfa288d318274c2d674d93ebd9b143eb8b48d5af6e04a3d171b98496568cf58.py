#!/usr/bin/env python3
"""Exact arithmetic check of the finite Gaussian suspension constants.

This verifies only the Hessian-threshold and selected-block arithmetic for the
closed-form example in ROOT_SUSPENSION_AUDIT.txt. The Gaussian MGF derivatives
and log-concavity proof are given analytically in that report.
"""

from fractions import Fraction as F


# mu=N(0,1), f=(x^2-1)/sqrt(2): ||Hess f||^2=2 and ||T_2 f||^2=1/2.
d_factorial_sq = F(4)
t2_norm_sq = F(1, 2)
hessian_norm_sq = F(2)
a = F(1)
b_candidate = F(3, 2)

# q^2=(d! alpha)^2/b and beta^2=4/(q^2-1).
q_sq = d_factorial_sq * t2_norm_sq / b_candidate
assert q_sq == F(4, 3)
beta_sq = F(4) / (q_sq - 1)
assert beta_sq == 12

# Source convexity threshold: N >= beta^2 ||Hess f||^2/a^2.
n_replicas = max(1, (beta_sq * hessian_norm_sq + a * a - 1) // (a * a))
assert n_replicas == 24
assert beta_sq * hessian_norm_sq / (n_replicas * a * a) <= 1

sigma_sq = 1 + F(2) / beta_sq
assert sigma_sq == F(7, 6) < q_sq
selected_cumulant_norm_sq = d_factorial_sq * t2_norm_sq / sigma_sq
assert selected_cumulant_norm_sq == F(12, 7)
assert selected_cumulant_norm_sq > b_candidate

print({
    "status": "EXACT_ARITHMETIC_SANITY_ONLY",
    "d": 2,
    "candidate_b": str(b_candidate),
    "q_squared": str(q_sq),
    "beta_squared": str(beta_sq),
    "replicas": n_replicas,
    "lifted_dimension": n_replicas + 1,
    "sigma_squared": str(sigma_sq),
    "selected_cumulant_norm_squared_lower_bound": str(selected_cumulant_norm_sq),
    "convexity_threshold_passes": True,
    "full_tensor_or_numerical_whitening_checked": False,
})
