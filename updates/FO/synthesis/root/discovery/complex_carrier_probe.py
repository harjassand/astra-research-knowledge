"""Exact six-variable gauge algebra and sampled test of complex-amplitude extension."""
from pathlib import Path
import json
import sympy as S
import numpy as np
from scipy.optimize import differential_evolution
r,s,p,q,t,h=S.symbols('r s p q t h',real=True)
v=(r,s,p,q,t,h)
def mul(a,b):
 c={}
 for k,x in a.items():
  for j,y in b.items():c[k+j]=S.expand(c.get(k+j,0)+x*y)
 return c
def conj(a):return {-k:S.conjugate(x) for k,x in a.items()}
def add(a,b):
 c=a.copy()
 for k,x in b.items():c[k]=S.expand(c.get(k,0)+x)
 return c
def scale(a,k):return {j:S.expand(k*x) for j,x in a.items()}
def mean(a):return S.expand(a.get(0,0))
x={1:p+S.I*t,-1:q+S.I*h};y={1:S.I*r,-1:-S.I*s}
u=mul(x,conj(x));vv=mul(y,conj(y));xy=mul(conj(x),y)
j=scale(add(xy,scale(conj(xy),-1)),1/(2*S.I))
E=add(add(u,vv),scale(j,-2))
L=mean(add(add(scale(mul(E,E),3),scale(mul(u,u),S.Rational(35,24))),add(mul(j,j),scale(mul(j,u),-S.Rational(5,2)))))
N=mean(mul(add(u,vv),add(u,vv)))
P=-S.Rational(16,3)*r**4+S.Rational(25,4)*s**4-S.Rational(11,6)*r*r*s*s
margin=S.expand(L-S.diff(P,r)*p-S.diff(P,s)*q-N/2)
fun=S.lambdify(v,margin,'numpy')
def obj(a):
 th,p0,q0,t0,h0=a
 return float(fun(np.cos(th),np.sin(th),p0,q0,t0,h0))
res=differential_evolution(obj,[(0,np.pi/2)]+[(-8,8)]*4,seed=20261015,popsize=20,maxiter=500,tol=1e-10)
root=Path(__file__).resolve().parent
(root/'COMPLEX_PROBE.json').write_text(json.dumps(dict(scope='Exact gauge polynomial and bounded numerical countertest,not positivity proof',L=str(L),N=str(N),margin=str(margin),minimum_found=float(res.fun),candidate=res.x.tolist(),seed=20261015),indent=2)+'\n')
print('minimum',res.fun,'at',res.x,flush=True)
