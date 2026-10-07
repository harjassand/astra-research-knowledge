"""Exact finite check: one-time statistics do not fix a product-growth rate."""
from fractions import Fraction

orbit = (Fraction(2), Fraction(1, 2))
mean_log_terms = (0, 0)  # log(2) and log(1/2) cancel exactly over one orbit.
mean_square = sum((x * x for x in orbit), Fraction()) / len(orbit)
assert mean_square == Fraction(17, 8)
for m in range(2, 102, 2):
    product = Fraction(1)
    for j in range(m):
        product *= orbit[j % 2]
    assert product == 1
# Thus lim_m (1/m) log(product) = 0, while the independent/lognormal
# one-marginal expression (1/4) log(E[f^2]) is strictly positive.
assert mean_log_terms == (0, 0)
assert mean_square > 1
print({"even_products": 50, "all_equal_one": True,
       "stationary_cycle_mean_f_squared": str(mean_square),
       "actual_asymptotic_rate": "0",
       "independent_formula": "(1/4) log(17/8) > 0"})
