"""Exact arithmetic for the deterministic-grid spectral degree certificate."""
from fractions import Fraction
from math import isqrt
import json

q = 2**61 - 1
r = 1_200_000
s = q // 10
m = q**5
N = s**5
rho = Fraction(N, m)
mu = (q-1)*rho

# For q>=18, (2 sqrt(q)+1)^2 < 5q. This check uses the stronger
# rational square-root upper bound isqrt(q)+1 rather than floating point.
root_upper = isqrt(q)+1
beta_squared_upper = (2*root_upper+1)**2
assert beta_squared_upper < 5*q

# At an exceptional vertex, |d-mu| > mu-4r^2. Sum of squared deviations
# is at most beta^2 N(1-rho). The following gives a strict rational bound.
E_fraction_upper = Fraction(beta_squared_upper)*rho*(1-rho)/(mu-4*r*r)**2
assert mu >= 8*r*r
assert E_fraction_upper < Fraction(1, 2*r)
gap_fraction_lower = rho*r/4 - 2 - r*E_fraction_upper
assert gap_fraction_lower > Fraction(1, 5)

# Positive error tolerance for the inherited permutation obstruction.
tolerance_charge_upper = rho*r/Fraction(100)
assert tolerance_charge_upper < gap_fraction_lower

# Classical Lucas-Lehmer test, prime exponent 61.
residue = 4
for _ in range(59):
    residue = (residue*residue-2) % q
assert residue == 0

print(json.dumps({
  'q': q, 'r': r, 's': s,
  'q_is_prime_by_Lucas_Lehmer': residue == 0,
  'rho_float_for_readability': float(rho),
  'mu_float_for_readability': float(mu),
  'beta_squared_upper': beta_squared_upper,
  'E_over_m_upper_float_for_readability': float(E_fraction_upper),
  'required_E_over_m': float(Fraction(1, 2*r)),
  'Delta_over_m_lower_float_for_readability': float(gap_fraction_lower),
  'm_digits': len(str(m)), 'N_digits': len(str(N)),
  'incidence_digits': len(str(N*(q-1))),
  'triangle_upper_digits': len(str(N*(q-1)*r*r)),
  'all_assertions_pass': True
}, indent=2))
