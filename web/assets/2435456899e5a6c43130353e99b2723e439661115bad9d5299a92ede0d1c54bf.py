"""Exact finite checks of the exposed finite-field baseline, not a proof verifier."""
from itertools import combinations, product
from fractions import Fraction as F
from math import comb, factorial, log2
from pathlib import Path
from collections import defaultdict
import hashlib
import json

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
ORIGIN = ROOT/'work/agents/complexity_proof_recon/cycle04_memory_blind/INDEPENDENT_BASELINE.txt'
EXPECTED = '342987893f1a0101d905afa6f35b0a3de067cfae431a208495dd034f6780ff55'


def dot(x, y):
    return (x & y).bit_count() & 1


def binary_rank(vectors):
    pivots = {}
    for v in vectors:
        while v:
            p = v.bit_length()-1
            if p in pivots:
                v ^= pivots[p]
            else:
                pivots[p] = v
                break
    return len(pivots)


def subspaces(m, r):
    for piv in combinations(range(m), r):
        slots = [(i,j) for i,p in enumerate(piv) for j in range(p+1,m) if j not in piv]
        for bits in product((0,1), repeat=len(slots)):
            basis = [1 << p for p in piv]
            for bit, (i,j) in zip(bits,slots):
                if bit:
                    basis[i] |= 1 << j
            space = {0}
            for v in basis:
                space |= {x ^ v for x in tuple(space)}
            assert len(space) == 2**r
            yield basis, space-{0}


def h2(p):
    p = float(p)
    return 0.0 if p in (0,1) else -p*log2(p)-(1-p)*log2(1-p)


def entropy(p):
    return -sum(float(v)*log2(float(v)) for v in p.values() if v)


def mix_uniform(support, whole, noise):
    return {x:(1-noise)*(F(1,len(support)) if x in support else 0)+noise*F(1,len(whole))
            for x in whole}


def check(m):
    v = range(1, 2**m)
    n, d, c = 2**m-1, 2**(m-1)-1, 2**(m-2)-1
    orth = {x:{y for y in v if dot(x,y)==0} for x in v}
    assert all(len(s)==d for s in orth.values())
    assert all((x in orth[y])==(y in orth[x]) for x in v for y in v)
    assert any(x in orth[x] for x in v)
    for x in v:
        for y in v:
            assert len(orth[x] & orth[y]) == (d if x == y else c)
    gamma = F(2**(m-2),d*d)
    assert gamma == F(n+1,(n-1)**2) <= F(2,9)
    assert F(c,d*d) == (1-gamma)/n
    # Uniform subspace witness, including all self-orthogonal diagonal pairs.
    r = m//2
    b_m = (2**r-1)*(2**(m-r)-1)
    counts = defaultdict(int)
    total_spaces = 0
    first_basis = None
    for basis, space in subspaces(m,r):
        first_basis = first_basis or basis
        perp = {y for y in v if all(dot(u,y)==0 for u in basis)}
        assert len(space)*len(perp)==b_m
        for x,y in product(space,perp):
            counts[(x,y)] += 1
        total_spaces += 1
    target_pairs = {(x,y) for x in v for y in orth[x]}
    assert counts.keys() == target_pairs
    assert len(set(counts.values())) == 1
    incidence = next(iter(counts.values()))
    assert total_spaces*b_m == n*d*incidence
    # Every support-size split is bounded by the balanced split.
    for rr in range(1,m):
        assert (2**rr-1)*(2**(m-rr)-1) <= b_m
    assert n*d >= 2**(2*m-2)
    # Exercise robust component inequality for low and high forbidden mass.
    support_x = {0}
    for z in first_basis:
        support_x |= {x^z for x in tuple(support_x)}
    support_x -= {0}
    support_y = {y for y in v if all(dot(x,y)==0 for x in first_basis)}
    eta = F(1,20)
    tests = 0
    for nx,ny in product((F(0),F(1,100),F(1,25),F(1,5),F(1)), repeat=2):
        a = mix_uniform(support_x,v,nx)
        b = mix_uniform(support_y,v,ny)
        parity_error = {y:sum(a[x] for x in v if dot(x,y)) for y in v}
        e = sum(b[y]*parity_error[y] for y in v)
        g = {y for y in v if parity_error[y] <= eta}
        tau = sum(b[y] for y in v if y not in g)
        rr = binary_rank(g)
        assert tau <= e/eta
        assert entropy(a) <= m-rr+rr*h2(eta)+1e-10
        assert entropy(b) <= rr+float(tau)*m+h2(tau)+1e-10
        rhs = (1+h2(eta)+(1-h2(eta))*float(tau))*m+(1-h2(eta))*h2(tau)
        assert entropy(a)+entropy(b) <= rhs+1e-10
        tests += 1
    return {'m':m,'N':n,'d':d,'B_m':b_m,'subspaces':total_spaces,
            'incidence_per_orthogonal_pair':incidence,'exact_capacity':f'ln({n}/{d})',
            'exact_Wyner':f'ln({n*d}/{b_m})','component_tests':tests,
            'diagonal_pairs_included':True,'A_squared_identity':True,
            'two_step_TV_contraction':str(gamma)}


def main():
    assert hashlib.sha256(ORIGIN.read_bytes()).hexdigest() == EXPECTED
    assert sum(F(3**k,factorial(k)) for k in range(9)) > 20
    assert sum(F(5**k,factorial(k)) for k in range(7)) > 100
    assert h2(F(1,20)) < .3 and h2(F(1,100)) < .1
    alpha = 1-.02-h2(.05)-(1-h2(.05))*.2
    additive = 2+h2(.01)+(1-h2(.05))*h2(.2)
    assert alpha > .54 and additive < 3.1
    output = {'status':'EXPOSED_FINITE_DIAGNOSTICS_PASS','origin_sha256':EXPECTED,
              'scope':'Exact incidence counts and scalar normalization; floating entropy spot checks; not a general or formal verifier.',
              'alpha_at_delta_point01':alpha,'additive_at_delta_point01':additive,
              'examples':[check(m) for m in range(3,7)]}
    (BASE/'orthogonality_diagnostics.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'m':[3,4,5,6],
                      'alpha':alpha,'additive':additive,'general_quantifiers_verified':False}))


if __name__ == '__main__':
    main()
