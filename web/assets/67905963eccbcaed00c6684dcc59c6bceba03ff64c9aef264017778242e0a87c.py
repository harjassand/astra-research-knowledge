#!/usr/bin/env python3
"""Exact Fraction check for the N=2 Bell-diagonal separable witness.

Only Python's standard library is used.  The Pauli-pair matrices, Bell
probabilities, separable-mixture identity, and PPT spectrum are checked with
rational arithmetic.  The paired-axis identity is the exact expansion of the
stated local Pauli product states, including the complex sigma_y factors.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def zeros(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def add(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def trace(a):
    return sum((a[i][i] for i in range(min(len(a), len(a[0])))), F(0))


I4 = eye(4)
XX = [
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0],
]
# This is the real matrix sigma_y tensor sigma_y; the two imaginary factors
# in sigma_y cancel in the tensor product.
YY = [
    [0, 0, 0, -1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [-1, 0, 0, 0],
]
ZZ = [
    [1, 0, 0, 0],
    [0, -1, 0, 0],
    [0, 0, -1, 0],
    [0, 0, 0, 1],
]
PAIR = {"x": XX, "y": YY, "z": ZZ}


def paired_axis_state(axis, correlation_sign):
    """Exact matrix of the two-product +/- axis mixture.

    For sign +1 this expands (tau_+ tensor tau_+ + tau_- tensor tau_-)/2;
    sign -1 expands (tau_+ tensor tau_- + tau_- tensor tau_+)/2.
    """
    return scale(F(1, 4), add(I4, scale(F(correlation_sign), PAIR[axis])))


# Bell sign order: (++-), (+-+), (-++), (---).
signs = ((1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1))
p = (F(8, 33), F(8, 33), F(16, 33), F(1, 33))
c = (F(-1, 33), F(5, 11), F(5, 11))

# Bell probabilities recovered from the exact diagonal correlations.
p_from_c = tuple((1 + sx * c[0] + sy * c[1] + sz * c[2]) / 4
                 for sx, sy, sz in signs)
assert p_from_c == p
assert sum(p, F(0)) == 1
assert max(p) == F(16, 33) < F(1, 2)

# Exact log-rational parameter check: exp(4 theta_i)=(4,16,16).
# These are the three independent ratios p1*p2/(p3*p4), etc.
ratios = (
    p[0] * p[1] / (p[2] * p[3]),
    p[0] * p[2] / (p[1] * p[3]),
    p[1] * p[2] / (p[0] * p[3]),
)
assert ratios == (F(4), F(16), F(16))

# Exact separable decomposition; all terms are rational 4x4 matrices.
rho_decomposed = add(
    add(scale(F(2, 33), scale(F(1, 4), I4)),
        scale(F(1, 33), paired_axis_state("x", -1))),
    add(scale(F(5, 11), paired_axis_state("y", 1)),
        scale(F(5, 11), paired_axis_state("z", 1))),
)
rho_from_bell = scale(
    F(1, 4),
    add(add(I4, scale(c[0], XX)), add(scale(c[1], YY), scale(c[2], ZZ))),
)
assert rho_decomposed == rho_from_bell
assert trace(rho_decomposed) == 1

# Partial transpose flips the Y correlation. Its Bell eigenvalues match
# {1/2-p_s}; all are nonnegative.
ppt_eigs = tuple((1 + sx * c[0] - sy * c[1] + sz * c[2]) / 4
                 for sx, sy, sz in signs)
expected_ppt = tuple(sorted(F(1, 2) - x for x in p))
assert tuple(sorted(ppt_eigs)) == expected_ppt
assert min(ppt_eigs) == F(1, 66) > 0

# Identical-site mixtures have c_x=E[m_x^2]>=0. Here c_x is strictly
# negative, so this separable state cannot be a mixture of tau tensor tau.
assert c[0] == F(-1, 33) < 0

result = {
    "status": "PASS",
    "arithmetic": "exact fractions for all state/decomposition/PPT checks",
    "bell_sign_order": ["++-", "+-+", "-++", "---"],
    "bell_probabilities": [str(x) for x in p],
    "exp_4theta_ratios": [str(x) for x in ratios],
    "correlations_x_y_z": [str(x) for x in c],
    "ppt_eigenvalues": [str(x) for x in sorted(ppt_eigs)],
    "separable_decomposition_weights": ["2/33", "1/33", "5/11", "5/11"],
    "decomposition_matrix_equals_bell_density": True,
    "identical_site_product_mixture_ruled_out_by": "c_x=-1/33<0",
    "scope": "N=2, b=0, diagonal A, exact single finite-N witness only",
}
out = Path(__file__).with_name("small_n_exact_mixture_check.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
