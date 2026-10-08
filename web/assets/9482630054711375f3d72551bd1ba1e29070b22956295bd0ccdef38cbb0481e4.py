"""Exact finite diagnostics for the independent contact lemmas.

These checks supplement the proofs in complexity_proof_recon.txt. They are not
a formal proof or a general-circuit identity test. Uses only the Python stdlib.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb, factorial
from pathlib import Path
import json
import random


def mul(a, b, length):
    out = [Q(0)] * length
    for i, x in enumerate(a[:length]):
        if x:
            for j, y in enumerate(b[:length-i]):
                if y:
                    out[i+j] += x*y
    return out


def power(a, exponent, length):
    out = [Q(1)] + [Q(0)] * (length-1)
    while exponent:
        if exponent & 1:
            out = mul(out, a, length)
        exponent //= 2
        if exponent:
            a = mul(a, a, length)
    return out


def inverse(a, length):
    assert a[0]
    out = [1/a[0]]
    for k in range(1, length):
        out.append(-sum(a[j]*out[k-j] for j in range(1,k+1))/a[0])
    return out


def log_unit(a, length):
    assert a[0] == 1
    inv = inverse(a, length)
    derivative = [j*a[j] for j in range(1, length)]
    hprime = mul(derivative, inv, length-1)
    return [Q(0)] + [hprime[k-1]/k for k in range(1, length)]


def unit_monomial(alpha, length):
    # (prod i**alpha[i]) * ell**alpha / z**sum(alpha)
    out = [Q(1)] + [Q(0)]*(length-1)
    for i, a in enumerate(alpha, 1):
        unit = [Q((-1)**k, (k+1)*i**k) for k in range(length)]
        out = mul(out, power(unit, a, length), length)
    return out


def compositions(d, n):
    if n == 1:
        yield (d,)
        return
    for first in range(d+1):
        for tail in compositions(d-first, n-1):
            yield (first,) + tail


def binomial_check(alpha, beta):
    assert sum(alpha) == sum(beta) and alpha != beta
    n = len(alpha)
    e = [a-b for a,b in zip(alpha,beta)]
    m = sum(x != 0 for x in e)
    first_moment = next(k for k in range(1,m)
                        if sum(Q(x,i**k) for i,x in enumerate(e,1)))
    a = unit_monomial(alpha, n+1)
    b = unit_monomial(beta, n+1)
    first_series = next(k for k in range(n+1) if a[k] != b[k])
    assert first_series == first_moment <= m-1
    return sum(alpha) + first_series


def main():
    length = 31
    g = [Q((-1)**k,k+1) for k in range(length)]
    h = log_unit(g, length)
    assert all((-1)**k*h[k] > 0 for k in range(1,length))
    positive_g = [Q(1,k+1) for k in range(length)]
    reciprocal = inverse(positive_g,length)
    assert all(x < 0 for x in reciprocal[1:])
    # An independent classical unsigned-Stirling coefficient expression.
    stirling = [1]
    for k in range(1,length):
        row = [0]*(k+1)
        for j in range(1,k+1):
            row[j] = (stirling[j-1]
                      + (k-1)*(stirling[j] if j < len(stirling) else 0))
        stirling = row
        c2 = sum(Q(row[j],j+1) for j in range(1,k+1))
        assert h[k] == Q((-1)**k, k*factorial(k))*c2

    count = 0
    for n in range(2,5):
        for d in range(1,7):
            for a,b in combinations(list(compositions(d,n)),2):
                binomial_check(a,b)
                count += 1
    rng = random.Random(250246)
    random_count = 0
    for n in range(2,13):
        for _ in range(25):
            d = rng.randrange(1,51)
            a,b = [0]*n,[0]*n
            for _ in range(d):
                a[rng.randrange(n)] += 1
                b[rng.randrange(n)] += 1
            if a != b:
                binomial_check(tuple(a),tuple(b))
                random_count += 1

    sharp = []
    for n in range(2,13):
        e = [(-1)**(i-1)*comb(n-1,i-1)*i**(n-2) for i in range(1,n+1)]
        a = tuple(max(x,0) for x in e)
        b = tuple(max(-x,0) for x in e)
        assert sum(a) == sum(b)
        contact = binomial_check(a,b)
        assert contact == sum(a)+n-1
        sharp.append({'n':n,'degree':sum(a),'contact':contact,
                      'alpha':a,'beta':b})

    # Sharp affine forms L_n have coefficient (-1)^(n-1)/n^2 at z^n.
    for n in range(1,31):
        c = [(-1)**(i-1)*comb(n-1,i-1)*i**(n-1)
             for i in range(1,n+1)]
        for k in range(1,n):
            assert sum(Q(x,i**k) for i,x in enumerate(c,1)) == 0
        assert Q((-1)**(n-1),n)*sum(Q(x,i**n) for i,x in enumerate(c,1)) == Q((-1)**(n-1),n*n)

    # A degree-two rational pullback genuinely gives order two, and needs two logs.
    # 1 + (z^2/(z+1))/4 = (z+2)^2/(4(z+1)).
    ell1 = [Q(0)] + [Q((-1)**(k-1),k) for k in range(1,10)]
    ell2 = [Q(0)] + [Q((-1)**(k-1),k*2**k) for k in range(1,10)]
    pullback_log = [2*b-a for a,b in zip(ell1,ell2)]
    assert next(k for k,x in enumerate(pullback_log) if x) == 2
    assert pullback_log[2] == Q(1,4)

    result = {'status':'PASS','scope':'finite exact diagnostics; proofs remain separate',
              'h_coefficient_and_stirling_checks':length-1,
              'exhaustive_normalized_binomials_n_2_to_4_degree_1_to_6':count,
              'seeded_normalized_binomials_n_2_to_12_degree_at_most_50':random_count,
              'sharp_binomial_families':sharp,
              'sharp_affine_forms_n_1_to_30':30,
              'rational_pullback_fixture':{'R':'z^2/(z+1)','target_pole':4,
                  'source_poles':[1,2],'identity':'ell_4(R)=2 ell_2-ell_1','order':2}}
    out = Path(__file__).with_name('contact_checks.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'sharp_binomial_families'},indent=2))


if __name__ == '__main__':
    main()
