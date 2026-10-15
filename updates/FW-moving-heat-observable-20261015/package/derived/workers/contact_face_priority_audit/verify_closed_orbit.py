#!/usr/bin/env python3
"""Exact algebra supporting CLOSED_ORBIT_ADDENDUM.txt; no numerical tests."""
from pathlib import Path
import hashlib
import json
import sympy as sp

here = Path(__file__).resolve().parent
p1,p2,p3,p4,b1,b2,b3,b4 = sp.symbols('p1 p2 p3 p4 b1 b2 b3 b4',real=True)
co,si = sp.symbols('co si',real=True)
P=sp.Matrix([[p1,p2],[p3,p4]])
B=sp.Matrix([[b1,b2],[b3,b4]])
R=sp.Matrix([[co,-si],[si,co]])
checks=[]

def equal(name,lhs,rhs):
    residual=sp.factor(sp.expand(lhs-rhs))
    assert residual==0,(name,residual)
    checks.append(name)

def norm2(X):
    return sp.trace(X.T*X)

def average(poly):
    answer=0
    for (i,j),v in sp.Poly(sp.expand(poly),co,si).terms():
        if i%2 or j%2:
            moment=0
        else:
            moment=sp.rf(sp.Rational(1,2),i//2)*sp.rf(sp.Rational(1,2),j//2)/sp.factorial((i+j)//2)
        answer+=v*moment
    return sp.expand(answer)

tp=norm2(P)
dp=P.det()
kp=(3*tp**2-4*dp**2)/8
equal('second rotation moment',average(norm2(P*R*B)),tp*norm2(B)/2)
equal('fourth rotation moment',average(norm2(P*R*B)**2),
      kp*norm2(B)**2-(tp**2-4*dp**2)*B.det()**2/2)

a0,b0,c0,x,y,h = sp.symbols('a0 b0 c0 x y h',real=True)
def Q(X):
    return a0*norm2(X)**2+b0*norm2(X)*X.det()+c0*X.det()**2
equal('source coefficient acoustic bound',
      sp.diff(Q(sp.Matrix([[x,h],[0,y]])),h,2).subs(h,0),
      4*a0*(x*x+y*y)+2*b0*x*y)

tt,dd = sp.symbols('tt dd',real=True)
kk=(3*tt*tt-4*dd*dd)/8
equal('uniform average mixed coefficient bound identity',
      2*kk-dd*tt,(tt-2*dd)*(3*tt+2*dd)/4)

z,w = sp.symbols('z w',real=True)
T=sp.Matrix([[z,w],[w,1-z]])
equal('trace one determinant upper bound',sp.Rational(1,4)-T.det(),(z-sp.Rational(1,2))**2+w*w)
equal('trace one diagonal square lower bound',z*z+(1-z)**2-sp.Rational(1,2),2*(z-sp.Rational(1,2))**2)

E,F,G=sp.symbols('E F G',real=True)
A=sp.Matrix([[b1,b2],[b3,b4]])
qt=sp.trace(A.T*A*T)
f=E*qt**2+F*qt*A.det()+G*A.det()**2
equal('rank one trace bound sample',f.subs({b1:1,b2:0,b3:0,b4:0})+
      f.subs({b1:0,b2:1,b3:0,b4:0}),E*(z*z+(1-z)**2))
equal('identity controls last coefficient',f.subs({b1:1,b2:0,b3:0,b4:1}),E+F+G)
equal('radial trace one limit',f.subs({z:sp.Rational(1,2),w:0}),
      E*norm2(A)**2/4+F*norm2(A)*A.det()/2+G*A.det()**2)

r=sp.symbols('r',real=True)
alpha=3*r/(8*(r+2));beta=r*(r-1)/6
equal('sharp rank one positive first coefficient',alpha+beta,r*(2*r+1)**2/(24*(r+2)))
J=alpha*(norm2(A)-2*A.det())**2+beta*(b1*b1+b3*b3)**2+A.det()**2+r*(b1*b1+b3*b3)*A.det()
turn=sp.Matrix([[0,-1],[1,0]])
def JJ(X):
    return J.subs(dict(zip([b1,b2,b3,b4],list(X))),simultaneous=True)
equal('sharp quarter-turn obstruction',JJ(A*turn)-J,
      ((b2*b2+b4*b4)-(b1*b1+b3*b3))*(beta*norm2(A)+r*A.det()))

receipt={
    'status':'EXACT_PASS','check_count':len(checks),'checks':checks,
    'proof_sha256':hashlib.sha256((here/'CLOSED_ORBIT_ADDENDUM.txt').read_bytes()).hexdigest(),
    'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope':'Exact average and coefficient identities; compactness and extremality arguments are readable in the proof.',
}
(here/'CLOSED_ORBIT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
