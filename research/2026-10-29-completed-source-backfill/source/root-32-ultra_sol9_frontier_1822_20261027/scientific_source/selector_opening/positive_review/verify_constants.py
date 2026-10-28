#!/usr/bin/env python3
"""Independent literal coefficient reconstruction for the positive review."""
from pathlib import Path
import json
import time
import sympy as s

start=time.perf_counter()
a,b,c,d=s.symbols('a b c d',real=True)
A=(a,b,c,d)
u,v,w,q=a*a+c*c,b*b+d*d,a*b+c*d,a*d-b*c
x,y,z=u-v,2*w,2*q
F=(s.Rational(55220381,10000000000)*(u*u+v*v)
   +s.Rational(114430029,625000000)*u*v
   -s.Rational(801761987,5000000000)*w*w
   +s.Rational(118849817,4000000000)*q*(u-v))
p=(s.Rational(6222019,200000000)*x**3
   +s.Rational(1686519911,10000000000)*x*x*z
   +s.Rational(81172813,2000000000)*x*z*z
   +s.Rational(1726116771,10000000000)*z**3
   +s.Rational(128626163,5000000000)*x*y*y
   +s.Rational(373321239,2000000000)*y*y*z)
C=sum(abs(coef) for coef in s.Poly(F,*A).coeffs())
P=sum(abs(coef) for coef in s.Poly(p,*A).coeffs())
U,V=12*C+11*P,10*P
delta=s.Rational(1,2400000)
M1=(U*U+V*V)/delta
assert C==s.Rational(2535570311,2500000000)
assert P==s.Rational(1976430361,156250000)
assert U==s.Rational(94569646817,625000000)
assert V==s.Rational(1976430361,15625000)
assert M1==s.Rational(45580383762312788235267,488281250000)
norm2=sum(aa*aa for aa in A)
k=p/norm2**2
for aa in A:
    expected=s.diff(p,aa)/norm2**2-4*p*aa/norm2**3
    assert s.cancel(s.diff(k,aa)-expected)==0
cof=s.Matrix([d,-c,-b,a])
J=cof.jacobian(A)
assert J.T*J==s.eye(4)
assert s.expand(sum(cof[i]*A[i] for i in range(4))-2*q)==0
data={'status':'INDEPENDENT_EXACT_CONSTANTS_PASS','C':str(C),'P':str(P),
      'U':str(U),'V':str(V),'delta':str(delta),'M1':str(M1),
      'rational_selector_derivative_identity':'PASS',
      'cofactor_isometry_identity':'PASS',
      'runtime_seconds':time.perf_counter()-start}
Path(__file__).with_name('REPLAY.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
