"""Exact failure threshold and floating-point rate-transfer budget."""
from fractions import Fraction
from pathlib import Path
import json
import math

n = 80
m = 64
eta = Fraction(1, 10**6)
c = Fraction(1, 2)
exit_cap = n * c
gap = 2 * c
entropy_floor = exit_cap * eta**2 / (2 * (1 + eta))
killed_eigenvalue_upper = (m * c) / (2**m - 1)
ratio = entropy_floor / killed_eigenvalue_upper
reduced_entropy_floor = (m * c) * eta**2 / (2 * (1 + eta))
reduced_ratio = reduced_entropy_floor / killed_eigenvalue_upper
assert ratio > 115 * 10**5
assert reduced_ratio > 922 * 10**4

# Strongest ordinary reference calculation: exact Hamming-weight lumping.
difference = [Fraction(0)] * (m + 1)
difference[m] = 1 / (m * c)
for k in range(m - 1, 0, -1):
    difference[k] = (1 + (m - k) * c * difference[k + 1]) / (k * c)
mean_by_weight = [sum(difference[:k+1]) for k in range(m + 1)]
reference_mean = sum(Fraction(math.comb(m, k), 2**m - 1) * mean_by_weight[k]
                     for k in range(1, m + 1))

# Exact local Kolmogorov-square violation for the concrete triple contexts.
rate = lambda bits, i: c * (1 + eta * (-1)**sum(bits[i:i+3]))
cw = ccw = Fraction(1)
for order, which in [([0, 1, 0, 1], 'cw'), ([1, 0, 1, 0], 'ccw')]:
    bits = [0, 0, 0, 0]
    prod = Fraction(1)
    for i in order:
        prod *= rate(bits, i)
        bits[i] ^= 1
    if which == 'cw':
        cw = prod
    else:
        ccw = prod
assert cw / ccw == ((1 + eta) / (1 - eta))**2
assert cw != ccw

a0 = eta * exit_cap / (c * (1 - eta))
beta = a0 / (1 + a0)
r_beta = math.log(4 * (n - 1) / float(beta)) / (2 * float(c))
u = 2 * float(eta * exit_cap / (1 - eta)) * r_beta - math.log1p(-float(beta))
v = u - math.log1p(-float(eta))
log_f = 2 * math.asinh(math.sqrt(float(2 * exit_cap / gap)) * math.sinh(v / 2))
generic_log_factor = 3 * u + log_f
p0 = 2.0**(-m)
rare_upper_log = 2 * u + math.log((1 - p0) / (1 - math.exp(u) * p0)) + log_f
result = {
    'n': n, 'm': m, 'target': 'First m bits zero; all other bits free.',
    'eta_exact': str(eta), 'c_exact': str(c),
    'reference_exit_cap_exact': str(exit_cap),
    'reference_gap_exact': str(gap),
    'entropy_floor_exact': str(entropy_floor),
    'killed_eigenvalue_upper_exact': str(killed_eigenvalue_upper),
    'entropy_floor_over_eigenvalue_upper_exact': str(ratio),
    'entropy_floor_over_eigenvalue_upper_approx': float(ratio),
    'reduced_m_coordinate_entropy_floor_exact': str(reduced_entropy_floor),
    'reduced_entropy_floor_over_eigenvalue_upper_exact': str(reduced_ratio),
    'reduced_entropy_floor_over_eigenvalue_upper_approx': float(reduced_ratio),
    'stopped_path_entropy_mean_upper_bound': 'infinite',
    'ordinary_lumped_reference_mean_exact': str(reference_mean),
    'ordinary_lumped_reference_mean_approx': float(reference_mean),
    'local_square_forward_reverse_ratio_exact': str(cw / ccw),
    'actual_local_family_is_nonreversible': True,
    'beta_exact': str(beta), 'relative_mixing_horizon': r_beta,
    'stationary_log_bound': u, 'flow_log_bound': v,
    'mixed_capacity_log_factor': log_f,
    'all_target_mean_log_factor': generic_log_factor,
    'all_target_mean_factor': math.exp(generic_log_factor),
    'coarse_target_mean_upper_factor': math.exp(rare_upper_log),
    'scope': 'Exact rational entropy-divergence and nonreversibility checks; transfer scalar constants evaluated in floating point. Not a physical observation or a universal impossibility for goal-oriented relative entropy.',
}
out = Path(__file__).resolve().parent / 'entropy_comparator_results.json'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
