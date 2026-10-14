"""Small independent arithmetic check of the exact two-level identities.

This is a finite diagnostic, not a proof or a replay of producer code.
Only the Python standard library is used.
"""

import json
import math


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def tr(a):
    return sum(a[i][i] for i in range(len(a)))


def scale(a, s):
    return [[s * x for x in row] for row in a]


def comm(h, x):
    return sub(mm(h, x), mm(x, h))


h = [[0.0, 0.0], [0.0, 1.0]]
beta = math.log(3.0)
rho = [[0.75, 0.0], [0.0, 0.25]]
eta = 1.0
sigma_x = [[0.0, 1.0], [1.0, 0.0]]

la_x = comm(h, sigma_x)
l2a_x = comm(h, la_x)
# Here L^2(A)=A exactly, so (L^2+eta^2 I)^-1 L(A)=L(A)/2.
y_x = scale(la_x, 1.0 / (1.0 + eta * eta))
spectral_x = 2.0 * (0.75 - 0.25) / (1.0 + eta * eta)
resolvent_x = 2.0 * tr(mm(mm(rho, sigma_x), y_x))
kms_norm_x = 2.0 * (0.75 - 0.25) / beta
kms_x = beta * kms_norm_x * (1.0 / (1.0 + eta * eta))

commuting_a = [[1.0, 0.0], [0.0, -1.0]]
la_c = comm(h, commuting_a)
y_c = [[0.0, 0.0], [0.0, 0.0]]
dynamic_c = 2.0 * tr(mm(mm(rho, commuting_a), y_c))
mean_a = 0.75 * 1.0 + 0.25 * -1.0
variance_a = 0.75 * 1.0 + 0.25 * 1.0 - mean_a * mean_a
isothermal_c = beta * variance_a

tol = 1e-14
assert abs(spectral_x - resolvent_x) < tol
assert abs(spectral_x - kms_x) < tol
assert max(abs(l2a_x[i][j] - sigma_x[i][j]) for i in range(2) for j in range(2)) < tol
assert max(abs(la_c[i][j]) for i in range(2) for j in range(2)) == 0.0
assert abs(dynamic_c) < tol
assert abs(isothermal_c - 0.75 * math.log(3.0)) < tol

result = {
    "status": "finite_float_diagnostic_pass",
    "scope": "two exact two-level formulas; not proof, general validation, or source replay",
    "input": {"H": [[0, 0], [0, 1]], "beta_exact": "log(3)", "eta": 1},
    "offdiagonal_observable": "|0><1| + |1><0|",
    "offdiagonal_exact_chi": "1/2",
    "offdiagonal_spectral": spectral_x,
    "offdiagonal_kms_positive_form": kms_x,
    "offdiagonal_doubled_resolvent": resolvent_x,
    "commuting_observable": "diag(1,-1)",
    "commuting_exact_dynamic_chi": "0",
    "commuting_dynamic_resolvent": dynamic_c,
    "commuting_exact_isothermal_derivative": "3 log(3) / 4",
    "commuting_isothermal_derivative": isothermal_c,
}
print(json.dumps(result, indent=2, sort_keys=True))
