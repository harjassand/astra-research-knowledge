from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

def dot(x,y): return sum(a*b for a,b in zip(x,y))
def mv(A,x): return [dot(row,x) for row in A]
def mm(A,B): return [[dot(row,col) for col in zip(*B)] for row in A]

records=[]
for d in range(1,7):
    p=0
    while 2**(2*p)<2*d: p+=1
    v=[F(i) for i in range(1,d+1)]
    vn=dot(v,v)
    H=[[F(int(i==j))-2*v[i]*v[j]/vn for j in range(d)] for i in range(d)]
    for eigs in [[F(1)]+[F(1,2)]*(d-1), [F(1)]+[F(1,4)]*(d-1), [F(1)]+[F(0)]*(d-1)]:
        HD=[[H[i][j]*eigs[j] for j in range(d)] for i in range(d)]
        R=mm(HD,H)
        success=0
        for sign in product([-1,1],repeat=d):
            q=list(map(F,sign))
            for _ in range(p): q=mv(R,q)
            den=dot(q,q)
            rho=F(0) if den==0 else dot(q,mv(R,q))/den
            assert 0<=rho<=1
            success+=int(rho>=F(1,2))
        assert success*12>=2**d
        records.append(dict(d=d,p=p,eigenvalues=[str(x) for x in eigs],success=success,total=2**d))
with (Path(__file__).resolve().parents[1]/'results'/'rademacher_tester_checks.json').open('w') as f:
    json.dump({'status':'passed','arithmetic':'Python exact fractions','cases':records},f,indent=2)
print(json.dumps({'status':'passed','cases':len(records),'arithmetic':'exact rational'}))
