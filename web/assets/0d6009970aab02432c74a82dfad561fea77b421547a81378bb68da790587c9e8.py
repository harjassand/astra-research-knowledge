"""Finite exact-arithmetic diagnostic for the Cycle 3 dark-count lemma.

The all-POVM proof is algebraic. This small Pauli POVM fixture checks that the
probability vectors sum to one, the nuisance backgrounds stay nonnegative and
bounded, the illuminated means match exactly, and the stated blank KL upper
bound holds numerically for one orthogonal pair.
"""

from fractions import Fraction as F
from math import log, sqrt


def kl_poisson(u: float, v: float) -> float:
    return u * log(u / v) - u + v


S = F(10, 1)
r = F(1, 160)  # r*S = 1/16
# Four-outcome qubit POVM { (I+X)/4, (I-X)/4, (I+Z)/4, (I-Z)/4 }
# evaluated on |0> and |1>.
p_x = (F(1, 4), F(1, 4), F(1, 2), F(0))
p_y = (F(1, 4), F(1, 4), F(0), F(1, 2))
assert sum(p_x) == sum(p_y) == 1
assert sum(v * v for v in p_x) <= 1
assert sum(v * v for v in p_y) <= 1

beta_x = tuple(S * (2 - p) for p in p_x)
beta_y = tuple(S * (2 - p) for p in p_y)
signal_x = tuple(S * p for p in p_x)
signal_y = tuple(S * p for p in p_y)
illum_x = tuple(a + b for a, b in zip(signal_x, beta_x))
illum_y = tuple(a + b for a, b in zip(signal_y, beta_y))
assert illum_x == illum_y == (2 * S,) * 4
assert all(S <= b <= 2 * S for b in beta_x + beta_y)

blank_kl = sum(
    kl_poisson(float(r * a), float(r * b)) for a, b in zip(beta_x, beta_y)
)
tv_bound = sqrt(blank_kl / 2)
assert blank_kl <= float(2 * r * S) + 1e-14
assert tv_bound <= 0.25 + 1e-14

print({
    "p_x": [str(v) for v in p_x],
    "p_y": [str(v) for v in p_y],
    "signal_laws_equal": illum_x == illum_y,
    "background_bounds": [str(min(beta_x + beta_y)), str(max(beta_x + beta_y))],
    "blank_kl": blank_kl,
    "analytic_kl_upper": float(2 * r * S),
    "pinsker_tv_upper_from_numeric_kl": tv_bound,
    "mean_test_error_lower": (1 - tv_bound) / 2,
    "analytic_tv_upper": 0.25,
    "analytic_average_test_error_lower": 0.375,
})
