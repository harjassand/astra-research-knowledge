#!/usr/bin/env python3
"""Verify the exact ordered-area loss of real-path streaming Schur sampling.

This is a validation script for clt_block_analysis.md.  It constructs the
physical projective instrument, retains every path label and each spin irrep,
and compares its exact tracial Q loss to the analytic lower bound.  No
optimization and no expansion in the collision angle are used.
"""
from pathlib import Path
import json
import math
import numpy as np
from threadpoolctl import threadpool_limits
from cg_half import cg_half

threadpool_limits(1)
PAULI = [np.eye(2), np.array([[0, 1], [1, 0]], complex),
         np.array([[0, -1j], [1j, 0]], complex), np.diag([1., -1.])]


def epsilon(a, b, c):
    if len({a, b, c}) < 3:
        return 0
    return 1 if (a, b, c) in [(1, 2, 3), (2, 3, 1), (3, 1, 2)] else -1


def kron_all(items):
    out = np.ones((1, 1))
    for item in items:
        out = np.kron(out, item)
    return out


def pauli_matrix(string):
    return kron_all([PAULI[x] for x in string])


def logical_coefficients(b, theta, logical=3):
    """Pauli coefficients of U_b...(sigma_logical tensor I)...U_b^dagger."""
    c, s = np.cos(theta), np.sin(theta)
    current = {(logical,): 1.}
    for _ in range(b):
        nxt = {}

        def add(string, value):
            nxt[string] = nxt.get(string, 0.) + value

        for string, value in current.items():
            a = string[0]
            if a == 0:
                add(string + (0,), value)
                continue
            add(string + (0,), c*c*value)
            add((0,) + string[1:] + (a,), s*s*value)
            for x in range(1, 4):
                for y in range(1, 4):
                    e = epsilon(a, x, y)
                    if e:
                        add((x,) + string[1:] + (y,), -c*s*e*value)
        current = nxt
    return current


def path_isometries(b):
    """All standard real Clebsch-Gordan paths V_j -> (C^2)^tensor b."""
    paths = [(0., (), np.ones((1, 1)))]
    for _ in range(b):
        nxt = []
        for j, labels, v in paths:
            for sign in [1, -1]:
                if j + sign/2 < 0:
                    continue
                c = cg_half(j, sign)
                nxt.append((j + sign/2, labels + (sign,), np.kron(v, np.eye(2)) @ c))
        paths = nxt
    return paths


def ordered_area(b):
    result = [np.zeros((2**b, 2**b), complex) for _ in range(3)]
    for a in range(1, 4):
        for i in range(b):
            for j in range(i+1, b):
                for x in range(1, 4):
                    for y in range(1, 4):
                        e = epsilon(a, x, y)
                        if e:
                            string = [0]*b
                            string[i], string[j] = x, y
                            result[a-1] += e*pauli_matrix(string)
    return result


def pinched_norm(x, isometries):
    total = 0.
    for v in isometries:
        lift = np.kron(np.eye(2), v)
        part = lift.conj().T @ x @ lift
        total += np.vdot(part, part).real
    return total/x.shape[0]


def check_case(b, theta):
    c, s = np.cos(theta), np.sin(theta)
    coefficients = logical_coefficients(b, theta)
    d = 2**b
    x = sum(value*pauli_matrix(string) for string, value in coefficients.items())
    p = sum(value*pauli_matrix(string) for string, value in coefficients.items() if string[0] == 0)
    q = x-p
    paths = path_isometries(b)
    isometries = [v for j, labels, v in paths]
    identity = sum(v@v.conj().T for v in isometries)
    y = ordered_area(b)
    y_path_residual = max(np.linalg.norm(v.conj().T @ item @ v)
                          for v in isometries for item in y)
    z = sum(epsilon(3, u, v)*np.kron(PAULI[u], y[v-1])
            for u in range(1, 4) for v in range(1, 4))
    znorm = np.vdot(z, z).real/(2*d)
    z_coefficient = (np.vdot(z, q).real/(2*d))/znorm
    q_before = np.vdot(q, q).real/(2*d)
    q_after = pinched_norm(q, isometries)
    a_after = pinched_norm(p, isometries)
    lower = .5*b*(b-1)*c**(4*b-4)*s**4
    r = 1-s**4
    weight_residual = max(abs(sum(value*value for string, value in coefficients.items()
                                  if string[0] and sum(x != 0 for x in string[1:]) == k)
                              - math.comb(b, k)*c**(4*b-2*k)*2**k*s**(2*k))
                          for k in range(b+1))
    result = dict(b=b, theta=theta, path_count=len(paths),
                  completeness_residual=float(np.linalg.norm(identity-np.eye(d))),
                  Y_path_residual=float(y_path_residual),
                  Y_norm_squared=[float(np.vdot(item, item).real/d) for item in y],
                  Z_norm_squared=float(znorm),
                  Z_coefficient=float(z_coefficient),
                  predicted_Z_coefficient=float(-.5*c**(2*b-2)*s*s),
                  q_before=float(q_before), q_after=float(q_after),
                  a_after=float(a_after), loss_Q=float(q_before-q_after),
                  exact_lower_bound=float(lower),
                  lower_bound_slack=float(q_before-q_after-lower),
                  block_acquisition_upper=float(1-r**b),
                  actual_repeated_block_a_limit=float(a_after/(1-q_after)),
                  analytic_a_limit_upper=float((1-r**b)/(1-r**b+lower)),
                  weight_distribution_residual=float(weight_residual))
    assert result['completeness_residual'] < 1e-12
    assert result['Y_path_residual'] < 1e-12
    assert abs(z_coefficient+.5*c**(2*b-2)*s*s) < 1e-13
    assert abs(znorm-2*b*(b-1)) < 1e-12
    assert abs(q_before-r**b) < 1e-12
    assert result['lower_bound_slack'] > -1e-12
    assert result['weight_distribution_residual'] < 1e-12
    return result


if __name__ == '__main__':
    checks = [check_case(b, theta) for b in range(2, 7) for theta in [.03, .1, .3, .7]]
    target = Path(__file__).with_name('schur_block_checks.json')
    target.write_text(json.dumps(checks, indent=2))
    print(json.dumps(dict(cases=len(checks),
                         max_Y_residual=max(x['Y_path_residual'] for x in checks),
                         max_weight_residual=max(x['weight_distribution_residual'] for x in checks),
                         minimum_bound_slack=min(x['lower_bound_slack'] for x in checks),
                         weak_angle_limits=[{k: x[k] for k in ['b', 'actual_repeated_block_a_limit', 'analytic_a_limit_upper']}
                                            for x in checks if x['theta'] == .03]), indent=2))
