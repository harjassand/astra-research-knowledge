"""Symbolic universal coefficients for the active family and static metric."""
from pathlib import Path
import json,time
START=time.monotonic()
import sympy as s
OUT=Path(__file__).resolve().parent
a,b,c,g,d,t=s.symbols('a b c gamma d tau',real=True)
x=s.Matrix([-3,-1,1,3]);one=s.ones(4,1);u=s.Matrix([1,-1,-1,1]);v=s.Matrix([1,-3,3,-1])
K=g*(u*v.T-v*u.T)
A=c*s.ones(4)-(4*c+2*a)*s.eye(4)+K
B=A-(d-1)*s.diag(*[a+b*z for z in x])
f1=a*one+b*x;f2=a*one-b*x
P=s.eye(4)+t*A;R=s.eye(4)+t*B
delta=s.factor(t*t*( (f1.T*R*P*R*R*f2)[0]-(f2.T*R*R*P*R*f1)[0] )/6)
print('DIFFERENCE',delta,flush=True)
assert delta==-s.Rational(256,1)*g*b**5*(d-1)**3*t**6
H=s.Matrix.hstack(one,x,u,v)
T=s.simplify(H.inv()*B*H)
rho=s.factor(4*T[2,3]/T[3,2])
metric=s.diag(4,20,4,rho)
assert s.simplify(metric*T-T.T*metric)==s.zeros(4)
print('STATIC_METRIC',rho,flush=True)
result={'difference':str(delta),'static_internal_coordinates':str(T),'metric_v':str(rho),
        'symbols':'a=port average,b=port slope,c=internal symmetric rate,gamma=circulation,d=field square-root weight,tau=tick duration',
        'seconds':time.monotonic()-START}
(OUT/'SYMBOLIC_FAMILY.json').write_text(json.dumps(result,indent=2)+'\n')
