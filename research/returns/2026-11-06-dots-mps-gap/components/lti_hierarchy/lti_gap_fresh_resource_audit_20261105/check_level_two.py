"""Exact rational counterexample to allowing the nearest-neighbor level n=2."""
import itertools,json
import sympy as s
from functools import reduce
bp=s.Matrix([[0,1,0],[0,0,1],[0,0,0]])
z=s.diag(1,0,-1)
x=s.kronecker_product(bp,bp.T)+s.kronecker_product(bp.T,bp)+s.kronecker_product(z,z)
h=(x+2*s.eye(9))*(x+s.eye(9))/6
assert h*h==h and h!=s.zeros(9)
N=4
states=[a for a in itertools.product(range(3),repeat=N) if sum(a)==3]
index={a:i for i,a in enumerate(states)}
H=s.zeros(len(states))
for c,a in enumerate(states):
    for i in range(N):
        j=(i+1)%N
        old=3*a[i]+a[j]
        for r in range(9):
            v=h[r,old]
            if v:
                b=list(a);b[i]=r//3;b[j]=r%3
                H[index[tuple(b)],c]+=v
v=(H-s.eye(H.rows)/3).nullspace()[0]
v=v*s.ilcm(*[x.q for x in v])
assert H*v==v/3 and v!=s.zeros(v.rows,1)
result={'statement':'AKLT gamma_2=1, but Delta_4 <= 1/3. Explicit nonzero rational 1/3-energy eigenvector. Labels 0,1,2 mean spin z=+1,0,-1.', 'witness':{''.join(map(str,a)):str(v[i]) for i,a in enumerate(states) if v[i]},'squared_norm':str((v.T*v)[0]),'exact_eigenvalue':'1/3','exact_checks_passed':True}
with open('level_two_counterexample.json','w') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
