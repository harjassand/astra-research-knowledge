#!/usr/bin/env python3
"""Exact checks for the 2026-11-06 QUBO continuation.

Standard library only. This is an audit program, not a polynomial-time
unrestricted QUBO solver. Exhaustive checks are deliberately bounded.
The quantified arguments are in RESEARCH_REPORT.txt.
"""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
from math import comb
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def clean(p):
    return {k: Q(v) for k, v in p.items() if v}


def add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, 0) + v
    return clean(out)


def scale(p, a):
    return clean({k: a*v for k, v in p.items()})


def mul(p, q):
    # Products reduced by x_i^2 = x_i.
    out = {}
    for a, u in p.items():
        for b, v in q.items():
            k = tuple(sorted(set(a) | set(b)))
            out[k] = out.get(k, 0) + u*v
    return clean(out)


def constant(c):
    return clean({(): c})


def var(i):
    return {(i,): Q(1)}


def affine(c, weights):
    return add(constant(c), {(i,): Q(w) for i, w in enumerate(weights)})


def evaluate(p, x):
    return sum(v for k, v in p.items() if all(x[i] for i in k))


def restrict(p, index, bit):
    out = {}
    for k, v in p.items():
        if index in k:
            if not bit:
                continue
            k = tuple(i for i in k if i != index)
        out[k] = out.get(k, 0) + v
    return clean(out)


def odd_family(n):
    assert n >= 3 and n % 2 == 1
    m = (n-1)//2
    W = n*(n+1)//2
    A = W+1
    energy = {(): A*n*n}
    energy.update({(i,): 4*A*(1-n)+i+1 for i in range(n)})
    energy.update({(i, j): 8*A for i, j in combinations(range(n), 2)})
    optimum = A + m*(m+1)//2
    minimizer = (1,)*m + (0,)*(m+1)
    return clean(energy), m, W, A, optimum, minimizer


def odd_certificate(n):
    energy, m, W, A, optimum, minimizer = odd_family(n)
    t = affine(-m, [1]*n)
    out = add(scale(mul(t, add(t, constant(-1))), 16*A-n),
              scale(mul(t, add(t, constant(1))), n))
    for i in range(1, m+1):
        out = add(out, scale(add(constant(1), scale(var(i-1), -1)),
                             2*(n-2*i)))
    for i in range(m+1, n+1):
        out = add(out, scale(var(i-1), 2*(2*i-n)))
    assert out == scale(add(energy, constant(-optimum)), 4)
    return out


def frontier_count(m):
    table = {}
    for p in range(m, -1, -1):
        for q in range(m, -1, -1):
            table[p, q] = (1 if p == m or q == m else
                           table[p+1, q] + table[p, q+1])
    return table[0, 0]


def check_moments(n):
    _, m, W, A, optimum, _ = odd_family(n)
    count = 0
    for p in range(m):
        for q in range(m):
            f = n-p-q
            r = Q(n, 2)-p
            mu = r/f
            nu = r*(r-1)/(f*(f-1))
            p11 = nu
            p10 = r*(f-r)/(f*(f-1))
            p00 = (f-r)*(f-r-1)/(f*(f-1))
            assert min(p11, p10, p00) >= 0
            assert p00+2*p10+p11 == 1
            diagonal = mu-mu*mu
            offdiagonal = nu-mu*mu
            assert diagonal + (f-1)*offdiagonal == 0
            assert diagonal-offdiagonal == r*(f-r)/(f*(f-1)) >= 0
            mean_S = p+f*mu
            second_S = p*p+2*p*f*mu+f*mu+f*(f-1)*nu
            assert mean_S == Q(n, 2)
            assert second_S-mean_S*mean_S == 0
            assert A*(4*second_S-4*n*mean_S+n*n) == 0
            assert 0 <= mu <= 1 and W < optimum
            count += 1
    return count


def grishukhin_qubo():
    p = add(scale(var(4), 3), var(5))
    for i, j in combinations(range(4), 2):
        p = add(p, mul(var(i), var(j)))
    for i in range(4):
        p = add(p, scale(mul(var(4), var(i)), -2))
    p = add(p, scale(mul(var(5), var(0)), -1),
            scale(mul(var(5), var(2)), -1), mul(var(4), var(5)))
    return p


def determinant(matrix):
    a = [[Q(v) for v in row] for row in matrix]
    n = len(a)
    assert all(len(row) == n for row in a)
    out = Q(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            out = -out
        d = a[j][j]
        out *= d
        for i in range(j+1, n):
            ratio = a[i][j]/d
            for k in range(j+1, n):
                a[i][k] -= ratio*a[j][k]
            a[i][j] = 0
    return out


def grishukhin_witness():
    p = grishukhin_qubo()
    S = add(*(var(i) for i in range(4)))
    L = add(var(0), var(2), scale(var(5), -1))
    zero_case = scale(mul(L, add(L, constant(-1))), Q(1, 2))
    for i, j in combinations(range(4), 2):
        if (i, j) != (0, 2):
            zero_case = add(zero_case, mul(var(i), var(j)))
    one_case = add(scale(mul(add(S, constant(-2)), add(S, constant(-3))), Q(1, 2)),
                   mul(var(5), add(constant(1), scale(var(0), -1))),
                   mul(var(5), add(constant(1), scale(var(2), -1))))
    assert restrict(p, 4, 0) == zero_case
    assert restrict(p, 4, 1) == one_case
    combined = add(mul(add(constant(1), scale(var(4), -1)), zero_case),
                   mul(var(4), one_case))
    assert combined == p

    features = [()] + [(i,) for i in range(6)] + list(combinations(range(6), 2))
    zeros, rows, energies = [], [], []
    for x in product((0, 1), repeat=6):
        value = evaluate(p, x)
        assert value >= 0 and value.denominator == 1
        energies.append(int(value))
        if value == 0:
            zeros.append(''.join(map(str, x)))
            rows.append([int(all(x[i] for i in k)) for k in features])
    assert len(zeros) == 21
    vector = [int(p.get(k, 0)) for k in features]
    assert all(sum(u*v for u, v in zip(row, vector)) == 0 for row in rows)
    # Exclude the x5*x6 column. This square minor certifies rank at least 21.
    cols = list(range(21))
    det = determinant([[row[j] for j in cols] for row in rows])
    assert abs(det) == 1
    assert p[(0, 1)] == 1 and p[(0, 5)] == -1 and p.get((1, 5), 0) == 0
    return {
        'feature_order': ['1' if not k else '*'.join('x'+str(i+1) for i in k)
                          for k in features],
        'coefficient_vector': vector,
        'zero_assignments_x1_through_x6': zeros,
        'evaluation_matrix': rows,
        'minor_column_indices_zero_based': cols,
        'minor_determinant': int(det),
        'exact_rank': 21,
        'nullspace_dimension': 1,
        'energy_histogram': {str(v): energies.count(v) for v in sorted(set(energies))},
        'all_64_assignments_nonnegative': True,
        'conditional_identities_verified_symbolically': True,
        'offdiagonal_obstruction': {'b12': 1, 'b16': -1, 'b26': 0},
    }


def signed_binary(v):
    assert Q(v).denominator == 1
    v = int(v)
    return ('-' if v < 0 else '+')+format(abs(v), 'b')


def fixture(p, n):
    return {
        'variables_explicit': [{'index_binary': format(i+1, 'b'), 'name': 'x'+str(i+1)}
                               for i in range(n)],
        'constant_signed_binary': signed_binary(p.get((), 0)),
        'linear': [{'index_binary': format(i+1, 'b'),
                    'coefficient_signed_binary': signed_binary(p.get((i,), 0))}
                   for i in range(n)],
        'quadratic': [{'i_binary': format(i+1, 'b'), 'j_binary': format(j+1, 'b'),
                       'coefficient_signed_binary': signed_binary(p.get((i, j), 0))}
                      for i, j in combinations(range(n), 2)],
    }


def read_fixture(data):
    n = len(data['variables_explicit'])
    assert [int(v['index_binary'], 2) for v in data['variables_explicit']] == list(range(1, n+1))
    p = {(): int(data['constant_signed_binary'], 2)}
    assert len(data['linear']) == n and len(data['quadratic']) == n*(n-1)//2
    for v in data['linear']:
        p[(int(v['index_binary'], 2)-1,)] = int(v['coefficient_signed_binary'], 2)
    for v in data['quadratic']:
        i, j = int(v['i_binary'], 2)-1, int(v['j_binary'], 2)-1
        assert 0 <= i < j < n
        p[(i, j)] = int(v['coefficient_signed_binary'], 2)
    return clean(p)


def write_json(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')


def main():
    finite = []
    for n in range(3, 14, 2):
        energy, m, W, A, optimum, minimizer = odd_family(n)
        best, minimizers = None, []
        for x in product((0, 1), repeat=n):
            value = evaluate(energy, x)
            if best is None or value < best:
                best, minimizers = value, [x]
            elif value == best:
                minimizers.append(x)
        assert best == optimum and minimizers == [minimizer]
        finite.append({'n': n, 'A': A, 'minimum': optimum,
                       'unique_minimizer': ''.join(map(str, minimizer)),
                       'assignments_checked': 2**n})
    for n in range(3, 102, 2):
        odd_certificate(n)
    moment_states = sum(check_moments(n) for n in range(3, 62, 2))
    frontiers = []
    for m in range(1, 31):
        actual = frontier_count(m)
        assert actual == 2*comb(2*m-1, m)
        frontiers.append({'n': 2*m+1, 'mandatory_frontier': actual})
    witness = grishukhin_witness()
    fixtures = {'odd_family_n5': fixture(odd_family(5)[0], 5),
                'grishukhin_n6': fixture(grishukhin_qubo(), 6)}
    assert read_fixture(fixtures['odd_family_n5']) == odd_family(5)[0]
    assert read_fixture(fixtures['grishukhin_n6']) == grishukhin_qubo()
    write_json('SIGNED_BINARY_FIXTURES.json', fixtures)
    write_json('GRISHUKHIN_WITNESS.json', witness)
    result = {
        'status': 'All stated finite exact checks passed; unrestricted question unresolved.',
        'arithmetic': 'Python arbitrary-precision integers and fractions; no floating point or solver oracle.',
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'odd_family_exhaustive_checks': finite,
        'total_assignments_enumerated_for_odd_family': sum(v['assignments_checked'] for v in finite),
        'symbolic_identity_checks_n': list(range(3, 102, 2)),
        'moment_parameter_states_checked': moment_states,
        'frontier_recurrence_checks': frontiers,
        'grishukhin_summary': {k: v for k, v in witness.items()
                               if k not in ('evaluation_matrix', 'feature_order',
                                            'zero_assignments_x1_through_x6', 'coefficient_vector')},
        'binary_fixture_roundtrips': 2,
        'heat_bath_transfer': 'Retained as supplied. Dynamics not re-proved or used as an optimisation lower bound.',
        'warning': 'Finite family checks do not prove asymptotic statements. See the separate mathematical proofs.',
    }
    write_json('AUDIT_RESULTS.json', result)
    print(json.dumps({
        'odd_family_assignments_checked': result['total_assignments_enumerated_for_odd_family'],
        'symbolic_identity_checks': len(result['symbolic_identity_checks_n']),
        'moment_parameter_states_checked': moment_states,
        'frontier_recurrence_checks': len(frontiers),
        'grishukhin_zero_count': len(witness['zero_assignments_x1_through_x6']),
        'grishukhin_rank': witness['exact_rank'],
        'grishukhin_minor_determinant': witness['minor_determinant'],
        'status': 'passed',
    }, indent=2))


if __name__ == '__main__':
    main()
