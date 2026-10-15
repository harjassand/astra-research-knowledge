#!/usr/bin/env python3
"""Exact real-parameter identities for SYMMETRY_NORMALIZATION.txt."""
from pathlib import Path
import hashlib
import json
import sympy as sp

here=Path(__file__).resolve().parent
a,b,c,d,h,t,r=sp.symbols('a b c d h t r',real=True)
A=sp.Matrix([[a,b],[c,d]])
Q=sp.Matrix([[0,-1],[1,0]])
checks=[]
def equal(name,lhs,rhs):
    if isinstance(lhs,sp.MatrixBase):
        residual=(lhs-rhs).applyfunc(lambda x:sp.factor(sp.cancel(x)))
        assert residual==sp.zeros(*lhs.shape),(name,residual)
    else:
        residual=sp.factor(sp.cancel(lhs-rhs))
        assert residual==0,(name,residual)
    checks.append(name)
def uvj(B):
    return B[0,0]**2+B[1,0]**2,B[0,1]**2+B[1,1]**2,B.det()
def J(B,rr):
    u,v,j=uvj(B)
    return 3*rr/(8*(rr+2))*(u+v-2*j)**2+rr*(rr-1)/6*u*u+j*j+rr*u*j
rr=-(3*h*h+1)/2
D=sp.diag(1/h,1)
T=sp.Matrix([[0,-h],[1/h,0]])
alpha=3*rr/(8*(rr+2))
u,v,j=uvj(A)
equal('conjugated quarter turn',D.inv()*Q*D,T)
equal('conjugated action order four',T*T,-sp.eye(2))
equal('conjugated action orientation',T.det(),1)
equal('sharp action invariance',J(A*T,rr),J(A,rr))
equal('standard C4 after right stretch',J(A*Q*D,rr),J(A*D,rr))
equal('explicit C4 normalized family',J(A*D,rr)/alpha,
      u*u+v*v+2*u*v/h**2-4*(u+v)*j/h+4*(5*h*h-1)/(h*h*(3*h*h+1))*j*j)
Wt=u*u+v*v+2*t*t*u*v-4*t*(u+v)*j+4*t*t*(5-t*t)/(3+t*t)*j*j
equal('unit interval C4 parameterization',(J(A*D,rr)/alpha).subs(h,1/t),Wt)
equal('unit interval sharp parameter',rr.subs(h,1/t),-(3+t*t)/(2*t*t))
equal('C4 convex endpoint t one',Wt.subs(t,1),(u+v-2*j)**2)
equal('C4 convex endpoint t zero',Wt.subs(t,0),u*u+v*v)
receipt={
    'status':'EXACT_PASS','check_count':len(checks),'checks':checks,
    'proof_sha256':hashlib.sha256((here/'SYMMETRY_NORMALIZATION.txt').read_bytes()).hexdigest(),
    'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope':'Algebraic symmetry normalization only; no QC or historical-priority claim.',
}
(here/'SYMMETRY_NORMALIZATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
