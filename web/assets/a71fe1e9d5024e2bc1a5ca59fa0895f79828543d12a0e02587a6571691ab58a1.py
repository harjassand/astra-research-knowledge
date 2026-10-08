#!/usr/bin/env python3
"""Exact finite checks for the logarithmic PIT investigation.

Python >= 3.10; standard library only. This checks finite certificates, not
all-parameter theorems or historical novelty. Run beside contact_examples.json:
    python verify.py --output verification_results.json
No network, randomness, floating point, or external theorem prover is used.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import product, permutations
from math import comb, factorial
from pathlib import Path
import json
import sys

Poly = dict[tuple[int, ...], F]


def rank(rows: list[list[F | int]]) -> int:
    if not rows:
        return 0
    a = [[F(x) for x in row] for row in rows]
    cols = len(a[0])
    if any(len(row) != cols for row in a):
        raise ValueError('Ragged matrix')
    r = 0
    for c in range(cols):
        pivot = next((j for j in range(r, len(a)) if a[j][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = a[r][c]
        a[r] = [x/z for x in a[r]]
        for j in range(r+1, len(a)):
            z = a[j][c]
            if z:
                for k in range(c, cols):
                    a[j][k] -= z*a[r][k]
        r += 1
        if r == len(a):
            break
    return r


def mul(a: list[F], b: list[F], L: int) -> list[F]:
    out = [F(0)]*L
    for i, ai in enumerate(a[:L]):
        if ai:
            for j, bj in enumerate(b[:L-i]):
                if bj:
                    out[i+j] += ai*bj
    return out


def logs(n: int, L: int) -> list[list[F]]:
    return [[F(0)]+[F((-1)**(k-1), k*i**k) for k in range(1,L)]
            for i in range(1,n+1)]


def jet(poly: Poly, xs: list[list[F]], L: int) -> list[F]:
    n = len(xs)
    maxes = [max((e[i] for e in poly), default=0) for i in range(n)]
    powers = []
    for i in range(n):
        arr = [[F(1)]+[F(0)]*(L-1)]
        for k in range(maxes[i]):
            arr.append(mul(arr[-1], xs[i], L))
        powers.append(arr)
    ans = [F(0)]*L
    for exponents, coefficient in poly.items():
        value = [F(1)]+[F(0)]*(L-1)
        for i, e in enumerate(exponents):
            value = mul(value, powers[i][e], L)
        ans = [a+coefficient*b for a,b in zip(ans,value)]
    return ans


def ord0(a: list[F]) -> int | None:
    return next((i for i,x in enumerate(a) if x), None)


def diff(p: Poly, i: int) -> Poly:
    out: Poly = {}
    for exponents,c in p.items():
        if exponents[i]:
            e = list(exponents)
            e[i] -= 1
            out[tuple(e)] = c*exponents[i]
    return out


def derivative_dimension(p: Poly) -> int:
    if not p:
        return 0
    n = len(next(iter(p)))
    derivatives: list[Poly] = []
    stack = [p]
    seen = set()
    while stack:
        q = stack.pop()
        signature = tuple(sorted(q.items()))
        if not q or signature in seen:
            continue
        seen.add(signature)
        derivatives.append(q)
        stack.extend(diff(q,i) for i in range(n))
    monomials = sorted({e for q in derivatives for e in q})
    return rank([[q.get(e,F(0)) for e in monomials] for q in derivatives])


def eval_poly(p: Poly, values: list[F]) -> F:
    ans = F(0)
    for exponents,c in p.items():
        v = c
        for x,e in zip(values,exponents):
            v *= x**e
        ans += v
    return ans


def volterra(word: tuple[int,...], L: int) -> list[F]:
    a = [F(1)]+[F(0)]*(L-1)
    for i in reversed(word):
        kernel = [F((-1)**j, i**(j+1)) for j in range(L)]
        integrand = mul(a,kernel,L)
        a = [F(0)]+[integrand[k-1]/k for k in range(1,L)]
    return a


def run() -> dict:
    results: dict = {'arithmetic':'exact integers and fractions',
                     'scope':'finite checks only; proofs are in RESEARCH_STATE.md',
                     'python_version':sys.version.split()[0]}
    # Hankel diagonal certificates for symmetrization and sorted lifts.
    certificates=[]
    for n in range(1,9):
        full = (1<<n)-1
        checked=0
        for S in range(1<<n):
            for T in range(1<<n):
                complement = full ^ T
                actual = ((S & complement)==0 and (S | complement)==full)
                assert actual == (S==T)
                checked += 1
        certificates.append({'n':n,'diagonal_minor_size':1<<n,'entries_checked':checked})
    results['subset_hankel_certificates'] = certificates
    # Full injective-word coefficient flattenings; omitted noninjective rows are zero.
    cuts=[]
    for n in range(1,7):
        alphabet=tuple(range(n))
        for k in range(n+1):
            rows=list(permutations(alphabet,k))
            cols=list(permutations(alphabet,n-k))
            M=[[int(len(set(u+v))==n) for v in cols] for u in rows]
            r=rank(M)
            assert r == comb(n,k)
            # Every nonzero block is a k! by (n-k)! all-ones block.
            # This independently confirms the squared singular values via M M^T.
            block_product = factorial(k)*factorial(n-k)
            if n <= 4:
                gram=[[sum(M[i][j]*M[h][j] for j in range(len(cols)))
                       for h in range(len(rows))] for i in range(len(rows))]
                for i in range(len(rows)):
                    for h in range(len(rows)):
                        square=sum(gram[i][j]*gram[j][h] for j in range(len(rows)))
                        assert square == block_product*gram[i][h]
            cuts.append({'n':n,'k':k,'rank':r,
                         'normalized_nonzero_singular_value_squared':
                         str(F(block_product,factorial(n)**2))})
    results['coefficient_cut_ranks'] = cuts
    # Translation orbit of products: boolean shifts, with period scaled to 1.
    translations=[]
    for n in range(1,7):
        masks=range(1<<n)
        full=(1<<n)-1
        M=[[int(((full ^ e) & ~shift)==0) for e in masks] for shift in masks]
        r=rank(M)
        assert r==1<<n
        translations.append({'n':n,'translation_span_rank':r})
    # Powers with repeated exponents: independent finite-difference grid.
    for ds in [(2,), (2,2), (2,3), (1,2,1)]:
        exps=list(product(*(range(d+1) for d in ds)))
        M=[]
        for shift in exps:
            row=[]
            for e in exps:
                c=1
                for d,a,b in zip(ds,shift,e):
                    c*=comb(d,b)*a**(d-b)
                row.append(c)
            M.append(row)
        r=rank(M)
        assert r==len(exps)
        translations.append({'exponents':list(ds),'translation_span_rank':r})
    results['monodromy_polynomial_models']=translations
    # Shuffle identity and explicit commutator signal.
    shuffle=[]
    for n in range(1,6):
        L=2*n+4
        target=jet({(1,)*n:F(1)},logs(n,L),L)
        lhs=[F(0)]*L
        for word in permutations(range(1,n+1)):
            lhs=[x+y for x,y in zip(lhs,volterra(word,L))]
        assert lhs==target
        shuffle.append({'n':n,'checked_coefficients':L})
    comm=[a-b for a,b in zip(volterra((1,2),7),volterra((2,1),7))]
    assert ord0(comm)==3 and comm[3]==F(-1,24)
    results['shuffle_checks']=shuffle
    results['commutator']={'order':3,'leading_coefficient':str(comm[3])}
    # Contact examples were discovered with SymPy, replayed here without SymPy.
    examples=json.loads((Path(__file__).with_name('contact_examples.json')).read_text())
    contacts=[]
    for case in examples:
        n=case['n']
        p={tuple(t['exponents']):F(t['coefficient']) for t in case['terms']}
        L=(1<<n)+4
        j=jet(p,logs(n,L),L)
        order=ord0(j)
        assert order == case['order'] == (1<<n)-1
        contacts.append({'n':n,'order':order,'leading_coefficient':str(j[order]),
                         'derivative_dimension':derivative_dimension(p),
                         'verified_coefficients':L})
    results['high_contact_examples']=contacts
    # Degree/rank boundaries and nonmonomial polynomial fixtures.
    fixtures=[]
    for n in range(1,5):
        fixtures.append((f'squarefree_product_{n}', {(1,)*n:F(1)}))
    for d in range(0,8):
        fixtures.append((f'univariate_power_{d}', {(d,):F(1)}))
    fixtures += [
      ('quadratic_sum', {(2,0):F(1),(0,2):F(1)}),
      ('square_linear_form', {(2,0):F(1),(1,1):F(2),(0,2):F(1)}),
      ('inhomogeneous', {(2,1):F(2),(1,2):F(-3),(0,0):F(7)}),
      ('linear_cancellation', {(1,0):F(1),(0,1):F(-2)}),
      ('cubic_difference', {(3,0):F(1),(0,3):F(-8)}),
      ('bilinear_sum', {(1,1,0):F(1),(1,0,1):F(1),(0,1,1):F(1)}),
    ]
    hitting=[]
    for name,p in fixtures:
        n=len(next(iter(p)))
        D=max(sum(e) for e in p)
        r=derivative_dimension(p)
        assert D+1<=r
        L=(n-1)*comb(r,2)+r
        js=logs(n,L)
        j=jet(p,js,L)
        order=ord0(j)
        assert order is not None and order<L
        bound=D*(L-1)
        witness=None
        for t in range(bound+1):
            values=[sum(c*F(t)**k for k,c in enumerate(a)) for a in js]
            value=eval_poly(p,values)
            if value:
                witness={'t':t,'value':str(value)}
                break
        assert witness is not None
        hitting.append({'name':name,'n':n,'degree':D,'derivative_dimension':r,
                        'jet_length':L,'order':order,'hitting_set_size_bound':bound+1,
                        'witness':witness})
    results['logarithmic_generator_fixtures']=hitting
    results['result']='ALL CHECKS PASSED'
    results['no_formal_prover_run']=True
    return results


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('verification_results.json'))
    args=parser.parse_args()
    results=run()
    args.output.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(results['result'])
    print('Hankel certificates:',len(results['subset_hankel_certificates']))
    print('Coefficient cut matrices:',len(results['coefficient_cut_ranks']))
    print('Translation models:',len(results['monodromy_polynomial_models']))
    print('Shuffle identities:',len(results['shuffle_checks']))
    print('Contact examples:',len(results['high_contact_examples']))
    print('Generator fixtures:',len(results['logarithmic_generator_fixtures']))
    print('Results:',args.output.resolve())

if __name__=='__main__':
    main()
