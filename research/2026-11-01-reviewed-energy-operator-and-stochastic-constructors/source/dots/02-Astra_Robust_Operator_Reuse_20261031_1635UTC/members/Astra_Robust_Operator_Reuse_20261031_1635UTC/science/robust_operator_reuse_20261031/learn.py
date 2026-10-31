#!/usr/bin/env python3
"""Exact rational observable certificates; ordinary retained Krylov acquisition."""
from fractions import Fraction as F
from pathlib import Path
import json
import random
import re
import sys
import time
import sympy as sp

sys.set_int_max_str_digits(0)  # Known finite exact-rational artifacts, not IEEE doubles.


def inner(x, y, pi):
    return sum(pi[i]*x[i]*y[i] for i in range(len(pi)))


def metric(matrices):
    if type(matrices) not in (list,tuple) or not matrices or not all(isinstance(A,sp.MatrixBase) for A in matrices):
        raise ValueError('nonempty rational matrix family required')
    n = matrices[0].rows
    if n<1:raise ValueError('positive matrix dimension required')
    one = sp.ones(n, 1)
    assert matrices and all(A.shape == (n, n) for A in matrices)
    for A in matrices:
        assert all(isinstance(x,sp.Rational) for x in A) and all(x >= 0 for x in A)
        assert A*one == one
    null = (matrices[0].T-sp.eye(n)).nullspace()
    if len(null) != 1:
        raise ValueError('INCONCLUSIVE: unique positive equilibrium not acquired')
    pi = null[0] / sum(null[0])
    assert all(x > 0 for x in pi)
    for A in matrices:
        if A.T*pi != pi:
            raise ValueError('INCONCLUSIVE: no verified common equilibrium')
    d = min(A[i,j]/pi[j] for A in matrices for i in range(n) for j in range(n))
    assert 0 <= d <= 1
    H = sp.diag(*pi)
    adjoints = [H.inv()*A.T*H for A in matrices]
    return pi, adjoints, 1-d


def residual(x, basis, pi):
    out = x.copy()
    for v in basis:
        out -= v * (inner(v, x, pi)/inner(v, v, pi))
    return out


def sum_kernel(length, alpha):
    # Exact nonnegative recurrence, including alpha=0/1.
    geom = sp.Rational(0)
    total = sp.Rational(0)
    for _ in range(length):
        total += geom
        geom = 1 + alpha*geom
    return total


def measure(basis, images, pi, m):
    bounds = [sp.Rational(0), sp.Rational(0)]
    best = (sp.Rational(-1), None)
    for side in range(2):
        for a in range(m):
            total = sp.Rational(0)
            for j, v in enumerate(basis):
                e = residual(images[side][a][j], basis, pi)
                score = inner(e, e, pi)/inner(v, v, pi)
                assert score >= 0
                total += score
                if score > best[0]:
                    best = score, e
            bounds[side] = max(bounds[side], total)
    return bounds, best


def acquire(matrices, b, c, length, tolerance, stopping='quadratic'):
    assert type(length) is int and length >= 0
    tolerance = sp.Rational(tolerance)
    assert tolerance > 0 and stopping in ('quadratic', 'state')
    start = time.perf_counter()
    pi, adjoints, alpha = metric(matrices)
    n = matrices[0].rows
    assert isinstance(b,sp.MatrixBase) and isinstance(c,sp.MatrixBase)
    assert b.shape == c.shape == (n, 1)
    assert all(isinstance(x,sp.Rational) for x in list(b)+list(c))
    basis = []
    images = [[[] for _ in matrices] for _ in range(2)]
    mvps = 0

    def append(x):
        nonlocal mvps
        e = residual(x, basis, pi)
        if e == sp.zeros(n, 1):
            return False
        # A rational rescaling avoids gratuitously tiny denominators; no sqrt.
        j = max(range(n), key=lambda k: abs(e[k]))
        e = e/e[j]
        basis.append(e)
        for side, operators in enumerate((matrices, adjoints)):
            for a, A in enumerate(operators):
                images[side][a].append(A*e)
                mvps += 1
        return True

    for x in (sp.ones(n,1), b, c):
        append(x)
    rounds = []
    S = sum_kernel(length, alpha)
    norm_product_squared = inner(b,b,pi)*inner(c,c,pi)
    while True:
        (in2, out2), best = measure(basis, images, pi, len(matrices))
        product_bound = (in2+out2)/2
        quadratic_bound_squared = product_bound**2*S**2*norm_product_squared
        state_bound_squared = length**2*in2*norm_product_squared
        rounds.append({'rank':len(basis), 'enter_squared':str(in2), 'return_squared':str(out2),
                       'quadratic_error_bound_squared':str(quadratic_bound_squared),
                       'state_error_bound_squared':str(state_bound_squared)})
        bound = quadratic_bound_squared if stopping == 'quadratic' else state_bound_squared
        if bound <= tolerance**2:
            break
        assert len(basis) < n and best[0] > 0
        assert append(best[1])
    V = sp.Matrix.hstack(*basis)
    G = V.T*sp.diag(*pi)*V
    assert G == sp.diag(*[G[i,i] for i in range(G.rows)])
    B = [G.inv()*V.T*sp.diag(*pi)*A*V for A in matrices]
    u = G.inv()*V.T*sp.diag(*pi)*b
    v = G.inv()*V.T*sp.diag(*pi)*c
    assert V*u == b and V*v == c
    rationals = list(V)+list(G)+list(u)+list(v)
    for A in B:
        rationals += list(A)
    maxbits = max(max(abs(int(x.p)).bit_length(), int(x.q).bit_length()) for x in rationals)
    return {'basis':V,'gram':G,'operators':B,'left':v,'right':u,'pi':pi,
            'alpha':alpha,'rounds':rounds,'stopping':stopping,'length':length,
            'tolerance':tolerance,'quadratic_error_bound_squared':quadratic_bound_squared,
            'state_error_bound_squared':state_bound_squared,
            'ledger':{'rank':V.cols,'ambient':n,'generators':len(matrices),
                      'generator_or_adjoint_vector_products':mvps,
                      'retained_construction_image_entries':2*len(matrices)*n*V.cols,
                      'stored_reduced_operator_entries':len(matrices)*V.cols**2,
                      'max_representation_entry_bits':maxbits,
                      'bit_scope':'Representation entries only here; serialization is scanned separately. Intermediate arithmetic is not fully instrumented.',
                      'acquisition_seconds':time.perf_counter()-start}}


def evaluate(model, word):
    assert len(word) <= model['length']
    x = model['right']
    for a in word:
        assert type(a) is int and 0 <= a < len(model['operators'])
        x = model['operators'][a]*x
    return (model['left'].T*model['gram']*x)[0]


def exact(matrices, b, c, pi, word):
    x = b
    for a in word:
        x = matrices[a]*x
    return inner(c,x,pi)


def fixture(n=12, groups=3, noise=sp.Rational(1,10000), seed=718):
    assert n % groups == 0
    rng = random.Random(seed)
    def symmetric_kernel(size):
        W = sp.zeros(size)
        for i in range(size):
            for j in range(i):
                W[i,j] = W[j,i] = rng.randrange(1,8)
        ds = [sum(W.row(i)) for i in range(size)]
        return sp.eye(size)-(sp.diag(*ds)-W)/(2*max(ds))
    perm = list(range(n));rng.shuffle(perm)
    mats=[]
    for _ in range(2):
        Q = symmetric_kernel(groups)
        lifted = sp.kronecker_product(Q,sp.ones(n//groups)/(n//groups))
        base = sp.eye(n)/5 + sp.Rational(4,5)*lifted
        raw = (1-noise)*base + noise*symmetric_kernel(n)
        mats.append(raw.extract(perm,perm))
    b=sp.eye(n)[:,0];c=sp.eye(n)[:,n//2]
    return mats,b,c


def encode_matrix(A):
    return [[[int(A[i,j].p),int(A[i,j].q)] for j in range(A.cols)] for i in range(A.rows)]


def encode(model):
    out={k:v for k,v in model.items() if k not in ('basis','gram','operators','left','right','pi')}
    for k in ('alpha','tolerance','quadratic_error_bound_squared','state_error_bound_squared'):
        out[k]=str(out[k])
    for k in ('basis','gram','left','right','pi'):
        out[k]=encode_matrix(model[k])
    out['operators']=[encode_matrix(A) for A in model['operators']]
    def integer_bits(x):
        if type(x) is int:return abs(x).bit_length()
        if type(x) is list:return max((integer_bits(y) for y in x),default=0)
        if type(x) is dict:return max((integer_bits(y) for y in x.values()),default=0)
        if type(x) is str and re.fullmatch(r'-?[0-9]+(?:/[1-9][0-9]*)?',x):
            f=F(x);return max(abs(f.numerator).bit_length(),f.denominator.bit_length())
        return 0
    out['ledger']['max_serialized_rational_integer_bits']=integer_bits(out)
    return out


if __name__ == '__main__':
    mats,b,c=fixture()
    result={}
    for rule in ('quadratic','state'):
        model=acquire(mats,b,c,30,sp.Rational(1,100000),rule)
        result[rule]=encode(model)
        print(rule,model['ledger'],flush=True)
    Path('acquisition_results.json').write_text(json.dumps(result,indent=2)+'\n')
