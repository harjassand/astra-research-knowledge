#!/usr/bin/env python3
"""Finite diagnostic of the marked-current/Dirichlet-variational identity.

No third-party packages. Exact Fraction arithmetic checks the central identity;
the tiny state enumeration is only a diagnostic, not the proposed algorithm.
"""

from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path


def solve(a, b):
    a = [list(row) + [rhs] for row, rhs in zip(a, b)]
    n = len(a)
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        z = a[k][k]
        a[k] = [x / z for x in a[k]]
        for i in range(n):
            if i != k:
                z = a[i][k]
                a[i] = [x - z * y for x, y in zip(a[i], a[k])]
    return [row[-1] for row in a]


def symmetric_eigenvalues(a):
    a = [[float(x) for x in row] for row in a]
    n = len(a)
    for _ in range(10000):
        p, q = max(((i, j) for i in range(n) for j in range(i + 1, n)), key=lambda ij: abs(a[ij[0]][ij[1]]))
        if abs(a[p][q]) < 1e-13:
            break
        ang = 0.5 * math.atan2(2 * a[p][q], a[q][q] - a[p][p])
        c, s = math.cos(ang), math.sin(ang)
        # R has columns (c,-s) and (s,c) in the p,q plane.
        ap, aq = a[p][p], a[q][q]
        bpq = a[p][q]
        for k in range(n):
            if k not in (p, q):
                x, y = a[k][p], a[k][q]
                a[k][p] = a[p][k] = c * x - s * y
                a[k][q] = a[q][k] = s * x + c * y
        a[p][p] = c * c * ap - 2 * c * s * bpq + s * s * aq
        a[q][q] = s * s * ap + 2 * c * s * bpq + c * c * aq
        a[p][q] = a[q][p] = 0.0
    return sorted(a[i][i] for i in range(n))


def check(a, rho):
    # Lambda={0,...,4}, Lambda^-={1,2,3}, issued bonds x,x+1 for x=0,...,4.
    interior = (1, 2, 3)
    ghost = (-1, 0, 4, 5, 6)
    states = list(product((0, 1), repeat=len(interior)))
    lookup = {state: i for i, state in enumerate(states)}
    n = len(states)
    weights = [rho ** sum(state) * (1 - rho) ** (len(interior) - sum(state)) for state in states]
    transitions = [[] for _ in states]
    generator = [[F(0) for _ in states] for _ in states]
    j, activity = [F(0) for _ in states], F(0)
    for idx, state in enumerate(states):
        for gbits in product((0, 1), repeat=len(ghost)):
            gw = rho ** sum(gbits) * (1 - rho) ** (len(ghost) - sum(gbits))
            eta = dict(zip(interior, state)) | dict(zip(ghost, gbits))
            for x in range(5):
                y = x + 1
                rate = gw * (1 + a * eta[x - 1] * eta[x + 2])
                mark = eta[x] - eta[y]
                changed = eta.copy()
                changed[x], changed[y] = eta[y], eta[x]
                other = lookup[tuple(changed[k] for k in interior)]
                transitions[idx].append((other, mark, rate))
                if other != idx:
                    generator[idx][other] += rate
                    generator[idx][idx] -= rate
                j[idx] += rate * mark
                activity += weights[idx] * rate * mark * mark
    assert sum(w * x for w, x in zip(weights, j)) == 0
    assert all(sum(generator[i][j] for j in range(n)) == 0 for i in range(n))
    assert all(weights[i] * generator[i][k] == weights[k] * generator[k][i] for i in range(n) for k in range(n))
    positive = [[-x for x in row] for row in generator]
    f = solve([row[:-1] for row in positive[:-1]], j[:-1]) + [F(0)]
    assert all(sum(positive[i][k] * f[k] for k in range(n)) == j[i] for i in range(n))
    mean = sum(w * x for w, x in zip(weights, f))
    f = [x - mean for x in f]
    green_kubo = activity - 2 * sum(w * q * x for w, q, x in zip(weights, j, f))
    objective = sum(weights[i] * rate * (mark + f[k] - f[i]) ** 2 for i in range(n) for k, mark, rate in transitions[i])
    assert objective == green_kubo
    assert green_kubo >= 0
    poisson_energy = sum(weights[i] * f[i] * j[i] for i in range(n))
    assert 2 * poisson_energy <= activity
    sym = [[float(positive[i][k]) * math.sqrt(float(weights[i] / weights[k])) for k in range(n)] for i in range(n)]
    eig = symmetric_eigenvalues(sym)
    gap = next(x for x in eig if x > 1e-8)
    a_cutoff = min(rho, 1-rho)
    analytic_gap_bound = float(a_cutoff * a_cutoff / (3 * 5 * 5))
    assert gap + 1e-10 >= analytic_gap_bound
    return {
        'a': str(a), 'rho': str(rho), 'active_states_diagnostic_only': n,
        'volume': 5, 'activity_A': str(activity),
        'green_kubo_asymptotic_variance': str(green_kubo),
        'dirichlet_objective': str(objective),
        'conductivity_cell': str(green_kubo / 5),
        'gap_diagnostic': gap, 'derived_gap_lower_bound': analytic_gap_bound,
        'poisson_l2_norm_squared': str(sum(w * x * x for w, x in zip(weights, f))),
        'finite_time_bias_certificate_numerator_A_over_gapV': float(activity) / (gap * 5),
        'identity_exact': True,
    }


def check_weighted_detector():
    # General xi directions have nonunit known magnitudes. A plain event-count
    # subtraction is biased; the correct subtraction uses sum of mark squares.
    weights, signs, visibility = (F(1, 2), F(1, 3)), (1, -1), F(1, 2)
    p_correct = (1 + visibility) / 2
    target = sum(w * s for w, s in zip(weights, signs)) ** 2
    k2 = sum(w * w for w in weights)
    mean_correct = F(0)
    mean_wrong = F(0)
    for errors in product((1, -1), repeat=2):
        probability = F(1)
        for error in errors:
            probability *= p_correct if error == 1 else 1 - p_correct
        score = sum(w * sign * error / visibility for w, sign, error in zip(weights, signs, errors))
        mean_correct += probability * (score * score - k2 * (visibility ** -2 - 1))
        mean_wrong += probability * (score * score - 2 * (visibility ** -2 - 1))
    assert mean_correct == target
    assert mean_wrong != target
    return {'weights': [str(x) for x in weights], 'visibility': str(visibility),
            'target_current_square': str(target), 'correct_K2_subtraction_mean': str(mean_correct),
            'incorrect_count_subtraction_mean': str(mean_wrong), 'identity_exact': True}


if __name__ == '__main__':
    results = [check(a, rho) for a in (F(0), F(1), F(2)) for rho in (F(1, 3), F(1, 2), F(2, 3))]
    # SSEP constant rate one must give sigma=2 rho(1-rho) with the issued-bond convention.
    for row in results:
        if row['a'] == '0':
            rho = F(row['rho'])
            assert F(row['conductivity_cell']) == 2 * rho * (1-rho)
    output = Path(__file__).with_name('cell_current_check.json')
    detector = check_weighted_detector()
    output.write_text(json.dumps({'scope':'Exact finite diagnostic; not an infinite-volume proof',
                                 'results': results, 'weighted_detector': detector}, indent=2) + '\n')
    print(json.dumps({'checked_cells': len(results), 'all_exact_identities_passed': True,
                      'weighted_detector_passed': True, 'output': str(output.resolve())}))
