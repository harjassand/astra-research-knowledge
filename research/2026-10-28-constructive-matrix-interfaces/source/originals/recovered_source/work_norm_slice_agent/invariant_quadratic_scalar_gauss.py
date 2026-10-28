#!/usr/bin/env python3
"""Two scalar Gauss sums suffice for every matrix size in the e2/trace class.

This is a separate implementation, not a modification of the parent compiler.
The exact identities and acquisition audit are in INVARIANT_QUADRATIC_AUDIT.md.
No field elements or matrices are enumerated by these functions.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_norm_frontier_agent'))
sys.path.insert(0, str(ROOT / 'work_ring_count_agent'))
from matrix_kloosterman import Field
from chain_ring_kloosterman import quadratic_sum


def polynomial_value(poly, x):
    return sum((m & x) == m for m in poly) & 1


def scalar_gauss_data(h, beta, qpoly):
    F = Field(h)
    if not 0 < beta < F.q:
        raise ValueError('the two-scalar formula requires a nonzero e2 coefficient')
    qpoly = frozenset(qpoly)
    if any(type(m) is not int or m < 0 or m.bit_length() > F.a or m.bit_count() > 2
           for m in qpoly):
        raise ValueError('expected Boolean quadratic ANF on the field coordinates')
    eta = F.pow(F.inv(beta), F.q // 2)
    G = [quadratic_sum(lambda x, epsilon=epsilon:
         polynomial_value(qpoly, x) ^
         (F.trace(F.mul(beta, F.mul(x, x))) if epsilon else 0), F.a)
         for epsilon in range(2)]
    return F, qpoly, eta, G


def two_scalar_matrix_gaussians(t, h, beta, qpoly):
    """J_r for 0<=r<=t, with exactly two Gauss problems on a field bits."""
    if type(t) is not int or t < 0:
        raise ValueError('matrix size must be a nonnegative integer')
    F, qpoly, eta, G = scalar_gauss_data(h, beta, qpoly)
    values = []
    for r in range(t + 1):
        m = r // 2
        if r % 2 == 0:
            exponent = (F.a * (m * (m - 1) // 2) +
                        polynomial_value(qpoly, eta if m % 2 else 0)) & 1
            values.append((1 - 2 * exponent) << (F.a * (r * r // 2)))
        else:
            exponent = (F.a * (m * (m + 1) // 2)) & 1
            values.append((1 - 2 * exponent) * G[m % 2] *
                          (1 << (F.a * ((r * r - 1) // 2))))
    return values, dict(field_modulus=h, field_degree=F.a, beta=beta,
                       trace_quadratic_anf=sorted(qpoly), inverse_square_root=eta,
                       scalar_gauss_sums=G, gauss_dimensions=[F.a, F.a],
                       enumerated_field_elements=0, enumerated_matrices=0)


def scalar_incidence_gap(t, h, beta, qpoly):
    """Exact gap of Tr tr(XYZ)+Tr beta e2(X)+q(tr X)."""
    J, data = two_scalar_matrix_gaussians(t, h, beta, qpoly)
    F = Field(h)
    gaussian = 1
    onto = 1
    total = 0
    for hdim in range(t + 1):
        r = t - hdim
        total += gaussian * onto * (F.q ** (hdim * r)) * J[r]
        if hdim < t:
            numerator = gaussian * (F.q ** (t - hdim) - 1)
            gaussian, remainder = divmod(numerator, F.q ** (hdim + 1) - 1)
            if remainder:
                raise AssertionError('nonintegral Gaussian coefficient')
            onto *= F.q ** t - F.q ** hdim
    return total * (F.q ** (t * t)), data
