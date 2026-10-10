from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

def mul(u,v):
    z,x,y=u;w,X,Y=v
    t=max(z*X-w*y,F(0))
    return (t,x*t/z,Y*t/w) if t else (F(0),)*3

S=sorted(set((z,z*a,z*b) for z,a,b in product([F(0),F(1,4),F(1,2),F(1)],repeat=3) if a<=b))
assert all(mul(u,u)==(F(0),)*3 for u in S)
n=0
for u,v,w in product(S,repeat=3):
    assert mul(mul(u,v),w)==mul(u,mul(v,w));n+=1
prefixes=[]
p=None
for i in range(1,41):
    a=1-F(1,2**i);v=(F(1),a,a);p=v if p is None else mul(p,v)
    assert p[0]>0
    prefixes.append({'length':i,'amplitude':str(p[0])})
out={'status':'PASS','exact_rational_points':len(S),'associativity_triples':n,'square_zero_checks':len(S),'nonzero_prefixes':prefixes,'scope':'Finite rational checks support the explicit analytical proof, not a quantum-channel realization.'}
Path(__file__).with_name('nil_semigroup_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='nonzero_prefixes'}))
