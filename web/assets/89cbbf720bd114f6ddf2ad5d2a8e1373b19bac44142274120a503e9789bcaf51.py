from fractions import Fraction as F
from math import isqrt
import json


def ceil_sqrt_fraction(x: F) -> int:
    assert x >= 0
    n, d = x.numerator, x.denominator
    j = isqrt(n // d)
    while j * j * d < n:
        j += 1
    while j > 0 and (j - 1) * (j - 1) * d >= n:
        j -= 1
    return j


m = 1
A = F(2, 1)
epsilon = F(1, 1000)
assert m >= 1 and A >= 1 and epsilon > 0

moment_bracket = (
    F(3)
    + 21 * A * m
    + 27 * A**2 * m * (m + 2)
    + 9 * A**3 * m * (m + 2) * (m + 4)
)
M_upper = F(484, 49) * moment_bracket
J = max(4, ceil_sqrt_fraction(F(8 * m, 1) * M_upper / epsilon))
assert F(8 * m, 1) * M_upper / (J * J) <= epsilon
labels = J**m

result = {
    "status": "PASS_EXACT_RATIONAL_COST_ARITHMETIC",
    "dimension_m": m,
    "covariance_spectrum_interval": ["1", str(A)],
    "epsilon": str(epsilon),
    "pi_squared_upper": "484/49",
    "M_upper": str(M_upper),
    "mesh_cells_per_coordinate_J": J,
    "total_labels_D": labels,
    "verified_inequality": "8*m*M_upper/J^2 <= epsilon",
    "scope": "Checks rational label-count arithmetic only; the derivative theorem is proved in R2.txt.",
    "limitations": [
        "fixed dimension only; D grows as epsilon^(-m/2)",
        "ideal real Cauchy CDF, inverse CDF, and continuous sampling",
        "does not bound mutual information or solve the scale integral",
        "does not establish external priority"
    ]
}
print(json.dumps(result, indent=2))
