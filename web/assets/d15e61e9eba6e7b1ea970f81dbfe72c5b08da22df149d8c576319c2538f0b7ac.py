"""Independent exact audit. Python stdlib only; no source generator imports.

Rebuilds log jets with Fraction, solves the interpolation problem independently,
and builds the 8-dimensional quotient by elementary univariate recurrences.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import math

SOURCE = Path(__file__).resolve().parent.parent/'contact'
OUT = Path(__file__).resolve().parent
P = 101

def conv(a, b, n):
    return [sum((a[j] * b[k-j] for j in range(k+1)), F(0))
            for k in range(n)]

def rref(matrix):
    a = [[F(t) for t in row] for row in matrix]
    pivots = []
    nr, nc = len(a), len(a[0])
    for c in range(nc):
        r = len(pivots)
        pivot = next((i for i in range(r, nr) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = a[r][c]
        a[r] = [v/z for v in a[r]]
        for i in range(nr):
            if i != r and a[i][c]:
                z = a[i][c]
                a[i] = [v-z*w for v, w in zip(a[i], a[r])]
        pivots.append(c)
        if len(pivots) == nr:
            break
    return a, pivots

def det(matrix):
    a = [[F(v) for v in row] for row in matrix]
    value = F(1)
    n = len(a)
    for j in range(n):
        r = next((r for r in range(j, n) if a[r][j]), None)
        if r is None:
            return F(0)
        if r != j:
            a[j], a[r] = a[r], a[j]
            value = -value
        pivot = a[j][j]
        value *= pivot
        for i in range(j+1, n):
            multiplier = a[i][j]/pivot
            for k in range(j+1, n):
                a[i][k] -= multiplier*a[j][k]
    return value

def mod(v):
    v = F(v)
    return v.numerator % P * pow(v.denominator % P, -1, P) % P

fixture_bytes = (SOURCE/'extremal_multiaffine_4.json').read_bytes()
fixture = json.loads(fixture_bytes)
c = fixture['coefficients']
assert fixture['n'] == 4 and len(c) == 16
assert math.gcd(*c) == 1 and c[-1] > 0
original_path = SOURCE.parent/'frontier/d-de03f8ff1da7598d.txt'
original_bytes = None
if original_path.is_file():
    original_bytes = original_path.read_bytes()
    original_fixture = next(v for v in json.loads(original_bytes) if v['n'] == 4)
    original_coefficients = [0]*16
    for term in original_fixture['terms']:
        exponents = term['exponents']
        assert len(exponents) == 4 and all(e in (0,1) for e in exponents)
        mask = sum(e << i for i,e in enumerate(exponents))
        assert not original_coefficients[mask]
        original_coefficients[mask] = int(term['coefficient'])
    assert original_coefficients == c
    assert original_fixture['order'] == 15
# Compute every masked monomial's log jet independently.
L = 18
logs = [[F(0)] + [F((-1)**(k+1), k*i**k) for k in range(1, L)]
        for i in range(1, 5)]
jets = []
for mask in range(16):
    jet = [F(1)] + [F(0)]*(L-1)
    for i in range(4):
        if mask & (1 << i):
            jet = conv(jet, logs[i], L)
    jets.append(jet)
jet_matrix = [[jets[mask][k] for mask in range(16)] for k in range(L)]
reduced, pivots = rref(jet_matrix[:15])
assert pivots == list(range(15)), pivots
independent_normalized = [-reduced[i][15] for i in range(15)] + [F(1)]
assert independent_normalized == [F(v,c[-1]) for v in c]
_, pivots16 = rref(jet_matrix[:16])
assert len(pivots16) == 16
pullback = [sum((c[i]*jets[i][k] for i in range(16)), F(0))
            for k in range(L)]
assert all(v == 0 for v in pullback[:15]) and pullback[15] != 0
assert [[k,str(pullback[k])] for k in range(15,18)] == fixture['first_nonzero']

# Principal-minor convention: coefficient of x_[4]\\S is det A[S,S].
q = independent_normalized
minor = lambda indices: q[15 ^ sum(1 << i for i in indices)]
a = [minor([i]) for i in range(4)]
r = {(i,j): a[i]*a[j]-minor([i,j]) for i,j in combinations(range(4),2)}
def t(i,j,k):
    return (minor([i,j,k])-a[i]*a[j]*a[k]
            + a[i]*r[j,k]+a[j]*r[i,k]+a[k]*r[i,j])

# u^2=alpha*u+beta, etc. Nonzero mod P confirms all inversions legal
# over the localization Z_(P), as well as over Q.
assert c[-1] % P
assert all(mod(v) for v in r.values())
reductions = [(t(0,1,2)/r[0,2], -r[0,1]*r[1,2]/r[0,2]),
              (t(0,1,3)/r[0,3], -r[0,1]*r[1,3]/r[0,3]),
              (t(0,2,3)/r[0,3], -r[0,2]*r[2,3]/r[0,3])]
base = list(product(range(2), repeat=3))
g_terms = {(2,0,2):r[1,3], (0,2,0):r[1,2]*r[2,3],
           (1,1,1):-t(1,2,3)}

def make_matrix(red, terms):
    powers = []
    for alpha,beta in red:
        values = [(F(1),F(0)), (F(0),F(1))]
        for n in range(2,4):
            x,y = values[-1]
            values.append((y*beta, x+y*alpha))
        powers.append(values)
    matrix = [[F(0) for _ in base] for _ in base]
    for j,b in enumerate(base):
        for e,coefficient in terms.items():
            degree = tuple(e[i]+b[i] for i in range(3))
            for k,target in enumerate(base):
                value = coefficient
                for i in range(3):
                    value *= powers[i][degree[i]][target[i]]
                matrix[k][j] += value
    return matrix

mq = make_matrix(reductions, g_terms)
mp = [[mod(v) for v in row] for row in mq]
# A separate construction with reduced input agrees, not just the final norm.
mp_from_reduced_inputs = make_matrix([(mod(x),mod(y)) for x,y in reductions],
                                    {e:mod(v) for e,v in g_terms.items()})
assert mp == [[mod(v) for v in row] for row in mp_from_reduced_inputs]
source_cert = json.loads((SOURCE/'norm_certificate_mod101.json').read_text())
assert mp == source_cert['multiplication_matrix']
np = mod(det(mp))
assert np == source_cert['norm'] == 17
nq = det(mq)
assert nq and mod(nq) == 17

# Provide a checkable inverse witness for g in the finite F101 quotient.
# Solve over Q first for the integer representative matrix, then reduce mod P.
aug = [row+[int(i==0)] for i,row in enumerate(mp)]
rr,pi = rref(aug)
assert pi == list(range(8))
inverse = [mod(rr[i][-1]) for i in range(8)]
assert [sum(mp[i][j]*inverse[j] for j in range(8)) % P for i in range(8)] == [1,0,0,0,0,0,0,0]

result = {
    'status':'PASS: exact contact and necessary principal-minor obstruction',
    'fixture_sha256':hashlib.sha256(fixture_bytes).hexdigest(),
    'source_fixture_path':str(original_path),
    'source_fixture_sha256':hashlib.sha256(original_bytes).hexdigest() if original_bytes is not None else None,
    'source_fixture_terms_identical':True if original_bytes is not None else 'not rerun: external source excluded from this archive',
    'independent_method':'Python stdlib Fraction arithmetic; no SymPy or generator imports',
    'jet_rank_rows_0_through_14':len(pivots),
    'jet_rank_rows_0_through_15':len(pivots16),
    'normalization':'coefficient of x1*x2*x3*x4 equals 1',
    'fixture_matches_independent_kernel':True,
    'first_nonzero_primitive_integer_pullback':[15,str(pullback[15])],
    'first_nonzero_monic_pullback':[15,str(pullback[15]/c[-1])],
    'full_monomial_integer_coefficient_mod101':c[-1] % P,
    'diagonal_mod101':[mod(v) for v in a],
    'pair_products_mod101':{str(k):mod(v) for k,v in r.items()},
    'triple_cycle_sums_mod101':{str(k):mod(t(*k)) for k in combinations(range(4),3)},
    'quadratic_reduction_alpha_beta_mod101':[[mod(x),mod(y)] for x,y in reductions],
    'basis_exponents':base,
    'multiplication_matrix_mod101':mp,
    'norm_mod101':np,
    'inverse_of_g_coefficients_mod101':inverse,
    'norm_over_Q':str(nq),
    'norm_over_Q_numerator_digits':len(str(abs(nq.numerator))),
    'norm_over_Q_denominator_digits':len(str(nq.denominator)),
    'rational_norm_reduces_to_modular_norm':True,
    'algebraic_closure_exclusion':'Invertible multiplication by g in a finite free quotient implies g is a unit; a common zero in any field extension would contradict g*h=1.'
}
(OUT/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('norm_over_Q','multiplication_matrix_mod101')},indent=2))
