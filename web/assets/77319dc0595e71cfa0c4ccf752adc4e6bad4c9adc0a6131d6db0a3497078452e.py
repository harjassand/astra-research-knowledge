"""Exact diagnostics for a bounded-precision sparse nc acquisition construction.

Oracle evaluation and decoding are separate. Fraction.limit_denominator implements
continued-fraction rational recovery; SymPy is used for exact rank/linear algebra
and integer-root factoring in these finite diagnostics.
"""
from fractions import Fraction as F
from math import comb
import json
import random
from pathlib import Path
import sympy as sp


def zero(d):
    return [[F(0) for _ in range(d)] for _ in range(d)]


def identity(d):
    a = zero(d)
    for i in range(d):
        a[i][i] = F(1)
    return a


def mul(a, b):
    d = len(a)
    c = zero(d)
    for i in range(d):
        for k in range(d):
            if a[i][k]:
                for j in range(d):
                    if b[k][j]:
                        c[i][j] += a[i][k] * b[k][j]
    return c


def query(n, s):
    d = 2*s
    B = 1
    while B <= n+1:
        B *= 2
    matrices = []
    for i in range(1, n+1):
        a = zero(d)
        for row in range(d):
            for col in range(row, d):
                a[row][col] = F(comb(col, row)*i**(col-row), B**col)
        assert max(sum(abs(a[row][col]) for row in range(d))
                   for col in range(d)) == 1
        matrices.append(a)
    return B, matrices


def exact_oracle(matrices, terms):
    d = len(matrices[0])
    answer = zero(d)
    for word, coefficient in terms:
        w = identity(d)
        for letter in word:
            w = mul(w, matrices[letter-1])
        for i in range(d):
            for j in range(d):
                answer[i][j] += coefficient*w[i][j]
    return answer


def approximate_oracle(answer, precision, seed):
    scale = 1 << precision
    result = zero(len(answer))
    for i in range(len(answer)):
        for j in range(len(answer)):
            x = answer[i][j]*scale
            floor = x.numerator//x.denominator
            perturbation = F((-1 if (i+j+seed)%2 else 1), 2*scale)
            result[i][j] = F(floor, scale)+perturbation
            assert abs(result[i][j]-answer[i][j]) <= F(3, 2*scale)
    return result


def to_sympy(q):
    return sp.Rational(q.numerator, q.denominator)


def decode(n, s, degree, height, approximate):
    B, _ = query(n, s)
    d = 2*s
    Q = (1 << (s*height))*B**((d-1)*degree)
    recovered = [[q.limit_denominator(Q) for q in row] for row in approximate]
    t = [sum(recovered[i][j] for i in range(d)) for j in range(d)]
    # beta(w)=B**degree*alpha(w) is an integer for every legal word.
    moments = [to_sympy(t[k]*B**(degree*k)) for k in range(d)]
    hankel = sp.Matrix(s, s, lambda i, j: moments[i+j])
    rank = hankel.rank()
    if rank == 0:
        return [], recovered
    leading = hankel[:rank, :rank]
    rhs = -sp.Matrix(moments[rank:2*rank])
    recurrence = list(leading.inv()*rhs)
    z = sp.Symbol('z')
    poly = sp.Poly(z**rank+sum(recurrence[k]*z**k for k in range(rank)), z)
    roots_dict = sp.polys.polytools.ground_roots(poly)
    assert len(roots_dict) == rank and all(x == 1 for x in roots_dict.values())
    roots = sorted(int(a) for a in roots_dict)
    vandermonde = sp.Matrix(rank, rank, lambda i, j: roots[j]**i)
    coefficients = list(vandermonde.inv()*sp.Matrix(moments[:rank]))
    result = []
    for beta, coefficient in zip(roots, coefficients):
        if beta == B**degree:
            word = ()
        else:
            q = beta
            trailing = 0
            while q % B == 0:
                trailing += 1
                q //= B
            length = degree-trailing
            digits = []
            while q:
                digits.append(q % B)
                q //= B
            assert len(digits) == length
            word = (digits[0]-1, *digits[1:])
            assert all(1 <= x <= n for x in word)
        result.append((word, F(int(coefficient.p), int(coefficient.q))))
    return sorted(result), recovered


def canonical(terms):
    combined = {}
    for word, coefficient in terms:
        combined[word] = combined.get(word, F(0))+coefficient
    return sorted((word, coefficient) for word, coefficient in combined.items()
                  if coefficient)


def inertia(matrix):
    """Exact rational symmetric elimination, including zero diagonal pivots."""
    a = sp.Matrix(matrix)
    positive = negative = zeros = 0
    while a.rows:
        n = a.rows
        pivot = next((i for i in range(n) if a[i, i] != 0), None)
        if pivot is not None:
            order = [pivot]+[i for i in range(n) if i != pivot]
            a = a.extract(order, order)
            value = a[0, 0]
            positive += 1 if value > 0 else 0
            negative += 1 if value < 0 else 0
            a = a[1:, 1:]-a[1:, :1]*a[:1, 1:]/value
        else:
            pair = next(((i, j) for i in range(n) for j in range(i+1, n)
                         if a[i, j] != 0), None)
            if pair is None:
                zeros += n
                break
            order = list(pair)+[i for i in range(n) if i not in pair]
            a = a.extract(order, order)
            positive += 1
            negative += 1
            a = a[2:, 2:]-a[2:, :2]*a[:2, :2].inv()*a[:2, 2:]
    return positive, negative, zeros


def robust_precision(n, s, degree, height):
    B, _ = query(n, s)
    d = 2*s
    U = 2**(s-1)*B**(degree*(s-1))
    K = 2**height*s*s*U*U
    annihilator_denominator = 32*K*s*d*2**s*B**(degree*s)
    coefficient_denominator = 8*s*U*d*2**(2*height)
    needed = max(annihilator_denominator, coefficient_denominator)
    return (needed-1).bit_length()+4


def robust_decode(n, s, degree, height, approximate):
    """Decode noisy moments before recovering exact full response entries."""
    B, _ = query(n, s)
    d = 2*s
    U = 2**(s-1)*B**(degree*(s-1))
    K = 2**height*s*s*U*U
    t = [to_sympy(sum(approximate[i][j] for i in range(d))) for j in range(d)]
    hankel = sp.Matrix(s, s, lambda i, j: t[i+j])
    threshold = sp.Rational(1, 4*K)
    rank = inertia(hankel-threshold*sp.eye(s))[0]+inertia(
        hankel+threshold*sp.eye(s))[1]
    if rank == 0:
        return []
    p = list(hankel[:rank, :rank].inv()*(-sp.Matrix(t[rank:2*rank])))
    z = sp.Symbol('z')
    p_integer = [int(sp.floor(p[j]*B**(degree*(rank-j))+sp.Rational(1, 2)))
                 for j in range(rank)]
    poly = sp.Poly(z**rank+sum(p_integer[j]*z**j for j in range(rank)), z)
    roots_dict = sp.polys.polytools.ground_roots(poly)
    assert len(roots_dict) == rank and all(x == 1 for x in roots_dict.values())
    roots = sorted(int(a) for a in roots_dict)
    alpha = [sp.Rational(a, B**degree) for a in roots]
    vandermonde = sp.Matrix(rank, rank, lambda i, j: alpha[j]**i)
    c_approx = list(vandermonde.inv()*sp.Matrix(t[:rank]))
    result = []
    for beta, coefficient in zip(roots, c_approx):
        if beta == B**degree:
            word = ()
        else:
            q = beta
            trailing = 0
            while q % B == 0:
                trailing += 1
                q //= B
            length = degree-trailing
            digits = []
            while q:
                digits.append(q % B)
                q //= B
            assert len(digits) == length
            word = (digits[0]-1, *digits[1:])
            assert all(1 <= x <= n for x in word)
        recovered = F(int(coefficient.p), int(coefficient.q)).limit_denominator(2**height)
        result.append((word, recovered))
    return sorted(result)


def main():
    rng = random.Random(10172026)
    cases = []
    for trial in range(72):
        n = 1+trial%3
        s = 1+trial%4
        degree = 1+trial%17
        height = 8
        B, matrices = query(n, s)
        terms = []
        words = set()
        target = rng.randrange(min(s, sum(n**k for k in range(degree+1)))+1)
        while len(words) < target:
            word = tuple(rng.randint(1, n) for _ in range(rng.randint(0, degree)))
            words.add(word)
        for word in sorted(words):
            coefficient = F(rng.choice([-1, 1])*rng.randint(1, 200),
                            rng.randint(1, 200))
            terms.append((word, coefficient))
        if trial == 3:
            terms = [((), F(1)), ((1,), F(-1))]
        if trial == 7:
            terms = [((1, 2), F(1, 7)), ((2, 1), F(-1, 7))]
        if trial == 11:
            terms = [((1,)*degree, F(1, 251)), ((1,)*(degree-1), F(-1, 251))]
        assert len(terms) <= s
        answer = exact_oracle(matrices, terms)
        qbits = s*height+(2*s-1)*degree*(B.bit_length()-1)
        Q = 1 << qbits
        precision = 2*qbits+4
        assert all(q.denominator <= Q for row in answer for q in row)
        assert max(abs(q) for row in answer for q in row) <= s*(1 << height)
        approximate = approximate_oracle(answer, precision, trial)
        expected = canonical(terms)
        decoded, recovered = decode(n, s, degree, height, approximate)
        assert recovered == answer
        assert decoded == expected, (trial, decoded, expected)
        p_robust = robust_precision(n, s, degree, height)
        approx_robust = approximate_oracle(answer, p_robust, trial)
        decoded_robust = robust_decode(n, s, degree, height, approx_robust)
        assert decoded_robust == expected, (trial, decoded_robust, expected)
        cases.append(dict(trial=trial, n=n, s=s, degree=degree, height=height,
                          dimension=2*s, precision=precision,
                          improved_precision=p_robust,
                          actual_terms=len(expected), rational_recovery=True,
                          word_coefficient_recovery=True,
                          improved_moment_recovery=True))
    # The characteristic-two shortcut in TR26-173 is singular.
    a = [[0, 1], [0, 0]]
    b = [[0, 0], [1, 0]]
    ab = mul(a, b)
    ba = mul(b, a)
    commutator_mod2 = [[int(ab[i][j]+ba[i][j]) % 2 for j in range(2)]
                       for i in range(2)]
    assert commutator_mod2 == [[1, 0], [0, 1]]
    quantized_sketch_checks = []
    for trial in range(32):
        n = 3+trial%3
        latent = sp.zeros(n, n)
        for _ in range(4):
            latent[rng.randrange(n), rng.randrange(n)] = rng.randint(-5, 5)
        noise = sp.Matrix(n, n, lambda i, j:
                          sp.Rational(rng.choice([-1, 0, 1]), 4*n*n))
        assert sum(abs(x) for x in noise) < sp.Rational(1, 2)
        H = sp.Matrix(2+trial%3, n, lambda i, j: rng.randrange(2))
        G = sp.Matrix(2+trial%2, n, lambda i, j: rng.randrange(2))
        noisy = H*(latent+noise)*G.T
        rounded = noisy.applyfunc(lambda x: sp.floor(x+sp.Rational(1, 2)))
        assert rounded == H*latent*G.T
        quantized_sketch_checks.append(True)
    # Frobenius-small noise alone does not make binary measurement rounding exact.
    n = 3
    noise = sp.ones(n, n)*sp.Rational(1, 4*n)
    assert sum(x*x for x in noise) == sp.Rational(1, 16)
    bad_sketch = (sp.ones(1, n)*noise*sp.ones(n, 1))[0]
    assert bad_sketch == sp.Rational(3, 4)
    assert sp.floor(bad_sketch+sp.Rational(1, 2)) == 1
    output = dict(status='all finite diagnostics passed', count=len(cases),
                  cases=cases, characteristic_two_commutator=commutator_mod2,
                  quantized_sketch_check_count=len(quantized_sketch_checks),
                  frobenius_noise_counterexample=str(bad_sketch),
                  universal_claim='proved in accompanying report; tests are scoped')
    Path('work/cycle1/algebra_contracting_sparse_checks.json').write_text(
        json.dumps(output, indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'cases'}))


if __name__ == '__main__':
    main()
