#!/usr/bin/env python3
"""Independent exact qubit reconstruction and fixed-epsilon certificate.

Different implementation from the root replay: exact Fraction interval
endpoints throughout; E reduced to one rational Mobius function of sqrt(det).
Only the final exported decimal-rational enclosure is rounded outward.
This is executable exact arithmetic, not proof-assistant formalization.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import hashlib
import json


def matrix(a):
    return [[F(x) for x in row] for row in a]


def plus(a, b):
    return [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]


def times(c, a):
    return [[c * x for x in row] for row in a]


def product(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]


def trace(a):
    return a[0][0] + a[1][1]


def pairing(a, b):
    return trace(product(a, b))


def determinant(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


I = matrix([[1, 0], [0, 1]])
P = [times(F(1, 25), matrix([[9, 12], [12, 16]])),
     times(F(1, 25), matrix([[16, -12], [-12, 9]]))]
prepared = [times(F(1, 265), matrix([[9, 48], [48, 256]])),
            times(F(1, 10), matrix([[1, -3], [-3, 9]]))]
sigma = times(F(1, 17), matrix([[1, 0], [0, 16]]))
sqrt_sigma_unscaled = matrix([[1, 0], [0, 4]])
quarter_unscaled = matrix([[1, 0], [0, 2]])
inverse_quarter_unscaled = matrix([[1, 0], [0, F(1, 2)]])


def phi(a):
    return plus(times(pairing(P[0], a), prepared[0]),
                times(pairing(P[1], a), prepared[1]))


def phi_adjoint(a):
    return plus(times(pairing(prepared[0], a), P[0]),
                times(pairing(prepared[1], a), P[1]))


def weighted_T(a):
    z = product(product(quarter_unscaled, a), quarter_unscaled)
    z = phi(z)
    return product(product(inverse_quarter_unscaled, z), inverse_quarter_unscaled)


assert plus(P[0], P[1]) == I
assert phi(sigma) == sigma
assert phi_adjoint(I) == I
for p, z in zip(P, prepared):
    assert product(p, p) == p and trace(p) == 1
    assert determinant(z) == 0 and trace(z) == 1 and z[0][0] > 0
    r = pairing(sigma, p)
    assert r > 0
    assert times(F(1, 17), product(product(sqrt_sigma_unscaled, p),
                                 sqrt_sigma_unscaled)) == times(r, z)

basis = [matrix([[1, 0], [0, 0]]), matrix([[0, 1], [0, 0]]),
         matrix([[0, 0], [1, 0]]), matrix([[0, 0], [0, 1]])]
for x in basis:
    gamma_x = times(F(1, 17), product(product(sqrt_sigma_unscaled, x),
                                    sqrt_sigma_unscaled))
    gamma_adjoint_x = times(F(1, 17), product(product(sqrt_sigma_unscaled,
                                                     phi_adjoint(x)),
                                            sqrt_sigma_unscaled))
    assert phi(gamma_x) == gamma_adjoint_x
columns = [sum(weighted_T(x), []) for x in basis]
T4 = [[columns[j][i] for j in range(4)] for i in range(4)]
assert all(T4[i][j] == T4[j][i] for i in range(4) for j in range(4))
assert weighted_T(sqrt_sigma_unscaled) == sqrt_sigma_unscaled
expected_T = [
    [F(101, 1325), F(-84, 1325), F(-84, 1325), F(306, 1325)],
    [F(-84, 1325), F(306, 1325), F(306, 1325), F(21, 1325)],
    [F(-84, 1325), F(306, 1325), F(306, 1325), F(21, 1325)],
    [F(306, 1325), F(21, 1325), F(21, 1325), F(2497, 2650)],
]
assert T4 == expected_T
# The independent rank-two frame formula and fixed eigenvector imply the
# remaining nonzero eigenvalue from the trace. Confirm that value exactly.
assert sum(T4[i][i] for i in range(4)) - 1 == F(1273, 2650)
assert phi(basis[0])[0][1] == F(-168, 1325)
gns_left = trace(product(product(sigma, basis[0]), phi_adjoint(basis[1])))
gns_right = trace(product(product(sigma, phi_adjoint(basis[0])), basis[1]))
assert gns_left == F(-168, 22525) and gns_right == F(-672, 22525)
transition = [[pairing(p, z) for z in prepared] for p in P]
assert all(x > 0 for row in transition for x in row)

X = times(F(1, 17), matrix([[-4, 1], [1, 4]]))
# Dsqrt_sigma[X] = Q/sqrt(17); Dlog_sigma[X]=A+ln2*B.
Q = matrix([[-2, F(1, 5)], [F(1, 5), F(1, 2)]])
log_A = matrix([[-4, 0], [0, F(1, 4)]])
log_B = matrix([[0, F(4, 15)], [F(4, 15), 0]])
delta_X = plus(X, times(-1, phi(X)))
E_hessian = pairing(Q, plus(Q, times(-1, weighted_T(Q)))) / 17
J_hessian_constant = pairing(delta_X, log_A)
J_hessian_log2 = pairing(delta_X, log_B)
assert E_hessian == F(1088273, 4505000)
assert J_hessian_constant == F(2559, 2650)
assert J_hessian_log2 == F(-8, 337875)
assert J_hessian_constant - 4 * E_hessian == F(-349, 563125)


def sqrt_enclosure(x, decimal_places=30):
    """Exact rational endpoints bounding sqrt(x), using integer squares."""
    assert x >= 0
    scale = 10 ** decimal_places
    a = isqrt(x.numerator * scale * scale // x.denominator)
    lo = F(a, scale)
    if lo * lo == x:
        return lo, lo
    hi = F(a + 1, scale)
    assert lo * lo < x < hi * hi
    return lo, hi


def positive_series_at(x, terms):
    """Exact partial sum of atanh(x)/x and exact geometric upper tail."""
    assert 0 <= x < 1
    z = x * x
    power = F(1)
    partial = F(0)
    for k in range(terms):
        partial += power / (2 * k + 1)
        power *= z
    tail = power / ((2 * terms + 1) * (1 - z))
    return partial, partial + tail


def mobius_E(s, a, b):
    return (a + b * s) / (1 + 2 * s)


epsilon = F(1, 100)
rho = plus(sigma, times(epsilon, X))
assert trace(rho) == 1 and rho[0][0] > 0 and determinant(rho) > 0
# Explicitly construct Gamma^-1(rho).
inverse_sqrt_unscaled = matrix([[1, 0], [0, F(1, 4)]])
f = times(17, product(product(inverse_sqrt_unscaled, rho), inverse_sqrt_unscaled))
assert f == matrix([[F(24, 25), F(1, 400)], [F(1, 400), F(401, 400)]])
assert determinant(f) > 0

delta = plus(rho, times(-1, phi(rho)))
assert trace(delta) == 0
radicand_r = (rho[0][0] - rho[1][1]) ** 2 + 4 * rho[0][1] ** 2
r_lo, r_hi = sqrt_enclosure(radicand_r)
A_lo = positive_series_at(r_lo, 200)[0]
A_hi = positive_series_at(r_hi, 200)[1]
L_lo, L_hi = positive_series_at(F(1, 3), 40)
log2_lo, log2_hi = F(2, 3) * L_lo, F(2, 3) * L_hi
J_mult = pairing(delta, plus(times(2, rho), times(-1, I)))
log2_mult = 4 * delta[1][1]
assert J_mult > 0 and log2_mult > 0
J_lo = J_mult * A_lo - log2_mult * log2_hi
J_hi = J_mult * A_hi - log2_mult * log2_lo

# sqrt(rho)=(rho+sI)/sqrt(1+2s). Self-adjointness of T makes its
# quadratic numerator A+2sB+s^2C. No interval matrix multiplication.
det = determinant(rho)
s_lo, s_hi = sqrt_enclosure(det)
A = pairing(rho, weighted_T(rho))
B = pairing(rho, weighted_T(I))
C = pairing(I, weighted_T(I))
E_a = 1 - A - det * C
E_b = 2 * (1 - B)
derivative_numerator = E_b - 2 * E_a
endpoints = [mobius_E(s_lo, E_a, E_b), mobius_E(s_hi, E_a, E_b)]
E_lo, E_hi = min(endpoints), max(endpoints)
gap_lo, gap_hi = J_lo - 4 * E_hi, J_hi - 4 * E_lo
assert E_lo > 0 and gap_hi < 0
assert gap_hi < -F(7, 10**8)

workspace = Path(__file__).resolve().parents[4]
root_json = workspace / 'work/agents/root_cycle06/replay_kms_c4_root.json'
root_data = json.loads(root_json.read_text())
root_state = next(x for x in root_data['fixed_states'] if x['epsilon'] == '1/100')


def source_bounds(d):
    return F(int(d['lower_numerator']), int(d['denominator'])), \
        F(int(d['upper_numerator']), int(d['denominator']))


for key, lo, hi in [('J', J_lo, J_hi), ('E', E_lo, E_hi),
                    ('J_minus_4E', gap_lo, gap_hi)]:
    source_lo, source_hi = source_bounds(root_state[key])
    assert lo <= source_lo <= source_hi <= hi, key


def export_enclosure(lo, hi, places=25):
    """Round outward only for compact JSON; analytic endpoints remain exact."""
    scale = 10 ** places
    low = lo.numerator * scale // lo.denominator
    high = -((-hi.numerator * scale) // hi.denominator)
    assert F(low, scale) <= lo <= hi <= F(high, scale)
    return {'lower_numerator': str(low), 'upper_numerator': str(high),
            'denominator': str(scale)}


result = {
    'scope': 'Independent exact rational certificate; not formal/external validation.',
    'epsilon': str(epsilon),
    'rho': [[str(x) for x in row] for row in rho],
    'positive_relative_density_f': [[str(x) for x in row] for row in f],
    'channel_and_stationarity_checks': True,
    'weighted_T_matrix_and_eigenvalue_checks': True,
    'gns_pairing_mismatch': [str(gns_left), str(gns_right)],
    'positive_two_step_transition_matrix': [[str(x) for x in row] for row in transition],
    'E_second_coefficient': str(E_hessian),
    'J_second_coefficients_constant_log2': [str(J_hessian_constant), str(J_hessian_log2)],
    'gap_second_coefficients_constant_log2': [str(J_hessian_constant - 4 * E_hessian), str(J_hessian_log2)],
    'E_closed_form': {'a': str(E_a), 'b': str(E_b),
                      'formula': '(a+b*sqrt(det(rho)))/(1+2*sqrt(det(rho)))',
                      'monotonic_derivative_numerator': str(derivative_numerator)},
    'log2': export_enclosure(log2_lo, log2_hi),
    'J': export_enclosure(J_lo, J_hi),
    'E': export_enclosure(E_lo, E_hi),
    'J_minus_4E': export_enclosure(gap_lo, gap_hi),
    'negative_upper_bound_verified': True,
    'root_epsilon_1_100_intervals_contained': True,
    'root_json_sha256_at_comparison': hashlib.sha256(root_json.read_bytes()).hexdigest(),
    'method': 'Integer-square radical bounds at 10^-30, exact Fraction series (200 terms for state,40 for log2), positive geometric tails; Mobius E monotonicity; final outward export at 10^-25.'
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
