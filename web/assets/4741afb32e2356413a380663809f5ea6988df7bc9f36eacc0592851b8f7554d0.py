"""Exact rational axial N=6 counter; no floating PSD solver is used."""
from fractions import Fraction as F
from math import comb, log
import json
from pathlib import Path

x = F(19, 25)
q = [x ** ((k - 3) ** 2) / comb(6, k) for k in range(7)]
a, b, c, d = q[:4]
det_odd = (a - d) * (c - d) - (b - c) ** 2
r, s = -(b - c), a - d
v_hankel = [r, s, -s, -r]
quad = sum(v_hankel[i] * q[i + j] * v_hankel[j]
           for i in range(4) for j in range(4))
assert quad == 2 * (a - d) * det_odd < 0
adjacent = [q[k - 1] * q[k + 1] - q[k] ** 2 for k in range(1, 6)]
assert all(z > 0 for z in adjacent)

# In the 3|3 partial-transpose difference-zero block, B=D H0 D,
# D_ii=binom(3,i). Divide the Hankel vector by D to obtain its physical vector.
v_pt = [v_hankel[i] / comb(3, i) for i in range(4)]
pt_quad = sum(v_pt[i] * comb(3, i) * q[i + j] * comb(3, j) * v_pt[j]
              for i in range(4) for j in range(4))
assert pt_quad == quad
norm2 = sum(z * z for z in v_pt)
Z_sym = sum(comb(6, k) * q[k] for k in range(7))
nu = -quad / (Z_sym * norm2)
assert nu > 0

# alpha=40 log 2 and delta=6 log(25/19). From the exact spin gap,
# T(full rho, symmetric rho)<=2^N/(N+1) exp(-alpha+delta*N/4).
alpha_power = 40
trace_distance_bound = F(64, 7) * x ** (-9) * F(1, 2 ** alpha_power)
assert 2 * trace_distance_bound < nu

def frac(z):
    return {"numerator": str(z.numerator), "denominator": str(z.denominator),
            "diagnostic_decimal": float(z)}

report = {
    "status": "EXACT_RATIONAL_NPT_COUNTER_CERTIFICATE",
    "N": 6,
    "alpha_exact": "40 log 2",
    "delta_exact": "6 log(25/19)",
    "alpha_diagnostic": alpha_power * log(2),
    "delta_diagnostic": 6 * log(25 / 19),
    "x": frac(x),
    "q": [frac(z) for z in q],
    "strict_adjacent_logconvex_minors": [frac(z) for z in adjacent],
    "odd_hankel_determinant": frac(det_odd),
    "hankel_negative_vector": [frac(z) for z in v_hankel],
    "physical_PT_negative_vector_unnormalized": [frac(z) for z in v_pt],
    "hankel_and_PT_quadratic_form": frac(quad),
    "symmetric_normalizer": frac(Z_sym),
    "physical_vector_norm_squared": frac(norm2),
    "normalized_witness_negativity_nu": frac(nu),
    "finite_alpha_trace_distance_upper_bound": frac(trace_distance_bound),
    "strict_finite_alpha_witness_margin": frac(nu - 2 * trace_distance_bound),
    "scope": "Whole six-qubit Gibbs state is NPT across 3|3. Adjacent log-convexity is strictly satisfied in the symmetric limit. This does not refute a uniform positive radius <=2 log 2.",
}
target = Path(__file__).with_suffix(".json")
target.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: report[k] for k in ("status", "N", "alpha_exact", "delta_exact", "delta_diagnostic", "odd_hankel_determinant", "normalized_witness_negativity_nu", "strict_finite_alpha_witness_margin")}, indent=2))
