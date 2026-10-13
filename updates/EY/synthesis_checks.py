#!/usr/bin/env python3
"""Finite rational diagnostics for SYNTHESIS.md; not proof or physical validation."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def mv(a, v):
    return [sum(x*y for x, y in zip(row, v)) for row in a]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def inv2(a):
    (a0, b), (c, d) = a
    det = a0*d-b*c
    assert det
    return [[d/det, -b/det], [-c/det, a0/det]]


def kernel(a):
    a = [row[:] for row in a]
    n = len(a[0]); pivots = []; k = 0
    for j in range(n):
        pivot = next((i for i in range(k, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        scale = a[k][j]; a[k] = [x/scale for x in a[k]]
        for i in range(len(a)):
            if i != k:
                scale = a[i][j]
                a[i] = [x-scale*y for x, y in zip(a[i], a[k])]
        pivots.append(j); k += 1
        if k == len(a):
            break
    out = []
    for j in range(n):
        if j not in pivots:
            v = [F(0)]*n; v[j] = F(1)
            for i, p in enumerate(pivots):
                v[p] = -a[i][j]
            out.append(v)
    return out


def defect_block(y, yp, current):
    n = len(y[0])
    return [[sum(j*(q[i]*q[k]-p[i]*p[k]) for p, q, j in zip(y, yp, current))
             for k in range(n)] for i in range(n)]


def safe_space(y, yp):
    s = transpose([[q-p for p, q in zip(yr, ypr)] for yr, ypr in zip(y, yp)])
    cycles = kernel(s)
    blocks = [defect_block(y, yp, v) for v in cycles]
    z = [row for block in blocks for row in block]
    w = kernel(z) if z else [[F(i == j) for i in range(len(y[0]))] for j in range(len(y[0]))]
    for v in cycles:
        assert mv(s, v) == [0]*len(s)
    return cycles, blocks, w


def check_adjoint():
    y = mat([[0, 0], [1, 0], [0, 1]])
    yp = mat([[2, 0], [0, 1], [0, 0]])
    cycles, blocks, w = safe_space(y, yp)
    assert cycles == [[F(1, 2), F(1), F(1)]]
    assert w == [[F(0), F(1)]]
    j = mat([[-7, 1], [3, -4]])
    h = mat([[-9, 3], [1, -4]])
    m = defect_block(y, yp, [F(1), F(2), F(2)])
    assert transpose(j) == add(h, m)
    assert m == mat([[2, 0], [0, 0]])
    safe_a = [F(-3), F(4)]
    safe = mv(inv2(h), [-x for x in safe_a])
    assert safe == [0, 1]
    assert mv(transpose(j), safe) == [-x for x in safe_a]
    unsafe_a = [F(1), F(3, 5)]
    naive = mv(inv2(h), [-x for x in unsafe_a])
    exact = mv(inv2(transpose(j)), [-x for x in unsafe_a])
    s = [F(-1), F(1)]
    g_true = 2*sum(x*y for x, y in zip(s, exact))
    g_naive = 2*sum(x*y for x, y in zip(s, naive))
    assert g_true == F(-6, 125) and g_naive == F(2, 55)
    corrected = 0
    for a in [safe_a, unsafe_a, [F(2, 7), F(-5, 11)]]:
        ell = mv(inv2(h), [-x for x in a])
        xi = [x+y for x, y in zip(mv(transpose(j), ell), a)]
        assert xi == mv(m, ell)
        lam = mv(inv2(transpose(j)), [-x for x in a])
        error = [x-y for x, y in zip(lam, ell)]
        assert error == [-x for x in mv(inv2(transpose(j)), xi)]
        for b in [[F(1), F(0)], [F(-1), F(1)], [F(2, 3), F(5, 7)]]:
            lhs = sum(x*y for x, y in zip(b, error))
            rn_b = [-x for x in mv(inv2(j), b)]
            assert lhs == sum(x*y for x, y in zip(xi, rn_b))
            corrected += 1
    for scale in [F(1, 7), F(1), F(5, 2), F(100)]:
        d = defect_block(y, yp, [scale, 2*scale, 2*scale])
        assert mv(d, w[0]) == [0, 0]
    # The structural safe space can be trivial.
    _, _, no_safe = safe_space(mat([[0], [1], [2]]), mat([[1], [2], [0]]))
    assert no_safe == []
    return {'safe_space_basis': w, 'nonzero_defect': m, 'safe_objective': safe_a,
            'safe_adjoint': safe, 'unsafe_true_derivative': g_true,
            'unsafe_naive_derivative': g_naive, 'projection_identity_cases': corrected,
            'cycle_scales': 4, 'zero_safe_space_fixture': True}


def monomial(c, y):
    out = F(1)
    for x, power in zip(c, y):
        out *= x**int(power)
    return out


def check_relocation():
    y = mat([[0, 0], [2, 0], [1, 1], [0, 0], [1, 0], [0, 1]])
    yp = mat([[2, 0], [1, 1], [0, 0], [1, 0], [0, 1], [0, 0]])
    s = transpose([[q-p for p, q in zip(ar, br)] for ar, br in zip(y, yp)])
    target = [F(6, 5), F(11, 10)]
    rho = [(F(1)-F(1, 2))/(monomial(target, ar)-F(1, 2)*monomial(target, br))
           for ar, br in zip(y, yp)]
    caps = list(map(F, [2, 1, 1, F(3, 2), 1, 1]))
    weights = [list(map(F, [1, 1, 1, 1, 1, 1])), list(map(F, [1, 2, 1, 2, 1, 1]))]
    budgets = [sum(w) for w in weights]
    cases = 0
    for a, b in [(F(1), F(2)), (F(3), F(7)), (F(1, 10), F(1, 100))]:
        currents = [a, a, a, b, b, b]
        assert mv(s, currents) == [0, 0]
        for sigma in [F(1), F(3, 4)]:
            gates = [sigma*r for r in rho]
            new = [g*(2*j*monomial(target, ar)-j*monomial(target, br))
                   for g, j, ar, br in zip(gates, currents, y, yp)]
            assert new == [sigma*j for j in currents]
            assert mv(s, new) == [0, 0]
            assert all(0 < g <= cap for g, cap in zip(gates, caps))
            assert all(sum(x*g for x, g in zip(w, gates)) <= budget for w, budget in zip(weights, budgets))
            cases += 1
    # Exact Hessian quadratic forms of log rho, using rational x=exp(-A+s.h).
    psd_cases = 0
    for ar, br in zip(y, yp):
        x = F(1, 2)*monomial(target, br)/monomial(target, ar)
        assert 0 < x < 1
        for v in [[F(1), F(0)], [F(0), F(1)], [F(-2), F(3)]]:
            dot = sum((q-p)*vi for p, q, vi in zip(ar, br, v))
            assert x/(1-x)**2*dot**2 >= 0
            psd_cases += 1
    # Zero-affinity special handling, without evaluating a 0/0 relocation.
    c = [F(6, 5), F(6, 5)]; sigma = F(3, 2)
    gate = sigma/c[0]
    assert gate*c[0] == gate*c[1] == sigma
    return {'target_concentration': target, 'rho': rho, 'caps': caps,
            'resource_budgets': budgets,
            'costs_at_sigma_one': [sum(x*r for x, r in zip(w, rho)) for w in weights],
            'kinetic_models': 3, 'common_scale_cases': cases,
            'hessian_direction_cases': psd_cases, 'zero_current_case': True,
            'hidden_rate_constants_used_only_by_direct_fixture_check': True,
            'convergence_or_physical_access_tested': False}


def pack(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, list):
        return [pack(y) for y in x]
    if isinstance(x, dict):
        return {k: pack(v) for k, v in x.items()}
    return x


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path)
    args = p.parse_args()
    result = pack({'status': 'PASS', 'arithmetic': 'exact Python Fraction',
                   'adjoint': check_adjoint(), 'relocation': check_relocation(),
                   'scope': 'Finite internally authored diagnostics; universal arguments are in SYNTHESIS.md. No physical validation, novelty or matched speedup.'})
    text = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
