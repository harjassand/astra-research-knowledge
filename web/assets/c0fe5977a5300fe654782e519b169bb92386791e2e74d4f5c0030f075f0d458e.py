"""Finite checks of the exact reductions; no asymptotic theorem certification."""
from functools import lru_cache
from pathlib import Path
import json
from fractions import Fraction
from itertools import combinations, product
from math import factorial


def count_pm(n, edges):
    neighbors = [0] * n
    for a, b in edges:
        neighbors[a] |= 1 << b
        neighbors[b] |= 1 << a

    @lru_cache(None)
    def visit(mask):
        if not mask:
            return 1
        vertices = [i for i in range(n) if mask >> i & 1]
        a = min(vertices, key=lambda i: (neighbors[i] & mask).bit_count())
        choices = neighbors[a] & mask
        result = 0
        while choices:
            bit = choices & -choices
            choices ^= bit
            result += visit(mask ^ (1 << a) ^ bit)
        return result

    return visit((1 << n) - 1)


def weight_gadget(weight):
    assert weight >= 1
    bits = bin(weight)[2:]
    arcs = []
    source = previous = 0
    nodes = 1
    for bit in bits[1:]:
        a, b, target = nodes, nodes + 1, nodes + 2
        nodes += 3
        arcs.extend([(previous, a), (previous, b), (a, target), (b, target)])
        if bit == '1':
            arcs.append((source, target))
        previous = target
    # Original terminals 0 and 1; internal left/right vertex pairs start at 2.
    edges = [(2 + 2*i, 3 + 2*i) for i in range(nodes)]
    edges += [(2 + 2*i, 3 + 2*j) for i, j in arcs]
    edges += [(0, 3 + 2*source), (2 + 2*previous, 1)]
    return 2 + 2*nodes, edges


def induced_count(n, edges, terminals_present):
    kept = list(terminals_present) + list(range(2, n))
    translate = {v: i for i, v in enumerate(kept)}
    reduced = [(translate[a], translate[b]) for a, b in edges if a in translate and b in translate]
    return count_pm(len(kept), reduced)


def rank_mod(rows, prime):
    rows = [row[:] for row in rows]
    if not rows:
        return 0
    pivot = 0
    for column in range(len(rows[0])):
        found = next((i for i in range(pivot, len(rows)) if rows[i][column] % prime), None)
        if found is None:
            continue
        rows[pivot], rows[found] = rows[found], rows[pivot]
        inverse = pow(rows[pivot][column] % prime, -1, prime)
        rows[pivot] = [(x*inverse) % prime for x in rows[pivot]]
        for i in range(len(rows)):
            if i != pivot:
                coefficient = rows[i][column] % prime
                rows[i] = [(x-coefficient*y) % prime for x, y in zip(rows[i], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def first_jet_generators(size, level, prime):
    rows = []
    for degree in range(level):
        for a in range(size):
            for b in range(size):
                if a != b:
                    row = [0] * (level*size*size)
                    row[degree*size*size + a*size+b] = 1
                    rows.append(row)
        # Conjugating E_ab by I+E_ba produces E_ab+E_bb-E_aa-E_ba.
        for a in range(size-1):
            b = size-1
            row = [0] * (level*size*size)
            row[degree*size*size+a*size+b] = 1
            row[degree*size*size+b*size+b] = 1
            row[degree*size*size+a*size+a] = -1 % prime
            row[degree*size*size+b*size+a] = -1 % prime
            rows.append(row)
    return rows


def matrix_inverse(matrix):
    n = len(matrix)
    rows = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for column in range(n):
        pivot = next(i for i in range(column, n) if rows[i][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        divisor = rows[column][column]
        rows[column] = [x/divisor for x in rows[column]]
        for i in range(n):
            if i != column:
                factor = rows[i][column]
                rows[i] = [x-factor*y for x, y in zip(rows[i], rows[column])]
    return [row[n:] for row in rows]


def multiply(a, b):
    if not a or not b:
        return []
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def marginal_matrix(b, modes):
    m = len(b)
    c = [[Fraction(0) if (i < m) == (j < m) else b[i % m][j % m]
          for j in range(2*m)] for i in range(2*m)]
    q = matrix_inverse([[Fraction(i == j)-c[i][j] for j in range(2*m)]
                        for i in range(2*m)])
    keep = list(modes) + [i+m for i in modes]
    rest = [i for i in range(2*m) if i not in keep]
    qs = [[q[i][j] for j in keep] for i in keep]
    qs_inv = matrix_inverse(qs)
    o = [[Fraction(i == j)-qs_inv[i][j] for j in range(len(keep))]
         for i in range(len(keep))]
    schur = [[c[i][j] for j in keep] for i in keep]
    if rest:
        c_jt = [[c[i][j] for j in rest] for i in keep]
        c_tj = [[c[i][j] for j in keep] for i in rest]
        inverse_rest = matrix_inverse([[Fraction(i == j)-c[i][j] for j in rest]
                                       for i in rest])
        term = multiply(multiply(c_jt, inverse_rest), c_tj)
        schur = [[x+y for x, y in zip(a, z)] for a, z in zip(schur, term)]
    assert o == schur
    s = len(modes)
    a = [o[(i+s) % (2*s)] for i in range(2*s)]
    assert all(x >= 0 for row in a for x in row)
    assert a == [list(row) for row in zip(*a)]
    return a


def hafnian(matrix):
    n = len(matrix)

    @lru_cache(None)
    def visit(indices):
        if not indices:
            return Fraction(1)
        if len(indices) % 2:
            return Fraction(0)
        first = indices[0]
        return sum(matrix[first][indices[j]]*visit(indices[1:j]+indices[j+1:])
                   for j in range(1, len(indices)))

    return visit(tuple(range(n)))


def prism_count_law(copies, b):
    base = 2*copies
    n = 2*base
    neighbors = [[] for _ in range(n)]
    for a in range(base):
        neighbors[a].append((a+base, Fraction(1)))
        neighbors[a+base].append((a, Fraction(1)))
    for layer in [0, base]:
        for a in range(copies):
            for t in range(copies):
                x, y = a+layer, copies+t+layer
                neighbors[x].append((y, b/copies))
                neighbors[y].append((x, b/copies))

    @lru_cache(None)
    def visit(mask):
        if not mask:
            return {(0, 0): Fraction(1)}
        a = (mask & -mask).bit_length()-1
        law = {}
        for t, weight in neighbors[a]:
            if not mask >> t & 1:
                continue
            delta = (1, 1) if a < base and t < base else (0, 0)
            for pattern, mass in visit(mask ^ (1 << a) ^ (1 << t)).items():
                pattern = tuple(x+y for x, y in zip(pattern, delta))
                law[pattern] = law.get(pattern, Fraction(0)) + weight*mass
        return law

    return visit((1 << n)-1)


def multiply_polynomials(a, b, degree):
    result = {}
    for x, wx in a.items():
        for y, wy in b.items():
            z = tuple(i+j for i, j in zip(x, y))
            if sum(z) <= degree:
                result[z] = result.get(z, Fraction(0)) + wx*wy
    return result


def check_loop_generating_identity(b, degree=6):
    m = len(b)
    logarithm = {}
    walk_count = 0
    for length in range(2, degree+1, 2):
        for walk in product(range(m), repeat=length):
            weight = Fraction(1, length)
            for i in range(length):
                weight *= b[walk[i]][walk[(i+1) % length]]
            if weight:
                counts = tuple(walk.count(i) for i in range(m))
                logarithm[counts] = logarithm.get(counts, Fraction(0)) + weight
                walk_count += 1
    zero = (0,)*m
    generating = {zero: Fraction(1)}
    term = {zero: Fraction(1)}
    for power in range(1, degree//2+1):
        term = multiply_polynomials(term, logarithm, degree)
        for counts, weight in term.items():
            generating[counts] = generating.get(counts, Fraction(0)) + weight/factorial(power)
    checked = 0
    for counts in product(range(degree+1), repeat=m):
        if sum(counts) > degree:
            continue
        indices = [i for i, count in enumerate(counts) for _ in range(count)]
        repeated = [[b[i][j] for j in indices] for i in indices]
        amplitude = hafnian(repeated)
        expected = amplitude*amplitude
        for count in counts:
            expected /= factorial(count)
        assert generating.get(counts, Fraction(0)) == expected, (counts, expected)
        checked += 1
    return {'mode_count': m, 'total_degree': degree, 'patterns_checked': checked,
            'positive_closed_walks_enumerated': walk_count, 'exact_identity': True}


def main():
    gadget_cases = []
    for weight in range(1, 65):
        n, edges = weight_gadget(weight)
        signature = {
            'inactive': induced_count(n, edges, []),
            'active': induced_count(n, edges, [0, 1]),
            'left_only': induced_count(n, edges, [0]),
            'right_only': induced_count(n, edges, [1]),
        }
        assert signature == {'inactive': 1, 'active': weight, 'left_only': 0, 'right_only': 0}
        gadget_cases.append({'weight': weight, 'vertices': n, 'signature': signature})

    # Enumerate the whole simple unweighted reduction of a weighted K4.
    weighted_edges = [(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 2), (1, 3, 1), (2, 3, 3)]
    n = 4
    expanded_edges = []
    for a, b, weight in weighted_edges:
        gadget_n, gadget_edges = weight_gadget(weight)
        mapping = {0: a, 1: b, **{i: n+i-2 for i in range(2, gadget_n)}}
        expanded_edges += [(mapping[x], mapping[y]) for x, y in gadget_edges]
        n += gadget_n-2
    expected = 2*3 + 3*1 + 1*2
    expanded_count = count_pm(n, expanded_edges)
    assert expanded_count == expected

    jet_cases = []
    for size in [3, 4, 5]:
        for level in [1, 2, 3]:
            for prime in [3, 5, 7]:
                rows = first_jet_generators(size, level, prime)
                actual = rank_mod(rows, prime)
                expected_rank = level*(size*size-1)
                assert actual == expected_rank
                jet_cases.append({'matrix_size': size, 'level': level, 'prime': prime, 'rank': actual})

    # Exact rational marginal checks: row sums below one guarantee ||B|| < 1.
    matrices = [
        [[Fraction(0), Fraction(1, 3)], [Fraction(1, 3), Fraction(0)]],
        [[Fraction(x, 10) for x in row] for row in [[1, 2, 1], [2, 0, 1], [1, 1, 1]]],
        [[Fraction(x, 20) for x in row] for row in
         [[0, 1, 2, 1], [1, 1, 1, 2], [2, 1, 0, 1], [1, 2, 1, 1]]],
    ]
    marginal_cases = []
    for b in matrices:
        size = len(b)
        for count in range(1, size+1):
            for modes in combinations(range(size), count):
                marginal_matrix(b, modes)
                marginal_cases.append({'mode_count': size, 'kept_modes': list(modes),
                                       'exact_schur_identity': True, 'nonnegative_symmetric': True})

    b = Fraction(1, 3)
    thermal_a = marginal_matrix(matrices[0], [0])
    assert thermal_a == [[0, b*b], [b*b, 0]]
    thermal_cases = []
    for photons in range(7):
        indices = [0]*photons + [1]*photons
        repeated = [[thermal_a[i][j] for j in indices] for i in indices]
        probability = (1-b*b)*hafnian(repeated)/factorial(photons)
        assert probability == (1-b*b)*b**(2*photons)
        thermal_cases.append({'photons': photons, 'probability': str(probability)})

    replica_cases = []
    for copies in range(1, 4):
        actual = prism_count_law(copies, b)
        expected_law = {}
        for photons in range(copies+1):
            falling = factorial(copies)//factorial(copies-photons)
            mass = Fraction(falling, copies**photons)**2*b**(2*photons)
            expected_law[(photons, photons)] = mass
        assert actual == expected_law
        # The exact normalizer ratio is E_P[r_k] for the two-mode squeezed state.
        acceptance = (1-b*b)*sum(actual.values())
        mean = 2*b*b/(1-b*b)
        second_factorial = mean*mean + mean + 4*(b*b/(1-b*b))**2
        assert 1-acceptance <= second_factorial/(2*copies)
        replica_cases.append({'copies_per_mode': copies, 'weighted_prism_vertices': 4*copies,
                              'unnormalized_pattern_masses': {str(k): str(v) for k, v in actual.items()},
                              'normalizer_ratio': str(acceptance),
                              'birthday_bound': str(second_factorial/(2*copies))})

    loop_cases = [check_loop_generating_identity(b) for b in matrices]

    evidence = {
        'status': 'finite interface checks, not source theorem or asymptotic verification',
        'gadget_cases': gadget_cases,
        'weighted_K4': {'original_weighted_hafnian': expected, 'expanded_count': expanded_count,
                        'expanded_vertices': n},
        'first_jet_cases': jet_cases,
        'signed_counterexample': {'hafnian': 0, 'absolute_weight_hafnian': 2},
        'gaussian_marginal_cases': marginal_cases,
        'two_mode_thermal_cases': thermal_cases,
        'collision_replica_cases': replica_cases,
        'loop_generating_cases': loop_cases,
    }
    Path(__file__).with_name('interface_evidence.json').write_text(json.dumps(evidence, indent=2)+'\n')
    print(json.dumps({'gadget_signatures': len(gadget_cases), 'first_jet_ranks': len(jet_cases),
                      'weighted_K4_count': expanded_count, 'gaussian_marginals': len(marginal_cases),
                      'thermal_probabilities': len(thermal_cases), 'collision_replicas': len(replica_cases),
                      'loop_hafnian_patterns': sum(case['patterns_checked'] for case in loop_cases),
                      'violations': 0}))


if __name__ == '__main__':
    main()
