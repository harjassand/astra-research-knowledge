"""Exact integer/rational replay of one algebraic KMS-qubit upper certificate.

No random search, optimization, floating-point premise or external dependency.
Run from any cwd: python3 /absolute/path/to/check_exact_upper.py
"""
from fractions import Fraction as F
from pathlib import Path
import json


def require(condition, label):
    if not condition:
        raise AssertionError(label)
    checks[label] = True


def fraction_record(value):
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


checks = {}

# Substitute the frozen analytic Bloch coefficients exactly, keeping the two
# square roots as named basis elements rather than numerically approximating.
c, r, noise_a = F(999, 1000), F(364, 365), F(9)
C_alpha, S_alpha, h = F(5, 3), F(4, 3), F(338, 365)
energy_rational = C_alpha-1+h*c*c-S_alpha*r*c+noise_a**2*h*(1-c*c)
energy_sqrt1999 = noise_a*F(2, 1000)*(r/2-h*c)
entropy_rational = (3*r*((C_alpha-1)+(C_alpha+1)*c*c)
                    -2*c*(r*C_alpha+3*S_alpha)+2*S_alpha
                    +noise_a**2*6*r*(1-c*c))
entropy_sqrt5997 = noise_a*F(1, 1000)*(3*S_alpha+r-8*r*c)
require(energy_rational == F(2822593, 6843750), "exact_energy_rational_coefficient")
require(energy_sqrt1999 == -F(700479, 91250000), "exact_energy_radical_coefficient")
require(entropy_rational == F(311978753, 136875000), "exact_entropy_rational_coefficient")
require(entropy_sqrt5997 == -F(305181, 11406250), "exact_entropy_radical_coefficient")

# The common factor 1/sqrt(10) cancels from the Lyapunov identity.
stationary_root = [[F(3), F(0)], [F(0), F(1)]]
noise = [[F(9), F(1)], [F(1), F(-9)]]
potential = [[F(244, 3), F(9)], [F(9), F(84)]]


def matmul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(2)), F(0))
             for j in range(2)] for i in range(2)]


sv, vs = matmul(stationary_root, potential), matmul(potential, stationary_root)
lyapunov = [[(sv[i][j]+vs[i][j])/2 for j in range(2)] for i in range(2)]
require(lyapunov == matmul(matmul(noise, stationary_root), noise), "exact_Lyapunov_stationarity")

scale = 10**15
sq1999_lo = 44710177812216314
sq1999_hi = 44710177812216315
sq5997_lo = 77440299586197366
sq5997_hi = 77440299586197367
require(sq1999_lo**2 < 1999 * scale**2 < sq1999_hi**2, "sqrt1999_exact_bracket")
require(sq5997_lo**2 < 5997 * scale**2 < sq5997_hi**2, "sqrt5997_exact_bracket")
s1999_lo, s1999_hi = F(sq1999_lo, scale), F(sq1999_hi, scale)
s5997_lo, s5997_hi = F(sq5997_lo, scale), F(sq5997_hi, scale)

last = 26
log_lo = sum((F(1, (2*k+1)*4**k) for k in range(last+1)), F(0))
tail = F(4, 3*(2*last+3)*4**(last+1))
require(tail == F(1, 743093938516131840), "log_series_tail_identity")
log_hi = log_lo + tail

e_lo = F(2822593, 6843750) - F(700479, 91250000)*s1999_hi
e_hi = F(2822593, 6843750) - F(700479, 91250000)*s1999_lo
a_lo = F(311978753, 136875000) - F(305181, 11406250)*s5997_hi
a_hi = F(311978753, 136875000) - F(305181, 11406250)*s5997_lo
require(e_hi > e_lo > 0, "energy_positive_exact_interval")
require(a_hi > a_lo > 0, "entropy_coefficient_positive_exact_interval")
j_lo, j_hi = log_lo*a_lo, log_hi*a_hi
ratio_lo, ratio_hi = F(32908400, 10**7), F(32908401, 10**7)
lower_margin = j_lo-ratio_lo*e_hi
upper_margin = ratio_hi*e_lo-j_hi
require(lower_margin > 0, "strict_ratio_lower_bound")
require(upper_margin > 0, "strict_ratio_upper_bound")
require(ratio_hi < F(10, 3) < 4, "upper_below_ten_thirds_and_four")
require(1999+999**2 == 1000**2, "bloch_direction_exact_unit_length")
require(F(1, 2)*(1+F(364, 365)) == F(729, 730), "rho_large_eigenvalue")
require(F(1, 2)*(1-F(364, 365)) == F(1, 730), "rho_small_eigenvalue")
require(60766 < 249**2, "nonzero_H_eigenvalues_positive")

result = {
    "status": "PASS_EXACT_SINGLE_CERTIFICATE",
    "checks": checks,
    "ratio_interval": [str(ratio_lo), str(ratio_hi)],
    "lower_margin": fraction_record(lower_margin),
    "upper_margin": fraction_record(upper_margin),
    "scope": "Exact arithmetic replay of displayed qubit example; no universal theorem follows from this replay.",
    "external_validation": False,
    "formal_verification": False,
}
destination = Path(__file__).with_suffix(".json")
destination.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"status": result["status"], "checks_passed": len(checks), "ratio_interval": result["ratio_interval"]}, indent=2))
