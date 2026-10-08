"""Independent stdlib-only exact certificate checker using Fraction polynomials."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import json
ZERO={}
def const(c): return {} if c==0 else {(0,0,0):F(c)}
def linear(a,b,c):return {e:F(k) for e,k in [((1,0,0),a),((0,1,0),b),((0,0,1),c)] if k}
def add(*ps):
    out={}
    for p in ps:
        for e,c in p.items():out[e]=out.get(e,F(0))+c
    return {e:c for e,c in out.items() if c}
def scale(p,k):return {e:c*F(k) for e,c in p.items() if c*F(k)}
def mul(a,b):
    out={}
    for e,c in a.items():
        for f,d in b.items():
            g=tuple(x+y for x,y in zip(e,f));out[g]=out.get(g,F(0))+c*d
    return {e:c for e,c in out.items() if c}
def det(M):
    n=len(M);out={}
    for p in permutations(range(n)):
        sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=const(sign)
        for i,j in enumerate(p):term=mul(term,M[i][j])
        out=add(out,term)
    return out

params={'A':[(1,2,2),(0,1,1),(0,0,1)],'B1':[(1,2,2),(1,1,1),(0,0,1)],'B2':[(1,3,2),(1,3,1),(0,2,1)],'C':[(1,3,2),(1,3,1),(1,2,1)]}
certificate=json.loads(Path(__file__).with_name('FULL_WEIGHTS_EXACT_COEFFICIENTS.json').read_text())
cert={(r['cone'],r['block'],r['leading_size']):{tuple(e):F(c) for e,c in r['terms']} for r in certificate['certificate']}
checked=0
for cone,triples in params.items():
    H=[linear(*r) for r in triples]
    if cone=='A':Z=[ZERO,H[0],H[0]]
    elif cone in ['B1','B2']:
        Z=[scale(add(scale(H[1],2),scale(H[0],-1)),F(2,3)),scale(add(scale(H[0],2),scale(H[1],-1)),F(2,3)),scale(add(H[0],H[1]),F(2,3))]
    else:Z=[add(*H,scale(H[i],-2)) for i in range(3)]
    W=[mul(p,p) for p in H];Q=[add(*W,scale(W[i],-1),mul(Z[i],Z[i])) for i in range(3)]
    blocks=[]
    for i in range(3):
        j,k=[x for x in range(3) if x!=i]
        qi,qj,qk=Q[i],Q[j],Q[k];wi,wj,wk=W[i],W[j],W[k]
        # Congruence diag(1,1,sqrt2,1,sqrt2) makes the 5x5 block rational.
        sym=[[qi,ZERO,scale(wk,-2),ZERO,scale(wj,-2)],
             [ZERO,scale(add(scale(qi,3),scale(qj,2)),F(1,5)),scale(wk,2),ZERO,ZERO],
             [scale(wk,-2),scale(wk,2),scale(add(qi,scale(qj,4)),F(2,5)),ZERO,scale(wi,-2)],
             [ZERO,ZERO,ZERO,scale(add(scale(qi,3),scale(qk,2)),F(1,5)),scale(wj,2)],
             [scale(wj,-2),ZERO,scale(wi,-2),scale(wj,2),scale(add(qi,scale(qk,4)),F(2,5))]]
        anti=[[scale(add(qi,scale(qj,4)),F(1,5)),scale(wi,-1)],[scale(wi,-1),scale(add(qi,scale(qk,4)),F(1,5))]]
        blocks.extend([(f'odd_color{i+1}_sym',sym,True),(f'odd_color{i+1}_anti',anti,False)])
    for sign,label in [(1,'sym'),(-1,'anti')]:
        M=[[ZERO for _ in range(3)] for _ in range(3)]
        for i in range(3):M[i][i]=scale(add(scale(Q[i],3),Q[(i+1)%3],Q[(i+2)%3]),F(1,5))
        for i in range(3):
            for j in range(i+1,3):M[i][j]=M[j][i]=scale(W[3-i-j],sign)
        blocks.append((f'color123_{label}',M,False))
    for name,M,rescaled in blocks:
        for n in range(1,len(M)+1):
            P=det([row[:n] for row in M[:n]])
            factor=[1,1,2,2,4][n-1] if rescaled else 1
            expected=scale(cert[(cone,name,n)],factor)
            assert P==expected,(cone,name,n,'determinant identity mismatch')
            assert P and all(c>=0 for c in P.values()) and any(c>0 for c in P.values())
            assert all(sum(e)==2*n for e in P),(cone,name,n,'wrong homogeneity')
            checked+=1
    print('PASS',cone,'all27 determinant identities, nonnegative/nonzero exact Fraction coefficients.')
assert checked==108
print('PASS all108 identities by independent standard-library rational polynomial arithmetic.')
