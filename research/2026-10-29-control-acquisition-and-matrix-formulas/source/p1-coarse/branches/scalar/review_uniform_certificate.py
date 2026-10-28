"""Independent exact replay of published uniform certificate inequalities.

Reads decoded scalar intervals, not source matrices. Does not import the root
compiler, its PSD test, or its moment expression builder. PSD is checked by
all principal minors (small published 3x3 matrices only). This is deliberately
a verifier of the reported finite witnesses, not a new acquisition algorithm.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations, permutations
import json, hashlib
ROOT=Path(__file__).resolve().parents[2]

def decode(x):
    if isinstance(x,dict) and 'rational' in x:return F(x['rational'])
    if isinstance(x,dict):return {k:decode(v) for k,v in x.items()}
    if isinstance(x,list):return [decode(v) for v in x]
    return x

def dot(x,y):return sum((a*b for a,b in zip(x,y)),F(0))
def tr(A):return list(map(list,zip(*A)))
def mm(A,B):return [[dot(r,c) for c in zip(*B)] for r in A]
def sub(A,B):return [[a-b for a,b in zip(x,y)] for x,y in zip(A,B)]
def scale(s,A):return [[s*a for a in r] for r in A]
def diag(x):return [[a if i==j else F(0) for j in range(len(x))] for i,a in enumerate(x)]
def determinant(A):
    n=len(A);out=F(0)
    for p in permutations(range(n)):
        sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=F(sign)
        for i in range(n):term*=A[i][p[i]]
        out+=term
    return out

def all_principal_psd(A,strict=False):
    assert A==tr(A)
    for k in range(1,len(A)+1):
        for inds in combinations(range(len(A)),k):
            d=determinant([[A[i][j] for j in inds] for i in inds])
            assert d>0 if strict else d>=0, (inds,d)

def canon(w):
    w=tuple(w);return min(w,w[::-1])
def ew(left,middle,right):return canon(tuple(right)+tuple(middle)+tuple(left)[::-1])
def interval(expr,records):
    lo=hi=F(0)
    for w,c in expr.items():
        a,b=records[w]
        lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return (lo,hi)
def main():
    payload=decode(json.loads((ROOT/'results/ECHO_EXPERIMENT.json').read_text()))
    checks=[]
    for f in payload['fixtures']:
        dictionary=f['dictionary'];r=len(dictionary);T=f['maps']
        records={tuple(e['word']):(e['interval']['lo'],e['interval']['hi']) for e in f['decoded_records']}
        C=f['uniform_certificate'];W=C['metric'];rho=C['rho']
        all_principal_psd(W,strict=True)
        assert F(0)<=rho<1
        for L in T:all_principal_psd(sub(scale(rho*rho,W),mm(mm(tr(L),W),L)))
        for i,L in enumerate(T):
            intervals=[]
            for j in range(r):
                row=[]
                for k in range(r):
                    coeff={}
                    def term(a,mid,b,c):
                        w=ew(dictionary[a],mid,dictionary[b]);coeff[w]=coeff.get(w,F(0))+c
                    term(j,(i,i),k,F(1))
                    for l in range(r):
                        term(j,(i,),l,-L[l][k]);term(l,(i,),k,-L[l][j])
                        for m in range(r):term(l,(),m,L[l][j]*L[m][k])
                    row.append(interval(coeff,records))
                intervals.append(row)
            mid=[[(a+b)/2 for a,b in row] for row in intervals]
            rows=[sum(((b-a)/2 for a,b in row),F(0)) for row in intervals]
            upper=[[mid[j][k]+(rows[j] if j==k else 0) for k in range(r)] for j in range(r)]
            assert upper==C['residual_uppers'][i]
            all_principal_psd(sub(scale(C['per_action_eps2'][i],W),upper))
        for middle,gamma in [((),C['gamma_g'])]+[((i,),C['gamma_m']) for i in range(len(T))]:
            rows=[]
            for a in dictionary:
                rows.append(sum(((records[ew(a,middle,b)][1]-records[ew(a,middle,b)][0])/2 for b in dictionary),F(0)))
            all_principal_psd(sub(scale(gamma,W),diag(rows)))
        norm=W[0][0]
        eps=max(C['per_action_eps2'])
        rem=norm*eps/(1-rho)**2
        measure=norm*(C['gamma_g']+(C['gamma_m']+rho*C['gamma_g'])/(1-rho))
        assert C['eps2']==eps
        assert C['all_word_residual_bound']==rem
        assert C['all_word_measurement_bound']==measure
        assert C['all_word_total_bound']==rem+measure
        checks.append({'fixture':f['fixture'],'dimension':r,
                       'all_word_bound':str(rem+measure),'all_word_bound_float':float(rem+measure),
                       'matrix_inequalities_verified_by_all_principal_minors':True,
                       'residual_intervals_independently_reconstructed':True})
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [ROOT/'core/echo_compiler.py',ROOT/'core/uniform_certificate.py',ROOT/'results/ECHO_EXPERIMENT.json']}
    out={'scope':'Exact source-free replay from supplied decoded scalar intervals of four finite uniform-certificate witnesses. Calibration decoding and hidden physical contracts not audited here.',
         'hashes':hashes,'checks':checks}
    Path(__file__).with_name('UNIFORM_CERTIFICATE_REVIEW_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
