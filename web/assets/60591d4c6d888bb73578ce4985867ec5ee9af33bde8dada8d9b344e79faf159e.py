"""Verify the supplemental Nanson certificate and its universal identity.

Sparse integer polynomial arithmetic in all 12 off-diagonal matrix entries.
No source generator or symbolic algebra library is used.
"""
from itertools import permutations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
ZERO = (0,)*12

class Poly:
    def __init__(self, x):
        self.d = {ZERO:x} if isinstance(x,int) and x else ({} if isinstance(x,int) else {e:c for e,c in x.items() if c})
    def __add__(self, other):
        other = other if isinstance(other,Poly) else Poly(other)
        d = self.d.copy()
        for e,c in other.d.items():
            d[e] = d.get(e,0)+c
        return Poly(d)
    __radd__ = __add__
    def __mul__(self, other):
        other = other if isinstance(other,Poly) else Poly(other)
        d = {}
        for e,c in self.d.items():
            for f,b in other.d.items():
                k = tuple(x+y for x,y in zip(e,f))
                d[k] = d.get(k,0)+c*b
        return Poly(d)
    __rmul__ = __mul__

def nanson(r,t):
    a,b,c,d = t[1,2,3],t[1,2,4],t[1,3,4],t[2,3,4]
    return [[a*r[1,4], b*r[1,3], c*r[1,2], 2*d*r[1,2]*r[1,3]*r[1,4]+c*b*a],
            [b*r[2,3], a*r[2,4], d*r[1,2], 2*c*r[1,2]*r[2,3]*r[2,4]+d*b*a],
            [c*r[2,3], d*r[1,3], a*r[3,4], 2*b*r[1,3]*r[2,3]*r[3,4]+d*c*a],
            [d*r[1,4], c*r[2,4], b*r[3,4], 2*a*r[1,4]*r[2,4]*r[3,4]+d*c*b]]

def determinant(m):
    out = 0
    for perm in permutations(range(4)):
        sign = (-1)**sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
        term = sign
        for i,j in enumerate(perm):
            term *= m[i][j]
        out += term
    return out

pairs = [(i,j) for i in range(1,5) for j in range(1,5) if i != j]
entries = {ij:Poly({tuple(int(k==h) for h in range(12)):1}) for k,ij in enumerate(pairs)}
r = {(i,j):entries[i,j]*entries[j,i] for i in range(1,5) for j in range(i+1,5)}
t = {(i,j,k):entries[i,j]*entries[j,k]*entries[k,i]+entries[i,k]*entries[k,j]*entries[j,i]
     for i in range(1,5) for j in range(i+1,5) for k in range(j+1,5)}
identity = determinant(nanson(r,t))
assert identity.d == {}, identity.d

# Derive input from independently audited source coefficients.
audit = json.loads((ROOT/'independent_results.json').read_text())
rs = list(audit['pair_products_mod101'].values())
ts = list(audit['triple_cycle_sums_mod101'].values())
rn = dict(zip(r,rs))
tn = dict(zip(t,ts))
m = [[x % 101 for x in row] for row in nanson(rn,tn)]
d = determinant(m) % 101
source = json.loads((ROOT.parent/'contact/nanson_certificate_mod101.json').read_text())
assert m == source['matrix']
assert d == source['det'] == 5
result = {
    'status':'PASS',
    'identity_verification':'Exact expansion over Z in 12 independent off-diagonal matrix entries has zero coefficients',
    'identity_final_nonzero_monomial_count':len(identity.d),
    'fixture_matrix_mod101':m,
    'fixture_determinant_mod101':d,
    'source_formula':'https://arxiv.org/html/0812.0601v3#S3',
    'scope':'Universal necessary principal-minor identity only; no sufficiency or novelty claim'
}
(ROOT/'nanson_independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
