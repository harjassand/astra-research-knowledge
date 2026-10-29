#!/usr/bin/env python3
"""Exact controls for reflected finite histories and sensor scope.

The examples are rational discrete skeletons, not claimed CTMC embeddings.
The parent theorem is a CTMC theorem proved in the accompanying review.
No native preparation, measurement, or experimental operation occurs.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import math

from check_copositive_lag import log_interval

HERE = Path(__file__).resolve().parent


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def sym(a):
    return [[(a[i][j]+a[j][i])/2 for j in range(len(a))]
            for i in range(len(a))]


def total(a):
    return sum(map(sum, a), F(0))


def exact_receipt(a):
    return [[str(x) for x in row] for row in a]


def coarse(x):
    return int(x != 0)


def deterministic_kernel(word):
    code = 4*coarse(word[0])+2*coarse(word[1])+coarse(word[2])
    return [F(a == code) for a in range(8)]


def randomized_kernel(word):
    code = 4*coarse(word[0])+2*coarse(word[1])+coarse(word[2])
    r = F(code+1, 9)
    return [1-r, r]


def history_joint(matrix, pi, kernel):
    """Left label uses (X0,X-1,X-2), right (X0,X1,X2)."""
    n = len(matrix)
    labels = len(kernel((0, 0, 0)))
    c = zero(labels)
    for path in product(range(n), repeat=5):
        mass = pi[path[0]]
        for i in range(4):
            mass *= matrix[path[i]][path[i+1]]
        left = kernel((path[2], path[1], path[0]))
        right = kernel((path[2], path[3], path[4]))
        for a in range(labels):
            for b in range(labels):
                c[a][b] += mass*left[a]*right[b]
    return c


def half_weights(matrix, kernel):
    n = len(matrix)
    labels = len(kernel((0, 0, 0)))
    v = [[F(0) for _ in range(labels)] for _ in range(n)]
    for x, y, z in product(range(n), repeat=3):
        k = kernel((x, y, z))
        for a in range(labels):
            v[x][a] += matrix[x][y]*matrix[y][z]*k[a]
    return v


def gram(v, pi):
    labels = len(v[0])
    return [[sum(pi[x]*v[x][a]*v[x][b] for x in range(len(pi)))
             for b in range(labels)] for a in range(labels)]


def rounded_interval(lo, hi, places=20):
    scale = 10**places
    lower = F((lo.numerator*scale)//lo.denominator, scale)
    upper = F(-((-hi.numerator*scale)//hi.denominator), scale)
    assert lower <= lo <= hi <= upper
    return lower, upper


def psi_interval(s):
    assert 0 < s <= 1
    if s == 1:
        return F(0), F(0)
    radicand = 1-s*s
    scale = 10**22
    floor = math.isqrt((radicand.numerator*scale*scale)//radicand.denominator)
    zl, zu = F(floor, scale), F(floor+1, scale)
    assert zl*zl <= radicand < zu*zu and zu < 1
    ll, _ = log_interval((1+zl)/(1-zl))
    _, lu = log_interval((1+zu)/(1-zu))
    return rounded_interval(zl*ll, zu*lu)


def rational_skeleton():
    n = 3
    pi = [F(1, 3)]*n
    p = [[F(4, 9) if i == j or j == (i+1) % n else F(1, 9)
          for j in range(n)] for i in range(n)]
    g = [[F(4, 9) if i == j else F(2, 9)
          for j in range(n)] for i in range(n)]
    for i in range(n):
        assert sum(p[i]) == 1
        assert sum(p[j][i] for j in range(n)) == 1
        for j in range(n):
            assert g[i][j]*g[i][j] == p[i][j]*p[j][i]

    results = {}
    for name, kernel in [('binary_history_words', deterministic_kernel),
                         ('independent_random_half_labels', randomized_kernel)]:
        c = sym(history_joint(p, pi, kernel))
        b = history_joint(g, pi, kernel)
        v = half_weights(g, kernel)
        assert b == gram(v, pi)
        assert total(c) == 1
        assert total(b) == F(8, 9)**4
        for i in range(len(c)):
            for j in range(len(c)):
                assert c[i][j] >= b[i][j] >= 0
        deficit = total(c)-total(b)
        # Stationary microscopic Jeffreys / relative entropy over four steps.
        lo_log4, hi_log4 = log_interval(F(4))
        entropy_lo, entropy_hi = F(4, 3)*lo_log4, F(4, 3)*hi_log4
        assert entropy_lo >= 4*deficit
        jensen_lo = jensen_hi = F(0)
        for i in range(len(c)):
            for j in range(len(c)):
                if c[i][j]:
                    lo, hi = psi_interval(b[i][j]/c[i][j])
                    jensen_lo += c[i][j]*lo
                    jensen_hi += c[i][j]*hi
        assert entropy_lo >= jensen_hi
        assert jensen_lo >= 4*deficit
        results[name] = {
            'label_count':len(c), 'sym_joint':exact_receipt(c),
            'geometric_joint':exact_receipt(b),
            'exact_nonnegative_midpoint_factorization':'PASS',
            'exact_entrywise_dominance':'PASS',
            'affinity':str(total(b)), 'affinity_deficit':str(deficit),
            'four_times_deficit':str(4*deficit),
            'entropy_interval_decimal':[float(entropy_lo), float(entropy_hi)],
            'entrywise_Jensen_interval_decimal':[float(jensen_lo), float(jensen_hi)]}

    # Observed binary process is not Markov: histories have different
    # conditional next-label laws despite the same present visible label.
    conditional = []
    for past in (0, 1):
        numerator = denominator = F(0)
        for x, y, z in product(range(n), repeat=3):
            if coarse(x) == past and coarse(y) == 1:
                mass = pi[x]*p[x][y]*p[y][z]
                denominator += mass
                if coarse(z) == 0:
                    numerator += mass
        conditional.append(numerator/denominator)
    assert conditional[0] != conditional[1]
    results['visible_memory'] = {
        'P(Y2=0 | Y1=1,Y0=0)':str(conditional[0]),
        'P(Y2=0 | Y1=1,Y0=1)':str(conditional[1]),
        'non_Markov_coarse_observation':'EXACT PASS'}
    return results


def state_dependent_killing():
    g = [[F(1, 2), F(1, 6), F(1, 12)],
         [F(1, 6), F(1, 3), F(1, 6)],
         [F(1, 12), F(1, 6), F(1, 4)]]
    pi = [F(1, 3)]*3
    b = history_joint(g, pi, deterministic_kernel)
    v = half_weights(g, deterministic_kernel)
    assert b == gram(v, pi)
    s = list(map(sum, v))
    full_mass = total(b)
    assert full_mass == sum(pi[x]*s[x]*s[x] for x in range(3)) < 1
    midpoint = [pi[x]*s[x]*s[x]/full_mass for x in range(3)]
    assert midpoint != pi
    normalized = [[entry/s[x] for entry in v[x]] for x in range(3)]
    incorrect = gram(normalized, pi)
    assert total(incorrect) == 1 and incorrect != b
    return {'half_survival_weights':[str(x) for x in s],
            'full_geometric_mass':str(full_mass),
            'normalized_geometric_midpoint_distribution':[str(x) for x in midpoint],
            'unnormalized_half_Gram_identity':'EXACT PASS',
            'normalizing_halves_with_unchanged_pi_is_incorrect':'EXACT PASS'}


def sensor_scope():
    # One static hidden state, one shared fair midpoint emission.
    actual = [[F(1, 2), F(0)], [F(0), F(1, 2)]]
    incorrect = [[F(1, 4)]*2 for _ in range(2)]
    conditioned = gram([[F(1), F(0)], [F(0), F(1)]], [F(1, 2)]*2)
    assert actual == conditioned and actual != incorrect
    # Reversal-invariant correlated noise alone does not suffice.
    anti = [[F(0), F(1, 2)], [F(1, 2), F(0)]]
    h = [[F(1), F(-1)], [F(-1), F(1)]]  # (x0-x1)^2, hence copositive.
    witness = sum(h[i][j]*anti[i][j] for i in range(2) for j in range(2))
    assert witness == -1
    return {'shared_midpoint_joint':exact_receipt(actual),
            'incorrect_independent_midpoint_joint':exact_receipt(incorrect),
            'conditioning_on_shared_midpoint_restores_CP':'EXACT PASS',
            'correlated_antithetic_noise_joint':exact_receipt(anti),
            'copositive_quadratic':'(x0-x1)^2',
            'antithetic_noise_witness_pairing':str(witness),
            'scope':'The antithetic sensor is outside the independent-half contract; it is not a zero-dissipation physical device model.'}


def main():
    receipt = {'scope':'Exact rational discrete skeleton controls; no CTMC embedding or native acquisition asserted.',
               'rational_skeleton':rational_skeleton(),
               'state_dependent_killing':state_dependent_killing(),
               'sensor_scope':sensor_scope(),
               'native_observations':0, 'native_preparations':0,
               'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'helper_sha256':hashlib.sha256((HERE/'check_copositive_lag.py').read_bytes()).hexdigest()}
    (HERE/'REFLECTED_HISTORY_EXACT_CHECKS.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({'status':'PASS',
                      'finite_path_words_per_history_enumeration':3**5,
                      'coarse_history_labels':8,
                      'microscopic_relative_entropy':receipt['rational_skeleton']['binary_history_words']['entropy_interval_decimal'],
                      'Jensen_bound':receipt['rational_skeleton']['binary_history_words']['entrywise_Jensen_interval_decimal'],
                      'visible_memory':receipt['rational_skeleton']['visible_memory'],
                      'output':'REFLECTED_HISTORY_EXACT_CHECKS.json'}, indent=2))


if __name__ == '__main__':
    main()
