"""Exact ideal blow-up of the isolated acoustic zero in a polynomial matrix.

Builds an identity C = Q^(-T) D^T M D Q^(-1). Positivity is NOT assumed.
"""
from pathlib import Path
import json,time,os
import sympy as S
import numpy as np
p=Path(os.environ.get('ASTRA_ANGULAR_CASE',Path(__file__).parent))
b,d=S.symbols('b d',real=True)
loc={'b':b,'d':d}
C=S.Matrix([[S.sympify(x,locals=loc) for x in row] for row in json.loads((p/'boundary_matrix.json').read_text())])
cfg=json.loads((p/'case_config.json').read_text()) if (p/'case_config.json').exists() else {'k':'4/11','z2':'65/81'}
k0,z2=S.Rational(cfg['k']),S.Rational(cfg['z2'])
w=b*b+d*d+2*k0*d-1
g=S.Poly(d*d-z2*(1-k0*d)**2,d).clear_denoms()[1].primitive()[1].as_expr()

def divw(f):
    return [S.expand(x) for x in S.div(f,w,b)]

def red(f):
    rr=divw(S.expand(f))[1]
    return S.expand(sum(S.rem(co,g,d)*b**power[0] for power,co in S.Poly(rr,b).terms()))

def inv(f):
    basis=[1,b,d,b*d]
    mat=S.Matrix.hstack(*[S.Matrix([S.Poly(red(f*x),b,d).coeff_monomial(y) for y in basis]) for x in basis])
    sol=mat.inv()[:,0]
    return S.expand(sum(x*y for x,y in zip(sol,basis)))

start=time.perf_counter()
Cr=C.applyfunc(red)
# Solve the lower five equations with first kernel entry normalized to one.
aug=[[Cr[i,j] for j in range(1,6)]+[-Cr[i,0]] for i in range(1,6)]
for k in range(5):
    row=next(i for i in range(k,5) if aug[i][k]!=0)
    aug[k],aug[row]=aug[row],aug[k]
    ii=inv(aug[k][k]); aug[k]=[red(x*ii) for x in aug[k]]
    for i in range(5):
        if i==k: continue
        mul=aug[i][k]
        aug[i]=[red(x-mul*y) for x,y in zip(aug[i],aug[k])]
kernel=S.Matrix([1]+[aug[i][-1] for i in range(5)])
assert all(red(x)==0 for x in Cr*kernel)
print('exact quotient kernel',list(map(str,kernel)),flush=True)
Q=S.eye(6); Q[:,0]=kernel
Cp=(Q.T*C*Q).applyfunc(S.expand)
q1,rem0=divw(Cp[0,0]); q2,rem1=divw(q1)
cc=S.cancel(rem0/g**2); bb=S.cancel(rem1/g)
assert S.denom(cc)==1 and S.denom(bb)==1
M=S.zeros(7)
M[0,0]=q2; M[0,1]=M[1,0]=bb/2; M[1,1]=cc
for j in range(1,6):
    pp,rr=divw(Cp[0,j]); qq=S.cancel(rr/g)
    assert S.denom(qq)==1
    M[0,j+1]=M[j+1,0]=pp
    M[1,j+1]=M[j+1,1]=qq
for i in range(1,6):
    for j in range(1,6): M[i+1,j+1]=Cp[i,j]
D=S.zeros(7,6); D[0,0]=w;D[1,0]=g
for i in range(1,6):D[i+1,i]=1
assert all(S.expand(x)==0 for x in D.T*M*D-Cp)
out={'w':str(w),'g':str(g),'kernel':list(map(str,kernel)),
     'M':[[str(S.expand(x)) for x in row] for row in M.tolist()],
     'identity':'Q^T C Q = D^T M D; Q first column is kernel, other columns e1,...,e5; D00=w,D10=g,D_(j+1,j)=1',
     'seconds':time.perf_counter()-start}
(p/'acoustic_blowup.json').write_text(json.dumps(out))
dp=next(x for x in S.solve(g,d) if 0<float(x)<1)
bp=S.sqrt(1-dp*dp-2*k0*dp)
ff=S.lambdify((b,d),M,'numpy',cse=True)
print('zero',float(bp),float(dp),'lifted eigenvalues',np.linalg.eigvalsh(np.array(ff(float(bp),float(dp)),float)),flush=True)
print('seconds',time.perf_counter()-start,flush=True)
