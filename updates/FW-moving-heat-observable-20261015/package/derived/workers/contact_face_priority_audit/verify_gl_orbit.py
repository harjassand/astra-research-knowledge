#!/usr/bin/env python3
"""Exact algebraic checks supporting GL_ORBIT_ADDENDUM.txt; SymPy only."""
from pathlib import Path
import hashlib
import json
import sympy as sp

here = Path(__file__).resolve().parent
a,b,c,d,r,t = sp.symbols('a b c d r t', real=True)
A = sp.Matrix([[a,b],[c,d]])
checks = []

def equal(name, lhs, rhs):
    residual = sp.factor(sp.cancel(lhs-rhs))
    assert residual == 0, (name, residual)
    checks.append(name)

def invariants(B):
    return B[0,0]**2+B[1,0]**2, B[0,1]**2+B[1,1]**2, B.det()

alpha = 3*r/(8*(r+2))
beta = r*(r-1)/6
br = (2*r+1)/3
Ar = sp.Matrix([[0,br],[1,0]])

def J(B):
    u,v,j = invariants(B)
    return alpha*(u+v-2*j)**2+beta*u**2+j**2+r*u*j

u,v,j = invariants(A)
equal('alpha plus beta positive-coefficient identity', alpha+beta,
      r*(2*r+1)**2/(24*(r+2)))
equal('right contact symmetry u', invariants(A*Ar)[0], v)
equal('right contact symmetry v', invariants(A*Ar)[1], br**2*u)
equal('right contact symmetry j', invariants(A*Ar)[2], -br*j)
equal('exact discrete right symmetry', J(A*Ar), br**2*J(A))
equal('beta to alpha relation', beta/alpha, br**2-1)

for epsilon in [1,-1]:
    S = sp.diag(1,epsilon)
    equal(f'conjugation invariance epsilon {epsilon}', J(S*A*S), J(A))
    equal(f'conjugation plus right symmetry epsilon {epsilon}',
          J(S*A*S*Ar), br**2*J(A))
    for k,D in [('first',S),('second',S*Ar)]:
        B = S*D
        direction = sp.Matrix([[D[1,0],D[1,1]],[0,0]])
        equal(f'{k} transformed contact epsilon {epsilon}',
              sp.diff(J(B+t*direction),t,2).subs(t,0),0)

x1,x2,n1,n2 = sp.symbols('x1 x2 n1 n2', real=True)
rankone = sp.Matrix([x1,x2])*sp.Matrix([[n1,n2]])
equal('rank-one restriction', J(rankone), (x1*x1+x2*x2)**2*
      (alpha*(n1*n1+n2*n2)**2+beta*n1**4))
quarterturn = sp.Matrix([[0,-1],[1,0]])
J1 = sp.factor(J(A).subs(r,1))
equal('r one anisotropic expansion', J1,
      (u+v)**2/8+(u-v)*j/2+3*j*j/2)
equal('r one quarter-turn difference',
      sp.factor((J(A*quarterturn)-J(A)).subs(r,1)), -(u-v)*j)
assert sp.factor((u-v)*j) != 0
checks.append('quarter-turn obstruction is a nonzero polynomial')

receipt = {
    'status':'EXACT_PASS', 'check_count':len(checks), 'checks':checks,
    'proof_sha256':hashlib.sha256((here/'GL_ORBIT_ADDENDUM.txt').read_bytes()).hexdigest(),
    'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope':'Exact identities; analytic orbit proof uses the frozen acoustic zero classification.',
}
(here/'GL_ORBIT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
