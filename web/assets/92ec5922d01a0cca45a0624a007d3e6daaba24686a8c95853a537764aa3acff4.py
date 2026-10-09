#!/usr/bin/env python3
"""Exact finite scope/constant replay; no solver, random sampling or floats."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def mv(a, v):
    return [sum(a[i][j] * v[j] for j in range(len(v)))
            for i in range(len(a))]


def tau_quad(v, w):
    return sum(a * b for a, b in zip(v, w)) / len(v)


def subtract(v, w):
    return [a - b for a, b in zip(v, w)]


def half_l1_diag(v, w):
    return sum(abs(a-b) for a, b in zip(v, w)) / 2


def serialize(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k: serialize(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [serialize(v) for v in x]
    return x


# Exact Gaussian rational arithmetic is needed only to enumerate the
# canonical phase ensemble; no complex floating point is used.
Z = (F(0), F(0))
ONE = (F(1), F(0))
ROOTS = (ONE, (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1)))


def gadd(a, b):
    return (a[0]+b[0], a[1]+b[1])


def gmul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def gconj(a):
    return (a[0], -a[1])


def gscale(a, s):
    return (s*a[0], s*a[1])


def main():
    d = 4
    p = [[F(1, 2) if (i-j) % d in (1, 3) else F(0)
          for j in range(d)] for i in range(d)]
    q = [[F(1, d) for _ in range(d)] for _ in range(d)]
    v = [F(1), F(-1), F(1), F(-1)]
    assert all(sum(row) == 1 for row in p)
    assert all(sum(p[i][j] for i in range(d)) == 1 for j in range(d))
    assert all(p[i][j] >= 0 and p[i][j] == p[j][i]
               for i in range(d) for j in range(d))
    assert mv(p, v) == [-x for x in v]
    assert all(q[i][j]-p[i][j] == v[i]*v[j]/4
               for i in range(d) for j in range(d))

    phases = list(product(ROOTS, repeat=d))
    projectors = []
    for z in phases:
        projectors.append([[gscale(gmul(z[i], gconj(z[j])), F(1, 4))
                            for j in range(d)] for i in range(d)])
    count = len(projectors)
    assert count == 256
    for i in range(d):
        for j in range(d):
            total = Z
            for proj in projectors:
                total = gadd(total, proj[i][j])
            assert gscale(total, F(1, count)) == (
                F(1, d) if i == j else F(0), F(0))

    # Psi(E_kl)_ij = d avg(proj_ij proj_lk).
    for k in range(d):
        for l in range(d):
            for i in range(d):
                for j in range(d):
                    total = Z
                    for proj in projectors:
                        total = gadd(total, gmul(proj[i][j], proj[l][k]))
                    got = gscale(total, F(d, count))
                    expected = F(1, d) if k == l and i == j else F(0)
                    if k != l and i == k and j == l:
                        expected = F(1, d)
                    assert got == (expected, F(0))

    a = [F(1, 7), F(1, 7), F(5, 7), F(13, 7)]
    x = [ai*ai for ai in a]
    assert sum(x) / d == 1
    rho = [xi/d for xi in x]
    sigma = [F(1, d)] * d
    e_phi = tau_quad(a, subtract(a, mv(p, a)))
    e_phi_pairwise = sum(p[i][j]*(a[i]-a[j])**2
                         for i in range(d) for j in range(d)) / (2*d)
    e_psi = tau_quad(a, subtract(a, mv(q, a)))
    assert e_phi == e_phi_pairwise
    assert e_phi >= e_psi >= 0
    assert e_phi-e_psi == tau_quad(a, mv(
        [[v[i]*v[j]/4 for j in range(d)] for i in range(d)], a))
    b = half_l1_diag(rho, mv(p, rho))
    e = half_l1_diag(rho, sigma)
    assert e**2 <= 2*e_psi
    affinity_lower = sum(a)/d
    assert affinity_lower == F(5, 7)
    assert e_psi == 1-affinity_lower**2
    assert e**2 <= 1-affinity_lower**2

    # Exact scalar optimization identities after writing T^3=CD/(32b^2).
    optimized_cubic_factor = F(6)**3 / 32
    assert optimized_cubic_factor == F(27, 4)
    assert F(16) / 32 == F(1, 2)  # (4bT)^2 = CD/(2T).
    assert optimized_cubic_factor * 4 == 27
    assert F(5, 3)**3 > 4  # 3*2^(2/3)<5.

    # Nonphysical form-ordered obstruction: all inequalities here exact.
    r = F(1, 4)
    bad_b, bad_e = r/2, 2*r
    entropy_upper = r*r/(2*(1-r*r))
    assert entropy_upper == F(1, 30)
    asserted_cubic_upper = 27*entropy_upper*bad_b
    assert bad_e**3 == F(1, 8)
    assert asserted_cubic_upper == F(9, 80)
    assert bad_e**3 > asserted_cubic_upper
    assert 1-3*r > 0  # Gamma(rho) itself is a density.
    gamma_pure_block_eigenvalues = [F(2), F(-1)]
    assert min(gamma_pure_block_eigenvalues) < 0

    result = {
        "status": "EXACT_FINITE_IDENTITIES_PASS_GENERAL_PROOF_SEPARATE",
        "arithmetic": "integers, fractions, Gaussian rational pairs",
        "dimension": d,
        "negative_HS_eigenvalue": -1,
        "transition_matrix": p,
        "full_form_order_certificate": {
            "diagonal_Q_minus_P": "vv^T/4",
            "v": v,
            "off_diagonal_Psi_minus_Phi": F(1, 4),
            "C": 1,
        },
        "canonical_phase_vectors_enumerated": count,
        "matrix_units_action_verified": d*d,
        "rational_positive_state_check": {
            "sqrt_X": a, "rho": rho,
            "E_Phi_sqrt_X": e_phi,
            "E_Psi_sqrt_X": e_psi,
            "b": b, "e": e,
            "affinity_lower": affinity_lower,
        },
        "optimized_general_cubic_factor": optimized_cubic_factor,
        "optimized_C4_cubic_factor": 27,
        "squared_C4_coefficient_exact": "3*2^(2/3) < 5",
        "nonphysical_scope_obstruction": {
            "Gamma": "4*dephasing - 3*identity_superoperator",
            "global_form_C": 4,
            "b": bad_b, "e": bad_e,
            "entropy_upper": entropy_upper,
            "actual_e_cubed": bad_e**3,
            "bound_upper": asserted_cubic_upper,
            "positivity_violation_eigenvalues": gamma_pure_block_eigenvalues,
            "legal_counterexample": False,
        },
        "proves_general_theorem": False,
        "external_validation": "UNKNOWN",
    }
    out = Path(__file__).with_name("POWER_REPLAY_RESULT.json")
    out.write_text(json.dumps(serialize(result), indent=2)+"\n")
    print(json.dumps({"status": result["status"], "output": str(out),
                      "phase_vectors": count, "C4_cubic_factor": 27}))


if __name__ == "__main__":
    main()
