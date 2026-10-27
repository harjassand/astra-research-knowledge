"""Exact rational, count-only verification; no plant/scoring imports."""
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'counts.json').read_text())
tables={tuple(t['actions']):t for t in data['tables']}
w=F(*data['hoeffding_width_rational'])
def mat(a): return [[F(v) for v in row] for row in a]
def eye(): return mat([[1,0],[0,1]])
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def neg(a): return [[-x for x in row] for row in a]
def sub(a,b): return add(a,neg(b))
def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]
def ab(a): return [[abs(x) for x in row] for row in a]
def inv(a):
    det=a[0][0]*a[1][1]-a[0][1]*a[1][0]
    assert det
    return [[a[1][1]/det,-a[0][1]/det],[-a[1][0]/det,a[0][0]/det]]
def maxrowsum(a): return max(sum(abs(x) for x in row) for row in a)
def minimum(a): return min(x for row in a for x in row)
def probability(actions, requirements):
    t=tables[tuple(actions)]
    return F(sum(c for bits,c in t['counts'].items()
                 if all(int(bits[i])==o for i,o in requirements.items())),t['shots'])

H=mat([[1,1],[0,0]]); dH=mat([[0,0],[w,w]]); Hz={}; dHz={}
for j,prep in enumerate([(),(0,)]):
    H[1][j]=probability(prep+(1,),{len(prep):1})
for a,o in product(range(2),repeat=2):
    Hz[a,o]=mat([[0,0],[0,0]]); dHz[a,o]=mat([[w,w],[w,w]])
    for j,prep in enumerate([(),(0,)]):
        Hz[a,o][0][j]=probability(prep+(a,),{len(prep):o})
        Hz[a,o][1][j]=probability(prep+(a,1),{len(prep):o,len(prep)+1:1})

def verify(s):
    S=mat([[1+s,-s],[-s,1+s]])
    V=mul(H,S); dV=mul(dH,ab(S)); U=inv(V); A=mul(ab(U),dV)
    nu=maxrowsum(A)
    if nu>=1: return {'s':s,'status':'UNKNOWN_INVERSE'}
    M=mul(inv(sub(eye(),A)),ab(U)); assert minimum(M)>=0
    raw={z:mul(mul(U,v),S) for z,v in Hz.items()}
    errors={z:mul(M,add(mul(dHz[z],ab(S)),mul(dV,ab(raw[z])))) for z in raw}
    margin=min(minimum(sub(raw[z],errors[z])) for z in raw)
    initial=mul(inv(S),mat([[1],[0]]))
    if margin<0 or minimum(initial)<0:
        return {'s':s,'status':'UNKNOWN_POSITIVITY','margin':margin,'nu':nu}
    t=F(0)
    for a,j in product(range(2),repeat=2):
        p=[raw[a,o][i][j] for o in range(2) for i in range(2)]
        E=[errors[a,o][i][j] for o in range(2) for i in range(2)]
        assert sum(p)==1 and min(p)>=0
        low=[max(F(0),p0-e) for p0,e in zip(p,E)]
        high=[min(F(1),p0+e) for p0,e in zip(p,E)]
        assert sum(low)<=1<=sum(high)
        for mask in product([0,1],repeat=4):
            m=min(sum(u for u,k in zip(high,mask) if k),
                  1-sum(l for l,k in zip(low,mask) if not k))
            t=max(t,m-sum(v for v,k in zip(p,mask) if k))
    delta=F(2,5); gamma=1-delta
    return {'s':s,'status':'PASS','margin':margin,'nu':nu,'local_tv':t,
            'one_macro_tv':gamma*t/(delta+gamma*t),
            'two_macro_tv':1-(delta/(delta+gamma*t))**2,
            'initial':initial,'W':{str(z):v for z,v in raw.items()},
            'entry_errors':{str(z):v for z,v in errors.items()}}

def serialize(value):
    if isinstance(value,F): return {'rational':str(value),'decimal':float(value)}
    if isinstance(value,dict): return {str(k):serialize(v) for k,v in value.items()}
    if isinstance(value,list): return [serialize(v) for v in value]
    return value

def main():
    candidates=[verify(s) for s in [F(0),F(1,8),F(1,4),F(3,8),F(1,2),F(3,4),F(1)]]
    passing=[c for c in candidates if c['status']=='PASS']
    best=min(passing,key=lambda c:(c['local_tv'],-c['margin']))
    assert data['rank_upper_bound']==2 and H[1][1]-H[1][0]!=0
    n=min(t['shots'] for t in tables.values()); exponent=2*n*w*w
    out={'rank_upper_bound':2,'H_determinant':str(H[1][1]-H[1][0]),
         'hoeffding_failure_exact_expression':f"36 exp(-{exponent})",
         'hoeffding_failure_decimal':36*math.exp(-float(exponent)),
         'selected':best,'candidates':candidates}
    (ROOT/'rational_certificate.json').write_text(json.dumps(serialize(out),indent=2)+'\n')
    print(json.dumps(serialize({k:best[k] for k in ['s','status','margin','nu','local_tv','one_macro_tv','two_macro_tv']}),indent=2))
if __name__=='__main__': main()
