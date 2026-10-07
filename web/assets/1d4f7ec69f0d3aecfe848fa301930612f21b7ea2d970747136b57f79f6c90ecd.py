"""Exact finite convention checks; they do not prove the universal theorem."""
from fractions import Fraction
from itertools import permutations, product
import json
from pathlib import Path
from random import Random

OUT = Path(__file__).with_name('frontier_algebra_checks.json')
rng = Random(20261007)

def inverse(p):
    a = [0] * len(p)
    for j, v in enumerate(p):
        a[v] = j
    return tuple(a)

def compose(a, b):
    return tuple(a[b[j]] for j in range(len(a)))

def pmatrix(p):
    n = len(p)
    a = [[0] * n for _ in range(n)]
    for j, v in enumerate(p):
        a[v][j] = 1
    return a

def rank(a, prime=None):
    b = [[Fraction(v) if prime is None else v % prime for v in row] for row in a]
    k = 0
    for j in range(len(b[0])):
        pivot = next((i for i in range(k, len(b)) if b[i][j]), None)
        if pivot is None:
            continue
        b[k], b[pivot] = b[pivot], b[k]
        inv = 1 / b[k][j] if prime is None else pow(b[k][j], -1, prime)
        b[k] = [v * inv if prime is None else v * inv % prime for v in b[k]]
        for i in range(k + 1, len(b)):
            if b[i][j]:
                t = b[i][j]
                b[i] = [v - t*w if prime is None else (v - t*w) % prime
                        for v, w in zip(b[i], b[k])]
        k += 1
        if k == len(b):
            break
    return k

def blocks(ps, r, d):
    y = [[0] * (r*d) for _ in range(r*d)]
    for u in range(r):
        for v in range(r):
            for j, p in enumerate(ps[u*r+v]):
                y[u*d+p][v*d+j] = 1
    return y

def check_array(ps, r, d):
    y = blocks(ps, r, d)
    eps = Fraction(0)
    for u, uu, v, vv in product(range(r), repeat=4):
        if u == uu or v == vv:
            continue
        p = compose(compose(compose(ps[u*r+v], inverse(ps[uu*r+v])),
                            ps[uu*r+vv]), inverse(ps[u*r+vv]))
        eps = max(eps, Fraction(sum(j == p[j] for j in range(d)), d))
    gram = [[sum(a*b for a, b in zip(row, other)) for other in y] for row in y]
    t1 = sum(gram[j][j] for j in range(r*d))
    t2 = sum(v*v for row in gram for v in row)
    assert t1 == r*r*d
    assert t2 <= (2*r**3-r*r+r*r*(r-1)**2*eps)*d
    rq = rank(y)
    lower = Fraction(r*r*d, 2*r-1+(r-1)**2*eps)
    assert rq >= lower
    for p in (3, 5, 7):
        if p > r:
            assert 2*rank(y, p) >= rq

counts = {'exhaustive_arrays': 0, 'sampled_arrays': 0, 'triangle_blocks': 0,
          'line_certificates': 0, 'prime_iterations': 519,
          'residual_free_words': 0, 'residual_leaf_kill_checks': 0}
for d in (1, 2, 3):
    for ps in product(list(permutations(range(d))), repeat=4):
        check_array(ps, 2, d)
        counts['exhaustive_arrays'] += 1
for r, d in product((2, 3), (2, 3, 4, 5, 7)):
    for _ in range(12):
        ps = [tuple(rng.sample(range(d), d)) for _ in range(r*r)]
        check_array(ps, r, d)
        counts['sampled_arrays'] += 1

# Local Cartesian factorization with arbitrary permutations and controlled mutations.
for d in (2, 3, 5, 7):
    for _ in range(20):
        left = [[tuple(rng.sample(range(d), d)) for j in range(2)] for u in range(2)]
        right = [[tuple(rng.sample(range(d), d)) for k in range(2)] for v in range(2)]
        exact, perturbed, support = [], [], 0
        for alpha, beta in product(range(2), repeat=2):
            e, p = [], []
            for u, v in product(range(2), repeat=2):
                x = compose(inverse(left[u][(alpha+v) % 2]), right[v][(beta+u) % 2])
                z = list(x)
                if rng.randrange(3) == 0:
                    z[0], z[1] = z[1], z[0]
                z = tuple(z)
                support += sum(a != b for a, b in zip(x, z))
                e.append(x); p.append(z)
            exact.append(blocks(e, 2, d)); perturbed.append(blocks(p, 2, d))
        a = [[sum(y[i][j] for y in exact) for j in range(2*d)] for i in range(2*d)]
        b = [[sum(y[i][j] for y in perturbed) for j in range(2*d)] for i in range(2*d)]
        error = [[b[i][j]-a[i][j] for j in range(2*d)] for i in range(2*d)]
        for q in (3, 5, 7):
            assert rank(a, q) <= d
            assert rank(error, q) <= support
            assert rank(b, q) <= d + support
        counts['triangle_blocks'] += 1

# Product interpolation on F_7^2 with S={0,1}; all marked-line directions.
q = 7
marks = list(product((0, 1), repeat=2))
def weight(z):
    f = [((1-z[0]) if a == 0 else z[0])*((1-z[1]) if b == 0 else z[1]) % q
         for a, b in marks]
    return [[a*b % q for b in f] for a in f]
for index, mark in enumerate(marks):
    for direction in [(1, t) for t in range(q)] + [(0, 1)]:
        total = [[0]*4 for _ in range(4)]
        for t in range(1, q):
            z = tuple((a+t*b) % q for a, b in zip(mark, direction))
            h = weight(z)
            total = [[(total[i][j]+h[i][j]) % q for j in range(4)] for i in range(4)]
        assert total == [[(-1 if i == index and j == index else 0) % q
                          for j in range(4)] for i in range(4)]
        counts['line_certificates'] += 1

# Exact, specific prime and acquisition inequalities. Lucas-Lehmer at prime exponent 521.
p = 521
assert all(p % d for d in range(2, 23))
prime = (1 << p)-1
ll = 4
for _ in range(p-2):
    ll = (ll*ll-2) % prime
assert ll == 0
h = 20
c = Fraction(1, 100**h)
r = 100*100**h
Q = 64*r*r/c
m = prime**h
M0 = (prime//100)**h
assert prime > Q and M0 >= c*m/2
assert c*prime/8 >= 8*r*r
reject_bound = Fraction(128*r, 1)/(c*prime) + Fraction(120*r, prime**7)
assert reject_bound < Fraction(1, 2)
assert Fraction(1, 4*r*prime) <= c/4
assert c*r/16-Fraction(5, 2) == Fraction(15, 4)
assert Fraction(15, 800*r*prime) > Fraction(1, 100*r*prime)

# Execute the boundary controls rather than describing them as checked.
identity_blocks = [(0, 1)] * 4
identity_rank = rank(blocks(identity_blocks, 2, 2))
omitted_defect_bound = Fraction(2*2*2, 2*2-1)
assert identity_rank < omitted_defect_bound
small_prime_matrix = [[3, 0], [0, 3]]
small_prime_real_rank = rank(small_prime_matrix)
small_prime_mod_rank = rank(small_prime_matrix, 3)
assert 2*small_prime_mod_rank < small_prime_real_rank
linear_prime, linear_r = 37, 10
scalar_blocks = [[u+1+v+11 for v in range(linear_r)] for u in range(linear_r)]
linear_rank = rank(scalar_blocks, linear_prime)
linear_rectangle_count = 0
for u, uu, v, vv in product(range(linear_r), repeat=4):
    if u == uu or v == vv:
        continue
    rectangle = (scalar_blocks[u][v]*pow(scalar_blocks[uu][v], -1, linear_prime)
                 *scalar_blocks[uu][vv]*pow(scalar_blocks[u][vv], -1, linear_prime)) % linear_prime
    assert rectangle != 1
    linear_rectangle_count += 1
linear_false_bound = Fraction(linear_r*linear_r, 2*(2*linear_r-1))
assert linear_rank < linear_false_bound

# Finite checks of the explicit iterated-commutator word convention.
# The report proves arbitrary-H nontriviality using distinct free-product factors.
def freely_reduce(word):
    reduced = []
    for letter in word:
        if reduced and reduced[-1] == -letter:
            reduced.pop()
        else:
            reduced.append(letter)
    return reduced

def invert_word(word):
    return [-letter for letter in reversed(word)]

residual_word = []
for j in range(1, 9):
    leaf = [1]*j + [j+1] + [-1]*j
    residual_word = (leaf if j == 1 else residual_word + leaf
                     + invert_word(residual_word) + invert_word(leaf))
    assert freely_reduce(residual_word)
    assert len(residual_word) <= 16*(2**j)
    counts['residual_free_words'] += 1
    for k in range(1, j+1):
        killed = [letter for letter in residual_word if abs(letter) != k+1]
        assert not freely_reduce(killed)
        counts['residual_leaf_kill_checks'] += 1

result = {'status': 'PASS', 'counts': counts,
          'specific_prime': str(prime), 'prime_bits': prime.bit_length(),
          'lucas_lehmer_final': str(ll), 'h': h, 'r': str(r),
          'm_decimal_digits': len(str(m)), 'sampled_marks_decimal_digits': len(str(M0)),
          'maximum_incidence_edges_decimal_digits': len(str(M0*(prime-1))),
          'maximum_triangle_relations_decimal_digits': len(str(M0*(prime-1)*r*r)),
          'rejection_bound_exact': str(reject_bound),
          'negative_controls': {
             'omitting_rectangle_defect': {'counterexample_verified': True,
               'observed_rank': identity_rank, 'false_lower_bound': str(omitted_defect_bound)},
             'q_small': {'counterexample_verified': True, 'field_prime': 3,
               'row_norm_squared_budget': 9, 'real_rank': small_prime_real_rank,
               'modular_rank': small_prime_mod_rank},
             'general_linear_rank_freeness': {'counterexample_verified': True,
               'field_prime': linear_prime, 'array_size': linear_r,
               'rank_separated_rectangles': linear_rectangle_count,
               'observed_rank': linear_rank, 'false_lower_bound': str(linear_false_bound)}},
          'scope': 'Finite matrix/interpolation conventions and explicit arithmetic only; no incidence realization, full presentation, geometric proof, Lean replay, or external validation.'}
OUT.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','counts','prime_bits','lucas_lehmer_final','m_decimal_digits','sampled_marks_decimal_digits','maximum_incidence_edges_decimal_digits','maximum_triangle_relations_decimal_digits']}, indent=2))
